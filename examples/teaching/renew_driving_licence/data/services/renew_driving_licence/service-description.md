# Juhiloa uuendamine / Driving licence renewal

> Inimloetav teenusekirjeldus, avaldatav veebilehel. Masinloetav vaste:
> `service.yaml` samas kaustas — iga selle lehe lause peab olema sealt
> leitav, ja vastupidi.
> [Human-readable service description, publishable on a website. Machine
> counterpart: `service.yaml` in this directory — every sentence on this
> page must be traceable there, and back.]

---

## Mis teenus see on? / What is this service?

**ET.** Kui sinu juhiloa kehtivusaeg (B-kategoorial kümme aastat,
Liiklusseadus § 97 lg 7) hakkab läbi saama, saad taotleda Transpordiametilt
juhiloa vahetamist. Uus juhiluba väljastatakse kümne tööpäeva jooksul
taotluse esitamisest (LS § 98 lg 2).

**EN.** When your driving licence approaches the end of its validity (ten
years for category B, Road Traffic Act § 97 (7)), you can apply to the
Transport Administration (Transpordiamet) to have it replaced. The new
licence is issued within ten working days of the application (§ 98 (2)).

## Kellele? / Who is it for?

- Füüsiline isik, kelle alaline elukoht on Eestis (LS § 98 lg 1¹).
- Natural person whose permanent residence is in Estonia (§ 98 (1¹)).

## Mida on vaja? / What do you need?

| Tingimus / Condition | Kust riik seda kontrollib / How the state checks it |
|---|---|
| Esitatud vahetustaotlus / A submitted replacement application | Sinu taotlus ise / your request itself (LS § 98 lg 2) |
| Kehtiv tervisetõend / A valid medical certificate | Tervise infosüsteem / the health information system (LS § 101 lg 1 ja 8) |
| Tasutud riigilõiv / The state fee paid | Riigikassa maksete andmed / state treasury payment data (LS § 96 lg 9) |
| Juhtimisõigus ei ole peatatud ega ära võetud / Your right to drive is not suspended or withdrawn | Liiklusregister / the motor register (LS § 98 lg 3, § 96 lg 7) |

**ET.** Pane tähele: ainult taotluse esitamine on asi, mida sina väidad ja
mida riik usub sinu sõnast. Ülejäänud kolme tingimust kontrollitakse
registritest — sinu kinnitusest ei piisa, ja see on seaduse, mitte
ametniku valik.

**EN.** Note the difference: only the application itself is something you
declare and the state takes at your word. The other three conditions are
checked against registers — your say-so is not enough, and that is the
law's choice, not a clerk's.

## Kuidas otsus sünnib? / How is the decision made?

**ET.** Kui taotlus on esitatud, tervisetõend kehtib ja riigilõiv on
tasutud, juhiluba vahetatakse (LUBATUD). Kui juhtimisõigus on peatatud või
ära võetud, juhiluba ei väljastata (KEELDUTUD, LS § 98 lg 3). Kui mõni
registrikontroll jääb vastuseta — näiteks makse ei ole veel laekunud —
otsust ei tehta enne, kui puuduv teave on olemas (VAJA LISAINFOT).

**EN.** If the application is in, the medical certificate is valid, and the
state fee is paid, the licence is replaced (ALLOW). If your right to drive
is suspended or withdrawn, no licence is issued (DENY, § 98 (3)). If a
register check comes back empty — for example the payment has not yet
arrived — no decision is made until the missing information exists
(NEED MORE INFO).

## Hind ja aeg / Cost and time

- Riigilõiv / state fee: vastavalt riigilõivuseadusele (näidisväärtus
  selles paketis: 26 EUR) / per the State Fees Act (demo value in this
  pack: 26 EUR).
- Otsus / decision: kohe, kui kõik registrid vastavad; muidu kuni 10
  tööpäeva / immediate when all registers answer; otherwise up to 10
  working days (LS § 98 lg 2).

## Õiguslik alus / Legal basis

- Liiklusseadus, terviktekst RT I, 11.07.2026, 44:
  <https://www.riigiteataja.ee/et/akt/111072026044>
- Road Traffic Act, official English translation:
  <https://www.riigiteataja.ee/en/akt/527072026001>
- Väljavõte otsustamiseks vajalikest sätetest / excerpt of the
  decision-relevant provisions: `../../statutes/driving_licence_renewal/statute.txt`

## Kui midagi läheb valesti? / If something goes wrong

**ET.** Kui otsus on keelduv, saad teada, milline säte keeldumise põhjustas
(nt LS § 98 lg 3) ja millisest registrist see teave pärines. Kui register
on maas või andmed on vastuolulised, suunatakse asi inimesele.

**EN.** A refusal names the provision that caused it (e.g. § 98 (3)) and
the register the information came from. If a register is down or the data
conflicts, the case is routed to a human.

---

## Kuidas sellest lehest sai masinloetav fail / How this page became the machine-readable file

| See leht ütleb / This page says | `service.yaml` kannab / carries it as |
|---|---|
| "saad taotleda Transpordiametilt juhiloa vahetamist" | `service.purpose.concept: maintain_driving_entitlement` |
| tabeli rida "Esitatud vahetustaotlus" | `conditions[].term_id: renewal_application_submitted`, `evidence: user` |
| tabeli rida "Kehtiv tervisetõend … tervise infosüsteem" | `term_id: health_certificate_valid`, `register_id: …__health_registry` |
| tabeli rida "Tasutud riigilõiv" | `term_id: state_fee_paid`, `register_id: …__payment_ledger` |
| tabeli rida "Juhtimisõigus ei ole peatatud" | `term_id: driving_ban_active`, `register_id: …__traffic_registry` |
| "Kuidas otsus sünnib" kolm lõiku | `rules:` (allow_renewal, deny_driving_ban) + `outcome_space` |
| "Hind ja aeg" | `service_level` |
| "Kui midagi läheb valesti" | `escalation` |

Kui mõnda lauset ei saa sellesse tabelisse panna, on see kas (a) puuduv
väli masinloetavas failis või (b) sisutühi lause — mõlemal juhul paranda.
[If a sentence cannot be placed in this table, it is either (a) a missing
field in the machine-readable file or (b) an empty sentence — fix either
way.]
