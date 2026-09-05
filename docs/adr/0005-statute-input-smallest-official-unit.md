# ADR 0005: Statute input = the smallest official structural unit within a token budget

## Status

Accepted — 2026-09-06 (operator Ruling H)

## Context

Since Ruling G (2026-09-05) every prompt receives the whole act rendered from the
Riigi Teataja XML. Rendered sizes (tokens ≈ chars / 4): Law of Obligations Act
~316k, Building Code ~71k, Civil Service Act ~46k, Family Law Act ~45k, Personal
Data Protection Act ~20k, Land Tax Act ~6k. The Law of Obligations Act does not fit
the 200k context of the smallest configured model (haiku-4.5), and a 316k-token
prefix is a needless cost on the 1M-context models. Cutting the text by hand
(a slice of the declared provisions) would decide for the model which provisions
matter — the very question the llm-only baseline is asked.

## Decision

The statute text a model receives is an **official unit of the act**, chosen
deterministically (`legislation/units.py`):

1. the whole act, when its token estimate fits `max_statute_tokens`;
2. otherwise the **smallest** structural unit — part, chapter, division,
   subdivision, sub-subdivision, whichever the XML has (the five RT unit elements
   `riigiteataja.Act._walk_body` maps to `part`/`chp`/`dvs`/`subdvs`/`subsubdvs`;
   element names in `docs/reference/legislation-corpus.md`) — that encloses every provision the statute's `statute.yaml` declares
   (innermost common ancestor; `Act.enclosing_units`);
3. if even that unit exceeds the budget, `UnitTooLarge` — the harness never cuts
   official text on its own; the operator resizes the budget or the model grid.

Rendering (`Act.render_unit`) reuses the whole-act renderer: act header, a
`Structural unit: Part 1 GENERAL PART › Chapter 2 CONTRACT › Subchapter 4
Distance Contracts` breadcrumb, then the unit's own heading, nested unit headings
and every section with its official `§ N.`, `(n)`, `n)` numbering exactly as the
XML text has it. Structural units are addressed by their path eId
(`part_1__chp_2__dvs_4`; `references.parse_eid` accepts strictly descending
structural chains) because level-local numbers restart inside each parent.

**Token estimate:** `ceil(chars / 4)` — deterministic, offline, no tokenizer
dependency; the ledger keeps the vendor's real count per call beside it.

**Budget:** one number, `max_statute_tokens` on `experiment.yaml`
(`DEFAULT_MAX_STATUTE_TOKENS = 100 000`). Chosen so that every act except the Law
of Obligations Act stays whole (Building Code ~71k must fit) and so that budget +
prompt margin (8k: instructions, utterance, catalogue/rules, schema) +
`max_output_tokens` (8 192) fits the smallest context window on the grid.
Context windows are now recorded per model in `configs/llm/models.yaml`
(`context_tokens`, vendor pages linked, verified 2026-09-06): haiku-4.5 200k,
gpt-5-mini 400k, all others ≥ 1M. The runner logs a warning when a grid's
smallest window cannot take the budget.

**Provenance:** every row carries `statute_input = {act, global_id, sha256,
unit: {kind, eid | "act", display}, declared_provisions, method, chars,
tokens_estimate, max_tokens}`; the same record rides on every ledger line
(`meta.statute_input`) and in the `statute_text` node value. It replaces
`statute_source` (rows before 2026-09-06 keep the old key; not rewritten).

## Consequences

- Result under the default budget (`sd statute-input --candidates`):

  | act | unit | tokens |
  |---|---|---|
  | building_code | act | 70 518 |
  | civil_service_act | act | 46 437 |
  | family_law_act | act | 45 068 |
  | land_tax_act | act | 5 808 |
  | law_of_obligations_act | `part_1__chp_2__dvs_4` — Part 1 GENERAL PART › Chapter 2 CONTRACT › Subchapter 4 Distance Contracts (§§ 52–62) | 13 095 |
  | personal_data_protection_act | act | 19 648 |

  Only the Law of Obligations Act drops below the act, to the division the ruling
  anticipated (the English text labels `jagu` "Subchapter"; the eId level is `dvs`).
- The llm-only conditions become runnable on every configured model; the
  cacheable statute prefix for the LOA case shrinks from ~316k to ~13k tokens.
- `experiment.yaml` gains `max_statute_tokens` (template updated); `StatuteText`
  gains `unit`, `tokens_estimate`, `max_tokens` and `method: unit`.
- Tests: `tests/test_statute_units.py` (path eIds, nesting, common ancestor,
  rendering, whole/unit/too-large selection, the per-act table);
  `tests/test_data_validates.py` asserts the expected method per act.
- Not changed: `statute_text: slice` (the declared-provisions ablation) and the
  committed `statute.rendered.txt` artefacts.
