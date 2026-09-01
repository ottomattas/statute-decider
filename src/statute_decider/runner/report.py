"""Generated experiment report: summary.md opens with the bound matrix rows —
"what did we test" is generated, never reconstructed from memory."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from statute_decider.core.provenance import utc_now
from statute_decider.runner.matrix import bound_rows
from statute_decider.runner.scoring import SCORED_CLASSES, OutcomeAggregate


def _md_table(header: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join(["---"] * len(header)) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _ledger_totals(ledger_path: Path) -> dict[str, dict[str, float]]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {"eur": 0.0, "calls": 0})
    if not ledger_path.exists():
        return totals
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        model = str(row.get("model", "?"))
        totals[model]["eur"] += float(row.get("eur") or 0.0)
        totals[model]["calls"] += 1
    return totals


def render_summary(
    *,
    experiment: dict,
    condition,
    rows: list[dict],
    results_dir: Path,
    execution: str,
) -> str:
    parts: list[str] = []
    name = experiment.get("name", "experiment")
    parts.append(f"# {name}\n")
    parts.append(f"Generated {utc_now()} — execution `{execution}`, condition `{condition.condition}`.")
    if experiment.get("question"):
        parts.append(f"\n**Question:** {experiment['question']}")

    # What we tested: the bound matrix rows.
    parts.append("\n## Bound matrix rows\n")
    binding_rows = bound_rows(condition.bindings, condition.fuse)
    parts.append(
        _md_table(
            ["node", "method", "strategy", "prompt", "solver", "fused"],
            [
                [r["node"], r["method"], r["strategy"], r["prompt"], r["solver"], r["fused"]]
                for r in binding_rows
            ],
        )
    )
    if condition.fuse:
        parts.append(f"\nFuse pairs: {condition.fuse}; logic `{condition.logic}`; loop `{condition.loop}`.")

    # Data inventory.
    scenario_keys = sorted({(r["case_id"], r["scenario_id"]) for r in rows})
    cases = sorted({case for case, _ in scenario_keys})
    parts.append(
        f"\n## Data\n\n{len(scenario_keys)} scenarios across {len(cases)} cases: "
        + ", ".join(cases)
        + "."
    )

    # Results per model x prompt combo.
    ok_rows = [r for r in rows if not r.get("error")]
    err_rows = [r for r in rows if r.get("error")]

    def group_key(row: dict) -> str:
        model = row.get("model") or "deterministic"
        prompt = ";".join(sorted((row.get("prompts") or {}).values())) or "-"
        return f"{model} | {prompt}" if prompt != "-" else model

    groups: dict[str, OutcomeAggregate] = defaultdict(OutcomeAggregate)
    for row in ok_rows:
        if row.get("score"):
            groups[group_key(row)].add(row["score"])

    parts.append("\n## Outcomes (three-way scored)\n")
    header = ["group", "n", "acc"] + [f"F1 {cls}" for cls in SCORED_CLASSES] + [
        "macro F1",
        "missing P",
        "missing R",
        "missing F1",
    ]
    table_rows = []
    for key in sorted(groups):
        summary = groups[key].summary()
        table_rows.append(
            [
                key,
                summary["n"],
                f"{summary['accuracy']:.3f}",
                *[f"{summary['per_class'][cls]['f1']:.3f}" for cls in SCORED_CLASSES],
                f"{summary['macro_f1']:.3f}",
                f"{summary['missing_precision_mean']:.3f}",
                f"{summary['missing_recall_mean']:.3f}",
                f"{summary['missing_f1_mean']:.3f}",
            ]
        )
    parts.append(_md_table(header, table_rows))

    # Per-class support (from the first group; identical across groups).
    if groups:
        first = next(iter(sorted(groups)))
        per_class = groups[first].per_class()
        support = ", ".join(f"{cls}: {per_class[cls]['support']}" for cls in SCORED_CLASSES)
        parts.append(f"\nSupport per class (per repeat-model slice): {support}.")

    # Failure patterns: scenarios with any incorrect row.
    failures: dict[str, list[str]] = defaultdict(list)
    for row in ok_rows:
        score = row.get("score") or {}
        if score and not score.get("outcome_correct", True):
            failures[f"{row['case_id']}/{row['scenario_id']}"].append(
                f"{group_key(row)}: {score.get('produced_scored_as')} != {score.get('expected_scored_as')}"
            )
    if failures:
        parts.append("\n## Failure patterns\n")
        for key in sorted(failures):
            examples = failures[key]
            parts.append(f"- `{key}` — {len(examples)} wrong rows (e.g. {examples[0]})")

    if err_rows:
        parts.append(f"\n## Errors\n\n{len(err_rows)} rows errored:\n")
        for row in err_rows[:20]:
            parts.append(
                f"- `{row['case_id']}/{row['scenario_id']}` {row.get('model') or ''}: {row['error']}"
            )

    # Cost.
    totals = _ledger_totals(results_dir / "ledger.jsonl")
    if totals:
        parts.append("\n## Cost (ledger)\n")
        parts.append(
            _md_table(
                ["model", "calls", "EUR"],
                [
                    [model, int(vals["calls"]), f"{vals['eur']:.4f}"]
                    for model, vals in sorted(totals.items())
                ],
            )
        )
        total_eur = sum(vals["eur"] for vals in totals.values())
        parts.append(f"\nTotal: EUR {total_eur:.4f}.")

    parts.append("\n---\nRows: `results/rows.jsonl`; node values: `results/nodes/`; resolved config: `results/config.snapshot.yaml`.")
    return "\n".join(parts) + "\n"
