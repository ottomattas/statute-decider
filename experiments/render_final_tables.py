"""Compute FINAL-TABLES stats for the 25 Aug scale run (contract schema).

Emits, as markdown + LaTeX-ready table bodies, per (model, condition):
n, outcome accuracy (mean ± sample std across repeats), per-class accuracy
(± std), missing-fact set precision/recall (row means), and mean cost per
case (EUR, per-call ledger mean in the run window). Also experiment (i)
synthesis/selection claim-alignment F1 tables, the SOTA slice, a cost
summary, and diagnostic blocks (repeat variance, accuracy-per-EUR,
selection-vs-synthesis delta) consumed by FINAL-TABLES.md.

Usage (from repo root):
    framework/venv/bin/python experiments/render_final_tables.py \
        --scale-dir experiments/results/scale-20260825 \
        --since 2026-08-25T00:00:00Z
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "framework"))

from experiment_ii import aggregate  # noqa: E402

CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def dedupe(rows: list[dict]) -> list[dict]:
    """Success supersedes error for the same (label, provider, model) key."""
    by_key: dict[tuple, dict] = {}
    order: list[tuple] = []
    for i, row in enumerate(rows):
        key = (row.get("scenario_label"), row.get("provider"), row.get("model")) if row.get("scenario_label") else (i,)
        if key not in by_key:
            by_key[key] = row
            order.append(key)
        elif by_key[key].get("error") or not row.get("error"):
            by_key[key] = row
    return [by_key[k] for k in order]


def mean_std(values: list[float]) -> tuple[float | None, float | None]:
    values = [v for v in values if v is not None]
    if not values:
        return None, None
    m = sum(values) / len(values)
    s = statistics.stdev(values) if len(values) > 1 else 0.0
    return m, s


def fmt_ms(m: float | None, s: float | None) -> str:
    if m is None:
        return "—"
    if s is None:
        return f"{m:.3f}"
    return f"{m:.3f} ± {s:.3f}"


def repeat_level(rows: list[dict], cls: str | None = None) -> list[float]:
    """Outcome accuracy per repeat (optionally restricted to one gold class)."""
    by_rep: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("outcome_match") is None:
            continue
        if cls is not None and r.get("expected_paper_outcome") != cls:
            continue
        by_rep[int(r.get("repeat") or 0)].append(r)
    accs = []
    for rep in sorted(by_rep):
        sub = by_rep[rep]
        accs.append(sum(1 for r in sub if r["outcome_match"]) / len(sub))
    return accs


def ledger_per_call_eur(since: str) -> dict[tuple[str, str], list[float]]:
    """{(experiment, model): [eur per call]} for ledger rows at/after since."""
    out: dict[tuple[str, str], list[float]] = defaultdict(list)
    for line in (REPO_ROOT / "experiments" / "ledger.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        row = json.loads(line)
        if str(row.get("ts") or "") < since:
            continue
        out[(str(row.get("experiment")), str(row.get("model")))].append(float(row.get("eur") or 0.0))
    return out


def ledger_condition_eur(since: str) -> dict[tuple[str, str], list[float]]:
    """{(model, condition-from-label): [eur]} for experiment-i ledger rows."""
    out: dict[tuple[str, str], list[float]] = defaultdict(list)
    for line in (REPO_ROOT / "experiments" / "ledger.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        row = json.loads(line)
        if str(row.get("ts") or "") < since or row.get("experiment") != "i":
            continue
        label = str(row.get("scenario") or "")
        parts = label.split("#")
        condition = parts[1] if len(parts) >= 3 else "?"
        out[(str(row.get("model")), condition)].append(float(row.get("eur") or 0.0))
    return out


def latex_escape(text: str) -> str:
    return text.replace("_", "\\_")


def emit_table(title: str, header: list[str], rows: list[list[str]]) -> None:
    print(f"\n### {title}\n")
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows:
        print("| " + " | ".join(row) + " |")
    print("\nLaTeX body:\n")
    print("```latex")
    for row in rows:
        print(" & ".join(latex_escape(c.replace("±", "$\\pm$")) for c in row) + " \\\\")
    print("```")


def ii_row(model: str, rows: list[dict], cost: str, with_std: bool) -> list[str]:
    scored = [r for r in rows if r.get("outcome_match") is not None]
    stats = aggregate(scored)
    n_err = len(rows) - len(scored)
    cells = [model, "llm_only", f"{stats['n_scored']}" + (f" ({n_err} err)" if n_err else "")]
    if with_std:
        cells.append(fmt_ms(*mean_std(repeat_level(rows))))
        for cls in CLASSES:
            cells.append(fmt_ms(*mean_std(repeat_level(rows, cls))))
    else:
        cells.append(fmt_ms(stats["outcome_accuracy"], None))
        for cls in CLASSES:
            cells.append(fmt_ms(stats["per_class_accuracy"].get(cls), None))
    cells += [f"{stats['mean_precision']:.3f}", f"{stats['mean_recall']:.3f}", cost]
    return cells


def runtime_row(rows: list[dict]) -> list[str]:
    stats = aggregate(rows)
    per = stats["per_class_accuracy"]
    return [
        "z3 (solver)", "runtime", str(stats["n_scored"]),
        fmt_ms(stats["outcome_accuracy"], None),
        fmt_ms(per.get("ALLOW"), None), fmt_ms(per.get("DENY"), None),
        fmt_ms(per.get("NEED_MORE_INFO"), None),
        f"{stats['mean_precision']:.3f}", f"{stats['mean_recall']:.3f}", "0.0000",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale-dir", default="experiments/results/scale-20260825")
    parser.add_argument("--since", default="2026-08-25T00:00:00Z")
    args = parser.parse_args()
    scale = Path(args.scale_dir) if Path(args.scale_dir).is_absolute() else REPO_ROOT / args.scale_dir

    costs = ledger_per_call_eur(args.since)
    header = ["model", "condition", "n", "outcome acc", "acc ALLOW", "acc DENY",
              "acc NEED_MORE_INFO", "MF precision", "MF recall", "mean cost/case (EUR)"]

    # --- experiment (ii): cheap models, runtime vs llm-only -----------------
    llm = dedupe(load_jsonl(scale / "ii" / "experiment_ii_llm.jsonl"))
    runtime = load_jsonl(scale / "ii" / "experiment_ii_runtime.jsonl")
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in llm:
        by_model[r["model"]].append(r)
    rows_out = [runtime_row(runtime)]
    for model in sorted(by_model):
        calls = costs.get(("ii", model), [])
        cost = f"{sum(calls) / len(calls):.4f}" if calls else "—"
        rows_out.append(ii_row(model, by_model[model], cost, with_std=True))
    emit_table("Experiment (ii) — runtime vs LLM-only, cheap models (± sample std across 10 repeats)",
               header, rows_out)

    # --- SOTA slice ----------------------------------------------------------
    sota_llm = dedupe(load_jsonl(scale / "sota" / "experiment_ii_llm.jsonl"))
    sota_runtime = load_jsonl(scale / "sota" / "experiment_ii_runtime.jsonl")
    by_model = defaultdict(list)
    for r in sota_llm:
        by_model[r["model"]].append(r)
    rows_out = [runtime_row(sota_runtime)]
    for model in sorted(by_model):
        calls = costs.get(("ii", model), [])
        cost = f"{sum(calls) / len(calls):.4f}" if calls else "—"
        rows_out.append(ii_row(model, by_model[model], cost, with_std=False))
    emit_table("SOTA slice (n=12, single repeat — qualitative only)", header, rows_out)

    # --- experiment (i): synthesis and selection -----------------------------
    cond_costs = ledger_condition_eur(args.since)
    i_header = ["model", "condition", "n", "align F1", "claim F1", "rule F1",
                "equiv rate", "errors", "mean cost/case (EUR)"]
    rows_out = []
    diag_f1: dict[tuple[str, str], float] = {}
    for leg, cond in (("i-synthesis", "synthesis"), ("i-selection", "selection")):
        rows = dedupe(load_jsonl(scale / leg / "experiment_i.jsonl"))
        by_model = defaultdict(list)
        for r in rows:
            by_model[r["model"]].append(r)
        for model in sorted(by_model):
            group = by_model[model]
            ok = [r for r in group if not r.get("error")]
            errs = len(group) - len(ok)

            def rep_means(key: str) -> list[float]:
                by_rep: dict[int, list[float]] = defaultdict(list)
                for r in ok:
                    v = r.get(key)
                    if isinstance(v, (int, float)):
                        by_rep[int(r.get("repeat") or 0)].append(float(v))
                return [sum(v) / len(v) for _, v in sorted(by_rep.items()) if v]

            def cell(key: str) -> str:
                return fmt_ms(*mean_std(rep_means(key)))

            calls = cond_costs.get((model, cond), [])
            # experiment (i) may make >1 provider call per case; per-case cost
            # = total window EUR / scored cases.
            cost = f"{sum(calls) / len(ok):.4f}" if calls and ok else "—"
            align_all = [r["alignment_f1"] for r in ok if isinstance(r.get("alignment_f1"), (int, float))]
            if align_all:
                diag_f1[(model, cond)] = sum(align_all) / len(align_all)
            rows_out.append([model, cond, str(len(ok)), cell("alignment_f1"),
                             cell("claim_f1"), cell("rule_f1"),
                             cell("equivalence_rate"), str(errs), cost])
    emit_table("Experiment (i) — synthesis vs selection (claim-alignment F1, ± std across 5 repeats)",
               i_header, rows_out)

    # --- cost summary ---------------------------------------------------------
    total_all = 0.0
    rows_out = []
    for (exp, model), calls in sorted(costs.items()):
        rows_out.append([exp, model, str(len(calls)), f"{sum(calls):.4f}", f"{sum(calls) / len(calls):.5f}"])
        total_all += sum(calls)
    emit_table("Cost summary — ledger rows since " + args.since,
               ["experiment", "model", "calls", "total EUR", "mean EUR/call"], rows_out)
    print(f"\nTotal EUR in window: {total_all:.4f}")

    # lifetime ledger total
    lifetime = 0.0
    for line in (REPO_ROOT / "experiments" / "ledger.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            lifetime += float(json.loads(line).get("eur") or 0.0)
    print(f"Lifetime ledger EUR (all experiments ever): {lifetime:.4f}")

    # --- diagnostics ----------------------------------------------------------
    print("\n### Diagnostics")
    print("\nSelection-vs-synthesis alignment-F1 delta per model:")
    for model in sorted({m for m, _ in diag_f1}):
        syn = diag_f1.get((model, "synthesis"))
        sel = diag_f1.get((model, "selection"))
        if syn is not None and sel is not None:
            print(f"- {model}: synthesis {syn:.3f} vs selection {sel:.3f} (delta {sel - syn:+.3f})")

    print("\nAccuracy per EUR (experiment ii, overall acc / mean cost per case):")
    llm2 = dedupe(load_jsonl(scale / "ii" / "experiment_ii_llm.jsonl"))
    by_model = defaultdict(list)
    for r in llm2:
        by_model[r["model"]].append(r)
    for model in sorted(by_model):
        scored = [r for r in by_model[model] if r.get("outcome_match") is not None]
        acc = sum(1 for r in scored if r["outcome_match"]) / len(scored)
        calls = costs.get(("ii", model), [])
        if calls:
            per_case = sum(calls) / len(calls)
            print(f"- {model}: acc {acc:.3f}, cost/case EUR {per_case:.5f}, acc-per-milli-EUR {acc / (per_case * 1000):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
