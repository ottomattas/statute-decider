"""One-off authoring aid: re-author the validated v1 content in v2 shapes.

The v1 files (framework/examples/, tag ``pre-refactor``) are content reference
only — which statutes, which cases, which expected outcomes. This script reads
that content and writes fresh v2 data at its determining scope:

- data/statutes/<statute_id>/   statute.txt + statute.yaml + oracle text_term/term_rule
- data/registers/<register_id>/ schema.yaml + oracle record_term (field-to-term mapping)
- data/cases/<case_id>/         case.yaml, sources, scenarios, per-scenario oracle values

Every emitted file validates against the v2 core schemas. Run once from the
repo root, then hand-review; the script is kept for provenance.

Known authoring compromise (documented in README): v1 mock DBs keyed values by
claim id, so v2 register fields reuse those names and the record_term mapping
is an identity mapping. Field naming that genuinely diverges from the
vocabulary (with non-trivial transforms) is future authoring work; it does not
affect the committed runs, which bind record_term=oracle + term_fact=lookup.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "framework" / "examples"
DATA = ROOT / "data"

sys.path.insert(0, str(ROOT / "src"))

from statute_decider.core import (
    Availability,
    Case,
    ClaimPremise,
    ClaimSet,
    ClauseAnchor,
    DataStore,
    Evidence,
    MissingReason,
    MissingTerm,
    OutcomeDef,
    OutcomeState,
    PremiseOutcome,
    Provenance,
    RecordTermMap,
    RegisterRecord,
    RegisterState,
    RegistryState,
    RuleKind,
    RulePremise,
    RuleSet,
    Term,
    TermCatalog,
    TermRef,
    UtteranceTerms,
    Warrant,
    to_scored,
)
from statute_decider.core.terms import FieldToTerm
from statute_decider.nodes import lookup_facts

AUTHOR_NOTE = "Re-authored 2026-09-01 from v1 validated content (tag pre-refactor)."


def oracle_prov(node: str) -> Provenance:
    return Provenance(node=node, method="oracle", provider="human", model="operator", notes=AUTHOR_NOTE)


def write_json(path: Path, model) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(model.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


STATE_MAP = {
    "ALLOW": OutcomeState.ALLOW,
    "DENY": OutcomeState.DENY,
    "NEED_DB_INFO": OutcomeState.NEED_REGISTER_INFO,
    "NEED_USER_INFO": OutcomeState.NEED_USER_INFO,
    "UNVERIFIABLE_CLAIM": OutcomeState.UNVERIFIABLE_CLAIM,
}


def register_key(case_id: str, source_id: str) -> str:
    return f"{case_id}__{source_id}"


def is_special(source: dict) -> bool:
    return bool(source.get("trust_only")) or source.get("availability", "available") == "unavailable"


def resolve_registers(case_id: str, db: dict, overrides: dict) -> list[RegisterState]:
    """Mirror v1 semantics: overrides touch ordinary sources only; None removes."""
    special_keys: set[str] = set()
    for source in db["sources"]:
        if is_special(source):
            special_keys.update(source["values"].keys())
    states: list[RegisterState] = []
    for source in db["sources"]:
        values = dict(source["values"])
        if not is_special(source):
            for claim_id, value in overrides.items():
                if claim_id in special_keys:
                    continue
                if claim_id in values or value is not None:
                    if value is None:
                        values.pop(claim_id, None)
                    elif claim_id in values:
                        values[claim_id] = value
        states.append(
            RegisterState(
                register_id=register_key(case_id, source["source_id"]),
                label=source.get("label", ""),
                warrant=Warrant.TRUST_ONLY if source.get("trust_only") else Warrant.AUTHORITATIVE,
                availability=Availability(source.get("availability", "available")),
                records=[RegisterRecord(record_id="main", fields=values)],
            )
        )
    # Overrides that add a claim no ordinary source declares: attach to the
    # register whose union schema declares it (resolved by the caller).
    leftover = {
        claim_id: value
        for claim_id, value in overrides.items()
        if value is not None
        and claim_id not in special_keys
        and not any(claim_id in st.records[0].fields for st in states)
    }
    if leftover:
        raise ValueError(f"{case_id}: overrides add undeclared fields {sorted(leftover)}")
    return states


def diff_overrides(base: RegistryState, resolved: list[RegisterState]) -> dict:
    """Scenario override block = diff from the case base registry state."""
    out: dict = {}
    base_by_id = base.by_id()
    resolved_by_id = {st.register_id: st for st in resolved}
    for register_id, state in resolved_by_id.items():
        entry: dict = {}
        base_state = base_by_id.get(register_id)
        if base_state is None:
            entry["warrant"] = state.warrant.value
            entry["availability"] = state.availability.value
            entry["set"] = {"main": dict(state.records[0].fields)}
            out[register_id] = entry
            continue
        if state.availability != base_state.availability:
            entry["availability"] = state.availability.value
        if state.warrant != base_state.warrant:
            entry["warrant"] = state.warrant.value
        base_fields = base_state.records[0].fields if base_state.records else {}
        fields = state.records[0].fields if state.records else {}
        changed = {k: v for k, v in fields.items() if base_fields.get(k, "__absent__") != v}
        dropped = [k for k in base_fields if k not in fields]
        if changed:
            entry["set"] = {"main": changed}
        if dropped:
            entry["remove"] = {"main": dropped}
        if entry:
            out[register_id] = entry
    for register_id in base_by_id:
        if register_id not in resolved_by_id:
            out[register_id] = {"exclude": True}
    return out


def main() -> None:
    case_dirs = sorted(p for p in V1.iterdir() if (p / "use_case.json").exists())
    total_scenarios = 0
    for case_dir in case_dirs:
        case_id = case_dir.name
        use_case = json.loads((case_dir / "use_case.json").read_text(encoding="utf-8"))
        statute_id = case_id

        # --- statute (stored once) ---
        statute_dir = DATA / "statutes" / statute_id
        statute_dir.mkdir(parents=True, exist_ok=True)
        law_text = (case_dir / "law.txt").read_text(encoding="utf-8")
        (statute_dir / "statute.txt").write_text(law_text, encoding="utf-8")
        write_yaml(
            statute_dir / "statute.yaml",
            {
                "statute_id": statute_id,
                "kind": "statute_text",
                "title": use_case.get("title", ""),
                "jurisdiction": "EE",
                "language": "et",
                "notes": AUTHOR_NOTE,
            },
        )

        terms = []
        for claim in use_case["claims"]:
            anchors = [
                ClauseAnchor(
                    clause_id=ref.get("clause_id", ""),
                    clause_title=ref.get("clause_title", ""),
                    quote=ref.get("clause_text", ""),
                    note=ref.get("note", ""),
                )
                for ref in claim.get("law_references", [])
            ]
            terms.append(
                Term(
                    term_id=claim["claim_id"],
                    label=claim.get("label", ""),
                    definition=claim.get("description", ""),
                    evidence=Evidence.REGISTER if claim["source_type"] == "db" else Evidence.USER,
                    propositional=claim.get("propositional") or claim.get("lowered_atom", ""),
                    predicate=claim.get("predicate"),
                    higher_order=claim.get("higher_order"),
                    anchors=anchors,
                )
            )
        catalog = TermCatalog(statute_id=statute_id, terms=terms, provenance=oracle_prov("text_term"))
        write_json(statute_dir / "oracle" / "text_term.json", catalog)

        allow_id = deny_id = None
        outcome_defs = []
        for outcome in use_case["outcomes"]:
            outcome_defs.append(
                OutcomeDef(outcome_id=outcome["outcome_id"], label=outcome.get("label", ""))
            )
            role = outcome.get("administrative_role")
            if role == "allow":
                allow_id = outcome["outcome_id"]
            elif role == "deny":
                deny_id = outcome["outcome_id"]
        rules = []
        for rule in use_case["rules"]:
            refs = [
                ClauseAnchor(
                    clause_id=ref.get("clause_id", ""),
                    clause_title=ref.get("clause_title", ""),
                    quote=ref.get("clause_text", ""),
                    note=ref.get("note", ""),
                )
                for ref in rule.get("law_references", [])
            ]
            rules.append(
                RulePremise(
                    premise_id=rule["rule_id"],
                    rule_kind=RuleKind(rule["kind"]),
                    label=rule.get("label", ""),
                    when_term_ids=list(rule["when_claim_ids"]),
                    target_outcome_id=rule.get("target_outcome_id"),
                    target_term_id=rule.get("target_claim_id"),
                    law_references=refs,
                    notes=rule.get("formal_text", ""),
                )
            )
        ruleset = RuleSet(
            statute_id=statute_id,
            allow_outcome_id=allow_id,
            deny_outcome_id=deny_id,
            outcomes=outcome_defs,
            rules=rules,
            provenance=oracle_prov("term_rule"),
        )
        write_json(statute_dir / "oracle" / "term_rule.json", ruleset)
        term_ids = {t.term_id for t in terms}

        # --- registers (union across all db files of the case) ---
        db_files = sorted(case_dir.glob("mock_db*.json"))
        register_sources: dict[str, dict] = {}
        register_fields: dict[str, set[str]] = {}
        register_trust: dict[str, bool] = {}
        for db_file in db_files:
            db = json.loads(db_file.read_text(encoding="utf-8"))
            for source in db["sources"]:
                rid = register_key(case_id, source["source_id"])
                register_sources.setdefault(rid, source)
                register_fields.setdefault(rid, set()).update(source["values"].keys())
                register_trust[rid] = register_trust.get(rid, False) or bool(
                    source.get("trust_only")
                )
        mappings: list[RecordTermMap] = []
        for rid, source in register_sources.items():
            fields = sorted(register_fields[rid])
            write_yaml(
                DATA / "registers" / rid / "schema.yaml",
                {
                    "register_id": rid,
                    "label": source.get("label", ""),
                    "description": source.get("description", ""),
                    "fields": fields,
                    "default_warrant": "trust_only" if register_trust[rid] else "authoritative",
                    "notes": AUTHOR_NOTE
                    + " Field names mirror the vocabulary (v1 mock DBs were keyed by claim id);"
                    " the mapping is identity until richer field naming is authored.",
                },
            )
            mapping = RecordTermMap(
                register_id=rid,
                mappings=[
                    FieldToTerm(term_id=f, register_id=rid, field=f, transform="identity")
                    for f in fields
                    if f in term_ids
                ],
                provenance=oracle_prov("record_term"),
            )
            write_json(DATA / "registers" / rid / "oracle" / "record_term.json", mapping)
            mappings.append(mapping)
        mapping_by_id = {m.register_id: m for m in mappings}

        # --- case assembly ---
        case_root = DATA / "cases" / case_id
        base_db = json.loads((case_dir / "mock_db.json").read_text(encoding="utf-8"))
        base_registry = RegistryState(registers=resolve_registers(case_id, base_db, {}))
        # register order: base db order first, then variant-only registers.
        base_ids = [st.register_id for st in base_registry.registers]
        extra_ids = [rid for rid in register_sources if rid not in base_ids]
        case = Case(
            case_id=case_id,
            title=use_case.get("title", ""),
            description=use_case.get("description", ""),
            statute_ids=[statute_id],
            register_ids=base_ids + sorted(extra_ids),
            notes=AUTHOR_NOTE,
        )
        write_yaml(case_root / "case.yaml", case.model_dump(mode="json"))
        write_json(case_root / "sources" / "registry.json", base_registry)

        # utterances: one file per distinct request file.
        for request_file in sorted(
            {
                json.loads(p.read_text(encoding="utf-8")).get("request_file", "")
                for p in (case_dir / "scenarios").glob("*.json")
            }
        ):
            if not request_file:
                continue
            src = (case_dir / request_file).resolve()
            text = src.read_text(encoding="utf-8") if src.exists() else ""
            dest = case_root / "sources" / "utterances" / Path(request_file).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")

        # --- scenarios + oracle node values ---
        for scenario_path in sorted((case_dir / "scenarios").glob("*.json")):
            total_scenarios += 1
            raw = json.loads(scenario_path.read_text(encoding="utf-8"))
            scenario_id = scenario_path.stem
            db = json.loads((case_dir / raw["mock_db_file"]).read_text(encoding="utf-8"))
            resolved = resolve_registers(case_id, db, raw.get("mock_db_overrides") or {})
            overrides = diff_overrides(base_registry, resolved)

            notes = raw.get("gold_notes", "")
            if raw.get("law_file", "law.txt") != "law.txt":
                notes = (
                    notes
                    + " v1 used an unrelated law file for an extraction probe; v2 binds the"
                    " canonical statute text."
                ).strip()
            write_yaml(
                case_root / "scenarios" / f"{scenario_id}.yaml",
                {
                    "scenario_id": scenario_id,
                    "case_id": case_id,
                    "description": raw.get("description", ""),
                    "utterance_file": Path(raw["request_file"]).name,
                    "register_overrides": overrides,
                    "tags": raw.get("tags", []),
                    "gold_confidence": raw.get("gold_confidence", ""),
                    "notes": notes,
                    "provenance": (raw.get("provenance", "") + " | " + AUTHOR_NOTE).strip(" |"),
                },
            )

            assignments = {
                k: v for k, v in (raw.get("intent_assignments") or {}).items() if k in term_ids
            }
            write_json(
                case_root / "oracle" / "utterance_term" / f"{scenario_id}.json",
                UtteranceTerms(
                    scenario_id=scenario_id,
                    term_refs=[TermRef(term_id=k) for k in sorted(assignments)],
                    provenance=oracle_prov("utterance_term"),
                ),
            )
            write_json(
                case_root / "oracle" / "term_claim" / f"{scenario_id}.json",
                ClaimSet(
                    scenario_id=scenario_id,
                    claims=[
                        ClaimPremise(premise_id=f"claim_{k}", term_id=k, value=bool(v))
                        for k, v in sorted(assignments.items())
                        if v is not None
                    ],
                    provenance=oracle_prov("term_claim"),
                ),
            )

            scenario_mappings = [
                mapping_by_id[st.register_id]
                for st in resolved
                if st.register_id in mapping_by_id
            ]
            facts = lookup_facts(scenario_id, RegistryState(registers=resolved), scenario_mappings)
            facts.provenance = oracle_prov("term_fact")
            write_json(case_root / "oracle" / "term_fact" / f"{scenario_id}.json", facts)

            state = STATE_MAP[raw["expected_outcome"]]
            trust_terms = {f.term_id for f in facts.facts if f.warrant == Warrant.TRUST_ONLY}
            unavailable = set(facts.unavailable_terms)
            missing = []
            for term_id in raw.get("expected_missing_facts") or []:
                if term_id not in term_ids:
                    continue
                if term_id in unavailable:
                    reason = MissingReason.NO_REGISTER
                elif term_id in trust_terms:
                    reason = MissingReason.UNWARRANTED_ONLY
                elif term_id in set(facts.conflicts):
                    reason = MissingReason.CONFLICT
                else:
                    reason = MissingReason.NO_VALUE
                missing.append(MissingTerm(term_id=term_id, reason=reason))
            note_bits = [f"v1 expected_outcome={raw['expected_outcome']}"]
            if raw.get("expected_reason_code"):
                note_bits.append(f"v1 reason_code={raw['expected_reason_code']}")
            write_json(
                case_root / "oracle" / "premise_outcome" / f"{scenario_id}.json",
                PremiseOutcome(
                    scenario_id=scenario_id,
                    state=state,
                    scored_as=to_scored(state),
                    missing_terms=missing,
                    note="; ".join(note_bits),
                    provenance=oracle_prov("premise_outcome"),
                ),
            )

    print(f"Authored {len(case_dirs)} cases, {total_scenarios} scenarios into {DATA}")
    store = DataStore(DATA)
    print("Statutes:", store.statute_ids())
    print("Registers:", len(store.register_ids()))
    print("Scenario pairs:", len(store.all_scenarios()))


if __name__ == "__main__":
    main()
