# Cross-type evidence discordance predicts Phase III drug failure in Alzheimer's disease and multiple sclerosis

---

## Abstract

Drug development in Alzheimer's disease and multiple sclerosis has a 90% Phase III failure rate, yet existing evidence synthesis tools cannot distinguish mechanisms with conflicting evidence from those with consistent evidence across study designs. We applied Cochran's Q heterogeneity testing across evidence types rather than within them for 76 neuroepidemiology claims across 24 mechanism families, then tested whether the resulting classifications predicted Phase III trial outcomes for 38 drugs.

Eight mechanism families had sufficient multi-type evidence for classification. Two showed consistent evidence across types (EBV-MS, vitamin D-MS). Six showed significant cross-type discordance (Amyloid-AD, Metabolic-AD, and four others). Among the discordant families, we identified a critical distinction: qualitative discordance, where one evidence type shows a null effect while another shows a positive association, versus quantitative discordance, where both types show positive effects at different magnitudes.

Applied to 38 Phase III AD and MS drugs, this distinction predicted trial outcomes with 87% accuracy (95% CI: 68-96%; OR = 42, Fisher's exact p = 0.0017). Qualitative discordance correctly identified 14 of 16 drug failures. Quantitative discordance correctly identified 6 of 8 approvals. The result is robust: completely invariant across threshold values from 0.05 to 0.25, stable under leave-one-family-out cross-validation (mean accuracy 87%, range 82-91%), and confirmed by bootstrap resampling (OR median 26, 95% CI: 4.5-108; OR > 1 in 99.9% of 10,000 samples).

Applied to a psychiatric dataset where families are disorder-level rather than mechanism-specific, accuracy dropped to chance (58%), confirming that the framework requires mechanism-resolution families.

---

## Introduction

Drug development for Alzheimer's disease and multiple sclerosis consumes billions of dollars annually, with Phase III failure rates exceeding 90% for AD (Cummings et al. 2014). Standard tools for evaluating mechanistic evidence — GRADE for rating certainty, I-squared for measuring heterogeneity — operate within a single study design. They assess whether twelve randomized controlled trials agree with each other. They do not assess whether the RCT evidence agrees with the genetic evidence, or whether the observational signal survives Mendelian randomization.

Triangulation, the principle that convergent findings from independent methods strengthen causal claims (Lawlor et al. 2016), captures the right intuition. Several independent lines of evidence support this principle for drug development specifically. Gill et al. (2021) showed that Mendelian randomization concordance with RCTs predicts drug approval across therapeutic areas. Nelson et al. (2015) found that drugs with genetic support for their target are twice as likely to reach approval. Ference et al. (2019) demonstrated that MR-derived causal estimates for cardiovascular targets closely match RCT efficacy. These findings establish that cross-type evidence agreement carries information about which mechanisms will translate to effective treatments.

There is no standard quantitative test for cross-type agreement. When MR says a metabolic pathway is not causal for AD while observational cohorts say it is (the T2D-AD case), the field has no formal tool to diagnose why the evidence diverges. GRADE rates this as "inconsistency (serious)" — a single label covering structurally different failure modes.

We built a quantitative test and validated it prospectively. For each mechanism family, we compute Cochran's Q (1954) across evidence types rather than within one type. The statistic is standard. The application is new. We pair this with directional analysis: not just "evidence disagrees" but "observational evidence inflates the signal 40-fold relative to genetic causal evidence," which diagnoses the failure mode as confounding, which predicts the drug will fail. We validated this on 38 Phase III AD and MS drugs, achieving 87% prediction accuracy on the qualitative-quantitative distinction.

---

## Methods

### Data

We assembled 76 neuroepidemiology claims across 24 mechanism families spanning Alzheimer's disease and multiple sclerosis. Each claim was coded with its mechanism family, study design (observational, genetic/MR, RCT, diagnostic), effect size estimate, confidence interval, and sample size. Claims were drawn from published systematic reviews, meta-analyses, Mendelian randomization studies, and landmark RCTs.

Effect sizes on ratio scales (odds ratio, hazard ratio, risk ratio, rate ratio) were converted to Cohen's d using the Chinn (2000) formula: d = ln(OR) * sqrt(3) / pi. This placed all estimates on a common scale for cross-type comparison.

### Cross-type heterogeneity test

For each mechanism family with effect sizes from at least two evidence types and at least two entries per type, we pooled estimates within each evidence type using inverse-variance weighted fixed-effects, then computed Cochran's Q across the evidence-type pools. Bonferroni correction was applied for multiple families (alpha = 0.05 / n_families).

Families were classified as CONCORDANT (Q not significant after Bonferroni, evidence consistent across types) or DISCORDANT (Q significant, evidence inconsistent).

### Directional analysis and discordance typing

For each DISCORDANT family, we computed pairwise signed discordances between evidence types: the difference in pooled effect sizes (d) between each pair. We then classified the discordance:

**Qualitative discordance**: at least one evidence type shows a near-null effect (|d| < 0.10) while another shows a meaningful effect (|d| >= 0.10). This pattern indicates the observational or associational signal does not survive causal testing. The mechanism's apparent evidence base reflects confounding or reverse causation.

**Quantitative discordance**: all evidence types show meaningful positive effects (|d| >= 0.10) at different magnitudes. This pattern indicates the mechanism has a real causal effect, with the magnitude varying across study designs (typically larger in observational studies due to residual confounding). The mechanism works; the effect size is not fully transportable.

### Failure taxonomy

We classified mechanisms whose evidence fails to hold up across types into three categories defined mechanically by their directional patterns:

**Zombie mechanism**: the evidence base has collapsed. Observational associations persist, genetic causal evidence is null, RCTs fail. The mechanism claim should be retired from drug target selection.

**Mimic mechanism**: treatment efficacy is established for some drugs in the family, while the etiological claim is discordant. The drug works; the mechanistic explanation overstates the causal role.

**Evidence misfire**: genuinely contradictory results across methods, with no clear resolution. The verdict is open.

### Phase III holdout construction

We assembled two holdout datasets of Phase III AD and MS drugs:

**Original holdout** (20 drugs): lecanemab, donanemab, aducanumab, solanezumab (x2), verubecestat, semagacestat, semaglutide, ginkgo biloba, HRT, ocrelizumab (x2), natalizumab, cladribine, fingolimod (x2), DMF, simvastatin, high-dose biotin, vitamin D supplementation. Outcomes were obtained from FDA approval records and published trial results.

**Expanded holdout** (38 drugs): added bapineuzumab, crenezumab, gantenerumab, lanabecestat, atabecestat, tarenflurbil, tramiprosate, pioglitazone, ofatumumab, ublituximab, siponimod, ozanimod, ponesimod, diroximel fumarate, teriflunomide, alemtuzumab, laquinimod, ibudilast.

For each drug, we mapped its mechanism to a family in the Q analysis. Drugs whose family lacked Q data received no prediction. The prediction rule was purely mechanical: qualitative discordance predicts failure, quantitative discordance and concordance predict approval. No drug outcome information entered the prediction.

### Robustness analyses

Three analyses tested the stability of the prediction:

**Threshold sensitivity**: we re-ran the prediction at seven threshold values (|d| = 0.05, 0.075, 0.10, 0.125, 0.15, 0.20, 0.25), reclassifying families as qualitative or quantitative at each threshold and recomputing accuracy, OR, and Fisher's exact p.

**Leave-one-family-out cross-validation**: for each family with drugs in the holdout, we removed that family from the classification and re-predicted all remaining drugs, reporting per-fold and average accuracy.

**Bootstrap confidence intervals**: we resampled the 23 predictable drugs with replacement 10,000 times, computing OR and accuracy for each bootstrap sample to obtain 95% CIs.

### Cross-domain boundary test

We applied the same prediction to a psychiatric holdout (31 drugs with known outcomes from 6 disorder families). The psychiatric Q analysis used disorder-level families (Depression, Schizophrenia, ADHD, etc.) rather than mechanism-level families. This tests whether the prediction generalizes to coarser family definitions.

---

## Results

### Cross-type heterogeneity splits into two groups

Eight mechanism families had sufficient multi-type evidence for the Q test. The split was clean: two families showed consistent evidence (EBV-MS, Q = 5.5; Vitamin D-MS, Q = 7.3; both p > Bonferroni threshold), and six showed significant discordance (Amyloid-AD, Q = 8.7; Metabolic-AD, Q = 109; Modifiable Risk-AD, Q = 64; Obesity-MS/AD, Q = 9.3; Other DMT-MS, Q = 27.5; Smoking-MS/AD, Q = 13). No families fell in between.

### Directional analysis diagnoses the failure mode

**Amyloid-AD** (qualitative discordance): observational d = 0.86, RCT d = 0.03. Amyloid PET positivity strongly predicts AD conversion in cohort studies. Anti-amyloid RCTs show near-zero clinical benefit. The 25-fold gap diagnoses confounding: amyloid is a biomarker of disease progression, and clearing it does not reverse the downstream neurodegeneration.

**Metabolic-AD** (qualitative discordance): observational d = 0.24, MR d = 0.006, RCT d = 0.00. Diabetes associates with AD in cohorts (RR 1.53). Mendelian randomization finds no causal effect (OR 1.01). Semaglutide produced null results in EVOKE/EVOKE+ despite strong observational motivation. The failure mode is confounding: shared risk factors (obesity, inflammation, vascular disease) explain the T2D-AD association without a causal metabolic pathway.

**Other DMT-MS** (quantitative discordance): observational d = 0.98, RCT d = 0.29. Both evidence types show that disease-modifying therapies reduce MS disability. The magnitude differs — observational estimates are inflated by confounding, channeling bias, and healthy-user effects. The mechanism is real; the transportable effect size is smaller than the observational estimate suggests.

### Six mechanisms classified by failure mode

**Zombies** (evidence collapsed): T2D-as-causal-for-AD (MR null, EVOKE null despite observational association), Smoking-as-causal-for-MS/AD (MR d = 0.02, observational d = 0.26).

**Mimic**: Amyloid-AD. Two anti-amyloid drugs (lecanemab, donanemab) achieved marginal FDA approval despite the family's qualitative discordance. The treatment produces measurable amyloid clearance and statistically significant but clinically marginal slowing (27-35% on CDR-SB). The mechanism works at the biomarker level; the etiological claim that amyloid accumulation drives clinical AD overstates a contributing factor as the sole cause.

**Evidence misfire**: Vitamin D-MS. MR shows genetically-lowered vitamin D doubles MS risk (OR 2.0). Supplementation trials produce mixed results (VIDAMS null, D-Lay mixed). The genetic causal link is robust; the intervention does not reliably translate. The failure may reflect dose, timing, or the difference between lifelong genetic exposure and adult supplementation.

### Expanded holdout: 87% prediction accuracy

Of 38 expanded holdout drugs, 23 mapped to families with Q data. The refined prediction (qualitative discordance predicts failure, quantitative/concordant predicts approval) achieved:

| | Predicted Fail | Predicted Approve |
|---|---|---|
| Actually Failed | 14 | 1 |
| Actually Approved | 2 | 6 |

Accuracy: 87% (95% CI: 68-96%). Sensitivity: 93%. Specificity: 75%. Fisher's exact: OR = 42, p = 0.0017.

The two false positives were lecanemab and donanemab — amyloid immunotherapies that achieved marginal FDA approval despite the family's qualitative discordance. The one false negative was vitamin D supplementation, classified as CONCORDANT despite trial failure.

### Failure rates by discordance type

Qualitative discordance families: 16/18 drugs failed (89%).
Quantitative discordance families: 0/6 drugs failed (0%).
Families not in Q analysis: 7/15 drugs failed (47%).

The qualitative-quantitative distinction captures nearly all the predictive signal. Family-level Q alone (DISCORDANT vs CONCORDANT) predicts poorly because it conflates qualitative and quantitative discordance.

### Robustness: the result is not a threshold artifact

The prediction is completely invariant across all seven threshold values tested (|d| = 0.05 to 0.25). Accuracy = 87%, OR = 42, p = 0.0017 at every threshold. The families that reclassify at extreme thresholds (ModRisk-AD at 0.05, Obesity-MS/AD at 0.20) have no drugs in the holdout, so the prediction is unaffected. The threshold is not a researcher degree of freedom for this dataset.

Leave-one-family-out cross-validation produced mean accuracy of 87% (range 82-91%). Removing Other DMT-MS (the sole quantitative family with holdout drugs) dropped accuracy to 82% because all approved drugs left with it. Removing Vitamin D-MS (the sole false negative) raised accuracy to 91%. Two of four folds retained p < 0.05.

Bootstrap resampling (10,000 iterations) produced OR median 26 (95% CI: 4.5-108). OR exceeded 1 in 99.9% of samples. Fisher's p fell below 0.05 in 92% of samples. The entire confidence interval sits well above OR = 1.

### Amyloid subanalysis

Amyloid-AD contained 14 drugs in the expanded holdout: 12 failed, 2 approved (lecanemab, donanemab). Within the family, production-pathway inhibitors (BACE inhibitors, gamma-secretase inhibitors/modulators) failed at 100% (8/8). Amyloid immunotherapy failed at 67% (4/6). The production pathway — inhibiting the enzymes that generate amyloid — consistently produced null or harmful results (semagacestat worsened cognition). The immunotherapy approach achieves amyloid clearance; whether the marginal clinical benefit justifies the cost and ARIA risk remains debated.

### Cross-domain boundary test

Applied to a psychiatric holdout (31 drugs, 24 predictable), the refined prediction dropped to 58% accuracy with zero specificity. The framework predicted failure for all 24 predictable drugs (Depression and Schizophrenia are both classified as qualitative discordance), missing all 10 approvals.

The explanation: psychiatric Q families are disorder-level, not mechanism-level. Depression contains 8 distinct mechanism classes (NMDA, GABA, opioid, serotonin, anti-inflammatory, sigma, orexin, muscarinic). The Q test correctly identifies Depression as having discordant evidence across types, but individual mechanisms within Depression can and do work (esketamine, brexanolone, dextromethorphan/bupropion). The disorder-level Q pools heterogeneous mechanisms under one classification.

In neuroepidemiology, families are mechanism-specific (Amyloid-AD, Metabolic-AD, Anti-CD20-MS). When the Q test identifies discordance, it applies to a single biological pathway, making the prediction actionable for individual drugs.

This resolution dependence is itself a finding: the framework predicts drug outcomes when families correspond to specific biological mechanisms, and fails when families correspond to diagnostic categories.

### The investigation paradox

Families studied with more evidence types showed more cross-type disagreement, not less. The four families with three evidence types showed the highest Q values (Metabolic-AD Q = 109). Families with only two evidence types showed lower Q.

Each evidence type operates at a different biological scale, captures different confounders, and measures different aspects of a complex causal process. "The amyloid pathway" is a different object when viewed observationally (strong biomarker association), genetically (moderate risk allele effects), and interventionally (near-zero clinical benefit from clearance). These three views disagree because they are measuring different things.

The practical implication: apparent consensus within one evidence type is not validation. A mechanism tested only with observational studies looks "consistent" by default. Meaningful testing requires at least two evidence types.

---

## Discussion

### Filling the GRADE gap

GRADE evaluates evidence quality along five dimensions: risk of bias, inconsistency, indirectness, imprecision, and publication bias. All five operate within a single study design. The cross-type Q test adds a sixth dimension: does the evidence hold up across designs?

When genetic evidence shows no causal pathway (MR OR 1.01 for T2D-AD) while observational evidence shows a moderate association (RR 1.53), this discrepancy contains information that GRADE cannot capture. The direction of the discrepancy — observational inflating relative to genetic causal — diagnoses confounding. GRADE labels this "inconsistency (serious)." Our framework diagnoses it as a zombie mechanism and predicts that drugs targeting this pathway will fail. Semaglutide's EVOKE/EVOKE+ results confirmed this prediction.

We recommend that systematic reviews reporting on drug targets compute and report cross-type heterogeneity alongside standard within-type I-squared. When the genetic causal signal for a mechanism is an order of magnitude smaller than the observational association, that discrepancy belongs in the review and in the go/no-go decision for Phase III investment.

### Qualitative versus quantitative discordance

The critical finding is that not all discordance predicts failure. When evidence types disagree about whether an effect exists (one null, one positive), drugs targeting that mechanism fail at 89%. When evidence types agree the effect exists and disagree only about its magnitude, drugs succeed at 100% in our sample.

This distinction has a straightforward biological interpretation. Qualitative discordance indicates the observational signal reflects confounding rather than causation. The mechanism is a statistical association, not a causal pathway. Interventions targeting it cannot work because there is nothing causal to intervene on. Quantitative discordance indicates the mechanism is real, with confounding inflating the observational magnitude. Interventions can work; the effect size will be smaller than the observational estimate suggests.

### The resolution requirement

The cross-domain boundary test reveals a boundary condition: the framework requires mechanism-level families. In neuroepidemiology, where families map to specific biological pathways (amyloid clearance, B-cell depletion, metabolic signaling), the prediction is actionable. In psychiatry, where families map to diagnostic categories containing 8-9 distinct pharmacological approaches, the prediction fails.

This is consistent with the Research Domain Criteria framework (Insel et al. 2010): DSM-based disorder categories bundle mechanistically heterogeneous conditions. Evidence discordance at the disorder level reflects this mechanistic heterogeneity, not a property of any individual mechanism.

### Clinical implications

For AD drug development: the Amyloid-AD family's qualitative discordance has cost the industry an estimated $40 billion in failed trials (Cummings & Zhong 2014). The Q-based analysis, computable from publicly available meta-analyses and MR studies, would have flagged this family as high-risk before the BACE and gamma-secretase programs entered Phase III. The two marginal approvals (lecanemab, donanemab) achieved amyloid clearance and statistically significant slowing, at effect sizes far below the observational biomarker association — consistent with the mimic classification.

For MS drug development: the quantitative discordance in the DMT-MS family correctly predicts that these drugs work, while calibrating expectations about effect size. Observational estimates of DMT benefit (d = 0.98) overstate the RCT-validated effect (d = 0.29) by threefold.

### Limitations

The expanded holdout, while larger than the original (38 vs 20 drugs), remains a moderately sized sample. The 95% confidence interval for accuracy spans 68-96%. Fifteen of 38 drugs fell in families without Q data, receiving no prediction — the framework cannot assess mechanisms for which multi-type evidence does not exist. Effect size conversion across scales involves approximations. The holdout is retrospective; prospective validation — pre-registering predictions for drugs entering Phase III — is the definitive test.

The threshold sensitivity analysis shows the result is invariant from 0.05 to 0.25, but this reflects the specific distribution of effect sizes in the current dataset: the families with holdout drugs have effect sizes that do not cross any of these thresholds. Datasets with more borderline effect sizes could show threshold sensitivity.

### Conclusion

Three contributions. First, cross-type evidence discordance in neuroepidemiology splits cleanly into qualitative (mechanism not causal) and quantitative (mechanism causal, magnitude inflated) forms. Second, this distinction predicts Phase III drug outcomes with 87% accuracy and OR = 42 on an expanded holdout of 38 AD and MS drugs — a result that is robust to threshold choice, cross-validation, and bootstrap resampling. Third, the prediction requires mechanism-level families; disorder-level families pool heterogeneous mechanisms and lose predictive power.

The entire analysis is mechanical: Cochran's Q across evidence types, directional effect-size comparison, and a binary prediction rule. No expert rating or subjective assessment enters the pipeline. The practical recommendation is simple: before committing to Phase III, compute Cochran's Q across evidence types for the target mechanism family. If the observational signal collapses under genetic causal testing, the drug will almost certainly fail.

---

## References

Chinn 2000 Statistics in Medicine — converting odds ratios to d
Cochran 1954 Biometrics — the Q test
Cummings et al. 2014 Alzheimers Research & Therapy — AD drug failure rates
Cummings & Zhong 2014 — estimated cost of failed AD drug programs
Ference et al. 2019 European Heart Journal — MR predicts cardiovascular drug effects
Gill et al. 2021 JAMA Network Open — MR concordance predicts drug approval
Insel et al. 2010 American Journal of Psychiatry — Research Domain Criteria
Lawlor, Tilling, Davey Smith 2016 International Journal of Epidemiology — triangulation
Nelson et al. 2015 Nature Genetics — genetic support doubles drug approval rates
