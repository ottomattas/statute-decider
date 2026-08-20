# Agent-Ready Issue Template

Use this template when preparing a tracking issue for bounded autonomous execution.

## Objective

<One sentence defining the intended outcome.>

## Allowed scope

- <files/directories/projects/issues the agent may touch>

## Out of scope

- <files/decisions the agent must not change>

## Acceptance criteria

- <concrete reviewable end state>

## Validation commands

- `source framework/venv/bin/activate && python -m unittest discover -s framework/tests -v`
- <any issue-specific command>

## Stop conditions

- <when the agent must stop and ask for a human decision>

## Human checkpoint needed?

- yes / no
- If yes: <what kind of decision requires review?>

## Handoff format

- PR or branch link
- changed files summary
- validation summary
- unresolved questions
