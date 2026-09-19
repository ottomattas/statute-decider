"""A finished solver-only --resume must not rewrite any result sidecar."""

from __future__ import annotations

import hashlib
from pathlib import Path

from statute_decider.runner.experiment import run_experiment

EXPERIMENT_YAML = """\
name: resume-noop-test
condition: solver-validation
cases:
  - building_permit_grant
scenarios:
  - building_permit_grant/deny_register_only_plan_nonconformity
models: []
repeats: 1
budget_eur: 0.0
"""


def _snapshot(results_dir: Path) -> dict[str, tuple[int, str]]:
    out: dict[str, tuple[int, str]] = {}
    for path in sorted(results_dir.rglob("*")):
        if path.is_file():
            out[str(path.relative_to(results_dir))] = (
                path.stat().st_mtime_ns,
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
    return out


def test_resume_noop_does_not_touch_results(tmp_path, root):
    exp_dir = tmp_path / "resume-noop-test"
    exp_dir.mkdir()
    (exp_dir / "experiment.yaml").write_text(EXPERIMENT_YAML, encoding="utf-8")
    results = run_experiment(
        root, exp_dir, execution="sequential", models=["all"]
    )
    before = _snapshot(results)
    assert before
    again = run_experiment(
        root, exp_dir, execution="sequential", models=["all"], resume=True
    )
    assert again == results
    assert _snapshot(results) == before
