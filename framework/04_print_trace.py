"""Step 4: print the plain-text reasoning trace for the solved case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from logic_levels import render_solution_trace
from schemas import SolutionArtifact


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the explanation step."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", required=True, help="Path to the checked solution JSON.")
    parser.add_argument("--out", help="Optional output file for the plain-text trace.")
    return parser.parse_args()


def main() -> None:
    """Read a solution artifact and print or persist the trace output."""
    args = parse_args()
    raw = json.loads(Path(args.solution).read_text(encoding="utf-8"))
    solution = SolutionArtifact.model_validate(raw)
    rendered = render_solution_trace(solution)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
