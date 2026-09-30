"""sd list reads the committed inventory and the premise_outcome gold."""

from statute_decider.cli import main


def test_list_shows_the_balanced_inventory(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "6 cases, 54 scenarios, 18/18/18" in out
    assert "building_permit_grant" in out
    assert "ALLOW 3 DENY 3 NEED_MORE_INFO 3" in out


def test_list_scenarios_include_tags_and_gold(capsys):
    assert main(["list", "--scenarios"]) == 0
    out = capsys.readouterr().out
    assert "6 cases, 54 scenarios, 18/18/18" in out
    rows = [line for line in out.splitlines() if line.startswith("land_tax_home_exemption\t")]
    assert len(rows) == 9
    assert any(line.endswith("\tALLOW") or line.endswith("\tDENY") or line.endswith("\tNEED_MORE_INFO") for line in rows)
    assert all(line.count("\t") == 3 for line in rows)
