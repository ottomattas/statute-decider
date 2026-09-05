import json, subprocess
from pathlib import Path
from statute_decider.core.store import DataStore
from statute_decider.solvers.z3_backend import Z3Solver

ROOT = Path("/Users/ottomattas/src/ottomattas/statute-decider")
store = DataStore(ROOT / "data")
z3 = Z3Solver()

PATHS = {
    "allow_register_only_sole_custody": "No claims. Stage 1 leaves every allow path open on register terms; stage 2 draws `applicant_is_parent=true` (population register) and `sole_custody=true` (custody register, scenario override). `allow_sole_custody` (§ 120 (2) 1)) is entailed; both facts are authoritative, so no warrant flag → **ALLOW**.",
    "allow_alt_rule_sole_custody_overrides_register": "Claims seed `applicant_is_parent=true`, `applicant_is_not_parent=false`, `sole_custody=true`. `allow_sole_custody` is entailed from claims alone. Warrant check: both antecedents are register-evidence terms covered by available registers; the population register confirms parenthood (authoritative, true); the custody register holds `sole_custody=false`, i.e. an authoritative value exists for the term, so it is not 'claim on a silent register' — the claim takes precedence (defeasible premises win at stage 1; facts only fill what is missing). → **ALLOW** via the alternative rule. Same shape as `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register`.",
    "allow_alt_rule_delegated_right_overrides_register": "Claims: parent true, not-parent false, `sole_custody=false`, `delegated_decision_right=true`. `allow_delegated_right` (§ 120 (2) 2)) is entailed from claims; the custody register's `delegated_decision_right=false` is an authoritative value, so the warrant check has nothing unverified to flag. → **ALLOW**.",
    "allow_register_only_citizenship": "Only the user-evidence claim `no_conflict_declared=true`. Stage 2 draws `ee_citizen`, `secondary_education`, `speaks_estonian`, `full_capacity` (all true, authoritative). `allow_ee_citizen` (§ 14 (1)) is entailed; `criminal_conviction` is a deny-only term and is not consulted. → **ALLOW**.",
    "allow_register_only_purpose_from_cms": "Claims: `public_interest=true`, `journalism_ethics=true`, `excessive_harm=false` (user-evidence terms). Stage 2 draws `journalistic_purpose=true` from the editorial CMS. `allow_journalism_basis` (§ 4, first sentence) is entailed; the defeater `block_ethics_when_excessive_harm` does not fire. → **ALLOW**.",
    "allow_register_only_consent_from_register": "No claims. Stage 2 draws `subject_consent=true` (consent register, scenario override) and `journalistic_purpose=true`. `allow_consent_basis` is entailed on an authoritative fact; the journalism path stays open on user terms but is irrelevant once ALLOW is entailed. → **ALLOW**.",
    "deny_register_only_plan_nonconformity": "No claims. Stage 2 draws the five § 42 (1) terms; `plan_conformant=false` (building register, scenario override) closes the only allow path. The register also records `plan_violation=true`, but the solver draws register facts only for open allow-path terms, so `deny_plan_violation` is not triggered from the register. Nothing decision-relevant is missing → default **DENY** (no applicable rules). This is the one register-only DENY in the suite and documents a solver property worth the operator's attention (see the ES report).",
    "deny_no_allow_path_fee_unpaid": "Claims set all § 42 (1) terms true except `fee_paid=false`; `plan_violation=false`. `allow_building_permit` is blocked on `fee_paid`; the deny rule does not fire. Nothing missing → **DENY** (no applicable rules). Different term from the existing `designer_not_competent` / `no_site_study` variants.",
    "deny_no_allow_path_no_estonian_language": "Claims: `ee_citizen=true`, `eu_citizen=false`, `speaks_estonian=false`, the rest true, `criminal_conviction=false`, `no_conflict_declared=true`. Both § 14 paths require `speaks_estonian`; both are blocked; `deny_conviction` does not fire → **DENY** (no applicable rules).",
    "deny_no_allow_path_deadline_expired": "Claims: `is_consumer=true`, `distance_contract=true`, `excluded_category=false`, `within_14_days=false`, `notice_sent_in_time=false`. `allow_distance_withdrawal` (§ 56 (1)) is blocked on the two user terms; `deny_excluded_category` (§ 53 (4)) does not fire → **DENY** (no applicable rules).",
    "deny_no_allow_path_no_public_interest": "Claims: `journalistic_purpose=true`, `journalism_ethics=true`, `public_interest=false`, `subject_consent=false`, `excessive_harm=false`. `allow_journalism_basis` is blocked on `public_interest`; `allow_consent_basis` is blocked on `subject_consent`; the defeater does not fire → **DENY** (no applicable rules).",
    "deny_no_allow_path_municipality_not_set": "Claims: owner, pensioner, residential land, residence registered, application submitted all true; `municipality_exemption_set=false`. Both `allow_home_land_exemption` (§ 11 (1)) and `allow_pensioner_supplement` (§ 11 (5) 1)) require the council's incentive; both blocked; no deny rule exists → **DENY** (no applicable rules).",
}

