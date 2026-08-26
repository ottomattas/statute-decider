# Experiment (ii) mismatch drill-down — gold vs model response

**SMOKE / SCALE — UNVALIDATED.** Do not quote as results.

Generated 2026-08-26T05:51:50Z by `experiments/render_drilldown.py`.

A *failed cell* is an LLM-only row with a wrong 3-way outcome, an
imperfect missing-fact set (P or R < 1 despite a correct outcome), or a
hard error. Gold is shown once per scenario; every failing model
response is listed against it.

Rows whose gold is `gold_confidence: low` (solver-proposed, unaudited) are marked **[GOLD UNAUDITED]**; treat their mismatches as provisional until the operator audit lands.

## Source `smoke` — `experiments/results/experiment_ii_llm.jsonl`

- rows: 188 (188 scored); failed cells: 62 = 50 wrong outcome + 12 fact-set-only + 0 hard errors

### Wrong outcomes by provider and expected class

| provider | ALLOW | DENY | NEED_MORE_INFO |
|---|---|---|---|
| anthropic | 3/14 | 1/12 | 8/21 |
| deepseek | 2/14 | 1/12 | 7/21 |
| gemini | 2/14 | 0/12 | 13/21 |
| openai | 1/14 | 1/12 | 11/21 |

### `building_permit_deny_no_site_study`

**Gold:** outcome `DENY`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| openai | 0 | ALLOW | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _openai#r0_: Known facts show the project conforms to the detailed plan (plan_conformant = true), meets building requirements, was prepared by a competent designer, and the fee is paid. Under §42 an ehitusluba is granted where these conditions are met, and none of the §44 refusal grounds are met on the given facts. Therefore the permit is allowed.

### `building_permit_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `fee_paid`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The submitted building project conforms to the detailed plan and meets all construction requirements, as stated in § 42(1). Furthermore, none of the conditions for refusal listed in § 44 are met: the project conforms to the plan and requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site study (§ 44(3)). The state fee has also been paid, as mentioned in the cas
- _openai#r0_: All statutory requirements in §42 are satisfied (plan_conformant, building_requirements_met, competent_designer, site_study_provided) and none of the refusal grounds in §44 apply (no plan violation, competent designer prepared project, site study provided). Therefore the permit may be granted.
- _anthropic#r0_: Under § 42(1), a building permit shall be granted if the submitted project meets the requirements set out in legal acts, in particular the detailed plan or design conditions and the requirements for the building and construction. Under § 44, a permit may be denied only if: (1) the project does not conform to the detailed plan, design conditions, special planning, or building/construction requireme
- _deepseek#r0_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee payment is not a statutory condition for granting the permit under the cited provisions.

### `building_permit_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `fee_paid`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The submitted building project conforms to the detailed plan and meets all construction requirements, as stated in § 42(1). Furthermore, none of the conditions for refusal listed in § 44 are met: the project conforms to the plan and requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site study (§ 44(3)). The state fee has also been paid, as mentioned in the cas
- _openai#r0_: §42 allows issuance where the project meets statutory requirements. §44 lists only three grounds for refusal: nonconformity with plan/requirements, lack of a competent designer or expertise, or missing/unused site study. All those are negated here (plan_conformant=true, building_requirements_met=true, competent_designer=true, site_study_provided=true, plan_violation=false). The statute as provided
- _anthropic#r0_: Under § 42(1), a building permit shall be granted if the submitted project meets the requirements set out in legal acts, in particular the detailed plan or design conditions and the requirements for the building and construction. Under § 44, a permit may be denied only if: (1) the project does not conform to the detailed plan, design conditions, special planning, or building/construction requireme
- _deepseek#r0_: The project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided. No planning violations are recorded. The fee payment is not required by the statute for granting a permit, so it is not a missing fact.

### `building_permit_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `building_requirements_met`, `competent_designer`, `fee_paid`, `plan_conformant`, `site_study_provided`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The submitted building project conforms to the detailed plan and meets all building requirements. The design was prepared by a competent person, and the site study is available. None of the conditions for refusing a building permit are met, and the conditions for granting a permit are satisfied.
- _openai#r0_: All statutory conditions for issuing an ehitusluba are met (conforms to detailplaneering, meets building requirements, competent designer prepared the project, site study provided) and none of the refusal grounds in §44 apply.
- _anthropic#r0_: Under § 42(1), a building permit shall be granted if the submitted building project complies with legal requirements, in particular the detailed plan and construction requirements. Under § 44, a permit may be denied only if: (1) the project does not conform to the detailed plan or construction requirements, (2) the design was not prepared by a competent person, or (3) the site study is missing or 
- _deepseek#r0_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study was provided, and no planning violations exist. The fee payment is not a statutory condition for granting the permit.

### `civil_service_allow_eu_path`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _anthropic#r0_: § 14(1) requires that an official must be an Estonian citizen (Eesti Vabariigi kodanik). The applicant is an EU citizen but not an Estonian citizen (ee_citizen = false). While § 14(2) permits EU citizens to be appointed as officials in general, the applicant has not specified which position is sought. However, the fundamental requirement of § 14(1) is not met: the applicant is not an Estonian citi

### `civil_service_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `ee_citizen`, `eu_citizen`, `full_capacity`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 0 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |

Model reasoning (deduplicated):

- _gemini#r0_: The applicant meets all the requirements for being taken into service as an official under § 14(1) and does not fall under any of the prohibitions listed in § 15, based on the provided facts and the applicant's statements.
- _openai#r0_: Statute requires the applicant be an Estonian citizen and have full legal capacity; those catalog claims are not provided. Other disqualifying factors (conviction, family conflict, education, language) are known and acceptable.
- _anthropic#r0_: § 14(1) requires that an applicant be an Estonian citizen with full legal capacity, have at least secondary education, and speak Estonian at the required level. While the applicant has confirmed secondary education, Estonian language proficiency, and no criminal conviction, the critical facts of Estonian citizenship (ee_citizen) and full legal capacity (full_capacity) remain unknown and are mandat
- _deepseek#r0_: The statute requires the applicant to be an Estonian citizen (or EU citizen with restrictions) and have full legal capacity. These facts are unknown and necessary to decide.

### `civil_service_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `ee_citizen`, `eu_citizen`, `full_capacity`, `secondary_education`, `speaks_estonian`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The applicant meets all the requirements of § 14 (1) as an Estonian citizen with secondary education, full legal capacity, and Estonian language proficiency. None of the disqualifications listed in § 15 apply, as the applicant has no criminal convictions and no family conflict with a supervising official.
- _openai#r0_: Applicant is an Estonian citizen with secondary education, full legal capacity, and required Estonian language skills, and has no disqualifying conviction or family conflict under §15, so statute permits appointment.
- _anthropic#r0_: The applicant meets all requirements under § 14(1): Estonian citizen (ee_citizen: true), full legal capacity (full_capacity: true), secondary education (secondary_education: true), and speaks Estonian at required level (speaks_estonian: true). The applicant satisfies all exclusion criteria under § 15: no criminal conviction (criminal_conviction: false) and no family conflict with supervising offic
- _deepseek#r0_: Applicant meets all requirements: Estonian citizen, secondary education, Estonian language, full capacity, no criminal conviction, and no family conflict.

### `civil_service_u8_need_user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `no_conflict_declared`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: All requirements under § 14 (1) are met, and no disqualifying conditions under § 15 (1), (2), or (4) are present based on the provided facts and the user's declaration.
- _openai#r0_: All statutory requirements of §14(1) are met (Estonian citizen, secondary education, full legal capacity, required Estonian language). No disqualifying grounds from §15 are present (no conviction for intentional crime and no family conflict with a supervising official). Therefore appointment is permitted.

### `consumer_withdrawal_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `distance_contract`, `is_consumer`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The consumer has the right to withdraw from a distance contract within 14 days, provided the notice is sent in time and the contract does not fall under any excluded categories. All these conditions are met in this case.

### `consumer_withdrawal_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `distance_contract`, `is_consumer`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The consumer has the right to withdraw from the distance contract within 14 days, and all conditions for withdrawal, including timely notice and the absence of excluded categories, are met according to the statute.
- _openai#r0_: As a consumer who concluded a distance (sidevahendi) contract, you may withdraw within 14 days (§56(1)). You sent the withdrawal notice in time (§56(2^1)) and the laptop is not in an excluded category (§53(4) exclusions) — so withdrawal is permitted.
- _anthropic#r0_: Under § 56(1), a consumer may withdraw from a distance contract within 14 days without stating reasons. § 53(4) lists exclusions, but the laptop is a standard catalogue model, not a custom-made item, perishable good, or sealed hygiene product—so no exclusion applies. All required conditions are met: the consumer (is_consumer: true) concluded a distance contract (distance_contract: true), sent with
- _deepseek#r0_: The consumer has a valid distance contract, is within the 14-day withdrawal period, sent notice in time, and the contract is not excluded under § 53(4).

### `db-then-user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `emergency`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |

Model reasoning (deduplicated):

- _openai#r0_: Applicant is a parent but has no sole custody or delegated decision right and the other parent does not consent. The statute does not clearly permit unilateral access to a child’s data from third parties in these circumstances; access may be allowed in an emergency or if the other parent is unreachable. Need to know whether an emergency exists or the other parent is unreachable.
- _anthropic#r0_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent or delegated decision rights. Under Perekonnaseadus § 120, parents with joint custody must act jointly in decisions about the child, unless one parent has been given specific decision-making authority or there is an emergency. To determine whether the parent can access the child's data unilat
- _deepseek#r0_: The statute allows a parent to act alone in urgent situations or if the other parent is unreachable, but these facts are unknown.

### `deny`

**Gold:** outcome `DENY`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |

Model reasoning (deduplicated):

- _anthropic#r0_: Under Estonian family law (Perekonnaseadus § 120), a child's legal representative is normally a parent with custody rights. The applicant is the child's aunt without delegated authority or parental consent. Section § 120(3) allows a non-custodial parent to make necessary decisions alone if delay would conflict with the child's interests, but this requires an emergency situation. Section § 120(5) p
- _deepseek#r0_: The statute allows a non-parent to make decisions for a child only in specific circumstances, such as an emergency or when one parent is unreachable. Since these facts are unknown, more information is needed.

### `journalism_allow_via_consent`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The statute permits processing without consent for journalistic purposes only if there is public interest and it aligns with journalism ethics. According to the known facts, the processing does not have a journalistic purpose, there is no public interest, and it does not respect journalism ethics. Therefore, the conditions for processing under §4 are not met.
- _anthropic#r0_: The statute permits processing personal data for journalistic purposes without consent only if: (1) there is a journalistic purpose, (2) there is public interest, (3) it complies with journalism ethics principles, and (4) publication does not excessively harm the data subject's rights. The known facts show journalistic_purpose=false, public_interest=false, and journalism_ethics=false. Although the
- _deepseek#r0_: The statute requires journalistic purpose, public interest, and compliance with journalism ethics. All three are false, so the processing is not permitted despite consent.

### `journalism_need_user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalism_ethics`, `public_interest`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |

