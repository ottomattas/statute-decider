# 20260901-llm-only-smoke

Generated 2026-09-05T21:24:46Z — execution `parallel`, condition `llm-only`.

**Question:** Smoke: do all four providers return parseable decide + justify responses under the llm-only condition on one case?


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
| premise_outcome | llm | decide | decide-raw-sources |  |  |
| outcome_trace | llm | justify | justify-v1 |  |  |

## Data

7 scenarios across 1 cases: child_representation_by_one_parent.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 7 | 0.286 | 0.000 | 0.500 | 0.286 | 0.262 | 0.571 | 0.571 | 0.571 |
| gemini-2.5-flash | 6 | 0.667 | 1.000 | 0.000 | 0.667 | 0.556 | 0.500 | 0.500 | 0.500 |
| gpt-5-mini | 2 | 1.000 | 1.000 | 0.000 | 1.000 | 0.667 | 0.500 | 0.500 | 0.500 |
| haiku-4.5 | 7 | 0.429 | 0.000 | 0.667 | 0.500 | 0.389 | 0.571 | 0.571 | 0.571 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 1, NEED_MORE_INFO: 3.

## Failure patterns

- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — 2 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — 2 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/allow_claims_verified_emergency` — 2 wrong rows (e.g. deepseek-v4-flash: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 1 wrong rows (e.g. gemini-2.5-flash: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — 3 wrong rows (e.g. deepseek-v4-flash: DENY != NEED_MORE_INFO)

## Errors

6 rows errored:

- `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` gpt-5-mini: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.1781).
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` gpt-5-mini: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.1781).
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` gpt-5-mini: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.1781).
- `child_representation_by_one_parent/deny_own_admission_not_parent` gpt-5-mini: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.1922).
- `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` gemini-2.5-flash: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.2078).
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` gpt-5-mini: BudgetExceeded: Budget cap EUR 1.00 reached (spent 1.2705).

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 28 | 0.3543 |
| gemini-2.5-flash | 26 | 0.4040 |
| gpt-5-mini | 20 | 0.2705 |
| haiku-4.5 | 14 | 0.8379 |

Total: EUR 1.8668.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
