# Composed synthesis cell — LLM-synthesized encoding + deterministic solver

Generated 2026-08-28T06:41:23+00:00 by `experiments/compose_synthesis_cell.py` from
`experiments/results/synthesis-20260827/experiment_i.jsonl` (27 Aug re-run of
the synthesis leg with persisted DomainArtifact bodies). Deterministic solver
(z3), zero LLM calls beyond the extraction re-run itself. Scoring uses the
same `score_row`/`aggregate`/paper-outcome code paths as the selection cell.

## Protocol

- Synthesized claims aligned to gold (per-row alignment `matches`) are renamed
  to the gold claim id, so intent/registry facts ground them. Unaligned claims
  keep their synthesized ids (prefixed `syn::` only on collision with a gold
  id) and receive no facts: the solver treats them as unknown. Rules get the
  same id substitution and nothing else; encodings are never repaired.
- Predicted missing facts still in synthesized vocabulary stay in the predicted
  set and count against precision; they are also tallied as unmappable below.
- A domain that fails to rebuild scores its scenarios as incorrect
  (outcome mismatch, precision/recall 0), as in the selection composer.

## Grounding coverage

- Synthesized claims aligned to gold vocabulary: 201/1122 (17.9%).
- Rules running with ≥1 ungrounded claim: 663/716 (92.6%).
- Predicted missing facts unmappable to gold vocabulary: 2412/2689.
- Encoding rebuild failures: 0 of 120.

## Per-model composed synthesis cell

Accuracy cells are mean ± sample std across the 5 repeats (each repeat = 47 scenarios). MF precision/recall are pooled row means.

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | failed encodings |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | synthesis + solver | 235 | 0.579 ± 0.035 | 0.043 ± 0.039 | 0.600 ± 0.109 | 0.924 ± 0.087 | 0.385 | 0.687 | 0 |
| deepseek-v4-flash | synthesis + solver | 235 | 0.391 ± 0.039 | 0.114 ± 0.064 | 0.233 ± 0.109 | 0.667 ± 0.143 | 0.484 | 0.588 | 0 |
| gemini-2.5-flash | synthesis + solver | 235 | 0.515 ± 0.010 | 0.000 ± 0.000 | 0.267 ± 0.037 | 1.000 ± 0.000 | 0.294 | 0.628 | 0 |
| gpt-5-mini | synthesis + solver | 235 | 0.511 ± 0.056 | 0.014 ± 0.032 | 0.300 ± 0.126 | 0.962 ± 0.085 | 0.277 | 0.661 | 0 |

## Mismatch confusion (expected → predicted, pooled)

| expected → predicted | total |
|---|---|
| ALLOW → NEED_MORE_INFO | 222 |
| DENY → NEED_MORE_INFO | 146 |
| ALLOW → DENY | 46 |
| NEED_MORE_INFO → DENY | 35 |
| NEED_MORE_INFO → ALLOW | 12 |
| DENY → ALLOW | 10 |

## Failure pattern

Synthesized vocabulary barely grounds: only 17.9% of synthesized claims align
to the gold ids the fact tables are keyed by, and 92.6% of rules run with at
least one ungrounded claim. The solver therefore cannot see most facts and
over-abstains — 368 of 471 outcome mismatches are decidable cases (gold ALLOW
or DENY) pushed to NEED_MORE_INFO, and the missing-fact sets it reports are
mostly in synthesized vocabulary (2412 of 2689 predicted ids unmappable to
gold), collapsing precision to 0.28–0.48. The composed synthesis cell is the
quantified version of the extraction finding: models cannot write encodings
that drive the pipeline, which is why selection is its extraction mode.
