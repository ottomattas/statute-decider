"""Join experiment (i) and (ii) over ``experiments/matrix.yaml``.

Runtime rows are free (no API). LLM rows halt at ``FRAMEWORK_BUDGET_EUR``
(default 10). Missing keys skip that provider with a log line; they do not
block the run.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

FRAMEWORK_ROOT = Path(__file__).resolve().parent
REPO_ROOT = FRAMEWORK_ROOT.parent
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from experiment_i import render_markdown as render_experiment_i  # noqa: E402
from experiment_i import run_selection_condition, run_synthesis_condition  # noqa: E402
from experiment_ii import (  # noqa: E402
    aggregate,
    pair_rows,
    render_markdown_table,
    render_paired_markdown,
    run_llm_row,
    run_runtime_row,
)
from experiments.budget import BudgetExceeded, BudgetGuard, usd_to_eur  # noqa: E402
from experiments.ledger import (  # noqa: E402
    append_ledger,
    estimate_usd,
    estimate_worst_case_usd,
    ledger_path,
)
from providers import get_provider, list_available_providers  # noqa: E402
from scenario_suite import discover_suite_scenario_files_for_case  # noqa: E402
from use_case_files import EXAMPLES_ROOT  # noqa: E402

log = logging.getLogger("run_experiments")

SMOKE_BANNER = "SMOKE — UNVALIDATED"
GOLD_CASES = [
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
    "section_120_demo",
]

_KEY_NAMES = (
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY",
    "FRAMEWORK_BUDGET_EUR",
    "FRAMEWORK_GEMINI_MODEL",
    "FRAMEWORK_OPENAI_MODEL",
    "FRAMEWORK_ANTHROPIC_MODEL",
    "FRAMEWORK_DEEPSEEK_MODEL",
)


def default_matrix_path() -> Path:
    return REPO_ROOT / "experiments" / "matrix.yaml"


def default_results_dir() -> Path:
    return REPO_ROOT / "experiments" / "results"


def load_matrix(path: str | Path) -> dict[str, Any]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"matrix file {path} must be a mapping")
    return raw


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].strip()
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    if not key:
        return None
    return key, value


def load_env_file(path: Path) -> int:
    """Load KEY=value lines into os.environ without overwriting existing keys.

    Returns the number of keys newly set. Never logs values.
    """
    if not path.is_file():
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        log.warning("Could not read env file %s: %s", path.name, exc)
        return 0
    added = 0
    for line in text.splitlines():
        parsed = _parse_env_line(line)
        if parsed is None:
            continue
        key, value = parsed
        if key in os.environ and os.environ[key].strip():
            continue
        os.environ[key] = value
        added += 1
    return added


def load_runtime_env() -> list[str]:
    """Load repo ``.env`` into os.environ. Existing keys win; values are never logged."""
    loaded: list[str] = []
    path = REPO_ROOT / ".env"
    n = load_env_file(path)
    if n:
        loaded.append(path.name)
    return loaded


def gold_scenario_files(config: dict[str, Any] | None = None) -> list[Path]:
    """Suite gold files (five domains + §120), optionally filtered by matrix."""
    exp = (config or {}).get("experiment_ii") or {}
    names = exp.get("scenarios")
    if names:
        wanted = {str(name) for name in names}
        files: list[Path] = []
        for case in GOLD_CASES:
            for path in discover_suite_scenario_files_for_case(case):
                if path.stem in wanted:
                    files.append(path)
        return files
    files = []
    for case in GOLD_CASES:
        files.extend(discover_suite_scenario_files_for_case(case))
    return files


@dataclass
class Label:
    value: str = "unknown"


@dataclass
class HaltState:
    error: BudgetExceeded | None = None


# Transport-level flakes (capacity, rate limits, gateway errors) are retried;
# model-produced garbage (invalid JSON, schema misses) is NOT — that is a
# finding, not an infrastructure problem.
_TRANSIENT_MARKERS = (
    "503",
    "unavailable",
    "429",
    "rate limit",
    "rate_limit",
    "overloaded",
    "high demand",
    "500",
    "502",
    "504",
    "timeout",
    "timed out",
    "connection error",
)
_MAX_TRANSIENT_RETRIES = 5


def _is_transient(exc: Exception) -> bool:
    # Timeout exception classes (httpx.ReadTimeout, openai.APITimeoutError, …)
    # can carry an empty message, so check the type as well as the text.
    if isinstance(exc, TimeoutError):
        return True
    if "timeout" in type(exc).__name__.lower():
        return True
    text = str(exc).lower()
    return any(marker in text for marker in _TRANSIENT_MARKERS)


def make_tracked_complete(
    provider: Any,
    *,
    experiment: str,
    label: Label,
    guard: BudgetGuard,
    halt: HaltState,
) -> Callable[..., Any]:
    """Wrap ``provider.complete`` with worst-case pre-check and ledger write."""

    def complete(
        *,
        system: str | None = None,
        user: str | None = None,
        system_instruction: str | None = None,
        user_content: str | None = None,
        response_model: type,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> Any:
        del kwargs
        if halt.error is not None:
            raise halt.error
        sys_txt = system if system is not None else (system_instruction or "")
        user_txt = user if user is not None else (user_content or "")
        worst = estimate_worst_case_usd(provider.model)
        guard.check_or_raise(usd_to_eur(worst))
        for attempt in range(_MAX_TRANSIENT_RETRIES + 1):
            try:
                result = provider.complete(
                    system=sys_txt,
                    user=user_txt,
                    response_model=response_model,
                    temperature=temperature,
                )
                break
            except Exception as exc:  # noqa: BLE001 — retry transport flakes only
                if attempt >= _MAX_TRANSIENT_RETRIES or not _is_transient(exc):
                    raise
                delay = min(60.0, (2.0**attempt) * 2.0) + random.uniform(0.0, 1.0)
                log.warning(
                    "Transient %s error (attempt %d/%d), retrying in %.1fs: %s",
                    provider.name,
                    attempt + 1,
                    _MAX_TRANSIENT_RETRIES,
                    delay,
                    exc,
                )
                time.sleep(delay)
        if getattr(result, "skipped", False):
            raise RuntimeError(getattr(result, "skip_reason", "") or f"{provider.name} skipped")
        usage = result.usage
        usd = estimate_usd(result.model, usage)
        append_ledger(
            provider=result.provider,
            model=result.model,
            experiment=experiment,
            scenario=label.value,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            usd=usd,
        )
        try:
            guard.record_usd(usd)
        except BudgetExceeded as exc:
            halt.error = exc
        return result

    return complete


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, default=str) + "\n")


def _append_jsonl_row(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True, default=str) + "\n")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            rows.append(json.loads(stripped))
    return rows


# --- Resume-from-state (operator policy 2026-08-25) -------------------------
# Experiment records are append-only. A row identified by
# (experiment, scenario label incl. repeat tag, provider, model) that already
# has a successful record is SKIPPED on relaunch — no re-spend, no overwrite.
# Error rows are re-attempted. Two sources of truth:
#   1. the leg's append-only results JSONL (rows written as they complete);
#   2. the cost ledger at/after --resume-since (covers rows whose process
#      died between the ledger append and any results write).

RowKey = tuple[str, str, str, str]


def _result_row_key(experiment: str, row: dict[str, Any]) -> RowKey | None:
    label = row.get("scenario_label")
    provider = row.get("provider")
    model = row.get("model")
    if not (label and provider and model):
        return None
    return (experiment, str(label), str(provider), str(model))


def load_completed_keys(
    *,
    experiment: str,
    results_path: Path,
    resume_since: str | None,
) -> set[RowKey]:
    done: set[RowKey] = set()
    for row in _load_jsonl(results_path):
        if row.get("error"):
            continue
        key = _result_row_key(experiment, row)
        if key is not None:
            done.add(key)
    if resume_since:
        from experiments.ledger import iter_ledger

        for row in iter_ledger():
            if str(row.get("experiment")) != experiment:
                continue
            if str(row.get("ts") or "") < resume_since:
                continue
            done.add(
                (
                    experiment,
                    str(row.get("scenario")),
                    str(row.get("provider")),
                    str(row.get("model")),
                )
            )
    return done


def _dedupe_result_rows(
    experiment: str, rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Collapse retried keys: a success supersedes errors; later wins otherwise."""
    by_key: dict[RowKey | int, dict[str, Any]] = {}
    order: list[RowKey | int] = []
    for index, row in enumerate(rows):
        key: RowKey | int = _result_row_key(experiment, row) or index
        if key not in by_key:
            by_key[key] = row
            order.append(key)
        elif by_key[key].get("error") or not row.get("error"):
            by_key[key] = row
    return [by_key[key] for key in order]


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.3f}"


