# ADR 0003: Keep the promoted `framework` CLI proposition-first until the audit path is stable

## Status

Accepted

## Context

The current runnable implementation was first developed under `poc3/` and has now been promoted into `framework/` as the main executable code path. The immediate requirements remain:

- a simple four-step CLI
- direct file-path inputs
- editable prompt files outside Python
- auditable traces
- explicit missing-information handling
- neutral blockage reporting when a law text does not support the fixed worked example

At the same time, there is pressure to widen the scope quickly:

- richer logic levels
- broader ontology induction
- additional law families
- heavier abstraction layers

The risk is that premature generalization would make the current demo harder to inspect while also encouraging novelty claims that the implementation does not yet justify.

## Decision

Keep the promoted `framework/` implementation disciplined:

- Treat propositional logic as the only executable core for now.
- Keep predicate and higher-order logic as explicit future-facing render/lower views, not active execution paths.
- Keep the user-facing surface as direct file-path flags and avoid adding required pack or catalog abstractions.
- Keep the current demo law-swappable and prompt-swappable, but acknowledge that it still runs against one fixed internal Section 120 vocabulary.
- Defer a second real ontology and broader non-propositional execution until the current extraction, metadata, trace, and scenario-regeneration path is stable.

## Consequences

- The main implementation root is again `framework/`, which matches the repo-level docs and command conventions.
- The runnable demo remains easier to explain and audit.
- The current work can make honest claims about solver-centered inspection and missing-information handling without overstating ontology generalization.
- Future expansion is still possible, but it will be staged after the current proposition-first path is reliable enough to serve as a baseline.
