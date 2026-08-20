# Scenarios: personal_data_journalism

Domain: Personal Data Protection Act (IKS) § 4 — journalism basis for consent-free processing.

| Scenario | Tag | Expected outcome | Key condition |
|---|---|---|---|
| `journalism_allow` | positive | ALLOW | Journalistic purpose + public interest + ethics, no excessive harm |
| `journalism_deny` | negative | DENY | Excessive harm defeats ethics compliance (§ 4 lause 2 override) |
| `journalism_need_user` | needs-info | NEED_USER_INFO | CMS confirms journalistic purpose; editorial public-interest and ethics judgements not yet provided |

Variables: `journalistic_purpose`, `subject_consent` (DB-sourced);
`public_interest`, `journalism_ethics`, `excessive_harm` (user-sourced).

Rules: `allow_journalism_basis`, `allow_consent_basis`, `block_ethics_when_excessive_harm` (set-false).
