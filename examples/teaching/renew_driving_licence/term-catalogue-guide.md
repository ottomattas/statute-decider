# From law text to a term catalogue — a 3-step guide

You do not need to be a programmer for this. You need to read a law the way
an official reads it: *what exactly has to be true before the state says
yes?* The three steps below turn that reading into a **term catalogue** —
the shared vocabulary that the service description, the registers, and the
decision rules all speak.

Worked example throughout: driving licence renewal, Road Traffic Act
([official English translation](https://www.riigiteataja.ee/en/akt/527072026001);
the legally binding Estonian text is
[RT I, 11.07.2026, 44](https://www.riigiteataja.ee/et/akt/111072026044)).
Open `data/statutes/driving_licence_renewal/road_traffic_act_en_marked.txt`
to see where these few provisions sit inside the full act.

---

## Step 1 — Highlight the conditions in the law text

Read the provisions that govern your service and mark every phrase that is
a **condition** (something that must be true or false) or a **consequence**
(what happens when the conditions hold). Ignore everything else — forms,
deadlines for the agency, ministerial regulations.

This is what the highlighting looks like on the real text (bold = what we
marked):

> **§ 98 (2).** Provisional driving licences and driving licences are
> issued within ten working days as of the day after which the respective
> test was passed or **an application for replacement of the driving
> licence was submitted**.
>
> **§ 101 (1).** ... Compliance with the medical requirements **is proven
> by a medical certificate** issued by the person who carried out the
> medical examination.
>
> **§ 96 (9).** **A state fee is payable** for issuing or replacing a
> driving licence.
>
> **§ 98 (3).** A provisional driving licence and a driving licences **is
> not issued** to a person ... **whose right to drive has been suspended or
> withdrawn** in accordance with § 125 of this Act ...

Four highlights: three conditions for a yes, one condition that forces a
no. Notice the last one is a consequence too ("is not issued") — deny
conditions usually carry their consequence in the same sentence.

## Step 2 — Turn each highlight into a term

For every highlight, write **one yes/no statement in the present tense**,
give it a short machine name (`snake_case`), and answer the key question:

> **Who can warrant this?** Is the person's own word enough (the law treats
> it as their declaration), or must a register confirm it (the law demands
> proof)? If a register — which one? The law often names it outright:
> § 101 (8) says the certificate is issued "via the health information
> system"; § 96 (7) says the right to drive "is proven based on the data of
> the motor register".

The worked catalogue:

| Highlight | Term (yes/no statement) | `term_id` | Who warrants it? |
|---|---|---|---|
| "an application for replacement ... was submitted" (§ 98 (2)) | The person has submitted a replacement application | `renewal_application_submitted` | **The person** — the request itself |
| "is proven by a medical certificate" (§ 101 (1), (8)) | A valid medical certificate is on record | `health_certificate_valid` | **Register:** health information system |
| "a state fee is payable" (§ 96 (9)) | The state fee has been paid | `state_fee_paid` | **Register:** state treasury payment ledger |
| "right to drive has been suspended or withdrawn" (§ 98 (3)) | The right to drive is suspended or withdrawn | `driving_ban_active` | **Register:** motor register |

Rules of thumb:

- One term = one fact. "Has a valid certificate and paid the fee" is two
  terms, not one.
- Phrase it so *true* has a clear meaning. Prefer "driving_ban_active is
  true" over "no_ban is false" — double negatives breed mistakes.
- If you cannot answer "who warrants this?", that is not a modelling
  failure — it is your best interview question for the officials.

## Step 3 — Write the rules and check them

Combine the terms into decision rules. Two shapes cover almost everything:

```text
ALLOW if ALL of: renewal_application_submitted,
                 health_certificate_valid,
                 state_fee_paid            -> licence_renewed   (§ 98 (2), § 101 (1), § 96 (9))

DENY  if:        driving_ban_active       -> renewal_refused   (§ 98 (3))
```

Then run the completeness check: give only the catalogue and the rules to
someone who has not read the law. For each of these three requests, they
must reach the same answer you do:

1. Everything in order → ALLOW.
2. The person admits their licence is suspended → DENY.
3. The person says nothing about the fee and the ledger shows no payment →
   neither rule can fire → NEED MORE INFO (the honest third answer: the
   decision waits for the missing register value).

If they hesitate anywhere, a term is missing, doubled, or badly phrased.
Fix the catalogue, not the reader.

---

That is the whole method. In this pack, the result of the three steps lives
in machine form at `data/statutes/driving_licence_renewal/oracle/`
(`text_term.json` = step 2, `term_rule.json` = step 3), and
`run_demo.py` executes the check from step 3 on a real solver.
