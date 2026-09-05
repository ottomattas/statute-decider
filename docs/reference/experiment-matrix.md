# JURIX 2026 experiment matrix

Locked with Priit 2026-08-18. This file is the table he can argue with.
Smoke numbers from the overnight build are labeled **SMOKE — UNVALIDATED**
and must not be quoted as results.

Paper: `MattasJarvTammet-2026-NeSy-Statute-Logic`.
Tool commit is pinned in `article.tex` after a run.

> **Id rename 2026-09-05.** This document predates the v2 tree and the
> 2026-09-05 rename. Where it names ids, the current names are used below
> and the pre-rename names are in `docs/reference/id-aliases.md`. The
> conditions of this matrix map to `configs/conditions/`: *runtime* →
> `solver-validation` / `architecture`, *LLM-only* → `llm-only`; the encoding
> experiment (i) has no committed condition yet.

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
| `child_representation_by_one_parent` (Family Law Act § 120) | 7 | promoted overnight; audit `gold_confidence` |
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
| **LLM-only** | No solver; **one** structured call returning `{steps[], outcome, missing_terms[], justification}` (Ruling J, 2026-09-06; `steps` before `outcome`) | same metrics |

### Justification on every row (Ruling J, 2026-09-06)

Every result row carries `justification`: a list of entries
`{source, steps, text, model?, prompt_id?, prompt_hash?}` with `source` in
`llm_inline` (the deciding model's own reasoning from its single decide call),
`solver_trace` (the rendered inference record; `outcome_trace=render`), or
`llm_post` (the optional `justify` node, `outcome_trace=llm`, which *appends*
and never overwrites). LLM-decided conditions bind `outcome_trace=passthrough`
and therefore make **exactly one call per scenario**; before 2026-09-06 the
`llm-only` condition made two (decide + justify), so per-row cost for that
cell roughly halves and older `llm-only` ledgers count 2 calls per row. The
`justify` node is not part of either default pipeline.

### Statute input (Ruling H, 2026-09-06)

Prompts receive the whole act when it fits `max_statute_tokens` (default
100 000), otherwise the smallest official structural unit (part / chapter /
division) that contains every provision `statute.yaml` declares. On the
current corpus only the Law of Obligations Act drops below the act (to
`part_1__chp_2__dvs_4`, Part 1 General Part › Chapter 2 Contract ›
Subchapter 4 Distance Contracts, §§ 52–62, ≈13k tokens instead of ≈316k);
`sd statute-input` prints the table. Rows record
`statute_input = {act, global_id, sha256, unit, declared_provisions, tokens_estimate}`.

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

## Suite change 2026-09-05 (read before comparing tables)

Every table below this heading was produced on the **47-scenario** suite
(ALLOW 14 / DENY 12 / NEED_MORE_INFO 21) with Estonian-laced request texts.
On 2026-09-05 the suite became **54 scenarios, 18/18/18**, English-only
(five retired, twelve authored — `docs/reference/id-aliases.md` → "Retired" /
"Authored"; hand-verification: `docs/reference/gold-review-2026-09-05.md`).
Solver validation on the new suite: `experiments/20260906-solver-validation`
= 54/54, macro F1 1.000. Historical rows are kept as they are; **every LLM
cell changes** when re-run (new texts, new class prior, +7 scenarios), so do
not splice old and new numbers into one table.

## Smoke results

**SMOKE — UNVALIDATED** (generated 2026-08-21T08:18Z). Operator has not
audited `gold_confidence: low` rows or claim alignments. **Do not quote as
results.**

| Cell | n | Notes |
|---|---|---|
| runtime 3-way | 47/47 = 1.000 | ALLOW 14, DENY 12, NEED_MORE_INFO 21 (2026-09-05 suite: 54/54, 18/18/18 — see above) |
| LLM-only 3-way | 188 = 47×4 | pooled acc **0.734**; NEED_MORE_INFO 0.536 is the miss; DENY 0.938 |
| LLM-only by provider | 47 each | deepseek 0.787, anthropic 0.745, openai 0.723, gemini 0.681 |
| missing-fact P/R runtime | 0.936 / 1.000 | P gap = three low-confidence `allow_register_only*` scenarios |
| missing-fact P/R LLM-only | 0.970 / 0.785 | high precision, under-recall (they omit required facts) |
| synthesis alignment F1 | mean **0.263** (n=11) | civil ~0.48–0.56 (audit); withdrawal 0.13–0.31; §120 ~0 |
| spend EUR | **0.95 / 10.00** | no halt; Tue 25 €100 still almost intact |

Gemini `child_representation_by_one_parent` synthesis returned truncated JSON (1 failed row).
`civil_service` alignments need hand audit (near-duplicate / negated labels).

Low-confidence gold (audit before Tue 25):
`consumer_purchase_withdrawal/allow_register_only_consumer_status`,
`land_tax_home_exemption/allow_register_only_ownership_and_residence`,
`building_permit_grant/allow_register_only`,
`child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a`
(retired 2026-09-05; all four audited 2026-08-26, ALLOW/empty confirmed).

Full tables: `experiments/results/SMOKE-UNVALIDATED.md`,
`experiment_ii_llm.md`, `experiment_i.md`.
