# Development Guide

## Repository surfaces

This compendium currently has four main working surfaces:

| Surface | Path | Role |
|---------|------|------|
| Implementation | `framework/` | Current CLI, examples, symbolic solver, and tests. |
| Documentation | `docs/` | Canonical docs and architecture records. |
| Paper | `paper/` | Thesis and paper sources. |
| WIP | `wip/` | Local working material such as supervision notes and transcript-derived artifacts. |

**Scheduling** lives in **Linear** (or your named tracker), not only in the repo. When scope is broad, default to the active implementation in `framework/` and update `docs/` alongside it as needed.

## Environment

Keep the Python environment in `framework/venv`, but prefer running commands from the repo root:

```bash
python3 -m venv framework/venv
source framework/venv/bin/activate
pip install -q -r framework/requirements.txt
```

## Default commands

Core validation commands from the repo root:

```bash
source framework/venv/bin/activate
python -m unittest discover -s framework/tests -v
python framework/run_scenarios.py --scenario allow --mode deterministic
```

The scenario runner doubles as a lightweight end-to-end smoke test for the current CLI workflow.

## Change discipline

- Keep LLM output structured and solver authority deterministic.
- Keep the runnable surface file-backed and auditable: use-case definitions belong in `framework/examples/`, not hardcoded Python modules.
- Keep the implementation as use-case agnostic as the current schema supports by externalizing vocabulary, prompts, and scenarios.
- When changing schema, reasoner, workflow, or CLI semantics, update the matching reference document in `docs/reference/` or `docs/guides/` in the same work unit.

## Validation

For normal implementation work:

1. activate `framework/venv`
2. run the focused validation commands from the repo root
3. review changed docs for public-safe phrasing

## Commit cadence

When the user requests commits for a larger rewrite, prefer one signed commit per completed phase rather than one large end-state commit. Update the relevant tracker issue after each committed phase.

Keep signing enabled. If `git commit` fails in a sandboxed agent session because GPG or keybox access is blocked, retry the same commit outside the sandbox rather than disabling signing or changing git config.
