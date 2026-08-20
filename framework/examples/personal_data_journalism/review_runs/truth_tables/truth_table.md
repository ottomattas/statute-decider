# Truth table - personal_data_journalism

- claims: 5
- rows: 32

| journalistic_purpose | public_interest | journalism_ethics | subject_consent | excessive_harm | outcome | reason_code |
|---|---|---|---|---|---|---|
| F | F | F | F | F | DENY | no_applicable_rules |
| F | F | F | F | T | DENY | no_applicable_rules |
| F | F | F | T | F | ALLOW | — |
| F | F | F | T | T | ALLOW | — |
| F | F | T | F | F | DENY | no_applicable_rules |
| F | F | T | F | T | DENY | solver_inconsistent |
| F | F | T | T | F | ALLOW | — |
| F | F | T | T | T | DENY | solver_inconsistent |
| F | T | F | F | F | DENY | no_applicable_rules |
| F | T | F | F | T | DENY | no_applicable_rules |
| F | T | F | T | F | ALLOW | — |
| F | T | F | T | T | ALLOW | — |
| F | T | T | F | F | DENY | no_applicable_rules |
| F | T | T | F | T | DENY | solver_inconsistent |
| F | T | T | T | F | ALLOW | — |
| F | T | T | T | T | DENY | solver_inconsistent |
| T | F | F | F | F | DENY | no_applicable_rules |
| T | F | F | F | T | DENY | no_applicable_rules |
| T | F | F | T | F | ALLOW | — |
| T | F | F | T | T | ALLOW | — |
| T | F | T | F | F | DENY | no_applicable_rules |
| T | F | T | F | T | DENY | solver_inconsistent |
| T | F | T | T | F | ALLOW | — |
| T | F | T | T | T | DENY | solver_inconsistent |
| T | T | F | F | F | DENY | no_applicable_rules |
| T | T | F | F | T | DENY | no_applicable_rules |
| T | T | F | T | F | ALLOW | — |
| T | T | F | T | T | ALLOW | — |
| T | T | T | F | F | ALLOW | — |
| T | T | T | F | T | DENY | solver_inconsistent |
| T | T | T | T | F | ALLOW | — |
| T | T | T | T | T | DENY | solver_inconsistent |
