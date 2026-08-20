# Scenarios: land_tax_exemption

Domain: Land Tax Act (MMS) § 11 — home-land and pensioner supplementary exemption.

| Scenario | Tag | Expected outcome | Key condition |
|---|---|---|---|
| `land_tax_allow` | positive | ALLOW | Pensioner owner with residence registered, municipality exemption set |
| `land_tax_deny` | negative | DENY | Applicant not the owner and not registered on the parcel |
| `land_tax_need_db` | needs-info | NEED_DB_INFO | Municipality exemption record absent from DB (`municipality_exemption_set` not stored) |

Variables: `residential_land`, `primary_residence_registered`, `applicant_is_owner`,
`receives_pension`, `municipality_exemption_set` (DB-sourced);
`application_submitted` (user-sourced).

Rules: `allow_home_land_exemption`, `allow_pensioner_supplement`.
