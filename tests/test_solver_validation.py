"""The acceptance test: the trusted path reproduces every oracle outcome.

Runs the solver-validation condition (every node oracle/file, z3 decision,
rendered trace) over all 47 scenarios and requires exact agreement on the
scored outcome, the fine-grained state, and the missing-term set.
"""

from statute_decider.runner.conditions import load_condition
from statute_decider.runner.engine import CellServices, run_scenario
from statute_decider.runner.scoring import score_outcome


def test_solver_validation_full_agreement(root, store):
    condition = load_condition(root / "configs" / "conditions" / "solver-validation.yaml")
    services = CellServices(prompts_dir=root / "prompts")
    failures = []
    for case_id, scenario_id in store.all_scenarios():
        run = run_scenario(store, condition, case_id, scenario_id, services)
        produced = run.value("premise_outcome")
        oracle = store.oracle_value(case_id, "premise_outcome", scenario_id)
        score = score_outcome(produced, oracle)
        if not (
            score["outcome_correct"] and score["state_correct"] and score["missing_f1"] == 1.0
        ):
            failures.append((case_id, scenario_id, score))
        trace = run.value("outcome_trace")
        assert trace is not None and trace.justification
    assert not failures, failures
