# Faithful-inputs audit (Ruling A) — 2026-09-05

Question: for each of the 47 scenarios, does the request text (`utterance_file`)
say exactly what the oracle `utterance_term` / `term_claim` files say the
applicant says? Before this audit 47 scenarios shared 19 files; the register
variants read the base `request_allow.txt` while their oracles were trimmed to
what the solver should get from the user, and several value variants shared a
file whose text contradicted their oracle. Extraction metrics (term P/R/F1,
claim accuracy, spurious count) therefore mixed model error with authoring
convention (see ES `phd3-jurix-remaining-cells-2026-09-05.md` §2).

**Principle.** The oracle claim set is the specification of the intended
mechanism; the utterance is rewritten to match it. No oracle file, gold
(`oracle/premise_outcome`) or register data was changed. Each rewritten
scenario now has its own file `sources/utterances/<scenario_id>.txt`; files
that no scenario referenced any more were removed. Voice, register and length
follow the 2026-09-01 files. (That morning's texts still carried Estonian legal
terms inline; the same evening's "Ruling E — English only" pass replaced them with
the official translation's terminology — the quotes below are the current wording.)
Rewritten scenarios carry the tag `utterance-rewritten-20260905` and a `notes`
entry. Applied by a one-off script, retired to git history after use (commit
`e2d00f4`, `tools/author_faithful_inputs_20260905.py`).

Classes:

- **FAITHFUL** — every oracle claim is stated or clearly implied by the text and the text asserts nothing the oracle omits. Unchanged.
- **TRIMMED** — the text asserted terms the oracle leaves out (register variants). Rewritten so the applicant states only what the oracle says they state.
- **CONTRADICTS** — at least one oracle claim contradicts the text. The offending sentence(s) rewritten so the applicant asserts the oracle value.
- **UNDERSTATED** — the oracle claims terms the text never mentions (no contradiction, no surplus). One clause added so the applicant states them. (Not in the plan's three-way split; kept separate so the plan's "13 claim/fact-conflict" and "17 trimmed" sets stay recognisable.)

Counts: FAITHFUL 14, TRIMMED 18, CONTRADICTS 9, UNDERSTATED 6 → **33 of 47
scenarios have new input text**, in 6 cases.

## Per scenario

| scenario (new id) | class | what changed | old file → new file |
|---|---|---|---|
| `building_permit_grant/allow_claims_verified` | FAITHFUL | six § 42 (1) terms asserted, all in oracle | `request_allow.txt` (kept) |
| `building_permit_grant/allow_register_only` | TRIMMED | oracle has no claims; text asserted all six terms → bare request ("please check whether the building permit can be issued") | `request_allow.txt` → `allow_register_only.txt` |
| `building_permit_grant/deny_own_admission_plan_violation` | UNDERSTATED | oracle also claims `building_requirements_met`, `site_study_provided` = true; added "meets the requirements for construction works and building work, the site investigations have been performed" | `request_deny.txt` → `deny_own_admission_plan_violation.txt` |
| `building_permit_grant/deny_no_allow_path_designer_not_competent` | CONTRADICTS | text said plan violation + competent person; oracle: `plan_conformant`=t, `plan_violation`=f, `competent_designer`=f → allow text with "the building design documentation was prepared by a relative who is not a competent person" | `request_deny.txt` → `deny_no_allow_path_designer_not_competent.txt` |
| `building_permit_grant/deny_no_allow_path_no_site_study` | CONTRADICTS | text said plan violation; oracle: plan conforms, `site_study_provided`=f → "no site investigations have been carried out yet" | `request_deny.txt` → `deny_no_allow_path_no_site_study.txt` |
| `building_permit_grant/need_register_silent_fee` | TRIMMED | oracle has no claims → bare request | `request_allow.txt` → `need_register_silent_fee.txt` |
| `building_permit_grant/unverifiable_register_down_payment_ledger` | TRIMMED | oracle has no claims → bare request | `request_allow.txt` → `unverifiable_register_down_payment_ledger.txt` |
| `building_permit_grant/unverifiable_trust_only_designer_selfreport` | TRIMMED | oracle has no claims → bare request | `request_allow.txt` → `unverifiable_trust_only_designer_selfreport.txt` |
| `civil_service_admission/allow_claims_verified` | FAITHFUL | all seven oracle claims stated (`eu_citizen`=f read as implied by "Estonian citizen" under the catalog's exclusive reading — see caveat) | `request_allow.txt` (kept) |
| `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` | CONTRADICTS | text said "Estonian citizen"; oracle `ee_citizen`=f, `eu_citizen`=t → "not an Estonian citizen but a citizen of Finland, an EU member state" | `request_allow.txt` → `allow_alt_rule_eu_citizen_overrides_register.txt` |
| `civil_service_admission/deny_own_admission_conviction` | UNDERSTATED | oracle also claims education, language, capacity, no-conflict = true; those clauses added around the conviction admission | `request_deny.txt` → `deny_own_admission_conviction.txt` |
| `civil_service_admission/deny_no_allow_path_no_citizenship` | CONTRADICTS | text said Estonian citizen with a conviction; oracle: `ee_citizen`=f, `eu_citizen`=f, `criminal_conviction`=f → "citizen of Georgia - neither an Estonian citizen nor a citizen of an EU member state", no conviction | `request_deny.txt` → `deny_no_allow_path_no_citizenship.txt` |
| `civil_service_admission/need_register_silent_citizenship` | TRIMMED | oracle claims only `no_conflict_declared`=t → request + conflict declaration only | `request_allow.txt` → `need_register_silent_citizenship.txt` |
| `civil_service_admission/unverifiable_register_down_population_registry` | TRIMMED | same as above | `request_allow.txt` → `unverifiable_register_down_population_registry.txt` |
| `civil_service_admission/unverifiable_trust_only_applicant_selfreport` | TRIMMED | same as above | `request_allow.txt` → `unverifiable_trust_only_applicant_selfreport.txt` |
| `civil_service_admission/need_user_silent_conflict_declaration` | FAITHFUL | six claims stated, conflict declaration silent (same `eu_citizen` caveat) | `request_allow_conflict_silent.txt` (kept) |
| `consumer_purchase_withdrawal/allow_claims_verified` | FAITHFUL | all five claims stated | `request_allow.txt` (kept) |
| `consumer_purchase_withdrawal/allow_register_only_consumer_status` | TRIMMED | oracle claims only `within_14_days`, `notice_sent_in_time` → "I want to withdraw from a purchase ... the 14-day withdrawal period is still running ... sent the withdrawal notice" (no consumer / distance / catalogue wording) | `request_allow.txt` → `allow_register_only_consumer_status.txt` |
| `consumer_purchase_withdrawal/deny_own_admission_custom_goods` | UNDERSTATED | oracle also claims `notice_sent_in_time`=t and `distance_contract`=t; added "the contract was concluded at a distance" and "I sent the withdrawal notice to the seller yesterday" | `request_deny.txt` → `deny_own_admission_custom_goods.txt` |
| `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` | CONTRADICTS | text said made to order + "I am a consumer"; oracle `is_consumer`=f, `excluded_category`=f → standard catalogue chair bought for the company, "as a trader and not as a consumer" | `request_deny.txt` → `deny_no_allow_path_not_consumer.txt` |
| `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` | FAITHFUL | consumer, distance, standard goods stated; deadline and notice explicitly unsure | `request_need_user.txt` (kept) |
| `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` | TRIMMED | as `allow_register_only_consumer_status` | `request_allow.txt` → `unverifiable_register_down_trader_crm.txt` |
| `consumer_purchase_withdrawal/need_register_silent_consumer_status` | TRIMMED | as above | `request_allow.txt` → `need_register_silent_consumer_status.txt` |
| `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` | TRIMMED | as above | `request_allow.txt` → `unverifiable_trust_only_trader_selfreport.txt` |
| `land_tax_home_exemption/allow_claims_verified` | FAITHFUL | all six claims stated | `request_allow.txt` (kept) |
| `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` | FAITHFUL | identical inputs to `allow_claims_verified` (tag `extra`) | `request_allow.txt` (kept) |
| `land_tax_home_exemption/allow_register_only_ownership_and_residence` | TRIMMED | oracle claims only `municipality_exemption_set`, `application_submitted` → those two sentences only | `request_allow.txt` → `allow_register_only_ownership_and_residence.txt` |
| `land_tax_home_exemption/deny_own_admission_not_owner` | UNDERSTATED | oracle also claims `receives_pension`=t, `municipality_exemption_set`=t, `application_submitted`=f; added "I am a pensioner", "the municipal council has set the home-land exemption, but I have not submitted any application" | `request_deny.txt` → `deny_own_admission_not_owner.txt` |
| `land_tax_home_exemption/deny_no_allow_path_not_residential` | CONTRADICTS | text said not owner, residence elsewhere, parcel is residential land; oracle: owner, residence there, `residential_land`=f → "intended purpose of the land as profit-yielding land, not residential land" | `request_deny.txt` → `deny_no_allow_path_not_residential.txt` |
| `land_tax_home_exemption/need_register_silent_municipality_exemption` | TRIMMED | oracle claims only `application_submitted`=t; text asserted pension/owner/residential/residence too → "I have submitted the application ... but I do not know whether the municipal council has set the incentive" | `request_need_db.txt` → `need_register_silent_municipality_exemption.txt` |
| `land_tax_home_exemption/unverifiable_register_down_population_registry` | TRIMMED | oracle claims only `application_submitted`=t | `request_allow.txt` → `unverifiable_register_down_population_registry.txt` |
| `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` | CONTRADICTS | oracle's only claim is `application_submitted`=**false**; text said submitted (and asserted five more terms) → "I have not yet submitted an application" | `request_allow.txt` → `unverifiable_trust_only_applicant_selfreport.txt` |
| `journalistic_data_disclosure/allow_claims_verified` | FAITHFUL | purpose, public interest, ethics, no consent stated; "proportionate" read as `excessive_harm`=f | `request_allow.txt` (kept) |
| `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` | CONTRADICTS | oracle: purpose=f, public_interest=f, ethics=f, consent=**t**, harm=f — the text said the opposite of all four → sponsored feature, no public interest, not under the ethics code, explicit written consent, no harm | `request_allow.txt` → `allow_alt_rule_consent_overrides_register.txt` |
| `journalistic_data_disclosure/deny_own_admission_excessive_harm` | UNDERSTATED | oracle also claims `journalism_ethics`=t; added "the reporting follows the principles of journalism ethics" | `request_deny.txt` → `deny_own_admission_excessive_harm.txt` |
| `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` | CONTRADICTS | text said journalistic purpose + excessive harm; oracle: purpose=f, harm=f, public_interest=t, ethics=t → "commercial advertorial rather than journalistic processing ... would not cause excessive damage" | `request_deny.txt` → `deny_no_allow_path_no_purpose_no_consent.txt` |
| `journalistic_data_disclosure/need_user_silent_editorial_judgements` | TRIMMED | "but the reporting is proportionate" asserted `excessive_harm`=f, which the oracle omits; clause dropped | `request_allow_confirmations_silent.txt` → `need_user_silent_editorial_judgements.txt` |
| `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` | TRIMMED | oracle claims public_interest, ethics, harm=f only (purpose and consent left to registers) → text no longer asserts purpose or consent | `request_allow.txt` → `unverifiable_register_down_editorial_cms.txt` |
| `journalistic_data_disclosure/need_register_silent_purpose_and_consent` | TRIMMED | same as above | `request_allow.txt` → `need_register_silent_purpose_and_consent.txt` |
| `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` | TRIMMED | same as above | `request_allow.txt` → `unverifiable_trust_only_editorial_selfreport.txt` |
| `child_representation_by_one_parent/allow_claims_verified_emergency` | FAITHFUL | mother, hospital emergency, other parent unreachable | `request_allow.txt` (kept) |
| `child_representation_by_one_parent/deny_own_admission_not_parent` | FAITHFUL | aunt, no delegation, no written consent | `request_deny.txt` (kept) |
| `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` | FAITHFUL | no claims; emergency mentioned as unknown | `request_register_then_user.txt` (kept; file renamed from its v1 name on 2026-09-05) |
| `child_representation_by_one_parent/need_user_silent_emergency_bare_request` | FAITHFUL | bare request, no claims | `request_need_db.txt` (kept) |
| `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` | UNDERSTATED | oracle also claims `one_parent_unreachable`=f; added "The other parent is reachable." | `request_need_user.txt` → `need_user_silent_emergency_all_else_claimed.txt` |
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` | FAITHFUL | duplicate of the allow scenario | `request_allow.txt` (kept) |
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` | FAITHFUL | duplicate of the allow scenario | `request_allow.txt` (kept) |

Removed (no longer referenced): `building_permit_grant/request_deny.txt`,
`civil_service_admission/request_deny.txt`, `consumer_purchase_withdrawal/request_deny.txt`,
`land_tax_home_exemption/{request_deny,request_need_db}.txt`,
`journalistic_data_disclosure/{request_deny,request_allow_confirmations_silent}.txt`,
`child_representation_by_one_parent/request_need_user.txt`. Their text survives in
git history (`0d28213`) and inside the pre-rename transcripts.

## Caveats found on the way (not fixed here; oracle/catalog questions)

- `civil_service_admission`: the catalog treats `ee_citizen` and `eu_citizen`
  as exclusive (`eu_citizen` = citizen of *another* EU state for the § 14 (2)
  path), so the oracles claim `eu_citizen`=false for an Estonian citizen. A
  model reading "Estonian citizen" may reasonably answer `eu_citizen`=true or
  unknown. Either rename/redefine the term (`other_eu_citizen`) or accept the
  claim-accuracy hit; a term-definition change is out of scope for this pass.
- `journalistic_data_disclosure/allow_claims_verified`: `excessive_harm`=false
  rests on "the reporting is proportionate"; acceptable as implied, but a
  model may leave it unknown.
- The scored outcome of every scenario is unaffected by this audit: gold and
  oracle claims are unchanged, and `solver-validation` (oracle claims in, z3
  decides) still reproduces all 47 (pytest). Only conditions that *read the
  utterance* see different inputs — see the re-run list below.

## Scenarios whose inputs changed (drives the re-run)

33 scenarios; every LLM cell that reads the utterance must be re-run for them
(in practice: re-run the whole grid, the per-scenario subset is not a CLI option).

```
building_permit_grant/allow_register_only
building_permit_grant/deny_own_admission_plan_violation
building_permit_grant/deny_no_allow_path_designer_not_competent
building_permit_grant/deny_no_allow_path_no_site_study
building_permit_grant/need_register_silent_fee
building_permit_grant/unverifiable_register_down_payment_ledger
building_permit_grant/unverifiable_trust_only_designer_selfreport
civil_service_admission/allow_alt_rule_eu_citizen_overrides_register
civil_service_admission/deny_own_admission_conviction
civil_service_admission/deny_no_allow_path_no_citizenship
civil_service_admission/need_register_silent_citizenship
civil_service_admission/unverifiable_register_down_population_registry
civil_service_admission/unverifiable_trust_only_applicant_selfreport
consumer_purchase_withdrawal/allow_register_only_consumer_status
consumer_purchase_withdrawal/deny_own_admission_custom_goods
consumer_purchase_withdrawal/deny_no_allow_path_not_consumer
consumer_purchase_withdrawal/unverifiable_register_down_trader_crm
consumer_purchase_withdrawal/need_register_silent_consumer_status
consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport
land_tax_home_exemption/allow_register_only_ownership_and_residence
land_tax_home_exemption/deny_own_admission_not_owner
land_tax_home_exemption/deny_no_allow_path_not_residential
land_tax_home_exemption/need_register_silent_municipality_exemption
land_tax_home_exemption/unverifiable_register_down_population_registry
land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport
journalistic_data_disclosure/allow_alt_rule_consent_overrides_register
journalistic_data_disclosure/deny_own_admission_excessive_harm
journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent
journalistic_data_disclosure/need_user_silent_editorial_judgements
journalistic_data_disclosure/unverifiable_register_down_editorial_cms
journalistic_data_disclosure/need_register_silent_purpose_and_consent
journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport
child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed
```

Unchanged (14): `building_permit_grant/allow_claims_verified`,
`civil_service_admission/{allow_claims_verified,need_user_silent_conflict_declaration}`,
`consumer_purchase_withdrawal/{allow_claims_verified,need_user_silent_deadline_and_notice}`,
`land_tax_home_exemption/{allow_claims_verified,allow_claims_verified_pensioner_supplement}`,
`journalistic_data_disclosure/allow_claims_verified`,
`child_representation_by_one_parent/{allow_claims_verified_emergency,deny_own_admission_not_parent,need_user_silent_emergency_after_register_lookup,need_user_silent_emergency_bare_request,allow_claims_verified_duplicate_probe_a,allow_claims_verified_duplicate_probe_b}`.
