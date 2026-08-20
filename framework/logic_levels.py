"""Level-specific rendering, artifact builders, and trace formatting for `framework`."""

from __future__ import annotations

from dataclasses import dataclass

from schemas import (
    DomainArtifact,
    DomainClaim,
    DomainRule,
    EvidenceSnippet,
    ExtractionRunMetadata,
    IntentArtifact,
    IntentClaim,
    LawReference,
    LogicLevel,
    OutcomeDefinition,
    PremiseEvaluation,
    PromptMetadata,
    RuleKind,
    RuleTraceRow,
    SolutionArtifact,
)
from uncertainty_routing import routing_for_reason_code
from use_case_files import UseCaseDefinition


@dataclass(frozen=True)
class LogicLevelSpec:
    """Display and lowering metadata for one logic level."""

    level: LogicLevel
    display_name: str
    lowering_note: str


LOGIC_LEVEL_SPECS: dict[LogicLevel, LogicLevelSpec] = {
    LogicLevel.PROPOSITIONAL: LogicLevelSpec(
        level=LogicLevel.PROPOSITIONAL,
        display_name="Propositional logic",
        lowering_note="The selected logic level already matches the Boolean Z3 core.",
    ),
    LogicLevel.PREDICATE: LogicLevelSpec(
        level=LogicLevel.PREDICATE,
        display_name="Predicate-style logic",
        lowering_note=(
            "Predicate-style forms are preserved in the artifacts and then lowered explicitly "
            "to propositional atoms for the small Z3 core."
        ),
    ),
    LogicLevel.HIGHER_ORDER: LogicLevelSpec(
        level=LogicLevel.HIGHER_ORDER,
        display_name="Higher-order-style logic",
        lowering_note=(
            "Higher-order-style application forms are preserved in the artifacts and then lowered "
            "explicitly to propositional atoms for the small Z3 core."
        ),
    ),
}


def _claim_form(template: object, logic_level: LogicLevel) -> str:
    if logic_level == LogicLevel.PROPOSITIONAL:
        return template.propositional
    if logic_level == LogicLevel.PREDICATE:
        return template.predicate
    return template.higher_order


def _outcome_form(template: object, logic_level: LogicLevel) -> str:
    if logic_level == LogicLevel.PROPOSITIONAL:
        return template.propositional
    if logic_level == LogicLevel.PREDICATE:
        return template.predicate
    return template.higher_order


def _path_or_inline(value: str | None) -> str:
    return value or "(inline text)"


def _prompt_summary(prompt: PromptMetadata) -> str:
    return (
        f"system={_path_or_inline(prompt.system_prompt_path)} [{prompt.system_prompt_sha256 or 'no-hash'}], "
        f"user={_path_or_inline(prompt.user_prompt_path)} [{prompt.user_prompt_sha256 or 'no-hash'}]"
    )


def claim_catalog_text(use_case: UseCaseDefinition, logic_level: LogicLevel) -> str:
    """Render the claim catalog for prompts and debugging."""
    lines: list[str] = []
    for template in use_case.claims:
        lines.append(
            f"- {template.claim_id}: {template.label} | form={_claim_form(template, logic_level)} | "
            f"source={template.source_type.value}"
        )
    return "\n".join(lines)


def rule_catalog_text(use_case: UseCaseDefinition, logic_level: LogicLevel) -> str:
    """Render the rule catalog for prompts and debugging."""
    lines: list[str] = []
    for template in use_case.rules:
        lines.append(f"- {template.rule_id}: {render_rule_formula(use_case, template, logic_level)}")
    return "\n".join(lines)


def outcome_catalog_text(use_case: UseCaseDefinition, logic_level: LogicLevel) -> str:
    """Render the outcome catalog for prompts and debugging."""
    lines: list[str] = []
    for template in use_case.outcomes:
        lines.append(
            f"- {template.outcome_id}: {template.label} | form={_outcome_form(template, logic_level)}"
        )
    return "\n".join(lines)


