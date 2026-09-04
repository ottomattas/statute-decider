"""The experiment engine: grid expansion, parallel execution, recorded results.

An experiment names a condition, cases, models, prompts, repeats, and budget;
the run snapshots everything it resolved (``config.snapshot.yaml``), records
every node value (``nodes/<node>.jsonl``), one row per grid cell
(``rows.jsonl``), the cost slice (``ledger.jsonl``), and a generated report
(``summary.md``).
"""

from __future__ import annotations

import itertools
import json
import logging
import threading
import uuid
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from statute_decider.core import DataStore
from statute_decider.core.provenance import utc_now
from statute_decider.llm import BudgetGuard, LLMClient, ModelRegistry, load_dotenv
from statute_decider.nodes import NODE_ORDER
from statute_decider.runner.conditions import load_condition
from statute_decider.runner.engine import CellServices, node_value_dump, run_scenario
from statute_decider.runner.report import render_summary
from statute_decider.runner.scoring import score_claims, score_outcome, score_utterance_terms

log = logging.getLogger(__name__)


class ExperimentConfig(BaseModel):
    name: str
    question: str = ""
    condition: str
    cases: list[str] | str = "all"
    models: list[str] = Field(default_factory=list)
    prompts: dict[str, list[str]] = Field(default_factory=dict)  # node -> variants (sweep)
    repeats: int = 1
    temperature: float = 0.0
    max_output_tokens: int = 8192
    budget_eur: float = 5.0
    notes: str = ""


class _JsonlWriter:
    def __init__(self, path: Path, *, append: bool = False) -> None:
        self.path = path
        self.lock = threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)
        if not append or not path.exists():
            path.write_text("", encoding="utf-8")

    def write(self, row: dict) -> None:
        line = json.dumps(row, ensure_ascii=False, default=str)
        with self.lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def _cell_key(row: dict) -> tuple:
    """Identity of one grid cell: what --resume compares against."""
    prompts = row.get("prompts") or {}
    return (
        row.get("case_id"),
        row.get("scenario_id"),
        row.get("model"),
        tuple(sorted(prompts.items())),
        int(row.get("repeat") or 1),
    )


