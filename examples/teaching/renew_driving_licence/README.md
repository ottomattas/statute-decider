# Teaching example: driving licence renewal (juhiloa uuendamine)

One very simple public service, worked end to end through the statute-decider
architecture. Use it on a whiteboard, as slides (`side-by-side.svg`), and as
the reference shape for student field work.

## The story in one minute

A person writes to the Transport Administration: *"I want to renew my driving
licence, I've paid the fee."* To decide, the state needs three kinds of
knowledge, each living in a different artefact:

1. **Service description** (`data/services/renew_driving_licence/service.yaml`)
   — what the service is, who provides it, which conditions it checks, what an
   agent may do on the person's behalf, and what gets audited.
2. **Statute** (`data/statutes/driving_licence_renewal/`) — the legal text,
   its vocabulary of *terms* (application submitted, health certificate valid,
   fee paid, driving ban active), and the hand-authored *rules* over them.
3. **Registers** (`data/registers/driving_licence_renewal__*/`) — who can
   *warrant* each term: the health information system, the payment ledger, the
   traffic register.

What the person **claims** is only *asserted*; what a register confirms is
*warranted*. The solver applies the rules and refuses to let unwarranted
information decide an outcome — that is the warrant principle.

## Three scenarios, one per outcome

| Scenario | What happens | Outcome |
|---|---|---|
| `renewal_allow` | Fee claim verified by the payment ledger, health certificate confirmed | **ALLOW** |
| `renewal_deny_ban` | Applicant admits the driving ban in the request itself; register confirms | **DENY** |
| `renewal_need_fee` | Applicant silent about the fee, ledger has no payment on record | **NEED_REGISTER_INFO** |

Run them live on the real pipeline (no LLM, no cost), from the repo root:

```bash
.venv/bin/python examples/teaching/renew_driving_licence/run_demo.py
```

Each run prints the outcome, the fired rule with its statutory anchor, and the
rendered justification trace — and checks the result against the oracle files.

## What is in this folder

```
service.yaml lives in ..... data/services/renew_driving_licence/
statute + terms + rules ... data/statutes/driving_licence_renewal/
registers + mappings ...... data/registers/driving_licence_renewal__*/
case, scenarios, oracle ... data/cases/driving_licence_renewal/
slide visual .............. side-by-side.svg
runnable demo ............. run_demo.py
```

The `data/` tree uses exactly the same layout and schemas as the main
benchmark (`data/` at the repo root), so everything you learn here transfers
1:1. The statute text is a **simplified paraphrase** of Liiklusseadus for
teaching; real work must anchor to the official Riigi Teataja consolidated
text, paragraph and subsection precise.

## The student assignment

Go to a governmental office (or its public documentation) and pick **one
concrete service**. Interview the professionals: they know which register
holds what, which conditions are checked, and where the law lives. Then
produce this same package for your service:

1. **Service description** — copy `service.yaml` as a template. Fill every
   layer: discovery, purpose, eligibility, machine-checkable conditions,
   required data, process, agent actions with authority limits, audit.
2. **Statute mapping** — find the governing act in Riigi Teataja. Extract the
   boolean *terms* the service actually checks and write the allow/deny
   *rules*, each anchored to a real § and lg.
3. **Register map** — for each register-evidence term, name the register that
   can warrant it (ask the officials — they know), and whether its answer is
   authoritative or trust-only.
4. **Scenarios with oracle outcomes** — author at least three realistic
   requests, one per outcome class (allow / deny / need-more-info), and state
   the correct outcome with its reason. This is oracle-grade data: a later
   system run must be able to be graded against it.

### Agent-ready maturity ladder (where does your service sit today?)

- **L0 Human only** — web page and free text.
- **L1 Discoverable** — machine-readable metadata and a semantic purpose.
- **L2 Understandable** — inputs, eligibility, preconditions, outcomes are machine-readable.
- **L3 Executable** — the actions can be performed via an API.
- **L4 Delegatable** — actions carry machine-readable authority, limits, and legal effect.
- **L5 Agent-ready** — an agent can discover, plan, compose, execute, and every step is auditable.

Your deliverable lifts a service from L0/L1 to L2 on paper — and maps the path
to L4/L5.

### Checklist before you hand it in

- [ ] Every machine-checkable condition names a `term_id`.
- [ ] Every term is anchored to a Riigi Teataja § (quote it).
- [ ] Every register-evidence term names the register that warrants it.
- [ ] Rules are boolean and complete: reading only terms + rules, a third
      person reaches the same outcome you did.
- [ ] Three or more scenarios, at least one per outcome class, each with the
      gold outcome and the reason.
- [ ] No invented registers or paragraphs — if the officials could not name a
      source, record that as an open question instead.
