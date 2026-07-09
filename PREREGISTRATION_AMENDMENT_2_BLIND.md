# Pre-Registration Amendment 2B: Blind Domain-Extension Families

**Status:** FROZEN (pending commit SHA)
**Date:** 2026-07-09
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9)
**Scope:** Five additional mechanism families declared under blinding, expanding the exploratory extension to cover four new disease domains (psychiatry, gastroenterology, ophthalmology, musculoskeletal). Two families share a domain (psychiatry) to test opposing failure modes.

**Integrity protocol:** Same freeze-before-data protocol as all prior amendments. This amendment is written under **strict blinding**: the declaring agent has not seen, requested, or accessed any classification results, accuracy numbers, classifier code, or data files from the study. Family selection is based entirely on domain knowledge of the MR, observational, and drug-development literatures. Every family declared below will be scored; none may be dropped post hoc.

**Commit SHA:** 12ea0ed

---

## Blinding declaration

The five families below were selected without access to:
- Any `.py`, `.json`, or computed output files in this repository
- Any classification results from prior families
- Any accuracy statistics or confusion matrices
- The `paper/reference/` directory or any data extraction files

Selection was based on:
1. Domain knowledge of the Mendelian randomization literature
2. Published drug approval/failure records
3. The observational epidemiology of each exposure-outcome pair
4. Awareness of existing domain coverage from the parent pre-registrations (neuro, cardio, autoimmune, oncology, respiratory, metabolic)

The declaring agent committed to including families expected to generate both correct and incorrect classifications, and to including at least one family that shares instruments with an existing declared family.

---

## Relationship to prior amendments

These five families constitute a **second exploratory batch**, distinct from both the primary pre-registered families (neuro + cardio + autoimmune) and the first exploratory extension (oncology + respiratory + metabolic). They are added to the exploratory denominator and reported alongside Amendment 1 and Amendment 2 extension families, clearly labeled as blind declarations.

The classification rule, scoring procedure, scale harmonization, and all decision criteria carry forward from the parent documents without modification.

---

## New families

### Family B1: IL-6 signaling -> major depressive disorder

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | IL-6 signaling (proxied by CRP reduction via IL-6 receptor blockade) -> major depressive disorder (MDD) incidence |
| **Domain** | Psychiatry (new domain) |
| **MR instrument** | IL6R cis-pQTL variants, primarily rs2228145 (Asp358Ala) and rs4129267, instrumenting downstream IL-6 signaling via CRP as a readout. These are the standard instruments used in drug-target MR for IL-6 pathway studies (e.g., Khandaker et al. 2018 BMJ, Hartwig et al. 2017). |
| **MR scale** | Per 1 SD decrease in CRP (as proxy for IL-6R blockade). IL6R MR studies typically report per-SD CRP or per-unit log-CRP. |
| **Rescaling needed?** | No (per-SD is exposure-comparable) |
| **Expected OBS source** | Meta-analyses of CRP/IL-6 levels and depression risk from prospective cohort studies. Haapakoski et al. (2015 J Psychiatr Res) report pooled OR ~ 1.31 for elevated CRP and depression incidence; Valkanova et al. (2013 Biol Psychiatry) report similar estimates. Expected OBS d ~ 0.15-0.25 from these meta-analyses. |
| **Drug class** | Anti-IL-6 monoclonal antibodies: sirukumab (Janssen) |
| **Drug outcome** | Sirukumab failed Phase II for treatment-resistant MDD (Boyle et al. 2020, Mol Psychiatry). The trial was terminated early for futility. No anti-IL-6 or anti-IL-6R agent has received FDA approval for any psychiatric indication. Coded as **Failed**. |
| **Rationale** | Tests the classification rule in psychiatry, a domain with pervasive residual confounding in observational studies (depression-inflammation associations confounded by BMI, smoking, sleep, physical inactivity, antidepressant use). The IL6R instrument is the same instrument class used in cardiometabolic IL-6 families but applied to a psychiatric outcome. If the framework correctly identifies this as a zombie mechanism (non-trivial OBS driven by confounding, null MR), it demonstrates cross-domain generalizability of the discordance signal. |

**Shared-instrument note:** This family shares the IL6R cis-pQTL instruments with any existing IL-6R -> CHD family in the cardiometabolic domain. Same exposure instrument, different outcome. Per the family definition rule, these are separate families.

