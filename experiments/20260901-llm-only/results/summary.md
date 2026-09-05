# 20260901-llm-only

Generated 2026-09-05T22:04:44Z — execution `parallel`, condition `llm-only`.

**Question:** Committed run 2 of 3: LLM-only source-to-trace. Raw statute text, utterance, and registry go to the model, which decides and justifies without any intermediate structure. The comparison floor for the architecture condition.


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
| outcome_trace | llm | justify | justify |  |  |

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.660 | 0.629 | 0.889 | 0.500 | 0.672 | 0.553 | 0.553 | 0.553 |
| gemini-2.5-flash | 470 | 0.594 | 0.595 | 0.486 | 0.640 | 0.574 | 0.553 | 0.553 | 0.553 |
| gpt-5-mini | 470 | 0.491 | 0.494 | 0.258 | 0.574 | 0.442 | 0.553 | 0.553 | 0.553 |
| haiku-4.5 | 470 | 0.662 | 0.579 | 0.891 | 0.574 | 0.681 | 0.553 | 0.553 | 0.553 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit_grant/allow_claims_verified` — 10 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only` — 11 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit_grant/need_register_silent_fee` — 33 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 9 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 21 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 15 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 15 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 34 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 18 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 17 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 22 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 25 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 20 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 14 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 12 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_register_silent_consumer_status` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 11 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 15 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 38 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 30 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 9 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 9 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 10 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 40 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 940 | 1.9964 |
| gemini-2.5-flash | 940 | 2.6844 |
| gpt-5-mini | 942 | 3.4053 |
| haiku-4.5 | 942 | 10.0282 |

Total: EUR 18.1142.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