Model reasoning (deduplicated):

- _gemini#r0_: The processing is for journalistic purposes, there is public interest, it follows journalism ethics, and the reporting is proportionate, meaning it does not excessively harm the data subject's rights. All conditions for processing without consent under § 4 are met.
- _openai#r0_: The statute allows processing without consent only if there is public interest, it complies with journalism ethics, and publication does not excessively harm the subject. Those three facts are not provided, so more information is required.
- _anthropic#r0_: The statute permits processing of personal data without subject consent (nõusolek) for journalistic purposes when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. The case confirms journalistic_purpose=true, the editor confirms public_interest exists, journalism_ethics are followed, and the reporting i
- _deepseek#r0_: The statute requires public interest, compliance with journalism ethics, and no excessive harm. These facts are unknown.

### `journalism_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The statute permits processing without consent for journalistic purposes if there is public interest, it aligns with journalistic ethics, and does not excessively harm the data subject. All these conditions are met: the processing is for a journalistic purpose, there is public interest, journalistic ethics are followed, and there is no excessive harm. Consent is not required under these circumstan
- _openai#r0_: All statutory conditions are met: the processing has a journalistic purpose, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject; consent is not required under the statute.

### `journalism_u5_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`, `subject_consent`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The statute permits processing without consent for journalistic purposes if there is public interest, it aligns with journalism ethics, and does not excessively harm the data subject. All these conditions are met: the purpose is journalistic, there is public interest, journalism ethics are followed, and the reporting is not excessively harmful.
- _openai#r0_: All statutory requirements are met: the processing has a journalistic purpose, there is public interest (public_interest=true), it complies with journalism ethics (journalism_ethics=true), and publication does not excessively harm the subject (excessive_harm=false). Consent is not required under the statute in these circumstances.
- _anthropic#r0_: The statute permits personal data processing for journalistic purposes without consent if there is public interest, journalism ethics are respected, and there is no excessive harm. Known facts confirm public_interest (true), journalism_ethics (true), and excessive_harm (false). However, journalistic_purpose is unknown and required to establish that the processing itself qualifies as 'ajakirjandusl

### `journalism_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`, `subject_consent`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The statute permits processing personal data for journalistic purposes without consent if there is public interest, it aligns with journalism ethics, and does not excessively harm the data subject's rights. All these conditions are met according to the known facts.
- _openai#r0_: All statutory conditions are satisfied: processing is journalistic, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject. Consent is not required under the statute in these circumstances.
- _anthropic#r0_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, excessive_harm=false. The absence of subjec
- _deepseek#r0_: All required conditions are met: journalistic purpose, public interest, ethics, no excessive harm, and consent is not required.

### `land_tax_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `applicant_is_owner`, `municipality_exemption_set`, `primary_residence_registered`, `residential_land`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 0 | DENY | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The applicant does not receive a state pension, failing the eligibility criteria for the target group in §11(5)1. Additionally, the application for the supplementary exemption has not been submitted, which is required by §11(7).
- _openai#r0_: To receive the supplementary pensioner maksusoodustus the person must be a pension recipient and must submit the application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the supplementary pensioner exemption are not met.
- _anthropic#r0_: The applicant meets the conditions for the basic home-land exemption (residential land, primary residence registered, is owner, municipality exemption set). However, to qualify for the supplementary pensioner exemption under § 11(5)(1), the applicant must both (1) receive a state pension and (2) submit an application. The known facts show receives_pension = false and application_submitted = false.
- _deepseek#r0_: The applicant does not receive a state pension (receives_pension=false), so they do not qualify for the supplementary pensioner exemption under §11(5)(1). Also, the application was not submitted (application_submitted=false), but the primary disqualifier is the lack of pension status.

### `need-db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `emergency`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The applicant is a parent with joint custody, and the other parent's consent is not given. While parents with joint custody generally act in agreement (§ 118 (1)), one parent may act alone in the child's interests if a delay would be detrimental to the child's interests (§ 120 (3)). This could apply in an emergency or if the other parent is unreachable. Therefore, information on whether there is a
- _openai#r0_: Applicant is a parent (known true). Under §144 a parent has the right to require from the other parent information about the child’s person and property unless this would be contrary to the child’s interests. No known fact indicates such a prohibition, so access is permitted.
- _anthropic#r0_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian family law (Perekonnaseadus § 120), parents with joint custody must act in agreement regarding significant matters affecting the child. To determine whether the applicant can unilaterally access the child's data, it is necessary to establish whether:
- _deepseek#r0_: The statute allows a parent to act alone in urgent situations or if the other parent is unreachable, but these facts are unknown.

### `unrelated-law`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 0 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| openai | 0 | DENY | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The provided statute, 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Act on the Implementation of the Building Code and the Planning Act), pertains exclusively to planning and construction law. It contains no provisions or rules applicable to medical decisions for children, parental consent, or emergency medical situations. Therefore, this statute does not provide a legal basis to de
- _openai#r0_: The provided statute concerns planning and building (ehitus/planeerimine) transitional rules and does not authorize or regulate parental medical decision-making. On the given facts, the statute does not permit the applicant to make the requested medical decision, so the request is denied under the text supplied.
- _anthropic#r0_: The statute provided is the Estonian 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Implementation Act for Building Code and Planning Act), which concerns construction and planning law matters. It contains no provisions regarding parental decision-making, medical treatment authorization, emergency medical procedures, or custody rights. The case request concerns a medical emergency re
- _deepseek#r0_: The statute does not address medical decisions for a child. The known facts are irrelevant to the statute's provisions, which concern planning and construction. No applicable rule can be identified, so the outcome is indeterminate.

## Source `scale` — `experiments/results/scale-20260825/ii/experiment_ii_llm.jsonl`

- rows: 1884 (1880 scored); failed cells: 599 = 482 wrong outcome + 113 fact-set-only + 4 hard errors

### Wrong outcomes by provider and expected class

| provider | ALLOW | DENY | NEED_MORE_INFO |
|---|---|---|---|
| anthropic | 30/140 | 10/120 | 72/210 |
| deepseek | 20/140 | 10/120 | 70/210 |
| gemini | 22/140 | 0/120 | 130/210 |
| openai | 6/140 | 6/120 | 106/210 |

### `building_permit_deny_no_site_study`

**Gold:** outcome `DENY`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| deepseek | 0 | ERROR | — | — | — | Expecting ',' delimiter: line 1 column 1609 (char 1608) |
| deepseek | 2 | ERROR | — | — | — | Expecting ',' delimiter: line 1 column 1249 (char 1248) |
| deepseek | 8 | ERROR | — | — | — | Expecting ',' delimiter: line 1 column 1377 (char 1376) |
| openai | 1 | ALLOW | NO | 1.00 | 1.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 1.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _openai#r1_: Under §42 the permit is granted where the project meets the detailed plan and construction requirements and is prepared by a competent person. The known facts state plan_conformant=true, building_requirements_met=true and competent_designer=true, so the §44 refusal grounds (plan non‑conformity or incompetent designer) do not apply. The absent site study is not shown to be a required study in the f
- _openai#r2_: Under §42 a permit is issued where the project meets the detailed plan and building requirements. Here plan_conformant=true, building_requirements_met=true and competent_designer=true (fee_paid=true). The refusal grounds in §44 (non‑conformity with the detailed plan, incompetent designer or missing required site study) are not triggered on the known facts, so the statute permits issuance of the pe
- _openai#r9_: Known facts show the project conforms to the detailed plan, meets building requirements, and was prepared by a competent designer. §42 permits granting a permit when these conditions are met. §44 refusal grounds (in particular a missing required site study) are not established by the given facts (site_study_provided is false but there is no fact that such a study is required), so no statutory refu

### `building_permit_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `fee_paid`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r1, gemini#r2, gemini#r4, gemini#r5_: The submitted building project conforms to the detailed plan and meets all construction requirements, as stated in § 42(1). Furthermore, none of the conditions for refusal listed in § 44 are met: the project conforms to the plan and requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site study (§ 44(3)). The state fee has also been paid, as mentioned in the cas
- _gemini#r3, gemini#r6, gemini#r7, gemini#r8, gemini#r9, gemini#r0_: The submitted building project conforms to the detailed plan and meets the building requirements, satisfying § 42(1). All conditions for refusal under § 44 are avoided: the project complies with the detailed plan and building requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site construction study (§ 44(3)). The statute provided does not list fee payment as a
- _openai#r0_: All statutory requirements for issuing a building permit are satisfied and none of the §44 refusal grounds apply: project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided. Therefore the permit may be granted under §42.
- _openai#r1_: Under §42 a building permit is granted if the project meets the legal requirements. The §44 refusal grounds are not met here: the project conforms to the detailed plan (plan_conformant=true; plan_violation=false), meets construction requirements (building_requirements_met=true), was prepared by a competent designer (competent_designer=true), and the site study is provided (site_study_provided=true
- _openai#r2_: All statutory conditions for granting a building permit are met (project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study provided) and none of the statutory refusal grounds in §44 apply.
- _openai#r3_: All statutory requirements for granting (§42) are satisfied (project conforms to the detailed plan and to building requirements; competent designer prepared the project; site study provided). None of the refusal grounds in §44( ) apply, so the permit may be granted.
- _openai#r4_: All statutory conditions for refusal (§44) are absent: the project conforms to the detailed plan (plan_conformant true; plan_violation false), meets building requirements (building_requirements_met true), was prepared by a competent designer (competent_designer true), and the site study is provided (site_study_provided true). Section 42’s approval criteria are therefore satisfied. The unknown fee_
- _openai#r5_: All statutory conditions for refusal (§44) are absent: the project conforms to the detailed plan, meets construction requirements, was prepared by a competent designer, and the site study is provided. Under §42 the permit is granted when these requirements are met.
- _openai#r6_: All statutory conditions for refusal (§44) are absent: the project conforms to the detailed plan, meets construction requirements, was prepared by a competent designer, and a site study is provided. Under §42 these facts support granting the building permit; no statute-provided ground for denial applies.
- _openai#r7_: All statutory requirements in §42 are satisfied (project conforms to the detailed plan and building requirements; competent designer prepared the project; site study provided) and none of the §44 refusal grounds apply on the given facts. The statute excerpts do not make payment of the state fee a condition for refusing the permit.
- _openai#r8_: None of the §44 refusal grounds apply: the project conforms to the detailed plan (plan_conformant=true, plan_violation=false), meets building requirements (building_requirements_met=true), was prepared by a competent designer (competent_designer=true), and the site study is provided (site_study_provided=true). Under §42, these satisfied conditions permit issuance of the building permit.
- _openai#r9_: Under §42 the permit is granted if the project meets applicable legal requirements. None of the §44 refusal grounds apply: plan_conformant is true (and plan_violation false), building_requirements_met is true, competent_designer is true, and site_study_provided is true. Therefore the statute permits issuing the building permit on the known facts.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under § 42(1), a building permit shall be granted if the submitted project meets the requirements set out in legal acts, in particular the detailed plan or design conditions and the requirements for the building and construction. Under § 44, a permit may be denied only if: (1) the project does not conform to the detailed plan, design conditions, special planning, or building/construction requireme
- _deepseek#r0, deepseek#r1, deepseek#r2, deepseek#r6, deepseek#r7, deepseek#r9_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee payment is not a statutory condition for granting the permit under the cited provisions.
- _deepseek#r3, deepseek#r4, deepseek#r5_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee status is not a statutory condition for granting the permit under the cited provisions.
- _deepseek#r8_: All required conditions for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee payment is not a statutory condition for granting the permit under the cited provisions.