def _load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _ledger_spent(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            total += float(json.loads(line).get("eur") or 0.0)
    return total


def load_experiment(path: Path | str) -> ExperimentConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ExperimentConfig.model_validate(raw)


def _prompt_combos(sweep: dict[str, list[str]]) -> list[dict[str, str]]:
    if not sweep:
        return [{}]
    nodes = sorted(sweep)
    combos = []
    for values in itertools.product(*(sweep[node] for node in nodes)):
        combos.append(dict(zip(nodes, values)))
    return combos


def run_experiment(
    root: Path | str,
    experiment_path: Path | str,
    *,
    execution: str,
    models: list[str],
    providers: list[str] | None = None,
    solver: str | None = None,
    resume: bool = False,
    rerun_errors: bool = False,
    limit: int | None = None,
) -> Path:
    """Run one experiment; returns the results directory.

    ``resume`` skips cells that already have a row (``rerun_errors`` re-runs
    the errored ones); ``limit`` caps how many new cells this invocation runs,
    so an expensive grid can be advanced in budget-sized batches.
    """
    root = Path(root)
    experiment_path = Path(experiment_path)
    if experiment_path.is_dir():
        experiment_path = experiment_path / "experiment.yaml"
    experiment_dir = experiment_path.parent
    config = load_experiment(experiment_path)
    condition = load_condition(root / "configs" / "conditions" / f"{config.condition}.yaml")
    store = DataStore(root / "data")
    load_dotenv(root / ".env")

    results_dir = experiment_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # --resume: keep every finished cell (and, unless --rerun-errors, every
    # errored one) from results/rows.jsonl; append to rows/nodes/ledger/log
    # instead of truncating; the budget guard starts from what the ledger
    # already spent. Without --resume a rerun overwrites rows and nodes but
    # the ledger still appends — so never rerun a finished experiment blind.
    previous_rows: list[dict] = []
    done_keys: set[tuple] = set()
    if resume:
        previous_rows = _load_rows(results_dir / "rows.jsonl")
        if not rerun_errors:
            done_keys = {_cell_key(r) for r in previous_rows}
        else:
            done_keys = {_cell_key(r) for r in previous_rows if not r.get("error")}
            previous_rows = [r for r in previous_rows if not r.get("error")]
        # Rewrite rows.jsonl to the kept set so a dropped error row is not
        # duplicated by its rerun.
        with (results_dir / "rows.jsonl").open("w", encoding="utf-8") as handle:
            for r in previous_rows:
                handle.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

    file_handler = logging.FileHandler(
        results_dir / "run.log", mode="a" if resume else "w", encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)

    registry = ModelRegistry(
        root / "configs" / "llm" / "models.yaml", root / "configs" / "llm" / "prices.yaml"
    )
    budget = BudgetGuard(
        cap_eur=config.budget_eur,
        ledger_path=results_dir / "ledger.jsonl",
        usd_to_eur=registry.usd_to_eur,
    )
    if resume:
        budget.spent_eur = _ledger_spent(results_dir / "ledger.jsonl")
    elif (results_dir / "ledger.jsonl").exists():
        (results_dir / "ledger.jsonl").unlink()  # fresh run: fresh ledger, no double count
    # 5 attempts with 20/40/60/80 s backoff: a multi-minute network blip (3 Sep
    # 23:18 lost 33 cells to DNS failures under 3 x 5 s) must not cost rows.
    # Budget and vendor 4xx errors still surface after the last attempt.
    client = LLMClient(
        registry,
        budget,
        max_retries=4,
        retry_backoff_s=20.0,
        transcript_path=results_dir / "transcript.jsonl",
    )

    # Resolve the model grid. 'all' means the experiment's declared list (or the
    # whole registry when the experiment declares none). Conditions with no llm
    # node run once, deterministically.
    if condition.uses_llm():
        requested = models
        if any(m == "all" for m in requested):
            requested = config.models or ["all"]
        specs = registry.resolve(requested)
        if providers:
            specs = [spec for spec in specs if spec.provider in providers]
        if not specs:
            raise ValueError("Model selection resolved to an empty grid.")
        repeats = config.repeats
    else:
        specs = [None]
        repeats = 1
        if not any(m == "all" for m in models):
            log.info("Condition %s has no llm nodes; --models ignored.", condition.condition)

    case_ids = None if config.cases == "all" else list(config.cases)
    pairs = store.all_scenarios(case_ids)
    combos = _prompt_combos(config.prompts)

    rows_writer = _JsonlWriter(results_dir / "rows.jsonl", append=resume)
    node_writers = {
        node: _JsonlWriter(results_dir / "nodes" / f"{node}.jsonl", append=resume)
        for node in NODE_ORDER
    }
    if not resume and (results_dir / "transcript.jsonl").exists():
        (results_dir / "transcript.jsonl").unlink()  # client appends; fresh run starts clean

    snapshot = {
        "generated_at": utc_now(),
        "experiment": config.model_dump(),
        "condition": condition.model_dump(),
        "execution": execution,
        "models": [spec.model_id for spec in specs if spec is not None],
        "providers_filter": providers or [],
        "solver_override": solver,
        "prompt_combos": combos,
        "repeats": repeats,
        "scenarios": [f"{case}/{scen}" for case, scen in pairs],
        "budget_eur": config.budget_eur,
        "resume": resume,
        "rerun_errors": rerun_errors,
        "limit": limit,
        "kept_rows": len(previous_rows),
    }
    (results_dir / "config.snapshot.yaml").write_text(
        yaml.safe_dump(snapshot, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    # Every invocation is recorded; a resumed experiment has several.
    with (results_dir / "invocations.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, ensure_ascii=False, default=str) + "\n")

    rows: list[dict] = list(previous_rows)
    rows_lock = threading.Lock()

    def make_unit(case_id: str, scenario_id: str, spec, combo: dict[str, str], repeat: int):
        def unit() -> None:
            run_id = uuid.uuid4().hex[:12]
            row: dict = {
                "run_id": run_id,
                "timestamp": utc_now(),
                "experiment": config.name,
                "condition": condition.condition,
                "case_id": case_id,
                "scenario_id": scenario_id,
                "provider": spec.provider if spec else "code",
                "model": spec.model_id if spec else None,
                "prompts": combo,
                "solver": solver or condition.binding("premise_outcome").solver,
                "repeat": repeat,
                "logic": condition.logic,
                "fuse": condition.fuse,
                "execution": execution,
                "temperature": config.temperature,
                "error": "",
            }
            try:
                services = CellServices(
                    prompts_dir=root / "prompts",
                    client=client if spec else None,
                    model_id=spec.model_id if spec else None,
                    temperature=config.temperature,
                    max_output_tokens=config.max_output_tokens,
                    prompt_overrides=combo,
                    solver_override=solver,
                    meta={"experiment": config.name, "run_id": run_id, "repeat": repeat,
                          "model": spec.model_id if spec else None},
                )
                run = run_scenario(store, condition, case_id, scenario_id, services)
                produced_outcome = run.value("premise_outcome")
                if produced_outcome is not None:
                    row["produced_state"] = produced_outcome.state.value
                    row["produced_scored_as"] = produced_outcome.scored_as.value
                    row["missing_terms"] = sorted(produced_outcome.missing_term_ids())
                    row["free_missing"] = produced_outcome.free_missing
                    oracle_outcome = store.oracle_value(case_id, "premise_outcome", scenario_id)
                    if oracle_outcome is not None:
                        row["score"] = score_outcome(produced_outcome, oracle_outcome)
                produced_terms = run.value("utterance_term")
                oracle_terms = store.oracle_value(case_id, "utterance_term", scenario_id)
                if produced_terms is not None and oracle_terms is not None:
                    row["term_score"] = score_utterance_terms(produced_terms, oracle_terms)
                produced_claims = run.value("term_claim")
                oracle_claims = store.oracle_value(case_id, "term_claim", scenario_id)
                if produced_claims is not None and oracle_claims is not None:
                    row["claim_score"] = score_claims(produced_claims, oracle_claims)
                for node in NODE_ORDER:
                    value = run.value(node)
                    if value is None or isinstance(value, str):
                        continue
                    node_writers[node].write(
                        {
                            "run_id": run_id,
                            "case_id": case_id,
                            "scenario_id": scenario_id,
                            "model": row["model"],
                            "repeat": repeat,
                            "value": node_value_dump(value),
                        }
                    )
            except Exception as exc:  # noqa: BLE001 - a cell failure must not kill the grid
                row["error"] = f"{type(exc).__name__}: {exc}"
                log.warning("Cell failed %s/%s %s: %s", case_id, scenario_id, row["model"], exc)
            rows_writer.write(row)
            with rows_lock:
                rows.append(row)

        provider = spec.provider if spec else "code"
        return provider, unit

    all_cells = [
        (case_id, scenario_id, spec, combo, repeat)
        for (case_id, scenario_id) in pairs
        for spec in specs
        for combo in combos
        for repeat in range(1, repeats + 1)
    ]
    pending = [
        cell
        for cell in all_cells
        if _cell_key(
            {
                "case_id": cell[0],
                "scenario_id": cell[1],
                "model": cell[2].model_id if cell[2] else None,
                "prompts": cell[3],
                "repeat": cell[4],
            }
        )
        not in done_keys
    ]
    if limit is not None:
        pending = pending[: max(0, limit)]
    units = [make_unit(*cell) for cell in pending]
    log.info(
        "Experiment %s: %d cells (%d scenarios x %d models x %d prompt combos x %d repeats), "
        "%d kept from a previous run, %d to run now%s, %s.",
        config.name,
        len(all_cells),
        len(pairs),
        len(specs),
        len(combos),
        repeats,
        len(previous_rows),
        len(units),
        f" (limit {limit})" if limit is not None else "",
        execution,
    )
    if units:
        client.run_units(units, execution=execution)

    summary = render_summary(
        experiment=config.model_dump(),
        condition=condition,
        rows=rows,
        results_dir=results_dir,
        execution=execution,
    )
    (results_dir / "summary.md").write_text(summary, encoding="utf-8")
    log.info("Experiment %s done: %d rows, EUR %.4f.", config.name, len(rows), budget.spent_eur)
    logging.getLogger().removeHandler(file_handler)
    return results_dir
