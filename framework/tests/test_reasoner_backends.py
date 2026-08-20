"""Smoke + parity tests for the three Wave-2 reasoner backends (ADR 0004).

Each backend is treated as optional: clingo and PySAT depend on external
packages, Horn is pure-Python. Tests skip cleanly when a backend's import
fails. Parity coverage runs all available backends over the 15 seed
scenarios and reports mismatches collectively.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from bench_reasoners import BENCHMARK_CASES, _build_case_bundle  # noqa: E402
from reasoner import ReasonerBackend, get_backend  # noqa: E402
from scenario_suite import discover_suite_scenario_files_for_case  # noqa: E402
from schemas import SolverOutcome  # noqa: E402


try:  # pragma: no cover - availability probe
    import clingo  # type: ignore  # noqa: F401
    CLINGO_AVAILABLE = True
except ImportError:
    CLINGO_AVAILABLE = False

try:  # pragma: no cover - availability probe
    from pysat.solvers import Glucose3  # type: ignore  # noqa: F401
    PYSAT_AVAILABLE = True
except ImportError:
    PYSAT_AVAILABLE = False


def _solve_scenario(backend: ReasonerBackend, scenario_path: Path) -> SolverOutcome:
    _, bundle = _build_case_bundle(scenario_path)
    return backend.solve_case_bundle(bundle).final_outcome


def _find_scenario(case: str, name: str) -> Path:
    for path in discover_suite_scenario_files_for_case(case):
        if path.stem == name:
            return path
    raise FileNotFoundError(f"scenario {case}/{name} not found")


class TestHornBackend(unittest.TestCase):
    def test_horn_satisfies_protocol(self) -> None:
        from reasoner_horn import HornBackend
        backend = HornBackend()
        self.assertIsInstance(backend, ReasonerBackend)

    def test_horn_always_available_via_dispatcher(self) -> None:
        backend = get_backend("horn")
        self.assertIsInstance(backend, ReasonerBackend)


class TestClingoBackend(unittest.TestCase):
    @unittest.skipIf(not CLINGO_AVAILABLE, "clingo optional dep not installed")
    def test_clingo_satisfies_protocol(self) -> None:
        from reasoner_clingo import ClingoBackend
        backend = ClingoBackend()
        self.assertIsInstance(backend, ReasonerBackend)

    @unittest.skipIf(not CLINGO_AVAILABLE, "clingo optional dep not installed")
    def test_get_backend_clingo_returns_instance_when_installed(self) -> None:
        backend = get_backend("clingo")
        self.assertIsInstance(backend, ReasonerBackend)

    @unittest.skipIf(CLINGO_AVAILABLE, "clingo is installed; cannot probe missing-import path")
    def test_get_backend_clingo_raises_import_error_when_missing(self) -> None:
        with self.assertRaises(ImportError):
            get_backend("clingo")


class TestPySatBackend(unittest.TestCase):
    @unittest.skipIf(not PYSAT_AVAILABLE, "python-sat optional dep not installed")
    def test_pysat_satisfies_protocol(self) -> None:
        from reasoner_pysat import PySatBackend
        backend = PySatBackend()
        self.assertIsInstance(backend, ReasonerBackend)

    @unittest.skipIf(not PYSAT_AVAILABLE, "python-sat optional dep not installed")
    def test_get_backend_pysat_returns_instance_when_installed(self) -> None:
        backend = get_backend("pysat")
        self.assertIsInstance(backend, ReasonerBackend)

    @unittest.skipIf(PYSAT_AVAILABLE, "python-sat is installed; cannot probe missing-import path")
    def test_get_backend_pysat_raises_import_error_when_missing(self) -> None:
        with self.assertRaises(ImportError):
            get_backend("pysat")


class TestDispatcher(unittest.TestCase):
    def test_get_backend_bogus_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            get_backend("bogus-backend")


class TestSection120Scenarios(unittest.TestCase):
    """Per-backend outcome smoke tests on the section_120_demo allow/deny scenarios."""

    def _each_available_backend(self):
        backends: list[tuple[str, ReasonerBackend]] = [("horn", get_backend("horn"))]
        if CLINGO_AVAILABLE:
            backends.append(("clingo", get_backend("clingo")))
        if PYSAT_AVAILABLE:
            backends.append(("pysat", get_backend("pysat")))
        return backends

    def test_section_120_allow(self) -> None:
        path = _find_scenario("section_120_demo", "allow")
        for name, backend in self._each_available_backend():
            with self.subTest(backend=name):
                self.assertEqual(_solve_scenario(backend, path), SolverOutcome.ALLOW)

    def test_section_120_deny(self) -> None:
        path = _find_scenario("section_120_demo", "deny")
        for name, backend in self._each_available_backend():
            with self.subTest(backend=name):
                self.assertEqual(_solve_scenario(backend, path), SolverOutcome.DENY)


_UNCERTAINTY_TAGS = frozenset({"uncertainty", "u1", "u2", "u3", "u4", "u6", "u7", "u9", "u10", "u11", "u12"})


class TestSeedScenarioParity(unittest.TestCase):
    """All seed scenarios agree with their expected outcome on every available backend.

    Scenarios that exercise the Wave-2 U-code taxonomy (UNVERIFIABLE_CLAIM /
    NEED_EXPERT_JUDGMENT) are skipped here because only the z3 backend wires up
    :mod:`uncertainty_routing`; the other backends fall back to the legacy
    NEED_DB_INFO / NEED_USER_INFO / ALLOW paths by design.
    """

    def test_each_backend_matches_expected_outcomes(self) -> None:
        backends: list[tuple[str, ReasonerBackend]] = [("horn", get_backend("horn"))]
        if CLINGO_AVAILABLE:
            backends.append(("clingo", get_backend("clingo")))
        if PYSAT_AVAILABLE:
            backends.append(("pysat", get_backend("pysat")))

        mismatches: list[str] = []
        for case in BENCHMARK_CASES:
            for scenario_path in discover_suite_scenario_files_for_case(case):
                suite_sc, bundle = _build_case_bundle(scenario_path)
                if suite_sc.expected_outcome is None:
                    continue
                if _UNCERTAINTY_TAGS.intersection(suite_sc.tags):
                    continue
                for name, backend in backends:
                    actual = backend.solve_case_bundle(bundle).final_outcome
                    if actual != suite_sc.expected_outcome:
                        mismatches.append(
                            f"{case}/{suite_sc.name} via {name}: "
                            f"expected {suite_sc.expected_outcome.value}, got {actual.value}"
                        )
        if mismatches:
            self.fail("Backend mismatches against expected_outcome:\n  - " + "\n  - ".join(mismatches))


if __name__ == "__main__":
    unittest.main()
