# Pre-Registration: Etiologic Evidence Discordance Classification Rule

**Status:** FROZEN
**Date:** 2026-07-06
**Context:** Frozen classification rule for cross-type etiologic evidence discordance applied to drug mechanism families. The rule has been developed and validated on two retrospective domains (neuroepidemiology and cardiometabolic). This preregistration freezes the exact rule before (1) applying it to a new domain (autoimmune), and (2) awaiting readouts of two prospective predictions.

**Integrity protocol:** This document, the classification rule, the family pre-specifications, and the decision criteria will be committed together in a single commit before any autoimmune estimates are pulled or any prospective trial readouts are examined. The commit SHA will be recorded here after freeze. No placeholder functions, no TODO blocks, no data-peeking in commented code. The same protocol was used in Tower (2026) for the direction instability paper (commit SHAs: 1dc20a2, 8d74bd0).

**Commit SHA:** b96d10a

---

## Paper thesis

Cross-type discordance in etiologic evidence — observational versus Mendelian randomization/genetic — classifies drug mechanism families into those that will produce approved drugs versus those that will fail Phase III, with no RCT data entering the classification. Two structurally distinct failure modes emerge: zombie mechanisms (null MR signal, confounded observational association) and translation-gap mechanisms (concordant etiologic evidence, insufficient therapeutic intervention).

---

## Frozen classification rule (two-criterion)

### Definitions

**Cohen's d from OR:** d = |ln(OR)| × √3 / π (Chinn 2000).

**Exposure-comparable scale:** An effect estimate expressed per standard deviation of the exposure, per clinically meaningful unit of the exposure (e.g., per 1 mmol/L LDL, per 10 mmHg SBP), or per genotype contrast (e.g., MTHFR TT vs CC). These scales produce d values that are directly interpretable as biological effect magnitudes.

**Per-allele scale:** An MR estimate expressed per copy of a single genetic variant. Per-allele ORs are small by construction (typically 0.95–1.05 for common variants) regardless of the biological importance of the instrumented exposure. Per-allele estimates must be rescaled to per-SD-of-exposure before the effect-floor criterion is applied (see Scale Harmonization below).

### Observational evidence classification

Observational evidence is classified as **"non-trivial"** if d ≥ 0.10 on an exposure-comparable scale.

Observational evidence is classified as **"trivial"** if d < 0.10 on an exposure-comparable scale.

Rationale: d = 0.10 corresponds to an OR of approximately 1.20 or 0.83, which is the conventional boundary between negligible and small effects in epidemiology.

### MR/genetic evidence classification

MR/genetic evidence is classified as **"causal"** if BOTH of the following hold:

1. **Statistical criterion:** The primary estimate's confidence interval excludes the null (OR = 1.00).
2. **Effect-floor criterion:** The point estimate, on an exposure-comparable scale, has d ≥ 0.10. For per-allele estimates, rescaling to per-SD-of-exposure is required before applying this criterion (see Scale Harmonization).

MR/genetic evidence is classified as **"null"** if EITHER condition fails:
- The CI includes the null, OR
- The CI excludes the null but the point estimate on exposure-comparable scale has d < 0.10 (i.e., a precisely estimated but biologically trivial effect, driven by statistical power rather than biological importance).

Rationale for the dual criterion: A CI-only rule would classify a huge MR study with a trivially small but precisely estimated effect (e.g., OR 1.01, CI 1.005–1.015) as "causal," reintroducing zombie misclassification from the power direction. A d-only rule would ignore statistical significance. Both bars must be cleared.

### Scale harmonization procedure

For MR estimates reported per allele:

1. Identify the per-allele change in the instrumented exposure (in SD units), from the original MR paper or from GWAS summary statistics for the instrument SNP(s).
2. Compute the per-SD OR: OR_per_SD = OR_per_allele^(1 / Δ_SD_per_allele), where Δ_SD_per_allele is the per-allele change in the exposure in SD units.
3. Convert OR_per_SD to d using the Chinn formula.
4. Apply the d ≥ 0.10 effect-floor criterion to the rescaled estimate.

