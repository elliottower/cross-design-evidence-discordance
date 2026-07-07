# Perplexity Prompt Batches for Neuroepidemiology Validity Audit

Generated 2026-07-02. Three batches, paste each one separately.
Copy the response and paste it back to Claude.

---

## PROMPT 1: Fill missing 95% CIs on existing rows (highest priority)

```
I need the PRIMARY (most-adjusted) odds ratio, hazard ratio, or risk ratio WITH 95% confidence intervals for each of these 10 neuroepidemiology claims. For each one I already have a point estimate — I need the CI from the original or a major meta-analysis.

FORMAT YOUR RESPONSE AS A CSV with columns:
case_id, claim, estimate_type, estimate, ci_low, ci_high, n_cases, n_controls, population, PMID, source_paper, notes

Here are the 10 claims:

1. MS-005a: "Elevated baseline serum neurofilament light chain (sNfL) predicts reaching EDSS 4.0 in MS"
   - I have: risk ratio ≈ 4.3
   - Source context: long-term MS cohort, baseline sNfL 7.62 pg/mL threshold, direction = higher sNfL → worse outcome
   - Need: the RR or OR with 95% CI from the primary study (likely Barro et al. or Disanto et al.)

2. MS-005b: "Baseline sNfL > 10.2 pg/mL predicts disability progression in progressive MS"
   - I have: adjusted OR ≈ 7.8
   - Source context: JNNP progressive-MS cohort
   - Need: adjusted OR with 95% CI

3. MS-005c: "Rising sNfL trajectory over baseline-to-6-years predicts progression in progressive MS"
   - I have: OR ≈ 49.0
   - Source context: same JNNP progressive-MS cohort as MS-005b
   - Need: OR with 95% CI (this is a very large effect, likely wide CI)

4. MS-007: "Genetically lowered 25-hydroxyvitamin D causally increases MS risk (Mendelian randomization)"
   - I have: OR ≈ 2.0 per 1-SD decrease in log-25(OH)D
   - Source context: IMSGC MR study, European population, n_cases ≈ 14,498
   - Need: OR with 95% CI from the primary IMSGC MR publication (Mokry et al. 2015 or Rhead et al. 2016)

5. MS-010: "Lower deep gray matter volume predicts faster time-to-EDSS-progression in MS"
   - I have: HR ≈ 0.73 per SD (protective direction: more volume → less progression)
   - Source context: MAGNIMS consortium, n = 1,417, 7-center study
   - Need: HR with 95% CI from the MAGNIMS publication

6. MS-013b: "Higher adult BMI causally increases MS risk (Mendelian randomization)"
   - I have: OR ≈ 1.43 per SD, pleiotropy-robust
   - Source context: MR using UKB/IMSGC, European, n_cases ≈ 14,802, n_controls ≈ 26,703
   - Need: OR with 95% CI from the primary MR publication

7. MS-017: "HLA-DRB1*15:01 is the strongest single genetic risk factor for MS"
   - I have: OR ≈ 3.06
   - Source context: meta-analysis across Caucasian, Asian, African American populations
   - Need: OR with 95% CI from the primary meta-analysis (Moutsianas et al. or IMSGC)

8. AD-002b: "APOE ε4 homozygosity dramatically increases Alzheimer's disease risk"
   - I have: OR ≈ 23.5 (midpoint of reported 13–34 range)
   - Source context: meta-analyses of APOE4 dosage, multi-ethnic
   - Need: OR with 95% CI from the largest/most recent meta-analysis (Belloy et al. 2023 or Farrer et al. 1997)

9. AD-002c: "APOE ε4/ε4 women have higher AD risk than APOE ε4/ε4 men"
   - I have: OR ≈ 13.5 (midpoint of reported 12–15 range)
   - Source context: sex-stratified APOE4 analysis
   - Need: OR with 95% CI, separately for women

10. AD-009c: "Abnormal plasma p-tau217 in cognitively unimpaired individuals predicts cognitive impairment"
    - I have: HR ≈ 6.6 (AT+ subgroup)
    - Source context: cognitively unimpaired (CU) cohort with plasma biomarker follow-up
    - Need: HR with 95% CI from the primary publication

IMPORTANT RULES:
- Only report the PRIMARY or MOST-ADJUSTED estimate from each study
- If you cannot find the exact CI, say "CI not found in available text" — do NOT fabricate
- Include the PMID so I can verify
- If the estimate you find differs from mine, report YOURS with a note explaining the discrepancy
- Prefer meta-analyses over single studies when available
```

