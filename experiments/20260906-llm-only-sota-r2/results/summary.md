# 20260906-llm-only-sota-r2

Generated 2026-09-06T18:12:54Z — execution `parallel`, condition `llm-only`.

**Question:** Does a frontier model close the gap to the architecture without it? LLM-only single call, SOTA x 1, indicative.

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
| deepseek-v4-pro | 54 | 0.741 | 0.765 | 0.788 | 0.683 | 0.745 | 0.667 | 0.667 | 0.667 |
| fable-5.1 | 54 | 0.759 | 0.732 | 0.621 | 0.895 | 0.749 | 0.667 | 0.667 | 0.667 |
| gemini-3.1-pro | 54 | 0.648 | 0.500 | 0.688 | 0.708 | 0.632 | 0.667 | 0.667 | 0.667 |
| gpt-5.6-sol | 54 | 0.630 | 0.562 | 0.621 | 0.681 | 0.621 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

## Failure patterns

- `building_permit_grant/allow_claims_verified` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only` — 2 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only_design_conformity` — 2 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 3 wrong rows (e.g. fable-5.1: NEED_MORE_INFO != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 2 wrong rows (e.g. fable-5.1: ALLOW != DENY)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 1 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 3 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 2 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 3 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 3 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 4 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 2 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 3 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 2 wrong rows (e.g. gemini-3.1-pro: ALLOW != DENY)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 54 | 0.6181 |
| fable-5.1 | 54 | 11.8875 |
| gemini-3.1-pro | 56 | 1.4503 |
| gpt-5.6-sol | 54 | 1.3467 |

Total: EUR 15.3026.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
