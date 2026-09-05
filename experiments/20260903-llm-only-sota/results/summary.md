# 20260903-llm-only-sota

Generated 2026-09-05T17:46:55Z — execution `parallel`, condition `llm-only`.

**Question:** Does a frontier model close the gap to the architecture without it? LLM-only baseline on the four SOTA models, one repeat (indicative, n=47 per model).


## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | skip |  |  |  |  |
| term_rule | skip |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | skip |  |  |  |  |
| term_claim | skip |  |  |  |  |
| registry_record | file |  |  |  |  |
| record_term | skip |  |  |  |  |
| term_fact | skip |  |  |  |  |
| premise_outcome | llm | decide | decide-raw-sources |  |  |
| outcome_trace | llm | justify | justify-v1 |  |  |

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-pro | 47 | 0.575 | 0.595 | 0.800 | 0.375 | 0.590 | 0.553 | 0.553 | 0.553 |
| fable-5.1 | 47 | 0.553 | 0.611 | 0.250 | 0.619 | 0.493 | 0.553 | 0.553 | 0.553 |
| gemini-3.1-pro | 47 | 0.723 | 0.667 | 0.783 | 0.723 | 0.724 | 0.553 | 0.553 | 0.553 |
| gpt-5.6-sol | 47 | 0.575 | 0.593 | 0.250 | 0.667 | 0.503 | 0.553 | 0.553 | 0.553 |

Support per class (per repeat-model slice): ALLOW: 14, DENY: 12, NEED_MORE_INFO: 21.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit_grant/need_register_silent_fee` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_trust_only_designer_selfreport` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 4 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_register_silent_consumer_status` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 2 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 4 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 94 | 0.5196 |
| fable-5.1 | 94 | 5.1316 |
| gemini-3.1-pro | 94 | 0.8922 |
| gpt-5.6-sol | 94 | 2.9477 |

Total: EUR 9.4911.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
