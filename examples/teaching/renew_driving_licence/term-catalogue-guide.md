# From law text to a term catalogue — a 3-step guide

You do not need to be a programmer for this. You need to read a law the way
an official reads it: *what exactly has to be true before the state says
yes?* The three steps below turn that reading into a **term catalogue** —
the shared vocabulary that the service description, the registers, and the
decision rules all speak.

Worked example throughout: driving licence renewal, Liiklusseadus
([ET terviktekst](https://www.riigiteataja.ee/et/akt/111072026044),
[official EN translation](https://www.riigiteataja.ee/en/akt/527072026001)).

---

## Step 1 — Highlight the conditions in the law text

Read the provisions that govern your service and mark every phrase that is
a **condition** (something that must be true or false) or a **consequence**
(what happens when the conditions hold). Ignore everything else — forms,
deadlines for the agency, ministerial regulations.

This is what the highlighting looks like on the real text (bold = what we
marked):

> **LS § 98 lg 2.** Esmane juhiluba ja juhiluba antakse välja kümne
> tööpäeva jooksul sellekohase eksami sooritamisele või **juhiloa
> vahetamise taotluse esitamisele** järgnevast päevast arvates.
>
> **LS § 101 lg 1.** ... Tervisenõuetele vastavust tõendab tervisekontrolli
> teostaja väljastatud **tervisetõend**.
>
> **LS § 96 lg 9.** Juhiloa väljastamise ja vahetamise eest **tuleb tasuda
> riigilõivu**.
>
> **LS § 98 lg 3.** Esmast juhiluba ja juhiluba **ei väljastata** isikule,
> ... **kelle juhtimisõigus on peatatud või** käesoleva seaduse § 125
> kohaselt **ära võetud** ...

Four highlights: three conditions for a yes, one condition that forces a
no. Notice the last one is a consequence too ("ei väljastata") — deny
conditions usually carry their consequence in the same sentence.

## Step 2 — Turn each highlight into a term

For every highlight, write **one yes/no statement in the present tense**,
give it a short machine name (`snake_case`), and answer the key question:

> **Who can warrant this?** Is the person's own word enough (the law treats
> it as their declaration), or must a register confirm it (the law demands
> proof)? If a register — which one? The law often names it outright:
> § 101 lg 8 says the certificate arrives "tervise infosüsteemi
> vahendusel"; § 96 lg 7 says the right to drive is proven "liiklusregistri
> andmete alusel".

The worked catalogue:

| Highlight | Term (yes/no statement) | `term_id` | Who warrants it? |
|---|---|---|---|
| "juhiloa vahetamise taotluse esitamisele" (§ 98 lg 2) | The person has submitted a replacement application | `renewal_application_submitted` | **The person** — the request itself |
| "tervisetõend" (§ 101 lg 1, lg 8) | A valid medical certificate is on record | `health_certificate_valid` | **Register:** tervise infosüsteem |
| "tuleb tasuda riigilõivu" (§ 96 lg 9) | The state fee has been paid | `state_fee_paid` | **Register:** payment ledger (riigikassa) |
| "juhtimisõigus on peatatud või ... ära võetud" (§ 98 lg 3) | The right to drive is suspended or withdrawn | `driving_ban_active` | **Register:** liiklusregister |

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
                 state_fee_paid            -> licence_renewed   (§ 98 lg 2, § 101 lg 1, § 96 lg 9)

DENY  if:        driving_ban_active       -> renewal_refused   (§ 98 lg 3)
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
