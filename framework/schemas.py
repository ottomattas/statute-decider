"""Typed schemas for the small four-step `framework` implementation."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class LogicLevel(str, Enum):
    """Supported logic levels for the end-to-end `framework` pipeline."""

    PROPOSITIONAL = "propositional"
    PREDICATE = "predicate"
    HIGHER_ORDER = "higher_order"


class ClaimSource(str, Enum):
    """Authoritative source category for a claim.

    ``expert`` and ``statute_open`` were added in Wave 2 Stream B (ART-64) so
    that the uncertainty taxonomy (see ``framework/uncertainty_routing.py``)
    can distinguish statute-level openness (U1) and expert-required claims
    (U10) from ordinary ``user``/``db`` claims.
    """

    USER = "user"
    DB = "db"
    DERIVED = "derived"
    EXPERT = "expert"
    STATUTE_OPEN = "statute_open"


class RuleKind(str, Enum):
    """Small rule family for one externally defined use case."""

    ALLOW_IF_ALL = "allow_if_all"
    DENY_IF_ALL = "deny_if_all"
    SET_FALSE_IF_ALL = "set_false_if_all"


class SolverOutcome(str, Enum):
    """Administrative outcomes produced by the symbolic layer.

    The last three values were added in Wave 2 Stream B (ART-64) as
    first-class outcomes for the uncertainty taxonomy; see
    ``framework/uncertainty_routing.py`` for the U1..U12 routing.
    """

    ALLOW = "ALLOW"
    DENY = "DENY"
    NEED_DB_INFO = "NEED_DB_INFO"
    NEED_USER_INFO = "NEED_USER_INFO"
    NEED_EXPERT_JUDGMENT = "NEED_EXPERT_JUDGMENT"
    UNDETERMINED_INTERPRETATION = "UNDETERMINED_INTERPRETATION"
    UNVERIFIABLE_CLAIM = "UNVERIFIABLE_CLAIM"


class BlockReasonCode(str, Enum):
    """Neutral blockage codes for trace reporting.

    The nine uncertainty-specific codes below were added in Wave 2 Stream B
    (ART-64). Each corresponds to one entry in the U1..U12 routing table in
    ``framework/uncertainty_routing.py``.
    """

    DOMAIN_EXTRACTION_EMPTY = "domain_extraction_empty"
    DOMAIN_EXTRACTION_SPARSE = "domain_extraction_sparse"
    NO_APPLICABLE_RULES = "no_applicable_rules"
    NEEDS_DB_INFO = "needs_db_info"
    NEEDS_USER_INFO = "needs_user_info"
    SOLVER_INCONSISTENT = "solver_inconsistent"
    STATUTE_UNDERSPECIFIED = "statute_underspecified"
    INTERPRETATION_AMBIGUOUS = "interpretation_ambiguous"
    NO_REGISTER = "no_register"
    PROCESS_INDETERMINATE = "process_indeterminate"
    SUBJECTIVE_PARTY = "subjective_party"
    TRUST_ONLY = "trust_only"
    CONTEXT_DEPENDENT = "context_dependent"
    GLOSSARY_LOW_CONFIDENCE = "glossary_low_confidence"
    MODEL_DRIFT = "model_drift"
    EXPERT_JUDGMENT_REQUIRED = "expert_judgment_required"


class RuleStatus(str, Enum):
    """Trace-level rule state for the current fact valuation."""

    FIRES = "fires"
    BLOCKED = "blocked"
    NEEDS_INFO = "needs_info"


class EvidenceSnippet(BaseModel):
    """Text evidence attached to an extracted claim."""

    snippet: str = ""
    note: str = ""


class PromptMetadata(BaseModel):
    """Prompt file paths and digests for one extraction call."""

    system_prompt_path: str | None = None
    user_prompt_path: str | None = None
    system_prompt_sha256: str = ""
    user_prompt_sha256: str = ""


class ExtractionRunMetadata(BaseModel):
    """Metadata attached to step-1 and step-2 extraction artifacts."""

    generated_at_utc: str = ""
    model_name: str = ""
    source_path: str | None = None
    prompt: PromptMetadata = Field(default_factory=PromptMetadata)


class SolveRunMetadata(BaseModel):
    """Metadata attached to the step-3 solution artifact."""

    generated_at_utc: str = ""
    domain_artifact_path: str | None = None
    intent_artifact_path: str | None = None
    mock_db_path: str | None = None


class LawReference(BaseModel):
    """Link one claim or rule back to the law text excerpt."""

    clause_id: str
    clause_title: str
    clause_text: str
    note: str = ""


class IntentClaim(BaseModel):
    """One machine-readable claim extracted from the user request.

    The three boolean flags below were added in Wave 2 Stream B (ART-64) as
    optional triggers for the U6/U11/U12 uncertainty kinds. They default to
    ``False`` so that existing intent artifacts continue to validate
    unchanged.
    """

    claim_id: str
    lowered_atom: str
    label: str
    description: str
    source_type: ClaimSource
    formal_text: str
    value: bool | None = None
    reason: str = ""
    provenance: list[EvidenceSnippet] = Field(default_factory=list)
    subjective_party: bool = False
    glossary_low_confidence: bool = False
    model_drift: bool = False


class DomainClaim(BaseModel):
    """One claim available in the domain model."""

    claim_id: str
    lowered_atom: str
    label: str
    description: str
    source_type: ClaimSource
    formal_text: str
    law_references: list[LawReference] = Field(default_factory=list)


class OutcomeDefinition(BaseModel):
    """Outcome atom rendered in the selected logic level."""

    outcome_id: str
    lowered_atom: str
    label: str
    formal_text: str


class DomainRule(BaseModel):
    """Readable rule plus its explicit propositional lowering.

    The three boolean flags below were added in Wave 2 Stream B (ART-64) as
    optional rule-level triggers for the U2/U4/U9 uncertainty kinds. They
    default to ``False`` so that existing domain artifacts continue to
    validate unchanged.
    """

    rule_id: str
    kind: RuleKind
    label: str
    when_claim_ids: list[str]
    formal_text: str
    lowered_formula: str
    target_outcome_id: str | None = None
    target_claim_id: str | None = None
    law_references: list[LawReference] = Field(default_factory=list)
    interpretation_ambiguous: bool = False
    process_indeterminate: bool = False
    context_dependent: bool = False

    @model_validator(mode="after")
    def validate_target_shape(self) -> "DomainRule":
        """Ensure each rule points to exactly one valid conclusion shape."""
        if self.kind == RuleKind.SET_FALSE_IF_ALL:
            if not self.target_claim_id or self.target_outcome_id:
                raise ValueError(
                    "set_false_if_all requires target_claim_id and forbids target_outcome_id"
                )
        else:
            if not self.target_outcome_id or self.target_claim_id:
                raise ValueError(
                    "allow_if_all/deny_if_all require target_outcome_id and forbid target_claim_id"
                )
        return self


class IntentArtifact(BaseModel):
    """Checked intent artifact written by step 1."""

    artifact_type: Literal["intent"] = "intent"
    logic_level: LogicLevel
    request_text: str
    lowered_view_note: str = ""
    run_metadata: ExtractionRunMetadata = Field(default_factory=ExtractionRunMetadata)
    claims: list[IntentClaim]


class DomainArtifact(BaseModel):
    """Checked domain artifact written by step 2."""

    artifact_type: Literal["domain"] = "domain"
    logic_level: LogicLevel
    title: str
    law_text: str
    lowered_view_note: str = ""
    allow_outcome_id: str
    deny_outcome_id: str
    run_metadata: ExtractionRunMetadata = Field(default_factory=ExtractionRunMetadata)
    claims: list[DomainClaim]
    outcomes: list[OutcomeDefinition]
    rules: list[DomainRule]


class LookupSource(BaseModel):
    """One local mock database source.

    ``availability`` and ``trust_only`` were added in Wave 2 Stream B
    (ART-64) so that the mock DB can simulate U3 (NO_REGISTER) and U7
    (TRUST_ONLY) for the uncertainty taxonomy. Defaults preserve backward
    compatibility with existing fixtures.
    """

    source_id: str
    label: str
    description: str
    values: dict[str, bool | None]
    availability: Literal["available", "unavailable"] = "available"
    trust_only: bool = False


class MockDbArtifact(BaseModel):
    """Checked mock DB artifact used by step 3."""

    sources: list[LookupSource]


class LookupEvent(BaseModel):
    """One DB lookup batch recorded in the final trace."""

    stage: str
    source_id: str
    source_label: str
    requested_claim_ids: list[str]
    returned_values: dict[str, bool | None]
    note: str = ""


class PremiseEvaluation(BaseModel):
    """One premise row inside a rule trace item."""

    claim_id: str
    label: str
    formal_text: str
    lowered_atom: str
    value: bool | None = None


class RuleTraceRow(BaseModel):
    """One rule's status under the current valuation."""

    rule_id: str
    label: str
    kind: RuleKind
    status: RuleStatus
    formal_text: str
    lowered_formula: str
    premises: list[PremiseEvaluation]
    true_claim_ids: list[str]
    false_claim_ids: list[str]
    unknown_claim_ids: list[str]


