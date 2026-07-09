# Pre-Registration Amendment 2: Additional Extension Families

**Status:** FROZEN (pending commit SHA)
**Date:** 2026-07-09
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9)
**Scope:** Two additional mechanism families added to the exploratory extension, expanding from 9 to 11 families across 7 disease domains. Of these 11, 3 are construct-limited and 8 are scoreable.

**Integrity protocol:** Same freeze-before-data protocol. Family declarations and hypotheses committed before effect sizes are pulled.

**Commit SHA:** 5117419

---

## Relationship to prior amendments

This amendment adds two families to the exploratory extension declared in Amendment 1. These families expand the domain coverage (adding renal and hepatic) and were selected to include one expected discordance case (uric acid/CKD) and one expected concordance case (alcohol/liver disease). Both are well-characterized in the MR literature.

The two new families (X1 and X2) were selected after preliminary review of the literature and are reported as a clearly-labeled second exploratory batch. They are not blind additions.

The exploratory status, scoring rules, and separation from the primary pre-registered accuracy carry forward from Amendment 1 without modification. The two new families are added to the exploratory denominator.

Family R2 (IL4Ra-Asthma) remains construct-limited. Although a cis-pQTL MR study exists (Bretherick 2020, PMID 32628676, OR 0.87), the pQTL instruments soluble IL4R (a decoy receptor that sequesters IL-4), not the membrane-bound IL4R that dupilumab targets. Because the genetic instrument measures a different molecular entity than the drug modulates, R2 does not meet the construct-matching requirement for scoring.

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

## Transparency: families considered and excluded

Two additional families were considered during literature review and excluded before scoring:

1. **PCSK9 -> Type 2 diabetes.** PCSK9 inhibitors have a small diabetogenic signal in trials, but the framework predicts drug success or failure for treating a disease, and diabetes is a side effect of PCSK9 inhibitors, not the therapeutic indication (which is cardiovascular disease, already covered by Family LDL/PCSK9). The observational effect size was also trivial (d = 0.047), below any plausible threshold.

2. **IL-6 -> coronary heart disease.** An IL-6R family already exists in the pre-registered cardio families (IL-6R, cardio domain). Including a second IL-6 pathway family for the same cardiovascular outcome would double-count the same mechanism.

---

## Updated boundary conditions

| Boundary type | Family | Mechanism |
|---------------|--------|-----------|
| Pharmacological amplification | O3 (Estrogen-BC) | Unchanged from Amendment 1 |
| Construct dilution | R1 (Eos-Asthma) | Unchanged from Amendment 1 |
| Instrument sensitivity | M1 (SGLT2-HF) | Unchanged from Amendment 1 |
| Multi-construct divergence | M2 (GLP1R) | Unchanged from Amendment 1 |
| Construct definition | R3 (TSLP-Asthma) | Unchanged from Amendment 1 |

---

## Updated hypotheses

H_ext1 through H_ext4 from Amendment 1 are updated to reflect the expanded denominator (11 families total, 3 construct-limited, 8 scoreable):

- **H_ext1**: ≥5/8 scored families correctly classified (63%). Unchanged threshold, smaller denominator (R2 remains construct-limited).
- **H_ext2**: ≥1 boundary condition observed. Unchanged.
- **H_ext3**: Positive controls (M3 Urate-Gout, R1 Eos-Asthma, **X2 Alcohol-Liver**) classify correctly. X2 added as third positive control.
- **H_ext4**: Combined accuracy across all scored extension families exceeds chance (binomial p < 0.05). Now 7 domains.

---

## Updated power considerations

With 11 extension families and 8 scoreable (R2, R3, M2 remain construct-limited), the binomial test at alpha=0.05 against H0: accuracy=0.50 achieves significance at >=7/8 (one-sided p=0.035, significant) or 8/8 (p=0.004). This is comparable to Amendment 1's power with 6 scoreable families.
