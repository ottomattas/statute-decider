"""Config-plane models: statutes, registers, cases, scenarios (YAML), plus the
data-plane registry state (JSON) that mocks what a register interface returns.

Design rule: sources are vocabulary-free. Registry records hold raw fields;
translating fields into terms is ``record_term``'s job. Each register carries
its warrant — the trust axis is source data, not run configuration.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from statute_decider.core.enums import Availability, Warrant


class StatuteSidecar(BaseModel):
    """YAML sidecar next to ``statute.txt``."""

    statute_id: str
    kind: str = "statute_text"  # future: regulation_text, caselaw_text, ...
    title: str = ""
    act_references: list[str] = Field(default_factory=list)
    jurisdiction: str = "EE"
    language: str = "en"
    version_date: str = ""
    # Official translation the text was taken from (Riigi Teataja English
    # translations, https://www.riigiteataja.ee/en/). Empty for original-language texts.
    translation_id: str = ""  # Riigi Teataja translation id, e.g. "505012026005"
    translation_url: str = ""
    translation_in_force_from: str = ""  # header "In force from" (dd.mm.yyyy)
    translation_in_force_until: str = ""  # header "In force until" ("In force" = open-ended)
    translation_published: str = ""  # header "Translation published"
    provisions: str = ""  # which §§ / subsections / clauses the slice reproduces
    notes: str = ""


class RegisterSchema(BaseModel):
    """YAML schema of one register: raw fields and default warrant."""

    register_id: str
    label: str = ""
    description: str = ""
    fields: list[str] = Field(default_factory=list)
    default_warrant: Warrant = Warrant.AUTHORITATIVE
    notes: str = ""


class RegisterRecord(BaseModel):
    record_id: str
    fields: dict[str, bool | None] = Field(default_factory=dict)


class RegisterState(BaseModel):
    """One register's mock state for a case (raw fields + warrant + availability)."""

    register_id: str
    label: str = ""
    warrant: Warrant = Warrant.AUTHORITATIVE
    availability: Availability = Availability.REGISTER_AVAILABLE
    records: list[RegisterRecord] = Field(default_factory=list)


class RegistryState(BaseModel):
    """Output of ``registry_record``: what the registers return for a scenario."""

    node: Literal["registry_record"] = "registry_record"
    registers: list[RegisterState] = Field(default_factory=list)

    def by_id(self) -> dict[str, RegisterState]:
        return {reg.register_id: reg for reg in self.registers}


class RegisterOverride(BaseModel):
    """Scenario-level diff against the case's base registry state.

    A register unknown to the base state is *created* (e.g. a trust-only
    self-report register that exists only in one scenario); ``exclude`` drops
    a base register entirely for this scenario.
    """

    model_config = {"extra": "forbid"}

    exclude: bool = False
    availability: Availability | None = None
    warrant: Warrant | None = None
    label: str = ""
    set: dict[str, dict[str, bool | None]] = Field(default_factory=dict)  # record -> field -> value
    remove: dict[str, list[str]] = Field(default_factory=dict)  # record -> fields to drop


class Scenario(BaseModel):
    """Hand-authored YAML binding sources to expectations for one scenario.

    Expected node values live as oracle JSON under
    ``data/cases/<case>/oracle/<node>/<scenario>.json`` in the same schemas as
    produced values.
    """

    scenario_id: str
    case_id: str
    label: str = ""  # human display name (<= 60 chars, English); not an id
    mechanism: str = ""  # cross-case mechanism vocabulary, see docs/reference/id-aliases.md
    description: str = ""
    utterance_file: str = ""  # relative to case sources/utterances/
    register_overrides: dict[str, RegisterOverride] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    gold_confidence: str = ""
    notes: str = ""
    provenance: str = ""


class Case(BaseModel):
    """Thin assembly: a case names its shared statute(s) and register(s)."""

    case_id: str
    title: str = ""
    description: str = ""
    statute_ids: list[str] = Field(default_factory=list)
    register_ids: list[str] = Field(default_factory=list)
    notes: str = ""


def apply_register_overrides(
    base: RegistryState, overrides: dict[str, RegisterOverride]
) -> RegistryState:
    """Return the scenario's registry state: the case base plus the scenario diff."""
    state = base.model_copy(deep=True)
    by_id = {reg.register_id: reg for reg in state.registers}
    for register_id, override in overrides.items():
        if override.exclude:
            state.registers = [r for r in state.registers if r.register_id != register_id]
            by_id.pop(register_id, None)
            continue
        reg = by_id.get(register_id)
        if reg is None:
            reg = RegisterState(register_id=register_id, label=override.label)
            state.registers.append(reg)
            by_id[register_id] = reg
        if override.availability is not None:
            reg.availability = override.availability
        if override.warrant is not None:
            reg.warrant = override.warrant
        records = {rec.record_id: rec for rec in reg.records}
        for record_id, fields in override.set.items():
            rec = records.get(record_id)
            if rec is None:
                rec = RegisterRecord(record_id=record_id)
                reg.records.append(rec)
                records[record_id] = rec
            rec.fields.update(fields)
        for record_id, drop in override.remove.items():
            rec = records.get(record_id)
            if rec is None:
                continue
            for field in drop:
                rec.fields.pop(field, None)
    return state
