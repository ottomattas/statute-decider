# 20260906-llm-only

Generated 2026-09-06T15:05:44Z — execution `parallel`, condition `llm-only`.

**Question:** LLM-only baseline from raw sources: full act unit, request, registers; one structured call (Ruling J). Cheap grid x 10.

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
| outcome_trace | passthrough |  |  |  |  |

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 540 | 0.791 | 0.753 | 0.775 | 0.849 | 0.792 | 0.667 | 0.667 | 0.667 |
| gemini-2.5-flash | 540 | 0.619 | 0.557 | 0.657 | 0.643 | 0.619 | 0.667 | 0.667 | 0.667 |
| gpt-5-mini | 540 | 0.593 | 0.582 | 0.515 | 0.656 | 0.585 | 0.667 | 0.667 | 0.667 |
| haiku-4.5 | 540 | 0.667 | 0.702 | 0.728 | 0.582 | 0.670 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/allow_claims_verified` — 3 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only` — 9 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only_design_conformity` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 21 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 24 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 6 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 3 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 2 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 6 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_register_only_not_parent` — 6 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 6 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 4 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 26 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 4 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 8 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 23 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 39 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 11 wrong rows (e.g. gemini-2.5-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 7 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 2 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 35 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 22 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 28 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` — 22 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 39 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 18 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 39 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 29 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 25 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 23 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 24 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 13 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/unverifiable_register_down_population_registry` — 2 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 5 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.2646 |
| gemini-2.5-flash | 540 | 1.3417 |
| gpt-5-mini | 540 | 1.6493 |
| haiku-4.5 | 540 | 3.1757 |

Total: EUR 6.4313.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