### `building_permit_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `fee_paid`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r1, gemini#r3, gemini#r5, gemini#r6, gemini#r7, gemini#r8, gemini#r9_: The submitted building project conforms to the detailed plan and meets the building requirements, satisfying § 42(1). All conditions for refusal under § 44 are avoided: the project complies with the detailed plan and building requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site construction study (§ 44(3)). The statute provided does not list fee payment as a
- _gemini#r2, gemini#r4, gemini#r0_: The submitted building project conforms to the detailed plan and meets all construction requirements, as stated in § 42(1). Furthermore, none of the conditions for refusal listed in § 44 are met: the project conforms to the plan and requirements (§ 44(1)), was prepared by a competent person (§ 44(2)), and is based on a site study (§ 44(3)). The state fee has also been paid, as mentioned in the cas
- _openai#r0_: All statutory preconditions for refusal (§44) are absent: the project conforms to the detailed plan, meets construction requirements, was prepared by a competent designer, and the required site study is provided. Under §42 a permit is therefore permitted.
- _openai#r1_: None of the §44 refusal grounds apply: the project conforms to the detailed plan (plan_conformant true, plan_violation false), meets building requirements (building_requirements_met true), was prepared by a competent designer (competent_designer true), and the site study is provided (site_study_provided true). Therefore under §42 the permit may be granted. (The fee_paid fact is not needed to apply
- _openai#r2_: All statutory grant conditions are met (project conforms to the detailed plan and building requirements; competent designer prepared the project; required site study provided), and none of the refusal grounds in §44 apply.
- _openai#r3_: §42 permits issuing a building permit where the project conforms to the detailed plan and building requirements. §44 refusal grounds (non‑conformity with plan/requirements, lack of competent designer or missing site study) do not apply here—plan_conformant, building_requirements_met, competent_designer, and site_study_provided are true and plan_violation is false. The statute does not make payment
- _openai#r4_: Under §42 a permit is given when the project meets legal requirements; here the project conforms to the detailed plan and building requirements, was prepared by a competent designer, and the site study is provided. None of the §44 refusal grounds apply (no plan non‑conformance, no incompetent designer, no missing site study), so the permit may be granted.
- _openai#r5_: No refusal grounds under §44 are present: project conforms to the detailed plan (plan_conformant true; plan_violation false), meets building requirements (building_requirements_met true), was prepared by a competent designer (competent_designer true), and the site study is provided (site_study_provided true). Under §42 the permit may be granted.
- _openai#r6_: All statutory requirements are satisfied and none of the refusal grounds in §44 apply: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided. The statute does not make fee payment a ground for refusal.
- _openai#r7_: All statutory grounds for refusal (non-conformity with the detailed plan or building requirements; lack of a competent designer or missing expertise; missing or ignored site study) are absent: plan_conformant=true, building_requirements_met=true, competent_designer=true, site_study_provided=true, plan_violation=false. Under §42 the permit is to be granted when these requirements are met, so the ap
- _openai#r8_: All statutory grant conditions are satisfied and none of the refusal grounds in §44 apply: the project conforms to the detailed plan, meets construction requirements, was prepared by a competent designer, and the site study is provided (no plan violation). Therefore the permit may be granted under §42.
- _openai#r9_: All statutory acceptance requirements are met (project conforms to the detailed plan and building requirements per §42) and none of the refusal grounds in §44 apply: no plan violation, competent designer prepared the project, and the required site study is provided. The listed unknown (fee_paid) is not a statutory refusal ground in the provided provisions, so it is not required to decide.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under § 42(1), a building permit shall be granted if the submitted project meets the requirements set out in legal acts, in particular the detailed plan or design conditions and the requirements for the building and construction. Under § 44, a permit may be denied only if: (1) the project does not conform to the detailed plan, design conditions, special planning, or building/construction requireme
- _deepseek#r0, deepseek#r5_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee status is not a statutory condition for granting the permit under the cited provisions.
- _deepseek#r1, deepseek#r2, deepseek#r4, deepseek#r7, deepseek#r8, deepseek#r9_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee payment is not a statutory condition for granting the permit under the cited provisions.
- _deepseek#r3_: All required conditions for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided. No planning violations exist. The fee status is not required by the statute for granting or refusing a permit.
- _deepseek#r6_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist. The fee payment is not a statutory condition for granting the permit under the cited sections.

### `building_permit_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `building_requirements_met`, `competent_designer`, `fee_paid`, `plan_conformant`, `site_study_provided`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r1, gemini#r5, gemini#r8, gemini#r9, gemini#r0_: The submitted building project conforms to the detailed plan and meets all building requirements. The design was prepared by a competent person, and the site study is available. None of the conditions for refusing a building permit are met, and the conditions for granting a permit are satisfied.
- _gemini#r2, gemini#r3, gemini#r4, gemini#r6, gemini#r7_: The submitted project conforms to the detailed plan and building requirements, as per § 42(1). Furthermore, none of the refusal conditions under § 44 are met: the project conforms to the plan and requirements, was prepared by a competent person, and is based on the required site study. All known facts support the permit.
- _openai#r0_: All statutory requirements are met and none of the refusal grounds apply: project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study is provided, and no plan violation exists.
- _openai#r1_: All statutory conditions for granting an ehitusluba are met (project conforms to detailed plan, meets building requirements, prepared by a competent designer, site study provided) and none of the refusal grounds in §44 apply.
- _openai#r2_: All statutory conditions for granting an ehitusluba are satisfied and none of the §44 refusal grounds apply: project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study is provided, and there is no plan violation.
- _openai#r3_: All statutory preconditions for granting an ehitusluba are satisfied (project conforms to the detailplan, meets building requirements, prepared by a competent designer, and site study provided). None of the §44 refusal grounds apply, so the permit should be granted.
- _openai#r4_: All conditions for refusal in §44 are absent (project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and required site study is provided). §42 authorizes granting the permit when these requirements are met.
- _openai#r5_: All statutory grant conditions are satisfied (project conforms to the detailed plan and building requirements, prepared by a competent designer, site study provided, fee paid) and none of the §44 denial grounds apply, so the building permit should be granted under §42.
- _openai#r6_: All statutory conditions for refusal (nonconformity with plan, unmet building requirements, incompetent designer, or missing site study) are false and the project meets the detailed plan and building requirements, competent designer prepared the project, site study provided, and fee paid; therefore the permit must be granted under §42 and §44.
- _openai#r7_: All statutory conditions for granting a permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided. None of the refusal grounds in §44 apply.
- _openai#r8_: All statutory requirements for granting a permit are met (project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study provided and fee paid) and none of the refusal grounds in §44 apply.
- _openai#r9_: All statutory conditions for refusal (§44) are absent (project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study is provided). §42 therefore permits granting the building permit.
- _anthropic#r0, anthropic#r3_: Under § 42(1), a building permit shall be granted if the submitted building project meets the requirements set out in legal acts, in particular the detailed plan or design conditions and the requirements for the building and construction. Under § 44, the competent authority refuses a permit only if: (1) the planned building does not conform to the detailed plan, design conditions, special plans, b
- _anthropic#r1, anthropic#r2, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under § 42(1), a building permit shall be granted if the submitted building project complies with legal requirements, particularly the detailed plan and construction requirements. Under § 44, a permit may be denied only if: (1) the project fails to meet the detailed plan, construction requirements, or other public-law restrictions; (2) the project was not prepared by a competent person or lacks ex
- _deepseek#r0, deepseek#r2, deepseek#r7_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study was provided, and no planning violations exist. The fee payment is not a statutory condition for granting the permit.
- _deepseek#r1, deepseek#r3_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist.
- _deepseek#r4, deepseek#r5, deepseek#r6_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, site study was provided, and no planning violations exist. The fee payment is not a statutory condition for granting the permit under §42/44.
- _deepseek#r8_: All statutory requirements for granting a building permit are met: the project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and the site study was provided. No planning violations exist, and the fee has been paid.
- _deepseek#r9_: All statutory requirements are met: plan conformant, building requirements met, competent designer, site study provided, no plan violations, and fee paid.

### `civil_service_allow_eu_path`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 1 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 2 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 3 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 4 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 5 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 6 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 7 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 8 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 9 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 2 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 3 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 4 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 5 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 6 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 7 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 9 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r5, gemini#r6, gemini#r7, gemini#r9_: The applicant is an EU citizen, not an Estonian citizen. While § 14 (2) allows EU citizens to be taken into service, it explicitly states that for certain positions (e.g., management, state supervision, national defense, handling state secrets, or roles involving restricting fundamental rights), only an Estonian citizen may be appointed. The provided facts do not specify the nature of the position
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under § 14(1), an official may only be hired if they are an Estonian citizen (among other requirements). The applicant is an EU citizen but NOT an Estonian citizen (ee_citizen = false). While § 14(2) permits EU citizens to be hired in general, it does not override the primary requirement in § 14(1) that applicants must be Estonian citizens. The applicant fails the fundamental eligibility criterion

