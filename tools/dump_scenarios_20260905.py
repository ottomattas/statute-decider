"""Dump every scenario's gold, mechanism, claims, facts, overrides and text (review aid, 2026-09-05)."""
import json, sys
from pathlib import Path
from statute_decider.core.store import DataStore

root = Path(__file__).resolve().parents[1]
store = DataStore(root / "data")
full = "--full" in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith("--")]
for case_id in store.case_ids():
    if only and case_id not in only:
        continue
    case = store.case(case_id)
    print(f"\n######## {case_id}  statutes={case.statute_ids}")
    print("registers:", case.register_ids)
    reg = json.loads((root / "data/cases" / case_id / "sources/registry.json").read_text())
    print("registry.json:", json.dumps(reg)[:1500])
    for cid, sid in store.all_scenarios():
        if cid != case_id:
            continue
        sc = store.scenario(case_id, sid)
        out = store.oracle_value(case_id, "premise_outcome", sid)
        claims = store.oracle_value(case_id, "term_claim", sid)
        facts = store.oracle_value(case_id, "term_fact", sid)
        ut = store.oracle_value(case_id, "utterance_term", sid)
        print(f"\n-- {sid}  gold={out.state.value} mech={sc.mechanism} utt={sc.utterance_file} tags={sc.tags}")
        print("   label:", sc.label)
        print("   desc:", sc.description)
        print("   overrides:", json.dumps({k: v.model_dump(exclude_defaults=True) for k, v in sc.register_overrides.items()}))
        print("   claims:", {c.term_id: c.value for c in claims.claims})
        print("   utt_terms:", [t.term_id for t in ut.term_refs])
        print("   facts:", {f.term_id: (f.value, f.warrant.value, f.register_id.split('__')[-1]) for f in facts.facts},
              "unavail_regs=", facts.unavailable_registers, "unavail_terms=", facts.unavailable_terms,
              "conflicts=", facts.conflicts, "covered=", facts.covered_terms)
        print("   missing:", [(m.term_id, m.reason.value) for m in out.missing_terms], "fired:", [f.premise_id for f in out.fired_rules], "note:", out.note)
        if full:
            print("   TEXT:", store.utterance_text(case_id, sc).strip())
