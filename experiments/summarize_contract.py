"""Render experiment (ii) results in the paper's results-table contract schema.

Contract (agreed with the article agent): one row per (model, condition) with
columns: model, condition, n, outcome accuracy overall, accuracy per class
(ALLOW / DENY / NEED_MORE_INFO), missing-fact set precision, missing-fact set
recall, mean cost per case (EUR).

Cost comes from ``experiments/ledger.jsonl`` filtered to a [since, until)
UTC window and experiment "ii", grouped by provider. Retried transport
failures that never returned a usable response are not in the ledger, so the
EUR column is a lower bound in the presence of retries.

Usage (from repo root), one --run per results leg:
    python experiments/summarize_contract.py \
        --run "cheap;experiments/results/scale-20260825/ii;2026-08-25T11:14;2026-08-25T23:59" \
        --run "sota;experiments/results/scale-20260825/sota;2026-08-25T11:14;2026-08-26T23:59" \
        --out experiments/results/contract-tables.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "framework"))

from experiment_ii import aggregate  # noqa: E402

CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")
HEADER = (
    "| model | condition | n | outcome acc | acc ALLOW | acc DENY | "
    "acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |"
)
SEP = "|---|---|---|---|---|---|---|---|---|---|"


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def ledger_cost_by_provider(
    since: str, until: str, model_map: dict[str, str] | None = None
) -> dict[str, tuple[float, str]]:
    """{provider: (total_eur, model)} for experiment-ii rows in the window.

    With ``model_map`` (provider -> expected model id) only matching rows
    count, so overlapping windows of cheap and SOTA legs cannot cross-bill.
    """
    out: dict[str, list] = defaultdict(lambda: [0.0, ""])
    ledger = REPO_ROOT / "experiments" / "ledger.jsonl"
    for line in ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        row = json.loads(line)
        if row.get("experiment") != "ii":
            continue
        if not (since <= row["ts"] < until):
            continue
        provider = row["provider"]
        if model_map is not None and row.get("model") != model_map.get(provider):
            continue
        entry = out[provider]
        entry[0] += float(row.get("eur") or 0.0)
        entry[1] = row.get("model") or entry[1]
    return {k: (v[0], v[1]) for k, v in out.items()}


def fmt(value) -> str:
    return "—" if value is None else f"{value:.3f}"


def contract_rows(
    tag: str,
    results_dir: Path,
    since: str,
    until: str,
    model_map: dict[str, str] | None = None,
) -> list[str]:
    lines: list[str] = [f"## Run `{tag}` — `{results_dir}`", ""]
    runtime_rows = load_jsonl(results_dir / "experiment_ii_runtime.jsonl")
    llm_rows = load_jsonl(results_dir / "experiment_ii_llm.jsonl")
    if not runtime_rows and not llm_rows:
        lines += ["_No rows yet (run still in progress?)._", ""]
        return lines

    costs = ledger_cost_by_provider(since, until, model_map)
    lines += [HEADER, SEP]

    if runtime_rows:
        stats = aggregate(runtime_rows)
        per = stats["per_class_accuracy"]
        lines.append(
            f"| z3 (solver) | runtime | {stats['n_scored']} | "
            f"{fmt(stats['outcome_accuracy'])} | {fmt(per.get('ALLOW'))} | "
            f"{fmt(per.get('DENY'))} | {fmt(per.get('NEED_MORE_INFO'))} | "
            f"{fmt(stats['mean_precision'])} | {fmt(stats['mean_recall'])} | 0.0000 |"
        )

    by_provider: dict[str, list[dict]] = defaultdict(list)
    for row in llm_rows:
        by_provider[row.get("provider") or "?"].append(row)
    for provider in sorted(by_provider):
        rows = by_provider[provider]
        scored = [r for r in rows if r.get("outcome_match") is not None]
        stats = aggregate(scored)
        per = stats["per_class_accuracy"]
        eur, model = costs.get(provider, (0.0, provider))
        n_errors = len(rows) - len(scored)
        mean_cost = eur / len(rows) if rows else 0.0
        model_label = model or provider
        err_note = f" ({n_errors} err)" if n_errors else ""
        lines.append(
            f"| {model_label} | llm_only | {stats['n_scored']}{err_note} | "
            f"{fmt(stats['outcome_accuracy'])} | {fmt(per.get('ALLOW'))} | "
            f"{fmt(per.get('DENY'))} | {fmt(per.get('NEED_MORE_INFO'))} | "
            f"{fmt(stats['mean_precision'])} | {fmt(stats['mean_recall'])} | "
            f"{mean_cost:.4f} |"
        )
    lines.append("")
    return lines


def extraction_rows(tag: str, results_dir: Path) -> list[str]:
    rows = load_jsonl(results_dir / "experiment_i.jsonl")
    if not rows:
        return []
    lines = [
        f"## Experiment (i) `{tag}` — `{results_dir}` (secondary; not in the contract schema)",
        "",
        "| provider | condition | n | mean align F1 | mean claim F1 | mean rule F1 | mean equiv rate | errors |",
        "|---|---|---|---|---|---|---|---|",
    ]
    by_provider: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        by_provider[(row.get("provider") or "?", row.get("condition") or "?")].append(row)

    def mean(vals):
        vals = [v for v in vals if isinstance(v, (int, float))]
        return f"{sum(vals) / len(vals):.3f}" if vals else "—"

    for (provider, condition) in sorted(by_provider):
        group = by_provider[(provider, condition)]
        ok = [r for r in group if not r.get("error")]
        errors = len(group) - len(ok)
        lines.append(
            f"| {provider} | {condition} | {len(ok)} | "
            f"{mean(r.get('alignment_f1') for r in ok)} | "
            f"{mean(r.get('claim_f1') for r in ok)} | "
            f"{mean(r.get('rule_f1') for r in ok)} | "
            f"{mean(r.get('equivalence_rate') for r in ok)} | {errors} |"
        )
    lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        metavar="TAG;DIR;SINCE;UNTIL[;MAP]",
        help=(
            "tag;results_dir;since_ts;until_ts[;provider=model,provider=model] "
            "(UTC prefixes, repeatable; MAP restricts ledger cost rows)"
        ),
    )
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Results tables — contract schema (model, condition)",
        "",
        "**UNVALIDATED until gold `low` rows are operator-audited.** "
        "Do not quote as results.",
        "",
        f"Generated {generated} by `experiments/summarize_contract.py`.",
        "",
        "Schema notes:",
        "",
        "- `n` counts scored rows (cases x repeats); `(k err)` marks rows that",
        "  errored after transport retries and are excluded from accuracy.",
        "- `MF precision/recall` are row-mean missing-fact set scores"
        " (empty gold vs empty prediction scores 1/1).",
        "- `mean cost/case (EUR)` divides ledger EUR for the run window by all",
        "  attempted rows; runtime (solver) rows cost 0 by construction.",
        "- Tokens burned by calls that failed all transport retries never reach",
        "  the ledger, so EUR is a lower bound under retries.",
        "- Per-class accuracy is `—` when the slice has no gold rows of that class.",
        "",
    ]
    for item in args.run:
        parts = item.split(";")
        tag, dir_str, since, until = parts[0], parts[1], parts[2], parts[3]
        model_map = None
        if len(parts) > 4 and parts[4]:
            model_map = dict(pair.split("=", 1) for pair in parts[4].split(","))
        results_dir = Path(dir_str)
        lines += contract_rows(tag, results_dir, since, until, model_map)
        lines += extraction_rows(tag, results_dir)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