### `civil_service_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `ee_citizen`, `eu_citizen`, `full_capacity`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 1 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 2 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 3 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 4 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 5 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 6 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 7 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 8 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| anthropic | 9 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 0 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 1 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 2 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 3 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 4 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 5 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 6 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 7 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 8 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| deepseek | 9 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| openai | 2 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| openai | 4 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| openai | 6 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |
| openai | 9 | NEED_MORE_INFO | YES | 1.00 | 0.67 | `ee_citizen`, `full_capacity` |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r5, gemini#r6, gemini#r0, gemini#r1_: The applicant meets all requirements of § 14(1) (Estonian citizenship, secondary education, full legal capacity, and Estonian language proficiency). No disqualifying conditions from § 15(1), § 15(2), or § 15(4) are met based on the provided facts and user statements.
- _gemini#r7, gemini#r8, gemini#r9_: The applicant meets all the requirements for being taken into service as an official under § 14(1) and does not fall under any of the prohibitions listed in § 15, based on the provided facts and the applicant's statements.
- _openai#r1_: Under §14(1) an official must be an Estonian citizen and have full legal capacity in addition to secondary education and Estonian language ability. Those two claims (ee_citizen and full_capacity) are unknown; criminal conviction and family-conflict disqualifiers appear absent.
- _openai#r2_: §14(1) requires the applicant be an Estonian citizen and have full legal capacity; those claims are unknown. Other statutory disqualifications (conviction, family conflict, education, language) are satisfied.
- _openai#r4_: §14(1) requires the applicant to be an Estonian citizen and to have full legal capacity; those claim ids are unknown. Other statutory disqualifications (conviction, family conflict) are known and satisfied.
- _openai#r6_: Statute §14 requires the applicant be an Estonian citizen (or, per §14(2), an EU citizen meeting legal requirements) and have full legal capacity. Citizenship (ee_citizen) and full_capacity are not provided, so a decision cannot be made.
- _openai#r9_: §14(1) requires an Estonian citizen with full legal capacity, secondary education, and required Estonian language skills. Secondary education and language are known true and §15 disqualifications (conviction, family conflict) are not present, but ee_citizen and full_capacity are not provided and are needed to decide.
- _anthropic#r0_: § 14(1) requires that an official must be an Estonian citizen with full legal capacity, secondary education, and Estonian language proficiency. While secondary education, Estonian language, and absence of criminal conviction are confirmed, the applicant's Estonian citizenship (ee_citizen) and full legal capacity (full_capacity) remain unknown and are essential to determine eligibility. The case re
- _anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: § 14(1) requires that an official must be an Estonian citizen with full legal capacity, secondary education, and Estonian language skills. While secondary education, Estonian language, and absence of criminal conviction are confirmed, the applicant's Estonian citizenship (ee_citizen) and full legal capacity (full_capacity) remain unknown and are essential to determine eligibility.
- _deepseek#r0, deepseek#r1, deepseek#r4_: The statute requires the applicant to be an Estonian citizen (or EU citizen meeting requirements) and have full legal capacity. These facts are unknown and necessary to decide.
- _deepseek#r2, deepseek#r3, deepseek#r5, deepseek#r7, deepseek#r8, deepseek#r9_: The statute requires the applicant to be an Estonian citizen (or EU citizen with restrictions) and have full legal capacity. These facts are unknown and necessary to decide.
- _deepseek#r6_: The statute requires the applicant to be an Estonian citizen (or EU citizen under certain conditions) and have full legal capacity. These facts are unknown and necessary to decide.

### `civil_service_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `ee_citizen`, `eu_citizen`, `full_capacity`, `secondary_education`, `speaks_estonian`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r5, gemini#r7, gemini#r1_: The applicant meets all the requirements for service under § 14 (1) and is not subject to any disqualifications listed in § 15.
- _gemini#r6, gemini#r8, gemini#r9, gemini#r0_: The applicant meets all the requirements of § 14 (1) as an Estonian citizen with secondary education, full legal capacity, and Estonian language proficiency. None of the disqualifications listed in § 15 apply, as the applicant has no criminal convictions and no family conflict with a supervising official.
- _openai#r0_: Under §14(1) the applicant qualifies as an official: Estonian citizen, at least secondary education, full legal capacity, and speaks Estonian at required level. None of the §15 disqualifications apply (no conviction for an intentional crime and no family conflict with a supervising official). Therefore the statute permits appointment.
- _openai#r1_: Applicant meets §14(1) requirements (Estonian citizen, secondary education, full legal capacity, required Estonian language ability) and is not barred under §15 (no intentional-crime conviction and no family conflict with supervising official).
- _openai#r2_: All statutory requirements of §14(1) are satisfied (Estonian citizen, at least secondary education, full legal capacity, required Estonian language skill) and none of the disqualifications in §15 apply (no conviction, no family conflict declared).
- _openai#r3_: All statutory requirements are met: applicant is an Estonian citizen, has at least secondary education, full legal capacity, and speaks Estonian as required (§14(1)). No disqualifying grounds under §15 apply (no conviction for an intentional crime and no family conflict with a supervising official).
- _openai#r4_: All statutory requirements are met: applicant is an Estonian citizen with at least secondary education, full legal capacity, and speaks Estonian at the required level (§14(1)), and is not barred by §15 (no intentional-crime conviction and no disqualifying family relation). Therefore hiring as an ametnik is permitted.
- _openai#r5_: All statutory hiring requirements in §14(1) are met (Estonian citizen, at least secondary education, full legal capacity, required Estonian language). No disqualifying conditions under §15 apply (no conviction for an intentional crime and no prohibited family relationship).
- _openai#r6_: Applicant meets §14(1) requirements (Estonian citizen, at least secondary education, full legal capacity, required Estonian language skill) and none of the §15 disqualifications apply (no criminal conviction and no family conflict with a supervising official).
- _openai#r7_: Applicant satisfies §14(1) requirements (Estonian citizen, at least secondary education, full legal capacity, speaks Estonian) and is not barred by §15 (no conviction, no family conflict), so hiring is permitted.
- _openai#r8_: All statutory requirements of §14(1) are met (Estonian citizen, secondary education, full legal capacity, required Estonian language skill) and no disqualifying conditions from §15 apply (no intentional conviction, no family conflict, etc.).
- _openai#r9_: Applicant meets §14(1) requirements (Estonian citizen, at least secondary education, full legal capacity, speaks Estonian) and none of the disqualifications in §15 apply (no conviction, no family conflict). Therefore hiring is permitted.
- _anthropic#r0, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r9_: The applicant meets all requirements under § 14(1): Estonian citizen (ee_citizen: true), full legal capacity (full_capacity: true), secondary education (secondary_education: true), and speaks Estonian at required level (speaks_estonian: true). The applicant satisfies all exclusion criteria under § 15: no criminal conviction (criminal_conviction: false) and no family conflict with supervising offic
- _anthropic#r1, anthropic#r8_: The applicant meets all requirements under § 14(1): Estonian citizen (ee_citizen: true), full legal capacity (full_capacity: true), secondary education (secondary_education: true), and speaks Estonian at required level (speaks_estonian: true). The applicant satisfies all disqualification criteria under § 15: no criminal conviction for intentional crime (criminal_conviction: false) and no family co
- _anthropic#r6, anthropic#r7_: The applicant meets all requirements under § 14(1): Estonian citizen (ee_citizen: true), full legal capacity (full_capacity: true), secondary education (secondary_education: true), and speaks Estonian at required level (speaks_estonian: true). The applicant satisfies all disqualification criteria under § 15: no criminal conviction (criminal_conviction: false) and no family conflict with supervisin
- _deepseek#r0, deepseek#r3, deepseek#r6_: Applicant meets all requirements: Estonian citizen, secondary education, Estonian language, full legal capacity, no criminal conviction, and no family conflict.
- _deepseek#r1_: Applicant meets all requirements under § 14(1) and none of the disqualifications under § 15 apply.
- _deepseek#r2, deepseek#r4, deepseek#r5, deepseek#r7, deepseek#r8, deepseek#r9_: Applicant meets all requirements: Estonian citizen, secondary education, Estonian language, full capacity, no criminal conviction, and no family conflict.

### `civil_service_u8_need_user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `no_conflict_declared`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r5, gemini#r0_: All requirements under § 14 (1) are met, and no disqualifying conditions under § 15 (1), (2), or (4) are present based on the provided facts and the user's declaration.
- _openai#r1_: All statutory requirements of §14(1) are met (Estonian citizen, secondary education, required Estonian, full legal capacity). None of the prohibitions in §15 apply: no conviction for an intentional crime and no family conflict with a supervising official. Therefore appointment is permitted.

### `consumer_withdrawal_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `distance_contract`, `is_consumer`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r5, gemini#r7_: The consumer has the right to withdraw from a distance contract within 14 days, provided the notice is sent in time and the contract does not fall under any excluded categories. All these conditions are met in this case.
- _gemini#r4, gemini#r6, gemini#r8, gemini#r9, gemini#r0, gemini#r1_: The consumer has the right to withdraw from the distance contract within 14 days, and all conditions for withdrawal are met, including timely notice and the absence of any exclusion categories.
- _openai#r6_: All statutory conditions are met: the contract was concluded by means of distance communication, the buyer is a consumer, the 14‑day withdrawal period is still running and the withdrawal notice was sent in time, and the laptop is not an excluded §53(4) category. §56 therefore permits withdrawal.

### `consumer_withdrawal_u5_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `is_consumer`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r5, gemini#r7, gemini#r0_: The consumer has the right to withdraw from a distance contract within 14 days, provided the contract does not fall under an excluded category. All conditions are met: the applicant is a consumer, the contract was concluded by distance means, the withdrawal notice was sent within the 14-day period, and the laptop is a standard catalogue model, meaning it does not fall into any of the excluded cate
- _openai#r1_: All statutory conditions for taganemine are met: the buyer is a tarbija (consumer), the contract was concluded by distance communication, the 14-day withdrawal period is still running and the notice was sent in time, and the laptop is not in a §53(4) excluded category (standard catalogue model). Therefore withdrawal is permitted under §56.
- _openai#r5_: You are a consumer, the contract was concluded by distance communication, the 14‑day withdrawal period is still running, you sent the withdrawal notice in time, and the laptop is not in an excluded category (§56(1), §56(2^1); exclusions in §53(4) do not apply). Thus the statute permits withdrawal.
- _openai#r9_: All statutory conditions for withdrawal are met: this is a distance (sidevahendi) contract, the 14-day withdrawal period is running and you sent timely notice, and the laptop is not in a §53(4) excluded category (standard catalogue model). Under §56(1) the consumer may withdraw within 14 days.

