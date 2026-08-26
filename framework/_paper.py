"""Local fallback for the paper 3-way outcome mapping (WS-A owns ``paper_outcomes``).

``experiment_ii`` imports ``paper_outcomes`` when that module exists and falls
back to this copy so the LLM-only runner can land first. ALLOW/DENY stay;
every other solver outcome maps to NEED_MORE_INFO. Fine-grained solver
outcomes remain on the runtime row as secondary reporting.
"""

from __future__ import annotations

from collections.abc import Iterable

from schemas import SolutionArtifact, SolverOutcome

PAPER_OUTCOMES = ("ALLOW", "DENY", "NEED_MORE_INFO")


def to_paper_outcome(outcome: SolverOutcome | str) -> str:
    """ALLOW stays ALLOW, DENY stays DENY, everything else -> NEED_MORE_INFO."""
    value = outcome.value if isinstance(outcome, SolverOutcome) else str(outcome)
    if value in ("ALLOW", "DENY"):
        return value
    return "NEED_MORE_INFO"


def missing_facts_from_solution(solution: SolutionArtifact) -> list[str]:
    """Sorted unique missing DB + user claim ids, outcome-aware.

    A decided case (paper ALLOW/DENY) has an empty missing set by definition:
    facts that earlier snapshots listed as missing but a later stage (e.g. DB
    lookup) resolved are not missing. An undecided case takes the last snapshot
    that lists any ids, because some terminal outcomes (e.g. UNVERIFIABLE_CLAIM)
    end with empty lists in the final snapshot even though facts remain
    unresolved. (Gold audit 2026-08-26: the previous unconditional walk-back
    inflated the missing set on decided-via-DB cases.)
    """
    if to_paper_outcome(solution.final_outcome) != "NEED_MORE_INFO":
        return []
    snapshots = solution.snapshots or []
    if not snapshots:
        return sorted(set(solution.unresolved_claim_ids))
    for snap in reversed(snapshots):
        ids = set(snap.missing_db_claim_ids).union(snap.missing_user_claim_ids)
        if ids:
            return sorted(ids)
    return []


def fact_set_precision_recall(expected: Iterable[str], actual: Iterable[str]) -> tuple[float, float]:
    """Set precision/recall for missing-fact ids.

    Empty expected and empty actual => (1.0, 1.0).
    Empty expected and nonempty actual => (0.0, 1.0) — nothing to recall.
    Nonempty expected and empty actual => (1.0, 0.0) — no false positives.
    Otherwise tp/len(actual) and tp/len(expected).
    """
    exp = set(expected)
    act = set(actual)
    if not exp and not act:
        return (1.0, 1.0)
    if not exp and act:
        return (0.0, 1.0)
    if exp and not act:
        return (1.0, 0.0)
    true_positive = len(exp & act)
    return (true_positive / len(act), true_positive / len(exp))
