# 20260903-llm-structured

Generated 2026-09-03T22:38:27Z — execution `parallel`, condition `llm-structured`.

**Question:** Candidate minus the solver: oracle rules, LLM-extracted claims (fused ground), looked-up facts, LLM decides on those premises.


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
| premise_outcome | llm | decide | solver-inputs-v1 |  |  |
| outcome_trace | skip |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 469 | 0.618 | 0.661 | 0.662 | 0.521 | 0.615 | 0.646 | 0.662 | 0.647 |
| gemini-2.5-flash | 468 | 0.763 | 0.872 | 0.286 | 0.830 | 0.662 | 0.827 | 0.780 | 0.794 |
| gpt-5-mini | 470 | 0.681 | 0.778 | 0.286 | 0.727 | 0.597 | 0.745 | 0.698 | 0.712 |
| haiku-4.5 | 470 | 0.523 | 0.341 | 0.268 | 0.665 | 0.425 | 0.448 | 0.502 | 0.459 |

Support per class (per repeat-model slice): ALLOW: 139, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_deny` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u3_no_register` — 17 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u7_trust_only` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 1 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_allow_eu_path` — 3 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny` — 24 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 24 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u3_no_register` — 16 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 13 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_allow_via_db` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_need_user` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u3_no_register` — 10 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 11 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 30 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_need_db` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u3_no_register` — 12 wrong rows (e.g. gemini-2.5-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u7_trust_only` — 20 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 17 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 16 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `personal_data_journalism/journalism_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_deny_no_basis` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u5_need_db` — 9 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `section_120_demo/allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `section_120_demo/db-then-user` — 12 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 11 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 19 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `section_120_demo/unrelated-law` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)

## Errors

3 rows errored:

- `personal_data_journalism/journalism_allow_via_consent` deepseek-v4-flash: RuntimeError: deepseek/deepseek-v4-flash failed after 5 attempts: Request timed out.
- `personal_data_journalism/journalism_allow_via_consent` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u3_no_register` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 939 | 0.0792 |
| gemini-2.5-flash | 936 | 0.4109 |
| gpt-5-mini | 940 | 1.4563 |
| haiku-4.5 | 940 | 1.5918 |

Total: EUR 3.5381.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