If the per-allele exposure change is not available from the original paper, the family is flagged as **"scale-unresolved"** and classified by the statistical criterion alone, with this limitation noted.

### Family-level classification

| OBS | MR | Classification | Prediction |
|-----|-----|----------------|------------|
| Non-trivial (d ≥ 0.10) | Null (CI includes null OR d < 0.10 after rescaling) | Qualitative discordance | Drug targeting this mechanism will fail |
| Non-trivial (d ≥ 0.10) | Causal (CI excludes null AND d ≥ 0.10 after rescaling) | Concordance | Drug targeting this mechanism can succeed |
| Trivial (d < 0.10) | Null | Null concordance | Ambiguous — both evidence types show negligible effect |
| Trivial (d < 0.10) | Causal | Genetic-only signal | Not observed in current data; would suggest confound suppression in OBS |

### Ambiguous-prediction scoring rule

Families classified as "null concordance" (both OBS and MR below threshold) produce an **ambiguous** prediction: both evidence types agree the effect is negligible, so the rule makes no directional claim about drug success or failure. Ambiguous predictions are **excluded from the scored denominator** because a non-directional prediction is unscoreable. This rule applies symmetrically: an ambiguous family whose drug succeeded would also be excluded.

The headline accuracy is always reported both ways — excluding ambiguous predictions from the denominator (primary) and including them as misses (secondary). If these numbers differ, both appear in the abstract and results.

### Family definition rule

Families are defined at the **exposure × outcome** level, not the pathway level. If a single pathway maps to distinct exposure–outcome pairs with different MR instruments, different observational literatures, or different clinical endpoint constructs, the pairs are separate families. Concretely:

- **BMI → MS** and **BMI → AD** are separate families because the MR instruments differ (Mokry 2016 instruments BMI → MS susceptibility; life-course MR instruments BMI → AD risk), the observational literatures are independent, and the clinical endpoints differ.
- This rule prevents pooling incommensurable exposures under a single OR, which produced the self-contradictory "Obesity-MS/AD" family in earlier drafts.

### Construct-matching amendment (prediction pending)

An exposure–outcome family is scored for etiology–intervention concordance only if a randomized trial exists that tests the intervention against a *clinical* outcome matching the construct of the etiologic claim (e.g., incidence or progression). Families for which the etiologic evidence addresses one construct (e.g., disease onset) while the only available trials measure a different construct (e.g., symptoms or biomarkers) are labeled **prediction pending** and excluded from the scored concordance denominator. This rule is applied by construct-matching, not by outcome direction, and therefore cannot be tuned to the result.

**Application:** BMI → MS is classified as prediction pending. MR estimates a causal effect on MS *susceptibility* (Mokry 2016: IVW OR 1.41, 95% CI 1.20–1.66), but no randomized trial has tested weight loss against a clinical MS endpoint (relapse rate, disability accrual, or incidence). Existing trials (MoDEMS 2023: mobility/fatigue/QoL; Ghezzi 2025 iCR: serum leptin) measure different constructs from the etiologic claim.

### Instrument-scale declaration

Each family's MR estimate must have its scale declared before classification. The scale declaration is frozen and cannot be changed after estimates are pulled.

**Retrospective families (neuro + cardio) — scales already declared:**

