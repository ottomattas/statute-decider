# 20260901-smoke-candidate

Generated 2026-09-01T20:04:25Z — execution `parallel`, condition `candidate`.

**Question:** Smoke: do all four providers return parseable fused ground responses under the candidate condition on one case?


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

7 scenarios across 1 cases: section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemini-2.5-flash | 7 | 0.857 | 0.800 | 0.667 | 1.000 | 0.822 | 1.000 | 1.000 | 1.000 |
| gpt-5-mini | 7 | 0.857 | 1.000 | 0.667 | 0.800 | 0.822 | 0.857 | 0.857 | 0.857 |
| haiku-4.5 | 7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Failure patterns

- `section_120_demo/need-db` — 1 wrong rows (e.g. gpt-5-mini: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 1 wrong rows (e.g. gemini-2.5-flash: DENY != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 7 | 0.0011 |
| gemini-2.5-flash | 7 | 0.0027 |
| gpt-5-mini | 7 | 0.0097 |
| haiku-4.5 | 7 | 0.0083 |

Total: EUR 0.0217.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
