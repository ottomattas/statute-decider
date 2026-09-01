"""Z3 backend: staged, warrant-aware boolean inference.

Semantics (validated against the 47-scenario oracle suite; v1-equivalent):

1. Stage 1 — claims. Claims are defeasible premises: what the applicant
   asserts seeds the valuation for any catalog term (statements against
   interest legitimately fire deny rules; the oracle outcomes depend on this).
2. If the outcome is still open on register-evidence terms, stage 2 merges
   facts *for the missing terms only* (registers are consulted for
   decision-relevant terms, mirroring an on-demand lookup). Facts never
   override an explicit assertion; they fill what is missing.
3. The warrant machinery lives on the register path: trust-only facts merge
   at claim-strength — if the final ALLOW rests on any of them, the state is
   UNVERIFIABLE_CLAIM and the *whole allow-path register evidence* is flagged
   for verification: every register-evidence antecedent of an allow rule,
   except terms definitively excluded by an authoritative false value.
   Trust-only-valued terms carry reason ``unwarranted_only``; the rest of the
   flagged evidence carries ``no_value`` (to be re-verified).
4. Remaining missing register terms classify per term: ``no_register`` when
   the covering register is unavailable, ``conflict`` when available registers
   disagree, else ``no_value``. Any ``no_register`` makes the state
   UNVERIFIABLE_CLAIM; else NEED_REGISTER_INFO / NEED_USER_INFO; with nothing
   decision-relevant missing, the default is DENY.

An inconsistent boolean theory (unsat) falls back to DENY with a note.
"""

from __future__ import annotations

import threading

from z3 import And, Bool, Implies, Not, Solver, sat

from statute_decider.core import (
    ClaimSet,
    Evidence,
    FactSet,
    FiredRule,
    MissingReason,
    MissingTerm,
    OutcomeState,
    PremiseOutcome,
    Provenance,
    RuleKind,
    RuleSet,
    TermCatalog,
    Warrant,
    to_scored,
)
from statute_decider.solvers.base import register_solver

try:  # pragma: no cover - version lookup only
    from importlib.metadata import version as _pkg_version

    _Z3_VERSION = _pkg_version("z3-solver")
except Exception:  # noqa: BLE001  # pragma: no cover
    _Z3_VERSION = "unknown"


def _symbols(catalog: TermCatalog, rules: RuleSet) -> set[str]:
    ids = set(catalog.term_ids())
    ids.update(out.outcome_id for out in rules.outcomes)
    ids.add(rules.allow_outcome_id)
    ids.add(rules.deny_outcome_id)
    for rule in rules.rules:
        ids.update(rule.when_term_ids)
        if rule.target_outcome_id:
            ids.add(rule.target_outcome_id)
        if rule.target_term_id:
            ids.add(rule.target_term_id)
    return ids


class _Theory:
    """One z3 theory over the rule set; entailment by refutation."""

    def __init__(self, catalog: TermCatalog, rules: RuleSet) -> None:
        self.catalog = catalog
        self.rules = rules
        self.vars = {sid: Bool(f"sd_{sid}") for sid in sorted(_symbols(catalog, rules))}

    def _base(self, valuation: dict[str, bool]) -> Solver:
        solver = Solver()
        for rule in self.rules.rules:
            antecedents = [self.vars[tid] for tid in rule.when_term_ids]
            lhs = And(antecedents) if len(antecedents) > 1 else antecedents[0]
            if rule.rule_kind == RuleKind.SET_FALSE_IF_ALL:
                solver.add(Implies(lhs, Not(self.vars[rule.target_term_id])))
            else:
                solver.add(Implies(lhs, self.vars[rule.target_outcome_id]))
        for sid, value in valuation.items():
            if sid in self.vars:
                solver.add(self.vars[sid] if value else Not(self.vars[sid]))
        return solver

    def consistent(self, valuation: dict[str, bool]) -> bool:
        return self._base(valuation).check() == sat

    def entailed(self, valuation: dict[str, bool], symbol: str) -> bool | None:
        neg = self._base(valuation)
        neg.add(Not(self.vars[symbol]))
        if neg.check() != sat:
            return True
        pos = self._base(valuation)
        pos.add(self.vars[symbol])
        if pos.check() != sat:
            return False
        return None


def _derived_valuation(theory: _Theory, valuation: dict[str, bool]) -> dict[str, bool]:
    """Extend the valuation with entailed term values (rewrite-rule chains)."""
    derived = dict(valuation)
    for term_id in theory.catalog.term_ids():
        if term_id in derived:
            continue
        value = theory.entailed(valuation, term_id)
        if value is not None:
            derived[term_id] = value
    return derived


