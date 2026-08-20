# Development

## Surfaces

| Path | Role |
|------|------|
| `framework/` | CLI, examples, solvers, tests |
| `docs/` | Architecture, schema, reasoner reference, ADRs |

Run commands from the repository root. Keep the virtualenv at `framework/venv`.

## Setup

```bash
uv venv --python 3.12 framework/venv   # or: python3.12 -m venv framework/venv
framework/venv/bin/pip install -r framework/requirements.txt
cp .env.example .env                   # only if you will call a live model
```

Python ≥ 3.10 is required (`str | None` typing). 3.12 is what CI and the
maintainer venv use.

## Validate

```bash
framework/venv/bin/python -m unittest discover -s framework/tests -v
framework/venv/bin/python framework/run_scenarios.py --scenario allow --mode deterministic
```

From `framework/` you can also `make test`, `make scenarios`, and
`make truth-tables` (same commands CI runs).

Live extraction (steps 1–2) needs `GEMINI_API_KEY` or `GOOGLE_API_KEY` in the
environment. The deterministic fixtures do not.

## Change discipline

- Solver authority stays deterministic; LLM output is structured input to the solver.
- Use-case vocabulary, prompts, and scenarios live under `framework/examples/`, not in Python modules.
- Schema or reasoner changes update the matching document under `docs/reference/` or `docs/adr/` in the same work unit.
