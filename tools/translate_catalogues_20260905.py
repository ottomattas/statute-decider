"""Translate the remaining Estonian strings in data/statutes/*/oracle/{text_term,term_rule}.json.

Anchor quotes are replaced with the corresponding official English translation text
(same provision), clause titles switch to the "§ N (subsection) clause)" style, and
labels/definitions/notes lose their Estonian parentheticals. clause_id values are untouched.
"""
import json, re, glob, sys

ROOT = "/Users/ottomattas/src/ottomattas/statute-decider"

ATS_14_1 = "An Estonian citizen who has at least a secondary education, has active legal capacity and is proficient in Estonian to the extent provided by law or on the basis thereof may be employed in the service."
ATS_14_2 = "A citizen of a Member State of the European Union who conforms to the requirements established by law and on the basis thereof may also be employed in the service."
EHS_42_1 = "The building permit is issued if the building design documentation that has been filed conforms to the requirements established in legislation, i.e., above all to the detailed spatial plan or design specifications and to the requirements for construction works and for building work."
IKS_4_S1 = "Personal data may be processed and disclosed in the media for journalistic purposes without the consent of the data subject, in particular disclosed in the media, if there is public interest and this is in accordance with the principles of journalism ethics."
IKS_4_S2 = "Disclosure of personal data must not cause excessive damage to the rights of any data subjects."
MMS_11_1 = "The municipal council may establish by a regulation, under the conditions provided in subsection 1¹ of this section, a tax incentive of up to 1,000 euros on the land under the home at the latest by 1 October of the year preceding the tax period."
MMS_11_7 = "To receive additional tax incentive specified in subsection 5 or 6 of this section, a person who meets the conditions provided in this section submits an application to the municipality in accordance with the procedure established by the council."
VOS_56_1 = "A consumer may withdraw from a distance contract within 14 days without giving any reason."
VOS_56_21 = "The deadline for withdrawal from a distance contract shall be deemed to have been observed by the consumer if the consumer has dispatched a notification concerning the withdrawal to the trader during the withdrawal period."
PKS_120_1 = "A parent who has legal custody is the legal representative of a child. Parents who have joint legal custody have a joint right of representation."
PKS_120_2 = "A parent represents his or her child alone if: 1) he or she has sole legal custody of the child, or 2) the powers of decision have been transferred to him or her pursuant to § 119 of this Act."
PKS_120_3 = "If making a joint declaration of intention of the parents would cause a delay in conflict with the interests of the child, one parent has the right to enter into necessary transactions and perform necessary acts in the interests of the child also alone."
PKS_118_1_120_1 = "Parents shall exercise joint legal custody with respect to their child and perform the custodial obligation on their own responsibility and unanimously considering all-round well-being of the child. Parents who have joint legal custody have a joint right of representation."