### `consumer_withdrawal_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `distance_contract`, `is_consumer`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r7, gemini#r9, gemini#r0, gemini#r1_: The consumer has the right to withdraw from the distance contract within 14 days, and all conditions for withdrawal, including timely notice and the absence of excluded categories, are met according to the statute.
- _gemini#r3, gemini#r4, gemini#r5, gemini#r6, gemini#r8_: The consumer meets all conditions for withdrawal under § 56 (1) and (2^1), as the contract was concluded by distance means, the consumer is a private individual, the 14-day period is still running, and the notice was sent in time. Furthermore, the subject of the contract (a standard catalogue laptop) does not fall under any of the exceptions listed in § 53 (4).
- _openai#r0_: Under §56(1) a consumer may withdraw from a distance contract within 14 days. The item (standard catalogue laptop) is not in the §53(4) exclusions, you are a consumer, the 14‑day period is running, and you sent the withdrawal notice in time, so withdrawal is permitted.
- _openai#r1_: All statutory conditions are met: you are a consumer, the contract was concluded by means of distance communication, the 14‑day withdrawal period is running, the item is not in a §53(4) excluded category, and you sent the withdrawal notice in time. Under §56(1) and (2^1) you may validly withdraw.
- _openai#r2_: Statute §56(1) gives the consumer the right to withdraw within 14 days; you are a consumer, the contract was concluded by distance means, the 14‑day term is running and you sent timely notice per §56(2^1)/(2^2). The item is not an excluded category under §53(4), so withdrawal is permitted.
- _openai#r3_: Tarbijal on §56 lg 1 järgi õigus 14 päeva jooksul lepingu taganeda; teade saadeti tähtajaks (§56 lg 2^1) ja lepingu predmet ei kuulu §53 lg 4 alusel välistatud kategooriasse, seega taganemine on lubatud.
- _openai#r4_: Under §56(1) the consumer may withdraw within 14 days; §56(2^1) confirms timely notice if sent within the period (notice_sent_in_time = true). The purchase is a distance contract and not in an excluded category (§53(4) exclusion = false). Therefore withdrawal is permitted.
- _openai#r5_: Under §56(1) a consumer may withdraw from a distance contract within 14 days. You are a consumer, the contract was concluded by distance means, the 14‑day term is running and you sent notice in time (§56(2^1)), and the item is not in the §53(4) exclusions. Therefore withdrawal is permitted.
- _openai#r6_: All required conditions are met: you are a consumer, the contract was concluded by distance communication, the 14‑day withdrawal period is running and you sent timely notice, and the laptop is not an excluded category under §53(4). Therefore withdrawal is permitted under §56.
- _openai#r7_: You are a consumer who concluded a contract by means of distance communication, the 14‑day withdrawal period is still running, you sent notice in time, and the item is not in a §53(4) excluded category — §56(1)–(2^1) therefore permits withdrawal.
- _openai#r8_: §56(1) grants the consumer a 14-day withdrawal right for distance contracts; §56(2^1) treats a timely-sent notice as timely (notice_sent_in_time = true). The item is not in a §53(4) excluded category (excluded_category = false). Therefore withdrawal is permitted.
- _openai#r9_: As a consumer in a distance contract you have the statutory right to withdraw within 14 days (§56(1)), you sent timely notice (§56(2^1)), and the laptop is not in an excluded category under §53(4); therefore withdrawal is permitted.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under § 56(1), a consumer may withdraw from a distance contract within 14 days without stating reasons. § 56(2^1) provides that timely withdrawal occurs when notice is sent to the seller within the withdrawal period. All conditions are satisfied: the applicant is a consumer (is_consumer: true), the contract was concluded by distance communication (distance_contract: true), the 14-day period is sti
- _deepseek#r0, deepseek#r1, deepseek#r8_: The consumer has a right to withdraw from a distance contract within 14 days, the notice was sent in time, and the contract is not excluded under § 53(4).
- _deepseek#r2, deepseek#r6_: The consumer has a right to withdraw from a distance contract within 14 days, the notice was sent in time, and the laptop is not in an excluded category.
- _deepseek#r3, deepseek#r5, deepseek#r7_: The consumer has a right to withdraw from a distance contract within 14 days, and the notice was sent in time. The contract is not excluded under § 53(4) because excluded_category is false.
- _deepseek#r4_: The consumer has a right to withdraw from a distance contract within 14 days, notice was sent in time, and the contract is not excluded under § 53(4).
- _deepseek#r9_: The consumer has a valid distance contract, is within the 14-day withdrawal period, sent notice in time, and the contract is not excluded under § 53(4).

### `db-then-user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `emergency`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 1 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 2 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 3 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 5 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 7 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 8 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 9 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 1 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 2 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 3 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 5 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 7 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 8 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 9 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _openai#r0_: Applicant is a parent but not sole custodian and both parents do not consent. The statute allows parental rights to information but access without the other parent's consent may only be justified in an emergency or if the other parent is unreachable; need to know whether 'emergency' or 'one_parent_unreachable' applies.
- _openai#r1_: Applicant is a parent (known true) and under §144 of the Perekonnaseadus a parent has the right to demand information from the other parent about important matters concerning the child. No sole custody, delegated decision right or both-parents’ consent is required for this right, so access to the child’s data is permitted.
- _openai#r2_: Applicant is a parent but has no sole custody, no delegated decision right and both parents do not consent. Under §120(2)–(3) a parent may act alone only if joint decision would cause harmful delay (e.g., an emergency) or similar justification (e.g., the other parent is unreachable). Need to know if an emergency exists or one parent is unreachable.
- _openai#r3_: Applicant is a parent. Under §120 a parent is the child’s legal representative and §144 expressly gives a parent the right to request information about the child from the other parent. No additional facts (e.g. emergency or other parent unreachable) are required to permit access to the child’s data on the given facts.
- _openai#r4_: A parent is a child’s legal representative only if they exercise hooldusõigus (custody) and, for joint custody, certain decisions require both parents’ consent or a court decision. You state you are a parent but do not have sole custody and do not have the other parent’s consent. The statute allows disclosure without the other parent’s consent in urgent/emergency situations or when the other paren
- _openai#r5_: Applicant is a parent. Perekonnaseaduse §144 gives a parent the right to require from the other parent information about the child’s person and property (unless disclosure would be contrary to the child’s interests or another legal restriction). No known facts indicate such a restriction, so access is permitted.
- _openai#r6_: Applicant is a parent and thus a legal representative of the child (see §120). Perekonnaseadus §144 expressly gives a parent the right to demand information from the other parent about the child’s person and property, unless providing the information would be contrary to the child’s interests. No facts here indicate such a restriction, so access is permitted on the known facts.
- _openai#r7_: Applicant is a parent but does not have sole custody or delegated decision-right and both parents do not consent. Under the Act parents with joint custody are joint legal representatives (§120) and one parent may act alone only in urgent situations or if the other parent cannot be reached. Whether access is permitted therefore depends on if there is an emergency or the other parent is unreachable.
- _openai#r8_: As a parent (applicant_is_parent=true) the applicant has a statutory right to information about the child. Perekonnaseaduse §144 grants a parent the right to request information on important matters relating to the child, and §§116–120 confirm parents’ equal rights and that a parent is a legal representative for the child. No facts indicating loss of parental/representation rights were given, so a
- _openai#r9_: Applicant is a parent (applicant_is_parent=true). Under §144 a parent has the right to demand information from the other parent about important matters concerning the child unless disclosure would be contrary to the child’s interests. No facts here show such a conflict or a legal restriction, sole custody, or delegated decision rights that would prevent the request.
- _anthropic#r0, anthropic#r3, anthropic#r8_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent or delegated decision rights. Under Perekonnaseadus § 120, parents with joint custody must act jointly in decisions about the child, unless one parent has been given specific decision-making authority or there is an emergency. To determine whether the parent can access the child's data unilat
- _anthropic#r1, anthropic#r2, anthropic#r4, anthropic#r6, anthropic#r7, anthropic#r9_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent or delegated decision rights. Under Perekonnaseadus § 120, parents with joint custody must act jointly in decisions about the child, unless one parent has been given specific decision-making authority or there is an emergency. To determine whether the parent can unilaterally access the child'
- _anthropic#r5_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent or delegated decision rights. Under Perekonnaseadus § 120, parents with joint custody must act jointly in representing the child, except in urgent matters or when one parent cannot be reached. To determine whether the applicant can unilaterally access the child's data, it is necessary to esta
- _deepseek#r0, deepseek#r1, deepseek#r4, deepseek#r6, deepseek#r9_: The statute allows a parent to act alone in urgent situations or if the other parent is unreachable, but these facts are unknown.
- _deepseek#r2_: The statute requires either an emergency or one parent being unreachable to allow a parent to act alone without the other parent's consent. These facts are unknown.
- _deepseek#r3, deepseek#r8_: The statute allows a parent to act alone in urgent situations or when the other parent is unreachable, but these facts are unknown.
- _deepseek#r5, deepseek#r7_: The statute allows a parent to act alone in emergencies or if one parent is unreachable, but these facts are unknown.

### `deny`

**Gold:** outcome `DENY`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 1 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 2 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 3 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 4 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 5 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 6 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 7 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 8 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 9 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 1 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 2 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 3 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 4 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 5 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 6 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 7 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 8 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 9 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 1 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 3 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 5 | NEED_MORE_INFO | NO | 0.00 | 1.00 | `emergency`, `one_parent_unreachable` |

Model reasoning (deduplicated):

- _openai#r1_: As the aunt you are not a parent, do not have delegated decision rights and do not have the parents' consent, so you lack legal authority to act as the child’s legal representative (see §120 and §174–176). Removal or decision-making without parental consent is only allowed in exceptional circumstances (e.g. child’s welfare endangered, emergency measures by authorities under §134–136) or if a paren
- _openai#r3_: An aunt who is not a parent and has no delegated decision right and no parents' consent generally cannot give the parental consent required (see §§152,155–156). There are narrow exceptions (e.g. if a parent is unreachable or in an emergency), so those facts are needed to decide.
- _openai#r5_: As the aunt (not a parent) without delegated decision right or both parents' consent, she has no general authority to act for the child. Court/authorities or appointment of a guardian may be possible only in special circumstances (e.g. an emergency or a parent being unreachable); those facts are unknown and required to decide.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: Under Estonian family law (Perekonnaseadus § 120), a child's legal representative is normally a parent with custody rights. The applicant is the child's aunt without delegated authority or parental consent. Section § 120(3) allows a non-custodial parent to make necessary decisions alone if delay would conflict with the child's interests, but this requires an emergency situation. Section § 120(5) p
- _deepseek#r0, deepseek#r1, deepseek#r4, deepseek#r6, deepseek#r7, deepseek#r8_: The statute requires either an emergency or one parent being unreachable for a non-parent to act without consent or delegated authority.
- _deepseek#r2, deepseek#r3, deepseek#r5_: The statute requires either an emergency or one parent being unreachable for a non-parent to act without delegated authority or parental consent.
- _deepseek#r9_: The statute allows a non-parent to make decisions for a child only in specific circumstances, such as an emergency or when one parent is unreachable. Since these facts are unknown, more information is needed.

### `journalism_allow_via_consent`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 1 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 2 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 3 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 4 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 5 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 6 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 7 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 8 | DENY | NO | 1.00 | 1.00 | (none) |
| anthropic | 9 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 1 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 2 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 3 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 4 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 5 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 6 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 7 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 8 | DENY | NO | 1.00 | 1.00 | (none) |
| deepseek | 9 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 1 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 3 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 4 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 5 | DENY | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r3, gemini#r4, gemini#r5, gemini#r0, gemini#r1_: The statute permits processing without consent for journalistic purposes only if there is public interest and it aligns with journalism ethics. According to the known facts, the processing does not have a journalistic purpose, there is no public interest, and it does not respect journalism ethics. Therefore, the conditions for processing under §4 are not met.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: The statute permits processing personal data without consent for journalistic purposes only if: (1) there is a journalistic purpose, (2) there is public interest, (3) it complies with journalism ethics principles, and (4) publication does not excessively harm the data subject's rights. The known facts show journalistic_purpose=false, public_interest=false, and journalism_ethics=false. Although the
- _deepseek#r0, deepseek#r2, deepseek#r4, deepseek#r5, deepseek#r7, deepseek#r8_: The statute requires journalistic purpose, public interest, and compliance with journalism ethics. Here, journalistic_purpose, public_interest, and journalism_ethics are all false, so the processing is not permitted despite consent and lack of excessive harm.
- _deepseek#r1, deepseek#r6_: The statute requires journalistic purpose, public interest, and compliance with journalism ethics. All three are false, so the processing is not permitted despite consent.
- _deepseek#r3_: The statute requires journalistic purpose, public interest, and compliance with journalism ethics. Here, journalistic_purpose is false, public_interest is false, and journalism_ethics is false, so the processing is not permitted despite consent and lack of excessive harm.
- _deepseek#r9_: The statute requires journalistic purpose, public interest, and compliance with journalism ethics. All are false, so the processing is not permitted despite consent.

