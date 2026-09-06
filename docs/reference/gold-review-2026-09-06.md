# Gold review — 2026-09-06 (per-case balance: 3 ALLOW / 3 DENY / 3 NEED_MORE_INFO in every case)

Operator hand-verification sheet for the suite change of 2026-09-06 (operator ruling 13:45:
the 18/18/18 total of 2026-09-05 must hold **per case** — nine scenarios per case, 54 in all).
Everything below was regenerated from the data files by a script, then annotated. The solver
column is the z3 result on oracle claims + oracle facts (the `solver-validation` condition);
the oracle `term_fact` of every scenario was also re-derived from the live register lookup
and compared. Full run: `experiments/20260906-solver-validation/results/summary.md` — 54/54,
macro F1 1.000. Predecessor sheet: `docs/reference/gold-review-2026-09-05.md`
(the twelve scenarios authored that day; three of them are dropped here).

Sections: 1. class table before → after · 2. every scenario per case (hand-verify column;
**NEW** and **DROPPED** rows marked) · 3. the six authored scenarios in detail · 4. the six
dropped scenarios · 5. other edits made on the way.

Reading the anchor column: the provision(s) the solver's path turns on — the fired rule's
clause for ALLOW / entailed DENY, the denied antecedent's anchor for a default DENY, the
open term's anchor for NEED. `<act_slug>/<eId>` as in `docs/reference/legislation-corpus.md`.

## 1. Class table (scored three-way), before → after

| case | ALLOW | DENY | NEED_MORE_INFO | total |
|---|---|---|---|---|
| `building_permit_grant` | 2 → **3** | 5 → **3** | 3 → **3** | 10 → **9** |
| `child_representation_by_one_parent` | 4 → **3** | 1 → **3** | 1 → **3** | 6 → **9** |
| `civil_service_admission` | 3 → **3** | 3 → **3** | 3 → **3** | 9 → **9** |
| `consumer_purchase_withdrawal` | 2 → **3** | 3 → **3** | 4 → **3** | 9 → **9** |
| `journalistic_data_disclosure` | 4 → **3** | 3 → **3** | 4 → **3** | 11 → **9** |
| `land_tax_home_exemption` | 3 → **3** | 3 → **3** | 3 → **3** | 9 → **9** |
| **total** | 18 → **18** | 18 → **18** | 18 → **18** | 54 → **54** |

NEED_MORE_INFO pools NEED_REGISTER_INFO, NEED_USER_INFO and UNVERIFIABLE_CLAIM (fine states kept
in the oracle and shown below). Six scenarios dropped, six authored; the total and the 18/18/18
ruling are unchanged.

Mechanism spread after the change (`scenario.mechanism`): ALLOW — `claims_verified` 7,
`register_only` 8, `alt_rule_claim_overrides_register` 3; DENY — `own_admission` 6,
`no_allow_path` 10, `register_only` 2; NEED — `register_silent` 5, `register_down` 5,
`trust_only` 5, `user_silent` 3. No mechanism left the suite.

## 2. Every scenario, per case

Columns: ☐ hand-verify · status (**NEW** = authored 2026-09-06; blank = unchanged from the
2026-09-05 sheet) · id · gold (fine state → scored) · mechanism · decisive provision(s) ·
request text · solver check. Dropped rows follow each table in a separate list.