def render_rule_formula(use_case: UseCaseDefinition, template: object, logic_level: LogicLevel) -> str:
    """Render one rule in the selected logic level."""
    premise = " AND ".join(
        _claim_form(use_case.claim_by_id[claim_id], logic_level) for claim_id in template.when_claim_ids
    )
    if template.kind == RuleKind.SET_FALSE_IF_ALL:
        conclusion = f"NOT {_claim_form(use_case.claim_by_id[template.target_claim_id], logic_level)}"
    else:
        conclusion = _outcome_form(use_case.outcome_by_id[template.target_outcome_id], logic_level)
    return f"({premise}) -> {conclusion}" if len(template.when_claim_ids) > 1 else f"{premise} -> {conclusion}"


def render_rule_lowering(use_case: UseCaseDefinition, template: object) -> str:
    """Render the propositional lowering for one rule."""
    premise = " AND ".join(use_case.claim_by_id[claim_id].lowered_atom for claim_id in template.when_claim_ids)
    if template.kind == RuleKind.SET_FALSE_IF_ALL:
        conclusion = f"NOT {use_case.claim_by_id[template.target_claim_id].lowered_atom}"
    else:
        conclusion = use_case.outcome_by_id[template.target_outcome_id].lowered_atom
    return f"({premise}) -> {conclusion}" if len(template.when_claim_ids) > 1 else f"{premise} -> {conclusion}"


def build_domain_artifact(
    use_case: UseCaseDefinition,
    logic_level: LogicLevel,
    law_text: str,
    *,
    title: str | None = None,
    run_metadata: ExtractionRunMetadata | None = None,
) -> DomainArtifact:
    """Build a checked domain artifact from the selected external use case."""
    claims = [
        DomainClaim(
            claim_id=template.claim_id,
            lowered_atom=template.lowered_atom,
            label=template.label,
            description=template.description,
            source_type=template.source_type,
            formal_text=_claim_form(template, logic_level),
            law_references=[LawReference.model_validate(reference.model_dump()) for reference in template.law_references],
        )
        for template in use_case.claims
    ]
    outcomes = [
        OutcomeDefinition(
            outcome_id=template.outcome_id,
            lowered_atom=template.lowered_atom,
            label=template.label,
            formal_text=_outcome_form(template, logic_level),
        )
        for template in use_case.outcomes
    ]
    rules = [
        DomainRule(
            rule_id=template.rule_id,
            kind=template.kind,
            label=template.label,
            when_claim_ids=list(template.when_claim_ids),
            formal_text=render_rule_formula(use_case, template, logic_level),
            lowered_formula=render_rule_lowering(use_case, template),
            target_outcome_id=template.target_outcome_id,
            target_claim_id=template.target_claim_id,
            law_references=[LawReference.model_validate(reference.model_dump()) for reference in template.law_references],
        )
        for template in use_case.rules
    ]
    return DomainArtifact(
        logic_level=logic_level,
        title=title or use_case.title,
        law_text=law_text,
        lowered_view_note=LOGIC_LEVEL_SPECS[logic_level].lowering_note,
        allow_outcome_id=use_case.allow_outcome_id,
        deny_outcome_id=use_case.deny_outcome_id,
        run_metadata=run_metadata or ExtractionRunMetadata(prompt=PromptMetadata()),
        claims=claims,
        outcomes=outcomes,
        rules=rules,
    )


def build_intent_artifact(
    use_case: UseCaseDefinition,
    request_text: str,
    logic_level: LogicLevel,
    assignments: dict[str, bool | None],
    *,
    reasons: dict[str, str] | None = None,
    snippets: dict[str, list[str]] | None = None,
    run_metadata: ExtractionRunMetadata | None = None,
) -> IntentArtifact:
    """Build an intent artifact from explicit claim assignments."""
    reasons = reasons or {}
    snippets = snippets or {}
    claims = []
    for template in use_case.claims:
        claim_snippets = [
            EvidenceSnippet(snippet=item, note="Matched user text")
            for item in snippets.get(template.claim_id, [])
        ]
        claims.append(
            IntentClaim(
                claim_id=template.claim_id,
                lowered_atom=template.lowered_atom,
                label=template.label,
                description=template.description,
                source_type=template.source_type,
                formal_text=_claim_form(template, logic_level),
                value=assignments.get(template.claim_id),
                reason=reasons.get(template.claim_id, ""),
                provenance=claim_snippets,
            )
        )
    return IntentArtifact(
        logic_level=logic_level,
        request_text=request_text,
        lowered_view_note=LOGIC_LEVEL_SPECS[logic_level].lowering_note,
        run_metadata=run_metadata or ExtractionRunMetadata(prompt=PromptMetadata()),
        claims=claims,
    )


