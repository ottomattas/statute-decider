"""Trace level: the justification, separately measurable and swappable."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from statute_decider.core.provenance import Provenance


class TraceStep(BaseModel):
    step: int
    message: str
    premise_ids: list[str] = Field(default_factory=list)


class OutcomeTrace(BaseModel):
    """Output of ``outcome_trace``: ordered inference steps + rendered justification."""

    node: Literal["outcome_trace"] = "outcome_trace"
    scenario_id: str
    steps: list[TraceStep] = Field(default_factory=list)
    justification: str = ""
    provenance: Provenance | None = None
