"""Every data file loads through the core schemas; ids cross-reference."""


def test_inventory(store):
    assert len(store.statute_ids()) == 6
    assert len(store.case_ids()) == 6
    assert len(store.all_scenarios()) == 47


def test_statutes_load(store):
    for statute_id in store.statute_ids():
        assert store.statute_text(statute_id).strip()
        sidecar = store.statute_sidecar(statute_id)
        assert sidecar.statute_id == statute_id
        catalog = store.oracle_text_term(statute_id)
        assert catalog.terms
        ruleset = store.oracle_term_rule(statute_id)
        assert ruleset.rules
        assert ruleset.allow_outcome_id and ruleset.deny_outcome_id
        term_ids = catalog.term_ids()
        for rule in ruleset.rules:
            for term_id in rule.when_term_ids:
                assert term_id in term_ids, f"{statute_id}:{rule.premise_id} references {term_id}"


def test_registers_load(store):
    for register_id in store.register_ids():
        schema = store.register_schema(register_id)
        assert schema.register_id == register_id
        mapping = store.oracle_record_term(register_id)
        assert mapping.register_id == register_id


def test_cases_reference_shared_entities(store):
    statutes = set(store.statute_ids())
    registers = set(store.register_ids())
    for case_id in store.case_ids():
        case = store.case(case_id)
        assert set(case.statute_ids) <= statutes
        assert set(case.register_ids) <= registers


MECHANISMS = {
    "claims_verified",
    "register_only",
    "alt_rule_claim_overrides_register",
    "own_admission",
    "no_allow_path",
    "register_silent",
    "user_silent",
    "register_down",
    "trust_only",
}


def test_scenarios_carry_display_fields(store):
    """Every scenario has a short human label and a mechanism from the fixed vocabulary."""
    for case_id, scenario_id in store.all_scenarios():
        scenario = store.scenario(case_id, scenario_id)
        assert scenario.label and len(scenario.label) <= 60, f"{case_id}/{scenario_id}"
        assert scenario.mechanism in MECHANISMS, f"{case_id}/{scenario_id}: {scenario.mechanism!r}"


def test_scenarios_have_oracle_outcomes(store):
    for case_id, scenario_id in store.all_scenarios():
        scenario = store.scenario(case_id, scenario_id)
        assert store.utterance_text(case_id, scenario).strip(), f"{case_id}/{scenario_id}"
        outcome = store.oracle_value(case_id, "premise_outcome", scenario_id)
        assert outcome is not None, f"{case_id}/{scenario_id} lacks oracle premise_outcome"
        claims = store.oracle_value(case_id, "term_claim", scenario_id)
        assert claims is not None
        facts = store.oracle_value(case_id, "term_fact", scenario_id)
        assert facts is not None
