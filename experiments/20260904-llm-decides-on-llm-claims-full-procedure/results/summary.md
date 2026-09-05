# 20260904-llm-decides-on-llm-claims-full-procedure

Generated 2026-09-05T22:04:48Z — execution `parallel`, condition `llm-decides-on-llm-claims-full-procedure`.

**Question:** The architecture condition minus the solver, decide prompt with the staged specification (solver-inputs-full-procedure).

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
| outcome_trace | skip |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.757 | 0.827 | 0.811 | 0.630 | 0.756 | 0.757 | 0.745 | 0.748 |
| gemini-2.5-flash | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 | 0.977 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.979 |
| haiku-4.5 | 470 | 0.651 | 0.626 | 0.566 | 0.695 | 0.629 | 0.525 | 0.544 | 0.523 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 1 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 1 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_trust_only_designer_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 14 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/need_register_silent_citizenship` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 11 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 8 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 9 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_register_silent_consumer_status` — 7 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 6 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/need_register_silent_municipality_exemption` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 942 | 0.0821 |
| gemini-2.5-flash | 941 | 0.4283 |
| gpt-5-mini | 942 | 1.4808 |
| haiku-4.5 | 942 | 1.6966 |

Total: EUR 3.6877.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
