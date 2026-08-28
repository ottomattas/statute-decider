"""u7 disclosure probe: does telling the baseline a fact is unverified fix u7?

The 25 Aug LLM-only baseline fails all 200 u7_trust_only rows because the
prompt presents trust-only registry values as ordinary known facts. This probe
re-runs exactly the five u7 scenarios across the four cheap models with the
disclosure variant of the baseline (trust-only facts moved to an UNVERIFIED
ASSERTIONS section, one added system-prompt paragraph, missing-fact filter
widened to accept the disclosed ids). One repeat; ~20 calls; budget-guarded
and ledger-tracked like every other run.

Usage (from repo root):
    framework/venv/bin/python experiments/u7_disclosure_probe.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "framework"))

from experiment_ii import load_gold, score_row  # noqa: E402
from experiments.budget import BudgetGuard  # noqa: E402
from llm_baseline import (  # noqa: E402
    decide_llm_only,
    load_scenario_context,
    trust_only_claim_ids_for_scenario,
)
from metadata import utc_timestamp  # noqa: E402
from paper_outcomes import to_paper_outcome  # noqa: E402
from providers import get_provider  # noqa: E402
from run_experiments import HaltState, Label, load_runtime_env, make_tracked_complete  # noqa: E402

PROVIDERS = ["gemini", "openai", "anthropic", "deepseek"]
OUT_DIR = REPO_ROOT / "experiments/results/u7-disclosure-20260827"


def u7_scenario_paths() -> list[Path]:
    return sorted((REPO_ROOT / "framework/examples").glob("*/scenarios/*u7_trust_only.json"))


def main() -> int:
    load_runtime_env()
    from experiments.ledger import ledger_path  # noqa: PLC0415

    prior = 0.0
    if ledger_path().exists():
        for line in ledger_path().read_text(encoding="utf-8").splitlines():
            if line.strip():
                prior += float(json.loads(line).get("eur") or 0.0)
    guard = BudgetGuard(cap_eur=prior + 1.0)
    guard.spent_eur = prior
    halt = HaltState()

    scenarios = u7_scenario_paths()
    print(f"u7 scenarios: {[p.stem for p in scenarios]}; prior ledger EUR {prior:.4f}")

    rows: list[dict] = []
    for provider_name in PROVIDERS:
        provider = get_provider(provider_name)
        if not provider.available():
            print(f"skip {provider_name}: not available")
            continue
        label = Label(value="u7-disclosure")
        complete = make_tracked_complete(
            provider, experiment="u7-disclosure", label=label, guard=guard, halt=halt
        )
        model = getattr(provider, "model", provider_name)
        for path in scenarios:
            label.value = f"{path.stem}#disclosure#r0"
            ctx = load_scenario_context(path)
            trust_ids = trust_only_claim_ids_for_scenario(ctx.scenario, ctx.use_case, ctx.mock_db)
            unverified = {fid: ctx.known_facts[fid] for fid in trust_ids if fid in ctx.known_facts}
            known = {k: v for k, v in ctx.known_facts.items() if k not in unverified}
            try:
                decision = decide_llm_only(
                    law_text=ctx.law_text,
                    request_text=ctx.request_text,
                    known_facts=known,
                    unknown_claim_ids=ctx.unknown_claim_ids,
                    claim_catalog_text=ctx.catalog_text,
                    provider_complete=complete,
                    unverified_facts=unverified,
                )
            except Exception as exc:  # noqa: BLE001 — provider outages must not sink the probe
                print(f"ERROR {model} {path.stem}: {type(exc).__name__}: {exc}")
                rows.append(
                    {
                        "scenario": path.stem,
                        "provider": provider_name,
                        "model": model,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue
            expected_raw, expected_facts = load_gold(path)
            expected_paper = to_paper_outcome(expected_raw)
            scored = score_row(expected_paper, expected_facts, decision.outcome, decision.missing_facts)
            row = {
                "scenario": path.stem,
                "provider": provider_name,
                "model": model,
                "disclosed_ids": trust_ids,
                "outcome": decision.outcome,
                "missing_facts": decision.missing_facts,
                "expected_paper_outcome": expected_paper,
                "expected_missing_facts": expected_facts,
                **scored,
                "reason": decision.reason,
            }
            rows.append(row)
            print(
                f"{model} {path.stem}: {decision.outcome} "
                f"(match={scored['outcome_match']} P={scored['precision']:.2f} R={scored['recall']:.2f})"
            )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "u7_probe_rows.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    lines = [
        "# u7 disclosure probe — trust-only facts disclosed to the LLM-only baseline",
        "",
        f"Generated {utc_timestamp()} by `experiments/u7_disclosure_probe.py`. Five",
        "`*_u7_trust_only` scenarios × 4 cheap models × 1 repeat, disclosure variant",
        "of `llm_baseline` (trust-only facts moved to an UNVERIFIED ASSERTIONS prompt",
        "section; one system-prompt paragraph added; missing-fact filter widened to",
        "accept disclosed ids). Baseline comparison: 0/200 correct on these scenarios",
        "in the 25 Aug run.",
        "",
        "| model | correct outcome | mean MF precision | mean MF recall |",
        "|---|---|---|---|",
    ]
    scored_rows = [row for row in rows if "error" not in row]
    models = sorted({row["model"] for row in scored_rows})
    for model in models:
        mrows = [row for row in scored_rows if row["model"] == model]
        correct = sum(1 for row in mrows if row["outcome_match"])
        mp = sum(row["precision"] for row in mrows) / len(mrows)
        mr = sum(row["recall"] for row in mrows) / len(mrows)
        lines.append(f"| {model} | {correct}/{len(mrows)} | {mp:.3f} | {mr:.3f} |")
    lines += ["", "## Per-row outcomes", "", "| model | scenario | outcome | missing facts |", "|---|---|---|---|"]
    for row in rows:
        if "error" in row:
            lines.append(f"| {row['model']} | {row['scenario']} | ERROR | {row['error']} |")
        else:
            lines.append(
                f"| {row['model']} | {row['scenario']} | {row['outcome']} | {', '.join(row['missing_facts']) or '—'} |"
            )
    lines.append("")
    (OUT_DIR / "u7_probe.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(rows)} rows and u7_probe.md -> {OUT_DIR}")
    print(f"New spend this probe: EUR {guard.spent_eur - prior:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
