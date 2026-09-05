# 20260903-llm-decides-on-oracle-inputs-partial-specification

Generated 2026-09-05T17:46:54Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-partial-specification`.

**Question:** Decision-step isolation with identical inputs: oracle rules + oracle claims + looked-up facts, LLM decides. Pair row for solver-validation (1.00).


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
| deepseek-v4-flash | 469 | 0.544 | 0.483 | 0.464 | 0.665 | 0.537 | 0.748 | 0.726 | 0.733 |
| gemini-2.5-flash | 470 | 0.702 | 0.638 | 0.143 | 0.923 | 0.568 | 0.925 | 0.889 | 0.900 |
| gpt-5-mini | 470 | 0.743 | 0.699 | 0.143 | 0.975 | 0.606 | 0.977 | 0.940 | 0.951 |
| haiku-4.5 | 470 | 0.519 | 0.453 | 0.041 | 0.670 | 0.388 | 0.571 | 0.560 | 0.552 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 209.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 12 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 27 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 14 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_claims_verified` — 9 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 30 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/need_user_silent_conflict_declaration` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 40 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 21 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 16 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 5 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 20 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 20 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Errors

1 rows errored:

- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` deepseek-v4-flash: RuntimeError: deepseek/deepseek-v4-flash failed after 3 attempts: Expecting ',' delimiter: line 1 column 1369 (char 1368)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 469 | 0.1420 |
| gemini-2.5-flash | 470 | 0.2132 |
| gpt-5-mini | 470 | 0.7743 |
| haiku-4.5 | 470 | 0.8809 |

Total: EUR 2.0104.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
