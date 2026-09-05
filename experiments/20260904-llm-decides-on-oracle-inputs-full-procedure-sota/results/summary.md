# 20260904-llm-decides-on-oracle-inputs-full-procedure-sota

Generated 2026-09-05T21:24:46Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-full-procedure`.

**Question:** SOTA models as solver with the full staged specification (solver-inputs-full-procedure), 3 repeats.

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
| deepseek-v4-pro | 141 | 0.752 | 0.741 | 0.652 | 0.844 | 0.746 | 0.879 | 0.844 | 0.856 |
| fable-5.1 | 141 | 0.972 | 0.950 | 1.000 | 0.969 | 0.973 | 0.972 | 0.972 | 0.972 |
| gemini-3.1-pro | 141 | 0.957 | 0.923 | 1.000 | 0.955 | 0.959 | 0.957 | 0.957 | 0.957 |
| gpt-5.6-sol | 141 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 42, DENY: 36, NEED_MORE_INFO: 63.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_no_site_study` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 5 wrong rows (e.g. fable-5.1: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 2 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/need_user_silent_conflict_declaration` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 8 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 141 | 0.1044 |
| fable-5.1 | 141 | 5.0912 |
| gemini-3.1-pro | 141 | 0.4635 |
| gpt-5.6-sol | 141 | 0.6840 |

Total: EUR 6.3431.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
