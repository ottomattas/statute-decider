"""The legislation package: RT-id <-> eId bijection, slicing, metadata, references."""

import pytest

from statute_decider.legislation import (
    display_eid,
    display_reference,
    eid_to_rt_id,
    is_within,
    parse_reference,
    rt_id_to_eid,
    validate_eid,
)
from statute_decider.legislation.corpus import Corpus
from statute_decider.legislation.riigiteataja import (
    ProvisionNotFound,
    load_act,
    provision_rt_ids,
)


@pytest.fixture(scope="session")
def corpus(root):
    corpus = Corpus(root / "data" / "sources" / "legislation")
    if not corpus.catalogue.entries:
        pytest.skip("corpus not ingested (sd corpus ingest-dir)")
    return corpus


@pytest.fixture(scope="session")
def land_tax_act(corpus):
    return corpus.load(corpus.entry_for("land_tax_act", "en").global_id)


# --- bijection ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("rt_id", "eid"),
    [
        ("para11", "sec_11"),
        ("para11b1", "sec_11_1"),
        ("para11lg1", "sec_11__subsec_1"),
        ("para11lg1b1", "sec_11__subsec_1_1"),
        ("para11lg5p1", "sec_11__subsec_5__point_1"),
        ("para53lg4p4b1", "sec_53__subsec_4__point_4_1"),
        ("para54b1lg1p13b1", "sec_54_1__subsec_1__point_13_1"),
        ("ptk3", "chp_3"),
        ("jg2", "dvs_2"),
        ("osa1", "part_1"),
    ],
)
def test_bijection_examples(rt_id, eid):
    assert rt_id_to_eid(rt_id) == eid
    assert eid_to_rt_id(eid) == rt_id


def test_bijection_rejects_unknown_shapes():
    with pytest.raises(ValueError):
        rt_id_to_eid("para11lg1x2")
    with pytest.raises(ValueError):
        rt_id_to_eid("8c12c4b4-dae8-48c1-8d57-60605d40ba17")
    with pytest.raises(ValueError):
        eid_to_rt_id("sec_11__point_1")  # point without subsection
    with pytest.raises(ValueError):
        validate_eid("subsec_1")


def test_bijection_round_trips_every_id_in_the_corpus(corpus):
    """Every structural id in all 14 files survives rt -> eId -> rt (parts: ``o1`` is the
    English spelling of ``osa1``; both map to ``part_1``, the inverse is canonical ``osa``)."""
    checked = 0
    for entry in corpus.catalogue.entries:
        for rt_id in provision_rt_ids(corpus.path_of(entry)):
            eid = rt_id_to_eid(rt_id)
            back = eid_to_rt_id(eid)
            if rt_id.startswith("o") and not rt_id.startswith("osa"):
                assert back == "osa" + rt_id[1:]
            else:
                assert back == rt_id, (entry.file, rt_id, eid, back)
            checked += 1
    assert checked > 10000


def test_every_act_loads_and_indexes_unique_provisions(corpus):
    for entry in corpus.catalogue.entries:
        act = corpus.load(entry.global_id)
        assert act.metadata.global_id == entry.global_id
        assert act.sha256 == entry.sha256
        assert len(act.index) > 50
        for eid in act.index:
            validate_eid(eid)


# --- slicing -------------------------------------------------------------------------


def test_slice_section_yields_all_subsections(land_tax_act):
    text = land_tax_act.render_slice(["sec_11"])
    assert text.startswith("Land Tax Act — selected provisions: § 11\n")
    assert "§ 11. Tax incentives" in text
    for marker in ("(1) ", "(1¹) ", "(2) ", "(5) ", "1) pension recipients", "2) persons who", "(7) ", "(9) "):
        assert marker in text, marker
    assert "§ 10." not in text and "§ 12" not in text


def test_slice_point_yields_exactly_that_clause(land_tax_act):
    assert (
        land_tax_act.render_provision("sec_11__subsec_5__point_1")
        == "1) pension recipients based on the State Pension Insurance Act;"
    )
    sliced = land_tax_act.render_slice(["sec_11__subsec_5__point_1"])
    # heading + the enumerating lead-in of the undeclared parent, then the one clause
    assert "§ 11. Tax incentives" in sliced
    assert "(5) The municipal council may determine" in sliced
    assert "1) pension recipients" in sliced
    assert "2) persons who" not in sliced
    assert "(1) The municipal council may establish" not in sliced


def test_strip_markers_drops_amendment_lines_but_keeps_repeals(land_tax_act):
    kept = land_tax_act.render_provision("sec_11__subsec_1")
    assert "[RT I, 30.06.2024, 1 - entry into force 01.03.2025]" in kept
    stripped = land_tax_act.render_provision("sec_11__subsec_1", strip_markers=True)
    assert "[RT I" not in stripped
    assert "(1) The municipal council may establish" in stripped
    repealed = land_tax_act.render_provision("sec_11__subsec_4", strip_markers=True)
    assert repealed.startswith("(4) [Repealed")