### `journalism_need_user`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalism_ethics`, `public_interest`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 1 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 2 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 3 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 4 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 5 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 6 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 7 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 8 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| anthropic | 9 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 1 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 2 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 3 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 4 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 5 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 6 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 7 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 8 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| deepseek | 9 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| openai | 4 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| openai | 5 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |
| openai | 9 | NEED_MORE_INFO | YES | 0.67 | 1.00 | `public_interest`, `journalism_ethics`, `excessive_harm` |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r5, gemini#r6, gemini#r7, gemini#r8, gemini#r9, gemini#r0_: The processing is for a journalistic purpose, there is public interest, it adheres to journalistic ethics, and the reporting is proportionate, meaning it does not excessively harm the data subject's rights. The statute permits processing without consent under these conditions.
- _gemini#r4, gemini#r1_: The processing is for journalistic purposes, there is public interest, it follows journalism ethics, and the reporting is proportionate, meaning it does not excessively harm the data subject's rights. All conditions for processing without consent under § 4 are met.
- _openai#r0_: The processing is for a journalistic purpose, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject; under the statute consent is not required in these circumstances.
- _openai#r1_: Statute permits processing without consent for journalistic purposes where there is public interest, the reporting conforms to journalism ethics, and publication does not excessively harm the data subject. Here the processing is journalistic, the editor confirms avalik huvi and compliance with ajakirjanduseetika, and the reporting is proportionate (no excessive harm), so the statute permits the pu
- _openai#r2_: Statute permits processing without consent for journalistic purposes when there is public interest, it complies with journalism ethics, and it does not excessively harm the subject. The case facts state journalistic_purpose, public_interest, journalism_ethics and that the reporting is proportionate (no excessive_harm), so the processing is allowed.
- _openai#r3_: The statute permits processing without consent only if there is public interest, compliance with journalism ethics, and no excessive harm to the data subject. journalistic_purpose is true, but public_interest, journalism_ethics, and excessive_harm are unknown and required to decide.
- _openai#r4_: The statute allows processing without consent only if there is public interest, the processing complies with journalism ethics, and the disclosure would not excessively harm the data subject. Those three facts are not established in the known facts, so more information is required.
- _openai#r5_: The statute allows processing without consent only if there is public interest, it complies with journalism ethics, and it does not excessively harm the data subject. Those three factual elements are not given in the known facts and are required to decide.
- _openai#r6_: All statutory conditions are met: processing is journalistic (journalistic_purpose=true), there is public interest (public_interest asserted), the reporting respects journalism ethics (journalism_ethics asserted), and publication is proportionate so it does not unduly/excessively harm the data subject (excessive_harm=false). Therefore processing without the subject’s consent is permitted.
- _openai#r7_: All statutory conditions are met: processing is for a journalistic purpose, there is public interest, it complies with journalistic ethics, and publication would not excessively harm the data subject; consent is therefore not required.
- _openai#r8_: Statute permits processing without consent only if there is public_interest, it respects journalism_ethics, and publication does not excessively_harm the subject; those claims are unknown and required to decide.
- _openai#r9_: The statute allows non-consensual journalistic processing only if there is public interest, it complies with journalism ethics, and it does not excessively harm the data subject — those three facts are not provided.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: The statute permits processing without consent for journalistic purposes only if three conditions are met: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) publication does not excessively harm the data subject's rights. While journalistic_purpose is confirmed true and subject_consent is false (which is permitted), the three critical conditions—public_intere
- _deepseek#r0, deepseek#r1, deepseek#r2, deepseek#r3, deepseek#r4, deepseek#r5, deepseek#r6, deepseek#r7, deepseek#r8, deepseek#r9_: The statute requires public interest, compliance with journalism ethics, and no excessive harm. These facts are unknown.

### `journalism_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r5, gemini#r6, gemini#r7, gemini#r0, gemini#r1_: The statute permits processing without consent for journalistic purposes if there is public interest, it aligns with journalistic ethics, and does not excessively harm the data subject. All these conditions are met: the processing is for a journalistic purpose, there is public interest, journalistic ethics are followed, and there is no excessive harm. Consent is not required under these circumstan
- _gemini#r8, gemini#r9_: The statute permits processing without consent for journalistic purposes if there is public interest, it aligns with journalism ethics, and does not excessively harm the data subject. All these conditions are met: the processing has a journalistic purpose, there is public interest, journalism ethics are followed, and there is no excessive harm. The lack of subject consent is explicitly allowed by 
- _openai#r0_: All statutory conditions are satisfied: the processing has a journalistic purpose, there is public interest (public_interest = true), it respects journalism ethics (journalism_ethics = true), and publication would not excessively harm the data subject (excessive_harm = false). Therefore processing without the subject’s consent is permitted under the statute.
- _openai#r9_: All statutory conditions are met: processing is for a journalistic purpose, there is public interest (public_interest=true), it complies with journalism ethics (journalism_ethics=true), and disclosure would not excessively harm the data subject (excessive_harm=false). Consent is not required in these circumstances.

### `journalism_u5_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`, `subject_consent`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 2 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 3 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 4 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 5 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 6 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 7 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 8 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ERROR | — | — | — | Expecting ',' delimiter: line 1 column 1669 (char 1668) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| openai | 2 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r4, gemini#r6, gemini#r7, gemini#r9, gemini#r0_: The statute permits processing without consent for journalistic purposes if there is public interest, it aligns with journalism ethics, and does not excessively harm the data subject. All these conditions are met: the purpose is journalistic, there is public interest, journalism ethics are followed, and the reporting is not excessively harmful.
- _gemini#r3, gemini#r5, gemini#r8, gemini#r1_: The statute permits processing for journalistic purposes without consent if there is public interest, it aligns with journalistic ethics, and does not cause excessive harm. All these conditions are met according to the known facts and case request.
- _openai#r0_: All statutory conditions for processing without consent are met: the processing is journalistic, there is public interest, it follows journalism ethics, and publication would not excessively harm the data subject; consent is therefore not required.
- _openai#r1_: The statute permits processing without consent only for journalistic purposes when there is public interest, compliance with journalism ethics, and no excessive harm. public_interest, journalism_ethics, and excessive_harm are known to satisfy the statute, but journalistic_purpose is not provided — need that fact to decide.
- _openai#r2_: The statute allows non-consensual processing only when it is for a journalistic purpose. public_interest, journalism_ethics, and lack of excessive_harm are satisfied, but whether the processing is indeed journalistic_purpose is unknown and required to decide.
- _openai#r3_: Statute permits processing without the data subject’s consent for journalistic purposes when there is public interest, the reporting complies with journalism ethics, and publication does not excessively harm the subject. Those conditions are met (journalistic purpose, public_interest=true, journalism_ethics=true, excessive_harm=false). Consent is not required.
- _openai#r4_: Statute permits processing without consent for journalistic purposes when there is public interest, it complies with journalism ethics, and it does not excessively harm the data subject. Here: journalistic_purpose = true, public_interest = true, journalism_ethics = true, excessive_harm = false, so the processing is allowed.
- _openai#r5_: The statute permits processing personal data without the data subject's consent for journalistic purposes when there is public interest, it complies with journalism ethics, and it does not excessively harm the subject. The facts show journalistic purpose, public_interest=true, journalism_ethics=true and excessive_harm=false, so the processing is allowed.
- _openai#r6_: All statutory conditions for processing without consent are met: the processing is journalistic, there is public interest (true), it complies with journalism ethics (true), and publication will not excessively harm the data subject (false for excessive_harm). Consent is not required under these circumstances, so the statute permits the publication.
- _openai#r7_: The statute permits processing without consent only when the processing is for a journalistic purpose and the other conditions hold. public_interest, journalism_ethics and lack of excessive_harm are satisfied, but it is unknown whether the processing has a journalistic purpose.
- _openai#r8_: The statute permits processing without consent for journalistic purposes where there is public interest, it complies with journalism ethics, and it does not excessively harm the data subject. Here the processing is journalistic, public_interest=true, journalism_ethics=true, and excessive_harm=false, so the statute allows the publication (subject_consent is not required).
- _openai#r9_: The statute allows processing without the data subject’s consent for journalistic purposes where there is public interest, the processing complies with journalism ethics, and it does not excessively harm the subject. All these conditions are met here (journalistic_purpose, public_interest, journalism_ethics true; excessive_harm false).
- _anthropic#r0_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest (confirmed true), (2) it complies with journalism ethics principles (confirmed true), and (3) it does not excessively harm the data subject's rights (confirmed false - no excessive harm). The case facts establish all three permitting conditions are satisfied. Althoug
- _anthropic#r1_: The statute permits personal data processing for journalistic purposes without consent if there is public interest, journalism ethics are respected, and there is no excessive harm. Known facts confirm public_interest (true), journalism_ethics (true), and excessive_harm (false). However, journalistic_purpose is unknown and required to establish that the processing itself qualifies as 'ajakirjandusl
- _anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8_: The statute permits personal data processing without consent for journalistic purposes if there is public interest, journalism ethics are respected, and there is no excessive harm. Known facts confirm public_interest (true), journalism_ethics (true), and excessive_harm (false). However, journalistic_purpose is unknown and required to establish that the processing itself has a journalistic purpose 
- _anthropic#r9_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest (confirmed true), (2) it complies with journalism ethics principles (confirmed true), and (3) it does not excessively harm the data subject's rights (confirmed false - no excessive harm). The case facts establish all three conditions are satisfied. Although 'journali

