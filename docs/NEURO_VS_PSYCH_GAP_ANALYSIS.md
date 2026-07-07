# Neuroepidemiology Audit: Gap Analysis vs Psychiatry Audit

**Date:** 2026-07-02
**Purpose:** Assess whether the neuro dataset can support the same per-edge discordance study as the psych audit

---

## Dataset comparison

| Dimension | Psych (master) | Neuro (v11) | Gap? |
|-----------|---------------|-------------|------|
| Total rows | 97 | 76 | Comparable |
| Numeric estimates | 69 | 70 | Good |
| With 95% CIs | ~55 | 52 | Good |
| Disease families | 13 (Depression, Schizophrenia, ADHD, etc.) | 2 (MS=33, AD=43) | Different structure |
| Tier coverage | Disconfirmed through Triangulated + Validated | Disconfirmed through Triangulated | No Validated |
| Design types | meta-analysis, RCT, observational, MR, imaging, genetic | observational (32), RCT (27), MR (9), genetic (4), diagnostic (3) | Neuro has fewer but cleaner types |
| `family` column | Yes (13 disorder families) | **NO — MUST ADD** | Blocking |
| Per-edge analysis scripts | sheaf_q_test.py, h1_transportability.py, permutation_test.py, meta_regression.py | geometric_validation.py ONLY | Must port or adapt |
| External ground truth (RCT/GWAS/animal) | data/external_ground_truth.csv (64 rows) | **None** | Must create |
| Independent institutional scores | data/independent_ground_truth.csv (64 rows, 5 dims) | **None** | Must create |
| Tier assignment method | Perplexity RAG + human review | Perplexity RAG + human review | Same |

---

## What the neuro dataset HAS that psych doesn't

1. **Stronger per-mechanism case studies:**
   - EBV → MS: HR = 32.4 (4.3-245) from Bjornevik 2022 Science. A single landmark study.
   - APOE4 → AD: OR = 3.46 (het), 23.5 (hom). Strongest genetic effect in all of medicine.
   - Vitamin D → MS: MR says OR = 2.0 (causal), RCTs say null (MS-030 OR=0.98, MS-007d HR=1.17). This is the PROTOTYPE mimic/evidence-misfire case.
   - Fingolimod: reduces relapses (rate ratio 0.52) but NOT disability progression (HR 0.83, null). Same drug, same trial, different endpoints → opposite conclusions. The ultimate per-edge discordance.

2. **Failed drug cluster in AD:**
   - 6+ null RCTs: solanezumab (A4, EXPEDITION3), semaglutide (EVOKE), semagacestat (harmful), aducanumab (ENGAGE null), verubecestat (null/worse), ginkgo (GEM null). All HR ≈ 1.0.
   - Frechet T = 0.004 — these drugs CONVERGE on null. This is the opposite of the psych finding.

3. **MR as negative control:**
   - Smoking → MS: observational positive, MR null (OR 1.03, 0.89-1.19). Classic confounding case.
   - IL-6 → AD: MR null (OR 1.0, 0.92-1.09). Inflammation non-causal on this axis.
   - These are DESIGNED discordances — the MR result is the correct one, the observational result is confounded.

4. **Better CI coverage:** 52/76 rows have verified CIs (68%) vs psych (~57%)

---

## What's MISSING (must create)

### 1. `family` column (BLOCKING — everything else depends on this)

Proposed family assignments for the 76 rows:

