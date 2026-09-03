"""Provider-agnostic structured-completion interface."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class Usage:
    """Token counts as the provider reports them.

    ``input_tokens`` is the full prompt (cache hits included, as every vendor
    reports it); ``cached_input_tokens`` is the part served from a prompt cache
    at the cached rate; ``cache_write_input_tokens`` is the part written to a
    cache at the write surcharge (Anthropic reports it; OpenAI/Gemini/DeepSeek
    fold writes into the normal input price).
    """

    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0


@dataclass
class LLMResult:
    parsed: Any  # pydantic model instance
    raw_text: str
    usage: Usage = field(default_factory=Usage)
    provider: str = ""
    model: str = ""
    latency_ms: int = 0


class ProviderAdapter(Protocol):
    name: str

    def available(self) -> bool: ...

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
    ) -> LLMResult: ...


def load_dotenv(path: Path | str = ".env") -> None:
    """Fill os.environ from a .env file without overriding existing values."""
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def call_timeout_s() -> float:
    """Hard per-call timeout: no provider call may hang a run indefinitely."""
    raw = env("SD_LLM_TIMEOUT_S", "120") or "120"
    try:
        return float(raw)
    except ValueError:
        return 120.0


def parse_model_json[M: BaseModel](response_model: type[M], raw_text: str) -> M:
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


def strict_json_schema(response_model: type[BaseModel]) -> dict[str, Any]:
    """Pydantic JSON schema with OpenAI/Anthropic strict-object constraints."""
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
            node[defs_key] = {k: _strictify(v) for k, v in node[defs_key].items()}
    for alt_key in ("anyOf", "oneOf", "allOf"):
        if alt_key in node:
            node[alt_key] = [_strictify(v) for v in node[alt_key]]
    if "prefixItems" in node:
        node["prefixItems"] = [_strictify(v) for v in node["prefixItems"]]
    return node


def schema_name(response_model: type[BaseModel]) -> str:
    raw = "".join(ch if ch.isalnum() else "_" for ch in response_model.__name__)
    return (raw or "Result")[:64]
