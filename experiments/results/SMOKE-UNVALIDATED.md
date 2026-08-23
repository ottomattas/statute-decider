# SMOKE — UNVALIDATED

Generated 2026-08-21T08:18:32Z. Overnight cap EUR 10.00; spent EUR 0.9516; remaining EUR 9.0484.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `smoke-2026-08-20`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: gemini, openai, anthropic, deepseek.
Providers skipped (missing key or stub): —.

### Experiment (ii) — runtime (solver)

- n scored: 47 / 47
- outcome accuracy: 1.000
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 1.000
- mean missing-fact P/R: 0.936 / 1.000
- macro missing-fact P/R: 0.929 / 1.000

### Experiment (ii) — LLM-only (all providers)

- n scored: 188 / 188
- outcome accuracy: 0.734
- ALLOW accuracy: 0.857
- DENY accuracy: 0.938
- NEED_MORE_INFO accuracy: 0.536
- mean missing-fact P/R: 0.970 / 0.785
- macro missing-fact P/R: 0.972 / 0.839

### Experiment (ii) — LLM-only `gemini`

- n scored: 47 / 47
- outcome accuracy: 0.681
- ALLOW accuracy: 0.857
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.381
- mean missing-fact P/R: 0.989 / 0.723
- macro missing-fact P/R: 0.992 / 0.794

### Experiment (ii) — LLM-only `openai`

- n scored: 47 / 47
- outcome accuracy: 0.723
- ALLOW accuracy: 0.929
- DENY accuracy: 0.917
- NEED_MORE_INFO accuracy: 0.476
- mean missing-fact P/R: 0.982 / 0.759
- macro missing-fact P/R: 0.987 / 0.820

### Experiment (ii) — LLM-only `anthropic`

- n scored: 47 / 47
- outcome accuracy: 0.745
- ALLOW accuracy: 0.786
- DENY accuracy: 0.917
- NEED_MORE_INFO accuracy: 0.619
- mean missing-fact P/R: 0.957 / 0.812
- macro missing-fact P/R: 0.956 / 0.860

### Experiment (ii) — LLM-only `deepseek`

- n scored: 47 / 47
- outcome accuracy: 0.787
- ALLOW accuracy: 0.857
- DENY accuracy: 0.917
- NEED_MORE_INFO accuracy: 0.667
- mean missing-fact P/R: 0.950 / 0.844
- macro missing-fact P/R: 0.951 / 0.884

### Experiment (i) — encoding

# Experiment (i) — synthesis extraction vs gold encoding

Catalog-held-out boolean synthesis scored by lexical claim alignment and truth-table paper-outcome equivalence. Selection-mode ablation scores catalog-id F1 via existing `llm.extract_domain_artifact`.

| case | provider | align F1 | equivalent | rate | n_agree/n_rows | audit | dropped rules |
| --- | --- | --- | --- | --- | --- | --- | --- |
| consumer_withdrawal | gemini | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| civil_service_eligibility | gemini | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| section_120_demo | gemini | — | error | — | — | — | — |
| consumer_withdrawal | openai | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| civil_service_eligibility | openai | 0.48 | no | 0.97 | 31/32 | yes | 0 |
| section_120_demo | openai | 0.00 | no | 0.00 | 0/0 | no | 0 |
| consumer_withdrawal | anthropic | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| civil_service_eligibility | anthropic | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| section_120_demo | anthropic | 0.00 | no | 0.00 | 0/0 | no | 0 |
| consumer_withdrawal | deepseek | 0.31 | yes | 1.00 | 4/4 | no | 0 |
| civil_service_eligibility | deepseek | 0.56 | no | 0.84 | 27/32 | yes | 6 |
| section_120_demo | deepseek | 0.00 | no | 0.00 | 0/0 | no | 0 |

## Needs operator audit

- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency_met', 'position_is_estonian_citizen_only', 'has_conviction_for_intentional_state_crime', 'prohibited_from_position_by_court_order', 'is_relative_of_direct_supervisor', 'position_is_not_estonian_citizen_only']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['is_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'meets_language_requirement', 'meets_statutory_requirements_for_eu', 'no_disqualifying_record', 'has_conviction_intentional_state_crime', 'court_prohibition_on_position', 'is_close_relative_of_supervising_official']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'is_sensitive_position', 'meets_general_requirements']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_other_legal_requirements', 'position_restricted_to_estonian_citizens', 'no_intentional_crime_against_state_conviction', 'no_court_restriction_on_position', 'no_family_relationship_with_supervisor']`.

Mean alignment F1: 0.263 (n=11).

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).

## This run (21 Aug 08:18Z)

- All four cheap providers completed experiment (ii): 188 LLM rows, no budget halt.
- Gemini `section_120_demo` synthesis: truncated JSON (`Unterminated string`).
- §120 synthesis F1 = 0 on the three models that parsed: they invented marriage-capacity claims, not the gold parent/custody vocabulary.
- “Equivalent yes” on consumer_withdrawal is on a 2–4 row aligned subspace (often only `distance_contract`). Do not read that as full-encoding match.
- OpenAI civil-service alignment includes a suspect pair (`ee_citizen` ~ `is_not_estonian_citizen`). Hand-audit before treating F1 as evidence.
