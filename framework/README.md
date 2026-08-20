# `framework`

`framework/` is the current implementation root. It is a small four-step CLI plus a scenario runner:

1. request text -> `intent.json`
2. law text -> `domain.json`
3. `intent + domain + mock_db` -> `solution.json`
4. `solution.json` -> plain-text reasoning trace

Each use case lives under `framework/examples/` with:
- `use_case.json`
- prompt files
- request files
- law files
- mock DB data
- generated artifacts and traces

The user-facing surface is direct file-path flags plus one `--use-case-dir`. You can swap the request, law, DB, or prompt files without editing Python.

Only `propositional` is executable in this iteration. `--logic-level` exists only on steps 1 and 2. Steps 3 and 4 infer the stored `logic_level` from the artifacts.

## Environment

From the repo root:

```bash
python3 -m venv framework/venv
source framework/venv/bin/activate
pip install -q -r framework/requirements.txt
```

If `framework/venv` already exists, just activate it and reinstall requirements when dependencies change.

## Root-Run Convention

Run the CLI from the repo root by executing the scripts via their `framework/` paths. When you pass explicit files, use repo-root-relative paths such as `framework/examples/section_120_demo/law.txt`.

Step 1 and step 2 use structured Gemini output. Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` first. The experiment harness also reads `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `DEEPSEEK_API_KEY` (a missing key skips that provider). Optional model override env vars:

- `FRAMEWORK_GEMINI_MODEL`
- `FRAMEWORK_OPENAI_MODEL` (default `gpt-5-mini`)
- `FRAMEWORK_ANTHROPIC_MODEL` (default `claude-haiku-4-5-20251001`)
- `FRAMEWORK_DEEPSEEK_MODEL` (default `deepseek-v4-flash`)
- `FRAMEWORK_BUDGET_EUR` (default `10`; overnight halt)

## Fast Deterministic Run

This is the quickest walkthrough because it skips live LLM calls and regenerates deterministic artifacts.

```bash
source framework/venv/bin/activate

python framework/run_scenarios.py \
  --scenario allow \
  --mode deterministic

python framework/03_solve_case.py \
  --domain framework/examples/review_runs/scenario_suite/allow/domain.json \
  --intent framework/examples/review_runs/scenario_suite/allow/intent.json \
  --db framework/examples/section_120_demo/mock_db.json \
  --out /tmp/framework_solution.json

python framework/04_print_trace.py \
  --solution /tmp/framework_solution.json
```

## Scenario Runner

The fastest way to regenerate the stable demo bundle is:

```bash
source framework/venv/bin/activate
python framework/run_scenarios.py --mode deterministic
```

This writes:

- `framework/examples/review_runs/scenario_suite.txt`
- one subdirectory per scenario under `framework/examples/review_runs/scenario_suite/`

Stable scenario names:

- `allow`
- `deny`
- `need-db`
- `need-user`
- `db-then-user`
- `unrelated-law`
- `prompt-swap`

Use `--mode live` if you want the transcript to include actual extraction commands and live model output.

## Live Four-Step Run

```bash
source framework/venv/bin/activate

python framework/01_extract_intent.py \
  --use-case-dir framework/examples/section_120_demo \
  --text-file framework/examples/section_120_demo/request_allow.txt \
  --out /tmp/framework_intent.json

python framework/02_extract_domain.py \
  --use-case-dir framework/examples/section_120_demo \
  --law-file framework/examples/section_120_demo/law.txt \
  --out /tmp/framework_domain.json

python framework/03_solve_case.py \
  --domain /tmp/framework_domain.json \
  --intent /tmp/framework_intent.json \
  --db framework/examples/section_120_demo/mock_db.json \
  --out /tmp/framework_solution.json

python framework/04_print_trace.py \
  --solution /tmp/framework_solution.json
```

## Prompt And Law Files

Default prompt templates for the worked example live in:

- `framework/examples/section_120_demo/prompts/intent/system.propositional.txt`
- `framework/examples/section_120_demo/prompts/intent/user.txt`
- `framework/examples/section_120_demo/prompts/domain/system.propositional.txt`
- `framework/examples/section_120_demo/prompts/domain/user.txt`

Stricter user-prompt variants:

- `framework/examples/section_120_demo/prompts/intent/user.strict.txt`
- `framework/examples/section_120_demo/prompts/domain/user.strict.txt`

Alternative law files:

- `framework/examples/alternative_laws/118032026007.txt`
- `framework/examples/alternative_laws/121112025003.txt`

## Experiment harness

Matrix config: `experiments/matrix.yaml`. Overnight cap: `FRAMEWORK_BUDGET_EUR` (default 10).

```bash
# Plan only: which providers have keys, how many gold scenarios
framework/venv/bin/python framework/run_experiments.py --config experiments/matrix.yaml --dry-run

# Solver runtime rows only (no API)
framework/venv/bin/python framework/run_experiments.py --config experiments/matrix.yaml --runtime-only

# Full smoke: runtime + LLM-only + synthesis extraction, halt at the EUR cap
framework/venv/bin/python framework/run_experiments.py --config experiments/matrix.yaml
```

Markdown summaries land in `experiments/results/` (committed). JSONL rows are gitignored. Label every overnight table **SMOKE — UNVALIDATED**.

Step 2 catalog-held-out synthesis:

```bash
python framework/02_extract_domain.py \
  --use-case-dir framework/examples/section_120_demo \
  --law-file framework/examples/section_120_demo/law.txt \
  --condition synthesis \
  --provider gemini \
  --out /tmp/synthesized.domain.json
```

## Test

```bash
source framework/venv/bin/activate
python -m unittest discover -s framework/tests -v
```
