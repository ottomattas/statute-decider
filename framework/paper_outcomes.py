"""Scoring-layer mapping from fine-grained solver outcomes to paper 3-outcomes.

The JURIX experiment scores ALLOW / DENY / NEED_MORE_INFO. Fine-grained
``SolverOutcome`` values stay on the solver and the suite; this module does
not change the enum. Fact-set precision/recall is defined on missing claim
ids (DB + user) taken from the last informative solve snapshot.
"""

from __future__ import annotations

from collections.abc import Iterable

from schemas import SolutionArtifact, SolveSnapshot, SolverOutcome


PAPER_OUTCOMES = ("ALLOW", "DENY", "NEED_MORE_INFO")

_TERMINAL_ALLOW = "ALLOW"
_TERMINAL_DENY = "DENY"
_NEED_MORE_INFO = "NEED_MORE_INFO"


def to_paper_outcome(outcome: SolverOutcome | str) -> str:
    """ALLOW stays ALLOW, DENY stays DENY, everything else -> NEED_MORE_INFO."""
    value = outcome.value if isinstance(outcome, SolverOutcome) else str(outcome)
    if value == _TERMINAL_ALLOW:
        return _TERMINAL_ALLOW
    if value == _TERMINAL_DENY:
        return _TERMINAL_DENY
    return _NEED_MORE_INFO


def _snapshot_missing_ids(snapshot: SolveSnapshot) -> list[str]:
    """Unique missing DB + user claim ids from one snapshot, sorted."""
    return sorted(set(snapshot.missing_db_claim_ids) | set(snapshot.missing_user_claim_ids))


def _last_informative_snapshot(solution: SolutionArtifact) -> SolveSnapshot | None:
    """Prefer the last snapshot that lists any missing ids; else the last snapshot."""
    if not solution.snapshots:
        return None
    for snapshot in reversed(solution.snapshots):
        if snapshot.missing_db_claim_ids or snapshot.missing_user_claim_ids:
            return snapshot
    return solution.snapshots[-1]


def missing_facts_from_solution(solution: SolutionArtifact) -> list[str]:
    """Sorted unique missing_db_claim_ids + missing_user_claim_ids from the last informative snapshot."""
    snapshot = _last_informative_snapshot(solution)
    if snapshot is None:
        return []
    return _snapshot_missing_ids(snapshot)


def fact_set_precision_recall(expected: Iterable[str], actual: Iterable[str]) -> tuple[float, float]:
    """Set precision/recall over missing-fact ids.

    Empty expected AND empty actual => (1.0, 1.0).
    Empty expected, nonempty actual => precision 0.0, recall 1.0 (nothing to recall).
    Nonempty expected, empty actual => precision 1.0 (no false positives), recall 0.0.
    Otherwise precision = |tp| / |actual| and recall = |tp| / |expected|.
    """
    exp = set(expected)
    act = set(actual)
    if not exp and not act:
        return (1.0, 1.0)
    tp = len(exp & act)
    precision = (tp / len(act)) if act else 1.0
    recall = (tp / len(exp)) if exp else 1.0
    return (precision, recall)
