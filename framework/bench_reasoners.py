"""Wave-2 reasoner benchmark harness (ADR 0004).

Runs every available backend against the 15 seed scenarios that live under
``framework/examples/<case>/scenarios/``. Emits a Markdown table to
``framework/examples/review_runs/reasoner_benchmark/<ISO-date>.md`` and a
summary on stdout.

Exit policy:
- Non-zero exit only if Z3 itself diverges from a scenario's
  ``expected_outcome`` (treated as a regression).
- Divergences between backends are reported, not errored.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from statistics import mean

from logic_levels import build_domain_artifact, build_intent_artifact
from metadata import utc_timestamp
from mock_db import load_mock_db
from reasoner import ReasonerBackend
from scenario_suite import (
    SuiteScenario,
    _apply_db_overrides,
    discover_suite_scenario_files_for_case,
    load_suite_scenario,
)
from schemas import (
    CaseBundle,
    ExtractionRunMetadata,
    SolverOutcome,
)
from use_case_files import (
    EXAMPLES_ROOT,
    FRAMEWORK_ROOT,
    load_use_case_from_dir,
    resolve_example_path,
)


BENCHMARK_CASES: tuple[str, ...] = (
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
)

ALL_BACKEND_NAMES: tuple[str, ...] = ("z3", "clingo", "pysat", "horn")


@dataclass
class BenchRun:
    """One backend run on one scenario."""

    outcome: SolverOutcome | None
    block_reason_code: str | None
    wall_time_ms: float
    error: str | None = None


@dataclass
class BenchRow:
    """Aggregate row for one scenario across all selected backends."""

    case: str
    scenario: str
    expected_outcome: SolverOutcome | None
    runs: dict[str, BenchRun] = field(default_factory=dict)


def _build_case_bundle(scenario_path: Path) -> tuple[SuiteScenario, CaseBundle]:
    """Construct a ``CaseBundle`` for one suite scenario without solving it.

    Mirrors the loader in ``scenario_suite.run_suite_scenario`` (which is
    read-only from this module's perspective), but stops short of dispatching
    to the reasoner so the bench can drive each backend directly.
    """
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
    base_db = load_mock_db(resolve_example_path(case_dir, suite_sc.mock_db_file))
    mock_db = _apply_db_overrides(base_db, suite_sc.mock_db_overrides)
    bundle = CaseBundle(
        logic_level=use_case.default_logic_level,
        domain=domain,
        intent=intent,
        mock_db=mock_db,
    )
    return suite_sc, bundle


def _try_instantiate(name: str) -> tuple[ReasonerBackend | None, str | None]:
    """Attempt to import + instantiate one backend; return (instance, error)."""
    try:
        if name == "z3":
            from reasoner_z3 import Z3Backend
            return Z3Backend(), None
        if name == "clingo":
            from reasoner_clingo import ClingoBackend
            return ClingoBackend(), None
        if name == "pysat":
            from reasoner_pysat import PySatBackend
            return PySatBackend(), None
        if name == "horn":
            from reasoner_horn import HornBackend
            return HornBackend(), None
        return None, f"unknown backend '{name}'"
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _run_one(backend: ReasonerBackend, bundle: CaseBundle) -> BenchRun:
    start = time.perf_counter()
    try:
        solution = backend.solve_case_bundle(bundle)
    except Exception as exc:
        wall = (time.perf_counter() - start) * 1000.0
        return BenchRun(outcome=None, block_reason_code=None, wall_time_ms=wall, error=f"{type(exc).__name__}: {exc}")
    wall = (time.perf_counter() - start) * 1000.0
    return BenchRun(
        outcome=solution.final_outcome,
        block_reason_code=solution.block_reason_code.value if solution.block_reason_code else None,
        wall_time_ms=wall,
    )


def _collect_scenarios() -> list[Path]:
    """Return the 15 seed scenario files (3 per benchmark case)."""
    paths: list[Path] = []
    for case in BENCHMARK_CASES:
        paths.extend(discover_suite_scenario_files_for_case(case))
    return paths


def _format_cell(run: BenchRun | None) -> str:
    if run is None:
        return "—"
    if run.error:
        return "error"
    if run.outcome is None:
        return "null"
    return run.outcome.value


def _agreement(rows: list[BenchRow], reference: str) -> dict[str, tuple[int, int]]:
    """Agreement counts of each backend with *reference* across all rows."""
    agree: dict[str, tuple[int, int]] = {}
    for row in rows:
        ref = row.runs.get(reference)
        if ref is None or ref.outcome is None:
            continue
        for name, run in row.runs.items():
            if name == reference or run.error or run.outcome is None:
                continue
            matched, total = agree.get(name, (0, 0))
            total += 1
            if run.outcome == ref.outcome:
                matched += 1
            agree[name] = (matched, total)
    return agree


def _mean_walltime(rows: list[BenchRow]) -> dict[str, float]:
    by_backend: dict[str, list[float]] = {}
    for row in rows:
        for name, run in row.runs.items():
            by_backend.setdefault(name, []).append(run.wall_time_ms)
    return {name: mean(vals) for name, vals in by_backend.items() if vals}


def _row_agreement_cell(row: BenchRow, backends: list[str]) -> str:
    """Return YES if every available backend agrees with the reference Z3 outcome."""
    reference = row.runs.get("z3")
    if reference is None or reference.outcome is None:
        return "—"
    for name in backends:
        if name == "z3":
            continue
        run = row.runs.get(name)
        if run is None or run.error or run.outcome is None:
            continue
        if run.outcome != reference.outcome:
            return "NO"
    return "YES"


def _render_table(rows: list[BenchRow], backends: list[str], availability: dict[str, str | None]) -> str:
    header_cols = ["scenario", "case", "expected_outcome"] + backends + ["agreement"]
    sep_cols = ["---"] * len(header_cols)
    lines = [
        "| " + " | ".join(header_cols) + " |",
        "|" + "|".join(sep_cols) + "|",
    ]
    for row in rows:
        expected = row.expected_outcome.value if row.expected_outcome else "—"
        cells = [row.scenario, row.case, expected]
        for name in backends:
            if availability[name] is not None:
                cells.append("unavailable")
            else:
                cells.append(_format_cell(row.runs.get(name)))
        cells.append(_row_agreement_cell(row, backends))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def _write_report(report: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date.today().isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    return out_path


def run_benchmark(backend_names: list[str]) -> tuple[int, Path, list[BenchRow], dict[str, str | None]]:
    """Execute the benchmark and return (regression_count, report_path, rows, availability)."""
    availability: dict[str, str | None] = {}
    backends: dict[str, ReasonerBackend] = {}
    for name in backend_names:
        backend, error = _try_instantiate(name)
        availability[name] = error
        if backend is not None:
            backends[name] = backend

    scenario_paths = _collect_scenarios()
    rows: list[BenchRow] = []
    for path in scenario_paths:
        suite_sc, bundle = _build_case_bundle(path)
        case_name = path.resolve().parents[1].name
        row = BenchRow(
            case=case_name,
            scenario=suite_sc.name,
            expected_outcome=suite_sc.expected_outcome,
        )
        for name, backend in backends.items():
            row.runs[name] = _run_one(backend, bundle)
        rows.append(row)

    regression_count = 0
    regressions: list[str] = []
    if "z3" in backends:
        for row in rows:
            ref = row.runs.get("z3")
            if row.expected_outcome is None or ref is None or ref.outcome is None:
                continue
            if ref.outcome != row.expected_outcome:
                regression_count += 1
                regressions.append(
                    f"  - {row.case}/{row.scenario}: expected {row.expected_outcome.value}, z3 returned {ref.outcome.value}"
                )

    agree = _agreement(rows, "z3") if "z3" in backends else {}
    walltimes = _mean_walltime(rows)

    summary_lines: list[str] = ["", "## Summary", ""]
    summary_lines.append("Backend availability:")
    for name in backend_names:
        err = availability[name]
        summary_lines.append(
            f"- `{name}`: " + ("OK" if err is None else f"unavailable ({err})")
        )
    summary_lines.append("")
    summary_lines.append("Agreement with Z3 (on scenarios where both ran):")
    if not agree:
        summary_lines.append("- (Z3 unavailable; no reference run.)")
    else:
        for name in backend_names:
            if name == "z3" or name not in agree:
                continue
            matched, total = agree[name]
            pct = (matched / total * 100.0) if total else 0.0
            summary_lines.append(f"- `{name}`: {matched}/{total} scenarios ({pct:.1f}%)")
    summary_lines.append("")
    summary_lines.append("Mean wall-time per backend (ms):")
    for name in backend_names:
        if name not in walltimes:
            continue
        summary_lines.append(f"- `{name}`: {walltimes[name]:.2f}")
    summary_lines.append("")
    if regressions:
        summary_lines.append("**Z3 regressions detected:**")
        summary_lines.extend(regressions)
        summary_lines.append("")

    divergences: list[str] = []
    if "z3" in backends:
        for row in rows:
            ref = row.runs.get("z3")
            if ref is None or ref.outcome is None:
                continue
            for name in backend_names:
                if name == "z3" or name not in backends:
                    continue
                run = row.runs.get(name)
                if run is None or run.error or run.outcome is None:
                    continue
                if run.outcome != ref.outcome:
                    divergences.append(
                        f"- {row.case}/{row.scenario}: z3={ref.outcome.value}, {name}={run.outcome.value}"
                    )
    if divergences:
        summary_lines.append("Backend divergences from Z3:")
        summary_lines.extend(divergences)
    else:
        summary_lines.append("No backend divergences from Z3 on scenarios where both ran.")

    table = _render_table(rows, backend_names, availability)
    report = (
        f"# Reasoner backend benchmark\n\n"
        f"Generated: {utc_timestamp()}\n\n"
        f"Scenarios: {len(rows)} ({', '.join(BENCHMARK_CASES)})\n\n"
        + table
        + "\n".join(summary_lines).rstrip()
        + "\n"
    )
    out_dir = FRAMEWORK_ROOT / "examples" / "review_runs" / "reasoner_benchmark"
    out_path = _write_report(report, out_dir)
    return regression_count, out_path, rows, availability


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    env_default = os.environ.get("FRAMEWORK_REASONER")
    default = env_default if env_default else ",".join(ALL_BACKEND_NAMES)
    parser.add_argument(
        "--backends",
        default=default,
        help="Comma-separated backend names (default: all four; or FRAMEWORK_REASONER if set).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    requested = [name.strip() for name in args.backends.split(",") if name.strip()]
    for name in requested:
        if name not in ALL_BACKEND_NAMES:
            print(f"Unknown backend name: {name}", file=sys.stderr)
            return 2

    regressions, out_path, rows, availability = run_benchmark(requested)

    rel_path = out_path.relative_to(FRAMEWORK_ROOT) if out_path.is_relative_to(FRAMEWORK_ROOT) else out_path
    print(f"Wrote benchmark report: {rel_path}")
    print(f"Scenarios: {len(rows)}")
    for name in requested:
        err = availability[name]
        status = "OK" if err is None else f"unavailable ({err})"
        print(f"  - {name}: {status}")
    if "z3" in availability and availability["z3"] is None:
        agree = _agreement(rows, "z3")
        for name in requested:
            if name in agree:
                matched, total = agree[name]
                print(f"  agreement with z3: {name} = {matched}/{total}")
        walltimes = _mean_walltime(rows)
        for name in requested:
            if name in walltimes:
                print(f"  mean wall_time: {name} = {walltimes[name]:.2f} ms")
    if regressions:
        print(f"REGRESSION: Z3 disagreed with expected_outcome on {regressions} scenario(s).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
