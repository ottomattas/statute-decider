"""Oracle-rules + LLM-decider: the missing 2x2 matrix cell (supervision 2026-08-28).

The 2x2 grid crosses WHO authors the rules with WHO decides:

|                    | solver decides            | LLM decides                  |
|--------------------|---------------------------|------------------------------|
| oracle rules       | runtime row (1.000)       | **this condition**           |
| LLM-selected rules | composed cell (0.74-0.87) | (LLM-only baseline, no rules)|

Inputs are byte-identical to the LLM-only baseline (statute, case request,
known facts, unknown claim ids, claim catalog) PLUS a clearly delimited
REFERENCE DECISION RULES section rendering the hand-authored gold encoding
(`use_case.json`): boolean claim variables and allow_if_all / deny_if_all /
set_false_if_all rules, e.g. ``parent AND emergency -> ALLOW``. The system
prompt instructs the model to play solver: apply the rules to the known
facts; abstain with NEED_MORE_INFO listing exactly the claim ids that could
still change the outcome; missing_facts must be empty on ALLOW/DENY.

Grid: 4 cheap scale-run models x 47 gold scenarios x 10 repeats, temperature
0, same structured-output schema (``BaselineDecision``) and provider plumbing
as the baseline. Hard cap: EUR 10 on top of prior ledger spend. Rows are
append-only and resume-keyed by (condition, scenario#repeat, provider,
model); call failures are recorded as error rows and the run continues.

Usage (from repo root):
    framework/venv/bin/python experiments/oracle_rules_llm_decider.py --smoke
    framework/venv/bin/python experiments/oracle_rules_llm_decider.py
    framework/venv/bin/python experiments/oracle_rules_llm_decider.py --summarize-only
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "framework"))

from experiment_ii import load_gold, score_row  # noqa: E402
from experiments.budget import BudgetExceeded, BudgetGuard  # noqa: E402
from experiments.ledger import iter_ledger  # noqa: E402
from llm_baseline import (  # noqa: E402
    BaselineDecision,
    ScenarioContext,
    _call_complete,
    _filter_missing_facts,
    build_user_prompt,
    load_scenario_context,
)
from metadata import utc_timestamp  # noqa: E402
from paper_outcomes import to_paper_outcome  # noqa: E402
from providers import get_provider  # noqa: E402
from run_experiments import (  # noqa: E402
    HaltState,
    Label,
    gold_scenario_files,
    load_runtime_env,
    make_tracked_complete,
)
from schemas import RuleKind  # noqa: E402
from use_case_files import UseCaseDefinition  # noqa: E402

CONDITION = "oracle_rules_llm"
EXPERIMENT = "oracle-llm"
SMOKE_EXPERIMENT = "oracle-llm-smoke"
# Cheapest first so a budget halt costs the fewest complete (model x 470) cells.
PROVIDERS = ["deepseek", "gemini", "openai", "anthropic"]
OUT_DIR = REPO_ROOT / "experiments/results/oracle-llm-20260901"
RUN_CAP_EUR = 10.0
PAPER_CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")

_SYSTEM_PROMPT = """You decide a statutory case by applying the REFERENCE DECISION RULES to the KNOWN FACTS. The rules are the authoritative encoding of the statute for this case; where your own reading of the statute text would differ, the rules win.

Rule semantics:
- Every claim id is a boolean variable. KNOWN FACTS fixes some of them; ids under UNKNOWN CLAIM IDS have no value.
- "a AND b -> ALLOW" fires when every premise on the left is true. Same for "-> DENY".
- "a AND b -> NOT c" fires when every premise is true and then sets claim c to false. Apply these before evaluating allow/deny rules.
- A rule with at least one false premise is blocked and can never fire. A rule with no false premise but at least one unknown premise is open: it could still fire.

Decide exactly one outcome, in this order:
1. DENY if a deny rule fires on the known facts.
2. Otherwise ALLOW if an allow rule fires on the known facts.
3. Otherwise NEED_MORE_INFO if at least one allow rule is open. In missing_facts list exactly the unknown claim ids appearing in the open allow rules — the facts that could still change the outcome — and nothing else.
4. Otherwise DENY: every allow rule is blocked, so no assignment of the unknown claims can produce ALLOW.