### `building_permit_grant`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_claims_verified` | ALLOW | `claims_verified` | `building_code/sec_42__subsec_1` | We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. A competent person prepared the building design documentation, the site investigations have been performed, and the state fee has been paid. The building register shows no planning violations. | ALLOW; fired allow_building_permit |
| ☐ |  | `allow_register_only` | ALLOW | `register_only` | `building_code/sec_42__subsec_1` | We submitted the building-permit application for our project. Please check whether the building permit can be issued. | ALLOW; fired allow_building_permit |
| ☐ | **NEW** | `allow_register_only_design_conformity` | ALLOW | `register_only` | `building_code/sec_42__subsec_1` | We submitted the building-permit application for our project and we have paid the state fee. Please check everything else against the registers and tell us whether the building permit can be issued. | ALLOW; fired allow_building_permit |
| ☐ |  | `deny_no_allow_path_designer_not_competent` | DENY | `no_allow_path` | `building_code/sec_44__subsec_1__point_2` | We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. The site investigations have been performed and the state fee has been paid. However, the building design documentation was prepared by a relative who is not a competent person. The building register shows no planning violations. | DENY; fired — |
| ☐ |  | `deny_own_admission_plan_violation` | DENY | `own_admission` | `building_code/sec_44__subsec_1__point_1` | The local planning authority has confirmed that the project does not conform to the detailed spatial plan - it exceeds the permitted building footprint and height. Although the project meets the requirements for construction works and building work, the site investigations have been performed, the state fee has been paid and a competent person designed it, the plan violation blocks the permit. | DENY; fired deny_plan_violation |
| ☐ |  | `deny_register_only_plan_nonconformity` | DENY | `register_only` | `building_code/sec_44__subsec_1__point_1` | We submitted the building-permit application for our project. Please check whether the building permit can be issued. | DENY; fired deny_plan_violation |
| ☐ |  | `need_register_silent_fee` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `building_code/sec_42__subsec_1` | We submitted the building-permit application for our project. Please check whether the building permit can be issued. | NEED_REGISTER_INFO; fired —; missing fee_paid:no_value |
| ☐ |  | `unverifiable_register_down_payment_ledger` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `building_code/sec_42__subsec_1` | We submitted the building-permit application for our project. Please check whether the building permit can be issued. | UNVERIFIABLE_CLAIM; fired —; missing fee_paid:no_register |
| ☐ |  | `unverifiable_trust_only_designer_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `building_code/sec_42__subsec_1` | We submitted the building-permit application for our project. Please check whether the building permit can be issued. | UNVERIFIABLE_CLAIM; fired allow_building_permit; missing building_requirements_met:no_value, competent_designer:unwarranted_only, fee_paid:unwarranted_only, plan_conformant:no_value, site_study_provided:no_value |

- **DROPPED** `deny_no_allow_path_no_site_study` — DENY, `no_allow_path`, `building_code/sec_44__subsec_1__point_3` — “We submitted the building-permit application. The project conforms to the detailed spatial plan and also meets the requirements for construction works and building work. A competent person prepared the building design documentation and the state fee has been paid, but no site investigations have been carried out yet. The building register shows no planning violations.” — *third `no_allow_path` on the one § 42 (1) rule; `designer_not_competent` (v1 lineage) kept*
- **DROPPED** `deny_no_allow_path_fee_unpaid` — DENY, `no_allow_path`, `building_code/sec_42__subsec_1` — “We submitted the building-permit application. The project conforms to the detailed spatial plan and meets the requirements for construction works and building work. A competent person prepared the building design documentation and the site investigations have been performed, but we have not yet paid the state fee. The building register shows no planning violations.” — *authored 2026-09-05 for the DENY total only; surplus once the case is 3/3/3*

### `child_representation_by_one_parent`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_alt_rule_delegated_right_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | `family_law_act/sec_120__subsec_2` | I am the child's mother. We have joint custody, but the court has granted me the power of decision in this matter under § 119 of the Family Law Act, so I may decide alone. | ALLOW; fired allow_delegated_right |
| ☐ |  | `allow_claims_verified_emergency` | ALLOW | `claims_verified` | `family_law_act/sec_120__subsec_3` | I am the child's mother. The child is in hospital and the doctor needs a quick decision. The other parent is unreachable and not answering the phone. | ALLOW; fired allow_emergency, block_consent_when_unreachable |
| ☐ |  | `allow_register_only_sole_custody` | ALLOW | `register_only` | `family_law_act/sec_120__subsec_2` | I need access to the child's data to make a decision on the child's behalf. Please check the registers and tell me whether I can act alone. | ALLOW; fired allow_sole_custody |
| ☐ | **NEW** | `deny_no_allow_path_joint_custody_no_basis` | DENY | `no_allow_path` | `family_law_act/sec_120__subsec_2`, `family_law_act/sec_120__subsec_3`, `family_law_act/sec_118__subsec_1` | I am the child's father. The child's mother and I have joint custody; no court has given me sole custody or transferred the power of decision to me. The matter is not urgent and the mother is reachable, but she does not agree and has not given her consent. Can I nevertheless decide alone? | DENY; fired — |
| ☐ |  | `deny_own_admission_not_parent` | DENY | `own_admission` | `family_law_act/sec_120__subsec_1` | I am the child's aunt. I do not have delegated authority and I do not have the parents' written consent. | DENY; fired deny_non_parent |
| ☐ | **NEW** | `deny_register_only_not_parent` | DENY | `register_only` | `family_law_act/sec_120__subsec_1` | I need to make a decision on the child's behalf and to see the child's data. Please check the registers and tell me whether I can do this alone. | DENY; fired deny_non_parent |
| ☐ | **NEW** | `need_register_silent_custody_record` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `family_law_act/sec_120__subsec_2` | I am the child's father and I need to act for the child alone in a routine matter. It is not urgent and the child's mother is reachable. Please check the custody register for whether I am entitled to act alone. | NEED_REGISTER_INFO; fired —; missing delegated_decision_right:no_value, sole_custody:no_value |
| ☐ |  | `need_user_silent_emergency_after_register_lookup` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `family_law_act/sec_120__subsec_3` | I need access to the child's data. I do not yet know whether this is an emergency. | NEED_USER_INFO; fired —; missing emergency:no_value |
| ☐ | **NEW** | `unverifiable_register_down_custody_registry` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `family_law_act/sec_120__subsec_2` | I am the child's mother and I want to act for the child alone in a routine matter. There is no emergency and the child's father is reachable. Please confirm against the custody register that I may act alone. | UNVERIFIABLE_CLAIM; fired —; missing delegated_decision_right:no_register, sole_custody:no_register |

- **DROPPED** `allow_alt_rule_sole_custody_overrides_register` — ALLOW, `alt_rule_claim_overrides_register`, `family_law_act/sec_120__subsec_2` — “I am the child's father and I have sole custody of the child by court order. I need to act on the child's behalf alone.” — *second `alt_rule` in the case; `sole_custody` still exercised by `allow_register_only_sole_custody`, the mechanism by the § 119 variant*

### `civil_service_admission`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_alt_rule_eu_citizen_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | `civil_service_act/sec_14__subsec_2` | I am not an Estonian citizen but a citizen of Finland, another EU Member State, with a completed secondary education, and I am proficient in Estonian to the extent required by law. I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency. | ALLOW; fired allow_eu_citizen |
| ☐ |  | `allow_claims_verified` | ALLOW | `claims_verified` | `civil_service_act/sec_14__subsec_1` | I am an Estonian citizen with a completed secondary education and I am proficient in Estonian to the extent required by law. I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency. | ALLOW; fired allow_ee_citizen |
| ☐ |  | `allow_register_only_citizenship` | ALLOW | `register_only` | `civil_service_act/sec_14__subsec_1` | I am applying for a civil-service position; please check my eligibility against the registers. I confirm I have no family conflict with any supervising official at the agency. | ALLOW; fired allow_ee_citizen |
| ☐ |  | `deny_no_allow_path_no_citizenship` | DENY | `no_allow_path` | `civil_service_act/sec_14__subsec_1`, `civil_service_act/sec_14__subsec_2` | I am applying for a civil-service position. I am a citizen of Georgia - neither an Estonian citizen nor a citizen of an EU Member State - with a completed secondary education, I am proficient in Estonian to the extent required by law and I have active legal capacity. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency. | DENY; fired — |
| ☐ |  | `deny_no_allow_path_no_estonian_language` | DENY | `no_allow_path` | `civil_service_act/sec_14__subsec_1`, `civil_service_act/sec_14__subsec_2` | I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education and active legal capacity, but I do not yet speak Estonian at the level required by law. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency. | DENY; fired — |
| ☐ |  | `deny_own_admission_conviction` | DENY | `own_admission` | `civil_service_act/sec_14__subsec_1`, `civil_service_act/sec_15__subsec_1__point_1` | I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education, I am proficient in Estonian to the extent required by law and I have active legal capacity, but I was convicted of an intentional criminal offence two years ago and the conviction is still on record. I confirm I have no family conflict with any supervising official at the agency. | DENY; fired allow_ee_citizen, deny_conviction |
| ☐ |  | `need_register_silent_citizenship` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `civil_service_act/sec_14__subsec_1` | I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency. | NEED_REGISTER_INFO; fired —; missing ee_citizen:no_value |
| ☐ |  | `unverifiable_register_down_population_registry` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `civil_service_act/sec_14__subsec_1`, `civil_service_act/sec_14__subsec_2` | I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency. | UNVERIFIABLE_CLAIM; fired —; missing ee_citizen:no_register, eu_citizen:no_register, full_capacity:no_register |
| ☐ |  | `unverifiable_trust_only_applicant_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `civil_service_act/sec_14__subsec_1` | I am applying for a civil-service position. I confirm I have no family conflict with any supervising official at the agency. | UNVERIFIABLE_CLAIM; fired allow_ee_citizen; missing ee_citizen:unwarranted_only, eu_citizen:unwarranted_only, full_capacity:unwarranted_only, secondary_education:no_value, speaks_estonian:no_value |

