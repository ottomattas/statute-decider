"""Collect structured user input from free-form utterances.

This module backs step 00 of the `framework` pipeline: turning a short list
of natural-language utterances into a structured `UserInputSession` whose
bridge into `build_intent_artifact` feeds step 01. The deterministic path
lives here and is authoritative; an optional LLM path is provided for
future automation and is kept strictly off by default. See
``docs/reference/nl-extraction.md`` for semantics and U5/U8 routing.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Callable

from pydantic import BaseModel, Field

from schemas import EvidenceSnippet, LogicLevel
from use_case_files import (
    UseCaseDefinition,
    _normalize_text,
    request_mentions_claim,
)


_NEGATION_PATTERN = re.compile(
    r"\b("
    r"not|no|never|n't|cannot|can't|without|neither|nor|none|"
    r"ei ole|ma ei|ei|pole|mitte"
    r")\b",
    re.IGNORECASE,
)

_HEDGE_PATTERN = re.compile(
    r"\b("
    r"i think|i guess|i believe|i suppose|i assume|"
    r"maybe|perhaps|probably|possibly|might be|could be|"
    r"not entirely sure|not completely sure|not fully sure|not 100% sure|"
    r"not sure|unsure|"
    r"fairly sure|pretty sure|somewhat sure|"
    r"arvan|vist|ilmselt|vahest|võib olla|mulle tundub|pole kindel"
    r")\b",
    re.IGNORECASE,
)

_UNKNOWN_PATTERN = re.compile(
    r"\b("
    r"i do not know|i don't know|don't know|do not know|no idea|"
    r"unclear|unknown|"
    r"can't tell|cannot tell|"
    r"ei tea|ma ei tea"
    r")\b",
    re.IGNORECASE,
)

_AFFIRMATION_PATTERN = re.compile(
    r"\b("
    r"yes|yep|correct|confirmed|confirm|indeed|absolutely|definitely|jah|"
    r"i am|i have|i did|we have|we did|it is|it does"
    r")\b",
    re.IGNORECASE,
)


class UserUtterance(BaseModel):
    """One free-form utterance from the applicant or an intake officer."""

    text: str
    source: str = "user"
    timestamp_utc: str | None = None


class ClaimResponse(BaseModel):
    """One claim-level response derived from the utterances."""

    claim_id: str
    value: bool | None = None
    confidence: float = 1.0
    evidence: list[EvidenceSnippet] = Field(default_factory=list)
    needs_user_confirmation: bool = False


class UserInputSession(BaseModel):
    """Aggregate of utterances and per-claim responses for one use case."""

    use_case_id: str
    utterances: list[UserUtterance] = Field(default_factory=list)
    responses: list[ClaimResponse] = Field(default_factory=list)
    unresolved_claim_ids: list[str] = Field(default_factory=list)


def _fragments(text: str) -> list[str]:
    """Split an utterance into short fragments for local cue checks."""
    return [fragment.strip() for fragment in re.split(r"[.!?\n;]+", text) if fragment.strip()]


def _fragment_has(pattern: re.Pattern[str], fragment: str) -> bool:
    return bool(pattern.search(fragment))


def _classify_fragment(fragment: str) -> dict[str, bool]:
    """Classify a fragment for unknown/hedge/negation/affirmation cues."""
    return {
        "unknown": _fragment_has(_UNKNOWN_PATTERN, fragment),
        "hedge": _fragment_has(_HEDGE_PATTERN, fragment),
        "negation": _fragment_has(_NEGATION_PATTERN, fragment),
        "affirmation": _fragment_has(_AFFIRMATION_PATTERN, fragment),
    }


def _claim_keywords(use_case: UseCaseDefinition, claim_id: str) -> list[str]:
    template = use_case.claim_by_id[claim_id]
    keywords: list[str] = []
    for group in template.request_cue_groups:
        keywords.extend(term for term in group if term)
    return keywords


def _negation_near_keyword(fragment: str, keywords: list[str]) -> bool:
    """Check whether a negation token sits adjacent to (but outside) a keyword match.

    Negation inside the keyword itself (e.g. "no conflict" as a positive cue)
    does NOT count — only negation that frames the keyword from outside the
    match span.
    """
    lowered = _normalize_text(fragment)
    for keyword in keywords:
        normalized = keyword.casefold()
        if normalized not in lowered:
            continue
        for match in re.finditer(re.escape(normalized), lowered):
            before = lowered[max(0, match.start() - 48) : match.start()]
            after = lowered[match.end() : min(len(lowered), match.end() + 24)]
            if _NEGATION_PATTERN.search(before):
                return True
            if _NEGATION_PATTERN.search(after):
                return True
    return False


def _response_from_fragments(
    use_case: UseCaseDefinition,
    claim_id: str,
    matching_fragments: list[str],
) -> ClaimResponse:
    """Collapse all matching fragments for one claim into a `ClaimResponse`."""
    keywords = _claim_keywords(use_case, claim_id)
    evidence = [
        EvidenceSnippet(snippet=fragment, note="Matched user text")
        for fragment in matching_fragments
    ]

    any_unknown = False
    any_hedge = False
    any_negation_near = False
    any_plain_affirmation = False
    for fragment in matching_fragments:
        flags = _classify_fragment(fragment)
        any_unknown = any_unknown or flags["unknown"]
        any_hedge = any_hedge or flags["hedge"]
        near = flags["negation"] and _negation_near_keyword(fragment, keywords)
        any_negation_near = any_negation_near or near
        if flags["affirmation"] and not near:
            any_plain_affirmation = True

    if any_unknown:
        return ClaimResponse(
            claim_id=claim_id,
            value=None,
            confidence=0.0,
            evidence=evidence,
            needs_user_confirmation=False,
        )
    if any_hedge:
        return ClaimResponse(
            claim_id=claim_id,
            value=None,
            confidence=0.3,
            evidence=evidence,
            needs_user_confirmation=True,
        )
    if any_negation_near:
        return ClaimResponse(
            claim_id=claim_id,
            value=False,
            confidence=0.9,
            evidence=evidence,
        )
    if any_plain_affirmation:
        return ClaimResponse(
            claim_id=claim_id,
            value=True,
            confidence=0.9,
            evidence=evidence,
        )
    return ClaimResponse(
        claim_id=claim_id,
        value=True,
        confidence=0.7,
        evidence=evidence,
    )


def extract_user_input_deterministic(
    use_case: UseCaseDefinition,
    utterances: list[UserUtterance],
) -> UserInputSession:
    """Deterministic lexical extractor producing a `UserInputSession`.

    Policy:
    - A claim mentioned by a fragment with "I don't know"-style phrasing
      stays unresolved with ``value=None`` and ``needs_user_confirmation=False``.
    - A hedged mention ("I think so but I'm not sure") yields ``value=None``
      and ``needs_user_confirmation=True`` — the U8 follow-up trigger.
    - An explicit negation near the keyword yields ``value=False``.
    - A plain positive mention yields ``value=True``.
    - A claim with no matching fragment at all is recorded in
      ``unresolved_claim_ids`` — this is the U5 signal downstream.
    """
    all_fragments: list[str] = []
    for utterance in utterances:
        all_fragments.extend(_fragments(utterance.text))

    responses: list[ClaimResponse] = []
    unresolved: list[str] = []
    for claim_id in use_case.claim_by_id:
        matching = [
            fragment
            for fragment in all_fragments
            if request_mentions_claim(use_case, claim_id, fragment)
        ]
        if not matching:
            unresolved.append(claim_id)
            continue
        responses.append(_response_from_fragments(use_case, claim_id, matching))

    return UserInputSession(
        use_case_id=use_case.title,
        utterances=list(utterances),
        responses=responses,
        unresolved_claim_ids=unresolved,
    )


def session_to_intent_assignments(
    session: UserInputSession,
) -> tuple[dict[str, bool | None], dict[str, str], dict[str, list[str]]]:
    """Bridge session responses into the tuple accepted by ``build_intent_artifact``.

    The returned ``reasons`` map includes a ``needs_user_confirmation=true``
    marker whenever a response is hedged so that downstream code can emit a
    U8 follow-up. ``snippets`` carries the raw matched fragments used as
    provenance.
    """
    assignments: dict[str, bool | None] = {}
    reasons: dict[str, str] = {}
    snippets: dict[str, list[str]] = {}
    for response in session.responses:
        assignments[response.claim_id] = response.value
        reason_parts: list[str] = []
        if response.needs_user_confirmation:
            reason_parts.append("needs_user_confirmation=true")
        reason_parts.append(f"confidence={response.confidence:.2f}")
        if response.value is None and not response.needs_user_confirmation:
            reason_parts.append("user expressed explicit uncertainty")
        reasons[response.claim_id] = "; ".join(reason_parts)
        snippets[response.claim_id] = [
            item.snippet for item in response.evidence if item.snippet
        ]
    for claim_id in session.unresolved_claim_ids:
        assignments.setdefault(claim_id, None)
        reasons.setdefault(
            claim_id,
            "No utterance mentioned this claim; routed to NEED_DB_INFO/NEED_USER_INFO downstream.",
        )
        snippets.setdefault(claim_id, [])
    return assignments, reasons, snippets


def _default_system_prompt_path(
    use_case_dir: str | Path,
    logic_level: LogicLevel,
) -> Path:
    """Per-case system prompt path for the user-input step."""
    return (
        Path(use_case_dir).resolve()
        / "prompts"
        / "user_input"
        / f"system.{logic_level.value}.txt"
    )


def _shared_system_prompt_path(logic_level: LogicLevel) -> Path:
    """Shared fallback system prompt path for the user-input step."""
    return (
        Path(__file__).resolve().parent
        / "prompts"
        / "user_input"
        / f"system.{logic_level.value}.txt"
    )


def resolve_user_input_system_prompt_path(
    use_case_dir: str | Path,
    logic_level: LogicLevel,
) -> Path:
    """Resolve the system prompt path, preferring the per-case override."""
    per_case = _default_system_prompt_path(use_case_dir, logic_level)
    if per_case.exists():
        return per_case
    return _shared_system_prompt_path(logic_level)


def extract_user_input_llm(
    use_case: UseCaseDefinition,
    utterances: list[UserUtterance],
    *,
    use_case_dir: str | Path,
    logic_level: LogicLevel = LogicLevel.PROPOSITIONAL,
    generator: Callable[..., Any] | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> UserInputSession:
    """LLM-backed extractor. Lazy-imports `llm` so `google.genai` stays optional."""
    from llm import (
        UserInputExtractionResponse,
        build_user_input_prompts,
        gemini_structured_completion,
    )

    active_generator = generator or gemini_structured_completion
    system_text, user_text, _system_path, _user_path = build_user_input_prompts(
        use_case,
        use_case_dir,
        utterances,
        logic_level,
    )
    response = active_generator(
        system_instruction=system_text,
        user_content=user_text,
        response_model=UserInputExtractionResponse,
        model=model,
        api_key=api_key,
    )

    responses: list[ClaimResponse] = []
    seen: set[str] = set()
    for item in response.claims:
        if item.claim_id not in use_case.claim_by_id:
            raise ValueError(f"Unknown claim id from LLM response: {item.claim_id}")
        seen.add(item.claim_id)
        responses.append(
            ClaimResponse(
                claim_id=item.claim_id,
                value=item.value,
                confidence=item.confidence,
                evidence=list(item.evidence),
                needs_user_confirmation=item.needs_user_confirmation,
            )
        )
    unresolved = [
        claim_id for claim_id in use_case.claim_by_id if claim_id not in seen
    ]
    return UserInputSession(
        use_case_id=use_case.title,
        utterances=list(utterances),
        responses=responses,
        unresolved_claim_ids=unresolved,
    )
