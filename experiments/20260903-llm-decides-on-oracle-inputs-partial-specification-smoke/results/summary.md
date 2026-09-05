# 20260903-llm-decides-on-oracle-inputs-partial-specification-smoke

Generated 2026-09-05T21:24:46Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-partial-specification`.

**Question:** Plumbing smoke for condition llm-decides-on-oracle-inputs-partial-specification (one case, one model, one repeat).

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
| premise_outcome | llm | decide | solver-inputs-partial-specification |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

7 scenarios across 1 cases: child_representation_by_one_parent.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 0.143 | 0.000 | 0.250 | 0.000 | 0.083 | 0.571 | 0.571 | 0.571 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Failure patterns

- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != ALLOW)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 14 | 0.0049 |

Total: EUR 0.0049.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
