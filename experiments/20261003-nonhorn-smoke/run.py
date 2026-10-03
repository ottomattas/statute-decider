"""Non-Horn smoke: statutory cases through the unchanged Step 4.

Step 4 is ``Z3Solver.solve`` in ``src/statute_decider/solvers/z3_backend.py``. No rule kind
has two positive literals, so the clauses the schema cannot state enter the theory through a
raw-clause path: for each solve, the module's ``_Theory`` is swapped for a subclass whose
solver holds the compiled rules plus the raw clauses. Stage 1, Stage 2, both consistency
tests, entailment, the warrant check, the missing set and default DENY run as committed.
The script stops if the backend or the rule schema differs from HEAD.

    .venv/bin/python experiments/20261003-nonhorn-smoke/run.py

Writes ``results/outcomes.jsonl`` and ``results/summary.md`` beside this file.
"""

from __future__ import annotations

import json
import platform
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

import z3
from z3 import Bool, Not, Or

from statute_decider.core import (
    ClaimPremise,
    ClaimSet,
    Evidence,
    FactPremise,
    FactSet,
    OutcomeDef,
    RuleKind,
    RulePremise,
    RuleSet,
    Term,
    TermCatalog,
    Warrant,
)
from statute_decider.solvers import get_solver, z3_backend

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINNED = (
    "src/statute_decider/solvers/z3_backend.py",
    "src/statute_decider/core/premises.py",
    "src/statute_decider/core/enums.py",
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def pin() -> dict:
    """HEAD and the blob of every file Step 4 is made of; any drift stops the run."""
    blobs = {}
    for path in PINNED:
        head = git("rev-parse", f"HEAD:{path}")
        if git("hash-object", path) != head:
            raise SystemExit(
                f"{path} differs from HEAD; this smoke runs the committed Step 4 only."
            )
        blobs[path] = head
    return {"head": git("rev-parse", "HEAD"), "blobs": blobs}


class _RawClauseTheory(z3_backend._Theory):
    """The committed theory plus clauses no rule kind can state (``~`` marks a negative literal)."""

    clauses: tuple[tuple[str, ...], ...] = ()

    def __init__(self, catalog: TermCatalog, rules: RuleSet) -> None:
        super().__init__(catalog, rules)
        for clause in self.clauses:
            for literal in clause:
                atom = literal.removeprefix("~")
                self.vars.setdefault(atom, Bool(f"sd_{atom}"))

    def _base(self, valuation: dict[str, bool]):
        solver = super()._base(valuation)
        for clause in self.clauses:
            solver.add(
                Or(
                    [
                        Not(self.vars[lit[1:]]) if lit.startswith("~") else self.vars[lit]
                        for lit in clause
                    ]
                )
            )
        return solver


@contextmanager
def raw_clauses(clauses: tuple[tuple[str, ...], ...]):
    committed = z3_backend._Theory
    z3_backend._Theory = type("RawClauseTheory", (_RawClauseTheory,), {"clauses": clauses})
    try:
        yield
    finally:
        z3_backend._Theory = committed


@dataclass
class Scenario:
    scenario_id: str
    story: str
    gold: str  # ALLOW | DENY | NEED_MORE_INFO | DISCRETION (both outcomes lawful)
    facts: dict[str, bool] = field(default_factory=dict)  # authoritative register values
    claims: dict[str, bool] = field(default_factory=dict)
    covered: tuple[str, ...] = ()  # terms an available register answers, with or without a value


@dataclass
class Case:
    case_id: str
    title: str
    kind: str
    catalog: TermCatalog
    rules: RuleSet
    clauses: tuple[tuple[str, ...], ...]
    registers: dict[str, str]
    scenarios: list[Scenario]


def claim_set(sc: Scenario) -> ClaimSet:
    return ClaimSet(
        scenario_id=sc.scenario_id,
        claims=[
            ClaimPremise(premise_id=f"claim_{tid}", term_id=tid, value=value)
            for tid, value in sc.claims.items()
        ],
    )


def fact_set(case: Case, sc: Scenario) -> FactSet:
    return FactSet(
        scenario_id=sc.scenario_id,
        facts=[
            FactPremise(
                premise_id=f"fact_{tid}",
                term_id=tid,
                value=value,
                register_id=case.registers[tid],
                record_id="main",
                field=tid,
                warrant=Warrant.AUTHORITATIVE,
            )
            for tid, value in sc.facts.items()
        ],
        covered_terms=sorted(set(sc.covered) | set(sc.facts)),
    )


def route(note: str) -> str:
    """Which branch of Step 4 produced the state, read from the solver's own note."""
    text = note.lower()
    if "inconsistent" in text:
        return "inconsistent"
    if "warrant principle" in text:
        return "warrant"
    if "default deny" in text:
        return "default"
    if "entailed" in text:
        return "entailed"
    return "missing set"


# --- Civil Service Act § 108 (3) -------------------------------------------------------------

CS = "civil_service_act"
SUBMITTED = "composition_submitted"
REASON = "justified_reason"
NO_REASON = "no_justified_reason"
APPROVED = "approved"
REFUSED = "refused"


def cs108_catalog(renamed: bool = False) -> TermCatalog:
    terms = [
        Term(
            term_id=SUBMITTED,
            label="Staff composition and salary guide submitted for approval",
            definition=(
                "The authority submitted its staff composition and salary guide to the Ministry "
                "of Finance for approval (§ 108 (1)); the Ministry's document register records it."
            ),
            evidence=Evidence.REGISTER,
        ),
        Term(
            term_id=REASON,
            label="Justified reason to refuse approval",
            definition=(
                "The Ministry's review found a justified reason to refuse, e.g. the staff "
                "composition does not comply with the definition of an official in § 7 "
                "(§ 108 (1), last sentence; § 108 (3))."
            ),
            evidence=Evidence.REGISTER,
        ),
    ]
    if renamed:
        terms.append(
            Term(
                term_id=NO_REASON,
                label="No justified reason to refuse approval",
                definition=(
                    "The Ministry's review found no justified reason to refuse. A term of its own "
                    "so the allow rule stays Horn; no clause says that one of the two holds."
                ),
                evidence=Evidence.REGISTER,
            )
        )
    return TermCatalog(statute_id=CS, terms=terms)


def cs108_rules(rules: list[RulePremise]) -> RuleSet:
    return RuleSet(
        statute_id=CS,
        allow_outcome_id=APPROVED,
        deny_outcome_id=REFUSED,
        outcomes=[
            OutcomeDef(outcome_id=APPROVED, label="The Ministry approves the composition"),
            OutcomeDef(outcome_id=REFUSED, label="The Ministry refuses to approve the composition"),
        ],
        rules=rules,
    )


CS108_REGISTERS = {
    SUBMITTED: "mof_document_register",
    REASON: "mof_review_record",
    NO_REASON: "mof_review_record",
}


def cs108_scenarios(renamed: bool = False) -> list[Scenario]:
    def review(found: bool) -> dict[str, bool]:
        return {REASON: found, NO_REASON: not found} if renamed else {REASON: found}

    review_terms = (REASON, NO_REASON) if renamed else (REASON,)
    scenarios = [
        Scenario(
            "allow_review_found_no_reason",
            "Submitted; the review found the composition consistent with § 7 and no other reason to refuse.",
            "ALLOW",
            facts={SUBMITTED: True, **review(False)},
        ),
        Scenario(
            "deny_review_found_reason",
            "Submitted; the review found posts that exercise official authority under § 7 (3) "
            "staffed as employee jobs (§ 7 (4)): a justified reason to refuse.",
            "DENY",
            facts={SUBMITTED: True, **review(True)},
        ),
        Scenario(
            "need_review_not_recorded",
            "Submitted; the review record holds no finding yet (the two months are running).",
            "NEED_MORE_INFO",
            facts={SUBMITTED: True},
            covered=review_terms,
        ),
        Scenario(
            "deny_not_submitted",
            "The document register holds no submission from this authority; there is nothing to approve.",
            "DENY",
            facts={SUBMITTED: False},
            covered=review_terms,
        ),
        Scenario(
            "need_claimed_submission_register_silent",
            "The authority states it submitted; the document register covers submissions but has no "
            "record of this one; the review record shows no reason to refuse.",
            "NEED_MORE_INFO",
            claims={SUBMITTED: True},
            facts=review(False),
            covered=(SUBMITTED, *review_terms),
        ),
    ]
    if renamed:
        scenarios.append(
            Scenario(
                "allow_review_records_reason_field_only",
                "As the first scenario, but the review record answers only 'justified reason "
                "found: no', and nothing fills the renamed term.",
                "ALLOW",
                facts={SUBMITTED: True, REASON: False},
                covered=review_terms,
            )
        )
    return scenarios


def asserted(sc: Scenario) -> Scenario:
    """The same values as decision-grade claims, with no register present."""
    return Scenario(
        sc.scenario_id,
        sc.story + " Values asserted; no register present.",
        sc.gold,
        claims={**sc.facts, **sc.claims},
    )


# --- Public Information Act §§ 18 (1), 23 ----------------------------------------------------

PIA = "public_information_act"
REGISTERED = "request_registered"
MANDATORY = "mandatory_refusal_ground"
PERMISSIVE = "permissive_refusal_ground"
RELEASED = "information_released"
REQUEST_REFUSED = "request_refused"


def pia_case() -> Case:
    catalog = TermCatalog(
        statute_id=PIA,
        terms=[
            Term(
                term_id=REGISTERED,
                label="Request for information registered",
                definition="The holder registered the request; the terms run from the next working day (§ 18 (3)).",
                evidence=Evidence.REGISTER,
            ),
            Term(
                term_id=MANDATORY,
                label="A § 23 (1) refusal ground applies",
                definition=(
                    "E.g. an access restriction applies to the requested information and the "
                    "requester has no right of access (§ 23 (1) 1)). The holder shall refuse."
                ),
                evidence=Evidence.REGISTER,
            ),
            Term(
                term_id=PERMISSIVE,
                label="A § 23 (2) refusal ground applies",
                definition=(
                    "E.g. the information was already released to the requester, who does not "
                    "justify a second release (§ 23 (2) 1)). The holder may refuse."
                ),
                evidence=Evidence.REGISTER,
            ),
        ],
    )
    rules = RuleSet(
        statute_id=PIA,
        allow_outcome_id=RELEASED,
        deny_outcome_id=REQUEST_REFUSED,
        outcomes=[
            OutcomeDef(outcome_id=RELEASED, label="The request is complied with (§ 18 (1))"),
            OutcomeDef(outcome_id=REQUEST_REFUSED, label="The request is refused (§ 23)"),
        ],
        rules=[
            RulePremise(
                premise_id="deny_mandatory_ground",
                rule_kind=RuleKind.DENY_IF_ALL,
                label="A holder of information shall refuse on a § 23 (1) ground.",
                when_term_ids=[REGISTERED, MANDATORY],
                target_outcome_id=REQUEST_REFUSED,
            )
        ],
    )
    clauses = (
        ("~" + REGISTERED, RELEASED, REQUEST_REFUSED),  # § 18 (1) with § 23 as its exceptions
        ("~" + REQUEST_REFUSED, MANDATORY, PERMISSIVE),  # a refusal needs a § 23 ground
        ("~" + RELEASED, "~" + REQUEST_REFUSED),
    )
    registers = {term: "holder_document_register" for term in (REGISTERED, MANDATORY, PERMISSIVE)}
    scenarios = [
        Scenario(
            "allow_no_ground",
            "A journalist asks a ministry for a contract it holds; no access restriction is "
            "recorded and the contract was never released to this person.",
            "ALLOW",
            facts={REGISTERED: True, MANDATORY: False, PERMISSIVE: False},
        ),
        Scenario(
            "deny_restricted_no_access_right",
            "The document is marked for internal use and the requester has no right of access.",
            "DENY",
            facts={REGISTERED: True, MANDATORY: True, PERMISSIVE: False},
        ),
        Scenario(
            "discretion_already_released",
            "The same document was released to the same person last month and the new request "
            "gives no reason for a second release. The holder may refuse and may comply.",
            "DISCRETION",
            facts={REGISTERED: True, MANDATORY: False, PERMISSIVE: True},
        ),
        Scenario(
            "need_grounds_not_checked",
            "The request is registered; the register answers both grounds but holds no value "
            "for either yet.",
            "NEED_MORE_INFO",
            facts={REGISTERED: True},
            covered=(MANDATORY, PERMISSIVE),
        ),
    ]
    return Case(
        "pia_request",
        "Public Information Act §§ 18 (1), 23: comply unless refused; shall refuse on (1), may refuse on (2)",
        "statutory reading; act in the corpus, outside the six suite acts",
        catalog,
        rules,
        clauses,
        registers,
        scenarios,
    )


def cases() -> list[Case]:
    c1 = ("~" + SUBMITTED, APPROVED, REFUSED)  # (C1) s -> a v n
    c2 = ("~" + APPROVED, "~" + REFUSED)  # (C2) not (a and n)
    c3 = ("~" + REFUSED, REASON)  # (C3) n -> j
    p2 = ("~" + SUBMITTED, REASON, APPROVED)  # s and not j -> a
    deny_reason = RulePremise(
        premise_id="deny_reason_found",
        rule_kind=RuleKind.DENY_IF_ALL,
        label="Refuse when the review found a justified reason (§ 108 (3)).",
        when_term_ids=[SUBMITTED, REASON],
        target_outcome_id=REFUSED,
    )
    manuscript = cs108_scenarios()
    return [
        Case(
            "cs108_manuscript",
            "Civil Service Act § 108 (3) as in article.tex Table 1: (C1) s -> a v n, (C2) not(a and n), (C3) n -> j",
            "statutory text; every clause raw (no rule kind states C1, C2 or C3)",
            cs108_catalog(),
            cs108_rules([]),
            (c1, c2, c3),
            CS108_REGISTERS,
            manuscript,
        ),
        Case(
            "cs108_manuscript_asserted",
            "The same theory, the same values asserted with no register present",
            "statutory text; isolates the entailment test from the register lookup",
            cs108_catalog(),
            cs108_rules([]),
            (c1, c2, c3),
            CS108_REGISTERS,
            [asserted(sc) for sc in manuscript if not sc.claims],
        ),
        Case(
            "cs108_review_first",
            "§ 108 (3) read review-first (refuse if a justified reason is found, approve if not): "
            "s and j -> n (schema rule); s and not j -> a, not(a and n) (raw)",
            "statutory reading; one Horn rule in the schema, the non-Horn clause raw",
            cs108_catalog(),
            cs108_rules([deny_reason]),
            (p2, c2),
            CS108_REGISTERS,
            cs108_scenarios(),
        ),
        Case(
            "cs108_horn_renamed",
            "§ 108 (3) in the current schema: s and k -> a, s and j -> n, j -> not k (k = no justified reason)",
            "control: current schema only, no raw clause; the dropped clause is j v k",
            cs108_catalog(renamed=True),
            cs108_rules(
                [
                    RulePremise(
                        premise_id="allow_no_reason",
                        rule_kind=RuleKind.ALLOW_IF_ALL,
                        label="Approve when the review found no justified reason.",
                        when_term_ids=[SUBMITTED, NO_REASON],
                        target_outcome_id=APPROVED,
                    ),
                    deny_reason,
                    RulePremise(
                        premise_id="reason_excludes_no_reason",
                        rule_kind=RuleKind.SET_FALSE_IF_ALL,
                        label="A found reason rules out the no-reason finding.",
                        when_term_ids=[REASON],
                        target_term_id=NO_REASON,
                    ),
                ]
            ),
            (),
            CS108_REGISTERS,
            cs108_scenarios(renamed=True),
        ),
        pia_case(),
    ]


def verdict(gold: str, scored: str) -> str:
    if gold == "DISCRETION":
        return "both lawful"
    return "yes" if gold == scored else "no"


def main() -> int:
    pins = pin()
    solver = get_solver("z3")
    rows = []
    for case in cases():
        for sc in case.scenarios:
            with raw_clauses(case.clauses):
                out = solver.solve(case.catalog, case.rules, claim_set(sc), fact_set(case, sc))
            rows.append(
                {
                    "case_id": case.case_id,
                    "scenario_id": sc.scenario_id,
                    "gold": sc.gold,
                    "state": out.state.value,
                    "scored_as": out.scored_as.value,
                    "matches_gold": verdict(sc.gold, out.scored_as.value),
                    "route": route(out.note),
                    "missing_terms": [f"{m.term_id} ({m.reason.value})" for m in out.missing_terms],
                    "fired_rules": [f.premise_id for f in out.fired_rules],
                    "valuation": out.valuation,
                    "claims": sc.claims,
                    "facts": sc.facts,
                    "covered": sorted(set(sc.covered) | set(sc.facts)),
                    "note": out.note,
                    "story": sc.story,
                }
            )

    results = HERE / "results"
    results.mkdir(exist_ok=True)
    with (results / "outcomes.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    lines = [
        "# Non-Horn smoke — outcomes",
        "",
        "Generated by `run.py`; do not hand-edit.",
        "",
        f"- statute-decider HEAD `{pins['head']}`",
        *(f"- `{path}` blob `{blob}` (= HEAD)" for path, blob in pins["blobs"].items()),
        f"- Python {platform.python_version()}, z3 {z3.get_version_string()}",
        "- `route`: the Step 4 branch that produced the state (entailed / warrant / missing set / default / inconsistent)",
        "",
    ]
    for case in cases():
        lines += [f"## `{case.case_id}`", "", case.title, "", f"Kind: {case.kind}.", ""]
        if case.clauses:
            lines.append("Raw clauses: " + "; ".join(" v ".join(c) for c in case.clauses) + ".")
            lines.append("")
        lines += [
            "| scenario | gold | Step 4 state | scored | matches gold | route | missing | fired |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for row in (r for r in rows if r["case_id"] == case.case_id):
            lines.append(
                f"| `{row['scenario_id']}` | {row['gold']} | {row['state']} | {row['scored_as']} | "
                f"{row['matches_gold']} | {row['route']} | {', '.join(row['missing_terms']) or '—'} | "
                f"{', '.join(row['fired_rules']) or '—'} |"
            )
        lines.append("")
    (results / "summary.md").write_text("\n".join(lines), encoding="utf-8")

    for row in rows:
        print(
            f"{row['case_id']:<28} {row['scenario_id']:<42} gold {row['gold']:<15} "
            f"-> {row['state']:<19} {row['route']:<12} {row['matches_gold']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
