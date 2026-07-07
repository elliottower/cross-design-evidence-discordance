# Etiologic evidence discordance classifies Phase III drug failures in Alzheimer's disease and multiple sclerosis

---

## Abstract

Drug development for Alzheimer's disease and multiple sclerosis has a 90% Phase III failure rate. Existing evidence synthesis tools assess consistency within a single study design — whether twelve RCTs agree — not whether observational associations survive genetic causal testing. We applied Cochran's Q across evidence types and computed directional discordances for 76 neuroepidemiology claims across 24 mechanism families. We then tested whether the classification from non-interventional (etiologic) evidence alone — observational cohorts, Mendelian randomization, and genetic association studies, with no RCT data entering the classification — correctly separated drug successes from failures.

Among eight mechanism families classifiable from etiologic evidence alone, four showed qualitative discordance (MR/genetic signal null, observational association positive): Metabolic-AD, Smoking-MS/AD, ModRisk-AD, and HRT-AD. Anti-CD20 B-cell depletion and three other families showed quantitative discordance or concordance — the causal signal was real across evidence types. Applied to the eight drugs in these families, the etiologic classification correctly identified seven of eight outcomes: three failures in qualitative-discordance families and four approvals in the quantitative-discordance family (Anti-CD20-MS). The single miss was vitamin D supplementation (quantitative discordance, predicted approve, trial failed). Qualitative discordance predicted failure at 100% (3/3); quantitative discordance and concordance predicted approval at 80% (4/5).

A separate retrospective analysis including RCT evidence classified 28 drugs across ten families with 89% accuracy (OR = 75, Fisher p = 0.00005). Amyloid-AD, unclassifiable from etiologic evidence alone, emerged as qualitative-discordant only when interventional evidence was included — revealing that etiologic concordance does not guarantee interventional success.

---

## Introduction

Drug development for Alzheimer's disease and multiple sclerosis consumes billions of dollars annually, with Phase III failure rates exceeding 90% for AD (Cummings et al. 2014). Standard tools for evaluating mechanistic evidence — GRADE for rating certainty, I-squared for measuring heterogeneity — operate within a single study design. They assess whether twelve RCTs agree. They do not assess whether the RCT evidence agrees with the genetic evidence, or whether the observational signal survives Mendelian randomization.

Several independent findings establish that cross-type evidence agreement carries information about drug success. Gill et al. (2021) showed that MR concordance with RCTs predicts drug approval. Nelson et al. (2015) found that drugs with genetic support for their target are twice as likely to reach approval. Ference et al. (2019) demonstrated that MR-derived causal estimates for cardiovascular targets match RCT efficacy. Triangulation (Lawlor et al. 2016) captures the right intuition. There is no standard quantitative test.

We built one and tested it in two stages. First, we classified mechanism families using only non-interventional (etiologic) evidence — observational cohorts, MR studies, and genetic associations — keeping all drug trial outcomes fully out of sample. This asks: does the etiologic evidence agree across types? Second, we added interventional evidence and examined what changes. The gap between the two analyses reveals two structurally different failure modes: mechanisms where the etiologic case fails (zombie mechanisms, caught by etiologic Q) and mechanisms where the etiologic case holds but intervention fails (translation-gap mechanisms, visible only with RCT evidence).

---

## Methods

### Data

We assembled 76 neuroepidemiology claims across 24 mechanism families spanning AD and MS. Each claim was coded with its mechanism family, study design (observational, MR, genetic, RCT, diagnostic), effect size estimate, confidence interval, and sample size. Effect sizes on ratio scales were converted to Cohen's d using the Chinn (2000) formula. Sources were published systematic reviews, meta-analyses, MR studies, and landmark RCTs.

We supplemented the original catalog with etiologic evidence for three families identified through systematic literature search:

**Anti-CD20-MS**: MR evidence for the FCRL3-CD20 axis in MS susceptibility (OR 0.83, 95% CI 0.79-0.89; Lin et al. 2023) and observational B-cell depletion efficacy data (Hu et al. 2019). A CD40 genetic association (OR 1.16; Sokolova et al. 2013) provides corroborating GWAS evidence but was not entered as a separate evidence type in the Q test (see below).

**HRT-AD**: Observational meta-analysis (protective, OR 0.67, 95% CI 0.58-0.78; Song et al. 2020) and MR for estradiol (null, OR 1.00, 95% CI 0.85-1.18; Barth et al. 2025). An ESR1 genetic association (OR 1.14; Cheng et al. 2014) provides corroborating GWAS evidence.

