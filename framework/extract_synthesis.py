"""Catalog-held-out domain synthesis for experiment (i).

Selection-mode extraction (`llm.extract_domain_artifact`) stays the ablation:
it chooses ids from the gold catalogs. This module asks a model to *invent*
boolean claims and `allow_if_all` / `deny_if_all` rules from statute text
plus the paper outcome vocabulary only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from pydantic import BaseModel, Field

from logic_levels import LOGIC_LEVEL_SPECS
from metadata import sha256_text, utc_timestamp
from schemas import (
    ClaimSource,
    DomainArtifact,
    DomainClaim,
    DomainRule,
    ExtractionRunMetadata,
    LogicLevel,
    OutcomeDefinition,
    PromptMetadata,
    RuleKind,
)

FRAMEWORK_ROOT = Path(__file__).resolve().parent
SYNTHESIS_SYSTEM_PROMPT_PATH = (
    FRAMEWORK_ROOT / "prompts" / "synthesis" / "system.propositional.txt"
)
SYNTHESIS_USER_PROMPT_PATH = FRAMEWORK_ROOT / "prompts" / "synthesis" / "user.txt"

PAPER_OUTCOMES_EXPLANATION = (
    "ALLOW — the request is granted.\n"
    "DENY — the request is refused.\n"
    "NEED_MORE_INFO — a required fact is still unknown (register or applicant). "
    "The solver reports this when an allow-rule is open on unresolved premises."
)

_ATOM_RE = re.compile(r"[A-Za-z0-9]+")


class SynthesizedClaim(BaseModel):
    """One free-form claim invented by the synthesis extractor."""

    claim_id: str
    lowered_atom: str = ""
    label: str = ""
    source_type: ClaimSource = ClaimSource.USER
    formal_text: str = ""
    description: str = ""


class SynthesizedRule(BaseModel):
    """One free-form rule invented by the synthesis extractor."""

    rule_id: str
    kind: RuleKind | str
    label: str = ""
    when_claim_ids: list[str] = Field(default_factory=list)
    target_outcome_id: str | None = None
    target_claim_id: str | None = None
    formal_text: str = ""
    lowered_formula: str = ""


class SynthesisResponse(BaseModel):
    """Structured JSON the synthesis prompt is asked to return."""

    title: str = "synthesized"
    claims: list[SynthesizedClaim] = Field(default_factory=list)
    rules: list[SynthesizedRule] = Field(default_factory=list)
    allow_outcome_id: str = "allow"
    deny_outcome_id: str = "deny"
    summary: str = ""


@dataclass(frozen=True)
class MappedSynthesis:
    """Domain artifact plus defensive drop counts from one synthesis response."""

    artifact: DomainArtifact
    dropped_rules: int
    dropped_claims: int = 0


CompleteFn = Callable[..., Any]


def _load_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _slug_atom(claim_id: str) -> str:
    parts = _ATOM_RE.findall(claim_id)
    return "_".join(part.upper() for part in parts) or "CLAIM"


def _coerce_kind(kind: RuleKind | str) -> RuleKind | None:
    if isinstance(kind, RuleKind):
        return kind
    try:
        return RuleKind(str(kind).strip())
    except ValueError:
        return None


def _rule_formula(when_atoms: list[str], conclusion: str) -> str:
    premise = " AND ".join(when_atoms)
    if len(when_atoms) > 1:
        return f"({premise}) -> {conclusion}"
    if when_atoms:
        return f"{premise} -> {conclusion}"
    return f"-> {conclusion}"


def resolve_complete_fn(complete_fn: CompleteFn | None) -> CompleteFn:
    """Return an injectable structured-completion callable.

    Preference: the caller-supplied ``complete_fn``; else ``providers`` if that
    module is importable (WS-B); else ``llm.gemini_structured_completion``.
    The callable is expected to accept the Gemini helper kwargs
    (``system_instruction``, ``user_content``, ``response_model``) and return a
    parsed pydantic model. A providers-style ``complete(system=, user=)``
    returning ``.parsed`` is wrapped when needed.
    """
    if complete_fn is not None:
        return complete_fn
    try:
        from providers import get_provider  # type: ignore[import-not-found]
    except ImportError:
        from llm import gemini_structured_completion

        return gemini_structured_completion

    def _via_provider(
        *,
        system_instruction: str,
        user_content: str,
        response_model: type,
        **kwargs: Any,
    ) -> Any:
        provider_name = str(kwargs.get("provider") or "gemini")
        try:
            provider = get_provider(provider_name)
        except Exception:
            from llm import gemini_structured_completion

            return gemini_structured_completion(
                system_instruction=system_instruction,
                user_content=user_content,
                response_model=response_model,
                **kwargs,
            )
        result = provider.complete(
            system=system_instruction,
            user=user_content,
            response_model=response_model,
            temperature=float(kwargs.get("temperature") or 0.0),
        )
        if getattr(result, "skipped", False):
            raise RuntimeError(getattr(result, "skip_reason", "") or "provider skipped")
        return result.parsed

    return _via_provider


def render_synthesis_prompts(law_text: str) -> tuple[str, str]:
    """Render the shared synthesis system and user prompts (catalog held out)."""
    system_text = _load_prompt(SYNTHESIS_SYSTEM_PROMPT_PATH)
    user_template = _load_prompt(SYNTHESIS_USER_PROMPT_PATH)
    user_text = user_template.format(
        law_text=law_text,
        paper_outcomes=PAPER_OUTCOMES_EXPLANATION,
    )
    return system_text, user_text


def map_synthesis_response(
    response: SynthesisResponse,
    *,
    law_text: str,
    title: str = "synthesized",
    run_metadata: ExtractionRunMetadata | None = None,
) -> MappedSynthesis:
    """Convert a synthesis JSON blob into a checked ``DomainArtifact``.

    Invalid rules are skipped rather than raising; ``dropped_rules`` counts them.
    """
    allow_outcome_id = (response.allow_outcome_id or "allow").strip() or "allow"
    deny_outcome_id = (response.deny_outcome_id or "deny").strip() or "deny"
    if allow_outcome_id == deny_outcome_id:
        deny_outcome_id = "deny" if allow_outcome_id != "deny" else "deny_outcome"

    claims: list[DomainClaim] = []
    seen_ids: set[str] = set()
    dropped_claims = 0
    for item in response.claims:
        claim_id = (item.claim_id or "").strip()
        if not claim_id or claim_id in seen_ids:
            dropped_claims += 1
            continue
        seen_ids.add(claim_id)
        lowered = (item.lowered_atom or "").strip() or _slug_atom(claim_id)
        label = (item.label or "").strip() or claim_id
        formal = (item.formal_text or "").strip() or lowered
        try:
            source_type = (
                item.source_type
                if isinstance(item.source_type, ClaimSource)
                else ClaimSource(str(item.source_type))
            )
        except ValueError:
            source_type = ClaimSource.USER
        claims.append(
            DomainClaim(
                claim_id=claim_id,
                lowered_atom=lowered,
                label=label,
                description=(item.description or "").strip() or label,
                source_type=source_type,
                formal_text=formal,
            )
        )

    atom_by_id = {claim.claim_id: claim.lowered_atom for claim in claims}
    known_claim_ids = set(atom_by_id)
    outcomes = [
        OutcomeDefinition(
            outcome_id=allow_outcome_id,
            lowered_atom=_slug_atom(allow_outcome_id),
            label="Allow",
            formal_text="ALLOW",
        ),
        OutcomeDefinition(
            outcome_id=deny_outcome_id,
            lowered_atom=_slug_atom(deny_outcome_id),
            label="Deny",
            formal_text="DENY",
        ),
    ]
    outcome_atoms = {item.outcome_id: item.lowered_atom for item in outcomes}

    rules: list[DomainRule] = []
    dropped_rules = 0
    seen_rule_ids: set[str] = set()
    for item in response.rules:
        rule_id = (item.rule_id or "").strip()
        kind = _coerce_kind(item.kind)
        when_ids = [cid.strip() for cid in item.when_claim_ids if cid and cid.strip()]
        if not rule_id or rule_id in seen_rule_ids or kind is None or not when_ids:
            dropped_rules += 1
            continue
        if any(cid not in known_claim_ids for cid in when_ids):
            dropped_rules += 1
            continue
        target_outcome_id = (item.target_outcome_id or None) or None
        target_claim_id = (item.target_claim_id or None) or None
        if kind == RuleKind.SET_FALSE_IF_ALL:
            if not target_claim_id or target_claim_id not in known_claim_ids or target_outcome_id:
                dropped_rules += 1
                continue
        else:
            if target_claim_id:
                dropped_rules += 1
                continue
            if not target_outcome_id:
                target_outcome_id = (
                    allow_outcome_id if kind == RuleKind.ALLOW_IF_ALL else deny_outcome_id
                )
            if target_outcome_id not in outcome_atoms:
                dropped_rules += 1
                continue
        when_atoms = [atom_by_id[cid] for cid in when_ids]
        if kind == RuleKind.SET_FALSE_IF_ALL:
            conclusion = f"NOT {atom_by_id[target_claim_id]}"
        else:
            conclusion = outcome_atoms[target_outcome_id]
        formula = (item.formal_text or "").strip() or _rule_formula(when_atoms, conclusion)
        lowered = (item.lowered_formula or "").strip() or _rule_formula(when_atoms, conclusion)
        try:
            rules.append(
                DomainRule(
                    rule_id=rule_id,
                    kind=kind,
                    label=(item.label or "").strip() or rule_id,
                    when_claim_ids=when_ids,
                    formal_text=formula,
                    lowered_formula=lowered,
                    target_outcome_id=target_outcome_id,
                    target_claim_id=target_claim_id,
                )
            )
        except (ValueError, TypeError):
            dropped_rules += 1
            continue
        seen_rule_ids.add(rule_id)

    artifact = DomainArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        title=(title or response.title or "synthesized").strip() or "synthesized",
        law_text=law_text,
        lowered_view_note=LOGIC_LEVEL_SPECS[LogicLevel.PROPOSITIONAL].lowering_note,
        allow_outcome_id=allow_outcome_id,
        deny_outcome_id=deny_outcome_id,
        run_metadata=run_metadata or ExtractionRunMetadata(),
        claims=claims,
        outcomes=outcomes,
        rules=rules,
    )
    return MappedSynthesis(
        artifact=artifact,
        dropped_rules=dropped_rules,
        dropped_claims=dropped_claims,
    )


def synthesize_domain(
    law_text: str,
    *,
    complete_fn: CompleteFn,
    title: str = "synthesized",
    stats: dict[str, Any] | None = None,
    model: str | None = None,
) -> DomainArtifact:
    """Run catalog-held-out synthesis and return a ``DomainArtifact``.

    ``complete_fn`` is required so tests can inject a fake (no live API).
    Invalid rules are skipped; pass ``stats`` to recover ``dropped_rules``.
    """
    system_instruction, user_content = render_synthesis_prompts(law_text)
    try:
        from providers import invoke_structured
    except ImportError:
        invoke_structured = None
    if invoke_structured is not None:
        response = invoke_structured(
            complete_fn,
            system=system_instruction,
            user=user_content,
            response_model=SynthesisResponse,
        )
    else:
        raw = complete_fn(
            system_instruction=system_instruction,
            user_content=user_content,
            response_model=SynthesisResponse,
            model=model,
        )
        if isinstance(raw, SynthesisResponse):
            response = raw
        elif isinstance(raw, Mapping):
            response = SynthesisResponse.model_validate(raw)
        else:
            response = SynthesisResponse.model_validate(raw)

    run_metadata = ExtractionRunMetadata(
        generated_at_utc=utc_timestamp(),
        model_name=model or "synthesis",
        prompt=PromptMetadata(
            system_prompt_path=str(SYNTHESIS_SYSTEM_PROMPT_PATH),
            user_prompt_path=str(SYNTHESIS_USER_PROMPT_PATH),
            system_prompt_sha256=sha256_text(system_instruction),
            user_prompt_sha256=sha256_text(user_content),
        ),
    )
    mapped = map_synthesis_response(
        response,
        law_text=law_text,
        title=title or response.title or "synthesized",
        run_metadata=run_metadata,
    )
    if stats is not None:
        stats["dropped_rules"] = mapped.dropped_rules
        stats["dropped_claims"] = mapped.dropped_claims
    return mapped.artifact
