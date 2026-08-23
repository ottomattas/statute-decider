# Experiment (i) — SMOKE — UNVALIDATED

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
