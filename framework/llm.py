"""Tiny structured LLM helpers for `framework` intent and domain extraction."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Any, Callable, TypeVar

from pydantic import BaseModel, Field

from logic_levels import (
    build_domain_artifact,
    build_intent_artifact,
    claim_catalog_text,
    ensure_executable_logic_level,
    outcome_catalog_text,
    rule_catalog_text,
)
from metadata import normalized_path, sha256_text, utc_timestamp
from schemas import (
    DomainArtifact,
    EvidenceSnippet,
    ExtractionRunMetadata,
    IntentArtifact,
    LogicLevel,
    PromptMetadata,
)
from use_case_files import (
    UseCaseDefinition,
    law_supports_claim,
    law_supports_rule,
    law_supports_use_case,
    load_use_case_from_dir,
    request_mentions_claim,
)

T = TypeVar("T", bound=BaseModel)

_DEFAULT_MODEL_ENV = "FRAMEWORK_GEMINI_MODEL"
_API_KEY_ENVS = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
_UNKNOWN_SENTENCE_PATTERN = re.compile(
    r"\b("
    r"i do not know|don't know|do not yet know|not sure|unclear|unknown|unsure|"
    r"have not confirmed|has not been confirmed|cannot yet confirm"
    r")\b",
    re.IGNORECASE,
)


class IntentExtractionItem(BaseModel):
    """One claim valuation returned by the LLM."""

    claim_id: str
    value: bool | None = None
    reason: str = ""
    provenance: list[EvidenceSnippet] = Field(default_factory=list)


class IntentExtractionResponse(BaseModel):
    """Structured response for the intent extraction step."""

    claims: list[IntentExtractionItem]


class DomainExtractionResponse(BaseModel):
    """Structured response for the domain extraction step."""

    title: str
    claim_ids: list[str]
    rule_ids: list[str]
    summary: str = ""


class UserInputExtractionItem(BaseModel):
    """One claim response returned by the LLM user-input extractor (step 00)."""

    claim_id: str
    value: bool | None = None
    confidence: float = 0.0
    needs_user_confirmation: bool = False
    reason: str = ""
    evidence: list[EvidenceSnippet] = Field(default_factory=list)


class UserInputExtractionResponse(BaseModel):
    """Structured response for the step-00 user-input extraction step."""

    claims: list[UserInputExtractionItem]


def default_model_name() -> str:
    """Return the configured Gemini model name for `framework`."""
    return os.environ.get(_DEFAULT_MODEL_ENV, "gemini-2.5-pro").strip() or "gemini-2.5-pro"


def resolve_api_key(explicit: str | None = None) -> str:
    """Resolve the Gemini API key from explicit input or environment."""
    if explicit and explicit.strip():
        return explicit.strip()
    for env_name in _API_KEY_ENVS:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    raise RuntimeError("No Gemini API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY.")


def gemini_structured_completion(
    *,
    system_instruction: str,
    user_content: str,
    response_model: type[T],
    model: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.0,
) -> T:
    """Call Gemini once with a Pydantic-backed JSON schema."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=resolve_api_key(api_key))
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        response_mime_type="application/json",
        response_json_schema=response_model.model_json_schema(),
    )
    response = client.models.generate_content(
        model=model or default_model_name(),
        contents=user_content,
        config=config,
    )
    if not response.text:
        raise RuntimeError("Empty Gemini response.")
    return response_model.model_validate(json.loads(response.text))


def _validate_known_ids(ids: list[str], known_ids: set[str], kind: str) -> list[str]:
    """Reject unknown ids early so the checked artifacts stay stable."""
    bad = sorted(set(ids) - known_ids)
    if bad:
        raise ValueError(f"Unknown {kind} ids from LLM response: {', '.join(bad)}")
    return ids


def default_system_prompt_path(use_case_dir: str | Path, kind: str, logic_level: LogicLevel) -> Path:
    """Return the default system prompt path inside one use-case directory."""
    return Path(use_case_dir).resolve() / "prompts" / kind / f"system.{logic_level.value}.txt"


def default_user_prompt_path(use_case_dir: str | Path, kind: str) -> Path:
    """Return the default user prompt path inside one use-case directory."""
    return Path(use_case_dir).resolve() / "prompts" / kind / "user.txt"


