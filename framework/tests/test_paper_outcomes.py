"""Unit tests for the paper 3-outcome scoring layer."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from paper_outcomes import (  # noqa: E402
    PAPER_OUTCOMES,
    fact_set_precision_recall,
    missing_facts_from_solution,
    to_paper_outcome,
)
from schemas import (  # noqa: E402
    LogicLevel,
    SolutionArtifact,
    SolveSnapshot,
    SolverOutcome,
)


def _solution(*snapshots: SolveSnapshot, outcome: SolverOutcome = SolverOutcome.NEED_DB_INFO) -> SolutionArtifact:
    return SolutionArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        domain_title="test",
        request_text="test request",
        final_outcome=outcome,
        snapshots=list(snapshots),
    )


def _snap(
    stage: str,
    *,
    missing_db: list[str] | None = None,
    missing_user: list[str] | None = None,
    outcome: SolverOutcome = SolverOutcome.NEED_DB_INFO,
) -> SolveSnapshot:
    return SolveSnapshot(
        stage=stage,
        outcome=outcome,
        resolved_claims=[],
        rule_trace=[],
        missing_db_claim_ids=missing_db or [],
        missing_user_claim_ids=missing_user or [],
    )


class TestToPaperOutcome(unittest.TestCase):
    def test_paper_outcomes_tuple(self) -> None:
        self.assertEqual(PAPER_OUTCOMES, ("ALLOW", "DENY", "NEED_MORE_INFO"))

    def test_allow_and_deny_stay(self) -> None:
        self.assertEqual(to_paper_outcome(SolverOutcome.ALLOW), "ALLOW")
        self.assertEqual(to_paper_outcome(SolverOutcome.DENY), "DENY")
        self.assertEqual(to_paper_outcome("ALLOW"), "ALLOW")
        self.assertEqual(to_paper_outcome("DENY"), "DENY")

    def test_everything_else_is_need_more_info(self) -> None:
        for outcome in (
            SolverOutcome.NEED_DB_INFO,
            SolverOutcome.NEED_USER_INFO,
            SolverOutcome.NEED_EXPERT_JUDGMENT,
            SolverOutcome.UNDETERMINED_INTERPRETATION,
            SolverOutcome.UNVERIFIABLE_CLAIM,
        ):
            with self.subTest(outcome=outcome):
                self.assertEqual(to_paper_outcome(outcome), "NEED_MORE_INFO")
                self.assertEqual(to_paper_outcome(outcome.value), "NEED_MORE_INFO")

    def test_does_not_mutate_solver_outcome_enum(self) -> None:
        names = {member.name for member in SolverOutcome}
        self.assertIn("NEED_DB_INFO", names)
        self.assertNotIn("NEED_MORE_INFO", names)


class TestFactSetPrecisionRecall(unittest.TestCase):
    def test_empty_empty(self) -> None:
        self.assertEqual(fact_set_precision_recall([], []), (1.0, 1.0))

    def test_empty_expected_nonempty_actual(self) -> None:
        precision, recall = fact_set_precision_recall([], ["a"])
        self.assertEqual(precision, 0.0)
        self.assertEqual(recall, 1.0)

    def test_nonempty_expected_empty_actual(self) -> None:
        precision, recall = fact_set_precision_recall(["a"], [])
        self.assertEqual(precision, 1.0)
        self.assertEqual(recall, 0.0)

    def test_exact_match(self) -> None:
        self.assertEqual(fact_set_precision_recall(["a", "b"], ["b", "a"]), (1.0, 1.0))

    def test_partial_overlap(self) -> None:
        precision, recall = fact_set_precision_recall(["a", "b"], ["a", "c"])
        self.assertEqual(precision, 0.5)
        self.assertEqual(recall, 0.5)

    def test_duplicates_are_sets(self) -> None:
        self.assertEqual(fact_set_precision_recall(["a", "a"], ["a", "a", "a"]), (1.0, 1.0))


class TestMissingFactsFromSolution(unittest.TestCase):
    def test_empty_snapshots(self) -> None:
        self.assertEqual(missing_facts_from_solution(_solution()), [])

    def test_last_snapshot_when_it_has_missing_ids(self) -> None:
        solution = _solution(
            _snap("first", missing_db=["old_db"]),
            _snap("last", missing_user=["emergency"]),
        )
        self.assertEqual(missing_facts_from_solution(solution), ["emergency"])

    def test_walks_back_when_last_snapshot_is_empty(self) -> None:
        solution = _solution(
            _snap("first", missing_db=["ee_citizen"]),
            _snap("last"),
        )
        self.assertEqual(missing_facts_from_solution(solution), ["ee_citizen"])

    def test_all_empty_uses_last_snapshot(self) -> None:
        solution = _solution(_snap("first"), _snap("last"))
        self.assertEqual(missing_facts_from_solution(solution), [])

    def test_unions_db_and_user_and_sorts(self) -> None:
        solution = _solution(_snap("only", missing_db=["z_db", "a_db"], missing_user=["m_user"]))
        self.assertEqual(missing_facts_from_solution(solution), ["a_db", "m_user", "z_db"])


if __name__ == "__main__":
    unittest.main()
