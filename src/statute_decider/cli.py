"""``sd`` — the statute-decider CLI.

Flags carry no silent defaults: ``sd run`` requires ``--execution`` and
``--models`` (one id, a list, or explicit ``all``).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def _find_root(start: Path | None = None) -> Path:
    """The repo root: the nearest ancestor containing ``configs/`` and ``data/``."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "configs").is_dir() and (candidate / "data").is_dir():
            return candidate
    return current


def _cmd_run(args: argparse.Namespace) -> int:
    from statute_decider.runner.experiment import run_experiment

    root = _find_root(Path(args.root) if args.root else None)
    results_dir = run_experiment(
        root,
        args.experiment,
        execution=args.execution,
        models=args.models,
        providers=args.providers,
        solver=args.solver,
        resume=args.resume,
        rerun_errors=args.rerun_errors,
        limit=args.limit,
    )
    print(f"Results: {results_dir}")
    print(f"Summary: {results_dir / 'summary.md'}")
    return 0


def _cmd_matrix(args: argparse.Namespace) -> int:
    from statute_decider.llm.registry import ModelRegistry
    from statute_decider.runner.matrix import export_matrix

    root = _find_root(Path(args.root) if args.root else None)
    registry = ModelRegistry(
        root / "configs" / "llm" / "models.yaml", root / "configs" / "llm" / "prices.yaml"
    )
    out = export_matrix(root, registry, Path(args.out) if args.out else None)
    print(f"Matrix exported: {out}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """Validate every data file against the core schemas."""
    from statute_decider.core import DataStore

    root = _find_root(Path(args.root) if args.root else None)
    store = DataStore(root / "data")
    problems: list[str] = []
    statutes = store.statute_ids()
    registers = store.register_ids()
    cases = store.case_ids()
    for statute_id in statutes:
        try:
            store.statute_text(statute_id)
            store.statute_sidecar(statute_id)
            store.oracle_text_term(statute_id)
            store.oracle_term_rule(statute_id)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"statute {statute_id}: {exc}")
    for register_id in registers:
        try:
            store.register_schema(register_id)
            store.oracle_record_term(register_id)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"register {register_id}: {exc}")
    scenario_count = 0
    for case_id in cases:
        try:
            case = store.case(case_id)
            for sid in case.statute_ids:
                assert sid in statutes, f"unknown statute {sid}"
            for rid in case.register_ids:
                assert rid in registers, f"unknown register {rid}"
            store.base_registry(case_id)
            for scenario_id in store.scenario_ids(case_id):
                scenario_count += 1
                scenario = store.scenario(case_id, scenario_id)
                store.utterance_text(case_id, scenario)
                store.scenario_registry(case_id, scenario)
                for node in ("utterance_term", "term_claim", "term_fact", "premise_outcome"):
                    store.oracle_value(case_id, node, scenario_id)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"case {case_id}: {exc}")
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    print(
        f"OK: {len(statutes)} statutes, {len(registers)} registers, "
        f"{len(cases)} cases, {scenario_count} scenarios validate."
    )
    return 0


def _corpus(args: argparse.Namespace):
    from statute_decider.legislation.corpus import CORPUS_RELATIVE, Corpus

    root = _find_root(Path(args.root) if args.root else None)
    return Corpus(root / CORPUS_RELATIVE)


def _cmd_corpus_ingest(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    entry = corpus.ingest(args.file, args.url, act_slug=args.slug, force=args.force)
    print(
        f"Ingested {entry.global_id} ({entry.language}) {entry.title!r} -> {entry.file} "
        f"as act {entry.act_slug}; sha256 {entry.sha256[:12]}…"
    )
    return 0


def _cmd_corpus_ingest_dir(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    entries = corpus.ingest_dir(args.dir, force=args.force)
    for entry in entries:
        print(f"Ingested {entry.global_id} ({entry.language}) {entry.title!r} -> {entry.file} as {entry.act_slug}")
    print(f"{len(entries)} files; catalogue: {corpus.catalogue_path}")
    return 0


def _cmd_corpus_check(args: argparse.Namespace) -> int:
    report = _corpus(args).check()
    print(report.render())
    return 0 if report.ok else 1


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(prog="sd", description=__doc__)
    parser.add_argument("--root", default=None, help="Repo root (default: auto-detect).")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run an experiment.")
    run_parser.add_argument("--experiment", required=True, help="experiment.yaml or its folder.")
    run_parser.add_argument(
        "--execution",
        required=True,
        choices=["parallel", "sequential"],
        help="Required; no default.",
    )
    run_parser.add_argument(
        "--models",
        required=True,
        nargs="+",
        help="Required: one id, a list, or explicit 'all'.",
    )
    run_parser.add_argument("--providers", nargs="+", default=None, help="Optional filter.")
    run_parser.add_argument("--solver", default=None, help="Override premise_outcome.solver.")
    run_parser.add_argument(
        "--resume",
        action="store_true",
        help="Keep cells already in results/rows.jsonl; run only the missing ones.",
    )
    run_parser.add_argument(
        "--rerun-errors",
        action="store_true",
        help="With --resume: also re-run cells whose row has an error.",
    )
    run_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run at most N new cells this invocation (batching; combine with --resume).",
    )
    run_parser.set_defaults(func=_cmd_run)

    matrix_parser = sub.add_parser("matrix", help="Matrix operations.")
    matrix_sub = matrix_parser.add_subparsers(dest="matrix_command", required=True)
    export_parser = matrix_sub.add_parser("export", help="Export docs/matrix.csv.")
    export_parser.add_argument("--out", default=None)
    export_parser.set_defaults(func=_cmd_matrix)

    validate_parser = sub.add_parser("validate", help="Validate all data files.")
    validate_parser.set_defaults(func=_cmd_validate)

    corpus_parser = sub.add_parser("corpus", help="Legislation corpus (data/sources/legislation).")
    corpus_sub = corpus_parser.add_subparsers(dest="corpus_command", required=True)
    ingest_parser = corpus_sub.add_parser("ingest", help="Copy one Riigi Teataja XML in and catalogue it.")
    ingest_parser.add_argument("file", help="Downloaded .akt (XML) file.")
    ingest_parser.add_argument("--url", required=True, help="Official Riigi Teataja URL it was fetched from.")
    ingest_parser.add_argument("--slug", default=None, help="Override the act slug (default: from the English title).")
    ingest_parser.add_argument("--force", action="store_true", help="Replace a differing file of the same global id.")
    ingest_parser.set_defaults(func=_cmd_corpus_ingest)
    ingest_dir_parser = corpus_sub.add_parser(
        "ingest-dir", help="Ingest every <jur>-<lang>-<act>.txt (URL + file name) in a directory."
    )
    ingest_dir_parser.add_argument("dir")
    ingest_dir_parser.add_argument("--force", action="store_true")
    ingest_dir_parser.set_defaults(func=_cmd_corpus_ingest_dir)
    check_parser = corpus_sub.add_parser("check", help="Re-hash every file; report drift and validity windows.")
    check_parser.set_defaults(func=_cmd_corpus_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
