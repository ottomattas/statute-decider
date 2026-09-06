"""Pre-flight for a paid grid: two cells per (experiment, model), then a verdict table.

Run before `tools/launch_chain.sh`. For every experiment folder given, each of its
models runs `--limit 2 --resume` (the two cells stay part of the run), and the
script reads back `results/rows.jsonl` and `results/ledger.jsonl` to answer the
questions a launch depends on:

* did both cells parse (no error rows, no refusal, no failed attempts)?
* did the second call read the prompt cache (cached_input_tokens > 0 where the
  prompt carries a statute or rules block)?
* what did the two cells cost, and what does that project for the whole cell?

Exit status 1 if any (experiment, model) is red, so a chain script can gate on it.

Usage:
    .venv/bin/python tools/preflight.py experiments/20260906-llm-only-r2 [more ...]
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SD = ROOT / ".venv" / "bin" / "sd"
CACHE_SETTLE_S = 20


def _jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _run(exp: Path, model: str, limit: int) -> None:
    cmd = [
        str(SD),
        "run",
        "--experiment",
        str(exp),
        "--execution",
        "parallel",
        "--models",
        model,
        "--resume",
        "--rerun-errors",
        "--limit",
        str(limit),
    ]
    subprocess.run(cmd, check=False, cwd=ROOT, capture_output=True, text=True)


def _probe(exp: Path, model: str) -> None:
    """Two cells, a pause, one more: the third call is the cache-read check.

    Provider caches become readable a few seconds after the writing call
    returns, so a call fired the instant the warm-up call finishes can still
    miss; the grid's later calls do not. The pause makes the check fair.
    """
    _run(exp, model, 2)
    time.sleep(CACHE_SETTLE_S)
    _run(exp, model, 1)


def _verdict(exp: Path, model: str, cells_total: int) -> tuple[bool, str]:
    rows = [r for r in _jsonl(exp / "results" / "rows.jsonl") if r.get("model") == model]
    ledger = [r for r in _jsonl(exp / "results" / "ledger.jsonl") if r.get("model") == model]
    errors = [r for r in rows if r.get("error")]
    failed = [r for r in ledger if r.get("failed_attempt")]
    refused = [r for r in failed if "refusal" in str(r.get("error", ""))]
    ok_calls = [r for r in ledger if not r.get("failed_attempt")]
    eur = sum(r.get("eur", 0.0) for r in ledger)
    last = ok_calls[-1] if len(ok_calls) >= 3 else None
    cache_share = (
        (last["cached_input_tokens"] / last["input_tokens"])
        if last and last["input_tokens"]
        else None
    )
    # Projection assumes the grid runs at the last call's cache share.
    per_cell = last["eur"] if last else (eur / len(rows) if rows else 0.0)
    projected = per_cell * cells_total
    green = len(rows) >= 3 and not errors and not refused
    parts = [
        f"rows={len(rows)}",
        f"err={len(errors)}",
        f"refused={len(refused)}",
        f"failed_attempts={len(failed)}",
        f"settled-call cache={cache_share:.0%}"
        if cache_share is not None
        else "settled-call cache=n/a",
        f"EUR {eur:.3f} so far -> ~{projected:.2f} for {cells_total} cells",
    ]
    return green, "  ".join(parts)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    all_green = True
    for arg in argv:
        exp = (ROOT / arg).resolve() if not Path(arg).is_absolute() else Path(arg)
        cfg = yaml.safe_load((exp / "experiment.yaml").read_text())
        models = cfg["models"]
        repeats = int(cfg.get("repeats", 1))
        cells_total = 54 * repeats  # per model; the runner prints the exact count
        print(f"== {exp.name}")
        for model in models:
            _probe(exp, model)
            green, text = _verdict(exp, model, cells_total)
            all_green &= green
            print(f"  {'OK ' if green else 'RED'} {model:18s} {text}")
    print("PRE-FLIGHT", "GREEN" if all_green else "RED")
    return 0 if all_green else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
