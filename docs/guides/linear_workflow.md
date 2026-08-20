# Tracker Workflow

## Purpose

The issue tracker is the source of truth for execution scope, issue states, and delivery sequencing.

## Execution pattern

For each major phase:

1. move the active issue into `In Progress`
2. keep implementation scoped to that issue
3. validate the work
4. create one signed commit for the completed phase when requested
5. move the issue forward and add a short comment with the commit hash

## Issue design

- Prefer one issue per conceptual boundary, such as schema, reasoner, governance, docs, or cutover.
- Create a new issue when the discovered work is meaningfully separate instead of silently expanding the active one.
- Keep the active queue small enough to steer development.
- Routine docs cleanup or paper-facing clarity work should usually stay inside the parent issue.
- Create a separate docs issue only when the documentation artifact is itself a durable deliverable or a genuinely separate workstream.

## Repo sync rules

- Runtime vocabulary changes should be reflected in issue descriptions.
- Durable design decisions belong in docs or ADRs, not tracker-only notes.
- Committed repo files should not contain private tracker identifiers or status snapshots.

## Agent-ready work

Only treat a task as automation-ready when it clearly states:

- objective
- allowed scope
- out-of-scope boundaries
- validation command
- stop conditions
- handoff format
