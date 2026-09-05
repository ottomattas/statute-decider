"""Ruling J (ADR 0007): one structured decide call; justification is a list of
entries on every row.

A fake client stands in for the providers: it returns a canned structured
response for whichever ``response_model`` the call asks for and counts calls.
No network, no cost.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import pytest

from statute_decider.core import JustificationEntry, OutcomeTrace, PremiseOutcome
from statute_decider.llm.base import LLMResult, Usage
from statute_decider.nodes import passthrough_trace, render_trace
from statute_decider.nodes.llm_io import DecideResponse, JustifyResponse
from statute_decider.runner.conditions import load_condition
from statute_decider.runner.engine import CellServices, run_scenario


@dataclass
class FakeClient:
    """Minimal stand-in for ``LLMClient``: canned answers, a call log."""

    calls: list = field(default_factory=list)

    def complete(self, call):
        self.calls.append(call)
        if call.response_model is DecideResponse:
            payload = {
                "steps": ["read the statute", "check the registers", "decide"],
                "outcome": "DENY",
                "missing_terms": [],
                "justification": "The register records a deny ground.",
            }
        elif call.response_model is JustifyResponse:
            payload = {
                "steps": ["restate the ground"],
                "justification": "Post-hoc paragraph.",
            }
        else:  # pragma: no cover - the tests below only exercise decide/justify
            raise AssertionError(f"unexpected response model {call.response_model}")
        return LLMResult(
            parsed=call.response_model.model_validate(payload),
            raw_text=json.dumps(payload),
            usage=Usage(input_tokens=10, output_tokens=5),
            provider="fake",
            model=call.model_id,
        )


def _first_scenario(store):
    return next(iter(store.all_scenarios()))


# --- schema ---


def test_decide_response_schema_orders_steps_before_outcome():
    keys = list(DecideResponse.model_json_schema()["properties"])
    assert keys == ["steps", "outcome", "missing_terms", "justification"]
    parsed = DecideResponse.model_validate(
        {"steps": ["a"], "outcome": "ALLOW", "missing_terms": [], "justification": "ok"}
    )
    assert parsed.steps == ["a"] and parsed.outcome == "ALLOW"


def test_justification_entry_schema():
    entry = JustificationEntry(source="llm_inline", steps=["s"], text="t", model="m")
    dumped = entry.model_dump(exclude_none=True)
    assert set(dumped) == {"source", "steps", "text", "model"}
    with pytest.raises(ValueError):
        JustificationEntry(source="other", steps=[], text="")  # type: ignore[arg-type]


# --- one call per scenario, pass-through entry ---


def test_llm_only_condition_makes_exactly_one_call(root, store):
    condition = load_condition(root / "configs" / "conditions" / "llm-only.yaml")
    assert condition.binding("outcome_trace").method == "passthrough"
    client = FakeClient()
    services = CellServices(prompts_dir=root / "prompts", client=client, model_id="fake-model")
    case_id, scenario_id = _first_scenario(store)
    run = run_scenario(store, condition, case_id, scenario_id, services)

    assert len(client.calls) == 1, [c.meta.get("node") for c in client.calls]
    assert client.calls[0].meta["node"] == "premise_outcome"
    assert "Reason step by step before you decide." in client.calls[0].system

    outcome: PremiseOutcome = run.value("premise_outcome")
    assert outcome.steps == ["read the statute", "check the registers", "decide"]
    assert outcome.note == "The register records a deny ground."

    trace: OutcomeTrace = run.value("outcome_trace")
    assert [e.source for e in trace.justification] == ["llm_inline"]
    entry = trace.justification[0]
    assert entry.steps == outcome.steps and entry.text == outcome.note
    assert entry.model == "fake-model"
    assert entry.prompt_id == "premise_outcome/decide/decide-raw-sources"
    assert entry.prompt_hash and entry.prompt_hash == outcome.provenance.prompt_hash
    assert trace.provenance.method == "passthrough"


@pytest.mark.parametrize(
    "name",
    [
        "llm-only-plus-rules",
        "llm-decides-on-oracle-inputs-full-procedure",
        "llm-decides-on-oracle-inputs-partial-specification",
    ],
)
def test_every_llm_decided_condition_passes_its_reasoning_through(root, store, name):
    condition = load_condition(root / "configs" / "conditions" / f"{name}.yaml")
    client = FakeClient()
    services = CellServices(prompts_dir=root / "prompts", client=client, model_id="fake-model")
    case_id, scenario_id = _first_scenario(store)
    run = run_scenario(store, condition, case_id, scenario_id, services)
    assert [c.meta.get("node") for c in client.calls] == ["premise_outcome"]
    trace = run.value("outcome_trace")
    assert [e.source for e in trace.justification] == ["llm_inline"]


def test_passthrough_refuses_a_solver_outcome(root, store):
    condition = load_condition(root / "configs" / "conditions" / "solver-validation.yaml")
    case_id, scenario_id = _first_scenario(store)
    run = run_scenario(store, condition, case_id, scenario_id, CellServices(prompts_dir=root / "prompts"))
    outcome = run.value("premise_outcome")
    with pytest.raises(RuntimeError, match="passthrough"):
        passthrough_trace(scenario_id, outcome)
    trace = run.value("outcome_trace")
    assert [e.source for e in trace.justification] == ["solver_trace"]
    assert trace.justification[0].steps and trace.justification[0].text


# --- the optional justify node appends, never overwrites ---


def test_justify_appends_llm_post_to_inline_entry(root, store, tmp_path):
    import yaml

    base = yaml.safe_load((root / "configs" / "conditions" / "llm-only.yaml").read_text())
    base["condition"] = "llm-only-then-justify"
    base["outcome_trace"] = {"method": "llm", "strategy": "justify", "prompt": "justify"}
    path = tmp_path / "llm-only-then-justify.yaml"
    path.write_text(yaml.safe_dump(base))
    condition = load_condition(path)

    client = FakeClient()
    services = CellServices(prompts_dir=root / "prompts", client=client, model_id="fake-model")
    case_id, scenario_id = _first_scenario(store)
    run = run_scenario(store, condition, case_id, scenario_id, services)

    assert [c.meta.get("node") for c in client.calls] == ["premise_outcome", "outcome_trace"]
    justify_call = client.calls[1]
    # The justify prompt sees the row's existing reasoning, not a bare "reason".
    assert "[llm_inline]" in justify_call.user
    assert "1. read the statute" in justify_call.user
    assert "The register records a deny ground." in justify_call.user

    trace: OutcomeTrace = run.value("outcome_trace")
    assert [e.source for e in trace.justification] == ["llm_inline", "llm_post"]
    inline, post = trace.justification
    assert inline.text == "The register records a deny ground."
    assert post.steps == ["restate the ground"] and post.text == "Post-hoc paragraph."
    assert post.prompt_id == "outcome_trace/justify/justify"
    assert trace.primary is inline


def test_justify_appends_llm_post_to_solver_trace(root, store, tmp_path):
    import yaml

    base = yaml.safe_load((root / "configs" / "conditions" / "solver-validation.yaml").read_text())
    base["condition"] = "solver-then-justify"
    base["outcome_trace"] = {"method": "llm", "strategy": "justify", "prompt": "justify"}
    path = tmp_path / "solver-then-justify.yaml"
    path.write_text(yaml.safe_dump(base))
    condition = load_condition(path)

    client = FakeClient()
    services = CellServices(prompts_dir=root / "prompts", client=client, model_id="fake-model")
    case_id, scenario_id = _first_scenario(store)
    run = run_scenario(store, condition, case_id, scenario_id, services)

    assert [c.meta.get("node") for c in client.calls] == ["outcome_trace"]
    trace: OutcomeTrace = run.value("outcome_trace")
    assert [e.source for e in trace.justification] == ["solver_trace", "llm_post"]
    # The solver's rendering is untouched by the append.
    rendered = render_trace(
        scenario_id, run.value("premise_outcome"), run.value("term_rule"), run.value("text_term")
    )
    assert trace.justification[0].steps == rendered.justification[0].steps
    assert trace.justification[0].text == rendered.justification[0].text
