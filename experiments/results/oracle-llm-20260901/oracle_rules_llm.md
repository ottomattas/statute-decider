# Oracle rules + LLM decider — the missing 2x2 cell

Generated 2026-09-01T09:43:10+00:00 by `experiments/oracle_rules_llm_decider.py`.
All 47 gold scenarios x 4 cheap models x 10 repeats, temperature 0.
Inputs identical to the LLM-only baseline (`framework/llm_baseline.py`) plus
a REFERENCE DECISION RULES section rendering the hand-authored gold
encoding (`use_case.json`); the system prompt instructs the model to play
solver over those rules (fire deny, then allow; abstain listing the unknown
claim ids in open allow rules; default DENY when no allow path remains).
Scoring uses the same `score_row`/`fact_set_precision_recall` code paths as
FINAL-TABLES.md; costs from `experiments/ledger.jsonl`
(experiment `oracle-llm`).

## Per-model results

Accuracy cells are mean ± sample std across the 10 repeats
(each repeat = 47 scenarios). MF precision/recall are pooled row
means. Mean cost/case is the per-call ledger mean.

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | oracle rules + LLM | 470 | 0.851 ± 0.000 | 0.857 ± 0.000 | 1.000 ± 0.000 | 0.762 ± 0.000 | 0.972 | 0.876 | 0.0098 |
| deepseek-v4-flash | oracle rules + LLM | 470 | 0.894 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.762 ± 0.000 | 0.997 | 0.883 | 0.0020 |
| gemini-2.5-flash | oracle rules + LLM | 470 | 0.894 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.762 ± 0.000 | 0.993 | 0.894 | 0.0024 |
| gpt-5-mini | oracle rules + LLM | 470 | 0.894 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.762 ± 0.000 | 1.000 | 0.894 | 0.0026 |

## 2x2 comparison — rule author x decider

New rows next to the existing conditions. `oracle + solver` is the runtime
row (FINAL-TABLES.md, gold-audited); `selected + solver` is the composed
cell (compose-20260827, 5 repeats); `LLM-only` is the 25 Aug scale run
(no rules in the prompt). Prior accuracies are pooled means.

| model | condition | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall |
|---|---|---|---|---|---|---|---|
| z3 (solver) | oracle + solver | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| claude-haiku-4-5-20251001 | **oracle rules + LLM** | 0.851 | 0.857 | 1.000 | 0.762 | 0.972 | 0.876 |
| claude-haiku-4-5-20251001 | selected + solver | 0.851 | 0.714 | 1.000 | 0.857 | 1.000 | 0.915 |
| claude-haiku-4-5-20251001 | LLM-only | 0.762 | 0.786 | 0.917 | 0.657 | 0.950 | 0.831 |
| deepseek-v4-flash | **oracle rules + LLM** | 0.894 | 1.000 | 1.000 | 0.762 | 0.997 | 0.883 |
| deepseek-v4-flash | selected + solver | 0.851 | 0.714 | 1.000 | 0.857 | 1.000 | 0.915 |
| deepseek-v4-flash | LLM-only | 0.787 | 0.857 | 0.917 | 0.667 | 0.950 | 0.844 |
| gemini-2.5-flash | **oracle rules + LLM** | 0.894 | 1.000 | 1.000 | 0.762 | 0.993 | 0.894 |
| gemini-2.5-flash | selected + solver | 0.868 | 0.786 | 0.983 | 0.857 | 1.000 | 0.915 |
| gemini-2.5-flash | LLM-only | 0.677 | 0.843 | 1.000 | 0.381 | 0.994 | 0.723 |
| gpt-5-mini | **oracle rules + LLM** | 0.894 | 1.000 | 1.000 | 0.762 | 1.000 | 0.894 |
| gpt-5-mini | selected + solver | 0.736 | 0.557 | 0.983 | 0.714 | 1.000 | 0.849 |
| gpt-5-mini | LLM-only | 0.749 | 0.957 | 0.950 | 0.495 | 0.984 | 0.768 |

## Failure pattern

| scenario | expected → predicted | rows | models |
|---|---|---|---|
| building_permit_u7_trust_only | NEED_MORE_INFO → ALLOW | 40 | claude-haiku-4-5-20251001 (10), deepseek-v4-flash (10), gemini-2.5-flash (10), gpt-5-mini (10) |
| civil_service_allow_eu_path | ALLOW → DENY | 10 | claude-haiku-4-5-20251001 (10) |
| civil_service_u7_trust_only | NEED_MORE_INFO → ALLOW | 40 | claude-haiku-4-5-20251001 (10), deepseek-v4-flash (10), gemini-2.5-flash (10), gpt-5-mini (10) |
| consumer_withdrawal_u7_trust_only | NEED_MORE_INFO → ALLOW | 40 | claude-haiku-4-5-20251001 (10), deepseek-v4-flash (10), gemini-2.5-flash (10), gpt-5-mini (10) |
| journalism_allow_via_consent | ALLOW → DENY | 10 | claude-haiku-4-5-20251001 (10) |
| journalism_u7_trust_only | NEED_MORE_INFO → ALLOW | 40 | claude-haiku-4-5-20251001 (10), deepseek-v4-flash (10), gemini-2.5-flash (10), gpt-5-mini (10) |
| land_tax_u7_trust_only | NEED_MORE_INFO → ALLOW | 30 | claude-haiku-4-5-20251001 (10), gemini-2.5-flash (10), gpt-5-mini (10) |
| land_tax_u7_trust_only | NEED_MORE_INFO → DENY | 10 | deepseek-v4-flash (10) |

Fact-set-only misses (outcome correct, missing-fact set imperfect):

- civil_service_u3_no_register: claude-haiku-4-5-20251001 (10)
- db-then-user: claude-haiku-4-5-20251001 (10)
- journalism_need_user: claude-haiku-4-5-20251001 (10), deepseek-v4-flash (4), gemini-2.5-flash (10)
- journalism_u5_need_db: claude-haiku-4-5-20251001 (10), deepseek-v4-flash (10)
- need-db: claude-haiku-4-5-20251001 (10)

## Error rows

None.

## Cost

Ledger rows tagged `oracle-llm`: 1880 calls, EUR 7.8710 total.