missing_facts must be an empty list when the outcome is ALLOW or DENY. Use only claim ids that appear under UNKNOWN CLAIM IDS. Do not invent claim identifiers. Give a short reason naming the rule(s) you applied.
"""


# ---------------------------------------------------------------------------
# Rules rendering (hand-authored gold encoding -> readable prompt section)
# ---------------------------------------------------------------------------


def _rule_conclusion(use_case: UseCaseDefinition, rule: Any) -> str:
    if rule.kind == RuleKind.SET_FALSE_IF_ALL:
        return f"NOT {rule.target_claim_id}"
    if rule.target_outcome_id == use_case.allow_outcome_id:
        return "ALLOW"
    if rule.target_outcome_id == use_case.deny_outcome_id:
        return "DENY"
    return str(rule.target_outcome_id)


def render_rules_section(use_case: UseCaseDefinition) -> str:
    """Render the gold encoding as boolean variables plus readable rules."""
    var_lines = [f"- {claim.claim_id}: {claim.label}" for claim in use_case.claims]
    rule_lines = []
    for rule in use_case.rules:
        premise = " AND ".join(rule.when_claim_ids)
        rule_lines.append(
            f"- {rule.rule_id} ({rule.kind.value}): {premise} -> {_rule_conclusion(use_case, rule)}"
        )
    return (
        "REFERENCE DECISION RULES (hand-authored encoding of the statute; "
        "boolean variables are the claim ids):\n"
        "Variables:\n" + "\n".join(var_lines) + "\n"
        "Rules:\n" + "\n".join(rule_lines)
    )


def build_rules_user_prompt(ctx: ScenarioContext) -> str:
    """Baseline user prompt (byte-identical inputs) plus the delimited rules block."""
    base = build_user_prompt(
        law_text=ctx.law_text,
        request_text=ctx.request_text,
        known_facts=ctx.known_facts,
        unknown_claim_ids=ctx.unknown_claim_ids,
        claim_catalog_text=ctx.catalog_text,
    )
    return base + "\n" + render_rules_section(ctx.use_case) + "\n"


def decide_with_rules(ctx: ScenarioContext, provider_complete: Any) -> BaselineDecision:
    """One structured decision call with the gold rules in the prompt."""
    decision = _call_complete(
        provider_complete,
        system=_SYSTEM_PROMPT,
        user=build_rules_user_prompt(ctx),
        response_model=BaselineDecision,
    )
    decision.missing_facts = _filter_missing_facts(decision.missing_facts, ctx.unknown_claim_ids)
    return decision


# ---------------------------------------------------------------------------
# Append-only rows + resume keys (same policy as run_experiments)
# ---------------------------------------------------------------------------


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _append_row(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=True, default=str) + "\n")


def completed_keys(rows: list[dict[str, Any]]) -> set[tuple[str, str, str, str]]:
    done = set()
    for row in rows:
        if row.get("error"):
            continue
        done.add((CONDITION, str(row.get("scenario_label")), str(row.get("provider")), str(row.get("model"))))
    return done


def dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Success supersedes error for the same (label, provider, model) key."""
    by_key: dict[Any, dict[str, Any]] = {}
    order: list[Any] = []
    for index, row in enumerate(rows):
        label = row.get("scenario_label")
        key = (label, row.get("provider"), row.get("model")) if label else index
        if key not in by_key:
            by_key[key] = row
            order.append(key)
        elif by_key[key].get("error") or not row.get("error"):
            by_key[key] = row
    return [by_key[key] for key in order]


# ---------------------------------------------------------------------------
# Run loop
# ---------------------------------------------------------------------------