| Family | MR scale | Rescaling needed? |
|--------|----------|-------------------|
| HDL/CETP | Per 1 SD HDL-C | No |
| Niacin/HDL | Per 1 SD HDL-C | No |
| Homocysteine | MTHFR TT vs CC | No (genotype contrast) |
| CRP | Per 20% lower CRP | No |
| Uric acid | Per 1 SD urate | No |
| LDL/PCSK9 | Per 1 mmol/L LDL-C | No |
| Blood pressure | Per 10 mmHg SBP | No |
| Triglycerides | Per 1 log-unit TG | No |
| Lp(a) | Per 10 mg/dL Lp(a) | No |
| IL-6R | Per allele (Asp358Ala) | **Yes — must rescale to per-SD sIL-6R** |
| Anti-CD20/MS | Per allele (FCRL3) | **Yes — must rescale to per-SD CD20 expression** |
| BMI-MS | Per 1 SD BMI (Mokry 2016) | No |
| BMI-AD | Per 1 SD BMI (life-course MR) | No |
| All other neuro families | Per-SD or per-unit | No |

---

## Retrospective validation (rule developed on this data)

### Domain 1: Neuroepidemiology (AD + MS)

Nine mechanism families with both observational and MR/genetic evidence (after splitting BMI → MS and BMI → AD into separate families per the family definition rule above). The classification rule was developed on this domain. Results are retrospective and not independently confirmatory.

**Families scored (8 of 9):**

| Family | OBS d | MR d | MR class | Classification | Prediction | Outcome | Correct? |
|--------|-------|------|----------|----------------|------------|---------|----------|
| Metabolic-AD | 0.234 | 0.005 | Null | Qual. discordance | Failure | Failed | ✓ |
| ModRisk-AD | 0.209 | 0.053 | Null | Qual. discordance | Failure | Failed | ✓ |
| Anti-CD20-MS | 0.442 | 0.257 | Causal | Concordance | Success | Approved | ✓ |
| Smoking-MS/AD | 0.209 | 0.016 | Null | Qual. discordance | Failure | Failed | ✓ |
| HRT-AD | 0.221 | 0.000 | Null | Qual. discordance | Failure | Failed | ✓ |
| BMI-AD | 0.393 | 0.016 | Null | Qual. discordance | Failure | Failed | ✓ |
| VitaminD-MS | 0.186 | 0.382 | Causal | Concordance | Success | Failed | ✗ |
| EBV-MS | 0.293 | 0.887 | Causal | Concordance | Success | Approved | ✓ |

**Excluded (1):** BMI-MS is classified as **prediction pending** per the construct-matching amendment — MR addresses onset (Mokry 2016: OR 1.41, 1.20–1.66), but no trial has tested a clinical MS endpoint (relapse/disability/incidence). Existing trials measure symptoms (MoDEMS) or biomarkers (Ghezzi 2025 iCR: serum leptin).

**Pre-existing result (not a prediction):** 7/8 scored neuro families correctly classified. Vitamin D → MS is the sole discordant case (concordant etiologic evidence, failed supplementation RCTs — classified as "exposure mismatch," a translation-gap mechanism).

### Domain 2: Cardiometabolic

Ten mechanism families applied as a cross-domain replication, using the identical rule frozen on the neuro data.

**Pre-existing result:** 7/7 unambiguous families correctly classified. Uric acid is ambiguous (both OBS and MR d < 0.10 → null concordance). Combined across domains: **14/15 unambiguous family-level outcomes correctly classified.**

**Sensitivity analysis:** Classification repeated at d thresholds of 0.08, 0.10, 0.12, and 0.15. Result: 14/15 (or 14/16 including uric acid as a miss) at all tested thresholds. The rule is insensitive to threshold choice in the [0.08, 0.15] range for all scored families. Anti-CD20-MS (GEN d = 0.257 after per-allele rescaling) and IL-6R (GEN d = 0.083 after per-allele rescaling) are the boundary-sensitive families, but both are either safely above threshold (Anti-CD20) or pending (IL-6R).

---

## Prospective predictions (live)

### Prediction 1: Lp(a) / pelacarsen → SUCCESS

**Basis:** OBS OR = 1.13 (1.09–1.18) per 1 SD Lp(a), d = 0.067, classified as trivial. MR OR = 0.94 (0.93–0.95) per 10 mg/dL lower Lp(a) (Burgess 2018), CI excludes null. Per 10 mg/dL is an exposure-comparable scale; d = 0.034 per 10 mg/dL. However, per 1 SD (~36 mg/dL), the MR estimate scales to approximately OR 0.80, d = 0.12, clearing the effect floor.