### `consumer_purchase_withdrawal`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_claims_verified` | ALLOW | `claims_verified` | `law_of_obligations_act/sec_56__subsec_1` | I bought a laptop from an online shop 5 days ago and it is a standard catalogue model (not made to order). I am a private consumer, the contract was concluded at a distance, the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller yesterday. | ALLOW; fired allow_distance_withdrawal |
| ☐ | **NEW** | `allow_register_only_catalogue_clears_exclusion` | ALLOW | `register_only` | `law_of_obligations_act/sec_56__subsec_1` | I bought a pair of headphones from an online shop as a private consumer; the contract was concluded at a distance. I received them five days ago, so the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller this morning. Please check in your product catalogue whether anything prevents the withdrawal. | ALLOW; fired allow_distance_withdrawal |
| ☐ |  | `allow_register_only_consumer_status` | ALLOW | `register_only` | `law_of_obligations_act/sec_56__subsec_1` | I want to withdraw from a purchase I made 5 days ago. The 14-day withdrawal period is still running and I sent the withdrawal notice to the seller yesterday. | ALLOW; fired allow_distance_withdrawal |
| ☐ |  | `deny_no_allow_path_deadline_expired` | DENY | `no_allow_path` | `law_of_obligations_act/sec_56__subsec_1`, `law_of_obligations_act/sec_56__subsec_2_1` | I bought a standard catalogue laptop (not made to order) from an online shop as a private consumer; the contract was concluded at a distance. I received it six weeks ago, so the 14-day withdrawal period has already expired, and I only sent the withdrawal notice to the seller yesterday, after the period had run out. | DENY; fired — |
| ☐ |  | `deny_no_allow_path_not_consumer` | DENY | `no_allow_path` | `law_of_obligations_act/sec_56__subsec_1` | I ordered a standard catalogue office chair (not made to order) from an online shop for my company, and the invoice is in the company's name, so I am buying as a trader and not as a consumer. The contract was concluded at a distance, the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller yesterday. | DENY; fired — |
| ☐ |  | `deny_own_admission_custom_goods` | DENY | `own_admission` | `law_of_obligations_act/sec_56__subsec_1`, `law_of_obligations_act/sec_53__subsec_4` | I ordered a custom engraved piece of furniture made to my personal specifications from an online shop; the contract was concluded at a distance. The product catalogue flags it as made to order, so under § 53 (4) the right of withdrawal is excluded even though I am a consumer, the 14-day period has not expired and I sent the withdrawal notice to the seller yesterday. | DENY; fired allow_distance_withdrawal, deny_excluded_category |
| ☐ |  | `need_user_silent_deadline_and_notice` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `law_of_obligations_act/sec_56__subsec_2_1`, `law_of_obligations_act/sec_56__subsec_1` | I bought a standard catalogue laptop from an online shop and I am a consumer. The contract was concluded at a distance. I am not yet sure whether the 14-day withdrawal period is still running or whether I have sent a proper withdrawal notice - can the system decide based on what the trader knows? | NEED_USER_INFO; fired —; missing notice_sent_in_time:no_value, within_14_days:no_value |
| ☐ |  | `unverifiable_register_down_trader_crm` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `law_of_obligations_act/sec_56__subsec_1` | I want to withdraw from a purchase I made 5 days ago. The 14-day withdrawal period is still running and I sent the withdrawal notice to the seller yesterday. | UNVERIFIABLE_CLAIM; fired —; missing distance_contract:no_register, is_consumer:no_register |
| ☐ |  | `unverifiable_trust_only_trader_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `law_of_obligations_act/sec_56__subsec_1` | I want to withdraw from a purchase I made 5 days ago. The 14-day withdrawal period is still running and I sent the withdrawal notice to the seller yesterday. | UNVERIFIABLE_CLAIM; fired allow_distance_withdrawal; missing distance_contract:unwarranted_only, is_consumer:unwarranted_only |

- **DROPPED** `need_register_silent_consumer_status` — NEED_REGISTER_INFO, `register_silent`, `law_of_obligations_act/sec_56__subsec_1` — “I want to withdraw from a purchase I made 5 days ago. The 14-day withdrawal period is still running and I sent the withdrawal notice to the seller yesterday.” — *same claims and text as the kept `unverifiable_register_down_trader_crm` (same register, both terms); `register_silent` keeps five instances*

### `journalistic_data_disclosure`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_alt_rule_consent_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | `personal_data_protection_act/sec_4` | Our newsroom wants to publish personal data about a private individual. The processing is not journalistic in purpose - it is a sponsored lifestyle feature - there is no public interest in it and it was not prepared under the principles of journalism ethics. The data subject has, however, granted explicit written consent to the publication, and it would not cause excessive damage to their rights. | ALLOW; fired allow_consent_basis |
| ☐ |  | `allow_claims_verified` | ALLOW | `claims_verified` | `personal_data_protection_act/sec_4` | Our newsroom is preparing an investigative article. The processing is journalistic in purpose. The editor confirms there is public interest in the story and the reporting follows the principles of journalism ethics. The data subject has not granted a separate consent, and disclosure would not cause excessive damage to the subject's rights. | ALLOW; fired allow_journalism_basis |
| ☐ |  | `allow_register_only_purpose_from_cms` | ALLOW | `register_only` | `personal_data_protection_act/sec_4` | We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights. Please check the editorial system for the classification of the processing. | ALLOW; fired allow_journalism_basis |
| ☐ |  | `deny_no_allow_path_no_public_interest` | DENY | `no_allow_path` | `personal_data_protection_act/sec_4` | Our editor reviewed the story. The processing is journalistic in purpose and the reporting follows the principles of journalism ethics, but the editor finds no public interest in the private details it discloses. No consent from the subject is on record. The risk review concludes that publication would not cause excessive damage to the subject's rights. | DENY; fired — |
| ☐ |  | `deny_no_allow_path_no_purpose_no_consent` | DENY | `no_allow_path` | `personal_data_protection_act/sec_4` | Our editor reviewed the piece. It is a commercial advertorial rather than journalistic processing, although there is public interest in the topic and the text follows the principles of journalism ethics. No consent from the subject is on record. The newsroom risk review concludes that publication would not cause excessive damage to the subject's rights. | DENY; fired — |
| ☐ |  | `deny_own_admission_excessive_harm` | DENY | `own_admission` | `personal_data_protection_act/sec_4` | Our editor reviewed the story. The processing is journalistic in purpose, there is public interest and the reporting follows the principles of journalism ethics. No consent from the subject is on record. The newsroom risk review concludes that publication would cause excessive damage to the subject's private life and mental health. | DENY; fired allow_journalism_basis, block_ethics_when_excessive_harm |
| ☐ |  | `need_register_silent_purpose_and_consent` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `personal_data_protection_act/sec_4` | We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights. | NEED_REGISTER_INFO; fired —; missing journalistic_purpose:no_value, subject_consent:no_value |
| ☐ |  | `need_user_silent_editorial_judgements` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `personal_data_protection_act/sec_4` | Our newsroom is preparing an investigative article. The processing is journalistic in purpose. The data subject has not granted a separate consent. | NEED_USER_INFO; fired —; missing journalism_ethics:no_value, public_interest:no_value |
| ☐ |  | `unverifiable_trust_only_editorial_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `personal_data_protection_act/sec_4` | We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights. | UNVERIFIABLE_CLAIM; fired allow_journalism_basis; missing journalistic_purpose:unwarranted_only, subject_consent:unwarranted_only |

