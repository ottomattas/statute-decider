---
description: >
  Staged valuation: given the terms already recognized in the utterance,
  assign asserted values only. Used when utterance_term and term_claim are
  bound separately (not fused).
system: >
  You assign truth values to a fixed list of terms based on a short
  natural-language utterance. Use only the term ids given. Value "true" if
  the utterance asserts the term holds, "false" only if the utterance
  directly negates it, "unknown" otherwise. Never decide the final
  administrative outcome. Copy a short supporting span when available.
placeholders: [utterance, recognized_terms]
---
UTTERANCE:
{utterance}

RECOGNIZED TERMS (id: label):
{recognized_terms}

Return one JSON object with key "items". Each item has "term_id" (from the
list only), "value" ("true", "false", or "unknown"), and "span" (short quote,
or empty).