| Family | Case IDs | N | Description |
|--------|----------|---|-------------|
| EBV_MS | MS-001, MS-018a, MS-018b | 3 | EBV seroconversion and interaction |
| VitD_MS | MS-007, MS-007b, MS-007c, MS-007d, MS-030 | 5 | Vitamin D MR + RCT cluster |
| NfL_MS | MS-005a, MS-005b, MS-005c | 3 | Neurofilament light biomarker |
| HLA_MS | MS-017, MS-018a | 2* | HLA-DRB1*15:01 (overlaps EBV) |
| Obesity_MS_AD | MS-013a, MS-013b, AD-005h, AD-005h2 | 4 | BMI/obesity → MS/AD |
| AntiCD20_MS | MS-011, MS-031, MS-032b | 3 | Ocrelizumab/anti-CD20 |
| OtherDMT_MS | MS-028, MS-029, MS-033, MS-033b, MS-034, MS-035, MS-036 | 7 | Other disease-modifying therapies |
| APOE_AD | AD-002a, AD-002b, AD-002c | 3 | APOE4 genetic risk |
| Amyloid_AD | AD-001, AD-001b, AD-C1, AD-032, AD-033, AD-035, AD-036, AD-037 | 8 | Amyloid hypothesis + anti-amyloid drugs |
| Tau_AD | AD-C2, AD-007 | 2 | Tau pathway |
| Biomarker_AD | AD-006, AD-009a, AD-009b, AD-009c, AD-010 | 5 | Diagnostic biomarkers |
| ModRisk_AD | AD-005a-p (hearing, social, alcohol, TBI, smoking, etc.) | ~15 | Modifiable risk factors |
| Metabolic_AD | AD-005b, AD-005l, AD-020, AD-023, AD-034 | 5 | T2D/GLP-1/metabolic |
| Inflammation_AD | AD-003, AD-004 | 2 | TREM2/IL-6 neuroinflammation |
| HRT_AD | AD-031, AD-031b | 2 | Hormone replacement therapy |
| Other_AD | AD-030 | 1 | Ginkgo etc. |

Some rows may belong to multiple families (MS-018a in both EBV and HLA). Need to pick primary.

### 2. Per-edge discordance analysis (PORT from psych)

The psych repo has `analysis/geometric_causal/sheaf_q_test.py` which computes:
- Pool within each evidence type per family
- Cochran's Q across evidence-type strata
- Per-edge signed discordances

Must adapt for neuro's:
- Different column names (`n_cases`/`n_controls` vs `n`)
- Different tier naming (T1-T4 vs Proposed/Causally Suggestive/etc. — wait, v11 uses the SAME names as psych now)
- Different design categories (neuro has `genetic/cohort`, `diagnostic`)
- Need the `family` column first

### 3. External ground truth

For neuro (MS + AD), we can collect:
- **FDA drug approval status** for DMTs (ocrelizumab approved, simvastatin null, biotin null) and AD drugs (lecanemab approved, aducanumab withdrawn, solanezumab failed)
- **Clinical guideline endorsement** (AAN, McDonald criteria for MS; NIA-AA for AD)
- **Biomarker validation status** (NfL, p-tau217 FDA-cleared?)
- **Replication in independent cohorts** (ENIGMA, ADNI, UK Biobank, ABCD)
- **GWAS support** (APOE4, HLA-DRB1*15:01, EBV — all strong)

### 4. Independent institutional scores (same 5 dimensions as psych)

| Signal | MS source | AD source |
|--------|-----------|-----------|
| FDA approval (0-2) | DMT approvals | Anti-amyloid approvals |
| GRADE certainty (0-4) | Cochrane MS DMTs | Cochrane AD drugs |
| Guideline endorsement (0-3) | AAN 2018, McDonald 2017 | NIA-AA 2018 |
| Textbook status (0-3) | Adams & Victor's, Ropper | Kandel, Bear |
| Replication status (0-3) | ENIGMA, UK Biobank, IMSGC | ADNI, ABCD, PGC-ALZ |

---

## Can we do the same study?

### Per-edge discordance: YES, and neuro has BETTER case studies

The vitamin D case is the clearest per-edge discordance in either dataset:
- MR: OR = 2.0 (1.7-2.5) — genetically lowered vitamin D CAUSES MS risk
- RCT (D-Lay MS): HR = 0.66 (0.50-0.87) for disease activity — SOME support
- RCT (VIDAMS): HR = 1.17 (0.67-2.05) — NULL
- RCT (early meta): OR = 0.98 (0.45-2.16) — NULL
- Edge: MR says causal, RCTs are mixed-to-null. Direction: MR estimates a larger effect than RCTs deliver.

