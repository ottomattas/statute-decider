"""LLM strategies (prompt templates) and loop strategies.

Strategy picks the code path; ``prompt`` picks the wording variant within it.
Loop strategies (``remap``, ``regenerate``) are declared grid coordinates;
``off`` is the only one implemented in this submission.
"""

from statute_decider.strategies.prompts import PromptTemplate, list_variants, load_prompt

__all__ = ["PromptTemplate", "list_variants", "load_prompt"]
