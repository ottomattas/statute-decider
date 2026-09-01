# 20260901-candidate

Generated 2026-09-01T20:30:21Z — execution `parallel`, condition `candidate`.

**Question:** Committed run 3 of 3: the proposed architecture. Statute chain oracle, user chain fused LLM grounding (utterance_term + term_claim in one call), register chain deterministic lookup, decision by z3, trace rendered.


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
| premise_outcome | solver |  |  | z3 |  |
| outcome_trace | render |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 0.660 | 0.636 | 1.000 | 0.385 | 0.674 | 0.660 | 0.660 | 0.660 |
| gemini-2.5-flash | 464 | 0.664 | 0.639 | 1.000 | 0.391 | 0.676 | 0.664 | 0.664 | 0.664 |
| gpt-5-mini | 470 | 0.660 | 0.636 | 1.000 | 0.385 | 0.674 | 0.660 | 0.660 | 0.660 |
| haiku-4.5 | 470 | 0.660 | 0.636 | 1.000 | 0.385 | 0.674 | 0.660 | 0.660 | 0.660 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Failure patterns

- `building_permit/building_permit_need_db` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u3_no_register` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `building_permit/building_permit_u7_trust_only` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_need_db` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u3_no_register` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u7_trust_only` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u3_no_register` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u5_need_db` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `consumer_withdrawal/consumer_withdrawal_u7_trust_only` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u3_no_register` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u7_trust_only` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_need_user` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u3_no_register` — 40 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u5_need_db` — 37 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)
- `personal_data_journalism/journalism_u7_trust_only` — 39 wrong rows (e.g. haiku-4.5: ALLOW != NEED_MORE_INFO)

## Errors

6 rows errored:

- `personal_data_journalism/journalism_allow` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_allow_via_consent` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u5_need_db` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u5_need_db` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u5_need_db` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u7_trust_only` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 3 attempts: Unterminated string starting at: line 1 column 314 (char 313)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.1059 |
| gemini-2.5-flash | 500 | 0.2343 |
| gpt-5-mini | 477 | 0.7102 |
| haiku-4.5 | 536 | 0.7824 |

Total: EUR 1.8328.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
