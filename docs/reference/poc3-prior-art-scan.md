# `framework` CLI Prior-Art Scan

## Scope

This note records a focused prior-art scan for the current `framework` CLI shape. The implementation was first developed under `poc3/`, so older notes may still use that name:

1. request text -> structured claims
2. law text -> structured rules/domain
3. symbolic solve with final authority in the reasoner
4. plain-text auditable trace with explicit missing-information handling

The goal is not to collect every AI-and-law paper. The goal is to identify the closest implemented or seriously prototyped systems so the current `framework` CLI does not reinvent well-known legal expert-system ideas under newer terminology.

## Executive Summary

The main conclusion is conservative:

- The broad idea of translating law into executable rules is old and well explored.
- Legal expert systems with explanation, statutory formalization, and rule-grounded decision support are also old and well explored.
- Modern law-as-code systems such as `Catala` and `OpenFisca` show that auditable executable legal rules are already a mature practical line.
- Recent work now adds LLM-assisted extraction and hybrid LLM/symbolic pipelines, but the design space is still uneven.

What still looks less saturated is not the existence of a legal expert system by itself. The more defensible niche is the exact combination of:

- LLMs restricted to structured extraction rather than final adjudication
- a symbolic solver retaining final authority
- explicit `NEED_DB_INFO` vs `NEED_USER_INFO` states
- neutral blockage reporting for irrelevant or insufficient law text
- a small, hand-auditable CLI pipeline designed for inspection rather than deployment claims

## Closest Systems

