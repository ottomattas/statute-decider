"""LLM-only decision baseline for JURIX experiment (ii).

Same inputs the solver runtime sees (statute, case request, known true/false
facts from intent + mock DB) but no symbolic solver. The model returns a
paper 3-way outcome plus a missing-fact set drawn from the claim catalog.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal

from pydantic import BaseModel, Field

from logic_levels import claim_catalog_text
from mock_db import load_mock_db
from scenario_suite import SuiteScenario, _apply_db_overrides, load_suite_scenario
from schemas import CaseBundle, ExtractionRunMetadata, MockDbArtifact
from use_case_files import (
    UseCaseDefinition,
    load_use_case_from_dir,
    resolve_example_path,
)

ProviderComplete = Callable[..., Any]


class BaselineDecision(BaseModel):
    """Structured LLM-only decision (no solver)."""

    outcome: Literal["ALLOW", "DENY", "NEED_MORE_INFO"]
    missing_facts: list[str] = Field(default_factory=list)
    reason: str = ""


@dataclass(frozen=True)
class ScenarioContext:
    """Loaded scenario inputs shared by the LLM-only and runtime rows."""

    path: Path
    scenario: SuiteScenario
    use_case: UseCaseDefinition
    case_dir: Path
    law_text: str
    request_text: str
    mock_db: MockDbArtifact
    known_facts: dict[str, bool]
    unknown_claim_ids: list[str]
    catalog_text: str


_SYSTEM_PROMPT = """You decide a statutory case from the text of the statute and the facts given.

You are not a solver. Do not invent claim identifiers. Use only claim ids that appear in the catalog.

Choose exactly one outcome:
- ALLOW — the statute permits the requested act on the known facts.
- DENY — the statute forbids the requested act on the known facts.
- NEED_MORE_INFO — at least one catalog claim is still unknown and is required to decide.

If the outcome is NEED_MORE_INFO, list missing_facts as claim ids from the catalog that are not already known. List only ids that appear under UNKNOWN CLAIM IDS. If the outcome is ALLOW or DENY, missing_facts must be an empty list.