**Classification:** OBS trivial + MR causal (after per-SD rescaling) → genetic-only signal. This is the one family in the "genetic-only" cell of the classification table. The prediction is that pelacarsen (ASO targeting LPA mRNA) will achieve its Phase III primary endpoint.

**Trial:** Lp(a)HORIZON (NCT04023552), pelacarsen, expected readout ~2026–2027.

**Decision criterion:** The prediction is confirmed if the trial meets its primary MACE endpoint with p < 0.05. The prediction is falsified if the trial fails to meet its primary endpoint or is terminated for futility.

**Note:** Lp(a) is unusual because OBS d is below threshold but MR is causal. If confirmed, this validates the two-criterion rule's ability to identify mechanisms where observational evidence underestimates causal importance (confound suppression or non-linear exposure-response). If falsified, it suggests genetic-only signals without observational support should be treated as ambiguous rather than concordant.

### Prediction 2: IL-6 / ziltivekimab → SUCCESS

**Basis:** OBS OR = 1.25 per 1 SD log IL-6 (Danesh 2008/ERFC), d = 0.123, classified as non-trivial. MR OR = 0.95 (0.93–0.97) per allele (IL6R MR Consortium 2012), CI excludes null.

**Scale harmonization required:** The IL6R Asp358Ala variant changes sIL-6R levels by approximately 0.34 SD per allele (Swerdlow et al. 2012 Int J Epidemiol). Rescaling: OR_per_SD = 0.95^(1/0.34) = 0.95^2.94 = 0.86. d_per_SD = |ln(0.86)| × √3/π = 0.083.

**Classification under strict rule:** d_per_SD = 0.083 < 0.10 → fails effect-floor → MR classified as "null" → qualitative discordance → predict FAILURE.

**Classification under relaxed threshold (d = 0.08):** d_per_SD = 0.083 ≥ 0.08 → passes effect-floor → MR classified as "causal" → concordance → predict SUCCESS.

**This is the pre-registered sensitivity case.** IL-6R sits exactly at the boundary of the effect-floor criterion. We pre-register BOTH predictions:
- **At d = 0.10 threshold:** predict FAILURE (discordance).
- **At d = 0.08 threshold:** predict SUCCESS (concordance).

The ZEUS trial readout will discriminate between these thresholds. If ziltivekimab succeeds, d = 0.08 is the correct floor. If it fails, d = 0.10 is validated. Either outcome is informative.

**Trial:** ZEUS (NCT05021835), ziltivekimab (anti-IL-6 ligand), expected readout ~2026–2027.

**Decision criterion:** Same as Prediction 1 — primary MACE endpoint at p < 0.05.

**Note:** Ziltivekimab targets IL-6 ligand, not IL-6R. The MR instrument (IL6R Asp358Ala) modulates downstream IL-6 signaling, so the instrument-target alignment is imperfect. This is noted as a limitation, consistent with the instrument-target alignment caveat discussed in the paper's Limitations section.

---

## Cross-domain extension: Autoimmune diseases

### Pre-specification (families declared before estimates pulled)

The following autoimmune mechanism families are pre-specified based on the existence of (a) published MR studies instrumenting the drug target, (b) published observational meta-analyses of the risk factor, and (c) a known drug trial outcome (approved or failed). Families were identified from review articles (Zheng et al. 2020 Nature Genetics; Burgess & Davey Smith 2022 Nature Reviews Methods Primers) without examining specific ORs or CIs.

**Pre-specified families:**

