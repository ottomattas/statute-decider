"""Run the teaching case end to end on the real pipeline and print the traces.

Usage (from the repo root):

    .venv/bin/python examples/teaching/renew_driving_licence/run_demo.py

Uses the solver-validation condition: oracle claims, live register lookup,
z3 decision, rendered trace. No LLM calls, no cost.
"""

from __future__ import annotations

from pathlib import Path

from statute_decider.core import DataStore
from statute_decider.runner.conditions import load_condition
from statute_decider.runner.engine import CellServices, run_scenario

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

CASE_ID = "driving_licence_renewal"


def main() -> None:
    store = DataStore(HERE / "data")
    condition = load_condition(REPO / "configs" / "conditions" / "solver-validation.yaml")
    services = CellServices(prompts_dir=REPO / "prompts")

    print(f"Case: {CASE_ID} (teaching example)\n" + "=" * 72)
    for scenario_id in store.scenario_ids(CASE_ID):
        scenario = store.scenario(CASE_ID, scenario_id)
        run = run_scenario(store, condition, CASE_ID, scenario_id, services)
        outcome = run.value("premise_outcome")
        trace = run.value("outcome_trace")
        oracle = store.oracle_value(CASE_ID, "premise_outcome", scenario_id)

        print(f"\nScenario: {scenario_id}")
        print(f"  {scenario.description.strip()}")
        print(f"  Utterance: {store.utterance_text(CASE_ID, scenario).strip()!r}")
        print(f"  Outcome:   {outcome.state.value}  (oracle: {oracle.state.value})"
              f"  {'OK' if outcome.state == oracle.state else 'MISMATCH'}")
        if outcome.fired_rules:
            fired = ", ".join(f"{r.premise_id} -> {r.effect}" for r in outcome.fired_rules)
            print(f"  Fired:     {fired}")
        if outcome.missing_terms:
            missing = ", ".join(f"{m.term_id} ({m.reason.value})" for m in outcome.missing_terms)
            print(f"  Missing:   {missing}")
        if trace is not None:
            print("  Trace:")
            for line in trace.justification.strip().splitlines():
                print(f"    {line}")


if __name__ == "__main__":
    main()
