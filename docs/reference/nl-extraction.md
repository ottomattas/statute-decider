# NL User-Input Extraction (Step 00)

## Overview

Step 00 turns short natural-language utterances from the applicant (or an
intake officer) into a structured `UserInputSession` that feeds the rest
of the `framework` pipeline. It is the entry point for Track C of the
post-17 Apr plan (Linear ART-66, parent ART-60): a separate workstream
from "law → rules", matching Priit's 17 Apr ask to start deterministic
and layer LLMs on top.

The deterministic path is authoritative and must not silently deny: any
claim the utterances do not ground is left unresolved, which the reasoner
then surfaces as a U5 (`NEED_DB_INFO`) or U8 (`NEED_USER_INFO`) follow-up
rather than a default `false`.

Plan reference: Track C in the `post-17apr-research-push` plan.

## Artifacts

- Module: `framework/user_input.py` — pure library, no `google.genai`
  import at module load.
- CLI: `framework/00_collect_intent.py` — numbered entry point that runs
  before `framework/01_extract_intent.py`.
- LLM helpers: `UserInputExtractionItem`, `UserInputExtractionResponse`,
  and `build_user_input_prompts` in `framework/llm.py`.
- Shared prompts: `framework/prompts/user_input/{system,user}.propositional.txt`.
- Per-case prompts: `framework/examples/<case>/prompts/user_input/system.propositional.txt`.
- Per-case fixtures: `framework/examples/<case>/user_input/utterances_{allow,deny,needs_user}.json`.

## Data model

Three Pydantic models in `framework/user_input.py`:

| Model | Purpose |
|---|---|
| `UserUtterance` | One free-form utterance: `text`, `source` ("user" / "officer" / "chat"), optional `timestamp_utc`. |
| `ClaimResponse` | One claim-level response: `claim_id`, `value: bool \| None`, `confidence`, `evidence: list[EvidenceSnippet]`, `needs_user_confirmation`. |
| `UserInputSession` | Aggregate: `use_case_id`, `utterances`, `responses`, `unresolved_claim_ids`. |

`ClaimResponse.evidence` reuses the existing `EvidenceSnippet` schema
from `framework/schemas.py`, so provenance flows through to step 01
without schema drift.

## Deterministic extractor

`extract_user_input_deterministic(use_case, utterances) -> UserInputSession`
applies a small, auditable lexical policy:

1. For each fragment in each utterance, check `request_mentions_claim`
   (from `framework/use_case_files.py`) against every claim template.
2. Classify the fragment along four axes: `unknown`, `hedge`, `negation`,
   `affirmation`. Negation only counts when it sits *outside* the keyword
   match span, so cues like "no family conflict" stay positive.
3. Collapse all matching fragments for one claim into a single response:
   - `I don't know` / `no idea` / `unknown` → `value=None`,
     `needs_user_confirmation=False`, `confidence=0.0`.
   - `I think` / `maybe` / `not sure` near the cue → `value=None`,
     `needs_user_confirmation=True`, `confidence=0.3` (the U8 trigger).
   - Negation near the cue with no affirmation → `value=False`.
   - Plain affirmation ("I am", "I have", "we did") → `value=True`.
   - Fallback cue match with no polarity signal → `value=True`,
     `confidence=0.7`.
4. Any claim id with no matching fragment at all is listed in
   `unresolved_claim_ids` (the U5 signal).

## LLM extractor (behind `--llm`)

`extract_user_input_llm(use_case, utterances, *, use_case_dir, logic_level,
generator=gemini_structured_completion, model=None, api_key=None)` calls
`build_user_input_prompts` from `framework/llm.py` and expects a
`UserInputExtractionResponse`. The helper lazy-imports the `llm` module
so `google.genai` is never loaded on the deterministic path.

System prompts are resolved with per-case override:

1. `framework/examples/<case>/prompts/user_input/system.<level>.txt`
   (preferred when present).
2. `framework/prompts/user_input/system.<level>.txt` (fallback).

The user prompt template lives at
`framework/prompts/user_input/user.txt` and is shared across cases.

## Bridge into step 01

`session_to_intent_assignments(session)` returns exactly the tuple shape
accepted by `build_intent_artifact`:

```python
assignments, reasons, snippets = session_to_intent_assignments(session)
intent = build_intent_artifact(
    use_case=use_case,
    request_text=request_text,
    logic_level=LogicLevel.PROPOSITIONAL,
    assignments=assignments,
    reasons=reasons,
    snippets=snippets,
)
```

`reasons[claim_id]` carries a `needs_user_confirmation=true` marker for
every hedged response so the downstream reasoner or UI layer can emit a
U8 follow-up question without re-deriving the signal.

## CLI

```bash
python framework/00_collect_intent.py \
    --use-case-dir framework/examples/land_tax_exemption \
    --utterances-file framework/examples/land_tax_exemption/user_input/utterances_allow.json \
    --out session.json \
    --request-text-out request.txt

python framework/01_extract_intent.py \
    --use-case-dir framework/examples/land_tax_exemption \
    --text-file request.txt \
    --out intent.json
```

Key flags:

| Flag | Purpose |
|---|---|
| `--use-case-dir` | Use-case directory (required). |
| `--utterances-file` | JSON file holding a list of `UserUtterance` entries (required). |
| `--out` | Where to write the session JSON (required). |
| `--logic-level` | Used to resolve the per-case system prompt (LLM path only). |
| `--llm` | Opt in to the LLM extractor. Off by default. |
| `--model`, `--api-key` | Gemini overrides, forwarded to the LLM helper. |
| `--request-text-out` | Optional concatenated NL request file that step 01 consumes. |

Stdout prints a short per-category summary (resolved true/false,
unresolved_mentioned, needs_confirmation, not_mentioned). The `--llm`
path and the deterministic path share this output shape.

## U5 / U8 routing

Unresolved claims flow into the solver's existing uncertainty routing:

- `unresolved_claim_ids` (no utterance mentioned the claim) — the reasoner
  treats them as `None` and then classifies them via
  `framework/uncertainty_routing.py`. DB-sourced claims get U5
  (`NEED_DB_INFO`); user-sourced claims get U8 (`NEED_USER_INFO`).
- `needs_user_confirmation=True` responses (hedged mentions) — the intent
  artifact carries `value=None` plus a reason string starting with
  `needs_user_confirmation=true;...`, which the UI can use to prompt the
  user for a firm yes/no. This is the explicit U8 trigger path.

## Fixtures and tests

Each of the five Wave 1/2 target domains ships with three utterance
fixtures under `framework/examples/<case>/user_input/`:

- `utterances_allow.json` — grounds the positive path.
- `utterances_deny.json` — grounds at least one denying claim.
- `utterances_needs_user.json` — leaves some claims unmentioned (U5) and
  includes at least one hedged utterance (U8).

Two test modules (both fully offline):

- `framework/tests/test_user_input.py` — deterministic coverage per
  domain, hedge detection, negation handling, "no family conflict" cue
  non-negation, explicit-unknown handling, and the bridge shape. The
  LLM path is exercised with an in-memory fake generator.
- `framework/tests/test_00_collect_intent.py` — CLI end-to-end on one
  domain, `--help` sanity, and the needs_user fixture behaviour.

Run the full suite from the repo root:

```bash
source framework/venv/bin/activate
python -m unittest discover -s framework/tests -v
```

## See also

- `docs/reference/schema.md` — full U1..U12 routing table.
- `docs/reference/reasoner.md` — backend dispatcher side.
- `docs/reference/scenario-suite.md` — expected-vs-actual harness.