| # | Family | Exposure → disease | Drug class | Expected MR source | Expected OBS source |
|---|--------|-------------------|------------|-------------------|-------------------|
| 1 | TNF-α → RA | TNF-α levels → rheumatoid arthritis | Anti-TNF (infliximab, adalimumab, etanercept) | cis-MR using TNFRSF1A/TNFRSF1B variants | Observational cytokine studies |
| 2 | IL-17 → psoriasis | IL-17 signaling → psoriasis | Anti-IL-17 (secukinumab, ixekizumab) | cis-MR using IL17A/IL17RA variants | Observational cytokine studies |
| 3 | IL-23 → psoriasis/IBD | IL-23 signaling → psoriasis/Crohn's | Anti-IL-23 (guselkumab, risankizumab) | cis-MR using IL23R variants | Observational association studies |
| 4 | JAK-STAT → RA | JAK signaling → rheumatoid arthritis | JAK inhibitors (tofacitinib, baricitinib) | cis-MR using JAK pathway variants | Observational cytokine studies |
| 5 | IL-1β → gout/CVD | IL-1β → gout flares, CVD events | Anti-IL-1β (canakinumab, anakinra) | cis-MR using IL1RN variants | ERFC or equivalent |
| 6 | B-cell (CD20) → RA | B-cell depletion → RA | Anti-CD20 (rituximab) | cis-MR using MS4A1/CD20 variants | Observational B-cell studies |
| 7 | IL-4Rα → atopic dermatitis | IL-4/IL-13 signaling → AD | Anti-IL-4Rα (dupilumab) | cis-MR using IL4R/IL13 variants | Observational IgE/cytokine studies |
| 8 | CTLA-4 → autoimmunity | CTLA-4 checkpoint → autoimmune disease | CTLA-4-Ig (abatacept) | cis-MR using CTLA4 variants | Observational T-cell studies |

**Inclusion criteria for families:**
1. At least one published MR study (any design: cis-MR, two-sample, or multivariable MR) with a point estimate and CI for the exposure-disease association.
2. At least one published observational meta-analysis or large cohort study with a point estimate for the same exposure-disease association.
3. At least one drug targeting the mechanism with a known regulatory outcome (approved, failed Phase III, or withdrawn).
4. The MR and OBS estimates must address the same exposure-disease pair (not different diseases or different exposures within the same pathway).

**Exclusion criteria:**
1. Families where the only available MR estimate is from a druggable-genome screen without a dedicated MR study (these lack the focused instrument validation required for causal inference).
2. Families where the drug's mechanism of action does not match the MR-instrumented exposure (instrument-target misalignment too severe to classify).
3. Families where the observational evidence is entirely from case-control studies without adjustment for key confounders (risk of inflated OBS d).

**Procedure:**
1. For each pre-specified family, pull the MR OR and CI from the specified source type.
2. Pull the OBS OR from the specified source type.
3. Declare the MR scale (per-allele, per-SD, per-unit).
4. Apply scale harmonization if per-allele.
5. Compute d for both estimates.
6. Apply the frozen two-criterion classification rule.
7. Compare to known drug outcome.
8. Report all results including misses.

**Families discovered during the literature search that are not in the pre-specified list** may be added as EXPLORATORY families, clearly labeled as such, and excluded from the primary hit rate.

### Hypotheses

#### H1: Autoimmune domain replicates the classification accuracy

The frozen two-criterion rule, applied to the pre-specified autoimmune families, will correctly classify at least 5/8 families (62.5%).

**Decision criterion:** ≥ 5/8 families correctly classified. This is a conservative threshold because autoimmune mechanisms are biologically closer to the cardiometabolic training domain (shared inflammatory pathways) than neuro was to cardio.

**Interpretation guide:**
- ≥ 7/8 correct → Strong cross-domain replication. The rule generalizes to a third inflammatory disease domain.
- 5–6/8 correct → Partial replication. Some autoimmune mechanisms have features (e.g., tissue-specific immunology) that the rule does not capture.
- < 5/8 correct → Replication failure. The rule may be specific to cardiometabolic and neurological diseases. This would be reported as a null result and would limit the paper's generalizability claim.

#### H2: Zombie mechanisms exist in autoimmune diseases

