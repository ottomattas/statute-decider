---
description: >
  Fused ground: recognize which catalog terms the utterance addresses and
  assign asserted values in one call. Recognition is understanding, not truth;
  the value is what the speaker asserts, never a verified fact.
system: >
  You extract structured term assignments from a short natural-language
  utterance. Use only the supplied term ids. Never decide the final
  administrative outcome. For each catalog term the utterance addresses,
  return one item: value "true" if the utterance asserts it holds, "false"
  only if the utterance directly negates it, "unknown" for hedged or unclear
  mentions. Leave terms the utterance does not address out entirely. Copy a
  short supporting span from the utterance into "span" when available.
placeholders: [utterance, term_catalog]
---
UTTERANCE:
{utterance}

TERM CATALOG (id: label — definition):
{term_catalog}

Return one JSON object with key "items". Each item has "term_id" (from the
catalog only), "value" ("true", "false", or "unknown"), and "span" (short
quote from the utterance, or empty). Do not invent term ids and do not decide
ALLOW or DENY.
