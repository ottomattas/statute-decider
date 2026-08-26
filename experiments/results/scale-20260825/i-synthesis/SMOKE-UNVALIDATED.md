# SMOKE — UNVALIDATED

Generated 2026-08-26T06:15:30Z. Overnight cap EUR 100.00; spent EUR 13.3658; remaining EUR 86.6342.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `scale-2026-08-25-i-synthesis`.
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
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.33 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.15 | no | 0.50 | 2/4 | yes | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.40 | no | 0.50 | 2/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.25 | yes | 1.00 | 4/4 | no | 2 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.15 | no | 0.50 | 2/4 | yes | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.53 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.36 | yes | 1.00 | 4/4 | no | 0 |
| building_permit | synthesis | 0.11 | yes | 1.00 | 2/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.63 | no | 0.97 | 62/64 | no | 0 |
| consumer_withdrawal | synthesis | 0.15 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.31 | no | 0.25 | 1/4 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 2 |
| civil_service_eligibility | synthesis | 0.59 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.15 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.21 | yes | 1.00 | 4/4 | no | 0 |
| personal_data_journalism | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.15 | no | 0.00 | 0/2 | yes | 0 |
| land_tax_exemption | synthesis | 0.12 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| building_permit | synthesis | 0.09 | yes | 1.00 | 2/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.50 | yes | 1.00 | 32/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| personal_data_journalism | synthesis | 0.43 | no | 0.00 | 0/8 | yes | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.17 | no | 0.50 | 1/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.40 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.17 | no | 0.50 | 1/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | yes | 1.00 | 8/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.17 | no | 0.50 | 1/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.40 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.60 | no | 0.50 | 4/8 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | yes | 1.00 | 32/32 | no | 0 |
| consumer_withdrawal | synthesis | 0.17 | yes | 1.00 | 2/2 | no | 0 |
| land_tax_exemption | synthesis | 0.14 | yes | 1.00 | 2/2 | no | 2 |
| personal_data_journalism | synthesis | 0.40 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.13 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| land_tax_exemption | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.44 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.14 | no | 0.50 | 1/2 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.15 | no | 0.00 | 0/2 | no | 0 |
| land_tax_exemption | synthesis | 0.13 | yes | 1.00 | 2/2 | no | 0 |
| personal_data_journalism | synthesis | 0.44 | no | 0.50 | 2/4 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.29 | no | 0.50 | 2/4 | no | 0 |
| land_tax_exemption | synthesis | 0.29 | no | 0.50 | 2/4 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.84 | 27/32 | yes | 6 |
| consumer_withdrawal | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| land_tax_exemption | synthesis | 0.31 | no | 0.50 | 2/4 | no | 0 |
| personal_data_journalism | synthesis | 0.44 | no | 0.25 | 1/4 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| civil_service_eligibility | synthesis | 0.56 | no | 0.91 | 29/32 | yes | 0 |
| consumer_withdrawal | synthesis | 0.31 | no | 0.50 | 2/4 | no | 0 |
| land_tax_exemption | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| personal_data_journalism | synthesis | 0.25 | no | 0.50 | 1/2 | no | 0 |
| building_permit | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |
| section_120_demo | synthesis | 0.00 | no | 0.00 | 0/0 | no | 0 |

## Needs operator audit

- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency_met', 'position_is_estonian_citizen_only', 'has_conviction_for_intentional_state_crime', 'prohibited_from_position_by_court_order', 'is_relative_of_direct_supervisor', 'position_is_not_estonian_citizen_only']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['estonian_language_proficiency_met', 'position_is_estonian_citizen_only', 'has_conviction_for_intentional_state_crime', 'prohibited_from_position_by_court_order', 'is_relative_of_direct_supervisor', 'position_is_not_estonian_citizen_only']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `building_permit`: unmatched gold `['plan_conformant', 'site_study_provided', 'fee_paid', 'plan_violation']`; unmatched pred `['project_meets_detailed_plan', 'project_meets_design_conditions', 'building_meets_special_plan_if_applicable', 'project_meets_construction_requirements', 'project_meets_public_law_restrictions', 'project_prepared_by_competent_person', 'expert_review_performed_by_competent_person', 'project_based_on_survey_results', 'required_survey_completed', 'project_fails_detailed_plan', 'project_fails_design_conditions', 'project_fails_special_plan', 'project_fails_building_requirements', 'project_fails_construction_requirements', 'project_fails_public_law_restrictions', 'expert_review_not_performed', 'project_not_based_on_survey', 'required_survey_missing']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `personal_data_journalism`: unmatched gold `['journalistic_purpose', 'journalism_ethics', 'subject_consent']`; unmatched pred `['request_is_for_journalistic_purpose', 'processing_is_ethical', 'no_excessive_harm_from_disclosure']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['applicant_masters_estonian_language', 'applicant_is_not_estonian_citizen', 'position_is_sensitive', 'position_is_not_sensitive', 'applicant_has_conviction_intentional_crime', 'applicant_deprived_right_to_work', 'current_position_is_restricted_by_court_order', 'applicant_is_relative_of_supervisor']`.
- `building_permit`: unmatched gold `['plan_conformant', 'site_study_provided', 'fee_paid', 'plan_violation']`; unmatched pred `['project_meets_detailed_plan', 'project_meets_design_conditions', 'building_meets_special_plan_if_applicable', 'project_meets_construction_requirements', 'project_meets_public_law_restrictions', 'project_prepared_by_competent_person', 'expert_review_performed_by_competent_person', 'project_based_on_survey_results', 'required_survey_completed', 'project_fails_detailed_plan', 'project_fails_design_conditions', 'project_fails_special_plan', 'project_fails_building_requirements', 'project_fails_construction_requirements', 'project_fails_public_law_restrictions', 'expert_review_not_performed', 'project_not_based_on_survey', 'required_survey_missing']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['is_not_estonian_citizen', 'meets_estonian_language_requirement', 'meets_statutory_requirements_for_non_estonian_citizen', 'position_reserved_for_estonian_citizens', 'convicted_of_intentional_state_crime', 'deprived_by_final_court_of_right_to_work_in_this_office_or_activity', 'prohibited_relative_relation_with_supervisor']`.
- `personal_data_journalism`: unmatched gold `['journalism_ethics', 'subject_consent', 'excessive_harm']`; unmatched pred `['personal_data', 'public_interest_absent', 'aligns_with_journalism_ethics', 'conflicts_with_journalism_ethics', 'disclosure_would_overly_harm_subject', 'disclosure_would_not_overly_harm_subject']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['proficient_in_estonian_required_level', 'position_allows_non_estonian', 'complies_with_additional_legal_requirements', 'convicted_of_intentional_state_crime', 'court_prohibited_from_position_or_field', 'is_close_relative_of_immediate_supervisor_for_position']`.
- `consumer_withdrawal`: unmatched gold `['is_consumer', 'excluded_category', 'within_14_days', 'notice_sent_in_time']`; unmatched pred `['is_distance_contract', 'withdrawal_notice_sent_within_14_days_and_valid', 'service_or_ongoing_performance_fully_performed_exception', 'good_made_for_consumer_personal_needs', 'good_made_according_to_consumer_specifications', 'perishable_good', 'sealed_hygiene_good_opened_after_delivery']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['lacks_full_legal_capacity', 'speaks_estonian_as_required_by_law', 'eu_meets_statutory_requirements', 'conviction_intentional_treason', 'court_prohibition_for_post_or_field', 'position_restricted_to_estonian_citizens', 'is_non_estonian_citizen', 'is_close_relative_of_supervising_officer']`.
- `personal_data_journalism`: unmatched gold `['subject_consent', 'excessive_harm']`; unmatched pred `['is_personal_data', 'purpose_not_journalistic', 'public_interest_absent', 'ethics_violation', 'not_unduly_harmful', 'unduly_harmful']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_requires_estonian_citizenship', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_close_relative_in_supervisory_chain']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_requires_estonian_citizenship', 'no_intentional_crime_against_state_conviction', 'no_court_restriction_on_position', 'no_family_relationship_with_supervisor']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_restricted_to_estonian_citizens', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_family_relationship_with_supervisor']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_restricted_to_estonian_citizens', 'no_conviction_for_intentional_crime_against_state', 'no_court_order_restricting_position', 'no_close_relative_supervising']`.
- `civil_service_eligibility`: unmatched gold `['speaks_estonian', 'no_conflict_declared']`; unmatched pred `['meets_estonian_language_requirement', 'meets_eu_citizen_requirements', 'position_requires_estonian_citizenship', 'no_conviction_for_intentional_crime_against_state', 'no_court_restriction_on_position', 'no_close_relative_in_supervisory_chain']`.

Mean alignment F1: 0.218 (n=120).

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).
