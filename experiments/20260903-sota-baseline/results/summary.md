# 20260903-sota-baseline

Generated 2026-09-04T00:28:49Z — execution `parallel`, condition `baseline`.

**Question:** Does a frontier model close the gap to the architecture without it? LLM-only baseline on the four SOTA models, one repeat (indicative, n=47 per model).


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
| premise_outcome | llm | decide | decide-v1 |  |  |
| outcome_trace | llm | justify | justify-v1 |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-pro | 47 | 0.575 | 0.595 | 0.800 | 0.375 | 0.590 | 0.553 | 0.553 | 0.553 |
| fable-5.1 | 47 | 0.553 | 0.611 | 0.250 | 0.619 | 0.493 | 0.553 | 0.553 | 0.553 |
| gemini-3.1-pro | 47 | 0.723 | 0.667 | 0.783 | 0.723 | 0.724 | 0.553 | 0.553 | 0.553 |
| gpt-5.6-sol | 47 | 0.575 | 0.593 | 0.250 | 0.667 | 0.503 | 0.553 | 0.553 | 0.553 |

Support per class (per repeat-model slice): ALLOW: 14, DENY: 12, NEED_MORE_INFO: 21.

## Failure patterns

- `building_permit/building_permit_deny` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_deny_incompetent` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_deny_no_site_study` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_need_db` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u3_no_register` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u7_trust_only` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_allow_eu_path` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `civil_service_eligibility/civil_service_need_db` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u3_no_register` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_allow_via_db` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 4 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_u3_no_register` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u5_need_db` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u7_trust_only` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 2 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_u7_trust_only` — 4 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_u3_no_register` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u5_need_db` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `section_120_demo/allow` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `section_120_demo/db-then-user` — 1 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 4 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `section_120_demo/unrelated-law` — 1 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 94 | 0.5196 |
| fable-5.1 | 94 | 5.1316 |
| gemini-3.1-pro | 94 | 0.8922 |
| gpt-5.6-sol | 94 | 2.9477 |

Total: EUR 9.4911.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
