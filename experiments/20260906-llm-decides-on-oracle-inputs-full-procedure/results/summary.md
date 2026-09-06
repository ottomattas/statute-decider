# 20260906-llm-decides-on-oracle-inputs-full-procedure

Generated 2026-09-06T13:19:02Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-full-procedure`.

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
| deepseek-v4-flash | 540 | 0.902 | 0.867 | 0.962 | 0.875 | 0.901 | 0.907 | 0.899 | 0.901 |
| gemini-2.5-flash | 540 | 0.980 | 0.969 | 1.000 | 0.970 | 0.980 | 0.980 | 0.953 | 0.961 |
| gpt-5-mini | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.987 | 0.992 |
| haiku-4.5 | 540 | 0.833 | 0.803 | 0.790 | 0.900 | 0.831 | 0.930 | 0.898 | 0.908 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 5 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 26 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 4 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 7 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 3 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 12 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 6 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 7 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 12 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 7 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_register_only_purpose_from_cms` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 4 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 2 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 2 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/need_register_silent_municipality_exemption` — 8 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 2 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.1080 |
| gemini-2.5-flash | 540 | 0.5763 |
| gpt-5-mini | 540 | 1.1501 |
| haiku-4.5 | 540 | 1.8917 |

Total: EUR 3.7262.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
