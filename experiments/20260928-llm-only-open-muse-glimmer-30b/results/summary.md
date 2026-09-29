# 20260928-llm-only-open-muse-glimmer-30b

Generated 2026-09-28T22:24:04Z — execution `parallel`, condition `llm-only`.

**Question:** Does a self-hosted open-weight model close the gap to the architecture without it? LLM-only single call, open x 1, indicative.

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

54 scenarios across 6 cases: building_permit_grant, child_representation_by_one_parent, civil_service_admission, consumer_purchase_withdrawal, journalistic_data_disclosure, land_tax_home_exemption.

## Outcomes (three-way scored)

| group | n | acc | F1 ALLOW | F1 DENY | F1 NEED_MORE_INFO | macro F1 | missing P | missing R | missing F1 |
|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b@taltech-hpc | 54 | 0.574 | 0.550 | 0.444 | 0.683 | 0.559 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

## Failure patterns

- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `building_permit_grant/unverifiable_register_down_payment_ledger` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != NEED_MORE_INFO)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: DENY != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != DENY)
- `civil_service_admission/allow_claims_verified` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: DENY != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: DENY != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 1 wrong rows (e.g. muse-glimmer-30b@taltech-hpc: ALLOW != DENY)

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| muse-glimmer-30b@taltech-hpc | 54 | 0.0000 |

Total: EUR 0.0000.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
