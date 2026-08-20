# Research Question

This document states the current primary research question (RQ), its
sub-questions, supporting property, scope boundaries, and success criteria.
It is the authoritative single-page anchor for the thesis narrative.

Last revised: 2026-04-21. Locked decisions in
`.cursor/plans/post-17apr-research-push_a0104936.plan.md` §7.

---

## Primary Research Question (locked)

> **How can a neurosymbolic system elicit the *minimal* information needed for a
> legally sound decision, and differentiate the kinds of uncertainty it
> encounters along the way?**

The two italicized components are jointly necessary:

- **Minimal-information elicitation** — the system must not ask for information
  it does not need. The halting condition (`NEED_DB_INFO` / `NEED_USER_INFO`)
  must be source-typed so that the orchestration layer can route each request
  to the appropriate actor without re-invoking the LLM.
- **Differentiated uncertainty taxonomy** — when the system cannot reach a
  determinate verdict, it must characterize *why* using a structured taxonomy
  (U1–U12, §1 below) rather than collapsing all blockages into a single denial
  or unknown state.

The combination anchors both the empirical novelty pitch (no surveyed system
does source-typed minimal elicitation) and the taxonomy contribution that feeds
the paper §Methodology.

---

## Sub-questions

### SQ1 — Uncertainty taxonomy

Can the twelve uncertainty kinds (U1–U12) be reliably distinguished at
extraction time and propagated end-to-end through the solver trace?

| Code | Name | Brief definition |
|---|---|---|
| U1 | Statute under-specification | Concept not defined concretely enough in law (e.g., "journalist") |
| U2 | Interpretation ambiguity | Multiple admissible statutory readings; cannot pick without case law |
| U3 | Missing register / ground-truth source | No database exists to answer the claim |
| U4 | Process indeterminacy | Real-world procedure not automated or formalized |
| U5 | Inter-variable context dependence | Variable values are extractable but their relations are case-specific |
| U6 | Subjective / party-biased facts | Applicant can self-declare strategically |
| U7 | Trust-based identity / verification | Real process uses trust signals rather than registers |
| U8 | Missing user information | User's utterance does not cover a needed variable |
| U9 | Epistemic uncertainty about ground truth | Even the modeler cannot determine the correct answer in hard legal cases |
| U10 | Multi-level alignment uncertainty | Compounded ambiguity of statute and NL utterance when aligned |
| U11 | Glossary / lexicon confidence | Uncertainty in the hand-built domain vocabulary itself |
| U12 | Model-drift / replicability | LLM / ML extraction outputs are not stable across runs or model versions |

Engineering target: extend `BlockReasonCode` / `SolverOutcome` in
`framework/schemas.py` with codes for each U-category (Track A).

### SQ2 — Reasoner semantics

What is the minimal symbolic backend whose semantics match the target
uncertainty space, given the working assumption of monotonicity (Priit,
2026-04-14)? Stance: propositional-first per ADR 0003; `clingo` (ASP) as the
primary re-selection candidate per ADR 0004. Non-monotonic reasoning is
deferred (see scope boundaries).

### SQ3 — Model-agnostic extraction vs. trust-at-solver

Should trust placement (U7) be decided at extraction time by the LLM, or
deferred to the solver? Current architecture: the LLM tags each claim with
`source_type` (`db`, `user`, `expert`, `derived`, `statute_open`) at Step 1,
so the solver requires no separate trust model. Decoupling principle (Otto,
2026-04-14, ~51:46); to be validated against the scenario suite.

---

## Supporting Property (not the headline RQ)

**Trustworthiness** — the property that the system's outputs are verifiable,
auditable, and traceable to statutory provenance. Trustworthiness is a
consequence of the architecture (symbolic final authority + explicit trace +
opinion-free halting) rather than the primary scientific question. It should
appear in §Introduction and §Discussion but not as the lead RQ.

---

## Scope Boundaries

The following are explicitly out of scope for the current phase:

| Exclusion | Justification |
|---|---|
| Full non-monotonic reasoning (defeasible logic, well-founded semantics) | Priit's 2026-04-14 decision: assume monotonic first; a non-monotonic extension would require a substantially different logic treatment (~25:28–26:35). Locked in plan §7. |
| Court-decision modelling | The pipeline targets administrative eligibility and consent decisions, not adversarial judicial proceedings. No citation base for court-decision modelling exists in `paper/bibliography.bib`. |
| Building a machine-readable law model from scratch | The pipeline extracts from existing statutory text via LLM; it does not author a new formal legal ontology. |
| End-to-end evaluation over a production statutory corpus | The current scenario suite (~50 cases) is a research-grade harness; deployment claims are explicitly disclaimed. |
| LLM-as-final-decision-maker | Architectural invariant per `project_knowledge.mdc`; the solver retains final authority unconditionally. |

---

## Success Criteria

1. **Scenario suite pass rate:** ≥ 50 validated scenarios (5 domains × ~10 cases)
   with `expected_vs_actual` match across the default backend (Track B).
2. **Differentiated uncertainty codes:** at least one scenario per U-code
   (U1–U12) surfaces a distinct `BlockReasonCode` in the trace (Track A).
3. **Reasoner-benchmark parity:** clingo, PySAT, Horn, and Z3-reference agree
   on every monotonic-fragment scenario; discrepancies recorded with analysis.
4. **Source-typed halting:** zero `NEED_DB_INFO` events routed to the user
   channel and vice versa on the scenario suite.

---

## References

Plan: `.cursor/plans/post-17apr-research-push_a0104936.plan.md` §1, §7. ADR
0003: `docs/adr/0003-poc3-proposition-first-staging.md`. ADR 0004:
`docs/adr/0004-reasoner-reselection.md` (pending). Rules:
`.cursor/rules/project_knowledge.mdc`. Paper: `paper/main.tex` §3.4.
