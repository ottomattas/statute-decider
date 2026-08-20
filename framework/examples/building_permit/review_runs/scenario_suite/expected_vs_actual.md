| id | description | expected | actual | match | missing | notes |
|----|-------------|----------|--------|-------|---------|-------|
| building_permit_allow | All five § 42 lg 1 positive conditions hold and no § 44 refusal ground fires, yielding ALLOW. | ALLOW | ALLOW | YES | — |  |
| building_permit_allow_via_db | Intent supplies nothing; all five positive conditions and the plan-violation flag resolve via DB lookup -> ALLOW via § 42 lg 1. | ALLOW | ALLOW | YES | —→building_requirements_met,competent_designer,fee_paid,plan_conformant,site_study_provided |  |
| building_permit_deny | Detail-plan violation under § 44 p 1 fires the deny rule, yielding DENY. | DENY | DENY | YES | — |  |
| building_permit_deny_incompetent | Designer competence is false, blocking allow_building_permit; plan-violation is false so deny_plan_violation does not fire -> DENY with no applicable rules (§ 44 p 2 fallback). | DENY | DENY | YES | — |  |
| building_permit_deny_no_site_study | Site-study requirement is unmet, blocking allow_building_permit; no plan-violation so no deny rule fires -> DENY with no applicable rules (§ 44 p 3 fallback). | DENY | DENY | YES | — |  |
| building_permit_need_db | State-fee payment record absent from the payment ledger; solver cannot confirm fee_paid after DB lookup -> NEED_DB_INFO. | NEED_DB_INFO | NEED_DB_INFO | YES | fee_paid |  |
| building_permit_u3_no_register | State-fee ledger is unreachable, so fee_paid cannot be verified; allow_building_permit stalls on that claim -> U3 UNVERIFIABLE_CLAIM (no_register). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | fee_paid |  |
| building_permit_u7_trust_only | Designer self-report (trust-only) covers competence and state-fee; allow_building_permit fires via lookup but supporting facts are unverifiable -> U7 UNVERIFIABLE_CLAIM (trust_only). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | building_requirements_met,competent_designer,fee_paid,plan_conformant,site_study_provided |  |