def _summary_block(title: str, stats: dict[str, Any]) -> list[str]:
    per_class = stats.get("per_class_accuracy") or {}
    lines = [
        f"### {title}",
        "",
        f"- n scored: {stats.get('n_scored', 0)} / {stats.get('n', 0)}",
        f"- outcome accuracy: {_fmt_pct(stats.get('outcome_accuracy'))}",
        f"- ALLOW accuracy: {_fmt_pct(per_class.get('ALLOW'))}",
        f"- DENY accuracy: {_fmt_pct(per_class.get('DENY'))}",
        f"- NEED_MORE_INFO accuracy: {_fmt_pct(per_class.get('NEED_MORE_INFO'))}",
        f"- mean missing-fact P/R: {_fmt_pct(stats.get('mean_precision'))} / {_fmt_pct(stats.get('mean_recall'))}",
        f"- macro missing-fact P/R: {_fmt_pct(stats.get('macro_precision'))} / {_fmt_pct(stats.get('macro_recall'))}",
        "",
    ]
    return lines


def requested_providers(config: dict[str, Any]) -> list[str]:
    names = [str(item).strip().lower() for item in (config.get("providers") or [])]
    return [name for name in names if name and name != "ollama"]


def available_requested_providers(config: dict[str, Any]) -> tuple[list[str], list[str]]:
    requested = requested_providers(config)
    live = set(list_available_providers())
    present = [name for name in requested if name in live]
    missing = [name for name in requested if name not in live]
    return present, missing