# (clause_id, old Estonian quote prefix) -> (new clause_title, new quote)
ANCHORS = {
    ("ats_14_1", "Ametnikuna"): ("§ 14 (1)", ATS_14_1),
    ("ats_14_2", "Ametnikuna"): ("§ 14 (2)", ATS_14_2),
    ("ats_15_1", "Teenistusse"): ("§ 15 1)", "The following person may not be employed in service: 1) who is under punishment for an intentionally committed criminal offence;"),
    ("ats_15_4", "Teenistusse"): ("§ 15 4)", "The following person may not be employed in service: ... 4) who is a spouse or a partner in the marriage-like relationship (hereinafter unmarried partner) or a grandparent, a parent of an official who has direct control over the corresponding post, or a parent or a descendant of the parent, including a child and grandchild, of a spouse or an unmarried partner."),
    ("emergency_exception", "Kui vanemate"): ("§ 120 (3)", PKS_120_3),
    ("es_42_1", "... ning"): ("§ 42 (1)", "... and to the requirements for construction works and for building work."),
    ("es_42_1", "Ehitusluba antakse, kui esitatud ehitusprojekt vastab õigusaktides sätestatud nõuetele, eelkõige"): ("§ 42 (1)", EHS_42_1),
    ("es_42_1", "Ehitusluba antakse, kui esitatud ehitusprojekt vastab õigusaktides sätestatud nõuetele ..."): ("§ 42 (1) (requirements established in legislation)", "The building permit is issued if the building design documentation that has been filed conforms to the requirements established in legislation ..."),
    ("es_44_1", "... kavandatav"): ("§ 44 1)", "... the envisaged construction work does not conform to the detailed spatial plan, design specifications, ... the requirements established for construction works or for building work, or other public-law restrictions;"),
    ("es_44_2", "... ehitusprojekti"): ("§ 44 2)", "... the building design documentation has not been created by a competent person or an expert assessment by a competent person has not been performed in respect of the building design documentation;"),
    ("es_44_3", "... ehitusprojekt"): ("§ 44 3)", "... the building design documentation does not take into account the results of the site investigations conducted at the site of the construction work to be built or the required site investigations have not been performed;"),
    ("iks_4", "Isikuandmeid võib andmesubjekti nõusolekuta töödelda ajakirjanduslikul eesmärgil ..."): ("§ 4 (implicit consent baseline)", "Personal data may be processed and disclosed in the media for journalistic purposes without the consent of the data subject ..."),
    ("iks_4", "Isikuandmeid võib andmesubjekti nõusolekuta töödelda ajakirjanduslikul eesmärgil, eelkõige"): (None, IKS_4_S1),  # title set below per old title
    ("iks_4_harm", "Isikuandmete avalikustamine"): ("§ 4, second sentence", IKS_4_S2),
    ("joint_consent", "Vanemad"): ("§ 118 (1) and § 120 (1)", PKS_118_1_120_1),
    ("mms_11_1", "Kohaliku omavalitsuse üksuse volikogu võib määrusega kehtestada ..."): ("§ 11 (1)", "The municipal council may establish by a regulation ... a tax incentive ... on the land under the home ..."),
    ("mms_11_1", "Kohaliku omavalitsuse üksuse volikogu võib määrusega kehtestada käesoleva"): ("§ 11 (1)", MMS_11_1),
    ("mms_11_1_1", "... kui sellel"): ("§ 11 (1¹)", "... in case the building on this land is the residence of the land owner or user according to the residence data entered in the population register."),
    ("mms_11_1_1", "Kodualuse maana käsitatakse maa omaniku omandis olevat ... maad ..."): ("§ 11 (1¹)", "The land under the home is considered to be land owned by the land owner ..."),
    ("mms_11_1_1", "Kodualuse maana käsitatakse maa omaniku omandis olevat ... maad, mille"): ("§ 11 (1¹)", "The land under the home is considered to be land owned by the land owner ... the intended purpose or one of the intended purposes of which is residential land ..."),
    ("mms_11_5_1", "... täiendava"): ("§ 11 (5) 1)", "... an additional tax incentive of up to 1,000 euros to the following target groups: 1) pension recipients based on the State Pension Insurance Act;"),
    ("mms_11_5_1", "Kohaliku"): ("§ 11 (5) 1)", "The municipal council may determine ... an additional tax incentive ... 1) pension recipients based on the State Pension Insurance Act;"),
    ("mms_11_7", "Täiendava"): ("§ 11 (7)", MMS_11_7),
    ("representation_parent", "Hooldusõiguslik"): ("§ 120 (1)", PKS_120_1),
    ("single_action_authority", "Vanem esindab"): ("§ 120 (2)", PKS_120_2),
    ("vos_53_4", "Käesoleva"): ("§ 53 (4)", "The right of withdrawal provided for in subsection 1 of § 56 of this Act shall not apply to contracts the object of which is: ..."),
    ("vos_56_1", "... 14"): ("§ 56 (1)", "... within 14 days ..."),
    ("vos_56_1", "... sidevahendi"): ("§ 56 (1)", "... withdraw from a distance contract ..."),
    ("vos_56_1", "Tarbija"): ("§ 56 (1)", VOS_56_1),
    ("vos_56_21", "Loetakse"): ("§ 56 (2¹)", VOS_56_21),
}
IKS_TITLES = {
    "§ 4 Isikuandmete töötlemine ajakirjanduslikul eesmärgil": "§ 4 Processing of personal data for journalistic purposes",
    "§ 4, esimene lause": "§ 4, first sentence",
}

