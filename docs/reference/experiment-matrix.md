# JURIX 2026 experiment matrix

Locked with Priit 2026-08-18. This file is the table he can argue with.
Smoke numbers from the overnight build are labeled **SMOKE — UNVALIDATED**
and must not be quoted as results.

Paper: `MattasJarvTammet-2026-NeSy-Statute-Logic`.
Tool commit is pinned in `article.tex` after a run.

## Claims under test

1. **Extraction vs gold.** On one hand-auditable Estonian statute slice (five
   domains + §120), how reliably can an LLM extract boolean claims and
   `allow_if_all` / `deny_if_all` rules, measured against the hand-authored
   `use_case.json` encoding.
2. **Runtime vs LLM-only.** A solver-backed runtime that decides ALLOW / DENY /
   NEED_MORE_INFO — with visible variables, a trace, and a *set* of required
   facts — compared to an LLM-only baseline given the same tasks. The LLM never
   has final authority over the runtime outcome.

Do not pre-write the contrast. If LLM-only matches the runtime on outcomes,
the paper leans on fact-set precision/recall (partial recall of a required set
is better than nothing and still legally wrong).

## Gold

| Slice | Scenarios | Gold |
|---|---|---|
| Five suite domains | 40 | `expected_outcome` + `expected_missing_facts` |
| `section_120_demo` | 7 | promoted overnight; audit `gold_confidence` |
| Paper 3-way map | scoring layer | NEED_DB / NEED_USER / NEED_EXPERT / UN* → NEED_MORE_INFO |

`gold_confidence: low` rows are solver-proposed and need operator audit before
Tue 25. They are not circular-trusted as publication gold.

## Conditions

### Experiment (i) — encoding

| Condition | What the model sees | Score |
|---|---|---|
| **synthesis** (headline) | Raw statute + outcome vocabulary only; catalog held out | claim-alignment F1; truth-table equivalence on aligned claims |
| **selection** (ablation) | Existing step-02 catalog ID filter | id-set F1 vs gold claim/rule ids |

### Experiment (ii) — decision

| Condition | Authority | Score |
|---|---|---|
| **runtime** | Deterministic solver (`z3` default) | paper 3-way accuracy; missing-fact P/R (should be ~1 on gold) |
| **LLM-only** | No solver; structured `{outcome, missing_facts[]}` | same metrics |

## Model grid (cheap first)

Overnight smoke cap **€10**. Tue 25 cap **€100**. Ollama is a stub.

| Slot | Default id | API |
|---|---|---|
| Gemini Flash | `gemini-2.5-flash` | google-genai structured JSON |
| GPT mini | `gpt-5-mini` | OpenAI Responses + json_schema |
| Claude Haiku | `claude-haiku-4-5-20251001` | Messages + output_config json_schema |
| DeepSeek Flash | `deepseek-v4-flash` | OpenAI-compatible JSON mode |
| Ollama local | stub | not called |
| SOTA slice (~5%, after Tue 25) | not in smoke | frontier only as a door-closer |

Missing API keys skip that provider; they do not halt the run.

## Metrics

- Outcome: per-class accuracy on {ALLOW, DENY, NEED_MORE_INFO} (gold is
  imbalanced; do not report a single accuracy as the headline).
- Missing facts: precision/recall of the required-fact *set*. Empty/empty = 1/1.
- Extraction: alignment F1; fraction of gold rules semantically equivalent
  under the aligned vocabulary (truth-table agree rate); skip if >6 aligned vars.
- Cost: USD and EUR from `experiments/prices.yaml` + `experiments/ledger.jsonl`.

## Repeats and spend plan

| Window | Repeats | Scope | Cap |
|---|---|---|---|
| Overnight smoke (21 Aug morning) | 1 | (ii) all gold scenarios; (i) 2–3 domains synthesis | €10 |
| Mon 24 abstract | whatever exists | numbers that exist, labeled incomplete | inside €100 |
| Tue 25 checkpoint | confirm claims | decide scale (e.g. 10 → 90) | ≤ €100 cumulative |
| After 25 Aug | scale + SOTA slice | jointly confirmed | revisit |

## How to run

```bash
# deterministic gold / runtime row (no API)
framework/venv/bin/python framework/run_scenarios.py --scenarios

# full matrix (uses FRAMEWORK_BUDGET_EUR, default 10)
framework/venv/bin/python framework/run_experiments.py --config experiments/matrix.yaml
```

Outputs: `experiments/results/*.jsonl` and generated markdown tables
(gitignored JSONL; committed summary markdown under `experiments/results/`).

## Smoke results

**SMOKE — UNVALIDATED** (generated 2026-08-20T19:52Z). Operator has not
audited `gold_confidence: low` rows or claim alignments. **Do not quote as
results.** Tool commit: `statute-decider` `97ee6e8`, pinned in `article.tex`.

| Cell | n | Notes |
|---|---|---|
| runtime 3-way | 47/47 = 1.000 | ALLOW 14, DENY 12, NEED_MORE_INFO 21; all classes 1.000 |
| LLM-only 3-way | 0 | no API keys in env or repo `.env`; providers skipped |
| missing-fact P/R runtime | mean 0.936 / 1.000 | P<1 only on three `*_allow_via_db` (gold ∅, solver listed premises; `gold_confidence: low`) |
| missing-fact P/R LLM-only | — | not run |
| synthesis alignment F1 | — | not run (same key gap) |
| spend EUR | 0.00 / 10.00 | cap unused; Tue 25 €100 still intact |

Low-confidence gold (operator audit before Tue 25):
`consumer_withdrawal_allow_via_db`, `land_tax_allow_via_db`,
`building_permit_allow_via_db`, `section_120_demo/prompt-swap`.

Full tables: `experiments/results/SMOKE-UNVALIDATED.md` and
`experiments/results/experiment_ii_runtime.md`.