- **DROPPED** `allow_register_only_consent_from_register` — ALLOW, `register_only`, `personal_data_protection_act/sec_4` — “We want to publish personal data about an individual in an upcoming piece. Please check the registers for whether we may proceed.” — *second `register_only` ALLOW in the case; consent basis still exercised by `allow_alt_rule_consent_overrides_register`*
- **DROPPED** `unverifiable_register_down_editorial_cms` — UNVERIFIABLE_CLAIM, `register_down`, `personal_data_protection_act/sec_4` — “We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights.” — *same claims and text as the kept `need_register_silent_purpose_and_consent` (both registers); `register_down` keeps five instances*

### `land_tax_home_exemption`

| ☐ | status | scenario | gold | mechanism | anchor | request text | solver |
|---|---|---|---|---|---|---|---|
| ☐ |  | `allow_claims_verified` | ALLOW | `claims_verified` | `land_tax_act/sec_11__subsec_1`, `land_tax_act/sec_11__subsec_5__point_1` | I am a pensioner and the owner of the parcel in Tartu. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. The municipal council has set the home-land exemption and I have submitted the application for the supplementary pensioner exemption. | ALLOW; fired allow_home_land_exemption, allow_pensioner_supplement |
| ☐ |  | `allow_claims_verified_pensioner_supplement` | ALLOW | `claims_verified` | `land_tax_act/sec_11__subsec_1`, `land_tax_act/sec_11__subsec_5__point_1` | I am a pensioner and the owner of the parcel in Tartu. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. The municipal council has set the home-land exemption and I have submitted the application for the supplementary pensioner exemption. | ALLOW; fired allow_home_land_exemption, allow_pensioner_supplement |
| ☐ |  | `allow_register_only_ownership_and_residence` | ALLOW | `register_only` | `land_tax_act/sec_11__subsec_1`, `land_tax_act/sec_11__subsec_5__point_1` | I am applying for the home-land tax incentive for my parcel in Tartu. The municipal council has set the home-land exemption and I have submitted the application for the supplementary exemption. | ALLOW; fired allow_home_land_exemption, allow_pensioner_supplement |
| ☐ |  | `deny_no_allow_path_municipality_not_set` | DENY | `no_allow_path` | `land_tax_act/sec_11__subsec_1` | I am a pensioner and the owner of the parcel in a rural municipality. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. I have submitted the application for the supplementary pensioner exemption, but the municipal council has not set any home-land exemption for the coming tax period. | DENY; fired — |
| ☐ |  | `deny_no_allow_path_not_residential` | DENY | `no_allow_path` | `land_tax_act/sec_11__subsec_1_1` | I am a pensioner and the owner of the parcel in Tartu. The population register has my residence at that address, but the cadastre lists the intended purpose of the land as profit-yielding land, not residential land. The municipal council has set the home-land exemption and I have submitted the application for the supplementary pensioner exemption. | DENY; fired — |
| ☐ |  | `deny_own_admission_not_owner` | DENY | `own_admission` | `land_tax_act/sec_11__subsec_1_1`, `land_tax_act/sec_11__subsec_7` | I am a pensioner and I live in a rented apartment. I am not the owner of the land and my residence in the population register is elsewhere. The parcel is residential land owned by my neighbour. The municipal council has set the home-land exemption, but I have not submitted any application for the supplementary exemption. | DENY; fired — |
| ☐ |  | `need_register_silent_municipality_exemption` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `land_tax_act/sec_11__subsec_1` | I have submitted the application for the § 11 land tax incentive for my parcel in a rural municipality, but I do not know whether the municipal council has set the incentive yet. | NEED_REGISTER_INFO; fired —; missing municipality_exemption_set:no_value |
| ☐ |  | `unverifiable_register_down_population_registry` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `land_tax_act/sec_11__subsec_1_1` | I am applying for the home-land tax incentive for my parcel in Tartu and I have submitted the application for the supplementary exemption. | UNVERIFIABLE_CLAIM; fired —; missing primary_residence_registered:no_register |
| ☐ |  | `unverifiable_trust_only_applicant_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `land_tax_act/sec_11__subsec_1` | I am applying for the home-land tax incentive for my parcel in Tartu. I have not yet submitted an application for the supplementary exemption. | UNVERIFIABLE_CLAIM; fired allow_home_land_exemption; missing applicant_is_owner:unwarranted_only, municipality_exemption_set:unwarranted_only, primary_residence_registered:unwarranted_only, residential_land:unwarranted_only |

## 3. Authored scenarios (6)

Each block: request text → oracle claims → register overrides → facts the lookup produces → expected outcome → rule path (why the solver lands there, with the provision) → solver check. Request texts follow the faithful-inputs rules of 2026-09-05: every oracle claim is stated in the text, the text asserts no catalogue term the oracle omits, terminology from the official translation.

### 3.1 `building_permit_grant/allow_register_only_design_conformity`

- **Label:** Permit: fee paid claimed, design terms from registers  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Anchor:** `building_code/sec_42__subsec_1`
- **Request text:** “We submitted the building-permit application for our project and we have paid the state fee. Please check everything else against the registers and tell us whether the building permit can be issued.”
- **Oracle claims:** `fee_paid=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `building_requirements_met=true` (building_registry, authoritative), `competent_designer=true` (designer_registry, authoritative), `fee_paid=true` (payment_ledger, authoritative), `plan_conformant=true` (building_registry, authoritative), `plan_violation=false` (building_registry, authoritative), `site_study_provided=true` (building_registry, authoritative)
- **Rule path:** Only `fee_paid=true` is claimed (the applicant's own act). Stage 2 draws `plan_conformant`, `building_requirements_met`, `site_study_provided`, `plan_violation=false` from the building register and `competent_designer` from the designer register (all authoritative). `allow_building_permit` (§ 42 (1)) is entailed; `deny_plan_violation` (§ 44 1)) does not fire; the claimed `fee_paid` has an authoritative payment-ledger value, so nothing is flagged → **ALLOW**. Third ALLOW of the case: the Building Code has one allow rule, so no `alt_rule` variant exists; this is the mirror of `allow_register_only` (bare request) with the applicant supplying the one term only they would know first-hand.
- **Solver check:** ALLOW; fired = ['allow_building_permit']; missing = none; note: “ALLOW entailed.”

### 3.2 `child_representation_by_one_parent/deny_no_allow_path_joint_custody_no_basis`

- **Label:** Child: joint custody, no basis to act alone  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Anchor:** `family_law_act/sec_120__subsec_2`, `family_law_act/sec_120__subsec_3`, `family_law_act/sec_118__subsec_1`
- **Request text:** “I am the child's father. The child's mother and I have joint custody; no court has given me sole custody or transferred the power of decision to me. The matter is not urgent and the mother is reachable, but she does not agree and has not given her consent. Can I nevertheless decide alone?”
- **Oracle claims:** `applicant_is_not_parent=false`, `applicant_is_parent=true`, `both_parents_consent=false`, `delegated_decision_right=false`, `emergency=false`, `one_parent_unreachable=false`, `sole_custody=false`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative), `delegated_decision_right=false` (custody_registry, authoritative), `sole_custody=false` (custody_registry, authoritative)
- **Rule path:** Claims: `applicant_is_parent=true`, `applicant_is_not_parent=false`, `sole_custody=false`, `delegated_decision_right=false` (§ 120 (2) 1)–2) both denied), `emergency=false`, `one_parent_unreachable=false` (§ 120 (3) denied), `both_parents_consent=false` (§ 118 (1) / § 120 (1) joint representation not exercised). All four allow rules carry a false antecedent; `deny_non_parent` needs `applicant_is_not_parent=true` and does not fire; registers agree with every claim; nothing decision-relevant is open → default **DENY** (no applicable rules). Legally: a parent with joint custody has only a joint right of representation (§ 120 (1) second sentence); acting alone needs one of § 120 (2)–(3), none of which holds.
- **Solver check:** DENY; fired = none; missing = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 3.3 `child_representation_by_one_parent/deny_register_only_not_parent`

