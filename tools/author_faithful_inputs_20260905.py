"""One-off: write utterance-faithful request files (Ruling A), point scenarios at them.
Run from the statute-decider repo root. Oracle files, gold and register data untouched."""
import subprocess, sys, yaml
from pathlib import Path

sys.path.insert(0, "src")

NEW = {
# ---------------- building_permit_grant ----------------
("building_permit_grant", "allow_register_only"): (
    "TRIMMED",
    "We submitted the building-permit application for our project. Please check whether the ehitusluba can be issued.\n"),
("building_permit_grant", "need_register_silent_fee"): (
    "TRIMMED",
    "We submitted the building-permit application for our project. Please check whether the ehitusluba can be issued.\n"),
("building_permit_grant", "unverifiable_register_down_payment_ledger"): (
    "TRIMMED",
    "We submitted the building-permit application for our project. Please check whether the ehitusluba can be issued.\n"),
("building_permit_grant", "unverifiable_trust_only_designer_selfreport"): (
    "TRIMMED",
    "We submitted the building-permit application for our project. Please check whether the ehitusluba can be issued.\n"),
("building_permit_grant", "deny_own_admission_plan_violation"): (
    "UNDERSTATED",
    "The local planning authority has confirmed that the project is detailplaneeringuga vastuolus - it exceeds the permitted building footprint and height. Although the project meets the ehitusnõue in the building code, the ehitusuuring is available, riigilõiv has been paid and a pädev isik designed it, the plan violation blocks the permit.\n"),
("building_permit_grant", "deny_no_allow_path_designer_not_competent"): (
    "CONTRADICTS",
    "We submitted the building-permit application. The project vastab detailplaneeringule and also meets the ehitusnõue in the building code. The ehitusuuring is available and the riigilõiv has been paid. However, the design was prepared by a relative who is not a pädev isik. The building registry shows no planning violations.\n"),
("building_permit_grant", "deny_no_allow_path_no_site_study"): (
    "CONTRADICTS",
    "We submitted the building-permit application. The project vastab detailplaneeringule and also meets the ehitusnõue in the building code. The pädev isik prepared the design and the riigilõiv has been paid, but no ehitusuuring has been carried out yet. The building registry shows no planning violations.\n"),
# ---------------- civil_service_admission ----------------
("civil_service_admission", "allow_alt_rule_eu_citizen_overrides_register"): (
    "CONTRADICTS",
    "I am not an Estonian citizen but a citizen of Finland, an EU member state, with a completed secondary education and I valdab eesti keelt at the level required by law. I have full legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.\n"),
("civil_service_admission", "deny_own_admission_conviction"): (
    "UNDERSTATED",
    "I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education, I valdab eesti keelt at the level required by law and I have full legal capacity, but I was karistatud for an intentional crime two years ago and the conviction is still on record. I confirm I have no family conflict with any supervising official at the agency.\n"),
("civil_service_admission", "deny_no_allow_path_no_citizenship"): (
    "CONTRADICTS",
    "I am applying for a civil-service position. I am a citizen of Georgia - neither an Estonian citizen nor a citizen of an EU member state - with a completed secondary education, I valdab eesti keelt at the level required by law and I have full legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.\n"),
("civil_service_admission", "need_register_silent_citizenship"): (
    "TRIMMED",
    "I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency.\n"),
("civil_service_admission", "unverifiable_register_down_population_registry"): (
    "TRIMMED",
    "I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency.\n"),
("civil_service_admission", "unverifiable_trust_only_applicant_selfreport"): (
    "TRIMMED",
    "I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency.\n"),
# ---------------- consumer_purchase_withdrawal ----------------
("consumer_purchase_withdrawal", "allow_register_only_consumer_status"): (
    "TRIMMED",
    "I want to withdraw from a purchase I made 5 days ago. The 14 päeva tähtaeg is still running and I sent the taganemisavaldus to the seller yesterday.\n"),
("consumer_purchase_withdrawal", "need_register_silent_consumer_status"): (
    "TRIMMED",
    "I want to withdraw from a purchase I made 5 days ago. The 14 päeva tähtaeg is still running and I sent the taganemisavaldus to the seller yesterday.\n"),
("consumer_purchase_withdrawal", "unverifiable_register_down_trader_crm"): (
    "TRIMMED",
    "I want to withdraw from a purchase I made 5 days ago. The 14 päeva tähtaeg is still running and I sent the taganemisavaldus to the seller yesterday.\n"),
("consumer_purchase_withdrawal", "unverifiable_trust_only_trader_selfreport"): (
    "TRIMMED",
    "I want to withdraw from a purchase I made 5 days ago. The 14 päeva tähtaeg is still running and I sent the taganemisavaldus to the seller yesterday.\n"),
("consumer_purchase_withdrawal", "deny_own_admission_custom_goods"): (
    "UNDERSTATED",
    "I ordered a custom engraved piece of furniture tailored to my isiklikud vajadused from an e-pood; the leping was sõlmitud sidevahendi abil. The product catalogue flags it as tellimustöö, so under § 53 (4) the taganemisõigus is excluded even though I am a tarbija, the 14-day deadline has not expired and I sent the taganemisavaldus to the seller yesterday.\n"),
("consumer_purchase_withdrawal", "deny_no_allow_path_not_consumer"): (
    "CONTRADICTS",
    "I ordered a standard catalogue office chair (not a tellimustöö) from an e-pood for my company, and the invoice is in the company's name, so I am buying as an ettevõtja and not as a tarbija. The leping was sõlmitud sidevahendi abil, the 14 päeva tähtaeg is still running, and I sent the taganemisavaldus to the seller yesterday.\n"),
# ---------------- land_tax_home_exemption ----------------
("land_tax_home_exemption", "allow_register_only_ownership_and_residence"): (
    "TRIMMED",
    "I am applying for the home-land maamaksuvabastus for my parcel in Tartu. The local omavalitsuse volikogu has set the home-land exemption and I have submitted the taotlus for the supplementary exemption.\n"),
("land_tax_home_exemption", "deny_own_admission_not_owner"): (
    "UNDERSTATED",
    "I am a pensionär and I live in a rented apartment. I am not the omanik of the land and my elukoht in the rahvastikuregister is elsewhere. The parcel is elamumaa owned by my neighbour. The local omavalitsuse volikogu has set the home-land exemption, but I have not submitted any taotlus for the supplementary exemption.\n"),
("land_tax_home_exemption", "deny_no_allow_path_not_residential"): (
    "CONTRADICTS",
    "I am a pensionär and the omanik of the parcel in Tartu. The rahvastikuregister has my elukoht at that address, but the cadastre lists the maa sihtotstarve as maatulundusmaa, not elamumaa. The local omavalitsuse volikogu has set the home-land exemption and I have submitted the taotlus for the supplementary pensioner exemption.\n"),
("land_tax_home_exemption", "need_register_silent_municipality_exemption"): (
    "TRIMMED",
    "I have submitted the taotlus for the § 11 maamaksusoodustus for my parcel in a rural municipality, but I do not know whether the local omavalitsuse volikogu has set the soodustus yet.\n"),
("land_tax_home_exemption", "unverifiable_register_down_population_registry"): (
    "TRIMMED",
    "I am applying for the home-land maamaksuvabastus for my parcel in Tartu and I have submitted the taotlus for the supplementary exemption.\n"),
("land_tax_home_exemption", "unverifiable_trust_only_applicant_selfreport"): (
    "CONTRADICTS",
    "I am applying for the home-land maamaksuvabastus for my parcel in Tartu. I have not yet submitted a taotlus for the supplementary exemption.\n"),
# ---------------- journalistic_data_disclosure ----------------
("journalistic_data_disclosure", "allow_alt_rule_consent_overrides_register"): (
    "CONTRADICTS",
    "Our newsroom wants to publish personal data about a private individual. The processing is not ajakirjanduslik in purpose - it is a sponsored lifestyle feature - there is no avalik huvi in it and it was not prepared under the code of ajakirjanduseetika. The data subject has, however, granted an explicit written nõusolek to the publication, and it would not ülemäära kahjusta them.\n"),
("journalistic_data_disclosure", "deny_own_admission_excessive_harm"): (
    "UNDERSTATED",
    "Our editor reviewed the story. The processing is ajakirjanduslik in purpose, there is avalik huvi and the reporting follows the code of ajakirjanduseetika. No nõusolek from the subject is on record. The newsroom risk-review concludes that publication would ülemäära kahjustaks the subject's private life and mental health.\n"),
("journalistic_data_disclosure", "deny_no_allow_path_no_purpose_no_consent"): (
    "CONTRADICTS",
    "Our editor reviewed the piece. It is a commercial advertorial rather than ajakirjanduslik processing, although there is avalik huvi in the topic and the text follows the code of ajakirjanduseetika. No nõusolek from the subject is on record. The newsroom risk-review concludes that publication would not ülemäära kahjusta the subject.\n"),
("journalistic_data_disclosure", "need_user_silent_editorial_judgements"): (
    "TRIMMED",
    "Our newsroom is preparing an investigative article. The processing is ajakirjanduslik in purpose. The data subject has not granted a separate nõusolek.\n"),
("journalistic_data_disclosure", "unverifiable_register_down_editorial_cms"): (
    "TRIMMED",
    "We are preparing a story about a public official. The editor confirms there is avalik huvi in it and the work follows the code of ajakirjanduseetika; publication would not ülemäära kahjusta the subject.\n"),
("journalistic_data_disclosure", "need_register_silent_purpose_and_consent"): (
    "TRIMMED",
    "We are preparing a story about a public official. The editor confirms there is avalik huvi in it and the work follows the code of ajakirjanduseetika; publication would not ülemäära kahjusta the subject.\n"),
("journalistic_data_disclosure", "unverifiable_trust_only_editorial_selfreport"): (
    "TRIMMED",
    "We are preparing a story about a public official. The editor confirms there is avalik huvi in it and the work follows the code of ajakirjanduseetika; publication would not ülemäära kahjusta the subject.\n"),
# ---------------- child_representation_by_one_parent ----------------
("child_representation_by_one_parent", "need_user_silent_emergency_all_else_claimed"): (
    "UNDERSTATED",
    "I am the child's mother. I do not have sole custody. No decision right was delegated to me. Both parents' consent has not been confirmed. The other parent is reachable. I do not yet know whether this is an emergency.\n"),
}

