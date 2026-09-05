# Scenario Suite

> **Historical (v1 `framework/` tree).** This document describes the 2026-04 harness;
> the v2 suite is `data/cases/**` (54 scenarios, `docs/reference/gold-review-2026-09-05.md`)
> and is run through `experiments/*/experiment.yaml`. Identifiers below are shown in the
> current vocabulary; the v1 names are kept only in `docs/reference/id-aliases.md`.

## Overview

The scenario suite is a systematic harness for validating the symbolic reasoner
against a curated set of expected outcomes across the five framework domains.
It directly addresses the supervisor ask from 2026-04-17: build many real test
cases with expected-vs-actual reporting, aiming for full truth-table coverage
where variable count allows.

Plan reference: Track B in `post-17apr-research-push` plan.

## Domains covered

| Case directory | Statute | Scenarios |
|---|---|---|
| `civil_service_admission` | Civil Service Act §§ 14–15 | ALLOW, DENY, NEED_REGISTER_INFO |
| `consumer_purchase_withdrawal` | Law of Obligations Act § 53 (4), § 56 (1) | ALLOW, DENY, NEED_USER_INFO |
| `land_tax_home_exemption` | Land Tax Act § 11 | ALLOW, DENY, NEED_REGISTER_INFO |
| `journalistic_data_disclosure` | Personal Data Protection Act § 4 | ALLOW, DENY, NEED_USER_INFO |
| `building_permit_grant` | Building Code §§ 42, 44 | ALLOW, DENY, NEED_REGISTER_INFO |

## JSON schema for one scenario

Each file in `framework/examples/<case>/scenarios/*.json` is a superset of the
legacy `ScenarioDefinition` shape. Fields understood by the harness:

```json
{
  "name": "allow_claims_verified",
  "description": "Human-readable description of the scenario.",
  "request_file": "request_allow.txt",
  "law_file": "law.txt",
  "mock_db_file": "mock_db.json",
  "intent_assignments": {
    "ee_citizen": true,
    "criminal_conviction": false
  },
  "mock_db_overrides": {
    "ee_citizen": null
  },
  "expected_outcome": "ALLOW",
  "expected_reason_code": null,
  "tags": ["positive"],
  "provenance": "Supervisor meeting 2026-04-17"
}
```

### Field reference

| Field | Pydantic model | Description |
|---|---|---|
| `name` | `SuiteScenario.name` | Unique name; also the file stem. |
| `description` | `SuiteScenario.description` | One-sentence human description. |
| `request_file` | `SuiteScenario.request_file` | Request text file (used for metadata). |
| `law_file` | `SuiteScenario.law_file` | Law text file used to build the domain. |
| `mock_db_file` | `SuiteScenario.mock_db_file` | Base mock-DB JSON. |
| `intent_assignments` | `SuiteScenario.intent_assignments` | Claim values to inject at the intent stage; `null` means "unknown". |
| `mock_db_overrides` | `SuiteScenario.mock_db_overrides` | Per-claim DB value overrides applied on top of `mock_db_file`; `null` removes the key (simulates missing data). |
| `expected_outcome` | `SuiteScenario.expected_outcome` | One of `ALLOW`, `DENY`, `NEED_DB_INFO`, `NEED_USER_INFO` (matches `SolverOutcome`). |
| `expected_reason_code` | `SuiteScenario.expected_reason_code` | One of the `BlockReasonCode` values, or `null` (Wave 2 will fill these). |
| `tags` | `SuiteScenario.tags` | Free-text tags: `positive`, `negative`, `needs-info`. |
| `provenance` | `SuiteScenario.provenance` | Source reference for audit trail. |

The legacy fields (`name`, `request_file`, `law_file`, `mock_db_file`,
`intent_assignments`) are also consumed by the existing `run_scenarios.py`
review-run generator without change.

## How to run

From the repository root with the framework venv active:

```bash
source framework/venv/bin/activate

# Run the full suite (all 5 domains):
python framework/run_scenarios.py --scenarios

# Run only one scenario for debugging:
python framework/run_scenarios.py --scenarios --scenario-id allow_claims_verified
```

The harness exits non-zero if any scenario's actual outcome differs from
`expected_outcome` (or from `expected_reason_code` when set), so it can gate
CI in deterministic mode.

Output:
- Per-case Markdown tables written to
  `framework/examples/<case>/review_runs/scenario_suite/expected_vs_actual.md`.
- A totals line printed to stdout.

## How to add a new scenario

1. Identify the target case directory under `framework/examples/`.
2. Copy an existing scenario JSON from `scenarios/` as a template.
3. Set `intent_assignments` and `mock_db_overrides` so the solver reaches the
   desired state without any live LLM call.
4. Set `expected_outcome` to the matching `SolverOutcome` enum value and run
   `python framework/run_scenarios.py --scenarios --scenario-id <name>` to
   confirm the harness reports a match.

Wave 3 will add `expected_reason_code` values once the uncertainty-taxonomy
enum extension (Track A) lands.

## Truth-table mode

In addition to hand-written scenarios, the harness can enumerate the
complete boolean truth table of one case. This is a Wave 3a deliverable
(ART-65) aimed at proving rule completeness for small cases.

### How to run

From the `framework/` directory with the venv active:

```bash
# Enumerate all five target domains and write Markdown reports:
python run_scenarios.py --truth-table

# Or via the Makefile (equivalent):
make truth-tables

# Lower the cap to force certain domains to be skipped:
python run_scenarios.py --truth-table --max-vars 4
```

Output:

- Per-case Markdown reports are written to
  `framework/examples/<case>/review_runs/truth_tables/truth_table.md`.
- A totals line (`<N> enumerated, <M> skipped`) is printed to stdout.

### Semantics

`framework/truth_table.py` exposes:

- `TruthTableRow`: one enumerated assignment and its
  `(SolverOutcome, BlockReasonCode)`.
- `TruthTableReport`: all rows for one case plus `skipped` / `skip_reason`.
- `enumerate_truth_table(case_name, max_vars=6, mock_db_file=..., law_file=...)`:
  enumerate every `2**n` boolean assignment, building the intent artifact
  and applying the assignment as DB overrides before calling
  `reasoner.solve_case_bundle`. When `n > max_vars`, the report is flagged
  as skipped with no rows.
- `render_markdown(report)` / `write_markdown(report)`: render and
  persist the Markdown report.

### Domain coverage at `max_vars=6`

| Case | Claims | Rows |
|---|---|---|
| `civil_service_admission` | 7 | _skipped_ |
| `consumer_purchase_withdrawal` | 5 | 32 |
| `land_tax_home_exemption` | 6 | 64 |
| `journalistic_data_disclosure` | 5 | 32 |
| `building_permit_grant` | 6 | 64 |

### CI

The top-level `framework/Makefile` exposes three reproducible targets
that the GitHub Actions workflow (`.github/workflows/ci.yml`) invokes
in order:

```make
make test           # unittest discover under tests/
make scenarios      # python run_scenarios.py --scenarios
make truth-tables   # python run_scenarios.py --truth-table
```

## See also

- `docs/reference/nl-extraction.md` — step-00 NL user-input extractor
  (Track C, ART-66) that produces the intent assignments consumed by
  this harness when a scenario does not pin them explicitly.
