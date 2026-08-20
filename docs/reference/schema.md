# Schema Reference

## Implementation layout

The current implementation lives directly under `framework/` as a path-executed CLI:

- `framework/01_extract_intent.py`
- `framework/02_extract_domain.py`
- `framework/03_solve_case.py`
- `framework/04_print_trace.py`
- `framework/run_scenarios.py`

Use-case definitions and deterministic scenarios live under `framework/examples/` and are loaded by `framework/use_case_files.py`.

## Core artifact flow

The end-to-end pipeline works over five main schema families:

1. `UseCaseDefinition` and `ScenarioDefinition`
2. `IntentArtifact`
3. `DomainArtifact`
4. `MockDbArtifact`
5. `SolutionArtifact`

The runtime bundle passed into the solver is `CaseBundle`, which combines the checked domain, intent, and mock DB artifacts under one `logic_level`.

## Enumerations

The most important enums in `framework/schemas.py` are:

- `LogicLevel`: `propositional`, `predicate`, `higher_order`
- `ClaimSource`: `user`, `db`, `derived`, `expert`, `statute_open`
- `RuleKind`: `allow_if_all`, `deny_if_all`, `set_false_if_all`
- `SolverOutcome`: `ALLOW`, `DENY`, `NEED_DB_INFO`, `NEED_USER_INFO`, `NEED_EXPERT_JUDGMENT`, `UNDETERMINED_INTERPRETATION`, `UNVERIFIABLE_CLAIM`
- `BlockReasonCode`: neutral blockage reasons. Process-level: `domain_extraction_empty`, `domain_extraction_sparse`, `no_applicable_rules`, `needs_db_info`, `needs_user_info`, `solver_inconsistent`. Uncertainty-specific (Wave 2 Stream B / ART-64): `statute_underspecified`, `interpretation_ambiguous`, `no_register`, `process_indeterminate`, `subjective_party`, `trust_only`, `context_dependent`, `glossary_low_confidence`, `model_drift`, `expert_judgment_required`
- `RuleStatus`: `fires`, `blocked`, `needs_info`

Only `propositional` is executable today. The other logic levels are retained as rendered and lowered views in the artifacts.

## Uncertainty taxonomy (U1..U12)

Wave 2 Stream B (ART-64) promotes twelve distinct kinds of uncertainty to first-class outcome / reason-code pairs. Backend-neutral routing logic lives in `framework/uncertainty_routing.py`; see [the reasoner reference](./reasoner.md) for the backend dispatcher. Every code is present in `ROUTING_TABLE`; the reasoner pragmatically routes the codes whose triggers fire in Wave 2.

| Code | Name | SolverOutcome | BlockReasonCode | Trigger |
|------|------|---------------|-----------------|---------|
| U1 | Statute under-specification | `UNDETERMINED_INTERPRETATION` | `statute_underspecified` | `DomainClaim.source_type == statute_open` |
| U2 | Interpretation ambiguity | `UNDETERMINED_INTERPRETATION` | `interpretation_ambiguous` | `DomainRule.interpretation_ambiguous == True` |
| U3 | Missing data source / no register | `UNVERIFIABLE_CLAIM` | `no_register` | `LookupSource.availability == "unavailable"` covering the missing claim |
| U4 | Process indeterminacy | `UNDETERMINED_INTERPRETATION` | `process_indeterminate` | `DomainRule.process_indeterminate == True` |
| U5 | Needs DB info | `NEED_DB_INFO` | `needs_db_info` | Missing DB-sourced claim (legacy path) |
| U6 | Subjective / party-biased claim | `UNVERIFIABLE_CLAIM` | `subjective_party` | `IntentClaim.subjective_party == True` |
| U7 | Trust-only claim | `UNVERIFIABLE_CLAIM` | `trust_only` | `LookupSource.trust_only == True` resolves the claim (overrides ALLOW) |
| U8 | Needs user info | `NEED_USER_INFO` | `needs_user_info` | Missing USER-sourced claim (legacy path) |
| U9 | Context-dependent applicability | `NEED_USER_INFO` | `context_dependent` | `DomainRule.context_dependent == True` |
| U10 | Expert judgment required | `NEED_EXPERT_JUDGMENT` | `expert_judgment_required` | `DomainClaim.source_type == expert` |
| U11 | Glossary / lexicon confidence | `UNDETERMINED_INTERPRETATION` | `glossary_low_confidence` | `IntentClaim.glossary_low_confidence == True` |
| U12 | Model drift / non-replicability | `UNDETERMINED_INTERPRETATION` | `model_drift` | `IntentClaim.model_drift == True` |

Trigger priority (first match wins, evaluated inside `classify_claim_uncertainty` / `classify_rule_uncertainty`):

1. Rule-level flags: U4 > U2 > U9.
2. Claim-level triggers: U1 > U10 > U3 > U7 > U6 > U12 > U11.
3. Legacy fallbacks: U5 (NEED_DB_INFO) and U8 (NEED_USER_INFO) emit `None` from the helpers so the reasoner keeps its pre-Wave-2 behaviour.

Trace rendering (`framework/logic_levels.py`) prefixes any uncertainty-specific `BlockReasonCode` with its U-code, for example `BLOCK REASON CODE: [U3:no_register] no_register`, and `ResolvedClaim.uncertainty_code` is shown inline next to the claim it annotates (for example when a trust-only source supplied the value).

