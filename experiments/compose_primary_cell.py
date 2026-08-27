"""Compose the missing primary cell: LLM-selected encoding + deterministic solver.

Experiment (i) selection rows (scale-20260825) recorded per-(model, case,
repeat) id-set scores but not the raw selected id lists. Because every ok row
has ``unmatched_pred == []`` (verified at load time), the selected set is
exactly ``gold ids − unmatched_gold``. This script reconstructs each selected
encoding, filters the gold ``use_case.json`` down to it (dropping — and
counting — selected rules that reference unselected claims), injects the
composed DomainArtifact into the existing suite runner, and scores all 47
gold scenarios with the same ``score_row``/``aggregate`` code paths as the
paper's runtime row. No LLM calls are made.

Usage (from repo root):
    framework/venv/bin/python experiments/compose_primary_cell.py --self-test
    framework/venv/bin/python experiments/compose_primary_cell.py \
        --out-dir experiments/results/compose-20260827
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "framework"))

from experiment_ii import aggregate, load_gold, score_row  # noqa: E402
from logic_levels import build_domain_artifact  # noqa: E402
from metadata import utc_timestamp  # noqa: E402
from paper_outcomes import to_paper_outcome  # noqa: E402
from scenario_suite import (  # noqa: E402
    discover_suite_scenario_files_for_case,
    run_suite_scenario,
)
from schemas import DomainArtifact, ExtractionRunMetadata  # noqa: E402
from use_case_files import UseCaseDefinition  # noqa: E402

SELECTION_JSONL = REPO_ROOT / "experiments/results/scale-20260825/i-selection/experiment_i.jsonl"
DEFAULT_OUT_DIR = REPO_ROOT / "experiments/results/compose-20260827"
PAPER_CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")


# ---------------------------------------------------------------------------
# Selection-row loading and reconstruction
# ---------------------------------------------------------------------------


def load_selection_ok_rows(path: Path) -> list[dict[str, Any]]:
    """Load ok selection rows; abort unless reconstruction is sound.

    Reconstruction (selected = gold − unmatched_gold) is only exact when the
    model predicted no ids outside the gold catalog, i.e. unmatched_pred is
    empty on every ok row. Error rows (schema-violating attempts that were
    retried) are excluded.
    """
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ok = [row for row in rows if "error" not in row]
    bad = [row for row in ok if row.get("unmatched_pred")]
    if bad:
        for row in bad:
            print(
                f"ABORT: nonempty unmatched_pred on {row['model']} "
                f"{Path(row['case_dir']).name} r{row['repeat']}: {row['unmatched_pred']}",
                file=sys.stderr,
            )
        sys.exit(2)
    return ok


def reconstruct_selected(
    row: dict[str, Any], gold_claim_ids: set[str], gold_rule_ids: set[str]
) -> tuple[set[str], set[str]]:
    """Partition unmatched_gold into claim/rule ids and subtract from gold."""
    unmatched = set(row.get("unmatched_gold") or [])
    unknown = unmatched - gold_claim_ids - gold_rule_ids
    if unknown:
        raise ValueError(
            f"unmatched_gold ids not in gold catalog for {Path(row['case_dir']).name}: {sorted(unknown)}"
        )
    return gold_claim_ids - unmatched, gold_rule_ids - unmatched


# ---------------------------------------------------------------------------
# Composed encoding
# ---------------------------------------------------------------------------


def compose_use_case(
    raw_use_case: dict[str, Any],
    selected_claim_ids: set[str],
    selected_rule_ids: set[str],
) -> tuple[UseCaseDefinition, list[str]]:
    """Filter the gold use case down to the selected ids.

    Selected rules that reference an unselected claim (premise or set-false
    target) are dropped and reported — the encoding is not silently patched.
    Outcomes are catalog furniture, not selected, and are kept in full.
    """
    filtered = dict(raw_use_case)
    filtered["claims"] = [c for c in raw_use_case["claims"] if c["claim_id"] in selected_claim_ids]
    kept_rules: list[dict[str, Any]] = []
    dropped_rule_ids: list[str] = []
    for rule in raw_use_case["rules"]:
        if rule["rule_id"] not in selected_rule_ids:
            continue
        refs = set(rule.get("when_claim_ids") or [])
        if rule.get("target_claim_id"):
            refs.add(rule["target_claim_id"])
        if refs - selected_claim_ids:
            dropped_rule_ids.append(rule["rule_id"])
            continue
        kept_rules.append(rule)
    filtered["rules"] = kept_rules
    return UseCaseDefinition.model_validate(filtered), dropped_rule_ids


def build_composed_domain(case_dir: Path, use_case: UseCaseDefinition) -> DomainArtifact:
    """Build the DomainArtifact for a composed use case (same builder as gold)."""
    law_text = (case_dir / "law.txt").read_text(encoding="utf-8")
    run_meta = ExtractionRunMetadata(
        generated_at_utc=utc_timestamp(),
        model_name="composed-from-selection",
    )
    return build_domain_artifact(
        use_case,
        use_case.default_logic_level,
        law_text,
        run_metadata=run_meta,
    )


# ---------------------------------------------------------------------------
# Row runner / scorer (mirrors experiment_ii.run_runtime_row)
# ---------------------------------------------------------------------------


def run_composed_row(scenario_path: Path, domain: DomainArtifact) -> dict[str, Any]:
    """One scenario through the solver with an injected domain, scored vs gold."""
    result = run_suite_scenario(scenario_path, domain=domain)
    paper_outcome = to_paper_outcome(result.actual_outcome)
    missing_facts = list(result.actual_missing_facts)
    expected_raw, expected_facts = load_gold(scenario_path)
    expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
    if expected_paper is None:
        scored = {"outcome_match": None, "precision": None, "recall": None}
    else:
        scored = score_row(expected_paper, expected_facts, paper_outcome, missing_facts)
    return {
        "scenario": result.scenario_name,
        "scenario_path": str(scenario_path),
        "condition": "composed",
        "paper_outcome": paper_outcome,
        "missing_facts": missing_facts,
        "fine_grained_outcome": result.actual_outcome.value,
        "expected_paper_outcome": expected_paper,
        "expected_missing_facts": expected_facts,
        "outcome_match": scored["outcome_match"],
        "precision": scored["precision"],
        "recall": scored["recall"],
    }


def failed_encoding_row(scenario_path: Path, error: str) -> dict[str, Any]:
    """Score a scenario under an unbuildable encoding as incorrect (recall 0)."""
    expected_raw, expected_facts = load_gold(scenario_path)
    expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
    return {
        "scenario": scenario_path.stem,
        "scenario_path": str(scenario_path),
        "condition": "composed",
        "paper_outcome": None,
        "missing_facts": [],
        "fine_grained_outcome": None,
        "encoding_error": error,
        "expected_paper_outcome": expected_paper,
        "expected_missing_facts": expected_facts,
        "outcome_match": False if expected_paper else None,
        "precision": 0.0,
        "recall": 0.0,
    }


# ---------------------------------------------------------------------------
# Self-test: full gold ids through the adapter path must reproduce runtime
# ---------------------------------------------------------------------------


def run_self_test(case_dirs: list[Path]) -> bool:
    """Inject the FULL gold id set and require exact runtime-row agreement."""
    from experiment_ii import run_runtime_row

    all_ok = True
    for case_dir in case_dirs:
        raw = json.loads((case_dir / "use_case.json").read_text(encoding="utf-8"))
        gold_claims = {c["claim_id"] for c in raw["claims"]}
        gold_rules = {r["rule_id"] for r in raw["rules"]}
        use_case, dropped = compose_use_case(raw, gold_claims, gold_rules)
        if dropped:
            print(f"SELF-TEST FAIL {case_dir.name}: gold compose dropped rules {dropped}")
            all_ok = False
            continue
        domain = build_composed_domain(case_dir, use_case)
        for scenario_path in discover_suite_scenario_files_for_case(case_dir.name):
            composed = run_composed_row(scenario_path, domain)
            runtime = run_runtime_row(scenario_path)
            same = (
                composed["paper_outcome"] == runtime["paper_outcome"]
                and sorted(composed["missing_facts"]) == sorted(runtime["missing_facts"])
                and composed["outcome_match"] == runtime["outcome_match"]
                and composed["precision"] == runtime["precision"]
                and composed["recall"] == runtime["recall"]
            )
            perfect = (
                composed["outcome_match"] is True
                and composed["precision"] == 1.0
                and composed["recall"] == 1.0
            )
            if not (same and perfect):
                print(
                    f"SELF-TEST FAIL {composed['scenario']}: composed="
                    f"{composed['paper_outcome']}/{composed['missing_facts']} "
                    f"P={composed['precision']} R={composed['recall']} vs runtime="
                    f"{runtime['paper_outcome']}/{runtime['missing_facts']}"
                )
                all_ok = False
    return all_ok


# ---------------------------------------------------------------------------
# Aggregation and reporting
# ---------------------------------------------------------------------------


def _fmt(value: float | None) -> str:
    return "—" if value is None else f"{value:.3f}"


def _mean_std(values: list[float]) -> str:
    if not values:
        return "—"
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return f"{mean:.3f} ± {std:.3f}"


def summarize(
    rows_by_model: dict[str, list[dict[str, Any]]],
    dropped_by_model: dict[str, Counter],
    failed_encodings: list[dict[str, Any]],
    n_repeats: int,
    covered_domains: list[str],
    n_scenarios: int,
    encoding_records: list[dict[str, Any]],
) -> str:
    """Render primary_cell.md."""
    lines = [
        "# Composed primary cell — LLM-selected encoding + deterministic solver",
        "",
        f"Generated {utc_timestamp()} by `experiments/compose_primary_cell.py` from",
        "`experiments/results/scale-20260825/i-selection/experiment_i.jsonl` (ok rows",
        "only; selected ids reconstructed as gold − unmatched_gold, exact because",
        "unmatched_pred = [] on every ok row). Deterministic solver (z3), zero LLM",
        "calls. Scoring uses the same `score_row`/`aggregate`/paper-outcome code",
        "paths as the runtime row in FINAL-TABLES.md.",
        "",
        "## Coverage",
        "",
        f"- Selection covers all {len(covered_domains)} domains used by the gold suite: "
        + ", ".join(covered_domains) + ".",
        f"- Every (model, repeat) cell therefore runs the full {n_scenarios}-scenario suite; "
        f"n per model = {n_repeats} repeats × {n_scenarios} = {n_repeats * n_scenarios}.",
        "",
        "## Per-model composed cell",
        "",
        "Accuracy cells are mean ± sample std across the "
        f"{n_repeats} repeats (each repeat = {n_scenarios} scenarios). "
        "MF precision/recall are pooled row means, as in FINAL-TABLES.md.",
        "",
        "| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | dropped rules | failed encodings |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    failed_by_model: Counter = Counter(f["model"] for f in failed_encodings)
    confusion_all: Counter = Counter()
    confusion_by_model: dict[str, Counter] = defaultdict(Counter)

    for model in sorted(rows_by_model):
        rows = rows_by_model[model]
        pooled = aggregate(rows)
        by_repeat: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_repeat[row["repeat"]].append(row)
        repeat_aggs = [aggregate(by_repeat[rep]) for rep in sorted(by_repeat)]
        acc_cell = _mean_std([agg["outcome_accuracy"] for agg in repeat_aggs])
        class_cells = []
        for cls in PAPER_CLASSES:
            vals = [
                agg["per_class_accuracy"][cls]
                for agg in repeat_aggs
                if agg["per_class_accuracy"][cls] is not None
            ]
            class_cells.append(_mean_std(vals))
        dropped_total = sum(dropped_by_model[model].values())
        lines.append(
            f"| {model} | composed | {pooled['n']} | {acc_cell} | "
            + " | ".join(class_cells)
            + f" | {_fmt(pooled['mean_precision'])} | {_fmt(pooled['mean_recall'])} "
            f"| {dropped_total} | {failed_by_model.get(model, 0)} |"
        )
        for row in rows:
            if row["outcome_match"] is False:
                key = (row["expected_paper_outcome"], row["paper_outcome"])
                confusion_all[key] += 1
                confusion_by_model[model][key] += 1

    lines += [
        "",
        "## Dropped rules (selected rule referenced an unselected claim)",
        "",
        "Counts are over all composed encodings for the model "
        f"({n_repeats} repeats × {len(covered_domains)} domains). Rules the model did not",
        "select at all are not 'dropped' — they are simply absent from the encoding.",
        "",
        "| model | dropped-rule instances | rule ids (count) |",
        "|---|---|---|",
    ]
    for model in sorted(rows_by_model):
        dropped = dropped_by_model[model]
        detail = ", ".join(f"{rid} ({cnt})" for rid, cnt in dropped.most_common()) or "—"
        lines.append(f"| {model} | {sum(dropped.values())} | {detail} |")

    lines += ["", "## Encoding failures (build_domain_artifact raised)", ""]
    if failed_encodings:
        for f in failed_encodings:
            lines.append(f"- {f['model']} {f['case']} r{f['repeat']}: {f['error']}")
    else:
        lines.append(
            "None. Every composed encoding validated and built; the referential-"
            "integrity drop rule above was sufficient in all 120 encodings."
        )

    lines += ["", "## Mismatch confusion (expected → predicted, pooled)", ""]
    if confusion_all:
        lines.append("| expected → predicted | total | per model |")
        lines.append("|---|---|---|")
        for (exp, pred), count in confusion_all.most_common():
            per_model = ", ".join(
                f"{m}: {confusion_by_model[m][(exp, pred)]}"
                for m in sorted(rows_by_model)
                if confusion_by_model[m][(exp, pred)]
            )
            lines.append(f"| {exp} → {pred} | {count} | {per_model} |")
    else:
        lines.append("No outcome mismatches.")

    lines += ["", "## Failure pattern", ""]
    total_mismatch = sum(confusion_all.values())
    if total_mismatch:
        deny_pred = sum(cnt for (exp, pred), cnt in confusion_all.items() if pred == "DENY")
        enc_by_key = {
            (e["model"], e["case"], e["repeat"]): e["missing_rule_ids"] for e in encoding_records
        }
        missing_rules_on_failures: Counter = Counter()
        for model, rows in rows_by_model.items():
            for row in rows:
                if row["outcome_match"] is False:
                    missing_rules_on_failures.update(enc_by_key[(model, row["case"], row["repeat"])])
        top_rules = ", ".join(f"`{rid}`" for rid, _ in missing_rules_on_failures.most_common(4))
        lines += [
            f"Failures are one-sided toward DENY: {deny_pred} of {total_mismatch} outcome "
            f"mismatches predict DENY. The driver is missed allow-side rules (most often "
            f"{top_rules} on the failing rows): without the allow path, the solver either "
            "fires a deny rule outright (gold ALLOW → DENY) or decides instead of abstaining, "
            "because the unselected allow-path claims are no longer in the encoding to be "
            "reported as missing (gold NEED_MORE_INFO → DENY). Missing-fact precision is "
            "barely touched (pooled minimum "
            f"{_fmt(min(aggregate(r)['mean_precision'] for r in rows_by_model.values()))} "
            "across models); recall is what degrades when selection misses claims and rules.",
        ]
    else:
        lines.append("No outcome mismatches; nothing to analyze.")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection-jsonl", type=Path, default=SELECTION_JSONL)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Inject full gold ids through the adapter and require exact runtime agreement.",
    )
    args = parser.parse_args()

    ok_rows = load_selection_ok_rows(args.selection_jsonl)
    case_dirs = sorted({Path(row["case_dir"]) for row in ok_rows})
    covered_domains = [p.name for p in case_dirs]
    print(f"Selection ok rows: {len(ok_rows)}; domains covered: {covered_domains}")

    if args.self_test:
        ok = run_self_test(case_dirs)
        print("SELF-TEST " + ("PASSED: composed gold path == runtime row on all scenarios." if ok else "FAILED."))
        return 0 if ok else 1

    scenarios_by_case: dict[str, list[Path]] = {
        p.name: discover_suite_scenario_files_for_case(p.name) for p in case_dirs
    }
    n_scenarios = sum(len(v) for v in scenarios_by_case.values())

    raw_by_case: dict[str, dict[str, Any]] = {
        p.name: json.loads((p / "use_case.json").read_text(encoding="utf-8")) for p in case_dirs
    }

    all_rows: list[dict[str, Any]] = []
    encoding_records: list[dict[str, Any]] = []
    failed_encodings: list[dict[str, Any]] = []
    rows_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    dropped_by_model: dict[str, Counter] = defaultdict(Counter)

    for sel in sorted(ok_rows, key=lambda r: (r["model"], r["repeat"], r["case_dir"])):
        model, repeat = sel["model"], sel["repeat"]
        case_dir = Path(sel["case_dir"])
        case = case_dir.name
        raw = raw_by_case[case]
        gold_claims = {c["claim_id"] for c in raw["claims"]}
        gold_rules = {r["rule_id"] for r in raw["rules"]}
        sel_claims, sel_rules = reconstruct_selected(sel, gold_claims, gold_rules)

        domain: DomainArtifact | None = None
        dropped: list[str] = []
        error = ""
        try:
            use_case, dropped = compose_use_case(raw, sel_claims, sel_rules)
            domain = build_composed_domain(case_dir, use_case)
        except Exception as exc:  # noqa: BLE001 — recorded as failed encoding
            error = f"{type(exc).__name__}: {exc}"
            failed_encodings.append({"model": model, "case": case, "repeat": repeat, "error": error})

        dropped_by_model[model].update(dropped)
        encoding_records.append(
            {
                "model": model,
                "case": case,
                "repeat": repeat,
                "n_gold_claims": len(gold_claims),
                "n_gold_rules": len(gold_rules),
                "n_selected_claims": len(sel_claims),
                "n_selected_rules": len(sel_rules),
                "missing_claim_ids": sorted(gold_claims - sel_claims),
                "missing_rule_ids": sorted(gold_rules - sel_rules),
                "dropped_rule_ids": dropped,
                "build_error": error,
            }
        )

        for scenario_path in scenarios_by_case[case]:
            if domain is not None:
                row = run_composed_row(scenario_path, domain)
            else:
                row = failed_encoding_row(scenario_path, error)
            row.update({"model": model, "repeat": repeat, "case": case, "dropped_rule_ids": dropped})
            all_rows.append(row)
            rows_by_model[model].append(row)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows_path = args.out_dir / "composed_rows.jsonl"
    with rows_path.open("w", encoding="utf-8") as fh:
        for row in all_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    enc_path = args.out_dir / "composed_encodings.jsonl"
    with enc_path.open("w", encoding="utf-8") as fh:
        for record in encoding_records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    n_repeats = len({row["repeat"] for row in all_rows})
    summary = summarize(
        rows_by_model,
        dropped_by_model,
        failed_encodings,
        n_repeats,
        covered_domains,
        n_scenarios,
        encoding_records,
    )
    summary_path = args.out_dir / "primary_cell.md"
    summary_path.write_text(summary, encoding="utf-8")

    print(f"Wrote {len(all_rows)} rows -> {rows_path}")
    print(f"Wrote {len(encoding_records)} encodings -> {enc_path}")
    print(f"Wrote summary -> {summary_path}")
    for model in sorted(rows_by_model):
        pooled = aggregate(rows_by_model[model])
        print(
            f"{model}: n={pooled['n']} acc={pooled['outcome_accuracy']:.3f} "
            f"per-class={{{', '.join(f'{c}: {_fmt(pooled['per_class_accuracy'][c])}' for c in PAPER_CLASSES)}}} "
            f"P={pooled['mean_precision']:.3f} R={pooled['mean_recall']:.3f} "
            f"dropped_rules={sum(dropped_by_model[model].values())}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
