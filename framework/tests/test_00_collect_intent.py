"""CLI tests for step 00 (Wave 3 Track C, ART-66)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from user_input import UserInputSession  # noqa: E402


CLI_PATH = FRAMEWORK_ROOT / "00_collect_intent.py"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Invoke the step-00 CLI with the current Python interpreter."""
    cmd = [sys.executable, str(CLI_PATH), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        cwd=str(FRAMEWORK_ROOT),
    )


class TestCollectIntentCli(unittest.TestCase):
    def test_cli_emits_session_json_and_optional_request_text(self) -> None:
        case_dir = FRAMEWORK_ROOT / "examples" / "land_tax_exemption"
        utterances_file = case_dir / "user_input" / "utterances_allow.json"
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "session.json"
            req_path = Path(tmp) / "request.txt"
            result = _run_cli(
                "--use-case-dir",
                str(case_dir),
                "--utterances-file",
                str(utterances_file),
                "--out",
                str(out_path),
                "--request-text-out",
                str(req_path),
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=f"CLI failed: stderr={result.stderr}",
            )
            # Session file exists and validates.
            raw = json.loads(out_path.read_text(encoding="utf-8"))
            session = UserInputSession.model_validate(raw)
            self.assertEqual(len(session.utterances), 4)
            self.assertTrue(session.responses)
            # Concatenated request text is non-empty.
            request_text = req_path.read_text(encoding="utf-8")
            self.assertTrue(request_text.strip())
            # Each utterance text appears in the concatenated request.
            for utterance in session.utterances:
                self.assertIn(utterance.text.strip(), request_text)
            # Stdout summary includes the per-category counts.
            self.assertIn("resolved_true", result.stdout)
            self.assertIn("needs_confirmation", result.stdout)

    def test_cli_help_runs_without_gemini_dependency(self) -> None:
        """`--help` must work without importing google.genai."""
        result = _run_cli("--help")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("--use-case-dir", result.stdout)
        self.assertIn("--utterances-file", result.stdout)
        self.assertIn("--llm", result.stdout)
        self.assertIn("--request-text-out", result.stdout)

    def test_cli_needs_user_fixture_flags_hedged_responses(self) -> None:
        case_dir = FRAMEWORK_ROOT / "examples" / "consumer_withdrawal"
        utterances_file = case_dir / "user_input" / "utterances_needs_user.json"
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "session.json"
            result = _run_cli(
                "--use-case-dir",
                str(case_dir),
                "--utterances-file",
                str(utterances_file),
                "--out",
                str(out_path),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            session = UserInputSession.model_validate_json(
                out_path.read_text(encoding="utf-8")
            )
            self.assertTrue(
                any(r.needs_user_confirmation for r in session.responses),
                "needs_user fixture produced no hedged response",
            )
            self.assertTrue(session.unresolved_claim_ids)


if __name__ == "__main__":
    unittest.main()
