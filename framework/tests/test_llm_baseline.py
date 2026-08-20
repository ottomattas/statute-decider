"""Tests for the LLM-only baseline and experiment (ii) paired runner."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from experiment_ii import (  # noqa: E402
    aggregate,
    pair_rows,
    render_markdown_table,
    render_paired_markdown,
    run_llm_row,
    run_runtime_row,
    score_row,
)
from llm_baseline import (  # noqa: E402
    BaselineDecision,
    known_facts_for_scenario,
    load_scenario_context,
)
from mock_db import load_mock_db  # noqa: E402
from scenario_suite import load_suite_scenario  # noqa: E402
from use_case_files import load_use_case_from_dir, resolve_example_path  # noqa: E402

ALLOW_PATH = (
    FRAMEWORK_ROOT / "examples/civil_service_eligibility/scenarios/civil_service_allow.json"
)
NEED_DB_PATH = (
    FRAMEWORK_ROOT / "examples/civil_service_eligibility/scenarios/civil_service_need_db.json"
)


def _fake_need_more_info(*, system, user, response_model, temperature=0.0):  # noqa: ARG001
    """Injected complete() — must not touch a network."""
    return response_model(
        outcome="NEED_MORE_INFO",
        missing_facts=["ee_citizen", "not_a_real_claim"],
        reason="citizenship is still open",
    )


class TestLlmBaselineScoring(unittest.TestCase):
    def test_fake_provider_need_more_info_scoring_matches(self) -> None:
        row = run_llm_row(NEED_DB_PATH, "fake", _fake_need_more_info)
        self.assertEqual(row["condition"], "llm")
        self.assertEqual(row["provider"], "fake")
        self.assertEqual(row["paper_outcome"], "NEED_MORE_INFO")
        self.assertEqual(row["missing_facts"], ["ee_citizen"])
        self.assertNotIn("not_a_real_claim", row["missing_facts"])
        scored = score_row(
            "NEED_MORE_INFO",
            ["ee_citizen"],
            row["paper_outcome"],
            row["missing_facts"],
        )
        self.assertTrue(scored["outcome_match"])
        self.assertEqual(scored["precision"], 1.0)
        self.assertEqual(scored["recall"], 1.0)

    def test_score_row_partial_fact_set(self) -> None:
        scored = score_row(
            "NEED_MORE_INFO",
            ["ee_citizen", "full_capacity"],
            "NEED_MORE_INFO",
            ["ee_citizen"],
        )
        self.assertTrue(scored["outcome_match"])
        self.assertEqual(scored["precision"], 1.0)
        self.assertEqual(scored["recall"], 0.5)


class TestRuntimeRow(unittest.TestCase):
    def test_allow_scenario_paper_outcome_and_empty_facts(self) -> None:
        row = run_runtime_row(ALLOW_PATH)
        self.assertEqual(row["condition"], "runtime")
        self.assertEqual(row["paper_outcome"], "ALLOW")
        self.assertEqual(row["fine_grained_outcome"], "ALLOW")
        self.assertEqual(row["missing_facts"], [])
        self.assertEqual(row["expected_paper_outcome"], "ALLOW")
        self.assertTrue(row["outcome_match"])
        self.assertEqual(row["precision"], 1.0)
        self.assertEqual(row["recall"], 1.0)

    def test_known_facts_merge_intent_and_db_overrides(self) -> None:
        scenario = load_suite_scenario(NEED_DB_PATH)
        case_dir = NEED_DB_PATH.parents[1]
        use_case = load_use_case_from_dir(case_dir)
        mock_db = load_mock_db(resolve_example_path(case_dir, scenario.mock_db_file))
        known = known_facts_for_scenario(scenario, use_case, mock_db)
        self.assertEqual(known["no_conflict_declared"], True)
        self.assertNotIn("ee_citizen", known)
        self.assertIn("full_capacity", known)
        ctx = load_scenario_context(NEED_DB_PATH)
        self.assertIn("ee_citizen", ctx.unknown_claim_ids)


class TestPairingAndAggregate(unittest.TestCase):
    def test_pair_and_aggregate_one_scenario(self) -> None:
        runtime = run_runtime_row(ALLOW_PATH)
        llm = run_llm_row(ALLOW_PATH, "fake", _fake_need_more_info)
        paired = pair_rows(runtime, llm)
        self.assertEqual(paired["runtime_paper_outcome"], "ALLOW")
        self.assertEqual(paired["llm_paper_outcome"], "NEED_MORE_INFO")
        self.assertTrue(paired["runtime_outcome_match"])
        self.assertFalse(paired["llm_outcome_match"])
        summary = aggregate([runtime, llm])
        self.assertEqual(summary["n"], 2)
        self.assertEqual(summary["per_class_accuracy"]["ALLOW"], 0.5)
        table = render_paired_markdown([paired])
        self.assertIn("civil_service_allow", table)
        self.assertIn("NEED_MORE_INFO", table)
        single = render_markdown_table([runtime])
        self.assertIn("runtime", single)

    def test_baseline_decision_schema(self) -> None:
        decision = BaselineDecision(outcome="DENY")
        self.assertEqual(decision.missing_facts, [])
        self.assertEqual(decision.reason, "")


if __name__ == "__main__":
    unittest.main()
