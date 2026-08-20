# SMOKE — UNVALIDATED

Generated 2026-08-20T19:52:08Z. Overnight cap EUR 10.00; spent EUR 0.0000; remaining EUR 10.0000.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `smoke-2026-08-20`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: (none — runtime only).
Providers skipped (missing key or stub): gemini, openai, anthropic, deepseek.

### Experiment (ii) — runtime (solver)

- n scored: 47 / 47
- outcome accuracy: 1.000
- ALLOW accuracy: 1.000
- DENY accuracy: 1.000
- NEED_MORE_INFO accuracy: 1.000
- mean missing-fact P/R: 0.936 / 1.000
- macro missing-fact P/R: 0.929 / 1.000

### Experiment (ii) — LLM-only

_No LLM rows (no keys, skipped, or runtime-only)._

### Experiment (i) — encoding

_No extraction rows._

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).

## Overnight notes

- No `GEMINI_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `DEEPSEEK_API_KEY`
  in the process environment or repo `.env`. LLM-only and synthesis cells are
  empty on purpose, not failed calls.
- Precision 0.00 on `consumer_withdrawal_allow_via_db`,
  `land_tax_allow_via_db`, `building_permit_allow_via_db`: gold missing-fact
  set is empty (ALLOW) but the solver still listed premises. Those three are
  `gold_confidence: low` (do not treat as publication gold).
- `section_120_demo/prompt-swap` is also `gold_confidence: low`.
- Outcome accuracy 1.000 on 47/47 is the solver matching its own gold
  outcomes. That is a sanity check on the instrument, not a scientific result.
