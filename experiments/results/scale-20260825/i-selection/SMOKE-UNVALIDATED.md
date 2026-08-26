# SMOKE — UNVALIDATED

Generated 2026-08-26T06:15:30Z. Overnight cap EUR 100.00; spent EUR 13.3658; remaining EUR 86.6342.
Do not quote these numbers as results. Gold `low` rows and claim alignments still need operator audit.

Matrix label: `scale-2026-08-25-i-selection`.
Providers requested: gemini, openai, anthropic, deepseek.
Providers run: gemini, openai, anthropic, deepseek.
Providers skipped (missing key or stub): —.

### Experiment (ii) — runtime (solver)

- n scored: 0 / 0
- outcome accuracy: 0.000
- ALLOW accuracy: —
- DENY accuracy: —
- NEED_MORE_INFO accuracy: —
- mean missing-fact P/R: 0.000 / 0.000
- macro missing-fact P/R: 0.000 / 0.000

### Experiment (ii) — LLM-only

_No LLM rows (no keys, skipped, or runtime-only)._

### Experiment (i) — encoding

# Experiment (i) — synthesis extraction vs gold encoding

Catalog-held-out boolean synthesis scored by lexical claim alignment and truth-table paper-outcome equivalence. Selection-mode ablation scores catalog-id F1 via existing `llm.extract_domain_artifact`.

| case | condition | align F1 | equivalent | rate | n_agree/n_rows | audit | dropped rules |
| --- | --- | --- | --- | --- | --- | --- | --- |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.90 | id-set (claim F1 1.00, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.75 | id-set (claim F1 1.00, rule F1 0.50) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.90 | id-set (claim F1 1.00, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.90 | id-set (claim F1 1.00, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.92 | id-set (claim F1 0.92, rule F1 0.91) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.90 | id-set (claim F1 1.00, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.92 | id-set (claim F1 0.92, rule F1 0.91) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.95 | id-set (claim F1 1.00, rule F1 0.91) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.86 | id-set (claim F1 0.92, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.92 | id-set (claim F1 0.92, rule F1 0.91) | — | — | — | — |
| civil_service_eligibility | selection | 0.90 | id-set (claim F1 1.00, rule F1 0.80) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.69 | id-set (claim F1 0.89, rule F1 0.50) | — | — | — | — |
| building_permit | selection | 0.79 | id-set (claim F1 0.91, rule F1 0.67) | — | — | — | — |
| section_120_demo | selection | 0.92 | id-set (claim F1 0.92, rule F1 0.91) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.82 | id-set (claim F1 0.83, rule F1 0.80) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.00 | id-set (claim F1 0.00, rule F1 0.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.00 | id-set (claim F1 0.00, rule F1 0.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.00 | id-set (claim F1 0.00, rule F1 0.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.00 | id-set (claim F1 0.00, rule F1 0.00) | — | — | — | — |
| civil_service_eligibility | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| consumer_withdrawal | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| land_tax_exemption | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| personal_data_journalism | selection | 0.84 | id-set (claim F1 0.89, rule F1 0.80) | — | — | — | — |
| building_permit | selection | 1.00 | id-set (claim F1 1.00, rule F1 1.00) | — | — | — | — |
| section_120_demo | selection | 0.00 | id-set (claim F1 0.00, rule F1 0.00) | — | — | — | — |

Mean alignment F1: 0.900 (n=120).

## How to read this

- Runtime accuracy on gold should be ~1; anything below is a suite bug, not a finding.
- LLM-only matching runtime on outcomes does **not** kill the paper: lean on fact-set P/R.
- Near-zero synthesis F1 is a finding (variant B: runtime vs LLM-only).
