# Reasoner Reference

Canonical reference for the pluggable symbolic reasoning layer defined by
[`ADR 0004`](../adr/0004-reasoner-reselection.md). The public entry point
is the `ReasonerBackend` `typing.Protocol` declared in
`framework/reasoner.py`; every backend implements
`solve_case_bundle(CaseBundle) -> SolutionArtifact` and produces a
schema-identical `SolutionArtifact` on the monotonic rule fragment
(`ALLOW_IF_ALL`, `DENY_IF_ALL`, `SET_FALSE_IF_ALL`) exercised by the seed
scenarios.

## Available backends

| Name     | Module                                  | One-liner |
|----------|-----------------------------------------|-----------|
| `z3`     | `framework/reasoner_z3.py`              | Reference SMT backend (Boolean core) — always available; pinned for review-run reproducibility. |
| `clingo` | `framework/reasoner_clingo.py`          | ASP encoding with choice atoms for unknown claims; entailment via cautious/brave model enumeration. Tanel's 10 Apr recommendation. |
| `pysat`  | `framework/reasoner_pysat.py`           | Horn-CNF encoding over `Glucose3`; entailment via the two-call UNSAT pattern (facts ∪ theory ∪ ¬x) used by Z3. |
| `horn`   | `framework/reasoner_horn.py`            | Pure-Python forward-chaining fixpoint; zero external deps; pedagogical oracle and parity baseline. |

The `clingo` and `pysat` backends fail soft: if their optional
dependency is missing, the class stays importable but instantiation
raises `ImportError` with a pointer to `framework/requirements.txt`.
`horn` is pure Python and always available.

## Selecting a backend

The dispatcher `framework.reasoner.get_backend(name)` resolves in this
order:

1. Explicit `name` argument, when supplied.
2. `FRAMEWORK_REASONER` environment variable.
3. Default `"z3"`.

```bash
# one-shot override
FRAMEWORK_REASONER=clingo python framework/run_scenarios.py --scenarios

# benchmark-mode flag: run every available backend in one pass
python framework/bench_reasoners.py --backends z3,clingo,pysat,horn
```

`bench_reasoners.py` also honours `FRAMEWORK_REASONER` as the default
`--backends` value when it is set.

Unknown names raise `ValueError` pointing at ADR 0004.

## When to pick which

- Use **`clingo`** for any workflow that will eventually need defaults,
  exceptions, or abduction — it is the intended default once Wave 3
  lands the uncertainty-code wiring. On the current monotonic fragment
  it matches Z3 exactly and runs ~12× faster per solve.
- Use **`pysat`** when the workload is purely propositional Horn and
  wall-time matters. It is the fallback if a clingo grounding ever
  regresses on a new seed scenario.
- Use **`horn`** as the parity oracle in tests and for environments
  without native build toolchains; zero deps, slowest to extend.
- Keep **`z3`** for reproducing Wave 1 review runs byte-for-byte and
  for the `reasoner_z3.py` reference implementation of the plumbing
  (seed → snapshot → DB lookup → classify → blockage).

## Benchmark & rationale

See [`ADR 0004 — Reasoner re-selection`](../adr/0004-reasoner-reselection.md)
for the full decision record and the Recommendation section. The
per-run benchmark output is written to
`framework/examples/review_runs/reasoner_benchmark/<ISO-date>.md`.

## Roadmap notes

- **Uncertainty routing (U1..U12).** ART-64 owns the uncertainty-code
  schema. Once it lands, see [`schema.md`](schema.md) for the code list
  and this page will be updated with how each backend surfaces the
  codes.
- **Abduction.** The Wave 2 backends support the monotonic fragment
  only; abductive layering (hypothesising missing premises) is a Wave 3
  extension. Each backend file carries a `TODO` noting the gap.
