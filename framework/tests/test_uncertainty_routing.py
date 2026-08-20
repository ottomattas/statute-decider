"""Unit tests for the backend-agnostic uncertainty routing (ART-64).

Covers ``framework/uncertainty_routing.py``:

- ``ROUTING_TABLE`` completeness and uniqueness.
- ``classify_claim_uncertainty`` decision boundaries for every U-code that
  is driven by a claim-level trigger.
- ``classify_rule_uncertainty`` for every U-code that is driven by a
  rule-level flag.
- Invariants on the inverse ``routing_for_reason_code`` lookup.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from schemas import (  # noqa: E402
    BlockReasonCode,
    ClaimSource,
    DomainClaim,
    DomainRule,
    IntentClaim,
    LookupEvent,
    PremiseEvaluation,
    RuleKind,
    RuleStatus,
    RuleTraceRow,
    SolverOutcome,
)
from uncertainty_routing import (  # noqa: E402
    ROUTING_TABLE,
    classify_claim_uncertainty,
    classify_rule_uncertainty,
    has_trust_only_resolution,
    routing_for_reason_code,
    trust_only_claim_ids,
)


EXPECTED_CODES = [f"U{i}" for i in range(1, 13)]


def _db_claim(source_type: ClaimSource = ClaimSource.DB, claim_id: str = "c1") -> DomainClaim:
    return DomainClaim(
        claim_id=claim_id,
        lowered_atom=claim_id,
        label=claim_id,
        description="",
        source_type=source_type,
        formal_text=claim_id,
    )


def _intent_claim(
    claim_id: str = "c1",
    *,
    source_type: ClaimSource = ClaimSource.USER,
    subjective_party: bool = False,
    glossary_low_confidence: bool = False,
    model_drift: bool = False,
) -> IntentClaim:
    return IntentClaim(
        claim_id=claim_id,
        lowered_atom=claim_id,
        label=claim_id,
        description="",
        source_type=source_type,
        formal_text=claim_id,
        subjective_party=subjective_party,
        glossary_low_confidence=glossary_low_confidence,
        model_drift=model_drift,
    )


def _rule(
    *,
    interpretation_ambiguous: bool = False,
    process_indeterminate: bool = False,
    context_dependent: bool = False,
) -> DomainRule:
    return DomainRule(
        rule_id="r1",
        kind=RuleKind.ALLOW_IF_ALL,
        label="r1",
        when_claim_ids=["c1"],
        formal_text="c1 -> ALLOW",
        lowered_formula="c1 -> ALLOW",
        target_outcome_id="ALLOW",
        interpretation_ambiguous=interpretation_ambiguous,
        process_indeterminate=process_indeterminate,
        context_dependent=context_dependent,
    )


def _needs_info_row(rule_id: str = "r1") -> RuleTraceRow:
    premise = PremiseEvaluation(
        claim_id="c1",
        label="c1",
        formal_text="c1",
        lowered_atom="c1",
        value=None,
    )
    return RuleTraceRow(
        rule_id=rule_id,
        label=rule_id,
        kind=RuleKind.ALLOW_IF_ALL,
        status=RuleStatus.NEEDS_INFO,
        formal_text="c1 -> ALLOW",
        lowered_formula="c1 -> ALLOW",
        premises=[premise],
        true_claim_ids=[],
        false_claim_ids=[],
        unknown_claim_ids=["c1"],
    )


def _firing_row(rule_id: str = "r1") -> RuleTraceRow:
    premise = PremiseEvaluation(
        claim_id="c1",
        label="c1",
        formal_text="c1",
        lowered_atom="c1",
        value=True,
    )
    return RuleTraceRow(
        rule_id=rule_id,
        label=rule_id,
        kind=RuleKind.ALLOW_IF_ALL,
        status=RuleStatus.FIRES,
        formal_text="c1 -> ALLOW",
        lowered_formula="c1 -> ALLOW",
        premises=[premise],
        true_claim_ids=["c1"],
        false_claim_ids=[],
        unknown_claim_ids=[],
    )


class TestRoutingTableCompleteness(unittest.TestCase):
    def test_routing_table_has_12_entries(self) -> None:
        self.assertEqual(sorted(ROUTING_TABLE.keys(), key=lambda c: int(c[1:])), EXPECTED_CODES)

    def test_every_entry_has_outcome_and_reason_code(self) -> None:
        for code in EXPECTED_CODES:
            entry = ROUTING_TABLE[code]
            self.assertEqual(entry.code, code)
            self.assertIsInstance(entry.outcome, SolverOutcome)
            self.assertIsInstance(entry.reason_code, BlockReasonCode)
            self.assertTrue(entry.description)

    def test_reason_codes_are_unique(self) -> None:
        codes = [ROUTING_TABLE[c].reason_code for c in EXPECTED_CODES]
        self.assertEqual(len(codes), len(set(codes)))


class TestRoutingForReasonCode(unittest.TestCase):
    def test_none_input_returns_none(self) -> None:
        self.assertIsNone(routing_for_reason_code(None))

    def test_non_uncertainty_reason_code_returns_none(self) -> None:
        self.assertIsNone(routing_for_reason_code(BlockReasonCode.DOMAIN_EXTRACTION_EMPTY))
        self.assertIsNone(routing_for_reason_code(BlockReasonCode.SOLVER_INCONSISTENT))

    def test_every_routing_reason_code_round_trips(self) -> None:
        for code in EXPECTED_CODES:
            entry = ROUTING_TABLE[code]
            routed = routing_for_reason_code(entry.reason_code)
            self.assertIsNotNone(routed)
            self.assertEqual(routed.code, code)


class TestClassifyClaimUncertainty(unittest.TestCase):
    def test_u1_statute_open(self) -> None:
        claim = _db_claim(source_type=ClaimSource.STATUTE_OPEN)
        hit = classify_claim_uncertainty(claim)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U1")
        self.assertEqual(hit.outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(hit.reason_code, BlockReasonCode.STATUTE_UNDERSPECIFIED)

    def test_u3_unavailable_source(self) -> None:
        claim = _db_claim()
        event = LookupEvent(
            stage="db_lookup",
            source_id="s1",
            source_label="s1",
            requested_claim_ids=["c1"],
            returned_values={"c1": None},
            note="source_unavailable",
        )
        hit = classify_claim_uncertainty(claim, lookup_events=[event])
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U3")

    def test_u5_default_db_claim_returns_none(self) -> None:
        claim = _db_claim()
        self.assertIsNone(classify_claim_uncertainty(claim))

    def test_u6_subjective_party(self) -> None:
        domain = _db_claim(source_type=ClaimSource.USER)
        intent = _intent_claim(subjective_party=True)
        hit = classify_claim_uncertainty(domain, intent)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U6")
        self.assertEqual(hit.reason_code, BlockReasonCode.SUBJECTIVE_PARTY)

    def test_u7_trust_only_event(self) -> None:
        claim = _db_claim()
        event = LookupEvent(
            stage="db_lookup",
            source_id="s1",
            source_label="s1",
            requested_claim_ids=["c1"],
            returned_values={"c1": True},
            note="trust_only",
        )
        hit = classify_claim_uncertainty(claim, lookup_events=[event])
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U7")
        self.assertEqual(hit.reason_code, BlockReasonCode.TRUST_ONLY)

    def test_u8_default_user_claim_returns_none(self) -> None:
        domain = _db_claim(source_type=ClaimSource.USER)
        intent = _intent_claim()
        self.assertIsNone(classify_claim_uncertainty(domain, intent))

    def test_u10_expert_source_type(self) -> None:
        claim = _db_claim(source_type=ClaimSource.EXPERT)
        hit = classify_claim_uncertainty(claim)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U10")
        self.assertEqual(hit.outcome, SolverOutcome.NEED_EXPERT_JUDGMENT)

    def test_u11_glossary_low_confidence(self) -> None:
        domain = _db_claim(source_type=ClaimSource.USER)
        intent = _intent_claim(glossary_low_confidence=True)
        hit = classify_claim_uncertainty(domain, intent)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U11")

    def test_u12_model_drift(self) -> None:
        domain = _db_claim(source_type=ClaimSource.USER)
        intent = _intent_claim(model_drift=True)
        hit = classify_claim_uncertainty(domain, intent)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U12")

    def test_statute_open_wins_over_subjective_party(self) -> None:
        claim = _db_claim(source_type=ClaimSource.STATUTE_OPEN)
        intent = _intent_claim(subjective_party=True)
        hit = classify_claim_uncertainty(claim, intent)
        self.assertEqual(hit.code, "U1")

    def test_unavailable_source_wins_over_trust_only(self) -> None:
        claim = _db_claim()
        events = [
            LookupEvent(
                stage="db_lookup",
                source_id="s1",
                source_label="s1",
                requested_claim_ids=["c1"],
                returned_values={"c1": None},
                note="source_unavailable",
            ),
            LookupEvent(
                stage="db_lookup",
                source_id="s2",
                source_label="s2",
                requested_claim_ids=["c1"],
                returned_values={"c1": True},
                note="trust_only",
            ),
        ]
        hit = classify_claim_uncertainty(claim, lookup_events=events)
        self.assertEqual(hit.code, "U3")


class TestClassifyRuleUncertainty(unittest.TestCase):
    def test_u2_interpretation_ambiguous(self) -> None:
        rule = _rule(interpretation_ambiguous=True)
        hit = classify_rule_uncertainty(rule, _needs_info_row())
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U2")

    def test_u4_process_indeterminate(self) -> None:
        rule = _rule(process_indeterminate=True)
        hit = classify_rule_uncertainty(rule, _needs_info_row())
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U4")

    def test_u9_context_dependent(self) -> None:
        rule = _rule(context_dependent=True)
        hit = classify_rule_uncertainty(rule, _needs_info_row())
        self.assertIsNotNone(hit)
        self.assertEqual(hit.code, "U9")
        self.assertEqual(hit.outcome, SolverOutcome.NEED_USER_INFO)

    def test_firing_rule_short_circuits_to_none(self) -> None:
        rule = _rule(interpretation_ambiguous=True)
        self.assertIsNone(classify_rule_uncertainty(rule, _firing_row()))

    def test_process_indeterminate_wins_over_interpretation(self) -> None:
        rule = _rule(interpretation_ambiguous=True, process_indeterminate=True)
        hit = classify_rule_uncertainty(rule, _needs_info_row())
        self.assertEqual(hit.code, "U4")

    def test_plain_rule_returns_none(self) -> None:
        self.assertIsNone(classify_rule_uncertainty(_rule(), _needs_info_row()))


class TestTrustOnlyHelpers(unittest.TestCase):
    def test_has_trust_only_resolution_true(self) -> None:
        event = LookupEvent(
            stage="db_lookup",
            source_id="s1",
            source_label="s1",
            requested_claim_ids=["c1"],
            returned_values={"c1": True},
            note="trust_only",
        )
        self.assertTrue(has_trust_only_resolution([event]))

    def test_has_trust_only_resolution_false_without_values(self) -> None:
        event = LookupEvent(
            stage="db_lookup",
            source_id="s1",
            source_label="s1",
            requested_claim_ids=["c1"],
            returned_values={},
            note="trust_only",
        )
        self.assertFalse(has_trust_only_resolution([event]))

    def test_trust_only_claim_ids_ignores_none_values(self) -> None:
        event = LookupEvent(
            stage="db_lookup",
            source_id="s1",
            source_label="s1",
            requested_claim_ids=["c1", "c2"],
            returned_values={"c1": True, "c2": None},
            note="trust_only",
        )
        self.assertEqual(trust_only_claim_ids([event]), {"c1"})


if __name__ == "__main__":
    unittest.main()
