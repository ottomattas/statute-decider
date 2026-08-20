# Cloud Agent Runbook

This runbook defines how to use cloud agents safely for this repository.

## Preconditions

Before a task is delegated:

- the relevant tracking issue follows the `Agent-ready issue contract`;
- the issue is labeled appropriately (for example `agent-ready`, `safe-autonomy`, `ci-required`, `needs-human-decision`, `research-open-ended`);
- the repository is accessible to the cloud agent through GitHub;
- required secrets are configured in the cloud-agent platform, not committed to the repo;
- the task has explicit validation commands.

## Secrets

- Use platform-managed secrets only.
- Do not commit `.env`, credentials, API keys, or copied secret values.
- If a task depends on a missing secret, stop and hand control back.

## Branch naming

- Prefer branches that include a generic task ID or scope tag.
- Recommended format: `<task-id>-<short-scope>`
- If the cloud tool chooses the branch automatically, ensure the task identifier still appears in the PR title or handoff summary.

## Standard validation

Use the standardized commands unless the issue explicitly overrides them:

```bash
source framework/venv/bin/activate
python -m unittest discover -s framework/tests -v
```

Add issue-specific commands only when needed.

## Review policy

- Default to **PR-first**, not direct merge.
- Include a short handoff note: changed files, validation run, and remaining questions.
- Require human review before merging anything that changes semantics, research framing, paper text, or external dependencies.

## Red lines

Cloud agents must stop and request human review if the task would require:

- changing solver semantics or schema meaning;
- changing thesis claims, scientific framing, or paper argumentation;
- adding a dependency without clear justification;
- touching files outside the declared scope;
- using destructive git operations;
- bypassing validation or review requirements.

## Good task types

- bounded docs updates;
- repo drift fixes;
- scenario or test scaffolding with explicit expected behavior;
- workflow/tooling changes with clear validation;
- issue and transcript synchronization.

## Poor task types

- open-ended novelty work;
- literature interpretation and citation-sensitive writing;
- hypothesis changes;
- under-specified extraction or evaluation experiments.

## Handoff checklist

Every cloud-agent run should return:

- branch or PR reference;
- concise summary of changes;
- exact validation commands run;
- validation results;
- unresolved questions or reasons for stopping.
