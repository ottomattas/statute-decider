# Id aliases — old → new (rename of 2026-09-05)

Machine-readable source: `tools/rename_map.yaml`; applied by `tools/rename_ids.py`;
losslessness proven by `tools/fingerprint_results.py --compare` (row counts,
per-group outcome aggregates, and the canonical row multiset are identical
before and after). Everything produced before this date (`run.log`, chain logs,
the paper's pinned commit `0d28213`, ES notes) uses the **old** column.

## Conventions

| level | convention |
|---|---|
| statute | English act slug (`land_tax_act`) = `act_slug` in the legislation catalogue; the input is always the full act (Ruling G, 2026-09-05 evening) |
| provision | `<act_slug>/<eId>` — Akoma Ntoso-style eId (`sec_11__subsec_5__point_1`); display form `§ 11 (5) 1)`; see `docs/reference/legislation-corpus.md` |
| case | the citizen's service question |
| scenario | `<gold>_<mechanism>[_<distinguisher>]`; unique within a case; global id `<case>/<scenario>` |
| register | `<case>__<register>` — per-case forks kept for now (see "Registers") |
| condition | who does what: `solver-validation`, `llm-only`, `architecture`, `llm-decides-on-<inputs>-<specification>` |
| experiment | `<date>-<condition>[-smoke|-sota]` (no suffix = cheap grid × 10 repeats) |
| prompt | what the decider sees (`decide-raw-sources[-plus-rules]`) / which specification it gets (`solver-inputs-{partial-specification,full-procedure}`) |

Mechanism vocabulary (`scenario.mechanism`, fixed, cross-case): `claims_verified`
(claims + registers agree), `register_only` (no claims; registers resolve
everything), `alt_rule_claim_overrides_register` (a claim fires a second allow
rule that the registers alone would not), `own_admission` (statement against
interest fires a deny rule / defeater or blocks the allow path),
`no_allow_path` (a positive condition denied; no deny rule fires),
`register_silent` (a register field is missing), `user_silent` (a user-only
term is not stated), `register_down` (register unavailable), `trust_only`
(the only source is a trust-only self-report).

## Statutes

Two renames on 2026-09-05: the morning pass (v1 case names → act abbreviation + §§)
and the evening pass (Ruling G: → English act slugs, one per act, since the input is now
the whole act read from the XML corpus). `statute_id` / `statute_ids` in cases, oracle
JSONs and results `nodes/*.jsonl` carry the newest column; `tools/rename_ids.py
--scope statutes` applied the evening pass.

| v1 (before 2026-09-05) | morning 2026-09-05 | **current** | act |
|---|---|---|---|
| `building_permit` | `ehs_42_44` | `building_code` | Building Code (Ehitusseadustik); rules cite §§ 42, 44 |
| `civil_service_eligibility` | `ats_14_15` | `civil_service_act` | Civil Service Act (Avaliku teenistuse seadus); §§ 14–15 |
| `consumer_withdrawal` | `vos_53_56` | `law_of_obligations_act` | Law of Obligations Act (Võlaõigusseadus); § 53 (4), § 56 |
| `land_tax_exemption` | `mms_11` | `land_tax_act` | Land Tax Act (Maamaksuseadus); § 11 |
| `personal_data_journalism` | `iks_4` | `personal_data_protection_act` | Personal Data Protection Act (Isikuandmete kaitse seadus); § 4 |
| `section_120_demo` | `pks_120` | `family_law_act` | Family Law Act (Perekonnaseadus); § 120, § 118 (1) |
| — | — | `public_information_act` | Public Information Act (Avaliku teabe seadus); catalogue only, no case |

### Provision references (clause ids)

Before the evening pass a `clause_id` was an ad-hoc token (`mms_11_5_1`, `es_44_1`,
`ats_15_1`, `iks_4_harm`); now it is `<act_slug>/<eId>` and `clause_title` is the
display form the corpus renders. Old `clause_title` qualifiers that the display form
cannot carry ("first sentence", "implicit consent baseline") moved into the anchor's
`note` as `Cited as “…”.` Results `nodes/term_rule.jsonl` and `nodes/text_term.jsonl`
carry the new `clause_id`; their recorded `clause_title` strings are untouched.

| old `clause_id` | new `clause_id` | display |
|---|---|---|
| `mms_11_1` | `land_tax_act/sec_11__subsec_1` | § 11 (1) |
| `mms_11_1_1` | `land_tax_act/sec_11__subsec_1_1` | § 11 (1¹) |
| `mms_11_5_1` | `land_tax_act/sec_11__subsec_5__point_1` | § 11 (5) 1) |
| `mms_11_7` | `land_tax_act/sec_11__subsec_7` | § 11 (7) |
| `vos_53_4` | `law_of_obligations_act/sec_53__subsec_4` | § 53 (4) |
| `vos_56_1` | `law_of_obligations_act/sec_56__subsec_1` | § 56 (1) |
| `vos_56_2_1` | `law_of_obligations_act/sec_56__subsec_2_1` | § 56 (2¹) |
| `es_42_1` | `building_code/sec_42__subsec_1` | § 42 (1) |
| `es_44_1` / `es_44_2` / `es_44_3` | `building_code/sec_44__subsec_1__point_1` … `_3` | § 44 1) … 3) |
| `ats_14_1` / `ats_14_2` | `civil_service_act/sec_14__subsec_1` / `_2` | § 14 (1) / (2) |
| `ats_15_1` / `ats_15_4` | `civil_service_act/sec_15__subsec_1__point_1` / `_4` | § 15 1) / 4) |
| `iks_4`, `iks_4_harm` | `personal_data_protection_act/sec_4` | § 4 |
| `pks_118_1` | `family_law_act/sec_118__subsec_1` | § 118 (1) |
| `pks_120_1` / `_2` / `_3` | `family_law_act/sec_120__subsec_1` / `_2` / `_3` | § 120 (1) / (2) / (3) |

