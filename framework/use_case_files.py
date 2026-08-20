"""Generic file-backed use-case and scenario loaders for `framework`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from schemas import ClaimSource, LawReference, LogicLevel, RuleKind


FRAMEWORK_ROOT = Path(__file__).resolve().parent
EXAMPLES_ROOT = FRAMEWORK_ROOT / "examples"


class UseCaseClaimTemplate(BaseModel):
    """One externally defined claim template."""

    claim_id: str
    lowered_atom: str
    label: str
    description: str
    source_type: ClaimSource
    propositional: str
    predicate: str
    higher_order: str
    law_references: list[LawReference] = Field(default_factory=list)
    request_cue_groups: list[list[str]] = Field(default_factory=list)
    law_cue_groups: list[list[str]] = Field(default_factory=list)


class UseCaseOutcomeTemplate(BaseModel):
    """One externally defined outcome template."""

    outcome_id: str
    lowered_atom: str
    label: str
    propositional: str
    predicate: str
    higher_order: str
    administrative_role: Literal["allow", "deny"] | None = None


class UseCaseRuleTemplate(BaseModel):
    """One externally defined rule template."""

    rule_id: str
    kind: RuleKind
    label: str
    when_claim_ids: list[str]
    target_outcome_id: str | None = None
    target_claim_id: str | None = None
    law_references: list[LawReference] = Field(default_factory=list)
    law_cue_groups: list[list[str]] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_target_shape(self) -> "UseCaseRuleTemplate":
        """Ensure rule targets match the rule kind."""
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


class UseCaseDefinition(BaseModel):
    """One use-case definition loaded from `examples/`."""

    title: str
    description: str = ""
    default_logic_level: LogicLevel = LogicLevel.PROPOSITIONAL
    claims: list[UseCaseClaimTemplate]
    outcomes: list[UseCaseOutcomeTemplate]
    rules: list[UseCaseRuleTemplate]

    @model_validator(mode="after")
    def validate_internal_references(self) -> "UseCaseDefinition":
        """Ensure the external file defines a coherent closed set of ids."""
        claim_ids = [claim.claim_id for claim in self.claims]
        outcome_ids = [outcome.outcome_id for outcome in self.outcomes]
        rule_ids = [rule.rule_id for rule in self.rules]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("Duplicate claim ids in use case definition.")
        if len(outcome_ids) != len(set(outcome_ids)):
            raise ValueError("Duplicate outcome ids in use case definition.")
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("Duplicate rule ids in use case definition.")
        known_claim_ids = set(claim_ids)
        known_outcome_ids = set(outcome_ids)
        for rule in self.rules:
            unknown_claim_ids = sorted(set(rule.when_claim_ids) - known_claim_ids)
            if unknown_claim_ids:
                raise ValueError(
                    f"Rule `{rule.rule_id}` references unknown claim ids: {', '.join(unknown_claim_ids)}"
                )
            if rule.target_claim_id and rule.target_claim_id not in known_claim_ids:
                raise ValueError(
                    f"Rule `{rule.rule_id}` references unknown target claim `{rule.target_claim_id}`."
                )
            if rule.target_outcome_id and rule.target_outcome_id not in known_outcome_ids:
                raise ValueError(
                    f"Rule `{rule.rule_id}` references unknown target outcome `{rule.target_outcome_id}`."
                )
        if self.allow_outcome_id is None or self.deny_outcome_id is None:
            raise ValueError("Use case definition must mark one allow and one deny outcome.")
        return self

    @property
    def claim_by_id(self) -> dict[str, UseCaseClaimTemplate]:
        """Index claim templates by id."""
        return {claim.claim_id: claim for claim in self.claims}

    @property
    def outcome_by_id(self) -> dict[str, UseCaseOutcomeTemplate]:
        """Index outcome templates by id."""
        return {outcome.outcome_id: outcome for outcome in self.outcomes}

    @property
    def rule_by_id(self) -> dict[str, UseCaseRuleTemplate]:
        """Index rule templates by id."""
        return {rule.rule_id: rule for rule in self.rules}

    @property
    def allow_outcome_id(self) -> str | None:
        """Return the outcome id mapped to administrative ALLOW."""
        for outcome in self.outcomes:
            if outcome.administrative_role == "allow":
                return outcome.outcome_id
        return None

    @property
    def deny_outcome_id(self) -> str | None:
        """Return the outcome id mapped to administrative DENY."""
        for outcome in self.outcomes:
            if outcome.administrative_role == "deny":
                return outcome.outcome_id
        return None


class ScenarioDefinition(BaseModel):
    """One deterministic or live scenario definition stored under `examples/`."""

    name: str
    description: str
    request_file: str
    law_file: str
    mock_db_file: str = "mock_db.json"
    intent_assignments: dict[str, bool | None] = Field(default_factory=dict)
    intent_user_prompt_file: str | None = None
    domain_user_prompt_file: str | None = None


def load_use_case(path: str | Path) -> UseCaseDefinition:
    """Load one use-case definition from JSON."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return UseCaseDefinition.model_validate(raw)


