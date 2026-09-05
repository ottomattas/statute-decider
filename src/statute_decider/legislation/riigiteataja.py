"""Riigi Teataja consolidated-text XML (schema ``tyviseadus_1_10.02.2010``).

Standard library only (``xml.etree``). Three jobs:

1. **Metadata** — ``<metaandmed>``: global id, text-group id (stable across
   redactions of one act; links the English translation to the Estonian
   original), validity window, publication, title.
2. **Provisions** — ``<paragrahv id="para11">`` -> ``<loige id="para11lg1">``
   -> ``<alampunkt id="para11lg5p1">``; superscript numbers carry a ``b<n>``
   suffix (``para11lg1b1`` = § 11 (1¹)). The RT id <-> Akoma Ntoso eId
   mapping (``rt_id_to_eid`` / ``eid_to_rt_id``) is a bijection; RT ids are
   never written anywhere by this repo — they are recomputed here at lookup.
3. **Rendering** — a provision, a selection of provisions, or the whole act
   as plain text with the official display numbers (``<kuvatavNr>``),
   ``<sup>`` as Unicode superscripts, ``<reavahetus/>`` as a newline, and
   the inline amendment markers (``[RT I, … – entry into force …]``) kept
   unless ``strip_markers`` is set.

Quirks of the files this was written against (14 acts, 7 × {et, en}):

* The UUID ``id`` attributes on most elements are reused within a file and
  absent from the counterpart language; only the structural ids
  (``para…``, ``ptk…``, ``jg…``, …) are meaningful. UUIDs are ignored.
* English files encode a section-level amendment or repeal note as an extra
  ``<loige id="paraNlg1">`` with an empty ``<loigeNr/>`` before the real
  (1); the Estonian files use ``<muutmismarge>`` instead. Such unnumbered
  siblings of numbered subsections are *notes*, not provisions, and are
  rendered under the section heading without an eId.
* A section whose only subsection is unnumbered (§ 15 of the Civil Service
  Act, § 44 of the Building Code, § 4 of the Personal Data Protection Act)
  still carries ``paraNlg1`` in the XML; it is the provision
  ``sec_N__subsec_1`` and is displayed without the ``(1)``.
* Annex PDFs are embedded base64 (``<lisaViide>``/``<fail>``) and skipped;
  footnotes (``<normtehnmarkusTekst>``) are rendered at the end.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from statute_decider.legislation.references import (
    EidPart,
    display_parts,
    parse_eid,
    superscript,
)

SCHEMA_NAME = "tyviseadus_1_10.02.2010"

# --- RT id <-> eId bijection --------------------------------------------------

_RT_PROVISION_RE = re.compile(
    r"^para(?P<sec>\d+)(?:b(?P<sec_sup>\d+))?"
    r"(?:lg(?P<subsec>\d+)(?:b(?P<subsec_sup>\d+))?"
    r"(?:p(?P<point>\d+)(?:b(?P<point_sup>\d+))?)?)?$"
)
_RT_STRUCT_RE = re.compile(r"^(?P<kind>osa|o|ptk|jg|jaotis|alljaotis)(?P<num>\d+)$")
_RT_STRUCT_TO_LEVEL = {
    "osa": "part",
    "o": "part",  # English files spell the part id ``o1``; ``osa1`` is canonical
    "ptk": "chp",
    "jg": "dvs",
    "jaotis": "subdvs",
    "alljaotis": "subsubdvs",
}
_LEVEL_TO_RT_STRUCT = {
    "part": "osa",
    "chp": "ptk",
    "dvs": "jg",
    "subdvs": "jaotis",
    "subsubdvs": "alljaotis",
}
_LEVEL_TO_RT_PROVISION = {"sec": "para", "subsec": "lg", "point": "p"}


def rt_id_to_eid(rt_id: str) -> str:
    """``para11lg5p1`` -> ``sec_11__subsec_5__point_1``; ``para11lg1b1`` -> ``sec_11__subsec_1_1``.

    Structural units: ``ptk3`` -> ``chp_3``, ``jg2`` -> ``dvs_2``, ``osa1``/``o1`` -> ``part_1``.
    Raises ``ValueError`` on any id shape not covered — never guesses.
    """
    match = _RT_PROVISION_RE.match(rt_id)
    if match:
        groups = match.groupdict()
        parts = [f"sec_{groups['sec']}" + (f"_{groups['sec_sup']}" if groups["sec_sup"] else "")]
        if groups["subsec"]:
            parts.append(
                f"subsec_{groups['subsec']}"
                + (f"_{groups['subsec_sup']}" if groups["subsec_sup"] else "")
            )
        if groups["point"]:
            parts.append(
                f"point_{groups['point']}"
                + (f"_{groups['point_sup']}" if groups["point_sup"] else "")
            )
        return "__".join(parts)
    match = _RT_STRUCT_RE.match(rt_id)
    if match:
        return f"{_RT_STRUCT_TO_LEVEL[match.group('kind')]}_{match.group('num')}"
    raise ValueError(f"Unrecognised Riigi Teataja element id {rt_id!r}")


def eid_to_rt_id(eid: str) -> str:
    """Inverse of ``rt_id_to_eid`` (canonical ``osa`` for parts)."""
    parts = parse_eid(eid)
    if parts[0].level in _LEVEL_TO_RT_STRUCT:
        return f"{_LEVEL_TO_RT_STRUCT[parts[0].level]}{parts[0].number}"
    out = ""
    for part in parts:
        out += _LEVEL_TO_RT_PROVISION[part.level] + part.number
        if part.sup:
            out += f"b{part.sup}"
    return out


# --- XML helpers -------------------------------------------------------------


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _children(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if _local(c.tag) == name]


def _text(el: ET.Element | None) -> str:
    return (el.text or "").strip() if el is not None else ""


def _path_text(el: ET.Element, *names: str) -> str:
    cur: ET.Element | None = el
    for name in names:
        if cur is None:
            return ""
        cur = _child(cur, name)
    return _text(cur)


_SUP_MARKUP_RE = re.compile(r"<sup>(.*?)</sup>")
_WS_RE = re.compile(r"[ \t\r\f\v]+")
_NL_TOKEN = "\u0000"
MARKER_LINE_RE = re.compile(r"^\[RT\s+[IVX]+[ ,].*\]$")


def _display_number(el: ET.Element) -> str:
    """``<kuvatavNr>`` CDATA -> ``§ 11.`` / ``(1¹)`` / ``1)`` / ``Chapter 1``; empty when unnumbered."""
    raw = _text(_child(el, "kuvatavNr"))
    raw = _SUP_MARKUP_RE.sub(lambda m: superscript(m.group(1).strip()), raw)
    return _WS_RE.sub(" ", raw).strip()


def _inline(el: ET.Element, language: str) -> str:
    """Flatten mixed content; ``<sup>`` -> superscript, ``<reavahetus/>`` -> newline token."""
    out: list[str] = []
    if el.text:
        out.append(el.text)
    for child in el:
        name = _local(child.tag)
        if name == "sup":
            out.append(superscript("".join(child.itertext()).strip()))
        elif name == "reavahetus":
            out.append(_NL_TOKEN)
        elif name == "viide":
            out.append(_text(_child(child, "kuvatavTekst")))
        elif name in ("viideURID", "viideURI", "fail", "lisaViit"):
            pass
        elif name == "muutmismarge":
            out.append(_NL_TOKEN + _amendment_marker(child, language) + _NL_TOKEN)
        elif name in ("tavatekst", "sisuTekst", "i", "b", "u", "kuvatavTekst"):
            out.append(_inline(child, language))
        else:
            out.append(_inline(child, language))
        if child.tail:
            out.append(child.tail)
    return "".join(out)


def _normalise(text: str) -> str:
    text = text.replace("\n", " ")
    text = _WS_RE.sub(" ", text)
    lines = [line.strip() for line in text.split(_NL_TOKEN)]
    return "\n".join(line for line in lines if line)


def _publication(el: ET.Element | None) -> str:
    """``<avaldamismarge>`` -> ``RT I, 30.06.2024, 1`` / ``RT I 1993, 24, 428`` / ``RT V, 05.01.2026, 5``."""
    if el is None:
        return ""
    osa = _path_text(el, "RTosa")
    date = _path_text(el, "avaldamineKuupaev")
    year = _path_text(el, "RTaasta")
    nr = _path_text(el, "RTnr")
    art = _path_text(el, "RTartikkel")
    if date:
        return f"{osa}, {_dmy(_date(date))}, {art}".strip(", ")
    pieces = [p for p in (f"{osa} {year}".strip(), nr, art) if p]
    return ", ".join(pieces)


_ISO_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:[T+\-].*)?$")


def _date(value: str) -> str:
    """Normalise an RT date: some carry a timezone suffix (``2026-03-16+02:00``) -> ``2026-03-16``."""
    m = _ISO_DATE_RE.match(value.strip())
    return m.group(1) if m else value.strip()


def _dmy(iso: str) -> str:
    """``2024-06-30`` -> ``30.06.2024`` (RT citation style); passthrough otherwise."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", _date(iso))
    return f"{m.group(3)}.{m.group(2)}.{m.group(1)}" if m else iso


