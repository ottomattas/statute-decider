"""Outcome level: the decision, plus the missing-term set."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from statute_decider.core.enums import MissingReason, OutcomeState, ScoredOutcome
from statute_decider.core.provenance import Provenance


class MissingTerm(BaseModel):
    """A term that could still change the outcome and has no decision-grade value."""

    term_id: str
    reason: MissingReason = MissingReason.NO_VALUE


class FiredRule(BaseModel):
    premise_id: str
    effect: str = ""  # target outcome id / "not <term>" for rewrites


class PremiseOutcome(BaseModel):
    """Output of ``premise_outcome``: the decision produced from the premise set."""

    node: Literal["premise_outcome"] = "premise_outcome"
    scenario_id: str
    state: OutcomeState
    scored_as: ScoredOutcome
    missing_terms: list[MissingTerm] = Field(default_factory=list)
    fired_rules: list[FiredRule] = Field(default_factory=list)
    valuation: dict[str, bool] = Field(default_factory=dict)  # term values the decision used
    free_missing: list[str] = Field(default_factory=list)  # non-catalog missing items (llm methods)
    # An LLM decision reasons before it decides (Ruling J): the ordered steps it
    # wrote, and its justification in ``note``. A solver leaves ``steps`` empty;
    # its inference record is ``fired_rules`` + ``valuation``.
    steps: list[str] = Field(default_factory=list)
    note: str = ""
    provenance: Provenance | None = None

    def missing_term_ids(self) -> set[str]:
        return {item.term_id for item in self.missing_terms}
