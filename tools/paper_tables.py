"""Every number the JURIX paper quotes, computed from committed experiment folders.

    .venv/bin/python tools/paper_tables.py experiments/20260906-architecture experiments/20260906-llm-only ...

For each (experiment, model) the script prints the main-table row (n, errors, accuracy, per-class
F1, macro F1) plus the diagnostics the Results prose uses: missing-set F1 mean, fine-state
agreement, extraction quality where the rows carry it (term recall, claim accuracy), error
direction on gold NEED_MORE_INFO / DENY / ALLOW rows, trust-only rows decided anyway, and the
ledger cost. `--tex` adds ready-to-paste tabular rows in the article's column order
(model & condition & n & Acc & F1 A & F1 D & F1 N). Scoring reuses the runner's aggregate so the
figures match `results/summary.md` exactly.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from statute_decider.runner.scoring import OutcomeAggregate

DISPLAY = {
    "haiku-4.5": "Haiku~4.5",
    "deepseek-v4-flash": "DeepSeek-flash",
    "gemini-2.5-flash": "Gemini-flash",
    "gpt-5-mini": "GPT-5-mini",
    "gemini-3.1-pro": "Gemini 3.1 Pro",
    "gpt-5.6-sol": "GPT-5.6",
    "fable-5.1": "Claude Fable~5.1",
    "deepseek-v4-pro": "DeepSeek-pro",
}
MODEL_ORDER = list(DISPLAY)


def load_mechanisms() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in (ROOT / "data" / "cases").glob("*/scenarios/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        out[f"{doc['case_id']}/{doc['scenario_id']}"] = doc.get("mechanism", "")
    return out


def load_rows(folder: Path) -> list[dict]:
    path = folder / "results" / "rows.jsonl"
    if not path.exists():
        raise SystemExit(f"{path} missing")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_cost(folder: Path) -> dict[str, float]:
    path = folder / "results" / "ledger.jsonl"
    cost: dict[str, float] = defaultdict(float)
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                entry = json.loads(line)
                cost[entry["model"]] += float(entry.get("eur", 0.0))
    return cost


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def fmt(value: float | None, digits: int = 2) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def analyse(folder: Path, mechanisms: dict[str, str]) -> list[dict]:
    rows = load_rows(folder)
    cost = load_cost(folder)
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)
    condition = rows[0]["condition"] if rows else folder.name
    out = []
    for model in sorted(by_model, key=lambda m: MODEL_ORDER.index(m) if m in MODEL_ORDER else 99):
        model_rows = by_model[model]
        scored = [r for r in model_rows if r.get("score") and not r.get("error")]
        errors = len(model_rows) - len(scored)
        agg = OutcomeAggregate()
        for r in scored:
            agg.add(r["score"])
        summary = agg.summary()
        states = [r["score"]["state_correct"] for r in scored]
        term_recall = [r["term_score"]["term_recall"] for r in scored if r.get("term_score")]
        term_precision = [r["term_score"]["term_precision"] for r in scored if r.get("term_score")]
        claim_acc = [r["claim_score"]["claim_accuracy"] for r in scored if r.get("claim_score")]
        # Error direction.
        gold_need = [r for r in scored if r["score"]["expected_scored_as"] == "NEED_MORE_INFO"]
        need_decided = Counter(r["score"]["produced_scored_as"] for r in gold_need)
        gold_deny = [r for r in scored if r["score"]["expected_scored_as"] == "DENY"]
        deny_as = Counter(r["score"]["produced_scored_as"] for r in gold_deny)
        gold_allow = [r for r in scored if r["score"]["expected_scored_as"] == "ALLOW"]
        allow_as = Counter(r["score"]["produced_scored_as"] for r in gold_allow)
        trust = [
            r
            for r in scored
            if mechanisms.get(f"{r['case_id']}/{r['scenario_id']}") == "trust_only"
        ]
        trust_decided = Counter(
            r["score"]["produced_scored_as"]
            for r in trust
            if r["score"]["produced_scored_as"] != "NEED_MORE_INFO"
        )
        exact_missing = sum(1 for r in scored if r["score"]["missing_f1"] == 1.0)
        out.append(
            {
                "experiment": folder.name,
                "condition": condition,
                "model": model,
                "n": summary["n"],
                "errors": errors,
                "acc": summary["accuracy"],
                "f1": {cls: stats["f1"] for cls, stats in summary["per_class"].items()},
                "support": {cls: stats["support"] for cls, stats in summary["per_class"].items()},
                "macro_f1": summary["macro_f1"],
                "missing_f1_mean": summary["missing_f1_mean"],
                "missing_exact": exact_missing,
                "state_agreement": mean([1.0 if s else 0.0 for s in states]),
                "term_recall": mean(term_recall),
                "term_precision": mean(term_precision),
                "claim_accuracy": mean(claim_acc),
                "gold_need": len(gold_need),
                "need_decided": dict(need_decided),
                "gold_deny": len(gold_deny),
                "deny_as": dict(deny_as),
                "gold_allow": len(gold_allow),
                "allow_as": dict(allow_as),
                "trust_rows": len(trust),
                "trust_decided": dict(trust_decided),
                "eur": cost.get(model, 0.0),
            }
        )
    return out


def print_markdown(results: list[dict]) -> None:
    print(
        "| experiment | model | n | err | acc | F1 A | F1 D | F1 N | macro | miss F1 | exact miss | state | term R | claim acc | EUR |"
    )
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in results:
        print(
            f"| {r['experiment']} | {r['model']} | {r['n']} | {r['errors']} | {r['acc']:.3f} | "
            f"{r['f1'].get('ALLOW', 0):.3f} | {r['f1'].get('DENY', 0):.3f} | {r['f1'].get('NEED_MORE_INFO', 0):.3f} | "
            f"{r['macro_f1']:.3f} | {r['missing_f1_mean']:.3f} | {r['missing_exact']}/{r['n']} | "
            f"{fmt(r['state_agreement'], 3)} | {fmt(r['term_recall'], 3)} | {fmt(r['claim_accuracy'], 3)} | {r['eur']:.2f} |"
        )
    print()
    print("Error direction (scored rows):")
    for r in results:
        nd = r["need_decided"]
        decided = nd.get("ALLOW", 0) + nd.get("DENY", 0)
        print(
            f"- {r['experiment']} / {r['model']}: gold NEED {r['gold_need']} → decided {decided} "
            f"(ALLOW {nd.get('ALLOW', 0)}, DENY {nd.get('DENY', 0)}); gold DENY {r['gold_deny']} → DENY "
            f"{r['deny_as'].get('DENY', 0)}, ALLOW {r['deny_as'].get('ALLOW', 0)}, NEED {r['deny_as'].get('NEED_MORE_INFO', 0)}; "
            f"gold ALLOW {r['gold_allow']} → ALLOW {r['allow_as'].get('ALLOW', 0)}, NEED {r['allow_as'].get('NEED_MORE_INFO', 0)}, "
            f"DENY {r['allow_as'].get('DENY', 0)}; trust-only {r['trust_rows']} rows decided "
            f"{sum(r['trust_decided'].values())} (ALLOW {r['trust_decided'].get('ALLOW', 0)}, DENY {r['trust_decided'].get('DENY', 0)})"
        )


def print_tex(results: list[dict], labels: dict[str, str]) -> None:
    print()
    print("% tabular rows: model & condition & n & Acc & F1 ALLOW & F1 DENY & F1 NEED")
    for r in results:
        label = labels.get(r["experiment"], r["condition"])
        print(
            f"{DISPLAY.get(r['model'], r['model'])} & {label} & {r['n']} & {r['acc']:.2f} & "
            f"{r['f1'].get('ALLOW', 0):.2f} & {r['f1'].get('DENY', 0):.2f} & {r['f1'].get('NEED_MORE_INFO', 0):.2f} \\\\"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("experiments", nargs="+", help="experiment folders")
    parser.add_argument("--tex", action="store_true", help="also print LaTeX tabular rows")
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        metavar="FOLDER=LABEL",
        help="condition label for the tex rows (default: the condition id)",
    )
    parser.add_argument("--json", action="store_true", help="dump the raw per-model dicts")
    args = parser.parse_args()
    labels = dict(item.split("=", 1) for item in args.label)
    mechanisms = load_mechanisms()
    results: list[dict] = []
    for exp in args.experiments:
        results.extend(analyse(Path(exp), mechanisms))
    if args.json:
        print(json.dumps(results, indent=2))
        return
    print_markdown(results)
    if args.tex:
        print_tex(results, {Path(k).name: v for k, v in labels.items()})
    total = sum(r["eur"] for r in results)
    print(f"\nTotal ledger cost across the listed experiments: EUR {total:.2f}")


if __name__ == "__main__":
    main()
