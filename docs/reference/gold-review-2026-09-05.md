# Gold review — 2026-09-05 (English request texts, balanced 18/18/18)

Operator hand-verification sheet for the suite change of 2026-09-05 (execution brief
"Ruling E — English only" and "Ruling F — balanced gold"). Everything below was
regenerated from the data files by a script, then annotated; the solver check column
is the z3 result on oracle claims + oracle facts (the `solver-validation` condition).
Full run: `experiments/20260906-solver-validation/results/summary.md` — 54/54, macro F1 1.000.

Sections: 1. class table · 2. the twelve authored scenarios · 3. retired scenarios ·
4. request texts that changed (all 35 rewritten files, with the one material change flagged) ·
5. catalogue wording changes that touch gold reasoning.

## 1. Class table (scored three-way)


| case | ALLOW | DENY | NEED_MORE_INFO | total |
|---|---|---|---|---|
| `building_permit_grant` | 2 | 5 | 3 | 10 |
| `child_representation_by_one_parent` | 4 | 1 | 1 | 6 |
| `civil_service_admission` | 3 | 3 | 3 | 9 |
| `consumer_purchase_withdrawal` | 2 | 3 | 4 | 9 |
| `journalistic_data_disclosure` | 4 | 3 | 4 | 11 |
| `land_tax_home_exemption` | 3 | 3 | 3 | 9 |
| **total** | **18** | **18** | **18** | **54** |

NEED_MORE_INFO pools NEED_REGISTER_INFO, NEED_USER_INFO and UNVERIFIABLE_CLAIM (fine states kept in the oracle). Before: 47 = 14/12/21.

## 2. Authored scenarios (12)

Each block: request text → oracle claims → register overrides → facts the lookup produces → expected outcome → rule path (why the solver lands there) → solver check.

### 2.1 `building_permit_grant/deny_no_allow_path_fee_unpaid`

