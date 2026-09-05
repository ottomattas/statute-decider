"""Provision references: ``<act_slug>/<eId>`` keys and their display form.

The eId grammar is the Akoma Ntoso naming convention restricted to what the
Riigi Teataja schema carries::

    sec_11                          § 11
    sec_11_1                        § 11¹          (superscript section number)
    sec_11__subsec_1                § 11 (1)
    sec_11__subsec_1_1              § 11 (1¹)      (superscript subsection number)
    sec_11__subsec_5__point_1       § 11 (5) 1)
    sec_11__subsec_5__point_4_1     § 11 (5) 4¹)
    chp_3 / part_2 / dvs_1 / subdvs_1 / subsubdvs_1   structural units (headings only)

Levels are joined with ``__``; a superscript is a ``_<n>`` suffix on the
level's own number. The mapping to RT element ids lives in
``riigiteataja.rt_id_to_eid`` / ``eid_to_rt_id`` (a bijection); this module
never sees RT ids.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

SUPERSCRIPT_DIGITS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

PROVISION_LEVELS = ("sec", "subsec", "point")
STRUCTURAL_LEVELS = ("part", "chp", "dvs", "subdvs", "subsubdvs")

_LEVEL_RE = re.compile(r"^(sec|subsec|point|part|chp|dvs|subdvs|subsubdvs)_(\d+)(?:_(\d+))?$")
_SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def superscript(digits: str) -> str:
    """``"1"`` -> ``"¹"``; anything non-numeric falls back to ``^`` notation."""
    if digits.isdigit():
        return digits.translate(SUPERSCRIPT_DIGITS)
    return "^" + digits


@dataclass(frozen=True)
class EidPart:
    level: str
    number: str
    sup: str | None = None

    def render(self) -> str:
        return f"{self.level}_{self.number}" + (f"_{self.sup}" if self.sup else "")


def parse_eid(eid: str) -> tuple[EidPart, ...]:
    """Split an eId into its levels; raise ``ValueError`` on any deviation."""
    if not eid or "__" not in eid and "_" not in eid:
        raise ValueError(f"Malformed eId {eid!r}")
    parts: list[EidPart] = []
    for chunk in eid.split("__"):
        match = _LEVEL_RE.match(chunk)
        if not match:
            raise ValueError(f"Malformed eId {eid!r}: level {chunk!r}")
        parts.append(EidPart(match.group(1), match.group(2), match.group(3)))
    levels = [p.level for p in parts]
    if levels[0] in STRUCTURAL_LEVELS:
        if len(parts) != 1:
            raise ValueError(f"Structural eId {eid!r} must be a single level")
        return tuple(parts)
    expected = list(PROVISION_LEVELS[: len(parts)])
    if levels != expected:
        raise ValueError(f"eId {eid!r} levels {levels} are not a prefix of {list(PROVISION_LEVELS)}")
    return tuple(parts)


def validate_eid(eid: str) -> str:
    parse_eid(eid)
    return eid


def display_eid(eid: str) -> str:
    """Pure display form of an eId: ``sec_11__subsec_5__point_1`` -> ``§ 11 (5) 1)``.

    Knows nothing about the document, so an unnumbered subsection (a § whose
    single subsection carries no number, e.g. § 15 1)) is shown as ``(1)``;
    ``Act.display`` uses the document and drops it.
    """
    parts = parse_eid(eid)
    return display_parts(parts)


def display_parts(parts: tuple[EidPart, ...], *, hide_subsec: bool = False) -> str:
    out: list[str] = []
    for part in parts:
        num = part.number + (superscript(part.sup) if part.sup else "")
        if part.level == "sec":
            out.append(f"§ {num}")
        elif part.level == "subsec":
            if not hide_subsec:
                out.append(f"({num})")
        elif part.level == "point":
            out.append(f"{num})")
        elif part.level == "part":
            out.append(f"Part {num}")
        elif part.level == "chp":
            out.append(f"Chapter {num}")
        elif part.level == "dvs":
            out.append(f"Division {num}")
        elif part.level == "subdvs":
            out.append(f"Subdivision {num}")
        elif part.level == "subsubdvs":
            out.append(f"Sub-subdivision {num}")
    return " ".join(out)


@dataclass(frozen=True)
class ProvisionRef:
    """``<act_slug>/<eId>`` — the one provision key used in rules, traces, specs, docs."""

    act_slug: str
    eid: str

    def __str__(self) -> str:
        return f"{self.act_slug}/{self.eid}"

    @property
    def key(self) -> str:
        return str(self)


def parse_reference(text: str) -> ProvisionRef:
    """Parse and validate ``<act_slug>/<eId>``."""
    if text.count("/") != 1:
        raise ValueError(f"Provision reference {text!r} must be '<act_slug>/<eId>'")
    slug, eid = text.split("/", 1)
    if not _SLUG_RE.match(slug):
        raise ValueError(f"Provision reference {text!r}: bad act slug {slug!r}")
    validate_eid(eid)
    return ProvisionRef(slug, eid)


def is_within(eid: str, ancestor: str) -> bool:
    """True when ``eid`` equals ``ancestor`` or lies below it (``sec_11__subsec_1`` within ``sec_11``)."""
    return eid == ancestor or eid.startswith(ancestor + "__")


def display_reference(ref: ProvisionRef | str, act_title: str = "", *, act=None) -> str:
    """``"Land Tax Act § 11 (5) 1)"`` — one renderer for every surface.

    With ``act`` (a loaded ``riigiteataja.Act``) the document's own numbering
    is used, so an unnumbered single subsection disappears (``§ 15 1)``).
    """
    if isinstance(ref, str):
        ref = parse_reference(ref)
    body = act.display(ref.eid) if act is not None else display_eid(ref.eid)
    title = act_title or (act.metadata.title if act is not None else "")
    return f"{title} {body}".strip()
