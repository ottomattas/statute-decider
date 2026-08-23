# Experiment (ii) paired — SMOKE — UNVALIDATED

| scenario | expected | runtime | llm | rt match | llm match | P_rt | R_rt | P_llm | R_llm | rt facts | llm facts |
|----------|----------|---------|-----|----------|-----------|------|------|-------|--------|----------|-----------|
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow_eu_path | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny_no_citizenship | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ee_citizen | ee_citizen |
| civil_service_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | ee_citizen, eu_citizen, full_capacity | ∅ |
| civil_service_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | ee_citizen, eu_citizen, full_capacity, secondary_education, speaks_estonian | ∅ |
| civil_service_u8_need_user | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | no_conflict_declared | ∅ |
| consumer_withdrawal_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny_not_consumer | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | distance_contract, is_consumer | ∅ |
| consumer_withdrawal_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | is_consumer | is_consumer |
| consumer_withdrawal_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | distance_contract, is_consumer | ∅ |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_pensioner | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | applicant_is_owner, primary_residence_registered, receives_pension, residential_land | ∅ |
| land_tax_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_deny_not_residential | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| land_tax_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | primary_residence_registered | primary_residence_registered |
| land_tax_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | applicant_is_owner, municipality_exemption_set, primary_residence_registered, residential_land | ∅ |
| journalism_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_allow_via_consent | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny_no_basis | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_need_user | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalism_ethics, public_interest | ∅ |
| journalism_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| journalism_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| building_permit_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_incompetent | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_no_site_study | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| db-then-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| prompt-swap | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| unrelated-law | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow_eu_path | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny_no_citizenship | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ee_citizen | ee_citizen |
| civil_service_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.67 | ee_citizen, eu_citizen, full_capacity | ee_citizen, full_capacity |
| civil_service_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | ee_citizen, eu_citizen, full_capacity, secondary_education, speaks_estonian | ∅ |
| civil_service_u8_need_user | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | no_conflict_declared | ∅ |
| consumer_withdrawal_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny_not_consumer | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | is_consumer | is_consumer |
| consumer_withdrawal_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | distance_contract, is_consumer | ∅ |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_pensioner | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | applicant_is_owner, primary_residence_registered, receives_pension, residential_land | ∅ |
| land_tax_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_deny_not_residential | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| land_tax_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | primary_residence_registered | primary_residence_registered |
| land_tax_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | applicant_is_owner, municipality_exemption_set, primary_residence_registered, residential_land | ∅ |
| journalism_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_allow_via_consent | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny_no_basis | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.67 | 1.00 | journalism_ethics, public_interest | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| journalism_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| building_permit_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_incompetent | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_no_site_study | DENY | DENY | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| db-then-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | emergency | ∅ |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| prompt-swap | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| unrelated-law | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow_eu_path | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny_no_citizenship | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ee_citizen | ee_citizen |
| civil_service_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.67 | ee_citizen, eu_citizen, full_capacity | ee_citizen, full_capacity |
| civil_service_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | ee_citizen, eu_citizen, full_capacity, secondary_education, speaks_estonian | ∅ |
| civil_service_u8_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | no_conflict_declared | no_conflict_declared |
| consumer_withdrawal_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny_not_consumer | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | is_consumer | is_consumer |
| consumer_withdrawal_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | distance_contract, is_consumer | ∅ |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_pensioner | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | applicant_is_owner, primary_residence_registered, receives_pension, residential_land | ∅ |
| land_tax_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_deny_not_residential | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| land_tax_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | primary_residence_registered | primary_residence_registered |
| land_tax_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | applicant_is_owner, municipality_exemption_set, primary_residence_registered, residential_land | ∅ |
| journalism_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_allow_via_consent | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny_no_basis | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_need_user | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalism_ethics, public_interest | ∅ |
| journalism_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | journalistic_purpose | journalistic_purpose |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.50 | journalistic_purpose, subject_consent | journalistic_purpose |
| journalism_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| building_permit_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_incompetent | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_no_site_study | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| db-then-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| deny | DENY | DENY | NEED_MORE_INFO | YES | NO | 1.00 | 1.00 | 0.00 | 1.00 | ∅ | emergency, one_parent_unreachable |
| need-db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| prompt-swap | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| unrelated-law | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_allow_eu_path | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny_no_citizenship | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ee_citizen | ee_citizen |
| civil_service_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.67 | ee_citizen, eu_citizen, full_capacity | ee_citizen, full_capacity |
| civil_service_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | ee_citizen, eu_citizen, full_capacity, secondary_education, speaks_estonian | ∅ |
| civil_service_u8_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | no_conflict_declared | no_conflict_declared |
| consumer_withdrawal_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny_not_consumer | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | distance_contract, is_consumer | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | is_consumer | is_consumer |
| consumer_withdrawal_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | distance_contract, is_consumer | ∅ |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_pensioner | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | applicant_is_owner, primary_residence_registered, receives_pension, residential_land | ∅ |
| land_tax_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_deny_not_residential | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| land_tax_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | primary_residence_registered | primary_residence_registered |
| land_tax_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | applicant_is_owner, municipality_exemption_set, primary_residence_registered, residential_land | ∅ |
| journalism_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_allow_via_consent | ALLOW | ALLOW | DENY | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_deny_no_basis | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.67 | 1.00 | journalism_ethics, public_interest | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | journalistic_purpose | journalistic_purpose |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | journalistic_purpose, subject_consent | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_allow_via_db | ALLOW | ALLOW | ALLOW | YES | YES | 0.00 | 1.00 | 1.00 | 1.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| building_permit_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_incompetent | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_deny_no_site_study | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| building_permit_u7_trust_only | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | building_requirements_met, competent_designer, fee_paid, plan_conformant, site_study_provided | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| db-then-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| deny | DENY | DENY | NEED_MORE_INFO | YES | NO | 1.00 | 1.00 | 0.00 | 1.00 | ∅ | emergency, one_parent_unreachable |
| need-db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 0.50 | 1.00 | emergency | emergency, one_parent_unreachable |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| prompt-swap | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| unrelated-law | ALLOW | ALLOW | NEED_MORE_INFO | YES | NO | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