def _amendment_marker(el: ET.Element, language: str) -> str:
    """``<muutmismarge>`` inside the body -> ``[Kehtetu - RT I, 10.03.2022, 2 - jõust. 01.01.2024]``."""
    prefix = " ".join(_text(t) for t in _children(el, "tavatekst")).strip()
    ref = _publication(_child(el, "avaldamismarge"))
    force = _path_text(el, "joustumine")
    word = "jõust." if language == "et" else "entry into force"
    body = ref + (f" - {word} {_dmy(force)}" if force else "")
    if prefix:
        body = f"{prefix} {body}".replace("-  ", "- ").strip()
    return f"[{body}]"


# --- document model -----------------------------------------------------------


@dataclass
class ActMetadata:
    global_id: str
    group_id: str
    title: str
    language: str  # "en" (RT V translation) | "et" (RT I original)
    publication: str  # this consolidated text's own RT reference
    publication_date: str  # ISO
    document_type: str
    text_type: str
    issuer: str
    abbreviation: str
    adopted_on: str
    entry_into_force: str
    original_publication: str
    in_force_from: str
    in_force_until: str | None
    schema: str
    version_date: str


@dataclass
class Provision:
    eid: str
    level: str  # sec | subsec | point
    display_number: str  # "§ 11." / "(1¹)" / "1)" — "" for an unnumbered subsection
    heading: str = ""  # section title (sections only)
    text: str = ""  # own text: the subsection/point body, or a section's lead-in
    notes: list[str] = field(default_factory=list)  # section-level notes (no eId)
    children: list[Provision] = field(default_factory=list)
    parent: Provision | None = field(default=None, repr=False)
    repealed: bool = False

    @property
    def section(self) -> Provision:
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