- **Label:** Permit: state fee unpaid, no allow path  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “We submitted the building-permit application. The project conforms to the detailed spatial plan and meets the requirements for construction works and building work. A competent person prepared the building design documentation and the site investigations have been performed, but we have not yet paid the state fee. The building register shows no planning violations.”
- **Oracle claims:** `building_requirements_met=true`, `competent_designer=true`, `fee_paid=false`, `plan_conformant=true`, `plan_violation=false`, `site_study_provided=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `building_requirements_met=true` (building_registry, authoritative), `competent_designer=true` (designer_registry, authoritative), `fee_paid=true` (payment_ledger, authoritative), `plan_conformant=true` (building_registry, authoritative), `plan_violation=false` (building_registry, authoritative), `site_study_provided=true` (building_registry, authoritative)
- **Rule path:** Claims set all § 42 (1) terms true except `fee_paid=false`; `plan_violation=false`. `allow_building_permit` is blocked on `fee_paid`; the deny rule does not fire. Nothing missing → **DENY** (no applicable rules). Different term from the existing `designer_not_competent` / `no_site_study` variants.
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 2.2 `building_permit_grant/deny_register_only_plan_nonconformity`

- **Label:** Permit: bare request, register shows plan non-conformity  
- **Mechanism:** `register_only`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “We submitted the building-permit application for our project. Please check whether the building permit can be issued.”
- **Oracle claims:** none (bare request)
- **Register overrides:** `{"building_permit_grant__building_registry": {"set": {"main": {"plan_violation": true, "plan_conformant": false}}}}`
- **Facts (lookup):** `building_requirements_met=true` (building_registry, authoritative), `competent_designer=true` (designer_registry, authoritative), `fee_paid=true` (payment_ledger, authoritative), `plan_conformant=false` (building_registry, authoritative), `plan_violation=true` (building_registry, authoritative), `site_study_provided=true` (building_registry, authoritative)
- **Rule path:** No claims. Stage 2 draws the five § 42 (1) terms; `plan_conformant=false` (building register, scenario override) closes the only allow path. The register also records `plan_violation=true`, but the solver draws register facts only for open allow-path terms, so `deny_plan_violation` is not triggered from the register. Nothing decision-relevant is missing → default **DENY** (no applicable rules). This is the one register-only DENY in the suite and documents a solver property worth the operator's attention (see the ES report).
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 2.3 `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register`

- **Label:** Child: parent claims § 119 power of decision  
- **Mechanism:** `alt_rule_claim_overrides_register`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “I am the child's mother. We have joint custody, but the court has granted me the power of decision in this matter under § 119 of the Family Law Act, so I may decide alone.”
- **Oracle claims:** `applicant_is_not_parent=false`, `applicant_is_parent=true`, `delegated_decision_right=true`, `sole_custody=false`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative), `delegated_decision_right=false` (custody_registry, authoritative), `sole_custody=false` (custody_registry, authoritative)
- **Rule path:** Claims: parent true, not-parent false, `sole_custody=false`, `delegated_decision_right=true`. `allow_delegated_right` (§ 120 (2) 2)) is entailed from claims; the custody register's `delegated_decision_right=false` is an authoritative value, so the warrant check has nothing unverified to flag. → **ALLOW**.
- **Solver check:** ALLOW; fired = ['allow_delegated_right']; note: “ALLOW entailed.”

### 2.4 `child_representation_by_one_parent/allow_alt_rule_sole_custody_overrides_register`

- **Label:** Child: parent claims sole custody, register says joint  
- **Mechanism:** `alt_rule_claim_overrides_register`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “I am the child's father and I have sole custody of the child by court order. I need to act on the child's behalf alone.”
- **Oracle claims:** `applicant_is_not_parent=false`, `applicant_is_parent=true`, `sole_custody=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative), `delegated_decision_right=false` (custody_registry, authoritative), `sole_custody=false` (custody_registry, authoritative)
- **Rule path:** Claims seed `applicant_is_parent=true`, `applicant_is_not_parent=false`, `sole_custody=true`. `allow_sole_custody` is entailed from claims alone. Warrant check: both antecedents are register-evidence terms covered by available registers; the population register confirms parenthood (authoritative, true); the custody register holds `sole_custody=false`, i.e. an authoritative value exists for the term, so it is not 'claim on a silent register' — the claim takes precedence (defeasible premises win at stage 1; facts only fill what is missing). → **ALLOW** via the alternative rule. Same shape as `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register`.
- **Solver check:** ALLOW; fired = ['allow_sole_custody']; note: “ALLOW entailed.”

### 2.5 `child_representation_by_one_parent/allow_register_only_sole_custody`

- **Label:** Child: bare request, custody register shows sole custody  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “I need access to the child's data to make a decision on the child's behalf. Please check the registers and tell me whether I can act alone.”
- **Oracle claims:** none (bare request)
- **Register overrides:** `{"child_representation_by_one_parent__custody_registry": {"set": {"main": {"sole_custody": true}}}}`
- **Facts (lookup):** `applicant_is_not_parent=false` (population_registry, authoritative), `applicant_is_parent=true` (population_registry, authoritative), `both_parents_consent=false` (consent_service, authoritative), `delegated_decision_right=false` (custody_registry, authoritative), `sole_custody=true` (custody_registry, authoritative)
- **Rule path:** No claims. Stage 1 leaves every allow path open on register terms; stage 2 draws `applicant_is_parent=true` (population register) and `sole_custody=true` (custody register, scenario override). `allow_sole_custody` (§ 120 (2) 1)) is entailed; both facts are authoritative, so no warrant flag → **ALLOW**.
- **Solver check:** ALLOW; fired = ['allow_sole_custody']; note: “ALLOW entailed.”

### 2.6 `civil_service_admission/allow_register_only_citizenship`