### `journalism_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`, `subject_consent`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r5, gemini#r0_: The processing is for a journalistic purpose, there is public interest, it adheres to journalism ethics, and it does not excessively harm the data subject's rights, all of which are conditions for processing without consent under the statute.
- _gemini#r3, gemini#r4, gemini#r6, gemini#r7, gemini#r8, gemini#r9, gemini#r1_: The statute permits processing personal data for journalistic purposes without consent if there is public interest, it aligns with journalism ethics, and does not excessively harm the data subject's rights. All these conditions are met according to the known facts.
- _openai#r0_: All statutory conditions for processing without consent are met: the purpose is journalistic, there is public interest, the reporting follows journalism ethics, and publication will not excessively harm the data subject. Therefore the statute permits the processing.
- _openai#r1_: Statute permits processing without consent for journalistic purposes when there is public interest, it aligns with journalism ethics, and it does not excessively harm the data subject — all of which are satisfied on the known facts.
- _openai#r2_: All statutory conditions are met: processing is for a journalistic purpose, there is public interest, it complies with journalism ethics, and publication would not cause excessive harm to the data subject; consent is therefore not required.
- _openai#r3_: All statutory conditions are met: processing is journalistic, there is public interest, it complies with journalism ethics, and publication does not excessively harm the data subject; consent is not required under the statute.
- _openai#r4_: Statute permits processing personal data without consent for journalistic purposes when there is public interest, the reporting follows journalism ethics, and publication does not excessively harm the data subject. All required facts (journalistic_purpose, public_interest, journalism_ethics, excessive_harm=false) are satisfied.
- _openai#r5_: All statutory conditions are met: processing is for a journalistic purpose, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject. The statute permits processing without the subject's consent under these facts.
- _openai#r6_: All statutory conditions are met: processing is for a journalistic purpose, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject’s rights; consent is not required under §4 in these circumstances.
- _openai#r7_: All statute conditions are met: processing is journalistic, there is public interest, it complies with journalism ethics, and publication will not excessively harm the data subject; consent is not required under the statute.
- _openai#r8_: All statutory conditions are met: processing is journalistic, there is public interest, it complies with journalism ethics, and publication will not excessively harm the data subject. Consent is not required under the statute.
- _openai#r9_: All statutory conditions are met: processing is journalistic, there is public interest, it complies with journalism ethics, and publication would not excessively harm the data subject; consent is not required under the statute.
- _anthropic#r0, anthropic#r2, anthropic#r5, anthropic#r8, anthropic#r9_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, and excessive_harm=false. The absence of su
- _anthropic#r1_: The statute permits processing of personal data without subject consent (nõusolek) for journalistic purposes when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, and excessive_harm=false. The ab
- _anthropic#r3_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, subject_consent=false (not required), and e
- _anthropic#r4_: The statute permits processing of personal data for journalistic purposes without subject consent when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, excessive_harm=false, and subject_consent i
- _anthropic#r6_: The statute permits processing of personal data without subject consent (nõusolek) for journalistic purposes when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) publication does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, and excessive_harm=fals
- _anthropic#r7_: The statute permits processing of personal data without subject consent (nõusolek) for journalistic purposes when: (1) there is public interest, (2) it complies with journalism ethics principles, and (3) it does not excessively harm the data subject's rights. All four conditions are satisfied: journalistic_purpose=true, public_interest=true, journalism_ethics=true, and excessive_harm=false. The pr
- _deepseek#r0, deepseek#r1, deepseek#r2, deepseek#r4, deepseek#r7, deepseek#r8_: All required conditions are met: journalistic purpose, public interest, ethics, no excessive harm, and no consent needed.
- _deepseek#r3_: All required conditions are met: journalistic purpose, public interest, journalism ethics, no excessive harm, and consent is not required when public interest exists.
- _deepseek#r5_: The statute permits processing without consent if there is public interest, compliance with journalism ethics, and no excessive harm. All required conditions are met: journalistic purpose, public interest, ethics, and no excessive harm. Consent is not required.
- _deepseek#r6, deepseek#r9_: All required conditions are met: journalistic purpose, public interest, ethics, no excessive harm, and consent is not required.

### `land_tax_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `primary_residence_registered`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _openai#r2_: Under §11(1¹) an owner’s parcel with sihtotstarve=elamumaa qualifies as kodualuse maa. The municipality has set the exemption, the volikogu may grant the supplementary pensioner exemption under §11(5) when conditions in (1¹) are met, the applicant is a pensioner, and the application was submitted per §11(7). All required facts are true, so the exemption is allowed.
- _openai#r3_: Under §11(1^1) land with sihtotstarve elamumaa qualifies as kodualuse maa; §11(5) allows a municipality to grant a supplementary exemption to pension recipients; §11(7) requires a submitted application. Known facts show the parcel is residential land, the applicant is the owner, is a pension recipient, the municipality has set the exemption, and the application was submitted — so the statute permi
- _openai#r5_: All statutory conditions are met: the parcel is residential land (§1¹), the applicant is a pensioner, the municipality has set the supplementary exemption, and the applicant submitted the application per §7. Registered primary residence is not required for land with sihtotstarve elamumaa, so no additional facts are needed.

### `land_tax_u7_trust_only`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `applicant_is_owner`, `municipality_exemption_set`, `primary_residence_registered`, `residential_land`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 1 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 2 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 3 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 4 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 5 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 6 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 7 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 8 | DENY | NO | 1.00 | 0.00 | (none) |
| anthropic | 9 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 1 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 2 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 3 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 4 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 5 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 6 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 7 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 8 | DENY | NO | 1.00 | 0.00 | (none) |
| deepseek | 9 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 1 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 2 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 3 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 4 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 5 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 6 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 7 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 8 | DENY | NO | 1.00 | 0.00 | (none) |
| gemini | 9 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 0 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 1 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 2 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 3 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 4 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 5 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 6 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 7 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 8 | DENY | NO | 1.00 | 0.00 | (none) |
| openai | 9 | DENY | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r2, gemini#r3, gemini#r4, gemini#r9, gemini#r1_: The applicant does not receive a state pension, which is a requirement for the supplementary exemption under § 11(5). Additionally, the application for the supplementary exemption has not been submitted, as required by § 11(7).
- _gemini#r5, gemini#r6, gemini#r7, gemini#r8, gemini#r0_: The applicant does not receive a state pension, failing the eligibility criteria for the target group in §11(5)1. Additionally, the application for the supplementary exemption has not been submitted, which is required by §11(7).
- _openai#r0_: Although the land and residency conditions and the municipality exemption are met, paragraph 5 limits the additional exemption to pensioners and paragraph 7 requires an application. Known facts show the applicant does not receive a state pension and has not submitted the application, so the supplementary pensioner exemption is not permitted.
- _openai#r1_: Under §11(5) the supplementary exemption for pensioners applies only to persons who receive a state pension, and §11(7) requires submitting an application. Known facts show receives_pension = false and application_submitted = false, so the applicant does not meet the statutory eligibility and procedure requirements.
- _openai#r2_: Although the municipality has set the home-land exemption and the parcel meets the §11(1^1) conditions (residential land, primary residence registered, owner), the supplementary pensioner exemption under §11(5) requires being a pension recipient and, per §11(7), submitting an application. Known facts show receives_pension=false and application_submitted=false, so the supplementary pensioner exempt
- _openai#r3_: Paragraph 5 grants an additional exemption for pensioners, and paragraph 7 requires submitting an application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the supplementary pensioner exemption are not met.
- _openai#r4_: Although the parcel is residential, your primary residence is registered there, you own it, and the municipality set the exemption, the statute requires (a) that the person be a pensioner and (b) that they submit the supplementary-exemption application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the pensioner supplementary exemption
- _openai#r5_: The municipality has set the exemptions and the parcel meets kodualuse maa conditions, but paragraph 5 requires the recipient be a pensioner and paragraph 7 requires a submitted application. Known facts show receives_pension = false and application_submitted = false, so the supplementary pensioner exemption may not be granted.
- _openai#r6_: Although the parcel meets the kodualuse-maa criteria (residential land, owner, primary residence registered) and the municipality set the exemption, the additional pensioner exemption under §11(5) requires (a) that the applicant be a pension recipient and (b) that the applicant submit the required application per §11(7). The known facts show receives_pension = false and application_submitted = fal
- _openai#r7_: The additional (pensioner) exemption under §11(5) requires the person to be a pension recipient and, per §11(7), to submit an application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the supplementary pensioner exemption are not met.
- _openai#r8_: Under §11(5) the additional exemption may be granted to pensioners, and §11(7) requires submission of an application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the supplementary pensioner exemption are not met.
- _openai#r9_: Clause 5 limits the additional exemption to pension recipients and clause 7 requires a submitted application. Known facts show receives_pension = false and application_submitted = false, so the statutory conditions for the supplementary pensioner exemption are not met.
- _anthropic#r0, anthropic#r1, anthropic#r2, anthropic#r3, anthropic#r4, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: The applicant meets the conditions for the basic home-land exemption (residential land, primary residence registered, is owner, municipality exemption set). However, to qualify for the supplementary pensioner exemption under § 11(5)(1), the applicant must both (1) receive a state pension and (2) submit an application. The known facts show receives_pension = false and application_submitted = false.
- _deepseek#r0, deepseek#r1, deepseek#r2, deepseek#r5, deepseek#r6, deepseek#r7, deepseek#r8, deepseek#r9_: The applicant does not receive a state pension (receives_pension=false), so they do not qualify for the supplementary pensioner exemption under §11(5)(1).
- _deepseek#r3_: The applicant does not receive a state pension (receives_pension=false), so they do not qualify for the supplementary pensioner exemption under §11(5)(1). Also, the application was not submitted (application_submitted=false), but the substantive requirement fails regardless.
- _deepseek#r4_: The applicant does not receive a state pension, so they do not qualify for the supplementary pensioner exemption. Additionally, the application has not been submitted, but the pension requirement is not met.

