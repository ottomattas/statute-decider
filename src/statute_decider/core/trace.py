"""Trace level: the justification, separately measurable and swappable.

Ruling J (2026-09-06, ADR 0007): a row's justification is a **list of
entries**, each saying where it came from —

* ``llm_inline`` — the reasoning steps and justification the deciding model
  wrote in the *same* structured call that produced the outcome (the llm-only
  baseline is one call per scenario; ``outcome_trace: passthrough`` stores it);
* ``solver_trace`` — the deterministic rendering of a solver's inference record
  (``outcome_trace: render``);
* ``llm_post`` — a post-hoc justification by the optional ``justify`` node
  (``outcome_trace: llm``), which *appends* to whatever the row already has and
  never overwrites.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from statute_decider.core.provenance import Provenance

JustificationSource = Literal["llm_inline", "solver_trace", "llm_post"]


class JustificationEntry(BaseModel):
    source: JustificationSource
    steps: list[str] = Field(default_factory=list)
    text: str = ""
    model: str | None = None  # llm sources
    prompt_id: str | None = None
    prompt_hash: str | None = None


class OutcomeTrace(BaseModel):
    """Output of ``outcome_trace``: the row's justification entries, in the order produced."""

    node: Literal["outcome_trace"] = "outcome_trace"
    scenario_id: str
    justification: list[JustificationEntry] = Field(default_factory=list)
    provenance: Provenance | None = None

    def appended(self, entry: JustificationEntry, provenance: Provenance | None = None) -> OutcomeTrace:
        """A new trace with ``entry`` added after the existing ones (never overwrites)."""
        return OutcomeTrace(
            scenario_id=self.scenario_id,
            justification=[*self.justification, entry],
            provenance=provenance or self.provenance,
        )

    @property
    def primary(self) -> JustificationEntry | None:
        return self.justification[0] if self.justification else None