ORDER = ["scenario_id", "case_id", "label", "mechanism", "description", "utterance_file",
         "register_overrides", "tags", "gold_confidence", "notes", "provenance"]
TAG = "utterance-rewritten-20260905"
old_files: dict[tuple[str, str], str] = {}
for (case, scen), (cls, text) in NEW.items():
    p = Path(f"data/cases/{case}/scenarios/{scen}.yaml")
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    old_files[(case, scen)] = d["utterance_file"]
    out = Path(f"data/cases/{case}/sources/utterances/{scen}.txt")
    out.write_text(text, encoding="utf-8")
    d["utterance_file"] = f"{scen}.txt"
    if TAG not in d["tags"]:
        d["tags"].append(TAG)
    note = (f"Utterance rewritten 2026-09-05 to match the oracle claim set ({cls}; was {old_files[(case, scen)]}); "
            "see docs/reference/faithful-inputs-audit-2026-09-05.md.")
    d["notes"] = (str(d.get("notes") or "").strip() + " | " if d.get("notes") else "") + note
    ordered = {k: d[k] for k in ORDER if k in d}
    ordered.update({k: v for k, v in d.items() if k not in ordered})
    p.write_text(yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True), encoding="utf-8")

# remove old utterance files no longer referenced by any scenario
from statute_decider.core import DataStore
store = DataStore("data")
used = {(c, store.scenario(c, s).utterance_file) for c, s in store.all_scenarios()}
for case in store.case_ids():
    for f in sorted(Path(f"data/cases/{case}/sources/utterances").glob("*.txt")):
        if (case, f.name) not in used:
            subprocess.run(["git", "rm", "-q", str(f)], check=True)
            print("removed unused", f)
print("done", len(NEW))
