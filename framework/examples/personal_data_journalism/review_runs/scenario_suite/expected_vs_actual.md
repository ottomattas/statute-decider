| id | description | expected | actual | match | missing | notes |
|----|-------------|----------|--------|-------|---------|-------|
| journalism_allow | Journalistic purpose with editorial public-interest and ethics assessment resolves to ALLOW. | ALLOW | ALLOW | YES | — |  |
| journalism_allow_via_consent | Data subject has consented; consent baseline rule fires independently of the journalism basis -> ALLOW. | ALLOW | ALLOW | YES | — |  |
| journalism_deny | Excessive harm defeats ethics compliance and blocks the journalism basis; no consent on record. | DENY | DENY | YES | — |  |
| journalism_deny_no_basis | No consent and no journalistic purpose, so both allow rules are blocked and nothing triggers a deny-set -> DENY with no applicable rules. | DENY | DENY | YES | — |  |
| journalism_need_user | CMS confirms journalistic purpose; public_interest and ethics_ok are editorial judgements not yet provided -> NEED_USER_INFO. | NEED_USER_INFO | NEED_USER_INFO | YES | journalism_ethics,public_interest |  |
| journalism_u3_no_register | Editorial CMS is unavailable so the journalistic-purpose classification cannot be verified; allow_journalism_basis stalls on it -> U3 UNVERIFIABLE_CLAIM (no_register). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | journalistic_purpose |  |
| journalism_u5_need_db | DB override removes journalistic_purpose; both allow rules stall waiting for DB information with no source-unavailable flag -> U5 NEED_DB_INFO. | NEED_DB_INFO | NEED_DB_INFO | YES | journalistic_purpose,subject_consent |  |
| journalism_u7_trust_only | Editorial self-report is trust-only; allow_journalism_basis fires once public-interest and ethics are pinned, but the journalistic-purpose classification is unverifiable -> U7 UNVERIFIABLE_CLAIM (trust_only). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | journalistic_purpose,subject_consent |  |