The fingolimod case is a per-edge discordance WITHIN a single trial:
- Relapse: rate ratio 0.52 (0.40-0.66) — strong
- Disability: HR 0.83 (0.61-1.12) — null
- Edge: same drug, same mechanism, same trial, different outcomes → different conclusions

### Investigation paradox: TESTABLE but prediction is different

In psych: well-studied families (Depression, Schizophrenia) showed MORE cross-type Q.
In neuro: AD has way more evidence types and rows (43) than MS (33). Does AD show more discordance?

The AD failed-drug cluster CONVERGES (T = 0.004, all HR ≈ 1.0). So the investigation paradox might go the OTHER WAY in neuro: more study of amyloid hypothesis produced convergent failure. That's actually a different and complementary finding.

### Institutional lag: YES, strongest case is AD amyloid

Aducanumab: FDA approved (accelerated, 2021) despite ENGAGE trial being null. Later effectively withdrawn. Institutional score would be HIGH (FDA approved, guideline-mentioned), tier = Disconfirmed for ENGAGE. This is a STRONGER mimic/institutional-lag case than serotonin, because the institutional decision was MORE controversial and more recent.

### Temporal holdout: YES, AD drug pipeline is perfect

AD has the richest Phase III pipeline of any disease:
- Donanemab (approved 2024) — clean holdout for 2019-cutoff model
- Lecanemab (approved 2023) — clean holdout
- EVOKE semaglutide (failed 2025) — clean holdout
- A4 solanezumab (failed 2023) — clean holdout
- Multiple Phase III tau drugs — ongoing

### PrimeKG: YES, and AD/MS have the best coverage in PrimeKG

PrimeKG was built WITH Alzheimer's and neurological diseases as primary use cases. Node coverage for APOE4, APP, PSEN1, MAPT, SLC6A4, HTR2A, etc. should be excellent.

### Philosophy papers: YES

**Triangulation Paradox** applies: vitamin D → MS is the worked example (MR causal, RCTs null).
**Etiology-Treatment Inference Barrier** applies: fingolimod is the worked example (reduces relapses, not disability).

---

## Recommended next steps

1. **Add `family` column to effect_sizes_v11.csv** (or create v12 with it) — BLOCKING
2. **Port sheaf_q_test.py** from psych repo → adapt for neuro column structure
3. **Port h1_transportability.py** and **permutation_test.py**
4. **Create external_ground_truth.csv** and **independent_ground_truth.csv** for neuro
5. **Run the per-edge analysis** — vitamin D and fingolimod cases should produce striking results
6. **Write MOLPSYCH-equivalent outline** targeting IJE or Lancet Neurology

---

## Does the dataset need more data from Perplexity?

**Probably not for the core analysis.** 76 rows with 70 numeric estimates and 52 CIs is sufficient. The psych analysis works on 97 rows / 69 numeric.

**BUT — for better per-edge analysis, we need more MR and genetic rows.** Currently:
- MR: 9 rows (5 for MS, 4 for AD) — thin
- Genetic: 4 rows (all MS) — very thin for AD
- The per-edge discordance between MR and observational is the KEY analysis. With only 9 MR rows, we have limited families where both MR AND observational exist.

**Specific gaps to fill:**
- AD MR studies: BMI → AD (MR), education → AD (MR), blood pressure → AD (MR) — these exist but lack numeric estimates (AD-020, AD-021, AD-022 all have empty `estimate` fields)
- MS genetic: more HLA variants, non-HLA risk loci from IMSGC
- AD genetic: TREM2 rare variant OR, CLU, BIN1, PICALM from IGAP/Bellenguez 2022

So: **ask Perplexity to fill the 3 empty MR rows (AD-020, AD-021, AD-022) with numeric estimates** and potentially add 3-5 more genetic/MR rows for AD. That's the minimum to make per-edge analysis robust.
