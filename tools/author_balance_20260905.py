"""2026-09-05 Rulings E+F on the scenario suite.

Ruling E (English only): rewrite every request text in plain English, faithful to the
oracle claim set established by the 5 Sep audit (same claims, same silences); translate
case titles and scenario labels/descriptions.

Ruling F (balanced gold 18/18/18): retire five scenarios and author twelve new ones
(6 ALLOW, 6 DENY). For each new scenario the script writes scenarios/<id>.yaml, the
request text, and the four oracle files. ``term_fact`` is derived with the runtime
``lookup_facts`` over the overridden registry; ``premise_outcome`` is the operator's
expected gold and the script *asserts* that the z3 solver reproduces it before writing.

Run once from the repo root: ``.venv/bin/python tools/author_balance_20260905.py``.
Kept under tools/ for provenance (see docs/reference/gold-review-2026-09-05.md).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

from statute_decider.core.casefiles import RegisterOverride, Scenario
from statute_decider.core.enums import MissingReason, OutcomeState, ScoredOutcome
from statute_decider.core.outcome import MissingTerm, PremiseOutcome
from statute_decider.core.premises import ClaimPremise, ClaimSet
from statute_decider.core.provenance import Provenance
from statute_decider.core.store import DataStore
from statute_decider.core.terms import TermRef, UtteranceTerms
from statute_decider.nodes.executors import lookup_facts
from statute_decider.solvers.z3_backend import Z3Solver

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
store = DataStore(DATA)
STAMP = "2026-09-05T21:00:00Z"
NOTE = "Authored 2026-09-05 (Ruling F, balanced gold 18/18/18); see docs/reference/gold-review-2026-09-05.md."


def prov(node: str, notes: str = NOTE) -> Provenance:
    return Provenance(node=node, method="oracle", provider="human", model="operator", timestamp=STAMP, notes=notes)


def dump_json(path: Path, model) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# E1. English request texts (existing files). Faithful to the oracle claim sets.
# ---------------------------------------------------------------------------
BARE_PERMIT = "We submitted the building-permit application for our project. Please check whether the building permit can be issued."
BARE_WITHDRAW = "I want to withdraw from a purchase I made 5 days ago. The 14-day withdrawal period is still running and I sent the withdrawal notice to the seller yesterday."
STORY_OFFICIAL = "We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights."

TEXTS: dict[str, dict[str, str]] = {
    "building_permit_grant": {
        "allow_register_only.txt": BARE_PERMIT,
        "need_register_silent_fee.txt": BARE_PERMIT,
        "unverifiable_register_down_payment_ledger.txt": BARE_PERMIT,
        "unverifiable_trust_only_designer_selfreport.txt": BARE_PERMIT,
        "request_allow.txt": "We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. A competent person prepared the building design documentation, the site investigations have been performed, and the state fee has been paid. The building register shows no planning violations.",
        "deny_no_allow_path_designer_not_competent.txt": "We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. The site investigations have been performed and the state fee has been paid. However, the building design documentation was prepared by a relative who is not a competent person. The building register shows no planning violations.",
        "deny_no_allow_path_no_site_study.txt": "We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. A competent person prepared the building design documentation and the state fee has been paid, but no site investigations have been carried out yet. The building register shows no planning violations.",
        "deny_own_admission_plan_violation.txt": "The local planning authority has confirmed that the project does not conform to the detailed spatial plan - it exceeds the permitted building footprint and height. Although the project meets the requirements for construction works and building work, the site investigations have been performed, the state fee has been paid and a competent person designed it, the plan violation blocks the permit.",
    },
    "civil_service_admission": {
        "request_allow.txt": "I am an Estonian citizen with a completed secondary education and I am proficient in Estonian to the extent required by law. I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.",
        "allow_alt_rule_eu_citizen_overrides_register.txt": "I am not an Estonian citizen but a citizen of Finland, another EU Member State, with a completed secondary education, and I am proficient in Estonian to the extent required by law. I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.",
        "deny_no_allow_path_no_citizenship.txt": "I am applying for a civil-service position. I am a citizen of Georgia - neither an Estonian citizen nor a citizen of an EU Member State - with a completed secondary education, I am proficient in Estonian to the extent required by law and I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.",
        "deny_own_admission_conviction.txt": "I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education, I am proficient in Estonian to the extent required by law and I have active legal capacity, but I was convicted of an intentional criminal offence two years ago and the conviction is still on record. I confirm I have no family conflict with any supervising official at the agency.",
    },
    "consumer_purchase_withdrawal": {
        "request_allow.txt": "I bought a laptop from an online shop 5 days ago and it is a standard catalogue model (not made to order). I am a private consumer, the contract was concluded at a distance, the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller yesterday.",
        "allow_register_only_consumer_status.txt": BARE_WITHDRAW,
        "need_register_silent_consumer_status.txt": BARE_WITHDRAW,
        "unverifiable_register_down_trader_crm.txt": BARE_WITHDRAW,
        "unverifiable_trust_only_trader_selfreport.txt": BARE_WITHDRAW,
        "deny_no_allow_path_not_consumer.txt": "I ordered a standard catalogue office chair (not made to order) from an online shop for my company, and the invoice is in the company's name, so I am buying as a trader and not as a consumer. The contract was concluded at a distance, the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller yesterday.",
        "deny_own_admission_custom_goods.txt": "I ordered a custom engraved piece of furniture made to my personal specifications from an online shop; the contract was concluded at a distance. The product catalogue flags it as made to order, so under § 53 (4) the right of withdrawal is excluded even though I am a consumer, the 14-day period has not expired and I sent the withdrawal notice to the seller yesterday.",
        "request_need_user.txt": "I bought a standard catalogue laptop from an online shop and I am a consumer. The contract was concluded at a distance. I am not yet sure whether the 14-day withdrawal period is still running or whether I have sent a proper withdrawal notice - can the system decide based on what the trader knows?",
    },
    "journalistic_data_disclosure": {
        "request_allow.txt": "Our newsroom is preparing an investigative article. The processing is journalistic in purpose. The editor confirms there is public interest in the story and the reporting follows the principles of journalism ethics. The data subject has not granted a separate consent, and disclosure would not cause excessive damage to the subject's rights.",
        "allow_alt_rule_consent_overrides_register.txt": "Our newsroom wants to publish personal data about a private individual. The processing is not journalistic in purpose - it is a sponsored lifestyle feature - there is no public interest in it and it was not prepared under the principles of journalism ethics. The data subject has, however, granted explicit written consent to the publication, and it would not cause excessive damage to their rights.",
        "deny_no_allow_path_no_purpose_no_consent.txt": "Our editor reviewed the piece. It is a commercial advertorial rather than journalistic processing, although there is public interest in the topic and the text follows the principles of journalism ethics. No consent from the subject is on record. The newsroom risk review concludes that publication would not cause excessive damage to the subject's rights.",
        "deny_own_admission_excessive_harm.txt": "Our editor reviewed the story. The processing is journalistic in purpose, there is public interest and the reporting follows the principles of journalism ethics. No consent from the subject is on record. The newsroom risk review concludes that publication would cause excessive damage to the subject's private life and mental health.",
        "need_register_silent_purpose_and_consent.txt": STORY_OFFICIAL,
        "unverifiable_register_down_editorial_cms.txt": STORY_OFFICIAL,
        "unverifiable_trust_only_editorial_selfreport.txt": STORY_OFFICIAL,
        "need_user_silent_editorial_judgements.txt": "Our newsroom is preparing an investigative article. The processing is journalistic in purpose. The data subject has not granted a separate consent.",
    },
    "land_tax_home_exemption": {
        "request_allow.txt": "I am a pensioner and the owner of the parcel in Tartu. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. The municipal council has set the home-land exemption and I have submitted the application for the supplementary pensioner exemption.",
        "allow_register_only_ownership_and_residence.txt": "I am applying for the home-land tax incentive for my parcel in Tartu. The municipal council has set the home-land exemption and I have submitted the application for the supplementary exemption.",
        "deny_no_allow_path_not_residential.txt": "I am a pensioner and the owner of the parcel in Tartu. The population register has my residence at that address, but the cadastre lists the intended purpose of the land as profit-yielding land, not residential land. The municipal council has set the home-land exemption and I have submitted the application for the supplementary pensioner exemption.",
        "deny_own_admission_not_owner.txt": "I am a pensioner and I live in a rented apartment. I am not the owner of the land and my residence in the population register is elsewhere. The parcel is residential land owned by my neighbour. The municipal council has set the home-land exemption, but I have not submitted any application for the supplementary exemption.",
        "need_register_silent_municipality_exemption.txt": "I have submitted the application for the § 11 land tax incentive for my parcel in a rural municipality, but I do not know whether the municipal council has set the incentive yet.",
        "unverifiable_register_down_population_registry.txt": "I am applying for the home-land tax incentive for my parcel in Tartu and I have submitted the application for the supplementary exemption.",
        "unverifiable_trust_only_applicant_selfreport.txt": "I am applying for the home-land tax incentive for my parcel in Tartu. I have not yet submitted an application for the supplementary exemption.",
    },
}

SPAN_FIX = {
    "The processing is ajakirjanduslik in purpose": "The processing is journalistic in purpose",
    "has not granted a separate nõusolek": "has not granted a separate consent",
}

CASE_TITLES = {
    "building_permit_grant": ("Building Code §§ 42, 44", "Building-permit issuance check under the Building Code § 42 (1) and the § 44 refusal grounds."),
    "child_representation_by_one_parent": ("Family Law Act § 120", "Representation of a child by one parent under the Family Law Act § 120 (sole custody, delegated power of decision, emergency, joint consent)."),
    "civil_service_admission": ("Civil Service Act §§ 14–15", "Civil-servant appointment eligibility check under the Estonian Civil Service Act §§ 14–15."),
    "consumer_purchase_withdrawal": ("Law of Obligations Act § 53 (4), § 56 (1)", "Consumer right of withdrawal from a distance contract under the Law of Obligations Act § 56 (1), with the § 53 (4) exclusions."),
    "journalistic_data_disclosure": ("Personal Data Protection Act § 4", "Lawful-basis check for processing personal data for journalistic purposes without consent."),
    "land_tax_home_exemption": ("Land Tax Act § 11", "Home-land tax incentive and pensioner supplementary incentive under the Land Tax Act § 11."),
}

LABEL_SUBS = [
    (r"§ (\d+) lg (\d+) p (\d+)", r"§ \1 (\2) \3)"),
    (r"§ (\d+) lg (\d+)", r"§ \1 (\2)"),
    (r"§ (\d+) p (\d+)", r"§ \1 \2)"),
    (r"detail-plan", "detailed-spatial-plan"),
    (r"detail plan", "detailed spatial plan"),
    (r"NEED_DB_INFO", "NEED_REGISTER_INFO"),
    (r"needs_db_info", "needs_register_info"),
    (r"\bDB\b", "register"),
]


def english(s: str) -> str:
    for pat, rep in LABEL_SUBS:
        s = re.sub(pat, rep, s)
    return s


# ---------------------------------------------------------------------------
# F1. Retired scenarios (files removed; alias doc keeps the history rows)
# ---------------------------------------------------------------------------
RETIRE = {
    "child_representation_by_one_parent": [
        "allow_claims_verified_duplicate_probe_a",
        "allow_claims_verified_duplicate_probe_b",
        "need_user_silent_emergency_all_else_claimed",
        "need_user_silent_emergency_bare_request",
    ],
    "civil_service_admission": ["need_user_silent_conflict_declaration"],
}

# ---------------------------------------------------------------------------
# F2. New scenarios
# ---------------------------------------------------------------------------
NEW: list[dict] = [
    # ---- ALLOW -----------------------------------------------------------
    dict(
        case="child_representation_by_one_parent",
        id="allow_register_only_sole_custody",
        label="Child: bare request, custody register shows sole custody",
        mechanism="register_only",
        description="Intent supplies nothing; the population register resolves the parent and the custody register records sole custody -> ALLOW via § 120 (2) 1) (allow_sole_custody).",
        text="I need access to the child's data to make a decision on the child's behalf. Please check the registers and tell me whether I can act alone.",
        claims={},
        overrides={"child_representation_by_one_parent__custody_registry": {"set": {"main": {"sole_custody": True}}}},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "db-resolved", "via_db", "authored-20260905"],
    ),
    dict(
        case="child_representation_by_one_parent",
        id="allow_alt_rule_sole_custody_overrides_register",
        label="Child: parent claims sole custody, register says joint",
        mechanism="alt_rule_claim_overrides_register",
        description="Applicant asserts parenthood and sole custody; the custody register still shows joint custody, but the asserted claim takes precedence and the alternative rule allow_sole_custody fires -> ALLOW via § 120 (2) 1).",
        text="I am the child's father and I have sole custody of the child by court order. I need to act on the child's behalf alone.",
        claims={"applicant_is_parent": True, "applicant_is_not_parent": False, "sole_custody": True},
        overrides={},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="child_representation_by_one_parent",
        id="allow_alt_rule_delegated_right_overrides_register",
        label="Child: parent claims § 119 power of decision",
        mechanism="alt_rule_claim_overrides_register",
        description="Applicant asserts parenthood, joint custody and a court-granted power of decision under § 119; the custody register does not record the delegation, but the claim takes precedence and allow_delegated_right fires -> ALLOW via § 120 (2) 2).",
        text="I am the child's mother. We have joint custody, but the court has granted me the power of decision in this matter under § 119 of the Family Law Act, so I may decide alone.",
        claims={"applicant_is_parent": True, "applicant_is_not_parent": False, "sole_custody": False, "delegated_decision_right": True},
        overrides={},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="civil_service_admission",
        id="allow_register_only_citizenship",
        label="Admission: registers supply § 14 (1), conflict declared",
        mechanism="register_only",
        description="Applicant only gives the user-sourced § 15 4) non-conflict declaration; citizenship, education, language, capacity and the clean record all resolve from the registers -> ALLOW via § 14 (1) (allow_ee_citizen).",
        text="I am applying for a civil-service position; please check my eligibility against the registers. I confirm I have no family conflict with any supervising official at the agency.",
        claims={"no_conflict_declared": True},
        overrides={},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "db-resolved", "via_db", "authored-20260905"],
    ),
    dict(
        case="journalistic_data_disclosure",
        id="allow_register_only_purpose_from_cms",
        label="Journalism: CMS confirms purpose, editor supplies judgements",
        mechanism="register_only",
        description="Editor supplies the user-sourced public-interest and ethics judgements (and no excessive harm); the editorial CMS confirms the journalistic purpose and the consent register shows no consent -> ALLOW via § 4, first sentence (allow_journalism_basis).",
        text=STORY_OFFICIAL + " Please check the editorial system for the classification of the processing.",
        claims={"public_interest": True, "journalism_ethics": True, "excessive_harm": False},
        overrides={},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "db-resolved", "via_db", "authored-20260905"],
    ),
    dict(
        case="journalistic_data_disclosure",
        id="allow_register_only_consent_from_register",
        label="Journalism: bare request, consent register shows consent",
        mechanism="register_only",
        description="Intent supplies nothing; the consent register records the data subject's consent, so the consent baseline rule fires independently of the journalism basis -> ALLOW (allow_consent_basis).",
        text="We want to publish personal data about an individual in an upcoming piece. Please check the registers for whether we may proceed.",
        claims={},
        overrides={"journalistic_data_disclosure__consent_registry": {"set": {"main": {"subject_consent": True}}}},
        gold=OutcomeState.ALLOW, missing=[],
        tags=["positive", "db-resolved", "via_db", "consent-baseline", "authored-20260905"],
    ),
    # ---- DENY ------------------------------------------------------------
    dict(
        case="building_permit_grant",
        id="deny_register_only_plan_nonconformity",
        label="Permit: bare request, register shows plan non-conformity",
        mechanism="register_only",
        description="Intent supplies nothing; the building register records that the project does not conform to the detailed spatial plan (plan_conformant false, plan_violation true). The register fact plan_conformant=false closes the only allow path (§ 42 (1)); the solver draws register facts only for open allow-path terms, so deny_plan_violation is not triggered from the register -> default DENY with no applicable rules.",
        text=BARE_PERMIT,
        claims={},
        overrides={"building_permit_grant__building_registry": {"set": {"main": {"plan_violation": True, "plan_conformant": False}}}},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "db-resolved", "via_db", "authored-20260905"],
    ),
    dict(
        case="building_permit_grant",
        id="deny_no_allow_path_fee_unpaid",
        label="Permit: state fee unpaid, no allow path",
        mechanism="no_allow_path",
        description="Applicant admits the state fee is unpaid, blocking allow_building_permit (fee_paid is one of the 'requirements established in legislation' under § 42 (1)); no plan violation, so no deny rule fires -> DENY with no applicable rules.",
        text="We submitted the building-permit application. The project conforms to the detailed spatial plan and meets the requirements for construction works and building work. A competent person prepared the building design documentation and the site investigations have been performed, but we have not yet paid the state fee. The building register shows no planning violations.",
        claims={"plan_conformant": True, "building_requirements_met": True, "competent_designer": True, "site_study_provided": True, "fee_paid": False, "plan_violation": False},
        overrides={},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "no-basis", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="civil_service_admission",
        id="deny_no_allow_path_no_estonian_language",
        label="Admission: language requirement unmet, no allow path",
        mechanism="no_allow_path",
        description="Estonian citizen who does not meet the statutory Estonian-language requirement; speaks_estonian is false in both § 14 paths, no § 15 bar fires -> DENY with no applicable rules.",
        text="I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education and active legal capacity, but I do not yet speak Estonian at the level required by law. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.",
        claims={"ee_citizen": True, "eu_citizen": False, "secondary_education": True, "speaks_estonian": False, "full_capacity": True, "criminal_conviction": False, "no_conflict_declared": True},
        overrides={},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "no-basis", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="consumer_purchase_withdrawal",
        id="deny_no_allow_path_deadline_expired",
        label="Withdrawal: 14-day period expired, no allow path",
        mechanism="no_allow_path",
        description="Consumer, distance contract and non-excluded goods hold, but the consumer admits the 14-day period has expired and the notice was sent late; allow_distance_withdrawal is blocked and no § 53 (4) exclusion applies -> DENY with no applicable rules.",
        text="I bought a standard catalogue laptop (not made to order) from an online shop as a private consumer; the contract was concluded at a distance. I received it six weeks ago, so the 14-day withdrawal period has already expired, and I only sent the withdrawal notice to the seller yesterday, after the period had run out.",
        claims={"is_consumer": True, "distance_contract": True, "excluded_category": False, "within_14_days": False, "notice_sent_in_time": False},
        overrides={},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "no-basis", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="journalistic_data_disclosure",
        id="deny_no_allow_path_no_public_interest",
        label="Journalism: no public interest, no allow path",
        mechanism="no_allow_path",
        description="Journalistic purpose and ethics hold but the editor finds no public interest, so allow_journalism_basis is blocked; no consent on record blocks the consent baseline; no excessive harm -> DENY with no applicable rules.",
        text="Our editor reviewed the story. The processing is journalistic in purpose and the reporting follows the principles of journalism ethics, but the editor finds no public interest in the private details it discloses. No consent from the subject is on record. The risk review concludes that publication would not cause excessive damage to the subject's rights.",
        claims={"journalistic_purpose": True, "journalism_ethics": True, "public_interest": False, "subject_consent": False, "excessive_harm": False},
        overrides={},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "no-basis", "scripted-claims", "authored-20260905"],
    ),
    dict(
        case="land_tax_home_exemption",
        id="deny_no_allow_path_municipality_not_set",
        label="Land tax: council has not set the exemption, no allow path",
        mechanism="no_allow_path",
        description="All personal conditions hold (owner, residence, residential land, pensioner, application submitted) but the municipal council has not set the § 11 (1) incentive; both allow rules require municipality_exemption_set -> DENY with no applicable rules.",
        text="I am a pensioner and the owner of the parcel in a rural municipality. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. I have submitted the application for the supplementary pensioner exemption, but the municipal council has not set any home-land exemption for the coming tax period.",
        claims={"applicant_is_owner": True, "receives_pension": True, "residential_land": True, "primary_residence_registered": True, "application_submitted": True, "municipality_exemption_set": False},
        overrides={},
        gold=OutcomeState.DENY, missing=[],
        tags=["negative", "no-basis", "scripted-claims", "authored-20260905"],
    ),
]

SCORED = {
    OutcomeState.ALLOW: ScoredOutcome.ALLOW,
    OutcomeState.DENY: ScoredOutcome.DENY,
}


def main() -> None:
    solver = Z3Solver()
    # ---- E1: request texts + spans + case titles + labels -------------------
    for case_id, files in TEXTS.items():
        for fname, text in files.items():
            (DATA / "cases" / case_id / "sources" / "utterances" / fname).write_text(text + "\n", encoding="utf-8")
    for node in ("utterance_term", "term_claim"):
        p = DATA / "cases/journalistic_data_disclosure/oracle" / node / "need_user_silent_editorial_judgements.json"
        s = p.read_text(encoding="utf-8")
        for old, new in SPAN_FIX.items():
            s = s.replace(old, new)
        p.write_text(s, encoding="utf-8")
    for case_id, (title, desc) in CASE_TITLES.items():
        p = DATA / "cases" / case_id / "case.yaml"
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        d["title"], d["description"] = title, desc
        p.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True), encoding="utf-8")
    for case_id in store.case_ids():
        for sp in sorted((DATA / "cases" / case_id / "scenarios").glob("*.yaml")):
            d = yaml.safe_load(sp.read_text(encoding="utf-8"))
            for k in ("label", "description", "notes"):
                if d.get(k):
                    d[k] = english(d[k])
            sp.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # ---- F1: retire ---------------------------------------------------------
    for case_id, sids in RETIRE.items():
        cdir = DATA / "cases" / case_id
        keep_utts = set()
        for sp in cdir.glob("scenarios/*.yaml"):
            d = yaml.safe_load(sp.read_text(encoding="utf-8"))
            if d["scenario_id"] not in sids:
                keep_utts.add(d["utterance_file"])
        for sid in sids:
            sp = cdir / "scenarios" / f"{sid}.yaml"
            if not sp.exists():
                continue
            d = yaml.safe_load(sp.read_text(encoding="utf-8"))
            sp.unlink()
            for node in ("utterance_term", "term_claim", "term_fact", "premise_outcome"):
                op = cdir / "oracle" / node / f"{sid}.json"
                if op.exists():
                    op.unlink()
            up = cdir / "sources/utterances" / d["utterance_file"]
            if d["utterance_file"] not in keep_utts and up.exists():
                up.unlink()
            print("retired", case_id, sid)

    # ---- F2: author ---------------------------------------------------------
    for spec in NEW:
        case_id, sid = spec["case"], spec["id"]
        cdir = DATA / "cases" / case_id
        case = store.case(case_id)
        (cdir / "sources/utterances" / f"{sid}.txt").write_text(spec["text"] + "\n", encoding="utf-8")
        overrides = {k: RegisterOverride(**v) for k, v in spec["overrides"].items()}
        sc = Scenario(
            scenario_id=sid, case_id=case_id, label=spec["label"], mechanism=spec["mechanism"],
            description=spec["description"], utterance_file=f"{sid}.txt", register_overrides=overrides,
            tags=spec["tags"], gold_confidence="high", notes="",
            provenance="Authored 2026-09-05 (Ruling F, balanced gold 18/18/18); hand-verified in docs/reference/gold-review-2026-09-05.md",
        )
        (cdir / "scenarios" / f"{sid}.yaml").write_text(
            yaml.safe_dump(sc.model_dump(mode="json"), sort_keys=False, allow_unicode=True), encoding="utf-8")
        # reload so the store sees the new scenario
        fresh = DataStore(DATA)
        scenario = fresh.scenario(case_id, sid)
        term_ids = sorted(spec["claims"])
        utt = UtteranceTerms(scenario_id=sid, term_refs=[TermRef(term_id=t, span="", confidence=None) for t in term_ids],
                             provenance=prov("utterance_term"))
        claims = ClaimSet(scenario_id=sid, claims=[
            ClaimPremise(premise_id=f"claim_{t}", term_id=t, value=spec["claims"][t], span="") for t in term_ids],
            provenance=prov("term_claim"))
        registry = fresh.scenario_registry(case_id, scenario)
        mappings = [fresh.oracle_record_term(rid) for rid in case.register_ids]
        facts = lookup_facts(sid, registry, mappings)
        facts.provenance = prov("term_fact")
        catalog = fresh.oracle_text_term(case.statute_ids[0])
        rules = fresh.oracle_term_rule(case.statute_ids[0])
        produced = solver.solve(catalog, rules, claims, facts)
        assert produced.state == spec["gold"], (sid, produced.state, produced.missing_terms, produced.fired_rules)
        assert sorted(m.term_id for m in produced.missing_terms) == sorted(spec["missing"]), (sid, produced.missing_terms)
        outcome = PremiseOutcome(
            scenario_id=sid, state=spec["gold"], scored_as=SCORED[spec["gold"]],
            missing_terms=[MissingTerm(term_id=t, reason=MissingReason.NO_VALUE) for t in spec["missing"]],
            fired_rules=[], valuation={}, free_missing=[],
            note=f"authored 2026-09-05; solver check: fired={[f.premise_id for f in produced.fired_rules]}",
            provenance=prov("premise_outcome"),
        )
        dump_json(cdir / "oracle/utterance_term" / f"{sid}.json", utt)
        dump_json(cdir / "oracle/term_claim" / f"{sid}.json", claims)
        dump_json(cdir / "oracle/term_fact" / f"{sid}.json", facts)
        dump_json(cdir / "oracle/premise_outcome" / f"{sid}.json", outcome)
        print(f"authored {case_id}/{sid}: {produced.state.value} fired={[f.premise_id for f in produced.fired_rules]}")

    # ---- class table --------------------------------------------------------
    fresh = DataStore(DATA)
    table: dict[str, dict[str, int]] = {}
    for case_id, sid in fresh.all_scenarios():
        st = fresh.oracle_value(case_id, "premise_outcome", sid).scored_as.value
        table.setdefault(case_id, {}).setdefault(st, 0)
        table[case_id][st] += 1
    tot: dict[str, int] = {}
    for case_id, row in table.items():
        print(f"{case_id:38} " + "  ".join(f"{k}={v}" for k, v in sorted(row.items())))
        for k, v in row.items():
            tot[k] = tot.get(k, 0) + v
    print("TOTAL", tot, sum(tot.values()))


if __name__ == "__main__":
    main()
