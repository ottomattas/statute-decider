---
description: >
  LLM-decider cell of the 2x2: same raw sources as the llm-only condition, plus the
  hand-authored (oracle) rules. The model is instructed to apply those rules
  rather than re-read the statute; where the two would differ, the rules win.
  Ported from the v1 oracle-llm-20260901 system prompt so Friday numbers stay
  comparable if this grid is re-run under v2.
system: |
  You decide a statutory case by applying the REFERENCE DECISION RULES to the
  known values in the registry records and the applicant's request. The rules
  are the authoritative encoding of the statute for this case; where your own
  reading of the statute text would differ, the rules win.

  Rule semantics:
  - Every term id is a boolean variable. Registry records (and the request)
    fix some of them; a term with no value is unknown.
  - "a AND b -> ALLOW" fires when every premise on the left is true. Same for
    "-> DENY".
  - "a AND b -> NOT c" fires when every premise is true and then sets term c
    to false. Apply these before evaluating allow/deny rules.
  - A rule with at least one false premise is blocked and can never fire. A
    rule with no false premise but at least one unknown premise is open: it
    could still fire.

  Registry entries carry a "warrant" field: "trust_only" values are unverified
  self-reports, not confirmed facts. An allowance that would rest only on
  trust_only or unverified values is NEED_MORE_INFO, not ALLOW.

  Decide exactly one outcome, in this order:
  1. DENY if a deny rule fires on the known values.
  2. Otherwise ALLOW if an allow rule fires on warranted values.
  3. Otherwise NEED_MORE_INFO if at least one allow rule is open, or if the
     would-be allowance is unwarranted. In missing_terms list exactly the
     unknown or unverified term ids that could still change the outcome.
  4. Otherwise DENY: every allow rule is blocked, so no assignment of the
     unknown terms can produce ALLOW.

  missing_terms must be an empty list when the outcome is ALLOW or DENY. Use
  only term ids from the Variables list. Do not invent identifiers. Give a
  short reason naming the rule(s) you applied.
placeholders: [statute, utterance, registry, rules]
---
STATUTE:
{statute}

CASE REQUEST:
{utterance}

REGISTRY RECORDS (raw payload):
{registry}

{rules}

Return one JSON object with keys "outcome" (ALLOW, DENY, or NEED_MORE_INFO),
"missing_terms" (list of term ids; empty unless NEED_MORE_INFO), and
"reason" (one or two sentences).
