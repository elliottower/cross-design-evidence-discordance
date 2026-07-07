# Batch 3: PubMed eutils extraction results (2026-07-02)

## What ran
`analysis/batch2/mechval_pubmed_fill.py` with expanded search terms for all 16 gap cases
(2 missing estimates, 14 missing CIs). Script queries NCBI eutils (esearch + efetch),
parses OR/HR/RR with 95% CIs from abstracts via regex, validates that parsed estimate
matches known estimate within 15%.

## Results

### New estimates filled (2)
| case_id | claim | estimate | CI | PMID | notes |
|---------|-------|----------|-----|------|-------|
| MS-002 | Iron-rim lesion burden vs disability | OR 0.24 | 0.15-0.39 | 42352643 | paramagnetic rim lesion; needs biostat check |
| MS-011 | Ocrelizumab PPMS progression | HR 0.70 | 0.57-0.86 | 42208561 | ORATORIO-HAND (Lancet 2026) |

### CIs recovered (3 validated)
| case_id | known est | CI found | PMID | est_in_abstract |
|---------|-----------|----------|------|-----------------|
| MS-001 | 32.0 | 2.3-327.6 | 38497939 | 27.6 (related study, very wide CI) |
| MS-013a | 1.26 | 1.17-1.77 | 37963678 | 1.18 (similar MR, slightly diff point est) |
| AD-002a | 3.4 | 2.82-3.76 | 41724662 | 3.25 (APOE4 het meta, close match) |

### CIs rejected by validation (2 removed post-hoc)
- MS-010: CI (1.002-1.012) from wrong effect (est=0.73)
- AD-004: CI (1.021-1.109) contradicts null finding (est=1.0)

### Failed lookups (9)
MS-005b, MS-005c, MS-007, MS-010, MS-013b, MS-017, AD-002b, AD-002c, AD-009c
Reason: abstract text doesn't contain explicit ratio+CI matching known estimate.

## Tier calibration update
- v2: n=14, tau=0.407, p=0.070
- v3: n=15, tau=0.360, p=0.090
- Adding MS-002 (T2-T3, small OR=0.24) slightly weakened correlation, expected.
- Still DESCRIPTIVE (n < 30 target).

## Pooling status
Still BLOCKED. CIs are spread across singleton (domain, design, scale) clusters.
DerSimonian-Laird needs >= 2 studies per cluster with CIs.

## Ceiling of abstract-based extraction
Most OR/HR/RR with 95% CIs appear in full text, tables, or supplements.
Abstract regex parsing has hit diminishing returns. Next steps to reach n>=30:
1. Manual full-text extraction (human reviewer)
2. PMC full-text API (for open-access papers)
3. Expand catalog claims (52 MS mechanisms, only ~15 currently extracted)
4. Cross-reference with Cochrane/Campbell reviews for pre-pooled estimates

## Files produced
- `data/effect_sizes_v3.csv` — 25 rows (all numeric), 5 with CIs
- `data/pooled_estimates_v3.csv` — all clusters still singleton
- `output/risk_forest_v3.png` — forest plot with CI whiskers
