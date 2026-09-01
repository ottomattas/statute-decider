"""Solver backends behind the ``premise_outcome`` node (Protocol + registry)."""

from statute_decider.solvers.base import SolverBackend, get_solver, register_solver, solver_names

# Importing backends registers them; z3 is optional (extra: .[solvers]).
try:  # pragma: no cover
    from statute_decider.solvers.z3_backend import Z3Solver  # noqa: F401
except ImportError:  # pragma: no cover
    pass

__all__ = ["SolverBackend", "get_solver", "register_solver", "solver_names"]
