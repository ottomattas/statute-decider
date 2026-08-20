"""Step 2: extract the law text into a checked domain artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from llm import extract_domain_artifact
from schemas import LogicLevel


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the domain extraction step."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--use-case-dir",
        required=True,
        help="Directory under examples/ that contains use_case.json and default prompts.",
    )
    parser.add_argument(
        "--logic-level",
        choices=[level.value for level in LogicLevel],
        default=LogicLevel.PROPOSITIONAL.value,
        help="Logic level for the extracted domain artifact.",
    )
    parser.add_argument("--law-file", required=True, help="Path to the law text file.")
    parser.add_argument(
        "--system-prompt-file",
        help="Optional path to the system prompt template for domain extraction.",
    )
    parser.add_argument(
        "--user-prompt-file",
        help="Optional path to the user prompt template for domain extraction.",
    )
    parser.add_argument("--out", required=True, help="Where to write the checked domain JSON.")
    parser.add_argument("--model", help="Optional Gemini model override.")
    parser.add_argument("--api-key", help="Optional Gemini API key override.")
    return parser.parse_args()


def main() -> None:
    """Run the step-2 extraction and persist the JSON artifact."""
    args = parse_args()
    law_text = Path(args.law_file).read_text(encoding="utf-8")
    artifact = extract_domain_artifact(
        use_case_dir=args.use_case_dir,
        law_text=law_text,
        logic_level=LogicLevel(args.logic_level),
        system_prompt_path=args.system_prompt_file,
        user_prompt_path=args.user_prompt_file,
        source_path=args.law_file,
        model=args.model,
        api_key=args.api_key,
    )
    Path(args.out).write_text(artifact.model_dump_json(indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
