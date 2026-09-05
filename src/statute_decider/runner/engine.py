"""The node engine: run one scenario under a condition binding.

Uniform node treatment: resolve the binding, execute the method, record the
value with provenance. Isolation testing is a condition whose other nodes bind
``oracle``; propagation is any condition consuming produced upstream values —
the engine does not distinguish them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from statute_decider.core import (
    ClaimSet,
    DataStore,
    FactSet,
    PremiseOutcome,
    RecordTermMap,
    RegistryState,
    RuleSet,
    StatuteText,
    TermCatalog,
    UtteranceTerms,
)
from statute_decider.legislation.units import DEFAULT_MAX_STATUTE_TOKENS
from statute_decider.llm import LLMClient
from statute_decider.nodes import (
    decide_llm,
    ground_utterance,
    justify_llm,
    lookup_facts,
    match_record_terms,
    render_trace,
    value_claims,
)
from statute_decider.runner.conditions import Condition, NodeBinding
from statute_decider.solvers import get_solver
from statute_decider.strategies import load_prompt


@dataclass
class CellServices:
    """Everything a grid cell needs beyond the data itself."""

    prompts_dir: Path
    client: LLMClient | None = None
    model_id: str | None = None
    temperature: float = 0.0
    max_output_tokens: int = 8192
    max_statute_tokens: int = DEFAULT_MAX_STATUTE_TOKENS  # Ruling H: statute unit budget
    prompt_overrides: dict[str, str] = field(default_factory=dict)
    solver_override: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def prompt_for(self, node: str, binding: NodeBinding):
        variant = self.prompt_overrides.get(node) or binding.prompt
        if not variant:
            raise ValueError(f"Node {node} bound to llm without a prompt variant.")
        # Accept both bare variants ("ground") and full ids ("utterance_term/ground/ground").
        if "/" in variant:
            variant = variant.rsplit("/", 1)[1]
        return load_prompt(self.prompts_dir, node, variant, strategy=binding.strategy)

    def require_llm(self, node: str) -> tuple[LLMClient, str]:
        if self.client is None or not self.model_id:
            raise RuntimeError(f"Node {node} bound to llm but no client/model configured.")
        return self.client, self.model_id


@dataclass
class ScenarioRun:
    case_id: str
    scenario_id: str
    condition: str
    values: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    def value(self, node: str):
        return self.values.get(node)


def _unsupported(node: str, method: str) -> RuntimeError:
    return RuntimeError(
        f"Node {node!r} declares method {method!r} in the matrix, but its executor "
        "is not implemented yet — it lands with the experiment that needs it."
    )


def run_scenario(
    store: DataStore,
    condition: Condition,
    case_id: str,
    scenario_id: str,
    services: CellServices,
) -> ScenarioRun:
    run = ScenarioRun(case_id=case_id, scenario_id=scenario_id, condition=condition.condition)
    values = run.values
    case = store.case(case_id)
    scenario = store.scenario(case_id, scenario_id)
    statute_id = case.statute_ids[0] if case.statute_ids else ""
    meta = {
        **services.meta,
        "case_id": case_id,
        "scenario_id": scenario_id,
        "condition": condition.condition,
    }

    def bind(node: str) -> NodeBinding:
        return condition.binding(node)

    # --- sources ---
    # statute_text: ``file`` = the official text rendered from the corpus XML —
    # the whole act, or the smallest structural unit enclosing the declared
    # provisions when the act exceeds ``max_statute_tokens`` (Ruling H; what
    # prompts receive); ``slice`` = only the provisions statute.yaml declares
    # (the ablation). Both record document + unit + provision provenance, and
    # the same ``statute_input`` record rides on every ledger line via ``meta``.
    statute: StatuteText | None = None
    statute_text_value: str | None = None
    st_method = bind("statute_text").method
    if st_method == "file":
        statute = store.statute_text(
            statute_id, method="full_act", max_tokens=services.max_statute_tokens
        )
    elif st_method == "slice":
        statute = store.statute_text(statute_id, method="slice")
    elif st_method != "skip":
        raise _unsupported("statute_text", st_method)
    if statute is not None:
        statute_text_value = statute.text
        meta["statute_input"] = statute.statute_input()
    values["statute_text"] = statute

    utterance: str = ""
    if bind("user_utterance").method == "file":
        utterance = store.utterance_text(case_id, scenario)
    elif bind("user_utterance").method != "skip":
        raise _unsupported("user_utterance", bind("user_utterance").method)
    values["user_utterance"] = utterance

    registry: RegistryState | None = None
    if bind("registry_record").method == "file":
        registry = store.scenario_registry(case_id, scenario)
    elif bind("registry_record").method != "skip":
        raise _unsupported("registry_record", bind("registry_record").method)
    values["registry_record"] = registry

    # --- statute chain ---
    catalog: TermCatalog | None = None
    method = bind("text_term").method
    if method == "oracle":
        catalog = store.oracle_text_term(statute_id)
    elif method != "skip":
        raise _unsupported("text_term", method)
    values["text_term"] = catalog

    ruleset: RuleSet | None = None
    method = bind("term_rule").method
    if method == "oracle":
        ruleset = store.oracle_term_rule(statute_id)
    elif method != "skip":
        raise _unsupported("term_rule", method)
    values["term_rule"] = ruleset

    # --- user chain (separately bindable; fusable) ---
    recognized: UtteranceTerms | None = None
    claims: ClaimSet | None = None
    ut_binding = bind("utterance_term")
    tc_binding = bind("term_claim")
    fused = condition.fused_with("utterance_term") == "term_claim"

    if ut_binding.method == "llm":
        client, model_id = services.require_llm("utterance_term")
        if catalog is None:
            raise RuntimeError("utterance_term=llm requires a term catalog (text_term).")
        prompt = services.prompt_for("utterance_term", ut_binding)
        recognized, fused_claims = ground_utterance(
            client,
            model_id,
            prompt,
            scenario_id=scenario_id,
            utterance=utterance,
            catalog=catalog,
            fused=fused and tc_binding.method == "llm",
            temperature=services.temperature,
            max_output_tokens=services.max_output_tokens,
            meta=meta,
        )
        if fused and tc_binding.method == "llm":
            claims = fused_claims
    elif ut_binding.method == "oracle":
        recognized = store.oracle_value(case_id, "utterance_term", scenario_id)
    elif ut_binding.method != "skip":
        raise _unsupported("utterance_term", ut_binding.method)
    values["utterance_term"] = recognized

    if claims is None:
        if tc_binding.method == "llm":
            client, model_id = services.require_llm("term_claim")
            if recognized is None:
                raise RuntimeError("term_claim=llm (staged) requires utterance_term output.")
            if catalog is None:
                raise RuntimeError("term_claim=llm requires a term catalog (text_term).")
            prompt = services.prompt_for("term_claim", tc_binding)
            claims = value_claims(
                client,
                model_id,
                prompt,
                scenario_id=scenario_id,
                utterance=utterance,
                catalog=catalog,
                recognized=recognized,
                temperature=services.temperature,
                max_output_tokens=services.max_output_tokens,
                meta=meta,
            )
        elif tc_binding.method == "oracle":
            claims = store.oracle_value(case_id, "term_claim", scenario_id)
        elif tc_binding.method != "skip":
            raise _unsupported("term_claim", tc_binding.method)
    values["term_claim"] = claims

    # --- register chain ---
    mappings: list[RecordTermMap] | None = None
    method = bind("record_term").method
    if method == "oracle":
        mappings = [store.oracle_record_term(rid) for rid in case.register_ids]
    elif method == "match":
        if registry is None or catalog is None:
            raise RuntimeError("record_term=match requires registry_record and text_term.")
        mappings = []
        for register in registry.registers:
            fields = sorted({f for rec in register.records for f in rec.fields})
            mappings.append(match_record_terms(register.register_id, fields, catalog))
    elif method != "skip":
        raise _unsupported("record_term", method)
    values["record_term"] = mappings

    facts: FactSet | None = None
    method = bind("term_fact").method
    if method == "lookup":
        if registry is None or mappings is None:
            raise RuntimeError("term_fact=lookup requires registry_record and record_term.")
        facts = lookup_facts(scenario_id, registry, mappings)
    elif method == "oracle":
        facts = store.oracle_value(case_id, "term_fact", scenario_id)
    elif method != "skip":
        raise _unsupported("term_fact", method)
    values["term_fact"] = facts

    # --- join: outcome ---
    outcome: PremiseOutcome | None = None
    po_binding = bind("premise_outcome")
    if po_binding.method == "solver":
        if catalog is None or ruleset is None:
            raise RuntimeError("premise_outcome=solver requires text_term and term_rule.")
        solver = get_solver(services.solver_override or po_binding.solver or "z3")
        outcome = solver.solve(
            catalog,
            ruleset,
            claims or ClaimSet(scenario_id=scenario_id),
            facts or FactSet(scenario_id=scenario_id),
        )
    elif po_binding.method == "llm":
        client, model_id = services.require_llm("premise_outcome")
        prompt = services.prompt_for("premise_outcome", po_binding)
        # The prompt's placeholders decide which inputs are required; decide_llm
        # raises if the condition left one of them unbound.
        outcome = decide_llm(
            client,
            model_id,
            prompt,
            scenario_id=scenario_id,
            statute_text=statute_text_value,
            utterance=utterance,
            registry=registry,
            catalog=catalog,
            rules=ruleset,
            claims=claims,
            facts=facts,
            temperature=services.temperature,
            max_output_tokens=services.max_output_tokens,
            meta=meta,
        )
    elif po_binding.method == "oracle":
        outcome = store.oracle_value(case_id, "premise_outcome", scenario_id)
    elif po_binding.method != "skip":
        raise _unsupported("premise_outcome", po_binding.method)
    values["premise_outcome"] = outcome

    # --- join: trace ---
    trace = None
    ot_binding = bind("outcome_trace")
    if ot_binding.method == "render":
        if outcome is None or ruleset is None or catalog is None:
            raise RuntimeError("outcome_trace=render requires an inference record.")
        trace = render_trace(scenario_id, outcome, ruleset, catalog)
    elif ot_binding.method == "llm":
        client, model_id = services.require_llm("outcome_trace")
        if outcome is None:
            raise RuntimeError("outcome_trace=llm requires premise_outcome.")
        prompt = services.prompt_for("outcome_trace", ot_binding)
        trace = justify_llm(
            client,
            model_id,
            prompt,
            scenario_id=scenario_id,
            statute_text=statute_text_value or "",
            utterance=utterance,
            outcome=outcome,
            temperature=services.temperature,
            max_output_tokens=services.max_output_tokens,
            meta=meta,
        )
    elif ot_binding.method == "oracle":
        trace = store.oracle_value(case_id, "outcome_trace", scenario_id)
    elif ot_binding.method != "skip":
        raise _unsupported("outcome_trace", ot_binding.method)
    values["outcome_trace"] = trace

    return run


def node_value_dump(value: Any) -> Any:
    """JSON-safe dump of a node value for nodes/<node>.jsonl."""
    if value is None:
        return None
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [node_value_dump(item) for item in value]
    return value
