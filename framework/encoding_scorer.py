"""Lexical claim alignment and truth-table encoding equivalence.

Experiment (i) scores a synthesized domain against the hand-authored gold
domain from ``use_case.json``. Claim ids will not match, so rules are compared
only after a 1-1 greedy lexical alignment, then by paper-level outcomes on the
aligned boolean subspace.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import product
from typing import Any, Iterable, Mapping, Sequence

from schemas import (
    CaseBundle,
    DomainArtifact,
    DomainClaim,
    DomainRule,
    IntentArtifact,
    IntentClaim,
    MockDbArtifact,
    SolverOutcome,
)

try:
    from paper_outcomes import to_paper_outcome
except ImportError:  # WS-A may land later; scoring-layer fallback.

    def to_paper_outcome(outcome: SolverOutcome | str) -> str:
        """ALLOW stays ALLOW, DENY stays DENY, everything else → NEED_MORE_INFO."""
        value = outcome.value if isinstance(outcome, SolverOutcome) else str(outcome)
        if value == "ALLOW":
            return "ALLOW"
        if value == "DENY":
            return "DENY"
        return "NEED_MORE_INFO"

from reasoner import solve_case_bundle

ALIGNMENT_THRESHOLD = 0.4
DEFAULT_MAX_VARS = 6

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "of",
        "in",
        "to",
        "for",
        "and",
        "or",
        "not",
        "on",
        "by",
        "with",
        "from",
        "that",
        "this",
        "it",
        "as",
        "at",
        "has",
        "have",
        "had",
    }
)


@dataclass(frozen=True)
class ClaimMatch:
    """One accepted gold↔pred claim pair."""

    gold_id: str
    pred_id: str
    score: float


@dataclass
class Alignment:
    """1-1 greedy lexical alignment of predicted claims onto gold claims."""

    matches: list[ClaimMatch] = field(default_factory=list)
    unmatched_gold: list[str] = field(default_factory=list)
    unmatched_pred: list[str] = field(default_factory=list)
    needs_audit: bool = False

    @property
    def gold_to_pred(self) -> dict[str, str]:
        return {match.gold_id: match.pred_id for match in self.matches}

    @property
    def pred_to_gold(self) -> dict[str, str]:
        return {match.pred_id: match.gold_id for match in self.matches}


def _claim_blob(claim: DomainClaim) -> str:
    return " ".join(
        part
        for part in (claim.label, claim.claim_id, claim.formal_text, claim.lowered_atom)
        if part
    )


def normalize_tokens(text: str) -> set[str]:
    """Lowercase alphanumeric tokens, dropping single letters and stopwords."""
    tokens = _TOKEN_RE.findall(text.lower().replace("_", " "))
    return {token for token in tokens if len(token) > 1 and token not in _STOPWORDS}


def token_overlap(left: str, right: str) -> float:
    """Jaccard overlap of normalized token sets. Empty∩empty is 0, not 1."""
    left_tokens = normalize_tokens(left)
    right_tokens = normalize_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _pair_score(gold: DomainClaim, pred: DomainClaim) -> float:
    return token_overlap(_claim_blob(gold), _claim_blob(pred))


def align_claims(
    gold_claims: Sequence[DomainClaim],
    pred_claims: Sequence[DomainClaim],
    *,
    threshold: float = ALIGNMENT_THRESHOLD,
) -> Alignment:
    """Greedy 1-1 match by token overlap of label + claim_id + formal_text.

    Pairs below ``threshold`` (default 0.4) are left unmatched. If two gold
    claims are both viable for the same predicted claim (or vice versa),
    ``needs_audit`` is set; greedy still keeps the highest-scoring exclusive
    pairs.
    """
    gold_list = list(gold_claims)
    pred_list = list(pred_claims)
    scores: list[tuple[float, str, str]] = []
    above_for_pred: dict[str, list[tuple[float, str]]] = {claim.claim_id: [] for claim in pred_list}
    above_for_gold: dict[str, list[tuple[float, str]]] = {claim.claim_id: [] for claim in gold_list}

    for gold in gold_list:
        for pred in pred_list:
            score = _pair_score(gold, pred)
            scores.append((score, gold.claim_id, pred.claim_id))
            if score >= threshold:
                above_for_pred[pred.claim_id].append((score, gold.claim_id))
                above_for_gold[gold.claim_id].append((score, pred.claim_id))

    needs_audit = any(len(hits) >= 2 for hits in above_for_pred.values()) or any(
        len(hits) >= 2 for hits in above_for_gold.values()
    )

    scores.sort(key=lambda row: (-row[0], row[1], row[2]))
    used_gold: set[str] = set()
    used_pred: set[str] = set()
    matches: list[ClaimMatch] = []
    for score, gold_id, pred_id in scores:
        if score < threshold:
            break
        if gold_id in used_gold or pred_id in used_pred:
            continue
        used_gold.add(gold_id)
        used_pred.add(pred_id)
        matches.append(ClaimMatch(gold_id=gold_id, pred_id=pred_id, score=score))

    gold_ids = [claim.claim_id for claim in gold_list]
    pred_ids = [claim.claim_id for claim in pred_list]
    return Alignment(
        matches=matches,
        unmatched_gold=[cid for cid in gold_ids if cid not in used_gold],
        unmatched_pred=[cid for cid in pred_ids if cid not in used_pred],
        needs_audit=needs_audit,
    )


def claim_alignment_f1(alignment: Alignment) -> float:
    """F1 over 1-1 matches vs unmatched gold (fn) and unmatched pred (fp).

    Empty gold and empty pred → 1.0. Empty gold with leftover pred → 0 precision
    and recall 1.0 (nothing to recover), so F1 is 0.
    """
    true_positive = len(alignment.matches)
    false_positive = len(alignment.unmatched_pred)
    false_negative = len(alignment.unmatched_gold)
    precision = (
        true_positive / (true_positive + false_positive) if (true_positive + false_positive) else 1.0
    )
    recall = (
        true_positive / (true_positive + false_negative) if (true_positive + false_negative) else 1.0
    )
    if precision + recall == 0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


def remap_rules(pred_rules: Sequence[DomainRule], alignment: Alignment) -> list[DomainRule]:
    """Rewrite predicted rule premises onto gold claim ids where aligned.

    Unaligned ids are left unchanged. Outcome ids are not rewritten.
    """
    pred_to_gold = alignment.pred_to_gold
    remapped: list[DomainRule] = []
    for rule in pred_rules:
        when_claim_ids = [pred_to_gold.get(cid, cid) for cid in rule.when_claim_ids]
        target_claim_id = rule.target_claim_id
        if target_claim_id:
            target_claim_id = pred_to_gold.get(target_claim_id, target_claim_id)
        remapped.append(
            rule.model_copy(
                update={
                    "when_claim_ids": when_claim_ids,
                    "target_claim_id": target_claim_id,
                }
            )
        )
    return remapped


def _intent_from_domain(
    domain: DomainArtifact,
    assignments: Mapping[str, bool | None],
    *,
    request_text: str = "",
) -> IntentArtifact:
    """Build an intent artifact whose claims mirror ``domain.claims``.

    Same shape as ``logic_levels.build_intent_artifact``, but does not require
    a ``UseCaseDefinition`` (predicted domains have invented ids).
    """
    claims: list[IntentClaim] = []
    for claim in domain.claims:
        claims.append(
            IntentClaim(
                claim_id=claim.claim_id,
                lowered_atom=claim.lowered_atom,
                label=claim.label,
                description=claim.description,
                source_type=claim.source_type,
                formal_text=claim.formal_text,
                value=assignments.get(claim.claim_id),
            )
        )
    return IntentArtifact(
        logic_level=domain.logic_level,
        request_text=request_text,
        lowered_view_note=domain.lowered_view_note,
        claims=claims,
    )


def _remap_pred_domain(pred_domain: DomainArtifact, alignment: Alignment) -> DomainArtifact:
    """Copy of ``pred_domain`` with aligned claim ids rewritten to gold ids."""
    pred_to_gold = alignment.pred_to_gold
    claims: list[DomainClaim] = []
    seen: set[str] = set()
    for claim in pred_domain.claims:
        new_id = pred_to_gold.get(claim.claim_id, claim.claim_id)
        if new_id in seen:
            continue
        seen.add(new_id)
        claims.append(claim.model_copy(update={"claim_id": new_id}))
    rules = remap_rules(pred_domain.rules, alignment)
    return pred_domain.model_copy(update={"claims": claims, "rules": rules})


def _iter_assignments(claim_ids: Sequence[str]) -> Iterable[dict[str, bool]]:
    for combo in product((False, True), repeat=len(claim_ids)):
        yield dict(zip(claim_ids, combo))


def _empty_mock_db() -> MockDbArtifact:
    return MockDbArtifact(sources=[])


def _paper_outcome_for(
    domain: DomainArtifact,
    assignments: Mapping[str, bool | None],
) -> str:
    intent = _intent_from_domain(domain, assignments)
    bundle = CaseBundle(
        logic_level=domain.logic_level,
        domain=domain,
        intent=intent,
        mock_db=_empty_mock_db(),
    )
    solution = solve_case_bundle(bundle)
    return to_paper_outcome(solution.final_outcome)


def semantic_equivalence(
    gold_domain: DomainArtifact,
    pred_domain: DomainArtifact,
    alignment: Alignment,
    *,
    max_vars: int = DEFAULT_MAX_VARS,
) -> dict[str, Any]:
    """Enumerate aligned gold assignments and compare paper-level solver outcomes.

    Variables are the gold claim ids in ``alignment.matches``. Predicted rules
    are remapped onto those ids. A gold claim with no aligned pred is unknown
    (``None``) on the predicted side. When ``n > max_vars`` the table is skipped.
    """
    aligned_gold_ids = [match.gold_id for match in alignment.matches]
    n_vars = len(aligned_gold_ids)
    if n_vars == 0:
        return {
            "equivalent": False,
            "skipped": False,
            "n_agree": 0,
            "n_rows": 0,
            "skip_reason": "no aligned claims",
        }
    if n_vars > max_vars:
        return {
            "equivalent": False,
            "skipped": True,
            "n_agree": 0,
            "n_rows": 0,
            "skip_reason": (
                f"Aligned claim count {n_vars} exceeds max_vars={max_vars}; "
                "truth-table enumeration skipped."
            ),
        }

    remapped_pred = _remap_pred_domain(pred_domain, alignment)
    gold_ids = [claim.claim_id for claim in gold_domain.claims]
    pred_claim_ids = {claim.claim_id for claim in remapped_pred.claims}
    n_agree = 0
    n_rows = 0
    for aligned_assignment in _iter_assignments(aligned_gold_ids):
        gold_assignments: dict[str, bool | None] = {cid: None for cid in gold_ids}
        gold_assignments.update(aligned_assignment)
        pred_assignments: dict[str, bool | None] = {
            cid: None for cid in pred_claim_ids
        }
        for gold_id, value in aligned_assignment.items():
            if gold_id in pred_claim_ids:
                pred_assignments[gold_id] = value
            # else: pred missing this gold claim → unknown/None
        gold_paper = _paper_outcome_for(gold_domain, gold_assignments)
        pred_paper = _paper_outcome_for(remapped_pred, pred_assignments)
        n_rows += 1
        if gold_paper == pred_paper:
            n_agree += 1

    return {
        "equivalent": n_agree == n_rows and n_rows > 0,
        "skipped": False,
        "n_agree": n_agree,
        "n_rows": n_rows,
        "skip_reason": "",
    }
