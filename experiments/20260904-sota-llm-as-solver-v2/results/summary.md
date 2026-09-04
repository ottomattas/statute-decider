# 20260904-sota-llm-as-solver-v2

Generated 2026-09-04T04:56:54Z — execution `parallel`, condition `llm-as-solver-v2`.

**Question:** SOTA models as solver with the full staged specification (solver-inputs-v2), 3 repeats.

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
| premise_outcome | llm | decide | solver-inputs-v2 |  |  |
| outcome_trace | skip |  |  |  |  |

## Data

47 scenarios across 6 cases: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-pro | 141 | 0.752 | 0.741 | 0.652 | 0.844 | 0.746 | 0.879 | 0.844 | 0.856 |
| fable-5.1 | 141 | 0.972 | 0.950 | 1.000 | 0.969 | 0.973 | 0.972 | 0.972 | 0.972 |
| gemini-3.1-pro | 141 | 0.957 | 0.923 | 1.000 | 0.955 | 0.959 | 0.957 | 0.957 | 0.957 |
| gpt-5.6-sol | 141 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Support per class (per repeat-model slice): ALLOW: 42, DENY: 36, NEED_MORE_INFO: 63.

## Failure patterns

- `building_permit/building_permit_deny_no_site_study` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_eligibility/civil_service_allow_eu_path` — 5 wrong rows (e.g. fable-5.1: NEED_MORE_INFO != ALLOW)
- `civil_service_eligibility/civil_service_deny_no_citizenship` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_eligibility/civil_service_need_db` — 2 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_eligibility/civil_service_u8_need_user` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `land_tax_exemption/land_tax_u7_trust_only` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `personal_data_journalism/journalism_allow_via_consent` — 8 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `section_120_demo/allow` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `section_120_demo/db-then-user` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/need-db` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/need-user` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `section_120_demo/prompt-swap` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `section_120_demo/unrelated-law` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 141 | 0.1044 |
| fable-5.1 | 141 | 5.0912 |
| gemini-3.1-pro | 141 | 0.4635 |
| gpt-5.6-sol | 141 | 0.6840 |

Total: EUR 6.3431.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