def fix_anchor(a):
    for (cid, prefix), (title, quote) in ANCHORS.items():
        if a["clause_id"] == cid and a["quote"].startswith(prefix):
            # longest-prefix wins: iterate and keep the longest matching prefix
            pass
    cands = [(len(prefix), title, quote) for (cid, prefix), (title, quote) in ANCHORS.items()
             if a["clause_id"] == cid and a["quote"].startswith(prefix)]
    if not cands:
        raise SystemExit(f"unmapped anchor {a['clause_id']}: {a['quote'][:60]}")
    _, title, quote = max(cands)
    a["quote"] = quote
    a["clause_title"] = title if title is not None else IKS_TITLES[a["clause_title"]]
    return a

# free-text substitutions for labels / definitions / notes
SUBS = [
    (r"§ (\d+) lg (\d+)\^(\d)", lambda m: f"§ {m.group(1)} ({m.group(2)}{'¹²³'[int(m.group(3))-1]})"),
    (r"§ (\d+) lg (\d+) p (\d+)", r"§ \1 (\2) \3)"),
    (r"§ (\d+) lg (\d+)", r"§ \1 (\2)"),
    (r"§ (\d+) p (\d+)", r"§ \1 \2)"),
    (r"§ 4 lause 1", "§ 4, first sentence"),
    (r"§ 4 lause 2", "§ 4, second sentence"),
    (r" \(täielik teovõime\)", ""),
    (r"Land's intended use is residential \(elamumaa\)", "Intended purpose of the land is residential land"),
    (r"The cadastre records the land's intended use as residential\.", "The cadastre records the intended purpose (or one of the intended purposes) of the land as residential land."),
    (r"Site construction study has been provided", "Required site investigations have been performed"),
    (r"The building registry contains a valid site construction study \(ehitusuuring\)\.", "The building register records that the building design documentation takes into account the results of the required site investigations."),
    (r"State-fee obligation falls under 'õigusaktides sätestatud nõuded'\.", "State-fee obligation falls under the 'requirements established in legislation'."),
    (r"Consent baseline under IKS\.", "Consent baseline under the Personal Data Protection Act."),
    (r"Applicant has full legal capacity", "Applicant has active legal capacity"),
    (r"The applicant has full active legal capacity\.", "The applicant has active legal capacity."),
    (r"Publication would excessively harm the subject", "Disclosure would cause excessive damage to the data subject's rights"),
    (r"Editorial risk assessment concludes publication would excessively harm the subject's rights\.",
     "Editorial risk assessment concludes that disclosure would cause excessive damage to the data subject's rights (§ 4, second sentence)."),
    (r"Applicant is an EU member-state citizen", "Applicant is a citizen of another EU Member State"),
    (r"The applicant holds citizenship of an EU member state per the population registry\.",
     "The applicant holds citizenship of a Member State of the European Union other than Estonia per the population register (the § 14 (2) alternative to Estonian citizenship; exclusive of ee_citizen)."),
    (r"detail plan", "detailed spatial plan"),
    (r"detailed plan", "detailed spatial plan"),
    (r"detailed spatial plan or equivalent planning instrument", "detailed spatial plan or equivalent planning instrument"),
]

def fix_text(s):
    for pat, rep in SUBS:
        s = re.sub(pat, rep, s)
    return s

changed = 0
for f in sorted(glob.glob(f"{ROOT}/data/statutes/*/oracle/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    for it in d.get("terms", []) + d.get("rules", []) + d.get("outcomes", []):
        for k in ("label", "definition", "notes"):
            if k in it and it[k]:
                it[k] = fix_text(it[k])
        for a in it.get("anchors", []) + it.get("law_references", []):
            fix_anchor(a)
            a["note"] = fix_text(a.get("note", ""))
    d["provenance"]["notes"] = (d["provenance"].get("notes") or "").rstrip() + " Translated to English 2026-09-05 (anchor quotes from the official Riigi Teataja translation; clause_id values unchanged)."
    json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(f, "a", encoding="utf-8").write("\n")
    changed += 1
print("files rewritten:", changed)
