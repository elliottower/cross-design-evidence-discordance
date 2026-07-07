# TMLR Paper Scaffold: Geometric Causal Validity Across Domains

**Working title:** Mechanism Claims Are Geometric Objects: Convergence Tests and Transport Obstructions from Neural Circuits to Clinical Epidemiology

**Target:** TMLR (Transactions on Machine Learning Research)

**Thesis:** The (E, nabla, M) framework — identity fibers, transport structure, component ground set — developed for mechanistic interpretability of neural networks transfers without modification to clinical epidemiology. The same propositions (validity as filtration, realism as low Frechet variance, reference as section obstruction) produce calibrated, quantitative results on 59 neuroepidemiology claims spanning MS and AD. This validates the claim that "mechanism" has domain-invariant geometric structure.

**Why TMLR:** Rolling review, no fee, OpenReview, methods-focused. The contribution is framework validation via domain transfer, which is a methods claim about the generality of geometric causal inference tools developed in the ML interpretability context.

---

## Section 1: Introduction (~1000 words)

**Goal:** Mechanism claims are implicit geometric commitments. We made those commitments explicit for neural network interpretability. This paper shows the same geometry works in a completely different domain.

**Key claims:**
- The unification paper (Tower 2026) showed that five MI frameworks are constructions on three shared primitives (E, nabla, M)
- That paper conjectured domain-invariance (Section app:cross-domain sketched neuroscience, pharmacology, genetics examples but did no quantitative validation)
- This paper provides the first quantitative test: 59 ratio-scale neuroepidemiology claims across MS and AD
- All five constructions produce calibrated results without modifying the framework
- The geometric language is doing real work: it distinguishes failure modes that GRADE (the dominant epi framework) conflates

**Structure preview:** Section 2 recaps the framework. Section 3 adapts the fiber/transport/component instantiation to epidemiology. Section 4 presents five empirical analyses. Section 5 compares to GRADE and triangulation. Section 6 discusses what domain-invariance means and what it doesn't.

