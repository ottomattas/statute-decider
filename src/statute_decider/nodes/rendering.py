"""Deterministic text renderings of graph values (prompt inputs + trace)."""

from __future__ import annotations

import json

from statute_decider.core import (
    PremiseOutcome,
    RegistryState,
    RuleSet,
    TermCatalog,
)


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
        refs = "; ".join(
            f"{anchor.clause_title or anchor.clause_id}" for anchor in rule.law_references
        )
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
