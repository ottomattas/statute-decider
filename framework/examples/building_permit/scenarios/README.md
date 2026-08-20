# Scenarios: building_permit

Domain: Building Code (EhS) §§ 42, 44 — building-permit issuance and refusal.

| Scenario | Tag | Expected outcome | Key condition |
|---|---|---|---|
| `building_permit_allow` | positive | ALLOW | All five § 42 lg 1 conditions met, no § 44 refusal ground |
| `building_permit_deny` | negative | DENY | Project violates detail plan (§ 44 p 1) |
| `building_permit_need_db` | needs-info | NEED_DB_INFO | State-fee payment record absent from payment ledger (`fee_paid` overridden to null) |

Variables: `plan_conformant`, `building_requirements_met`, `competent_designer`,
`site_study_provided`, `fee_paid`, `plan_violation` (all DB-sourced).

Rules: `allow_building_permit`, `deny_plan_violation`.
