"""Ruling H: the statute input is the whole act or the smallest official
structural unit enclosing the declared provisions, within a token budget."""

import pytest

from statute_decider.legislation import (
    UnitTooLarge,
    estimate_tokens,
    parse_reference,
    select_statute_unit,
    unit_candidates,
)
from statute_decider.legislation.references import display_eid, parse_eid


def test_structural_path_eids_parse_and_display():
    assert [p.render() for p in parse_eid("part_1__chp_2__dvs_4")] == ["part_1", "chp_2", "dvs_4"]
    assert display_eid("part_1__chp_2__dvs_4") == "Part 1 Chapter 2 Division 4"
    assert display_eid("chp_2__dvs_1") == "Chapter 2 Division 1"  # a level may be skipped
    with pytest.raises(ValueError):
        parse_eid("dvs_4__chp_2")  # must descend
    with pytest.raises(ValueError):
        parse_eid("chp_2__chp_3")
    with pytest.raises(ValueError):
        parse_eid("chp_2__sec_5")  # provisions are not addressed through units
    parse_reference("law_of_obligations_act/part_1__chp_2__dvs_4")


def test_estimate_tokens_is_chars_over_four_rounded_up():
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2


def test_units_nest_and_sections_know_their_unit(store):
    act = store.statute_act("law_of_obligations_act")
    units = act.units()
    assert units and units[0].path == "part_1" and units[0].depth == 0
    dvs4 = act.unit("part_1__chp_2__dvs_4")
    assert dvs4.level == "dvs" and dvs4.eid == "dvs_4" and dvs4.depth == 2
    assert [u.path for u in dvs4.ancestors()] == ["part_1", "part_1__chp_2"]
    assert act.unit_of["sec_56"] is dvs4
    # level-local numbers repeat across the act; the path is unique
    assert len({u.path for u in units}) == len(units)
    assert len({u.eid for u in units}) < len(units)


def test_enclosing_units_is_the_common_ancestor_chain(store):
    act = store.statute_act("law_of_obligations_act")
    chain = act.enclosing_units(["sec_53__subsec_4", "sec_56__subsec_1"])
    assert [u.path for u in chain] == ["part_1", "part_1__chp_2", "part_1__chp_2__dvs_4"]
    # a provision from another chapter cuts the chain at the part
    assert [u.path for u in act.enclosing_units(["sec_53", "sec_76"])] == ["part_1"]
    # an act without structural units has no enclosing unit
    assert store.statute_act("land_tax_act").enclosing_units(["sec_11"]) == []


def test_render_unit_keeps_official_headings_and_numbering(store):
    act = store.statute_act("law_of_obligations_act")
    text = act.render_unit("part_1__chp_2__dvs_4")
    assert text.startswith("Law of Obligations Act\n")
    assert "Structural unit: Part 1 GENERAL PART › Chapter 2 CONTRACT › Subchapter 4 Distance Contracts" in text
    assert "\nSubchapter 4 Distance Contracts\n" in text
    assert "§ 52. Definition of distance contract" in text and "§ 62. Mandatory nature of provisions" in text
    assert "§ 63." not in text and "§ 51." not in text  # neighbours stay out
    # the unit's provisions render exactly as in the whole act
    full = act.render_full()
    para56 = act.render_provision("sec_56")
    assert para56 in text and para56 in full


def test_select_whole_act_when_it_fits(store):
    act = store.statute_act("land_tax_act")
    choice = select_statute_unit(act, ["sec_11"], max_tokens=100_000)
    assert choice.is_whole_act and choice.kind == "act" and choice.eid == "act"
    assert choice.text == act.render_full()
    assert choice.tokens_estimate == estimate_tokens(choice.text) <= 100_000


def test_select_smallest_enclosing_unit_when_act_exceeds_budget(store):
    act = store.statute_act("law_of_obligations_act")
    spec = store.statute_spec("law_of_obligations_act")
    choice = select_statute_unit(act, spec.provisions, max_tokens=100_000)
    assert not choice.is_whole_act
    assert choice.kind == "division" and choice.eid == "part_1__chp_2__dvs_4"
    assert choice.display.endswith("Subchapter 4 Distance Contracts")
    assert choice.tokens_estimate < 20_000
    kinds = [c.kind for c in choice.candidates]
    assert kinds == ["act", "part", "chapter", "division"]
    assert [c.tokens_estimate for c in choice.candidates] == sorted(
        (c.tokens_estimate for c in choice.candidates), reverse=True
    )


def test_select_is_strict_smallest_not_first_that_fits(store):
    """The chapter would also fit a 100k budget; the ruling says the smallest unit."""
    act = store.statute_act("law_of_obligations_act")
    cands = unit_candidates(act, ["sec_53__subsec_4", "sec_56__subsec_1"])
    chapter = next(c for c in cands if c.kind == "chapter")
    assert chapter.tokens_estimate <= 100_000
    choice = select_statute_unit(act, ["sec_53__subsec_4", "sec_56__subsec_1"], max_tokens=100_000)
    assert choice.kind == "division"


def test_select_raises_when_even_the_smallest_unit_is_too_large(store):
    act = store.statute_act("law_of_obligations_act")
    with pytest.raises(UnitTooLarge):
        select_statute_unit(act, ["sec_53__subsec_4"], max_tokens=1_000)
    land = store.statute_act("land_tax_act")
    with pytest.raises(UnitTooLarge):
        select_statute_unit(land, ["sec_11"], max_tokens=100)


def test_statute_text_records_the_unit_on_every_act(store):
    expected = {
        "building_code": "act",
        "civil_service_act": "act",
        "family_law_act": "act",
        "land_tax_act": "act",
        "law_of_obligations_act": "part_1__chp_2__dvs_4",
        "personal_data_protection_act": "act",
    }
    for statute_id, eid in expected.items():
        text = store.statute_text(statute_id)
        record = text.statute_input()
        assert record["unit"]["eid"] == eid, statute_id
        assert record["act"] == statute_id and record["max_tokens"] == 100_000
        assert record["tokens_estimate"] <= 100_000 and record["declared_provisions"]
        assert set(record) >= {"act", "global_id", "sha256", "unit", "declared_provisions"}
    small = store.statute_text("building_code", max_tokens=50_000)
    assert small.method == "unit" and small.unit.eid == "part_1__chp_4__dvs_2"
