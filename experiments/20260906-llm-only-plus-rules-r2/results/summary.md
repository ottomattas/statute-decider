# 20260906-llm-only-plus-rules-r2

Generated 2026-09-06T19:44:22Z — execution `parallel`, condition `llm-only-plus-rules`.

**Question:** Does adding the oracle rules to the raw-sources prompt close the gap without a solver? Single structured call (Ruling J). Cheap grid x 10.

## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | skip |  |  |  |  |
| term_claim | skip |  |  |  |  |
| registry_record | file |  |  |  |  |
| record_term | skip |  |  |  |  |
| term_fact | skip |  |  |  |  |
| premise_outcome | llm | decide | decide-raw-sources-plus-rules |  |  |
| outcome_trace | passthrough |  |  |  |  |

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 540 | 0.624 | 0.575 | 0.598 | 0.672 | 0.615 | 0.624 | 0.643 | 0.623 |
| gemini-2.5-flash | 540 | 0.619 | 0.538 | 0.648 | 0.654 | 0.613 | 0.624 | 0.634 | 0.622 |
| gpt-5-mini | 540 | 0.513 | 0.420 | 0.440 | 0.593 | 0.484 | 0.495 | 0.543 | 0.507 |
| haiku-4.5 | 540 | 0.609 | 0.556 | 0.621 | 0.643 | 0.607 | 0.634 | 0.634 | 0.626 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 30 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 28 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 4 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `building_permit_grant/unverifiable_trust_only_designer_selfreport` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 32 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 33 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis` — 25 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 17 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/unverifiable_register_down_custody_registry` — 6 wrong rows (e.g. gemini-2.5-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 29 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_admission/allow_claims_verified` — 12 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 23 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 31 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 37 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 39 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_register_down_population_registry` — 16 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 3 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 10 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_catalogue_clears_exclusion` — 12 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/allow_register_only_consumer_status` — 15 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 8 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 36 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 26 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 34 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 35 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/allow_register_only_purpose_from_cms` — 26 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_public_interest` — 13 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 3 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 16 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 4 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 39 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 21 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 36 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/unverifiable_register_down_population_registry` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 541 | 0.2709 |
| gemini-2.5-flash | 540 | 1.5924 |
| gpt-5-mini | 540 | 1.8374 |
| haiku-4.5 | 540 | 3.3747 |

Total: EUR 7.0754.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
