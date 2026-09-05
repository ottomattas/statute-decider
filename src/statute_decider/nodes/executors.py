"""Node executors: the method implementations behind each graph node.

Every executor produces a typed node value with provenance. The engine
(``runner.engine``) binds these to nodes according to the condition YAML.
Capability declarations (which node supports which method, including future
slots) live in ``runner.matrix``.
"""

from __future__ import annotations

from statute_decider.core import (
    Availability,
    ClaimPremise,
    ClaimSet,
    FactPremise,
    FactSet,
    MissingReason,
    MissingTerm,
    OutcomeState,
    OutcomeTrace,
    PremiseOutcome,
    Provenance,
    RecordTermMap,
    RegistryState,
    RuleSet,
    ScoredOutcome,
    TermCatalog,
    TermRef,
    TraceStep,
    UtteranceTerms,
)
from statute_decider.llm import LLMCall, LLMClient
from statute_decider.nodes.llm_io import (
    DecideResponse,
    GroundResponse,
    JustifyResponse,
    ValueResponse,
    tri_to_bool,
)
from statute_decider.nodes.rendering import (
    render_claims,
    render_facts,
    render_registry,
    render_rules,
    render_term_catalog,
    render_term_refs,
    render_trace_text,
)
from statute_decider.strategies import PromptTemplate


def _llm_provenance(
    node: str, strategy: str | None, prompt: PromptTemplate, result
) -> Provenance:
    return Provenance(
        node=node,
        method="llm",
        strategy=strategy,
        provider=result.provider,
        model=result.model,
        prompt_id=prompt.prompt_id,
        prompt_hash=prompt.sha256,
    )


# --- utterance_term / term_claim (llm, strategy=ground; fusable) ---


def ground_utterance(
    client: LLMClient,
    model_id: str,
    prompt: PromptTemplate,
    *,
    scenario_id: str,
    utterance: str,
    catalog: TermCatalog,
    fused: bool,
    temperature: float = 0.0,
    max_output_tokens: int = 8192,
    meta: dict | None = None,
) -> tuple[UtteranceTerms, ClaimSet | None]:
    """One llm call recognizes terms (and, when fused, assigns asserted values).

    Both node values are recorded either way; fusion is an execution
    optimization, never a scoring change.
    """
    user = prompt.render(
        utterance=utterance.strip(),
        term_catalog=render_term_catalog(catalog),
    )
    result = client.complete(
        LLMCall(
            model_id=model_id,
            system=prompt.system,
            user=user,
            response_model=GroundResponse,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            meta={**(meta or {}), "node": "utterance_term", "prompt_id": prompt.prompt_id},
        )
    )
    known_ids = catalog.term_ids()
    items = [item for item in result.parsed.items if item.term_id in known_ids]
    terms = UtteranceTerms(
        scenario_id=scenario_id,
        term_refs=[TermRef(term_id=item.term_id, span=item.span) for item in items],
        provenance=_llm_provenance("utterance_term", "ground", prompt, result),
    )
    claims: ClaimSet | None = None
    if fused:
        claims = ClaimSet(
            scenario_id=scenario_id,
            claims=[
                ClaimPremise(
                    premise_id=f"claim_{item.term_id}",
                    term_id=item.term_id,
                    value=tri_to_bool(item.value),
                    span=item.span,
                )
                for item in items
                if tri_to_bool(item.value) is not None
            ],
            provenance=_llm_provenance("term_claim", "ground", prompt, result),
        )
    return terms, claims


def value_claims(
    client: LLMClient,
    model_id: str,
    prompt: PromptTemplate,
    *,
    scenario_id: str,
    utterance: str,
    catalog: TermCatalog,
    recognized: UtteranceTerms,
    temperature: float = 0.0,
    max_output_tokens: int = 8192,
    meta: dict | None = None,
) -> ClaimSet:
    """Staged path: given recognized terms, assign asserted values only."""
    term_ids = sorted(recognized.term_ids())
    user = prompt.render(
        utterance=utterance.strip(),
        recognized_terms=render_term_refs(term_ids, catalog),
    )
    result = client.complete(
        LLMCall(
            model_id=model_id,
            system=prompt.system,
            user=user,
            response_model=ValueResponse,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            meta={**(meta or {}), "node": "term_claim", "prompt_id": prompt.prompt_id},
        )
    )
    allowed = set(term_ids)
    return ClaimSet(
        scenario_id=scenario_id,
        claims=[
            ClaimPremise(
                premise_id=f"claim_{item.term_id}",
                term_id=item.term_id,
                value=tri_to_bool(item.value),
                span=item.span,
            )
            for item in result.parsed.items
            if item.term_id in allowed and tri_to_bool(item.value) is not None
        ],
        provenance=_llm_provenance("term_claim", None, prompt, result),
    )


