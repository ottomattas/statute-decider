# 20260906-llm-decides-on-llm-claims-full-procedure-r2

Generated 2026-09-07T06:08:11Z — execution `parallel`, condition `llm-decides-on-llm-claims-full-procedure`.

**Question:** The architecture minus the solver: LLM-extracted claims, decide prompt with the full procedure. Cheap grid x 10.

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
| premise_outcome | llm | decide | solver-inputs-full-procedure |  |  |
| outcome_trace | passthrough |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 540 | 0.924 | 0.878 | 0.972 | 0.919 | 0.923 | 0.940 | 0.926 | 0.931 |
| gemini-2.5-flash | 540 | 0.989 | 0.983 | 1.000 | 0.984 | 0.989 | 0.989 | 0.967 | 0.975 |
| gpt-5-mini | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.978 | 0.986 |
| haiku-4.5 | 540 | 0.798 | 0.756 | 0.749 | 0.883 | 0.796 | 0.918 | 0.886 | 0.896 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 5 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 5 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 23 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 3 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 9 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 3 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 12 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 7 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 9 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 9 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 1 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 5 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 12 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 19 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 10 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_register_only_purpose_from_cms` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/allow_claims_verified` — 3 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 2 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `land_tax_home_exemption/need_register_silent_municipality_exemption` — 3 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 1081 | 0.1557 |
| gemini-2.5-flash | 1080 | 0.8683 |
| gpt-5-mini | 1080 | 1.9109 |
| haiku-4.5 | 1081 | 2.5524 |

Total: EUR 5.4872.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
