"""Term level: the one shared boolean vocabulary all chains meet in.

``text_term`` *defines* the vocabulary (authority), ``utterance_term``
*recognizes* which terms the utterance speaks about, ``record_term`` *maps*
register fields onto terms.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from statute_decider.core.enums import Evidence
from statute_decider.core.provenance import Provenance


class ClauseAnchor(BaseModel):
    """Anchor into the normative text (also used as a law reference on rules)."""

    clause_id: str
    clause_title: str = ""
    quote: str = ""
    note: str = ""


class Term(BaseModel):
    """One named boolean variable; the grounding currency of the graph."""

    term_id: str  # snake_case, singular
    label: str
    definition: str = ""
    evidence: Evidence = Evidence.USER  # who can supply a decision-grade value
    propositional: str = ""  # lowered atom for the propositional level
    predicate: str | None = None  # reserved for the logic upgrade
    higher_order: str | None = None  # reserved for the logic upgrade
    anchors: list[ClauseAnchor] = Field(default_factory=list)
    notes: str = ""


class TermCatalog(BaseModel):
    """Output of ``text_term``: the vocabulary a normative text defines."""

    node: Literal["text_term"] = "text_term"
    statute_id: str
    terms: list[Term]
    provenance: Provenance | None = None

    def by_id(self) -> dict[str, Term]:
        return {term.term_id: term for term in self.terms}

    def term_ids(self) -> set[str]:
        return {term.term_id for term in self.terms}


class TermRef(BaseModel):
    """One vocabulary item recognized in an utterance (understanding, not truth)."""

    term_id: str
    span: str = ""  # quoted utterance span, when known
    confidence: float | None = None


class UtteranceTerms(BaseModel):
    """Output of ``utterance_term``: which terms the utterance addresses."""

    node: Literal["utterance_term"] = "utterance_term"
    scenario_id: str
    term_refs: list[TermRef] = Field(default_factory=list)
    provenance: Provenance | None = None

    def term_ids(self) -> set[str]:
        return {ref.term_id for ref in self.term_refs}


class FieldToTerm(BaseModel):
    """One register field mapped onto a vocabulary term."""

    term_id: str
    register_id: str
    field: str
    transform: str = ""  # human-readable transform, e.g. "customer_type == 'consumer'"


class RecordTermMap(BaseModel):
    """Output of ``record_term``: the field-to-term mapping for one register."""

    node: Literal["record_term"] = "record_term"
    register_id: str
    mappings: list[FieldToTerm] = Field(default_factory=list)
    provenance: Provenance | None = None