class ResolvedClaim(BaseModel):
    """Final or intermediate value for one claim.

    ``uncertainty_code`` was added in Wave 2 Stream B (ART-64) so traces can
    carry the ``U1``..``U12`` label attached to a claim's resolution path
    (e.g. ``U7`` when the value was provided by a trust-only source).
    """

    claim_id: str
    lowered_atom: str
    label: str
    source_type: ClaimSource
    formal_text: str
    value: bool | None = None
    resolved_from: str = "unknown"
    reason: str = ""
    uncertainty_code: str | None = None


class SolveSnapshot(BaseModel):
    """One solver pass over the current fact set."""

    stage: str
    outcome: SolverOutcome
    resolved_claims: list[ResolvedClaim]
    rule_trace: list[RuleTraceRow]
    missing_db_claim_ids: list[str] = Field(default_factory=list)
    missing_user_claim_ids: list[str] = Field(default_factory=list)
    note: str = ""


class TraceEvent(BaseModel):
    """One human-readable event in the final explanation trace."""

    stage: str
    message: str


class CaseBundle(BaseModel):
    """Bundle domain, intent, and mock DB state for solving."""

    logic_level: LogicLevel
    domain: DomainArtifact
    intent: IntentArtifact
    mock_db: MockDbArtifact


class SolutionArtifact(BaseModel):
    """Final artifact written by step 3 and consumed by step 4."""

    artifact_type: Literal["solution"] = "solution"
    logic_level: LogicLevel
    domain_title: str
    request_text: str
    lowered_view_note: str = ""
    final_outcome: SolverOutcome
    intent_metadata: ExtractionRunMetadata = Field(default_factory=ExtractionRunMetadata)
    domain_metadata: ExtractionRunMetadata = Field(default_factory=ExtractionRunMetadata)
    solve_metadata: SolveRunMetadata = Field(default_factory=SolveRunMetadata)
    blocked_at_step: str | None = None
    block_reason_code: BlockReasonCode | None = None
    extracted_claim_count: int = 0
    extracted_rule_count: int = 0
    unresolved_claim_ids: list[str] = Field(default_factory=list)
    intent_claims: list[IntentClaim] = Field(default_factory=list)
    domain_claims: list[DomainClaim] = Field(default_factory=list)
    domain_rules: list[DomainRule] = Field(default_factory=list)
    trace_events: list[TraceEvent] = Field(default_factory=list)
    lookup_events: list[LookupEvent] = Field(default_factory=list)
    snapshots: list[SolveSnapshot] = Field(default_factory=list)
