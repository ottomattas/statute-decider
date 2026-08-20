"""Paired runner for JURIX experiment (ii): solver runtime vs LLM-only baseline.

Each scenario produces two rows with the same gold and the same metrics:
paper 3-way outcome accuracy and missing-fact precision/recall. Runtime
rows call the existing deterministic ``run_suite_scenario``; LLM rows call
``decide_llm_only`` with an injected complete() callable (no live API in tests).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Callable

from llm_baseline import (
    ScenarioContext,
    build_case_bundle,
    decide_llm_only,
    get_complete_fn,
    load_scenario_context,
)
from reasoner import solve_case_bundle
from scenario_suite import SuiteResult, run_suite_scenario

try:
    from paper_outcomes import (  # type: ignore[import-not-found]
        fact_set_precision_recall,
        missing_facts_from_solution,
        to_paper_outcome,
    )
except ImportError:
    from _paper import (
        fact_set_precision_recall,
        missing_facts_from_solution,
        to_paper_outcome,
    )

PAPER_CLASSES = ("ALLOW", "DENY", "NEED_MORE_INFO")
ProviderComplete = Callable[..., Any]


def load_gold(scenario_path: str | Path) -> tuple[str | None, list[str]]:
    """Read expected_outcome / expected_missing_facts from JSON without rewriting it.

    ``expected_missing_facts`` defaults to [] when the field is absent (WS-A
    may still be writing gold). ``expected_outcome`` may also be missing on
    unpromoted scenarios; the row still runs.
    """
    raw = json.loads(Path(scenario_path).read_text(encoding="utf-8"))
    expected_outcome = raw.get("expected_outcome")
    expected_facts = raw.get("expected_missing_facts")
    if expected_facts is None:
        expected_facts = []
    return expected_outcome, [str(item) for item in expected_facts]


def score_row(
    expected_paper_outcome: str,
    expected_facts: Sequence[str],
    actual_paper_outcome: str,
    actual_facts: Sequence[str],
) -> dict[str, Any]:
    """Score one paper outcome plus one missing-fact set against gold."""
    precision, recall = fact_set_precision_recall(expected_facts, actual_facts)
    return {
        "outcome_match": expected_paper_outcome == actual_paper_outcome,
        "precision": precision,
        "recall": recall,
    }


def _runtime_missing_facts(result: SuiteResult, ctx: ScenarioContext) -> list[str]:
    """Prefer WS-A's SuiteResult field; else recover from a deterministic solve."""
    if hasattr(result, "actual_missing_facts"):
        return list(getattr(result, "actual_missing_facts"))
    solution = solve_case_bundle(build_case_bundle(ctx))
    return missing_facts_from_solution(solution)


def _scored_row(
    *,
    ctx: ScenarioContext,
    condition: str,
    provider: str | None,
    paper_outcome: str,
    missing_facts: list[str],
    fine_grained_outcome: str | None,
    reason: str,
) -> dict[str, Any]:
    expected_raw, expected_facts = load_gold(ctx.path)
    expected_paper = to_paper_outcome(expected_raw) if expected_raw else None
    if expected_paper is None:
        scored = {"outcome_match": None, "precision": None, "recall": None}
    else:
        scored = score_row(expected_paper, expected_facts, paper_outcome, missing_facts)
    return {
        "scenario": ctx.scenario.name,
        "scenario_path": str(ctx.path),
        "condition": condition,
        "provider": provider,
        "paper_outcome": paper_outcome,
        "missing_facts": list(missing_facts),
        "fine_grained_outcome": fine_grained_outcome,
        "reason": reason,
        "expected_paper_outcome": expected_paper,
        "expected_missing_facts": expected_facts,
        "outcome_match": scored["outcome_match"],
        "precision": scored["precision"],
        "recall": scored["recall"],
    }


def run_runtime_row(scenario_path: str | Path) -> dict[str, Any]:
    """Deterministic solver row: ``run_suite_scenario`` plus paper mapping."""
    path = Path(scenario_path)
    ctx = load_scenario_context(path)
    result = run_suite_scenario(path)
    paper_outcome = to_paper_outcome(result.actual_outcome)
    missing_facts = _runtime_missing_facts(result, ctx)
    fine = result.actual_outcome.value if result.actual_outcome is not None else None
    return _scored_row(
        ctx=ctx,
        condition="runtime",
        provider=None,
        paper_outcome=paper_outcome,
        missing_facts=missing_facts,
        fine_grained_outcome=fine,
        reason=result.notes,
    )


def run_llm_row(
    scenario_path: str | Path,
    provider_name: str,
    complete_fn: ProviderComplete | None = None,
) -> dict[str, Any]:
    """LLM-only row. Inject ``complete_fn`` in tests; never call a live API there."""
    ctx = load_scenario_context(scenario_path)
    complete = complete_fn if complete_fn is not None else get_complete_fn(provider_name)
    decision = decide_llm_only(
        law_text=ctx.law_text,
        request_text=ctx.request_text,
        known_facts=ctx.known_facts,
        unknown_claim_ids=ctx.unknown_claim_ids,
        claim_catalog_text=ctx.catalog_text,
        provider_complete=complete,
    )
    return _scored_row(
        ctx=ctx,
        condition="llm",
        provider=provider_name,
        paper_outcome=decision.outcome,
        missing_facts=decision.missing_facts,
        fine_grained_outcome=None,
        reason=decision.reason,
    )


