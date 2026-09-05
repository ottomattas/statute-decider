"""One vocabulary, English, everywhere a reader or a model can see it (ruling of 2026-09-05).

Runs ``tools/check_vocabulary.py`` over the working tree: no retired identifiers,
no Riigi Teataja element ids, no Estonian outside the permitted paths (the XML
sources, their catalogue entries, the old -> new alias map and the bijection
module). The tool's docstring lists every exclusion and why.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_checker():
    name = "check_vocabulary"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / "check_vocabulary.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module  # dataclasses resolve postponed annotations through sys.modules
    spec.loader.exec_module(module)
    return module


def test_no_retired_ids_rt_ids_or_estonian_in_live_files():
    checker = _load_checker()
    hits = checker.scan(ROOT)
    assert not hits, "vocabulary violations:\n" + "\n".join(h.format() for h in hits[:200])


def test_checker_detects_each_class(tmp_path: Path):
    """The checker is not vacuous: one planted hit per class is reported."""
    checker = _load_checker()
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "rename_map.yaml").write_text(
        "statutes:\n  land_tax_exemption: mms_11\n  mms_11: land_tax_act\n"
        "conditions:\n  baseline: llm-only\n  llm-decider: llm-only-plus-rules\n"
        "scenarios:\n  section_120_demo/db-then-user: child_representation_by_one_parent/x\n",
        encoding="utf-8",
    )
    (tmp_path / "note.md").write_text(
        "statute mms_11 is retired\n"            # A: old statute id
        "condition llm-decider too\n"            # A: old condition name
        "the `baseline` condition\n"             # A: English word used as a condition name
        "tags:\n- via_db\n"                       # A: v1 tag line
        "cite para11lg5p1 here\n"                # B: RT element id
        "see § 42 lg 1\n"                        # B: Estonian citation style
        "the tarbija signed the leping\n"        # C: Estonian words, no diacritics
        "Võlaõigusseadus\n"                      # C: diacritics
        "memory lapses are English\n"            # not a hit: exact-word rule (lapse != lapses)
        "Riigi Teataja publishes in Tallinn\n",  # not a hit: allowed proper nouns
        encoding="utf-8",
    )
    hits = checker.scan(tmp_path)
    classes = {(h.cls, h.line) for h in hits}
    assert ("A", 1) in classes and ("A", 2) in classes and ("A", 3) in classes and ("A", 5) in classes
    assert ("B", 6) in classes and ("B", 7) in classes
    assert ("C", 8) in classes and ("C", 9) in classes
    assert all(h.line not in (10, 11) for h in hits), [h.format() for h in hits if h.line in (10, 11)]
