"""Tiny local lookup helpers for the mock DB layer in `framework`.

Wave 2 Stream B (ART-64) adds two uncertainty-aware flags on
``LookupSource``:

- ``availability="unavailable"`` simulates the U3 (NO_REGISTER) case: the
  source covers the requested claims but is currently inaccessible, so we
  emit a ``LookupEvent`` with ``note="source_unavailable"`` and return
  ``None`` values for every requested claim.
- ``trust_only=True`` simulates the U7 (TRUST_ONLY) case: the source has
  no independent verification; it returns the stored values verbatim and
  the resulting ``LookupEvent`` carries ``note="trust_only"`` so the
  routing layer can flag the resolved claim as unverifiable.

All existing fixtures retain their pre-Wave-2 behaviour because the new
flags default to ``"available"`` / ``False``.
"""

from __future__ import annotations

import json
from pathlib import Path

from schemas import LookupEvent, LookupSource, MockDbArtifact


def load_mock_db(path: str | Path) -> MockDbArtifact:
    """Load and validate the mock DB artifact from disk."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return MockDbArtifact.model_validate(raw)


def _source_covers_any(source: LookupSource, requested_claim_ids: list[str]) -> list[str]:
    """Return the subset of requested claims this source declares coverage for.

    An unavailable source can still advertise that it *would* hold these
    values, so we rely on ``source.values`` as the coverage declaration.
    """
    return [claim_id for claim_id in requested_claim_ids if claim_id in source.values]


def lookup_claims(
    sources: list[LookupSource],
    requested_claim_ids: list[str],
    *,
    stage: str,
) -> tuple[dict[str, bool | None], list[LookupEvent]]:
    """Query all sources for the requested claims and record visible lookup events.

    Ordinary available sources behave exactly as before. Unavailable
    sources emit a ``source_unavailable`` lookup event without resolving
    any values (U3). Trust-only sources resolve values verbatim but mark
    the event with ``trust_only`` so the routing layer can escalate to U7.
    """
    resolved: dict[str, bool | None] = {}
    events: list[LookupEvent] = []
    for source in sources:
        if source.availability == "unavailable":
            covered = _source_covers_any(source, requested_claim_ids)
            if not covered:
                continue
            returned_none: dict[str, bool | None] = {claim_id: None for claim_id in covered}
            events.append(
                LookupEvent(
                    stage=stage,
                    source_id=source.source_id,
                    source_label=source.label,
                    requested_claim_ids=requested_claim_ids,
                    returned_values=returned_none,
                    note="source_unavailable",
                )
            )
            continue

        returned: dict[str, bool | None] = {}
        for claim_id in requested_claim_ids:
            if claim_id not in source.values:
                continue
            value = source.values[claim_id]
            returned[claim_id] = value
            if claim_id not in resolved:
                resolved[claim_id] = value
            elif resolved[claim_id] != value:
                resolved[claim_id] = None
        if returned:
            events.append(
                LookupEvent(
                    stage=stage,
                    source_id=source.source_id,
                    source_label=source.label,
                    requested_claim_ids=requested_claim_ids,
                    returned_values=returned,
                    note="trust_only" if source.trust_only else source.description,
                )
            )
    return resolved, events
