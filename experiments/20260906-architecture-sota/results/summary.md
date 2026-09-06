# 20260906-architecture-sota

Generated 2026-09-06T15:18:22Z — execution `parallel`, condition `architecture`.

**Question:** Does a frontier model change the architecture's result? SOTA x 1, indicative.

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
| premise_outcome | solver |  |  | z3 |  |
| outcome_trace | render |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-pro | 54 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| fable-5.1 | 54 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.994 |
| gemini-3.1-pro | 54 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.994 |
| gpt-5.6-sol | 54 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.994 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 54 | 0.0459 |
| fable-5.1 | 54 | 0.8891 |
| gemini-3.1-pro | 54 | 0.0983 |
| gpt-5.6-sol | 54 | 0.2367 |

Total: EUR 1.2700.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
