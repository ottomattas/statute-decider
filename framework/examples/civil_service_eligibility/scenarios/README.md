# Scenarios: civil_service_eligibility

Domain: Estonian Civil Service Act (ATS) §§ 14–15 — appointment eligibility.

| Scenario | Tag | Expected outcome | Key condition |
|---|---|---|---|
| `civil_service_allow` | positive | ALLOW | Estonian citizen, clean record, no conflict |
| `civil_service_deny` | negative | DENY | Standing intentional-crime conviction (§ 15 p 1) |
| `civil_service_need_db` | needs-info | NEED_DB_INFO | Citizenship registry entry absent for `ee_citizen` |

Variables: `ee_citizen`, `eu_citizen`, `secondary_education`, `speaks_estonian`,
`full_capacity`, `criminal_conviction` (all DB-sourced); `no_conflict_declared` (user-sourced).

Rules: `allow_ee_citizen`, `allow_eu_citizen`, `deny_conviction`.
