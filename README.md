# statute-decider

A neurosymbolic decision tool for statutory law, structured as a five-level
decision graph:

```
source  →  term  →  premise  →  outcome  →  trace
```

Three symmetric chains feed the decision. Each chain derives shared vocabulary
(*terms*) from its source and then produces premises with a distinct epistemic
status:

| Chain | Source | Term node | Premise node | Epistemic status |
| --- | --- | --- | --- | --- |
| statute | `statute_text` | `text_term` | `term_rule` | normative |
| user | `user_utterance` | `utterance_term` | `term_claim` | asserted (defeasible) |
| register | `registry_record` | `record_term` | `term_fact` | warranted |

The chains meet in `premise_outcome` (solver-backed: ALLOW / DENY /
NEED_MORE_INFO with explicit missing-term sets) and end in `outcome_trace`
(the justification). The **warrant principle** is encoded in the types: a
claim may fire rules, but when the decision rests on unwarranted values for
register-evidence terms, the outcome is flagged unverifiable rather than
final. The LLM never has final authority over the outcome.

Every node is independently checkable: it can be bound to `oracle`
(hand-validated data), to an `llm` method, or to a deterministic method
(`solver`, `lookup`, `match`, `render`), so any step can be tested in
isolation or in propagation. Conditions (`configs/conditions/`) bind a method
to every node and are named for *who does what*: the three committed
conditions are **solver-validation** (all-oracle trusted path), **llm-only**
(LLM decides and justifies on raw sources in one structured call), and **architecture** (the proposed
architecture: LLM-extracted claims, register lookup, solver decides). Control
conditions swap the solver for an LLM on the same inputs
(`llm-decides-on-oracle-inputs-*`, `llm-decides-on-llm-claims-*`; the suffix
`partial-specification` / `full-procedure` says how much of the solver's
procedure the decide prompt states) or give the LLM the oracle rules
(`llm-only-plus-rules`).

Ids were renamed on 2026-09-05 (statutes by act, cases by service
question, scenarios as `<gold>_<mechanism>`, conditions as above). The
old → new tables, including the `u3/u5/u7/u8` legend, are in
[`docs/reference/id-aliases.md`](docs/reference/id-aliases.md); results
produced before the rename carry the new ids in their structured fields
and the old ids inside free-text prompt/response strings.

On 2026-09-05 the suite was also rebalanced and made English-only: 54
scenarios, 18 ALLOW / 18 DENY / 18 NEED_MORE_INFO (five near-duplicates
retired, twelve authored; hand-verification sheet in
[`docs/reference/gold-review-2026-09-05.md`](docs/reference/gold-review-2026-09-05.md)),
and every string a model or reader sees — request texts, term catalogues,
rule labels, register schemas, traces — is English. On 2026-09-06 the balance
was made to hold per case as well: six cases × (3 ALLOW / 3 DENY / 3
NEED_MORE_INFO) = 54 (six scenarios dropped, six authored; sheet in
[`docs/reference/gold-review-2026-09-06.md`](docs/reference/gold-review-2026-09-06.md)).
Experiment folders dated 2026-09-01 … 04 are 47-scenario history and are not
comparable cell-for-cell with runs on the 54-scenario suite; the
`20260906-*` folders written before the afternoon of 2026-09-06 saw the
per-total-only 54.

Statute texts come from the official Riigi Teataja consolidated-text XML
(`data/sources/legislation/`, 7 acts × {et, en}, byte-identical copies plus
a generated `catalogue.json`). The input to the system is the **official
text**, rendered deterministically from the XML: the whole act when it fits
the statute token budget (`max_statute_tokens`, default 100 000), otherwise
the smallest official structural unit (part / chapter / division) that
encloses every provision the statute's `statute.yaml` declares — never a
hand-made excerpt (ADR 0005; `sd statute-input` shows the choice per act).
Each statute's `statute.yaml` names the act (by `global_id`) and the
provisions its rules were written against. Statute ids are English act slugs (`land_tax_act`),
provision references are `<act_slug>/<eId>`
(`land_tax_act/sec_11__subsec_5__point_1`, displayed as `§ 11 (5) 1)`);
the RT element ids are never stored. Layout, catalogue schema and the
id bijection: [`docs/reference/legislation-corpus.md`](docs/reference/legislation-corpus.md).

