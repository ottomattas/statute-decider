# 20260906-llm-only-r2

Generated 2026-09-06T18:41:18Z — execution `parallel`, condition `llm-only`.

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
| deepseek-v4-flash | 540 | 0.719 | 0.687 | 0.755 | 0.722 | 0.721 | 0.667 | 0.667 | 0.667 |
| gemini-2.5-flash | 540 | 0.613 | 0.488 | 0.635 | 0.711 | 0.611 | 0.667 | 0.667 | 0.667 |
| gpt-5-mini | 540 | 0.606 | 0.587 | 0.498 | 0.695 | 0.593 | 0.667 | 0.667 | 0.667 |
| haiku-4.5 | 540 | 0.702 | 0.719 | 0.745 | 0.653 | 0.706 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/allow_claims_verified` — 10 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only` — 14 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only_design_conformity` — 15 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 27 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 20 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 7 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 9 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_register_only_sole_custody` — 1 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 6 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 9 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `child_representation_by_one_parent/deny_register_only_not_parent` — 6 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 3 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 17 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 6 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 22 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 6 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 19 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 26 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 4 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 37 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 34 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 32 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` — 13 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 37 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 10 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 37 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 11 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 24 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 24 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 23 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 14 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 19 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.2765 |
| gemini-2.5-flash | 540 | 1.3920 |
| gpt-5-mini | 540 | 1.5579 |
| haiku-4.5 | 540 | 3.2560 |

Total: EUR 6.4823.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
