"""Exhaustive truth-table enumeration for one example case.

For a use case with ``n`` claims we enumerate all ``2**n`` boolean
assignments, run :func:`reasoner.solve_case_bundle` for each, and record
the resulting ``(outcome, block_reason_code)``. When ``n > max_vars`` the
enumeration is skipped so that large cases do not blow up the runtime.

The module exposes a small public surface:

* :class:`TruthTableRow` - one enumerated assignment and its solver result.
* :class:`TruthTableReport` - full enumeration for one case plus skip
  metadata when the case was too large.
* :func:`enumerate_truth_table` - run the enumeration for one case.
* :func:`render_markdown` / :func:`write_markdown` - render and persist a
  report as a Markdown table under
  ``framework/examples/<case>/review_runs/truth_tables/truth_table.md``.

The helper uses only public APIs from the existing extraction and
reasoner pipeline (``logic_levels``, ``mock_db``, ``reasoner``,
``scenario_suite._apply_db_overrides``); it does not reach into any
solver-backend internals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import Iterable

from logic_levels import build_domain_artifact, build_intent_artifact
from metadata import utc_timestamp
from mock_db import load_mock_db
from reasoner import solve_case_bundle
from scenario_suite import _apply_db_overrides
from schemas import (
    BlockReasonCode,
    CaseBundle,
    ExtractionRunMetadata,
    SolverOutcome,
)
from use_case_files import EXAMPLES_ROOT, FRAMEWORK_ROOT, load_use_case_from_dir


DEFAULT_MAX_VARS = 6


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TruthTableRow:
    """One enumerated assignment and its solver result."""

    assignment: dict[str, bool]
    outcome: SolverOutcome
    reason_code: BlockReasonCode | None


@dataclass
class TruthTableReport:
    """Full truth-table enumeration for one example case."""

    case_name: str
    claim_ids: list[str]
    rows: list[TruthTableRow] = field(default_factory=list)
    skipped: bool = False
    skip_reason: str = ""

    @property
    def n_vars(self) -> int:
        return len(self.claim_ids)

    @property
    def n_rows(self) -> int:
        return len(self.rows)


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------


def _iter_assignments(claim_ids: list[str]) -> Iterable[dict[str, bool]]:
    """Yield every ``2**n`` boolean assignment over ``claim_ids`` in canonical order."""
    for combo in product((False, True), repeat=len(claim_ids)):
        yield dict(zip(claim_ids, combo))


def _resolve_case_dir(case_name: str) -> Path:
    """Return the example directory for ``case_name``."""
    return EXAMPLES_ROOT / case_name


def enumerate_truth_table(
    case_name: str,
    *,
    max_vars: int = DEFAULT_MAX_VARS,
    mock_db_file: str = "mock_db.json",
    law_file: str = "law.txt",
) -> TruthTableReport:
    """Enumerate every boolean assignment for one case and return a report.

    Parameters
    ----------
    case_name:
        Name of the example directory under ``framework/examples/``.
    max_vars:
        Maximum number of claims to enumerate. When the use case exposes
        more claims, the enumeration is skipped and ``skipped=True`` is
        set on the returned report (no rows are produced).
    mock_db_file:
        Mock-DB fixture to load as the base DB. Per-assignment overrides
        are applied on top of this fixture via
        :func:`scenario_suite._apply_db_overrides`.
    law_file:
        Law fixture to load alongside the use case.
    """
    case_dir = _resolve_case_dir(case_name)
    use_case = load_use_case_from_dir(case_dir)
    claim_ids = [claim.claim_id for claim in use_case.claims]
    report = TruthTableReport(case_name=case_name, claim_ids=list(claim_ids))

    if len(claim_ids) > max_vars:
        report.skipped = True
        report.skip_reason = (
            f"Case has {len(claim_ids)} claims, exceeding max_vars={max_vars}; "
            "truth-table enumeration skipped."
        )
        return report

    law_path = case_dir / law_file
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

    base_db_path = case_dir / mock_db_file
    base_db = load_mock_db(base_db_path)

    for assignment in _iter_assignments(claim_ids):
        intent = build_intent_artifact(
            use_case,
            "",
            use_case.default_logic_level,
            dict(assignment),
            run_metadata=run_meta,
        )
        mock_db = _apply_db_overrides(base_db, {k: v for k, v in assignment.items()})
        bundle = CaseBundle(
            logic_level=use_case.default_logic_level,
            domain=domain,
            intent=intent,
            mock_db=mock_db,
        )
        solution = solve_case_bundle(bundle)
        report.rows.append(
            TruthTableRow(
                assignment=dict(assignment),
                outcome=solution.final_outcome,
                reason_code=solution.block_reason_code,
            )
        )

    return report


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _outcome_str(outcome: SolverOutcome) -> str:
    return outcome.value


def _reason_str(code: BlockReasonCode | None) -> str:
    return code.value if code is not None else "—"


def _bool_str(value: bool) -> str:
    return "T" if value else "F"


def render_markdown(report: TruthTableReport) -> str:
    """Render a ``TruthTableReport`` as a Markdown document."""
    lines: list[str] = []
    lines.append(f"# Truth table - {report.case_name}")
    lines.append("")
    if report.skipped:
        lines.append(f"_Enumeration skipped._ {report.skip_reason}")
        lines.append("")
        lines.append(f"- claims: {len(report.claim_ids)}")
        if report.claim_ids:
            lines.append(f"- claim ids: {', '.join(report.claim_ids)}")
        return "\n".join(lines) + "\n"

    lines.append(f"- claims: {report.n_vars}")
    lines.append(f"- rows: {report.n_rows}")
    lines.append("")
    header_cells = list(report.claim_ids) + ["outcome", "reason_code"]
    separator_cells = ["---"] * len(header_cells)
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "|".join(separator_cells) + "|")
    for row in report.rows:
        values = [_bool_str(row.assignment[cid]) for cid in report.claim_ids]
        values.extend([_outcome_str(row.outcome), _reason_str(row.reason_code)])
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def write_markdown(report: TruthTableReport) -> Path:
    """Write the Markdown report for ``report.case_name`` and return its path."""
    out_dir = FRAMEWORK_ROOT / "examples" / report.case_name / "review_runs" / "truth_tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "truth_table.md"
    out_path.write_text(render_markdown(report), encoding="utf-8")
    return out_path