def run_runtime_phase(scenario_files: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in scenario_files:
        log.info("runtime %s", path.stem)
        rows.append(run_runtime_row(path))
    return rows


def run_llm_phase(
    *,
    scenario_files: list[Path],
    providers: list[str],
    repeats: int,
    guard: BudgetGuard,
    halt: HaltState,
    complete_factory: Callable[..., Any] | None = None,
    completed: set[RowKey] | None = None,
    results_path: Path | None = None,
) -> list[dict[str, Any]]:
    completed = completed or set()
    rows: list[dict[str, Any]] = []

    def emit(row: dict[str, Any]) -> None:
        rows.append(row)
        if results_path is not None:
            _append_jsonl_row(results_path, row)

    for provider_name in providers:
        if halt.error is not None:
            break
        try:
            provider = get_provider(provider_name)
        except ValueError:
            log.warning("Skipping unknown provider %s", provider_name)
            continue
        if not provider.available():
            log.warning("Skipping provider %s: not available", provider_name)
            continue
        label = Label(value="experiment_ii")
        complete = (
            complete_factory(provider, "ii", label, guard, halt)
            if complete_factory is not None
            else make_tracked_complete(
                provider, experiment="ii", label=label, guard=guard, halt=halt
            )
        )
        model = getattr(provider, "model", provider_name)
        for repeat in range(repeats):
            if halt.error is not None:
                break
            for path in scenario_files:
                if halt.error is not None:
                    log.warning("Budget halt before %s / %s", provider_name, path.stem)
                    break
                label.value = f"{path.stem}#r{repeat}"
                if ("ii", label.value, provider_name, model) in completed:
                    log.info(
                        "resume-skip %s/%s %s (already recorded)",
                        provider_name,
                        model,
                        label.value,
                    )
                    continue
                try:
                    row = run_llm_row(path, provider_name, complete)
                except BudgetExceeded as exc:
                    halt.error = exc
                    log.warning("Budget halt: %s", exc)
                    break
                except Exception as exc:  # noqa: BLE001 — keep the matrix moving
                    log.warning("LLM row failed %s / %s: %s", provider_name, path.stem, exc)
                    emit(
                        {
                            "scenario": path.stem,
                            "scenario_path": str(path),
                            "scenario_label": label.value,
                            "condition": "llm",
                            "provider": provider_name,
                            "model": model,
                            "repeat": repeat,
                            "error": str(exc),
                            "outcome_match": None,
                            "precision": None,
                            "recall": None,
                        }
                    )
                    continue
                row["repeat"] = repeat
                row["scenario_label"] = label.value
                row["model"] = model
                emit(row)
    return rows


def run_extraction_phase(
    *,
    cases: list[str],
    condition: str,
    providers: list[str],
    repeats: int,
    guard: BudgetGuard,
    halt: HaltState,
    complete_factory: Callable[..., Any] | None = None,
    completed: set[RowKey] | None = None,
    results_path: Path | None = None,
) -> list[dict[str, Any]]:
    runner = run_synthesis_condition if condition == "synthesis" else run_selection_condition
    completed = completed or set()
    rows: list[dict[str, Any]] = []

    def emit(row: dict[str, Any]) -> None:
        rows.append(row)
        if results_path is not None:
            _append_jsonl_row(results_path, row)

    for provider_name in providers:
        if halt.error is not None:
            break
        try:
            provider = get_provider(provider_name)
        except ValueError:
            log.warning("Skipping unknown provider %s", provider_name)
            continue
        if not provider.available():
            log.warning("Skipping provider %s: not available", provider_name)
            continue
        label = Label(value="experiment_i")
        complete = (
            complete_factory(provider, "i", label, guard, halt)
            if complete_factory is not None
            else make_tracked_complete(
                provider, experiment="i", label=label, guard=guard, halt=halt
            )
        )
        model = getattr(provider, "model", provider_name)
        for repeat in range(repeats):
            if halt.error is not None:
                break
            for case_name in cases:
                if halt.error is not None:
                    break
                case_dir = EXAMPLES_ROOT / case_name
                if not case_dir.is_dir():
                    log.warning("Missing case dir %s", case_dir)
                    continue
                label.value = f"{case_name}#{condition}#r{repeat}"
                if ("i", label.value, provider_name, model) in completed:
                    log.info(
                        "resume-skip %s/%s %s (already recorded)",
                        provider_name,
                        model,
                        label.value,
                    )
                    continue
                log.info("experiment (i) %s %s %s", condition, provider_name, case_name)
                try:
                    row = runner(case_dir, complete)
                except BudgetExceeded as exc:
                    halt.error = exc
                    log.warning("Budget halt: %s", exc)
                    break
                except Exception as exc:  # noqa: BLE001
                    log.warning("Extraction row failed %s / %s: %s", provider_name, case_name, exc)
                    emit(
                        {
                            "condition": condition,
                            "case_dir": str(case_dir),
                            "scenario_label": label.value,
                            "provider": provider_name,
                            "model": model,
                            "repeat": repeat,
                            "error": str(exc),
                            "skipped": True,
                        }
                    )
                    continue
                row["provider"] = provider_name
                row["repeat"] = repeat
                row["scenario_label"] = label.value
                row["model"] = model
                emit(row)
    return rows


def render_smoke_summary(
    *,
    config: dict[str, Any],
    runtime_rows: list[dict[str, Any]],
    llm_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    present: list[str],
    missing: list[str],
    guard: BudgetGuard,
    halt: HaltState,
) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# {SMOKE_BANNER}",
        "",
        f"Generated {generated}. Overnight cap EUR {guard.cap_eur:.2f}; "
        f"spent EUR {guard.spent_eur:.4f}; remaining EUR {guard.remaining():.4f}.",
        "Do not quote these numbers as results. Gold `low` rows and claim "
        "alignments still need operator audit.",
        "",
        f"Matrix label: `{config.get('label', 'unlabeled')}`.",
        f"Providers requested: {', '.join(requested_providers(config)) or '—'}.",
        f"Providers run: {', '.join(present) or '(none — runtime only)'}.",
        f"Providers skipped (missing key or stub): {', '.join(missing) or '—'}.",
        "",
    ]
    if halt.error is not None:
        lines.extend([f"**Budget halt:** {halt.error}", ""])
    lines.extend(_summary_block("Experiment (ii) — runtime (solver)", aggregate(runtime_rows)))
    if llm_rows:
        scored_llm = [row for row in llm_rows if row.get("outcome_match") is not None]
        lines.extend(_summary_block("Experiment (ii) — LLM-only (all providers)", aggregate(scored_llm)))
        for name in present:
            subset = [row for row in scored_llm if row.get("provider") == name]
            if subset:
                lines.extend(_summary_block(f"Experiment (ii) — LLM-only `{name}`", aggregate(subset)))
    else:
        lines.extend(["### Experiment (ii) — LLM-only", "", "_No LLM rows (no keys, skipped, or runtime-only)._", ""])
    if extraction_rows:
        lines.extend(["### Experiment (i) — encoding", ""])
        lines.append(render_experiment_i(extraction_rows))
        f1s = [row["alignment_f1"] for row in extraction_rows if isinstance(row.get("alignment_f1"), float)]
        if f1s:
            lines.append(f"Mean alignment F1: {sum(f1s) / len(f1s):.3f} (n={len(f1s)}).")
            lines.append("")
    else:
        lines.extend(["### Experiment (i) — encoding", "", "_No extraction rows._", ""])
    lines.extend(
        [
            "## How to read this",
            "",
            "- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.",
            "- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.",
            "- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).",
            "",
        ]
    )
    return "\n".join(lines)