**Prediction:** OBS non-trivial (d >= 0.10 from CRP/depression meta-analyses). MR null (IL6R MR for depression has been reported as null or with very small effect sizes in adequately powered studies; the Khandaker et al. CRP -> depression MR reported OR 0.95 per 1 SD lower CRP, CI including null). Classification: **discordance**. Predicted drug outcome: **failure**. Expected match: **correct**.

---

### Family B2: IL-23 -> Crohn's disease

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | IL-23 receptor signaling -> Crohn's disease incidence |
| **Domain** | Gastroenterology / inflammatory bowel disease (new domain) |
| **MR instrument** | IL23R cis-coding variant rs11209026 (R381Q), a loss-of-function variant that directly reduces IL-23 receptor signaling. This variant has been used in drug-target MR designs and is among the strongest known protective variants for Crohn's disease (Duerr et al. 2006 Science). Additional IL23R-region variants may serve as secondary instruments. |
| **MR scale** | Per allele (coding variant) |
| **Rescaling needed?** | **Yes -- per-allele estimate must be rescaled to per-SD of IL-23 signaling**. However, the per-allele OR is exceptionally large (OR ~ 0.26 for Crohn's per protective allele; d = \|ln(0.26)\| x sqrt(3)/pi ~ 0.74). Because the per-allele exposure change in SD units is < 1.0, the per-SD d will be *larger* than the per-allele d. The d >= 0.10 threshold will be exceeded under any plausible rescaling. If the per-allele exposure change in SD units is not available, this family will be flagged as "scale-unresolved" and classified by the statistical criterion alone. |
| **Expected OBS source** | Meta-analyses of circulating inflammatory markers (CRP, calprotectin, IL-23) and Crohn's disease. Prospective cohort data may be limited for IL-23 specifically; broader inflammatory marker associations (e.g., CRP and IBD incidence) from population-based cohorts serve as the observational evidence base. Expected OBS d >= 0.10 from CRP-IBD meta-analyses. |
| **Drug class** | Anti-IL-23p19 monoclonal antibodies: risankizumab (Skyrizi), guselkumab (Tremfya) |
| **Drug outcome** | Risankizumab received FDA approval for moderate-to-severe Crohn's disease (2022). Guselkumab is approved for related inflammatory conditions and has shown Phase III efficacy in Crohn's. Coded as **Approved**. |
| **Rationale** | The IL23R R381Q variant is one of the tightest instrument-target alignments in the drug-target MR literature: the genetic variant directly reduces signaling through the same receptor targeted by the drug. This family tests whether tight instrument-target alignment produces concordance, as expected. The gastroenterology domain is not represented in any prior amendment. |

**OBS evidence quality concern:** Prospective cohort studies measuring circulating IL-23 and subsequent Crohn's incidence may not exist. If the best available OBS evidence is cross-sectional cytokine data or indirect (CRP as a proxy for gut inflammation), this limitation is flagged. If no prospective or meta-analytic OBS estimate with a point estimate and CI can be located, the family is classified as "construct-limited" and excluded from the scored denominator.

**Prediction:** OBS non-trivial (d >= 0.10 from inflammatory marker meta-analyses). MR causal (IL23R per-allele OR ~ 0.26, CI excludes null, d >> 0.10 after any rescaling). Classification: **concordance**. Predicted drug outcome: **success**. Expected match: **correct**.

---

### Family B3: Complement pathway (Factor D) -> geographic atrophy

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Complement activation (proxied by complement pathway genetic variants) -> geographic atrophy (advanced dry age-related macular degeneration) |
| **Domain** | Ophthalmology (new domain) |
| **MR instrument** | Complement pathway variants: CFH rs1061170 (Y402H), C3 rs2230199 (R102G), CFB rs641153, C2/CFB haplotype variants. These are among the strongest known genetic associations with AMD (Fritsche et al. 2016 Nat Genet). cis-MR and pathway-based MR using these variants have been published. |
| **MR scale** | Per allele (expected for most complement-AMD genetic studies) |
| **Rescaling needed?** | **Yes -- per-allele estimate must be rescaled to per-SD of complement activation**. CFH Y402H has per-allele OR ~ 2.5-3.0 for AMD. Even before rescaling, d = \|ln(2.5)\| x sqrt(3)/pi ~ 0.50, well above 0.10. Rescaling will increase this further. |
| **Expected OBS source** | Observational studies of complement biomarkers (C3a, C5a, complement factor H levels) and AMD/GA. Several cross-sectional and case-control studies report elevated complement activation products in AMD patients. Prospective data on complement biomarkers and AMD incidence are sparser but exist in AREDS and similar cohort studies. Expected OBS d >= 0.10. |
| **Drug class** | Anti-complement Factor D monoclonal antibody: lampalizumab (Genentech/Roche) |
| **Drug outcome** | Lampalizumab failed both Phase III trials (CHROMA and SPECTRI, 2018) for geographic atrophy. Primary endpoint (change in GA lesion area) was not met in either trial. Coded as **Failed**. |
| **Rationale** | This family is declared with the **expectation that the classification rule will produce an incorrect prediction**. The complement pathway is causally implicated in AMD by some of the strongest genetic evidence in all of human genetics (CFH Y402H was one of the first GWAS hits). MR using complement pathway variants will almost certainly classify as "causal." OBS evidence for complement activation and AMD is non-trivial. Therefore the rule will predict concordance (success). But lampalizumab, targeting Factor D specifically, failed Phase III. This represents a **translation-gap** mechanism: the pathway is causal, but the specific drug target (one node among many in the complement cascade) was insufficient for therapeutic benefit. |

**Pathway-specificity caveat:** The MR instruments (CFH, C3, CFB) instrument overall complement pathway activation, not Factor D specifically. Lampalizumab targets Factor D, which acts upstream in the alternative complement pathway. The instrument-target misalignment is structural: no published MR study instruments circulating Factor D levels directly against AMD. This is analogous to Family O2 (IGF-1 -> CRC, where MR instruments the ligand but the drug targets the receptor), but with a larger gap (the MR instruments several pathway nodes, none of which is the drug target).

**Contrast with C3 inhibitors:** Pegcetacoplan (Syfovre, anti-C3) received FDA approval for geographic atrophy in 2023, and avacincaptad pegol (Izervay, anti-C5) was approved the same year. The same complement pathway that lampalizumab failed to drug has been successfully drugged at different nodes. This underscores that pathway-level MR concordance does not guarantee target-specific drug success, and the framework's unit of analysis (exposure-outcome pair, not target-outcome pair) cannot distinguish between druggable and undruggable nodes within a causal pathway.

**Prediction:** OBS non-trivial (d >= 0.10). MR causal (CI excludes null, d >> 0.10). Classification: **concordance**. Predicted drug outcome: **success**. Actual drug outcome: **Failed**. Expected match: **incorrect** (translation-gap miss).

---

### Family B4: Sclerostin -> osteoporotic fracture

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Circulating sclerostin levels -> osteoporotic fracture risk |
| **Domain** | Musculoskeletal / osteoporosis (new domain) |
| **MR instrument** | SOST cis-pQTL variants proxying circulating sclerostin levels. The SOST gene encodes sclerostin, and cis-variants in the SOST region have been used in drug-target MR studies (e.g., Bovijn et al. 2020 Nat Med proteome-wide MR; Zheng et al. 2020). The per-allele effect on circulating sclerostin is well-characterized from protein GWAS. |
| **MR scale** | Per 1 SD decrease in circulating sclerostin (or per allele if only per-allele estimates available) |
| **Rescaling needed?** | Per-SD: No. Per-allele: Yes, standard rescaling applies. |
| **Expected OBS source** | Prospective cohort studies and meta-analyses of circulating sclerostin levels and fracture risk. Several studies from population-based cohorts (e.g., MrOS, AGES-Reykjavik) have reported associations between higher sclerostin and fracture risk, though findings are mixed (some studies report higher sclerostin with lower fracture risk, reflecting complexity of sclerostin as both a marker of bone turnover and a causal mediator). Expected OBS d: uncertain, possibly >= 0.10 from meta-analyses but direction may depend on covariate adjustment. |
| **Drug class** | Anti-sclerostin monoclonal antibody: romosozumab (Evenity, Amgen/UCB) |
| **Drug outcome** | Romosozumab received FDA approval for osteoporosis in postmenopausal women at high fracture risk (2019). The ARCH trial showed 48% reduction in new vertebral fractures and 27% reduction in clinical fractures versus alendronate. Coded as **Approved**. |
| **Rationale** | Tests the classification rule in musculoskeletal disease, a domain with well-characterized genetic architecture (bone mineral density is highly heritable) and clean drug-target MR instruments. Sclerostin inhibition is a mechanistically direct intervention: sclerostin is an osteocyte-secreted inhibitor of Wnt signaling, and its blockade increases bone formation. The drug directly neutralizes the instrumented protein. |

**OBS evidence uncertainty:** The observational relationship between circulating sclerostin and fracture is bidirectional in the literature: some studies report that higher sclerostin predicts higher fracture risk (the "causal" direction consistent with the drug mechanism), while others report the opposite (higher sclerostin in patients with higher bone turnover, a reverse-causation signal). If the meta-analytic OBS estimate is null or in the wrong direction, OBS may be classified as trivial (d < 0.10), producing a "genetic-only signal" classification rather than concordance. This would still predict success (per the classification table), but through a different cell.

**Prediction:** OBS non-trivial (d >= 0.10, assuming meta-analyses resolve the direction toward the causal interpretation). MR causal (SOST cis-MR for BMD/fracture shows significant protective effect of lower sclerostin, CI excludes null, d likely >= 0.10). Classification: **concordance**. Predicted drug outcome: **success**. Expected match: **correct**, contingent on OBS evidence direction.

---

### Family B5: Serotonin transporter -> major depressive disorder

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Serotonin availability (proxied by serotonin transporter function) -> major depressive disorder incidence |
| **Domain** | Psychiatry (same domain as B1; different mechanism) |
| **MR instrument** | SLC6A4 cis-variants (serotonin transporter gene), including the 5-HTTLPR promoter polymorphism and surrounding SNPs. Additional instruments from serotonin-pathway GWAS (TPH2, HTR variants). Moncrieff et al. (2022 Mol Psychiatry) reviewed the full body of evidence including genetic association and MR studies of serotonin markers and depression, finding no consistent support for the serotonin hypothesis. |
| **MR scale** | Per allele (expected for cis-MR of 5-HTTLPR or SLC6A4 SNPs) |
| **Rescaling needed?** | **Yes -- per-allele estimate must be rescaled to per-SD of serotonin transporter activity or serotonin availability**. However, the entire premise of this family is that MR will show a null result, so the rescaling question may be moot. |
| **Expected OBS source** | Meta-analyses of serotonin-related biomarkers and depression. Peripheral serotonin measures (platelet serotonin, plasma tryptophan) have been associated with depression in numerous studies, though effect sizes are modest and confounding is pervasive. The Moncrieff et al. (2022) umbrella review found weak and inconsistent observational evidence. Expected OBS d: uncertain, possibly >= 0.10 from some meta-analyses of tryptophan/serotonin markers and depression, but possibly < 0.10 from better-controlled studies. |
| **Drug class** | Selective serotonin reuptake inhibitors (SSRIs): fluoxetine (Prozac), sertraline (Zoloft), escitalopram (Lexapro) |
| **Drug outcome** | SSRIs are among the most widely prescribed drug classes in history. Multiple SSRIs have FDA approval for major depressive disorder (fluoxetine 1987, sertraline 1991, escitalopram 2002, etc.). Meta-analyses (Cipriani et al. 2018 Lancet) confirm SSRIs are more effective than placebo for MDD, though effect sizes are debated. Coded as **Approved**. |
| **Rationale** | This family is declared with the **expectation that the classification rule will produce an incorrect prediction or an ambiguous/excluded result**. The serotonin hypothesis of depression has been seriously challenged by the Moncrieff et al. (2022) umbrella review, which found no consistent evidence that serotonin levels or serotonin transporter activity are causally related to depression. If MR is null, the rule predicts discordance (failure). But SSRIs are unambiguously approved. This represents a **mechanism-bypass** failure mode: the drug works, but possibly through a mechanism different from the one instrumented by MR (e.g., neuroplasticity, BDNF signaling, anti-inflammatory effects). The framework, which asks "does the instrumented exposure cause the disease?", cannot capture drug efficacy that operates through unmeasured or uninstrumented mechanisms. |

**OBS evidence risk:** If the OBS d is < 0.10 (plausible given the weak evidence reviewed by Moncrieff et al.), this family classifies as "null concordance" (both OBS and MR below threshold) and is excluded from the scored denominator as ambiguous. This would be informative but unscored. If OBS d >= 0.10, the family is scored and expected to produce a miss.

**Dual-psychiatry design note:** Families B1 and B5 share the same disease outcome (MDD) but instrument completely different exposures (IL-6 signaling vs serotonin transport). They test the classification rule from opposite directions:

| Family | OBS | MR | Classification | Drug outcome | Match? |
|--------|-----|-----|----------------|-------------|--------|
| B1 (IL-6 -> MDD) | Non-trivial | Null | Discordance -> Failure | Failed (sirukumab) | Correct |
| B5 (Serotonin -> MDD) | Non-trivial? | Null | Discordance -> Failure | Approved (SSRIs) | Incorrect |

If both predictions hold, the framework correctly identifies a zombie mechanism (IL-6/depression confounding) and incorrectly identifies a mechanism-bypass case (serotonin/depression where the drug works through uninstrumented pathways). This pair maps a boundary of the framework: discordance predicts failure when the causal pathway is genuinely absent, but not when the drug achieves efficacy through a different route than the instrumented exposure.

**Prediction:** OBS uncertain (d possibly >= 0.10 from some meta-analyses, possibly < 0.10 from Moncrieff-era reviews). MR null (no consistent MR evidence for serotonin -> depression). If OBS non-trivial: Classification **discordance**, predicted drug outcome **failure**, actual drug outcome **Approved**. Expected match: **incorrect** (mechanism-bypass miss). If OBS trivial: Classification **null concordance**, **ambiguous**, excluded from denominator.

---

## Summary table of blind declarations

| # | Family | Domain | Drug | Drug outcome | Instruments shared with | Expected classification | Expected match |
|---|--------|--------|------|-------------|------------------------|------------------------|----------------|
| B1 | IL-6 -> MDD | Psychiatry | Sirukumab | Failed | IL-6R cardio families | Discordance -> Failure | Correct |
| B2 | IL-23 -> Crohn's | Gastroenterology | Risankizumab | Approved | None | Concordance -> Success | Correct |
| B3 | Complement (Factor D) -> GA | Ophthalmology | Lampalizumab | Failed | None | Concordance -> Success | **Incorrect** |
| B4 | Sclerostin -> fracture | Musculoskeletal | Romosozumab | Approved | None | Concordance -> Success | Correct |
| B5 | Serotonin -> MDD | Psychiatry | SSRIs | Approved | None | Discordance -> Failure OR Ambiguous | **Incorrect or excluded** |

**Expected scorecard:** Of the 5 families:
- 2 expected construct-limited or ambiguous risk (B2 OBS quality, B5 OBS threshold)
- 3 expected cleanly scoreable (B1, B3, B4)
- Of those scored: 2 expected correct (B1, B4), 1 expected incorrect (B3)
- If all 5 are scored: 2 correct (B1, B4), 2 incorrect (B3, B5), 1 correct (B2) = 3/5
- If B5 is excluded as ambiguous: 2 correct (B1, B4), 1 incorrect (B3), 1 correct (B2) = 3/4

---

## Instrument-scale declarations

| # | Family | MR scale | Rescaling needed? | Rationale |
|---|--------|----------|-------------------|-----------|
| B1 | IL-6 -> MDD | Per 1 SD CRP (IL-6R blockade proxy) | No | IL6R MR studies report per-SD CRP |
| B2 | IL-23 -> Crohn's | Per allele (IL23R coding variant) | **Yes** | Per-allele OR so large (~ 0.26) that d >> 0.10 under any rescaling; may be scale-unresolved if per-allele exposure change unavailable |
| B3 | Complement -> GA | Per allele (CFH Y402H and others) | **Yes** | Per-allele ORs 2.0-3.0; d >> 0.10 before rescaling |
| B4 | Sclerostin -> fracture | Per 1 SD sclerostin (if pQTL-based) or per allele | Depends on source study | Per-SD if cis-pQTL MR; per-allele if GWAS-based |
| B5 | Serotonin -> MDD | Per allele (5-HTTLPR or SLC6A4 SNPs) | **Yes** | Predicted null regardless of rescaling |

---

## Hypotheses

### H_blind1: Blind families add at least one correct classification to the exploratory denominator

At least 2 of the scored blind families (those not excluded as construct-limited, data-not-available, or ambiguous) are correctly classified.

**Decision criterion:** >= 2 correct out of scored blind families. This is a weak bar deliberately, because 2 of the 5 families are declared with the expectation of incorrect classification.

### H_blind2: The two pre-specified failure modes are observed

At least one of the following occurs:
1. Family B3 produces a concordance classification and the drug failed (translation-gap miss)
2. Family B5 produces a discordance classification and the drug succeeded (mechanism-bypass miss)

**Decision criterion:** >= 1 of the two pre-specified failure modes is observed. If neither occurs (both families classify correctly or are excluded), the failure modes were wrongly anticipated and the rule is more robust to these challenges than expected.

### H_blind3: The B1-B5 pair demonstrates pathway specificity within psychiatry

Families B1 (IL-6 -> MDD, expected discordance) and B5 (Serotonin -> MDD, expected discordance) receive the same classification (both discordance) but map to different drug outcomes (failure vs success), producing one correct and one incorrect prediction. This demonstrates that same-disease families with different mechanisms can produce divergent accuracy, and that the framework's exposure-level classification does not reduce to a disease-level prediction.

**Decision criterion:** B1 and B5 both classified as discordance, B1 correct, B5 incorrect. If either family is excluded (construct-limited or ambiguous), H_blind3 is not testable.

### H_blind4: Combined accuracy including blind families does not degrade

Adding the blind families to the full exploratory denominator does not reduce the combined exploratory accuracy by more than 10 percentage points relative to the Amendment 1 + Amendment 2 exploratory accuracy.

**Decision criterion:** Accuracy(all exploratory families including blind) >= Accuracy(exploratory families excluding blind) - 0.10. This acknowledges that the blind families include deliberately challenging cases and accepts modest accuracy dilution.

---

## Pre-specified boundary conditions (new)

| Boundary type | Family | Mechanism | Expected consequence |
|---------------|--------|-----------|---------------------|
| Translation gap (pathway vs target) | B3 (Complement -> GA) | MR instruments the complement pathway broadly; drug targets Factor D specifically; C3 and C5 inhibitors succeeded for the same disease | Concordance classification, drug failed; a pathway-level causal signal does not guarantee target-level drug success |
| Mechanism bypass | B5 (Serotonin -> MDD) | MR and OBS may both be null/weak for serotonin-depression; SSRIs succeed through uninstrumented mechanisms (neuroplasticity, anti-inflammation) | Discordance or ambiguous classification; drug succeeded through pathway the framework cannot assess |
| OBS evidence quality | B2 (IL-23 -> Crohn's) | Prospective OBS data for IL-23 specifically and Crohn's may be limited to cross-sectional cytokine studies | Family may be construct-limited if no adequate OBS estimate exists |
| OBS direction ambiguity | B4 (Sclerostin -> fracture) | Observational sclerostin-fracture association is bidirectional in the literature (causal vs reverse-causation) | OBS d magnitude and direction uncertain; may classify as trivial if reverse-causation studies dominate the meta-analytic estimate |
| Zombie identification in psychiatry | B1 (IL-6 -> MDD) | Strong OBS confounding (BMI, smoking, inactivity all raise CRP and depression risk) should produce non-trivial OBS with null MR | Clean test of whether the framework identifies psychiatric zombie mechanisms |

---

## Anticipated results under different scenarios

**Best case (3-4/5 correct, pre-specified misses account for all errors):**
The framework correctly identifies B1 as a zombie (discordance -> failure), B2 as concordance (success), and B4 as concordance (success). B3 and B5 produce the pre-specified misses (translation gap and mechanism bypass). This outcome extends the framework to four new domains while mapping two distinct failure-mode boundaries.

**Moderate case (2-3/5 correct, some unexpected misses):**
One or more families produce misses not anticipated by the boundary conditions. For example: B4 misclassifies because OBS evidence is in the reverse-causation direction, or B2 is construct-limited. This outcome suggests the new domains introduce measurement challenges beyond what the existing rule handles.

**Worst case (<2/5 correct):**
The framework fails on most blind families. This would suggest that domain-knowledge-based family selection without data peeking produces systematically harder cases than the original domain-by-domain extension, or that the four new domains have structural features (weaker OBS evidence, more complex pathway architectures) that the two-criterion rule cannot accommodate.

---

## Inclusion in reporting

All five families and their outcomes are reported in full, regardless of accuracy. The blind-batch results are reported:
1. Separately from all other exploratory results (blind-batch accuracy)
2. Pooled with the full exploratory denominator (combined exploratory accuracy)
3. Never pooled with the primary pre-registered accuracy (neuro + cardio + autoimmune)

The blinding status of this amendment is stated in any manuscript that reports these results. Pre-specified misses (B3, B5) are reported as domain-of-validity boundaries, not excluded from the denominator.

---

## Power considerations

With 5 blind families (expected 3-4 scoreable after potential construct-limited exclusions), statistical testing within the blind batch alone is underpowered. A binomial test at alpha=0.05 against H0: accuracy=0.50 requires all scoreable families to classify correctly to reach significance (e.g., 4/4 has one-sided p=0.0625, not significant; 3/3 has p=0.125). The blind batch is therefore descriptive and hypothesis-generating, not independently confirmatory. Its primary contribution is mapping boundary conditions (translation gap, mechanism bypass) and testing blind generalizability.
