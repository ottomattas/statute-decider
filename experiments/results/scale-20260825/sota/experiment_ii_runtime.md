# Experiment (ii) runtime — SMOKE — UNVALIDATED

| scenario | condition | expected | actual | match | P | R | missing_facts |
|----------|-----------|----------|--------|-------|---|---|----------------|
| civil_service_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| civil_service_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| consumer_withdrawal_need_user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | notice_sent_in_time, within_14_days |
| land_tax_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| land_tax_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | municipality_exemption_set |
| journalism_deny | runtime | DENY | DENY | YES | 1.00 | 1.00 | ∅ |
| journalism_u5_need_db | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | journalistic_purpose, subject_consent |
| building_permit_allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| building_permit_u3_no_register | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | fee_paid |
| allow | runtime | ALLOW | ALLOW | YES | 1.00 | 1.00 | ∅ |
| need-user | runtime | NEED_MORE_INFO | NEED_MORE_INFO | YES | 1.00 | 1.00 | emergency |