Research software (Mättas / Järv / Tammet, TalTech). The current manuscript
that uses this tool is
[`MattasJarvTammet-2026-NeSy-Statute-Logic`](https://github.com/ottomattas/MattasJarvTammet-2026-NeSy-Statute-Logic).
Cite this repository at a pinned commit from any paper that depends on it.
The pre-rewrite (v1) tree is archived at the git tag `pre-refactor`.

## Requirements

- Python ≥ 3.12
- No API key for the solver-validation suite and unit tests
- Provider keys for LLM conditions: `GOOGLE_API_KEY` (or `GEMINI_API_KEY`),
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`; a missing key
  fails only the calls that need it
- Copy `.env.example` to `.env` (gitignored) for live runs

## Quick start

```bash
python3.12 -m venv .venv          # or: uv venv --python 3.12
.venv/bin/pip install -e '.[dev,solvers,llm]'

.venv/bin/pytest -q               # full test suite, incl. 54-scenario solver validation
.venv/bin/sd validate             # data inventory + schema check + every provision resolved against the XML
.venv/bin/sd corpus check         # re-hash the legislation corpus, report drift and validity windows
.venv/bin/sd statute-input --candidates   # offline: which official unit each act resolves to under the token budget
.venv/bin/sd matrix export        # regenerate docs/matrix.csv (the experiment menu)

# run the free committed condition end to end
.venv/bin/sd run --experiment experiments/20260901-solver-validation --execution sequential --models all
```

LLM experiments are budget-capped and parallel by default; every run writes
`results/rows.jsonl`, per-node recordings, a cost ledger, and `summary.md`
into its experiment folder. `results/transcript.jsonl` is the full LLM
audit trail: one entry per provider call with the rendered system and user
messages exactly as sent and the raw model response before any parsing.
Solver inputs and outputs live in `results/nodes/premise_outcome.jsonl`
(claims, facts, valuation, fired rules) and `results/nodes/outcome_trace.jsonl`.
Every row carries `justification`: a list of entries `{source, steps, text,
model?, prompt_id?, prompt_hash?}` — `llm_inline` (the deciding model's own
reasoning), `solver_trace` (rendered inference record) or `llm_post` (the
optional `justify` node, which appends; ADR 0007).

## Layout

```
src/statute_decider/   the package: core schemas, solvers, llm client, nodes, runner, cli
configs/conditions/    method-per-node bindings (solver-validation, llm-only, architecture, ...)
configs/llm/           model registry + prices
prompts/<node>/        prompt templates: one file per prompt, named for what it does; edits are
                       commits — the `prompt_hash` in the ledger pins the wording a run saw (no -vN files)
data/sources/legislation/  Riigi Teataja XML corpus + generated catalogue.json (sd corpus ingest / check)
data/statutes/         statute selection spec (statute.yaml) + rendered provisions + oracle terms/rules, stored once
data/registers/        register schemas + oracle field-to-term maps, stored once
data/cases/            thin assemblies: utterances, registry state, scenarios, oracle values
experiments/           one folder per run: experiment.yaml + results/ + analysis/
docs/matrix.csv        generated experimentation matrix (sd matrix export)
docs/architecture-plan.md  the design document for this architecture
docs/reference/id-aliases.md  old → new id tables (2026-09-05 renames)
docs/reference/legislation-corpus.md  the XML corpus, catalogue schema, reference vocabulary
tools/                 one-off authoring scripts (pre-rewrite data migration, id rename + fingerprint, vocabulary check)
```

## How to experiment

Copy `experiments/_template/`, name the folder `<YYYYMMDD>-<slug>`, point
`experiment.yaml` at a condition, cases, models, and prompts, set a budget,
and `sd run --experiment <folder>`. The run snapshots its resolved config, so
old experiments stay interpretable after configs change.
