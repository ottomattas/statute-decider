"""Experiment (i): catalog selection vs catalog-held-out synthesis.

Selection mode is the existing ``llm.extract_domain_artifact`` ablation
(model picks gold catalog ids). Synthesis mode invents claims and rules from
statute text only, then scores them with :mod:`encoding_scorer`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from encoding_scorer import (
    align_claims,
    claim_alignment_f1,
    semantic_equivalence,
)
from extract_synthesis import resolve_complete_fn, synthesize_domain
from llm import extract_domain_artifact
from logic_levels import build_domain_artifact
from use_case_files import load_use_case_from_dir

CompleteFn = Callable[..., Any]


def _id_set_prf(gold: set[str], pred: set[str]) -> tuple[float, float, float]:
    """Precision, recall, F1 over identifier sets. Empty/empty = 1."""
    if not gold and not pred:
        return 1.0, 1.0, 1.0
    tp = len(gold & pred)
    precision = (tp / len(pred)) if pred else 1.0
    recall = (tp / len(gold)) if gold else 1.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def run_selection_condition(
    case_dir: str | Path,
    complete_fn: CompleteFn,
) -> dict[str, Any]:
    """Ablation: catalog ID selection via ``llm.extract_domain_artifact``.

    The model sees the gold catalogs (existing step-02 prompts) and returns
    claim/rule ids. Score is id-set P/R/F1 against ``use_case.json``.
    """
    case_path = Path(case_dir).resolve()
    use_case = load_use_case_from_dir(case_path)
    law_path = case_path / "law.txt"
    law_text = law_path.read_text(encoding="utf-8")

    def generator(*, system_instruction, user_content, response_model, **kwargs):
        try:
            from providers import invoke_structured
        except ImportError:
            return complete_fn(
                system_instruction=system_instruction,
                user_content=user_content,
                response_model=response_model,
                **kwargs,
            )
        return invoke_structured(
            complete_fn,
            system=system_instruction,
            user=user_content,
            response_model=response_model,
            temperature=float(kwargs.get("temperature") or 0.0),
        )

    artifact = extract_domain_artifact(
        use_case_dir=case_path,
        law_text=law_text,
        logic_level=use_case.default_logic_level,
        generator=generator,
        source_path=law_path,
    )
    gold_claims = {claim.claim_id for claim in use_case.claims}
    gold_rules = {rule.rule_id for rule in use_case.rules}
    pred_claims = {claim.claim_id for claim in artifact.claims}
    pred_rules = {rule.rule_id for rule in artifact.rules}
    claim_p, claim_r, claim_f1 = _id_set_prf(gold_claims, pred_claims)
    rule_p, rule_r, rule_f1 = _id_set_prf(gold_rules, pred_rules)
    return {
        "condition": "selection",
        "case_dir": str(case_path),
        "case_title": use_case.title,
        "n_gold_claims": len(gold_claims),
        "n_pred_claims": len(pred_claims),
        "n_gold_rules": len(gold_rules),
        "n_pred_rules": len(pred_rules),
        "claim_precision": claim_p,
        "claim_recall": claim_r,
        "claim_f1": claim_f1,
        "rule_precision": rule_p,
        "rule_recall": rule_r,
        "rule_f1": rule_f1,
        "alignment_f1": (claim_f1 + rule_f1) / 2.0,
        "equivalent": None,
        "skipped": False,
        "n_agree": 0,
        "n_rows": 0,
        "equivalence_rate": None,
        "needs_audit": False,
        "unmatched_gold": sorted(gold_claims - pred_claims | gold_rules - pred_rules),
        "unmatched_pred": sorted(pred_claims - gold_claims | pred_rules - gold_rules),
        "dropped_rules": 0,
    }


def run_synthesis_condition(
    case_dir: str | Path,
    complete_fn: CompleteFn,
) -> dict[str, Any]:
    """Synthesize a domain from ``law.txt`` and score it against ``use_case.json``.

    ``complete_fn`` is required so unit tests never hit a provider. Gold claim
    and rule catalogs are not passed to the model.
    """
    case_path = Path(case_dir).resolve()
    use_case = load_use_case_from_dir(case_path)
    law_text = (case_path / "law.txt").read_text(encoding="utf-8")
    gold_domain = build_domain_artifact(
        use_case,
        use_case.default_logic_level,
        law_text,
    )
    stats: dict[str, Any] = {}
    pred_domain = synthesize_domain(
        law_text,
        complete_fn=complete_fn,
        title=use_case.title,
        stats=stats,
    )
    alignment = align_claims(gold_domain.claims, pred_domain.claims)
    equivalence = semantic_equivalence(gold_domain, pred_domain, alignment)
    alignment_f1 = claim_alignment_f1(alignment)
    n_rows = int(equivalence.get("n_rows") or 0)
    n_agree = int(equivalence.get("n_agree") or 0)
    equivalence_rate = (n_agree / n_rows) if n_rows else 0.0
    return {
        "condition": "synthesis",
        "case_dir": str(case_path),
        "case_title": use_case.title,
        "n_gold_claims": len(gold_domain.claims),
        "n_pred_claims": len(pred_domain.claims),
        "n_gold_rules": len(gold_domain.rules),
        "n_pred_rules": len(pred_domain.rules),
        "dropped_rules": int(stats.get("dropped_rules") or 0),
        "dropped_claims": int(stats.get("dropped_claims") or 0),
        "alignment_f1": alignment_f1,
        "unmatched_gold": list(alignment.unmatched_gold),
        "unmatched_pred": list(alignment.unmatched_pred),
        "needs_audit": alignment.needs_audit,
        "matches": [
            {
                "gold_id": match.gold_id,
                "pred_id": match.pred_id,
                "score": match.score,
            }
            for match in alignment.matches
        ],
        "equivalent": bool(equivalence.get("equivalent")),
        "skipped": bool(equivalence.get("skipped")),
        "n_agree": n_agree,
        "n_rows": n_rows,
        "equivalence_rate": equivalence_rate,
        "skip_reason": str(equivalence.get("skip_reason") or ""),
        "error_taxonomy": {
            "unmatched_gold": list(alignment.unmatched_gold),
            "unmatched_pred": list(alignment.unmatched_pred),
            "needs_audit": alignment.needs_audit,
            "dropped_rules": int(stats.get("dropped_rules") or 0),
            "skipped": bool(equivalence.get("skipped")),
        },
    }


def render_markdown(scores: Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> str:
    """Render one or more experiment-(i) score dicts as a Markdown table."""
    rows: list[Mapping[str, Any]]
    if isinstance(scores, Mapping) and "condition" in scores:
        rows = [scores]
    elif isinstance(scores, Mapping):
        rows = list(scores.values()) if scores else []
    else:
        rows = list(scores)

    lines = [
        "# Experiment (i) — synthesis extraction vs gold encoding",
        "",
        "Catalog-held-out boolean synthesis scored by lexical claim alignment "
        "and truth-table paper-outcome equivalence. Selection-mode ablation "
        "scores catalog-id F1 via existing `llm.extract_domain_artifact`.",
        "",
        "| case | condition | align F1 | equivalent | rate | n_agree/n_rows | audit | dropped rules |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        case = Path(str(row.get("case_dir") or row.get("case_title") or "")).name
        f1 = row.get("alignment_f1")
        f1_cell = f"{f1:.2f}" if isinstance(f1, float) else str(f1 or "—")
        if row.get("condition") == "selection":
            claim_f1 = row.get("claim_f1")
            rule_f1 = row.get("rule_f1")
            claim_cell = f"{claim_f1:.2f}" if isinstance(claim_f1, float) else "—"
            rule_cell = f"{rule_f1:.2f}" if isinstance(rule_f1, float) else "—"
            lines.append(
                f"| {case or '—'} | selection | {f1_cell} | id-set "
                f"(claim F1 {claim_cell}, rule F1 {rule_cell}) | — | — | — | — |"
            )
            continue
        skipped = bool(row.get("skipped"))
        equivalent = "skipped" if skipped else ("yes" if row.get("equivalent") else "no")
        rate = row.get("equivalence_rate")
        rate_cell = f"{rate:.2f}" if isinstance(rate, float) and not skipped else "—"
        n_cell = f"{row.get('n_agree', 0)}/{row.get('n_rows', 0)}"
        audit = "yes" if row.get("needs_audit") else "no"
        dropped = row.get("dropped_rules", 0)
        lines.append(
            f"| {case or '—'} | {row.get('condition', 'synthesis')} | {f1_cell} | "
            f"{equivalent} | {rate_cell} | {n_cell} | {audit} | {dropped} |"
        )
    lines.append("")
    audited = [row for row in rows if row.get("needs_audit")]
    if audited:
        lines.append("## Needs operator audit")
        lines.append("")
        for row in audited:
            case = Path(str(row.get("case_dir") or "")).name
            lines.append(
                f"- `{case}`: unmatched gold `{row.get('unmatched_gold')}`; "
                f"unmatched pred `{row.get('unmatched_pred')}`."
            )
        lines.append("")
    return "\n".join(lines)


def default_complete_fn() -> CompleteFn:
    """Resolve providers-or-Gemini completion for live overnight runs."""
    return resolve_complete_fn(None)
