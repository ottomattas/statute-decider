# 20260906-llm-only-cache-dry-run

Generated 2026-09-05T23:21:46Z — execution `parallel`, condition `llm-only`.

**Question:** What share of the statute prefix is actually served from the vendor prompt cache when the parallel
runner orders one act's scenarios as the real grid would? gpt-5-mini, llm-only, every scenario of the
Civil Service Act case (whole act, ~46k tokens), one repeat.


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
| outcome_trace | passthrough |  |  |  |  |

## Data

9 scenarios across 1 cases: civil_service_admission.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| gpt-5-mini | 9 | 0.667 | 0.667 | 0.000 | 1.000 | 0.556 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 3, DENY: 3, NEED_MORE_INFO: 3.

## Failure patterns

- `civil_service_admission/deny_no_allow_path_no_citizenship` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| gpt-5-mini | 9 | 0.0489 |

Total: EUR 0.0489.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
