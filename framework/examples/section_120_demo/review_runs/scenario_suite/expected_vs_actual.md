| id | description | expected | actual | match | missing | notes |
|----|-------------|----------|--------|-------|---------|-------|
| allow | Parent plus emergency facts resolve to ALLOW. | ALLOW | ALLOW | YES | — |  |
| db-then-user | The solver first needs DB facts and then still needs user input. | NEED_USER_INFO | NEED_USER_INFO | YES | emergency |  |
| deny | Non-parent request resolves to DENY. | DENY | DENY | YES | — |  |
| need-db | Sparse request needs DB-backed parent and custody facts. | NEED_USER_INFO | NEED_USER_INFO | YES | emergency |  |
| need-user | DB facts are known but the emergency fact remains open. | NEED_USER_INFO | NEED_USER_INFO | YES | emergency |  |
| prompt-swap | The same allow scenario, but with strict prompt metadata paths recorded. | ALLOW | ALLOW | YES | — |  |
| unrelated-law | A strong request with an unrelated law neutral-blocks at domain extraction. | ALLOW | ALLOW | YES | — |  |
