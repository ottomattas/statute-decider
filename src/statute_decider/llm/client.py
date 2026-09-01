"""The LLM client: structured calls, retries, budget, parallel fan-out.

One model or many: callers resolve model ids through the registry (``all`` is
explicit, never a silent default) and choose ``--execution
{parallel,sequential}`` — required flags, no defaults.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from statute_decider.llm.base import LLMResult
from statute_decider.llm.budget import BudgetExceeded, BudgetGuard
from statute_decider.llm.providers import get_adapter
from statute_decider.llm.registry import ModelRegistry, ModelSpec

T = TypeVar("T", bound=BaseModel)
log = logging.getLogger(__name__)

DEFAULT_PROVIDER_CONCURRENCY = 4


@dataclass
class LLMCall:
    """One structured completion request plus ledger metadata."""

    model_id: str
    system: str
    user: str
    response_model: type[BaseModel]
    temperature: float = 0.0
    max_output_tokens: int = 8192
    meta: dict[str, Any] = field(default_factory=dict)


class LLMClient:
    def __init__(
        self,
        registry: ModelRegistry,
        budget: BudgetGuard | None = None,
        *,
        max_retries: int = 2,
        retry_backoff_s: float = 5.0,
        provider_concurrency: int = DEFAULT_PROVIDER_CONCURRENCY,
        transcript_path: Path | str | None = None,
    ) -> None:
        self.registry = registry
        self.budget = budget
        self.max_retries = max_retries
        self.retry_backoff_s = retry_backoff_s
        self.provider_concurrency = provider_concurrency
        self.transcript_path = Path(transcript_path) if transcript_path else None
        self._transcript_lock = threading.Lock()
        self._semaphores: dict[str, asyncio.Semaphore] = {}

    def _record_transcript(
        self,
        call: LLMCall,
        spec: ModelSpec,
        *,
        attempt: int,
        raw_text: str | None,
        error: str | None,
        latency_ms: int | None,
    ) -> None:
        """Append the full request/response payload of one provider call.

        This is the audit trail for "exactly what was sent where": the rendered
        system and user messages as transmitted, and the raw model output before
        any parsing or filtering.
        """
        if self.transcript_path is None:
            return
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "provider": spec.provider,
            "model": spec.model_id,
            "api_model": spec.api_model,
            "attempt": attempt,
            "meta": call.meta,
            "response_schema": call.response_model.__name__,
            "system": call.system,
            "user": call.user,
            "raw_response": raw_text,
            "error": error,
            "latency_ms": latency_ms,
        }
        line = json.dumps(entry, ensure_ascii=False, default=str)
        with self._transcript_lock, self.transcript_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    # --- synchronous single call (used inside one pipeline pass) ---

    def complete(self, call: LLMCall) -> LLMResult:
        spec = self.registry.spec(call.model_id)
        adapter = get_adapter(spec.provider)
        if not adapter.available():
            raise RuntimeError(f"Provider {spec.provider} unavailable (missing API key).")
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            if self.budget is not None:
                self.budget.check()
            try:
                result = adapter.complete(
                    api_model=spec.api_model,
                    system=call.system,
                    user=call.user,
                    response_model=call.response_model,
                    temperature=call.temperature,
                    max_output_tokens=call.max_output_tokens,
                )
                result.model = spec.model_id
                self._record_transcript(
                    call,
                    spec,
                    attempt=attempt + 1,
                    raw_text=result.raw_text,
                    error=None,
                    latency_ms=result.latency_ms,
                )
                if self.budget is not None:
                    self.budget.record(
                        spec, result.usage, {**call.meta, "latency_ms": result.latency_ms}
                    )
                return result
            except BudgetExceeded:
                raise
            except Exception as exc:  # noqa: BLE001 - provider errors are heterogeneous
                last_error = exc
                self._record_transcript(
                    call,
                    spec,
                    attempt=attempt + 1,
                    raw_text=None,
                    error=str(exc),
                    latency_ms=None,
                )
                if attempt < self.max_retries:
                    wait = self.retry_backoff_s * (attempt + 1)
                    log.warning(
                        "%s/%s failed (attempt %d/%d): %s — retrying in %.0fs",
                        spec.provider,
                        spec.model_id,
                        attempt + 1,
                        self.max_retries + 1,
                        exc,
                        wait,
                    )
                    time.sleep(wait)
        raise RuntimeError(
            f"{spec.provider}/{spec.model_id} failed after {self.max_retries + 1} attempts: "
            f"{last_error}"
        ) from last_error

    # --- asyncio fan-out over independent work units ---

    def _semaphore(self, provider: str) -> asyncio.Semaphore:
        if provider not in self._semaphores:
            self._semaphores[provider] = asyncio.Semaphore(self.provider_concurrency)
        return self._semaphores[provider]

    async def _run_unit(
        self, provider: str, unit: Callable[[], Any], *, sequential_lock: asyncio.Lock | None
    ) -> Any:
        if sequential_lock is not None:
            async with sequential_lock:
                return await asyncio.to_thread(unit)
        async with self._semaphore(provider):
            return await asyncio.to_thread(unit)

    def run_units(
        self,
        units: list[tuple[str, Callable[[], Any]]],
        *,
        execution: str,
    ) -> list[Any]:
        """Run (provider, thunk) work units; parallel fans out with per-provider
        semaphores, sequential preserves order one at a time. Exceptions are
        returned in place of results."""
        if execution not in {"parallel", "sequential"}:
            raise ValueError("--execution must be 'parallel' or 'sequential' (no default).")

        async def runner() -> list[Any]:
            self._semaphores = {}
            lock = asyncio.Lock() if execution == "sequential" else None
            tasks = [
                self._run_unit(provider, unit, sequential_lock=lock)
                for provider, unit in units
            ]
            return await asyncio.gather(*tasks, return_exceptions=True)

        return asyncio.run(runner())


def resolve_models(registry: ModelRegistry, requested: list[str]) -> list[ModelSpec]:
    if not requested:
        raise ValueError("--models is required: one id, a list, or explicit 'all'.")
    return registry.resolve(requested)
