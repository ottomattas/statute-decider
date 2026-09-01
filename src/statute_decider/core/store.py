"""Filesystem access to ``data/``: store once, at the scope that determines it.

Statute-determined values live in ``data/statutes/<statute_id>/``,
register-determined in ``data/registers/<register_id>/``, scenario-determined
in ``data/cases/<case_id>/``. Everything else references by id.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from statute_decider.core.casefiles import (
    Case,
    RegisterSchema,
    RegistryState,
    Scenario,
    StatuteSidecar,
    apply_register_overrides,
)
from statute_decider.core.outcome import PremiseOutcome
from statute_decider.core.premises import ClaimSet, FactSet, RuleSet
from statute_decider.core.terms import RecordTermMap, TermCatalog, UtteranceTerms
from statute_decider.core.trace import OutcomeTrace

ORACLE_NODE_MODELS = {
    "utterance_term": UtteranceTerms,
    "term_claim": ClaimSet,
    "term_fact": FactSet,
    "premise_outcome": PremiseOutcome,
    "outcome_trace": OutcomeTrace,
}


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class DataStore:
    """Read-side accessors over the ``data/`` tree."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.statutes_dir = self.root / "statutes"
        self.registers_dir = self.root / "registers"
        self.cases_dir = self.root / "cases"

    # --- statutes (statute-determined, stored once) ---

    def statute_ids(self) -> list[str]:
        return sorted(p.name for p in self.statutes_dir.iterdir() if p.is_dir())

    def statute_text(self, statute_id: str) -> str:
        return (self.statutes_dir / statute_id / "statute.txt").read_text(encoding="utf-8")

    def statute_sidecar(self, statute_id: str) -> StatuteSidecar:
        return StatuteSidecar.model_validate(
            _read_yaml(self.statutes_dir / statute_id / "statute.yaml")
        )

    def oracle_text_term(self, statute_id: str) -> TermCatalog:
        return TermCatalog.model_validate(
            _read_json(self.statutes_dir / statute_id / "oracle" / "text_term.json")
        )

    def oracle_term_rule(self, statute_id: str) -> RuleSet:
        return RuleSet.model_validate(
            _read_json(self.statutes_dir / statute_id / "oracle" / "term_rule.json")
        )

    # --- registers (register-determined, stored once) ---

    def register_ids(self) -> list[str]:
        return sorted(p.name for p in self.registers_dir.iterdir() if p.is_dir())

    def register_schema(self, register_id: str) -> RegisterSchema:
        return RegisterSchema.model_validate(
            _read_yaml(self.registers_dir / register_id / "schema.yaml")
        )

    def oracle_record_term(self, register_id: str) -> RecordTermMap:
        return RecordTermMap.model_validate(
            _read_json(self.registers_dir / register_id / "oracle" / "record_term.json")
        )

    # --- cases (scenario-determined only; thin assembly) ---

    def case_ids(self) -> list[str]:
        return sorted(p.name for p in self.cases_dir.iterdir() if p.is_dir())

    def case(self, case_id: str) -> Case:
        return Case.model_validate(_read_yaml(self.cases_dir / case_id / "case.yaml"))

    def scenario_ids(self, case_id: str) -> list[str]:
        scen_dir = self.cases_dir / case_id / "scenarios"
        return sorted(p.stem for p in scen_dir.glob("*.yaml"))

    def scenario(self, case_id: str, scenario_id: str) -> Scenario:
        return Scenario.model_validate(
            _read_yaml(self.cases_dir / case_id / "scenarios" / f"{scenario_id}.yaml")
        )

    def utterance_text(self, case_id: str, scenario: Scenario) -> str:
        name = scenario.utterance_file or f"{scenario.scenario_id}.txt"
        path = self.cases_dir / case_id / "sources" / "utterances" / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def base_registry(self, case_id: str) -> RegistryState:
        path = self.cases_dir / case_id / "sources" / "registry.json"
        if not path.exists():
            return RegistryState()
        return RegistryState.model_validate(_read_json(path))

    def scenario_registry(self, case_id: str, scenario: Scenario) -> RegistryState:
        return apply_register_overrides(self.base_registry(case_id), scenario.register_overrides)

    # --- oracle node values (scenario-determined) ---

    def oracle_path(self, case_id: str, node: str, scenario_id: str) -> Path:
        return self.cases_dir / case_id / "oracle" / node / f"{scenario_id}.json"

    def oracle_value(self, case_id: str, node: str, scenario_id: str):
        model = ORACLE_NODE_MODELS[node]
        path = self.oracle_path(case_id, node, scenario_id)
        if not path.exists():
            return None
        return model.model_validate(_read_json(path))

    # --- iteration ---

    def all_scenarios(self, case_ids: list[str] | None = None) -> list[tuple[str, str]]:
        """(case_id, scenario_id) pairs, sorted."""
        pairs: list[tuple[str, str]] = []
        for case_id in case_ids or self.case_ids():
            for scenario_id in self.scenario_ids(case_id):
                pairs.append((case_id, scenario_id))
        return pairs
