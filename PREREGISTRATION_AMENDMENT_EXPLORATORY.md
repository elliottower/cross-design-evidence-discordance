# Pre-Registration Amendment: Exploratory Three-Domain Extension

**Status:** FROZEN (pending commit SHA)
**Date:** 2026-07-09
**Parent document:** PREREGISTRATION.md (commit SHA: b96d10a)
**Scope:** Exploratory extension of the frozen classification rule to three new disease domains (oncology, respiratory, metabolic/endocrine), comprising nine additional mechanism families.

**Integrity protocol:** This amendment, the family pre-specifications, instrument declarations, and hypotheses are committed before any MR or OBS effect sizes are pulled for the nine families below. The same freeze-before-data protocol from the parent pre-registration applies. The commit SHA will be recorded here after freeze.

**Commit SHA:** 1f300a9

---

## Relationship to primary pre-registration

This amendment declares an **exploratory extension** to the primary pre-registration. The nine families below are **excluded from the primary scored accuracy** (neuro + cardio + autoimmune). They constitute a separate, exploratory denominator reported alongside the primary result. The reason for exploratory status: these domains were identified after the autoimmune extension was designed, and the family selection process — while pre-specified here — was informed by awareness of which domains have clean MR instruments, introducing a non-trivial selection channel.

All results from these families will be reported in full (including misses), clearly labeled as exploratory, and separated from the primary accuracy in both abstract and results sections.

---

## Frozen classification rule

The classification rule is unchanged from the parent document (PREREGISTRATION.md, Section "Frozen classification rule"). For reference:

| OBS | MR | Classification | Prediction |
|-----|-----|----------------|------------|
| Non-trivial (d >= 0.10) | Null | Qualitative discordance | Failure |
| Non-trivial (d >= 0.10) | Causal (CI excl. null AND d >= 0.10) | Concordance | Success |
| Trivial (d < 0.10) | Null | Null concordance | Ambiguous |
| Trivial (d < 0.10) | Causal | Genetic-only signal | Success |