def load_use_case_from_dir(directory: str | Path) -> UseCaseDefinition:
    """Load `use_case.json` from one example directory."""
    return load_use_case(Path(directory) / "use_case.json")


def load_scenario(path: str | Path) -> ScenarioDefinition:
    """Load one scenario JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return ScenarioDefinition.model_validate(raw)


def discover_scenario_files() -> list[Path]:
    """Discover all scenario files under `examples/*/scenarios/`."""
    return sorted(EXAMPLES_ROOT.glob("*/scenarios/*.json"))


def scenario_names() -> list[str]:
    """Return stable scenario names discovered from the example files."""
    return [path.stem for path in discover_scenario_files()]


def scenario_file_by_name(name: str) -> Path:
    """Resolve one scenario name to its JSON file."""
    for path in discover_scenario_files():
        if path.stem == name:
            return path
    raise KeyError(f"Unknown scenario `{name}`.")


def example_dir_for_scenario(path: str | Path) -> Path:
    """Return the example directory that owns the scenario file."""
    return Path(path).resolve().parents[1]


def resolve_example_path(example_dir: str | Path, relative_path: str) -> Path:
    """Resolve a path stored inside a use-case or scenario file."""
    return (Path(example_dir).resolve() / relative_path).resolve()


def _normalize_text(text: str) -> str:
    """Normalize free text for lightweight cue matching."""
    return text.casefold()


def _matches_all_groups(text: str, cue_groups: list[list[str]]) -> bool:
    """Return whether each cue group has at least one matching term."""
    if not cue_groups:
        return True
    normalized = _normalize_text(text)
    return all(any(term.casefold() in normalized for term in group) for group in cue_groups)


def request_mentions_claim(use_case: UseCaseDefinition, claim_id: str, request_text: str) -> bool:
    """Return whether the request text mentions the claim's cue groups."""
    template = use_case.claim_by_id[claim_id]
    if not template.request_cue_groups:
        return False
    return _matches_all_groups(request_text, template.request_cue_groups)


def law_supports_use_case(use_case: UseCaseDefinition, law_text: str) -> bool:
    """Return whether the law text grounds at least one decision rule and one claim."""
    grounded_claim = any(law_supports_claim(use_case, claim.claim_id, law_text) for claim in use_case.claims)
    grounded_rule = any(law_supports_rule(use_case, rule.rule_id, law_text) for rule in use_case.rules)
    return grounded_claim and grounded_rule


def law_supports_claim(use_case: UseCaseDefinition, claim_id: str, law_text: str) -> bool:
    """Return whether the law text grounds the selected claim."""
    template = use_case.claim_by_id[claim_id]
    return _matches_all_groups(law_text, template.law_cue_groups)


def law_supports_rule(use_case: UseCaseDefinition, rule_id: str, law_text: str) -> bool:
    """Return whether the law text grounds the selected rule."""
    template = use_case.rule_by_id[rule_id]
    return _matches_all_groups(law_text, template.law_cue_groups)
