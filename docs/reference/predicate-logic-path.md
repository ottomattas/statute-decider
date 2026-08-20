# Predicate-Logic Path — Decision Note

**Status:** Stub retained. No code changes in this wave.

**Decision (locked 2026-04-21):** Keep the predicate-logic stub in
`framework/logic_levels.py`. Do not remove it. Do not promote it to an active
execution path.

---

## Stub Location

The enforcement point is `framework/logic_levels.py:238–244`,
function `ensure_executable_logic_level`, which raises `ValueError` when any
`LogicLevel` other than `PROPOSITIONAL` is passed. Predicate and higher-order
rendering forms also exist in `LOGIC_LEVEL_SPECS` (lines 36–58) and in
`_claim_form` / `_outcome_form` (lines 61–74), but these only return the
predicate-form string; they do not execute it.

**Required follow-up actions (not executed in this wave):**

1. Add a `# TODO: predicate execution not implemented` comment at the
   `ensure_executable_logic_level` definition site (`framework/logic_levels.py:238`).
2. Change the raised exception from `ValueError` to `NotImplementedError` so
   callers can distinguish an intentional stub from an unexpected value error.
3. Add a `logging.warning(...)` call before raising so CLI users who pass
   `--logic-level predicate` receive a readable message rather than a raw traceback.

Scope: `framework/logic_levels.py` only; update any test catching `ValueError`
at this call site accordingly.

---

## Justification

- **Design intent:** `project_knowledge.mdc` — "Only propositional execution
  is active today; predicate and higher-order views may exist as rendered or
  lowered forms, but they are not separate executable engines."
- **ADR 0003:** Defers non-propositional execution until the current
  extraction, metadata, trace, and scenario-regeneration path is stable.
- **Supervisor input:** Tanel (2026-04-10, ~29:31) observed that predicate logic
  does not fix the expressivity problems on its own; the more pressing structural
  question is the solver back-end semantics (ASP / abduction), not upgrading the
  logic level.

---

## Re-evaluation Triggers

The decision to keep the stub should be revisited if either of the following
occurs:

1. A concrete use case arises that cannot be encoded in propositional atoms
   without exponential blowup (e.g., a statute with universal quantification
   over unbounded populations).
2. The Wave 2 benchmark (Track E, ADR 0004) shows that the chosen back-end
   (clingo / PySAT) natively supports FOL and that the migration cost is
   negligible.

Until one of these triggers fires, the predicate path remains a stub.
