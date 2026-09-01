# Driving licence renewal

> Human-readable service description, publishable on a website. Machine
> counterpart: `service.yaml` in this directory — every sentence on this
> page must be traceable there, and back. When an agent later acts on a
> person's behalf, this page is what the person reads to understand what
> is being done for them.

---

## What is this service?

When your driving licence approaches the end of its validity (ten years
for category B, Road Traffic Act § 97 (7)), you can apply to the Transport
Administration (Transpordiamet) to have it replaced. The new licence is
issued within ten working days of the application (§ 98 (2)).

## Who is it for?

A natural person whose permanent residence is in Estonia (§ 98 (1¹)).

## What do you need?

| Condition | How the state checks it |
|---|---|
| A submitted replacement application | Your request itself (§ 98 (2)) |
| A valid medical certificate | The health information system (§ 101 (1) and (8)) |
| The state fee paid | State treasury payment data (§ 96 (9)) |
| Your right to drive is not suspended or withdrawn | The motor register (§ 98 (3), § 96 (7)) |

Note the difference: only the application itself is something you declare
and the state takes at your word. The other three conditions are checked
against registers — your say-so is not enough, and that is the law's
choice, not a clerk's.

## How is the decision made?

If the application is in, the medical certificate is valid, and the state
fee is paid, the licence is replaced (**ALLOW**). If your right to drive is
suspended or withdrawn, no licence is issued (**DENY**, § 98 (3)). If a
register check comes back empty — for example the payment has not yet
arrived — no decision is made until the missing information exists
(**NEED MORE INFO**).

## Cost and time

- State fee: per the State Fees Act (demo value in this pack: 26 EUR).
- Decision: immediate when all registers answer; otherwise within ten
  working days (§ 98 (2)).

## Legal basis

- Road Traffic Act, official English translation:
  <https://www.riigiteataja.ee/en/akt/527072026001>
- Legally binding Estonian consolidated text (RT I, 11.07.2026, 44):
  <https://www.riigiteataja.ee/et/akt/111072026044>
- Excerpt of the decision-relevant provisions:
  `../../statutes/driving_licence_renewal/statute.txt`; the full act with
  the same provisions highlighted:
  `../../statutes/driving_licence_renewal/road_traffic_act_en_highlighted.pdf`

## If something goes wrong

A refusal names the provision that caused it (e.g. § 98 (3)) and the
register the information came from. If a register is down or the data
conflicts, the case is routed to a human.

---

## How this page becomes the machine-readable file — and everything after it

Each block of this page lands in a `service.yaml` section, and each
`service.yaml` section is the seed for one machine artifact downstream:

| This page says | `service.yaml` carries it as | ... which later generates |
|---|---|---|
| "you can apply ... to have it replaced" | `service.purpose` | service discovery metadata |
| the "What do you need?" table, incl. the law §§ | `legal_mapping.conditions[]` (term, quote, evidence, register, field) | term catalogue (`text_term.json`) with verbatim anchors |
| the three "How is the decision made?" sentences | `legal_mapping.rules[]` + `outcomes[]` | decision rules (`term_rule.json`) |
| "the health information system", "the motor register" ... | `registers[]` (owner, warrant, fields, failure modes) | register schemas (`schema.yaml`) + field-to-term maps (`record_term.json`) |
| the ALLOW / DENY / NEED MORE INFO walk-through | `scenario_seeds[]` (request, expected outcome, reason) | scenarios, example requests, oracle outcomes |
| "Cost and time" | `service_level` | service runtime metadata |
| "If something goes wrong" | `escalation` | routing rules |

Two writing rules follow:

1. **If a sentence cannot be placed in this table**, it is either a missing
   field in the machine-readable file or an empty sentence — fix either way.
2. **If a `service.yaml` field cannot be traced to a sentence here**, the
   page is hiding something from the human — add the sentence.

While interviewing the service owner, make sure this page ends up
answering, for every register-checked condition: *which register, who owns
it, is its answer authoritative or merely trusted, and what does failure
look like* (empty record? system down?). Those are exactly the details the
downstream artifacts need and that no law text will tell you.