### Transcript provenance

Each shipped U-code traces to a specific moment in the 2026-04-10, 14, or 17 supervision
transcripts. Timestamps reference `wip/supervision_meeting_transcripts/*.vtt`
(kept out of the public tree per `.cursor/rules/public_repo_hygiene.mdc`).

| Code | Transcript anchor |
|------|-------------------|
| U1  | 2026-04-17 ~09:31 (Priit: "journalist" as an undefined normative term) |
| U2  | 2026-04-17 ~05:16, ~08:00 (multiple admissible readings of one clause) |
| U3  | 2026-04-17 ~11:29 (no register to answer full legal capacity) |
| U4  | 2026-04-17 ~14:40 (archive walks, process not formalised) |
| U5  | Pre-existing legacy path (`NEED_DB_INFO`); promoted to a named taxonomy slot in Wave 2 |
| U6  | 2026-04-17 ~38:48 (applicant self-declaration, party-biased) |
| U7  | 2026-04-17 ~41:35 (trust signals over registers) |
| U8  | Pre-existing legacy path (`NEED_USER_INFO`); promoted to a named taxonomy slot in Wave 2 |
| U9  | 2026-04-17 ~09:55 (inter-variable, case-specific relations) |
| U10 | 2026-04-17 ~28:59 (expert-only resolution; covers "epistemic" uncertainty at solve time) |
| U11 | 2026-04-10 ~24:16 (Tanel: hand-built glossary confidence) |
| U12 | 2026-04-10 ~41:50 (Priit: ML parsing replicability vs ground truth) |

### Reconciliation with the planning taxonomy

The `post-17apr-research-push_a0104936` plan §1 proposed a slightly different
numbering for U5, U9, and U10. Wave 2 Stream B shipped the numbering in the
table above; the plan was updated after Wave 2 to match. The net differences:

- **Plan U5 "Inter-variable context dependence" → shipped U9 "Context-dependent applicability"** (same concept, routed via `DomainRule.context_dependent`).
- **Plan U5 and U8 slots → reused for the legacy `NEED_DB_INFO` / `NEED_USER_INFO` paths**, so every solver outcome is labelled by a U-code rather than living outside the taxonomy.
- **Plan U9 "Epistemic uncertainty about ground truth"** collapses into the shipped U10 "Expert judgment required". The distinction is relevant at the *paper-discussion* level (the modeller may not know the correct answer in hard legal cases) but is not distinguishable from U10 at solve time, so it does not get its own routing code.
- **Plan U10 "Multi-level alignment uncertainty"** is a *compound* of U1, U11, and U12 (statute openness × lexicon confidence × model drift). The trace already surfaces each component; adding a dedicated code would double-count. Kept for paper §Discussion, not the schema.

## Use-case definition layer

`UseCaseDefinition` is loaded from `framework/examples/*/use_case.json` and defines:

- `title`
- `description`
- `default_logic_level`
- `claims`
- `outcomes`
- `rules`

Each claim template carries labels, formal renderings for each logic level, and optional cue groups for request-text and law-text grounding. Each rule template links premise claim IDs to either an outcome or a negated target claim.

`ScenarioDefinition` stores the deterministic or live run configuration for one named scenario:

- `name`
- `description`
- `request_file`
- `law_file`
- `mock_db_file`
- optional prompt overrides
- deterministic `intent_assignments`

## Extraction artifacts

`IntentArtifact` is the checked output of step 1. Key fields:

- `artifact_type`
- `logic_level`
- `request_text`
- `lowered_view_note`
- `run_metadata`
- `claims`

Each `IntentClaim` includes the claim ID, formal text, truth value, reason text, and provenance snippets.

`DomainArtifact` is the checked output of step 2. Key fields:

- `artifact_type`
- `logic_level`
- `title`
- `law_text`
- `lowered_view_note`
- `allow_outcome_id`
- `deny_outcome_id`
- `run_metadata`
- `claims`
- `outcomes`
- `rules`

Each `DomainRule` stores both a readable `formal_text` and an explicit `lowered_formula`, plus linked `LawReference` excerpts.

`ExtractionRunMetadata` and `PromptMetadata` capture provenance for both extraction steps: timestamps, model names, source paths, prompt paths, and prompt hashes.

## Solve-time artifacts

`MockDbArtifact` is a list of `LookupSource` entries, each exposing a stable source ID, label, description, and a claim-value map.

`CaseBundle` is the direct solver input:

- `logic_level`
- `domain`
- `intent`
- `mock_db`

`SolutionArtifact` is the checked output of step 3 and the input to step 4. Key fields:

- `final_outcome`
- `intent_metadata`
- `domain_metadata`
- `solve_metadata`
- `blocked_at_step`
- `block_reason_code`
- `extracted_claim_count`
- `extracted_rule_count`
- `unresolved_claim_ids`
- `intent_claims`
- `domain_claims`
- `domain_rules`
- `trace_events`
- `lookup_events`
- `snapshots`

`SolveSnapshot` records one solver pass, including resolved claims, rule trace rows, and outstanding DB/user information needs.

## Operational notes

- The LLM is limited to structured intermediate artifacts. It does not decide the final outcome.
- The symbolic solver has final authority over `ALLOW`, `DENY`, and missing-information states.
- Prompt paths, source paths, and law references are first-class schema fields because auditability and provenance are part of the current implementation contract.