Full map: `tools/rename_map.yaml` (`clauses:`). Grammar and bijection to Riigi Teataja
element ids: `docs/reference/legislation-corpus.md`.

## Cases

| old | new |
|---|---|
| `building_permit` | `building_permit_grant` |
| `civil_service_eligibility` | `civil_service_admission` |
| `consumer_withdrawal` | `consumer_purchase_withdrawal` |
| `land_tax_exemption` | `land_tax_home_exemption` |
| `personal_data_journalism` | `journalistic_data_disclosure` |
| `section_120_demo` | `child_representation_by_one_parent` |

## Registers

Only the `<case>__` prefix changed. Structured fields (`register_id`,
`unavailable_registers[]`, `register_ids[]`, `register_overrides` keys, the
`record_term` mappings) carry the new id everywhere, including in the
result files. **Free text does not**: the `user` prompt strings in
`transcript.jsonl` (raw registry payload in `llm-only`, `register.record.field`
sources in `llm-decides-on-*`) and the rendered `justification`/`message`
strings in `nodes/outcome_trace.jsonl` still show the old id, because those
strings are the audit trail of what was sent and produced.

| old | new |
|---|---|
| `building_permit__building_registry` | `building_permit_grant__building_registry` |
| `building_permit__designer_registry` | `building_permit_grant__designer_registry` |
| `building_permit__designer_selfreport` | `building_permit_grant__designer_selfreport` |
| `building_permit__payment_ledger` | `building_permit_grant__payment_ledger` |
| `civil_service_eligibility__criminal_records_registry` | `civil_service_admission__criminal_records_registry` |
| `civil_service_eligibility__education_registry` | `civil_service_admission__education_registry` |
| `civil_service_eligibility__language_registry` | `civil_service_admission__language_registry` |
| `civil_service_eligibility__population_registry` | `civil_service_admission__population_registry` |
| `civil_service_eligibility__population_registry_selfreport` | `civil_service_admission__population_registry_selfreport` |
| `consumer_withdrawal__product_catalogue` | `consumer_purchase_withdrawal__product_catalogue` |
| `consumer_withdrawal__trader_crm` | `consumer_purchase_withdrawal__trader_crm` |
| `consumer_withdrawal__trader_selfreport` | `consumer_purchase_withdrawal__trader_selfreport` |
| `land_tax_exemption__applicant_selfreport` | `land_tax_home_exemption__applicant_selfreport` |
| `land_tax_exemption__land_registry` | `land_tax_home_exemption__land_registry` |
| `land_tax_exemption__municipality_records` | `land_tax_home_exemption__municipality_records` |
| `land_tax_exemption__population_registry` | `land_tax_home_exemption__population_registry` |
| `land_tax_exemption__social_insurance_registry` | `land_tax_home_exemption__social_insurance_registry` |
| `personal_data_journalism__consent_registry` | `journalistic_data_disclosure__consent_registry` |
| `personal_data_journalism__editorial_cms` | `journalistic_data_disclosure__editorial_cms` |
| `personal_data_journalism__editorial_selfreport` | `journalistic_data_disclosure__editorial_selfreport` |
| `section_120_demo__consent_service` | `child_representation_by_one_parent__consent_service` |
| `section_120_demo__custody_registry` | `child_representation_by_one_parent__custody_registry` |
| `section_120_demo__population_registry` | `child_representation_by_one_parent__population_registry` |

