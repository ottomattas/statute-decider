# SMOKE — UNVALIDATED

Generated 2026-08-26T06:15:30Z. Overnight cap EUR 100.00; spent EUR 13.3658; remaining EUR 86.6342.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `scale-2026-08-25-sota`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: gemini, openai, anthropic, deepseek.
Providers skipped (missing key or stub): —.

### Experiment (ii) — runtime (solver)

- n scored: 12 / 12
- outcome accuracy: 1.000
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 1.000
- mean missing-fact P/R: 1.000 / 1.000
- macro missing-fact P/R: 1.000 / 1.000

### Experiment (ii) — LLM-only (all providers)

- n scored: 48 / 48
- outcome accuracy: 0.875
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.700
- mean missing-fact P/R: 1.000 / 0.854
- macro missing-fact P/R: 1.000 / 0.883

### Experiment (ii) — LLM-only `gemini`

- n scored: 12 / 12
- outcome accuracy: 0.833
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.600
- mean missing-fact P/R: 1.000 / 0.833
- macro missing-fact P/R: 1.000 / 0.867

### Experiment (ii) — LLM-only `openai`

- n scored: 12 / 12
- outcome accuracy: 0.917
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.800
- mean missing-fact P/R: 1.000 / 0.875
- macro missing-fact P/R: 1.000 / 0.900

### Experiment (ii) — LLM-only `anthropic`

- n scored: 12 / 12
- outcome accuracy: 0.917
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.800
- mean missing-fact P/R: 1.000 / 0.875
- macro missing-fact P/R: 1.000 / 0.900

### Experiment (ii) — LLM-only `deepseek`

- n scored: 12 / 12
- outcome accuracy: 0.833
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 0.600
- mean missing-fact P/R: 1.000 / 0.833
- macro missing-fact P/R: 1.000 / 0.867

### Experiment (i) — encoding

_No extraction rows._

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).
