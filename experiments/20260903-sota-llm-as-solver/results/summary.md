# 20260903-sota-llm-as-solver

Generated 2026-09-04T00:21:33Z — execution `parallel`, condition `llm-as-solver`.

**Question:** Do frontier models play solver correctly on identical inputs (oracle rules, oracle claims, looked-up facts with warrant, no statute text)? Three repeats.


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
| deepseek-v4-pro | 141 | 0.652 | 0.638 | 0.421 | 0.821 | 0.627 | 0.858 | 0.807 | 0.821 |
| fable-5.1 | 141 | 0.745 | 0.703 | 0.143 | 0.977 | 0.607 | 0.979 | 0.943 | 0.953 |
| gemini-3.1-pro | 141 | 0.745 | 0.703 | 0.143 | 0.977 | 0.607 | 0.979 | 0.943 | 0.953 |
| gpt-5.6-sol | 141 | 0.766 | 0.722 | 0.267 | 0.977 | 0.655 | 0.979 | 0.943 | 0.953 |

Support per class (per repeat-model slice): ALLOW: 42, DENY: 36, NEED_MORE_INFO: 63.

## Failure patterns

- `building_permit/building_permit_deny` — 9 wrong rows (e.g. fable-5.1: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_deny` — 8 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_eligibility/civil_service_u8_need_user` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_deny` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 12 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `land_tax_exemption/land_tax_deny` — 9 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 10 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_u7_trust_only` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow_via_consent` — 12 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `personal_data_journalism/journalism_deny_no_basis` — 11 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != DENY)
- `section_120_demo/allow` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `section_120_demo/db-then-user` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 9 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `section_120_demo/unrelated-law` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 141 | 0.1009 |
| fable-5.1 | 141 | 4.1342 |
| gemini-3.1-pro | 141 | 0.3958 |
| gpt-5.6-sol | 141 | 0.5929 |

Total: EUR 5.2239.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