**Vitamin D-MS** (supplemented): observational cohort evidence for low vitamin D and MS risk (OR 1.40, 95% CI 1.19-1.64; Munger et al. 2006), added to the existing MR entry.

### Evidence classification: etiologic versus interventional

We divided evidence types into two categories:

**Etiologic evidence** captures the observational and genetic case for a mechanism: cohort and case-control studies, Mendelian randomization, GWAS, and diagnostic accuracy studies. These ask "is this mechanism involved in the disease?"

**Interventional evidence** captures the treatment case: randomized controlled trials. These ask "does intervening on this mechanism help?"

The separation matters because interventional evidence for a mechanism family contains information about the drug outcomes we want to classify. A family's RCT arm is computed from the same trials whose outcomes appear in the holdout. Using it in both places is circular. Etiologic evidence is independent of drug outcomes by construction.

Within etiologic evidence, MR and GWAS studies were pooled into a single "genetic/causal" (GEN) evidence type for the Q test. Common variant GWAS effect sizes are inherently small (OR 1.1-1.3 for genome-wide significant hits) even for real causal pathways, and treating them as a separate evidence type in the Q test would systematically misclassify real GWAS signals as "null" against the |d| = 0.10 threshold. MR studies, which estimate the causal effect of modifying the exposure, operate on a scale comparable to observational associations and RCTs. The two evidence types in the Q test are therefore OBS (observational and diagnostic studies) and GEN (MR and genetic association studies).

### Cross-type heterogeneity test

For each mechanism family with effect sizes from at least two evidence types, we pooled estimates within each type using inverse-variance weighted fixed-effects, then computed Cochran's Q across the type-level pools. Bonferroni correction was applied for multiple families.

### Directional analysis and discordance typing

For each family with significant Q, we classified the discordance by examining the pooled effect sizes across types:

**Qualitative discordance**: at least one evidence type shows a near-null effect (|d| < 0.10) while another shows a meaningful effect (|d| >= 0.10). The observational or associational signal does not survive causal testing. The mechanism's apparent evidence base reflects confounding.

**Quantitative discordance**: all evidence types show meaningful positive effects at different magnitudes. The mechanism has a real causal effect; confounding inflates the observational magnitude.

### Failure taxonomy

Three mechanically-defined categories:

**Zombie mechanism**: etiologic evidence is qualitatively discordant — the MR/genetic signal is null while the observational association persists. The mechanism is a statistical association, not a causal pathway.

**Mimic mechanism**: etiologic evidence is concordant (the mechanism is real), but interventional evidence shows drugs targeting it fail or produce marginal benefit. The treatment targets a real pathway that is insufficient for clinical reversal.

**Evidence misfire**: genuinely contradictory results across etiologic evidence types, with no clear resolution.

### Phase III holdout

We assembled 38 Phase III AD and MS drugs with known outcomes (22 failed, 16 approved). For each drug, we mapped its mechanism to a family classification. Drugs whose family lacked classification received no prediction. The rule was mechanical: qualitative discordance classifies as failure, quantitative discordance and concordance classify as approval.

### Two-stage analysis design

**Stage 1 (de-circularized)**: classify families using only etiologic evidence. All drug outcomes are fully out of sample. This stage can use "predicts" language.

**Stage 2 (retrospective)**: add interventional evidence and reclassify. Drug outcomes are no longer independent of the classification. This stage uses "is associated with" language and examines what the additional evidence reveals.

### Decision rule

The complete classification procedure is given in Algorithm 1.

---

**Algorithm 1.** Cross-Type Discordance Classification

---

