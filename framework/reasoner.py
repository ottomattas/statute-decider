"""Reasoner dispatcher: thin Protocol layer over pluggable symbolic backends.

The Z3 implementation lives in ``reasoner_z3.py`` (moved verbatim from this module).
See ``docs/adr/0004-reasoner-reselection.md`` for the backend shortlist and rationale.
"""

from __future__ import annotations

import os
from typing import Protocol, runtime_checkable

from schemas import CaseBundle, SolutionArtifact


@runtime_checkable
class ReasonerBackend(Protocol):
    """Structural interface every symbolic-reasoning backend must satisfy.

    Any class that implements ``solve_case_bundle`` with this signature satisfies
    the Protocol without explicit inheritance (structural subtyping).
    """

    def solve_case_bundle(self, case_bundle: CaseBundle) -> SolutionArtifact:
        """Solve one case bundle and return the full solution artifact."""
        ...


def get_backend(name: str | None = None) -> ReasonerBackend:
    """Return the active backend instance.

    Resolution order: explicit *name* argument -> ``FRAMEWORK_REASONER`` env var -> ``"z3"``.

    Known backends: ``"z3"`` (reference), ``"clingo"``, ``"pysat"``, ``"horn"``.
    ``"clingo"`` and ``"pysat"`` raise ``ImportError`` at instantiation when
    their optional dependency is missing; ``"horn"`` is pure-Python and always
    available. See ``docs/adr/0004-reasoner-reselection.md`` for rationale.
    """
    resolved = name if name is not None else os.environ.get("FRAMEWORK_REASONER", "z3")
    if resolved in ("z3", ""):
        from reasoner_z3 import Z3Backend  # noqa: PLC0415
        return Z3Backend()
    if resolved == "clingo":
        from reasoner_clingo import ClingoBackend  # noqa: PLC0415
        return ClingoBackend()
    if resolved == "pysat":
        from reasoner_pysat import PySatBackend  # noqa: PLC0415
        return PySatBackend()
    if resolved == "horn":
        from reasoner_horn import HornBackend  # noqa: PLC0415
        return HornBackend()
    raise ValueError(
        f"Unknown reasoner backend: {resolved}. See docs/adr/0004-reasoner-reselection.md."
    )


def solve_case_bundle(case_bundle: CaseBundle) -> SolutionArtifact:
    """Dispatch to the active backend's solve implementation.

    This function is the primary public entry point and preserves backward
    compatibility for all existing call sites. It routes through the
    ``ReasonerBackend`` Protocol so the active engine is controlled by the
    ``FRAMEWORK_REASONER`` environment variable.
    """
    return get_backend().solve_case_bundle(case_bundle)
