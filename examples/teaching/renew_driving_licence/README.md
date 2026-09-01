# Teaching example: driving licence renewal (juhiloa uuendamine)

One familiar public service, worked end to end from the **real law text**
to a machine-decidable package. Use it on a whiteboard, as slides
(`side-by-side.svg`), and as the reference shape for student field work.

The law is real and you can check every claim yourself: Liiklusseadus,
consolidated text [RT I, 11.07.2026, 44](https://www.riigiteataja.ee/et/akt/111072026044)
(official English translation: [Road Traffic Act](https://www.riigiteataja.ee/en/akt/527072026001)).
Every quote in this pack is verbatim from those texts.

## The story in one minute

A person writes to the Transport Administration: *"I want to renew my
driving licence, I've paid the fee."* The law (§ 98 lg 2, § 101 lg 1,
§ 96 lg 9, § 98 lg 3) makes the decision depend on four facts, and it also
says **who may vouch for each fact**:

- the **application** — the person's own word suffices;
- the **medical certificate** — must come via the health information
  system (the law names it, § 101 lg 8);
- the **state fee** — must show in payment data;
- the **suspension of the right to drive** — established by the motor
  register (§ 96 lg 7), and it blocks the licence outright (§ 98 lg 3).

What the person merely **claims** is *asserted*; what a register confirms
is *warranted*. The solver applies the rules and refuses to let
unwarranted information decide an outcome — the warrant principle.

## Read in this order

1. **`data/statutes/driving_licence_renewal/statute.txt`** — the verbatim
   law excerpts (ET + official EN), the ground truth everything else maps to.
2. **`term-catalogue-guide.md`** — the 3-step method: highlight the
   conditions in the law → turn each highlight into a yes/no term with a
   warranting source → write the allow/deny rules. This is the skill the
   students practise.
3. **`data/services/renew_driving_licence/service-description.md`** — the
   human-readable service page (ET + EN, publishable on a website), written
   *first*, with the translation table showing how each sentence became a
   machine-readable field.
4. **`data/services/renew_driving_licence/service.yaml`** — the
   machine-readable Semantic Service Contract the page translates into; its
   `legal_mapping` block ties conditions → terms → registers.
5. **`side-by-side.svg`** — the one-slide overview of all three artefacts.

## Three scenarios, one per outcome

| Scenario | What happens | Outcome |
|---|---|---|
| `renewal_allow` | Fee claim verified by the payment ledger, medical certificate confirmed | **ALLOW** |
| `renewal_deny_ban` | Applicant admits the suspension in the request; motor register confirms (§ 98 lg 3) | **DENY** |
| `renewal_need_fee` | Applicant silent about the fee, ledger has no payment on record | **NEED_REGISTER_INFO** |

Run them live on the real pipeline (no LLM, no cost), from the repo root:

```bash
.venv/bin/python examples/teaching/renew_driving_licence/run_demo.py
```

Each run prints the outcome, the fired rule with its statutory anchor, and
the rendered justification trace — and checks the result against the
oracle files.

## What is in this folder

```
verbatim law excerpts ..... data/statutes/driving_licence_renewal/  (statute.txt + terms + rules)
term-catalogue method ..... term-catalogue-guide.md
human service page ........ data/services/renew_driving_licence/service-description.md
machine service contract .. data/services/renew_driving_licence/service.yaml
registers + mappings ...... data/registers/driving_licence_renewal__*/
case, scenarios, oracle ... data/cases/driving_licence_renewal/
slide visual .............. side-by-side.svg
runnable demo ............. run_demo.py
```

The `data/` tree uses exactly the same layout and schemas as the main
benchmark (`data/` at the repo root), so everything transfers 1:1.

## The student assignment

Go to a governmental office (or its public documentation) and pick **one
concrete service**. Interview the professionals: they know which register
holds what, which conditions are checked, and where the law lives. Then
produce this same package for your service, **in this order**:

1. **Find the law.** Locate the governing act on
   [riigiteataja.ee](https://www.riigiteataja.ee) and copy out, verbatim,
   the provisions that state the conditions and consequences of your
   service (our `statute.txt` shows the format).
2. **Build the term catalogue** with the 3-step method in
   `term-catalogue-guide.md`: highlight → name the yes/no terms → write the
   allow/deny rules, each anchored to a real § and lg. For every
   register-evidence term, ask the officials which register warrants it and
   whether its answer is authoritative or trust-only.
3. **Write the human-readable service page** (our
   `service-description.md` is the template): what the service is, who it
   is for, what is needed, how the decision is made, cost and time, legal
   basis. Plain language, publishable on a website.
4. **Translate it to the machine-readable contract** (`service.yaml`),
   filling the translation table at the bottom of the page as you go —
   every sentence must land in a field, every field must come from a
   sentence.
5. **Author scenarios with oracle outcomes** — at least three realistic
   requests, one per outcome class (allow / deny / need-more-info), each
   with the correct outcome and its reason. This is oracle-grade data: a
   later system run must be able to be graded against it.

### Agent-ready maturity ladder (where does your service sit today?)

- **L0 Human only** — web page and free text.
- **L1 Discoverable** — machine-readable metadata and a semantic purpose.
- **L2 Understandable** — inputs, eligibility, preconditions, outcomes are machine-readable.
- **L3 Executable** — the actions can be performed via an API.
- **L4 Delegatable** — actions carry machine-readable authority, limits, and legal effect.
- **L5 Agent-ready** — an agent can discover, plan, compose, execute, and every step is auditable.

Your deliverable lifts a service from L0/L1 to L2 on paper — and maps the
path to L4/L5. Note the pairing rule you just practised: at every level the
machine-readable artifact keeps a human-readable counterpart, so the person
an agent acts for can always understand what is being done on their behalf.

### Checklist before you hand it in

- [ ] Law provisions copied verbatim from Riigi Teataja, with the § and lg
      visible (no paraphrases presented as law).
- [ ] Every machine-checkable condition names a `term_id`.
- [ ] Every term is anchored to a real § (quote it).
- [ ] Every register-evidence term names the register that warrants it.
- [ ] Rules are boolean and complete: reading only terms + rules, a third
      person reaches the same outcome you did.
- [ ] The human-readable page and `service.yaml` translate into each other
      with nothing left over (use the translation table).
- [ ] Three or more scenarios, at least one per outcome class, each with
      the gold outcome and the reason.
- [ ] No invented registers or paragraphs — if the officials could not name
      a source, record that as an open question instead.
