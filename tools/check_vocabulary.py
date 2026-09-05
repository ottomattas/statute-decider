#!/usr/bin/env python3
"""One vocabulary, English, everywhere a reader or a model can see it.

Operator ruling of 2026-09-05: every live file uses the current identifiers
(``<act_slug>``, ``<act_slug>/<eId>``, ``<case>/<scenario>``, ``llm-only`` /
``architecture`` / ``llm-decides-on-*``) and plain English. The Estonian XML
sources under ``data/sources/legislation/ee/`` and their catalogue entries are
the only permitted Estonian content, together with git history.

Three classes of hit, each fatal:

* **A — retired identifiers.** Every *old* key of ``tools/rename_map.yaml``
  (statutes, clause ids, cases, registers, scenarios, conditions, experiments,
  prompt variants) plus the v1 tag/scenario fragments (``via_db``, ``u3_``,
  ``db-then-user``, ...) and the Estonian act abbreviations (``MMS § 11``).
  ``baseline`` / ``candidate`` are English words, so they are flagged only
  where they name a condition (backticked, ``condition baseline``, ``baseline
  run``, ``baseline.yaml``, ...).
* **B — Riigi Teataja element ids** (``para11lg5p1``) and Estonian citation
  style (``§ 42 lg 1``). The reference vocabulary is the eId and the display
  form ``§ 42 (1)``.
* **C — Estonian.** Any Estonian diacritic and a list of Estonian legal /
  common words, case-insensitive, whole-word, with and without diacritics.

Exclusions (why):

* ``data/sources/legislation/ee/**`` and every ``*.akt`` — the official texts
  (next phase; the only permitted Estonian content). ``catalogue.json`` keeps
  the ``et`` titles and the raw ``<dokumentLiik>`` value, so class C is
  skipped there; classes A and B still apply.
* ``docs/reference/id-aliases.md`` and ``tools/rename_map.yaml`` — the
  old → new map itself; ``tools/rename_ids.py`` consumes the map.
* ``src/statute_decider/legislation/riigiteataja.py``,
  ``tests/test_legislation.py``, ``docs/reference/legislation-corpus.md`` —
  the RT-id <-> eId bijection, its tests and its documentation: they must
  spell the RT ids and the RT XML element names (``paragrahv``, ``loige``,
  ``alampunkt``) and the parser emits the ``et`` rendering markers. Classes B
  and C skipped; class A applies. ``legislation/catalogue.py`` and
  ``legislation/corpus.py`` name raw RT XML values/attributes
  (``<dokumentLiik>``, ``terviktekstiGrupiID``); class C skipped.
* ``experiments/*/results/**`` except ``summary.md`` — the audit trail of what
  was sent and produced (``transcript.jsonl``, ``run.log``, config snapshots)
  is never rewritten; ``summary.md`` is regenerated from the current
  ``experiment.yaml`` and is checked.
* ``experiments/_chains/**`` — gitignored raw logs.
* No source-language exception anywhere else: the teaching example's Estonian
  text (``road_traffic_act_et_full.txt``) left the repo on 2026-09-06 and is
  archived in the ES inbox; its English translation is scanned like any file.
* Proper nouns that are English usage (Riigi Teataja, Estonia, Tallinn,
  Tartu) and the authors' names are stripped from a line before class C runs.
* This file and its test spell every pattern, so they skip themselves.

Usage: ``python tools/check_vocabulary.py [--root DIR] [--summary]``; exit 1
on any hit. ``tests/test_vocabulary.py`` runs it with the suite. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

ROOT = Path(__file__).resolve().parents[1]
RENAME_MAP = "tools/rename_map.yaml"

# --------------------------------------------------------------------------- scope

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
SKIP_DIR_SUFFIXES = (".egg-info",)
SKIP_SUFFIXES = {".akt", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".svg", ".pyc", ".zip", ".gz"}
# path prefixes (relative, posix) skipped entirely
SKIP_PREFIXES = (
    "data/sources/legislation/ee/",
    "experiments/_chains/",
)
# files skipped entirely (the old -> new map and the tool that applies it)
SKIP_FILES = {
    "docs/reference/id-aliases.md",
    RENAME_MAP,
    "tools/rename_ids.py",
    "tools/check_vocabulary.py",
    "tests/test_vocabulary.py",
}
# per-file class exemptions
EXEMPT_CLASSES: dict[str, set[str]] = {
    "src/statute_decider/legislation/riigiteataja.py": {"B", "C"},
    "tests/test_legislation.py": {"B", "C"},
    "docs/reference/legislation-corpus.md": {"B", "C"},
    "src/statute_decider/legislation/catalogue.py": {"C"},
    "src/statute_decider/legislation/corpus.py": {"C"},
    "data/sources/legislation/catalogue.json": {"C"},
}
RESULTS_KEEP = {"summary.md"}

# proper nouns and names that are English usage; removed before class C
ALLOWED_PHRASES = [
    "Riigi Teataja",
    "Estonia",
    "Estonian",
    "Tallinn",
    "Tartu",
    "Mättas",
    "Järv",
    "Tammet",
]

# --------------------------------------------------------------------------- class A

# v1 tag / scenario fragments and Estonian act abbreviations that the map does not list as keys
EXTRA_RETIRED = [
    r"via_db",
    r"db-then-user",
    r"db_then_user",
    r"need-db",
    r"need-user",
    r"prompt-swap",
    r"unrelated-law",
    r"u[3578]_",  # u3_no_register, u8_need_user
    r"U[3578] (?:UNVERIFIABLE_CLAIM|NEED_[A-Z_]+)",  # "U3 UNVERIFIABLE_CLAIM" in scenario descriptions
]
TAG_LINE_RE = re.compile(r"^\s*-\s*(u[3578]|via_db|db-then-user|prompt-swap|unrelated-law)\s*$")
ACT_ABBREV_RE = re.compile(r"\b(EhS|ATS|MMS|IKS|VÕS|VOS|PKS)\s+§")
HOMEMADE_CLAUSE_RE = re.compile(r"(?<![A-Za-z0-9_])(mms|vos|ehs|es|ats|iks|pks)_\d+(?:_\d+)*(?:_[a-z]+)?(?![A-Za-z0-9_])")
# baseline / candidate only where they name a condition
CONDITION_WORD_RES = [
    re.compile(r"`(baseline|candidate)`"),
    re.compile(r"\((baseline|candidate)\)"),
    re.compile(r"\b(baseline|candidate)(?:'s)? (condition|run|cell|grid|config)\b", re.I),
    re.compile(r"\bcondition[: ]+(baseline|candidate)\b", re.I),
    re.compile(r"\b(baseline|candidate)\.yaml\b"),
    re.compile(r"--condition (baseline|candidate)\b"),
    re.compile(r"oracle ?(/|→|->) ?baseline ?(/|→|->) ?candidate", re.I),
]


def _parse_rename_map(path: Path) -> dict[str, dict[str, str]]:
    """Minimal reader for the two-level ``section:\\n  old: new`` blocks (stdlib only)."""
    sections: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        if not line.startswith(" "):
            current = line.rstrip(":").strip()
            sections[current] = {}
            continue
        if current is None or line.startswith("    "):
            continue  # nested (scenario_fields) — not an id map
        if ":" not in line:
            continue
        key, _, value = line.strip().partition(":")
        sections[current][key.strip()] = value.strip()
    return sections


def retired_tokens(rename_map: Path) -> list[str]:
    """Every old id from the map that differs from its new id, as literal tokens."""
    sections = _parse_rename_map(rename_map)
    tokens: set[str] = set()
    for name in ("statutes", "clauses", "cases", "registers", "conditions", "experiments"):
        for old, new in sections.get(name, {}).items():
            if old != new:
                tokens.add(old)
    for old, new in sections.get("prompts", {}).items():
        if old != new:
            tokens.add(old.rsplit("/", 1)[-1])  # variant name, e.g. solver-inputs-v1
    for old in sections.get("scenarios", {}):
        tokens.add(old)  # old_case/old_scenario composite
        scenario = old.split("/", 1)[-1]
        if "_" in scenario or "-" in scenario:  # skip bare words: allow, deny
            tokens.add(scenario)
    # plain English words handled by CONDITION_WORD_RES
    tokens -= {"baseline", "candidate"}
    return sorted(tokens, key=len, reverse=True)


def build_retired_re(tokens: Iterable[str]) -> re.Pattern[str]:
    alts = [re.escape(t) for t in tokens] + EXTRA_RETIRED
    return re.compile(r"(?<![A-Za-z0-9_/-])(?:" + "|".join(alts) + r")(?![A-Za-z0-9_-])")


# --------------------------------------------------------------------------- class B

RT_ID_RE = re.compile(r"\bpara\d+lg\d*(?:p\d+)?(?:b\d+)?\b|\bpara\d+b\d+\b")
ET_CITATION_RE = re.compile(r"§\s?\d+\s+lg\b|\blg\s\d+\b|\b\d+\s+p\s\d+\)")

# --------------------------------------------------------------------------- class C

DIACRITIC_RE = re.compile(r"[õäöüšžÕÄÖÜŠŽ]")
ESTONIAN_WORDS = [
    # the brief's list
    "tarbija", "ettevõtja", "ehitusluba", "leping", "taganemis", "tähtaeg", "elamumaa",
    "omanik", "pensionär", "kodualune", "maamaks", "lõige", "punkt", "paragrahv", "seadus",
    "seadustik", "määrus", "riigikogu", "rahvastikuregister", "kinnistusraamat", "avaldus",
    "kohalik omavalitsus", "omavalitsus", "volikogu", "teenistus", "ametnik", "isikuandmed",
    "ajakirjandus", "eesti", "hooldusõigus", "vanem",
    # met on the way (2026-09-05 sweep)
    "elukoht", "riigilõiv", "nõusolek", "tellimustöö", "pädev", "detailplaneering",
    "ehitusnõue", "ehitusuuring", "sihtotstarve", "maatulundusmaa", "e-pood", "avalik huvi",
    "sõlmitud", "kahjusta", "vastuolus", "kodanik", "karistus", "keeleoskus",
    "haridus", "kinnistu", "maksuvabastus", "esindus", "hädaolukord", "taotlus",
    "soodustus", "isiklikud", "vajadused", "sidevahendi", "ülemäära", "tüüpi",
    "jõust", "kehtetu", "terviktekst", "loige", "alampunkt", "peatykk", "jaotis",
]
# stems that collide with English once a suffix is allowed (nous) — matched as
# whole words only. ``lapse`` (genitive of "child") was dropped 2026-09-06: it is
# also the English noun ("lapse of the suspension" in the Road Traffic Act
# translation) and the texts it guarded against are gone.
ESTONIAN_EXACT_WORDS = ["vastab", "nõus", "abil"]
_TRANSLIT = str.maketrans("õäöüšž", "oaousz")


def _word_variants(word: str) -> set[str]:
    return {word, word.translate(_TRANSLIT)}


def build_estonian_re(words: Iterable[str], exact: Iterable[str] = ()) -> re.Pattern[str]:
    stems: set[str] = set()
    for w in words:
        stems |= _word_variants(w)
    whole: set[str] = set()
    for w in exact:
        whole |= _word_variants(w)
    stem_alts = "|".join(sorted((re.escape(s) for s in stems), key=len, reverse=True))
    whole_alts = "|".join(sorted((re.escape(s) for s in whole), key=len, reverse=True))
    # a stem may carry an Estonian case ending; an exact word may not
    return re.compile(
        r"(?<![A-Za-z])(?:(?:" + stem_alts + r")[a-zõäöüšž]*|(?:" + whole_alts + r"))(?![A-Za-z])",
        re.I,
    )


# --------------------------------------------------------------------------- scan


@dataclass(frozen=True)
class Hit:
    path: str
    line: int
    cls: str
    match: str
    text: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: [{self.cls}] {self.match!r}  |  {self.text.strip()[:140]}"


def iter_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        if any(p in SKIP_DIRS or p.endswith(SKIP_DIR_SUFFIXES) for p in parts[:-1]):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if rel in SKIP_FILES or rel.startswith(SKIP_PREFIXES):
            continue
        if len(parts) >= 3 and parts[0] == "experiments" and parts[2] == "results" and path.name not in RESULTS_KEEP:
            continue
        yield path


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def _strip_allowed(line: str) -> str:
    for phrase in ALLOWED_PHRASES:
        line = line.replace(phrase, " ")
    return line


def scan(root: Path = ROOT) -> list[Hit]:
    retired_re = build_retired_re(retired_tokens(root / RENAME_MAP))
    estonian_re = build_estonian_re(ESTONIAN_WORDS, ESTONIAN_EXACT_WORDS)
    hits: list[Hit] = []
    for path in iter_files(root):
        text = _read(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        exempt = EXEMPT_CLASSES.get(rel, set())
        for no, line in enumerate(text.splitlines(), start=1):
            if "A" not in exempt:
                for m in retired_re.finditer(line):
                    hits.append(Hit(rel, no, "A", m.group(0), line))
                if TAG_LINE_RE.match(line):
                    hits.append(Hit(rel, no, "A", line.strip(), line))
                for m in ACT_ABBREV_RE.finditer(line):
                    hits.append(Hit(rel, no, "A", m.group(0), line))
                for m in HOMEMADE_CLAUSE_RE.finditer(line):
                    hits.append(Hit(rel, no, "A", m.group(0), line))
                for rx in CONDITION_WORD_RES:
                    for m in rx.finditer(line):
                        hits.append(Hit(rel, no, "A", m.group(0), line))
            if "B" not in exempt:
                for m in RT_ID_RE.finditer(line):
                    hits.append(Hit(rel, no, "B", m.group(0), line))
                for m in ET_CITATION_RE.finditer(line):
                    hits.append(Hit(rel, no, "B", m.group(0), line))
            if "C" not in exempt:
                clean = _strip_allowed(line)
                for m in DIACRITIC_RE.finditer(clean):
                    hits.append(Hit(rel, no, "C", m.group(0), line))
                for m in estonian_re.finditer(clean):
                    hits.append(Hit(rel, no, "C", m.group(0), line))
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--summary", action="store_true", help="print counts per class and file group only")
    args = ap.parse_args(argv)
    hits = scan(args.root.resolve())
    if args.summary or hits:
        by_class = Counter(h.cls for h in hits)
        by_group = Counter((h.cls, h.path.split("/", 1)[0]) for h in hits)
        print(f"check_vocabulary: {len(hits)} hit(s)  A={by_class['A']} B={by_class['B']} C={by_class['C']}")
        for (cls, group), n in sorted(by_group.items()):
            print(f"  [{cls}] {group}: {n}")
    if not args.summary:
        for h in hits:
            print(h.format())
    if not hits:
        print("check_vocabulary: OK — no retired ids, RT element ids or Estonian outside the permitted paths")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
