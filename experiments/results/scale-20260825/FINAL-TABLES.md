# SCALE results — 25 Aug 2026 run — GOLD AUDIT PENDING

**Status: SCALE (not smoke). Numbers are final for the 25 Aug matrix, but four
gold rows are `gold_confidence: low` and still need operator audit:**
`consumer_withdrawal_allow_via_db`, `land_tax_allow_via_db`,
`building_permit_allow_via_db`, `section_120_demo/prompt-swap`.
Audit exposure is low: across all 4 cheap models × 10 repeats, every model
agreed with the proposed gold on all four rows (40/40 outcome matches, perfect
fact sets), so an audit flip would *reduce* reported LLM accuracy, not inflate it.

Generated 2026-08-26 by `experiments/render_final_tables.py` (tables) and
`experiments/render_drilldown.py` (failure detail) from
`experiments/results/scale-20260825/`. Costs from `experiments/ledger.jsonl`,
window ≥ 2026-08-25T00:00:00Z (the scale run + 26 Aug fill-in).

## Completeness

Every cell is at its full target n after the 26 Aug fill-in (81 gemini-flash
experiment-ii rows whose scores were lost in the 25 Aug stall, plus 7 retries
of experiment-i selection error rows; fill-in cost EUR 0.14).

| leg | cell target | status |
|---|---|---|
| ii (cheap) | 470 per model (47 scenarios × 10 repeats) | 470/470 × 4 models, 0 unresolved errors |
| ii runtime | 47 | 47/47, accuracy 1.000 |
| i synthesis | 30 per model (6 cases × 5 repeats) | 30/30 × 4 models |
| i selection | 30 per model | 30/30 × 4 models (6 rows needed retries, see deviations) |
| SOTA | 12 per model (12 scenarios × 1 repeat) | 12/12 × 4 models |

## Experiment (ii) — runtime (solver) vs LLM-only, cheap models

Contract schema; accuracy cells are mean ± sample std across the 10 repeats
(each repeat = 47 scenarios). MF = missing-fact set (row means). Mean
cost/case is the per-call ledger mean for the run window.

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|---|
| z3 (solver) | runtime | 47 | 1.000 | 1.000 | 1.000 | 1.000 | 0.936 | 1.000 | 0.0000 |
| claude-haiku-4-5-20251001 | llm_only | 470 | 0.762 ± 0.009 | 0.786 ± 0.000 | 0.917 ± 0.000 | 0.657 ± 0.020 | 0.950 | 0.831 | 0.0096 |
| deepseek-v4-flash | llm_only | 470 | 0.787 ± 0.000 | 0.857 ± 0.000 | 0.917 ± 0.000 | 0.667 ± 0.000 | 0.950 | 0.844 | 0.0019 |
| gemini-2.5-flash | llm_only | 470 | 0.677 ± 0.030 | 0.843 ± 0.045 | 1.000 ± 0.000 | 0.381 ± 0.045 | 0.994 | 0.723 | 0.0022 |
| gpt-5-mini | llm_only | 470 | 0.749 ± 0.042 | 0.957 ± 0.037 | 0.950 ± 0.058 | 0.495 ± 0.064 | 0.984 | 0.768 | 0.0028 |

LaTeX body:

```latex
z3 (solver) & runtime & 47 & 1.000 & 1.000 & 1.000 & 1.000 & 0.936 & 1.000 & 0.0000 \\
claude-haiku-4-5 & llm\_only & 470 & 0.762 $\pm$ 0.009 & 0.786 $\pm$ 0.000 & 0.917 $\pm$ 0.000 & 0.657 $\pm$ 0.020 & 0.950 & 0.831 & 0.0096 \\
deepseek-v4-flash & llm\_only & 470 & 0.787 $\pm$ 0.000 & 0.857 $\pm$ 0.000 & 0.917 $\pm$ 0.000 & 0.667 $\pm$ 0.000 & 0.950 & 0.844 & 0.0019 \\
gemini-2.5-flash & llm\_only & 470 & 0.677 $\pm$ 0.030 & 0.843 $\pm$ 0.045 & 1.000 $\pm$ 0.000 & 0.381 $\pm$ 0.045 & 0.994 & 0.723 & 0.0022 \\
gpt-5-mini & llm\_only & 470 & 0.749 $\pm$ 0.042 & 0.957 $\pm$ 0.037 & 0.950 $\pm$ 0.058 & 0.495 $\pm$ 0.064 & 0.984 & 0.768 & 0.0028 \\
```

