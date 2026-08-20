"""Unit tests for the expected-vs-actual scenario-suite harness."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from scenario_suite import (  # noqa: E402
    CaseSuiteReport,
    SuiteResult,
    build_markdown_table,
    discover_suite_scenario_files,
    discover_suite_scenario_files_for_case,
    load_suite_scenario,
    run_case_suite,
    run_full_suite,
    run_suite_scenario,
    write_markdown_table,
)
from schemas import BlockReasonCode, SolverOutcome  # noqa: E402


FIVE_CASES = [
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
]


class TestSuiteScenarioDiscovery(unittest.TestCase):
    def test_discover_finds_at_least_15_scenarios(self) -> None:
        files = discover_suite_scenario_files()
        self.assertGreaterEqual(len(files), 15, "Expected at least 15 suite scenario files.")

    def test_each_target_case_has_at_least_3_scenarios(self) -> None:
        for case in FIVE_CASES:
            files = discover_suite_scenario_files_for_case(case)
            self.assertGreaterEqual(
                len(files),
                3,
                f"Case {case!r} should have at least 3 scenarios, found {len(files)}.",
            )


class TestSuiteScenarioLoad(unittest.TestCase):
    def test_load_allow_scenario(self) -> None:
        path = FRAMEWORK_ROOT / "examples/civil_service_eligibility/scenarios/civil_service_allow.json"
        sc = load_suite_scenario(path)
        self.assertEqual(sc.name, "civil_service_allow")
        self.assertEqual(sc.expected_outcome, SolverOutcome.ALLOW)
        self.assertIn("positive", sc.tags)

    def test_load_deny_scenario(self) -> None:
        path = FRAMEWORK_ROOT / "examples/civil_service_eligibility/scenarios/civil_service_deny.json"
        sc = load_suite_scenario(path)
        self.assertEqual(sc.expected_outcome, SolverOutcome.DENY)

    def test_load_need_db_scenario(self) -> None:
        path = FRAMEWORK_ROOT / "examples/civil_service_eligibility/scenarios/civil_service_need_db.json"
        sc = load_suite_scenario(path)
        self.assertEqual(sc.expected_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertIn("ee_citizen", sc.mock_db_overrides)
        self.assertIsNone(sc.mock_db_overrides["ee_citizen"])

    def test_all_seeded_scenarios_have_expected_outcome(self) -> None:
        for case in FIVE_CASES:
            for f in discover_suite_scenario_files_for_case(case):
                sc = load_suite_scenario(f)
                self.assertIsNotNone(
                    sc.expected_outcome,
                    f"Scenario {f.name!r} in {case!r} is missing expected_outcome.",
                )


class TestRunSuiteScenario(unittest.TestCase):
    def _run(self, case: str, name: str) -> SuiteResult:
        path = FRAMEWORK_ROOT / "examples" / case / "scenarios" / f"{name}.json"
        return run_suite_scenario(path)

    def test_civil_service_allow_passes(self) -> None:
        result = self._run("civil_service_eligibility", "civil_service_allow")
        self.assertEqual(result.actual_outcome, SolverOutcome.ALLOW)
        self.assertTrue(result.outcome_match)

    def test_civil_service_deny_passes(self) -> None:
        result = self._run("civil_service_eligibility", "civil_service_deny")
        self.assertEqual(result.actual_outcome, SolverOutcome.DENY)
        self.assertTrue(result.outcome_match)

    def test_civil_service_need_db_passes(self) -> None:
        result = self._run("civil_service_eligibility", "civil_service_need_db")
        self.assertEqual(result.actual_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertTrue(result.outcome_match)

    def test_consumer_withdrawal_allow_passes(self) -> None:
        result = self._run("consumer_withdrawal", "consumer_withdrawal_allow")
        self.assertEqual(result.actual_outcome, SolverOutcome.ALLOW)
        self.assertTrue(result.outcome_match)

    def test_consumer_withdrawal_deny_passes(self) -> None:
        result = self._run("consumer_withdrawal", "consumer_withdrawal_deny")
        self.assertEqual(result.actual_outcome, SolverOutcome.DENY)
        self.assertTrue(result.outcome_match)

    def test_consumer_withdrawal_need_user_passes(self) -> None:
        result = self._run("consumer_withdrawal", "consumer_withdrawal_need_user")
        self.assertEqual(result.actual_outcome, SolverOutcome.NEED_USER_INFO)
        self.assertTrue(result.outcome_match)

    def test_land_tax_allow_passes(self) -> None:
        result = self._run("land_tax_exemption", "land_tax_allow")
        self.assertEqual(result.actual_outcome, SolverOutcome.ALLOW)
        self.assertTrue(result.outcome_match)

    def test_land_tax_deny_passes(self) -> None:
        result = self._run("land_tax_exemption", "land_tax_deny")
        self.assertEqual(result.actual_outcome, SolverOutcome.DENY)
        self.assertTrue(result.outcome_match)

    def test_land_tax_need_db_passes(self) -> None:
        result = self._run("land_tax_exemption", "land_tax_need_db")
        self.assertEqual(result.actual_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertTrue(result.outcome_match)

    def test_journalism_allow_passes(self) -> None:
        result = self._run("personal_data_journalism", "journalism_allow")
        self.assertEqual(result.actual_outcome, SolverOutcome.ALLOW)
        self.assertTrue(result.outcome_match)

    def test_journalism_deny_passes(self) -> None:
        result = self._run("personal_data_journalism", "journalism_deny")
        self.assertEqual(result.actual_outcome, SolverOutcome.DENY)
        self.assertTrue(result.outcome_match)

    def test_journalism_need_user_passes(self) -> None:
        result = self._run("personal_data_journalism", "journalism_need_user")
        self.assertEqual(result.actual_outcome, SolverOutcome.NEED_USER_INFO)
        self.assertTrue(result.outcome_match)

    def test_building_permit_allow_passes(self) -> None:
        result = self._run("building_permit", "building_permit_allow")
        self.assertEqual(result.actual_outcome, SolverOutcome.ALLOW)
        self.assertTrue(result.outcome_match)

    def test_building_permit_deny_passes(self) -> None:
        result = self._run("building_permit", "building_permit_deny")
        self.assertEqual(result.actual_outcome, SolverOutcome.DENY)
        self.assertTrue(result.outcome_match)

    def test_building_permit_need_db_passes(self) -> None:
        result = self._run("building_permit", "building_permit_need_db")
        self.assertEqual(result.actual_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertTrue(result.outcome_match)


class TestMarkdownTable(unittest.TestCase):
    def _make_result(
        self,
        name: str,
        expected: SolverOutcome,
        actual: SolverOutcome,
    ) -> SuiteResult:
        match = expected == actual
        return SuiteResult(
            scenario_name=name,
            description="test",
            tags=[],
            expected_outcome=expected,
            expected_reason_code=None,
            actual_outcome=actual,
            actual_reason_code=None,
            outcome_match=match,
            reason_code_match=True,
            notes="" if match else f"outcome mismatch: expected {expected.value}, got {actual.value}",
        )

    def test_table_contains_header(self) -> None:
        results = [self._make_result("s1", SolverOutcome.ALLOW, SolverOutcome.ALLOW)]
        table = build_markdown_table(results)
        self.assertIn("| id |", table)
        self.assertIn("| expected |", table)
        self.assertIn("| actual |", table)
        self.assertIn("| match |", table)

    def test_table_shows_yes_for_match(self) -> None:
        results = [self._make_result("s1", SolverOutcome.ALLOW, SolverOutcome.ALLOW)]
        table = build_markdown_table(results)
        self.assertIn("YES", table)
        self.assertNotIn("NO", table)

    def test_table_shows_no_for_mismatch(self) -> None:
        results = [self._make_result("s1", SolverOutcome.ALLOW, SolverOutcome.DENY)]
        table = build_markdown_table(results)
        self.assertIn("NO", table)


class TestCaseSuiteReport(unittest.TestCase):
    def test_run_case_suite_civil_service(self) -> None:
        report = run_case_suite("civil_service_eligibility")
        self.assertGreaterEqual(report.total, 3)
        self.assertEqual(report.mismatches, 0, f"Unexpected mismatches: {report.mismatches}")

    def test_run_case_suite_writes_markdown_table(self) -> None:
        report = run_case_suite("civil_service_eligibility")
        self.assertIsNotNone(report.table_path)
        self.assertTrue(report.table_path.exists())
        content = report.table_path.read_text(encoding="utf-8")
        self.assertIn("| id |", content)
        self.assertIn("civil_service_allow", content)

    def test_mismatch_count_is_accurate(self) -> None:
        report = run_case_suite("civil_service_eligibility")
        actual_mismatches = sum(1 for r in report.results if not (r.outcome_match and r.reason_code_match))
        self.assertEqual(report.mismatches, actual_mismatches)


class TestFullSuite(unittest.TestCase):
    def test_full_suite_all_cases_pass(self) -> None:
        reports = run_full_suite()
        self.assertEqual(len(reports), 5, f"Expected 5 case reports, got {len(reports)}.")
        total_mismatches = sum(r.mismatches for r in reports)
        self.assertEqual(
            total_mismatches,
            0,
            f"Full suite produced {total_mismatches} mismatch(es).",
        )

    def test_full_suite_scenario_filter(self) -> None:
        reports = run_full_suite(scenario_filter="civil_service_allow")
        self.assertTrue(all(r.total <= 1 for r in reports))
        civil = next((r for r in reports if r.case_name == "civil_service_eligibility"), None)
        self.assertIsNotNone(civil)
        self.assertEqual(civil.total, 1)
        self.assertEqual(civil.results[0].scenario_name, "civil_service_allow")


if __name__ == "__main__":
    unittest.main()
