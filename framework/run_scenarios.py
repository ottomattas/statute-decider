"""Regenerate named `framework` scenarios and their review transcripts.

Pass ``--scenarios`` to run the expected-vs-actual scenario-suite harness
instead of the legacy review-run regeneration flow.  The two modes are fully
independent and share no mutable state.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from logic_levels import build_domain_artifact, build_intent_artifact
from metadata import normalized_path, sha256_text, utc_timestamp
from scenario_suite import print_suite_summary, run_full_suite
from schemas import ExtractionRunMetadata, PromptMetadata
from truth_table import DEFAULT_MAX_VARS, enumerate_truth_table, write_markdown
from use_case_files import (
    FRAMEWORK_ROOT,
    example_dir_for_scenario,
    law_supports_use_case,
    load_scenario,
    load_use_case_from_dir,
    request_mentions_claim,
    resolve_example_path,
    scenario_file_by_name,
    scenario_names,
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for scenario regeneration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenarios",
        action="store_true",
        help=(
            "Run the expected-vs-actual scenario-suite harness across all five "
            "target domains and write per-case Markdown tables."
        ),
    )
    parser.add_argument(
        "--truth-table",
        action="store_true",
        help=(
            "Enumerate the boolean truth table for each target domain (up to "
            "max_vars claims) and write per-case Markdown reports."
        ),
    )
    parser.add_argument(
        "--max-vars",
        type=int,
        default=DEFAULT_MAX_VARS,
        help=(
            "Maximum number of claims for --truth-table enumeration. Cases "
            "with more claims are skipped and annotated in the report."
        ),
    )
    parser.add_argument(
        "--scenario-id",
        metavar="ID",
        help=(
            "When used with --scenarios, run only the scenario whose name matches ID. "
            "Useful for debugging a single case."
        ),
    )
    parser.add_argument(
        "--scenario",
        action="append",
        choices=scenario_names(),
        help="(Legacy) scenario name to regenerate. Repeat to run a subset.",
    )
    parser.add_argument(
        "--mode",
        choices=("deterministic", "live"),
        default="deterministic",
        help="Use deterministic local fixtures or call the live extraction CLIs.",
    )
    parser.add_argument(
        "--out-dir",
        default="examples/review_runs/scenario_suite",
        help="Directory where scenario artifacts should be written.",
    )
    parser.add_argument(
        "--transcript-file",
        default="examples/review_runs/scenario_suite.txt",
        help="Plain-text transcript file to regenerate.",
    )
    parser.add_argument("--model", help="Optional model override for live extraction mode.")
    parser.add_argument("--api-key", help="Optional API key override for live extraction mode.")
    return parser.parse_args()


def _relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(FRAMEWORK_ROOT))
    except ValueError:
        return str(resolved)


def _write_artifact(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def _render_command(args: list[str]) -> str:
    rendered: list[str] = []
    for index, argument in enumerate(args):
        if index == 0 and Path(argument).name.startswith("python"):
            rendered.append("python")
        elif argument.startswith(str(FRAMEWORK_ROOT.resolve())):
            rendered.append(_relative(Path(argument)))
        else:
            rendered.append(argument)
    return " ".join(rendered)


def _run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=FRAMEWORK_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {_render_command(command)}\n{output}"
        )
    return output.strip()


def _live_extraction_commands(
    scenario_file: Path,
    scenario_dir: Path,
    *,
    model: str | None,
    api_key: str | None,
) -> list[list[str]]:
    scenario = load_scenario(scenario_file)
    example_dir = example_dir_for_scenario(scenario_file)
    commands: list[list[str]] = [
        [
            sys.executable,
            str((FRAMEWORK_ROOT / "01_extract_intent.py").resolve()),
            "--use-case-dir",
            str(example_dir),
            "--text-file",
            str(resolve_example_path(example_dir, scenario.request_file)),
            "--out",
            str((scenario_dir / "intent.json").resolve()),
        ],
        [
            sys.executable,
            str((FRAMEWORK_ROOT / "02_extract_domain.py").resolve()),
            "--use-case-dir",
            str(example_dir),
            "--law-file",
            str(resolve_example_path(example_dir, scenario.law_file)),
            "--out",
            str((scenario_dir / "domain.json").resolve()),
        ],
    ]
    if scenario.intent_user_prompt_file:
        commands[0].extend(
            [
                "--user-prompt-file",
                str(resolve_example_path(example_dir, scenario.intent_user_prompt_file)),
            ]
        )
    if scenario.domain_user_prompt_file:
        commands[1].extend(
            [
                "--user-prompt-file",
                str(resolve_example_path(example_dir, scenario.domain_user_prompt_file)),
            ]
        )
    for command in commands:
        if model:
            command.extend(["--model", model])
        if api_key:
            command.extend(["--api-key", api_key])
    return commands


def _solve_and_trace_commands(scenario_name: str, scenario_dir: Path) -> list[list[str]]:
    scenario_file = scenario_file_by_name(scenario_name)
    scenario = load_scenario(scenario_file)
    example_dir = example_dir_for_scenario(scenario_file)
    return [
        [
            sys.executable,
            str((FRAMEWORK_ROOT / "03_solve_case.py").resolve()),
            "--domain",
            str((scenario_dir / "domain.json").resolve()),
            "--intent",
            str((scenario_dir / "intent.json").resolve()),
            "--db",
            str(resolve_example_path(example_dir, scenario.mock_db_file)),
            "--out",
            str((scenario_dir / "solution.json").resolve()),
        ],
        [
            sys.executable,
            str((FRAMEWORK_ROOT / "04_print_trace.py").resolve()),
            "--solution",
            str((scenario_dir / "solution.json").resolve()),
            "--out",
            str((scenario_dir / "trace.txt").resolve()),
        ],
    ]


def _prepare_deterministic_artifacts(scenario_name: str, scenario_dir: Path) -> list[str]:
    scenario_file = scenario_file_by_name(scenario_name)
    scenario = load_scenario(scenario_file)
    example_dir = example_dir_for_scenario(scenario_file)
    use_case = load_use_case_from_dir(example_dir)
    request_path = resolve_example_path(example_dir, scenario.request_file)
    law_path = resolve_example_path(example_dir, scenario.law_file)
    intent_system_prompt_path = example_dir / "prompts" / "intent" / "system.propositional.txt"
    intent_user_prompt_path = (
        resolve_example_path(example_dir, scenario.intent_user_prompt_file)
        if scenario.intent_user_prompt_file
        else example_dir / "prompts" / "intent" / "user.txt"
    )
    domain_system_prompt_path = example_dir / "prompts" / "domain" / "system.propositional.txt"
    domain_user_prompt_path = (
        resolve_example_path(example_dir, scenario.domain_user_prompt_file)
        if scenario.domain_user_prompt_file
        else example_dir / "prompts" / "domain" / "user.txt"
    )
    request_text = request_path.read_text(encoding="utf-8")
    law_text = law_path.read_text(encoding="utf-8")
    snippets = {
        claim.claim_id: [
            line.strip()
            for line in request_text.splitlines()
            if request_mentions_claim(use_case, claim.claim_id, line)
        ]
        for claim in use_case.claims
    }
    reasons = {
        claim.claim_id: _reason_text(scenario.intent_assignments.get(claim.claim_id))
        for claim in use_case.claims
    }
    intent = build_intent_artifact(
        use_case=use_case,
        request_text=request_text,
        logic_level=use_case.default_logic_level,
        assignments=scenario.intent_assignments,
        reasons=reasons,
        snippets=snippets,
        run_metadata=ExtractionRunMetadata(
            generated_at_utc=utc_timestamp(),
            model_name="deterministic-fixture",
            source_path=normalized_path(request_path),
            prompt=_prompt_metadata(intent_system_prompt_path, intent_user_prompt_path),
        ),
    )
    full_domain = build_domain_artifact(
        use_case=use_case,
        logic_level=use_case.default_logic_level,
        law_text=law_text,
        title=use_case.title,
        run_metadata=ExtractionRunMetadata(
            generated_at_utc=utc_timestamp(),
            model_name="deterministic-fixture",
            source_path=normalized_path(law_path),
            prompt=_prompt_metadata(domain_system_prompt_path, domain_user_prompt_path),
        ),
    )
    if law_supports_use_case(use_case, law_text):
        domain = full_domain
    else:
        domain = full_domain.model_copy(update={"claims": [], "rules": []})
    _write_artifact(scenario_dir / "intent.json", intent.model_dump_json(indent=2))
    _write_artifact(scenario_dir / "domain.json", domain.model_dump_json(indent=2))
    return [
        f"# deterministic intent artifact -> {_relative(scenario_dir / 'intent.json')}",
        f"# deterministic domain artifact -> {_relative(scenario_dir / 'domain.json')}",
        f"# use case dir: {_relative(example_dir)}",
        f"# request file: {_relative(request_path)}",
        f"# law file: {_relative(law_path)}",
    ]


def _prompt_metadata(system_prompt_path: Path, user_prompt_path: Path) -> PromptMetadata:
    """Build prompt metadata for deterministic fixtures."""
    return PromptMetadata(
        system_prompt_path=str(system_prompt_path),
        user_prompt_path=str(user_prompt_path),
        system_prompt_sha256=sha256_text(system_prompt_path.read_text(encoding="utf-8")),
        user_prompt_sha256=sha256_text(user_prompt_path.read_text(encoding="utf-8")),
    )


def _reason_text(value: bool | None) -> str:
    """Render the fixed explanation text for deterministic assignments."""
    if value is True:
        return "Deterministic scenario fixture sets this claim to true."
    if value is False:
        return "Deterministic scenario fixture sets this claim to false."
    return "Deterministic scenario fixture leaves this claim unresolved."


def regenerate_scenario(
    scenario_name: str,
    *,
    mode: str,
    out_dir: Path,
    model: str | None,
    api_key: str | None,
) -> str:
    """Regenerate one named scenario and return its transcript block."""
    scenario = load_scenario(scenario_file_by_name(scenario_name))
    scenario_dir = (out_dir / scenario_name).resolve()
    scenario_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"SCENARIO: {scenario.name}",
        f"DESCRIPTION: {scenario.description}",
    ]
    if mode == "deterministic":
        lines.extend(_prepare_deterministic_artifacts(scenario_name, scenario_dir))
    else:
        for command in _live_extraction_commands(
            scenario_file_by_name(scenario_name),
            scenario_dir,
            model=model,
            api_key=api_key,
        ):
            lines.append(f"$ {_render_command(command)}")
            output = _run_command(command)
            lines.append(output or "(no output)")
    for command in _solve_and_trace_commands(scenario_name, scenario_dir):
        lines.append(f"$ {_render_command(command)}")
        output = _run_command(command)
        lines.append(output or "(no output)")
    lines.append("")
    transcript = "\n".join(lines).rstrip() + "\n"
    _write_artifact(scenario_dir / "session.txt", transcript)
    return transcript


def _run_scenario_suite(args: argparse.Namespace) -> None:
    """Entry point for the --scenarios harness."""
    print("Running expected-vs-actual scenario suite...")
    reports = run_full_suite(scenario_filter=args.scenario_id)
    mismatches = print_suite_summary(reports)
    if mismatches:
        sys.exit(1)


TRUTH_TABLE_CASES: tuple[str, ...] = (
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
)


def _run_truth_tables(args: argparse.Namespace) -> None:
    """Entry point for the --truth-table enumeration."""
    print(f"Running truth-table enumeration (max_vars={args.max_vars})...")
    enumerated = 0
    skipped = 0
    for case_name in TRUTH_TABLE_CASES:
        report = enumerate_truth_table(case_name, max_vars=args.max_vars)
        out_path = write_markdown(report)
        if report.skipped:
            skipped += 1
            print(f"  [SKIP] {case_name}: {report.skip_reason} -> {out_path}")
            continue
        enumerated += 1
        print(
            f"  [OK] {case_name}: {report.n_vars} claims, {report.n_rows} rows -> {out_path}"
        )
    print(f"\nTOTAL: {enumerated} enumerated, {skipped} skipped")


def main() -> None:
    """Regenerate the requested scenarios and the aggregate transcript."""
    args = parse_args()

    if args.scenarios:
        _run_scenario_suite(args)
        return

    if args.truth_table:
        _run_truth_tables(args)
        return

    selected = args.scenario or scenario_names()
    out_dir = (FRAMEWORK_ROOT / args.out_dir).resolve()
    transcript_path = (FRAMEWORK_ROOT / args.transcript_file).resolve()
    blocks = [
        regenerate_scenario(
            scenario_name,
            mode=args.mode,
            out_dir=out_dir,
            model=args.model,
            api_key=args.api_key,
        ).rstrip()
        for scenario_name in selected
    ]
    transcript = "\n\n".join(blocks) + "\n"
    _write_artifact(transcript_path, transcript)
    print(f"Wrote transcript to {_relative(transcript_path)}")


if __name__ == "__main__":
    main()