**Must cite:**
- Tower 2026 (the unification paper — self-cite)
- Lawlor et al. 2016 (triangulation — the epi-side intellectual ancestor)
- Pearl & Bareinboim 2011 (transportability — the causal inference connection)
- Guyatt et al. 2008 (GRADE — the thing we're comparing against)

---

## Section 2: Framework Recap (~1200 words)

**Goal:** Self-contained summary of the (E, nabla, M) framework from the unification paper. A reader who hasn't read the unification paper should understand the five propositions.

**Subsections:**

### 2.1 Three primitives
- Identity space E over claim base space C (fiber bundle pi: E -> C)
- Transport structure nabla (connection on fibers, context category G)
- Component ground set M (carrier sets for coverage)

### 2.2 Five constructions (one paragraph each, with proposition statement)
1. **Identity as quotient** (Prop 3.1): E_C = O/~_C. For subspace claims, E_C = Gr(k,d). For epidemiology: what are the fibers?
2. **Validity as filtered neighborhood** (Prop 3.2): Five validity dimensions, tier = min. Superlevel-set filtration.
3. **Realism as low Frechet variance** (Prop 3.3): T(C) = Var_F / sigma^2_null. T << 1 licenses realism. Concentration bound gives p-value.
4. **Reference as section obstruction** (Prop 3.4): Global section of reference functor F: G -> Sets. Five failure modes from identity and tier cocycles.
5. **Coverage as weighted rank** (Prop 3.5): Quality-weighted rank of deduplicated carrier sets.

### 2.3 The epistemic dependency chain
View -> Validity -> Realism -> Reference -> Coverage. Each construction's output is the next one's input.

**Key point:** Present the math properly here. This is TMLR, not IJE — the readership can handle fiber bundles and Grassmannians.

---

## Section 3: Epidemiological Instantiation (~1500 words)

**Goal:** Show how each primitive maps to epidemiology. This is where the domain-transfer claim lives or dies.

### 3.1 Claim base space C
- A claim is an (exposure, outcome, population, design) tuple
- Examples: (EBV, MS, European, genetic cohort), (ocrelizumab, MS progression, RRMS, Phase III RCT)
- The base space has natural stratification: etiologic claims vs therapeutic claims

### 3.2 Identity fibers E_C
- **Critical honesty required here.** In MI, the Grassmannian Gr(k,d) is the natural fiber for subspace claims because you're literally working with subspaces of R^d.
- In epidemiology, effect estimates are scalars (log hazard ratio, log odds ratio). The fiber is R, not a Grassmannian.
- BUT: the framework's propositions don't require Grassmannian fibers. Prop 3.3 (Frechet variance) works on any metric space. On R with the Euclidean metric, Frechet mean = arithmetic mean, Frechet variance = ordinary variance.
- The framework specializes, it doesn't break. State this explicitly.
- The TRANSPORT structure is where the geometry gets interesting: transporting a causal effect estimate from an MR design to an RCT design is a non-trivial operation that can fail in classified ways.

### 3.3 Transport category G
- Objects: experimental contexts (model, task, distribution, measurement) -> (exposure, outcome, population, study_design)
- Morphisms: admissible transport maps between contexts
  - Within-design: MR study 1 -> MR study 2 (different instruments, same exposure-outcome)
  - Cross-design: MR -> RCT (changes design while fixing exposure-outcome)
  - Cross-population: European -> East Asian (changes population)
- Admissibility is design-relative (parallel to view-relative in MI)

### 3.4 Component ground set M
- In MI: attention heads, MLP neurons, etc.
- In epidemiology: the set of exposure-outcome-mechanism pathways under study
- Coverage = what fraction of the causal landscape has been mapped at what quality

### 3.5 Validity dimensions in epidemiology
Map the five MI validity dimensions to epidemiological equivalents:
| MI dimension | Epi equivalent | What it tests |
|---|---|---|
| Construct | Exposure/outcome operationalization | Is "vitamin D" serum 25(OH)D or dietary intake or supplementation? |
| Measurement | Estimator agreement | Do different meta-analyses agree? Do different instruments give the same MR estimate? |
| Internal | Causal identification | Randomization, instrument validity, confounding control |
| External | Generalizability | Does the effect hold across populations, settings, time periods? |
| Interpretive | Mechanistic interpretation | Is the causal pathway what we think it is? |

---

## Section 4: Empirical Results (~2500 words)

**Goal:** Five analyses, each corresponding to one construction from the framework.

### 4.1 Data
- 59 ratio-scale claims, 51 with verified 95% CIs
- Sources: PubMed, Cochrane, MR studies, Phase III RCTs
- Two disease domains: Multiple Sclerosis (n=34) and Alzheimer's Disease (n=25)
- Five validity tiers assigned using the Prop 3.2 filtration
- **Blinding note:** [MUST ADD — were tiers assigned before or after effect sizes extracted?]

### 4.2 Split calibration (validity filtration in action)
- Kendall tau(tier, |log(effect)|): overall tau=0.54, p<0.0001
- Etiologic stratum: tau=0.37, p=0.006
- Therapeutic stratum: tau=0.62, p=0.0002
- Meta-regression: |log(effect)| ~ tier * stratum
  - R^2 = 0.38 (OLS), 0.68 (WLS)
  - Interaction: beta = -0.51, p = 0.032
- **Interpretation:** The validity filtration predicts effect magnitude WITHIN each stratum. The interaction term shows that etiologic and therapeutic claims have different slopes — same ordinal ranking, different magnitude regimes.
- Jackknife: all leave-one-out p < 0.05, range [0.524, 0.575]

**Figure 1:** Four-panel: (a) meta-regression scatter with stratum-specific fit lines, (b) jackknife stability bars, (c) Frechet T-statistics, (d) invariance depth vs tier

### 4.3 Frechet variance realism test (Prop 3.3)
- Six claim families tested
- T(C) = Var_F / sigma^2_null where sigma^2_null is the marginal variance of |log(effect)| across all 59 rows
- Results:

| Family | F | T(C) | p_conv | Verdict |
|---|---|---|---|---|
| Failed AD RCTs | 6 | 0.004 | <0.001 | REALISM |
| Social isolation -> dementia | 4 | 0.011 | 0.001 | REALISM |
| Ocrelizumab -> MS | 3 | 0.016 | 0.016 | REALISM |
| Vitamin D -> MS | 5 | 0.158 | 0.025 | REALISM |
| Amyloid -> AD | 3 | 0.305 | 0.305 | PARTIAL |
| APOE4 -> AD | 3 | 1.098 | 1.0 | FRAGMENTED |

- **Key:** The Frechet variance test on R (scalar effects) is ordinary variance normalized by a null. This is a correct specialization of Prop 3.3 — the proposition doesn't require Grassmannian fibers, it requires a metric space. On R, it reduces to a variance-ratio test.
- **Honest note:** On R, this is I-squared's cross-design cousin. The geometric language adds the null model and the connection to the broader framework, not new statistical power.

### 4.4 Transport obstruction classification (Prop 3.4)
- Six failure modes identified, each classified by which cocycle is non-trivial:

1. **Vitamin D -> MS: EVIDENCE MISFIRE** — c_tau < 0
   - MR: OR=2.0 (Mechanistically Supported) -> RCT: HR=0.66-1.17 (Disconfirmed)
   - Identity preserved (vitamin D is vitamin D), tier collapses under design transport MR -> RCT
   - **Connection to transportability:** The MR estimand (lifetime genetic liability to low vitamin D) differs from the RCT estimand (adult supplementation). The transport formula requires invariance of the causal effect to the intervention type — it doesn't hold.

2. **Anti-tau CSF: MIMIC MECHANISM** — c_id non-trivial, c_tau = 0
   - 99% CSF target engagement, 0% clinical benefit
   - Tier preserved (good measurement), but identity rotates: pharmacological engagement ≠ disease modification

3. **APOE4 across ancestries: REFERENCE DEBT** — pi_0(N(G')) ≠ *
   - OR varies 1.9 (Hispanic) to 4.5 (East Asian)
   - Transport category has disconnected components — no global section

4. **Smoking -> MS: EVIDENCE MISFIRE** — c_tau < 0
   - Obs positive -> MR null (OR=1.03, CI 0.89-1.19)
   - Confound signature: observational confounding exposed by MR instrument

5. **Fingolimod relapse vs progression: MIMIC MECHANISM** — c_id non-trivial under outcome transport
   - ARR 0.52 (Mechanistically Supported) vs CDP 0.83 null (Disconfirmed) in same trial
   - Same drug, same trial, but the "mechanism" that reduces relapses is not the mechanism needed for progression

6. **TBI -> dementia vs AD: MIMIC MECHANISM** — c_id non-trivial under outcome refinement
   - TBI->dementia OR=1.81 vs TBI->AD OR=1.02 null
   - TBI causes vascular/mixed dementia, not Alzheimer's specifically

- **Key claim:** These six failure modes are not ad hoc categories. They fall out of Prop 3.4's decomposition into identity and tier cocycles. The same classification that produced evidence misfire, mimic mechanism, claim laundering, reference debt, and zombie mechanism in MI produces the same categories in epidemiology — because the obstruction theory is domain-invariant.

### 4.5 Invariance depth (realism criterion)
- 18 claim groups, delta computed with harmonic discounting within evidence families
- tau(best_tier, delta) = +0.42, p = 0.036
- Only 1/18 groups crosses delta >= 3: vitamin D -> MS (MR + RCT = 2 independent evidence families)
- **Interpretation:** Most claims have low invariance depth because most evidence comes from a single study design. The framework correctly identifies this as a ceiling on realism licensing.

---

## Section 5: Comparison to Existing Frameworks (~1000 words)

### 5.1 GRADE
- GRADE has five domains: risk of bias, inconsistency, indirectness, imprecision, publication bias
- MV tiers correlate with GRADE but are not equivalent
- **Key difference:** GRADE's "inconsistency" domain conflates all six failure modes into one label. MR causal + RCT null is "inconsistency" in GRADE. In the MV framework, it's specifically EVIDENCE MISFIRE with a formal cocycle diagnosis pointing to the estimand mismatch.
- **Table: MV vs GRADE vs Bradford Hill vs Lawlor triangulation, failure mode by failure mode**

[TODO: Build this comparison table. Must show that MV resolves cases GRADE cannot distinguish. Vitamin D is the worked example: GRADE says "inconsistency (serious)," MV says "evidence misfire, c_tau < 0, MR estimand ≠ RCT estimand."]

### 5.2 Triangulation (Lawlor et al. 2016)
- Triangulation says: use study designs with different bias structures; if they converge, the result is more credible
- The Frechet variance test operationalizes "converge" quantitatively: T(C) << 1 means convergence beyond chance
- Invariance depth operationalizes "different bias structures" via harmonic discounting across evidence families
- The transport obstruction taxonomy operationalizes "if they don't converge, WHY NOT"
- **Claim:** The MV framework is a formalization of Lawlor's triangulation intuition, with computable test statistics and classified failure modes

### 5.3 I-squared (Higgins & Thompson 2002)
- I-squared measures heterogeneity WITHIN a study design
- T(C) measures convergence ACROSS study designs
- These are complementary, not competing
- [TODO: Show the mathematical relationship. T(C) on R is a between-family variance ratio; I-squared is a within-study variance ratio. Different numerators, different denominators, different questions.]

---

## Section 6: Discussion (~1200 words)

### 6.1 What domain-invariance means
- The (E, nabla, M) primitives are abstract enough to instantiate in any field where mechanism claims are made
- The propositions don't assume a specific fiber type — they work on any metric space (R for scalars, Gr(k,d) for subspaces)
- The transport obstruction taxonomy produces the same five failure modes because the decomposition into identity and tier cocycles is algebraic, not domain-specific
- **BUT:** The Grassmannian structure that makes MI interesting (subspace angles, geodesic proximity, principal angles) trivializes in the epi setting where fibers are R. The geometric language is doing less work on scalar fibers than on Grassmannian fibers. State this honestly.

### 6.2 What domain-invariance doesn't mean
- The framework doesn't discover domain-specific causal mechanisms — it organizes and grades evidence about them
- The framework doesn't replace domain expertise — tier assignments require epidemiological judgment
- The framework doesn't solve the identification problem — T(C) << 1 is necessary for realism, not sufficient (correlated biases across studies can produce spurious convergence)
- [Address the circularity concern: tiers encode study design quality, which correlates with effect magnitude for known reasons. The framework adds the failure-mode taxonomy on top of the tier ordering — that's the genuine contribution.]

### 6.3 Limitations
- Small evidence base (59 claims, 2 diseases)
- Tier assignments not independently validated (no inter-rater reliability, no blinding protocol)
- Non-independence: some claims share data sources (meta-analyses with overlapping primaries)
- Scalar fibers: the Frechet test on R is equivalent to a variance-ratio test — the geometric apparatus adds conceptual clarity, not statistical power
- MR diagnostics incomplete: instrument strength and sensitivity analyses not systematically reported for all MR results
- [TODO: Cluster-robust reanalysis with random intercepts for claim family]

### 6.4 Future work
- Prospective validation: assign tiers to ongoing trials before results unblind
- Extend to other disease domains
- Develop the non-scalar fiber case in epi: multi-outcome claims have vector-valued effects where Grassmannian structure re-emerges
- Permutation-calibrated T(C) with finite-sample bounds
- Software: open-source implementation of the five-construction pipeline

---

## Appendix A: Mathematical Details

- Full Prop 3.3 derivation specialized to R (showing it reduces to variance ratio)
- Connection between T(C) and I-squared: formal mathematical comparison
- Transport obstruction cocycle calculations for each of the six case studies
- Permutation null derivation for T(C)

## Appendix B: Data

- Full 59-row table with case_id, claim, design, scale, estimate, CI, tier, stratum
- Tier assignment criteria for each row
- Source verification notes

## Appendix C: GRADE Comparison Table

- Row-by-row: each of the six failure modes, how GRADE handles it, how MV handles it, what resolution each provides

---

## Figures

1. **Four-panel main result** (existing geometric_validation_v10.png, cleaned up):
   (a) Meta-regression scatter with stratum-specific fit lines
   (b) Jackknife stability
   (c) Frechet T-statistics by family
   (d) Invariance depth vs tier

2. **Framework adaptation diagram**: Side-by-side showing (E, nabla, M) instantiation in MI vs epidemiology. Same abstract structure, different fibers.

3. **Transport obstruction case studies**: Visual for each of the six failure modes showing the cocycle structure.

4. **GRADE vs MV comparison**: Table showing diagnostic resolution on the vitamin D case.

---

## TODO before drafting

1. [ ] GRADE comparison table (non-negotiable — professors unanimous)
2. [ ] Blinding protocol for tier assignments (or explicit limitation statement)
3. [ ] Cluster-robust reanalysis (random intercepts for claim family + disease)
4. [ ] MR diagnostics table (F-statistics, sensitivity analyses for each MR result)
5. [ ] Sub-classification of 6 null AD RCTs by failure mode
6. [ ] Permutation null for T(C) (shuffle family labels, 10k iterations)
7. [ ] Formal I-squared vs T(C) mathematical comparison
8. [ ] Selection diagrams (Pearl/Bareinboim) for each transport obstruction
