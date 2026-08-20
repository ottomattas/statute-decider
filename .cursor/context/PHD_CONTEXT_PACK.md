# PhD Context Pack

This file is the portable assistant-facing context pack for the broader PhD workflow.
It must remain public-safe and should not store private tracker names, issue IDs, or detailed status snapshots.

## Decision

For now, the portable AI context layer lives as a **compact document pack**, not as a separate PhD meta-repo.

Rationale:

- it is faster to maintain;
- it avoids creating a new repository before the workflow is proven;
- it is easy to reuse in Cursor and easy to paste or upload to other assistants when needed.

Revisit the need for a metadata-only PhD repo later if cross-repo and cross-assistant coordination becomes too awkward with documents alone.

## Source of truth

- **Thesis-level coordination:** external tracker
- **Current paper execution:** paper-specific tracker and repo
- **Workflow/tooling execution:** separate tooling/workflow tracker

This file is a portable context summary. It should not become a second detailed backlog.
Use the external tracker when concrete project names, issue IDs, or current states are needed.

## Paper portfolio

- **Survey line**
  - Role: broad conceptual and literature foundation

- **Controlled reasoning benchmark line**
  - Role: controlled evidence on reasoning structure and bridge to Horn-like decomposition

- **Current applied execution line**
  - Role: active experimental testbed for formalization, execution, and provenance

## Active thesis directions

- explicit constraint representations may adapt better to changing laws and processes than hardcoded scripts;
- realistic decision problems may contain useful Horn-like substructures;
- intent detection should be treated as knowledge-enhanced scenario extraction with provenance;
- process simplification is an applied usefulness angle, not the sole scientific focus.

## Current implementation vocabulary

- `UseCaseDefinition`, `ScenarioDefinition`: externalized use-case and scenario specs under `framework/examples/`;
- `IntentArtifact`, `DomainArtifact`, `MockDbArtifact`, `CaseBundle`, `SolutionArtifact`: the checked pipeline artifacts;
- `LogicLevel`, `RuleKind`, `SolverOutcome`, `BlockReasonCode`: the main execution enums;
- `ExtractionRunMetadata`, `SolveRunMetadata`, `PromptMetadata`: provenance and audit metadata.

The current runtime is file-backed and auditable. New concepts should be introduced through use-case files, prompt files, or explicit schema changes rather than silent mutation at decision time.

## Near-term development lanes

- **Current phase default:** statute-grounded implementation work now happens directly under `framework/`, especially in `framework/examples/`, before `paper/` updates unless the tracker or user explicitly scopes otherwise (see root `AGENTS.md`).
- extract graph-native world structures from source text;
- extract case assertions and provenance from free-text case descriptions;
- wire extracted artefacts into end-to-end decision runs;
- extend evaluation fixtures and aligned docs around the new framework.

## Active repo pattern

- **Current repo pattern:** one dual-use research compendium with `paper/`, `framework/`, canonical docs under `docs/`, and local working material under `wip/` (reference sketch in `framework/POC.txt`)
- **Paper execution pattern:** one paper-specific tracker and repo
- **Workflow/tooling pattern:** separate workflow tracker

## Safe autonomy boundary

Good candidates for autonomous or cloud-agent execution:

- repo drift fixes;
- docs synchronization;
- transcript-to-tracker synchronization;
- bounded scenario and test generation;
- workflow/tooling tasks;
- small refactors with explicit validation commands.

Human-checkpoint tasks:

- open-ended novelty work;
- scientific framing changes;
- citation-sensitive writing;
- anything where acceptance criteria are not explicit.

## Update rhythm

Refresh this context pack when:

- a paper changes state;
- a supervision meeting changes direction;
- a new cross-paper claim or evidence gap becomes important;
- the automation workflow changes materially.
