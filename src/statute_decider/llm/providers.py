"""Per-vendor structured-JSON adapters.

API shapes verified 2026-08-20 in v1 and kept:
- Gemini ``google.genai``: ``models.generate_content`` + ``response_json_schema``
- OpenAI Responses: ``client.responses.create`` + ``text.format`` json_schema strict
- Anthropic Messages: ``output_config.format.type=json_schema`` (tool-call fallback)
- DeepSeek: OpenAI-compatible Chat Completions JSON mode at ``https://api.deepseek.com``

Vendor quirks that cost debugging time once, kept explicit:
- GPT-5-family and o-series reject a custom temperature on the Responses API.
- Fable/Mythos-generation Claude models use always-on adaptive thinking and
  reject ``temperature``.
- DeepSeek JSON mode requires the word "json" in the prompt; thinking is
  disabled explicitly for cheap runs.
- Every client gets a hard timeout: a dropped connection must fail the call,
  never hang the run (v1 lost ~2h to a bare SSL read).

Prompt caching (verified 2026-09-03 against vendor docs): the statute text is
the same across every scenario/repeat of a case, so it is passed as the
leading ``cache_prefix_len`` characters of the user message.
- Anthropic: explicit ``cache_control`` on a separate leading content block
  (min 1024 tokens; Haiku 4.5 needs 4096). Reads 0.1x (Fable 5.1: 0.025x),
  5-minute writes 1.25x. Reported as cache_read/cache_creation_input_tokens.
- OpenAI: automatic prefix caching (>=1024 tokens on GPT-5.6+, 2048 before);
  ``prompt_cache_key`` only steers routing. Reads 0.1x; usage reports
  ``input_tokens_details.cached_tokens``.
- Gemini 2.5+: implicit caching, no request change; ``cached_content_token_count``.
- DeepSeek: automatic disk cache; ``prompt_cache_hit_tokens`` in usage.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any, TypeVar

from pydantic import BaseModel

from statute_decider.llm.base import (
    LLMResult,
    Usage,
    call_timeout_s,
    env,
    parse_or_raise,
    schema_name,
    strict_json_schema,
)

T = TypeVar("T", bound=BaseModel)

_NO_TEMPERATURE_PREFIXES = ("gpt-5", "o1", "o3", "o4")


class GoogleAdapter:
    name = "google"

    def available(self) -> bool:
        return bool(env("GEMINI_API_KEY") or env("GOOGLE_API_KEY"))

    def complete(
        self,
        *,
        api_model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_output_tokens: int = 8192,
        cache_prefix_len: int = 0,
    ) -> LLMResult:
        del cache_prefix_len  # Gemini 2.5+ caches shared prefixes implicitly.
        from google import genai
        from google.genai import types

        api_key = env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")
        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": int(call_timeout_s() * 1000)},
        )
        config = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_json_schema=response_model.model_json_schema(),
        )
        started = time.monotonic()
        response = client.models.generate_content(model=api_model, contents=user, config=config)
        latency_ms = int((time.monotonic() - started) * 1000)
        raw_text = response.text or ""
        meta = getattr(response, "usage_metadata", None)
        usage = Usage(
            input_tokens=int(getattr(meta, "prompt_token_count", 0) or 0),
            output_tokens=int(getattr(meta, "candidates_token_count", 0) or 0),
            cached_input_tokens=int(getattr(meta, "cached_content_token_count", 0) or 0),
        )
        candidates = getattr(response, "candidates", None) or []
        finish = getattr(candidates[0], "finish_reason", None) if candidates else None
        parsed = parse_or_raise(response_model, raw_text, usage, f"finish_reason={finish}")
        return LLMResult(parsed, raw_text, usage, self.name, api_model, latency_ms)


class OpenAIAdapter:
    name = "openai"

    def available(self) -> bool:
        return bool(env("OPENAI_API_KEY"))

    def complete(
        self,
        *,
        api_model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_output_tokens: int = 8192,
        cache_prefix_len: int = 0,
    ) -> LLMResult:
        from openai import OpenAI

        client = OpenAI(api_key=env("OPENAI_API_KEY"), timeout=call_timeout_s())
        kwargs: dict[str, Any] = {
            "model": api_model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_output_tokens": max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name(response_model),
                    "strict": True,
                    "schema": strict_json_schema(response_model),
                }
            },
        }
        if not api_model.startswith(_NO_TEMPERATURE_PREFIXES):
            kwargs["temperature"] = temperature
        if cache_prefix_len > 0:
            # Same key for every call sharing this (system, statute) prefix so
            # they land on the same cache; caching itself is automatic.
            kwargs["prompt_cache_key"] = _prefix_key(system, user[:cache_prefix_len])
        started = time.monotonic()
        response = client.responses.create(**kwargs)
        latency_ms = int((time.monotonic() - started) * 1000)
        raw_text = getattr(response, "output_text", None) or ""
        usage_obj = getattr(response, "usage", None)
        details = getattr(usage_obj, "input_tokens_details", None) if usage_obj else None
        usage = Usage(
            input_tokens=int(getattr(usage_obj, "input_tokens", 0) or 0) if usage_obj else 0,
            output_tokens=int(getattr(usage_obj, "output_tokens", 0) or 0) if usage_obj else 0,
            cached_input_tokens=int(getattr(details, "cached_tokens", 0) or 0) if details else 0,
        )
        incomplete = getattr(response, "incomplete_details", None)
        detail = f"status={getattr(response, 'status', None)} incomplete={incomplete}"
        parsed = parse_or_raise(response_model, raw_text, usage, detail)
        return LLMResult(parsed, raw_text, usage, self.name, api_model, latency_ms)


class AnthropicAdapter:
    name = "anthropic"

    def available(self) -> bool:
        return bool(env("ANTHROPIC_API_KEY"))

    def complete(
        self,
        *,
        api_model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_output_tokens: int = 8192,
        cache_prefix_len: int = 0,
    ) -> LLMResult:
        import anthropic

        client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"), timeout=call_timeout_s())
        schema = strict_json_schema(response_model)
        del temperature  # SDK >= 1.3 removed sampling controls from messages.create
        content: Any = user
        if 0 < cache_prefix_len < len(user):
            # Static statute block gets the cache breakpoint; the scenario-specific
            # remainder follows as a second block. Text transmitted is unchanged.
            content = [
                {
                    "type": "text",
                    "text": user[:cache_prefix_len],
                    "cache_control": {"type": "ephemeral"},
                },
                {"type": "text", "text": user[cache_prefix_len:]},
            ]
        kwargs: dict[str, Any] = {
            "model": api_model,
            "max_tokens": max_output_tokens,
            "system": system,
            "messages": [{"role": "user", "content": content}],
        }
        started = time.monotonic()
        try:
            message = client.messages.create(
                **kwargs,
                output_config={"format": {"type": "json_schema", "schema": schema}},
            )
        except TypeError:
            # SDK build without output_config: force one tool call instead.
            message = client.messages.create(
                **kwargs,
                tools=[
                    {
                        "name": "emit_structured_json",
                        "description": "Return the result as a single JSON object.",
                        "input_schema": schema,
                    }
                ],
                tool_choice={"type": "tool", "name": "emit_structured_json"},
            )
        latency_ms = int((time.monotonic() - started) * 1000)
        raw_text = _anthropic_raw_text(message)
        usage_obj = getattr(message, "usage", None)
        usage = Usage(
            input_tokens=int(getattr(usage_obj, "input_tokens", 0) or 0) if usage_obj else 0,
            output_tokens=int(getattr(usage_obj, "output_tokens", 0) or 0) if usage_obj else 0,
            cached_input_tokens=int(getattr(usage_obj, "cache_read_input_tokens", 0) or 0)
            if usage_obj
            else 0,
            cache_write_input_tokens=int(getattr(usage_obj, "cache_creation_input_tokens", 0) or 0)
            if usage_obj
            else 0,
        )
        # Anthropic's input_tokens excludes cached/written tokens; normalize to
        # the full-prompt convention the other vendors and the ledger use.
        usage.input_tokens += usage.cached_input_tokens + usage.cache_write_input_tokens
        blocks = [getattr(b, "type", "?") for b in getattr(message, "content", None) or []]
        stop_reason = getattr(message, "stop_reason", None)
        detail = (
            f"stop_reason={stop_reason} "
            f"stop_details={getattr(message, 'stop_details', None)} "
            f"blocks={blocks} output_tokens={usage.output_tokens}"
        )
        if stop_reason == "refusal" and not blocks:
            # A classifier refusal before any output is not charged (usage is
            # reported, not billed): https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
            usage = Usage()
        parsed = parse_or_raise(response_model, raw_text, usage, detail)
        return LLMResult(parsed, raw_text, usage, self.name, api_model, latency_ms)


def _anthropic_raw_text(message: Any) -> str:
    texts: list[str] = []
    for block in getattr(message, "content", None) or []:
        btype = getattr(block, "type", None)
        if btype == "tool_use":
            return json.dumps(getattr(block, "input", None))
        if btype == "text":
            texts.append(getattr(block, "text", "") or "")
    return "".join(texts)


class DeepSeekAdapter:
    name = "deepseek"

    def available(self) -> bool:
        return bool(env("DEEPSEEK_API_KEY"))

    def complete(
        self,
        *,
        api_model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_output_tokens: int = 8192,
        cache_prefix_len: int = 0,
    ) -> LLMResult:
        del cache_prefix_len  # DeepSeek caches shared prefixes automatically.
        from openai import OpenAI

        client = OpenAI(
            api_key=env("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
            timeout=call_timeout_s(),
        )
        schema_text = json.dumps(response_model.model_json_schema())
        system_out = (
            f"{system}\n\nReturn a JSON object that matches this JSON schema:\n{schema_text}"
        )
        create_kwargs: dict[str, Any] = {
            "model": api_model,
            "messages": [
                {"role": "system", "content": system_out},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": temperature,
            "max_tokens": max_output_tokens,
            "extra_body": {"thinking": {"type": "disabled"}},
        }
        started = time.monotonic()
        try:
            response = client.chat.completions.create(**create_kwargs)
        except TypeError:
            create_kwargs.pop("extra_body", None)
            response = client.chat.completions.create(**create_kwargs)
        latency_ms = int((time.monotonic() - started) * 1000)
        choice = response.choices[0]
        raw_text = getattr(getattr(choice, "message", None), "content", None) or ""
        usage_obj = getattr(response, "usage", None)
        usage = Usage(
            input_tokens=int(getattr(usage_obj, "prompt_tokens", 0) or 0) if usage_obj else 0,
            output_tokens=int(getattr(usage_obj, "completion_tokens", 0) or 0) if usage_obj else 0,
            cached_input_tokens=int(getattr(usage_obj, "prompt_cache_hit_tokens", 0) or 0)
            if usage_obj
            else 0,
        )
        detail = f"finish_reason={getattr(choice, 'finish_reason', None)}"
        parsed = parse_or_raise(response_model, raw_text, usage, detail)
        return LLMResult(parsed, raw_text, usage, self.name, api_model, latency_ms)


def _prefix_key(system: str, prefix: str) -> str:
    return "sd-" + hashlib.sha256((system + "\x00" + prefix).encode("utf-8")).hexdigest()[:32]


ADAPTERS: dict[str, type] = {
    "google": GoogleAdapter,
    "openai": OpenAIAdapter,
    "anthropic": AnthropicAdapter,
    "deepseek": DeepSeekAdapter,
}


def get_adapter(provider: str):
    try:
        return ADAPTERS[provider]()
    except KeyError as exc:
        raise ValueError(f"Unknown provider {provider!r}. Known: {sorted(ADAPTERS)}") from exc
