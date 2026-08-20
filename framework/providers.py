"""Structured-JSON LLM providers for overnight experiments.

Live adapters (Gemini, OpenAI Responses, Anthropic Messages, DeepSeek) return
parsed Pydantic models plus token usage. Ollama is a stub. Missing API keys
make ``available()`` false; ``complete()`` then returns a skipped result
instead of raising.

Docs verified 2026-08-20:
- Gemini ``google.genai``: ``models.generate_content`` + ``response_json_schema``
- OpenAI Responses: ``client.responses.create`` + ``text.format`` json_schema strict
- Anthropic Messages: ``output_config.format.type=json_schema``
  (https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- DeepSeek Chat Completions JSON mode at ``https://api.deepseek.com``
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

log = logging.getLogger(__name__)

_PROVIDER_NAMES = ("gemini", "openai", "anthropic", "deepseek", "ollama")

# GPT-5 family rejects a custom temperature on the Responses API.
_NO_TEMPERATURE_PREFIXES = ("gpt-5", "o1", "o3", "o4")


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0


@dataclass
class ProviderResult:
    parsed: Any  # pydantic model instance, or None when skipped
    raw_text: str
    usage: Usage
    model: str
    provider: str
    skipped: bool = False
    skip_reason: str = ""


class Provider(Protocol):
    name: str

    def available(self) -> bool: ...

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult: ...


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _skipped(provider: str, model: str, reason: str) -> ProviderResult:
    log.warning("Skipping provider %s (%s): %s", provider, model, reason)
    return ProviderResult(
        parsed=None,
        raw_text="",
        usage=Usage(),
        model=model,
        provider=provider,
        skipped=True,
        skip_reason=reason,
    )


def _parse_model_json(response_model: type[T], raw_text: str) -> T:
    text = (raw_text or "").strip()
    if not text:
        raise RuntimeError("Empty model response.")
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return response_model.model_validate(json.loads(text))


def _strict_json_schema(response_model: type[BaseModel]) -> dict[str, Any]:
    """Pydantic JSON Schema with OpenAI/Anthropic strict-object constraints."""
    return _strictify(response_model.model_json_schema())


def _strictify(node: Any) -> Any:
    if not isinstance(node, dict):
        return node
    node = dict(node)
    for drop in ("title", "default", "examples"):
        node.pop(drop, None)
    if "properties" in node:
        node["type"] = node.get("type") or "object"
        node["additionalProperties"] = False
        props = {key: _strictify(value) for key, value in node["properties"].items()}
        node["properties"] = props
        node["required"] = list(props.keys())
    if "items" in node:
        node["items"] = _strictify(node["items"])
    for defs_key in ("$defs", "defs"):
        if defs_key in node:
            node[defs_key] = {key: _strictify(value) for key, value in node[defs_key].items()}
    for alt_key in ("anyOf", "oneOf", "allOf"):
        if alt_key in node:
            node[alt_key] = [_strictify(value) for value in node[alt_key]]
    if "prefixItems" in node:
        node["prefixItems"] = [_strictify(value) for value in node["prefixItems"]]
    return node


def _schema_name(response_model: type[BaseModel]) -> str:
    raw = "".join(ch if ch.isalnum() else "_" for ch in response_model.__name__)
    return (raw or "Result")[:64]


def _gemini_client(api_key: str):
    from google import genai

    return genai.Client(api_key=api_key)


def _openai_client(api_key: str):
    from openai import OpenAI

    return OpenAI(api_key=api_key)


def _anthropic_client(api_key: str):
    import anthropic

    return anthropic.Anthropic(api_key=api_key)


def _deepseek_client(api_key: str):
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


class GeminiProvider:
    name = "gemini"

    def __init__(self) -> None:
        self.model = _env("FRAMEWORK_GEMINI_MODEL", "gemini-2.5-flash") or "gemini-2.5-flash"

    def available(self) -> bool:
        return bool(_env("GEMINI_API_KEY") or _env("GOOGLE_API_KEY"))

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult:
        api_key = _env("GEMINI_API_KEY") or _env("GOOGLE_API_KEY")
        if not api_key:
            return _skipped(self.name, self.model, "missing GEMINI_API_KEY/GOOGLE_API_KEY")
        from google.genai import types

        client = _gemini_client(api_key)
        config = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            response_mime_type="application/json",
            response_json_schema=response_model.model_json_schema(),
        )
        response = client.models.generate_content(
            model=self.model,
            contents=user,
            config=config,
        )
        raw_text = response.text or ""
        parsed = _parse_model_json(response_model, raw_text)
        meta = getattr(response, "usage_metadata", None)
        usage = Usage()
        if meta is not None:
            usage = Usage(
                input_tokens=int(getattr(meta, "prompt_token_count", 0) or 0),
                output_tokens=int(getattr(meta, "candidates_token_count", 0) or 0),
                cached_input_tokens=int(getattr(meta, "cached_content_token_count", 0) or 0),
            )
        return ProviderResult(
            parsed=parsed,
            raw_text=raw_text,
            usage=usage,
            model=self.model,
            provider=self.name,
        )


class OpenAIProvider:
    name = "openai"

    def __init__(self) -> None:
        self.model = _env("FRAMEWORK_OPENAI_MODEL", "gpt-5-mini") or "gpt-5-mini"

    def available(self) -> bool:
        return bool(_env("OPENAI_API_KEY"))

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult:
        api_key = _env("OPENAI_API_KEY")
        if not api_key:
            return _skipped(self.name, self.model, "missing OPENAI_API_KEY")
        client = _openai_client(api_key)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": _schema_name(response_model),
                    "strict": True,
                    "schema": _strict_json_schema(response_model),
                }
            },
        }
        if not any(self.model.startswith(prefix) for prefix in _NO_TEMPERATURE_PREFIXES):
            kwargs["temperature"] = temperature
        response = client.responses.create(**kwargs)
        raw_text = getattr(response, "output_text", None) or ""
        parsed = _parse_model_json(response_model, raw_text)
        usage_obj = getattr(response, "usage", None)
        details = getattr(usage_obj, "input_tokens_details", None) if usage_obj else None
        usage = Usage(
            input_tokens=int(getattr(usage_obj, "input_tokens", 0) or 0) if usage_obj else 0,
            output_tokens=int(getattr(usage_obj, "output_tokens", 0) or 0) if usage_obj else 0,
            cached_input_tokens=int(getattr(details, "cached_tokens", 0) or 0) if details else 0,
        )
        return ProviderResult(
            parsed=parsed,
            raw_text=raw_text,
            usage=usage,
            model=self.model,
            provider=self.name,
        )


class AnthropicProvider:
    name = "anthropic"

    def __init__(self) -> None:
        self.model = (
            _env("FRAMEWORK_ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
            or "claude-haiku-4-5-20251001"
        )

    def available(self) -> bool:
        return bool(_env("ANTHROPIC_API_KEY"))

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult:
        api_key = _env("ANTHROPIC_API_KEY")
        if not api_key:
            return _skipped(self.name, self.model, "missing ANTHROPIC_API_KEY")
        client = _anthropic_client(api_key)
        schema = _strict_json_schema(response_model)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8192,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        try:
            message = client.messages.create(
                **kwargs,
                output_config={"format": {"type": "json_schema", "schema": schema}},
            )
        except TypeError:
            # Fallback: this anthropic SDK build does not accept output_config.
            # Force a single tool call and parse tool_use.input as the JSON object.
            # Live shape: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
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
        raw_text = _anthropic_raw_text(message)
        parsed = _parse_model_json(response_model, raw_text)
        usage_obj = getattr(message, "usage", None)
        usage = Usage(
            input_tokens=int(getattr(usage_obj, "input_tokens", 0) or 0) if usage_obj else 0,
            output_tokens=int(getattr(usage_obj, "output_tokens", 0) or 0) if usage_obj else 0,
            cached_input_tokens=int(
                getattr(usage_obj, "cache_read_input_tokens", 0) or 0
            )
            if usage_obj
            else 0,
        )
        return ProviderResult(
            parsed=parsed,
            raw_text=raw_text,
            usage=usage,
            model=self.model,
            provider=self.name,
        )


def _anthropic_raw_text(message: Any) -> str:
    blocks = getattr(message, "content", None) or []
    texts: list[str] = []
    for block in blocks:
        btype = getattr(block, "type", None)
        if btype == "tool_use":
            payload = getattr(block, "input", None)
            return json.dumps(payload)
        if btype == "text":
            texts.append(getattr(block, "text", "") or "")
    return "".join(texts)


class DeepSeekProvider:
    name = "deepseek"

    def __init__(self) -> None:
        self.model = _env("FRAMEWORK_DEEPSEEK_MODEL", "deepseek-v4-flash") or "deepseek-v4-flash"

    def available(self) -> bool:
        return bool(_env("DEEPSEEK_API_KEY"))

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult:
        api_key = _env("DEEPSEEK_API_KEY")
        if not api_key:
            return _skipped(self.name, self.model, "missing DEEPSEEK_API_KEY")
        # JSON mode requires the word "json" in the prompt
        # (https://api-docs.deepseek.com/guides/json_mode).
        schema_text = json.dumps(response_model.model_json_schema())
        system_out = (
            f"{system}\n\n"
            "Return a JSON object that matches this JSON schema:\n"
            f"{schema_text}"
        )
        client = _deepseek_client(api_key)
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_out},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": temperature,
            "max_tokens": 8192,
            # Thinking is on by default; disable it for cheap smoke.
            "extra_body": {"thinking": {"type": "disabled"}},
        }
        try:
            response = client.chat.completions.create(**create_kwargs)
        except TypeError:
            create_kwargs.pop("extra_body", None)
            response = client.chat.completions.create(**create_kwargs)
        choice = response.choices[0]
        raw_text = getattr(getattr(choice, "message", None), "content", None) or ""
        parsed = _parse_model_json(response_model, raw_text)
        usage_obj = getattr(response, "usage", None)
        input_tokens = 0
        output_tokens = 0
        if usage_obj is not None:
            input_tokens = int(
                getattr(usage_obj, "prompt_tokens", None)
                or getattr(usage_obj, "input_tokens", 0)
                or 0
            )
            output_tokens = int(
                getattr(usage_obj, "completion_tokens", None)
                or getattr(usage_obj, "output_tokens", 0)
                or 0
            )
        return ProviderResult(
            parsed=parsed,
            raw_text=raw_text,
            usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens),
            model=self.model,
            provider=self.name,
        )


class OllamaProvider:
    """Local Ollama adapter. Interface only; complete() never calls a host."""

    name = "ollama"

    def __init__(self) -> None:
        self.model = _env("FRAMEWORK_OLLAMA_MODEL", "ollama") or "ollama"
        self.host = _env("OLLAMA_HOST", "http://127.0.0.1:11434") or "http://127.0.0.1:11434"

    def available(self) -> bool:
        return False

    def complete(
        self,
        *,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
    ) -> ProviderResult:
        del system, user, response_model, temperature
        return _skipped(self.name, self.model, "ollama stub")


_FACTORIES: dict[str, type] = {
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "deepseek": DeepSeekProvider,
    "ollama": OllamaProvider,
}


def get_provider(name: str) -> Provider:
    key = name.strip().lower()
    try:
        factory = _FACTORIES[key]
    except KeyError as exc:
        known = ", ".join(_PROVIDER_NAMES)
        raise ValueError(f"Unknown provider {name!r}. Known: {known}") from exc
    return factory()


def list_available_providers() -> list[str]:
    return [name for name in _PROVIDER_NAMES if get_provider(name).available()]