def run_grid(
    *,
    providers: list[str],
    scenario_files: list[Path],
    repeats: int,
    rows_path: Path,
    experiment: str,
    guard: BudgetGuard,
) -> None:
    halt = HaltState()
    done = completed_keys(_load_jsonl(rows_path))
    if done:
        print(f"resume: {len(done)} rows already recorded in {rows_path.name}")
    contexts: dict[Path, ScenarioContext] = {}

    for provider_name in providers:
        if halt.error is not None:
            break
        provider = get_provider(provider_name)
        if not provider.available():
            print(f"skip {provider_name}: not available (missing key)")
            continue
        model = getattr(provider, "model", provider_name)
        label = Label(value=CONDITION)
        complete = make_tracked_complete(
            provider, experiment=experiment, label=label, guard=guard, halt=halt
        )
        for repeat in range(repeats):
            if halt.error is not None:
                break
            for path in scenario_files:
                if halt.error is not None:
                    print(f"budget halt before {provider_name} {path.stem} r{repeat}")
                    break
                label.value = f"{path.stem}#r{repeat}"
                key = (CONDITION, label.value, provider_name, model)
                if key in done:
                    continue
                ctx = contexts.get(path)
                if ctx is None:
                    ctx = load_scenario_context(path)
                    contexts[path] = ctx
                try:
                    decision = decide_with_rules(ctx, complete)
                except BudgetExceeded as exc:
                    halt.error = exc
                    print(f"BUDGET HALT: {exc}")
                    break
                except Exception as exc:  # noqa: BLE001 — call failures must not sink the grid
                    print(f"ERROR {model} {label.value}: {type(exc).__name__}: {exc}")
                    _append_row(
                        rows_path,
                        {
                            "scenario": path.stem,
                            "scenario_path": str(path),
                            "scenario_label": label.value,
                            "condition": CONDITION,
                            "provider": provider_name,
                            "model": model,
                            "repeat": repeat,
                            "error": f"{type(exc).__name__}: {exc}",
                            "outcome_match": None,
                            "precision": None,
                            "recall": None,
                        },
                    )
                    continue
                expected_raw, expected_facts = load_gold(path)
                expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
                if expected_paper is None:
                    scored = {"outcome_match": None, "precision": None, "recall": None}
                else:
                    scored = score_row(
                        expected_paper, expected_facts, decision.outcome, decision.missing_facts
                    )
                row = {
                    "scenario": path.stem,
                    "scenario_path": str(path),
                    "scenario_label": label.value,
                    "condition": CONDITION,
                    "provider": provider_name,
                    "model": model,
                    "repeat": repeat,
                    "paper_outcome": decision.outcome,
                    "missing_facts": decision.missing_facts,
                    "reason": decision.reason,
                    "expected_paper_outcome": expected_paper,
                    "expected_missing_facts": expected_facts,
                    **scored,
                }
                _append_row(rows_path, row)
                done.add(key)
                p_txt = "—" if scored["precision"] is None else f"{scored['precision']:.2f}"
                r_txt = "—" if scored["recall"] is None else f"{scored['recall']:.2f}"
                print(
                    f"{model} {label.value}: {decision.outcome} "
                    f"(match={scored['outcome_match']} P={p_txt} R={r_txt}) "
                    f"spent EUR {guard.spent_eur:.4f}"
                )
    if halt.error is not None:
        print(f"Run stopped at budget cap: {halt.error}")


# ---------------------------------------------------------------------------
# Summary (same shape as the FINAL-TABLES experiment (ii) block)
# ---------------------------------------------------------------------------

# Prior conditions for the paper's 2x2 comparison, copied verbatim from
# experiments/results/scale-20260825/FINAL-TABLES.md (LLM-only, gold-audited)
# and experiments/results/compose-20260827/primary_cell.md (selected+solver).
PRIOR_CONDITIONS: dict[str, list[tuple[str, str, str, str, str, str, str]]] = {
    "claude-haiku-4-5-20251001": [
        ("selected + solver", "0.851", "0.714", "1.000", "0.857", "1.000", "0.915"),
        ("LLM-only", "0.762", "0.786", "0.917", "0.657", "0.950", "0.831"),
    ],
    "deepseek-v4-flash": [
        ("selected + solver", "0.851", "0.714", "1.000", "0.857", "1.000", "0.915"),
        ("LLM-only", "0.787", "0.857", "0.917", "0.667", "0.950", "0.844"),
    ],
    "gemini-2.5-flash": [
        ("selected + solver", "0.868", "0.786", "0.983", "0.857", "1.000", "0.915"),
        ("LLM-only", "0.677", "0.843", "1.000", "0.381", "0.994", "0.723"),
    ],
    "gpt-5-mini": [
        ("selected + solver", "0.736", "0.557", "0.983", "0.714", "1.000", "0.849"),
        ("LLM-only", "0.749", "0.957", "0.950", "0.495", "0.984", "0.768"),
    ],
}


