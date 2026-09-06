# 20260906-llm-only-plus-rules

Generated 2026-09-06T14:36:13Z — execution `parallel`, condition `llm-only-plus-rules`.

**Question:** Does adding the oracle rules to the raw-sources prompt close the gap without a solver? Single structured call (Ruling J). Cheap grid x 10.

## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | skip |  |  |  |  |
| term_claim | skip |  |  |  |  |
| registry_record | file |  |  |  |  |
| record_term | skip |  |  |  |  |
| term_fact | skip |  |  |  |  |
| premise_outcome | llm | decide | decide-raw-sources-plus-rules |  |  |
| outcome_trace | passthrough |  |  |  |  |

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 540 | 0.619 | 0.542 | 0.589 | 0.683 | 0.605 | 0.611 | 0.629 | 0.610 |
| gemini-2.5-flash | 540 | 0.593 | 0.491 | 0.689 | 0.592 | 0.591 | 0.547 | 0.569 | 0.549 |
| gpt-5-mini | 540 | 0.526 | 0.419 | 0.443 | 0.619 | 0.494 | 0.519 | 0.561 | 0.528 |
| haiku-4.5 | 540 | 0.654 | 0.586 | 0.701 | 0.677 | 0.655 | 0.684 | 0.683 | 0.675 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 31 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 28 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 6 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 28 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 22 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 11 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 10 wrong rows (e.g. gemini-2.5-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 23 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_admission/allow_claims_verified` — 19 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 26 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 28 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 35 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 37 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 8 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 19 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 2 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 24 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_catalogue_clears_exclusion` — 22 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 35 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 39 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 17 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 37 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 17 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_register_only_purpose_from_cms` — 32 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_public_interest` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 32 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 5 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 17 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 39 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 39 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 15 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 23 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 33 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/unverifiable_register_down_population_registry` — 6 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.2801 |
| gemini-2.5-flash | 540 | 1.3701 |
| gpt-5-mini | 540 | 1.7810 |
| haiku-4.5 | 540 | 3.1883 |

Total: EUR 6.6196.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