- **Label:** Child: bare request, population register shows non-parent  
- **Mechanism:** `register_only`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Anchor:** `family_law_act/sec_120__subsec_1`
- **Request text:** “I need to make a decision on the child's behalf and to see the child's data. Please check the registers and tell me whether I can do this alone.”
- **Oracle claims:** none (bare request)
- **Register overrides:** `{"child_representation_by_one_parent__population_registry": {"set": {"main": {"applicant_is_parent": false, "applicant_is_not_parent": true}}}}`
- **Facts (lookup):** `applicant_is_not_parent=true` (population_registry, authoritative), `applicant_is_parent=false` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative), `delegated_decision_right=false` (custody_registry, authoritative), `sole_custody=false` (custody_registry, authoritative)
- **Rule path:** No claims. Stage 2 draws `applicant_is_parent=false`, `applicant_is_not_parent=true` (population register, scenario override), `sole_custody=false`, `delegated_decision_right=false`, `both_parents_consent=false`. Every allow rule is blocked on `applicant_is_parent`; `deny_non_parent` (§ 120 (1): only a parent with legal custody is the child's legal representative) fires from the register fact → **DENY** entailed. This is the register-recorded deny ground that Ruling I (ADR 0006) made visible — the same shape as `building_permit_grant/deny_register_only_plan_nonconformity` after that ruling.
- **Solver check:** DENY; fired = ['deny_non_parent']; missing = none; note: “DENY entailed.”

### 3.4 `child_representation_by_one_parent/need_register_silent_custody_record`

- **Label:** Child: custody register silent on the basis to act alone  
- **Mechanism:** `register_silent`  
- **Gold:** NEED_REGISTER_INFO (scored NEED_MORE_INFO); missing terms: ['delegated_decision_right', 'sole_custody']
- **Anchor:** `family_law_act/sec_120__subsec_2`
- **Request text:** “I am the child's father and I need to act for the child alone in a routine matter. It is not urgent and the child's mother is reachable. Please check the custody register for whether I am entitled to act alone.”
- **Oracle claims:** `applicant_is_not_parent=false`, `applicant_is_parent=true`, `emergency=false`, `one_parent_unreachable=false`
- **Register overrides:** `{"child_representation_by_one_parent__custody_registry": {"remove": {"main": ["sole_custody", "delegated_decision_right"]}}}`
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative)
- **Rule path:** Claims: `applicant_is_parent=true`, `applicant_is_not_parent=false`, `emergency=false`, `one_parent_unreachable=false`. Stage 2: population register confirms parenthood; consent service gives `both_parents_consent=false`; the custody register is available but its record has neither field (override `remove`). `allow_emergency` and `allow_joint_consent` are blocked; `allow_sole_custody` and `allow_delegated_right` stay open on `sole_custody` and `delegated_decision_right`, both register-evidence terms covered by an available register with no value → **NEED_REGISTER_INFO** `{delegated_decision_right, sole_custody}` (reason `no_value`). Legally: whether the father may act alone turns on § 120 (2) 1)–2), which only the custody register can answer.
- **Solver check:** NEED_REGISTER_INFO; fired = none; missing = [('delegated_decision_right', 'no_value'), ('sole_custody', 'no_value')]; note: “Decision-relevant register terms have no warranted value.”

