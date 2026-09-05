# 20260906-llm-only-smoke

Generated 2026-09-05T23:20:17Z — execution `parallel`, condition `llm-only`.

**Question:** Smoke after Rulings H and J: does every configured provider return one parseable single-call decide
response {steps, outcome, missing_terms, justification} under the llm-only condition on one scenario?


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

1 scenarios across 1 cases: land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 1 | 1.000 | 0.000 | 0.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 |
| gemini-2.5-flash | 1 | 1.000 | 0.000 | 0.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 |
| gpt-5-mini | 1 | 1.000 | 0.000 | 0.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 |
| haiku-4.5 | 1 | 1.000 | 0.000 | 0.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 |

Support per class (per repeat-model slice): ALLOW: 0, DENY: 0, NEED_MORE_INFO: 1.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 1 | 0.0016 |
| gemini-2.5-flash | 1 | 0.0030 |
| gpt-5-mini | 1 | 0.0040 |
| haiku-4.5 | 1 | 0.0117 |

Total: EUR 0.0203.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