Notes:

- Runtime MF precision 0.936 < 1 is a property of the gold/solver fact-set
  convention (solver enumerates every open claim; four gold rows expect a
  subset), not a solver bug; recall is 1.000.
- The z3 runtime is deterministic; no repeats needed.

## Experiment (i) — synthesis vs selection (claim-alignment F1)

± sample std across the 5 repeats (each repeat = 6 case dirs).
**Schema deviation note:** the two conditions score different things.
*Synthesis* aligns free-form model-synthesized claims/rules against gold
semantically (`alignment_f1` from the alignment matcher; `equiv rate` =
solver-checked rule equivalence). *Selection* asks the model to pick claim and
rule IDs from the provided catalogue, so its F1 is an exact ID-set score and
`align F1` = (claim F1 + rule F1)/2. The two F1 columns are not directly
comparable metrics — the delta is still the paper's point (constrained
selection works; open synthesis does not).

| model | condition | n | align F1 | claim F1 | rule F1 | equiv rate | errors | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | synthesis | 30 | 0.246 ± 0.018 | — | — | 0.608 ± 0.063 | 0 | 0.0201 |
| deepseek-v4-flash | synthesis | 30 | 0.212 ± 0.016 | — | — | 0.366 ± 0.072 | 0 | 0.0035 |
| gemini-2.5-flash | synthesis | 30 | 0.231 ± 0.017 | — | — | 0.617 ± 0.046 | 0 | 0.0086 |
| gpt-5-mini | synthesis | 30 | 0.182 ± 0.027 | — | — | 0.541 ± 0.182 | 0 | 0.0113 |
| claude-haiku-4-5-20251001 | selection | 30 | 0.944 ± 0.000 | 0.954 ± 0.000 | 0.933 ± 0.000 | — | 0 | 0.0117 |
| deepseek-v4-flash | selection | 30 | 0.807 ± 0.000 | 0.815 ± 0.000 | 0.800 ± 0.000 | — | 0 | 0.0023 |
| gemini-2.5-flash | selection | 30 | 0.937 ± 0.011 | 0.980 ± 0.007 | 0.895 ± 0.020 | — | 0 | 0.0031 |
| gpt-5-mini | selection | 30 | 0.913 ± 0.019 | 0.953 ± 0.010 | 0.872 ± 0.034 | — | 0 | 0.0043 |

LaTeX body:

```latex
claude-haiku-4-5 & synthesis & 30 & 0.246 $\pm$ 0.018 & — & — & 0.608 $\pm$ 0.063 & 0 & 0.0201 \\
deepseek-v4-flash & synthesis & 30 & 0.212 $\pm$ 0.016 & — & — & 0.366 $\pm$ 0.072 & 0 & 0.0035 \\
gemini-2.5-flash & synthesis & 30 & 0.231 $\pm$ 0.017 & — & — & 0.617 $\pm$ 0.046 & 0 & 0.0086 \\
gpt-5-mini & synthesis & 30 & 0.182 $\pm$ 0.027 & — & — & 0.541 $\pm$ 0.182 & 0 & 0.0113 \\
claude-haiku-4-5 & selection & 30 & 0.944 $\pm$ 0.000 & 0.954 $\pm$ 0.000 & 0.933 $\pm$ 0.000 & — & 0 & 0.0117 \\
deepseek-v4-flash & selection & 30 & 0.807 $\pm$ 0.000 & 0.815 $\pm$ 0.000 & 0.800 $\pm$ 0.000 & — & 0 & 0.0023 \\
gemini-2.5-flash & selection & 30 & 0.937 $\pm$ 0.011 & 0.980 $\pm$ 0.007 & 0.895 $\pm$ 0.020 & — & 0 & 0.0031 \\
gpt-5-mini & selection & 30 & 0.913 $\pm$ 0.019 & 0.953 $\pm$ 0.010 & 0.872 $\pm$ 0.034 & — & 0 & 0.0043 \\
```

