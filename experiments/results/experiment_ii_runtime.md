# Experiment (ii) runtime — SMOKE — UNVALIDATED

| scenario | condition | expected | actual | match | P | R | missing_facts |
|----------|-----------|----------|--------|-------|---|---|----------------|
| civil_service_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity, secondary_education, speaks_estonian |
| civil_service_u8_need_user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | runtime | ALLOW | ALLOW | YES | 0.00 | 1.00 | distance_contract, is_consumer |
| consumer_withdrawal_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | notice_sent_in_time, within_14_days |
| consumer_withdrawal_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | distance_contract, is_consumer |
| consumer_withdrawal_u5_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | distance_contract, is_consumer |
| land_tax_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | runtime | ALLOW | ALLOW | YES | 0.00 | 1.00 | applicant_is_owner, primary_residence_registered, receives_pension, residential_land |
| land_tax_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | applicant_is_owner, municipality_exemption_set, primary_residence_registered, residential_land |
| journalism_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalism_ethics, public_interest |
| journalism_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| building_permit_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | runtime | ALLOW | ALLOW | YES | 0.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided |
| building_permit_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | fee_paid |
| building_permit_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | fee_paid |
| building_permit_u7_trust_only | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided |
| allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| need-user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