Duplicates of one real register, forked per case (v1 mock DBs were
case-scoped; merging them is Ruling D of
`docs/proposals/2026-09-02-input-side-renaming.md`, out of scope here):

- Rahvastikuregister (population registry): `civil_service_admission__population_registry`,
  `land_tax_home_exemption__population_registry`, `child_representation_by_one_parent__population_registry`.
- Self-report registers are case-local by design (`*_selfreport`), not duplicates.

## Scenarios

47 scenarios, n unchanged. Gold is the oracle `premise_outcome` (`state` → `scored_as`
where they differ). Tags: the pre-existing tags plus those added by the rename
(legend below).

| old | new | gold | mechanism | tags |
|---|---|---|---|---|
| `building_permit/building_permit_allow` | `building_permit_grant/allow_claims_verified` | ALLOW | `claims_verified` | `positive` |
| `building_permit/building_permit_allow_via_db` | `building_permit_grant/allow_register_only` | ALLOW | `register_only` | `positive`, `db-resolved`, `via_db` |
| `building_permit/building_permit_deny` | `building_permit_grant/deny_own_admission_plan_violation` | DENY | `own_admission` | `negative` |
| `building_permit/building_permit_deny_incompetent` | `building_permit_grant/deny_no_allow_path_designer_not_competent` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `building_permit/building_permit_deny_no_site_study` | `building_permit_grant/deny_no_allow_path_no_site_study` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `building_permit/building_permit_need_db` | `building_permit_grant/need_register_silent_fee` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `needs-info` |
| `building_permit/building_permit_u3_no_register` | `building_permit_grant/unverifiable_register_down_payment_ledger` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `uncertainty`, `u3` |
| `building_permit/building_permit_u7_trust_only` | `building_permit_grant/unverifiable_trust_only_designer_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `uncertainty`, `u7` |
| `civil_service_eligibility/civil_service_allow` | `civil_service_admission/allow_claims_verified` | ALLOW | `claims_verified` | `positive` |
| `civil_service_eligibility/civil_service_allow_eu_path` | `civil_service_admission/allow_alt_rule_eu_citizen_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | `positive`, `eu-path`, `scripted-claims` |
| `civil_service_eligibility/civil_service_deny` | `civil_service_admission/deny_own_admission_conviction` | DENY | `own_admission` | `negative` |
| `civil_service_eligibility/civil_service_deny_no_citizenship` | `civil_service_admission/deny_no_allow_path_no_citizenship` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `civil_service_eligibility/civil_service_need_db` | `civil_service_admission/need_register_silent_citizenship` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `needs-info` |
| `civil_service_eligibility/civil_service_u3_no_register` | `civil_service_admission/unverifiable_register_down_population_registry` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `uncertainty`, `u3` |
| `civil_service_eligibility/civil_service_u7_trust_only` | `civil_service_admission/unverifiable_trust_only_applicant_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `uncertainty`, `u7` |
| `civil_service_eligibility/civil_service_u8_need_user` | `civil_service_admission/need_user_silent_conflict_declaration` — **retired 2026-09-05** (files removed; see "Retired" below) | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info`, `u8` |
| `consumer_withdrawal/consumer_withdrawal_allow` | `consumer_purchase_withdrawal/allow_claims_verified` | ALLOW | `claims_verified` | `positive` |
| `consumer_withdrawal/consumer_withdrawal_allow_via_db` | `consumer_purchase_withdrawal/allow_register_only_consumer_status` | ALLOW | `register_only` | `positive`, `db-resolved`, `via_db` |
| `consumer_withdrawal/consumer_withdrawal_deny` | `consumer_purchase_withdrawal/deny_own_admission_custom_goods` | DENY | `own_admission` | `negative` |
| `consumer_withdrawal/consumer_withdrawal_deny_not_consumer` | `consumer_purchase_withdrawal/deny_no_allow_path_not_consumer` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `consumer_withdrawal/consumer_withdrawal_need_user` | `consumer_purchase_withdrawal/need_user_silent_deadline_and_notice` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info` |
| `consumer_withdrawal/consumer_withdrawal_u3_no_register` | `consumer_purchase_withdrawal/unverifiable_register_down_trader_crm` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `uncertainty`, `u3` |
| `consumer_withdrawal/consumer_withdrawal_u5_need_db` | `consumer_purchase_withdrawal/need_register_silent_consumer_status` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `needs-info`, `u5` |
| `consumer_withdrawal/consumer_withdrawal_u7_trust_only` | `consumer_purchase_withdrawal/unverifiable_trust_only_trader_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `uncertainty`, `u7` |
| `land_tax_exemption/land_tax_allow` | `land_tax_home_exemption/allow_claims_verified` | ALLOW | `claims_verified` | `positive` |
| `land_tax_exemption/land_tax_allow_pensioner` | `land_tax_home_exemption/allow_claims_verified_pensioner_supplement` | ALLOW | `claims_verified` | `positive`, `pensioner`, `extra` |
| `land_tax_exemption/land_tax_allow_via_db` | `land_tax_home_exemption/allow_register_only_ownership_and_residence` | ALLOW | `register_only` | `positive`, `db-resolved`, `via_db` |
| `land_tax_exemption/land_tax_deny` | `land_tax_home_exemption/deny_own_admission_not_owner` | DENY | `own_admission` | `negative` |
| `land_tax_exemption/land_tax_deny_not_residential` | `land_tax_home_exemption/deny_no_allow_path_not_residential` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `land_tax_exemption/land_tax_need_db` | `land_tax_home_exemption/need_register_silent_municipality_exemption` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `needs-info` |
| `land_tax_exemption/land_tax_u3_no_register` | `land_tax_home_exemption/unverifiable_register_down_population_registry` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `uncertainty`, `u3` |
| `land_tax_exemption/land_tax_u7_trust_only` | `land_tax_home_exemption/unverifiable_trust_only_applicant_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `uncertainty`, `u7` |
| `personal_data_journalism/journalism_allow` | `journalistic_data_disclosure/allow_claims_verified` | ALLOW | `claims_verified` | `positive` |
| `personal_data_journalism/journalism_allow_via_consent` | `journalistic_data_disclosure/allow_alt_rule_consent_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` | `positive`, `consent-baseline`, `scripted-claims` |
| `personal_data_journalism/journalism_deny` | `journalistic_data_disclosure/deny_own_admission_excessive_harm` | DENY | `own_admission` | `negative` |
| `personal_data_journalism/journalism_deny_no_basis` | `journalistic_data_disclosure/deny_no_allow_path_no_purpose_no_consent` | DENY | `no_allow_path` | `negative`, `no-basis`, `scripted-claims` |
| `personal_data_journalism/journalism_need_user` | `journalistic_data_disclosure/need_user_silent_editorial_judgements` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info` |
| `personal_data_journalism/journalism_u3_no_register` | `journalistic_data_disclosure/unverifiable_register_down_editorial_cms` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `register_down` | `uncertainty`, `u3` |
| `personal_data_journalism/journalism_u5_need_db` | `journalistic_data_disclosure/need_register_silent_purpose_and_consent` | NEED_REGISTER_INFO → NEED_MORE_INFO | `register_silent` | `needs-info`, `u5` |
| `personal_data_journalism/journalism_u7_trust_only` | `journalistic_data_disclosure/unverifiable_trust_only_editorial_selfreport` | UNVERIFIABLE_CLAIM → NEED_MORE_INFO | `trust_only` | `uncertainty`, `u7` |
| `section_120_demo/allow` | `child_representation_by_one_parent/allow_claims_verified_emergency` | ALLOW | `claims_verified` | `positive` |
| `section_120_demo/deny` | `child_representation_by_one_parent/deny_own_admission_not_parent` | DENY | `own_admission` | `negative` |
| `section_120_demo/db-then-user` | `child_representation_by_one_parent/need_user_silent_emergency_after_register_lookup` | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info`, `db-then-user` |
| `section_120_demo/need-db` | `child_representation_by_one_parent/need_user_silent_emergency_bare_request` — **retired 2026-09-05** (files removed; see "Retired" below) | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info` |
| `section_120_demo/need-user` | `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` — **retired 2026-09-05** (files removed; see "Retired" below) | NEED_USER_INFO → NEED_MORE_INFO | `user_silent` | `needs-info` |
| `section_120_demo/prompt-swap` | `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` — **retired 2026-09-05** (files removed; see "Retired" below) | ALLOW | `claims_verified` | `positive`, `extra`, `prompt-swap` |
| `section_120_demo/unrelated-law` | `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` — **retired 2026-09-05** (files removed; see "Retired" below) | ALLOW | `claims_verified` | `positive`, `extra`, `unrelated-law` |