### 3.5 `child_representation_by_one_parent/unverifiable_register_down_custody_registry`

- **Label:** Child: custody register unavailable  
- **Mechanism:** `register_down`  
- **Gold:** UNVERIFIABLE_CLAIM (scored NEED_MORE_INFO); missing terms: ['delegated_decision_right', 'sole_custody']
- **Anchor:** `family_law_act/sec_120__subsec_2`
- **Request text:** “I am the child's mother and I want to act for the child alone in a routine matter. There is no emergency and the child's father is reachable. Please confirm against the custody register that I may act alone.”
- **Oracle claims:** `applicant_is_not_parent=false`, `applicant_is_parent=true`, `emergency=false`, `one_parent_unreachable=false`
- **Register overrides:** `{"child_representation_by_one_parent__custody_registry": {"availability": "unavailable"}}`
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative); unavailable: ['delegated_decision_right', 'sole_custody']
- **Rule path:** Same claims as `need_register_silent_custody_record`. The custody register is unavailable: its two mapped terms become `unavailable_terms`. Stage 2 fills parenthood (true) and consent (false); the two § 120 (2) allow rules stay open on `sole_custody` and `delegated_decision_right`, both `no_register` → **UNVERIFIABLE_CLAIM** (scored NEED_MORE_INFO), missing `{delegated_decision_right, sole_custody}`. Same shape as the other five `register_down` scenarios (open allow-path term, covering register down).
- **Solver check:** UNVERIFIABLE_CLAIM; fired = none; missing = [('delegated_decision_right', 'no_register'), ('sole_custody', 'no_register')]; note: “Decision-relevant register terms have no warranted value and the covering register is unavailable.”

