"""Scenario-suite harness: discover, run, and compare expected vs actual outcomes.

This module owns the new-layer schema (SuiteScenario) and the programmatic
harness that drives `run_scenarios.py --scenarios`.  The existing
ScenarioDefinition and its file-backed helpers remain unchanged; this module
wraps them additively.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from logic_levels import build_domain_artifact, build_intent_artifact
from metadata import utc_timestamp
from mock_db import load_mock_db
from reasoner import solve_case_bundle
from schemas import (
    BlockReasonCode,
    CaseBundle,
    ExtractionRunMetadata,
    LookupSource,
    MockDbArtifact,
    SolveRunMetadata,
    SolverOutcome,
)
from use_case_files import (
    EXAMPLES_ROOT,
    FRAMEWORK_ROOT,
    load_use_case_from_dir,
    resolve_example_path,
)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class SuiteScenario(BaseModel):
    """One scenario in the expected-vs-actual test suite.

    Extends the shape of ScenarioDefinition with harness-specific fields.
    Pydantic ignores extra fields on ScenarioDefinition, so existing loaders
    remain backward-compatible when they read these richer JSONs.
    """

    name: str
    description: str
    request_file: str
    law_file: str
    mock_db_file: str = "mock_db.json"
    intent_assignments: dict[str, bool | None] = Field(default_factory=dict)
    mock_db_overrides: dict[str, bool | None] = Field(default_factory=dict)
    expected_outcome: SolverOutcome | None = None
    expected_reason_code: BlockReasonCode | None = None
    tags: list[str] = Field(default_factory=list)
    provenance: str = ""


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class SuiteResult:
    """Outcome of running one suite scenario through the solver."""

    scenario_name: str
    description: str
    tags: list[str]
    expected_outcome: SolverOutcome | None
    expected_reason_code: BlockReasonCode | None
    actual_outcome: SolverOutcome
    actual_reason_code: BlockReasonCode | None
    outcome_match: bool
    reason_code_match: bool
    notes: str = ""


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_suite_scenario(path: str | Path) -> SuiteScenario:
    """Load a SuiteScenario from a JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return SuiteScenario.model_validate(raw)


def discover_suite_scenario_files() -> list[Path]:
    """Return every scenarios/*.json file under examples/*/."""
    return sorted(EXAMPLES_ROOT.glob("*/scenarios/*.json"))


def discover_suite_scenario_files_for_case(case_name: str) -> list[Path]:
    """Return scenario files for one named example case."""
    case_dir = EXAMPLES_ROOT / case_name
    return sorted(case_dir.glob("scenarios/*.json"))


# ---------------------------------------------------------------------------
# Mock-DB override support
# ---------------------------------------------------------------------------


def _is_special_source(source: LookupSource) -> bool:
    """A source carries U-code-relevant metadata (U3 unavailable or U7 trust-only)."""
    return source.availability == "unavailable" or source.trust_only


def _apply_db_overrides(mock_db: MockDbArtifact, overrides: dict[str, bool | None]) -> MockDbArtifact:
    """Apply per-scenario overrides on top of the base mock DB.

    None values remove the claim from the merged DB (simulating missing data).
    Non-None values replace the stored value for that claim.

    Sources that carry U-code-relevant metadata (``availability="unavailable"``
    for U3 NO_REGISTER or ``trust_only=True`` for U7 TRUST_ONLY) are preserved
    verbatim so the reasoner still emits the corresponding LookupEvent notes.
    Remaining ordinary sources are collapsed into a single merged source and
    per-scenario overrides are applied on top.
    """
    special_sources: list[LookupSource] = []
    special_keys: set[str] = set()
    merged: dict[str, bool | None] = {}
    for source in mock_db.sources:
        if _is_special_source(source):
            special_sources.append(source)
            special_keys.update(source.values.keys())
            continue
        merged.update(source.values)
    for claim_id, value in overrides.items():
        if claim_id in special_keys:
            continue
        if value is None:
            merged.pop(claim_id, None)
        else:
            merged[claim_id] = value
    sources: list[LookupSource] = list(special_sources)
    if merged:
        sources.append(
            LookupSource(
                source_id="suite_merged",
                label="Mock DB (suite overrides applied)",
                description="Single merged source after scenario-level overrides.",
                values=merged,
            )
        )
    return MockDbArtifact(sources=sources)


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------