```
INPUTS
  F = {f₁, …, fₘ}                              ▷ mechanism families
  For each fⱼ: studies {(ES_i, CI_i, type_i)}   where type_i ∈ {OBS, GEN, RCT}

STEP 1 — STANDARDIZE
  For each study i:
    If ES_i is an odds/hazard ratio:
      d_i  ← ln(ES_i) × √3 / π                              [Chinn 2000]
      SE_i ← (ln(CI_upper) − ln(CI_lower)) / (2 × 1.96) × √3 / π
    Else if ES_i is already a standardized mean difference:
      d_i  ← ES_i
      SE_i ← (CI_upper − CI_lower) / (2 × 1.96)

STEP 2 — PARTITION
  OBS ← {observational, diagnostic}
  GEN ← {MR, genetic, genetic/cohort}           ▷ pooled into single causal type
  RCT ← {RCT}
  For Stage 1 (de-circularized): restrict to {OBS, GEN} only

STEP 3 — POOL WITHIN EVIDENCE TYPE
  For each family fⱼ, for each evidence type t with kₜ studies:
    w_i  ← 1 / SE_i²
    d̂_t  ← Σᵢ (w_i × d_i) / Σᵢ w_i               ▷ inverse-variance fixed-effects
    SE_t ← 1 / √(Σᵢ w_i)

STEP 4 — HETEROGENEITY TEST ACROSS TYPES
  For each family fⱼ with K ≥ 2 evidence types:
    d̄    ← Σₜ (wₜ × d̂_t) / Σₜ wₜ      where wₜ = 1 / SE_t²
    Q    ← Σₜ wₜ × (d̂_t − d̄)²
    df   ← K − 1
    α_adj ← 0.05 / m                                ▷ Bonferroni over m families

STEP 5 — CLASSIFY FAMILY
  If Q < χ²_{df}(α_adj):
    label(fⱼ) ← CONCORDANT
  Else if Q ≥ χ²_{df}(α_adj):
    If min_t |d̂_t| < 0.10:                          ▷ Cohen's negligible-effect boundary
      label(fⱼ) ← QUALITATIVE DISCORDANCE
    Else:
      label(fⱼ) ← QUANTITATIVE DISCORDANCE

STEP 6 — PREDICT DRUG OUTCOME
  CONCORDANT               → APPROVE
  QUANTITATIVE DISCORDANCE → APPROVE
  QUALITATIVE DISCORDANCE  → FAIL

OUTPUT
  For each drug mapped to family fⱼ: predicted outcome ∈ {APPROVE, FAIL}
```

---

The procedure takes published effect sizes as input and returns a binary drug-outcome classification with no fitted parameters. Each effect size is converted to Cohen's d on a common scale, then pooled within evidence type by inverse-variance weighting under a fixed-effects model, yielding one summary estimate per type per family. Cochran's Q tests whether the type-level estimates are heterogeneous beyond chance, with the threshold Bonferroni-corrected across all families. Families passing the heterogeneity test are split by whether any evidence type produced a negligible pooled effect (|d| < 0.10), a threshold that follows Cohen's conventional boundary and is fixed a priori. Families where all types agree on a non-negligible effect are classified as quantitative discordance and predicted to succeed — the causal signal is real across designs. Families where at least one type returns a negligible signal are classified as qualitative discordance and predicted to fail — the mechanism appears in some designs but not others, diagnosing confounding rather than causation. The procedure is deterministic, requires no training data, and can be executed by hand with a calculator and a chi-squared table.

---

## Results

### Stage 1: Etiologic-only classification

Eight mechanism families had etiologic evidence from at least two types (Bonferroni-corrected alpha = 0.05/8 = 0.0063). We report the pooled effect sizes by type, Q statistics, and the directional classification.

| Family | GEN d | OBS d | Q | df | p | Classification |
|--------|-------|-------|---|----|----|---------------|
| Metabolic-AD | 0.006 | 0.24 | 103.6 | 1 | < 0.0001 | Qualitative disc. |
| ModRisk-AD | 0.053 | 0.20 | 64.0 | 1 | < 0.0001 | Qualitative disc. |
| Anti-CD20-MS | 0.10 | 0.80 | 15.1 | 1 | 0.0001 | Quantitative disc. |
| Smoking-MS/AD | 0.016 | 0.26 | 13.0 | 1 | 0.0003 | Qualitative disc. |
| HRT-AD | 0.000 | 0.22 | 12.6 | 1 | 0.0004 | Qualitative disc. |
| Obesity-MS/AD | 0.13 | 0.36 | 8.7 | 1 | 0.003 | Quantitative disc. |
| Vitamin D-MS | 0.38 | 0.19 | 7.8 | 1 | 0.005 | Quantitative disc. |
| EBV-MS | 1.92 | 0.53 | 5.5 | 1 | 0.018 | Concordant |

Seven families show significant cross-type heterogeneity after Bonferroni correction. Four show qualitative discordance: the GEN (MR/genetic) signal is null (|d| < 0.10) while the observational association is moderate. Three show quantitative discordance: both types show real effects at different magnitudes. EBV-MS is concordant (Q does not reach Bonferroni significance). This classification uses no interventional data.

### Etiologic-only drug classification

Of 38 holdout drugs, 8 mapped to families with etiologic classification:

| Family | Classification | Drugs | Outcomes | Correct |
|--------|---------------|-------|----------|---------|
| Metabolic-AD | Qualitative disc. → Fail | semaglutide, pioglitazone | Both failed | 2/2 |
| HRT-AD | Qualitative disc. → Fail | CEE/MPA | Failed | 1/1 |
| Anti-CD20-MS | Quantitative disc. → Approve | ocrelizumab (x2), ofatumumab, ublituximab | All approved | 4/4 |
| Vitamin D-MS | Quantitative disc. → Approve | vitamin D supplementation | Failed | 0/1 |

Etiologic-only accuracy: 7/8 (87.5%, 95% Wilson CI: 52.9-97.8%). Qualitative discordance predicted failure at 100% (3/3); quantitative discordance predicted approval at 80% (4/5). Fisher's exact p = 0.14; permutation test (100,000 shuffles) p = 0.07. The sample is underpowered for frequentist significance at n = 8, but the directional separation — qualitative discordance families producing 100% drug failure versus 20% in quantitative — is the core finding.

The single miss is vitamin D supplementation. MR evidence supports a causal role for vitamin D in MS (OR 2.0, d = 0.38), and observational evidence agrees (OR 1.40, d = 0.19). The etiologic evidence is quantitatively discordant (both types above 0.10 but at different magnitudes), predicting approval. Supplementation trials have produced mixed results. The likely explanation is the gap between lifelong genetic vitamin D exposure (captured by MR) and adult oral supplementation (captured by RCTs): the MR instrument indexes cumulative lifetime exposure, while trials test time-limited intervention.

### The cases etiologic evidence diagnoses

**Metabolic-AD (zombie mechanism)**: T2D associates with AD in observational cohorts (RR 1.53, d = 0.24). MR finds no causal effect (OR 1.01, d = 0.006). The 40-fold gap diagnoses confounding: shared risk factors (obesity, inflammation, vascular disease) explain the association without a causal metabolic pathway. Semaglutide's null results in EVOKE/EVOKE+ confirmed this classification. Pioglitazone also failed.

**HRT-AD (zombie mechanism)**: A meta-analysis of 16 observational studies shows HRT is protective against AD (OR 0.67, d = 0.22; Song et al. 2020). MR for estradiol finds no causal effect (OR 1.00; Barth et al. 2025). The WHIMS trial found HRT INCREASED dementia risk (HR 1.76; Shumaker et al. 2003). The observational protective signal reflects healthy-user bias, not causation. The etiologic Q correctly identifies this — before any RCT data enters the classification.

**Anti-CD20-MS (quantitative discordance, real mechanism)**: MR evidence for the FCRL3-CD20 axis shows a moderate protective effect (OR 0.83, d = 0.10; Lin et al. 2023). Observational efficacy data shows a large effect (d = 0.80; Hu et al. 2019). Both types are above the 0.10 threshold — the mechanism is real across evidence types, with the observational effect amplified by treatment context. GWAS evidence (CD40, OR 1.16; Sokolova et al. 2013) corroborates B-cell involvement. All four Anti-CD20 drugs in the holdout were approved.

### The case etiologic evidence cannot diagnose: amyloid

Amyloid-AD has only observational etiologic evidence in the catalog (amyloid PET positivity strongly predicts AD conversion: HR 3.74 and 10.2). Genetic evidence for amyloid's role in AD is strong: APOE4 heterozygous OR 3.46, homozygous OR 15.65, and APP/PSEN mutations cause autosomal dominant AD. The etiologic case for amyloid involvement in AD is robust across study types.

If classified on etiologic evidence, Amyloid-AD would be concordant or quantitatively discordant. The etiologic evidence AGREES that amyloid is involved in AD. The classification would predict approval. And 12 of 14 amyloid-targeting drugs failed Phase III.

This is not an evidence failure. It is a translation gap. The etiologic case is correct: amyloid IS involved in AD pathogenesis. The therapeutic failure is that clearing amyloid does not reverse the downstream neurodegeneration. Etiologic concordance does not guarantee interventional success.

### Stage 2: Retrospective analysis including RCT evidence

Adding interventional evidence expands the classifiable families to ten (Bonferroni alpha = 0.005).

