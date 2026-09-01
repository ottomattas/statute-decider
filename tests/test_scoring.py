"""Scoring math: set P/R/F1, per-class F1, aggregation."""

from statute_decider.core import (
    ClaimPremise,
    ClaimSet,
    OutcomeState,
    PremiseOutcome,
    ScoredOutcome,
    TermRef,
    UtteranceTerms,
)
from statute_decider.core.outcome import MissingTerm
from statute_decider.runner.scoring import (
    OutcomeAggregate,
    score_claims,
    score_outcome,
    score_utterance_terms,
    set_prf,
)


def outcome(state: OutcomeState, missing: list[str] = ()) -> PremiseOutcome:
    return PremiseOutcome(
        scenario_id="s",
        state=state,
        scored_as={
            OutcomeState.ALLOW: ScoredOutcome.ALLOW,
            OutcomeState.DENY: ScoredOutcome.DENY,
        }.get(state, ScoredOutcome.NEED_MORE_INFO),
        missing_terms=[MissingTerm(term_id=t) for t in missing],
    )


def test_set_prf():
    assert set_prf(set(), set()) == (1.0, 1.0, 1.0)
    assert set_prf({"a"}, set()) == (0.0, 0.0, 0.0)
    p, r, f1 = set_prf({"a", "b"}, {"b", "c"})
    assert (p, r) == (0.5, 0.5) and abs(f1 - 0.5) < 1e-9


def test_score_outcome_and_missing():
    score = score_outcome(
        outcome(OutcomeState.NEED_USER_INFO, ["x"]),
        outcome(OutcomeState.NEED_REGISTER_INFO, ["x", "y"]),
    )
    assert score["outcome_correct"] is True  # both score NEED_MORE_INFO
    assert score["state_correct"] is False
    assert score["missing_precision"] == 1.0 and score["missing_recall"] == 0.5


def test_per_class_f1():
    agg = OutcomeAggregate()
    agg.add(score_outcome(outcome(OutcomeState.ALLOW), outcome(OutcomeState.ALLOW)))
    agg.add(score_outcome(outcome(OutcomeState.DENY), outcome(OutcomeState.ALLOW)))
    agg.add(score_outcome(outcome(OutcomeState.DENY), outcome(OutcomeState.DENY)))
    summary = agg.summary()
    assert summary["n"] == 3
    assert abs(summary["accuracy"] - 2 / 3) < 1e-3  # summary rounds to 4 decimals
    allow = summary["per_class"]["ALLOW"]
    assert allow["precision"] == 1.0 and allow["recall"] == 0.5
    deny = summary["per_class"]["DENY"]
    assert deny["precision"] == 0.5 and deny["recall"] == 1.0


def test_term_and_claim_scores():
    produced = UtteranceTerms(scenario_id="s", term_refs=[TermRef(term_id="a"), TermRef(term_id="b")])
    oracle = UtteranceTerms(scenario_id="s", term_refs=[TermRef(term_id="a")])
    ts = score_utterance_terms(produced, oracle)
    assert ts["term_recall"] == 1.0 and ts["term_precision"] == 0.5

    produced_claims = ClaimSet(
        scenario_id="s",
        claims=[
            ClaimPremise(premise_id="c1", term_id="a", value=True),
            ClaimPremise(premise_id="c2", term_id="b", value=False),
            ClaimPremise(premise_id="c3", term_id="z", value=True),
        ],
    )
    oracle_claims = ClaimSet(
        scenario_id="s",
        claims=[
            ClaimPremise(premise_id="c1", term_id="a", value=True),
            ClaimPremise(premise_id="c2", term_id="b", value=True),
        ],
    )
    cs = score_claims(produced_claims, oracle_claims)
    assert cs["claim_accuracy"] == 0.5 and cs["claim_spurious"] == 1
