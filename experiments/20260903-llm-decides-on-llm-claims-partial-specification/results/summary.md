# 20260903-llm-decides-on-llm-claims-partial-specification

Generated 2026-09-05T22:04:46Z — execution `parallel`, condition `llm-decides-on-llm-claims-partial-specification`.

**Question:** The architecture condition minus the solver: oracle rules, LLM-extracted claims (fused ground), looked-up facts, LLM decides on those premises.


## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | llm | ground | ground |  | yes |
| term_claim | llm |  |  |  | yes |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | llm | decide | solver-inputs-partial-specification |  |  |
| outcome_trace | skip |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 469 | 0.618 | 0.661 | 0.662 | 0.521 | 0.615 | 0.646 | 0.662 | 0.647 |
| gemini-2.5-flash | 468 | 0.763 | 0.872 | 0.286 | 0.830 | 0.662 | 0.827 | 0.780 | 0.794 |
| gpt-5-mini | 470 | 0.681 | 0.778 | 0.286 | 0.727 | 0.597 | 0.745 | 0.698 | 0.712 |
| haiku-4.5 | 470 | 0.523 | 0.341 | 0.268 | 0.665 | 0.425 | 0.448 | 0.502 | 0.459 |

Support per class (per repeat-model slice): ALLOW: 139, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 17 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_trust_only_designer_selfreport` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 12 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 19 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 3 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 24 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 24 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 13 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 16 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 10 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 16 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 17 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/need_register_silent_municipality_exemption` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_register_down_population_registry` — 12 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Errors

3 rows errored:

- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` deepseek-v4-flash: RuntimeError: deepseek/deepseek-v4-flash failed after 5 attempts: Request timed out.
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 939 | 0.0792 |
| gemini-2.5-flash | 936 | 0.4109 |
| gpt-5-mini | 940 | 1.4563 |
| haiku-4.5 | 940 | 1.5918 |

Total: EUR 3.5381.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