def ensure_executable_logic_level(logic_level: LogicLevel) -> None:
    """Raise a clear error until non-propositional execution is implemented."""
    if logic_level != LogicLevel.PROPOSITIONAL:
        raise ValueError(
            "Only `propositional` is executable in this iteration. "
            f"`{logic_level.value}` is reserved for a future expansion."
        )


def format_claim_value(value: bool | None) -> str:
    """Return a compact truth symbol for the text trace."""
    if value is True:
        return "T"
    if value is False:
        return "F"
    return "U"


def format_rule_trace_row(row: RuleTraceRow) -> str:
    """Render one trace row as a short plain-text line."""
    premise_bits = ", ".join(
        f"{premise.formal_text}={format_claim_value(premise.value)}" for premise in row.premises
    )
    return f"{row.rule_id} [{row.status.value}] :: {row.formal_text} :: {premise_bits}"


def _append_metadata(lines: list[str], label: str, metadata: ExtractionRunMetadata) -> None:
    """Render one extraction metadata block."""
    lines.extend(
        [
            label,
            f"  generated_at_utc: {metadata.generated_at_utc or '(not recorded)'}",
            f"  model_name: {metadata.model_name or '(not recorded)'}",
            f"  source_path: {_path_or_inline(metadata.source_path)}",
            f"  prompts: {_prompt_summary(metadata.prompt)}",
        ]
    )


def _append_law_references(lines: list[str], law_references: list[LawReference], indent: str = "    ") -> None:
    """Render one law-reference list into the plain-text trace."""
    for reference in law_references:
        lines.append(f"{indent}- {reference.clause_title} [{reference.clause_id}]")
        lines.append(f"{indent}  text: {reference.clause_text}")
        if reference.note:
            lines.append(f"{indent}  note: {reference.note}")


def _append_intent_claims(lines: list[str], solution: SolutionArtifact) -> None:
    """Render the extracted intent claims and their provenance."""
    if not solution.intent_claims:
        return
    lines.append("")
    lines.append("INTENT CLAIMS")
    for claim in solution.intent_claims:
        lines.append(
            f"- {claim.claim_id} [{claim.formal_text}] = {format_claim_value(claim.value)} "
            f"(source_type={claim.source_type.value})"
        )
        if claim.reason:
            lines.append(f"  reason: {claim.reason}")
        if claim.provenance:
            lines.append("  provenance:")
            for snippet in claim.provenance:
                lines.append(f"    - {snippet.snippet}")
                if snippet.note:
                    lines.append(f"      note: {snippet.note}")


def _append_domain_summary(lines: list[str], solution: SolutionArtifact) -> None:
    """Render the extracted domain claims and rules with law grounding."""
    if solution.domain_claims:
        lines.append("")
        lines.append("DOMAIN CLAIMS")
        for claim in solution.domain_claims:
            lines.append(
                f"- {claim.claim_id} [{claim.formal_text}] (source_type={claim.source_type.value})"
            )
            _append_law_references(lines, claim.law_references)
    if solution.domain_rules:
        lines.append("")
        lines.append("DOMAIN RULES")
        for rule in solution.domain_rules:
            lines.append(f"- {rule.rule_id}: {rule.formal_text}")
            lines.append(f"  lowered: {rule.lowered_formula}")
            _append_law_references(lines, rule.law_references)


def _append_db_pass_summary(lines: list[str], solution: SolutionArtifact) -> None:
    """Render an explicit summary for DB-pass cases, especially DB-then-DENY paths."""
    if len(solution.snapshots) < 2:
        return
    initial = solution.snapshots[0]
    final = solution.snapshots[-1]
    lines.append("")
    lines.append("MULTI-SNAPSHOT SUMMARY")
    lines.append(f"- initial={initial.outcome.value} -> final={final.outcome.value}")
    if final.note:
        lines.append(f"  final_note: {final.note}")