out = []
out.append("# Gold review — 2026-09-05 (English request texts, balanced 18/18/18)\n")
out.append("""Operator hand-verification sheet for the suite change of 2026-09-05 (execution brief
"Ruling E — English only" and "Ruling F — balanced gold"). Everything below was
regenerated from the data files by a script, then annotated; the solver check column
is the z3 result on oracle claims + oracle facts (the `solver-validation` condition).
Full run: `experiments/20260906-solver-validation/results/summary.md` — 54/54, macro F1 1.000.

Sections: 1. class table · 2. the twelve authored scenarios · 3. retired scenarios ·
4. request texts that changed (all 35 rewritten files, with the one material change flagged) ·
5. catalogue wording changes that touch gold reasoning.

## 1. Class table (scored three-way)

""")
table = {}
for c, s in store.all_scenarios():
    st = store.oracle_value(c, "premise_outcome", s).scored_as.value
    table.setdefault(c, {"ALLOW": 0, "DENY": 0, "NEED_MORE_INFO": 0})[st] += 1
out.append("| case | ALLOW | DENY | NEED_MORE_INFO | total |\n|---|---|---|---|---|")
tot = {"ALLOW": 0, "DENY": 0, "NEED_MORE_INFO": 0}
for c, r in table.items():
    out.append(f"| `{c}` | {r['ALLOW']} | {r['DENY']} | {r['NEED_MORE_INFO']} | {sum(r.values())} |")
    for k in tot: tot[k] += r[k]
out.append(f"| **total** | **{tot['ALLOW']}** | **{tot['DENY']}** | **{tot['NEED_MORE_INFO']}** | **{sum(tot.values())}** |")
out.append("\nNEED_MORE_INFO pools NEED_REGISTER_INFO, NEED_USER_INFO and UNVERIFIABLE_CLAIM (fine states kept in the oracle). Before: 47 = 14/12/21.\n")

out.append("## 2. Authored scenarios (12)\n")
out.append("Each block: request text → oracle claims → register overrides → facts the lookup produces → expected outcome → rule path (why the solver lands there) → solver check.\n")
n = 0
for c, s in store.all_scenarios():
    sc = store.scenario(c, s)
    if "authored-20260905" not in sc.tags:
        continue
    n += 1
    case = store.case(c)
    claims = store.oracle_value(c, "term_claim", s)
    facts = store.oracle_value(c, "term_fact", s)
    gold = store.oracle_value(c, "premise_outcome", s)
    produced = z3.solve(store.oracle_text_term(case.statute_ids[0]), store.oracle_term_rule(case.statute_ids[0]), claims, facts)
    out.append(f"### 2.{n} `{c}/{s}`\n")
    out.append(f"- **Label:** {sc.label}  \n- **Mechanism:** `{sc.mechanism}`  \n- **Gold:** {gold.state.value} (scored {gold.scored_as.value}); missing terms: {[m.term_id for m in gold.missing_terms] or 'none'}")
    out.append(f"- **Request text:** “{store.utterance_text(c, sc).strip()}”")
    cl = ", ".join(f"`{x.term_id}={str(x.value).lower()}`" for x in claims.claims) or "none (bare request)"
    out.append(f"- **Oracle claims:** {cl}")
    ov = json.dumps({k: v.model_dump(exclude_defaults=True) for k, v in sc.register_overrides.items()}) if sc.register_overrides else "none (base registry)"
    out.append(f"- **Register overrides:** `{ov}`" if sc.register_overrides else f"- **Register overrides:** {ov}")
    fs = ", ".join(f"`{f.term_id}={str(f.value).lower()}` ({f.register_id.split('__')[-1]}, {f.warrant.value})" for f in facts.facts)
    out.append(f"- **Facts (lookup):** {fs}")
    out.append(f"- **Rule path:** {PATHS[s]}")
    out.append(f"- **Solver check:** {produced.state.value}; fired = {[f.premise_id for f in produced.fired_rules] or 'none'}; note: “{produced.note}”\n")