# --- record_term (match: deterministic field-to-term matching) ---


def match_record_terms(
    register_id: str,
    fields: list[str],
    catalog: TermCatalog,
) -> RecordTermMap:
    """Deterministic name/alias matching of raw fields against the term catalog."""
    from statute_decider.core.terms import FieldToTerm

    by_id = catalog.by_id()
    by_atom = {
        (term.propositional or "").lower(): term.term_id
        for term in catalog.terms
        if term.propositional
    }
    mappings = []
    for field in fields:
        key = field.strip().lower()
        term_id = key if key in by_id else by_atom.get(key)
        if term_id:
            mappings.append(
                FieldToTerm(
                    term_id=term_id,
                    register_id=register_id,
                    field=field,
                    transform="name match",
                )
            )
    return RecordTermMap(
        register_id=register_id,
        mappings=mappings,
        provenance=Provenance(node="record_term", method="match", provider="code"),
    )


# --- term_fact (lookup: deterministic via the mapping) ---


def lookup_facts(
    scenario_id: str,
    registry: RegistryState,
    mappings: list[RecordTermMap],
) -> FactSet:
    """Apply field-to-term mappings to the registry state.

    Unavailable registers contribute coverage (their mapped terms become
    ``unavailable_terms``) but no values. Conflicting values from available
    registers withdraw the fact and mark the term as a conflict. Null fields
    are declared-but-unknown: no fact.
    """
    registers = registry.by_id()
    facts: dict[str, FactPremise] = {}
    unavailable_registers: list[str] = []
    unavailable_terms: set[str] = set()
    conflicts: set[str] = set()
    covered_terms: set[str] = set()

    for mapping in mappings:
        reg = registers.get(mapping.register_id)
        if reg is None:
            continue
        if reg.availability != Availability.REGISTER_UNAVAILABLE:
            covered_terms.update(entry.term_id for entry in mapping.mappings)
        if reg.availability == Availability.REGISTER_UNAVAILABLE:
            if reg.register_id not in unavailable_registers:
                unavailable_registers.append(reg.register_id)
            covered = {
                m.term_id
                for m in mapping.mappings
                if any(m.field in rec.fields for rec in reg.records)
            }
            unavailable_terms.update(covered)
            continue
        for entry in mapping.mappings:
            for record in reg.records:
                if entry.field not in record.fields:
                    continue
                value = record.fields[entry.field]
                if value is None:
                    continue
                existing = facts.get(entry.term_id)
                if existing is not None and existing.value != value:
                    conflicts.add(entry.term_id)
                    continue
                if existing is None:
                    facts[entry.term_id] = FactPremise(
                        premise_id=f"fact_{entry.term_id}",
                        term_id=entry.term_id,
                        value=value,
                        register_id=reg.register_id,
                        record_id=record.record_id,
                        field=entry.field,
                        warrant=reg.warrant,
                    )

    for term_id in conflicts:
        facts.pop(term_id, None)

    return FactSet(
        scenario_id=scenario_id,
        facts=[facts[tid] for tid in sorted(facts)],
        unavailable_registers=sorted(unavailable_registers),
        unavailable_terms=sorted(unavailable_terms - set(facts)),
        conflicts=sorted(conflicts),
        covered_terms=sorted(covered_terms),
        provenance=Provenance(node="term_fact", method="lookup", provider="code"),
    )


# --- premise_outcome (llm decide: the llm-only condition's decision on raw sources) ---


