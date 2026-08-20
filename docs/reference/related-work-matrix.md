# Related-Work Matrix: Four-Step Pipeline vs. Surveyed Systems

This document maps surveyed systems and papers against the four steps of the
current `framework` CLI pipeline. The four steps are:

- **Step 1 — Intent:** translate user natural-language text into structured claim
  assignments.
- **Step 2 — Domain:** translate statutory or regulatory text into a machine-readable
  rule set.
- **Step 3 — Reasoner:** evaluate the claim assignments against the rule set and
  produce a verdict with missing-information states.
- **Step 4 — Trace / explanation:** produce an auditable, human-readable account of
  how the verdict was reached.

Bibliography keys for the current manuscript live in the paper repository
`MattasJarvTammet-2026-NeSy-Statute-Logic` (`bibliography.bib`).

---

## Matrix

| System / Paper | Step 1 — Intent | Step 2 — Domain | Step 3 — Reasoner | Step 4 — Trace | Domain locked? | Notable limitations |
|---|---|---|---|---|---|---|
| `sergot1986british` — Sergot et al. (1986), *British Nationality Act as a Logic Program* | Not automated; case facts supplied manually by a legal professional | Hand-encoded by lawyers into Prolog clauses | Prolog interpreter; pauses on unbound variables (Query-the-User) | Prolog proof tree; direct ancestor of `NEED_USER_INFO` | Yes — British Nationality Act | No NL extraction; encoding requires legal-AI expertise; no DB vs. user distinction |
| `mccarty1977taxman` — McCarty (1977), *TAXMAN* | Not automated; case record entered manually | Hand-crafted concept hierarchies | Analogical matching; forward inference on tax concepts | Implicit; verdict with concept trace | Yes — US corporate tax law | No NL extraction; analogical engine not symbolic decision procedure; fixed ontology |
| `merigoux2021catala` — Merigoux et al. (2021), *Catala* | Not present — Catala compiles statute, not user utterance | Lawyer + programmer write literate Catala source, compiled to OCaml / Z3 | OCaml runtime or Z3 back-end | Compilation errors surface statute conflicts; runtime trace for executed code | No — designed for any jurisdiction, but authoring requires programmer | No automated extraction; LLM not in the loop; DSL authoring cost; runtime availability |
| `governatori2026defeasible` — Governatori et al. (2026), *s(LAW)* | Not automated; structured fact base provided | Statutory text formalized as ASP / defeasible rules manually or semi-automatically | s(CASP) — ASP with constraint answer sets; supports defaults and exceptions | Justification trees; explicit defeasibility traces | No, but examples are public-administration statutes | No LLM extraction step; structured fact input required; abduction not interactive |
| `pan2023logic` — Pan et al. (2023), *Logic-LM* | LLM translates NL problem into symbolic specification | Not applicable — general reasoning, not statutory text | External symbolic solver (Z3, Pyke, Prolog) selected per task | Execution feedback loop; self-refinement | No — general logical reasoning benchmarks | FOL / SMT back-end; no domain extraction step; no NEED\_DB\_INFO vs. NEED\_USER\_INFO |
| `olausson2023linc` — Olausson et al. (2023), *LINC* | LLM translates NL premise/conclusion into FOL | Not applicable — benchmark sentences | FOL theorem prover (Prover9 / Vampire) | Prover output; no statutory trace | No — FOLIO / ProofWriter benchmarks | FOL only; no missing-information handling; no law-text step |
| `hsia2026neurosymbolic` — Hsia et al. (2026), *Neuro-Symbolic Compliance* | Multi-agent LLM pipeline (Rewriter, Execute, Analysis) extracts enforcement facts | LLM compiles enforcement-case text into Z3 constraints | Z3 with MaxSMT — computes minimal factual modification to restore compliance | Minimal-modification report; optimization-flavoured | Yes — financial legal compliance | Optimizes facts to force legality rather than halting and reporting; no NEED\_USER\_INFO; MaxSMT semantics differ from opinion-free halting |
| `callewaert2025verus` — Callewaert & Vandevelde (2025), *VERUS-LM* | LLM translates NL into FO(·) specification | LLM or human-authored FO(·) theory | IDP-Z3; simulates open-world reasoning with explicit `unknown` values per type | IDP-Z3 models as output | No — general verification tasks | FO(·) expressivity required; `unknown` is a single undifferentiated category; no source-typed halting |
| `wang2025trustworthy` — Wang et al. (2025), *Trustworthy Legal AI* | Multi-agent LLM pipeline extracts facts | LLM extracts rules; agents coordinate | Formal verification oracle; deterministic rule evaluator | Audit log from agent pipeline | Partially — legal Q&A datasets | Heavy agentic orchestration; no source-typed missing-info protocol; harder to audit at case level |
| `dragoni2017rule` — Dragoni et al. (2017), *Rule Extraction from Legal Documents* | Not automated — targeted extraction, not user-intent parsing | NLP pipeline extracts if-then rules; emits PROLEG encoding | PROLEG / Prolog | Symbolic derivation | Partially — GDPR / legal text corpora | No interactive user-facing step; no missing-information states; NLP pipeline quality-dependent |
| `nguyen2024krag` — Nguyen & Satoh (2024), *KRAG* | LLM front-end parses user query; Soft PROLEG allocates burden of proof | LLM extracts rules combined with knowledge graph retrieval | Soft PROLEG (defeasible Prolog) with Presupposed Ultimate Fact Theory | Proof tree with burden-of-proof allocation | Partially — legal Q&A benchmark | Burden-of-proof allocation, not source-typed halting; no explicit DB vs. user distinction |
| `nguyen2026pythen` — Nguyen & Satoh (2026), *PYTHEN* | LLM prompt generates Python-hosted defeasible rules and facts | LLM-to-Python autoformalization; lightweight target | PYTHEN Python runtime for defeasible logic | Python execution trace | No — any legal text in principle | Defeasible Python runtime is new and not independently validated; no separate domain vs. intent extraction |
| `kowalski2022logical` — Kowalski & Datoo (2022), *Logical English* | Controlled NL input; syntactic structure maps to Horn clauses | Lawyer authors Logical English text compiled to Prolog | Prolog | Prolog derivation; readable via Logical English surface | Domain-agnostic controlled-NL | Controlled NL authoring burden; no LLM extraction; no interactive missing-info protocol |
| `wong2026l4` — Wong et al. (2026), *L4* | Not present — L4 compiles statutes | Lawyer/programmer authors L4 DSL; compiled to s(CASP) / ASP | s(CASP) with ternary reasoning; ladder diagrams | Audit-grade justification tree | No — any rule-based domain | DSL authoring cost; no user-intent extraction layer; LLM integration left to caller |
| `morris2021blawx` — Morris (2021), *Blawx* | Not automated — structured scenario entry in browser UI | Lawyer authors rules in visual block editor; compiled to s(CASP) | s(CASP) — generates all consistent scenarios | Justification tree per scenario | No — any rule-based domain in principle | No NL extraction; structured scenario input only; browser-only runtime |
| `logitext2026` — Anonymous (2026), *Neurosymbolic Language Reasoning as SMT* | LLM generates SMT assertions from NL | LLM encodes domain theory as SMT assertions | Z3 / SMT inside LLM solving loop | SMT model as explanation | No — general NL reasoning | LLM is inside the solving loop — not decoupled; no legal-specific missing-info states |
| `holzenberger2020dataset` — Holzenberger et al. (2020), *Statutory Reasoning in Tax Law* | Dataset provides structured entailment pairs; no automated intent extraction | Tax-law rules as entailment problems | Textual entailment model (no symbolic reasoner) | No explicit trace | Yes — US tax code (IRC §526) | Neural-only; no symbolic solver; no missing-info states; evaluation dataset rather than system |

