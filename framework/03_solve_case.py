"""Step 3: solve the case bundle with Z3 and record the reasoning trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from metadata import normalized_path, utc_timestamp
from reasoner import solve_case_bundle
from schemas import CaseBundle, DomainArtifact, IntentArtifact, MockDbArtifact, SolveRunMetadata


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the solve step."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True, help="Path to the checked domain JSON.")
    parser.add_argument("--intent", required=True, help="Path to the checked intent JSON.")
    parser.add_argument("--db", required=True, help="Path to the mock DB JSON.")
    parser.add_argument("--out", required=True, help="Where to write the checked solution JSON.")
    return parser.parse_args()


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    """Load the case bundle, solve it, and persist the solution JSON."""
    args = parse_args()
    domain = DomainArtifact.model_validate(_load_json(args.domain))
    intent = IntentArtifact.model_validate(_load_json(args.intent))
    mock_db = MockDbArtifact.model_validate(_load_json(args.db))
    if domain.logic_level != intent.logic_level:
        raise SystemExit("The domain and intent artifacts use different logic levels.")
    bundle = CaseBundle(
        logic_level=domain.logic_level,
        domain=domain,
        intent=intent,
        mock_db=mock_db,
    )
    solution = solve_case_bundle(bundle)
    solution.solve_metadata = SolveRunMetadata(
        generated_at_utc=utc_timestamp(),
        domain_artifact_path=normalized_path(args.domain),
        intent_artifact_path=normalized_path(args.intent),
        mock_db_path=normalized_path(args.db),
    )
    Path(args.out).write_text(solution.model_dump_json(indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
