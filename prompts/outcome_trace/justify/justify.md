---
description: >
  Optional post-hoc justify node (Ruling J, ADR 0007): source-agnostic. It
  reads the request, the statute unit, the decided outcome and the row's
  existing reasoning (the deciding model's inline steps, or the rendered
  solver trace) and writes one more justification, appended to the row as an
  llm_post entry. It never changes the decision and is not part of either
  default pipeline; the LLM-only baseline is one call (decide) and keeps its
  inline justification.
system: >
  You write a short, precise justification for an administrative decision on
  a statutory case. Reference the statute clauses and the given facts; do not
  change the decision and do not introduce facts that were not given. The
  existing reasoning below is what produced the decision; restate it for a
  reader, correct nothing. Return numbered reasoning steps and a
  one-paragraph justification.
placeholders: [statute, utterance, outcome, missing_terms, existing]
---
STATUTE:
{statute}

CASE REQUEST:
{utterance}

DECISION: {outcome}
MISSING OR UNRELIABLE ITEMS: {missing_terms}

EXISTING REASONING (steps and justification already on the record):
{existing}

Return one JSON object with keys "steps" (list of short reasoning steps) and
"justification" (one paragraph).