All definitions (Cohen's d from OR, exposure-comparable scale, per-allele rescaling, ambiguous-prediction scoring) carry forward without modification.

---

## Domain 4: Oncology

### Family O1: Vitamin D -> colorectal cancer

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Circulating 25(OH)D -> colorectal cancer incidence |
| **MR instrument** | Genetic variants associated with circulating 25-hydroxyvitamin D levels (e.g., DHCR7, CYP2R1, GC, CYP24A1 from Jiang et al. 2019 or equivalent GWAS-based instruments) |
| **MR scale** | Per 1 SD increase in 25(OH)D |
| **Rescaling needed?** | No (per-SD is exposure-comparable) |
| **Expected OBS source** | Meta-analytic OR from pooled prospective cohort/case-control studies of circulating 25(OH)D and CRC incidence |
| **Drug class** | Vitamin D supplementation |
| **Drug outcome** | FDA has not approved vitamin D supplementation for colorectal cancer prevention. Large RCTs (VITAL: NCT01169259) did not show significant reduction in CRC incidence. Drug outcome coded as **Failed**. |
| **Rationale** | Tests the classification rule in a chemoprevention context where the exposure (a nutrient) is the intervention itself, removing the instrument-target alignment concern present in cytokine families. |

### Family O2: IGF-1 -> colorectal cancer

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Circulating IGF-1 -> colorectal cancer incidence |
| **MR instrument** | Genetic variants associated with circulating IGF-1 levels (from GWAS of IGF-1 concentrations) |
| **MR scale** | Per 1 SD increase in circulating IGF-1 |
| **Rescaling needed?** | No (per-SD is exposure-comparable) |
| **Expected OBS source** | Meta-analytic OR from prospective studies of circulating IGF-1 and CRC risk |
| **Drug class** | IGF-1 receptor (IGF-1R) inhibitors: ganitumab (AMG 479), figitumumab (CP-751,871) |
| **Drug outcome** | Both ganitumab and figitumumab failed in Phase III or late-stage trials for solid tumors. No IGF-1R inhibitor has received FDA approval for CRC or any solid tumor. Drug outcome coded as **Failed**. |
| **Rationale** | IGF-1R inhibitors target the receptor rather than the circulating ligand. The MR instrument (circulating IGF-1 levels) and the drug target (IGF-1R signaling) are on the same pathway but at different nodes. This is analogous to the IL-6 ligand vs IL-6R instrument-target alignment issue noted in the parent pre-registration. |

### Family O3: Estrogen -> breast cancer

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Circulating sex hormones (estradiol / estrogen pathway) -> breast cancer incidence |
| **MR instrument** | Genetic variants associated with circulating sex hormone levels (estradiol, SHBG) from GWAS |
| **MR scale** | Per allele (expected for most MR studies of sex hormone variants) |
| **Rescaling needed?** | **Yes — must rescale to per-SD circulating estradiol or equivalent** |
| **Expected OBS source** | Meta-analytic OR from prospective studies of endogenous hormone levels and breast cancer risk |
| **Drug class** | Selective estrogen receptor modulators (tamoxifen) and aromatase inhibitors (anastrozole, letrozole, exemestane) |
| **Drug outcome** | Tamoxifen is FDA-approved for breast cancer risk reduction. Aromatase inhibitors are FDA-approved for breast cancer treatment. Drug outcome coded as **Approved**. |
| **Rationale** | See "Small-effect boundary condition" below. |

**Small-effect boundary condition (pre-specified):** Estrogen modulation for breast cancer is a known positive-control family: the drugs are among the most successful in oncology. The classification rule should classify it as concordance (predict success). However, per-allele MR estimates for sex hormone variants typically produce small effect sizes per allele because common variants produce modest perturbations in circulating estradiol. After per-SD rescaling, the MR d may fall below 0.10 even though the causal pathway is genuine, because the drug produces a pharmacological perturbation (near-complete estrogen suppression with aromatase inhibitors) orders of magnitude larger than what germline variants achieve.

If the rescaled MR d falls below 0.10, this family will classify as MR null and produce a discordance prediction (failure) — which will be falsified by the approved drug. This would represent a **known failure mode** of the classification rule: it cannot detect causal pathways where germline variants produce effects below the biological-relevance threshold but pharmacological doses achieve therapeutic benefit. We pre-specify this as a "pharmacological amplification" boundary case, distinct from both zombie mechanisms and translation-gap mechanisms.

**Decision criterion for boundary interpretation:** If Family O3 is the sole miss in the oncology domain, and the miss is attributable to MR d falling below 0.10 after rescaling despite the CI excluding the null, this is coded as a pharmacological-amplification miss and reported as a domain-of-validity boundary rather than a rule failure.

---

## Domain 5: Respiratory

### Family R1: Eosinophils -> asthma

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Blood eosinophil count -> asthma risk |
| **MR instrument** | Genetic variants associated with blood eosinophil count (from GWAS of eosinophil counts, e.g., Astle et al. 2016 or UK Biobank blood cell trait GWAS) |
| **MR scale** | Per 1 SD increase in eosinophil count |
| **Rescaling needed?** | No (per-SD is exposure-comparable) |
| **Expected OBS source** | Meta-analytic OR from observational studies of blood eosinophil count and asthma prevalence/incidence |
| **Drug class** | Anti-IL-5 biologics: mepolizumab (Nucala) |
| **Drug outcome** | Mepolizumab is FDA-approved for severe eosinophilic asthma (2015) and related eosinophilic conditions. Drug outcome coded as **Approved**. |
| **Rationale** | See "Subtype-specificity construct mismatch" below. |

**Subtype-specificity construct mismatch (pre-specified):** Mepolizumab is approved for **severe eosinophilic asthma**, a clinical subtype defined by elevated eosinophils and frequent exacerbations. MR instruments for eosinophil count are derived from population-level GWAS and instrument eosinophil count against **asthma** as a broad diagnostic category. The etiologic claim (eosinophils cause asthma) and the therapeutic claim (reducing eosinophils treats severe eosinophilic asthma) address different constructs: population-level disease incidence vs subtype-specific symptom control.

If the OBS and MR estimates address "asthma" broadly and classify as concordant, the drug outcome (approved for the severe subtype) should be scored as a match. If MR estimates address "asthma" broadly but show a null result (because eosinophils are causal for only a subtype, diluting the population-level signal), the classification would be discordance predicting failure — falsified by the subtype-specific approval. This would represent a **construct-dilution** failure mode where MR's population-level instrument misses a subtype-specific causal pathway.

### Family R2: IL-4R-alpha -> asthma

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | IL-4/IL-13 signaling pathway -> asthma risk |
| **MR instrument** | cis-MR variants in the IL4R/IL13 gene region |
| **MR scale** | Per allele (expected for cis-MR) |
| **Rescaling needed?** | **Yes — must rescale to per-SD of relevant biomarker (IgE or cytokine level)** |
| **Expected OBS source** | Meta-analytic OR from observational studies of IgE levels, IL-4/IL-13 cytokine levels, or atopic markers and asthma risk |
| **Drug class** | Dupilumab (Dupixent): anti-IL-4 receptor alpha monoclonal antibody |
| **Drug outcome** | Dupilumab is FDA-approved for moderate-to-severe asthma (2018), atopic dermatitis (2017), and other type-2 inflammatory conditions. Drug outcome coded as **Approved**. |
| **Rationale** | This family shares the cis-MR instrument class (IL4R/IL13 variants) with the autoimmune domain's IL-4R-alpha -> atopic dermatitis family (Family 7 in the parent pre-registration). Construct-definition challenges noted for the atopic dermatitis family may recur here: the MR instrument may capture broad type-2 inflammation rather than asthma-specific pathway activation. |

**Construct-definition note:** IL-4R-alpha is a shared receptor for both IL-4 and IL-13. The MR instrument (IL4R variants) may instrument the combined IL-4/IL-13 signaling pathway rather than either cytokine individually. The drug (dupilumab) blocks both IL-4 and IL-13 signaling by targeting the shared receptor subunit. This instrument-target alignment is tighter than in families where the MR instrument and drug target act at different pathway nodes.

### Family R3: TSLP -> asthma

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Thymic stromal lymphopoietin (TSLP) signaling -> asthma risk |
| **MR instrument** | cis-MR variants in the TSLP gene region |
| **MR scale** | Per allele (expected for cis-MR) |
| **Rescaling needed?** | **Yes — must rescale to per-SD of circulating TSLP or equivalent biomarker** |
| **Expected OBS source** | Observational studies of TSLP levels or TSLP-related markers and asthma risk |
| **Drug class** | Tezepelumab (Tezspire): anti-TSLP monoclonal antibody |
| **Drug outcome** | Tezepelumab is FDA-approved for severe asthma (2021), notably without requiring an eosinophilic or type-2 biomarker for eligibility. Drug outcome coded as **Approved**. |
| **Rationale** | TSLP acts upstream of the eosinophilic/type-2 cascade. Tezepelumab's broad-label approval (not restricted to eosinophilic subtype) may make it a cleaner test of the etiologic claim than mepolizumab (Family R1), which is restricted to the eosinophilic subtype. |

**Construct-definition note:** TSLP is an epithelial cytokine acting upstream of multiple type-2 inflammatory pathways (IL-4, IL-5, IL-13). Published MR studies for TSLP and asthma may be sparse or limited to cis-eQTL/pQTL instruments. If no dedicated MR study with a point estimate and CI exists at the time of data extraction, this family is classified as **data not available** and excluded from the scored denominator.

---

## Domain 6: Metabolic/endocrine

### Family M1: SGLT2 -> heart failure

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | SGLT2-mediated renal glucose reabsorption -> heart failure risk |
| **MR instrument** | cis-MR variants in the SLC5A2 gene region (encoding SGLT2) |
| **MR scale** | Per allele (expected for cis-MR) |
| **Rescaling needed?** | **Yes — must rescale to per-SD of SGLT2-related biomarker (e.g., HbA1c, urinary glucose)** |
| **Expected OBS source** | Observational association between type 2 diabetes (or glycemic markers) and heart failure incidence |
| **Drug class** | SGLT2 inhibitors: empagliflozin (Jardiance), dapagliflozin (Farxiga) |
| **Drug outcome** | Empagliflozin and dapagliflozin are both FDA-approved for heart failure with reduced ejection fraction (2020-2021) and heart failure broadly (expanded labels). Drug outcome coded as **Approved**. |
| **Rationale** | See "Instrument-sensitivity" below. |

**Instrument-sensitivity (pre-specified):** SGLT2 inhibitors were developed for type 2 diabetes but showed unexpected heart failure benefit in cardiovascular outcome trials (EMPA-REG, DAPA-HF, EMPEROR-Reduced). The mechanism of HF benefit may be partially or wholly independent of glycemic control (proposed mechanisms include natriuresis, ketone metabolism, and cardiac energetics).

This creates an **instrument-selection sensitivity**: cis-MR variants in SLC5A2 that instrument glycemic effects (HbA1c reduction) may not capture the cardioprotective mechanism. Different instrument selections could produce divergent MR results:

- **Diabetes-focused instrument:** SLC5A2 variants -> HbA1c -> HF risk. This instruments the glycemic pathway and may show a weak or null effect on HF if the HF benefit is glucose-independent.
- **HF-focused instrument:** SLC5A2 variants -> HF directly (using cis-MR with HF as the outcome). This instruments the total effect of SGLT2 perturbation on HF, including non-glycemic mechanisms.

We pre-specify that **both instrument selections will be attempted** if data permit, and both results reported. If they diverge (one causal, one null), the divergence itself is an informative finding about the pathway specificity of the therapeutic mechanism.

### Family M2: GLP-1R -> T2D/obesity

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | GLP-1 receptor signaling -> type 2 diabetes risk and/or obesity |
| **MR instrument** | cis-MR variants in the GLP1R gene region |
| **MR scale** | Per allele (expected for cis-MR) |
| **Rescaling needed?** | **Yes — must rescale to per-SD of relevant biomarker (BMI, HbA1c, or fasting glucose)** |
| **Expected OBS source** | Observational studies of GLP-1-related markers, incretin levels, or T2D/obesity risk |
| **Drug class** | GLP-1 receptor agonists: semaglutide (Ozempic/Wegovy), liraglutide (Victoza/Saxenda) |
| **Drug outcome** | Semaglutide and liraglutide are FDA-approved for T2D (2010/2017) and obesity/weight management (2014/2021). Drug outcome coded as **Approved**. |
| **Rationale** | See "Multi-construct therapeutic claim" below. |

**Multi-construct therapeutic claim (pre-specified):** GLP-1R agonists are approved for two distinct indications (T2D, obesity) and show cardiovascular benefit in outcome trials (SELECT, SUSTAIN-6). The etiologic claim (GLP-1R signaling affects metabolic disease) and the therapeutic claim (GLP-1R agonists treat T2D/obesity) are well-aligned. However, the cardiovascular benefit represents a distinct construct: GLP-1R -> CV events is a separate exposure-outcome pair from GLP-1R -> T2D.

Per the family definition rule (families defined at the exposure x outcome level), GLP-1R -> T2D/obesity and GLP-1R -> CV events would be separate families. We pre-register GLP-1R -> T2D/obesity as the primary family for this extension because the MR evidence and drug development program were oriented around metabolic endpoints. The CV benefit, if scored separately, would require its own MR instrument selection and OBS evidence base.

### Family M3: Uric acid -> gout

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Serum uric acid levels -> gout incidence |
| **MR instrument** | Variants in urate transporter genes: SLC2A9, ABCG2, SLC22A12, and other GWAS-identified urate-associated loci |
| **MR scale** | Per 1 SD increase in serum urate |
| **Rescaling needed?** | No (per-SD is exposure-comparable) |
| **Expected OBS source** | Meta-analytic OR from prospective studies of serum urate and gout incidence |
| **Drug class** | Xanthine oxidase inhibitors (allopurinol, febuxostat) and uricosurics (probenecid, lesinurad) |
| **Drug outcome** | Allopurinol and febuxostat are FDA-approved for chronic gout / hyperuricemia management. Drug outcome coded as **Approved**. |
| **Rationale** | Uric acid -> gout is expected to be a strong concordance case: the causal relationship between hyperuricemia and gout is well-established, and urate-lowering therapy is the standard of care. This family serves as a positive control for the classification rule in the metabolic domain. Note: the parent pre-registration included uric acid -> CVD (cardiometabolic domain) as an ambiguous family (both OBS and MR d < 0.10). The gout family is distinct because gout is a direct consequence of urate crystallization, whereas CVD is a downstream systemic outcome with a less direct mechanistic link. |

---

## Instrument-scale declarations (summary table)

| # | Family | MR scale | Rescaling needed? | Rationale |
|---|--------|----------|-------------------|-----------|
| O1 | Vitamin D -> CRC | Per 1 SD 25(OH)D | No | GWAS-derived instruments report per-SD |
| O2 | IGF-1 -> CRC | Per 1 SD circulating IGF-1 | No | GWAS-derived instruments report per-SD |
| O3 | Estrogen -> breast cancer | Per allele (expected) | **Yes** | Must rescale to per-SD circulating estradiol |
| R1 | Eosinophils -> asthma | Per 1 SD eosinophil count | No | Blood cell trait GWAS reports per-SD |
| R2 | IL-4R-alpha -> asthma | Per allele (expected) | **Yes** | Must rescale to per-SD IgE or cytokine level |
| R3 | TSLP -> asthma | Per allele (expected) | **Yes** | Must rescale to per-SD TSLP or equivalent |
| M1 | SGLT2 -> HF | Per allele (expected) | **Yes** | Must rescale to per-SD of relevant biomarker |
| M2 | GLP-1R -> T2D/obesity | Per allele (expected) | **Yes** | Must rescale to per-SD BMI or HbA1c |
| M3 | Uric acid -> gout | Per 1 SD serum urate | No | GWAS-derived instruments report per-SD |

Families requiring rescaling (O3, R2, R3, M1, M2) follow the scale harmonization procedure from the parent pre-registration: OR_per_SD = OR_per_allele^(1 / delta_SD_per_allele). If the per-allele exposure change is unavailable, the family is flagged as "scale-unresolved."

---

## Hypotheses

### H_ext1: Exploratory extension classification accuracy

The frozen two-criterion rule, applied to the nine exploratory families, will correctly classify at least 5 of the 9 families (56%).

**Decision criterion:** >= 5/9 families correctly classified (excluding any families classified as ambiguous or data-not-available from the scored denominator).

**Interpretation guide:**

- 8-9/9 correct: The classification rule generalizes across six disease domains. This would represent the strongest evidence for domain-general validity, though the exploratory status limits inferential weight.
- 6-7/9 correct: Partial generalization. Misses concentrated in specific boundary conditions (pharmacological amplification, construct dilution, instrument sensitivity) would support the rule's validity within its domain-of-applicability while mapping its edges.
- 5/9 correct: Marginal. The rule performs above chance but with enough misses to suggest domain-specific limitations.
- < 5/9 correct: The rule does not generalize to these domains. Report as a null result bounding the rule's applicability.

### H_ext2: At least one boundary condition is observed

At least one of the four pre-specified boundary conditions (pharmacological amplification in O3, construct dilution in R1, instrument sensitivity in M1, multi-construct divergence in M2) will produce a classification that differs from the drug outcome.

**Decision criterion:** >= 1 boundary case identified. This hypothesis is directional: we expect the misses, if any, to concentrate at the pre-specified boundary conditions rather than at families with clean instrument-target alignment.

**Interpretation:** If all pre-specified boundary families classify correctly, the boundary conditions were over-anticipated and the rule is more robust than expected. If misses occur at non-boundary families, this indicates failure modes not captured by the pre-specified typology.

### H_ext3: Positive controls classify correctly

Families M3 (uric acid -> gout) and R1 (eosinophils -> asthma, if eosinophil MR d is above threshold) are expected to classify as concordance and predict success. These represent cases where the causal pathway is well-established and the drug directly targets the instrumented exposure.

**Decision criterion:** Both positive-control families classify as concordance and match the drug outcome. A miss on either positive control would indicate a systematic problem with the classification rule or the scale harmonization procedure, not a domain-of-validity boundary.

### H_ext4: Combined accuracy across all six domains exceeds chance

Across all six domains (neuro + cardio + autoimmune + oncology + respiratory + metabolic/endocrine), the classification rule correctly classifies significantly more families than expected by chance (50%).

**Decision criterion:** Binomial test p < 0.05 for the proportion of correct classifications across all unambiguous families in the combined six-domain sample. This test is reported as exploratory because the three new domains were not pre-registered before the autoimmune results were obtained.

---

## Pre-specified boundary conditions (summary)

| Boundary type | Family | Mechanism | Expected consequence |
|---------------|--------|-----------|---------------------|
| Pharmacological amplification | O3 (Estrogen -> breast cancer) | Germline variants produce small per-SD perturbation; drug produces near-complete pathway blockade | MR d may fall below 0.10 despite causal pathway being genuine; rule predicts failure, drug succeeded |
| Construct dilution | R1 (Eosinophils -> asthma) | Population-level MR instruments dilute subtype-specific causal signal | MR may show null for "asthma" broadly while drug is approved for severe eosinophilic subtype |
| Instrument sensitivity | M1 (SGLT2 -> HF) | Glycemic vs non-glycemic pathways produce different MR results for same drug | Different instrument selections may produce divergent classifications |
| Multi-construct divergence | M2 (GLP-1R -> T2D/obesity) | Etiologic claim (metabolic) and therapeutic expansion (CV benefit) address different constructs | Rule may classify metabolic endpoint correctly but cannot extrapolate to CV benefit without separate family |
| Construct definition | R2, R3 (IL-4R-alpha, TSLP -> asthma) | Upstream pathway instruments may not map cleanly to disease-level MR estimates | Similar challenges to IL-4R-alpha -> atopic dermatitis in autoimmune domain |

---

## Inclusion and exclusion criteria

Carried forward from the parent pre-registration without modification:

1. At least one published MR study with a point estimate and CI for the exposure-disease association.
2. At least one published observational meta-analysis or large cohort study with a point estimate.
3. At least one drug targeting the mechanism with a known regulatory outcome.
4. MR and OBS estimates must address the same exposure-disease pair.

Exclusions:
1. Families where the only MR estimate is from an undedicated druggable-genome screen.
2. Families where instrument-target misalignment is too severe to classify.
3. Families where OBS evidence is entirely from unadjusted case-control studies.

**Additional exclusion for this amendment:** If a family's MR estimate cannot be located in the published literature at the time of data extraction (no dedicated MR study exists), the family is classified as "data not available" and excluded from the scored denominator. This applies especially to Family R3 (TSLP -> asthma), where published MR evidence may be limited.

---

## Procedure

For each of the nine families:

1. Search PubMed for the most recent and comprehensive MR study instrumenting the specified exposure against the specified outcome. Record PMID, instrument SNPs, MR method, point estimate, and CI.
2. Search PubMed for the most recent meta-analytic or large-cohort observational estimate. Record PMID, study design, point estimate, and CI.
3. Declare the MR scale. Apply scale harmonization if per-allele.
4. Compute d for both estimates using the Chinn formula (d = |ln(OR)| x sqrt(3) / pi).
5. Apply the frozen two-criterion classification rule.
6. Compare to known drug outcome.
7. Record all results including misses, boundary-condition flags, and scale-unresolved flags.

---

## What counts as success for the exploratory extension

1. At least 5/9 exploratory families correctly classified (H_ext1).
2. Pre-specified boundary conditions account for the majority of misses (H_ext2).
3. Positive-control families (M3, R1) classify correctly (H_ext3).
4. Combined six-domain accuracy remains significant (H_ext4).

If all four criteria are met, the exploratory extension supports expanding the pre-registered domain set in future work. If criteria 1-3 are met but criterion 4 fails (combined significance lost), the new domains diluted the signal and require domain-specific investigation.

## What counts as failure for the exploratory extension

1. Fewer than 5/9 exploratory families correctly classified.
2. Misses occur at positive-control families (M3, R1) rather than at pre-specified boundary conditions.
3. Combined six-domain accuracy falls below significance.

Any of these outcomes limits the rule's generalizability claims and is reported as such.

## What we report either way

All nine family-level results, including misses, boundary-condition flags, instrument-sensitivity analyses (for M1), and scale-unresolved flags. Pre-specified boundary conditions are evaluated against observed misses. The exploratory denominator is reported separately from the primary denominator in all tables and figures. If fewer than 6 of the 9 families yield usable MR + OBS estimates, the extension is reported as underpowered and descriptive only.

---

## Sensitivity analyses (carried forward)

The same sensitivity analyses from the parent pre-registration apply to the exploratory families:

- **S1 (Threshold sensitivity):** Repeat classifications at d = 0.08, 0.10, 0.12, 0.15.
- **S2 (Instrument-scale sensitivity):** For per-allele families (O3, R2, R3, M1, M2), report classifications under strict rule, CI-only rule, and d-only rule.
- **S3 (Leave-one-domain-out):** Extended to six domains. Each domain is held out in turn; accuracy reported for the held-out domain with the threshold trained on the remaining five.

**Additional sensitivity for this amendment:**

- **S_ext1 (Instrument-selection sensitivity for SGLT2):** Report M1 classification under both diabetes-focused and HF-focused cis-MR instrument selections, if both are available in the literature.
- **S_ext2 (Construct-specificity for eosinophils):** If MR studies exist for both "asthma" broadly and "severe/eosinophilic asthma" specifically, report R1 classification under both outcome definitions.

---

## Effector-neutralization boundary (extension)

The effector-neutralization boundary pre-specified in the parent document (for autoimmune cytokine-target families) also applies to respiratory families R2 (IL-4R-alpha -> asthma) and R3 (TSLP -> asthma). These biologics neutralize upstream epithelial or type-2 cytokines. If germline variants perturbing baseline cytokine expression do not track asthma risk at the population level, the classification rule may produce discordance predictions that are falsified by drug approval. As in the autoimmune domain, such misses are scored (not excluded) and reported as domain-of-validity boundaries.

---

## Power considerations

With the autoimmune extension (target n ~ 23 scored families in the primary denominator) plus these 9 exploratory families (target n ~ 30-32 combined), the binomial test has power > 0.97 at a true accuracy of 0.80 (from the parent pre-registration's power table). The exploratory families contribute to the combined H_ext4 test but not to the primary H1/H3 tests.

For the exploratory-only denominator (n = 9), a binomial test at alpha = 0.05 against H0: accuracy = 0.50 has limited power: achieving significance requires >= 8/9 correct (one-sided p = 0.020) or 7/9 (p = 0.090, not significant). The exploratory extension is therefore powered to detect strong generalization (>= 8/9) but not moderate generalization (6-7/9). This limitation is accepted given the exploratory status; the primary contribution of these families is mapping boundary conditions, not achieving statistical significance in isolation.