def load_prompt_text(path: str | Path) -> str:
    """Load a prompt template from disk."""
    return Path(path).read_text(encoding="utf-8")


def render_prompt_template(template_text: str, **kwargs: str) -> str:
    """Fill a prompt template with the provided placeholders."""
    return template_text.format(**kwargs)


def build_intent_prompts(
    use_case: UseCaseDefinition,
    use_case_dir: str | Path,
    request_text: str,
    logic_level: LogicLevel,
    *,
    system_prompt_path: str | Path | None = None,
    user_prompt_path: str | Path | None = None,
) -> tuple[str, str, Path, Path]:
    """Build the rendered system and user prompts for step 1."""
    ensure_executable_logic_level(logic_level)
    resolved_system_prompt_path = Path(
        system_prompt_path or default_system_prompt_path(use_case_dir, "intent", logic_level)
    ).resolve()
    resolved_user_prompt_path = Path(
        user_prompt_path or default_user_prompt_path(use_case_dir, "intent")
    ).resolve()
    system_text = load_prompt_text(resolved_system_prompt_path)
    user_template = load_prompt_text(resolved_user_prompt_path)
    user_text = render_prompt_template(
        user_template,
        logic_level=logic_level.value,
        request_text=request_text,
        claim_catalog=claim_catalog_text(use_case, logic_level),
        rule_catalog=rule_catalog_text(use_case, logic_level),
        outcome_catalog=outcome_catalog_text(use_case, logic_level),
    )
    return system_text, user_text, resolved_system_prompt_path, resolved_user_prompt_path


def build_user_input_prompts(
    use_case: UseCaseDefinition,
    use_case_dir: str | Path,
    utterances: list[Any],
    logic_level: LogicLevel,
    *,
    system_prompt_path: str | Path | None = None,
    user_prompt_path: str | Path | None = None,
) -> tuple[str, str, Path, Path]:
    """Build the rendered system and user prompts for step 00 user-input extraction.

    The system prompt prefers a per-case file at
    ``<use_case_dir>/prompts/user_input/system.<level>.txt`` and falls back
    to a repo-wide default under ``framework/prompts/user_input/``. The
    user prompt is the shared template under ``framework/prompts/user_input/``.
    """
    ensure_executable_logic_level(logic_level)

    framework_root = Path(__file__).resolve().parent
    shared_system_default = (
        framework_root / "prompts" / "user_input" / f"system.{logic_level.value}.txt"
    )
    per_case_system = (
        Path(use_case_dir).resolve()
        / "prompts"
        / "user_input"
        / f"system.{logic_level.value}.txt"
    )
    if system_prompt_path is not None:
        resolved_system_prompt_path = Path(system_prompt_path).resolve()
    elif per_case_system.exists():
        resolved_system_prompt_path = per_case_system
    else:
        resolved_system_prompt_path = shared_system_default

    shared_user_default = framework_root / "prompts" / "user_input" / "user.txt"
    resolved_user_prompt_path = Path(
        user_prompt_path or shared_user_default
    ).resolve()

    system_text = load_prompt_text(resolved_system_prompt_path)
    user_template = load_prompt_text(resolved_user_prompt_path)
    utterances_block = "\n".join(
        f"- [{utterance.source}] {utterance.text}" for utterance in utterances
    ) or "(no utterances supplied)"
    user_text = render_prompt_template(
        user_template,
        logic_level=logic_level.value,
        utterances_block=utterances_block,
        claim_catalog=claim_catalog_text(use_case, logic_level),
    )
    return system_text, user_text, resolved_system_prompt_path, resolved_user_prompt_path


def build_domain_prompts(
    use_case: UseCaseDefinition,
    use_case_dir: str | Path,
    law_text: str,
    logic_level: LogicLevel,
    *,
    system_prompt_path: str | Path | None = None,
    user_prompt_path: str | Path | None = None,
) -> tuple[str, str, Path, Path]:
    """Build the rendered system and user prompts for step 2."""
    ensure_executable_logic_level(logic_level)
    resolved_system_prompt_path = Path(
        system_prompt_path or default_system_prompt_path(use_case_dir, "domain", logic_level)
    ).resolve()
    resolved_user_prompt_path = Path(
        user_prompt_path or default_user_prompt_path(use_case_dir, "domain")
    ).resolve()
    system_text = load_prompt_text(resolved_system_prompt_path)
    user_template = load_prompt_text(resolved_user_prompt_path)
    user_text = render_prompt_template(
        user_template,
        logic_level=logic_level.value,
        law_text=law_text,
        claim_catalog=claim_catalog_text(use_case, logic_level),
        rule_catalog=rule_catalog_text(use_case, logic_level),
        outcome_catalog=outcome_catalog_text(use_case, logic_level),
    )
    return system_text, user_text, resolved_system_prompt_path, resolved_user_prompt_path


