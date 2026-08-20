# Truth table - consumer_withdrawal

- claims: 5
- rows: 32

| is_consumer | distance_contract | excluded_category | within_14_days | notice_sent_in_time | outcome | reason_code |
|---|---|---|---|---|---|---|
| F | F | F | F | F | DENY | no_applicable_rules |
| F | F | F | F | T | DENY | no_applicable_rules |
| F | F | F | T | F | DENY | no_applicable_rules |
| F | F | F | T | T | DENY | no_applicable_rules |
| F | F | T | F | F | DENY | no_applicable_rules |
| F | F | T | F | T | DENY | no_applicable_rules |
| F | F | T | T | F | DENY | no_applicable_rules |
| F | F | T | T | T | DENY | no_applicable_rules |
| F | T | F | F | F | DENY | no_applicable_rules |
| F | T | F | F | T | DENY | no_applicable_rules |
| F | T | F | T | F | DENY | no_applicable_rules |
| F | T | F | T | T | DENY | no_applicable_rules |
| F | T | T | F | F | DENY | no_applicable_rules |
| F | T | T | F | T | DENY | no_applicable_rules |
| F | T | T | T | F | DENY | no_applicable_rules |
| F | T | T | T | T | DENY | no_applicable_rules |
| T | F | F | F | F | DENY | no_applicable_rules |
| T | F | F | F | T | DENY | no_applicable_rules |
| T | F | F | T | F | DENY | no_applicable_rules |
| T | F | F | T | T | DENY | no_applicable_rules |
| T | F | T | F | F | DENY | no_applicable_rules |
| T | F | T | F | T | DENY | no_applicable_rules |
| T | F | T | T | F | DENY | no_applicable_rules |
| T | F | T | T | T | DENY | no_applicable_rules |
| T | T | F | F | F | DENY | no_applicable_rules |
| T | T | F | F | T | DENY | no_applicable_rules |
| T | T | F | T | F | DENY | no_applicable_rules |
| T | T | F | T | T | ALLOW | — |
| T | T | T | F | F | DENY | no_applicable_rules |
| T | T | T | F | T | DENY | no_applicable_rules |
| T | T | T | T | F | DENY | no_applicable_rules |
| T | T | T | T | T | DENY | no_applicable_rules |