@dataclass
class Unit:
    """A structural heading (part / chapter / division …) in document order."""

    eid: str
    level: str
    display_number: str
    heading: str


class ProvisionNotFound(KeyError):
    pass


class Act:
    """One consolidated text: metadata, indexed provisions, renderers."""

    def __init__(self, path: Path, root: ET.Element, sha256: str) -> None:
        self.path = Path(path)
        self.sha256 = sha256
        self.metadata = _parse_metadata(root)
        self.body: list[Unit | Provision] = []
        self.index: dict[str, Provision] = {}
        self.footnotes: list[str] = []
        self.annexes: list[str] = []
        self._build(root)

    # -- building -----------------------------------------------------------

    def _build(self, root: ET.Element) -> None:
        lang = self.metadata.language
        sisu = _child(root, "sisu")
        if sisu is None:
            raise ValueError(f"{self.path}: no <sisu> body")
        self._walk_body(sisu)
        for note in _children(root, "normtehnmarkus"):
            body = _child(note, "normtehnmarkusTekst")
            text = _normalise(_inline(body, lang)) if body is not None else ""
            if text:
                self.footnotes.append(text)
        for annex in _children(root, "lisaViide"):
            name = _path_text(annex, "lisaViit", "lisaPealkiri", "lisaNimi") or _path_text(
                annex, "lisaViit", "lisaNimi"
            )
            fail = None
            for el in annex.iter():
                if _local(el.tag) == "fail":
                    fail = el
                    break
            label = name or (fail.get("failNimi", "") if fail is not None else "")
            if label:
                self.annexes.append(label)

    def _walk_body(self, el: ET.Element) -> None:
        for child in el:
            name = _local(child.tag)
            if name == "paragrahv":
                self._add_section(child)
            elif name in ("osa", "peatykk", "jagu", "jaotis", "alljaotis"):
                level = {
                    "osa": "part",
                    "peatykk": "chp",
                    "jagu": "dvs",
                    "jaotis": "subdvs",
                    "alljaotis": "subsubdvs",
                }[name]
                number = _path_text(child, f"{name}Nr")
                sup = _child(child, f"{name}Nr")
                sup_idx = sup.get("ylaIndeks") if sup is not None else None
                eid = f"{level}_{number}" + (f"_{sup_idx}" if sup_idx else "")
                self.body.append(
                    Unit(
                        eid=eid,
                        level=level,
                        display_number=_display_number(child),
                        heading=_path_text(child, f"{name}Pealkiri"),
                    )
                )
                self._walk_body(child)
            # anything else at body level (notes, ids) is not statute text

    def _add_section(self, el: ET.Element) -> None:
        lang = self.metadata.language
        rt_id = el.get("id", "")
        eid = rt_id_to_eid(rt_id)
        if not eid.startswith("sec_"):
            raise ValueError(f"{self.path}: <paragrahv id={rt_id!r}> is not a section id")
        nr = _child(el, "paragrahvNr")
        section = Provision(
            eid=eid,
            level="sec",
            display_number=_display_number(el),
            heading=_path_text(el, "paragrahvPealkiri"),
            repealed=(nr is not None and nr.get("kehtiv") == "0"),
        )
        # Section-level own text (repealed §§ carry a bare <sisuTekst>) and markers.
        own: list[str] = []
        for child in el:
            name = _local(child.tag)
            if name == "sisuTekst":
                own.append(_normalise(_inline(child, lang)))
            elif name == "muutmismarge":
                section.notes.append(_amendment_marker(child, lang))
        section.text = "\n".join(t for t in own if t)
        loiged = _children(el, "loige")
        numbered = [lg for lg in loiged if _text(_child(lg, "loigeNr"))]
        for lg in loiged:
            if not _text(_child(lg, "loigeNr")) and numbered:
                # English-file note: an unnumbered sibling of numbered subsections.
                text = _normalise(_inline_of(lg, lang))
                if text:
                    section.notes.append(text)
                continue
            self._add_subsection(section, lg)
        if section.text.startswith(("[Repealed", "[Kehtetu", "Kehtetu")) or any(
            n.startswith(("[Repealed", "[Kehtetu")) for n in section.notes
        ):
            section.repealed = True
        self._register(section)
        self.body.append(section)

    def _add_subsection(self, section: Provision, lg: ET.Element) -> None:
        lang = self.metadata.language
        rt_id = lg.get("id", "")
        eid = rt_id_to_eid(rt_id)
        if eid.count("__") != 1 or not eid.startswith(section.eid + "__subsec_"):
            raise ValueError(
                f"{self.path}: <loige id={rt_id!r}> under section {section.eid} has eId {eid}"
            )
        sub = Provision(
            eid=eid,
            level="subsec",
            display_number=_display_number(lg),
            text=_normalise(_inline_of(lg, lang)),
            parent=section,
        )
        sub.repealed = sub.text.startswith(("[Repealed", "[Kehtetu"))
        for punkt in lg:
            if _local(punkt.tag) in ("alampunkt", "punkt"):
                self._add_point(sub, punkt)
        section.children.append(sub)
        self._register(sub)

    def _add_point(self, sub: Provision, punkt: ET.Element) -> None:
        lang = self.metadata.language
        rt_id = punkt.get("id", "")
        eid = rt_id_to_eid(rt_id)
        if eid.count("__") != 2 or not eid.startswith(sub.eid + "__point_"):
            raise ValueError(
                f"{self.path}: <{_local(punkt.tag)} id={rt_id!r}> under {sub.eid} has eId {eid}"
            )
        point = Provision(
            eid=eid,
            level="point",
            display_number=_display_number(punkt),
            text=_normalise(_inline_of(punkt, lang)),
            parent=sub,
        )
        point.repealed = point.text.startswith(("[Repealed", "[Kehtetu"))
        for deeper in punkt:
            if _local(deeper.tag) in ("alampunkt", "punkt"):
                raise ValueError(
                    f"{self.path}: nested point under {eid} ({deeper.get('id')!r}) — "
                    "no eId level defined for it; extend references.PROVISION_LEVELS deliberately"
                )
        sub.children.append(point)
        self._register(point)

    def _register(self, prov: Provision) -> None:
        if prov.eid in self.index:
            raise ValueError(f"{self.path}: duplicate provision {prov.eid}")
        self.index[prov.eid] = prov

    # -- lookup -------------------------------------------------------------

    @property
    def sections(self) -> list[Provision]:
        return [item for item in self.body if isinstance(item, Provision)]

    def provision(self, eid: str) -> Provision:
        parse_eid(eid)
        try:
            return self.index[eid]
        except KeyError as exc:
            raise ProvisionNotFound(
                f"{self.metadata.title} ({self.metadata.global_id}) has no provision {eid}"
            ) from exc

    def has(self, eid: str) -> bool:
        return eid in self.index

    def provision_eids(self) -> list[str]:
        return list(self.index)

    def display(self, eid: str) -> str:
        """``§ 11 (5) 1)`` using the document's numbering (unnumbered subsections hidden)."""
        parts = parse_eid(eid)
        self.provision(eid)  # raises ProvisionNotFound
        hide = False
        if len(parts) >= 2:
            sub = self.provision("__".join(p.render() for p in parts[:2]))
            hide = sub.display_number == ""
        return display_parts(parts, hide_subsec=hide)

    # -- rendering ------------------------------------------------------------

    def header(self) -> str:
        m = self.metadata
        window = f"in force from {_dmy(m.in_force_from)}" if m.in_force_from else ""
        if m.in_force_until:
            window += f" until {_dmy(m.in_force_until)}"
        line = f"{m.publication}; {window}".strip("; ")
        return f"{m.title}\n{line}".rstrip()

    def render_provision(self, eid: str, *, strip_markers: bool = False) -> str:
        """Exactly one provision (with its descendants); a section includes its heading."""
        return "\n".join(self._lines(self.provision(eid), strip_markers, whole=True))

    def render_slice(self, eids: list[str], *, strip_markers: bool = False) -> str:
        """The declared provisions with their section headings and any lead-in text
        of an undeclared ancestor (so a point keeps its enumerating sentence)."""
        for eid in eids:
            self.provision(eid)
        out: list[str] = []
        for section in self.sections:
            declared = any(_within(section.eid, e) for e in eids)
            touched = declared or any(_within(e, section.eid) for e in eids)
            if not touched:
                continue
            out.append(self._section_heading(section))
            if declared:
                out.extend(self._body_lines(section, strip_markers, whole=True))
            else:
                out.extend(self._select_lines(section, eids, strip_markers))
            out.append("")
        title = f"{self.metadata.title} — selected provisions: " + ", ".join(
            self.display(e) for e in eids
        )
        return (title + "\n\n" + "\n".join(out)).rstrip() + "\n"

    def render_full(self, *, strip_markers: bool = False) -> str:
        out: list[str] = [self.header(), ""]
        for item in self.body:
            if isinstance(item, Unit):
                head = f"{item.display_number} {item.heading}".strip()
                out.extend(["", head, ""])
            else:
                out.extend(self._lines(item, strip_markers, whole=True))
                out.append("")
        if self.footnotes:
            out.append("")
            for i, note in enumerate(self.footnotes, 1):
                out.append(f"[Footnote {i}] {note}")
        if self.annexes:
            out.append("")
            for label in self.annexes:
                out.append(f"[Annex: {label}]")
        return "\n".join(out).rstrip() + "\n"

    # -- rendering internals ----------------------------------------------------

    def _section_heading(self, section: Provision) -> str:
        return f"{section.display_number} {section.heading}".strip()

    def _lines(self, prov: Provision, strip_markers: bool, *, whole: bool) -> list[str]:
        if prov.level == "sec":
            return [self._section_heading(prov), *self._body_lines(prov, strip_markers, whole=whole)]
        return self._body_lines(prov, strip_markers, whole=whole)

    def _body_lines(self, prov: Provision, strip_markers: bool, *, whole: bool) -> list[str]:
        lines: list[str] = []
        if prov.level == "sec":
            lines.extend(_filter(prov.notes, strip_markers))
        text_lines = _filter(prov.text.split("\n") if prov.text else [], strip_markers)
        if text_lines:
            first = f"{prov.display_number} {text_lines[0]}".strip() if prov.level != "sec" else text_lines[0]
            lines.append(first)
            lines.extend(text_lines[1:])
        elif prov.display_number and prov.level != "sec":
            lines.append(prov.display_number)
        if whole:
            for child in prov.children:
                lines.extend(self._body_lines(child, strip_markers, whole=True))
        return lines

    def _select_lines(self, node: Provision, eids: list[str], strip_markers: bool) -> list[str]:
        lines: list[str] = []
        for child in node.children:
            if any(_within(child.eid, e) for e in eids):
                lines.extend(self._body_lines(child, strip_markers, whole=True))
            elif any(_within(e, child.eid) for e in eids):
                lines.extend(self._body_lines(child, strip_markers, whole=False))
                lines.extend(self._select_lines(child, eids, strip_markers))
        return lines