### `need-db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `emergency`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 1 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 2 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 3 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 5 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 7 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 8 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| anthropic | 9 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 0 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 1 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 2 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 3 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 5 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 7 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 8 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| deepseek | 9 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 1 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 3 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 5 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 8 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| gemini | 9 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 1 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 2 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 3 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 4 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `emergency`, `one_parent_unreachable` |
| openai | 5 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 6 | NEED_MORE_INFO | YES | 0.50 | 1.00 | `one_parent_unreachable`, `emergency` |
| openai | 7 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 8 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 9 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r1, gemini#r3, gemini#r5, gemini#r6, gemini#r8, gemini#r9_: The applicant is a parent with joint custody, and the other parent's consent is not given. While parents with joint custody generally act in agreement (§ 118 (1)), one parent may act alone in the child's interests if a delay would be detrimental to the child's interests (§ 120 (3)). This could apply in an emergency or if the other parent is unreachable. Therefore, information on whether there is a
- _openai#r0_: Applicant is a parent. Perekonnaseaduse §144 gives a parent the right to require the other parent to provide information about the child’s person and property unless doing so would be contrary to the child’s interests. No facts here indicate the child’s interests bar disclosure, so the request is permitted.
- _openai#r1_: § 144 gives a parent the right to demand information about the child’s person and assets (unless contrary to the child’s interests). Applicant is a parent, so the statute permits access to the child’s data.
- _openai#r2_: Applicant is a parent. Under Perekonnaseadus §144 a parent has the right to demand information from the other parent about the child’s personal and property-related important circumstances unless disclosure would be contrary to the child’s interests. No facts here indicate such a prohibition, so access is permitted.
- _openai#r3_: Applicant is a parent (known true). Under §144 a parent has the right to require the other parent to provide information about the child’s person and property (unless disclosure would be against the child’s interests). Therefore access to the child’s data is permitted on the known facts.
- _openai#r4_: Applicant is a parent (legal representative) but parents have joint representation and other parent does not consent. Statute allows a single parent to act without the other only in urgent/exceptional situations (e.g. delay would harm the child or other parent is unreachable). Need to know whether an emergency exists or the other parent is unreachable to decide.
- _openai#r5_: Applicant is a parent. Under the Perekonnaseadus §144 a parent has the right to demand information about the child (unless disclosure would be contrary to the child’s interests or restricted by specific secrecy rules such as adoption secrecy). No facts indicating such a restriction are given, so access is permitted.
- _openai#r6_: Applicant is a parent but does not have sole custody or delegated decision right and the other parent does not consent. It is unclear whether an exception applies (emergency or the other parent being unreachable) that would permit access without both parents' consent; those facts are required to decide.
- _openai#r7_: §144 of the statute gives a parent the right to require from the other parent information about important matters concerning the child (person and property). That right does not require the other parent’s consent and is only limited if providing the information would be contrary to the child’s interests. On the known facts the applicant is a parent and there is no evidence that disclosure would be
- _openai#r8_: Applicant is a parent (known true) and under §144 a parent has the right to request information about the child’s person and property unless doing so would be contrary to the child’s interests. No facts show the child’s interests would be harmed, so access is permitted.
- _openai#r9_: Applicant is a parent. Under §144 a parent has the right to demand from the other parent information about the child; parents with custody are the child’s legal representatives (§120). No facts are given that disclosure would be contrary to the child’s interests or otherwise barred (e.g. adoption secrecy or court restriction), so access is permitted on the known facts.
- _anthropic#r0, anthropic#r1_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian family law (Perekonnaseadus § 120), parents with joint custody must act in agreement regarding important matters concerning the child. Access to child's data constitutes such an important matter. To determine if the applicant can unilaterally access 
- _anthropic#r2, anthropic#r3, anthropic#r6, anthropic#r7_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian family law (Perekonnaseadus § 120), parents with joint custody must act in agreement regarding important matters concerning the child. Access to the child's data would typically require either: (1) sole custody by the applicant, (2) delegation of dec
- _anthropic#r4_: Under Estonian family law (Perekonnaseadus § 120), a parent with joint custody can act alone in urgent matters affecting the child's interests if the other parent cannot be reached or if waiting for joint decision would cause harm. The applicant is a parent without sole custody and without delegated decision rights. To determine if access to child data is permitted, we need to establish whether: (
- _anthropic#r5_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian Family Law § 120, parents with joint custody must act in agreement regarding the child's representation and important matters. § 120(3) allows one parent to act unilaterally in emergencies or when the other parent is unreachable. The claims 'emergenc
- _anthropic#r8_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian family law (Perekonnaseadus § 120), parents with joint custody must act in agreement regarding the child's affairs. To determine whether the applicant can unilaterally access the child's data, it is necessary to establish whether: (1) there is an eme
- _anthropic#r9_: The applicant is a parent but does not have sole custody and there is no evidence of both parents' consent to access the child's data. Under Estonian family law (Perekonnaseadus § 120), parents with joint custody must act in agreement regarding important matters concerning the child. To determine whether the applicant can unilaterally access the child's data, it is necessary to establish whether: 
- _deepseek#r0, deepseek#r1, deepseek#r2, deepseek#r4, deepseek#r8_: The statute allows a parent to act alone in urgent situations or when the other parent is unreachable, but these facts are unknown.
- _deepseek#r3, deepseek#r6_: The statute allows a parent to act alone in emergencies or if the other parent is unreachable, but these facts are unknown.
- _deepseek#r5, deepseek#r7, deepseek#r9_: The statute allows a parent to act alone in urgent situations or if the other parent is unreachable, but these facts are unknown.

### `unrelated-law`

**Gold:** outcome `ALLOW`; missing facts: (none)

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 1 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 2 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 3 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 4 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 5 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 6 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 7 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 8 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| anthropic | 9 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 0 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 1 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 2 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 3 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 4 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 5 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 6 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 7 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 8 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| deepseek | 9 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| gemini | 0 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 1 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 2 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 3 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 4 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 5 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 6 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 7 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 8 | DENY | NO | 1.00 | 1.00 | (none) |
| gemini | 9 | DENY | NO | 1.00 | 1.00 | (none) |
| openai | 3 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| openai | 5 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| openai | 6 | DENY | NO | 1.00 | 1.00 | (none) |
| openai | 7 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| openai | 8 | NEED_MORE_INFO | NO | 1.00 | 1.00 | (none) |
| openai | 9 | DENY | NO | 1.00 | 1.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r1, gemini#r4, gemini#r5, gemini#r8, gemini#r9, gemini#r0_: The provided statute, 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Act on the Implementation of the Building Code and the Planning Act), pertains exclusively to planning and construction law. It contains no provisions or rules applicable to medical decisions for children, parental consent, or emergency medical situations. Therefore, this statute does not provide a legal basis to de
- _gemini#r2, gemini#r3, gemini#r6, gemini#r7_: The provided statute, 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Act on the Implementation of the Building Code and the Planning Act), pertains exclusively to building, planning, and related administrative procedures. It does not contain any provisions or rules regarding parental consent for medical decisions, emergency medical care for children, or situations where one parent is
- _openai#r3_: The provided statute governs planning and construction matters and contains no provisions on parental consent or medical decision-making for a child. Because the law excerpt is silent on whether a reachable parent may consent to urgent medical treatment when the other parent is unreachable, I cannot determine permissibility from this statute alone.
- _openai#r5_: The provided statute governs planning and construction matters and contains no rules on parental consent for medical treatment. There are no relevant unknown claim ids to resolve the question, so the statute does not permit a determination on whether the present parent may lawfully consent to urgent medical treatment for the child.
- _openai#r6_: The cited statute concerns planning and construction and contains no provision authorizing a parent to make medical decisions for a child in hospital or addressing emergency parental consent. On the given facts, the statute does not permit the requested act.
- _openai#r7_: The provided statute governs planning and construction and contains no rules on parental medical consent or emergency medical decision‑making. On the given facts (no unknown catalog claims), the statute does not permit or forbid the mother making a quick medical decision, so the matter cannot be decided from this statute alone.
- _openai#r8_: The cited statute concerns planning and construction and contains no provision on parental consent for medical treatment in emergencies. Based on the provided statutory text and known facts, the law as given does not resolve whether the mother may consent when the other parent is unreachable, so a decision cannot be made from this statute alone.
- _openai#r9_: The provided statute concerns planning and construction transitional rules and contains no provisions authorizing a parent to consent to medical treatment in an emergency when the other parent is unreachable. On the basis of this statute alone, the requested act is not permitted.
- _anthropic#r0, anthropic#r2, anthropic#r3, anthropic#r4_: This case request concerns medical decision-making for a child in an emergency situation. However, the provided statute is the Estonian 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Implementation Act of the Building Code and Planning Act), which governs construction, planning, and related administrative matters. This statute contains no provisions regarding parental consent for med
- _anthropic#r1, anthropic#r5, anthropic#r6, anthropic#r7, anthropic#r8, anthropic#r9_: This case request concerns medical decision-making for a child in an emergency situation. However, the provided statute is the Estonian 'Ehitusseadustiku ja planeerimisseaduse rakendamise seadus' (Implementation Act for the Building Code and Planning Act), which governs construction, planning, and related administrative matters. This statute contains no provisions regarding parental consent for me
- _deepseek#r0_: The statute provided does not address medical decisions for a child in an emergency. No relevant legal provision applies to the facts.
- _deepseek#r1, deepseek#r4, deepseek#r6, deepseek#r8_: The statute provided does not address medical decisions for a child in an emergency. No relevant legal provision applies to the request.
- _deepseek#r2_: The statute provided does not address medical decisions or parental consent in emergencies. No relevant legal provision applies to the described situation.
- _deepseek#r3_: The statute does not address medical decisions or parental consent for a child's treatment. The known facts (parent, emergency, other parent unreachable) do not map to any provision in the statute, which concerns construction and planning law. Therefore, the requested act is outside the statute's scope, and no decision can be made under it.
- _deepseek#r5_: The statute provided does not contain any provision about medical decisions for a child when one parent is unreachable. The known facts do not map to any statutory condition, and no unknown facts are listed. Therefore, the statute does not address the request, and more information is needed to determine if any other law applies.
- _deepseek#r7_: The statute provided does not address medical decisions for a child in an emergency. No relevant legal provision applies, so the request cannot be decided under this statute.
- _deepseek#r9_: The statute does not address medical decisions or parental consent for a child's treatment. The provided facts (parent, emergency, other parent unreachable) do not map to any provision in the statute, which concerns construction and planning. Therefore, the requested act is outside the statute's scope, and no decision can be made under it.

## Source `sota` — `experiments/results/scale-20260825/sota/experiment_ii_llm.jsonl`

- rows: 48 (48 scored); failed cells: 8 = 6 wrong outcome + 2 fact-set-only + 0 hard errors

### Wrong outcomes by provider and expected class

| provider | ALLOW | DENY | NEED_MORE_INFO |
|---|---|---|---|
| anthropic | 0/4 | 0/3 | 1/5 |
| deepseek | 0/4 | 0/3 | 2/5 |
| gemini | 0/4 | 0/3 | 2/5 |
| openai | 0/4 | 0/3 | 1/5 |

### `building_permit_u3_no_register`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `fee_paid`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |

Model reasoning (deduplicated):

- _gemini#r0_: The project conforms to the detailed plan and building requirements, was prepared by a competent designer, and includes the required site study, satisfying all statutory requirements for a building permit.
- _openai#r0_: Projekt vastab detailplaneeringule ja ehitusnõuetele, selle koostas pädev isik ning nõutav ehitusuuring on olemas. Ükski § 44 loetletud keeldumise alus ei esine; riigilõivu tasumine ei ole toodud sätetes ehitusloa andmise sisuline tingimus.
- _anthropic#r0_: The project conforms to the detailed plan and building requirements (§ 42(1)), and no refusal ground under § 44 applies: a competent designer prepared the project, the site study is available, and there is no plan violation. The state fee is not a statutory condition here (and was stated as paid anyway).
- _deepseek#r0_: The project conforms to the detailed plan, meets building requirements, was prepared by a competent designer, and a site study is provided. No grounds for refusal under § 44 are present. The unpaid fee is not a listed ground for refusal.

### `journalism_u5_need_db`

**Gold:** outcome `NEED_MORE_INFO`; missing facts: `journalistic_purpose`, `subject_consent`

| provider | repeat | model outcome | match | P | R | model missing facts |
|---|---|---|---|---|---|---|
| anthropic | 0 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |
| deepseek | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| gemini | 0 | ALLOW | NO | 1.00 | 0.00 | (none) |
| openai | 0 | NEED_MORE_INFO | YES | 1.00 | 0.50 | `journalistic_purpose` |

Model reasoning (deduplicated):

- _gemini#r0_: The statute permits processing personal data without consent for journalistic purposes if there is public interest, it aligns with journalism ethics, and it does not excessively harm the data subject. The facts confirm all these conditions are met.
- _openai#r0_: The consent-free exception requires a journalistic purpose. Public interest, compliance with journalism ethics, and absence of excessive harm are established; consent is not required under this exception.
- _anthropic#r0_: The statute permits processing without consent only if it is for a journalistic purpose, with public interest, ethics compliance, and no excessive harm. Public interest, ethics, and lack of excessive harm are established, and consent is unnecessary under this provision, but the journalistic purpose claim is not yet verified in the known facts.
- _deepseek#r0_: The statute permits processing without consent for journalistic purposes if there is public interest, compliance with journalism ethics, and no excessive harm. Known facts satisfy these conditions.

