"""Unit tests for :mod:`truth_table`."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from schemas import BlockReasonCode, SolverOutcome  # noqa: E402
from truth_table import (  # noqa: E402
    DEFAULT_MAX_VARS,
    TruthTableReport,
    TruthTableRow,
    enumerate_truth_table,
    render_markdown,
    write_markdown,
)


TARGET_CASES = (
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
)


class TestEnumerateTruthTableSkip(unittest.TestCase):
    """When ``n > max_vars`` the enumeration is skipped without producing rows."""

    def test_skip_when_max_vars_is_zero(self) -> None:
        report = enumerate_truth_table("consumer_withdrawal", max_vars=0)
        self.assertTrue(report.skipped)
        self.assertEqual(report.rows, [])
        self.assertIn("exceeding max_vars=0", report.skip_reason)
        self.assertGreater(report.n_vars, 0)

    def test_civil_service_skipped_at_default_max_vars(self) -> None:
        report = enumerate_truth_table("civil_service_eligibility", max_vars=DEFAULT_MAX_VARS)
        self.assertTrue(report.skipped)
        self.assertEqual(report.n_rows, 0)


class TestEnumerateTruthTableRowCount(unittest.TestCase):
    """A non-skipped report has exactly ``2 ** n_vars`` rows."""

    def test_consumer_withdrawal_has_2n_rows(self) -> None:
        report = enumerate_truth_table("consumer_withdrawal")
        self.assertFalse(report.skipped)
        self.assertEqual(report.n_rows, 2 ** report.n_vars)
        self.assertGreaterEqual(report.n_rows, 2)
        for row in report.rows:
            self.assertIsInstance(row, TruthTableRow)
            self.assertIsInstance(row.outcome, SolverOutcome)
            self.assertEqual(set(row.assignment.keys()), set(report.claim_ids))

    def test_all_assignments_are_unique(self) -> None:
        report = enumerate_truth_table("consumer_withdrawal")
        seen: set[tuple[tuple[str, bool], ...]] = set()
        for row in report.rows:
            key = tuple(sorted(row.assignment.items()))
            self.assertNotIn(key, seen)
            seen.add(key)


class TestRenderMarkdown(unittest.TestCase):
    """``render_markdown`` emits a well-formed table and handles the skip case."""

    def test_header_and_rows_present(self) -> None:
        report = enumerate_truth_table("consumer_withdrawal")
        text = render_markdown(report)
        self.assertIn("# Truth table - consumer_withdrawal", text)
        for claim_id in report.claim_ids:
            self.assertIn(claim_id, text)
        non_empty_body_lines = [
            line for line in text.splitlines() if line.startswith("|") and "---" not in line
        ]
        self.assertEqual(len(non_empty_body_lines), report.n_rows + 1)

    def test_skipped_report_contains_skip_marker(self) -> None:
        skipped = TruthTableReport(
            case_name="example",
            claim_ids=["a", "b", "c"],
            skipped=True,
            skip_reason="too large",
        )
        text = render_markdown(skipped)
        self.assertIn("Enumeration skipped", text)
        self.assertIn("too large", text)
        self.assertNotIn("| outcome |", text)


class TestWriteMarkdown(unittest.TestCase):
    """``write_markdown`` writes to the expected review-runs path."""

    def test_write_creates_file(self) -> None:
        report = enumerate_truth_table("consumer_withdrawal")
        path = write_markdown(report)
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())
        self.assertEqual(path.name, "truth_table.md")
        self.assertEqual(path.parent.name, "truth_tables")
        self.assertEqual(path.parent.parent.name, "review_runs")
        body = path.read_text(encoding="utf-8")
        self.assertIn("consumer_withdrawal", body)


class TestReasonerParity(unittest.TestCase):
    """Enumerated rows match the public solver's decisions for pinned assignments."""

    def test_all_true_row_matches_direct_solver_run(self) -> None:
        from logic_levels import build_domain_artifact, build_intent_artifact
        from metadata import utc_timestamp
        from mock_db import load_mock_db
        from reasoner import solve_case_bundle
        from scenario_suite import _apply_db_overrides
        from schemas import CaseBundle, ExtractionRunMetadata
        from use_case_files import EXAMPLES_ROOT, load_use_case_from_dir

        case_name = "consumer_withdrawal"
        report = enumerate_truth_table(case_name)
        case_dir = EXAMPLES_ROOT / case_name
        use_case = load_use_case_from_dir(case_dir)
        law_text = (case_dir / "law.txt").read_text(encoding="utf-8")
        run_meta = ExtractionRunMetadata(
            generated_at_utc=utc_timestamp(),
            model_name="deterministic-fixture",
        )
        domain = build_domain_artifact(
            use_case,
            use_case.default_logic_level,
            law_text,
            run_metadata=run_meta,
        )
        base_db = load_mock_db(case_dir / "mock_db.json")

        for row in report.rows:
            intent = build_intent_artifact(
                use_case,
                "",
                use_case.default_logic_level,
                dict(row.assignment),
                run_metadata=run_meta,
            )
            mock_db = _apply_db_overrides(base_db, dict(row.assignment))
            bundle = CaseBundle(
                logic_level=use_case.default_logic_level,
                domain=domain,
                intent=intent,
                mock_db=mock_db,
            )
            solution = solve_case_bundle(bundle)
            self.assertEqual(
                row.outcome,
                solution.final_outcome,
                msg=f"outcome mismatch for assignment {row.assignment}",
            )
            self.assertEqual(
                row.reason_code,
                solution.block_reason_code,
                msg=f"reason mismatch for assignment {row.assignment}",
            )


if __name__ == "__main__":
    unittest.main()
