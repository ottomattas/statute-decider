# 20260903-smoke-candidate-staged

Generated 2026-09-03T19:42:31Z — execution `parallel`, condition `candidate-staged`.

**Question:** Plumbing smoke for condition candidate-staged (one case, one model, one repeat).

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

7 scenarios across 1 cases: section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 14 | 0.0020 |

Total: EUR 0.0020.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
