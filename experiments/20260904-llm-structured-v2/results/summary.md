# 20260904-llm-structured-v2

Generated 2026-09-04T07:26:28Z — execution `parallel`, condition `llm-structured-v2`.

**Question:** Candidate minus the solver, decide prompt with the staged specification (solver-inputs-v2).

## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | llm | ground | ground-v1 |  | yes |
| term_claim | llm |  |  |  | yes |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | llm | decide | solver-inputs-v2 |  |  |
| outcome_trace | skip |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.757 | 0.827 | 0.811 | 0.630 | 0.756 | 0.757 | 0.745 | 0.748 |
| gemini-2.5-flash | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 | 0.977 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.979 |
| haiku-4.5 | 470 | 0.651 | 0.626 | 0.566 | 0.695 | 0.629 | 0.525 | 0.544 | 0.523 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_deny` — 1 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 1 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 3 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u7_trust_only` — 1 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 11 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_allow_via_db` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 9 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 8 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_u5_need_db` — 7 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u7_trust_only` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_deny_no_basis` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 6 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/db-then-user` — 13 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-db` — 14 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `section_120_demo/unrelated-law` — 2 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 942 | 0.0821 |
| gemini-2.5-flash | 941 | 0.4283 |
| gpt-5-mini | 942 | 1.4808 |
| haiku-4.5 | 942 | 1.6966 |

Total: EUR 3.6877.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
