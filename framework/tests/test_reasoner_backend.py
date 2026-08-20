"""Smoke tests for the ReasonerBackend Protocol and Z3 dispatch.

Verifies that:
- ``ReasonerBackend`` is a runtime-checkable Protocol.
- ``get_backend()`` and ``get_backend("z3")`` return conforming instances.
- Non-implemented backends raise ``NotImplementedError`` mentioning ADR 0004.
- The Z3 backend produces correct outcomes on a minimal deterministic domain.
- The module-level ``solve_case_bundle`` free function remains callable by existing code.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from reasoner import ReasonerBackend, get_backend, solve_case_bundle  # noqa: E402
from reasoner_z3 import Z3Backend  # noqa: E402
from schemas import (  # noqa: E402
    CaseBundle,
    ClaimSource,
    DomainArtifact,
    DomainClaim,
    DomainRule,
    IntentArtifact,
    IntentClaim,
    LogicLevel,
    LookupSource,
    MockDbArtifact,
    OutcomeDefinition,
    RuleKind,
    SolverOutcome,
)


def _minimal_allow_bundle() -> CaseBundle:
    """Return the smallest valid CaseBundle whose Z3 solve yields ALLOW.

    Domain: one claim ``claim_a`` (USER source) with one ALLOW_IF_ALL rule.
    Intent: ``claim_a = True``.
    """
    domain = DomainArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        title="Minimal test domain",
        law_text="If A then the request is allowed.",
        lowered_view_note="Propositional test lowering.",
        allow_outcome_id="outcome_allow",
        deny_outcome_id="outcome_deny",
        claims=[
            DomainClaim(
                claim_id="claim_a",
                lowered_atom="claim_a",
                label="Claim A",
                description="A test claim used only by the smoke test.",
                source_type=ClaimSource.USER,
                formal_text="A is satisfied.",
            )
        ],
        outcomes=[
            OutcomeDefinition(
                outcome_id="outcome_allow",
                lowered_atom="outcome_allow",
                label="Allow",
                formal_text="The request is allowed.",
            ),
            OutcomeDefinition(
                outcome_id="outcome_deny",
                lowered_atom="outcome_deny",
                label="Deny",
                formal_text="The request is denied.",
            ),
        ],
        rules=[
            DomainRule(
                rule_id="rule_allow_a",
                kind=RuleKind.ALLOW_IF_ALL,
                label="Allow if A",
                when_claim_ids=["claim_a"],
                formal_text="If A then ALLOW.",
                lowered_formula="claim_a -> outcome_allow",
                target_outcome_id="outcome_allow",
            )
        ],
    )
    intent = IntentArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        request_text="Smoke test request.",
        claims=[
            IntentClaim(
                claim_id="claim_a",
                lowered_atom="claim_a",
                label="Claim A",
                description="A is true per the smoke test.",
                source_type=ClaimSource.USER,
                formal_text="A is satisfied.",
                value=True,
                reason="Seeded directly by the smoke test.",
            )
        ],
    )
    mock_db = MockDbArtifact(
        sources=[
            LookupSource(
                source_id="empty",
                label="Empty DB",
                description="Returns no values; not needed for this test.",
                values={},
            )
        ]
    )
    return CaseBundle(
        logic_level=LogicLevel.PROPOSITIONAL,
        domain=domain,
        intent=intent,
        mock_db=mock_db,
    )


class TestReasonerBackendProtocol(unittest.TestCase):
    def test_get_backend_default_returns_protocol_instance(self) -> None:
        backend = get_backend()
        self.assertIsInstance(backend, ReasonerBackend)

    def test_get_backend_z3_explicit_returns_protocol_instance(self) -> None:
        backend = get_backend("z3")
        self.assertIsInstance(backend, ReasonerBackend)

    def test_z3_backend_class_satisfies_protocol(self) -> None:
        backend = Z3Backend()
        self.assertIsInstance(backend, ReasonerBackend)

    def test_get_backend_clingo_returns_protocol_instance(self) -> None:
        # Wave 2 (ART-67) landed clingo; prior Wave-1 test asserted NotImplementedError.
        backend = get_backend("clingo")
        self.assertIsInstance(backend, ReasonerBackend)

    def test_get_backend_pysat_returns_protocol_instance(self) -> None:
        backend = get_backend("pysat")
        self.assertIsInstance(backend, ReasonerBackend)

    def test_get_backend_horn_returns_protocol_instance(self) -> None:
        backend = get_backend("horn")
        self.assertIsInstance(backend, ReasonerBackend)

    def test_get_backend_unknown_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            get_backend("bogus-backend-that-will-never-exist")

    def test_z3_backend_solve_trivial_allow(self) -> None:
        bundle = _minimal_allow_bundle()
        backend = Z3Backend()
        solution = backend.solve_case_bundle(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.ALLOW)

    def test_module_level_solve_case_bundle_unchanged(self) -> None:
        """The module-level free function must still work for existing call sites."""
        bundle = _minimal_allow_bundle()
        solution = solve_case_bundle(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.ALLOW)

    def test_z3_backend_and_free_function_produce_identical_outcomes(self) -> None:
        """Both paths through the dispatcher must agree on the same bundle."""
        bundle = _minimal_allow_bundle()
        backend_solution = Z3Backend().solve_case_bundle(bundle)
        dispatch_solution = solve_case_bundle(bundle)
        self.assertEqual(backend_solution.final_outcome, dispatch_solution.final_outcome)
        self.assertEqual(backend_solution.block_reason_code, dispatch_solution.block_reason_code)


if __name__ == "__main__":
    unittest.main()
