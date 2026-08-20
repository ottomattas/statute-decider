"""Hard EUR budget guard for overnight smoke runs."""

from __future__ import annotations

import os
from pathlib import Path

# Overnight cap is EUR. This is a fixed conversion, not a live FX quote.
USD_TO_EUR = 0.92


class BudgetExceeded(RuntimeError):
    """Raised when a call would (or just did) exceed FRAMEWORK_BUDGET_EUR."""


def usd_to_eur(usd: float) -> float:
    return round(float(usd) * USD_TO_EUR, 6)


def default_cap_eur() -> float:
    raw = os.environ.get("FRAMEWORK_BUDGET_EUR", "10").strip() or "10"
    return float(raw)


class BudgetGuard:
    """Halt spend at ``cap_eur``. Never continue silently past the cap.

    Preferred loop: ``check_or_raise(worst_case_eur)`` before a call, then
    ``record_usd`` after. ``record_usd`` also raises if cumulative spend is
    already over the cap so a runner cannot start the next call.
    """

    def __init__(self, cap_eur: float | None = None, spent_eur: float = 0.0) -> None:
        self.cap_eur = default_cap_eur() if cap_eur is None else float(cap_eur)
        if self.cap_eur < 0:
            raise ValueError("cap_eur must be >= 0")
        self.spent_eur = float(spent_eur)
        if self.spent_eur < 0:
            raise ValueError("spent_eur must be >= 0")

    def remaining(self) -> float:
        return round(self.cap_eur - self.spent_eur, 6)

    def check_or_raise(self, estimated_eur: float = 0.0) -> None:
        """Refuse the next call if remaining is 0 or below the estimate."""
        if estimated_eur < 0:
            raise ValueError("estimated_eur must be >= 0")
        remaining = self.remaining()
        if remaining <= 0 or estimated_eur > remaining:
            raise BudgetExceeded(
                f"Budget cap EUR {self.cap_eur:.4f} exhausted "
                f"(spent EUR {self.spent_eur:.4f}, remaining EUR {remaining:.4f}, "
                f"estimated next EUR {estimated_eur:.4f})."
            )

    def record_usd(self, usd: float) -> None:
        """Add a completed call's USD cost. Raises if cumulative now exceeds the cap."""
        self.spent_eur = round(self.spent_eur + usd_to_eur(usd), 6)
        if self.spent_eur > self.cap_eur:
            raise BudgetExceeded(
                f"Budget cap EUR {self.cap_eur:.4f} exceeded after call "
                f"(spent EUR {self.spent_eur:.4f})."
            )

    def ingest_ledger(self, path: Path | None = None) -> None:
        """Add prior JSONL spend so a restarted overnight run cannot overrun."""
        from .ledger import iter_ledger

        for row in iter_ledger(path):
            self.spent_eur = round(self.spent_eur + float(row.get("eur") or 0), 6)
        if self.spent_eur > self.cap_eur:
            raise BudgetExceeded(
                f"Budget cap EUR {self.cap_eur:.4f} already exceeded by ledger "
                f"(spent EUR {self.spent_eur:.4f})."
            )