def _within(eid: str, ancestor: str) -> bool:
    return eid == ancestor or eid.startswith(ancestor + "__")


def _filter(lines: list[str], strip_markers: bool) -> list[str]:
    if not strip_markers:
        return list(lines)
    return [line for line in lines if not MARKER_LINE_RE.match(line)]


def _inline_of(el: ET.Element, language: str) -> str:
    """Text of a loige/alampunkt: its <sisuTekst> parts and inline markers, not its sub-points."""
    out: list[str] = []
    for child in el:
        name = _local(child.tag)
        if name == "sisuTekst":
            out.append(_inline(child, language))
        elif name == "muutmismarge":
            out.append(_NL_TOKEN + _amendment_marker(child, language))
    return _NL_TOKEN.join(out)


# --- metadata ----------------------------------------------------------------


def _parse_metadata(root: ET.Element) -> ActMetadata:
    meta = _child(root, "metaandmed")
    if meta is None:
        raise ValueError("no <metaandmed>")
    pub_el = _child(meta, "avaldamismarge")
    publication = _publication(pub_el)
    series = _path_text(pub_el, "RTosa") if pub_el is not None else ""
    language = "en" if series.startswith("RT V") else "et"
    adopted = _child(meta, "vastuvoetud")
    kehtivus = _child(meta, "kehtivus")
    until = _path_text(kehtivus, "kehtivuseLopp") if kehtivus is not None else ""
    title = _path_text(root, "aktinimi", "nimi", "pealkiri")
    return ActMetadata(
        global_id=_path_text(meta, "globaalID"),
        group_id=_path_text(meta, "terviktekstiGrupiID"),
        title=_WS_RE.sub(" ", title).strip(),
        language=language,
        publication=publication,
        publication_date=_date(_path_text(pub_el, "avaldamineKuupaev")) if pub_el is not None else "",
        document_type=_path_text(meta, "dokumentLiik"),
        text_type=_path_text(meta, "tekstiliik"),
        issuer=_path_text(meta, "valjaandja"),
        abbreviation=_path_text(meta, "lyhend"),
        adopted_on=_date(_path_text(adopted, "aktikuupaev")) if adopted is not None else "",
        entry_into_force=_date(_path_text(adopted, "joustumine")) if adopted is not None else "",
        original_publication=_publication(_child(adopted, "avaldamismarge")) if adopted is not None else "",
        in_force_from=_date(_path_text(kehtivus, "kehtivuseAlgus")) if kehtivus is not None else "",
        in_force_until=_date(until) or None,
        schema=_path_text(meta, "skeemiNimi"),
        version_date=_date(_path_text(meta, "versioon", "dokumentVersioonKuupaev")),
    )


