# 20260903-llm-decides-on-oracle-inputs-partial-specification-sota

Generated 2026-09-05T17:46:55Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-partial-specification`.

**Question:** Do frontier models play solver correctly on identical inputs (oracle rules, oracle claims, looked-up facts with warrant, no statute text)? Three repeats.


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
| premise_outcome | llm | decide | solver-inputs-partial-specification |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-pro | 141 | 0.652 | 0.638 | 0.421 | 0.821 | 0.627 | 0.858 | 0.807 | 0.821 |
| fable-5.1 | 141 | 0.745 | 0.703 | 0.143 | 0.977 | 0.607 | 0.979 | 0.943 | 0.953 |
| gemini-3.1-pro | 141 | 0.745 | 0.703 | 0.143 | 0.977 | 0.607 | 0.979 | 0.943 | 0.953 |
| gpt-5.6-sol | 141 | 0.766 | 0.722 | 0.267 | 0.977 | 0.655 | 0.979 | 0.943 | 0.953 |

Support per class (per repeat-model slice): ALLOW: 42, DENY: 36, NEED_MORE_INFO: 63.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 9 wrong rows (e.g. fable-5.1: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 9 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 8 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_admission/need_user_silent_conflict_declaration` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 12 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 11 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 10 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 9 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 141 | 0.1009 |
| fable-5.1 | 141 | 4.1342 |
| gemini-3.1-pro | 141 | 0.3958 |
| gpt-5.6-sol | 141 | 0.5929 |

Total: EUR 5.2239.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
