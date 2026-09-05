# 20260903-llm-decides-on-llm-claims-partial-specification-smoke

Generated 2026-09-05T22:04:46Z — execution `parallel`, condition `llm-decides-on-llm-claims-partial-specification`.

**Question:** Plumbing smoke for condition llm-decides-on-llm-claims-partial-specification (one case, one model, one repeat).

## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | llm | ground | ground |  | yes |
| term_claim | llm |  |  |  | yes |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | llm | decide | solver-inputs-partial-specification |  |  |
| outcome_trace | skip |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

7 scenarios across 1 cases: child_representation_by_one_parent.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 0.571 | 1.000 | 0.400 | 0.000 | 0.467 | 0.571 | 0.571 | 0.571 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Failure patterns

- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 14 | 0.0032 |

Total: EUR 0.0032.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
