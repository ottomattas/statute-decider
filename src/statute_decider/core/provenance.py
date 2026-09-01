"""Provenance recorded on every produced node value."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class Provenance(BaseModel):
    """Who/what produced a node value, and with which parameters.

    Every method has an executor (provider + model) and a consumed artifact:
    llm -> provider/model + prompt; solver -> backend + encoding; oracle ->
    human/operator + authoring notes; deterministic code -> code/commit +
    mapping/template/fixture path.
    """

    node: str
    method: str  # oracle | llm | solver | lookup | match | render | file | skip
    strategy: str | None = None
    provider: str | None = None  # anthropic | openai | google | deepseek | human | code | z3 ...
    model: str | None = None  # model id | "operator" | repo commit | backend version
    prompt_id: str | None = None
    prompt_hash: str | None = None
    consumed_artifact: str | None = None  # mapping file, template, fixture path, ...
    timestamp: str = Field(default_factory=utc_now)
    notes: str = ""


def oracle_provenance(node: str, notes: str = "") -> Provenance:
    return Provenance(node=node, method="oracle", provider="human", model="operator", notes=notes)
