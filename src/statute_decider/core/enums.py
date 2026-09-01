"""Closed vocabularies shared across the graph."""

from __future__ import annotations

from enum import Enum


class Level(str, Enum):
    """The five graph levels; every node belongs to exactly one."""

    SOURCE = "source"
    TERM = "term"
    PREMISE = "premise"
    OUTCOME = "outcome"
    TRACE = "trace"


class Chain(str, Enum):
    """Epistemic role of a chain: who vouches for its content."""

    STATUTE = "statute"  # normative
    USER = "user"  # asserted
    REGISTER = "register"  # warranted
    JOIN = "join"  # outcome + trace: fed by all three chains


class Epistemic(str, Enum):
    """Epistemic type of a premise (the warrant principle lives here)."""

    NORMATIVE = "normative"  # rules: neither true nor false, they bind
    ASSERTED = "asserted"  # claims: fallible, never decision-grade alone
    WARRANTED = "warranted"  # facts: institutionally warranted, decision-grade


class Evidence(str, Enum):
    """Which chain can supply a decision-grade value for a term."""

    USER = "user"  # self-declarable: the applicant's assertion is accepted
    REGISTER = "register"  # requires an institutional register value
    DERIVED = "derived"  # set only by rewrite rules, never asserted directly


class Warrant(str, Enum):
    """Trust level a register confers on its values (source data, not config)."""

    AUTHORITATIVE = "authoritative"
    TRUST_ONLY = "trust_only"  # accepted verbatim, unverifiable -> claim-strength


class Availability(str, Enum):
    REGISTER_AVAILABLE = "available"
    REGISTER_UNAVAILABLE = "unavailable"


class RuleKind(str, Enum):
    ALLOW_IF_ALL = "allow_if_all"
    DENY_IF_ALL = "deny_if_all"
    SET_FALSE_IF_ALL = "set_false_if_all"  # rewrite: forces a derived term false


class OutcomeState(str, Enum):
    """Fine-grained decision states (extensible beyond the scored three)."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    NEED_USER_INFO = "NEED_USER_INFO"
    NEED_REGISTER_INFO = "NEED_REGISTER_INFO"
    UNVERIFIABLE_CLAIM = "UNVERIFIABLE_CLAIM"
    NEED_MORE_INFO = "NEED_MORE_INFO"  # coarse state used by methods with no finer signal (llm)


class ScoredOutcome(str, Enum):
    """The three-way outcome every condition is scored on."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    NEED_MORE_INFO = "NEED_MORE_INFO"


class MissingReason(str, Enum):
    """Why a decision-relevant term has no decision-grade value."""

    NO_VALUE = "no_value"  # nobody supplied a value
    UNWARRANTED_ONLY = "unwarranted_only"  # only an assertion / trust-only value exists
    NO_REGISTER = "no_register"  # the authoritative register is unavailable
    CONFLICT = "conflict"  # available registers disagree


class LogicLevel(str, Enum):
    PROPOSITIONAL = "propositional"
    PREDICATE = "predicate"  # reserved for the logic upgrade
    HIGHER_ORDER = "higher_order"  # reserved for the logic upgrade


def to_scored(state: OutcomeState) -> ScoredOutcome:
    """ALLOW stays ALLOW, DENY stays DENY, everything else scores NEED_MORE_INFO."""
    if state == OutcomeState.ALLOW:
        return ScoredOutcome.ALLOW
    if state == OutcomeState.DENY:
        return ScoredOutcome.DENY
    return ScoredOutcome.NEED_MORE_INFO