- **Label:** Admission: registers supply § 14 (1), conflict declared  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “I am applying for a civil-service position; please check my eligibility against the registers. I confirm I have no family conflict with any supervising official at the agency.”
- **Oracle claims:** `no_conflict_declared=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `criminal_conviction=false` (criminal_records_registry, authoritative), `ee_citizen=true` (population_registry, authoritative), `eu_citizen=false` (population_registry, authoritative), `full_capacity=true` (population_registry, authoritative), `secondary_education=true` (education_registry, authoritative), `speaks_estonian=true` (language_registry, authoritative)
- **Rule path:** Only the user-evidence claim `no_conflict_declared=true`. Stage 2 draws `ee_citizen`, `secondary_education`, `speaks_estonian`, `full_capacity` (all true, authoritative). `allow_ee_citizen` (§ 14 (1)) is entailed; `criminal_conviction` is a deny-only term and is not consulted. → **ALLOW**.
- **Solver check:** ALLOW; fired = ['allow_ee_citizen']; note: “ALLOW entailed.”

### 2.7 `civil_service_admission/deny_no_allow_path_no_estonian_language`

- **Label:** Admission: language requirement unmet, no allow path  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “I am applying for a civil-service position. I am an Estonian citizen with a completed secondary education and active legal capacity, but I do not yet speak Estonian at the level required by law. I have no prior conviction on record. I confirm I have no family conflict with any supervising official at the agency.”
- **Oracle claims:** `criminal_conviction=false`, `ee_citizen=true`, `eu_citizen=false`, `full_capacity=true`, `no_conflict_declared=true`, `secondary_education=true`, `speaks_estonian=false`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `criminal_conviction=false` (criminal_records_registry, authoritative), `ee_citizen=true` (population_registry, authoritative), `eu_citizen=false` (population_registry, authoritative), `full_capacity=true` (population_registry, authoritative), `secondary_education=true` (education_registry, authoritative), `speaks_estonian=true` (language_registry, authoritative)
- **Rule path:** Claims: `ee_citizen=true`, `eu_citizen=false`, `speaks_estonian=false`, the rest true, `criminal_conviction=false`, `no_conflict_declared=true`. Both § 14 paths require `speaks_estonian`; both are blocked; `deny_conviction` does not fire → **DENY** (no applicable rules).
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 2.8 `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired`

- **Label:** Withdrawal: 14-day period expired, no allow path  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “I bought a standard catalogue laptop (not made to order) from an online shop as a private consumer; the contract was concluded at a distance. I received it six weeks ago, so the 14-day withdrawal period has already expired, and I only sent the withdrawal notice to the seller yesterday, after the period had run out.”
- **Oracle claims:** `distance_contract=true`, `excluded_category=false`, `is_consumer=true`, `notice_sent_in_time=false`, `within_14_days=false`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `distance_contract=true` (trader_crm, authoritative), `excluded_category=false` (product_catalogue, authoritative), `is_consumer=true` (trader_crm, authoritative)
- **Rule path:** Claims: `is_consumer=true`, `distance_contract=true`, `excluded_category=false`, `within_14_days=false`, `notice_sent_in_time=false`. `allow_distance_withdrawal` (§ 56 (1)) is blocked on the two user terms; `deny_excluded_category` (§ 53 (4)) does not fire → **DENY** (no applicable rules).
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 2.9 `journalistic_data_disclosure/allow_register_only_consent_from_register`

- **Label:** Journalism: bare request, consent register shows consent  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “We want to publish personal data about an individual in an upcoming piece. Please check the registers for whether we may proceed.”
- **Oracle claims:** none (bare request)
- **Register overrides:** `{"journalistic_data_disclosure__consent_registry": {"set": {"main": {"subject_consent": true}}}}`
- **Facts (lookup):** `journalistic_purpose=true` (editorial_cms, authoritative), `subject_consent=true` (consent_registry, authoritative)
- **Rule path:** No claims. Stage 2 draws `subject_consent=true` (consent register, scenario override) and `journalistic_purpose=true`. `allow_consent_basis` is entailed on an authoritative fact; the journalism path stays open on user terms but is irrelevant once ALLOW is entailed. → **ALLOW**.
- **Solver check:** ALLOW; fired = ['allow_consent_basis']; note: “ALLOW entailed.”

### 2.10 `journalistic_data_disclosure/allow_register_only_purpose_from_cms`

- **Label:** Journalism: CMS confirms purpose, editor supplies judgements  
- **Mechanism:** `register_only`  
- **Gold:** ALLOW (scored ALLOW); missing terms: none
- **Request text:** “We are preparing a story about a public official. The editor confirms there is public interest in it and the work follows the principles of journalism ethics; publication would not cause excessive damage to the subject's rights. Please check the editorial system for the classification of the processing.”
- **Oracle claims:** `excessive_harm=false`, `journalism_ethics=true`, `public_interest=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `journalistic_purpose=true` (editorial_cms, authoritative), `subject_consent=false` (consent_registry, authoritative)
- **Rule path:** Claims: `public_interest=true`, `journalism_ethics=true`, `excessive_harm=false` (user-evidence terms). Stage 2 draws `journalistic_purpose=true` from the editorial CMS. `allow_journalism_basis` (§ 4, first sentence) is entailed; the defeater `block_ethics_when_excessive_harm` does not fire. → **ALLOW**.
- **Solver check:** ALLOW; fired = ['allow_journalism_basis']; note: “ALLOW entailed.”

