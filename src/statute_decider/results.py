"""On-disk results I/O: gzip is the only committed transcript format.

``transcript.jsonl.gz`` is the audit trail. A resume appends a second gzip
member (``gzip.open(..., "at")``); the stdlib reader concatenates members.
A leftover plain ``transcript.jsonl`` is read-only compatibility during
migration — writers never create one.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TextIO

TRANSCRIPT = "transcript.jsonl.gz"
TRANSCRIPT_PLAIN = "transcript.jsonl"
MAX_TRACKED_BYTES = 90 * 1024 * 1024


def transcript_path(results_dir: Path | str) -> Path:
    return Path(results_dir) / TRANSCRIPT


def find_transcript(results_dir: Path | str) -> Path | None:
    """Prefer the gzip transcript; fall back to a leftover plain file."""
    results_dir = Path(results_dir)
    gz = results_dir / TRANSCRIPT
    if gz.exists():
        return gz
    plain = results_dir / TRANSCRIPT_PLAIN
    if plain.exists():
        return plain
    return None


def open_text(path: Path | str, mode: str = "rt") -> TextIO:
    """Open a text file; ``.gz`` goes through ``gzip.open``."""
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8")
    return path.open(mode, encoding="utf-8")


def iter_jsonl(path: Path | str) -> Iterator[dict[str, Any]]:
    with open_text(path, "rt") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


class TranscriptWriter:
    """One gzip handle for the run. A later resume opens a new member."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = gzip.open(self.path, "at", encoding="utf-8")  # noqa: SIM115 — one handle per run

    def write(self, entry: dict[str, Any]) -> None:
        line = json.dumps(entry, ensure_ascii=False, default=str)
        with self._lock:
            self._handle.write(line + "\n")
            self._handle.flush()

    def close(self) -> None:
        with self._lock:
            if self._handle is not None:
                self._handle.close()
                self._handle = None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compress_plain(plain: Path, *, delete_plain: bool = False) -> Path:
    """Gzip ``transcript.jsonl`` → ``transcript.jsonl.gz``; verify a round-trip."""
    plain = Path(plain)
    if not plain.exists():
        raise FileNotFoundError(plain)
    gz = Path(str(plain) + ".gz")
    raw = plain.read_bytes()
    with gzip.open(gz, "wb") as handle:
        handle.write(raw)
    with gzip.open(gz, "rb") as handle:
        roundtrip = handle.read()
    if sha256_bytes(raw) != sha256_bytes(roundtrip):
        gz.unlink(missing_ok=True)
        raise RuntimeError(f"gzip round-trip sha256 mismatch for {plain}")
    if delete_plain:
        plain.unlink()
    return gz


def check_tree(root: Path | str) -> list[str]:
    """Return problems: tracked file > 90 MB, leftover plain, corrupt gzip."""
    root = Path(root)
    problems: list[str] = []
    try:
        toplevel = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        listed = (
            subprocess.check_output(
                ["git", "ls-files", "experiments"],
                cwd=root,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            if Path(toplevel).resolve() == root.resolve()
            else ""
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        listed = ""
    for rel in listed.splitlines():
        path = root / rel
        if path.is_file() and path.stat().st_size > MAX_TRACKED_BYTES:
            problems.append(
                f"tracked {rel} is {path.stat().st_size} bytes (limit {MAX_TRACKED_BYTES})"
            )
    for path in sorted(root.glob(f"experiments/*/results/{TRANSCRIPT_PLAIN}")):
        problems.append(f"plain transcript must not exist: {path.relative_to(root)}")
    for path in sorted(root.glob(f"experiments/*/results/{TRANSCRIPT}")):
        try:
            with gzip.open(path, "rb") as handle:
                while handle.read(1024 * 1024):
                    pass
        except OSError as exc:
            problems.append(f"gzip integrity failed {path.relative_to(root)}: {exc}")
    return problems
