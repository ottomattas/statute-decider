# 20261003-nonhorn-smoke

What does the committed Step 4 (`Z3Solver.solve`, z3 backend at HEAD) do when the statute's faithful reading is not Horn? A smoke on oracle inputs, solver only, no LLM. It runs from its own script; there is no `experiment.yaml` and no `results/rows.jsonl`, so `sd run` and the fingerprint tools skip the folder.

```bash
.venv/bin/python experiments/20261003-nonhorn-smoke/run.py
```

Writes `results/outcomes.jsonl` (one row per scenario, with valuation, missing terms, fired rules and the solver's note) and `results/summary.md` (tables). The script stops if `z3_backend.py`, `core/premises.py` or `core/enums.py` differs from HEAD.

## Raw-clause path

No rule kind states (C1), (C2), (C3) or s ∧ ¬j → a below: none has two positive literals, none derives a positive term, none takes a negated condition, and none constrains the two outcomes against each other. Those clauses enter the theory through a raw-clause path: for each solve, `z3_backend._Theory` is swapped for a subclass whose solver holds the compiled rules plus the raw clauses. That is an input path, not a change to the procedure: Stage 1, Stage 2, both consistency tests, entailment, the warrant check, the missing set and default DENY run as committed.

## Cases

No synthetic cell: every case is official text from the corpus.

| case | source | kind |
|---|---|---|
| `cs108_manuscript` | Civil Service Act § 108 (3); the engine manuscript's encoding (C1) s → a ∨ n, (C2) ¬(a ∧ n), (C3) n → j | statutory text; all three clauses raw |
| `cs108_manuscript_asserted` | the same theory, values asserted with no register present | isolates the entailment test from the register lookup |
| `cs108_review_first` | § 108 (3) read review-first: s ∧ j → n (a `deny_if_all` rule), s ∧ ¬j → a and (C2) raw | statutory reading |
| `cs108_horn_renamed` | § 108 (3) in the current schema: "no justified reason" as its own term k; s ∧ k → a, s ∧ j → n, j → ¬k | control, no raw clause; the clause it drops is j ∨ k |
| `pia_request` | Public Information Act §§ 18 (1), 23: comply unless refused; shall refuse on a § 23 (1) ground; may refuse on a § 23 (2) ground | statutory reading; the act is in the corpus but outside the six suite acts |

s: the staff composition and salary guide were submitted (§ 108 (1)); a: the Ministry of Finance approves; n: it refuses; j: its review found a justified reason to refuse. The two-month deadline is not encoded. Scenario stories and gold labels are in `run.py`.

## What the run shows

- Entailment handles the disjunction. Where the clauses and the values force an outcome, Z3 finds it: (C1) with (C3) and ¬j entails a; s ∧ ¬j → a with ¬j entails a.
- Stage 2 asks the registers only about antecedents of schema rules. A term that occurs only in raw clauses is never looked up: in `cs108_manuscript` no register is read and every scenario ends in default DENY; in `pia_request` the § 23 (2) ground is never read.
- The missing set is the open antecedents of `allow_if_all` rules. A disjunctive head has none, so the scenario that should be NEED_MORE_INFO (submitted, review not recorded; grounds not yet checked) ends in default DENY.
- The warrant check reads the same rules. An ALLOW entailed through a raw clause is never checked: in `cs108_review_first` it rests on a claimed submission the document register does not show, and stays final.
- The Horn-renamed control decides every § 108 (3) scenario that values both j and k, and stalls (NEED_REGISTER_INFO) when the record values only j. The dropped clause becomes an obligation on the data.
- A § 23 (2) ground makes both outcomes lawful. Default DENY picks refusal, by the same branch that refuses when no ground has been checked.