def run_matrix(
    config: dict[str, Any],
    *,
    results_dir: Path,
    runtime_only: bool = False,
    complete_factory: Callable[..., Any] | None = None,
    ingest_ledger: bool = True,
    resume_since: str | None = None,
) -> dict[str, Any]:
    """Execute the matrix. Returns a JSON-serializable report dict.

    ``resume_since`` (ISO-8601 UTC, e.g. ``2026-08-25T00:00:00Z``) additionally
    treats ledger rows at/after that timestamp as completed, so a relaunched
    run skips rows it already paid for even when the previous process died
    before writing its results JSONL.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    cap = float(config.get("budget_eur") or os.environ.get("FRAMEWORK_BUDGET_EUR") or 10)
    os.environ.setdefault("FRAMEWORK_BUDGET_EUR", str(cap))
    guard = BudgetGuard(cap_eur=cap)
    if ingest_ledger:
        path = ledger_path()
        if path.is_file():
            try:
                guard.ingest_ledger(path)
            except BudgetExceeded as exc:
                log.warning("Ledger already at or over cap: %s", exc)
                runtime_only = True
    halt = HaltState()
    scenario_files = gold_scenario_files(config)
    repeats = int(config.get("repeats") or 1)
    present, missing = available_requested_providers(config)
    for name in missing:
        log.warning("Skipping provider %s: missing API key or stub", name)

    runtime_rows: list[dict[str, Any]] = []
    llm_rows: list[dict[str, Any]] = []
    extraction_rows: list[dict[str, Any]] = []

    # Append-only result files: never truncated, rows written as they finish.
    llm_results_path = results_dir / "experiment_ii_llm.jsonl"
    extraction_results_path = results_dir / "experiment_i.jsonl"

    exp_ii = config.get("experiment_ii") or {}
    if exp_ii.get("enabled", True):
        runtime_rows = run_runtime_phase(scenario_files)

    if not runtime_only:
        if exp_ii.get("enabled", True) and present:
            completed_ii = load_completed_keys(
                experiment="ii",
                results_path=llm_results_path,
                resume_since=resume_since,
            )
            if completed_ii:
                log.info("resume: %d experiment-ii keys already recorded", len(completed_ii))
            llm_rows = run_llm_phase(
                scenario_files=scenario_files,
                providers=present,
                repeats=repeats,
                guard=guard,
                halt=halt,
                complete_factory=complete_factory,
                completed=completed_ii,
                results_path=llm_results_path,
            )
        exp_i = config.get("experiment_i") or {}
        if exp_i.get("enabled", True) and present and halt.error is None:
            cases = [str(item) for item in (exp_i.get("cases") or [])]
            condition = str(exp_i.get("condition") or "synthesis")
            completed_i = load_completed_keys(
                experiment="i",
                results_path=extraction_results_path,
                resume_since=resume_since,
            )
            if completed_i:
                log.info("resume: %d experiment-i keys already recorded", len(completed_i))
            extraction_rows = run_extraction_phase(
                cases=cases,
                condition=condition,
                providers=present,
                repeats=repeats,
                guard=guard,
                halt=halt,
                complete_factory=complete_factory,
                completed=completed_i,
                results_path=extraction_results_path,
            )
    else:
        log.info("runtime-only: skipping LLM phases")

    # Runtime rows are free and deterministic; regenerating the file is safe.
    _write_jsonl(results_dir / "experiment_ii_runtime.jsonl", runtime_rows)
    # LLM/extraction rows: read the append-only files back so summaries and
    # markdown cover the whole run (prior resumed rows + this process's rows).
    llm_rows = _dedupe_result_rows("ii", _load_jsonl(llm_results_path))
    extraction_rows = _dedupe_result_rows("i", _load_jsonl(extraction_results_path))
    _write_text(
        results_dir / "experiment_ii_runtime.md",
        f"# Experiment (ii) runtime — {SMOKE_BANNER}\n\n"
        + render_markdown_table(runtime_rows),
    )
    _write_text(
        results_dir / "experiment_ii_llm.md",
        f"# Experiment (ii) LLM-only — {SMOKE_BANNER}\n\n"
        + (render_markdown_table(llm_rows) if llm_rows else "_No LLM rows._\n"),
    )
    pairs: list[dict[str, Any]] = []
    if runtime_rows and llm_rows:
        runtime_by_name = {row["scenario"]: row for row in runtime_rows}
        for llm_row in llm_rows:
            runtime_row = runtime_by_name.get(llm_row.get("scenario"))
            if runtime_row and llm_row.get("outcome_match") is not None:
                pair = pair_rows(runtime_row, llm_row)
                pair["llm_provider"] = llm_row.get("provider")
                pairs.append(pair)
        _write_text(
            results_dir / "experiment_ii_paired.md",
            f"# Experiment (ii) paired — {SMOKE_BANNER}\n\n"
            + render_paired_markdown(pairs),
        )
    _write_text(
        results_dir / "experiment_i.md",
        f"# Experiment (i) — {SMOKE_BANNER}\n\n"
        + (render_experiment_i(extraction_rows) if extraction_rows else "_No extraction rows._\n"),
    )
    summary = render_smoke_summary(
        config=config,
        runtime_rows=runtime_rows,
        llm_rows=llm_rows,
        extraction_rows=extraction_rows,
        present=present,
        missing=missing,
        guard=guard,
        halt=halt,
    )
    _write_text(results_dir / "SMOKE-UNVALIDATED.md", summary)

    report = {
        "label": config.get("label"),
        "n_runtime": len(runtime_rows),
        "n_llm": len(llm_rows),
        "n_extraction": len(extraction_rows),
        "providers_run": present,
        "providers_skipped": missing,
        "spent_eur": guard.spent_eur,
        "cap_eur": guard.cap_eur,
        "budget_halt": str(halt.error) if halt.error else None,
        "runtime_stats": aggregate(runtime_rows) if runtime_rows else {},
        "llm_stats": aggregate(
            [row for row in llm_rows if row.get("outcome_match") is not None]
        )
        if llm_rows
        else {},
        "results_dir": str(results_dir),
    }
    return report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(default_matrix_path()),
        help="Path to experiments/matrix.yaml",
    )
    parser.add_argument(
        "--results-dir",
        default=str(default_results_dir()),
        help="Directory for markdown summaries and gitignored JSONL",
    )
    parser.add_argument(
        "--runtime-only",
        action="store_true",
        help="Skip all LLM calls (still writes runtime gold rows).",
    )
    parser.add_argument(
        "--resume-since",
        default=None,
        help=(
            "ISO-8601 UTC timestamp (e.g. 2026-08-25T00:00:00Z): also skip "
            "rows the cost ledger recorded at/after this time. Rows in the "
            "results JSONL are always skipped."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan and available providers; do not run.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    loaded = load_runtime_env()
    if loaded:
        log.info("Loaded env from %s", ", ".join(loaded))
    config = load_matrix(args.config)
    present, missing = available_requested_providers(config)
    scenarios = gold_scenario_files(config)
    print(f"matrix: {config.get('label')}  scenarios: {len(scenarios)}")
    print(f"providers available: {present or '(none)'}")
    print(f"providers skipped: {missing or '(none)'}")
    set_keys = [name for name in _KEY_NAMES if os.environ.get(name, "").strip()]
    print(f"env keys present: {set_keys or '(none)'}")
    if args.dry_run:
        return 0
    report = run_matrix(
        config,
        results_dir=Path(args.results_dir),
        runtime_only=args.runtime_only,
        resume_since=args.resume_since,
    )
    print(json.dumps({k: v for k, v in report.items() if k != "runtime_stats"}, indent=2, default=str))
    if report.get("budget_halt"):
        log.warning("Stopped at budget cap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
