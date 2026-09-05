# Proposal: input-side renaming, restructure, and a balanced scenario suite

Status: **Rulings A–C executed 2026-09-05** on branch `feat/rename-and-faithful-inputs`
(`tools/rename_map.yaml`, `tools/rename_ids.py`, alias tables in
`docs/reference/id-aliases.md`; results migrated in place, numbers byte-identical).
**§ 3 (balanced suite) executed 2026-09-05** as the operator's "Ruling F — balanced gold"
(54 = 18/18/18; five retired, twelve authored; `docs/reference/gold-review-2026-09-05.md`),
together with "Ruling E — English only" of the same brief (all model-visible and
reader-visible strings in English; statute texts from the official Riigi Teataja
translations, interim snippets pending XML slicing). Those two brief labels are not
the § 2 Rulings E/F below (services source family; human+machine pairing), which
remain proposals. Ruling D (shared registers) remains open. Original text:
nothing renamed yet. The paper pins commit `b65d091`;
execute this after the JURIX submission (or on a branch that does not touch
the pinned history). Operator sign-off needed on the rename table before any
`git mv`.

## 1. What is wrong today

- **Case ids are opaque.** `section_120_demo` says nothing about the service;
  `civil_service_u8_need_user` carries v1 jargon (`u3/u5/u7/u8` were utterance
  numbering in the pre-refactor repo) that no longer means anything.
- **Scenario ids mix outcome, mechanism, and history.** `land_tax_allow_via_db`
  vs `land_tax_u3_no_register`: same axis, two vocabularies.
- **Register ids duplicate reality.** `land_tax_exemption__population_registry`
  and `civil_service_eligibility__population_registry` are the same real-world
  register, forked per case because v1 mock DBs were case-scoped.
- **47 scenarios is an accident of history** (v1 accumulated them), not a
  design: the outcome classes are unbalanced, which complicates per-class F1
  and makes "accuracy" partly a class-prior artifact.
- **Where do I select them?** Today: `experiment.yaml` → `cases:` (list of
  case ids or `all`); scenario selection is implicit (all scenarios of a
  case). There is no `sd list` to browse the inventory.

## 2. Naming rulings (proposed)

**Ruling A — official documents keep official names.** Statute directories are
named by the Riigi Teataja act abbreviation plus paragraph, e.g. `mms_11`
(Maamaksuseadus § 11), `ats_14` (Avaliku teenistuse seadus § 14). The
`statute.yaml` sidecar carries the full official title and the RT link; the
`statute.txt` is the official excerpt. Nothing invented, directly greppable
against the law.

**Ruling B — cases are named after the citizen's service question.** A case id
answers "what is the person asking for": `land_tax_home_exemption`,
`civil_service_admission`, `consumer_purchase_withdrawal`,
`building_permit_grant`, `journalistic_data_disclosure`. (Exact table below,
TBD confirm; `section_120_demo` needs a real service name.)

**Ruling C — scenario ids are `<outcome>_<mechanism>`.** The outcome bucket
first, the distinguishing mechanism second: `allow_registry_confirms`,
`allow_uncovered_claim`, `deny_own_admission`, `deny_no_allow_path`,
`need_user_silent`, `need_register_silent`, `unverifiable_trust_only`,
`unverifiable_register_down`. History (u-numbers, "via_db") moves to `tags`
and `provenance`. Scenario ids are unique within a case only; global id stays
`<case>/<scenario>`.

