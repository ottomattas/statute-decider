# 20260906-llm-only-sota

Generated 2026-09-06T16:18:55Z — execution `parallel`, condition `llm-only`.

**Question:** Does a frontier model close the gap to the architecture without it? LLM-only single call, SOTA x 1, indicative.

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
| deepseek-v4-pro | 54 | 0.833 | 0.842 | 0.833 | 0.824 | 0.833 | 0.667 | 0.667 | 0.667 |
| fable-5.1 | 3 | 0.667 | 0.000 | 0.667 | 0.667 | 0.445 | 0.667 | 0.667 | 0.667 |
| gemini-3.1-pro | 54 | 0.611 | 0.467 | 0.645 | 0.681 | 0.598 | 0.667 | 0.667 | 0.667 |
| gpt-5.6-sol | 54 | 0.611 | 0.647 | 0.462 | 0.667 | 0.592 | 0.667 | 0.667 | 0.667 |

Support per class (per repeat-model slice): ALLOW: 18, DENY: 18, NEED_MORE_INFO: 18.

## Failure patterns

- `building_permit_grant/allow_register_only` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/allow_register_only_design_conformity` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `building_permit_grant/deny_no_allow_path_designer_not_competent` — 2 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `building_permit_grant/deny_own_admission_plan_violation` — 3 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` — 3 wrong rows (e.g. deepseek-v4-pro: NEED_MORE_INFO != ALLOW)
- `child_representation_by_one_parent/deny_own_admission_not_parent` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/deny_register_only_not_parent` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `child_representation_by_one_parent/need_register_silent_custody_record` — 1 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` — 1 wrong rows (e.g. deepseek-v4-pro: DENY != NEED_MORE_INFO)
- `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_claims_verified` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/allow_register_only_citizenship` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `civil_service_admission/deny_no_allow_path_no_citizenship` — 2 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `civil_service_admission/deny_no_allow_path_no_estonian_language` — 2 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_admission/deny_own_admission_conviction` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != DENY)
- `civil_service_admission/need_register_silent_citizenship` — 2 wrong rows (e.g. gpt-5.6-sol: DENY != NEED_MORE_INFO)
- `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` — 2 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `consumer_purchase_withdrawal/deny_own_admission_custom_goods` — 1 wrong rows (e.g. gpt-5.6-sol: ALLOW != DENY)
- `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` — 1 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` — 3 wrong rows (e.g. deepseek-v4-pro: DENY != ALLOW)
- `journalistic_data_disclosure/allow_claims_verified` — 1 wrong rows (e.g. gemini-3.1-pro: NEED_MORE_INFO != ALLOW)
- `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `journalistic_data_disclosure/need_register_silent_purpose_and_consent` — 3 wrong rows (e.g. deepseek-v4-pro: ALLOW != NEED_MORE_INFO)
- `land_tax_home_exemption/allow_claims_verified` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/allow_register_only_ownership_and_residence` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != ALLOW)
- `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` — 1 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_no_allow_path_not_residential` — 2 wrong rows (e.g. gpt-5.6-sol: NEED_MORE_INFO != DENY)
- `land_tax_home_exemption/deny_own_admission_not_owner` — 1 wrong rows (e.g. gemini-3.1-pro: ALLOW != DENY)

## Errors

8 rows errored:

- `building_permit_grant/deny_no_allow_path_designer_not_competent` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `building_permit_grant/allow_claims_verified` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `building_permit_grant/allow_register_only_design_conformity` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `building_permit_grant/allow_register_only` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `building_permit_grant/unverifiable_register_down_payment_ledger` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `building_permit_grant/unverifiable_trust_only_designer_selfreport` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response.
- `child_representation_by_one_parent/allow_claims_verified_emergency` fable-5.1: RuntimeError: anthropic/fable-5.1 failed after 5 attempts: Empty model response. [stop_reason=refusal stop_details=RefusalStopDetails(category='reasoning_extraction', explanation="This request was blocked as it seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs. To learn more, visit https://www.anthropic.com/legal/commercial-terms. API integrators: you can reduce refusals for your users by configuring a fallback model — see https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback", type='refusal') blocks=[] output_tokens=0]

## Cost (ledger)

| model | calls | EUR |
|---|---|---|
| deepseek-v4-pro | 54 | 0.6792 |
| fable-5.1 | 5 | 2.5024 |
| gemini-3.1-pro | 54 | 1.4079 |
| gpt-5.6-sol | 54 | 6.1010 |

Total: EUR 10.6906.

---
Rows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.