### 3.6 `consumer_purchase_withdrawal/allow_register_only_catalogue_clears_exclusion`

- **Label:** Withdrawal: § 56 (1) claimed, catalogue clears § 53 (4)  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Anchor:** `law_of_obligations_act/sec_56__subsec_1`
- **Request text:** “I bought a pair of headphones from an online shop as a private consumer; the contract was concluded at a distance. I received them five days ago, so the 14-day withdrawal period is still running, and I sent the withdrawal notice to the seller this morning. Please check in your product catalogue whether anything prevents the withdrawal.”
- **Oracle claims:** `distance_contract=true`, `is_consumer=true`, `notice_sent_in_time=true`, `within_14_days=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `distance_contract=true` (trader_crm, authoritative), `excluded_category=false` (product_catalogue, authoritative), `is_consumer=true` (trader_crm, authoritative)
- **Rule path:** Claims: the four § 56 (1) antecedents (`is_consumer`, `distance_contract`, `within_14_days`, `notice_sent_in_time`), nothing about the goods. Stage 2 draws `excluded_category=false` from the product catalogue (§ 53 (4) deny ground; drawn for deny-rule antecedents since Ruling I) and confirms the two CRM terms. `allow_distance_withdrawal` is entailed, `deny_excluded_category` does not fire, the claimed register terms have authoritative values → **ALLOW**. Distinct from `allow_claims_verified` (applicant also asserts the goods are standard catalogue items) and `allow_register_only_consumer_status` (CRM supplies consumer/distance status).
- **Solver check:** ALLOW; fired = ['allow_distance_withdrawal']; missing = none; note: “ALLOW entailed.”

## 4. Dropped scenarios (6)

Drop rule: within a case, drop the surplus scenario whose mechanism the case still has
another instance of, preferring the one that duplicates another scenario's claim set or
term; never remove a mechanism from the suite; keep the paper's Figure 2/3 scenario
(`land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport`). Files removed:
scenario YAML, four oracle JSONs, request text (each used only by its scenario). Rows kept in
`docs/reference/id-aliases.md` ("Dropped 2026-09-06") and in every earlier experiment folder.

| id | gold | mechanism | why |
|---|---|---|---|
| `building_permit_grant/deny_no_allow_path_no_site_study` | DENY | `no_allow_path` | third `no_allow_path` on the one § 42 (1) rule; `designer_not_competent` (v1 lineage) kept |
| `building_permit_grant/deny_no_allow_path_fee_unpaid` | DENY | `no_allow_path` | authored 2026-09-05 for the DENY total only; surplus once the case is 3/3/3 |
| `child_representation_by_one_parent/allow_alt_rule_sole_custody_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | second `alt_rule` in the case; `sole_custody` still exercised by `allow_register_only_sole_custody`, the mechanism by the § 119 variant |
| `consumer_purchase_withdrawal/need_register_silent_consumer_status` | NEED_REGISTER_INFO | `register_silent` | same claims and text as the kept `unverifiable_register_down_trader_crm` (same register, both terms); `register_silent` keeps five instances |
| `journalistic_data_disclosure/allow_register_only_consent_from_register` | ALLOW | `register_only` | second `register_only` ALLOW in the case; consent basis still exercised by `allow_alt_rule_consent_overrides_register` |
| `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` | UNVERIFIABLE_CLAIM | `register_down` | same claims and text as the kept `need_register_silent_purpose_and_consent` (both registers); `register_down` keeps five instances |

