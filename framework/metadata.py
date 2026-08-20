"""Small metadata helpers for `framework` artifacts and logs."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path


def utc_timestamp() -> str:
    """Return the current UTC timestamp in a stable ISO-8601 form."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    """Return the SHA-256 digest for the supplied text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized_path(path: str | Path | None) -> str | None:
    """Return an absolute path string when a path is provided."""
    if path is None:
        return None
    return str(Path(path).expanduser().resolve())
