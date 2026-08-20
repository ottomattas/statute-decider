"""clingo (ASP) backend for the monotonic rule fragment.

Translates ``ALLOW_IF_ALL`` / ``DENY_IF_ALL`` rules into plain ASP
derivations and ``SET_FALSE_IF_ALL`` rules into integrity constraints.
Unknown claims are modelled as choice atoms so that entailment is
computed over the full stable-model set (atom in every model =
entailed True; atom in no model = entailed False; otherwise unknown).

Abductive support (U1..U12 uncertainty codes, missing-premise hypothesising)
is a Wave 3 extension — TODO once ART-64 lands.

A failed ``import clingo`` keeps the class importable; instantiation then
raises ``ImportError`` with a pointer to ``framework/requirements.txt``.
"""

from __future__ import annotations

from typing import Any

try:
    import clingo  # type: ignore
    _CLINGO_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:  # pragma: no cover - exercised only when clingo missing
    clingo = None  # type: ignore[assignment]
    _CLINGO_IMPORT_ERROR = exc

from reasoner_horn import solve_case_bundle_with_engine
from schemas import (
    CaseBundle,
    DomainArtifact,
    RuleKind,
    SolutionArtifact,
)


def _atom(name: str) -> str:
    """Render a claim/outcome id as a valid ASP atom.

    Atoms in the seed scenarios are already valid lowercase identifiers
    (``snake_case``). Digits at the front would be invalid; we prefix with
    an ``a_`` guard as a defensive measure.
    """
    if name and name[0].isdigit():
        return f"a_{name}"
    return name


def _run_clingo(domain: DomainArtifact, facts: dict[str, bool | None]) -> dict[str, Any]:
    """Ground + solve the ASP program and compute per-atom cautious/brave entailment."""
    if clingo is None:  # pragma: no cover - instantiation path already guards
        return {
            "engine": "clingo",
            "base_status": "error",
            "error": "clingo not installed",
            "claim_values": {claim.claim_id: None for claim in domain.claims},
            "outcome_values": {outcome.outcome_id: None for outcome in domain.outcomes},
        }

    claim_ids = [claim.claim_id for claim in domain.claims]
    outcome_ids = [outcome.outcome_id for outcome in domain.outcomes]

    lines: list[str] = []
    for claim_id in claim_ids:
        lines.append(f"{{ {_atom(claim_id)} }}.")
    for rule in domain.rules:
        body = ", ".join(_atom(pid) for pid in rule.when_claim_ids)
        if rule.kind == RuleKind.ALLOW_IF_ALL or rule.kind == RuleKind.DENY_IF_ALL:
            lines.append(f"{_atom(rule.target_outcome_id)} :- {body}.")
        elif rule.kind == RuleKind.SET_FALSE_IF_ALL:
            lines.append(f":- {body}, {_atom(rule.target_claim_id)}.")
    for claim_id, value in facts.items():
        if value is True:
            lines.append(f":- not {_atom(claim_id)}.")
        elif value is False:
            lines.append(f":- {_atom(claim_id)}.")
    program = "\n".join(lines)

    tracked_atoms = {_atom(cid): cid for cid in claim_ids}
    tracked_atoms.update({_atom(oid): oid for oid in outcome_ids})
    appears_in_all = {raw: True for raw in claim_ids + outcome_ids}
    appears_in_some = {raw: False for raw in claim_ids + outcome_ids}
    model_count = 0

    try:
        ctl = clingo.Control(["--models=0"])
        ctl.add("base", [], program)
        ctl.ground([("base", [])])

        def on_model(model: "clingo.Model") -> None:  # type: ignore[name-defined]
            nonlocal model_count
            model_count += 1
            atoms_in_model = {str(sym) for sym in model.symbols(atoms=True)}
            for atom_str, raw_id in tracked_atoms.items():
                if atom_str in atoms_in_model:
                    appears_in_some[raw_id] = True
                else:
                    appears_in_all[raw_id] = False

        res = ctl.solve(on_model=on_model)
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "engine": "clingo",
            "base_status": "error",
            "error": str(exc),
            "claim_values": {cid: None for cid in claim_ids},
            "outcome_values": {oid: None for oid in outcome_ids},
        }

    if not res.satisfiable or model_count == 0:
        return {
            "engine": "clingo",
            "base_status": "unsat",
            "claim_values": {cid: None for cid in claim_ids},
            "outcome_values": {oid: None for oid in outcome_ids},
        }

    def entailed(raw_id: str) -> bool | None:
        if appears_in_all[raw_id]:
            return True
        if not appears_in_some[raw_id]:
            return False
        return None

    return {
        "engine": "clingo",
        "base_status": "sat",
        "claim_values": {cid: entailed(cid) for cid in claim_ids},
        "outcome_values": {oid: entailed(oid) for oid in outcome_ids},
    }


class ClingoBackend:
    """ASP-based reasoner satisfying the ``ReasonerBackend`` Protocol."""

    def __init__(self) -> None:
        if clingo is None:
            raise ImportError(
                "clingo is not installed. Install it via "
                "`pip install -r framework/requirements.txt` "
                "(see ADR 0004)."
            ) from _CLINGO_IMPORT_ERROR

    def solve_case_bundle(self, case_bundle: CaseBundle) -> SolutionArtifact:
        return solve_case_bundle_with_engine(
            case_bundle,
            engine="clingo",
            run_engine=_run_clingo,
        )
