# 20260906-llm-decides-on-oracle-inputs-full-procedure-r2

Generated 2026-09-06T20:14:39Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-full-procedure`.

**Question:** With the solver's own inputs and its full procedure stated, how well does each cheap model decide in the solver's place? Cheap grid x 10.

## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | oracle |  |  |  |  |
| term_claim | oracle |  |  |  |  |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | llm | decide | solver-inputs-full-procedure |  |  |
| outcome_trace | passthrough |  |  |  |  |

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 540 | 0.937 | 0.900 | 0.992 | 0.919 | 0.937 | 0.935 | 0.929 | 0.928 |
| gemini-2.5-flash | 540 | 0.993 | 0.989 | 1.000 | 0.989 | 0.993 | 0.993 | 0.980 | 0.984 |
| gpt-5-mini | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.987 | 0.992 |
| haiku-4.5 | 540 | 0.832 | 0.815 | 0.789 | 0.884 | 0.830 | 0.918 | 0.885 | 0.895 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 16 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 4 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 2 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 4 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 3 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 5 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 2 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 5 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_register_only_purpose_from_cms` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/allow_claims_verified` — 1 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 6 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/need_register_silent_municipality_exemption` — 4 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_register_down_population_registry` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.1075 |
| gemini-2.5-flash | 540 | 0.6070 |
| gpt-5-mini | 540 | 1.1832 |
| haiku-4.5 | 540 | 1.8387 |

Total: EUR 3.7364.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
