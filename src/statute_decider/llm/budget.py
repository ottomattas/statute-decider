"""Budget guard + append-only cost ledger (EUR)."""

from __future__ import annotations

import json
import threading
from pathlib import Path

from statute_decider.core.provenance import utc_now
from statute_decider.llm.base import Usage
from statute_decider.llm.registry import ModelSpec


class BudgetExceeded(RuntimeError):
    pass


class BudgetGuard:
    """Thread-safe spend tracker; every recorded call appends one ledger row."""

    def __init__(self, cap_eur: float, ledger_path: Path | str, usd_to_eur: float = 0.92) -> None:
        self.cap_eur = cap_eur
        self.ledger_path = Path(ledger_path)
        self.usd_to_eur = usd_to_eur
        self.spent_eur = 0.0
        self._lock = threading.Lock()

    def check(self) -> None:
        with self._lock:
            if self.spent_eur >= self.cap_eur:
                raise BudgetExceeded(
                    f"Budget cap EUR {self.cap_eur:.2f} reached (spent {self.spent_eur:.4f})."
                )

    def record(self, spec: ModelSpec, usage: Usage, meta: dict | None = None) -> float:
        eur = spec.eur(
            usage.input_tokens,
            usage.output_tokens,
            self.usd_to_eur,
            cached_input_tokens=usage.cached_input_tokens,
            cache_write_input_tokens=usage.cache_write_input_tokens,
        )
        row = {
            "timestamp": utc_now(),
            "provider": spec.provider,
            "model": spec.model_id,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cached_input_tokens": usage.cached_input_tokens,
            "cache_write_input_tokens": usage.cache_write_input_tokens,
            "eur": round(eur, 6),
            **(meta or {}),
        }
        with self._lock:
            self.spent_eur += eur
            self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        return eur
