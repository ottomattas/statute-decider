# Teaching example: driving licence renewal

One familiar public service, worked end to end from the **real law text**
to a machine-decidable package. Use it on a whiteboard, as slides
(`side-by-side.svg`), and as the reference shape for student field work.

The law is real and you can check every claim yourself: Road Traffic Act,
[official English translation](https://www.riigiteataja.ee/en/akt/527072026001)
(the legally binding Estonian consolidated text is
[RT I, 11.07.2026, 44](https://www.riigiteataja.ee/et/akt/111072026044)).
Every quote in this pack is verbatim from the official translation.

## The workflow this pack demonstrates

1. **Talk to the service owner.** An official or service owner explains the
   service, names the registers, and points to the law.
2. **Read the law and find your provisions.** The act runs to hundreds of
   sections; this service needs eight paragraphs. Open
   `data/statutes/driving_licence_renewal/road_traffic_act_en_marked.txt`
   — the full act with exactly those paragraphs marked (the official PDFs
   sit next to it for page-level highlighting).
3. **Build the term catalogue** from the marked provisions
   (`term-catalogue-guide.md`, three steps).
4. **Write the human-readable service description**
   (`data/services/renew_driving_licence/service-description.md`) — plain
   language, publishable on a website.
5. **Translate it into the machine-readable contract**
   (`data/services/renew_driving_licence/service.yaml`) — rich enough to be
   the seed for every downstream artifact: terms, rules, register schemas,
   field mappings, scenarios, oracle outcomes.
6. **Author the scenarios and run them.** `run_demo.py` executes the three
   scenarios on the real solver pipeline and checks them against the oracle.

## The story in one minute

A person writes to the Transport Administration: *"I want to renew my
driving licence, I've paid the fee."* The law (§ 98 (2), § 101 (1),
§ 96 (9), § 98 (3)) makes the decision depend on four facts, and it also
says **who may vouch for each fact**:

- the **application** — the person's own word suffices;
- the **medical certificate** — must come via the health information
  system (the law names it, § 101 (8));
- the **state fee** — must show in payment data;
- the **suspension of the right to drive** — established by the motor
  register (§ 96 (7)), and it blocks the licence outright (§ 98 (3)).

What the person merely **claims** is *asserted*; what a register confirms
is *warranted*. The solver applies the rules and refuses to let
unwarranted information decide an outcome — the warrant principle.

## Three scenarios, one per outcome

| Scenario | What happens | Outcome |
|---|---|---|
| `renewal_allow` | Fee claim verified by the payment ledger, medical certificate confirmed | **ALLOW** |
| `renewal_deny_ban` | Applicant admits the suspension in the request; motor register confirms (§ 98 (3)) | **DENY** |
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
full act, English (text) .. data/statutes/driving_licence_renewal/road_traffic_act_en_full.txt
full act, Estonian (text) . data/statutes/driving_licence_renewal/road_traffic_act_et_full.txt
full act, marked .......... data/statutes/driving_licence_renewal/road_traffic_act_en_marked.txt
official PDFs ............. road_traffic_act_en.pdf / road_traffic_act_et.pdf (download from Riigi Teataja, see below)
verbatim excerpts ......... data/statutes/driving_licence_renewal/statute.txt (+ terms + rules in oracle/)
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

### Official PDFs

Riigi Teataja serves downloads only to a real browser, so fetch the two
PDFs manually and drop them into
`data/statutes/driving_licence_renewal/` as `road_traffic_act_en.pdf` and
`road_traffic_act_et.pdf`:

- English translation: <https://www.riigiteataja.ee/en/eli/527072026001>
  (use the *Download* link on the page)
- Estonian consolidated text: <https://www.riigiteataja.ee/akt/111072026044>
  (use the *Laadi alla* link on the page)

For the classroom, extract the pages containing § 96–98 and § 101 and
highlight the marked provisions — `road_traffic_act_en_marked.txt` tells
you exactly which paragraphs.

## From one seed file to all artifacts

`service.yaml` is deliberately rich so that everything else derives from
it. The derivation map:

| `service.yaml` block | becomes |
|---|---|
| `legal_mapping.conditions[]` (term, verbatim quote, evidence, register, field) | term catalogue `text_term.json` with anchors |
| `legal_mapping.rules[]` + `outcomes[]` | decision rules `term_rule.json` |
| `registers[]` (owner, warrant, fields, failure modes) | register `schema.yaml` + `record_term.json` |
| `scenario_seeds[]` (request, expected outcome, reason) | scenario YAMLs, example requests, oracle outcomes |
| `actions[]`, `audit`, `service_level`, `escalation` | service runtime layers (future work) |

If a student's `service.yaml` fills those blocks completely, producing the
machine artifacts is mechanical — which is the point.

## The student assignment

Go to a governmental office (or its public documentation) and pick **one
concrete service**. Then walk the six workflow steps above for your
service:

1. **Interview the professionals.** They know which register holds what,
   which conditions are checked, and where the law lives. For every
   register: who owns it, is its answer authoritative or merely trusted,
   and what does failure look like (empty record? system down?).
2. **Find the law on [riigiteataja.ee](https://www.riigiteataja.ee)** and
   copy out, verbatim, the provisions that state the conditions and
   consequences (our `statute.txt` shows the format; mark them in the full
   text like our `road_traffic_act_en_marked.txt`).
3. **Build the term catalogue** with the 3-step method in
   `term-catalogue-guide.md`: highlight → name the yes/no terms with a
   warranting source → write the allow/deny rules, each anchored to a real
   section and subsection.
4. **Write the human-readable service page** (our
   `service-description.md` is the template): what the service is, who it
   is for, what is needed, how the decision is made, cost and time, legal
   basis. Plain language, publishable on a website.
5. **Translate it to the machine-readable contract** (`service.yaml`),
   filling the translation table at the bottom of the page as you go —
   every sentence must land in a field, every field must come from a
   sentence. Fill all the seed blocks: conditions with quotes, registers
   with owners and warrants, scenario seeds.
6. **Author scenarios with oracle outcomes** — at least three realistic
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

- [ ] Law provisions copied verbatim from Riigi Teataja, with section and
      subsection visible (no paraphrases presented as law).
- [ ] Every machine-checkable condition names a `term_id` and quotes its
      law sentence.
- [ ] Every register-evidence term names the register that warrants it,
      its owner, and its failure modes.
- [ ] Rules are boolean and complete: reading only terms + rules, a third
      person reaches the same outcome you did.
- [ ] The human-readable page and `service.yaml` translate into each other
      with nothing left over (use the translation table).
- [ ] Three or more scenario seeds, at least one per outcome class, each
      with the gold outcome and the reason.
- [ ] No invented registers or paragraphs — if the officials could not name
      a source, record that as an open question instead.
