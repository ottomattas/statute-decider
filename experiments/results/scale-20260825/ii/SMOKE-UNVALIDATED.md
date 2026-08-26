# SMOKE — UNVALIDATED

Generated 2026-08-26T06:15:30Z. Overnight cap EUR 100.00; spent EUR 13.3658; remaining EUR 86.6342.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `scale-2026-08-25-ii`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: gemini, openai, anthropic, deepseek.
Providers skipped (missing key or stub): —.

### Experiment (ii) — runtime (solver)

- n scored: 47 / 47
- outcome accuracy: 1.000
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 1.000
- mean missing-fact P/R: 0.936 / 1.000
- macro missing-fact P/R: 0.929 / 1.000

### Experiment (ii) — LLM-only (all providers)

- n scored: 1880 / 1880
- outcome accuracy: 0.744
- ALLOW accuracy: 0.861
- DENY accuracy: 0.946
- NEED_MORE_INFO accuracy: 0.550
- mean missing-fact P/R: 0.970 / 0.792
- macro missing-fact P/R: 0.970 / 0.845

### Experiment (ii) — LLM-only `gemini`

- n scored: 470 / 470
- outcome accuracy: 0.677
- ALLOW accuracy: 0.843
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.381
- mean missing-fact P/R: 0.994 / 0.723
- macro missing-fact P/R: 0.995 / 0.794

### Experiment (ii) — LLM-only `openai`

- n scored: 470 / 470
- outcome accuracy: 0.749
- ALLOW accuracy: 0.957
- DENY accuracy: 0.950
- NEED_MORE_INFO accuracy: 0.495
- mean missing-fact P/R: 0.984 / 0.768
- macro missing-fact P/R: 0.984 / 0.827

### Experiment (ii) — LLM-only `anthropic`

- n scored: 470 / 470
- outcome accuracy: 0.762
- ALLOW accuracy: 0.786
- DENY accuracy: 0.917
- NEED_MORE_INFO accuracy: 0.657
- mean missing-fact P/R: 0.950 / 0.831
- macro missing-fact P/R: 0.951 / 0.874

### Experiment (ii) — LLM-only `deepseek`

- n scored: 470 / 470
- outcome accuracy: 0.787
- ALLOW accuracy: 0.857
- DENY accuracy: 0.917
- NEED_MORE_INFO accuracy: 0.667
- mean missing-fact P/R: 0.950 / 0.844
- macro missing-fact P/R: 0.951 / 0.884

### Experiment (i) — encoding

_No extraction rows._

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).
