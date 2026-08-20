# ADR 0002: Canonical docs tree and phase-based delivery

## Status

Accepted

## Context

Documentation had started to spread across implementation folders, while the framework rewrite also needed stronger coupling between code changes, docs updates, and tracker status.

## Decision

Use one canonical documentation tree at `docs/` with four durable areas:

- `architecture/`
- `reference/`
- `guides/`
- `adr/`

Require schema and reasoner changes to update the relevant reference document in the same work unit. For larger user-requested rewrites, land one signed commit per completed major phase and update the tracker after each phase.

## Consequences

- Documentation is easier to find and keep consistent.
- The repo avoids unmanaged Markdown growth inside implementation folders.
- Tracker status, commits, and docs stay aligned as the architecture evolves.
