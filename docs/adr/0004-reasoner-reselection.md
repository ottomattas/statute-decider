# ADR 0004: Reasoner re-selection — Z3 to a dedicated propositional/ASP backend

## Status

Accepted — 2026-04-21 (Wave 2 Stream A, ART-67)

## Context

The current implementation uses Z3 (`z3-solver`) as the sole symbolic engine throughout
`framework/reasoner.py`. Z3 is a general-purpose SMT solver designed for verification tasks
that mix arithmetic, bitvectors, and propositional logic. The pipeline is purely propositional:
it needs monotonic forward chaining, default/exception handling (defeasible reasoning), and
abduction over missing premises — none of which is a native strength of Z3.

Two supervision discussions crystallised this mismatch:

- **2026-04-10, ~36:50–37:54**: Tanel explicitly recommended against Z3 for this pipeline.
  His core argument (paraphrased): Z3 targets SMT verification problems that involve numbers
  and quantifiers; our tasks are structurally closer to ASP ("aspi tüüpi") — defaults,
  exceptions, and abductive reasoning over incomplete information. Otto acknowledged this as
  a single-module replacement feasible within the current architecture.

- **2026-04-14, ~25:28–26:35**: Priit's decision — assume monotonic semantics first;
  non-monotonic extensions (defaults, exceptions) require a different logic treatment and
  should land after the monotonic baseline is stable and tested.

The scientific framing in `.cursor/rules/project_knowledge.mdc` already targets
**enthymemes, defeasible logic, and abduction** — exactly the semantics Tanel identified as
better served by an ASP-style backend.

Current code uses Z3 throughout: `framework/reasoner.py` imports `z3.Solver`, `z3.Bool`,
`z3.Implies`, `z3.And`, `z3.Not`; `framework/requirements.txt` lists `z3-solver>=4.12`.
Every Z3 call must sit behind an abstraction before the swap can land safely.

## Decision

Introduce a `ReasonerBackend` `typing.Protocol` in `framework/reasoner.py` and move the
current Z3 implementation verbatim into `framework/reasoner_z3.py`. The public API used by
`framework/03_solve_case.py` (`solve_case_bundle`) is preserved unchanged for all existing
call sites.

**Shortlisted backends for Wave 2 benchmarking:**

| Backend | Engine | Rationale |
|---------|--------|-----------|
| clingo  | ASP via `clingo` | Primary candidate. Native defaults, exceptions, non-monotonic extension, and meta-encoded abduction match Tanel's 10 Apr recommendation. |
| PySAT   | propositional SAT via `python-sat` | Monotonic baseline; matches Priit's 14 Apr "monotonic first" decision. Fastest expected runtime. |
| Horn    | hand-rolled Horn forward-chaining | Pedagogical tie-break; no external dependency; oracle when SAT and ASP disagree. |
| Z3      | Z3 SMT | Reference implementation during benchmarking; retire only after a winner is confirmed. |

**Default engine in Wave 1:** Z3, unchanged. The active backend is controlled by the
environment variable `FRAMEWORK_REASONER` (accepted values: `z3` (default), `clingo`,
`pysat`, `horn`). Non-Z3 backends raise `NotImplementedError` with a pointer to this ADR
until Wave 2 implements them.

## Consequences

- `framework/reasoner.py` becomes a thin Protocol definition and dispatcher; all Z3 logic
  lives in `framework/reasoner_z3.py`.
- `from reasoner import solve_case_bundle` continues to work from every existing call site
  with no change in behaviour.
- Wave 2 adds `framework/reasoner_clingo.py`, `framework/reasoner_pysat.py`, and
  `framework/reasoner_horn.py` behind the same Protocol, then runs a benchmark harness
  (`framework/bench_reasoners.py`) to pick the default.
- Wave 3 writes the benchmark recommendation back into this ADR, updates
  `framework/requirements.txt` with the chosen engine, and changes the default
  `FRAMEWORK_REASONER` value.
- `.cursor/rules/neurosymbolic_coder.mdc` currently says "Z3 authoritative"; that clause
  should be updated in the same patch as the Wave 3 benchmark decision to read "chosen
  symbolic backend authoritative; default engine pinned in ADR 0004".

## Alternatives considered

- **pyDatalog**: pure-Python datalog; expressive but lacks a maintained abduction extension
  and has limited community momentum. Deferred.
- **clorm**: high-level clingo ORM; adds abstraction overhead before we know clingo fits.
  Deferred until clingo baseline is green.