out.append("## 3. Retired scenarios (5)\n")
out.append("""| id | gold | reason |
|---|---|---|
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` | ALLOW | inputs byte-identical to `allow_claims_verified_emergency` |
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` | ALLOW | inputs byte-identical to `allow_claims_verified_emergency` |
| `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` | NEED_USER_INFO | gold `{emergency}`, same as the kept `need_user_silent_emergency_after_register_lookup` |
| `child_representation_by_one_parent/need_user_silent_emergency_bare_request` | NEED_USER_INFO | gold `{emergency}`, same as the kept scenario |
| `civil_service_admission/need_user_silent_conflict_declaration` | NEED_USER_INFO | the operator's "one more": a single user-only term open after all register terms resolve — the shape the kept § 120 scenario already covers; the two-user-term `user_silent` variant survives in consumer and journalism; civil service keeps its `register_silent` / `register_down` / `trust_only` NEEDs, so the NEED grid stays 3–4 per case except child (1) |

Files removed: scenario YAML, four oracle JSONs, and the request texts used only by them
(`request_need_db.txt`, `need_user_silent_emergency_all_else_claimed.txt`,
`request_allow_conflict_silent.txt`). Rows stay in `docs/reference/id-aliases.md` (marked
retired) and in every pre-existing experiment folder.
""")

out.append("## 4. Request texts rewritten in English (35 files, 42 pre-existing scenarios)\n")
out.append("""Rule: same claims, same silences as the 5 Sep faithful-inputs audit; Estonian legal
terms replaced with the official translation's terminology (`building permit`,
`detailed spatial plan`, `competent person`, `site investigations`, `state fee`,
`consumer`, `distance contract`, `withdrawal notice`, `made to order`, `journalistic
purpose`, `public interest`, `principles of journalism ethics`, `consent`, `excessive
damage`, `home-land tax incentive`, `residential land`, `profit-yielding land`,
`population register`, `municipal council`, `proficient in Estonian`, `active legal
capacity`). Files already in plain English (child case; `need_register_silent_citizenship`
and its register_down / trust_only siblings) were left as they were.

Authoring scripts of that day (`tools/author_faithful_inputs_20260905.py`,
`tools/author_balance_20260905.py`) were retired to git history after use (commits
`e2d00f4`, `a60afa1`): their literals carried the superseded mixed-language texts.

**One material change** — `journalistic_data_disclosure/request_allow.txt` (used by
`allow_claims_verified`): the clause that carried `excessive_harm=false` read "but the
reporting is proportionate"; it now reads "and disclosure would not cause excessive damage
to the subject's rights", i.e. the statute's own § 4 second-sentence test. Claim set
unchanged. This closes the previous report's second catalogue caveat (`excessive_harm`
resting on "proportionate"). Spans in the two oracle files that quote text
(`need_user_silent_editorial_judgements`, `utterance_term` + `term_claim`) were updated
to the English wording.

| case | file | scenarios using it | claims (unchanged) |
|---|---|---|---|""")
seen = set()
for c, s in store.all_scenarios():
    sc = store.scenario(c, s)
    if "authored-20260905" in sc.tags:
        continue
    key = (c, sc.utterance_file)
    if key in seen:
        continue
    seen.add(key)
    users = [t for cc, t in store.all_scenarios() if cc == c and store.scenario(cc, t).utterance_file == sc.utterance_file]
    claims = store.oracle_value(c, "term_claim", s)
    cl = ", ".join(f"{x.term_id}={'T' if x.value else 'F'}" for x in claims.claims) or "—"
    out.append(f"| `{c}` | `{sc.utterance_file}` | {', '.join(f'`{u}`' for u in users)} | {cl} |")

out.append("""
## 5. Catalogue wording that touches gold reasoning

- `civil_service_act/eu_citizen` — label "Applicant is a citizen of another EU Member State";
  definition now states "other than Estonia … exclusive of `ee_citizen`". This makes the
  catalogue say what every scenario already assumed (`ee_citizen=true` ↔ `eu_citizen=false`
  in all claim sets and in the population register record) and matches § 14 (2)'s "may
  **also** be employed". No gold changes; the previous report's first caveat is closed as a
  wording fix.
- `personal_data_protection_act/excessive_harm` — label "Disclosure would cause excessive damage to the data
  subject's rights"; definition cites § 4, second sentence. Together with the request-text
  change above, the term no longer rests on "proportionate".
- `building_code/site_study_provided` — label "Required site investigations have been
  performed" (the official translation's wording); id unchanged.
- All `clause_title` values use "§ N (subsection) clause)" (e.g. `§ 11 (5) 1)`, `§ 56 (2¹)`,
  `§ 4`); since the evening of 2026-09-05 `clause_id` values are `<act_slug>/<eId>` resolved
  against the Riigi Teataja XML (`docs/reference/legislation-corpus.md`).
""")
(ROOT / "docs/reference/gold-review-2026-09-05.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("written", n)
