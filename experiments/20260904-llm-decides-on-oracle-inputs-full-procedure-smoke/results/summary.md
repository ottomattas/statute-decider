# 20260904-llm-decides-on-oracle-inputs-full-procedure-smoke

Generated 2026-09-05T17:46:56Z — execution `parallel`, condition `llm-decides-on-oracle-inputs-full-procedure`.

**Question:** Does stating the staged precedence rule remove the conflict-scenario misses? gpt-5-mini, 1 repeat.

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
| premise_outcome | llm | decide | solver-inputs-full-procedure |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| gpt-5-mini | 47 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.985 | 0.991 |

Support per class (per repeat-model slice): ALLOW: 14, DENY: 12, NEED_MORE_INFO: 21.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| gpt-5-mini | 47 | 0.0939 |

Total: EUR 0.0939.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
