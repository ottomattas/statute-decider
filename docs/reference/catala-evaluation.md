# Catala Evaluation

**Status:** Pending — Wave 2 spike (ART-70).

This document is a placeholder for the one-afternoon Catala evaluation spike
requested at the 2026-04-14 supervision session (~31:36–33:36). It records the
question, decision criteria, and risks so the spike has a clear scope when it
runs.

---

## Question

Can `Catala` \citep{merigoux2021catala} host or embed the current `framework`
propositional layer and rule syntax without forcing domain lock-in or
compromising the minimal-prop-engine goal?

Specifically: would adopting Catala as an optional compilation target or
embedded component reduce authoring cost while preserving the pipeline's
propositional runtime, source-typed halting, and auditable trace properties?

---

## Decision Criteria

| Criterion | Threshold for adoption | Notes |
|---|---|---|
| Expressivity | Can encode `allow_if_all`, `deny_if_all`, `set_false_if_all` rules without wrapping in higher-order constructs | Core rule kinds must map directly |
| Runtime availability | Catala runtime (OCaml or Z3 back-end) installable in the `framework/venv` Python environment, or callable as a subprocess | No hard dependency on a separate VM |
| Estonian-law fit | Literate Catala source can be written for at least one existing use-case statute without structural distortion | Test against one existing `framework/examples/` domain |
| Interop with Pydantic schemas | Catala output can be consumed by or converted to `DomainArtifact` / `CaseBundle` without a full rewrite | Conversion cost must be bounded |
| Migration cost | Spike estimate ≤ 1 person-week to replace one domain end-to-end | If higher, defer to a later wave |

---

## Risks

- **Domain lock-in** (Priit, 2026-04-14, ~32:55): Catala's literate style
  couples code tightly to one statute's paragraph structure. Swapping the
  domain may require rewriting the Catala source rather than swapping a JSON
  use-case file.
- **DSL runtime** (Otto, 2026-04-14, ~29:06): the OCaml runtime and the Catala
  compiler are not Python-native. Adding them as pipeline dependencies increases
  operational complexity and may break the single-venv constraint.
- **Divergence from minimal-prop-engine goal** (Otto, 2026-04-14, ~33:28):
  Catala compiles to OCaml or Z3 — both are substantially heavier than a
  hand-rolled propositional engine or a PySAT / clingo back-end. Adopting
  Catala could undermine the decidability and trace-simplicity argument.

---

## Output Form

Fill in the blanks after the spike runs:

- **Verdict:** [ ] Keep (adopt as optional component) / [ ] Reject / [ ] Defer
- **Rationale:** _______
- **Migration estimate:** _______
- **Impact on ADR 0004 (reasoner re-selection):** _______
- **Spike completed:** _______