def decide_llm(
    client: LLMClient,
    model_id: str,
    prompt: PromptTemplate,
    *,
    scenario_id: str,
    statute_text: str | None,
    utterance: str,
    registry: RegistryState | None,
    catalog: TermCatalog | None = None,
    rules: RuleSet | None = None,
    claims: ClaimSet | None = None,
    facts: FactSet | None = None,
    temperature: float = 0.0,
    max_output_tokens: int = 8192,
    meta: dict | None = None,
) -> PremiseOutcome:
    """LLM decision. The prompt's placeholders select the inputs: raw sources
    (llm-only), raw sources + oracle rules (llm-only-plus-rules), or the solver's
    own inputs — rules + claims + facts, no statute text (llm-decides-on-*)."""
    placeholders: dict[str, str] = {
        "utterance": utterance.strip() or "(no request text)",
    }
    wants = {name for name in ("statute", "registry", "rules", "claims", "facts") if f"{{{name}}}" in prompt.body}
    if "statute" in wants:
        if statute_text is None:
            raise RuntimeError(f"Prompt {prompt.prompt_id} expects {{statute}} but statute_text is unbound.")
        placeholders["statute"] = statute_text.strip()
    if "registry" in wants:
        if registry is None:
            raise RuntimeError(f"Prompt {prompt.prompt_id} expects {{registry}} but registry_record is unbound.")
        placeholders["registry"] = render_registry(registry)
    if "rules" in wants:
        if rules is None:
            raise RuntimeError(f"Prompt {prompt.prompt_id} expects {{rules}} but term_rule is unbound.")
        placeholders["rules"] = render_rules(rules, catalog)
    if "claims" in wants:
        placeholders["claims"] = render_claims(claims)
    if "facts" in wants:
        placeholders["facts"] = render_facts(facts)
    user, prefix_len = prompt.render_with_prefix("statute", **placeholders)
    result = client.complete(
        LLMCall(
            model_id=model_id,
            system=prompt.system,
            user=user,
            response_model=DecideResponse,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            meta={**(meta or {}), "node": "premise_outcome", "prompt_id": prompt.prompt_id},
            cache_prefix_len=prefix_len,
        )
    )
    decision: DecideResponse = result.parsed
    known_ids = catalog.term_ids() if catalog is not None else set()
    missing_terms = [
        MissingTerm(term_id=item, reason=MissingReason.NO_VALUE)
        for item in decision.missing_terms
        if item in known_ids
    ]
    free_missing = [item for item in decision.missing_terms if item not in known_ids]
    state = OutcomeState(decision.outcome) if decision.outcome != "NEED_MORE_INFO" else (
        OutcomeState.NEED_MORE_INFO
    )
    return PremiseOutcome(
        scenario_id=scenario_id,
        state=state,
        scored_as=ScoredOutcome(decision.outcome),
        missing_terms=missing_terms,
        free_missing=free_missing,
        note=decision.reason,
        provenance=_llm_provenance("premise_outcome", "decide", prompt, result),
    )


# --- outcome_trace (render / llm justify) ---


def render_trace(
    scenario_id: str,
    outcome: PremiseOutcome,
    rules: RuleSet,
    catalog: TermCatalog,
) -> OutcomeTrace:
    steps, justification = render_trace_text(outcome, rules, catalog)
    return OutcomeTrace(
        scenario_id=scenario_id,
        steps=[TraceStep(step=i + 1, message=msg) for i, msg in enumerate(steps)],
        justification=justification,
        provenance=Provenance(
            node="outcome_trace",
            method="render",
            provider="code",
            consumed_artifact="render:default",
        ),
    )


def justify_llm(
    client: LLMClient,
    model_id: str,
    prompt: PromptTemplate,
    *,
    scenario_id: str,
    statute_text: str,
    utterance: str,
    outcome: PremiseOutcome,
    temperature: float = 0.0,
    max_output_tokens: int = 8192,
    meta: dict | None = None,
) -> OutcomeTrace:
    """LLM-written justification (the only trace an llm-decided outcome can have)."""
    missing = ", ".join(sorted(outcome.missing_term_ids() | set(outcome.free_missing))) or "(none)"
    user, prefix_len = prompt.render_with_prefix(
        "statute",
        statute=statute_text.strip(),
        utterance=utterance.strip() or "(no request text)",
        outcome=outcome.scored_as.value,
        missing_terms=missing,
        reason=outcome.note or "(none)",
    )
    result = client.complete(
        LLMCall(
            model_id=model_id,
            system=prompt.system,
            user=user,
            response_model=JustifyResponse,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            meta={**(meta or {}), "node": "outcome_trace", "prompt_id": prompt.prompt_id},
            cache_prefix_len=prefix_len,
        )
    )
    justification: JustifyResponse = result.parsed
    return OutcomeTrace(
        scenario_id=scenario_id,
        steps=[TraceStep(step=i + 1, message=msg) for i, msg in enumerate(justification.steps)],
        justification=justification.justification,
        provenance=_llm_provenance("outcome_trace", "justify", prompt, result),
    )
