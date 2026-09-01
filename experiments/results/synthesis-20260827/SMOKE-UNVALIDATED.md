# SMOKE — UNVALIDATED

Generated 2026-08-28T06:01:52Z. Overnight cap EUR 18.36; spent EUR 14.6611; remaining EUR 3.6989.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `synthesis-2026-08-27-persisted`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: gemini, openai, anthropic, deepseek.
Providers skipped (missing key or stub): —.

### Experiment (ii) — runtime (solver)

- n scored: 0 / 0
- outcome accuracy: 0.000
- ALLOW accuracy: —
- DENY accuracy: —
- NEED_MORE_INFO accuracy: —
- mean missing-fact P/R: 0.000 / 0.000
- macro missing-fact P/R: 0.000 / 0.000

### Experiment (ii) — LLM-only

_No LLM rows (no keys, skipped, or runtime-only)._

### Experiment (i) — encoding

# Experiment (i) — synthesis extraction vs gold encoding

Catalog-held-out boolean synthesis scored by lexical claim alignment and truth-table paper-outcome equivalence. Selection-mode ablation scores catalog-id F1 via existing `llm.extract_domain_artifact`.

| case | condition | align F1 | equivalent | rate | n_agree/n_rows | audit | dropped rules |
| --- | --- | --- | --- | --- | --- | --- | --- |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.33 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.33 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.33 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.33 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.15 | no | 0.50 | 2/4 | yes | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.45 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.11 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.50 | no | 0.12 | 1/8 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.53 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.31 | yes | 1.00 | 4/4 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.31 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.53 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.11 | no | 0.00 | 0/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.63 | no | 0.97 | 62/64 | no | 0 |
| consumer_withdrawal | synthesis | 0.31 | yes | 1.00 | 4/4 | yes | 0 |
| land_tax_exemption | synthesis | 0.24 | no | 0.50 | 2/4 | no | 0 |
| personal_data_journalism | synthesis | 0.15 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 1 |
| civil_service_eligibility | synthesis | 0.40 | yes | 1.00 | 16/16 | yes | 0 |
| consumer_withdrawal | synthesis | 0.29 | no | 0.75 | 3/4 | yes | 0 |
| land_tax_exemption | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| personal_data_journalism | synthesis | 0.36 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.09 | yes | 1.00 | 2/2 | no | 2 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.17 | no | 0.50 | 1/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | yes | 1.00 | 8/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.17 | no | 0.50 | 1/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.80 | no | 0.44 | 7/16 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | yes | 1.00 | 8/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | yes | 1.00 | 8/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 2 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | no | 0.38 | 3/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.15 | no | 0.00 | 0/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.48 | no | 0.78 | 25/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.31 | no | 0.50 | 2/4 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.31 | no | 0.00 | 0/4 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.84 | 27/32 | yes | 6 |
| consumer_withdrawal | synthesis | 0.31 | no | 0.00 | 0/4 | no | 0 |
| land_tax_exemption | synthesis | 0.27 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.44 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.84 | 27/32 | yes | 6 |
| consumer_withdrawal | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.44 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |

## Needs operator audit

- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency_met', 'position_is_estonian_citizen_only', 'has_conviction_for_intentional_state_crime', 'prohibited_from_position_by_court_order', 'is_relative_of_direct_supervisor', 'position_is_not_estonian_citizen_only']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency_met', 'position_is_estonian_citizen_only', 'has_conviction_for_intentional_state_crime', 'prohibited_from_position_by_court_order', 'is_relative_of_direct_supervisor', 'position_is_not_estonian_citizen_only']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `building_permit`: unmatched gold `['plan_conformant', 'site_study_provided', 'fee_paid', 'plan_violation']`; unmatched pred `['project_meets_detailed_plan', 'project_meets_design_conditions', 'building_meets_special_plan_if_applicable', 'project_meets_construction_requirements', 'project_meets_public_law_restrictions', 'project_prepared_by_competent_person', 'expert_review_performed_by_competent_person', 'project_based_on_survey_results', 'required_survey_completed', 'project_fails_detailed_plan', 'project_fails_design_conditions', 'project_fails_special_plan', 'project_fails_building_requirements', 'project_fails_construction_requirements', 'project_fails_public_law_restrictions', 'expert_review_not_performed', 'project_not_based_on_survey', 'required_survey_missing']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['proficient_in_estonian_by_statute', 'meets_additional_statutory_requirements', 'position_restricted_to_estonian_citizens', 'applicant_is_non_estonian', 'punished_for_intentional_treason', 'court_ban_from_position_or_activity', 'close_relative_of_controlling_official']`.
- `consumer_withdrawal`: unmatched gold `['is_consumer', 'excluded_category', 'notice_sent_in_time']`; unmatched pred `['withdrawal_notice_not_sent_within_14_days', 'entrepreneur_obligations_fully_performed', 'item_custom_or_made_to_consumer_spec', 'item_spoils_or_ages_quickly', 'sealed_hygiene_not_returnable_and_opened_after_delivery', 'no_listed_exception_applies']`.
- `civil_service_eligibility`: unmatched gold `['secondary_education', 'speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_has_min_secondary_education', 'applicant_masters_estonian_language', 'eu_national_meets_statutory_requirements', 'position_is_restricted_to_estonian_citizens', 'position_is_not_restricted_to_estonian_citizens', 'applicant_punished_for_treason', 'applicant_deprived_by_court_for_position', 'applicant_is_close_relative_of_controlling_official', 'applicant_not_estonian_citizen']`.
- `consumer_withdrawal`: unmatched gold `['is_consumer', 'excluded_category', 'notice_sent_in_time']`; unmatched pred `['contract_is_not_distance_contract', 'withdrawal_notice_not_sent_within_14_days', 'service_or_ongoing_performance', 'entrepreneur_fulfilled_all_obligations', 'goods_custom_made_or_personal_needs', 'goods_perishable_or_rapidly_deteriorating', 'sealed_hygiene_good_opened_after_delivery']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'sensitive_position', 'rights_restriction_position']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'is_sensitive_position', 'meets_general_requirements']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'is_sensitive_position', 'meets_general_requirements']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'sensitive_position', 'meets_general_requirements']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency', 'conviction_state_crime', 'court_ban_position', 'family_conflict_of_interest', 'sensitive_position', 'meets_general_requirements']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_requires_estonian_citizenship', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_family_relationship_with_supervisor']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_restricted_to_estonian_citizens', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_close_relative_supervises', 'is_estonian_or_eu_citizen', 'meets_general_requirements', 'no_disqualifying_factors']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_other_legal_requirements', 'position_requires_estonian_citizenship', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_family_relationship_with_supervisor']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_requires_estonian_citizenship', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_close_relative_in_supervisory_chain']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_other_legal_requirements', 'position_restricted_to_estonian_citizens', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_family_relationship_with_supervisor']`.

Mean alignment F1: 0.228 (n=120).

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).
