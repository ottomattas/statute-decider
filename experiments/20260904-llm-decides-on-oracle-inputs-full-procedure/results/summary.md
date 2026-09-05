# 20260904-llm-decides-on-oracle-inputs-full-procedure

Generated 2026-09-05T21:24:46Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-full-procedure`.

**Question:** LLM decides on oracle inputs with the solver's staged precedence rule stated (solver-inputs-full-procedure). The partial-specification misses on 3 Sep were 100% on the 13 claim/fact-conflict scenarios for the strong models.


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
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.628 | 0.678 | 0.516 | 0.671 | 0.622 | 0.779 | 0.762 | 0.767 |
| gemini-2.5-flash | 470 | 0.983 | 0.971 | 1.000 | 0.981 | 0.984 | 0.983 | 0.967 | 0.973 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.985 | 0.991 |
| haiku-4.5 | 470 | 0.651 | 0.628 | 0.462 | 0.742 | 0.611 | 0.695 | 0.662 | 0.665 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 13 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_no_allow_path_no_site_study` — 20 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit_grant/need_register_silent_fee` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 3 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 2 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 1 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 15 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 12 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 18 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_admission/allow_claims_verified` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 20 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/unverifiable_trust_only_applicant_selfreport` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 18 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 20 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/deny_own_admission_excessive_harm` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_user_silent_editorial_judgements` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 14 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 7 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 4 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 20 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 470 | 0.0479 |
| gemini-2.5-flash | 470 | 0.1647 |
| gpt-5-mini | 470 | 0.8381 |
| haiku-4.5 | 470 | 0.9897 |

Total: EUR 2.0404.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
