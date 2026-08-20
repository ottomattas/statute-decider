"""Step 1: extract request intent into a checked machine-readable artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from llm import extract_intent_artifact
from schemas import LogicLevel


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the intent extraction step."""
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
        help="Logic level for the extraction artifact.",
    )
    parser.add_argument("--text-file", help="Path to the request text file.")
    parser.add_argument("--text", help="Request text provided directly on the command line.")
    parser.add_argument(
        "--system-prompt-file",
        help="Optional path to the system prompt template for intent extraction.",
    )
    parser.add_argument(
        "--user-prompt-file",
        help="Optional path to the user prompt template for intent extraction.",
    )
    parser.add_argument("--out", required=True, help="Where to write the checked intent JSON.")
    parser.add_argument("--model", help="Optional Gemini model override.")
    parser.add_argument("--api-key", help="Optional Gemini API key override.")
    return parser.parse_args()


def _load_text(args: argparse.Namespace) -> str:
    """Load the request text from either `--text` or `--text-file`."""
    if bool(args.text) == bool(args.text_file):
        raise SystemExit("Provide exactly one of --text or --text-file.")
    if args.text:
        return args.text
    return Path(args.text_file).read_text(encoding="utf-8")


def main() -> None:
    """Run the step-1 extraction and persist the JSON artifact."""
    args = parse_args()
    request_text = _load_text(args)
    artifact = extract_intent_artifact(
        use_case_dir=args.use_case_dir,
        request_text=request_text,
        logic_level=LogicLevel(args.logic_level),
        system_prompt_path=args.system_prompt_file,
        user_prompt_path=args.user_prompt_file,
        source_path=args.text_file,
        model=args.model,
        api_key=args.api_key,
    )
    Path(args.out).write_text(artifact.model_dump_json(indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