Selection schema deviations (all recovered on retry; final n = 30 everywhere):

- `gpt-5-mini` emitted invented claim IDs (`DISTANCE_CONTRACT`,
  `EXCLUDED_CATEGORY`, `IS_CONSUMER`, `NOTICE_SENT`) on
  `consumer_withdrawal` in 3 of 5 first-attempt repeats.
- `claude-haiku-4-5` emitted the invented claim ID
  `residential_land_registered` on `land_tax_exemption` in 3 of 5
  first-attempt repeats; one row needed two retries.
- These are model schema violations, not harness errors; the paper should
  mention that constrained selection still needs an ID-validity check.

## SOTA slice — explicitly qualitative (n = 12, single repeat)

12 representative high-confidence scenarios, 1 repeat. Too small for
significance claims; use only as a qualitative "frontier models do not close
the gap" observation.

| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |
|---|---|---|---|---|---|---|---|---|---|
| z3 (solver) | runtime | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0000 |
| claude-fable-5 | llm_only | 12 | 0.917 | 1.000 | 1.000 | 0.800 | 1.000 | 0.875 | 0.1388 |
| deepseek-v4-pro | llm_only | 12 | 0.833 | 1.000 | 1.000 | 0.600 | 1.000 | 0.833 | 0.0139 |
| gemini-3.1-pro-preview | llm_only | 12 | 0.833 | 1.000 | 1.000 | 0.600 | 1.000 | 0.833 | 0.0188 |
| gpt-5.6-sol | llm_only | 12 | 0.917 | 1.000 | 1.000 | 0.800 | 1.000 | 0.875 | 0.0356 |

LaTeX body:

```latex
z3 (solver) & runtime & 12 & 1.000 & 1.000 & 1.000 & 1.000 & 1.000 & 1.000 & 0.0000 \\
claude-fable-5 & llm\_only & 12 & 0.917 & 1.000 & 1.000 & 0.800 & 1.000 & 0.875 & 0.1388 \\
deepseek-v4-pro & llm\_only & 12 & 0.833 & 1.000 & 1.000 & 0.600 & 1.000 & 0.833 & 0.0139 \\
gemini-3.1-pro-preview & llm\_only & 12 & 0.833 & 1.000 & 1.000 & 0.600 & 1.000 & 0.833 & 0.0188 \\
gpt-5.6-sol & llm\_only & 12 & 0.917 & 1.000 & 1.000 & 0.800 & 1.000 & 0.875 & 0.0356 \\
```

Every SOTA miss is on NEED_MORE_INFO: all four frontier models fail
`building_permit_u3_no_register` (answer ALLOW instead of asking for
`fee_paid`), and all four fail or under-report `journalism_u5_need_db`
(gemini-3.1-pro and deepseek-v4-pro answer ALLOW outright; claude-fable-5 and
gpt-5.6-sol abstain but name only 1 of 2 missing facts). The frontier failure
mode is the same as the cheap-model failure mode, just rarer.

## Cost summary

Ledger window ≥ 2026-08-25T00:00Z (scale run + fill-in). Lifetime ledger
total incl. 21 Aug smoke and probes: **EUR 13.37 of the EUR 100 cap**.

| leg | calls | EUR |
|---|---|---|
| ii cheap (4 models) | 1987 | 7.98 |
| ii SOTA (4 models) | 48 | 2.48 |
| i synthesis + selection (4 models) | 247 | 1.95 |
| **window total** | **2282** | **12.41** |

LaTeX body:

```latex
(ii) cheap, 4 models & 1987 & 7.98 \\
(ii) SOTA, 4 models & 48 & 2.48 \\
(i) synthesis + selection & 247 & 1.95 \\
\midrule window total & 2282 & 12.41 \\
```

Ledger residue (documented, affects call counts, not scores): the gemini-flash
window count 577 = 470 scored + 81 rows paid on 25 Aug whose scores were lost
pre-per-row-writing (re-paid EUR 0.14 in the 26 Aug fill-in) + 26 rows
double-paid before the resume fix. Experiment-i counts include 7 selection
retries. Per-call means are unaffected by duplicates.