def sha256_of(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _parse_root(path: Path | str) -> tuple[ET.Element, str]:
    data = Path(path).read_bytes()
    root = ET.fromstring(data)
    if _local(root.tag) != "oigusakt":
        raise ValueError(f"{path}: root element is <{_local(root.tag)}>, expected <oigusakt>")
    return root, hashlib.sha256(data).hexdigest()


def parse_metadata(path: Path | str) -> ActMetadata:
    root, _ = _parse_root(path)
    return _parse_metadata(root)


def load_act(path: Path | str) -> Act:
    root, digest = _parse_root(path)
    return Act(Path(path), root, digest)


def provision_rt_ids(path: Path | str) -> list[str]:
    """Every structural id in the file (provision and unit elements) in document order —
    used by the bijection round-trip test; not by the resolver."""
    root, _ = _parse_root(path)
    out: list[str] = []
    for el in root.iter():
        name = _local(el.tag)
        if name in ("paragrahv", "loige", "alampunkt", "punkt", "osa", "peatykk", "jagu", "jaotis", "alljaotis"):
            rt_id = el.get("id", "")
            if rt_id and not re.fullmatch(r"[0-9a-f-]{36}", rt_id):
                out.append(rt_id)
    return out


__all__ = [
    "MARKER_LINE_RE",
    "SCHEMA_NAME",
    "Act",
    "ActMetadata",
    "EidPart",
    "Provision",
    "ProvisionNotFound",
    "Unit",
    "eid_to_rt_id",
    "load_act",
    "parse_metadata",
    "provision_rt_ids",
    "rt_id_to_eid",
    "sha256_of",
]
