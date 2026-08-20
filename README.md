# statute-decider

A neurosymbolic decision tool for statutory law: it extracts boolean rules and claims
from statute and case text (LLM-assisted, with provenance), then decides
**ALLOW / DENY / NEED_MORE_INFO** deterministically with a solver-backed reasoner —
visible variables, full trace, and explicit missing-fact sets. The LLM never has final
authority over the outcome.

Research software for the Language-to-Logic line (Mättas / Järv / Tammet, TalTech).
Papers cite this repo at a pinned commit; the manuscript for the current paper lives in
its own repository (`MattasJarvTammet-2026-NeSy-Statute-Logic`).

## Layout

| Path | Purpose |
|------|---------|
| `framework/` | Implementation root: four-step CLI, scenario runner, reasoner backends (Z3, clingo, PySAT, Horn), examples, tests. |
| `docs/` | Canonical technical documentation and architecture decision records. |

## Quick start

From the repo root:

```bash
uv venv --python 3.12 framework/venv   # or: python3.12 -m venv framework/venv
framework/venv/bin/pip install -q -r framework/requirements.txt
framework/venv/bin/python framework/run_scenarios.py --scenario allow --mode deterministic
framework/venv/bin/python -m unittest discover -s framework/tests -v
```

Requires Python ≥ 3.10. Live extraction (steps 1–2) needs `GEMINI_API_KEY` or
`GOOGLE_API_KEY`; the deterministic scenario suite runs without any key.

See `framework/README.md` for the full CLI workflow and `docs/README.md` for the
documentation entry point.
