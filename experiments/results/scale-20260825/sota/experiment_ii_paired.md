# Experiment (ii) paired — SMOKE — UNVALIDATED

| scenario | expected | runtime | llm | rt match | llm match | P_rt | R_rt | P_llm | R_llm | rt facts | llm facts |
|----------|----------|---------|-----|----------|-----------|------|------|-------|--------|----------|-----------|
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.50 | journalistic_purpose, subject_consent | journalistic_purpose |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 0.50 | journalistic_purpose, subject_consent | journalistic_purpose |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
| civil_service_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| civil_service_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| consumer_withdrawal_need_user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | notice_sent_in_time, within_14_days | within_14_days, notice_sent_in_time |
| land_tax_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| land_tax_need_db | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | municipality_exemption_set | municipality_exemption_set |
| journalism_deny | DENY | DENY | DENY | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| journalism_u5_need_db | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | journalistic_purpose, subject_consent | ∅ |
| building_permit_allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| building_permit_u3_no_register | NEED_MORE_INFO | NEED_MORE_INFO | ALLOW | YES | NO | 1.00 | 1.00 | 1.00 | 0.00 | fee_paid | ∅ |
| allow | ALLOW | ALLOW | ALLOW | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | ∅ | ∅ |
| need-user | NEED_MORE_INFO | NEED_MORE_INFO | NEED_MORE_INFO | YES | YES | 1.00 | 1.00 | 1.00 | 1.00 | emergency | emergency |