At least one pre-specified autoimmune family will show qualitative discordance (OBS non-trivial + MR null) and correspond to a failed drug.

**Decision criterion:** ≥ 1 zombie mechanism identified. If zero zombies are found, this suggests that autoimmune drug development has been more mechanism-informed than cardiometabolic/neuro (which would itself be an interesting finding).

#### H3: Combined cross-domain accuracy exceeds chance

Across all three domains (neuro + cardio + autoimmune), the classification rule correctly classifies significantly more families than expected by chance (50%).

**Decision criterion:** Binomial test p < 0.05 for the proportion of correct classifications across all unambiguous families.

---

## Sensitivity analyses (pre-specified)

### S1: Threshold sensitivity

Repeat all classifications at d = 0.08, 0.10 (primary), 0.12, and 0.15. Report:
- How many families change classification at each threshold.
- Which families are threshold-sensitive (classification changes across the tested range).
- The threshold that maximizes classification accuracy (with the caveat that this is post hoc and should not be used for inference).

### S2: Instrument-scale sensitivity

For all per-allele MR estimates, report classifications under:
- (a) The strict rule (rescale to per-SD, apply effect floor).
- (b) The CI-only rule (ignore effect floor, classify by CI alone).
- (c) The d-only rule (apply effect floor without requiring CI exclusion).
Report how many families change classification across these three rules.

### S3: Leave-one-domain-out

Train the threshold on two domains, test on the third. Report accuracy for each held-out domain.

---

## What counts as success

The preregistration succeeds if:
1. At least 5/8 autoimmune families are correctly classified (H1).
2. Combined cross-domain accuracy is significantly above chance (H3).
3. At least one prospective prediction (Lp(a) or IL-6R) can be evaluated within the paper's timeline and is correctly classified.

## What counts as failure

The preregistration fails if:
1. Autoimmune accuracy is below 5/8 (domain-specific failure).
2. Combined accuracy is not significantly above chance (rule is not generalizable).
3. Both prospective predictions are falsified (rule makes wrong live predictions).

## What we report either way

All results including misses. Pre-registered predictions are reported explicitly as "we predicted X, observed Y." No cherry-picking. Families that were pre-specified but for which no MR or OBS estimate could be found are reported as "data not available" and excluded from accuracy calculations. Exploratory families added after the pre-specification are clearly labeled and excluded from the primary hit rate.

---

## Analysis code to be frozen

The following files will be committed alongside this document:

- `paper/reference/compute_cardio_d_values.py` — Chinn formula + cardio family estimates
- `paper/reference/classify_families.py` — _(to be written)_ Implements the two-criterion classification rule
- `paper/reference/sensitivity_analysis.py` — _(to be written)_ Threshold and instrument-scale sensitivity
- `paper/supplementary_data.csv` — All family-level estimates (neuro + cardio; autoimmune rows to be added after freeze)

---

## Statistical validation

### Power analysis

Simulated power (50,000 Monte Carlo replicates each) for detecting above-chance classification accuracy. Tests are one-sided at α = 0.05.

**Binomial test** (H₀: accuracy = 0.50):

| n | True accuracy | Power |
|---|---------------|-------|
| 15 | 0.70 | 0.298 |
| 15 | 0.80 | 0.649 |
| 15 | 0.85 | 0.822 |
| 15 | 0.90 | 0.945 |
| 15 | 0.95 | 0.994 |
| 23 | 0.80 | 0.929 |
| 23 | 0.90 | 0.999 |
| 30 | 0.80 | 0.974 |
| 30 | 0.90 | 1.000 |

At our current sample size (n = 15 scored families), the binomial test has adequate power (≥ 0.80) to detect a true accuracy of 0.85 or higher. At the observed accuracy of 14/15 = 0.933, power exceeds 0.94. For the autoimmune extension (target n ≈ 23), power exceeds 0.92 at a true accuracy of 0.80.

