# statute-decider

A neurosymbolic decision tool for statutory law. It extracts boolean rules and
claims from statute and case text (LLM-assisted, with provenance), then decides
**ALLOW / DENY / NEED_MORE_INFO** with a solver-backed reasoner: visible
variables, a full trace, and explicit missing-fact sets. The LLM never has
final authority over the outcome.

Research software (Mättas / Järv / Tammet, TalTech). The current manuscript
that uses this tool is
[`MattasJarvTammet-2026-NeSy-Statute-Logic`](https://github.com/ottomattas/MattasJarvTammet-2026-NeSy-Statute-Logic).
Cite this repository at a pinned commit from any paper that depends on it.

## Requirements

- Python ≥ 3.10 (3.12 recommended; `uv` or a system interpreter both work)
- No API key for the deterministic suite and unit tests
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` only for live extraction (steps 1–2)

Copy `.env.example` to `.env` (gitignored) if you will run live extraction.

## Quick start

From the repository root:

```bash
uv venv --python 3.12 framework/venv   # or: python3.12 -m venv framework/venv
framework/venv/bin/pip install -r framework/requirements.txt
framework/venv/bin/python -m unittest discover -s framework/tests -v
framework/venv/bin/python framework/run_scenarios.py --scenario allow --mode deterministic
```

The last command writes a traced ALLOW/DENY/NEED_MORE_INFO decision for the
§ 120 family-law demo. Full CLI: `framework/README.md`. Architecture and
schema: `docs/README.md`.

## Layout

| Path | Purpose |
|------|---------|
| `framework/` | Four-step CLI, scenario runner, reasoner backends (Z3, clingo, PySAT, Horn), examples, tests |
| `docs/` | Architecture, schema, reasoner semantics, ADRs |
| `.github/workflows/ci.yml` | Unit tests, scenario suite, truth-table check on Python 3.12 |
