# neuroepidemiology-validity-audit

Claim-level validity audit of mechanism claims in MS and AD neuroepidemiology, scoring each against a four-tier evidence scale with causal decomposition and Levi contraction.

## What this is

The MS and AD literatures contain hundreds of mechanism claims at different levels of evidential support. Most have observational associations but lack the instruments, temporal ordering, or perturbation evidence needed for causal claims. The dominant failure mode is conflating mechanism-of-treatment with mechanism-of-disease, and mechanism-of-relapse with mechanism-of-progression.

This catalog audits 76 claims across MS and AD, decomposing each into causal legs and scoring on the Mechanistic Validity tier system:

| Tier | What it requires |
|---|---|
| Proposed | Construct defined; at least one measurement conducted |
| Causally Suggestive | Necessity via causal intervention; baseline separation |
| Mechanistically Supported | Sufficiency established; intervention reach across 2+ methods; specificity tested |
| Triangulated | Convergent evidence from 2+ independent evidence families; cross-distribution replication |
| Validated | All five validity dimensions addressed; measurement calibration audited |
| Disconfirmed | Negative result on a key criterion |

## Catalogs

- **`catalog_ms.md`** — 52 MS mechanism claims spanning EBV etiology, HLA genetics, relapse vs progression biology, treatment mechanisms, biomarker validation, and digital phenotyping
- **`catalog_ad.md`** — AD neurodegeneration claims covering amyloid cascade, tau propagation, APOE4, anti-amyloid therapeutics, plasma biomarkers, and ATN staging

## Experiments

Geometric and sheaf-cohomological experiments validating the catalog structure:

| Experiment | Result |
|---|---|
| Prerequisites | Contamination 0.9%, cohort stable, IRT theta > raw EDSS |
| Cocycle obstruction | Holonomy 1.851 matches predicted 1.869 (Berry phase) |
| Bracket-norm confound audit | All 4 imaging metrics T3-confirmed |
| Sheaf DAG adjudication | Per-edge Q detects infl/degen heterogeneity (Q > 1500) |
| H1 effect-modifier | 7/7 pairs correctly classified (100%) |

## Related

- [epidemiology-boundary-conditions](https://github.com/elliottower/epidemiology-boundary-conditions) — Methods paper characterizing when geometric tools (sheaf cohomology, Grassmannian holonomy, discrete curvature) outperform standard statistics. The MS/AD catalogs here provided the domain expertise that informed its simulation parameters.
- [Mechanistic Validity](https://github.com/mechanistic-validity) — The validity audit framework, which this catalog applies to clinical neuroepidemiology.

## Status

MS catalog is substantive (52 cases scored). AD catalog is partial (~13 cases). Extension spec describes phases 1-5 for scaling to real data (MR re-analysis, ADNI access, cross-domain meta-analysis).

## License

MIT
