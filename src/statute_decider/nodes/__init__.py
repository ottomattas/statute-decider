"""Node executors for the eleven graph nodes.

statute chain: statute_text -> text_term -> term_rule
user chain:    user_utterance -> utterance_term -> term_claim
register chain: registry_record -> record_term -> term_fact
join:          term_rule + term_claim + term_fact -> premise_outcome -> outcome_trace
"""

from statute_decider.nodes.executors import (
    decide_llm,
    ground_utterance,
    justify_llm,
    lookup_facts,
    match_record_terms,
    passthrough_trace,
    render_trace,
    value_claims,
)

NODE_ORDER = [
    "statute_text",
    "text_term",
    "term_rule",
    "user_utterance",
    "utterance_term",
    "term_claim",
    "registry_record",
    "record_term",
    "term_fact",
    "premise_outcome",
    "outcome_trace",
]

__all__ = [
    "NODE_ORDER",
    "decide_llm",
    "ground_utterance",
    "justify_llm",
    "lookup_facts",
    "match_record_terms",
    "passthrough_trace",
    "render_trace",
    "value_claims",
]