Each scenario YAML's `provenance` ends with `renamed 2026-09-05 from <old case>/<old scenario>`.

### Retired 2026-09-05 (balanced suite, 54 = 18/18/18)

Files removed from `data/cases/**` on 2026-09-05; rows above kept for history. Results
produced before that date (all `experiments/2026090[1-4]-*` folders) still carry their rows.

| retired id | gold | why |
|---|---|---|
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_a` | ALLOW | byte-identical inputs to `allow_claims_verified_emergency` (v1 prompt-swap probe) |
| `child_representation_by_one_parent/allow_claims_verified_duplicate_probe_b` | ALLOW | byte-identical inputs to `allow_claims_verified_emergency` (v1 unrelated-law probe) |
| `child_representation_by_one_parent/need_user_silent_emergency_all_else_claimed` | NEED_USER_INFO | same gold `{emergency}` as `need_user_silent_emergency_after_register_lookup` (kept) |
| `child_representation_by_one_parent/need_user_silent_emergency_bare_request` | NEED_USER_INFO | same gold `{emergency}` as `need_user_silent_emergency_after_register_lookup` (kept) |
| `civil_service_admission/need_user_silent_conflict_declaration` | NEED_USER_INFO | the operator's "one more": single user-only term open after every register term resolves — the same shape as the kept § 120 scenario; the two-user-term variant survives in consumer and journalism, and civil service keeps `register_silent`, `register_down`, `trust_only` |

### Authored 2026-09-05 (no old id)

| id | gold | mechanism |
|---|---|---|
| `child_representation_by_one_parent/allow_register_only_sole_custody` | ALLOW | `register_only` |
| `child_representation_by_one_parent/allow_alt_rule_sole_custody_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` |
| `child_representation_by_one_parent/allow_alt_rule_delegated_right_overrides_register` | ALLOW | `alt_rule_claim_overrides_register` |
| `civil_service_admission/allow_register_only_citizenship` | ALLOW | `register_only` |
| `journalistic_data_disclosure/allow_register_only_purpose_from_cms` | ALLOW | `register_only` |
| `journalistic_data_disclosure/allow_register_only_consent_from_register` | ALLOW | `register_only` |
| `building_permit_grant/deny_register_only_plan_nonconformity` | DENY | `register_only` |
| `building_permit_grant/deny_no_allow_path_fee_unpaid` | DENY | `no_allow_path` |
| `civil_service_admission/deny_no_allow_path_no_estonian_language` | DENY | `no_allow_path` |
| `consumer_purchase_withdrawal/deny_no_allow_path_deadline_expired` | DENY | `no_allow_path` |
| `journalistic_data_disclosure/deny_no_allow_path_no_public_interest` | DENY | `no_allow_path` |
| `land_tax_home_exemption/deny_no_allow_path_municipality_not_set` | DENY | `no_allow_path` |


### Tag legend (history carried in `tags`)

| tag | meaning |
|---|---|
| `u3` | v1 utterance numbering: UNVERIFIABLE_CLAIM with reason `no_register` (register unavailable) |
| `u5` | v1: NEED_DB_INFO (now NEED_REGISTER_INFO) with no unavailability flag — the field is simply absent |
| `u7` | v1: UNVERIFIABLE_CLAIM with reason `trust_only` (only a self-report vouches) |
| `u8` | v1: NEED_USER_INFO — a user-only term is not stated |
| `via_db` / `db-resolved` | old id fragment `_via_db`: the utterance carries no (or only user-only) claims; registers resolve the rest |
| `no-basis` | DENY with no applicable rule: a positive condition is denied, no deny rule fires |
| `db-then-user` | old id of the PKS § 120 scenario the paper cites: registers resolve parent/custody, `emergency` stays open |
| `prompt-swap`, `unrelated-law` | old ids of two v1 probes (strict prompt path; unrelated-law extraction); in v2 both are duplicates of the allow scenario |
| `scripted-claims` | the oracle claim set did not follow from the request text as authored on 2026-09-01 (utterance said one thing, oracle claimed another); the plan's "10 scripted" set. See `docs/reference/faithful-inputs-audit-2026-09-05.md` for the fix |
| `extra` | outside the 2026-09-01 core (duplicate probes — retired 2026-09-05 — and the pensioner variant with inputs identical to `allow_claims_verified`, kept as one of the 18 ALLOW) |
| `positive` / `negative` / `needs-info` / `uncertainty` | 2026-09-01 gold buckets (ALLOW / DENY / NEED_* / UNVERIFIABLE_*) |
| `authored-20260905` | one of the twelve scenarios authored on 2026-09-05 to balance the suite (no old id; hand-verification sheet: `docs/reference/gold-review-2026-09-05.md`) |

## Conditions

| old | new | reading |
|---|---|---|
| `solver-validation` | `solver-validation` | oracle rules + oracle claims + register lookup; solver decides |
| `baseline` | `llm-only` | raw sources in; LLM decides and justifies |
| `llm-decider` | `llm-only-plus-rules` | raw sources + oracle rules; LLM decides |
| `candidate` | `architecture` | oracle rules, LLM-extracted claims (fused), lookup; solver decides |
| `candidate-staged` | `architecture-staged-grounding` | same; grounding in two calls (recognize, then value) |
| `llm-as-solver` | `llm-decides-on-oracle-inputs-partial-specification` | solver-validation inputs; LLM decides; prompt omits the claim/fact precedence rule |
| `llm-as-solver-v2` | `llm-decides-on-oracle-inputs-full-procedure` | same inputs; prompt states the solver's staged semantics |
| `llm-structured` | `llm-decides-on-llm-claims-partial-specification` | architecture minus the solver; partial specification |
| `llm-structured-v2` | `llm-decides-on-llm-claims-full-procedure` | architecture minus the solver; full procedure |

## Prompts

Files renamed only; content (and therefore the `prompt_hash` recorded in every
provenance block) is unchanged. `prompt_id` in `ledger.jsonl`, `transcript.jsonl`
`meta`, `nodes/*.jsonl` provenance and the config snapshots carries the new id.

| old | new |
|---|---|
| `premise_outcome/decide/decide-v1` | `premise_outcome/decide/decide-raw-sources` |
| `premise_outcome/decide/oracle-rules-v1` | `premise_outcome/decide/decide-raw-sources-plus-rules` |
| `premise_outcome/decide/solver-inputs-v1` | `premise_outcome/decide/solver-inputs-partial-specification` |
| `premise_outcome/decide/solver-inputs-v2` | `premise_outcome/decide/solver-inputs-full-procedure` |
| `utterance_term/ground/ground-v1`, `term_claim/value-v1`, `outcome_trace/justify/justify-v1` | unchanged (single versions) |

## Experiments

`experiment.yaml.name` equals the folder name; `experiment` in `rows.jsonl`,
`ledger.jsonl`, `transcript.jsonl` `meta` and the config snapshots was rewritten
to match. Every `experiment.yaml` got one `notes` line recording the rename.

| old folder | new folder |
|---|---|
| `20260901-baseline` | `20260901-llm-only` |
| `20260901-candidate` | `20260901-architecture` |
| `20260901-smoke-baseline` | `20260901-llm-only-smoke` |
| `20260901-smoke-candidate` | `20260901-architecture-smoke` |
| `20260901-solver-validation` | `20260901-solver-validation` |
| `20260903-candidate-staged` | `20260903-architecture-staged-grounding` |
| `20260903-llm-decider` | `20260903-llm-only-plus-rules` |
| `20260903-llm-as-solver` | `20260903-llm-decides-on-oracle-inputs-partial-specification` |
| `20260903-llm-structured` | `20260903-llm-decides-on-llm-claims-partial-specification` |
| `20260903-smoke-candidate-staged` | `20260903-architecture-staged-grounding-smoke` |
| `20260903-smoke-llm-as-solver` | `20260903-llm-decides-on-oracle-inputs-partial-specification-smoke` |
| `20260903-smoke-llm-decider` | `20260903-llm-only-plus-rules-smoke` |
| `20260903-smoke-llm-structured` | `20260903-llm-decides-on-llm-claims-partial-specification-smoke` |
| `20260903-sota-baseline` | `20260903-llm-only-sota` |
| `20260903-sota-candidate` | `20260903-architecture-sota` |
| `20260903-sota-llm-as-solver` | `20260903-llm-decides-on-oracle-inputs-partial-specification-sota` |
| `20260904-llm-as-solver-v2` | `20260904-llm-decides-on-oracle-inputs-full-procedure` |
| `20260904-llm-structured-v2` | `20260904-llm-decides-on-llm-claims-full-procedure` |
| `20260904-smoke-as-solver-v2` | `20260904-llm-decides-on-oracle-inputs-full-procedure-smoke` |
| `20260904-sota-llm-as-solver-v2` | `20260904-llm-decides-on-oracle-inputs-full-procedure-sota` |

## What was deliberately not rewritten

- `results/run.log`, `experiments/_chains/*.log`, `experiments/_chains/aborted/llm-decider-results-2323/`
  (an aborted partial run kept as history) — verbatim, old ids.
- `transcript.jsonl` `system` / `user` / `raw_response`; `nodes/outcome_trace.jsonl`
  `steps[].message` / `justification`; `nodes/premise_outcome.jsonl` `note`; any
  `provenance.notes`; `error` strings — the audit trail of what was sent and produced.
- Prompt file contents (hash-stable); free text in the historical docs under
  `docs/adr/`, `docs/reference/scenario-suite.md`, `docs/reference/nl-extraction.md`,
  `docs/refactor-v2-plan.md` (they describe the v1 tree and the 2026-09-01 design).
- The paper (`article.tex`) pins `0d28213`, whose tree has the old names; if the
  paper adopts the new names it must cite a post-rename commit and change the
  `db-then-user` caption to `need_user_silent_emergency_after_register_lookup`.