| Closeness | Item | Type | Why it is close |
| --- | --- | --- | --- |
| 5/5 | M. J. Sergot, F. Sadri, R. A. Kowalski, F. Kriwaczek, P. Hammond, H. T. Cory, *The British Nationality Act as a Logic Program* (1986, *Communications of the ACM*), [doi](https://dl.acm.org/doi/10.1145/5689.5920) | paper + implemented logic program | Canonical law-text-to-logic reference. Statutory text was formalized into executable logic for legal problem solving. |
| 5/5 | Denis Merigoux, Nicolas Chataing, Jonathan Protzenko, *Catala: A Programming Language for the Law* (2021, PACMPL/POPL line), [arXiv](https://arxiv.org/abs/2103.03198) | paper + compiler + proofs + real PoCs | Extremely close on auditable law-to-code and explanation-friendly implementation, though `Catala` is programmer/lawyer authored rather than LLM-extracted at runtime. |
| 4.5/5 | `OpenFisca`, [official site](https://openfisca.org/en/) | production-style open-source rules-as-code system | Strong comparator for executable public-policy rules, transparent APIs, and law-change handling, though it does not center LLM extraction or symbolic proof traces. |
| 4.5/5 | J. Arias et al., *Automated Legal Reasoning with Discretion to Act using s(LAW)* (2024, *Artificial Intelligence and Law*), [arXiv](https://arxiv.org/abs/2401.14511) | paper + implemented framework | Very close on symbolic reasoning, explicit justifications, and public-sector style legal decision support, though it uses ASP/s(CASP) rather than SMT and is not LLM-centered. |
| 4/5 | Trevor Bench-Capon, Frans Coenen, Paul Orton, *Argument-based Explanation of the British Nationality Act as a Logic Program* (1993, *Information & Communications Technology Law*), [abstract](https://www.tandfonline.com/doi/abs/10.1080/13600834.1993.9965668) | explanation-focused follow-on paper | Close specifically on turning symbolic statutory reasoning into more usable explanations rather than leaving a raw proof trace. |
| 4/5 | Markus Bertl, Simon Price, Dirk Draheim, *Transforming legal texts into computational logic: Enhancing next generation public sector automation through explainable AI decision support* (2026, *International Journal of Cognitive Computing in Engineering*), [doi landing](https://doi.org/10.1016/j.ijcce.2025.07.003) | paper + law-as-code prototype | Close on law-text-to-computational-logic extraction, explainable decision support, and public-sector workflow framing. |
| 4/5 | Hossein Janatian et al., *From Text to Structure: Using Large Language Models to Support the Development of Legal Expert Systems* (2023), [arXiv](https://arxiv.org/abs/2311.04911) | paper + prototype workflow | Very relevant for the step-2 bottleneck: using LLMs to draft structured pathways for legal expert systems while keeping humans or symbolic systems in control. |
| 4/5 | *A Path Towards Legal Autonomy: An interoperable and explainable approach to extracting, transforming, loading and computing legal information using large language models, expert systems and Bayesian networks* (2024), [arXiv](https://arxiv.org/abs/2403.18537) | paper + architectural prototype | Close on interoperable legal extraction pipelines with explainability, though it mixes expert systems with Bayesian networks rather than insisting on symbolic final authority alone. |
| 3.5/5 | `LegalRuleML`, [OASIS core specification](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.html) | standard/specification | Not an end-user system, but highly relevant for isomorphism, source-rule association, defeasibility, temporal qualifiers, and provenance modeling. |
| 3.5/5 | D. Oberle et al., *Engineering Compliant Software: Advising Developers by Automating Legal Reasoning* (2012, *SCRIPTed*), [article](https://script-ed.org/article/engineering-compliant-software-advising-developers-automating-legal-reasoning/) | paper + compliance workflow prototype | Strong match on norm graphs, ontology-backed legal reasoning, and interactive completion of missing software facts. Less close on user-case adjudication. |
| 3.5/5 | *Towards Trustworthy Legal AI through LLM Agents and Formal Reasoning* (2025), [arXiv](https://arxiv.org/abs/2511.21033) | paper + hybrid prototype | The closest modern LLM-plus-formal-reasoning comparator. Very relevant because it also puts formal verification after extraction, but it is much heavier and more agentic than the current `framework` CLI. |

## Important Building Blocks

- Robert Kowalski, *Legislation as Logic Programs* (early 1990s), [Springer entry](https://link.springer.com/chapter/10.1007/3-540-55930-2_15). This is a direct conceptual ancestor of the “law text resembles executable rule structure” line.
- `Regorous`, e.g. *The Regorous Approach to Process Compliance*, [overview link](https://www.researchgate.net/publication/281095044_The_Regorous_Approach_to_Process_Compliance). Important for norm compliance, trace replay, and auditability, even though it is process-compliance oriented rather than user-request oriented.
- `LegalRuleML`. Important for legal-source linkage, defeasible priorities, temporal status, and explicit metadata about interpretation.

## Design Patterns Worth Reusing

- Keep law-text fragments linked to executable rules rather than treating the formal layer as detached code. The `LegalRuleML` isomorphism idea and the `Catala` literate style are strong precedents.
- Separate extraction from adjudication. The recent hybrid lines and the older expert-system lines both support this separation for different reasons.
- Keep explanation aligned with rule structure, not only with model outputs. The Bench-Capon explanation work and `s(LAW)` justifications are especially relevant here.
- Make missing information explicit. `OpenFisca` adjacent expert-system discussions and compliance workflows show that “unknown because not supplied yet” is operationally important.
- Treat law changes as a first-class maintenance problem. `Catala` and `OpenFisca` are especially relevant here.

## Claims To Avoid

The following would likely be overstated:

- claiming that executable legal rules are new
- claiming that auditable legal expert systems are new
- claiming that law text to machine-readable rules is new
- claiming that explanation traces for rule-based legal reasoning are new
- claiming that a solver-backed legal pipeline is new on its own

Even “LLM plus symbolic reasoning for law” should be phrased carefully, because that line is now emerging in several places.

## Plausible Contribution Space

The safer contribution angle for the current proposition-first `framework` CLI is narrower:

- a supervision-friendly, hand-auditable four-step pipeline
- strict symbolic final authority with LLMs limited to structured intermediate artifacts
- explicit modeling of open information and staged completion (`DB` vs user)
- neutral blockage reporting for mismatched or sparse laws
- a small experimental setup for studying how proposition-first formalization behaves under law swaps and prompt swaps

This is a stronger and more honest claim than presenting the `framework` CLI as a fully new category of legal AI system.

## Suggested First Reads

1. Sergot et al. (1986), *The British Nationality Act as a Logic Program*
2. Merigoux et al. (2021), *Catala: A Programming Language for the Law*
3. Arias et al. (2024), *Automated Legal Reasoning with Discretion to Act using s(LAW)*
4. Janatian et al. (2023), *From Text to Structure*
5. Bertl, Price, Draheim (2026), *Transforming legal texts into computational logic*

## Useful Manual Search Strings

- `legal expert system statutory logic program explanation`
- `law as code executable legislation audit trail`
- `LLM legal expert system structured extraction symbolic reasoning`
- `answer set programming legal reasoning explanation`
- `LegalRuleML provenance isomorphism defeasible legal rules`