---

## PROMPT 2: New MS ratio-scale claims (expand from 15 to ~25 rows)

```
I am building a quantitative catalog of neuroepidemiology mechanism claims with effect sizes. I need primary OR/HR/RR estimates WITH 95% CIs for the following MS (multiple sclerosis) claims. These come from a mechanistic validity audit and I need the quantitative anchors.

FORMAT YOUR RESPONSE AS A CSV with columns:
case_id, claim, design, scale, estimate, ci_low, ci_high, n_cases, n_controls, population, PMID, source_paper, verdict_suggestion, notes

Here are the claims to extract:

1. MS-006: "Oligoclonal bands (OCB) in CSF are associated with MS diagnosis and prognosis"
   - Need: OR for OCB-positive vs OCB-negative for MS diagnosis (vs other neurological diseases)
   - Also: HR for OCB+ predicting conversion from CIS to MS, if available
   - Source: likely Dobson et al. meta-analysis or the 2017 McDonald criteria validation studies

2. MS-018: "HLA-DRB1*15:01 × EBV interaction shows additive (but not multiplicative) effect modification for MS risk"
   - Need: the synergy index S with 95% CI from the meta-analysis (I believe S = 1.43, CI 1.05–1.95)
   - Also: the individual ORs for EBV alone and HLA alone from the same analysis
   - Source: Xiao et al. or similar interaction meta-analysis

3. MS-020: "Female sex is associated with ~3x higher MS incidence (and male sex with faster progression)"
   - Need: OR or incidence rate ratio for female vs male MS risk
   - Also: HR for male sex predicting faster disability progression, if available
   - Source: Walton et al. Atlas of MS, or Bove & Chitnis review

4. MS-021: "Smoking does NOT causally increase MS risk (MR disconfirmation of observational association)"
   - Need: the MR OR for smoking → MS (should be near 1.0, non-significant) as a NEGATIVE CONTROL
   - Also: the observational OR for comparison (should be ~1.5)
   - Source: Jacobs et al. or Gianfrancesco et al. MR studies

5. MS-022: "Spinal cord atrophy predicts disability progression better than brain atrophy in MS"
   - Need: HR per SD of spinal cord volume/area loss for EDSS progression
   - Source: Kearney et al., Eshaghi et al., or Lukas et al.

6. MS-028: "Cladribine reduces relapse rate and disability progression via durable lymphocyte depletion"
   - Need: HR for 12-week confirmed disability progression from CLARITY trial
   - Also: ARR ratio (cladribine vs placebo) with 95% CI
   - Source: Giovannoni et al. 2010 NEJM (CLARITY trial)

7. MS-029: "Natalizumab reduces relapse rate by ~68% and disability progression by ~42%"
   - Need: HR for disability progression from AFFIRM trial
   - Also: rate ratio for ARR with 95% CI
   - Source: Polman et al. 2006 NEJM (AFFIRM trial)

8. MS-032: "Vascular/metabolic comorbidities accelerate MS disability progression"
   - Need: HR for EDSS progression in MS patients with vs without vascular comorbidity
   - Source: Marrie et al. or similar large MS comorbidity cohort

9. MS-040: "DMT discontinuation in older stable MS patients — relapse/progression risk"
   - Need: HR for relapse or progression after DMT discontinuation vs continuation
   - Source: DISCOMS trial, Kister et al., or Bsteh et al.

10. MS-025: "HERV-W envelope protein (MSRV) is associated with MS risk"
    - Need: OR for HERV-W/MSRV detection in MS vs controls
    - Source: Morandi et al. meta-analysis or Dolei et al.

IMPORTANT RULES:
- Only report the PRIMARY or MOST-ADJUSTED estimate with 95% CI
- If a claim is only supported by descriptive/narrative evidence with no quantitative ratio, say "no ratio-scale estimate available" — do NOT fabricate
- Include PMID for every estimate
- For RCTs, prefer intention-to-treat analysis
- For MR studies, prefer IVW (inverse-variance weighted) estimate
- Mark verdict_suggestion as one of: SUPPORTED, SUGGESTIVE, DISCONFIRMED, CONFLICTED
```

