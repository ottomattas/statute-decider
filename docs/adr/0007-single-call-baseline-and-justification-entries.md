# ADR 0007: The LLM-only baseline is one structured call; justification is a list of entries on every row

## Status

Accepted — 2026-09-06 (operator Ruling J)

## Context

Until this ADR the `llm-only` condition made two LLM calls per scenario: a
`decide` call returning `{outcome, missing_terms, reason}` and a `justify`
call (`outcome_trace=llm`) that wrote steps and a paragraph for the decision
already taken. Two problems:

- the baseline paid twice and the second call could not change the decision,
  so its text was a rationalisation written after the fact, not the reasoning
  that produced the outcome;
- `OutcomeTrace` held a single `steps` + `justification` string, so a row
  could carry the solver's rendered trace *or* an LLM paragraph, never both,
  and nothing on the row said which model or prompt wrote it.

The other LLM-decided conditions (`llm-only-plus-rules`, the four
`llm-decides-on-*` cells) skipped the trace altogether, so their rows had no
justification at all.

## Decision

1. **Every decide prompt returns one object, reasoning first:**
   `{"steps": [...], "outcome": ..., "missing_terms": [...], "justification": "..."}`
   with `steps` before `outcome` in the schema and in the prompt tail, and
   "Reason step by step before you decide." in the system text.
   `nodes/llm_io.DecideResponse` declares the fields in that order (the
   strict JSON schema sent to the providers preserves property order, so the
   model writes the steps before it writes the outcome). Outcome and
   `missing_terms` semantics are unchanged. `PremiseOutcome` gains `steps`; the
   inline justification is its `note`.
2. **Justification is a list of entries on every row.** `OutcomeTrace.justification`
   is `list[JustificationEntry]`, each `{source, steps, text, model?, prompt_id?,
   prompt_hash?}` with `source` in:
   - `llm_inline` — the deciding model's own steps and justification from the
     single decide call (`outcome_trace=passthrough`, new executor
     `passthrough_trace`; no call);
   - `solver_trace` — the deterministic rendering of the inference record
     (`outcome_trace=render`, as before);
   - `llm_post` — the optional `justify` node (`outcome_trace=llm`), which reads
     the utterance, the statute unit, the outcome and the row's existing entries
     and **appends** one entry; it never overwrites.
   `experiment.run_experiment` writes `row["justification"]` (the entry list)
   on every result row that has a trace.
3. **LLM-decided conditions bind `outcome_trace: passthrough`** — `llm-only`,
   `llm-only-plus-rules` and the four `llm-decides-on-*` conditions therefore
   make exactly one LLM call per scenario. The `justify` node stays in the
   capability matrix as an optional post-processing step and is part of
   neither default pipeline.

## Consequences

- Cost: the `llm-only` cell halves its call count (1 call per row instead of
  2); the cost plan in the ES report of 2026-09-06 is recomputed on that
  basis. Ledgers from runs before this date count two `llm-only` calls per row
  and store the old single-string trace schema; they are not rewritten.
- `prompts/premise_outcome/decide/*.md` (four files) change wording, so their
  `prompt_hash` changes; every cell re-run after this date is a new prompt
  version by the ledger's own account (one file per prompt, ADR-free edits are
  commits, `prompt_hash` pins the wording — Ruling K).
- `prompts/outcome_trace/justify/justify.md` takes `existing` (the row's
  entries rendered as text) instead of the decide call's `reason`.
- `TraceStep` is gone; `render_trace` and `render_trace_text` still produce
  `steps` and the joined paragraph, now inside one `solver_trace` entry.
- Tests: `tests/test_justification.py` covers the response schema and field
  order, the single call count of the `llm-only` condition through a fake
  client, the pass-through entry, and the `justify` append.
