# Experiment (ii) LLM-only — SMOKE — UNVALIDATED

| scenario | condition | expected | actual | match | P | R | missing_facts |
|----------|-----------|----------|--------|-------|---|---|----------------|
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | ALLOW | NO | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | ALLOW | NO | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | one_parent_unreachable, emergency |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen, eu_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | ALLOW | NO | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.67 | ee_citizen, full_capacity |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer, distance_contract |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.67 | 1.00 | public_interest, journalism_ethics, excessive_harm |
| journalism_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| deny | llm | DENY | NEED_MORE_INFO | NO | 0.00 | 1.00 | emergency, one_parent_unreachable |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 0.50 | 1.00 | emergency, one_parent_unreachable |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | NEED_MORE_INFO | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_incompetent | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_deny_no_site_study | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| building_permit_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| db-then-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| need-db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| prompt-swap | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| unrelated-law | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_allow_eu_path | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny_no_citizenship | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| civil_service_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | ee_citizen |
| civil_service_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| civil_service_u8_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | no_conflict_declared |
| consumer_withdrawal_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny_not_consumer | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| consumer_withdrawal_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| consumer_withdrawal_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | is_consumer |
| consumer_withdrawal_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_pensioner | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_deny_not_residential | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| land_tax_u3_no_register | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | primary_residence_registered |
| land_tax_u7_trust_only | llm | NEED_MORE_INFO | DENY | NO | 1.00 | 0.00 | ∅ |
| journalism_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| journalism_allow_via_consent | llm | ALLOW | DENY | NO | 1.00 | 1.00 | ∅ |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_deny_no_basis | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_need_user | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| journalism_u7_trust_only | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_allow_via_db | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