---

## PROMPT 3: New AD ratio-scale claims (expand from 11 to ~17 rows)

```
I am building a quantitative catalog of Alzheimer's disease mechanism claims with effect sizes. I need primary OR/HR/RR estimates WITH 95% CIs for the following AD claims. These come from a mechanistic validity audit.

FORMAT YOUR RESPONSE AS A CSV with columns:
case_id, claim, design, scale, estimate, ci_low, ci_high, n_cases, n_controls, population, PMID, source_paper, verdict_suggestion, notes

Here are the claims to extract:

1. AD-001: "Amyloid-beta accumulation is THE causal initiating event in Alzheimer's disease"
   - Need: OR or HR for amyloid-PET positivity predicting conversion to AD dementia in cognitively normal elderly
   - Source: Jack et al. (A/T/N framework validation), or Ossenkoppele et al.

2. AD-005: "Midlife modifiable risk factors (hypertension, diabetes, hearing loss, low education, obesity, smoking, depression, physical inactivity, excessive alcohol, air pollution, social isolation, TBI) causally raise dementia risk"
   - Need: population-attributable fraction (PAF) from Lancet Commission 2020/2024
   - Also: individual OR/HR for the top 3 factors (hearing loss, education, hypertension) if available with CIs
   - Source: Livingston et al. Lancet 2020 or 2024 update

3. AD-007: "Tau PET is a valid biomarker for the T axis of the ATN framework"
   - Need: HR for tau-PET positivity predicting cognitive decline
   - Source: Ossenkoppele et al. 2022 Nature Medicine or La Joie et al.

4. AD-008: "Neurodegeneration markers (hippocampal atrophy, NfL) predict progression"
   - Need: HR per SD of hippocampal volume for progression to AD dementia
   - Also: HR per SD of plasma NfL for cognitive decline
   - Source: Jack et al. or Mattsson-Carlgren et al.

5. AD-010: "Glial/neuroinflammation biomarkers (sTREM2, GFAP, YKL-40) form a 4th axis beyond ATN"
   - Need: HR or OR for elevated sTREM2 or GFAP predicting progression
   - Source: Morenas-Rodriguez et al. or Benedet et al.

6. AD-C3: "GLP-1 receptor agonists (semaglutide) — biomarker movement but no cognitive benefit"
   - Need: HR or treatment effect for semaglutide in AD/MCI trials
   - Also: the biomarker effect size (e.g., amyloid PET change) if quantified
   - Source: Nørgaard et al. 2022 Alzheimer's & Dementia, or EVOKE trial data

7. AD-005a: "Hearing loss is the single largest modifiable risk factor for dementia"
   - Need: HR or RR for hearing loss → dementia, with 95% CI
   - Source: Livingston et al. Lancet 2024, or Deal et al. ACHIEVE trial

8. AD-005b: "Type 2 diabetes increases Alzheimer's risk"
   - Need: OR or HR for T2D → AD, from meta-analysis
   - Source: Zhang et al. meta-analysis, or Cheng et al. MR study

IMPORTANT RULES:
- Only report PRIMARY/MOST-ADJUSTED estimate with 95% CI
- If a claim has no ratio-scale estimate (only descriptive), say "no ratio-scale estimate available"
- Include PMID
- Prefer meta-analyses over single studies
- For ATN biomarker claims, prefer longitudinal studies with cognitive decline as outcome
- Mark verdict_suggestion as: SUPPORTED, SUGGESTIVE, DISCONFIRMED, CONFLICTED
```

---

## After pasting each response back

Tell Claude:
"Here's the Perplexity response for batch [1/2/3]. Integrate into effect_sizes_v4.csv, re-run tier calibration, and update the forest plot."
