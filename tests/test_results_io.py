"""Gzip transcript I/O: round-trip, multi-member resume, find, plain open."""

from __future__ import annotations

import gzip

import pytest

from statute_decider.results import (
    TranscriptWriter,
    compress_plain,
    find_transcript,
    iter_jsonl,
    open_text,
)


def test_gzip_round_trip(tmp_path):
    path = tmp_path / "transcript.jsonl.gz"
    writer = TranscriptWriter(path)
    writer.write({"n": 1, "text": "€"})
    writer.write({"n": 2})
    writer.close()
    rows = list(iter_jsonl(path))
    assert [row["n"] for row in rows] == [1, 2]
    assert rows[0]["text"] == "€"


def test_two_writer_sessions_are_one_readable_file(tmp_path):
    path = tmp_path / "transcript.jsonl.gz"
    first = TranscriptWriter(path)
    first.write({"n": 1})
    first.close()
    second = TranscriptWriter(path)
    second.write({"n": 2})
    second.write({"n": 3})
    second.close()
    assert [row["n"] for row in iter_jsonl(path)] == [1, 2, 3]


def test_find_transcript_prefers_gz(tmp_path):
    (tmp_path / "transcript.jsonl").write_text('{"plain": true}\n', encoding="utf-8")
    gz = tmp_path / "transcript.jsonl.gz"
    with gzip.open(gz, "wt", encoding="utf-8") as handle:
        handle.write('{"gz": true}\n')
    assert find_transcript(tmp_path) == gz
    assert find_transcript(tmp_path / "missing") is None


def test_compress_plain_leaves_matching_gz(tmp_path):
    plain = tmp_path / "transcript.jsonl"
    plain.write_text('{"n": 1}\n', encoding="utf-8")
    gz = compress_plain(plain)
    first = gz.read_bytes()
    again = compress_plain(plain, delete_plain=True)
    assert again == gz
    assert gz.read_bytes() == first
    assert not plain.exists()


def test_compress_plain_rejects_mismatch(tmp_path):
    plain = tmp_path / "transcript.jsonl"
    plain.write_text('{"n": 1}\n', encoding="utf-8")
    gz = compress_plain(plain)
    plain.write_text('{"n": 2}\n', encoding="utf-8")
    with pytest.raises(RuntimeError, match="does not match"):
        compress_plain(plain)
    assert gz.exists()


def test_open_text_plain(tmp_path):
    path = tmp_path / "rows.jsonl"
    path.write_text('{"a": 1}\n', encoding="utf-8")
    with open_text(path, "rt") as handle:
        assert handle.read() == '{"a": 1}\n'
    assert list(iter_jsonl(path)) == [{"a": 1}]
