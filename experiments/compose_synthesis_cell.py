"""Compose the synthesis analysis cell: LLM-synthesized encoding + solver.

The 27 Aug synthesis re-run (``experiments/results/synthesis-20260827``)
persists the full synthesized ``DomainArtifact`` per row, plus the claim
alignment against gold computed at scoring time. This script rebuilds each
synthesized domain, remaps aligned claim ids onto the gold vocabulary (the
scenario fact tables and mock DBs are keyed by gold claim ids), injects the
remapped domain into the suite runner, and scores all 47 gold scenarios with
the same ``score_row``/``aggregate`` code paths as the selection cell. No LLM
calls are made.

Protocol (documented verbatim in synthesis_cell.md):

- A synthesized claim aligned to a gold claim is renamed to the gold id, so
  intent/registry facts ground it. Unaligned synthesized claims keep their
  ids (prefixed ``syn::`` only on collision with a gold id) and therefore get
  no facts: the solver treats them as unknown. Rules are never rewritten
  beyond this id substitution and encodings are never repaired.
- Outcome scoring is the ordinary paper mapping over whatever the solver
  returns for the composed domain.
- Predicted missing facts that remain in synthesized vocabulary are kept in
  the predicted set and count against precision (they can never match gold);
  they are also counted separately as unmappable.
- A synthesized domain that fails to rebuild/validate scores its scenarios as
  incorrect (outcome mismatch, precision/recall 0), mirroring the selection
  composer's failed-encoding path.

Usage (from repo root):
    framework/venv/bin/python experiments/compose_synthesis_cell.py \
        --out-dir experiments/results/synthesis-20260827
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
from metadata import utc_timestamp  # noqa: E402
from paper_outcomes import to_paper_outcome  # noqa: E402
from scenario_suite import (  # noqa: E402
    discover_suite_scenario_files_for_case,
    run_suite_scenario,
)
from schemas import DomainArtifact  # noqa: E402

SYNTHESIS_JSONL = REPO_ROOT / "experiments/results/synthesis-20260827/experiment_i.jsonl"
DEFAULT_OUT_DIR = REPO_ROOT / "experiments/results/synthesis-20260827"
PAPER_CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")


def load_synthesis_ok_rows(path: Path) -> list[dict[str, Any]]:
    """Load ok synthesis rows that carry a persisted synthesized domain."""
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ok = [row for row in rows if "error" not in row]
    missing = [row for row in ok if not row.get("synthesized_domain")]
    if missing:
        for row in missing:
            print(
                f"ABORT: no synthesized_domain on {row['model']} "
                f"{Path(row['case_dir']).name} r{row['repeat']}",
                file=sys.stderr,
            )
        sys.exit(2)
    return ok


def remap_domain(
    row: dict[str, Any], gold_claim_ids: set[str]
) -> tuple[DomainArtifact, dict[str, Any]]:
    """Rebuild the synthesized domain with aligned claim ids renamed to gold.

    Returns the remapped domain plus grounding stats. Raises on rebuild
    failure (caller records a failed encoding).
    """
    raw = row["synthesized_domain"]
    mapping: dict[str, str] = {}
    for match in row.get("matches") or []:
        pred_id, gold_id = match["pred_id"], match["gold_id"]
        if gold_id not in gold_claim_ids:
            continue  # rule-level or non-claim alignment entries, if any
        # Keep the first (highest-scoring) alignment per pred and per gold id.
        if pred_id in mapping or gold_id in mapping.values():
            continue
        mapping[pred_id] = gold_id

    taken = set(gold_claim_ids)
    collisions = 0

    def rename(pred_id: str) -> str:
        nonlocal collisions
        if pred_id in mapping:
            return mapping[pred_id]
        if pred_id in taken:
            collisions += 1
            return f"syn::{pred_id}"
        return pred_id

    remapped = json.loads(json.dumps(raw, ensure_ascii=False))
    grounded = 0
    for claim in remapped.get("claims") or []:
        new_id = rename(claim["claim_id"])
        if new_id in gold_claim_ids:
            grounded += 1
        claim["claim_id"] = new_id
    ungrounded_rule_count = 0
    for rule in remapped.get("rules") or []:
        refs = [rename(cid) for cid in (rule.get("when_claim_ids") or [])]
        rule["when_claim_ids"] = refs
        if rule.get("target_claim_id"):
            rule["target_claim_id"] = rename(rule["target_claim_id"])
        if any(ref not in gold_claim_ids for ref in refs):
            ungrounded_rule_count += 1

    domain = DomainArtifact.model_validate(remapped)
    stats = {
        "n_pred_claims": len(remapped.get("claims") or []),
        "n_grounded_claims": grounded,
        "n_rules": len(remapped.get("rules") or []),
        "n_ungrounded_rules": ungrounded_rule_count,
        "collisions": collisions,
    }
    return domain, stats


def run_composed_row(
    scenario_path: Path, domain: DomainArtifact, gold_claim_ids: set[str]
) -> dict[str, Any]:
    """One scenario through the solver with the remapped synthesized domain."""
    result = run_suite_scenario(scenario_path, domain=domain)
    paper_outcome = to_paper_outcome(result.actual_outcome)
    missing_facts = list(result.actual_missing_facts)
    unmappable = sorted(f for f in missing_facts if f not in gold_claim_ids)
    expected_raw, expected_facts = load_gold(scenario_path)
    expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
    if expected_paper is None:
        scored = {"outcome_match": None, "precision": None, "recall": None}
    else:
        scored = score_row(expected_paper, expected_facts, paper_outcome, missing_facts)
    return {
        "scenario": result.scenario_name,
        "scenario_path": str(scenario_path),
        "condition": "synthesis-composed",
        "paper_outcome": paper_outcome,
        "missing_facts": missing_facts,
        "unmappable_missing_facts": unmappable,
        "fine_grained_outcome": result.actual_outcome.value,
        "expected_paper_outcome": expected_paper,
        "expected_missing_facts": expected_facts,
        "outcome_match": scored["outcome_match"],
        "precision": scored["precision"],
        "recall": scored["recall"],
    }


def failed_encoding_row(scenario_path: Path, error: str) -> dict[str, Any]:
    expected_raw, expected_facts = load_gold(scenario_path)
    expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
    return {
        "scenario": scenario_path.stem,
        "scenario_path": str(scenario_path),
        "condition": "synthesis-composed",
        "paper_outcome": None,
        "missing_facts": [],
        "unmappable_missing_facts": [],
        "fine_grained_outcome": None,
        "encoding_error": error,
        "expected_paper_outcome": expected_paper,
        "expected_missing_facts": expected_facts,
        "outcome_match": False if expected_paper else None,
        "precision": 0.0,
        "recall": 0.0,
    }


def _fmt(value: float | None) -> str:
    return "—" if value is None else f"{value:.3f}"


def _mean_std(values: list[float]) -> str:
    if not values:
        return "—"
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return f"{mean:.3f} ± {std:.3f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthesis-jsonl", type=Path, default=SYNTHESIS_JSONL)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    ok_rows = load_synthesis_ok_rows(args.synthesis_jsonl)
    case_dirs = sorted({Path(row["case_dir"]) for row in ok_rows})
    covered_domains = [p.name for p in case_dirs]
    print(f"Synthesis ok rows: {len(ok_rows)}; domains covered: {covered_domains}")

    scenarios_by_case = {p.name: discover_suite_scenario_files_for_case(p.name) for p in case_dirs}
    n_scenarios = sum(len(v) for v in scenarios_by_case.values())
    gold_claims_by_case: dict[str, set[str]] = {}
    for p in case_dirs:
        raw = json.loads((p / "use_case.json").read_text(encoding="utf-8"))
        gold_claims_by_case[p.name] = {c["claim_id"] for c in raw["claims"]}

    all_rows: list[dict[str, Any]] = []
    encoding_records: list[dict[str, Any]] = []
    failed_encodings: list[dict[str, Any]] = []
    rows_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for syn in sorted(ok_rows, key=lambda r: (r["model"], r["repeat"], r["case_dir"])):
        model, repeat = syn["model"], syn["repeat"]
        case = Path(syn["case_dir"]).name
        gold_claim_ids = gold_claims_by_case[case]

        domain: DomainArtifact | None = None
        stats: dict[str, Any] = {}
        error = ""
        try:
            domain, stats = remap_domain(syn, gold_claim_ids)
        except Exception as exc:  # noqa: BLE001 — recorded as failed encoding
            error = f"{type(exc).__name__}: {exc}"
            failed_encodings.append({"model": model, "case": case, "repeat": repeat, "error": error})

        encoding_records.append(
            {"model": model, "case": case, "repeat": repeat, "build_error": error, **stats}
        )

        for scenario_path in scenarios_by_case[case]:
            if domain is not None:
                row = run_composed_row(scenario_path, domain, gold_claim_ids)
            else:
                row = failed_encoding_row(scenario_path, error)
            row.update({"model": model, "repeat": repeat, "case": case})
            all_rows.append(row)
            rows_by_model[model].append(row)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows_path = args.out_dir / "synthesis_composed_rows.jsonl"
    with rows_path.open("w", encoding="utf-8") as fh:
        for row in all_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_repeats = len({row["repeat"] for row in all_rows})
    ok_encodings = [e for e in encoding_records if not e["build_error"]]
    total_claims = sum(e["n_pred_claims"] for e in ok_encodings)
    total_grounded = sum(e["n_grounded_claims"] for e in ok_encodings)
    total_rules = sum(e["n_rules"] for e in ok_encodings)
    total_ungrounded_rules = sum(e["n_ungrounded_rules"] for e in ok_encodings)
    unmappable_total = sum(len(r["unmappable_missing_facts"]) for r in all_rows)
    predicted_total = sum(len(r["missing_facts"]) for r in all_rows)

    failed_by_model: Counter = Counter(f["model"] for f in failed_encodings)
    confusion_all: Counter = Counter()
    lines = [
        "# Composed synthesis cell — LLM-synthesized encoding + deterministic solver",
        "",
        f"Generated {utc_timestamp()} by `experiments/compose_synthesis_cell.py` from",
        "`experiments/results/synthesis-20260827/experiment_i.jsonl` (27 Aug re-run of",
        "the synthesis leg with persisted DomainArtifact bodies). Deterministic solver",
        "(z3), zero LLM calls beyond the extraction re-run itself. Scoring uses the",
        "same `score_row`/`aggregate`/paper-outcome code paths as the selection cell.",
        "",
        "## Protocol",
        "",
        "- Synthesized claims aligned to gold (per-row alignment `matches`) are renamed",
        "  to the gold claim id, so intent/registry facts ground them. Unaligned claims",
        "  keep their synthesized ids (prefixed `syn::` only on collision with a gold",
        "  id) and receive no facts: the solver treats them as unknown. Rules get the",
        "  same id substitution and nothing else; encodings are never repaired.",
        "- Predicted missing facts still in synthesized vocabulary stay in the predicted",
        "  set and count against precision; they are also tallied as unmappable below.",
        "- A domain that fails to rebuild scores its scenarios as incorrect",
        "  (outcome mismatch, precision/recall 0), as in the selection composer.",
        "",
        "## Grounding coverage",
        "",
        f"- Synthesized claims aligned to gold vocabulary: {total_grounded}/{total_claims}"
        f" ({(total_grounded / total_claims):.1%})." if total_claims else "- No claims.",
        f"- Rules running with ≥1 ungrounded claim: {total_ungrounded_rules}/{total_rules}"
        f" ({(total_ungrounded_rules / total_rules):.1%})." if total_rules else "- No rules.",
        f"- Predicted missing facts unmappable to gold vocabulary: {unmappable_total}/{predicted_total}.",
        f"- Encoding rebuild failures: {len(failed_encodings)} of {len(encoding_records)}.",
        "",
        "## Per-model composed synthesis cell",
        "",
        f"Accuracy cells are mean ± sample std across the {n_repeats} repeats "
        f"(each repeat = {n_scenarios} scenarios). MF precision/recall are pooled row means.",
        "",
        "| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | failed encodings |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
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
        lines.append(
            f"| {model} | synthesis + solver | {pooled['n']} | {acc_cell} | "
            + " | ".join(class_cells)
            + f" | {_fmt(pooled['mean_precision'])} | {_fmt(pooled['mean_recall'])} "
            f"| {failed_by_model.get(model, 0)} |"
        )
        for row in rows:
            if row["outcome_match"] is False:
                confusion_all[(row["expected_paper_outcome"], row["paper_outcome"])] += 1

    lines += ["", "## Mismatch confusion (expected → predicted, pooled)", ""]
    if confusion_all:
        lines.append("| expected → predicted | total |")
        lines.append("|---|---|")
        for (exp, pred), count in confusion_all.most_common():
            lines.append(f"| {exp} → {pred} | {count} |")
    else:
        lines.append("No outcome mismatches.")
    lines.append("")

    summary_path = args.out_dir / "synthesis_cell.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(all_rows)} rows -> {rows_path}")
    print(f"Wrote summary -> {summary_path}")
    for model in sorted(rows_by_model):
        pooled = aggregate(rows_by_model[model])
        print(
            f"{model}: n={pooled['n']} acc={pooled['outcome_accuracy']:.3f} "
            f"P={_fmt(pooled['mean_precision'])} R={_fmt(pooled['mean_recall'])}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