Give a short reason.
"""


def known_facts_for_scenario(
    scenario: SuiteScenario,
    use_case: UseCaseDefinition,
    mock_db: MockDbArtifact,
) -> dict[str, bool]:
    """Build known true/false facts the same way the suite seeds the runtime.

    Non-null ``intent_assignments`` win. Remaining catalog claims take
    non-null values from the mock DB after ``mock_db_overrides`` (unavailable
    sources contribute nothing; conflicting available sources stay unknown).
    """
    catalog = {claim.claim_id for claim in use_case.claims}
    known: dict[str, bool] = {}
    for claim_id, value in scenario.intent_assignments.items():
        if value is None or claim_id not in catalog:
            continue
        known[claim_id] = bool(value)

    overridden = _apply_db_overrides(mock_db, scenario.mock_db_overrides)
    db_values: dict[str, bool | None] = {}
    for source in overridden.sources:
        if source.availability == "unavailable":
            continue
        for claim_id, value in source.values.items():
            if claim_id not in catalog:
                continue
            if claim_id not in db_values:
                db_values[claim_id] = value
            elif db_values[claim_id] != value:
                db_values[claim_id] = None
    for claim_id, value in db_values.items():
        if value is not None and claim_id not in known:
            known[claim_id] = bool(value)
    return known


def unknown_claim_ids_for_scenario(
    use_case: UseCaseDefinition,
    known_facts: dict[str, bool],
) -> list[str]:
    """Return catalog claim ids that do not yet have a true/false value."""
    return [claim.claim_id for claim in use_case.claims if claim.claim_id not in known_facts]


def load_scenario_context(scenario_path: str | Path) -> ScenarioContext:
    """Load a suite scenario plus law, request, mock DB, and known/unknown facts."""
    path = Path(scenario_path).resolve()
    scenario = load_suite_scenario(path)
    case_dir = path.parents[1]
    use_case = load_use_case_from_dir(case_dir)
    law_text = resolve_example_path(case_dir, scenario.law_file).read_text(encoding="utf-8")
    request_path = resolve_example_path(case_dir, scenario.request_file)
    request_text = request_path.read_text(encoding="utf-8") if request_path.exists() else ""
    base_db = load_mock_db(resolve_example_path(case_dir, scenario.mock_db_file))
    known = known_facts_for_scenario(scenario, use_case, base_db)
    unknown = unknown_claim_ids_for_scenario(use_case, known)
    catalog = claim_catalog_text(use_case, use_case.default_logic_level)
    return ScenarioContext(
        path=path,
        scenario=scenario,
        use_case=use_case,
        case_dir=case_dir,
        law_text=law_text,
        request_text=request_text,
        mock_db=_apply_db_overrides(base_db, scenario.mock_db_overrides),
        known_facts=known,
        unknown_claim_ids=unknown,
        catalog_text=catalog,
    )


def build_case_bundle(ctx: ScenarioContext) -> CaseBundle:
    """Build the same CaseBundle the suite solver path uses (deterministic fixtures)."""
    from logic_levels import build_domain_artifact, build_intent_artifact
    from metadata import utc_timestamp

    run_meta = ExtractionRunMetadata(
        generated_at_utc=utc_timestamp(),
        model_name="deterministic-fixture",
    )
    domain = build_domain_artifact(
        ctx.use_case,
        ctx.use_case.default_logic_level,
        ctx.law_text,
        run_metadata=run_meta,
    )
    intent = build_intent_artifact(
        ctx.use_case,
        ctx.request_text,
        ctx.use_case.default_logic_level,
        ctx.scenario.intent_assignments,
        run_metadata=run_meta,
    )
    return CaseBundle(
        logic_level=ctx.use_case.default_logic_level,
        domain=domain,
        intent=intent,
        mock_db=ctx.mock_db,
    )


def get_complete_fn(provider_name: str | None = None) -> ProviderComplete:
    """Return a structured-complete callable.

    Prefers ``providers.get_provider`` when WS-B has landed; otherwise wraps
    ``llm.gemini_structured_completion``. Callers that already have a fake or
    live complete function should pass it through instead of calling this.
    """
    if provider_name:
        try:
            from providers import get_provider
        except ImportError:
            get_provider = None
        if get_provider is not None:
            return get_provider(provider_name).complete
    from llm import gemini_structured_completion

    return gemini_structured_completion


def _unwrap_decision(result: Any, response_model: type[BaselineDecision]) -> BaselineDecision:
    """Accept a BaselineDecision, a provider result with ``.parsed``, or a dict."""
    if isinstance(result, response_model):
        return result
    parsed = getattr(result, "parsed", None)
    if parsed is not None:
        if getattr(result, "skipped", False):
            reason = getattr(result, "skip_reason", "") or "provider skipped"
            raise RuntimeError(reason)
        if isinstance(parsed, response_model):
            return parsed
        return response_model.model_validate(parsed)
    if isinstance(result, dict):
        return response_model.model_validate(result)
    raise TypeError(f"complete() returned unsupported type {type(result)!r}")


def _call_complete(
    complete_fn: ProviderComplete,
    *,
    system: str,
    user: str,
    response_model: type[BaselineDecision],
) -> BaselineDecision:
    """Invoke either the WS-B provider signature or ``gemini_structured_completion``."""
    try:
        result = complete_fn(
            system=system,
            user=user,
            response_model=response_model,
            temperature=0.0,
        )
    except TypeError:
        result = complete_fn(
            system_instruction=system,
            user_content=user,
            response_model=response_model,
            temperature=0.0,
        )
    return _unwrap_decision(result, response_model)


def _format_known_facts(known_facts: dict[str, bool]) -> str:
    if not known_facts:
        return "(none)"
    lines = [f"- {claim_id}: {'true' if value else 'false'}" for claim_id, value in known_facts.items()]
    return "\n".join(lines)


def _format_unknown_ids(unknown_claim_ids: list[str]) -> str:
    if not unknown_claim_ids:
        return "(none)"
    return "\n".join(f"- {claim_id}" for claim_id in unknown_claim_ids)


def build_user_prompt(
    *,
    law_text: str,
    request_text: str,
    known_facts: dict[str, bool],
    unknown_claim_ids: list[str],
    claim_catalog_text: str,
) -> str:
    """Render the user prompt for the LLM-only decision call."""
    return (
        "STATUTE:\n"
        f"{law_text.strip()}\n\n"
        "CASE REQUEST:\n"
        f"{request_text.strip() or '(no request text)'}\n\n"
        "KNOWN FACTS (claim_id = true/false):\n"
        f"{_format_known_facts(known_facts)}\n\n"
        "UNKNOWN CLAIM IDS (in the catalog; value not given):\n"
        f"{_format_unknown_ids(unknown_claim_ids)}\n\n"
        "CLAIM CATALOG (labels only; not the gold decision rules):\n"
        f"{claim_catalog_text.strip()}\n"
    )


def _filter_missing_facts(raw: list[str], unknown_claim_ids: list[str]) -> list[str]:
    allowed = set(unknown_claim_ids)
    seen: set[str] = set()
    filtered: list[str] = []
    for fact_id in raw:
        if fact_id in allowed and fact_id not in seen:
            seen.add(fact_id)
            filtered.append(fact_id)
    return filtered


def decide_llm_only(
    *,
    law_text: str,
    request_text: str,
    known_facts: dict[str, bool],
    unknown_claim_ids: list[str],
    claim_catalog_text: str,
    provider_complete: ProviderComplete,
) -> BaselineDecision:
    """Ask the model for ALLOW/DENY/NEED_MORE_INFO plus catalog missing-fact ids."""
    user_prompt = build_user_prompt(
        law_text=law_text,
        request_text=request_text,
        known_facts=known_facts,
        unknown_claim_ids=unknown_claim_ids,
        claim_catalog_text=claim_catalog_text,
    )
    decision = _call_complete(
        provider_complete,
        system=_SYSTEM_PROMPT,
        user=user_prompt,
        response_model=BaselineDecision,
    )
    decision.missing_facts = _filter_missing_facts(decision.missing_facts, unknown_claim_ids)
    return decision