def _mean_std(values: list[float]) -> str:
    if not values:
        return "—"
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return f"{mean:.3f} ± {std:.3f}"


def _repeat_accs(rows: list[dict[str, Any]], cls: str | None = None) -> list[float]:
    by_rep: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("outcome_match") is None:
            continue
        if cls is not None and row.get("expected_paper_outcome") != cls:
            continue
        by_rep[int(row.get("repeat") or 0)].append(row)
    return [
        sum(1 for r in by_rep[rep] if r["outcome_match"]) / len(by_rep[rep])
        for rep in sorted(by_rep)
        if by_rep[rep]
    ]


def _pooled_stats(rows: list[dict[str, Any]]) -> tuple[float, float, float]:
    scored = [r for r in rows if r.get("outcome_match") is not None]
    acc = sum(1 for r in scored if r["outcome_match"]) / len(scored) if scored else 0.0
    precisions = [r["precision"] for r in scored if r.get("precision") is not None]
    recalls = [r["recall"] for r in scored if r.get("recall") is not None]
    mp = sum(precisions) / len(precisions) if precisions else 0.0
    mr = sum(recalls) / len(recalls) if recalls else 0.0
    return acc, mp, mr


def ledger_cost_per_call(experiment: str) -> dict[str, list[float]]:
    out: dict[str, list[float]] = defaultdict(list)
    for row in iter_ledger():
        if str(row.get("experiment")) == experiment:
            out[str(row.get("model"))].append(float(row.get("eur") or 0.0))
    return out


