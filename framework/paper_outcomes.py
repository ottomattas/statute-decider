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


def missing_facts_from_solution(solution: SolutionArtifact) -> list[str]:
    """Sorted unique missing_db_claim_ids + missing_user_claim_ids, outcome-aware.

    A decided case (paper ALLOW/DENY) has an empty missing set by definition:
    facts that earlier snapshots listed as missing but a later stage (e.g. DB
    lookup) resolved are not missing. An undecided case takes the last snapshot
    that lists any ids, because some terminal outcomes (e.g. UNVERIFIABLE_CLAIM)
    end with empty lists in the final snapshot even though facts remain
    unresolved. (Gold audit 2026-08-26: the previous unconditional walk-back
    inflated the missing set on decided-via-DB cases.)
    """
    if to_paper_outcome(solution.final_outcome) != _NEED_MORE_INFO:
        return []
    for snapshot in reversed(solution.snapshots or []):
        ids = _snapshot_missing_ids(snapshot)
        if ids:
            return ids
    return []


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
