# Documentation

This directory is the canonical home for project documentation.

## Reading order

1. `architecture/overview.md` for the system structure and the separation between model, state, reasoning, and governed evolution.
2. `reference/schema.md` for the public object model.
3. `reference/reasoner.md` for staged evaluation semantics.
4. `guides/development.md` for local setup and validation.
5. `adr/` for durable architecture decisions.

## Canonical structure

- `architecture/` — system structure, data flow, and design rationale
- `reference/` — public schema and reasoner semantics; see also `reference/nl-extraction.md` for the step-00 user-input extractor
- `guides/` — local setup and validation
- `adr/` — architecture decision records

## Maintenance rules

- Update a canonical document here rather than adding ad hoc Markdown beside implementation files.
- Schema and reasoner changes should update the matching reference document in the same work unit.
- Durable design decisions belong in `adr/`.
- Root docs explain where implementation lives; implementation folders should not grow their own unmanaged docs trees.
