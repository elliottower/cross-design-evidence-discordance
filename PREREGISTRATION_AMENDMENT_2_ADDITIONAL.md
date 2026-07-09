# Pre-Registration Amendment 2: Additional Extension Families

**Status:** FROZEN (pending commit SHA)
**Date:** 2026-07-09
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9)
**Scope:** Two additional mechanism families added to the exploratory extension, expanding from 9 to 11 families across 7 disease domains.

**Integrity protocol:** Same freeze-before-data protocol. Family declarations and hypotheses committed before effect sizes are pulled.

**Commit SHA:** 5117419

---

## Relationship to prior amendments

This amendment adds two families to the exploratory extension declared in Amendment 1. These families expand the domain coverage (adding renal and hepatic) and were selected to include one expected discordance case (uric acid/CKD) and one expected concordance case (alcohol/liver disease). Both are well-characterized in the MR literature.

The exploratory status, scoring rules, and separation from the primary pre-registered accuracy carry forward from Amendment 1 without modification. The two new families are added to the exploratory denominator.

Additionally, Family R2 (IL4Ra-Asthma) is reclassified from "construct-limited" to "scoreable" based on identification of a published cis-pQTL MR study (Bretherick 2020, PMID 32628676). The soluble-vs-membrane receptor construct concern is retained as a pre-specified boundary condition.

---

## New families

### Family X1: Uric acid -> chronic kidney disease

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Serum uric acid levels -> CKD incidence/progression |
| **MR instrument** | Urate transporter variants (SLC2A9, ABCG2, SLC22A12) — same instruments as Family M3 (Urate-Gout) |
| **MR scale** | Per 1 mg/dL increase in serum urate |
| **Rescaling needed?** | No (same scale as OBS) |
| **Expected OBS source** | Meta-analysis of prospective cohort studies of serum urate and incident CKD |
| **Drug class** | Xanthine oxidase inhibitors (allopurinol, febuxostat) for CKD progression |
| **Drug outcome** | CKD-FIX trial (allopurinol, NEJM 2020): no benefit (P=0.85). FEATHER trial (febuxostat, AJKD 2018): failed primary endpoint (P=0.10). Coded as **Failed**. |
| **Rationale** | Tests the same instruments as M3 (Urate-Gout) against a different outcome. Gout is a direct consequence of urate crystallization; CKD is a systemic outcome with a less direct mechanistic link. If the rule correctly predicts gout (concordance/success) but also correctly predicts CKD (discordance/failure), it demonstrates outcome specificity within a shared exposure. |

### Family X2: Alcohol -> liver disease (cirrhosis)

| Field | Declaration |
|-------|-------------|
| **Exposure -> outcome** | Alcohol consumption -> liver cirrhosis |
| **MR instrument** | ALDH2 rs671 and ADH1B rs1229984 (alcohol metabolism variants) |
| **MR scale** | Per 280 g/week increase in genotype-predicted alcohol consumption |
| **Rescaling needed?** | No (both OBS and MR report per-unit alcohol consumption) |
| **Expected OBS source** | Prospective cohort study of alcohol consumption and liver cirrhosis incidence |
| **Drug class** | Naltrexone, acamprosate (FDA-approved for alcohol use disorder; reduce the causal exposure) |
| **Drug outcome** | Naltrexone FDA-approved 1994, acamprosate FDA-approved 2004. Meta-analyses confirm reduction in heavy drinking. Coded as **Approved**. |
| **Rationale** | Strong expected concordance case. Alcohol -> liver disease is among the best-established causal relationships in medicine. MR using East Asian alcohol metabolism variants provides strong instruments. This family serves as a second positive control (alongside M3 Urate-Gout) to verify the classification rule functions correctly on unambiguous causal pathways. |

**Exposure-reduction framing note:** Naltrexone and acamprosate treat alcohol use disorder (reducing consumption), not liver disease directly. The therapeutic mechanism is exposure reduction rather than pathway interruption. This is analogous to antihypertensives for stroke (reducing the causal exposure, blood pressure) rather than directly targeting cerebrovascular pathology. The framework scores the drug against the exposure-outcome pair, so exposure-reduction drugs are codeable as "Approved" when they are FDA-approved and have meta-analytic support for reducing the causal exposure.

---

## Updated R2 (IL4Ra-Asthma): reclassification from construct-limited to scoreable

A published cis-pQTL MR study was identified:

- **Bretherick et al. 2020** (PLOS Genetics, PMID 32628676): IL4R protein on asthma, OR ≈ 0.87 (0.82-0.93), P = 1.37E-05, FDR significant.
- Direction: higher soluble IL4R protein reduces asthma risk.

**Construct concern (retained):** The pQTL measures *soluble* IL4R (a decoy receptor that sequesters IL-4/IL-13 without signaling), not membrane-bound IL4R (the drug target for dupilumab). Higher soluble IL4R = less IL-4 signaling = less asthma, which is mechanistically consistent with dupilumab's action but instruments a different molecular entity than the drug modulates.

**Sensitivity instrument:** Nie et al. 2013 (PLOS ONE, PMID 23922637) meta-analysis of IL4RA coding variants: Q551R OR = 1.46 (1.22-1.75) for asthma. This instruments receptor function directly (gain-of-function = more asthma), but is a candidate gene meta-analysis rather than a formal MR study.

R2 is now scored with the Bretherick pQTL as the primary MR estimate and Nie coding variant as a sensitivity analysis. The soluble-vs-membrane construct issue is added to the boundary condition table.

---

## Updated boundary conditions

| Boundary type | Family | Mechanism |
|---------------|--------|-----------|
| Pharmacological amplification | O3 (Estrogen-BC) | Unchanged from Amendment 1 |
| Construct dilution | R1 (Eos-Asthma) | Unchanged from Amendment 1 |
| Instrument sensitivity | M1 (SGLT2-HF) | Unchanged from Amendment 1 |
| Multi-construct divergence | M2 (GLP1R) | Unchanged from Amendment 1 |
| Construct definition | R3 (TSLP-Asthma) | Unchanged from Amendment 1 |
| **Soluble-vs-membrane receptor** | **R2 (IL4Ra-Asthma)** | **NEW: pQTL instruments soluble decoy receptor, not the membrane-bound drug target** |

---

## Updated hypotheses

H_ext1 through H_ext4 from Amendment 1 are updated to reflect the expanded denominator (11 families, ~9 scoreable):

- **H_ext1**: ≥5/9 scored families correctly classified (56%). Unchanged threshold, larger denominator.
- **H_ext2**: ≥1 boundary condition observed. Unchanged.
- **H_ext3**: Positive controls (M3 Urate-Gout, R1 Eos-Asthma, **X2 Alcohol-Liver**) classify correctly. X2 added as third positive control.
- **H_ext4**: Combined six-domain accuracy exceeds chance (binomial p < 0.05). Now 7 domains.

---

## Updated power considerations

With 11 extension families and ~9 scoreable, the binomial test at α=0.05 against H0: accuracy=0.50 achieves significance at ≥7/9 (one-sided p=0.090, marginal) or ≥8/9 (p=0.020, significant). This is slightly more powered than the 6-scoreable denominator in Amendment 1.
