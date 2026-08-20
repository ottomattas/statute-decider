"""Backend-agnostic uncertainty routing for the U1..U12 taxonomy (ART-64).

Each of the twelve uncertainty kinds is mapped here to a first-class
``(SolverOutcome, BlockReasonCode)`` pair plus a short description. The
helpers ``classify_claim_uncertainty`` and ``classify_rule_uncertainty``
decide, given the artifact-level flags and (for U3/U7) the recorded DB
lookup events, which U-code applies to an unresolved claim or to a blocked
rule.

The routing table is complete (all twelve entries are present) even though
the reasoner only routes a pragmatic subset in Wave 2; unit tests in
``tests/test_uncertainty_routing.py`` exercise each code. The reasoner
backend ``reasoner_z3`` consumes these helpers before falling back to the
legacy NEED_DB_INFO / NEED_USER_INFO paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from schemas import (
    BlockReasonCode,
    ClaimSource,
    DomainClaim,
    DomainRule,
    IntentClaim,
    LookupEvent,
    RuleStatus,
    RuleTraceRow,
    SolverOutcome,
)


@dataclass(frozen=True)
class UncertaintyRouting:
    """One entry in the U1..U12 routing table."""

    code: str
    outcome: SolverOutcome
    reason_code: BlockReasonCode
    description: str


ROUTING_TABLE: dict[str, UncertaintyRouting] = {
    "U1": UncertaintyRouting(
        code="U1",
        outcome=SolverOutcome.UNDETERMINED_INTERPRETATION,
        reason_code=BlockReasonCode.STATUTE_UNDERSPECIFIED,
        description=(
            "Statute under-specification: a normative term in the law has no "
            "precise definition (e.g. 'journalist')."
        ),
    ),
    "U2": UncertaintyRouting(
        code="U2",
        outcome=SolverOutcome.UNDETERMINED_INTERPRETATION,
        reason_code=BlockReasonCode.INTERPRETATION_AMBIGUOUS,
        description=(
            "Interpretation ambiguity: multiple admissible readings of the "
            "same clause."
        ),
    ),
    "U3": UncertaintyRouting(
        code="U3",
        outcome=SolverOutcome.UNVERIFIABLE_CLAIM,
        reason_code=BlockReasonCode.NO_REGISTER,
        description=(
            "Missing data source / no register: the authoritative register "
            "does not exist or is inaccessible."
        ),
    ),
    "U4": UncertaintyRouting(
        code="U4",
        outcome=SolverOutcome.UNDETERMINED_INTERPRETATION,
        reason_code=BlockReasonCode.PROCESS_INDETERMINATE,
        description=(
            "Process indeterminacy: the applicable procedure is not fully "
            "specified in statute."
        ),
    ),
    "U5": UncertaintyRouting(
        code="U5",
        outcome=SolverOutcome.NEED_DB_INFO,
        reason_code=BlockReasonCode.NEEDS_DB_INFO,
        description=(
            "Needs DB info: a known DB source could answer but has not been "
            "consulted yet."
        ),
    ),
    "U6": UncertaintyRouting(
        code="U6",
        outcome=SolverOutcome.UNVERIFIABLE_CLAIM,
        reason_code=BlockReasonCode.SUBJECTIVE_PARTY,
        description=(
            "Subjective / party-biased claim: applicant self-declaration "
            "without independent verification."
        ),
    ),
    "U7": UncertaintyRouting(
        code="U7",
        outcome=SolverOutcome.UNVERIFIABLE_CLAIM,
        reason_code=BlockReasonCode.TRUST_ONLY,
        description=(
            "Trust-only claim: a fact that is by construction unverifiable; "
            "we must accept the applicant's word."
        ),
    ),
    "U8": UncertaintyRouting(
        code="U8",
        outcome=SolverOutcome.NEED_USER_INFO,
        reason_code=BlockReasonCode.NEEDS_USER_INFO,
        description=(
            "Needs user info: the user has not yet provided an answer."
        ),
    ),
    "U9": UncertaintyRouting(
        code="U9",
        outcome=SolverOutcome.NEED_USER_INFO,
        reason_code=BlockReasonCode.CONTEXT_DEPENDENT,
        description=(
            "Context-dependent applicability: rule applicability depends on "
            "context not yet elicited."
        ),
    ),
    "U10": UncertaintyRouting(
        code="U10",
        outcome=SolverOutcome.NEED_EXPERT_JUDGMENT,
        reason_code=BlockReasonCode.EXPERT_JUDGMENT_REQUIRED,
        description=(
            "Expert judgment required: resolution requires specialist "
            "evaluation (medical, legal, etc.)."
        ),
    ),
    "U11": UncertaintyRouting(
        code="U11",
        outcome=SolverOutcome.UNDETERMINED_INTERPRETATION,
        reason_code=BlockReasonCode.GLOSSARY_LOW_CONFIDENCE,
        description=(
            "Glossary / lexicon confidence: the term-level confidence from "
            "the extraction step is too low."
        ),
    ),
    "U12": UncertaintyRouting(
        code="U12",
        outcome=SolverOutcome.UNDETERMINED_INTERPRETATION,
        reason_code=BlockReasonCode.MODEL_DRIFT,
        description=(
            "Model drift / non-replicability: LLM-based extraction is "
            "non-deterministic across runs."
        ),
    ),
}


_REASON_CODE_TO_UCODE: dict[BlockReasonCode, str] = {
    routing.reason_code: code for code, routing in ROUTING_TABLE.items()
}


def routing_for_reason_code(reason_code: BlockReasonCode | None) -> UncertaintyRouting | None:
    """Invert the routing table to go from a ``BlockReasonCode`` to a U-code."""
    if reason_code is None:
        return None
    code = _REASON_CODE_TO_UCODE.get(reason_code)
    if code is None:
        return None
    return ROUTING_TABLE[code]


def _has_event_with_note(
    lookup_events: Iterable[LookupEvent],
    claim_id: str,
    note: str,
) -> bool:
    """Return True if any lookup event for ``claim_id`` carries ``note``."""
    for event in lookup_events:
        if event.note != note:
            continue
        if claim_id in event.requested_claim_ids or claim_id in event.returned_values:
            return True
    return False


def classify_claim_uncertainty(
    domain_claim: DomainClaim,
    intent_claim: IntentClaim | None = None,
    lookup_events: Iterable[LookupEvent] | None = None,
) -> UncertaintyRouting | None:
    """Return the routing for an unresolved claim, or ``None`` for the legacy path.

    Priority order (first match wins): ``U1``, ``U10``, ``U3``, ``U7``,
    ``U6``, ``U12``, ``U11``. ``U5`` (NEED_DB_INFO) and ``U8``
    (NEED_USER_INFO) remain the default legacy paths and are therefore
    returned as ``None`` so the caller keeps its existing behaviour.
    """
    lookup_events = list(lookup_events or [])

    if domain_claim.source_type == ClaimSource.STATUTE_OPEN:
        return ROUTING_TABLE["U1"]
    if domain_claim.source_type == ClaimSource.EXPERT:
        return ROUTING_TABLE["U10"]

    if _has_event_with_note(lookup_events, domain_claim.claim_id, "source_unavailable"):
        return ROUTING_TABLE["U3"]
    if _has_event_with_note(lookup_events, domain_claim.claim_id, "trust_only"):
        return ROUTING_TABLE["U7"]

    if intent_claim is not None:
        if intent_claim.subjective_party:
            return ROUTING_TABLE["U6"]
        if intent_claim.model_drift:
            return ROUTING_TABLE["U12"]
        if intent_claim.glossary_low_confidence:
            return ROUTING_TABLE["U11"]

    return None


def classify_rule_uncertainty(
    rule: DomainRule,
    rule_trace_row: RuleTraceRow | None = None,
) -> UncertaintyRouting | None:
    """Return the routing for a rule-level uncertainty (U2, U4, U9).

    A rule-level routing is only emitted when the rule is not firing
    (``blocked`` or ``needs_info``). Firing rules by definition have no
    uncertainty attached.
    """
    if rule_trace_row is not None and rule_trace_row.status == RuleStatus.FIRES:
        return None

    if rule.process_indeterminate:
        return ROUTING_TABLE["U4"]
    if rule.interpretation_ambiguous:
        return ROUTING_TABLE["U2"]
    if rule.context_dependent:
        return ROUTING_TABLE["U9"]
    return None


def has_trust_only_resolution(lookup_events: Iterable[LookupEvent]) -> bool:
    """Return True if any lookup event resolved a claim from a trust-only source."""
    for event in lookup_events:
        if event.note == "trust_only" and event.returned_values:
            return True
    return False


def trust_only_claim_ids(lookup_events: Iterable[LookupEvent]) -> set[str]:
    """Return the set of claim ids that were resolved by a trust-only source."""
    resolved: set[str] = set()
    for event in lookup_events:
        if event.note != "trust_only":
            continue
        for claim_id, value in event.returned_values.items():
            if value is not None:
                resolved.add(claim_id)
    return resolved