def run_suite_scenario(scenario_path: Path) -> SuiteResult:
    """Execute one suite scenario and return a SuiteResult."""
    suite_sc = load_suite_scenario(scenario_path)
    case_dir = scenario_path.resolve().parents[1]

    use_case = load_use_case_from_dir(case_dir)
    law_path = resolve_example_path(case_dir, suite_sc.law_file)
    law_text = law_path.read_text(encoding="utf-8")

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
    intent = build_intent_artifact(
        use_case,
        "",
        use_case.default_logic_level,
        suite_sc.intent_assignments,
        run_metadata=run_meta,
    )

    base_db_path = resolve_example_path(case_dir, suite_sc.mock_db_file)
    base_db = load_mock_db(base_db_path)
    mock_db = _apply_db_overrides(base_db, suite_sc.mock_db_overrides)

    bundle = CaseBundle(
        logic_level=use_case.default_logic_level,
        domain=domain,
        intent=intent,
        mock_db=mock_db,
    )
    solution = solve_case_bundle(bundle)
    solution.solve_metadata = SolveRunMetadata(
        generated_at_utc=utc_timestamp(),
        mock_db_path=str(base_db_path),
    )

    actual_outcome = solution.final_outcome
    actual_reason_code = solution.block_reason_code

    outcome_match = (suite_sc.expected_outcome is None) or (actual_outcome == suite_sc.expected_outcome)
    reason_code_match = (suite_sc.expected_reason_code is None) or (
        actual_reason_code == suite_sc.expected_reason_code
    )

    notes = ""
    if suite_sc.expected_outcome is None:
        notes = "expected_outcome not set (skip)"
    elif not outcome_match:
        notes = f"outcome mismatch: expected {suite_sc.expected_outcome.value}, got {actual_outcome.value}"
    elif suite_sc.expected_reason_code is not None and not reason_code_match:
        notes = (
            f"reason_code mismatch: expected {suite_sc.expected_reason_code.value}, "
            f"got {actual_reason_code.value if actual_reason_code else 'null'}"
        )

    return SuiteResult(
        scenario_name=suite_sc.name,
        description=suite_sc.description,
        tags=suite_sc.tags,
        expected_outcome=suite_sc.expected_outcome,
        expected_reason_code=suite_sc.expected_reason_code,
        actual_outcome=actual_outcome,
        actual_reason_code=actual_reason_code,
        outcome_match=outcome_match,
        reason_code_match=reason_code_match,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Markdown table writer
# ---------------------------------------------------------------------------


def _outcome_str(outcome: SolverOutcome | None) -> str:
    return outcome.value if outcome is not None else "—"


def _reason_str(code: BlockReasonCode | None) -> str:
    return code.value if code is not None else "—"


def _match_str(match: bool) -> str:
    return "YES" if match else "NO"


def build_markdown_table(results: list[SuiteResult]) -> str:
    """Render a Markdown table of expected-vs-actual results."""
    header = "| id | description | expected | actual | match | notes |"
    separator = "|----|-------------|----------|--------|-------|-------|"
    rows = [header, separator]
    for r in results:
        expected = _outcome_str(r.expected_outcome)
        actual = _outcome_str(r.actual_outcome)
        overall_match = r.outcome_match and r.reason_code_match
        rows.append(
            f"| {r.scenario_name} | {r.description} | {expected} | {actual} | {_match_str(overall_match)} | {r.notes} |"
        )
    return "\n".join(rows) + "\n"


def write_markdown_table(results: list[SuiteResult], case_name: str) -> Path:
    """Write the expected-vs-actual Markdown table for one case and return its path."""
    out_dir = FRAMEWORK_ROOT / "examples" / case_name / "review_runs" / "scenario_suite"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "expected_vs_actual.md"
    out_path.write_text(build_markdown_table(results), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Per-case and full-suite runners
# ---------------------------------------------------------------------------


@dataclass
class CaseSuiteReport:
    """Summary of running the scenario suite for one example case."""

    case_name: str
    results: list[SuiteResult] = field(default_factory=list)
    table_path: Path | None = None

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.outcome_match and r.reason_code_match)

    @property
    def mismatches(self) -> int:
        return self.total - self.passed


def run_case_suite(case_name: str, scenario_filter: str | None = None) -> CaseSuiteReport:
    """Run all suite scenarios for one example case and write the table."""
    files = discover_suite_scenario_files_for_case(case_name)
    report = CaseSuiteReport(case_name=case_name)
    for f in files:
        if scenario_filter and Path(f).stem != scenario_filter:
            continue
        result = run_suite_scenario(f)
        report.results.append(result)
    if report.results:
        report.table_path = write_markdown_table(report.results, case_name)
    return report


def run_full_suite(scenario_filter: str | None = None) -> list[CaseSuiteReport]:
    """Run the suite across all five target domains."""
    target_cases = [
        "civil_service_eligibility",
        "consumer_withdrawal",
        "land_tax_exemption",
        "personal_data_journalism",
        "building_permit",
    ]
    reports: list[CaseSuiteReport] = []
    for case_name in target_cases:
        case_dir = EXAMPLES_ROOT / case_name
        if not case_dir.exists():
            continue
        report = run_case_suite(case_name, scenario_filter=scenario_filter)
        reports.append(report)
    return reports


def print_suite_summary(reports: list[CaseSuiteReport]) -> int:
    """Print per-case summaries and a totals line; return mismatch count."""
    total_all = 0
    passed_all = 0
    for report in reports:
        total_all += report.total
        passed_all += report.passed
        status = "OK" if report.mismatches == 0 else "FAIL"
        print(
            f"  [{status}] {report.case_name}: {report.passed}/{report.total} passed"
            + (f"  -> {report.table_path}" if report.table_path else "")
        )
    mismatches_all = total_all - passed_all
    print(f"\nTOTAL: {passed_all}/{total_all} passed, {mismatches_all} mismatch(es)")
    return mismatches_all