def test_superscripts_and_unnumbered_subsections(corpus):
    ats = corpus.load(corpus.entry_for("civil_service_act", "en").global_id)
    assert ats.display("sec_15__subsec_1__point_1") == "§ 15 1)"
    assert ats.provision("sec_15__subsec_1").display_number == ""
    assert "§ 15. Persons who may not be employed in service" in ats.render_slice(["sec_15__subsec_1__point_1"])
    land = corpus.load(corpus.entry_for("land_tax_act", "en").global_id)
    assert land.display("sec_11__subsec_1_1") == "§ 11 (1¹)"
    assert land.provision("sec_11__subsec_1_1").display_number == "(1¹)"
    assert land.provision("sec_12_1").display_number == "§ 12¹."


def test_english_note_subsections_are_not_provisions(corpus):
    """An unnumbered <loige id="paraNlg1"> next to a numbered (1) is a section-level note."""
    ats = corpus.load(corpus.entry_for("civil_service_act", "en").global_id)
    sec = ats.provision("sec_49")
    assert sec.notes and sec.notes[0].startswith("[RT I, 13.12.2014, 1")
    assert ats.provision("sec_49__subsec_1").display_number == "(1)"


def test_missing_provision_raises(land_tax_act):
    with pytest.raises(ProvisionNotFound):
        land_tax_act.provision("sec_999")
    with pytest.raises(ValueError):
        land_tax_act.provision("para11lg1")  # RT ids are not accepted anywhere


def test_full_render_size_and_header(land_tax_act):
    full = land_tax_act.render_full()
    assert full.startswith("Land Tax Act\nRT V, 05.01.2026, 5; in force from 01.01.2026\n")
    assert "§ 1. Land tax" in full and "§ 11. Tax incentives" in full
    assert 20000 < len(full) < 30000


# --- metadata --------------------------------------------------------------------------


def test_metadata_extraction(corpus):
    entry = corpus.entry_for("land_tax_act", "en")
    assert entry.global_id == "505012026005"
    assert entry.language == "en" and entry.jurisdiction == "ee"
    assert entry.publication == "RT V, 05.01.2026, 5"
    assert entry.in_force_from == "2026-01-01" and entry.in_force_until is None
    assert entry.adopted_on == "1993-05-06" and entry.entry_into_force == "1993-07-01"
    assert entry.original_publication == "RT I 1993, 24, 428"
    assert entry.schema_name == "tyviseadus_1_10.02.2010.xsd"
    assert entry.source_url == "https://www.riigiteataja.ee/en/akt/505012026005"
    assert entry.counterparts == ["130062024005"]
    et = corpus.entry("130062024005")
    assert et.language == "et" and et.act_slug == "land_tax_act" and et.title == "Maamaksuseadus"
    assert et.counterparts == ["505012026005"]
    meta = load_act(corpus.path_of(et)).metadata
    assert meta.in_force_from == "2026-01-01"  # timezone suffix normalised away


def test_catalogue_covers_seven_acts_in_two_languages(corpus):
    slugs = corpus.catalogue.act_slugs()
    assert slugs == [
        "building_code",
        "civil_service_act",
        "family_law_act",
        "land_tax_act",
        "law_of_obligations_act",
        "personal_data_protection_act",
        "public_information_act",
    ]
    for slug in slugs:
        assert {e.language for e in corpus.catalogue.by_slug(slug)} == {"en", "et"}


def test_check_is_clean(corpus):
    report = corpus.check()
    assert report.ok, report.render()


# --- references ----------------------------------------------------------------------


def test_reference_parsing_and_display():
    ref = parse_reference("land_tax_act/sec_11__subsec_5__point_1")
    assert ref.act_slug == "land_tax_act" and ref.eid == "sec_11__subsec_5__point_1"
    assert display_eid(ref.eid) == "§ 11 (5) 1)"
    assert display_eid("sec_11__subsec_1_1") == "§ 11 (1¹)"
    assert display_reference(ref, "Land Tax Act") == "Land Tax Act § 11 (5) 1)"
    assert is_within("sec_11__subsec_1", "sec_11") and not is_within("sec_110", "sec_11")
    with pytest.raises(ValueError):
        parse_reference("mms_11_1")
    with pytest.raises(ValueError):
        parse_reference("land_tax_act/para11lg1")


def test_display_reference_with_document(corpus):
    ats = corpus.load(corpus.entry_for("civil_service_act", "en").global_id)
    assert display_reference("civil_service_act/sec_15__subsec_1__point_4", act=ats) == "Civil Service Act § 15 4)"