def render_solution_trace(solution: SolutionArtifact) -> str:
    """Render the final reasoning trace for the CLI explanation step."""
    level_spec = LOGIC_LEVEL_SPECS[solution.logic_level]
    lines = [
        f"LOGIC LEVEL: {level_spec.display_name} ({solution.logic_level.value})",
        f"LOWERING NOTE: {solution.lowered_view_note}",
        f"DOMAIN: {solution.domain_title}",
        f"REQUEST: {solution.request_text}",
        f"EXTRACTED CLAIM COUNT: {solution.extracted_claim_count}",
        f"EXTRACTED RULE COUNT: {solution.extracted_rule_count}",
    ]
    if solution.blocked_at_step:
        reason_code_value = solution.block_reason_code.value if solution.block_reason_code else ""
        routing = routing_for_reason_code(solution.block_reason_code)
        reason_code_line = reason_code_value
        if routing is not None:
            reason_code_line = f"[{routing.code}:{reason_code_value}] {reason_code_value}"
        lines.extend(
            [
                f"BLOCKED AT STEP: {solution.blocked_at_step}",
                f"BLOCK REASON CODE: {reason_code_line}",
            ]
        )
    if solution.unresolved_claim_ids:
        lines.append(f"UNRESOLVED CLAIM IDS: {', '.join(solution.unresolved_claim_ids)}")

    lines.extend(
        [
            "",
            "RUN METADATA",
            f"  solve_generated_at_utc: {solution.solve_metadata.generated_at_utc or '(not recorded)'}",
            f"  domain_artifact_path: {_path_or_inline(solution.solve_metadata.domain_artifact_path)}",
            f"  intent_artifact_path: {_path_or_inline(solution.solve_metadata.intent_artifact_path)}",
            f"  mock_db_path: {_path_or_inline(solution.solve_metadata.mock_db_path)}",
        ]
    )
    _append_metadata(lines, "INTENT EXTRACTION METADATA", solution.intent_metadata)
    _append_metadata(lines, "DOMAIN EXTRACTION METADATA", solution.domain_metadata)
    _append_intent_claims(lines, solution)
    _append_domain_summary(lines, solution)
    _append_db_pass_summary(lines, solution)

    lines.append("")
    lines.append("TRACE EVENTS")
    for event in solution.trace_events:
        lines.append(f"[{event.stage}] {event.message}")
    if solution.lookup_events:
        lines.append("")
        lines.append("DB LOOKUPS")
        for event in solution.lookup_events:
            returned = ", ".join(
                f"{claim_id}={value}" for claim_id, value in sorted(event.returned_values.items())
            )
            lines.append(
                f"- {event.source_label} ({event.source_id}) -> [{returned}] for {', '.join(event.requested_claim_ids)}"
            )
            if event.note:
                lines.append(f"  note: {event.note}")
    for snapshot in solution.snapshots:
        lines.append("")
        lines.append(f"SNAPSHOT: {snapshot.stage}")
        lines.append(f"  outcome: {snapshot.outcome.value}")
        if snapshot.note:
            lines.append(f"  note: {snapshot.note}")
        if snapshot.missing_db_claim_ids:
            lines.append(f"  missing_db: {', '.join(snapshot.missing_db_claim_ids)}")
        if snapshot.missing_user_claim_ids:
            lines.append(f"  missing_user: {', '.join(snapshot.missing_user_claim_ids)}")
        lines.append("  resolved_claims:")
        for claim in snapshot.resolved_claims:
            suffix = (
                f" [{claim.uncertainty_code}]" if claim.uncertainty_code else ""
            )
            lines.append(
                f"    - {claim.formal_text} [{claim.lowered_atom}] = {format_claim_value(claim.value)} "
                f"(source_type={claim.source_type.value}, resolved_from={claim.resolved_from}){suffix}"
            )
            if claim.reason:
                lines.append(f"      reason: {claim.reason}")
        lines.append("  rule_trace:")
        for row in snapshot.rule_trace:
            lines.append(f"    - {format_rule_trace_row(row)}")
    lines.append("")
    lines.append(f"FINAL OUTCOME: {solution.final_outcome.value}")
    return "\n".join(lines)


def claim_premise_for_trace(domain: DomainArtifact, claim_id: str, value: bool | None) -> PremiseEvaluation:
    """Create one premise row from the checked domain artifact."""
    claim = next(item for item in domain.claims if item.claim_id == claim_id)
    return PremiseEvaluation(
        claim_id=claim.claim_id,
        label=claim.label,
        formal_text=claim.formal_text,
        lowered_atom=claim.lowered_atom,
        value=value,
    )
