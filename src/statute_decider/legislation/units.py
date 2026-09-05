"""Statute input = the smallest official structural unit that holds the declared
provisions (Ruling H, 2026-09-06; ADR 0005).

A model never receives a hand-made excerpt. It receives either the whole act,
or one structural unit of the act exactly as the official text divides it —
part, chapter, division, subdivision, sub-subdivision (the five RT XML unit
elements ``riigiteataja.Act._walk_body`` maps to ``part``/``chp``/``dvs``/
``subdvs``/``subsubdvs``) — rendered by the same renderer as the whole act,
headings and provision numbering as in the XML. The choice is deterministic:

* the whole act when its token estimate fits ``max_tokens``;
* otherwise the **smallest** unit that encloses every provision the statute's
  ``statute.yaml`` declares (the innermost common ancestor);
* if even that unit exceeds the budget, ``UnitTooLarge`` — the operator decides,
  the harness does not cut official text.

Tokens are estimated as ``ceil(chars / 4)`` — deterministic, offline, and a
conservative reading of the ratio the vendors publish for English prose. No
network, no tokenizer dependency; the ledger records the vendor's real count
per call next to this estimate.

``DEFAULT_MAX_STATUTE_TOKENS`` (100 000) is chosen so that every act in the
benchmark except the Law of Obligations Act (~316k tokens) stays whole
(Building Code ~71k is the largest that must fit), and so that the statute
plus the rest of the prompt (utterance, rules, instructions: a few thousand
tokens) and the reply (``max_output_tokens`` 8 192) fit the smallest context
window among the configured models (``configs/llm/models.yaml``
``context_tokens``; 128k is the floor). The runner warns when a grid's models
cannot take the budget.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from statute_decider.legislation.riigiteataja import Act, Unit

DEFAULT_MAX_STATUTE_TOKENS = 100_000
CHARS_PER_TOKEN = 4

UNIT_KINDS = {
    "part": "part",
    "chp": "chapter",
    "dvs": "division",
    "subdvs": "subdivision",
    "subsubdvs": "sub-subdivision",
}


def estimate_tokens(text: str) -> int:
    """Deterministic ``ceil(len / 4)``; zero for an empty string."""
    return -(-len(text) // CHARS_PER_TOKEN)


class UnitTooLarge(ValueError):
    """Even the smallest enclosing unit exceeds the statute token budget."""


@dataclass(frozen=True)
class UnitCandidate:
    kind: str  # "act" | part | chapter | division | ...
    eid: str  # "act" or the unit path (part_1__chp_2__dvs_4)
    display: str  # "Part 1 GENERAL PART › Chapter 2 CONTRACT › Subchapter 4 Distance Contracts"
    tokens_estimate: int
    chars: int


@dataclass(frozen=True)
class UnitChoice:
    """What the statute_text node hands on: the chosen unit and its text."""

    kind: str
    eid: str
    display: str
    text: str
    tokens_estimate: int
    max_tokens: int
    candidates: list[UnitCandidate] = field(default_factory=list)  # act first, then outermost → innermost

    @property
    def is_whole_act(self) -> bool:
        return self.eid == "act"


def _display(unit: Unit) -> str:
    return " › ".join(u.title for u in [*unit.ancestors(), unit])


def unit_candidates(act: Act, provisions: list[str], *, strip_markers: bool = False) -> list[UnitCandidate]:
    """The whole act, then every enclosing unit outermost → innermost, each with its size."""
    full = act.render_full(strip_markers=strip_markers)
    out = [UnitCandidate("act", "act", act.metadata.title, estimate_tokens(full), len(full))]
    for unit in act.enclosing_units(provisions):
        text = act.render_unit(unit.path, strip_markers=strip_markers)
        out.append(
            UnitCandidate(UNIT_KINDS.get(unit.level, unit.level), unit.path, _display(unit), estimate_tokens(text), len(text))
        )
    return out


def select_statute_unit(
    act: Act,
    provisions: list[str],
    *,
    max_tokens: int = DEFAULT_MAX_STATUTE_TOKENS,
    strip_markers: bool = False,
) -> UnitChoice:
    """Whole act if it fits ``max_tokens``, else the smallest enclosing unit; raise
    ``UnitTooLarge`` when that still does not fit (or when the act has no unit
    enclosing the provisions and is itself too large)."""
    for eid in provisions:
        act.provision(eid)  # ProvisionNotFound early, with the act named
    candidates = unit_candidates(act, provisions, strip_markers=strip_markers)
    whole = candidates[0]
    if whole.tokens_estimate <= max_tokens:
        return UnitChoice(
            kind="act",
            eid="act",
            display=whole.display,
            text=act.render_full(strip_markers=strip_markers),
            tokens_estimate=whole.tokens_estimate,
            max_tokens=max_tokens,
            candidates=candidates,
        )
    if len(candidates) == 1:
        raise UnitTooLarge(
            f"{act.metadata.title}: the whole act is ~{whole.tokens_estimate} tokens > {max_tokens} "
            "and no structural unit encloses all declared provisions"
        )
    smallest = candidates[-1]
    if smallest.tokens_estimate > max_tokens:
        raise UnitTooLarge(
            f"{act.metadata.title}: smallest enclosing unit {smallest.eid} ({smallest.display}) is "
            f"~{smallest.tokens_estimate} tokens > {max_tokens}"
        )
    return UnitChoice(
        kind=smallest.kind,
        eid=smallest.eid,
        display=smallest.display,
        text=act.render_unit(smallest.eid, strip_markers=strip_markers),
        tokens_estimate=smallest.tokens_estimate,
        max_tokens=max_tokens,
        candidates=candidates,
    )
