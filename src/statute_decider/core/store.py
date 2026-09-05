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
    StatuteSpec,
    StatuteText,
    apply_register_overrides,
)
from statute_decider.core.outcome import PremiseOutcome
from statute_decider.core.premises import ClaimSet, FactSet, RuleSet
from statute_decider.core.provenance import Provenance
from statute_decider.core.terms import RecordTermMap, TermCatalog, UtteranceTerms
from statute_decider.core.trace import OutcomeTrace
from statute_decider.legislation.catalogue import CatalogueEntry
from statute_decider.legislation.corpus import Corpus
from statute_decider.legislation.riigiteataja import Act

RENDERED_FILE = "statute.rendered.txt"

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
        self.corpus = Corpus(self.root / "sources" / "legislation")
        self._specs: dict[str, StatuteSpec] = {}

    # --- statutes (statute-determined, stored once) ---

    def statute_ids(self) -> list[str]:
        return sorted(p.name for p in self.statutes_dir.iterdir() if p.is_dir())

    def statute_spec(self, statute_id: str) -> StatuteSpec:
        if statute_id not in self._specs:
            self._specs[statute_id] = StatuteSpec.model_validate(
                _read_yaml(self.statutes_dir / statute_id / "statute.yaml")
            )
        return self._specs[statute_id]

    def statute_entry(self, statute_id: str) -> CatalogueEntry:
        """The catalogue entry a statute reads: its ``source.global_id``, or the
        counterpart in ``source.language`` when that override is set."""
        spec = self.statute_spec(statute_id)
        entry = self.corpus.entry(spec.source.global_id)
        if spec.source.language and spec.source.language != entry.language:
            matches = [
                self.corpus.entry(gid)
                for gid in entry.counterparts
                if self.corpus.entry(gid).language == spec.source.language
            ]
            if not matches:
                raise KeyError(
                    f"statute {statute_id}: {entry.global_id} has no {spec.source.language} counterpart"
                )
            entry = matches[0]
        return entry

    def statute_act(self, statute_id: str) -> Act:
        return self.corpus.load(self.statute_entry(statute_id).global_id)

    def statute_text(self, statute_id: str, method: str = "full_act") -> StatuteText:
        """Render the statute from the corpus: the whole act (``full_act``, what
        prompts receive) or only the declared provisions (``slice``, the ablation)."""
        spec = self.statute_spec(statute_id)
        entry = self.statute_entry(statute_id)
        act = self.corpus.load(entry.global_id)
        if method == "full_act":
            text = act.render_full()
        elif method == "slice":
            text = act.render_slice(spec.provisions)
        else:
            raise ValueError(f"statute_text method {method!r} is not 'full_act' or 'slice'")
        return StatuteText(
            statute_id=statute_id,
            act_slug=entry.act_slug,
            global_id=entry.global_id,
            sha256=entry.sha256,
            language=entry.language,
            method=method,  # type: ignore[arg-type]
            provisions=list(spec.provisions),
            chars=len(text),
            text=text,
            provenance=Provenance(
                node="statute_text",
                method="file" if method == "full_act" else "slice",
                provider="code",
                consumed_artifact=f"{entry.file}#{entry.sha256[:12]}",
            ),
        )

    def statute_rendered_path(self, statute_id: str) -> Path:
        return self.statutes_dir / statute_id / RENDERED_FILE

    def render_declared_provisions(self, statute_id: str) -> str:
        """The committed, read-only ``statute.rendered.txt``: declared provisions, source language."""
        return self.statute_act(statute_id).render_slice(self.statute_spec(statute_id).provisions)

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
