# Results tables — contract schema (model, condition)

**UNVALIDATED until gold `low` rows are operator-audited.** Do not quote as results.

Generated 2026-08-26T05:51:51Z by `experiments/summarize_contract.py`.

Schema notes:

- `n` counts scored rows (cases x repeats); `(k err)` marks rows that
  errored after transport retries and are excluded from accuracy.
- `MF precision/recall` are row-mean missing-fact set scores (empty gold vs empty prediction scores 1/1).
- `mean cost/case (EUR)` divides ledger EUR for the run window by all
  attempted rows; runtime (solver) rows cost 0 by construction.
- Tokens burned by calls that failed all transport retries never reach
  the ledger, so EUR is a lower bound under retries.
- Per-class accuracy is `—` when the slice has no gold rows of that class.

## Run `cheap` — `experiments/results/scale-20260825/ii`

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|---|
| z3 (solver) | runtime | 47 | 1.000 | 1.000 | 1.000 | 1.000 | 0.936 | 1.000 | 0.0000 |
| claude-haiku-4-5-20251001 | llm_only | 470 | 0.762 | 0.786 | 0.917 | 0.657 | 0.950 | 0.831 | 0.0096 |
| deepseek-v4-flash | llm_only | 470 (4 err) | 0.787 | 0.857 | 0.917 | 0.667 | 0.950 | 0.844 | 0.0019 |
| gemini-2.5-flash | llm_only | 470 | 0.677 | 0.843 | 1.000 | 0.381 | 0.994 | 0.723 | 0.0027 |
| gpt-5-mini | llm_only | 470 | 0.749 | 0.957 | 0.950 | 0.495 | 0.984 | 0.768 | 0.0028 |

## Run `sota` — `experiments/results/scale-20260825/sota`

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|---|
| z3 (solver) | runtime | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0000 |
| claude-fable-5 | llm_only | 12 | 0.917 | 1.000 | 1.000 | 0.800 | 1.000 | 0.875 | 0.1388 |
| deepseek-v4-pro | llm_only | 12 | 0.833 | 1.000 | 1.000 | 0.600 | 1.000 | 0.833 | 0.0139 |
| gemini-3.1-pro-preview | llm_only | 12 | 0.833 | 1.000 | 1.000 | 0.600 | 1.000 | 0.833 | 0.0188 |
| gpt-5.6-sol | llm_only | 12 | 0.917 | 1.000 | 1.000 | 0.800 | 1.000 | 0.875 | 0.0356 |

