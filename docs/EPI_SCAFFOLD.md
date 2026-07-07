# Epidemiology Paper Scaffold: Formalizing Evidence Triangulation

**Working title:** Quantifying Evidence Triangulation: A Convergence Test and Failure Taxonomy for Neuroepidemiology

**Target:** International Journal of Epidemiology (IJE), Methods and Measures section
**Backup:** Epidemiologic Methods (De Gruyter) — lower bar, methods-focused, less competitive

**Relationship to TMLR paper:** This paper CITES the TMLR paper (Tower 2026b) for the mathematical framework. This paper's contribution is the applied epidemiological validation and the GRADE comparison. No fiber bundles in the main text.

**Thesis:** Evidence triangulation (Lawlor et al. 2016) can be formalized with two quantitative tools: (1) a cross-design convergence test T(C) that measures whether independent evidence streams agree beyond chance, and (2) a six-mode failure taxonomy that diagnoses WHY triangulation fails. We validate both on 59 ratio-scale neuroepidemiology claims spanning MS and AD, showing that the convergence test discriminates replicable from fragmented evidence and that the failure taxonomy captures discordance patterns that GRADE flags as generic "inconsistency" without diagnostic resolution.

---

## Section 1: Introduction (~600 words)

**GPS rhythm:** Goal -> Problem -> Solution

**Goal:** Causal claims in neuroepidemiology require convergent evidence from multiple study designs (Lawlor et al. 2016, Munafo & Davey Smith 2018).

**Problem:** Triangulation is qualitative. When MR says causal and RCTs say null (vitamin D -> MS), the field has no formal tool to diagnose why the evidence diverges. GRADE rates this as "inconsistency (serious)" — a single label covering at least six structurally different failure modes. Similarly, when six independent AD drugs all fail (HR ~1.0), there is no formal test for whether this convergence is statistically meaningful or coincidental.

**Solution:** We introduce two tools derived from a geometric framework for mechanism claims (Tower 2026b):
1. A variance-ratio convergence test T(C) = within-family variance / marginal variance, where T << 1 indicates convergence beyond chance
2. A six-mode taxonomy of triangulation failure: evidence misfire, mimic mechanism, reference debt, claim laundering, zombie mechanism, and each mode diagnosed by which component of the evidence profile breaks under transport across study designs

We validate these on 59 ratio-scale neuroepidemiology claims across MS and AD.

**Must cite in Introduction:**
- Lawlor, Tilling, Davey Smith 2016 (triangulation)
- Munafo & Davey Smith 2018 (robust research)
- Guyatt et al. 2008 (GRADE)
- Tower 2026b (the TMLR methods paper — for the mathematical foundations)
- Higgins & Thompson 2002 (I-squared — to position T(C) against)

---

## Section 2: Methods (~1200 words)

### 2.1 Data collection
- 59 ratio-scale claims across MS (n=34) and AD (n=25)
- Sources: PubMed systematic search, Cochrane reviews, landmark RCTs, MR studies
- Inclusion: ratio-scale effect estimate (HR, OR, RR, rate ratio) with identifiable exposure-outcome pair
- 51/59 have verified 95% CIs from source publications
- Stratification: etiologic (observational, MR, genetic; n=36) vs therapeutic (RCT; n=23)

### 2.2 Validity tier assignment
- Five-tier scale adapted from Tower 2026b:
  - Proposed: hypothesis only, no direct evidence
  - Causally Suggestive: directional evidence from one causal method (MR or single RCT), not replicated
  - Mechanistically Supported: replicated across methods or settings, consistent evidence within one family
  - Triangulated: convergent evidence from 2+ independent evidence families
  - Validated: all validity dimensions addressed, measurement calibration audited
  - Disconfirmed: negative result on a key criterion
