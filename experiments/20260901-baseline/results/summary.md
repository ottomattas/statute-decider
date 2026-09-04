# 20260901-baseline

Generated 2026-09-04T18:11:40Z — execution `parallel`, condition `baseline`.

**Question:** Committed run 2 of 3: LLM-only source-to-trace. Raw statute text, utterance, and registry go to the model, which decides and justifies without any intermediate structure. The comparison floor for the candidate.


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
| deepseek-v4-flash | 470 | 0.660 | 0.629 | 0.889 | 0.500 | 0.672 | 0.553 | 0.553 | 0.553 |
| gemini-2.5-flash | 470 | 0.594 | 0.595 | 0.486 | 0.640 | 0.574 | 0.553 | 0.553 | 0.553 |
| gpt-5-mini | 470 | 0.491 | 0.494 | 0.258 | 0.574 | 0.442 | 0.553 | 0.553 | 0.553 |
| haiku-4.5 | 470 | 0.662 | 0.579 | 0.891 | 0.574 | 0.681 | 0.553 | 0.553 | 0.553 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_allow` — 10 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit/building_permit_allow_via_db` — 11 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `building_permit/building_permit_deny` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_deny_incompetent` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_deny_no_site_study` — 20 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `building_permit/building_permit_need_db` — 33 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u3_no_register` — 9 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_allow` — 17 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_allow_eu_path` — 18 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `civil_service_eligibility/civil_service_need_db` — 22 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u3_no_register` — 20 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 25 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_deny` — 12 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` — 14 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != DENY)
- `consumer_withdrawal/consumer_withdrawal_u3_no_register` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u5_need_db` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u7_trust_only` — 40 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_allow` — 9 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_pensioner` — 9 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_allow_via_db` — 10 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `land_tax_exemption/land_tax_deny` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `land_tax_exemption/land_tax_deny_not_residential` — 20 wrong rows (e.g. gemini-2.5-flash: ALLOW != DENY)
- `land_tax_exemption/land_tax_u7_trust_only` — 40 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow` — 15 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_allow_via_consent` — 11 wrong rows (e.g. haiku-4.5: NEED_MORE_INFO != ALLOW)
- `personal_data_journalism/journalism_need_user` — 10 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 30 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u5_need_db` — 38 wrong rows (e.g. deepseek-v4-flash: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u7_trust_only` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `section_120_demo/allow` — 21 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `section_120_demo/db-then-user` — 15 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/deny` — 15 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `section_120_demo/need-db` — 34 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `section_120_demo/unrelated-law` — 20 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 940 | 1.9964 |
| gemini-2.5-flash | 940 | 2.6844 |
| gpt-5-mini | 942 | 3.4053 |
| haiku-4.5 | 942 | 10.0282 |

Total: EUR 18.1142.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
