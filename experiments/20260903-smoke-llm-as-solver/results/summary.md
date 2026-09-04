# 20260903-smoke-llm-as-solver

Generated 2026-09-03T19:44:20Z — execution `parallel`, condition `llm-as-solver`.

**Question:** Plumbing smoke for condition llm-as-solver (one case, one model, one repeat).

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

7 scenarios across 1 cases: section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 0.143 | 0.000 | 0.250 | 0.000 | 0.083 | 0.571 | 0.571 | 0.571 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Failure patterns

- `section_120_demo/allow` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `section_120_demo/db-then-user` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-db` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `section_120_demo/unrelated-law` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 14 | 0.0049 |

Total: EUR 0.0049.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