---

## Candidates to Survey

The following gap areas lack adequate coverage in the current bibliography. A
structured literature review should target:

1. **Abductive legal reasoning systems** — systems that infer missing premises
   from goals, beyond s(CASP) scenario enumeration. Key search terms:
   `abductive logic programming legal reasoning`.
2. **Interactive dialog for legal expert systems** — systems that dynamically
   ask follow-up questions to resolve under-specified facts; the Query-the-User
   protocol in `sergot1986british` is the only instance currently cited.
3. **OpenFisca** — the production-grade rules-as-code system for public-policy
   formulas; not yet in the bibliography. Strong comparator for transparent
   executable tax/benefit rules.
4. **LegalBench / MultiLegalPile** — benchmark suites for statutory reasoning;
   would contextualize the scenario-suite pass-rate metric.
5. **Defeasible logic programming beyond ASP** — `LegalRuleML` for provenance
   and temporal qualifiers; not yet in the bibliography.
6. **Monotonic vs. non-monotonic empirical comparison** — papers evaluating
   when monotonic propositional encoding suffices for administrative law; would
   directly justify the propositional-first stance of ADR 0003.

---

## Our Pipeline vs. the Matrix

### Positioning summary

The `framework` CLI occupies a specific cell in the design space that no single
surveyed system covers end-to-end:

| Property | `framework` | Closest comparator |
|---|---|---|
| Propositional-only runtime core | Yes (ADR 0003) | `sergot1986british` (Prolog, effectively propositional for BNA) |
| LLM restricted to structured extraction | Yes — LLM never decides the verdict | `hsia2026neurosymbolic`, `nguyen2024krag` (but both use richer logics) |
| Source-typed halting: DB vs. user | Yes — `NEED_DB_INFO` / `NEED_USER_INFO` at extraction time | None in surveyed set |
| Opinion-free halting at first blockage | Yes — no fact optimization or repair | Contrast with `hsia2026neurosymbolic` (MaxSMT repairs) |
| Minimal-information elicitation as research question | Yes (primary RQ) | Not articulated as a research question in any surveyed system |

### The minimal-information elicitation gap

At the 14 Apr supervision session (~22:04), the question arose whether any
surveyed system frames **minimal-information elicitation** — the problem of
identifying the smallest set of user-supplied facts needed to reach a
determinate verdict — as an explicit research target. The matrix shows that no
surveyed system does. `sergot1986british` pauses on any unbound variable but
does not order or minimize queries. `callewaert2025verus` marks values as
`unknown` but does not distinguish source types or minimize elicitation.

This gap is the primary novelty pitch articulated in the paper's §3.4 (Positioning
and Scope of Novelty) and aligns with the locked primary RQ.

### First-order vs. propositional observation

At the 14 Apr session (~19:52), it was noted that most published systems in the
legal AI and neurosymbolic compliance space operate over FOL or at minimum over
defeasible ASP: `olausson2023linc` (FOL), `callewaert2025verus` (FO(·)),
`hsia2026neurosymbolic` (SMT with arithmetic), `pan2023logic` (Z3 / Pyke),
`wong2026l4` (s(CASP)). The current `framework` deliberately operates over a
propositional core (ADR 0003), trading expressive power for decidability, trace
simplicity, and auditability in routine administrative workflows. This is a
deliberate design choice, not a limitation to be hidden.

The matrix above makes the FOL-vs-propositional split explicit in the Step 3
column and the Notable Limitations column, and the paper §Related Work §3.4
should foreground it as a positioning decision rather than a capability gap.
