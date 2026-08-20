"""Step 00: collect structured user input from free-form utterances.

Runs before step 01 in the `framework` pipeline. The deterministic path is
authoritative and never imports `google.genai`; `--llm` is opt-in. Step 00
produces a `UserInputSession` JSON and, when `--request-text-out` is given,
a concatenated natural-language request file that step 01 can consume:

    python framework/00_collect_intent.py \\
        --use-case-dir framework/examples/<case> \\
        --utterances-file framework/examples/<case>/user_input/utterances_allow.json \\
        --out session.json \\
        --request-text-out request.txt

    python framework/01_extract_intent.py \\
        --use-case-dir framework/examples/<case> \\
        --text-file request.txt \\
        --out intent.json

See ``docs/reference/nl-extraction.md`` for the full semantics, including
U5 (NEED_DB_INFO-style unresolved claims) and U8
(NEED_USER_INFO-style needs-confirmation claims).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from schemas import LogicLevel
from use_case_files import load_use_case_from_dir
from user_input import (
    UserInputSession,
    UserUtterance,
    extract_user_input_deterministic,
    extract_user_input_llm,
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for step 00."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--use-case-dir",
        required=True,
        help="Directory under examples/ that contains use_case.json and prompts.",
    )
    parser.add_argument(
        "--utterances-file",
        required=True,
        help="Path to a JSON file with a list of UserUtterance entries.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Where to write the checked user-input session JSON.",
    )
    parser.add_argument(
        "--logic-level",
        choices=[level.value for level in LogicLevel],
        default=LogicLevel.PROPOSITIONAL.value,
        help="Logic level used to select the per-case system prompt (LLM path only).",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Opt in to the LLM extractor. Lazy-imports google.genai.",
    )
    parser.add_argument("--model", help="Optional Gemini model override (LLM path only).")
    parser.add_argument("--api-key", help="Optional Gemini API key override (LLM path only).")
    parser.add_argument(
        "--request-text-out",
        help=(
            "Optional path for a concatenated NL request text that "
            "01_extract_intent.py can consume via --text-file."
        ),
    )
    return parser.parse_args()


def load_utterances(path: str | Path) -> list[UserUtterance]:
    """Load a list of `UserUtterance` entries from a JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise SystemExit("Utterances file must hold a JSON array of entries.")
    return [UserUtterance.model_validate(item) for item in raw]


def run(args: argparse.Namespace) -> UserInputSession:
    """Run step 00 and return the structured session."""
    use_case = load_use_case_from_dir(args.use_case_dir)
    utterances = load_utterances(args.utterances_file)

    if args.llm:
        session = extract_user_input_llm(
            use_case,
            utterances,
            use_case_dir=args.use_case_dir,
            logic_level=LogicLevel(args.logic_level),
            model=args.model,
            api_key=args.api_key,
        )
    else:
        session = extract_user_input_deterministic(use_case, utterances)
    return session


def write_request_text(utterances: list[UserUtterance], path: str | Path) -> None:
    """Concatenate the utterance texts into a single request file for step 01."""
    Path(path).write_text(
        "\n\n".join(utterance.text.strip() for utterance in utterances if utterance.text.strip()) + "\n",
        encoding="utf-8",
    )


def summarise(session: UserInputSession) -> str:
    """Return a compact human-readable summary for stdout."""
    resolved_true = sum(1 for r in session.responses if r.value is True)
    resolved_false = sum(1 for r in session.responses if r.value is False)
    needs_confirm = sum(1 for r in session.responses if r.needs_user_confirmation)
    unresolved_mentioned = sum(
        1
        for r in session.responses
        if r.value is None and not r.needs_user_confirmation
    )
    not_mentioned = len(session.unresolved_claim_ids)
    lines = [
        f"use_case_id: {session.use_case_id}",
        f"utterances: {len(session.utterances)}",
        f"resolved_true: {resolved_true}",
        f"resolved_false: {resolved_false}",
        f"unresolved_mentioned: {unresolved_mentioned}",
        f"needs_confirmation: {needs_confirm}",
        f"not_mentioned (U5 candidates): {not_mentioned}",
    ]
    if session.unresolved_claim_ids:
        lines.append("unresolved_claim_ids: " + ", ".join(session.unresolved_claim_ids))
    return "\n".join(lines)


def main() -> None:
    """CLI entry point for step 00."""
    args = parse_args()
    session = run(args)
    Path(args.out).write_text(session.model_dump_json(indent=2), encoding="utf-8")
    if args.request_text_out:
        write_request_text(session.utterances, args.request_text_out)
    print(summarise(session))


if __name__ == "__main__":
    main()
