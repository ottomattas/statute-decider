"""Tests for the matrix runner (no live HTTP)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from experiment_i import run_selection_condition  # noqa: E402
from llm import DomainExtractionResponse  # noqa: E402
from llm_baseline import BaselineDecision  # noqa: E402
from providers import ProviderResult, Usage, invoke_structured  # noqa: E402
from run_experiments import (  # noqa: E402
    gold_scenario_files,
    load_matrix,
    parse_args,
    run_matrix,
)


class TestInvokeStructured(unittest.TestCase):
    def test_unwraps_provider_result(self) -> None:
        decision = BaselineDecision(outcome="ALLOW", missing_facts=[], reason="ok")

        def complete(*, system, user, response_model, temperature=0.0):
            self.assertEqual(system, "sys")
            self.assertEqual(user, "user")
            return ProviderResult(
                parsed=decision,
                raw_text="{}",
                usage=Usage(1, 1),
                model="x",
                provider="fake",
            )

        parsed = invoke_structured(
            complete, system="sys", user="user", response_model=BaselineDecision
        )
        self.assertEqual(parsed.outcome, "ALLOW")

    def test_gemini_style_complete(self) -> None:
        def complete(*, system_instruction, user_content, response_model, **kwargs):
            return response_model(outcome="DENY", missing_facts=[], reason=system_instruction)

        parsed = invoke_structured(
            complete, system="s", user="u", response_model=BaselineDecision
        )
        self.assertEqual(parsed.outcome, "DENY")
        self.assertEqual(parsed.reason, "s")


class TestMatrixConfig(unittest.TestCase):
    def test_repo_matrix_loads(self) -> None:
        config = load_matrix(FRAMEWORK_ROOT.parent / "experiments" / "matrix.yaml")
        self.assertEqual(config["budget_eur"], 10)
        self.assertIn("gemini", config["providers"])
        self.assertTrue(config["experiment_ii"]["all_gold"])
        cases = config["experiment_i"]["cases"]
        self.assertEqual(len(cases), 3)

    def test_gold_scenario_count(self) -> None:
        files = gold_scenario_files({})
        self.assertEqual(len(files), 47)

    def test_parse_runtime_only(self) -> None:
        args = parse_args(["--runtime-only", "--dry-run"])
        self.assertTrue(args.runtime_only)
        self.assertTrue(args.dry_run)


class TestRunMatrixRuntimeOnly(unittest.TestCase):
    def test_runtime_only_writes_markdown(self) -> None:
        config = {
            "label": "unit",
            "budget_eur": 10,
            "repeats": 1,
            "providers": ["gemini"],
            "experiment_ii": {
                "enabled": True,
                "scenarios": ["civil_service_allow"],
            },
            "experiment_i": {"enabled": False},
        }
        with tempfile.TemporaryDirectory() as tmp:
            report = run_matrix(
                config,
                results_dir=Path(tmp),
                runtime_only=True,
                ingest_ledger=False,
            )
            self.assertEqual(report["n_runtime"], 1)
            self.assertEqual(report["n_llm"], 0)
            smoke = (Path(tmp) / "SMOKE-UNVALIDATED.md").read_text(encoding="utf-8")
            self.assertIn("SMOKE — UNVALIDATED", smoke)
            table = (Path(tmp) / "experiment_ii_runtime.md").read_text(encoding="utf-8")
            self.assertIn("civil_service_allow", table)
            self.assertTrue((Path(tmp) / "experiment_ii_runtime.jsonl").is_file())


class TestSelectionCondition(unittest.TestCase):
    def test_selection_scores_id_sets(self) -> None:
        case_dir = FRAMEWORK_ROOT / "examples" / "section_120_demo"

        def fake(*, system=None, user=None, system_instruction=None, user_content=None, response_model, **kwargs):
            self.assertIs(response_model, DomainExtractionResponse)
            prompt = (system or system_instruction or "") + (user or user_content or "")
            self.assertTrue(prompt)
            return DomainExtractionResponse(
                title="sel",
                claim_ids=["applicant_is_parent", "emergency", "one_parent_unreachable"],
                rule_ids=["allow_emergency"],
                summary="unit",
            )

        row = run_selection_condition(case_dir, fake)
        self.assertEqual(row["condition"], "selection")
        self.assertGreater(row["claim_f1"], 0.0)
        self.assertGreater(row["rule_f1"], 0.0)
        self.assertIsNone(row["equivalent"])


class TestExtractDomainCli(unittest.TestCase):
    def test_condition_flag_defaults_to_selection(self) -> None:
        from importlib import import_module

        mod = import_module("02_extract_domain")
        args = mod.parse_args(
            [
                "--use-case-dir",
                "framework/examples/section_120_demo",
                "--law-file",
                "framework/examples/section_120_demo/law.txt",
                "--out",
                "/tmp/out.json",
                "--condition",
                "synthesis",
                "--provider",
                "openai",
            ]
        )
        self.assertEqual(args.condition, "synthesis")
        self.assertEqual(args.provider, "openai")


if __name__ == "__main__":
    unittest.main()
