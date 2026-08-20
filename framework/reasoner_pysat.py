"""PySAT backend for the monotonic rule fragment.

Encodes each rule as a Horn clause over a propositional variable pool:

* ``ALLOW_IF_ALL`` / ``DENY_IF_ALL``: ``(¬p1 ∨ … ∨ ¬pn ∨ target_outcome)``.
* ``SET_FALSE_IF_ALL``: ``(¬p1 ∨ … ∨ ¬pn ∨ ¬target_claim)``.

Known-true / known-false facts are added as unit clauses. Entailment of
any individual atom ``x`` is decided by the standard two-call pattern used
by the Z3 reference: ``x`` is entailed-True iff ``theory ∪ facts ∪ {¬x}``
is UNSAT, entailed-False iff ``theory ∪ facts ∪ {x}`` is UNSAT, otherwise
unknown.

Abductive support is a Wave 3 extension (TODO).

If ``pysat`` is missing, the class stays importable; instantiation raises
``ImportError`` with a pointer to ``framework/requirements.txt``.
"""

from __future__ import annotations

from typing import Any

try:
    from pysat.formula import IDPool  # type: ignore
    from pysat.solvers import Glucose3  # type: ignore
    _PYSAT_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:  # pragma: no cover - exercised only when pysat missing
    IDPool = None  # type: ignore[assignment]
    Glucose3 = None  # type: ignore[assignment]
    _PYSAT_IMPORT_ERROR = exc

from reasoner_horn import solve_case_bundle_with_engine
from schemas import (
    CaseBundle,
    DomainArtifact,
    RuleKind,
    SolutionArtifact,
)


def _build_clauses(domain: DomainArtifact, facts: dict[str, bool | None]) -> tuple[list[list[int]], dict[str, int]]:
    """Return (clauses, var_by_id) for the domain + facts."""
    pool = IDPool()
    var_by_id: dict[str, int] = {}

    def _var(name: str) -> int:
        if name not in var_by_id:
            var_by_id[name] = pool.id(name)
        return var_by_id[name]

    for claim in domain.claims:
        _var(claim.claim_id)
    for outcome in domain.outcomes:
        _var(outcome.outcome_id)
    for rule in domain.rules:
        for pid in rule.when_claim_ids:
            _var(pid)
        if rule.target_claim_id:
            _var(rule.target_claim_id)
        if rule.target_outcome_id:
            _var(rule.target_outcome_id)

    clauses: list[list[int]] = []
    for rule in domain.rules:
        body = [-_var(pid) for pid in rule.when_claim_ids]
        if rule.kind == RuleKind.ALLOW_IF_ALL or rule.kind == RuleKind.DENY_IF_ALL:
            clauses.append(body + [_var(rule.target_outcome_id)])
        elif rule.kind == RuleKind.SET_FALSE_IF_ALL:
            clauses.append(body + [-_var(rule.target_claim_id)])

    for claim_id, value in facts.items():
        if claim_id not in var_by_id or value is None:
            continue
        lit = _var(claim_id) if value else -_var(claim_id)
        clauses.append([lit])

    return clauses, var_by_id


def _solve(clauses: list[list[int]], assumptions: list[int]) -> bool:
    """Return True iff the CNF + assumptions is satisfiable."""
    solver = Glucose3(bootstrap_with=clauses)
    try:
        return bool(solver.solve(assumptions=assumptions))
    finally:
        solver.delete()


def _run_pysat(domain: DomainArtifact, facts: dict[str, bool | None]) -> dict[str, Any]:
    """Build the CNF and compute per-atom entailment via two SAT calls each."""
    if Glucose3 is None or IDPool is None:  # pragma: no cover - guarded at instantiation
        return {
            "engine": "pysat",
            "base_status": "error",
            "error": "pysat not installed",
            "claim_values": {claim.claim_id: None for claim in domain.claims},
            "outcome_values": {outcome.outcome_id: None for outcome in domain.outcomes},
        }

    claim_ids = [claim.claim_id for claim in domain.claims]
    outcome_ids = [outcome.outcome_id for outcome in domain.outcomes]

    try:
        clauses, var_by_id = _build_clauses(domain, facts)
        if not _solve(clauses, assumptions=[]):
            return {
                "engine": "pysat",
                "base_status": "unsat",
                "claim_values": {cid: None for cid in claim_ids},
                "outcome_values": {oid: None for oid in outcome_ids},
            }

        def entailed(atom: str) -> bool | None:
            if atom not in var_by_id:
                return None
            var = var_by_id[atom]
            if not _solve(clauses, assumptions=[-var]):
                return True
            if not _solve(clauses, assumptions=[var]):
                return False
            return None

        return {
            "engine": "pysat",
            "base_status": "sat",
            "claim_values": {cid: entailed(cid) for cid in claim_ids},
            "outcome_values": {oid: entailed(oid) for oid in outcome_ids},
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "engine": "pysat",
            "base_status": "error",
            "error": str(exc),
            "claim_values": {cid: None for cid in claim_ids},
            "outcome_values": {oid: None for oid in outcome_ids},
        }


class PySatBackend:
    """PySAT CNF-based reasoner satisfying the ``ReasonerBackend`` Protocol."""

    def __init__(self) -> None:
        if Glucose3 is None or IDPool is None:
            raise ImportError(
                "python-sat is not installed. Install it via "
                "`pip install -r framework/requirements.txt` "
                "(see ADR 0004)."
            ) from _PYSAT_IMPORT_ERROR

    def solve_case_bundle(self, case_bundle: CaseBundle) -> SolutionArtifact:
        return solve_case_bundle_with_engine(
            case_bundle,
            engine="pysat",
            run_engine=_run_pysat,
        )
