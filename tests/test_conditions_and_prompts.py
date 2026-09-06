"""Condition loading, fuse declarations, prompt templates, matrix export."""

import json

import pytest

from statute_decider.llm.registry import ModelRegistry
from statute_decider.runner.conditions import load_condition
from statute_decider.runner.matrix import expand_rows
from statute_decider.strategies import load_prompt


def test_committed_conditions_load(root):
    for name in (
        "solver-validation",
        "llm-only",
        "architecture",
        "llm-only-plus-rules",
        "llm-decides-on-oracle-inputs-partial-specification",
        "llm-decides-on-oracle-inputs-full-procedure",
        "llm-decides-on-llm-claims-partial-specification",
        "llm-decides-on-llm-claims-full-procedure",
        "architecture-staged-grounding",
    ):
        condition = load_condition(root / "configs" / "conditions" / f"{name}.yaml")
        assert condition.condition == name
        assert len(condition.bindings) == 11


def test_solver_inputs_prompt_renders_premises(root):
    from statute_decider.core import DataStore
    from statute_decider.nodes import lookup_facts
    from statute_decider.nodes.rendering import render_claims, render_facts, render_rules

    store = DataStore(root / "data")
    case_id = "child_representation_by_one_parent"
    case = store.case(case_id)
    scenario_id = store.all_scenarios([case_id])[0][1]
    scenario = store.scenario(case_id, scenario_id)
    statute_id = case.statute_ids[0]
    registry = store.scenario_registry(case_id, scenario)
    mappings = [store.oracle_record_term(rid) for rid in case.register_ids]
    facts = lookup_facts(scenario_id, registry, mappings)
    claims = store.oracle_value(case_id, "term_claim", scenario_id)
    prompt = load_prompt(root / "prompts", "premise_outcome", "solver-inputs-partial-specification", strategy="decide")
    rendered = prompt.render(
        rules=render_rules(store.oracle_term_rule(statute_id), store.oracle_text_term(statute_id)),
        claims=render_claims(claims),
        facts=render_facts(facts),
    )
    assert "REFERENCE DECISION RULES" in rendered
    assert "CLAIMS" in rendered and "FACTS" in rendered
    assert "STATUTE" not in rendered


