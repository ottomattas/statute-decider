"""Small Z3-backed reasoner for file-backed `framework` use cases."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from z3 import And, Bool, Implies, Not, Solver, sat

from logic_levels import (
    claim_premise_for_trace,
    ensure_executable_logic_level,
)
from mock_db import lookup_claims
from schemas import (
    BlockReasonCode,
    CaseBundle,
    ClaimSource,
    DomainArtifact,
    DomainRule,
    IntentArtifact,
    LookupEvent,
    ResolvedClaim,
    RuleKind,
    RuleStatus,
    RuleTraceRow,
    SolveSnapshot,
    SolverOutcome,
    SolutionArtifact,
    TraceEvent,
)
from uncertainty_routing import (
    UncertaintyRouting,
    classify_claim_uncertainty,
    classify_rule_uncertainty,
    has_trust_only_resolution,
    trust_only_claim_ids,
)


def _make_vars(symbol_ids: set[str]) -> dict[str, Any]:
    return {symbol_id: Bool(f"framework_{symbol_id}") for symbol_id in sorted(symbol_ids)}


def _solver_symbol_ids(domain: DomainArtifact) -> set[str]:
    symbol_ids = {claim.claim_id for claim in domain.claims}
    symbol_ids.update(outcome.outcome_id for outcome in domain.outcomes)
    for rule in domain.rules:
        symbol_ids.update(rule.when_claim_ids)
        if rule.target_claim_id:
            symbol_ids.add(rule.target_claim_id)
        if rule.target_outcome_id:
            symbol_ids.add(rule.target_outcome_id)
    return symbol_ids


def _rule_lhs(vars_by_id: dict[str, Any], rule: DomainRule) -> Any:
    antecedents = [vars_by_id[claim_id] for claim_id in rule.when_claim_ids]
    return And(antecedents) if len(antecedents) > 1 else antecedents[0]


def _apply_facts(solver: Solver, vars_by_id: dict[str, Any], facts: dict[str, bool | None]) -> None:
    for claim_id, value in facts.items():
        if claim_id not in vars_by_id or value is None:
            continue
        solver.add(vars_by_id[claim_id] if value else Not(vars_by_id[claim_id]))


def _build_solver(domain: DomainArtifact, facts: dict[str, bool | None]) -> tuple[Solver, dict[str, Any]]:
    vars_by_id = _make_vars(_solver_symbol_ids(domain))
    solver = Solver()
    for rule in domain.rules:
        lhs = _rule_lhs(vars_by_id, rule)
        if rule.kind == RuleKind.ALLOW_IF_ALL:
            solver.add(Implies(lhs, vars_by_id[rule.target_outcome_id]))
        elif rule.kind == RuleKind.DENY_IF_ALL:
            solver.add(Implies(lhs, vars_by_id[rule.target_outcome_id]))
        elif rule.kind == RuleKind.SET_FALSE_IF_ALL:
            solver.add(Implies(lhs, Not(vars_by_id[rule.target_claim_id])))
    _apply_facts(solver, vars_by_id, facts)
    return solver, vars_by_id


def _entailed_value(domain: DomainArtifact, facts: dict[str, bool | None], symbol_id: str) -> bool | None:
    neg_solver, neg_vars = _build_solver(domain, facts)
    neg_solver.add(Not(neg_vars[symbol_id]))
    if neg_solver.check() != sat:
        return True

    pos_solver, pos_vars = _build_solver(domain, facts)
    pos_solver.add(pos_vars[symbol_id])
    if pos_solver.check() != sat:
        return False

    return None


def _run_z3(domain: DomainArtifact, facts: dict[str, bool | None]) -> dict[str, Any]:
    try:
        base_solver, _ = _build_solver(domain, facts)
        if base_solver.check() != sat:
            return {
                "engine": "z3",
                "base_status": "unsat",
                "claim_values": {claim.claim_id: None for claim in domain.claims},
                "outcome_values": {outcome.outcome_id: None for outcome in domain.outcomes},
            }
        claim_values = {
            claim.claim_id: _entailed_value(domain, facts, claim.claim_id) for claim in domain.claims
        }
        outcome_values = {
            outcome.outcome_id: _entailed_value(domain, facts, outcome.outcome_id)
            for outcome in domain.outcomes
        }
        return {
            "engine": "z3",
            "base_status": "sat",
            "claim_values": claim_values,
            "outcome_values": outcome_values,
        }
    except Exception as exc:
        return {
            "engine": "z3",
            "base_status": "error",
            "error": str(exc),
            "claim_values": {claim.claim_id: None for claim in domain.claims},
            "outcome_values": {outcome.outcome_id: None for outcome in domain.outcomes},
        }


def _seed_claims(case_bundle: CaseBundle) -> list[ResolvedClaim]:
    """Seed the working valuation from the step-1 intent artifact."""
    intent_by_id = {claim.claim_id: claim for claim in case_bundle.intent.claims}
    resolved: list[ResolvedClaim] = []
    for claim in case_bundle.domain.claims:
        intent_claim = intent_by_id.get(claim.claim_id)
        resolved.append(
            ResolvedClaim(
                claim_id=claim.claim_id,
                lowered_atom=claim.lowered_atom,
                label=claim.label,
                source_type=claim.source_type,
                formal_text=claim.formal_text,
                value=intent_claim.value if intent_claim else None,
                resolved_from="intent" if intent_claim and intent_claim.value is not None else "unknown",
                reason=intent_claim.reason if intent_claim and intent_claim.reason else "No resolved value yet.",
            )
        )
    return resolved


def _fact_map(resolved_claims: list[ResolvedClaim]) -> dict[str, bool | None]:
    return {claim.claim_id: claim.value for claim in resolved_claims}


def _apply_derived_claims(
    domain: DomainArtifact,
    resolved_claims: list[ResolvedClaim],
    solver_summary: dict[str, Any],
) -> list[ResolvedClaim]:
    """Inject entailed claim values into the working valuation for tracing."""
    rows = deepcopy(resolved_claims)
    by_id = {row.claim_id: row for row in rows}
    if solver_summary["base_status"] != "sat":
        return rows
    for claim_id, entailed in solver_summary["claim_values"].items():
        row = by_id[claim_id]
        if entailed is None:
            continue
        if row.value is None:
            row.value = entailed
            row.resolved_from = "reasoner"
            row.reason = "Entailed by the Z3 core."
    return rows


def _trace_rule(
    domain: DomainArtifact,
    domain_rule: DomainRule,
    resolved_claims: list[ResolvedClaim],
) -> RuleTraceRow:
    by_id = {claim.claim_id: claim for claim in resolved_claims}
    true_claim_ids: list[str] = []
    false_claim_ids: list[str] = []
    unknown_claim_ids: list[str] = []
    premises = []
    for claim_id in domain_rule.when_claim_ids:
        value = by_id[claim_id].value
        premises.append(claim_premise_for_trace(domain, claim_id, value))
        if value is True:
            true_claim_ids.append(claim_id)
        elif value is False:
            false_claim_ids.append(claim_id)
        else:
            unknown_claim_ids.append(claim_id)
    if false_claim_ids:
        status = RuleStatus.BLOCKED
    elif unknown_claim_ids:
        status = RuleStatus.NEEDS_INFO
    else:
        status = RuleStatus.FIRES
    return RuleTraceRow(
        rule_id=domain_rule.rule_id,
        label=domain_rule.label,
        kind=domain_rule.kind,
        status=status,
        formal_text=domain_rule.formal_text,
        lowered_formula=domain_rule.lowered_formula,
        premises=premises,
        true_claim_ids=true_claim_ids,
        false_claim_ids=false_claim_ids,
        unknown_claim_ids=unknown_claim_ids,
    )


_UNCERTAINTY_OUTCOMES = {
    SolverOutcome.UNDETERMINED_INTERPRETATION,
    SolverOutcome.UNVERIFIABLE_CLAIM,
    SolverOutcome.NEED_EXPERT_JUDGMENT,
}


def _priority_routing(
    domain: DomainArtifact,
    intent: IntentArtifact | None,
    missing_claim_ids: list[str],
    rule_trace: list[RuleTraceRow],
    lookup_events: list[LookupEvent],
) -> UncertaintyRouting | None:
    """Pick the most specific U-code that applies to the current blocked state.

    Rule-level routings (U2/U4/U9) take precedence over claim-level routings
    because they describe statute-level openness rather than individual
    missing facts. Claim-level routings are iterated in ``missing_claim_ids``
    order (already sorted by ``_classify_outcome``), and the first non-``None``
    hit wins.
    """
    trace_by_rule = {row.rule_id: row for row in rule_trace}
    for rule in domain.rules:
        row = trace_by_rule.get(rule.rule_id)
        if row is None or row.status == RuleStatus.FIRES:
            continue
        hit = classify_rule_uncertainty(rule, row)
        if hit is not None:
            return hit

    domain_claims = {claim.claim_id: claim for claim in domain.claims}
    intent_claims = (
        {claim.claim_id: claim for claim in intent.claims} if intent is not None else {}
    )
    for claim_id in missing_claim_ids:
        domain_claim = domain_claims.get(claim_id)
        if domain_claim is None:
            continue
        hit = classify_claim_uncertainty(
            domain_claim,
            intent_claims.get(claim_id),
            lookup_events,
        )
        if hit is not None:
            return hit
    return None


def _classify_outcome(
    domain: DomainArtifact,
    resolved_claims: list[ResolvedClaim],
    solver_summary: dict[str, Any],
    rule_trace: list[RuleTraceRow],
    *,
    db_lookup_performed: bool,
    intent: IntentArtifact | None = None,
    lookup_events: list[LookupEvent] | None = None,
) -> tuple[SolverOutcome, list[str], list[str], str]:
    """Classify the current run into one of the administrative outcomes.

    In Wave 2 Stream B (ART-64) this function consults
    :mod:`uncertainty_routing` to emit first-class U1..U12 outcomes before
    falling back to the original NEED_DB_INFO / NEED_USER_INFO paths.
    """
    lookup_events = lookup_events or []

    if solver_summary["base_status"] == "error":
        return (
            SolverOutcome.DENY,
            [],
            [],
            "Z3 raised an exception, so the solver fell back to DENY.",
        )
    if solver_summary["base_status"] == "unsat":
        return (
            SolverOutcome.DENY,
            [],
            [],
            "The Boolean theory is inconsistent, so the solver fell back to DENY.",
        )

    allow_truth = solver_summary["outcome_values"][domain.allow_outcome_id]
    deny_truth = solver_summary["outcome_values"][domain.deny_outcome_id]
    if allow_truth is True and deny_truth is not True:
        trust_only_hit = has_trust_only_resolution(lookup_events)
        if trust_only_hit:
            return (
                SolverOutcome.UNVERIFIABLE_CLAIM,
                [],
                [],
                (
                    "The lowered Z3 theory entails ALLOW, but the supporting "
                    "facts came from a trust-only source (U7:TRUST_ONLY), so "
                    "the outcome is flagged as unverifiable."
                ),
            )
        return (
            SolverOutcome.ALLOW,
            [],
            [],
            "The lowered Z3 theory entails ALLOW.",
        )
    if deny_truth is True:
        return (
            SolverOutcome.DENY,
            [],
            [],
            "The lowered Z3 theory entails DENY.",
        )

    domain_claims = {claim.claim_id: claim for claim in domain.claims}
    open_allow_rules = [
        row for row in rule_trace if row.kind == RuleKind.ALLOW_IF_ALL and row.status == RuleStatus.NEEDS_INFO
    ]
    missing_claim_ids = sorted({claim_id for row in open_allow_rules for claim_id in row.unknown_claim_ids})
    missing_db_claim_ids = [
        claim_id
        for claim_id in missing_claim_ids
        if domain_claims[claim_id].source_type == ClaimSource.DB
    ]
    missing_user_claim_ids = [
        claim_id
        for claim_id in missing_claim_ids
        if domain_claims[claim_id].source_type == ClaimSource.USER
    ]

    routing = _priority_routing(
        domain,
        intent,
        missing_claim_ids,
        rule_trace,
        lookup_events,
    )
    if routing is not None and routing.outcome in _UNCERTAINTY_OUTCOMES:
        return (
            routing.outcome,
            missing_db_claim_ids,
            missing_user_claim_ids,
            f"[{routing.code}:{routing.reason_code.value}] {routing.description}",
        )

    if missing_db_claim_ids:
        message = (
            "The allow path still depends on DB-backed claims."
            if not db_lookup_performed
            else "DB-backed claims are still unresolved after the current lookup pass."
        )
        return (
            SolverOutcome.NEED_DB_INFO,
            missing_db_claim_ids,
            missing_user_claim_ids,
            message,
        )
    if missing_user_claim_ids:
        if routing is not None and routing.outcome == SolverOutcome.NEED_USER_INFO:
            return (
                SolverOutcome.NEED_USER_INFO,
                missing_db_claim_ids,
                missing_user_claim_ids,
                f"[{routing.code}:{routing.reason_code.value}] {routing.description}",
            )
        return (
            SolverOutcome.NEED_USER_INFO,
            missing_db_claim_ids,
            missing_user_claim_ids,
            "The remaining open allow path depends on user-supplied claims.",
        )

    return (
        SolverOutcome.DENY,
        [],
        [],
        "No allow rule is entailed and no useful missing information remains, so the solver defaults to DENY.",
    )


def _build_snapshot(
    stage: str,
    case_bundle: CaseBundle,
    resolved_claims: list[ResolvedClaim],
    *,
    db_lookup_performed: bool,
    lookup_events: list[LookupEvent] | None = None,
) -> tuple[SolveSnapshot, dict[str, Any]]:
    solver_summary = _run_z3(case_bundle.domain, _fact_map(resolved_claims))
    derived_claims = _apply_derived_claims(case_bundle.domain, resolved_claims, solver_summary)
    rule_trace = [
        _trace_rule(case_bundle.domain, rule, derived_claims) for rule in case_bundle.domain.rules
    ]
    outcome, missing_db_claim_ids, missing_user_claim_ids, note = _classify_outcome(
        case_bundle.domain,
        derived_claims,
        solver_summary,
        rule_trace,
        db_lookup_performed=db_lookup_performed,
        intent=case_bundle.intent,
        lookup_events=lookup_events or [],
    )
    snapshot = SolveSnapshot(
        stage=stage,
        outcome=outcome,
        resolved_claims=derived_claims,
        rule_trace=rule_trace,
        missing_db_claim_ids=missing_db_claim_ids,
        missing_user_claim_ids=missing_user_claim_ids,
        note=note,
    )
    return snapshot, solver_summary


def _merge_db_values(
    resolved_claims: list[ResolvedClaim],
    looked_up_values: dict[str, bool | None],
    lookup_events: list[LookupEvent] | None = None,
) -> list[ResolvedClaim]:
    rows = deepcopy(resolved_claims)
    trust_only_ids = trust_only_claim_ids(lookup_events or [])
    for row in rows:
        if row.claim_id not in looked_up_values:
            continue
        if row.value is None and looked_up_values[row.claim_id] is not None:
            row.value = looked_up_values[row.claim_id]
            if row.claim_id in trust_only_ids:
                row.resolved_from = "db_trust_only"
                row.reason = (
                    "Resolved from a trust-only mock DB source "
                    "(U7:TRUST_ONLY) - value is accepted unverified."
                )
                row.uncertainty_code = "U7"
            else:
                row.resolved_from = "db"
                row.reason = "Resolved from the local mock DB."
    return rows


def _domain_blockage(domain: DomainArtifact) -> tuple[str, BlockReasonCode] | None:
    """Classify obviously unusable extracted domains without guessing intent."""
    claim_count = len(domain.claims)
    rule_count = len(domain.rules)
    decision_rule_count = sum(
        1 for rule in domain.rules if rule.kind in {RuleKind.ALLOW_IF_ALL, RuleKind.DENY_IF_ALL}
    )
    if claim_count == 0 and rule_count == 0:
        return ("domain_extraction", BlockReasonCode.DOMAIN_EXTRACTION_EMPTY)
    if claim_count == 0 or rule_count == 0 or decision_rule_count == 0:
        return ("domain_extraction", BlockReasonCode.DOMAIN_EXTRACTION_SPARSE)
    return None


_OUTCOME_TO_REASON_CODE = {
    SolverOutcome.NEED_DB_INFO: BlockReasonCode.NEEDS_DB_INFO,
    SolverOutcome.NEED_USER_INFO: BlockReasonCode.NEEDS_USER_INFO,
    SolverOutcome.NEED_EXPERT_JUDGMENT: BlockReasonCode.EXPERT_JUDGMENT_REQUIRED,
}


def _final_blockage(
    domain: DomainArtifact,
    final_snapshot: SolveSnapshot,
    solver_summary: dict[str, Any],
    *,
    intent: IntentArtifact | None = None,
    lookup_events: list[LookupEvent] | None = None,
) -> tuple[str, BlockReasonCode] | None:
    """Return the neutral blockage classification for the finished solve."""
    if final_snapshot.outcome == SolverOutcome.ALLOW:
        return None
    domain_blockage = _domain_blockage(domain)
    if domain_blockage is not None:
        return domain_blockage
    if solver_summary["base_status"] in {"error", "unsat"}:
        return ("solve", BlockReasonCode.SOLVER_INCONSISTENT)

    all_missing_claim_ids = sorted(
        {
            claim_id
            for row in final_snapshot.rule_trace
            if row.kind == RuleKind.ALLOW_IF_ALL and row.status == RuleStatus.NEEDS_INFO
            for claim_id in row.unknown_claim_ids
        }
    )
    routing = _priority_routing(
        domain,
        intent,
        all_missing_claim_ids,
        final_snapshot.rule_trace,
        lookup_events or [],
    )
    if routing is not None and final_snapshot.outcome in (
        SolverOutcome.UNDETERMINED_INTERPRETATION,
        SolverOutcome.UNVERIFIABLE_CLAIM,
        SolverOutcome.NEED_EXPERT_JUDGMENT,
        SolverOutcome.NEED_USER_INFO,
    ):
        return ("solve", routing.reason_code)

    if final_snapshot.outcome == SolverOutcome.UNVERIFIABLE_CLAIM:
        # Trust-only ALLOW override path: no unresolved claim list available,
        # but the snapshot note already signals U7.
        return ("solve", BlockReasonCode.TRUST_ONLY)

    mapped = _OUTCOME_TO_REASON_CODE.get(final_snapshot.outcome)
    if mapped is not None:
        return ("solve", mapped)
    return ("solve", BlockReasonCode.NO_APPLICABLE_RULES)


def solve_case_bundle(case_bundle: CaseBundle) -> SolutionArtifact:
    """Solve one case bundle and record all intermediate trace steps."""
    if case_bundle.logic_level != case_bundle.domain.logic_level:
        raise ValueError("Case bundle logic level does not match the domain artifact.")
    if case_bundle.logic_level != case_bundle.intent.logic_level:
        raise ValueError("Case bundle logic level does not match the intent artifact.")
    ensure_executable_logic_level(case_bundle.logic_level)

    trace_events = [
        TraceEvent(
            stage="setup",
            message=(
                f"Starting solve in {case_bundle.logic_level.value} mode. "
                f"{case_bundle.domain.lowered_view_note}"
            ),
        )
    ]
    seeded_claims = _seed_claims(case_bundle)
    initial_snapshot, initial_solver_summary = _build_snapshot(
        "initial",
        case_bundle,
        seeded_claims,
        db_lookup_performed=False,
    )
    trace_events.append(
        TraceEvent(
            stage="initial",
            message=initial_snapshot.note,
        )
    )

    snapshots = [initial_snapshot]
    lookup_events = []
    final_snapshot = initial_snapshot
    final_solver_summary = initial_solver_summary

    if initial_snapshot.outcome == SolverOutcome.NEED_DB_INFO:
        looked_up_values, lookup_events = lookup_claims(
            case_bundle.mock_db.sources,
            initial_snapshot.missing_db_claim_ids,
            stage="db_lookup",
        )
        trace_events.append(
            TraceEvent(
                stage="db_lookup",
                message=(
                    "Queried the local mock DB for: "
                    + ", ".join(initial_snapshot.missing_db_claim_ids)
                ),
            )
        )
        merged_claims = _merge_db_values(
            initial_snapshot.resolved_claims,
            looked_up_values,
            lookup_events,
        )
        final_snapshot, final_solver_summary = _build_snapshot(
            "after_db_lookup",
            case_bundle,
            merged_claims,
            db_lookup_performed=True,
            lookup_events=lookup_events,
        )
        snapshots.append(final_snapshot)
        trace_events.append(
            TraceEvent(
                stage="after_db_lookup",
                message=final_snapshot.note,
            )
        )

    blockage = _final_blockage(
        case_bundle.domain,
        final_snapshot,
        final_solver_summary,
        intent=case_bundle.intent,
        lookup_events=lookup_events,
    )
    unresolved_claim_ids = sorted(
        set(final_snapshot.missing_db_claim_ids).union(final_snapshot.missing_user_claim_ids)
    )
    if blockage is not None:
        blocked_at_step, block_reason_code = blockage
        trace_events.append(
            TraceEvent(
                stage="blockage",
                message=(
                    f"Blocked at `{blocked_at_step}` with neutral reason code "
                    f"`{block_reason_code.value}`."
                ),
            )
        )
    else:
        blocked_at_step = None
        block_reason_code = None

    return SolutionArtifact(
        logic_level=case_bundle.logic_level,
        domain_title=case_bundle.domain.title,
        request_text=case_bundle.intent.request_text,
        lowered_view_note=case_bundle.domain.lowered_view_note,
        final_outcome=final_snapshot.outcome,
        intent_metadata=case_bundle.intent.run_metadata,
        domain_metadata=case_bundle.domain.run_metadata,
        blocked_at_step=blocked_at_step,
        block_reason_code=block_reason_code,
        extracted_claim_count=len(case_bundle.domain.claims),
        extracted_rule_count=len(case_bundle.domain.rules),
        unresolved_claim_ids=unresolved_claim_ids,
        intent_claims=case_bundle.intent.claims,
        domain_claims=case_bundle.domain.claims,
        domain_rules=case_bundle.domain.rules,
        trace_events=trace_events,
        lookup_events=lookup_events,
        snapshots=snapshots,
    )


class Z3Backend:
    """Thin adapter that wraps the module-level Z3 functions behind ``ReasonerBackend``.

    Satisfies the ``ReasonerBackend`` Protocol structurally; no explicit inheritance needed.
    """

    def solve_case_bundle(self, case_bundle: CaseBundle) -> SolutionArtifact:
        """Delegate to the module-level Z3 implementation."""
        return solve_case_bundle(case_bundle)
