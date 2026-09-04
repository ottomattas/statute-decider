# 20260901-candidate

Generated 2026-09-04T18:13:48Z — execution `parallel`, condition `candidate`.

**Question:** Committed run 3 of 3: the proposed architecture. Statute chain oracle, user chain fused LLM grounding (utterance_term + term_claim in one call), register chain deterministic lookup, decision by z3, trace rendered.


## Bound matrix rows

| node | method | strategy | prompt | solver | fused |
|---|---|---|---|---|---|
| statute_text | file |  |  |  |  |
| text_term | oracle |  |  |  |  |
| term_rule | oracle |  |  |  |  |
| user_utterance | file |  |  |  |  |
| utterance_term | llm | ground | ground-v1 |  | yes |
| term_claim | llm |  |  |  | yes |
| registry_record | file |  |  |  |  |
| record_term | oracle |  |  |  |  |
| term_fact | lookup |  |  |  |  |
| premise_outcome | solver |  |  | z3 |  |
| outcome_trace | render |  |  |  |  |

Fuse pairs: [['utterance_term', 'term_claim']]; logic `propositional`; loop `off`.

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-flash | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemini-2.5-flash | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gpt-5-mini | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 0.997 |
| haiku-4.5 | 470 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 140, DENY: 120, NEED_MORE_INFO: 210.

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-flash | 1010 | 0.1977 |
| gemini-2.5-flash | 970 | 0.4519 |
| gpt-5-mini | 947 | 1.4012 |
| haiku-4.5 | 1006 | 1.4643 |

Total: EUR 3.5151.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
