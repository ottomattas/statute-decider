# Composed primary cell — LLM-selected encoding + deterministic solver

Generated 2026-08-27T19:43:58+00:00 by `experiments/compose_primary_cell.py` from
`experiments/results/scale-20260825/i-selection/experiment_i.jsonl` (ok rows
only; selected ids reconstructed as gold − unmatched_gold, exact because
unmatched_pred = [] on every ok row). Deterministic solver (z3), zero LLM
calls. Scoring uses the same `score_row`/`aggregate`/paper-outcome code
paths as the runtime row in FINAL-TABLES.md.

## Coverage

- Selection covers all 6 domains used by the gold suite: building_permit, civil_service_eligibility, consumer_withdrawal, land_tax_exemption, personal_data_journalism, section_120_demo.
- Every (model, repeat) cell therefore runs the full 47-scenario suite; n per model = 5 repeats × 47 = 235.

## Per-model composed cell

Accuracy cells are mean ± sample std across the 5 repeats (each repeat = 47 scenarios). MF precision/recall are pooled row means, as in FINAL-TABLES.md.

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | dropped rules | failed encodings |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | composed | 235 | 0.851 ± 0.000 | 0.714 ± 0.000 | 1.000 ± 0.000 | 0.857 ± 0.000 | 1.000 | 0.915 | 0 | 0 |
| deepseek-v4-flash | composed | 235 | 0.851 ± 0.000 | 0.714 ± 0.000 | 1.000 ± 0.000 | 0.857 ± 0.000 | 1.000 | 0.915 | 0 | 0 |
| gemini-2.5-flash | composed | 235 | 0.868 ± 0.010 | 0.786 ± 0.000 | 0.983 ± 0.037 | 0.857 ± 0.000 | 1.000 | 0.915 | 0 | 0 |
| gpt-5-mini | composed | 235 | 0.736 ± 0.019 | 0.557 ± 0.032 | 0.983 ± 0.037 | 0.714 ± 0.000 | 1.000 | 0.849 | 0 | 0 |

## Dropped rules (selected rule referenced an unselected claim)

Counts are over all composed encodings for the model (5 repeats × 6 domains). Rules the model did not
select at all are not 'dropped' — they are simply absent from the encoding.

| model | dropped-rule instances | rule ids (count) |
|---|---|---|
| claude-haiku-4-5-20251001 | 0 | — |
| deepseek-v4-flash | 0 | — |
| gemini-2.5-flash | 0 | — |
| gpt-5-mini | 0 | — |

## Encoding failures (build_domain_artifact raised)

None. Every composed encoding validated and built; the referential-integrity drop rule above was sufficient in all 120 encodings.

## Mismatch confusion (expected → predicted, pooled)

| expected → predicted | total | per model |
|---|---|---|
| ALLOW → DENY | 86 | claude-haiku-4-5-20251001: 20, deepseek-v4-flash: 20, gemini-2.5-flash: 15, gpt-5-mini: 31 |
| NEED_MORE_INFO → DENY | 75 | claude-haiku-4-5-20251001: 15, deepseek-v4-flash: 15, gemini-2.5-flash: 15, gpt-5-mini: 30 |
| DENY → ALLOW | 2 | gemini-2.5-flash: 1, gpt-5-mini: 1 |

## Failure pattern

Failures are one-sided toward DENY: 161 of 163 outcome mismatches predict DENY. The driver is missed allow-side rules (most often `allow_emergency`, `deny_non_parent`, `allow_building_permit`, `allow_delegated_right` on the failing rows): without the allow path, the solver either fires a deny rule outright (gold ALLOW → DENY) or decides instead of abstaining, because the unselected allow-path claims are no longer in the encoding to be reported as missing (gold NEED_MORE_INFO → DENY). Missing-fact precision is barely touched (pooled minimum 1.000 across models); recall is what degrades when selection misses claims and rules.
