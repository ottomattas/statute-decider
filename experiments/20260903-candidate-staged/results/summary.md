# 20260903-candidate-staged

Generated 2026-09-04T00:17:35Z — execution `parallel`, condition `candidate-staged`.

**Question:** Candidate with grounding staged in two calls (recognize, then value): does splitting recognition from valuation change term recall / claim accuracy / outcome?


## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | llm | ground | ground-v1 |  |  |
| term_claim | llm |  | value-v1 |  |  |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | solver |  |  | z3 |  |
| outcome_trace | render |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemini-2.5-flash | 468 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| haiku-4.5 | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Errors

2 rows errored:

- `personal_data_journalism/journalism_allow` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)
- `personal_data_journalism/journalism_u5_need_db` gemini-2.5-flash: RuntimeError: google/gemini-2.5-flash failed after 5 attempts: Unterminated string starting at: line 1 column 314 (char 313)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 940 | 0.0924 |
| gemini-2.5-flash | 936 | 0.4107 |
| gpt-5-mini | 940 | 1.3110 |
| haiku-4.5 | 940 | 1.2943 |

Total: EUR 3.1084.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