def pair_rows(runtime_row: dict[str, Any], llm_row: dict[str, Any]) -> dict[str, Any]:
    """Join one scenario's runtime and LLM-only rows for the contrast table."""
    if runtime_row["scenario"] != llm_row["scenario"]:
        raise ValueError(
            f"Cannot pair {runtime_row['scenario']!r} with {llm_row['scenario']!r}"
        )
    return {
        "scenario": runtime_row["scenario"],
        "expected_paper_outcome": runtime_row["expected_paper_outcome"],
        "expected_missing_facts": runtime_row["expected_missing_facts"],
        "runtime_paper_outcome": runtime_row["paper_outcome"],
        "runtime_missing_facts": runtime_row["missing_facts"],
        "runtime_fine_grained": runtime_row["fine_grained_outcome"],
        "runtime_outcome_match": runtime_row["outcome_match"],
        "runtime_precision": runtime_row["precision"],
        "runtime_recall": runtime_row["recall"],
        "llm_provider": llm_row["provider"],
        "llm_paper_outcome": llm_row["paper_outcome"],
        "llm_missing_facts": llm_row["missing_facts"],
        "llm_outcome_match": llm_row["outcome_match"],
        "llm_precision": llm_row["precision"],
        "llm_recall": llm_row["recall"],
    }


def aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Per-class outcome accuracy plus macro-averaged fact-set precision/recall.

    Macro P/R is the unweighted mean of per-class mean precision/recall over
    paper classes that have at least one gold row. Row-level means are also
    returned as ``mean_precision`` / ``mean_recall``.
    """
    n = len(rows)
    scored = [row for row in rows if row.get("outcome_match") is not None]
    outcome_accuracy = (
        sum(1 for row in scored if row["outcome_match"]) / len(scored) if scored else 0.0
    )
    per_class: dict[str, float | None] = {}
    class_precision: list[float] = []
    class_recall: list[float] = []
    for cls in PAPER_CLASSES:
        subset = [row for row in scored if row.get("expected_paper_outcome") == cls]
        if not subset:
            per_class[cls] = None
            continue
        per_class[cls] = sum(1 for row in subset if row["outcome_match"]) / len(subset)
        class_precision.append(sum(row["precision"] for row in subset) / len(subset))
        class_recall.append(sum(row["recall"] for row in subset) / len(subset))
    precisions = [row["precision"] for row in scored if row.get("precision") is not None]
    recalls = [row["recall"] for row in scored if row.get("recall") is not None]
    return {
        "n": n,
        "n_scored": len(scored),
        "outcome_accuracy": outcome_accuracy,
        "per_class_accuracy": per_class,
        "macro_precision": (sum(class_precision) / len(class_precision) if class_precision else 0.0),
        "macro_recall": (sum(class_recall) / len(class_recall) if class_recall else 0.0),
        "mean_precision": (sum(precisions) / len(precisions) if precisions else 0.0),
        "mean_recall": (sum(recalls) / len(recalls) if recalls else 0.0),
    }


def _fmt_facts(facts: Sequence[str] | None) -> str:
    if not facts:
        return "∅"
    return ", ".join(facts)


def _fmt_score(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.2f}"


def _fmt_match(value: bool | None) -> str:
    if value is None:
        return "—"
    return "YES" if value else "NO"


def render_markdown_table(rows: Sequence[dict[str, Any]]) -> str:
    """Render one-condition experiment (ii) rows as a Markdown table."""
    header = (
        "| scenario | condition | expected | actual | match | P | R | missing_facts |"
    )
    separator = "|----------|-----------|----------|--------|-------|---|---|----------------|"
    lines = [header, separator]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("scenario", "")),
                    str(row.get("condition", "")),
                    str(row.get("expected_paper_outcome") or "—"),
                    str(row.get("paper_outcome") or "—"),
                    _fmt_match(row.get("outcome_match")),
                    _fmt_score(row.get("precision")),
                    _fmt_score(row.get("recall")),
                    _fmt_facts(row.get("missing_facts")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def render_paired_markdown(pairs: Sequence[dict[str, Any]]) -> str:
    """Render runtime vs LLM-only contrast rows as a Markdown table."""
    header = (
        "| scenario | expected | runtime | llm | rt match | llm match "
        "| P_rt | R_rt | P_llm | R_llm | rt facts | llm facts |"
    )
    separator = (
        "|----------|----------|---------|-----|----------|-----------"
        "|------|------|-------|--------|----------|-----------|"
    )
    lines = [header, separator]
    for row in pairs:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("scenario", "")),
                    str(row.get("expected_paper_outcome") or "—"),
                    str(row.get("runtime_paper_outcome") or "—"),
                    str(row.get("llm_paper_outcome") or "—"),
                    _fmt_match(row.get("runtime_outcome_match")),
                    _fmt_match(row.get("llm_outcome_match")),
                    _fmt_score(row.get("runtime_precision")),
                    _fmt_score(row.get("runtime_recall")),
                    _fmt_score(row.get("llm_precision")),
                    _fmt_score(row.get("llm_recall")),
                    _fmt_facts(row.get("runtime_missing_facts")),
                    _fmt_facts(row.get("llm_missing_facts")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"
