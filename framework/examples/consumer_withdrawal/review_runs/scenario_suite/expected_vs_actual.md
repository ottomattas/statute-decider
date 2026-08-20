| id | description | expected | actual | match | missing | notes |
|----|-------------|----------|--------|-------|---------|-------|
| consumer_withdrawal_allow | Consumer, distance contract, within 14 days, notice sent in time, non-excluded goods -> ALLOW under § 56 lg 1. | ALLOW | ALLOW | YES | — |  |
| consumer_withdrawal_allow_via_db | Consumer status and distance-contract flag resolve via DB; user timely-dispatch facts are pinned true, so ALLOW fires via DB lookup. | ALLOW | ALLOW | YES | —→distance_contract,is_consumer |  |
| consumer_withdrawal_deny | Goods fall into § 53 lg 4 excluded category (custom-made), so withdrawal is blocked regardless of other facts. | DENY | DENY | YES | — |  |
| consumer_withdrawal_deny_not_consumer | Counter-party is not a consumer; allow_distance_withdrawal is blocked and no § 53 lg 4 exclusion applies -> DENY with no applicable rules. | DENY | DENY | YES | — |  |
| consumer_withdrawal_need_user | DB confirms consumer + distance-contract + non-excluded goods, but the user-sourced 14-day/notice facts are missing -> NEED_USER_INFO halt. | NEED_USER_INFO | NEED_USER_INFO | YES | notice_sent_in_time,within_14_days |  |
| consumer_withdrawal_u3_no_register | Trader CRM is unreachable, so is_consumer and distance_contract cannot be verified -> U3 UNVERIFIABLE_CLAIM (no_register). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | distance_contract,is_consumer |  |
| consumer_withdrawal_u5_need_db | DB lacks is_consumer with no source-unavailable flag; user timely-dispatch facts are pinned -> U5 NEED_DB_INFO. | NEED_DB_INFO | NEED_DB_INFO | YES | is_consumer |  |
| consumer_withdrawal_u7_trust_only | Consumer status and distance-contract flag come from a trust-only trader self-report; allow_distance_withdrawal fires but the facts are unverifiable -> U7 UNVERIFIABLE_CLAIM (trust_only). | UNVERIFIABLE_CLAIM | UNVERIFIABLE_CLAIM | YES | distance_contract,is_consumer |  |
