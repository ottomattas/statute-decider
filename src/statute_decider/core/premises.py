"""Premise level: rules, claims, and facts — the inputs to inference over terms.

One envelope, three kinds, distinguished by epistemic type. The warrant
principle is a data property here: a claim is *asserted* and never
decision-grade for a register-evidence term; a fact is *warranted* unless its
register is trust-only, in which case it is demoted to claim-strength at
decision time.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from statute_decider.core.enums import Epistemic, RuleKind, Warrant
from statute_decider.core.provenance import Provenance
from statute_decider.core.terms import ClauseAnchor


class OutcomeDef(BaseModel):
    """One administrative outcome atom the rules may target."""

    outcome_id: str
    label: str = ""


class RulePremise(BaseModel):
    """A norm as a boolean rule over terms. *Normative.*"""

    premise_id: str
    kind: Literal["rule"] = "rule"
    epistemic: Literal[Epistemic.NORMATIVE] = Epistemic.NORMATIVE
    rule_kind: RuleKind
    label: str = ""
    when_term_ids: list[str]
    target_outcome_id: str | None = None  # allow_if_all / deny_if_all
    target_term_id: str | None = None  # set_false_if_all (rewrite)
    law_references: list[ClauseAnchor] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _target_shape(self) -> RulePremise:
        if self.rule_kind == RuleKind.SET_FALSE_IF_ALL:
            if not self.target_term_id or self.target_outcome_id:
                raise ValueError("set_false_if_all requires target_term_id only")
        else:
            if not self.target_outcome_id or self.target_term_id:
                raise ValueError(f"{self.rule_kind} requires target_outcome_id only")
        return self


class RuleSet(BaseModel):
    """Output of ``term_rule``: the rules a normative text defines."""

    node: Literal["term_rule"] = "term_rule"
    statute_id: str
    allow_outcome_id: str
    deny_outcome_id: str
    outcomes: list[OutcomeDef] = Field(default_factory=list)
    rules: list[RulePremise] = Field(default_factory=list)
    provenance: Provenance | None = None


class ClaimPremise(BaseModel):
    """An *asserted* value for one term. Fallible; never decision-grade alone."""

    premise_id: str
    kind: Literal["claim"] = "claim"
    epistemic: Literal[Epistemic.ASSERTED] = Epistemic.ASSERTED
    term_id: str
    value: bool
    span: str = ""  # utterance span the assertion rests on
    notes: str = ""


class ClaimSet(BaseModel):
    """Output of ``term_claim`` for one scenario."""

    node: Literal["term_claim"] = "term_claim"
    scenario_id: str
    claims: list[ClaimPremise] = Field(default_factory=list)
    provenance: Provenance | None = None

    def by_term(self) -> dict[str, ClaimPremise]:
        return {claim.term_id: claim for claim in self.claims}


class FactPremise(BaseModel):
    """A *warranted* value for one term. Decision-grade — 'fact' means
    institutionally warranted, not metaphysically true."""

    premise_id: str
    kind: Literal["fact"] = "fact"
    epistemic: Literal[Epistemic.WARRANTED] = Epistemic.WARRANTED
    term_id: str
    value: bool
    register_id: str = ""
    record_id: str = ""
    field: str = ""
    warrant: Warrant = Warrant.AUTHORITATIVE  # trust_only facts demote to claim-strength
    notes: str = ""


class FactSet(BaseModel):
    """Output of ``term_fact`` for one scenario.

    ``unavailable_registers`` and ``conflicts`` carry lookup outcomes that
    produce no fact but matter to the decision (no_register / conflict
    missing-term reasons).
    """

    node: Literal["term_fact"] = "term_fact"
    scenario_id: str
    facts: list[FactPremise] = Field(default_factory=list)
    unavailable_registers: list[str] = Field(default_factory=list)
    unavailable_terms: list[str] = Field(default_factory=list)  # mapped terms those registers cover
    conflicts: list[str] = Field(default_factory=list)  # term_ids with conflicting values
    # Terms an available register in this scenario's registry state is declared
    # to answer (via record_term mappings), whether or not a value was found.
    # The warrant principle needs this: a claim on a covered-but-silent term is
    # unverified support, while a claim on an uncovered term has nothing to be
    # checked against and stays decision-grade.
    covered_terms: list[str] = Field(default_factory=list)
    provenance: Provenance | None = None

    def by_term(self) -> dict[str, FactPremise]:
        return {fact.term_id: fact for fact in self.facts}
