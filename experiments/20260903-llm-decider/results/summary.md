# 20260903-llm-decider

Generated 2026-09-03T21:24:04Z — execution `parallel`, condition `llm-decider`.

**Question:** Priit's 28 Aug missing 2x2 cell, re-run on v2: oracle rules + LLM decides from the same raw sources as the baseline. Compare to solver-validation 1.00 and to the v1 oracle-llm-20260901 numbers (0.85-0.89).


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
| premise_outcome | llm | decide | oracle-rules-v1 |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.655 | 0.377 | 0.889 | 0.646 | 0.637 | 0.488 | 0.519 | 0.493 |
| gemini-2.5-flash | 470 | 0.617 | 0.483 | 0.578 | 0.679 | 0.580 | 0.494 | 0.524 | 0.496 |
| gpt-5-mini | 470 | 0.523 | 0.273 | 0.273 | 0.668 | 0.405 | 0.435 | 0.492 | 0.447 |
| haiku-4.5 | 470 | 0.615 | 0.381 | 0.829 | 0.637 | 0.616 | 0.464 | 0.507 | 0.468 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_deny` — 10 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 10 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 6 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_allow_eu_path` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_need_db` — 23 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u3_no_register` — 10 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 37 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_allow_via_db` — 36 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 23 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 24 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_u3_no_register` — 8 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u5_need_db` — 11 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u7_trust_only` — 9 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 40 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 23 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 25 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_u3_no_register` — 5 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u7_trust_only` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 37 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 38 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_deny` — 14 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_deny_no_basis` — 11 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_u3_no_register` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u5_need_db` — 29 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u7_trust_only` — 7 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `section_120_demo/allow` — 30 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `section_120_demo/db-then-user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 30 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `section_120_demo/unrelated-law` — 29 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 470 | 0.0600 |
| gemini-2.5-flash | 470 | 0.4083 |
| gpt-5-mini | 470 | 1.0688 |
| haiku-4.5 | 470 | 1.5313 |

Total: EUR 3.0684.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
