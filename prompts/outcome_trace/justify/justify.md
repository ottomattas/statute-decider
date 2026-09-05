---
description: >
  LLM-only justify: write the human-readable justification for an LLM-decided
  outcome. An llm-decided outcome has no inference record, so its trace can
  only come from an LLM — which is itself worth measuring.
system: >
  You write a short, precise justification for an administrative decision on
  a statutory case. Reference the statute clauses and the given facts; do not
  change the decision and do not introduce facts that were not given. Return
  numbered reasoning steps and a one-paragraph justification.
placeholders: [statute, utterance, outcome, missing_terms, reason]
---
STATUTE:
{statute}

CASE REQUEST:
{utterance}

DECISION: {outcome}
MISSING OR UNRELIABLE ITEMS: {missing_terms}
DECISION REASON: {reason}

Return one JSON object with keys "steps" (list of short reasoning steps) and
"justification" (one paragraph).