def write_summary(rows_path: Path, out_path: Path, *, repeats: int, n_scenarios: int) -> None:
    rows = dedupe_rows(_load_jsonl(rows_path))
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)
    costs = ledger_cost_per_call(EXPERIMENT)

    lines = [
        "# Oracle rules + LLM decider — the missing 2x2 cell",
        "",
        f"Generated {utc_timestamp()} by `experiments/oracle_rules_llm_decider.py`.",
        f"All 47 gold scenarios x 4 cheap models x {repeats} repeats, temperature 0.",
        "Inputs identical to the LLM-only baseline (`framework/llm_baseline.py`) plus",
        "a REFERENCE DECISION RULES section rendering the hand-authored gold",
        "encoding (`use_case.json`); the system prompt instructs the model to play",
        "solver over those rules (fire deny, then allow; abstain listing the unknown",
        "claim ids in open allow rules; default DENY when no allow path remains).",
        "Scoring uses the same `score_row`/`fact_set_precision_recall` code paths as",
        "FINAL-TABLES.md; costs from `experiments/ledger.jsonl`",
        f"(experiment `{EXPERIMENT}`).",
        "",
        "## Per-model results",
        "",
        f"Accuracy cells are mean ± sample std across the {repeats} repeats",
        f"(each repeat = {n_scenarios} scenarios). MF precision/recall are pooled row",
        "means. Mean cost/case is the per-call ledger mean.",
        "",
        "| model | condition | n | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall | mean cost/case (EUR) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for model in sorted(by_model):
        mrows = by_model[model]
        scored = [r for r in mrows if r.get("outcome_match") is not None]
        n_err = len(mrows) - len(scored)
        _, mp, mr = _pooled_stats(mrows)
        acc_cell = _mean_std(_repeat_accs(mrows))
        class_cells = [_mean_std(_repeat_accs(mrows, cls)) for cls in PAPER_CLASSES]
        calls = costs.get(model, [])
        cost = f"{sum(calls) / len(calls):.4f}" if calls else "—"
        n_cell = f"{len(scored)}" + (f" ({n_err} err)" if n_err else "")
        lines.append(
            f"| {model} | oracle rules + LLM | {n_cell} | {acc_cell} | "
            + " | ".join(class_cells)
            + f" | {mp:.3f} | {mr:.3f} | {cost} |"
        )

    lines += [
        "",
        "## 2x2 comparison — rule author x decider",
        "",
        "New rows next to the existing conditions. `oracle + solver` is the runtime",
        "row (FINAL-TABLES.md, gold-audited); `selected + solver` is the composed",
        "cell (compose-20260827, 5 repeats); `LLM-only` is the 25 Aug scale run",
        "(no rules in the prompt). Prior accuracies are pooled means.",
        "",
        "| model | condition | outcome acc | acc ALLOW | acc DENY | acc NEED_MORE_INFO | MF precision | MF recall |",
        "|---|---|---|---|---|---|---|---|",
        "| z3 (solver) | oracle + solver | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |",
    ]
    for model in sorted(by_model):
        mrows = by_model[model]
        acc, mp, mr = _pooled_stats(mrows)
        scored = [r for r in mrows if r.get("outcome_match") is not None]
        cls_cells = []
        for cls in PAPER_CLASSES:
            subset = [r for r in scored if r.get("expected_paper_outcome") == cls]
            cls_cells.append(
                f"{sum(1 for r in subset if r['outcome_match']) / len(subset):.3f}" if subset else "—"
            )
        lines.append(
            f"| {model} | **oracle rules + LLM** | {acc:.3f} | "
            + " | ".join(cls_cells)
            + f" | {mp:.3f} | {mr:.3f} |"
        )
        for cond, oacc, a, d, n, p, r in PRIOR_CONDITIONS.get(model, []):
            lines.append(f"| {model} | {cond} | {oacc} | {a} | {d} | {n} | {p} | {r} |")

    error_rows = [row for row in _load_jsonl(rows_path) if row.get("error")]
    lines += ["", "## Error rows", ""]
    if error_rows:
        superseded = {
            (r.get("scenario_label"), r.get("provider"), r.get("model"))
            for r in rows
            if not r.get("error")
        }
        for row in error_rows:
            key = (row.get("scenario_label"), row.get("provider"), row.get("model"))
            status = "superseded by retry" if key in superseded else "UNRESOLVED"
            lines.append(f"- {row['model']} {row['scenario_label']}: {row['error']} ({status})")
    else:
        lines.append("None.")

    run_total = sum(sum(v) for v in costs.values())
    n_calls = sum(len(v) for v in costs.values())
    lines += [
        "",
        "## Cost",
        "",
        f"Ledger rows tagged `{EXPERIMENT}`: {n_calls} calls, EUR {run_total:.4f} total.",
        "",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote summary -> {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="1 model x 2 scenarios x 1 repeat")
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument(
        "--summarize-only", action="store_true", help="Rebuild the markdown from existing rows"
    )
    args = parser.parse_args()

    load_runtime_env()
    scenario_files = gold_scenario_files(None)
    rows_path = args.out_dir / ("smoke_rows.jsonl" if args.smoke else "oracle_rules_llm.jsonl")

    if args.summarize_only:
        write_summary(
            rows_path,
            args.out_dir / "oracle_rules_llm.md",
            repeats=args.repeats,
            n_scenarios=len(scenario_files),
        )
        return 0

    prior = sum(float(row.get("eur") or 0.0) for row in iter_ledger())
    guard = BudgetGuard(cap_eur=prior + RUN_CAP_EUR)
    guard.spent_eur = prior
    print(
        f"prior ledger EUR {prior:.4f}; this run capped at EUR {RUN_CAP_EUR:.2f} "
        f"({len(scenario_files)} scenarios)"
    )

    if args.smoke:
        run_grid(
            providers=["deepseek"],
            scenario_files=scenario_files[:2],
            repeats=1,
            rows_path=rows_path,
            experiment=SMOKE_EXPERIMENT,
            guard=guard,
        )
        print(f"Smoke spend: EUR {guard.spent_eur - prior:.4f}; rows -> {rows_path}")
        return 0

    run_grid(
        providers=PROVIDERS,
        scenario_files=scenario_files,
        repeats=args.repeats,
        rows_path=rows_path,
        experiment=EXPERIMENT,
        guard=guard,
    )
    print(f"Run spend: EUR {guard.spent_eur - prior:.4f}")
    write_summary(
        rows_path,
        args.out_dir / "oracle_rules_llm.md",
        repeats=args.repeats,
        n_scenarios=len(scenario_files),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