### 2.11 `journalistic_data_disclosure/deny_no_allow_path_no_public_interest`

- **Label:** Journalism: no public interest, no allow path  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “Our editor reviewed the story. The processing is journalistic in purpose and the reporting follows the principles of journalism ethics, but the editor finds no public interest in the private details it discloses. No consent from the subject is on record. The risk review concludes that publication would not cause excessive damage to the subject's rights.”
- **Oracle claims:** `excessive_harm=false`, `journalism_ethics=true`, `journalistic_purpose=true`, `public_interest=false`, `subject_consent=false`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `journalistic_purpose=true` (editorial_cms, authoritative), `subject_consent=false` (consent_registry, authoritative)
- **Rule path:** Claims: `journalistic_purpose=true`, `journalism_ethics=true`, `public_interest=false`, `subject_consent=false`, `excessive_harm=false`. `allow_journalism_basis` is blocked on `public_interest`; `allow_consent_basis` is blocked on `subject_consent`; the defeater does not fire → **DENY** (no applicable rules).
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

### 2.12 `land_tax_home_exemption/deny_no_allow_path_municipality_not_set`

- **Label:** Land tax: council has not set the exemption, no allow path  
- **Mechanism:** `no_allow_path`  
- **Gold:** DENY (scored DENY); missing terms: none
- **Request text:** “I am a pensioner and the owner of the parcel in a rural municipality. The cadastre lists the intended purpose of the land as residential land and the population register has my residence at that address. I have submitted the application for the supplementary pensioner exemption, but the municipal council has not set any home-land exemption for the coming tax period.”
- **Oracle claims:** `applicant_is_owner=true`, `application_submitted=true`, `municipality_exemption_set=false`, `primary_residence_registered=true`, `receives_pension=true`, `residential_land=true`
- **Register overrides:** none (base registry)
- **Facts (lookup):** `applicant_is_owner=true` (land_registry, authoritative), `primary_residence_registered=true` (population_registry, authoritative), `receives_pension=true` (social_insurance_registry, authoritative), `residential_land=true` (land_registry, authoritative)
- **Rule path:** Claims: owner, pensioner, residential land, residence registered, application submitted all true; `municipality_exemption_set=false`. Both `allow_home_land_exemption` (§ 11 (1)) and `allow_pensioner_supplement` (§ 11 (5) 1)) require the council's incentive; both blocked; no deny rule exists → **DENY** (no applicable rules).
- **Solver check:** DENY; fired = none; note: “No allow rule is entailed and nothing decision-relevant is missing; default DENY.”

## 3. Retired scenarios (5)

| id | gold | reason |
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

## 4. Request texts rewritten in English (35 files, 42 pre-existing scenarios)