## 5. Other edits made on the way

- `building_permit_grant/deny_register_only_plan_nonconformity`: the scenario description and
  the oracle note still described the pre-Ruling-I solver ("deny_plan_violation is not
  triggered from the register"). Since 2026-09-06 (ADR 0006) stage 2 draws facts for every
  rule's antecedents and the rule fires — the `20260906-solver-validation` notes already say
  so. Description and note updated; gold (DENY, no missing terms) unchanged. The new child
  scenario `deny_register_only_not_parent` is the second instance of that shape.
- `tests/test_conditions_and_prompts.py::test_resume_and_limit_continue_a_grid` counts the
  child case's scenarios (6 → 9).
- `tools/rename_map.yaml`: the three dropped scenarios that had a v1 id are removed from the
  `scenarios:` block (as on 2026-09-05); `docs/reference/id-aliases.md` keeps every row.
- No term or rule was added to any statute catalogue: every new scenario is built from the
  existing terms and rules of the Family Law Act, Building Code and Law of Obligations Act
  catalogues.
- Two of the six new request texts (`need_register_silent_custody_record`,
  `unverifiable_register_down_custody_registry`) carry the same claim set and differ in
  register state only — the same construction as the `register_silent` / `register_down` /
  `trust_only` triplets in the other five cases.

