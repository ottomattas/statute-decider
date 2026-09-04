# 20260903-llm-as-solver

Generated 2026-09-03T20:04:41Z — execution `parallel`, condition `llm-as-solver`.

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
| premise_outcome | llm | decide | solver-inputs-v1 |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 469 | 0.544 | 0.483 | 0.464 | 0.665 | 0.537 | 0.748 | 0.726 | 0.733 |
| gemini-2.5-flash | 470 | 0.702 | 0.638 | 0.143 | 0.923 | 0.568 | 0.925 | 0.889 | 0.900 |
| gpt-5-mini | 470 | 0.743 | 0.699 | 0.143 | 0.975 | 0.606 | 0.977 | 0.940 | 0.951 |
| haiku-4.5 | 470 | 0.519 | 0.453 | 0.041 | 0.670 | 0.388 | 0.571 | 0.560 | 0.552 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 209.

## Failure patterns

- `building_permit/building_permit_deny` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 9 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny` — 30 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `civil_service_eligibility/civil_service_u8_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_allow_via_db` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `consumer_withdrawal/consumer_withdrawal_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 20 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 20 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_u7_trust_only` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 21 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 40 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `personal_data_journalism/journalism_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_deny_no_basis` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 16 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u7_trust_only` — 5 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/allow` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `section_120_demo/db-then-user` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 27 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 14 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 12 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `section_120_demo/unrelated-law` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)

## Errors

1 rows errored:

- `personal_data_journalism/journalism_u3_no_register` deepseek-v4-flash: RuntimeError: deepseek/deepseek-v4-flash failed after 3 attempts: Expecting ',' delimiter: line 1 column 1369 (char 1368)

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
