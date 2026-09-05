"""Deterministic text renderings of graph values (prompt inputs + trace)."""

from __future__ import annotations

import json

from statute_decider.core import (
    ClaimSet,
    FactSet,
    PremiseOutcome,
    RegistryState,
    RuleSet,
    TermCatalog,
)
from statute_decider.core.terms import ClauseAnchor
from statute_decider.legislation.references import display_reference


def _display_anchor(anchor: ClauseAnchor) -> str:
    """Display form only ("§ 11 (5) 1)"), never the ``<act_slug>/<eId>`` key.

    ``clause_title`` is the corpus-checked display form (``sd validate``); when
    it is empty the form is derived from the reference itself.
    """
    if anchor.clause_title:
        return anchor.clause_title
    try:
        return display_reference(anchor.clause_id)
    except ValueError:
        return anchor.clause_id


def render_term_catalog(catalog: TermCatalog) -> str:
    """Term catalog as prompt-ready lines (labels and definitions, not rules)."""
    lines = []
    for term in catalog.terms:
        definition = f" — {term.definition}" if term.definition else ""
        lines.append(f"- {term.term_id}: {term.label}{definition}")
    return "\n".join(lines) or "(empty catalog)"


def render_term_refs(term_ids: list[str], catalog: TermCatalog) -> str:
    by_id = catalog.by_id()
    lines = []
    for term_id in term_ids:
        term = by_id.get(term_id)
        label = term.label if term else ""
        lines.append(f"- {term_id}: {label}")
    return "\n".join(lines) or "(none)"


def render_registry(registry: RegistryState) -> str:
    """Raw registry payload as compact JSON — exactly what a register returns."""
    return json.dumps(
        registry.model_dump(exclude={"node"}), ensure_ascii=False, indent=2, default=str
    )


def render_rules(rules: RuleSet, catalog: TermCatalog | None = None) -> str:
    """Hand-authored encoding as prompt-ready variables + readable rules.

    Used by the LLM-decider cell: the model is given the correct rules and
    asked to apply them, so the comparison with the solver is unattackable.
    """
    var_lines: list[str] = []
    if catalog is not None:
        for term in catalog.terms:
            definition = f" — {term.definition}" if term.definition else ""
            var_lines.append(f"- {term.term_id}: {term.label}{definition}")
    allow = rules.allow_outcome_id
    deny = rules.deny_outcome_id
    rule_lines: list[str] = []
    for rule in rules.rules:
        premise = " AND ".join(rule.when_term_ids) or "(empty)"
        if rule.rule_kind.value == "set_false_if_all":
            conclusion = f"NOT {rule.target_term_id}"
        elif rule.target_outcome_id == allow:
            conclusion = "ALLOW"
        elif rule.target_outcome_id == deny:
            conclusion = "DENY"
        else:
            conclusion = str(rule.target_outcome_id)
        rule_lines.append(
            f"- {rule.premise_id} ({rule.rule_kind.value}): {premise} -> {conclusion}"
        )
    variables = "\n".join(var_lines) if var_lines else "(no catalog)"
    rendered = "\n".join(rule_lines) if rule_lines else "(no rules)"
    return (
        "REFERENCE DECISION RULES (hand-authored encoding of the statute; "
        "boolean variables are the term ids):\n"
        f"ALLOW outcome: {allow}\nDENY outcome: {deny}\n"
        f"Variables:\n{variables}\n"
        f"Rules:\n{rendered}"
    )


def render_claims(claims: ClaimSet | None) -> str:
    """Asserted values, exactly as the solver receives them."""
    if claims is None or not claims.claims:
        return "CLAIMS (asserted by the applicant): (none)"
    lines = []
    for claim in claims.claims:
        span = f' — "{claim.span}"' if claim.span else ""
        lines.append(f"- {claim.term_id} = {'true' if claim.value else 'false'}{span}")
    return "CLAIMS (asserted by the applicant; fallible, not verified):\n" + "\n".join(lines)


def render_facts(facts: FactSet | None) -> str:
    """Warranted values plus register coverage, exactly as the solver receives them."""
    if facts is None:
        return "FACTS (from registers): (no register chain)"
    lines = []
    for fact in facts.facts:
        source = f"{fact.register_id}.{fact.record_id}.{fact.field}".strip(".")
        lines.append(
            f"- {fact.term_id} = {'true' if fact.value else 'false'} "
            f"[warrant: {fact.warrant.value}; source: {source or 'n/a'}]"
        )
    body = "\n".join(lines) if lines else "(no facts returned)"
    extras = [
        f"Registers unavailable this scenario: {', '.join(facts.unavailable_registers) or 'none'}",
        f"Terms those unavailable registers would answer: {', '.join(facts.unavailable_terms) or 'none'}",
        f"Terms an available register covers (can be checked): {', '.join(facts.covered_terms) or 'none'}",
        f"Terms with conflicting register values: {', '.join(facts.conflicts) or 'none'}",
    ]
    return "FACTS (from registers):\n" + body + "\n" + "\n".join(extras)


def render_trace_text(
    outcome: PremiseOutcome, rules: RuleSet, catalog: TermCatalog
) -> tuple[list[str], str]:
    """Default render template: inference record -> human-readable justification.

    Pure function of the decision payload; performs no reasoning and cannot
    change the outcome.
    """
    by_rule = {rule.premise_id: rule for rule in rules.rules}
    by_term = catalog.by_id()
    steps: list[str] = []

    used = [
        f"{term_id}={'true' if value else 'false'}"
        for term_id, value in sorted(outcome.valuation.items())
    ]
    steps.append("Valuation used: " + (", ".join(used) if used else "(none)"))

    for fired in outcome.fired_rules:
        rule = by_rule.get(fired.premise_id)
        if rule is None:
            steps.append(f"Rule {fired.premise_id} fired -> {fired.effect}.")
            continue
        refs = "; ".join(_display_anchor(anchor) for anchor in rule.law_references)
        label = rule.label or rule.premise_id
        steps.append(
            f"Rule {rule.premise_id} ({label}) fired -> {fired.effect}"
            + (f" [{refs}]" if refs else "")
            + "."
        )
    if not outcome.fired_rules:
        steps.append("No rule fired under the current valuation.")

    for missing in outcome.missing_terms:
        term = by_term.get(missing.term_id)
        label = term.label if term else missing.term_id
        steps.append(
            f"Missing decision-grade value: {missing.term_id} ({label}) — {missing.reason.value}."
        )

    steps.append(f"Decision: {outcome.state.value} (scored as {outcome.scored_as.value}).")
    if outcome.note:
        steps.append(outcome.note)

    justification = " ".join(steps)
    return steps, justification