- Assignment criteria: [describe the rubric used]
- [TODO: Blinding protocol — were tiers assigned before or after effect sizes?]
- [TODO: Inter-rater reliability — Cohen's kappa if second rater available]

### 2.3 Convergence test T(C)
- Group claims into families sharing a causal pathway (e.g., all vitamin D -> MS claims)
- Within each family f with F members:
  - Compute Frechet variance: Var_F = (1/F) * sum(|log(est_i) - mean_log|^2)
  - Null variance: sigma^2_null = marginal variance of |log(effect)| across all 59 rows
  - Test statistic: T(C) = Var_F / sigma^2_null
  - p-value via concentration bound (Tower 2026b, Proposition 3.3)
- Verdicts: REALISM (T < 0.2, p < 0.05), PARTIAL (0.2 <= T < 0.5), FRAGMENTED (T >= 0.5)
- [TODO: Permutation null — shuffle family labels 10k times for empirical calibration]

### 2.4 Transport obstruction classification
- For each claim where evidence from different study designs disagrees:
  - Identify the identity component: does the "same" exposure/mechanism refer to the same thing across designs?
  - Identify the tier component: does the evidence quality transfer across designs?
  - Classify into one of six modes based on which component fails

### 2.5 Calibration analysis
- Kendall tau between validity tier and |log(effect estimate)| for ratio-scale rows
- Split by stratum (etiologic vs therapeutic)
- Meta-regression: |log(effect)| ~ tier + stratum + tier*stratum
  - OLS on all 59 rows
  - WLS (inverse-variance weighted) on 51 rows with CIs
- Leave-one-out jackknife for robustness

### 2.6 Invariance depth
- Group claims into 18 claim groups by shared causal pathway
- Within each group, count evidence families (observational, MR, RCT, genetic, biomarker)
- Compute delta with harmonic discounting within families: k-th member of same family contributes 1/k
- Kendall tau between best tier in group and delta

### 2.7 GRADE comparison
- Assign GRADE certainty rating to each of the 59 rows independently
- Compute Kendall tau(GRADE, |log(effect)|) and compare to tau(MV_tier, |log(effect)|)
- Partial correlation: does MV tier add incremental predictive value beyond GRADE?
- Worked example: vitamin D -> MS — how GRADE vs MV handles the MR-RCT discordance

---

## Section 3: Results (~1500 words)

### 3.1 Descriptive statistics
- Table 1: Summary of 59 claims by disease, design, scale, stratum
- Effect sizes range from OR=0.66 (vitamin D supplementation RCT) to HR=32.4 (EBV -> MS)
- Tier distribution: Proposed (n=2), Causally Suggestive (n=15), Mechanistically Supported (n=40), Triangulated (n=3), Validated (n=0), Disconfirmed (n=16)

### 3.2 Calibration
- Overall: tau = 0.54, p < 0.0001
- Etiologic: tau = 0.37, p = 0.006
- Therapeutic: tau = 0.62, p = 0.0002
- Meta-regression: R^2 = 0.38, interaction p = 0.032
- WLS: R^2 = 0.68
- Jackknife: range [0.524, 0.575], all leave-one-out p < 0.05

### 3.3 Convergence test
- Table 2: Six claim families with T(C), p_convergence, verdict
- Failed AD RCTs: T = 0.004 (6 independent null drugs converge to HR ~1.0)
- Social isolation: T = 0.011 (4 meta-analyses converge)
- APOE4: T = 1.098 (FRAGMENTED — dose-response heterogeneity, not convergence)

### 3.4 Transport obstructions
- Table 3: Six classified failure modes with cocycle type and clinical interpretation
- Highlight the vitamin D case: MR and RCT measure different estimands (genetic liability vs supplementation). This is not generic "inconsistency" — it's a specific failure of the transport map between designs.
- Highlight the fingolimod case: same drug, same trial, different endpoints give opposite conclusions. The "mechanism" rotates under outcome transport.

### 3.5 Invariance depth
- tau(tier, delta) = 0.42, p = 0.036
- Only vitamin D -> MS crosses delta >= 3 (MR + RCT = 2 independent evidence families)

### 3.6 GRADE comparison
- [TODO: Compute GRADE ratings and head-to-head comparison]
- [Anticipated result: tau(GRADE) slightly lower than tau(MV) because GRADE doesn't capture the etiologic/therapeutic split or the failure-mode taxonomy]

---

## Section 4: Discussion (~1000 words)

### 4.1 What this adds to triangulation
- Lawlor et al. 2016 introduced the concept; this paper operationalizes it with computable statistics
- T(C) quantifies "convergence" — replaces the qualitative judgment "do these studies agree?"
- The failure taxonomy quantifies "disagreement type" — replaces the qualitative judgment "these studies are inconsistent"
- The split calibration finding (interaction p = 0.032) shows that etiologic and therapeutic evidence obey the same tier ordering but occupy different magnitude regimes — this is a new quantitative finding about the structure of epidemiological evidence

### 4.2 What this adds beyond GRADE
- GRADE's inconsistency domain conflates six structurally different failure modes
- The MV failure taxonomy distinguishes:
  - Evidence misfire (right mechanism, evidence doesn't transfer across designs)
  - Mimic mechanism (wrong mechanism, evidence looks right at the surrogate level)
  - Reference debt (mechanism varies across populations, no global estimate)
- These distinctions are actionable: "evidence misfire" suggests redesigning the study; "mimic mechanism" suggests abandoning the target

### 4.3 Relationship to I-squared
- I-squared measures within-design heterogeneity
- T(C) measures cross-design convergence
- Formally: I-squared is 1 - (within-study variance / total variance); T(C) is within-family variance / marginal variance
- They answer different questions and are complementary

### 4.4 Limitations
1. Small evidence base (59 claims, 2 diseases) — generalizability unknown
2. Tier assignments made by a single team without formal blinding protocol
3. Non-independence: some claims share primary data (overlapping meta-analyses)
4. The convergence test on scalar effects is equivalent to a variance-ratio test — the formal framework adds conceptual organization but no additional statistical power beyond what a standard test provides
5. MR diagnostics incomplete: instrument strength and sensitivity analyses not systematically audited
6. No prospective validation: all results are retrospective

### 4.5 Future directions
- Prospective application: assign tiers to ongoing Phase III trials before unblinding
- Extension to other disease domains
- Inter-rater reliability study for tier assignments
- Cluster-robust reanalysis accounting for nested data structure
- Software package implementing T(C) and the failure taxonomy for systematic reviewers

---

## Figures

1. **Split calibration forest plot** (existing split_calibration_v10.png, cleaned up):
   Blue circles = etiologic, red squares = therapeutic, arranged by tier

2. **Meta-regression scatter** (panel from geometric_validation_v10.png):
   |log(effect)| vs tier with stratum-specific regression lines

3. **Convergence test results** (panel from geometric_validation_v10.png):
   T-statistic bars by family with REALISM/PARTIAL/FRAGMENTED thresholds

4. **GRADE vs MV comparison table** (new):
   [TODO: Build this]

---

## Tables

1. Summary statistics: n by disease, design, stratum, tier
2. Convergence test results: family, F, Var_F, T(C), p, verdict
3. Transport obstruction classification: case, failure mode, evidence, clinical interpretation
4. GRADE vs MV head-to-head: failure mode, GRADE label, MV label, diagnostic resolution
5. Invariance depth by claim group

---

## TODO before drafting

1. [ ] GRADE ratings for all 59 rows (non-negotiable for IJE)
2. [ ] Head-to-head GRADE vs MV comparison table with partial correlation
3. [ ] Blinding protocol statement (or explicit limitation)
4. [ ] Inter-rater reliability (if second rater available)
5. [ ] Cluster-robust standard errors (mixed-effects meta-regression)
6. [ ] MR diagnostics table (F-stats, Egger, weighted median for each MR claim)
7. [ ] Sub-classify 6 null AD RCTs by mechanism failure type
8. [ ] Permutation-calibrated T(C)
9. [ ] I-squared within each Frechet family
10. [ ] Funnel plot or Egger's test for publication bias