## Interesting spots

### Repeat variance — which models are stable

Outcome-accuracy std across 10 repeats: **deepseek-v4-flash ± 0.000** (all 10
repeats identical: fully deterministic at temperature 0) and
**claude-haiku ± 0.009** are stable; **gemini-flash ± 0.030** and
**gpt-5-mini ± 0.042** are noisy — gpt-5-mini's per-class std reaches 0.064
on NEED_MORE_INFO. Consequence: single-repeat comparisons of flash-class
models can be off by ±4 points; 10 repeats were worth it.

### Per-class gaps — the NEED_MORE_INFO story

DENY is nearly solved (0.917–1.000) and ALLOW is decent (0.786–0.957), but
NEED_MORE_INFO — the abstention class, 210 of 470 rows — collapses to
0.381–0.667. When models get NMI wrong they overwhelmingly *answer anyway*:
gemini 120/130 NMI errors are NMI→ALLOW, gpt-5-mini 96/106. Exactly 10
NMI→DENY errors per model = `land_tax_u7_trust_only` ×10 repeats, every
model, every repeat. The runtime solver scores 1.000 on the same rows because
abstention is structural (open claims block the verdict), not a judgment call.

### Selection vs synthesis

Selection F1 0.807–0.944 vs synthesis F1 0.182–0.246: a +0.60 to +0.73 delta
per model (largest gpt-5-mini +0.731, smallest deepseek +0.595). Models can
reliably *pick* the right claims/rules from a catalogue but cannot *write*
them into the gold schema. Synthesis equivalence rate (0.366–0.617) shows
part of the loss is representational, not conceptual — some synthesized rules
are solver-equivalent despite failing string alignment.

### Accuracy per EUR

deepseek-v4-flash dominates: best cheap-model accuracy (0.787) at the lowest
cost (EUR 0.0019/case) — 0.41 accuracy-per-milli-EUR vs claude-haiku's 0.08
(5× worse; claude is the second-best scorer at 5× deepseek's price).
claude-fable-5 buys +0.13 accuracy over deepseek-flash at 72× the per-case
cost — and still loses to the free solver.

### Surprises

1. **`u7_trust_only` is a universal breaker:** all five domain variants of
   "user asserts a fact that requires register verification" fail 40/40 —
   every cheap model, every repeat, all five domains. Models take the user's
   word; the runtime's trust policy does not. This is the single cleanest
   design-level argument for the architecture in the whole dataset.
2. **`section_120_demo/deny` inverts the failure:** DENY→NEED_MORE_INFO ×23/40
   — the one place where models *over*-abstain, on the abstract §120 demo
   statute. Over- and under-abstention coexist; prompt-level "be careful"
   fixes would push the two failure modes in opposite directions.
3. **`unrelated-law` (ALLOW, 36/40 wrong, 24 as NMI):** an irrelevant statute
   in context makes models refuse a clear ALLOW.
4. **`journalism_allow_via_consent` ALLOW→DENY ×25:** models overweight the
   privacy default and miss the consent basis that flips it to ALLOW.
5. Frontier models fail the same NMI probes (see SOTA above): scale does not
   buy structural abstention.

### Drill-down highlights (regenerated: `experiments/results/mismatch-drilldown.md`)

Scale source: 1880 scored rows, 599 failed cells = 482 wrong outcome + 113
fact-set-only + 4 superseded hard errors. Most instructive cells:

- `*_u7_trust_only` (5 scenarios × 4 models × 10 repeats): 200/200 failed;
  four domains flip to ALLOW, `land_tax_u7_trust_only` flips to DENY.
- `building_permit_need_db` / `building_permit_u3_no_register`: 40/40 each —
  the building-permit domain's DB-verification probes defeat all models.
- `gemini-2.5-flash × journalism_need_user`, `× civil_service_u3_no_register`,
  `× consumer_withdrawal_u3_no_register`: 10/10 each — gemini is the most
  eager to answer without facts (NMI accuracy 0.381).
- Fact-set-only: `need-db` (28) and `db-then-user` (24) — outcome right but
  the model under-enumerates which facts are missing; this is where MF recall
  (0.723–0.844) is lost.
