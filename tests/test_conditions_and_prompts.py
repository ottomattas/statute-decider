"""Condition loading, fuse declarations, prompt templates, matrix export."""

import pytest

from statute_decider.llm.registry import ModelRegistry
from statute_decider.runner.conditions import load_condition
from statute_decider.runner.matrix import expand_rows
from statute_decider.strategies import load_prompt


def test_committed_conditions_load(root):
    for name in (
        "solver-validation",
        "baseline",
        "candidate",
        "llm-decider",
        "llm-as-solver",
        "llm-structured",
        "candidate-staged",
    ):
        condition = load_condition(root / "configs" / "conditions" / f"{name}.yaml")
        assert condition.condition == name
        assert len(condition.bindings) == 11


def test_solver_inputs_prompt_renders_premises(root):
    from statute_decider.core import DataStore
    from statute_decider.nodes import lookup_facts
    from statute_decider.nodes.rendering import render_claims, render_facts, render_rules

    store = DataStore(root / "data")
    case_id = "section_120_demo"
    case = store.case(case_id)
    scenario_id = store.all_scenarios([case_id])[0][1]
    scenario = store.scenario(case_id, scenario_id)
    statute_id = case.statute_ids[0]
    registry = store.scenario_registry(case_id, scenario)
    mappings = [store.oracle_record_term(rid) for rid in case.register_ids]
    facts = lookup_facts(scenario_id, registry, mappings)
    claims = store.oracle_value(case_id, "term_claim", scenario_id)
    prompt = load_prompt(root / "prompts", "premise_outcome", "solver-inputs-v1", strategy="decide")
    rendered = prompt.render(
        rules=render_rules(store.oracle_term_rule(statute_id), store.oracle_text_term(statute_id)),
        claims=render_claims(claims),
        facts=render_facts(facts),
    )
    assert "REFERENCE DECISION RULES" in rendered
    assert "CLAIMS" in rendered and "FACTS" in rendered
    assert "STATUTE" not in rendered


def test_llm_decider_binds_oracle_rules(root):
    condition = load_condition(root / "configs" / "conditions" / "llm-decider.yaml")
    assert condition.binding("term_rule").method == "oracle"
    assert condition.binding("text_term").method == "oracle"
    assert condition.binding("premise_outcome").method == "llm"
    assert condition.binding("premise_outcome").prompt == "oracle-rules-v1"
    assert condition.binding("outcome_trace").method == "skip"
    prompt = load_prompt(
        root / "prompts", "premise_outcome", "oracle-rules-v1", strategy="decide"
    )
    rendered = prompt.render(
        statute="Act", utterance="I apply", registry="{}", rules="Rules: parent -> ALLOW"
    )
    assert "I apply" in rendered
    assert "Rules: parent -> ALLOW" in rendered
    assert "{rules}" not in rendered


def test_render_oracle_rules(root):
    from statute_decider.core import DataStore
    from statute_decider.nodes.rendering import render_rules

    store = DataStore(root / "data")
    statute_id = store.statute_ids()[0]
    text = render_rules(store.oracle_term_rule(statute_id), store.oracle_text_term(statute_id))
    assert "Variables:" in text
    assert "Rules:" in text
    assert "ALLOW" in text


def test_candidate_fuses_user_chain(root):
    condition = load_condition(root / "configs" / "conditions" / "candidate.yaml")
    assert condition.fused_with("utterance_term") == "term_claim"
    assert condition.binding("premise_outcome").method == "solver"
    assert condition.uses_llm()


def test_baseline_skips_all_derivation(root):
    condition = load_condition(root / "configs" / "conditions" / "baseline.yaml")
    for node in ("text_term", "term_rule", "utterance_term", "term_claim", "record_term", "term_fact"):
        assert condition.binding(node).method == "skip"
    assert condition.binding("premise_outcome").method == "llm"


def test_condition_requires_all_nodes(tmp_path):
    partial = tmp_path / "partial.yaml"
    partial.write_text("condition: partial\nstatute_text: { method: file }\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unbound"):
        load_condition(partial)


def test_prompts_load_and_render(root):
    prompt = load_prompt(root / "prompts", "utterance_term", "ground-v1", strategy="ground")
    assert prompt.system and prompt.sha256
    rendered = prompt.render(utterance="Tere", term_catalog="- a: A")
    assert "Tere" in rendered and "- a: A" in rendered
    with pytest.raises(ValueError, match="placeholder"):
        prompt.render(utterance="Tere")


def test_matrix_expansion(root):
    registry = ModelRegistry(
        root / "configs" / "llm" / "models.yaml", root / "configs" / "llm" / "prices.yaml"
    )
    rows = expand_rows(root, registry)
    assert len(rows) > 100
    nodes = {row["node"] for row in rows}
    assert {"statute_text", "text_term", "term_rule", "utterance_term", "term_claim",
            "registry_record", "record_term", "term_fact", "premise_outcome",
            "outcome_trace"} <= nodes
    llm_rows = [r for r in rows if r["method"] == "llm" and r["node"] == "premise_outcome"]
    assert {r["provider"] for r in llm_rows} == {"google", "openai", "anthropic", "deepseek"}
    future_rows = [r for r in rows if r["future"] == "true"]
    assert future_rows, "future expansion slots must stay visible"


def test_registry_and_budget_math(root, tmp_path):
    from statute_decider.llm import BudgetExceeded, BudgetGuard, Usage

    registry = ModelRegistry(
        root / "configs" / "llm" / "models.yaml", root / "configs" / "llm" / "prices.yaml"
    )
    assert registry.resolve(["all"])
    spec = registry.spec("gpt-5-mini")
    assert spec.provider == "openai"
    eur = spec.eur(1_000_000, 1_000_000, registry.usd_to_eur)
    assert abs(eur - (0.25 + 2.00) * 0.92) < 1e-9

    guard = BudgetGuard(cap_eur=0.001, ledger_path=tmp_path / "ledger.jsonl")
    guard.record(spec, Usage(input_tokens=1_000_000, output_tokens=0))
    with pytest.raises(BudgetExceeded):
        guard.check()
    assert (tmp_path / "ledger.jsonl").read_text().count("\n") == 1
