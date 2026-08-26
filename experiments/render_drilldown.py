"""Render the gold-vs-response mismatch drill-down as presentable markdown.

Reads experiment (ii) LLM JSONL rows and, for every failed cell (wrong
outcome, imperfect missing-fact set, or a hard error), shows the gold next to
each model response. Re-run after every experiment batch; pass one or more
``tag=path`` inputs so smoke and scale data stay clearly separated.

Usage (from repo root):
    python experiments/render_drilldown.py \
        --input smoke=experiments/results/experiment_ii_llm.jsonl \
        --input scale=experiments/results/scale-20260825/ii/experiment_ii_llm.jsonl \
        --out experiments/results/mismatch-drilldown.md
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FLAGGED_NOTE = (
    "Rows whose gold is `gold_confidence: low` (solver-proposed, unaudited) are "
    "marked **[GOLD UNAUDITED]**; treat their mismatches as provisional until "
    "the operator audit lands."
)


def load_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def gold_confidence(scenario_path: str, cache: dict[str, str]) -> str:
    if scenario_path not in cache:
        conf = ""
        try:
            raw = json.loads(Path(scenario_path).read_text(encoding="utf-8"))
            conf = str(raw.get("gold_confidence") or "")
        except OSError:
            pass
        cache[scenario_path] = conf
    return cache[scenario_path]


def is_failed(row: dict) -> bool:
    if row.get("error"):
        return True
    if row.get("outcome_match") is False:
        return True
    precision = row.get("precision")
    recall = row.get("recall")
    if row.get("outcome_match") is True and (
        (precision is not None and precision < 1.0)
        or (recall is not None and recall < 1.0)
    ):
        return True
    return False


def fmt_facts(facts) -> str:
    if not facts:
        return "(none)"
    return ", ".join(f"`{f}`" for f in facts)


def fmt_score(value) -> str:
    return "—" if value is None else f"{value:.2f}"


def render(inputs: list[tuple[str, Path]], out_path: Path) -> None:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conf_cache: dict[str, str] = {}
    lines = [
        "# Experiment (ii) mismatch drill-down — gold vs model response",
        "",
        "**SMOKE / SCALE — UNVALIDATED.** Do not quote as results.",
        "",
        f"Generated {generated} by `experiments/render_drilldown.py`.",
        "",
        "A *failed cell* is an LLM-only row with a wrong 3-way outcome, an",
        "imperfect missing-fact set (P or R < 1 despite a correct outcome), or a",
        "hard error. Gold is shown once per scenario; every failing model",
        "response is listed against it.",
        "",
        FLAGGED_NOTE,
        "",
    ]

    for tag, path in inputs:
        rows = load_rows(path)
        scored = [r for r in rows if r.get("outcome_match") is not None]
        failed = [r for r in rows if is_failed(r)]
        outcome_wrong = [r for r in failed if r.get("outcome_match") is False]
        facts_only = [r for r in failed if r.get("outcome_match") is True]
        errors = [r for r in failed if r.get("error")]

        lines += [
            f"## Source `{tag}` — `{path}`",
            "",
            f"- rows: {len(rows)} ({len(scored)} scored); failed cells: "
            f"{len(failed)} = {len(outcome_wrong)} wrong outcome + "
            f"{len(facts_only)} fact-set-only + {len(errors)} hard errors",
            "",
        ]

        # summary: wrong outcomes per provider x expected class
        counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        totals: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for r in scored:
            cls = r.get("expected_paper_outcome") or "?"
            totals[r.get("provider") or "?"][cls] += 1
            if r.get("outcome_match") is False:
                counts[r.get("provider") or "?"][cls] += 1
        classes = ("ALLOW", "DENY", "NEED_MORE_INFO")
        lines += [
            "### Wrong outcomes by provider and expected class",
            "",
            "| provider | " + " | ".join(classes) + " |",
            "|---|" + "|".join(["---"] * len(classes)) + "|",
        ]
        for provider in sorted(totals):
            cells = [
                f"{counts[provider][c]}/{totals[provider][c]}" for c in classes
            ]
            lines.append(f"| {provider} | " + " | ".join(cells) + " |")
        lines.append("")

        # group failures by scenario
        by_scenario: dict[str, list[dict]] = defaultdict(list)
        for r in failed:
            by_scenario[r.get("scenario") or "?"].append(r)

        for scenario in sorted(by_scenario):
            group = by_scenario[scenario]
            first = group[0]
            conf = gold_confidence(str(first.get("scenario_path") or ""), conf_cache)
            flag = " **[GOLD UNAUDITED]**" if conf == "low" else ""
            lines += [
                f"### `{scenario}`{flag}",
                "",
                f"**Gold:** outcome `{first.get('expected_paper_outcome')}`; "
                f"missing facts: {fmt_facts(first.get('expected_missing_facts'))}",
                "",
                "| provider | repeat | model outcome | match | P | R | model missing facts |",
                "|---|---|---|---|---|---|---|",
            ]
            for r in sorted(
                group, key=lambda x: (str(x.get("provider")), x.get("repeat") or 0)
            ):
                if r.get("error"):
                    lines.append(
                        f"| {r.get('provider')} | {r.get('repeat', '—')} | "
                        f"ERROR | — | — | — | {str(r.get('error'))[:120]} |"
                    )
                    continue
                lines.append(
                    f"| {r.get('provider')} | {r.get('repeat', 0)} | "
                    f"{r.get('paper_outcome')} | "
                    f"{'YES' if r.get('outcome_match') else 'NO'} | "
                    f"{fmt_score(r.get('precision'))} | "
                    f"{fmt_score(r.get('recall'))} | "
                    f"{fmt_facts(r.get('missing_facts'))} |"
                )
            lines.append("")
            # model reasons, deduplicated
            seen: dict[str, list[str]] = {}
            for r in group:
                reason = (r.get("reason") or "").strip()
                if not reason:
                    continue
                key = reason[:400]
                seen.setdefault(key, []).append(
                    f"{r.get('provider')}#r{r.get('repeat', 0)}"
                )
            if seen:
                lines.append("Model reasoning (deduplicated):")
                lines.append("")
                for reason, who in seen.items():
                    lines.append(f"- _{', '.join(who)}_: {reason}")
                lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        metavar="TAG=PATH",
        help="tag=path to an experiment_ii_llm.jsonl (repeatable)",
    )
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    inputs = []
    for item in args.input:
        tag, _, path = item.partition("=")
        inputs.append((tag, Path(path)))
    render(inputs, Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
