# MechVal Quantitative Extension — QC Report (build 2026-07-02)

## Deliverables in output/
- mechval_effect_sizes_v2.csv   : 25 rows (23 numeric, 21 gap_reason flags), full provenance schema
- mechval_risk_forest.png       : risk-ratio forest, Kendall tau=0.41 p=0.069 n=14 (DESCRIPTIVE)
- mechval_pubmed_fill.py        : eutils gap-fill scaffold (run outside sandbox; captures est + 95% CI)
- mechval_meta.py               : Phase 2 DerSimonian-Laird pooling (homogeneous clusters only)
- mechval_pooled_estimates.csv  : current pooling attempt — ALL clusters BLOCKED (see below)

## Guardrail status
- No fabricated estimates. Every number traces to a catalog web### citation.
- 21/25 rows carry gap_reason (mostly narrative-only or no-CI claims).
- No cross-scale pooling: ratio-risk isolated from pct_slowing / r2 / sens-spec / effect-d.

## Key finding: pooling is currently BLOCKED
None of the extracted rows carry 95% CIs, so DerSimonian-Laird cannot weight studies.
=> The eutils fill step is a HARD PREREQUISITE for Phase 2, and it must parse CIs
   (mechval_pubmed_fill.py already regexes "95% CI lo-hi").

## Calibration status
- Baseline (cited subset): tau=0.89, n small.
- Current systematic risk-OR cluster: tau=0.41, p=0.069, n=14.
- Target (spec): tau, p<0.05, n>=30. NOT yet reached -> stays DESCRIPTIVE.

## Next actions (in order)
1. Build full TERMS map (MS 001-052, AD 001-010/C1-C3) -> run mechval_pubmed_fill.py -> v3 csv with CIs.
2. Re-run mechval_meta.py -> first real pooled ORs + I2 + Egger (where k>=10).
3. Re-run tier calibration on n>=30 risk cluster -> convert tau to a powered claim.
4. AD scaffold expansion (next task).