def _open_allow_missing(theory: _Theory, derived: dict[str, bool]) -> list[str]:
    """Unknown antecedents of allow rules that no false antecedent blocks."""
    missing: set[str] = set()
    for rule in theory.rules.rules:
        if rule.rule_kind != RuleKind.ALLOW_IF_ALL:
            continue
        values = [derived.get(tid) for tid in rule.when_term_ids]
        if any(v is False for v in values):
            continue  # blocked
        missing.update(
            tid for tid, v in zip(rule.when_term_ids, values) if v is None
        )
    return sorted(missing)


def _fired_rules(theory: _Theory, derived: dict[str, bool]) -> list[FiredRule]:
    fired: list[FiredRule] = []
    for rule in theory.rules.rules:
        if all(derived.get(tid) is True for tid in rule.when_term_ids):
            effect = rule.target_outcome_id or f"not {rule.target_term_id}"
            fired.append(FiredRule(premise_id=rule.premise_id, effect=effect))
    return fired


# The z3 Python bindings share one native context; concurrent solve calls from
# the parallel runner's worker threads crash the interpreter (silent SIGSEGV).
# Solves are millisecond-scale next to the LLM calls, so serializing is free.
_Z3_LOCK = threading.Lock()


@register_solver("z3")
class Z3Solver:
    name = "z3"
    version = _Z3_VERSION

    def _provenance(self, note: str = "") -> Provenance:
        return Provenance(
            node="premise_outcome",
            method="solver",
            provider="z3",
            model=f"z3-solver {self.version}",
            notes=note,
        )

    def solve(
        self,
        catalog: TermCatalog,
        rules: RuleSet,
        claims: ClaimSet,
        facts: FactSet,
    ) -> PremiseOutcome:
        with _Z3_LOCK:
            return self._solve_impl(catalog, rules, claims, facts)

    def _solve_impl(
        self,
        catalog: TermCatalog,
        rules: RuleSet,
        claims: ClaimSet,
        facts: FactSet,
    ) -> PremiseOutcome:
        theory = _Theory(catalog, rules)
        terms = catalog.by_id()

        def outcome(
            state: OutcomeState,
            derived: dict[str, bool],
            missing: list[MissingTerm],
            note: str,
        ) -> PremiseOutcome:
            return PremiseOutcome(
                scenario_id=claims.scenario_id or facts.scenario_id,
                state=state,
                scored_as=to_scored(state),
                missing_terms=missing,
                fired_rules=_fired_rules(theory, derived),
                valuation={k: v for k, v in sorted(derived.items()) if k in terms},
                note=note,
                provenance=self._provenance(note),
            )

        # Stage 1: claims seed the valuation for any catalog term (defeasible
        # premises; facts only ever fill what remains missing).
        valuation: dict[str, bool] = {}
        for claim in claims.claims:
            if claim.term_id in terms:
                valuation[claim.term_id] = claim.value

        if not theory.consistent(valuation):
            derived = dict(valuation)
            return outcome(
                OutcomeState.DENY, derived, [], "Boolean theory inconsistent; fallback DENY."
            )

        def classify(
            valuation: dict[str, bool],
            *,
            after_lookup: bool,
            trust_only_used: set[str],
            unavailable_terms: set[str],
            conflict_terms: set[str],
        ) -> PremiseOutcome | list[str]:
            """Return a final PremiseOutcome, or the missing register terms to look up."""
            derived = _derived_valuation(theory, valuation)
            allow = theory.entailed(valuation, rules.allow_outcome_id)
            deny = theory.entailed(valuation, rules.deny_outcome_id)
            if allow is True and deny is not True:
                # Warrant principle: an entailed ALLOW is only final when every
                # register-evidence antecedent on the allow path has warranted
                # support. Authoritative facts warrant; a trust-only fact taints
                # the entire allow path (verify everything before granting); a
                # claim on a term some available register covers but is silent
                # about is unverified support for that term; a claim on a term
                # no present register covers has nothing to be checked against
                # and stays decision-grade. Holds identically for scripted and
                # extracted claims.
                allow_register_antecedents = {
                    tid
                    for rule in rules.rules
                    if rule.rule_kind == RuleKind.ALLOW_IF_ALL
                    for tid in rule.when_term_ids
                    if tid in terms and terms[tid].evidence == Evidence.REGISTER
                }
                authoritative_terms = {
                    fact.term_id
                    for fact in facts.facts
                    if fact.warrant == Warrant.AUTHORITATIVE
                }
                authoritative_false = {
                    fact.term_id
                    for fact in facts.facts
                    if fact.warrant == Warrant.AUTHORITATIVE and fact.value is False
                }
                trust_terms = {
                    fact.term_id
                    for fact in facts.facts
                    if fact.warrant == Warrant.TRUST_ONLY
                } - authoritative_terms
                covered = set(facts.covered_terms)
                unavailable = set(facts.unavailable_terms)

                def reason_for(tid: str) -> MissingReason:
                    if tid in trust_terms:
                        return MissingReason.UNWARRANTED_ONLY
                    if tid in unavailable:
                        return MissingReason.NO_REGISTER
                    return MissingReason.NO_VALUE

                trust_taint = allow_register_antecedents & trust_terms
                unavailable_taint = (
                    allow_register_antecedents & unavailable
                ) - authoritative_terms
                claim_terms = {c.term_id for c in claims.claims if c.term_id in terms}
                claim_taint = {
                    tid
                    for tid in allow_register_antecedents & covered & claim_terms
                    if tid not in authoritative_terms
                    and tid not in trust_terms
                    and tid not in unavailable
                }
                if trust_taint:
                    flagged = sorted(allow_register_antecedents - authoritative_false)
                elif unavailable_taint or claim_taint:
                    flagged = sorted(unavailable_taint | claim_taint)
                else:
                    flagged = []
                if flagged:
                    missing = [
                        MissingTerm(term_id=tid, reason=reason_for(tid)) for tid in flagged
                    ]
                    return outcome(
                        OutcomeState.UNVERIFIABLE_CLAIM,
                        derived,
                        missing,
                        "ALLOW is entailed, but rests on unwarranted support "
                        "(claims or trust-only values) for register-evidence "
                        "terms; flagged for verification (warrant principle).",
                    )
                return outcome(OutcomeState.ALLOW, derived, [], "ALLOW entailed.")
            if deny is True:
                return outcome(OutcomeState.DENY, derived, [], "DENY entailed.")

            missing_ids = _open_allow_missing(theory, derived)
            missing_register = [
                tid for tid in missing_ids if terms[tid].evidence == Evidence.REGISTER
            ]
            missing_user = [tid for tid in missing_ids if terms[tid].evidence == Evidence.USER]

            if missing_register and not after_lookup:
                return missing_register  # stage 2 will consult the registers

            if missing_register:
                items: list[MissingTerm] = []
                unverifiable = False
                for tid in missing_register:
                    if tid in unavailable_terms:
                        items.append(
                            MissingTerm(term_id=tid, reason=MissingReason.NO_REGISTER)
                        )
                        unverifiable = True
                    elif tid in conflict_terms:
                        items.append(MissingTerm(term_id=tid, reason=MissingReason.CONFLICT))
                    else:
                        items.append(MissingTerm(term_id=tid, reason=MissingReason.NO_VALUE))
                items.extend(
                    MissingTerm(term_id=tid, reason=MissingReason.NO_VALUE)
                    for tid in missing_user
                )
                state = (
                    OutcomeState.UNVERIFIABLE_CLAIM
                    if unverifiable
                    else OutcomeState.NEED_REGISTER_INFO
                )
                note = (
                    "Decision-relevant register terms have no warranted value"
                    + (" and the covering register is unavailable." if unverifiable else ".")
                )
                return outcome(state, derived, items, note)

            if missing_user:
                items = [
                    MissingTerm(term_id=tid, reason=MissingReason.NO_VALUE)
                    for tid in missing_user
                ]
                return outcome(
                    OutcomeState.NEED_USER_INFO,
                    derived,
                    items,
                    "The open allow path depends on user-supplied terms.",
                )

            return outcome(
                OutcomeState.DENY,
                derived,
                [],
                "No allow rule is entailed and nothing decision-relevant is missing; "
                "default DENY.",
            )

        result = classify(
            valuation,
            after_lookup=False,
            trust_only_used=set(),
            unavailable_terms=set(),
            conflict_terms=set(),
        )
        if isinstance(result, PremiseOutcome):
            return result

        # Stage 2: consult facts for the missing register-evidence terms only.
        requested = result
        fact_by_term = facts.by_term()
        unavailable_terms = set(facts.unavailable_terms)
        conflict_terms = set(facts.conflicts)
        trust_only_used: set[str] = set()
        merged = dict(valuation)
        for tid in requested:
            fact = fact_by_term.get(tid)
            if fact is None or tid in unavailable_terms or tid in conflict_terms:
                continue
            merged[tid] = fact.value
            if fact.warrant == Warrant.TRUST_ONLY:
                trust_only_used.add(tid)

        if not theory.consistent(merged):
            return outcome(
                OutcomeState.DENY,
                dict(merged),
                [],
                "Boolean theory inconsistent after register lookup; fallback DENY.",
            )

        final = classify(
            merged,
            after_lookup=True,
            trust_only_used=trust_only_used,
            unavailable_terms=unavailable_terms,
            conflict_terms=conflict_terms,
        )
        assert isinstance(final, PremiseOutcome)
        return final
