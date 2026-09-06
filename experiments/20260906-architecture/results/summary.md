# 20260906-architecture

Generated 2026-09-06T12:51:34Z — execution `parallel`, condition `architecture`.

**Question:** Does the proposed architecture (LLM claim extraction + solver on the oracle rules) reproduce the gold on the balanced suite, and how stable is it over repeats? Cheap grid x 10.

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
| deepseek-v4-flash | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemini-2.5-flash | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.994 |
| gpt-5-mini | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0.994 |
| haiku-4.5 | 540 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 180, DENY: 180, NEED_MORE_INFO: 180.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 540 | 0.0467 |
| gemini-2.5-flash | 540 | 0.2325 |
| gpt-5-mini | 540 | 0.6643 |
| haiku-4.5 | 540 | 0.6977 |

Total: EUR 1.6412.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
