# 20260906-llm-only-cache-dry-run-warm

Generated 2026-09-05T23:24:56Z — execution `parallel`, condition `llm-only`.

**Question:** With the per-(model, statute) warm-up gate in the parallel runner (first call of a cache group runs
alone, the rest fan out after it), what share of the prompt is served from the vendor cache on a cold
prefix? gpt-5-mini, llm-only, every scenario of the Personal Data Protection Act case (~20k tokens).


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

11 scenarios across 1 cases: journalistic_data_disclosure.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| gpt-5-mini | 11 | 0.545 | 0.545 | 0.800 | 0.333 | 0.560 | 0.636 | 0.636 | 0.636 |

Support per class (per repeat-model slice): ALLOW: 4, DENY: 3, NEED_MORE_INFO: 4.

## Failure patterns

- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 1 wrong rows (e.g. gpt-5-mini: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 1 wrong rows (e.g. gpt-5-mini: ALLOW != NEED_MORE_INFO)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| gpt-5-mini | 11 | 0.0256 |

Total: EUR 0.0256.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