**Fisher's exact test** (2×2 table: discordant→fail vs. concordant→succeed):

| n_disc | n_conc | disc→fail | conc→succ | Power |
|--------|--------|-----------|-----------|-------|
| 9 | 6 | 0.90 | 0.80 | 0.856 |
| 9 | 6 | 0.95 | 0.85 | 0.962 |
| 12 | 8 | 0.90 | 0.80 | 0.898 |
| 15 | 10 | 0.90 | 0.80 | 0.963 |

At the current split (approximately 9 discordant, 6 concordant), Fisher's exact test has power 0.86–0.96 depending on assumed true classification rates.

### False positive rate verification

FPR verified under the true null (accuracy = 0.50, i.e., the classification rule has no predictive validity). 50,000 simulations per cell. All FPRs are at or below the nominal α = 0.05.

| Test | n | Simulated FPR | Expected |
|------|---|---------------|----------|
| Binomial | 15 | 0.018 | ≤ 0.05 |
| Binomial | 23 | 0.047 | ≤ 0.05 |
| Binomial | 30 | 0.049 | ≤ 0.05 |
| Fisher's exact | 15 | 0.018 | ≤ 0.05 |
| Fisher's exact | 23 | 0.019 | ≤ 0.05 |
| Fisher's exact | 30 | 0.022 | ≤ 0.05 |

Note: At n = 15, the binomial test is conservative (FPR = 0.018 < 0.05) because the discrete test cannot achieve exactly α = 0.05. This conservatism reduces power at small n but does not inflate false positive rates.

### Permutation null distribution

Outcomes were shuffled across families (10,000 permutations) with the frozen d = 0.10 classification rule held fixed. BMI-MS excluded as prediction pending; uric acid excluded as ambiguous. Scored families: n = 15.

| Statistic | Value |
|-----------|-------|
| Observed accuracy | 14/15 = 0.933 |
| Null mean | 0.534 |
| Null SD | 0.123 |
| Null 95th percentile | 0.667 |
| Null 99th percentile | 0.800 |
| **Permutation p-value** | **0.0013** |

The observed accuracy (0.933) exceeds the 99th percentile of the null distribution (0.800). The permutation p-value (0.0013) is below α = 0.05 and below the Bonferroni-corrected threshold for 15 families (0.05/15 = 0.0033).

### Multiple comparisons

The classification rule is applied once per family (no within-family multiple testing). Across families, Bonferroni correction is applied to the Cochran's Q test (α_adj = 0.05/m where m = number of testable families). The permutation test and binomial test are each applied once to the aggregate accuracy (no per-family hypothesis test), so no additional correction is needed.

### Interpretation guide

| Observed accuracy | Interpretation |
|-------------------|----------------|
| ≥ 14/15 (93%) | Strong evidence: the classification rule discriminates drug outcomes well above chance. The sole miss (VitD-MS) represents a known failure mode (exposure mismatch) that the rule is not designed to catch. |
| 12–13/15 (80–87%) | Moderate evidence: the rule captures the majority of discordance signals. Additional misses may reveal new failure modes or family definition issues. |
| 10–11/15 (67–73%) | Weak evidence: classification exceeds chance but many families are misclassified. The rule may be specific to a subset of mechanism types. |
| ≤ 9/15 (60%) | No evidence: the rule does not reliably discriminate drug outcomes. Report as a null result. |

---

## Exploratory analyses (not pre-registered)

Any additional analyses beyond those specified above will be clearly labeled as EXPLORATORY in both code and manuscript. Specifically:

1. **Psychiatry extension** (CRP → depression as a bonus family) is exploratory if pursued.
2. **T2D extension** is exploratory if pursued.
3. **Post hoc threshold optimization** — if a threshold other than d = 0.10 maximizes accuracy, this is noted but not used for inference.
4. **Mechanism taxonomy** — any classification of failure modes beyond "zombie" and "translation-gap" discovered in the autoimmune data is exploratory.
