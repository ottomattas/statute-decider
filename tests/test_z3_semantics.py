"""Unit tests of the staged, warrant-aware solver semantics on a mini-case."""

import pytest

from statute_decider.core import (
    Availability,
    ClaimPremise,
    ClaimSet,
    Evidence,
    FactPremise,
    FactSet,
    MissingReason,
    OutcomeState,
    RuleKind,
    RulePremise,
    RuleSet,
    Term,
    TermCatalog,
    Warrant,
)
from statute_decider.solvers import get_solver


def catalog() -> TermCatalog:
    return TermCatalog(
        statute_id="mini",
        terms=[
            Term(term_id="asked_nicely", label="", evidence=Evidence.USER),
            Term(term_id="is_registered", label="", evidence=Evidence.REGISTER),
            Term(term_id="is_banned", label="", evidence=Evidence.REGISTER),
        ],
    )


def rules() -> RuleSet:
    return RuleSet(
        statute_id="mini",
        allow_outcome_id="allowed",
        deny_outcome_id="denied",
        rules=[
            RulePremise(
                premise_id="allow_main",
                rule_kind=RuleKind.ALLOW_IF_ALL,
                when_term_ids=["asked_nicely", "is_registered"],
                target_outcome_id="allowed",
            ),
            RulePremise(
                premise_id="deny_ban",
                rule_kind=RuleKind.DENY_IF_ALL,
                when_term_ids=["is_banned"],
                target_outcome_id="denied",
            ),
        ],
    )


def claims(**values: bool) -> ClaimSet:
    return ClaimSet(
        scenario_id="s",
        claims=[
            ClaimPremise(premise_id=f"claim_{k}", term_id=k, value=v) for k, v in values.items()
        ],
    )


def fact(term_id: str, value: bool, warrant: Warrant = Warrant.AUTHORITATIVE) -> FactPremise:
    return FactPremise(
        premise_id=f"fact_{term_id}",
        term_id=term_id,
        value=value,
        register_id="reg",
        record_id="main",
        field=term_id,
        warrant=warrant,
    )


@pytest.fixture
def z3():
    return get_solver("z3")


def test_allow_via_register_fact(z3):
    facts = FactSet(scenario_id="s", facts=[fact("is_registered", True), fact("is_banned", False)])
    out = z3.solve(catalog(), rules(), claims(asked_nicely=True), facts)
    assert out.state == OutcomeState.ALLOW
    assert not out.missing_terms


def test_deny_fires_from_assertion_against_interest(z3):
    out = z3.solve(
        catalog(), rules(), claims(asked_nicely=True, is_banned=True), FactSet(scenario_id="s")
    )
    assert out.state == OutcomeState.DENY


def test_trust_only_allow_is_unverifiable(z3):
    facts = FactSet(
        scenario_id="s", facts=[fact("is_registered", True, Warrant.TRUST_ONLY)]
    )
    out = z3.solve(catalog(), rules(), claims(asked_nicely=True), facts)
    assert out.state == OutcomeState.UNVERIFIABLE_CLAIM
    assert out.scored_as.value == "NEED_MORE_INFO"
    reasons = {m.term_id: m.reason for m in out.missing_terms}
    assert reasons["is_registered"] == MissingReason.UNWARRANTED_ONLY


def test_unavailable_register_is_flagged(z3):
    facts = FactSet(
        scenario_id="s",
        facts=[],
        unavailable_registers=["reg"],
        unavailable_terms=["is_registered"],
    )
    out = z3.solve(catalog(), rules(), claims(asked_nicely=True), facts)
    assert out.state == OutcomeState.UNVERIFIABLE_CLAIM
    reasons = {m.term_id: m.reason for m in out.missing_terms}
    assert reasons["is_registered"] == MissingReason.NO_REGISTER


def test_missing_user_term(z3):
    facts = FactSet(scenario_id="s", facts=[fact("is_registered", True)])
    out = z3.solve(catalog(), rules(), ClaimSet(scenario_id="s"), facts)
    assert out.state == OutcomeState.NEED_USER_INFO
    assert [m.term_id for m in out.missing_terms] == ["asked_nicely"]


def test_default_deny_when_blocked(z3):
    facts = FactSet(scenario_id="s", facts=[fact("is_registered", False)])
    out = z3.solve(catalog(), rules(), claims(asked_nicely=True), facts)
    assert out.state == OutcomeState.DENY


def test_rewrite_rule_inconsistency_falls_back_to_deny(z3):
    ruleset = rules()
    ruleset.rules.append(
        RulePremise(
            premise_id="rewrite",
            rule_kind=RuleKind.SET_FALSE_IF_ALL,
            when_term_ids=["asked_nicely"],
            target_term_id="is_registered",
        )
    )
    out = z3.solve(
        catalog(),
        ruleset,
        claims(asked_nicely=True, is_registered=True),
        FactSet(scenario_id="s"),
    )
    assert out.state == OutcomeState.DENY
    assert "inconsistent" in out.note.lower()


def test_facts_never_override_claims(z3):
    facts = FactSet(scenario_id="s", facts=[fact("is_banned", False), fact("is_registered", True)])
    out = z3.solve(catalog(), rules(), claims(asked_nicely=True, is_banned=True), facts)
    assert out.state == OutcomeState.DENY


def test_register_availability_enum():
    assert Availability("available").value == "available"
