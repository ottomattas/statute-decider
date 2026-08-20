# Scenarios: consumer_withdrawal

Domain: Law of Obligations Act (VOS) §§ 53 lg 4, 56 lg 1 — consumer right of withdrawal.

| Scenario | Tag | Expected outcome | Key condition |
|---|---|---|---|
| `consumer_withdrawal_allow` | positive | ALLOW | Consumer, distance contract, within 14 days, notice sent |
| `consumer_withdrawal_deny` | negative | DENY | Goods in excluded category (§ 53 lg 4) |
| `consumer_withdrawal_need_user` | needs-info | NEED_USER_INFO | DB confirms consumer/contract; user not yet asked about 14-day window |

Variables: `is_consumer`, `distance_contract`, `excluded_category` (DB-sourced);
`within_14_days`, `notice_sent_in_time` (user-sourced).

Rules: `allow_distance_withdrawal`, `deny_excluded_category`.
