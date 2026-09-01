"""Scoring: node-appropriate metrics, isolation- and propagation-agnostic.

The scorer only ever compares a produced node value against the oracle node
value; whether the inputs were oracle (isolation) or produced upstream values
(propagation) is a property of the condition, not the scorer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from statute_decider.core import ClaimSet, PremiseOutcome, ScoredOutcome, UtteranceTerms

SCORED_CLASSES = [item.value for item in ScoredOutcome]


def set_prf(produced: set[str], expected: set[str]) -> tuple[float, float, float]:
    """Precision/recall/F1 over id sets; empty-vs-empty scores perfect."""
    if not produced and not expected:
        return 1.0, 1.0, 1.0
    tp = len(produced & expected)
    precision = tp / len(produced) if produced else 0.0
    recall = tp / len(expected) if expected else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return precision, recall, f1


def score_outcome(produced: PremiseOutcome, oracle: PremiseOutcome) -> dict:
    """Three-way outcome match + missing-term set metrics."""
    missing_p, missing_r, missing_f1 = set_prf(
        produced.missing_term_ids(), oracle.missing_term_ids()
    )
    return {
        "expected_scored_as": oracle.scored_as.value,
        "produced_scored_as": produced.scored_as.value,
        "outcome_correct": produced.scored_as == oracle.scored_as,
        "expected_state": oracle.state.value,
        "produced_state": produced.state.value,
        "state_correct": produced.state == oracle.state,
        "missing_precision": round(missing_p, 4),
        "missing_recall": round(missing_r, 4),
        "missing_f1": round(missing_f1, 4),
    }


def score_utterance_terms(produced: UtteranceTerms, oracle: UtteranceTerms) -> dict:
    """Coverage of the recognized-term set (understanding, not truth)."""
    precision, recall, f1 = set_prf(produced.term_ids(), oracle.term_ids())
    return {
        "term_precision": round(precision, 4),
        "term_recall": round(recall, 4),
        "term_f1": round(f1, 4),
    }


def score_claims(produced: ClaimSet, oracle: ClaimSet) -> dict:
    """Assignment accuracy over the oracle claim set + spurious-assignment count."""
    produced_by_term = produced.by_term()
    oracle_by_term = oracle.by_term()
    correct = sum(
        1
        for term_id, claim in oracle_by_term.items()
        if term_id in produced_by_term and produced_by_term[term_id].value == claim.value
    )
    total = len(oracle_by_term)
    spurious = len(set(produced_by_term) - set(oracle_by_term))
    return {
        "claim_accuracy": round(correct / total, 4) if total else 1.0,
        "claim_expected": total,
        "claim_correct": correct,
        "claim_spurious": spurious,
    }


@dataclass
class OutcomeAggregate:
    """n, accuracy, per-class P/R/F1, macro F1, missing-set means."""

    n: int = 0
    correct: int = 0
    confusion: dict[str, dict[str, int]] = field(default_factory=dict)
    missing_p_sum: float = 0.0
    missing_r_sum: float = 0.0
    missing_f1_sum: float = 0.0

    def add(self, score: dict) -> None:
        self.n += 1
        if score["outcome_correct"]:
            self.correct += 1
        expected = score["expected_scored_as"]
        produced = score["produced_scored_as"]
        self.confusion.setdefault(expected, {}).setdefault(produced, 0)
        self.confusion[expected][produced] += 1
        self.missing_p_sum += score["missing_precision"]
        self.missing_r_sum += score["missing_recall"]
        self.missing_f1_sum += score["missing_f1"]

    def per_class(self) -> dict[str, dict[str, float]]:
        result: dict[str, dict[str, float]] = {}
        for cls in SCORED_CLASSES:
            tp = self.confusion.get(cls, {}).get(cls, 0)
            fn = sum(self.confusion.get(cls, {}).values()) - tp
            fp = sum(
                counts.get(cls, 0) for expected, counts in self.confusion.items() if expected != cls
            )
            precision = tp / (tp + fp) if (tp + fp) else 0.0
            recall = tp / (tp + fn) if (tp + fn) else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
            support = tp + fn
            result[cls] = {
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "support": support,
            }
        return result

    def summary(self) -> dict:
        per_class = self.per_class()
        macro_f1 = (
            sum(stats["f1"] for stats in per_class.values()) / len(per_class)
            if per_class
            else 0.0
        )
        return {
            "n": self.n,
            "accuracy": round(self.correct / self.n, 4) if self.n else 0.0,
            "per_class": per_class,
            "macro_f1": round(macro_f1, 4),
            "missing_precision_mean": round(self.missing_p_sum / self.n, 4) if self.n else 0.0,
            "missing_recall_mean": round(self.missing_r_sum / self.n, 4) if self.n else 0.0,
            "missing_f1_mean": round(self.missing_f1_sum / self.n, 4) if self.n else 0.0,
        }
