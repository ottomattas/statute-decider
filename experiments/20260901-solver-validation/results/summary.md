# 20260901-solver-validation

Generated 2026-09-01T19:51:04Z — execution `sequential`, condition `solver-validation`.

**Question:** Do the solver endpoint and the oracle data agree end to end? Every node oracle/file, decision by z3, trace rendered. No LLM; row 1 of any table.


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

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deterministic | 47 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 14, DENY: 12, NEED_MORE_INFO: 21.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
