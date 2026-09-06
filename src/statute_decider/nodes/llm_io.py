"""Structured-output schemas shared by the LLM node executors.

Boolean-with-unknown is encoded as the enum {"true","false","unknown"} because
every provider's strict JSON-schema mode accepts string enums.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GroundItem(BaseModel):
    term_id: str
    value: Literal["true", "false", "unknown"] = "unknown"
    span: str = ""


class GroundResponse(BaseModel):
    """Terms recognized in an utterance, with asserted values where grounded."""

    items: list[GroundItem] = Field(default_factory=list)


class ValueItem(BaseModel):
    term_id: str
    value: Literal["true", "false", "unknown"] = "unknown"
    span: str = ""


class ValueResponse(BaseModel):
    """Asserted values for an already-recognized term list."""

    items: list[ValueItem] = Field(default_factory=list)


class DecideResponse(BaseModel):
    """Decision of an LLM decide call — one structured call per scenario (Ruling J).

    Field order is the schema order the model fills: ``steps`` come *before*
    ``outcome`` so the model reasons before it decides; ``justification`` is
    the inline justification stored on the row as an ``llm_inline`` entry.

    This docstring is developer text: ``strict_json_schema`` drops the schema
    ``description`` it would otherwise become. Until 6 Sep 2026 it reached the
    providers inside the JSON schema, and Claude Fable 5.1's safety classifier
    read "reasons before it decides" as a reasoning-extraction request and
    refused 57/60 llm-only calls; the prompt wording itself passes.
    """

    steps: list[str] = Field(default_factory=list)
    outcome: Literal["ALLOW", "DENY", "NEED_MORE_INFO"]
    missing_terms: list[str] = Field(default_factory=list)
    justification: str = ""


class JustifyResponse(BaseModel):
    """The optional post-hoc ``justify`` node: appended as an ``llm_post`` entry."""

    steps: list[str] = Field(default_factory=list)
    justification: str = ""


def tri_to_bool(value: str) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None