- **Raw SAT via CNF encoding**: lower-level than PySAT; manual CNF construction adds
  implementation risk without benchmarking benefit. Rejected for Wave 2.

All three may be revisited if clingo and PySAT both fail acceptance criteria.

## Recommendation

Wave 2 Stream A ran all four backends through the 15 seed scenarios
(`framework/examples/<case>/scenarios/*.json` across the five target cases:
civil_service_eligibility, consumer_withdrawal, land_tax_exemption,
personal_data_journalism, building_permit). Full benchmark output lives in
[`framework/examples/review_runs/reasoner_benchmark/2026-04-21.md`](../../framework/examples/review_runs/reasoner_benchmark/2026-04-21.md).

| scenario | case | expected | z3 | clingo | pysat | horn | agreement |
|---|---|---|---|---|---|---|---|
| civil_service_allow | civil_service_eligibility | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | YES |
| civil_service_deny | civil_service_eligibility | DENY | DENY | DENY | DENY | DENY | YES |
| civil_service_need_db | civil_service_eligibility | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | YES |
| consumer_withdrawal_allow | consumer_withdrawal | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | YES |
| consumer_withdrawal_deny | consumer_withdrawal | DENY | DENY | DENY | DENY | DENY | YES |
| consumer_withdrawal_need_user | consumer_withdrawal | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | YES |
| land_tax_allow | land_tax_exemption | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | YES |
| land_tax_deny | land_tax_exemption | DENY | DENY | DENY | DENY | DENY | YES |
| land_tax_need_db | land_tax_exemption | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | YES |
| journalism_allow | personal_data_journalism | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | YES |
| journalism_deny | personal_data_journalism | DENY | DENY | DENY | DENY | DENY | YES |
| journalism_need_user | personal_data_journalism | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | NEED_USER_INFO | YES |
| building_permit_allow | building_permit | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | YES |
| building_permit_deny | building_permit | DENY | DENY | DENY | DENY | DENY | YES |
| building_permit_need_db | building_permit | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | NEED_DB_INFO | YES |

Agreement with Z3: clingo 15/15, PySAT 15/15, Horn 15/15. No divergences
observed on the monotonic fragment exercised by the seed suite. Mean
wall-time per solve (15-scenario average):

| backend | mean wall-time (ms) |
|---------|--------------------:|
| Z3      | 7.00 |
| clingo  | 0.56 |
| PySAT   | 0.26 |
| Horn    | 0.09 |

**Chosen default engine: `clingo`.** Rationale:

- Tanel's 10 Apr recommendation explicitly targets ASP semantics (defaults,
  exceptions, abductive inference) over SMT; clingo is the only candidate
  that will still be appropriate once Wave 3 adds non-monotonic extensions
  (ART-64 uncertainty codes, abductive layer).
- On the monotonic fragment clingo matches Z3 exactly (15/15) and runs
  ~12× faster per solve.
- PySAT is kept as a pure-propositional fallback and is the right pick if
  a case ever hits a clingo grounding blow-up on this fragment — it
  matches Z3 on every seed scenario at the lowest wall-time among the
  SAT/ASP engines.
- Horn forward chaining is retained as the pedagogical oracle and
  zero-dependency smoke-test backend; it is not the default engine. Its
  role is to give the parity suite a fixed reference when the richer
  engines diverge.

**Rollout:** the dispatcher default remains `FRAMEWORK_REASONER=z3` in
this patch so the Wave 1 Z3 review runs stay reproducible byte-for-byte;
the default will flip to `clingo` in a Wave 3 patch alongside the
uncertainty-code wiring. Each backend's contract
(`solve_case_bundle_with_engine`, shared in `framework/reasoner_horn.py`)
produces the same `SolutionArtifact` shape, so switching the default is a
one-line change.

**Divergences:** none on the current seed suite. Once ART-64 adds the
U1..U12 uncertainty codes, the benchmark should be rerun and any engine
that diverges from clingo (the post-Wave-3 reference) should have its
encoding gap filed as a follow-up.

## References

- [ADR 0001: Graph-native knowledge objects](0001-graph-native-knowledge-objects.md)
- [ADR 0002: Canonical docs and phase-based delivery](0002-canonical-docs-and-phase-commits.md)
- [ADR 0003: Proposition-first staging](0003-poc3-proposition-first-staging.md)
- `.cursor/rules/project_knowledge.mdc` — scientific framing (enthymemes, defeasible logic,
  abduction)
- Plan §0.5 and Track E — `post-17apr-research-push_a0104936.plan.md`
