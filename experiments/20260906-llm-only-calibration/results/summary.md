# 20260906-llm-only-calibration

Generated 2026-09-06T12:19:33Z — execution `parallel`, condition `llm-only`.

**Question:** Calibration pass before the paid grids on the per-case-balanced 54-scenario suite (gold approved
2026-09-06 15:10): does the single-call llm-only baseline (Ruling J) parse and score cleanly on every
case with the warm-up gate, what is the real cached share and cost per (model, act), and does the
n = 1 Civil Service Act DENY -> ALLOW pattern from the smoke run hold? gpt-5-mini, one repeat.


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
| gpt-5-mini | 54 | 0.630 | 0.591 | 0.560 | 0.718 | 0.623 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| gpt-5-mini | 54 | 0.1998 |

Total: EUR 0.1998.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
