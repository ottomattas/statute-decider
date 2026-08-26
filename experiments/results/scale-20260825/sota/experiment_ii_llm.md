# Experiment (ii) LLM-only — SMOKE — UNVALIDATED

| scenario | condition | expected | actual | match | P | R | missing_facts |
|----------|-----------|----------|--------|-------|---|---|----------------|
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 0.50 | journalistic_purpose |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
| civil_service_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | within_14_days, notice_sent_in_time |
| land_tax_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| journalism_deny | llm | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_u5_need_db | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| building_permit_allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_u3_no_register | llm | NEED_MORE_INFO | ALLOW | NO | 1.00 | 0.00 | ∅ |
| allow | llm | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| need-user | llm | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
