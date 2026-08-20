| id | description | expected | actual | match | notes |
|----|-------------|----------|--------|-------|-------|
| land_tax_allow | Pensioner owner of registered residential land in a supporting municipality resolves to ALLOW. | ALLOW | ALLOW | YES |  |
| land_tax_allow_pensioner | Pensioner supplement path (§ 11 lg 5 p 1): all six conditions including pension status and submitted application hold -> ALLOW. | ALLOW | ALLOW | YES |  |
| land_tax_allow_via_db | Residential status, ownership and residence resolve via DB lookup; user pins municipality exemption and application -> ALLOW via home-land rule. | ALLOW | ALLOW | YES |  |
| land_tax_deny | Applicant is not the owner and registry does not place residence on the parcel, so no exemption rule fires. | DENY | DENY | YES |  |
| land_tax_deny_not_residential | Parcel is not residential land, blocking both home-land and pensioner supplement allow rules; no deny rule exists -> DENY with no applicable rules. | DENY | DENY | YES |  |
| land_tax_need_db | Municipality-level exemption record is missing from DB and intent, halting at NEED_DB_INFO. | NEED_DB_INFO | NEED_DB_INFO | YES |  |
| land_tax_u3_no_register | Population registry is unavailable, so primary-residence registration cannot be verified; home-land allow rule stalls on that claim -> U3 UNVERIFIABLE_CLAIM (no_register). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES |  |
| land_tax_u7_trust_only | All four § 11 lg 1 conditions resolve from a trust-only applicant self-report; home-land rule fires but supporting facts are unverifiable -> U7 UNVERIFIABLE_CLAIM (trust_only). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES |  |
