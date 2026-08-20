"""One-shot gold proposer for suite scenario missing-fact sets.

Runs each ``examples/*/scenarios/*.json`` through the deterministic suite
path (``run_suite_scenario``), then writes:

- ``expected_missing_facts`` from the solver's last informative snapshot
  (forced to ``[]`` on ALLOW/DENY even if the solver emitted extras)
- ``gold_confidence`` / ``gold_notes`` from circularity and source-type checks
- for ``section_120_demo`` only: ``expected_outcome`` and
  ``expected_reason_code`` from the solver (promotion to gold)

Do not invent missing facts by hand. Re-run after solver changes; operator
audits ``gold_confidence=low`` rows.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from schemas import ClaimSource, SolverOutcome  # noqa: E402
from scenario_suite import (  # noqa: E402
    discover_suite_scenario_files,
    run_suite_scenario,
)
from use_case_files import example_dir_for_scenario, load_use_case_from_dir  # noqa: E402


SECTION_120_CASE = "section_120_demo"
ALLOW_DENY = {SolverOutcome.ALLOW, SolverOutcome.DENY}
NEED_INFO = {
    SolverOutcome.NEED_DB_INFO,
    SolverOutcome.NEED_USER_INFO,
    SolverOutcome.NEED_EXPERT_JUDGMENT,
}

PREFERRED_KEY_ORDER = [
    "name",
    "description",
    "request_file",
    "law_file",
    "mock_db_file",
    "intent_assignments",
    "mock_db_overrides",
    "expected_outcome",
    "expected_reason_code",
    "expected_missing_facts",
    "gold_confidence",
    "gold_notes",
    "tags",
    "provenance",
    "intent_user_prompt_file",
    "domain_user_prompt_file",
]


def _case_name(scenario_path: Path) -> str:
    return scenario_path.resolve().parents[1].name


def _is_prompt_swap(scenario_path: Path, raw: dict) -> bool:
    name = str(raw.get("name") or scenario_path.stem)
    if "prompt-swap" in name or "prompt_swap" in name:
        return True
    tags = raw.get("tags") or []
    return any("prompt-swap" in str(tag) or "prompt_swap" in str(tag) for tag in tags)


def _source_of(catalog: dict, claim_id: str) -> ClaimSource | None:
    template = catalog.get(claim_id)
    return template.source_type if template is not None else None


def _classify_gold(
    *,
    outcome: SolverOutcome,
    solver_missing: list[str],
    catalog: dict,
    prompt_swap: bool,
) -> tuple[str, str]:
    """Return (gold_confidence, gold_notes)."""
    notes: list[str] = []
    unknown = [claim_id for claim_id in solver_missing if claim_id not in catalog]
    if unknown:
        notes.append("missing ids not in use-case catalog: " + ", ".join(unknown))

    if prompt_swap:
        notes.append("prompt-swap duplicate of allow; shares allow gold")

    if outcome in ALLOW_DENY:
        if solver_missing:
            notes.append(
                f"solver emitted missing facts on {outcome.value}: "
                + ", ".join(solver_missing)
                + "; gold records empty set"
            )
    elif outcome in NEED_INFO:
        if not solver_missing:
            notes.append(f"{outcome.value} with empty missing set")
        elif outcome == SolverOutcome.NEED_USER_INFO:
            non_user = [
                f"{claim_id} ({_source_of(catalog, claim_id).value})"
                for claim_id in solver_missing
                if claim_id in catalog and catalog[claim_id].source_type != ClaimSource.USER
            ]
            if non_user:
                notes.append("NEED_USER_INFO missing set includes non-user claims: " + ", ".join(non_user))
        elif outcome == SolverOutcome.NEED_DB_INFO:
            non_db = [
                f"{claim_id} ({_source_of(catalog, claim_id).value})"
                for claim_id in solver_missing
                if claim_id in catalog and catalog[claim_id].source_type != ClaimSource.DB
            ]
            if non_db:
                notes.append("NEED_DB_INFO missing set includes non-db claims: " + ", ".join(non_db))
        elif outcome == SolverOutcome.NEED_EXPERT_JUDGMENT:
            non_expert = [
                f"{claim_id} ({_source_of(catalog, claim_id).value})"
                for claim_id in solver_missing
                if claim_id in catalog and catalog[claim_id].source_type != ClaimSource.EXPERT
            ]
            if non_expert:
                notes.append(
                    "NEED_EXPERT_JUDGMENT missing set includes non-expert claims: " + ", ".join(non_expert)
                )

    confidence = "low" if notes else "high"
    return confidence, "; ".join(notes)


def _ordered_dump(raw: dict) -> dict:
    ordered: dict = {}
    for key in PREFERRED_KEY_ORDER:
        if key in raw:
            ordered[key] = raw[key]
    for key, value in raw.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def propose_for_file(scenario_path: Path) -> dict:
    """Update one scenario JSON in place; return a summary row."""
    raw = json.loads(scenario_path.read_text(encoding="utf-8"))
    result = run_suite_scenario(scenario_path)
    use_case = load_use_case_from_dir(example_dir_for_scenario(scenario_path))
    catalog = use_case.claim_by_id
    solver_missing = list(result.actual_missing_facts)
    outcome = result.actual_outcome
    prompt_swap = _is_prompt_swap(scenario_path, raw)

    if outcome in ALLOW_DENY:
        expected_missing = []
    else:
        expected_missing = solver_missing

    confidence, notes = _classify_gold(
        outcome=outcome,
        solver_missing=solver_missing,
        catalog=catalog,
        prompt_swap=prompt_swap,
    )

    case_name = _case_name(scenario_path)
    if case_name == SECTION_120_CASE:
        raw["expected_outcome"] = outcome.value
        raw["expected_reason_code"] = (
            result.actual_reason_code.value if result.actual_reason_code is not None else None
        )

    raw["expected_missing_facts"] = expected_missing
    raw["gold_confidence"] = confidence
    raw["gold_notes"] = notes

    scenario_path.write_text(
        json.dumps(_ordered_dump(raw), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "case": case_name,
        "name": raw.get("name", scenario_path.stem),
        "outcome": outcome.value,
        "expected_missing_facts": expected_missing,
        "solver_missing": solver_missing,
        "gold_confidence": confidence,
        "gold_notes": notes,
    }


def main() -> int:
    rows = [propose_for_file(path) for path in discover_suite_scenario_files()]
    high = sum(1 for row in rows if row["gold_confidence"] == "high")
    low = sum(1 for row in rows if row["gold_confidence"] == "low")
    print(f"Updated {len(rows)} scenarios: {high} high, {low} low gold_confidence")
    for row in rows:
        if row["gold_confidence"] == "low":
            print(f"  [low] {row['case']}/{row['name']}: {row['gold_notes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