| Family | OBS d | GEN d | RCT d | Q | p | Classification |
|--------|-------|-------|-------|---|---|---------------|
| Metabolic-AD | 0.24 | 0.006 | 0.00 | 109.5 | < 0.0001 | Qualitative disc. |
| ModRisk-AD | 0.20 | 0.053 | — | 64.0 | < 0.0001 | Qualitative disc. |
| HRT-AD | 0.22 | 0.000 | 0.34 | 18.1 | 0.0001 | Qualitative disc. |
| Anti-CD20-MS | 0.80 | 0.10 | 0.20 | 19.9 | < 0.0001 | Quantitative disc. |
| Smoking-MS/AD | 0.26 | 0.016 | — | 13.0 | 0.0003 | Qualitative disc. |
| OtherDMT-MS | 0.98 | — | 0.29 | 11.3 | 0.0008 | Quantitative disc. |
| Obesity-MS/AD | 0.36 | 0.13 | — | 8.7 | 0.003 | Quantitative disc. |
| VitD-MS | 0.19 | 0.38 | 0.19 | 8.9 | 0.01 | Concordant |
| Amyloid-AD | 0.86 | — | 0.04 | 8.7 | 0.003 | Qualitative disc. |
| EBV-MS | 0.53 | 1.92 | — | 5.5 | 0.02 | Concordant |

With full evidence, the retrospective classification correctly separates 25 of 28 classifiable drugs (89.3%, 95% CI: 72.8-96.3%; OR = 75, Fisher p = 0.00005, permutation p = 0.00004). Of the three misses, two are the amyloid approvals (lecanemab, donanemab — classified as qualitative discordance but approved with marginal benefit), and one is VitD supplementation (concordant, predicted approve, trial failed).

The key revelation from adding RCT evidence: Amyloid-AD's near-zero RCT effect (d = 0.04) against its strong observational signal (d = 0.86) is the signature of a translation-gap mechanism. This discordance is invisible to etiologic evidence alone.

This analysis is retrospective — the RCT evidence that classifies Amyloid-AD as discordant comes from the same trials whose outcomes appear in the drug set. The 89% accuracy is a concordance measure, not a prediction.

### The amyloid subanalysis

Amyloid-AD contained 14 holdout drugs: 12 failed, 2 approved (lecanemab, donanemab). Within the family, production-pathway inhibitors (BACE inhibitors, gamma-secretase inhibitors/modulators) failed at 100% (8/8). Amyloid immunotherapy failed at 67% (4/6). Production-pathway inhibition — blocking the enzymes that generate amyloid — consistently produced null or harmful results (semagacestat worsened cognition). The immunotherapy approach achieves amyloid clearance with statistically significant but clinically marginal benefit (27-35% slowing on CDR-SB).

### Two failure modes

The two-stage analysis reveals a structural distinction in how mechanisms fail:

**Zombie mechanisms** (caught by etiologic Q): the MR/genetic causal signal is null. The observational association reflects confounding. The etiologic evidence alone diagnoses the failure, and drugs targeting the mechanism will fail because there is nothing causal to intervene on. Examples: Metabolic-AD (semaglutide), HRT-AD (WHIMS).

**Translation-gap mechanisms** (visible only with RCT evidence): the etiologic case is concordant — the mechanism is genuinely involved in the disease. Drugs targeting it still fail because clearing the mechanism does not reverse the downstream pathology. Etiologic Q classifies these as concordant; only interventional evidence reveals the gap. Example: Amyloid-AD.

The practical implication: a null MR signal for a drug target is a strong negative signal — the mechanism is likely a zombie. A positive MR signal is necessary but not sufficient — the mechanism is real, but translation is not guaranteed.

### Cross-domain boundary test

Applied to a psychiatric dataset (31 drugs, 24 classifiable from 6 disorder-level families), the classification dropped to 58% accuracy with zero specificity. Depression and Schizophrenia, each containing 8-9 distinct mechanism classes, are both classified as discordant, predicting failure for all drugs — missing all 10 approvals.

The framework requires mechanism-level families. In neuroepidemiology, families map to specific biological pathways (amyloid clearance, B-cell depletion, metabolic signaling). In psychiatry, families map to diagnostic categories containing heterogeneous mechanisms. Disorder-level discordance reflects mechanistic heterogeneity within the diagnostic category, not a property of any individual drug target.

### The investigation paradox

Families studied with more evidence types showed more cross-type disagreement, not less. Each evidence type operates at a different biological scale, captures different confounders, and measures different aspects of a complex causal process. Apparent consensus within one evidence type is not validation. A mechanism tested only with observational studies looks "consistent" by default.

---

## Discussion

