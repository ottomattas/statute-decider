"""Unit tests for catalog-held-out synthesis mapping and the encoding scorer."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from encoding_scorer import (  # noqa: E402
    ALIGNMENT_THRESHOLD,
    Alignment,
    ClaimMatch,
    align_claims,
    claim_alignment_f1,
    remap_rules,
    semantic_equivalence,
)
from extract_synthesis import (  # noqa: E402
    SynthesizedClaim,
    SynthesizedRule,
    SynthesisResponse,
    map_synthesis_response,
    synthesize_domain,
)
from logic_levels import build_domain_artifact  # noqa: E402
from schemas import ClaimSource, DomainClaim, LogicLevel, RuleKind  # noqa: E402
from use_case_files import EXAMPLES_ROOT, load_use_case_from_dir  # noqa: E402


def _claim(*, claim_id: str, label: str, formal_text: str = "") -> DomainClaim:
    return DomainClaim(
        claim_id=claim_id,
        lowered_atom=claim_id.upper(),
        label=label,
        description=label,
        source_type=ClaimSource.USER,
        formal_text=formal_text or label,
    )


class TestClaimAlignment(unittest.TestCase):
    def test_identical_labels_match(self) -> None:
        gold = [_claim(claim_id="is_consumer", label="Applicant is a consumer")]
        pred = [_claim(claim_id="party_is_consumer", label="Applicant is a consumer")]
        alignment = align_claims(gold, pred)
        self.assertEqual(len(alignment.matches), 1)
        self.assertEqual(alignment.matches[0].gold_id, "is_consumer")
        self.assertEqual(alignment.matches[0].pred_id, "party_is_consumer")
        self.assertGreaterEqual(alignment.matches[0].score, ALIGNMENT_THRESHOLD)
        self.assertEqual(alignment.unmatched_gold, [])
        self.assertEqual(alignment.unmatched_pred, [])
        self.assertGreater(claim_alignment_f1(alignment), 0.99)

    def test_unrelated_labels_do_not_match(self) -> None:
        gold = [_claim(claim_id="is_consumer", label="Applicant is a consumer")]
        pred = [
            _claim(
                claim_id="heritage_zone",
                label="The building sits inside a heritage protection zone",
            )
        ]
        alignment = align_claims(gold, pred)
        self.assertEqual(alignment.matches, [])
        self.assertEqual(alignment.unmatched_gold, ["is_consumer"])
        self.assertEqual(alignment.unmatched_pred, ["heritage_zone"])
        self.assertEqual(claim_alignment_f1(alignment), 0.0)
        self.assertFalse(alignment.needs_audit)


class TestSemanticEquivalence(unittest.TestCase):
    def test_gold_domain_vs_itself_is_equivalent(self) -> None:
        case_dir = EXAMPLES_ROOT / "consumer_withdrawal"
        use_case = load_use_case_from_dir(case_dir)
        law_text = (case_dir / "law.txt").read_text(encoding="utf-8")
        gold = build_domain_artifact(use_case, LogicLevel.PROPOSITIONAL, law_text)
        alignment = Alignment(
            matches=[
                ClaimMatch(gold_id=claim.claim_id, pred_id=claim.claim_id, score=1.0)
                for claim in gold.claims
            ],
            unmatched_gold=[],
            unmatched_pred=[],
            needs_audit=False,
        )
        result = semantic_equivalence(gold, gold, alignment)
        self.assertFalse(result["skipped"])
        self.assertTrue(result["equivalent"])
        self.assertEqual(result["n_agree"], result["n_rows"])
        self.assertEqual(result["n_rows"], 2 ** len(gold.claims))

    def test_skips_when_aligned_count_exceeds_max_vars(self) -> None:
        case_dir = EXAMPLES_ROOT / "consumer_withdrawal"
        use_case = load_use_case_from_dir(case_dir)
        law_text = (case_dir / "law.txt").read_text(encoding="utf-8")
        gold = build_domain_artifact(use_case, LogicLevel.PROPOSITIONAL, law_text)
        alignment = Alignment(
            matches=[
                ClaimMatch(gold_id=claim.claim_id, pred_id=claim.claim_id, score=1.0)
                for claim in gold.claims
            ]
        )
        result = semantic_equivalence(gold, gold, alignment, max_vars=0)
        self.assertTrue(result["skipped"])
        self.assertFalse(result["equivalent"])
        self.assertEqual(result["n_rows"], 0)


class TestSynthesisParser(unittest.TestCase):
    def test_hand_built_response_becomes_valid_domain_artifact(self) -> None:
        response = SynthesisResponse(
            title="Withdrawal demo",
            allow_outcome_id="allow",
            deny_outcome_id="deny",
            claims=[
                SynthesizedClaim(
                    claim_id="is_consumer",
                    lowered_atom="IS_CONSUMER",
                    label="Applicant is a consumer",
                    source_type=ClaimSource.DB,
                    formal_text="IS_CONSUMER",
                ),
                SynthesizedClaim(
                    claim_id="within_14_days",
                    lowered_atom="WITHIN_14_DAYS",
                    label="The 14-day window is still running",
                    source_type=ClaimSource.USER,
                    formal_text="WITHIN_14_DAYS",
                ),
                SynthesizedClaim(
                    claim_id="excluded",
                    lowered_atom="EXCLUDED",
                    label="Goods are in an excluded category",
                    source_type=ClaimSource.DB,
                    formal_text="EXCLUDED",
                ),
            ],
            rules=[
                SynthesizedRule(
                    rule_id="allow_timely",
                    kind=RuleKind.ALLOW_IF_ALL,
                    label="Timely consumer withdrawal",
                    when_claim_ids=["is_consumer", "within_14_days"],
                    target_outcome_id="allow",
                ),
                SynthesizedRule(
                    rule_id="deny_excluded",
                    kind=RuleKind.DENY_IF_ALL,
                    label="Excluded goods block withdrawal",
                    when_claim_ids=["excluded"],
                    target_outcome_id="deny",
                ),
                SynthesizedRule(
                    rule_id="broken_unknown_premise",
                    kind=RuleKind.ALLOW_IF_ALL,
                    when_claim_ids=["not_a_real_claim"],
                    target_outcome_id="allow",
                ),
            ],
        )
        mapped = map_synthesis_response(response, law_text="dummy statute", title="Withdrawal demo")
        artifact = mapped.artifact
        artifact.model_validate(artifact.model_dump())
        self.assertEqual(artifact.allow_outcome_id, "allow")
        self.assertEqual(artifact.deny_outcome_id, "deny")
        self.assertEqual({claim.claim_id for claim in artifact.claims}, {
            "is_consumer",
            "within_14_days",
            "excluded",
        })
        self.assertEqual({rule.rule_id for rule in artifact.rules}, {"allow_timely", "deny_excluded"})
        self.assertEqual(mapped.dropped_rules, 1)
        self.assertTrue(any(rule.kind == RuleKind.ALLOW_IF_ALL for rule in artifact.rules))
        self.assertTrue(any(rule.kind == RuleKind.DENY_IF_ALL for rule in artifact.rules))

    def test_synthesize_domain_uses_injected_complete_fn(self) -> None:
        response = SynthesisResponse(
            title="injected",
            claims=[
                SynthesizedClaim(
                    claim_id="eligible",
                    label="Applicant is eligible",
                    source_type="user",
                    formal_text="ELIGIBLE",
                    lowered_atom="ELIGIBLE",
                )
            ],
            rules=[
                SynthesizedRule(
                    rule_id="allow_if_eligible",
                    kind="allow_if_all",
                    when_claim_ids=["eligible"],
                    target_outcome_id="allow",
                )
            ],
        )

        def fake_complete(*, system_instruction, user_content, response_model, **kwargs):
            self.assertIs(response_model, SynthesisResponse)
            self.assertIn("you do not receive a claim catalog", system_instruction.casefold())
            self.assertNotIn("Supported claim catalog", user_content)
            self.assertNotIn("{claim_catalog}", user_content)
            self.assertIn("ALLOW", user_content)
            self.assertIn("NEED_MORE_INFO", user_content)
            return response

        stats: dict[str, int] = {}
        artifact = synthesize_domain(
            "A person who is eligible may be allowed.",
            complete_fn=fake_complete,
            title="injected",
            stats=stats,
        )
        self.assertEqual(artifact.title, "injected")
        self.assertEqual(len(artifact.claims), 1)
        self.assertEqual(len(artifact.rules), 1)
        self.assertEqual(stats["dropped_rules"], 0)
        self.assertEqual(artifact.allow_outcome_id, "allow")
        self.assertEqual(artifact.deny_outcome_id, "deny")

    def test_remap_rules_rewrites_aligned_claim_ids(self) -> None:
        response = SynthesisResponse(
            claims=[
                SynthesizedClaim(claim_id="pred_a", label="Applicant is a consumer"),
            ],
            rules=[
                SynthesizedRule(
                    rule_id="r1",
                    kind=RuleKind.ALLOW_IF_ALL,
                    when_claim_ids=["pred_a"],
                    target_outcome_id="allow",
                )
            ],
        )
        mapped = map_synthesis_response(response, law_text="law")
        alignment = Alignment(
            matches=[ClaimMatch(gold_id="is_consumer", pred_id="pred_a", score=1.0)]
        )
        remapped = remap_rules(mapped.artifact.rules, alignment)
        self.assertEqual(remapped[0].when_claim_ids, ["is_consumer"])


if __name__ == "__main__":
    unittest.main()