Rule: same claims, same silences as the 5 Sep faithful-inputs audit; Estonian legal
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
|---|---|---|---|
| `building_permit_grant` | `request_allow.txt` | `allow_claims_verified` | building_requirements_met=T, competent_designer=T, fee_paid=T, plan_conformant=T, plan_violation=F, site_study_provided=T |
| `building_permit_grant` | `allow_register_only.txt` | `allow_register_only` | — |
| `building_permit_grant` | `deny_no_allow_path_designer_not_competent.txt` | `deny_no_allow_path_designer_not_competent` | building_requirements_met=T, competent_designer=F, fee_paid=T, plan_conformant=T, plan_violation=F, site_study_provided=T |
| `building_permit_grant` | `deny_no_allow_path_no_site_study.txt` | `deny_no_allow_path_no_site_study` | building_requirements_met=T, competent_designer=T, fee_paid=T, plan_conformant=T, plan_violation=F, site_study_provided=F |
| `building_permit_grant` | `deny_own_admission_plan_violation.txt` | `deny_own_admission_plan_violation` | building_requirements_met=T, competent_designer=T, fee_paid=T, plan_conformant=F, plan_violation=T, site_study_provided=T |
| `building_permit_grant` | `need_register_silent_fee.txt` | `need_register_silent_fee` | — |
| `building_permit_grant` | `unverifiable_register_down_payment_ledger.txt` | `unverifiable_register_down_payment_ledger` | — |
| `building_permit_grant` | `unverifiable_trust_only_designer_selfreport.txt` | `unverifiable_trust_only_designer_selfreport` | — |
| `child_representation_by_one_parent` | `request_allow.txt` | `allow_claims_verified_emergency` | applicant_is_not_parent=F, applicant_is_parent=T, emergency=T, one_parent_unreachable=T |
| `child_representation_by_one_parent` | `request_deny.txt` | `deny_own_admission_not_parent` | applicant_is_not_parent=T, applicant_is_parent=F, both_parents_consent=F, delegated_decision_right=F |
| `child_representation_by_one_parent` | `request_register_then_user.txt` | `need_user_silent_emergency_after_register_lookup` | — |
| `civil_service_admission` | `allow_alt_rule_eu_citizen_overrides_register.txt` | `allow_alt_rule_eu_citizen_overrides_register` | criminal_conviction=F, ee_citizen=F, eu_citizen=T, full_capacity=T, no_conflict_declared=T, secondary_education=T, speaks_estonian=T |
| `civil_service_admission` | `request_allow.txt` | `allow_claims_verified` | criminal_conviction=F, ee_citizen=T, eu_citizen=F, full_capacity=T, no_conflict_declared=T, secondary_education=T, speaks_estonian=T |
| `civil_service_admission` | `deny_no_allow_path_no_citizenship.txt` | `deny_no_allow_path_no_citizenship` | criminal_conviction=F, ee_citizen=F, eu_citizen=F, full_capacity=T, no_conflict_declared=T, secondary_education=T, speaks_estonian=T |
| `civil_service_admission` | `deny_own_admission_conviction.txt` | `deny_own_admission_conviction` | criminal_conviction=T, ee_citizen=T, eu_citizen=F, full_capacity=T, no_conflict_declared=T, secondary_education=T, speaks_estonian=T |
| `civil_service_admission` | `need_register_silent_citizenship.txt` | `need_register_silent_citizenship` | no_conflict_declared=T |
| `civil_service_admission` | `unverifiable_register_down_population_registry.txt` | `unverifiable_register_down_population_registry` | no_conflict_declared=T |
| `civil_service_admission` | `unverifiable_trust_only_applicant_selfreport.txt` | `unverifiable_trust_only_applicant_selfreport` | no_conflict_declared=T |
| `consumer_purchase_withdrawal` | `request_allow.txt` | `allow_claims_verified` | distance_contract=T, excluded_category=F, is_consumer=T, notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `allow_register_only_consumer_status.txt` | `allow_register_only_consumer_status` | notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `deny_no_allow_path_not_consumer.txt` | `deny_no_allow_path_not_consumer` | distance_contract=T, excluded_category=F, is_consumer=F, notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `deny_own_admission_custom_goods.txt` | `deny_own_admission_custom_goods` | distance_contract=T, excluded_category=T, is_consumer=T, notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `need_register_silent_consumer_status.txt` | `need_register_silent_consumer_status` | notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `request_need_user.txt` | `need_user_silent_deadline_and_notice` | distance_contract=T, excluded_category=F, is_consumer=T |
| `consumer_purchase_withdrawal` | `unverifiable_register_down_trader_crm.txt` | `unverifiable_register_down_trader_crm` | notice_sent_in_time=T, within_14_days=T |
| `consumer_purchase_withdrawal` | `unverifiable_trust_only_trader_selfreport.txt` | `unverifiable_trust_only_trader_selfreport` | notice_sent_in_time=T, within_14_days=T |
| `journalistic_data_disclosure` | `allow_alt_rule_consent_overrides_register.txt` | `allow_alt_rule_consent_overrides_register` | excessive_harm=F, journalism_ethics=F, journalistic_purpose=F, public_interest=F, subject_consent=T |
| `journalistic_data_disclosure` | `request_allow.txt` | `allow_claims_verified` | excessive_harm=F, journalism_ethics=T, journalistic_purpose=T, public_interest=T, subject_consent=F |
| `journalistic_data_disclosure` | `deny_no_allow_path_no_purpose_no_consent.txt` | `deny_no_allow_path_no_purpose_no_consent` | excessive_harm=F, journalism_ethics=T, journalistic_purpose=F, public_interest=T, subject_consent=F |
| `journalistic_data_disclosure` | `deny_own_admission_excessive_harm.txt` | `deny_own_admission_excessive_harm` | excessive_harm=T, journalism_ethics=T, journalistic_purpose=T, public_interest=T, subject_consent=F |
| `journalistic_data_disclosure` | `need_register_silent_purpose_and_consent.txt` | `need_register_silent_purpose_and_consent` | excessive_harm=F, journalism_ethics=T, public_interest=T |
| `journalistic_data_disclosure` | `need_user_silent_editorial_judgements.txt` | `need_user_silent_editorial_judgements` | journalistic_purpose=T, subject_consent=F |
| `journalistic_data_disclosure` | `unverifiable_register_down_editorial_cms.txt` | `unverifiable_register_down_editorial_cms` | excessive_harm=F, journalism_ethics=T, public_interest=T |
| `journalistic_data_disclosure` | `unverifiable_trust_only_editorial_selfreport.txt` | `unverifiable_trust_only_editorial_selfreport` | excessive_harm=F, journalism_ethics=T, public_interest=T |
| `land_tax_home_exemption` | `request_allow.txt` | `allow_claims_verified`, `allow_claims_verified_pensioner_supplement` | applicant_is_owner=T, application_submitted=T, municipality_exemption_set=T, primary_residence_registered=T, receives_pension=T, residential_land=T |
| `land_tax_home_exemption` | `allow_register_only_ownership_and_residence.txt` | `allow_register_only_ownership_and_residence` | application_submitted=T, municipality_exemption_set=T |
| `land_tax_home_exemption` | `deny_no_allow_path_not_residential.txt` | `deny_no_allow_path_not_residential` | applicant_is_owner=T, application_submitted=T, municipality_exemption_set=T, primary_residence_registered=T, receives_pension=T, residential_land=F |
| `land_tax_home_exemption` | `deny_own_admission_not_owner.txt` | `deny_own_admission_not_owner` | applicant_is_owner=F, application_submitted=F, municipality_exemption_set=T, primary_residence_registered=F, receives_pension=T, residential_land=T |
| `land_tax_home_exemption` | `need_register_silent_municipality_exemption.txt` | `need_register_silent_municipality_exemption` | application_submitted=T |
| `land_tax_home_exemption` | `unverifiable_register_down_population_registry.txt` | `unverifiable_register_down_population_registry` | application_submitted=T |
| `land_tax_home_exemption` | `unverifiable_trust_only_applicant_selfreport.txt` | `unverifiable_trust_only_applicant_selfreport` | application_submitted=F |

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

