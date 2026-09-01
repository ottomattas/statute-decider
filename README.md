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
to every node; the three committed conditions are **solver-validation**
(all-oracle trusted path), **baseline** (LLM-only source→trace), and
**candidate** (the proposed architecture).

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

.venv/bin/pytest -q               # full test suite, incl. 47-scenario solver validation
.venv/bin/sd validate             # data inventory + schema check
.venv/bin/sd matrix export        # regenerate docs/matrix.csv (the experiment menu)

# run the free committed condition end to end
.venv/bin/sd run --experiment experiments/20260901-solver-validation --execution sequential --models all
```

LLM experiments are budget-capped and parallel by default; every run writes
`results/rows.jsonl`, per-node recordings, a cost ledger, and `summary.md`
into its experiment folder.

## Layout

```
src/statute_decider/   the package: core schemas, solvers, llm client, nodes, runner, cli
configs/conditions/    method-per-node bindings (solver-validation, baseline, candidate)
configs/llm/           model registry + prices
prompts/<node>/        versioned prompt templates (new wording = new file)
data/statutes/         statute text + oracle terms/rules, stored once
data/registers/        register schemas + oracle field-to-term maps, stored once
data/cases/            thin assemblies: utterances, registry state, scenarios, oracle values
experiments/           one folder per run: experiment.yaml + results/ + analysis/
docs/matrix.csv        generated experimentation matrix (sd matrix export)
docs/refactor-v2-plan.md  the design document for this architecture
tools/                 one-off authoring scripts (e.g. v1 → v2 data migration)
```

## How to experiment

Copy `experiments/_template/`, name the folder `<YYYYMMDD>-<slug>`, point
`experiment.yaml` at a condition, cases, models, and prompts, set a budget,
and `sd run --experiment <folder>`. The run snapshots its resolved config, so
old experiments stay interpretable after configs change.
