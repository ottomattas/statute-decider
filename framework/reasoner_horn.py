"""Pure-Python Horn forward-chaining backend.

Implements a naive fixpoint evaluator over the monotonic rule fragment
(`ALLOW_IF_ALL`, `DENY_IF_ALL`, `SET_FALSE_IF_ALL`). Zero external
dependencies; it doubles as the pedagogical oracle backend in the
Wave 2 benchmark (see ``docs/adr/0004-reasoner-reselection.md``).

This module also hosts the engine-agnostic plumbing
(``solve_case_bundle_with_engine``, snapshot/classification helpers)
reused by ``reasoner_clingo.py`` and ``reasoner_pysat.py`` so that every
backend produces a schema-identical ``SolutionArtifact`` on the fragment.

Abduction and uncertainty-code routing are Wave 3 extensions (TODO).
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

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
    ResolvedClaim,
    RuleKind,
    RuleStatus,
    RuleTraceRow,
    SolveSnapshot,
    SolverOutcome,
    SolutionArtifact,
    TraceEvent,
)


# ---------------------------------------------------------------------------
# Horn fixpoint kernel
# ---------------------------------------------------------------------------


def _run_horn(domain: DomainArtifact, facts: dict[str, bool | None]) -> dict[str, Any]:
    """Naive forward-chaining fixpoint on the monotonic fragment.

    Iterates until no new claim/outcome value is derived. Rules fire only when
    every premise is known True. Detects inconsistency when a derivation would
    contradict a prior assignment (reported as ``base_status == "unsat"``).
    """
    values: dict[str, bool | None] = {}
    claim_ids = {claim.claim_id for claim in domain.claims}
    outcome_ids = {outcome.outcome_id for outcome in domain.outcomes}
    for claim in domain.claims:
        values[claim.claim_id] = None
    for outcome in domain.outcomes:
        values[outcome.outcome_id] = None
    for claim_id, value in facts.items():
        if claim_id in values and value is not None:
            values[claim_id] = value

    inconsistent = False
    changed = True
    while changed and not inconsistent:
        changed = False
        for rule in domain.rules:
            premise_values = [values.get(pid) for pid in rule.when_claim_ids]
            if not all(v is True for v in premise_values):
                continue
            if rule.kind == RuleKind.SET_FALSE_IF_ALL:
                target = rule.target_claim_id
                prior = values.get(target)
                if prior is True:
                    inconsistent = True
                    break
                if prior is not False:
                    values[target] = False
                    changed = True
            else:
                target = rule.target_outcome_id
                prior = values.get(target)
                if prior is False:
                    inconsistent = True
                    break
                if prior is not True:
                    values[target] = True
                    changed = True

    if inconsistent:
        return {
            "engine": "horn",
            "base_status": "unsat",
            "claim_values": {cid: None for cid in claim_ids},
            "outcome_values": {oid: None for oid in outcome_ids},
        }

    claim_values = {cid: values[cid] for cid in claim_ids}
    outcome_values = {oid: values[oid] for oid in outcome_ids}
    return {
        "engine": "horn",
        "base_status": "sat",
        "claim_values": claim_values,
        "outcome_values": outcome_values,
    }


# ---------------------------------------------------------------------------
# Engine-agnostic plumbing (shared by clingo / pysat / horn backends)
# ---------------------------------------------------------------------------


RunEngine = Callable[[DomainArtifact, dict[str, bool | None]], dict[str, Any]]


_ENGINE_LABEL = {
    "horn": "Horn forward-chaining",
    "clingo": "clingo answer-set",
    "pysat": "PySAT",
}


def _seed_claims(case_bundle: CaseBundle) -> list[ResolvedClaim]:
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
    engine: str,
) -> list[ResolvedClaim]:
    rows = deepcopy(resolved_claims)
    by_id = {row.claim_id: row for row in rows}
    if solver_summary["base_status"] != "sat":
        return rows
    label = _ENGINE_LABEL.get(engine, engine)
    for claim_id, entailed in solver_summary["claim_values"].items():
        row = by_id[claim_id]
        if entailed is None:
            continue
        if row.value is None:
            row.value = entailed
            row.resolved_from = "reasoner"
            row.reason = f"Entailed by the {label} core."
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


def _classify_outcome(
    domain: DomainArtifact,
    resolved_claims: list[ResolvedClaim],
    solver_summary: dict[str, Any],
    rule_trace: list[RuleTraceRow],
    *,
    db_lookup_performed: bool,
    engine: str,
) -> tuple[SolverOutcome, list[str], list[str], str]:
    label = _ENGINE_LABEL.get(engine, engine)
    if solver_summary["base_status"] == "error":
        return (
            SolverOutcome.DENY,
            [],
            [],
            f"The {label} backend raised an exception, so the solver fell back to DENY.",
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
        return (
            SolverOutcome.ALLOW,
            [],
            [],
            f"The {label} theory entails ALLOW.",
        )
    if deny_truth is True:
        return (
            SolverOutcome.DENY,
            [],
            [],
            f"The {label} theory entails DENY.",
        )

    domain_claims = {claim.claim_id: claim for claim in domain.claims}
    open_allow_rules = [
        row for row in rule_trace if row.kind == RuleKind.ALLOW_IF_ALL and row.status == RuleStatus.NEEDS_INFO
    ]
    missing_claim_ids = sorted({claim_id for row in open_allow_rules for claim_id in row.unknown_claim_ids})
    missing_db_claim_ids = [
        claim_id for claim_id in missing_claim_ids if domain_claims[claim_id].source_type == ClaimSource.DB
    ]
    missing_user_claim_ids = [
        claim_id for claim_id in missing_claim_ids if domain_claims[claim_id].source_type == ClaimSource.USER
    ]

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
    engine: str,
    run_engine: RunEngine,
) -> tuple[SolveSnapshot, dict[str, Any]]:
    solver_summary = run_engine(case_bundle.domain, _fact_map(resolved_claims))
    derived_claims = _apply_derived_claims(case_bundle.domain, resolved_claims, solver_summary, engine)
    rule_trace = [
        _trace_rule(case_bundle.domain, rule, derived_claims) for rule in case_bundle.domain.rules
    ]
    outcome, missing_db_claim_ids, missing_user_claim_ids, note = _classify_outcome(
        case_bundle.domain,
        derived_claims,
        solver_summary,
        rule_trace,
        db_lookup_performed=db_lookup_performed,
        engine=engine,
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
) -> list[ResolvedClaim]:
    rows = deepcopy(resolved_claims)
    for row in rows:
        if row.claim_id not in looked_up_values:
            continue
        if row.value is None and looked_up_values[row.claim_id] is not None:
            row.value = looked_up_values[row.claim_id]
            row.resolved_from = "db"
            row.reason = "Resolved from the local mock DB."
    return rows


def _domain_blockage(domain: DomainArtifact) -> tuple[str, BlockReasonCode] | None:
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


def _final_blockage(
    domain: DomainArtifact,
    final_snapshot: SolveSnapshot,
    solver_summary: dict[str, Any],
) -> tuple[str, BlockReasonCode] | None:
    if final_snapshot.outcome == SolverOutcome.ALLOW:
        return None
    domain_blockage = _domain_blockage(domain)
    if domain_blockage is not None:
        return domain_blockage
    if solver_summary["base_status"] in {"error", "unsat"}:
        return ("solve", BlockReasonCode.SOLVER_INCONSISTENT)
    if final_snapshot.outcome == SolverOutcome.NEED_DB_INFO:
        return ("solve", BlockReasonCode.NEEDS_DB_INFO)
    if final_snapshot.outcome == SolverOutcome.NEED_USER_INFO:
        return ("solve", BlockReasonCode.NEEDS_USER_INFO)
    return ("solve", BlockReasonCode.NO_APPLICABLE_RULES)


def solve_case_bundle_with_engine(
    case_bundle: CaseBundle,
    *,
    engine: str,
    run_engine: RunEngine,
) -> SolutionArtifact:
    """Engine-agnostic ``solve_case_bundle`` used by every non-Z3 backend.

    Reproduces the stage sequence (setup -> initial solve -> optional DB
    lookup -> final blockage classification) from ``reasoner_z3`` so the
    returned ``SolutionArtifact`` is schema-identical across backends.
    """
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
        engine=engine,
        run_engine=run_engine,
    )
    trace_events.append(TraceEvent(stage="initial", message=initial_snapshot.note))

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
        merged_claims = _merge_db_values(initial_snapshot.resolved_claims, looked_up_values)
        final_snapshot, final_solver_summary = _build_snapshot(
            "after_db_lookup",
            case_bundle,
            merged_claims,
            db_lookup_performed=True,
            engine=engine,
            run_engine=run_engine,
        )
        snapshots.append(final_snapshot)
        trace_events.append(TraceEvent(stage="after_db_lookup", message=final_snapshot.note))

    blockage = _final_blockage(case_bundle.domain, final_snapshot, final_solver_summary)
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


# ---------------------------------------------------------------------------
# HornBackend public class
# ---------------------------------------------------------------------------


class HornBackend:
    """Hand-rolled Horn forward-chaining backend.

    Always available (pure Python, zero external deps); retained as the
    pedagogical oracle in the ADR 0004 benchmark. Satisfies
    ``ReasonerBackend`` structurally — no explicit inheritance needed.
    """

    def solve_case_bundle(self, case_bundle: CaseBundle) -> SolutionArtifact:
        return solve_case_bundle_with_engine(
            case_bundle,
            engine="horn",
            run_engine=_run_horn,
        )
