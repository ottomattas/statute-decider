"""Solver Protocol behind ``premise_outcome.method=solver``.

``solve(term_rule, term_claim, term_fact) -> premise_outcome``; z3 first,
other backends (pysat, clingo, horn, HOL) join as the same Protocol.
"""

from __future__ import annotations

from typing import Protocol

from statute_decider.core import ClaimSet, FactSet, PremiseOutcome, RuleSet, TermCatalog


class SolverBackend(Protocol):
    name: str
    version: str

    def solve(
        self,
        catalog: TermCatalog,
        rules: RuleSet,
        claims: ClaimSet,
        facts: FactSet,
    ) -> PremiseOutcome: ...


_REGISTRY: dict[str, type] = {}


def register_solver(name: str):
    def wrap(cls: type) -> type:
        _REGISTRY[name] = cls
        return cls

    return wrap


def get_solver(name: str) -> SolverBackend:
    try:
        factory = _REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"Unknown solver {name!r}. Known: {sorted(_REGISTRY)}") from exc
    return factory()


def solver_names() -> list[str]:
    return sorted(_REGISTRY)