def test_llm_only_plus_rules_binds_oracle_rules(root):
    condition = load_condition(root / "configs" / "conditions" / "llm-only-plus-rules.yaml")
    assert condition.binding("term_rule").method == "oracle"
    assert condition.binding("text_term").method == "oracle"
    assert condition.binding("premise_outcome").method == "llm"
    assert condition.binding("premise_outcome").prompt == "decide-raw-sources-plus-rules"
    # Ruling J: the decide call's inline reasoning is the row's trace; no second call.
    assert condition.binding("outcome_trace").method == "passthrough"
    prompt = load_prompt(
        root / "prompts", "premise_outcome", "decide-raw-sources-plus-rules", strategy="decide"
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


def test_architecture_fuses_user_chain(root):
    condition = load_condition(root / "configs" / "conditions" / "architecture.yaml")
    assert condition.fused_with("utterance_term") == "term_claim"
    assert condition.binding("premise_outcome").method == "solver"
    assert condition.uses_llm()


def test_llm_only_skips_all_derivation(root):
    condition = load_condition(root / "configs" / "conditions" / "llm-only.yaml")
    for node in ("text_term", "term_rule", "utterance_term", "term_claim", "record_term", "term_fact"):
        assert condition.binding(node).method == "skip"
    assert condition.binding("premise_outcome").method == "llm"


def test_condition_requires_all_nodes(tmp_path):
    partial = tmp_path / "partial.yaml"
    partial.write_text("condition: partial\nstatute_text: { method: file }\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unbound"):
        load_condition(partial)


def test_prompts_load_and_render(root):
    prompt = load_prompt(root / "prompts", "utterance_term", "ground", strategy="ground")
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


def test_cache_aware_pricing(root, tmp_path):
    from statute_decider.llm import BudgetGuard, Usage

    registry = ModelRegistry(
        root / "configs" / "llm" / "models.yaml", root / "configs" / "llm" / "prices.yaml"
    )
    # OpenAI convention: input_tokens is the full prompt, cached is a subset.
    mini = registry.spec("gpt-5-mini")
    eur = mini.eur(1_000_000, 0, 1.0, cached_input_tokens=900_000)
    assert abs(eur - (0.1 * 0.25 + 0.9 * 0.025)) < 1e-9
    # Anthropic: write surcharge + cheap reads; fable-5.1 reads at 0.025x.
    fable = registry.spec("fable-5.1")
    assert fable.api_model == "claude-fable-5-1"
    eur = fable.eur(1_000_000, 0, 1.0, cached_input_tokens=800_000, cache_write_input_tokens=100_000)
    assert abs(eur - (0.1 * 10.0 + 0.8 * 0.25 + 0.1 * 12.5)) < 1e-9
    # No cache prices configured -> plain input rate (old behaviour).
    from statute_decider.llm.registry import ModelSpec

    bare = ModelSpec("x", "openai", "x", input_usd_per_million=1.0)
    assert abs(bare.eur(100, 0, 1.0, cached_input_tokens=50) - 1e-4) < 1e-12
    # Ledger row carries both cache fields.
    guard = BudgetGuard(cap_eur=10, ledger_path=tmp_path / "ledger.jsonl")
    guard.record(fable, Usage(input_tokens=10, output_tokens=0, cached_input_tokens=5))
    row = json.loads((tmp_path / "ledger.jsonl").read_text().splitlines()[0])
    assert row["cached_input_tokens"] == 5 and row["cache_write_input_tokens"] == 0


def test_render_with_prefix_splits_after_statute(root):
    prompt = load_prompt(root / "prompts", "premise_outcome", "decide-raw-sources", strategy="decide")
    text, n = prompt.render_with_prefix(
        "statute", statute="ACT TEXT", utterance="I apply", registry="{}"
    )
    assert text == prompt.render(statute="ACT TEXT", utterance="I apply", registry="{}")
    assert text[:n].endswith("ACT TEXT") and text[n:].lstrip().startswith("CASE REQUEST")
    solver = load_prompt(root / "prompts", "premise_outcome", "solver-inputs-partial-specification", strategy="decide")
    _, n2 = solver.render_with_prefix("statute", rules="R", claims="C", facts="F")
    assert n2 == 0


def test_resume_and_limit_continue_a_grid(root, tmp_path):
    from statute_decider.runner.experiment import run_experiment

    exp_dir = tmp_path / "exp"
    exp_dir.mkdir()
    (exp_dir / "experiment.yaml").write_text(
        "name: resume-test\nquestion: t\ncondition: solver-validation\n"
        "cases: [child_representation_by_one_parent]\nmodels: []\nrepeats: 1\nbudget_eur: 0\n",
        encoding="utf-8",
    )
    # Batch 1: three cells only.
    results = run_experiment(root, exp_dir, execution="sequential", models=["all"], limit=3)
    rows = [json.loads(l) for l in (results / "rows.jsonl").read_text().splitlines() if l.strip()]
    assert len(rows) == 3
    # Resume: the remaining six run (the case has nine scenarios since 2026-09-06), the first three are kept, none duplicated.
    run_experiment(root, exp_dir, execution="sequential", models=["all"], resume=True)
    rows = [json.loads(l) for l in (results / "rows.jsonl").read_text().splitlines() if l.strip()]
    assert len(rows) == 9
    assert len({(r["scenario_id"], r["repeat"]) for r in rows}) == 9
    # Resume again: nothing pending, rows unchanged; every invocation recorded.
    run_experiment(root, exp_dir, execution="sequential", models=["all"], resume=True)
    assert (results / "rows.jsonl").read_text().count("\n") == 9
    assert (results / "invocations.jsonl").read_text().count("\n") == 3


def test_parallel_runner_warms_each_cache_group_first(root):
    """Parallel: the first unit of a (model, statute) group finishes before any
    other unit of that group starts; other groups and providers are not held."""
    import threading
    import time

    from statute_decider.llm import LLMClient

    registry = ModelRegistry(root / "configs" / "llm" / "models.yaml")
    client = LLMClient(registry, provider_concurrency=4)
    events: list[tuple[str, str, float]] = []
    lock = threading.Lock()

    def unit(name: str, group: str, sleep_s: float):
        def run():
            with lock:
                events.append(("start", f"{group}:{name}", time.monotonic()))
            time.sleep(sleep_s)
            with lock:
                events.append(("end", f"{group}:{name}", time.monotonic()))
            return name

        return run

    units = [
        ("openai", "g1", unit("a", "g1", 0.2)),
        ("openai", "g1", unit("b", "g1", 0.01)),
        ("openai", "g1", unit("c", "g1", 0.01)),
        ("openai", "g2", unit("d", "g2", 0.01)),
        ("anthropic", "g3", unit("e", "g3", 0.01)),
        ("openai", unit("f", "nogroup", 0.01)),  # two-tuple form still accepted
    ]
    results = client.run_units(units, execution="parallel")
    assert results == ["a", "b", "c", "d", "e", "f"]
    when = {(kind, who): t for kind, who, t in events}
    for follower in ("b", "c"):
        assert when[("start", f"g1:{follower}")] >= when[("end", "g1:a")]
    # g2, g3 and the ungrouped unit start while g1's warm-up is still running.
    for other in ("g2:d", "g3:e", "nogroup:f"):
        assert when[("start", other)] < when[("end", "g1:a")]
    # Sequential ignores groups and keeps order.
    events.clear()
    assert client.run_units(units, execution="sequential") == ["a", "b", "c", "d", "e", "f"]
    starts = [who for kind, who, _ in events if kind == "start"]
    assert starts == ["g1:a", "g1:b", "g1:c", "g2:d", "g3:e", "nogroup:f"]


def test_scenarios_filter_narrows_the_grid(root, tmp_path):
    import pytest

    from statute_decider.runner.experiment import run_experiment

    exp_dir = tmp_path / "exp"
    exp_dir.mkdir()
    yaml_head = (
        "name: scenario-filter-test\nquestion: t\ncondition: solver-validation\n"
        "cases: [land_tax_home_exemption]\nmodels: []\nrepeats: 1\nbudget_eur: 0\n"
    )
    (exp_dir / "experiment.yaml").write_text(
        yaml_head + "scenarios: [land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport]\n",
        encoding="utf-8",
    )
    results = run_experiment(root, exp_dir, execution="sequential", models=["all"])
    rows = [json.loads(l) for l in (results / "rows.jsonl").read_text().splitlines() if l.strip()]
    assert [(r["case_id"], r["scenario_id"]) for r in rows] == [
        ("land_tax_home_exemption", "unverifiable_trust_only_applicant_selfreport")
    ]
    # A scenario outside the selected cases (or misspelt) is an error, not a silent empty grid.
    (exp_dir / "experiment.yaml").write_text(
        yaml_head + "scenarios: [land_tax_home_exemption/no_such_scenario]\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="no_such_scenario"):
        run_experiment(root, exp_dir, execution="sequential", models=["all"])
