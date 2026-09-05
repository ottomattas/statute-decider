# 20260906-solver-validation

Generated 2026-09-05T20:47:28Z — execution `sequential`, condition `solver-validation`.

**Question:** After the 2026-09-05 English-only rewrite (Ruling E) and the balanced 18/18/18 suite (Ruling F): do the solver endpoint and the oracle data still agree end to end over all 54 scenarios? Every node oracle/file, decision by z3, trace rendered. No LLM; row 1 of any table.


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
| premise_outcome | solver |  |  | z3 |  |
| outcome_trace | render |  |  |  |  |

## Data

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deterministic | 54 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
