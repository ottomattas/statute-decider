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
    """Decision of the llm-only condition: three-way outcome + missing items."""

    outcome: Literal["ALLOW", "DENY", "NEED_MORE_INFO"]
    missing_terms: list[str] = Field(default_factory=list)
    reason: str = ""


class JustifyResponse(BaseModel):
    steps: list[str] = Field(default_factory=list)
    justification: str = ""


def tri_to_bool(value: str) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None