def _prompt_metadata(
    *,
    system_prompt_path: Path,
    user_prompt_path: Path,
    system_text: str,
    user_text: str,
) -> PromptMetadata:
    """Build the prompt metadata block stored inside artifacts."""
    return PromptMetadata(
        system_prompt_path=str(system_prompt_path),
        user_prompt_path=str(user_prompt_path),
        system_prompt_sha256=sha256_text(system_text),
        user_prompt_sha256=sha256_text(user_text),
    )


def _sentence_fragments(text: str) -> list[str]:
    """Split a request into short fragments for local cue checks."""
    return [fragment.strip() for fragment in re.split(r"[.!?\n]+", text) if fragment.strip()]


def _claim_fragments(use_case: UseCaseDefinition, request_text: str, claim_id: str) -> list[str]:
    """Return fragments that locally mention the selected claim."""
    return [
        fragment
        for fragment in _sentence_fragments(request_text)
        if request_mentions_claim(use_case, claim_id, fragment)
    ]


def _post_validate_intent_assignments(
    use_case: UseCaseDefinition,
    request_text: str,
    assignments: dict[str, bool | None],
    reasons: dict[str, str],
) -> None:
    """Keep explicit uncertainty as `null` instead of collapsing it into `false` or `true`."""
    for claim_id, value in list(assignments.items()):
        if value is None:
            continue
        fragments = _claim_fragments(use_case, request_text, claim_id)
        if not fragments:
            continue
        explicit_unknown = any(_UNKNOWN_SENTENCE_PATTERN.search(fragment) for fragment in fragments)
        if explicit_unknown:
            assignments[claim_id] = None
            prior_reason = reasons.get(claim_id, "")
            reasons[claim_id] = (
                "Post-validation kept this claim unresolved because the request text expresses uncertainty."
                + (f" Original extractor note: {prior_reason}" if prior_reason else "")
            )


def _coherent_domain_ids(
    use_case: UseCaseDefinition,
    law_text: str,
    claim_ids: list[str],
    rule_ids: list[str],
) -> tuple[list[str], list[str]]:
    """Prune claim and rule ids that are not grounded in the supplied law text."""
    if not law_supports_use_case(use_case, law_text):
        return [], []

    grounded_claim_ids = {
        claim_id for claim_id in claim_ids if law_supports_claim(use_case, claim_id, law_text)
    }
    grounded_rule_ids: list[str] = []
    for rule_id in rule_ids:
        rule = use_case.rule_by_id[rule_id]
        if not law_supports_rule(use_case, rule_id, law_text):
            continue
        if any(
            not law_supports_claim(use_case, claim_id, law_text)
            for claim_id in rule.when_claim_ids
        ):
            continue
        if rule.target_claim_id and not law_supports_claim(use_case, rule.target_claim_id, law_text):
            continue
        grounded_rule_ids.append(rule_id)
        grounded_claim_ids.update(rule.when_claim_ids)
        if rule.target_claim_id:
            grounded_claim_ids.add(rule.target_claim_id)
    return sorted(grounded_claim_ids), grounded_rule_ids


