# statute-decider v2 — refactor plan (draft for operator review)

Date: 2026-09-01. Trigger: the 1 Sep supervision settled the experimental design (conditions matrix, per-class F1 metrics), and the current repo has outgrown its shape — a flat `framework/` of 30+ modules plus an `experiments/` folder mixing scripts, configs, logs, ledger, and results with ad-hoc naming. Operator requirements: proper software structure, modularity, findability; parallel execution across provider/model combinations with a sequential option retained; a provider-agnostic LLM client reusable in future projects.

## 1. Design principles

1. **The experiment is data, not code.** A run is a YAML config naming cells of the condition matrix; adding a condition or model never means writing a new one-off script.
2. **Conditions mirror the supervision matrix.** A condition is a triple: `rules_source` × `intent_source` × `decider` — exactly the axes Priit and Otto argue about. Paper conditions become named presets.
3. **One LLM client, many providers.** All API traffic goes through one client with pluggable provider adapters; budget, ledger, retries, and rate limits are client middleware, not per-script copy-paste.
4. **Parallel by default, sequential by flag.** The runner executes the task grid concurrently with bounded per-provider concurrency; `--sequential` (or `concurrency: 1`) preserves today's behavior for debugging and rate-limit emergencies.
5. **Append-only, resume-safe, budget-capped** — keep the current run protocol (rows keyed by condition/scenario/repeat/provider/model; ledger re-ingest; hard EUR cap) as invariants with tests.
6. **Reproducibility pins.** The paper cites a commit; v2 must reproduce recorded results from recorded artifacts (golden tests) before it replaces v1.

## 2. Target layout

```
statute-decider/
  pyproject.toml              # package metadata, deps, console entry point `sd`
  README.md                   # what it is, how to run one experiment, layout map
  src/statute_decider/
    core/                     # schemas.py (DomainArtifact, IntentArtifact, ...), use_cases.py, scenarios.py, gold.py
    solver/                   # solve.py (Z3 default), trace.py, reasoners/ (z3, pysat, clingo, horn — optional extras)
    steps/                    # intent_extraction.py, domain_extraction.py (selection, synthesis), llm_decider.py
    llm/                      # provider-agnostic client (see §3) — future standalone package
    experiments/              # conditions.py (registry), runner.py, scoring.py (incl. per-class F1), configs.py
    reporting/                # summaries.py, tables.py (md + LaTeX emitters for the paper)
  configs/                    # run configs (YAML), models.yaml, prices.yaml
  data/
    fragments/                # statute texts + reference encodings + catalogs (from framework/examples)
    gold/                     # scenario suites + gold labels
    mockdb/
  results/                    # results/<YYYYMMDD-name>/ : config snapshot, rows.jsonl, summary.md, ledger slice
  docs/                       # this plan, architecture notes, POC history
  tests/                      # unit + golden tests (reproduce recorded paper rows bit-for-bit)
  legacy/                     # v1 framework/ + experiments/ frozen read-only until deletion
```

Naming conventions: run IDs `YYYYMMDD-<purpose>` (e.g. `20260901-oracle-llm`); one results dir per run; no loose logs at repo root; scripts only as thin entry points (`sd run configs/20260903-rows25.yaml`).

## 3. LLM client (`statute_decider.llm`, future `llmkit`)

The reusable piece. Kept in-tree until stable, then extracted to its own repo for other projects.

- **Interface:** `Client.complete(req) -> Response` and `Client.structured(req, schema) -> ParsedResponse` for single calls; `Client.run(requests, mode="parallel"|"sequential", concurrency=...) -> list[Result]` for grids. Results preserve request order; individual failures return error results, never raise out of the batch.
- **Model registry** (`configs/models.yaml`): provider, API model id, display name, prices, structured-output capability, max concurrency. Experiments reference registry keys ("haiku-4.5"), never raw API ids.
- **Provider adapters:** anthropic, openai, gemini, deepseek behind one `Provider` protocol (auth, request shaping, structured-output mode, usage extraction). Adding a provider = one adapter file + registry entries.
- **Execution:** asyncio core with a sync facade; per-provider semaphores (parallelism across providers multiplies throughput without tripping any single provider's rate limit); exponential backoff on 429/5xx/timeouts; per-call timeout; deterministic seeds where supported.
- **Middleware:** budget guard (worst-case pre-check, hard halt), append-only ledger at dated prices, structured logging of every call (model, latency, tokens, EUR).
- **Non-goals for now:** streaming, tool use, multimodal — add when a future project needs them.

Expected practical win: the 1,880-call grid that takes ~2h sequentially compresses to roughly the slowest single provider's share (~25–35 min at concurrency 4×N), and mixed-provider matrices no longer serialize.

## 4. Experiment engine

- **Condition registry:**

| preset | rules_source | intent_source | decider |
|---|---|---|---|
| `solver-validation` | reference | gold (hand) | solver |
| `architecture` (paper rows 2–5) | reference | llm | solver |
| `llm-only` (baseline) | none | llm-implicit | llm |
| `oracle-rules-llm` (analysis) | reference | gold | llm |
| `selected-solver` (legacy/future) | llm_selection | gold | solver |
| `synthesis-solver` (legacy/future) | llm_synthesis | gold | solver |

- **Run config:** cells (condition × model list), scenarios, repeats, budget EUR, concurrency, output dir. Config snapshot is copied into the results dir.
- **Scoring:** three-class outcome match; **per-class F1 (one-vs-rest) as the headline per-class metric** (1 Sep decision); missing-fact set P/R computed and stored but no longer headline; per-model aggregation with repeat variance.
- **Reporting:** `sd report <run-id>` emits summary.md and the LaTeX rows for the paper table — the manual copy-into-Overleaf step becomes a paste of generated rows.

## 5. Migration phases (deadline-aware)

- **Phase 0 — this week, on v1, frozen:** everything the 13 Sep submission needs runs on the current stack (pinned commit for the paper): the new rows-2–5 condition (reference rules + LLM intent + solver), per-class F1 recompute of all existing tables. No refactor risk touches the paper.
- **Phase 1 — scaffold (can start in parallel):** pyproject + `src/` package + LLM client + port of core/solver with unit tests. Golden test: replay recorded selection outputs and reproduce the composed primary-cell rows exactly.
- **Phase 2 — engine:** condition registry, runner, scoring (F1), reporting; golden tests reproduce the paper's summary tables from recorded JSONLs.
- **Phase 3 — cutover (post-submission):** tag `jurix-2026-submission` at the paper pin; move v1 to `legacy/`; README rewrite; delete after one grace period.
- **Phase 4 — new science on v2:** the feedback-loop extraction experiments (solver output fed back for remap/regeneration — Priit: immediately post-submission) land as new conditions, not new scripts.

## 6. Open questions for the operator

1. Package/tool name: `statute_decider` with `sd` CLI? The future extracted client's name (`llmkit`? `provideragnostic`? bikeshed later)?
2. Results in git: keep (current practice, nice provenance) or move to LFS/releases as they grow?
3. Dependency manager: plain `requirements.txt` today — adopt `uv` + `pyproject.toml`?
4. Phase 1 timing: start now in parallel with paper week, or strictly after 13 Sep? (Plan assumes "start now, touch nothing the paper pins".)
5. Non-Z3 reasoners (pysat, clingo, horn): port as optional extras or park in `legacy/`?
