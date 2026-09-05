# 20260904-llm-as-solver-v2

Generated 2026-09-05T06:27:28Z — execution `parallel`, condition `llm-as-solver-v2`.

**Question:** LLM-as-solver with the solver's staged precedence rule stated (solver-inputs-v2). v1 misses on 3 Sep were 100% on the 13 claim/fact-conflict scenarios for the strong models.


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
| premise_outcome | llm | decide | solver-inputs-v2 |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.628 | 0.678 | 0.516 | 0.671 | 0.622 | 0.779 | 0.762 | 0.767 |
| gemini-2.5-flash | 470 | 0.983 | 0.971 | 1.000 | 0.981 | 0.984 | 0.983 | 0.967 | 0.973 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.985 | 0.991 |
| haiku-4.5 | 470 | 0.651 | 0.628 | 0.462 | 0.742 | 0.611 | 0.695 | 0.662 | 0.665 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_deny` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_incompetent` — 13 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_deny_no_site_study` — 20 wrong rows (e.g. deepseek-v4-flash: ALLOW != DENY)
- `building_permit/building_permit_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_allow_eu_path` — 18 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 20 wrong rows (e.g. haiku-4.5: ALLOW != DENY)
- `civil_service_eligibility/civil_service_need_db` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `consumer_withdrawal/consumer_withdrawal_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 18 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 7 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 4 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `land_tax_exemption/land_tax_u7_trust_only` — 20 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 20 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `personal_data_journalism/journalism_deny` — 5 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_deny_no_basis` — 10 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `personal_data_journalism/journalism_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 14 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `section_120_demo/allow` — 1 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `section_120_demo/db-then-user` — 15 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `section_120_demo/need-db` — 12 wrong rows (e.g. haiku-4.5: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 10 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 3 wrong rows (e.g. haiku-4.5: DENY != ALLOW)
- `section_120_demo/unrelated-law` — 2 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)

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
