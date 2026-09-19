"""sd transcript compress / check."""

from __future__ import annotations

from statute_decider.cli import main
from statute_decider.results import iter_jsonl


def _repo_stub(tmp_path):
    (tmp_path / "configs").mkdir()
    (tmp_path / "data").mkdir()
    results = tmp_path / "experiments" / "demo" / "results"
    results.mkdir(parents=True)
    return results


def test_compress_round_trip(tmp_path):
    results = _repo_stub(tmp_path)
    plain = results / "transcript.jsonl"
    lines = ['{"n": 1, "text": "€"}', '{"n": 2}']
    plain.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "transcript",
                "compress",
                "demo",
                "--delete-plain",
            ]
        )
        == 0
    )
    gz = results / "transcript.jsonl.gz"
    assert gz.exists()
    assert not plain.exists()
    assert [row["n"] for row in iter_jsonl(gz)] == [1, 2]


def test_check_flags_plain_transcript(tmp_path):
    results = _repo_stub(tmp_path)
    (results / "transcript.jsonl").write_text("{}\n", encoding="utf-8")
    assert main(["--root", str(tmp_path), "transcript", "check"]) == 1
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "transcript",
                "compress",
                "demo",
                "--delete-plain",
            ]
        )
        == 0
    )
    assert main(["--root", str(tmp_path), "transcript", "check"]) == 0
