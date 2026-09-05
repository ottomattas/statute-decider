# ADR 0006: Stage 2 draws facts for the antecedents of every rule

## Status

Accepted — 2026-09-06 (operator Ruling I)

## Context

`solvers/z3_backend.py` decides in two stages: the applicant's claims seed the
valuation (stage 1), then register facts are merged (stage 2). Until this ADR
stage 2 merged facts *only for the register-evidence terms still open on the
allow path* — an on-demand lookup that asked the registers no more than the
allow rules needed. Two consequences followed:

- a register-recorded **deny** ground was never read unless the applicant
  mentioned it: with `claims = {asked_nicely}` and `facts = {is_registered=true,
  is_banned=true}` the solver answered ALLOW;
- when the allow path was open only on a user-evidence term the solver stopped
  at NEED_USER_INFO without consulting a register at all.

The statutes do not condition refusal on the applicant raising the ground.
Building Code § 44: "The competent authority refuses to issue a building permit
if: 1) the envisaged construction work does not conform to the detailed spatial
plan, design specifications, …". Civil Service Act § 15 2): a person "who has
been punished for an intentionally committed criminal offence against the
state, regardless of the deletion of the information concerning punishment" may
not be employed in service. A deny ground the register records must fire the
deny rule on its own.

## Decision

Stage 2 draws a warranted value for **every catalog term any rule tests**
(allow, deny and rewrite rules alike) that the claims left open. The two
invariants of the staged semantics stand:

1. claims seed first and are never overridden by a fact, even an authoritative
   one that contradicts them (statements against interest keep firing deny
   rules; the oracle depends on this);
2. the warrant machinery is unchanged — a trust-only fact merges at claim
   strength, an entailed ALLOW that rests on unwarranted register evidence is
   UNVERIFIABLE_CLAIM with the same flagged set and reasons, a term whose
   register is unavailable or in conflict contributes no value.

Classification therefore always runs on the merged valuation; the stage-1
early exits (DENY on claims alone, NEED_USER_INFO before lookup) are gone as
separate code paths, though their outcomes are unchanged because a fact cannot
override a claim and a deny that fires on claims still fires with more values
present. `_rule_antecedents()` names the set stage 2 asks about.

## Consequences

- `experiments/20260906-solver-validation` re-run: 54/54, macro F1 1.000; no
  scenario changed its scored outcome, state or missing-term set. 20 rows carry
  a fuller `valuation` (deny-rule antecedents and blocked-allow-rule
  antecedents drawn from the registers appear where they used to be absent),
  and one fired-rule set changes:
  `building_permit_grant/deny_register_only_plan_nonconformity` now fires
  `deny_plan_violation` on the register-recorded `plan_violation=true` (before
  this ADR it was a default DENY with no rule fired — the very case
  `gold-review-2026-09-05.md` flagged as "a solver property worth the
  operator's attention"). Same outcome, now for the statutory reason.
- `tests/test_z3_semantics.py` gains three tests: the unmentioned deny ground
  fires; it fires even when the allow path is open only on a user term; a claim
  still beats a contradicting fact.
- The `solver-inputs-full-procedure` decide prompt, which states the solver's
  procedure to an LLM so that the comparison is executor-only, now states stage
  2 as "facts for the antecedents of every rule" (see ADR 0007 for the other
  prompt changes made the same day).
- `docs/reference/gold-review-2026-09-05.md` describes stage 2 per scenario in
  the old wording ("stage 2 draws the five § 42 (1) terms"); the outcomes it
  verifies are unchanged and the sheet is left as the record of that review.