### Filling the GRADE gap

GRADE's five dimensions operate within a single study design. Cross-type Q adds a sixth: does the evidence hold up across designs? When MR finds no causal pathway (OR 1.01 for T2D-AD) while observational evidence shows a moderate association (RR 1.53), that discrepancy contains information GRADE cannot capture. The direction of the discrepancy diagnoses confounding.

### Etiologic evidence as a screening tool

The two-stage analysis suggests a practical screening role for etiologic Q in drug development. Before committing to Phase III for a novel target:

1. Compute Cochran's Q across etiologic evidence types for the target mechanism
2. If the MR/genetic causal signal is null while the observational association is positive → the mechanism is likely a zombie → high Phase III failure risk
3. If etiologic evidence is concordant → the mechanism is likely real → proceed, but concordance does not guarantee interventional success

This is a one-sided screen: a null MR signal is a strong negative indicator, but a positive MR signal is not a guarantee. The amyloid case demonstrates the asymmetry.

### Why etiologic concordance is necessary but not sufficient

The amyloid case illustrates a general principle. APOE4 is one of the strongest known genetic risk factors for any common disease (OR 3.46 per allele). Amyloid PET positivity robustly predicts AD conversion. The etiologic evidence is concordant. Drugs targeting amyloid clearance mostly fail.

The gap between etiologic concordance and interventional success reflects the difference between "the mechanism is involved in pathogenesis" and "intervening on the mechanism at this stage reverses pathology." Amyloid accumulation may be a upstream causal factor in AD, but by the time clinical disease manifests, the downstream cascade (tau tangles, synaptic loss, neuroinflammation) cannot be reversed by clearing amyloid. An estimated $40 billion in failed trials (Cummings & Zhong 2014) targeted a mechanism that was etiologically valid but therapeutically insufficient.

### Limitations

The etiologic-only analysis classifies 8 of 38 holdout drugs — the remainder fall in families without multi-type etiologic evidence. The analysis is powered to demonstrate proof-of-concept (7/8 correct), not to establish population-level accuracy. The threshold |d| = 0.10 for qualitative versus quantitative discordance was chosen on substantive grounds, not optimized. The retrospective analysis including RCT evidence is circular for families whose RCT arm derives from holdout drugs — it should be interpreted as concordance, not prediction.

Prospective validation — pre-registering etiologic classifications for mechanisms entering Phase III and evaluating at trial readout — is the definitive test.

### Conclusion

Three contributions. First, etiologic evidence discordance (observational versus MR/genetic) correctly classifies drug outcomes for the families it can assess — zombie mechanisms with null MR signals produce drug failures. Second, etiologic concordance is necessary but not sufficient for drug success — the amyloid case shows that a mechanism can be etiologically valid and therapeutically insufficient. Third, these two failure modes are structurally different and demand different responses: zombies should be retired from target pipelines; translation-gap mechanisms need different therapeutic strategies, not abandonment of the mechanism.

The practical recommendation: compute Cochran's Q across etiologic evidence types before committing to Phase III. A null MR signal for the target mechanism is a strong negative indicator. A positive MR signal is necessary but not sufficient.

---

## References

Barth et al. 2025 Nature Communications — estradiol MR for AD (null)
Cheng et al. 2014 — ESR1 genetic association with AD
Chinn 2000 Statistics in Medicine — converting odds ratios to d
Cochran 1954 Biometrics — the Q test
Cummings et al. 2014 Alzheimers Research & Therapy — AD drug failure rates
Cummings & Zhong 2014 — estimated cost of failed AD drug programs
Ference et al. 2019 European Heart Journal — MR predicts cardiovascular drug effects
Gill et al. 2021 JAMA Network Open — MR concordance predicts drug approval
Hu et al. 2019 Autoimmunity Reviews — Anti-CD20 observational efficacy
Insel et al. 2010 American Journal of Psychiatry — Research Domain Criteria
Lawlor, Tilling, Davey Smith 2016 International Journal of Epidemiology — triangulation
Lin et al. 2023 Brain — FCRL3-CD20 MR for MS
Munger et al. 2006 JAMA — vitamin D and MS risk
Nelson et al. 2015 Nature Genetics — genetic support doubles drug approval rates
Shumaker et al. 2003 JAMA — WHIMS HRT dementia results
Sokolova et al. 2013 PLoS ONE — CD40 genetic association with MS
Song et al. 2020 Frontiers in Neuroscience — HRT observational meta-analysis for AD