**Ruling D — real registers become shared, first-class.** One directory per
real register (`population_registry`, `land_registry`,
`social_insurance_registry`, ...), shared across cases; per-case mock records
stay where they are today (`data/cases/<case>/sources/registry.json`). Purely
case-local sources (self-reports, a trader's CRM) keep a case prefix.

**Ruling E — services are a new source family.** Adopt the teaching package's
`data/services/<service_id>/service.yaml` (Semantic Service Contract) as a
first-class source: `service_record` joins `statute_text` / `user_utterance` /
`registry_record` as the fourth chain when student-collected services arrive.
The `legal_mapping` block (term_id + clause + register_id per condition) is
the bridge into the existing graph.

**Ruling F — human+machine pairing (proposed, discussion held for later).**
Every machine-readable artifact keeps a human-readable counterpart, authored
first and kept in translation with it (the teaching pack demonstrates the
pattern: `service-description.md` ↔ `service.yaml`, with an explicit
sentence↔field translation table). Rationale beyond pedagogy: when an agent
acts under delegation, the human behind it must be able to inspect, in plain
language, the service, the conditions, and what was done on their behalf —
so names, descriptions, and traces should ship in both registers.
Open questions to settle before adopting repo-wide: which artifacts are in
scope (services certainly; term catalogues and rules plausibly; oracle files
probably not), where the counterpart lives (sidecar `.md` next to each file
vs generated view), and whether the pairing is enforced (a validation step
that fails when the translation table has gaps) or advisory. Decide at the
same sitting as the rename execution; do not block it.

### Rename table (draft — confirm before executing)

| today | proposed | note |
|---|---|---|
| `section_120_demo` | TBD (name the actual service) | statute → its real act § |
| `land_tax_exemption` | `land_tax_home_exemption` | statute → `mms_11` |
| `civil_service_eligibility` | `civil_service_admission` | statute → `ats_14` (confirm §) |
| `consumer_withdrawal` | `consumer_purchase_withdrawal` | statute → `vos_56` (confirm §) |
| `building_permit` | `building_permit_grant` | statute → `ehs_..` (confirm §) |
| `personal_data_journalism` | `journalistic_data_disclosure` | statute → `iks_..` (confirm §) |

## 3. Balanced scenario suite (proposed)

Design instead of history: every case gets the **same nine-scenario menu**,
three per scored class, mechanisms standardized so cross-case analysis is
per-mechanism, not per-anecdote:

| scored class | mechanisms (3 each) |
|---|---|
| ALLOW | `allow_registry_confirms`, `allow_claim_verified`, `allow_uncovered_claim` |
| DENY | `deny_rule_fires`, `deny_own_admission`, `deny_no_allow_path` |
| NEED_MORE_INFO | `need_user_silent`, `need_register_silent`, `unverifiable_trust_only` |

Six benchmark cases × 9 = **54 scenarios, perfectly balanced 18/18/18** at the
scored 3-class level, with the finer states (NEED_USER / NEED_REGISTER /
UNVERIFIABLE) each represented once per case. Mechanisms that don't fit a
case honestly (e.g. no trust-only register exists) get authored rather than
faked — that is exactly the kind of scenario the current 47 lack. A tenth
slot per case stays open for case-specific oddities (tagged `extra`, excluded
from the balanced core by tag).

Benefits: accuracy comparable across classes, per-class F1 stable, every
warrant mechanism measured on every case, and the count argument ("why 47?")
disappears — 54 is a design, not a residue.

## 4. Execution plan (post-submission)

1. Freeze: confirm the rename table and the nine-mechanism menu (operator).
2. Write `tools/rename_map.yaml` (old id → new id, all levels: statutes,
   registers, cases, scenarios, terms untouched).
3. One script does the whole move: `git mv` directories, rewrite ids inside
   YAML/JSON (they are all schema-validated, so a load→rename→dump pass is
   safe), regenerate `docs/matrix.csv`.
4. Author the missing scenarios up to the 9-menu per case; oracle files per
   the teaching-package recipe; `pytest` gate (`test_solver_validation`
   grows from 47 to 54).
5. Add `sd list` (cases, scenarios, tags, outcome distribution) so selection
   is visible from the CLI, not just the filesystem.
6. Only then: rerun committed conditions; the paper keeps citing `b65d091`.

Nothing in this plan touches produced results or the pinned commit; it is a
data-plane refactor with a deterministic mechanical step and a bounded
authoring step (7 new scenarios per case on average).