def extract_intent_artifact(
    use_case_dir: str | Path,
    request_text: str,
    logic_level: LogicLevel,
    *,
    system_prompt_path: str | Path | None = None,
    user_prompt_path: str | Path | None = None,
    source_path: str | Path | None = None,
    generator: Callable[..., Any] = gemini_structured_completion,
    model: str | None = None,
    api_key: str | None = None,
) -> IntentArtifact:
    """Run step 1 and convert the structured response into a checked artifact."""
    use_case = load_use_case_from_dir(use_case_dir)
    system_instruction, user_content, resolved_system_prompt_path, resolved_user_prompt_path = build_intent_prompts(
        use_case,
        use_case_dir,
        request_text,
        logic_level,
        system_prompt_path=system_prompt_path,
        user_prompt_path=user_prompt_path,
    )
    response = generator(
        system_instruction=system_instruction,
        user_content=user_content,
        response_model=IntentExtractionResponse,
        model=model,
        api_key=api_key,
    )
    assignments: dict[str, bool | None] = {}
    reasons: dict[str, str] = {}
    snippets: dict[str, list[str]] = {}
    for item in response.claims:
        if item.claim_id not in use_case.claim_by_id:
            raise ValueError(f"Unknown claim id from LLM response: {item.claim_id}")
        assignments[item.claim_id] = item.value
        reasons[item.claim_id] = item.reason
        snippets[item.claim_id] = [evidence.snippet for evidence in item.provenance if evidence.snippet]
    for claim_id in use_case.claim_by_id:
        assignments.setdefault(claim_id, None)
        reasons.setdefault(claim_id, "LLM left this claim unresolved.")
        snippets.setdefault(claim_id, [])
    _post_validate_intent_assignments(use_case, request_text, assignments, reasons)
    run_metadata = ExtractionRunMetadata(
        generated_at_utc=utc_timestamp(),
        model_name=model or default_model_name(),
        source_path=normalized_path(source_path),
        prompt=_prompt_metadata(
            system_prompt_path=resolved_system_prompt_path,
            user_prompt_path=resolved_user_prompt_path,
            system_text=system_instruction,
            user_text=user_content,
        ),
    )
    return build_intent_artifact(
        use_case=use_case,
        request_text=request_text,
        logic_level=logic_level,
        assignments=assignments,
        reasons=reasons,
        snippets=snippets,
        run_metadata=run_metadata,
    )


def extract_domain_artifact(
    use_case_dir: str | Path,
    law_text: str,
    logic_level: LogicLevel,
    *,
    system_prompt_path: str | Path | None = None,
    user_prompt_path: str | Path | None = None,
    source_path: str | Path | None = None,
    generator: Callable[..., Any] = gemini_structured_completion,
    model: str | None = None,
    api_key: str | None = None,
) -> DomainArtifact:
    """Run step 2 and convert the structured response into a checked artifact."""
    use_case = load_use_case_from_dir(use_case_dir)
    system_instruction, user_content, resolved_system_prompt_path, resolved_user_prompt_path = build_domain_prompts(
        use_case,
        use_case_dir,
        law_text,
        logic_level,
        system_prompt_path=system_prompt_path,
        user_prompt_path=user_prompt_path,
    )
    response = generator(
        system_instruction=system_instruction,
        user_content=user_content,
        response_model=DomainExtractionResponse,
        model=model,
        api_key=api_key,
    )
    claim_ids = _validate_known_ids(response.claim_ids, set(use_case.claim_by_id), "claim")
    rule_ids = _validate_known_ids(response.rule_ids, set(use_case.rule_by_id), "rule")
    grounded_claim_ids, grounded_rule_ids = _coherent_domain_ids(use_case, law_text, claim_ids, rule_ids)
    run_metadata = ExtractionRunMetadata(
        generated_at_utc=utc_timestamp(),
        model_name=model or default_model_name(),
        source_path=normalized_path(source_path),
        prompt=_prompt_metadata(
            system_prompt_path=resolved_system_prompt_path,
            user_prompt_path=resolved_user_prompt_path,
            system_text=system_instruction,
            user_text=user_content,
        ),
    )
    full_domain = build_domain_artifact(
        use_case=use_case,
        logic_level=logic_level,
        law_text=law_text,
        title=response.title,
        run_metadata=run_metadata,
    )
    filtered_claims = [claim for claim in full_domain.claims if claim.claim_id in set(grounded_claim_ids)]
    filtered_rules = [rule for rule in full_domain.rules if rule.rule_id in set(grounded_rule_ids)]
    return DomainArtifact(
        logic_level=logic_level,
        title=response.title,
        law_text=law_text,
        lowered_view_note=full_domain.lowered_view_note,
        allow_outcome_id=full_domain.allow_outcome_id,
        deny_outcome_id=full_domain.deny_outcome_id,
        run_metadata=run_metadata,
        claims=filtered_claims,
        outcomes=full_domain.outcomes,
        rules=filtered_rules,
    )
