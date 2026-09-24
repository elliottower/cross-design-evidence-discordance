# IL6-MDD: source of the stored estimate, and the registration-consistent estimate

Executes items (3) and (4) of the disclosed deviation in
`PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md`
("Disclosed deviation: the IL6-MDD genetic instrument", frozen at commit fbc7d33).
All lookups used PubMed E-utilities and Europe PMC REST. No email address, API key or
`mailto` parameter was sent with any request; no browser was used; no publisher page was
fetched. Full text was read only where Europe PMC or PMC served it.

Run date: 2026-09-22 (timestamps below are UTC, recorded per query).

---

## Task 1: source of the estimate the frozen classifier holds

The classifier comment at `analysis/classifier/classify_families.py` (family B1, IL6-MDD) reads:

```
    # MR = genetically predicted CRP (>500 instruments) and depression
    #   (bidirectional MR, UK Biobank): OR 1.01 (0.99-1.04) per SD CRP — null
```

**The source is identified.**

**Galan D, Perry BI, Warrier V, Davidson CC, Stupart O, Easton D, Khandaker GM, Murray GK.
"Applying Mendelian randomization to appraise causality in relationships between smoking,
depression and inflammation." *Scientific Reports* 12 (2022).
PMID 36057695. PMC9440889. DOI 10.1038/s41598-022-19214-4.**

Abstract sentence (Europe PMC full text, `fullTextXML` for PMC9440889, fetched
2026-09-22T18:15:26Z):

> We did not find evidence for a reciprocal relationship between CRP levels (using > 500
> genetic instruments for CRP) and depression (OR CRP–Dep = 1.01, 95% CI 0.99–1.04;
> OR Dep–CRP = 1.03, 95% CI 0.99–1.07).

Table 3 of the same paper ("Inverse Variance Weighted Estimates for the univariable MR
analyses") gives the cell:

| Exposure | Outcome | SNPs | OR | Lower CI | Upper CI | StdErr | p-val |
|---|---|---|---|---|---|---|---|
| CRP | Depression | 512 | 1.01 | 0.99 | 1.04 | 0.01 | 0.225 |

Every element of the classifier's note matches: bidirectional (the reciprocal
depression → CRP estimate is reported alongside), >500 instruments (512 SNPs in the
CRP → depression direction; 521 in the CRP → smoking direction; the CRP GWAS carries 526
genome-wide significant SNPs), and UK Biobank (the CRP GWAS is Han et al., UK Biobank,
n = 418,642; the depression GWAS is Howard et al. / PGC, UK Biobank plus 33 cohorts,
170,756 cases and 329,443 controls, 23andMe excluded).

Two qualifications on the classifier's wording, stated because the row is being audited:

- The classifier records the estimate as "per SD CRP". Galan et al. report the exposure as
  CRP level on the Han et al. UK Biobank GWAS scale and do not label the contrast per SD in
  the table or the abstract sentence quoted above.
- The same table carries a cis-CRP row, `CRP (cis)* → Depression`, 1 SNP,
  OR 1.00 (0.92–1.09), p = 1.000, and an IL-6 activity row,
  `IL-6 Activity → Depression`, 7 SNPs, OR 0.93 (0.85–1.02), p = 0.127. Neither is the
  number the classifier holds; the classifier holds the 512-instrument polygenic CRP row,
  which is consistent with the amendment's description of it as a polygenic CRP estimate.

### Candidates examined for Task 1

Queries (PubMed E-utilities, `db=pubmed`, `retmode=xml`, `retmax=200`), all run
2026-09-22T18:14:47Z–18:14:48Z:

| label | query string | results |
|---|---|---|
| t1a | `C-reactive protein AND "mendelian randomization" AND (depression OR "depressive")` | 34 |
| t1b | `("C-reactive protein" OR CRP) AND bidirectional AND "mendelian randomi*" AND depression` | 10 |
| t1c | `CRP AND depression AND "UK Biobank" AND "mendelian randomi*"` | 13 |

Union: 42 distinct PMIDs (records fetched by `efetch` at 2026-09-22T18:14:58Z). Titles and
abstracts were read for all 42; every abstract was scanned for the literal strings `1.01`,
`0.99` and `1.04`. The CRP → depression (or inflammation → depression) estimate each
candidate reports, for the candidates that report one:

| PMID | First author, year, journal | CRP (or inflammatory exposure) → depression estimate | Match to 1.01 (0.99–1.04)? |
|---|---|---|---|
| 36057695 | Galan 2022, Sci Rep | OR 1.01 (0.99–1.04), 512 instruments, p = 0.225; cis-CRP 1.00 (0.92–1.09); IL-6 activity 0.93 (0.85–1.02) | **Yes — exact** |
| 42670184 | Luo 2026, Am J Epidemiol | OR 1.01 (0.92–1.10) for CRP on depression | No — same point, different interval |
| 24246360 | Wium-Andersen 2014, Biol Psychiatry | Causal OR 0.79 (0.51–1.22) per doubling of genetically elevated CRP | No |
| 30886334 | Khandaker 2020, Mol Psychiatry | Per-SD genetically predicted IL-6 OR 0.74 (0.62–0.89); triglycerides 1.18 (1.09–1.27) | No |
| 33079133 | Kappelmann 2021, JAMA Psychiatry | Genetic correlations 0.152–0.362 between CRP and depressive symptoms; symptom-specific MR, no 1.01 (0.99–1.04) | No |
| 34135474 | Milaneschi 2021, Mol Psychiatry | Symptom-level ORs (depressed mood 1.06 [1.05–1.08], appetite 1.25 [1.23–1.28], sleep 1.05 [1.04–1.06], fatigue 1.12) | No |
| 34280516 | Perry 2021, Brain Behav Immun | Bi-directional two-sample MR of immunological proteins with MDD; no CRP → depression 1.01 (0.99–1.04) | No |
| 34505025 | Ye 2021, EClinicalMedicine | Inflammation and depression/anxiety, specificity and linearity; no such cell in the abstract | No |
| 36712567 | Palmos 2023, Biol Psychiatry Glob Open Sci | 1.03 (1.00–1.05) and 1.02 (0.97–1.06) — already excluded in the amendment | No |
| 37710313 | Karageorgiou 2023, BMC Med | BMI and inflammation in depression / treatment-resistant depression | No |
| 39167384 | Zeng 2024, JAMA Psychiatry | Inflammatory biomarkers and psychiatric disorder risk | No |
| 39323965 | Mo 2024, Front Psychiatry | Blood biomarkers and major depression, East Asian ancestry | No |
| 41429762 | Dong 2025, Transl Psychiatry | Circulating inflammatory proteins and schizophrenia/bipolar/MDD | No |
| 42320223 | Rodríguez-Romero 2026, Eur Neuropsychopharmacol | Cross-trait genetic overlap of depression and CRP | No |
| 40768164 | Pistis 2025, JAMA Psychiatry | Energy homeostasis in depression | No |
| 40173244 | Jiang 2025, Sci Adv | Co-occurring pain conditions and depression | No |

The remaining 26 of the 42 are on other exposures or outcomes (smoking, education,
household income, erectile dysfunction, cortical structure, uric acid, allergy, immune
thrombocytopenia, PTSD, sex hormones, bibliometrics, and the IL6R-query records listed
under Task 2) and report no CRP → depression MR estimate.

---

## Task 2: the registration-consistent estimate

### Query, exactly as the amendment fixes it

```
IL6R AND "mendelian randomization" AND (depression OR "major depressive disorder")
```

Run against PubMed E-utilities `esearch.fcgi` (`db=pubmed`, `retmax=500`, `retmode=xml`) at
**2026-09-22T18:13:31Z**; records fetched with `efetch.fcgi` (`db=pubmed`, `retmode=xml`) at
**2026-09-22T18:13:41Z**.

`<Count>` = **8**. PubMed's query translation expanded `IL6R` to
`"il6r protein human"[Supplementary Concept] OR "il6r protein human"[All Fields] OR
"il6r"[All Fields]`, and `depression OR "major depressive disorder"` to the depression MeSH
tree plus text-word variants. All 8 PMIDs were screened on title and abstract, and full text
was read where available: PMC full text via Europe PMC `fullTextXML` (PMC12065825 at
2026-09-22T18:15:26Z; PMC12895973 and PMC8424591 at 2026-09-22T18:17:21Z) and via
E-utilities `efetch` `db=pmc` for the NIH author manuscript of Kelly et al.
(`id=11081733`, 2026-09-22T18:16:15Z), whose Europe PMC `fullTextXML` endpoint returns HTTP
500 because the record is not open access.

### Eligibility definition applied

Eligible = reports an instrumental-variable estimate of IL6R-region variation (cis
instruments only; soluble IL-6R, IL-6 or CRP as the exposure readout all count when the
instruments are IL6R-region) on depression, with a 95% confidence interval.

### All 8 results

| PMID | First author, year | Journal | Peer-reviewed / preprint | Exposure and instruments | IL6R-region cis? | Outcome definition | MDD cases | Primary estimate (95% CI), as the paper reports it | Direction convention | Eligible | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 41673668 | Zhang J, 2026 | Cardiovasc Diabetol | Peer-reviewed | Multivariate GWAS of 3 autoimmune and 4 cardiovascular diseases, with proteome-wide and drug-repurposing MR; IL6R prioritized as one of 15 therapeutic targets | Instruments are pQTL/eQTL for the autoimmune-CVD outcomes, not for depression | Autoimmune and cardiovascular diseases; "depressive episode" appears only in the phenome-wide scan of the AD-CVD polygenic risk score | n/a | PRS-phenotype association: depressive episode OR 1.11, P = 4.81 × 10⁻⁷⁹ | PRS-outcome association, higher PRS = higher risk | No | No instrumental-variable estimate of IL6R-region variation on depression; the only depression figure is a polygenic-risk-score phenome association |
| 40348744 | Mac Giollabhui N, 2025 | Transl Psychiatry | Peer-reviewed | GRSs for CRP, IL-6, IL-6R, sIL-6R and GlycA (association betas); the MR leg instruments CRP only | IL6R/sIL-6R enter only as genetic risk scores, not as IV instruments | MINI structured interview, DSM-IV MDD or dysthymia (Lifelines), plus affect and cognition scores | Not stated numerically; point prevalence ≈4% of ≈55,098 | GlycA GRS on MDD β = 0.001, p = 0.036; sIL-6R GRS on memory β = −0.009, p = 0.018; MR: CRP on anxiety β = 0.12, p = 0.054 | GRS-outcome regression betas on z-transformed scales | No | No IV estimate of IL6R-region variation on depression with a 95% CI; the IL6R/sIL-6R results are GRS-outcome associations and the MR exposure is CRP |
| 39149475 | Giollabhui NM, 2024 | Res Sq | Preprint | As PMID 40348744 | No | As PMID 40348744 | As above | As above | As above | No | Same ground as PMID 40348744 (no IL6R IV estimate); additionally a preprint of that article |
| 38699368 | Giollabhui NM, 2024 | medRxiv | Preprint | As PMID 40348744 | No | As PMID 40348744 | As above | As above | As above | No | Same ground as PMID 40348744; additionally a preprint of that article |
| 36729470 | Mourtzi N, 2023 | Age Ageing | Peer-reviewed | IL6R-locus variants associated with reduced CRP as proxies for IL-6 signaling downregulation; alternative instrument weighted on sIL-6R | Yes | Frailty Index (HELIAD, replicated in UK Biobank); depression- and cognition-related FI items excluded in sensitivity analyses | n/a | Frailty, categorical OR 0.15, continuous β = −0.09 (SE 0.003), p = 0.0009 | Downregulated IL-6 signaling = lower frailty risk | No | Outcome is frailty, not depression; the depression-related items are removed rather than analyzed as an outcome |
| 34522877 | Arleevskaya M, 2021 | J Transl Autoimmun | Peer-reviewed (narrative review) | None of its own; reviews MR findings on the IL-6/CRP/sIL-6R pathway in rheumatoid arthritis | n/a | Rheumatoid arthritis risk and protective factors | n/a | Reports sIL-6R-pathway ORs with CIs for coronary artery disease (1.02, 1.01–1.03), type 2 diabetes and chronic kidney disease; "depressive symptoms" is named with no estimate | n/a | No | A review that reports no instrumental-variable estimate of its own, and no estimate with a CI for depression |
| 33631287 | Kelly KM, 2021 | Brain Behav Immun | Peer-reviewed | sIL-6R (exposure coefficients from van Dongen 2014 and IMPROVE); rs2228145 as the single-SNP instrument, with rs4129267 and rs12126142 as r² > 0.99 proxies; all eligible sIL-6R SNPs on chromosome 1; PCA-IVW over 491 SNPs (4 PCs) | Yes | UK Biobank "recurrent depressive symptoms", defined from self-reported symptoms, n = 89,119; replication in PGC MDD 2018 (clinical MDD) | UK Biobank case count is in the supplemental note, not in the full text served; PGC MDD 2018 replication sample: 59,851 cases / 113,514 controls | PCA-IVW OR 1.023 (95% CI 1.006–1.039), p = 0.006 | Per 10⁻⁸ g/mL increase in sIL-6R; OR > 1 means higher sIL-6R raises the odds of depression. Higher sIL-6R is the rs2228145 minor-allele direction, which reduces IL-6 classical signaling, so OR > 1 is the direction indexing reduced classical IL6R signaling | **Yes** | — |
| 29197507 | Khandaker GM, 2018 | Brain Behav Immun | Peer-reviewed | IL6R Asp358Ala (rs2228145) genotype, ALSPAC birth cohort | Instrument is IL6R cis, but the reported quantity is a genotype-outcome association | Severe depressive episode (ICD-10) and/or psychotic disorder at age 18, as a combined outcome; total depression score analyzed separately | Small; the paper states the findings are "based on a small number of cases" | Adjusted OR 0.38 (95% CI 0.15–0.94) for CC versus AA genotype | Per-genotype contrast; CC (signaling-impairing) genotype = lower risk | No | The estimate is a variant-disease association, not an instrumental-variable estimate scaled by an exposure, and the outcome is a composite of severe depression and psychosis rather than depression |

### Which estimate the rule selects

Exactly one of the 8 results is eligible, so criteria (a)–(e) do not have to separate a field:
(a) peer-reviewed over preprint, (b) clinical MDD over symptom score, (c) largest number of
MDD cases, (d) most recent year and (e) lowest PMID all resolve trivially to the single
eligible paper.

**Selected: Kelly KM, Smith JA, Mezuk B. "Depression and interleukin-6 signaling: A
Mendelian Randomization study." *Brain, Behavior, and Immunity* 95 (2021) 106–114.
PMID 33631287. DOI 10.1016/j.bbi.2021.02.019.**

The estimate taken is the one the paper reports as primary — the PCA-IVW estimate with the
van Dongen exposure coefficients and the UK Biobank outcome sample, which is the estimate
carried in the abstract:

> Results are consistent with a causal effect of sIL-6R on depression (PCA-IVW Odds Ratio:
> 1.023 (95% Confidence Interval: 1.006-1.039), p = 0.006).

The results section states the same estimate with its scale:

> For example, using the PCA-IVW method with the van Dongen and UK Biobank samples, a 10⁻⁸
> g/mL increase in sIL-6R was associated with 1.023 times higher odds of depression (95%
> Confidence Interval: 1.006 – 1.039, p=0.006).

Table 2 of the paper gives the cell as `PCA-IVW  1.023 (1.006–1.039)  0.006  491 (4 PCs)`
in the UK Biobank column, beside `1.016 (1.003–1.029)  0.019  500 (4 PCs)` in the PGC MDD
2018 column.

Instrument note, against the Amendment 2 declaration: Amendment 2 declared rs2228145 and
rs4129267, and Kelly et al. use rs2228145 as the single-SNP instrument with rs4129267 as an
r² > 0.99 proxy where rs2228145 is unavailable, with the multi-SNP analyses drawn from the
same chromosome 1 region.

Direction note: the paper reports the effect per increase in sIL-6R, and an OR above 1 means
higher sIL-6R raises the odds of depression. Higher sIL-6R corresponds to the rs2228145
minor allele, which reduces IL-6 classical signaling, so the OR > 1 direction is the one
indexing reduced classical IL6R signaling. The registered rule is sign-blind, so direction
does not enter the classification.

### Chinn conversion

d = ln(OR) × √3 / π

| quantity | OR | d |
|---|---|---|
| point | 1.023 | 0.0125 |
| lower bound | 1.006 | 0.0033 |
| upper bound | 1.039 | 0.0211 |

The whole interval falls below the registered 0.10 floor, so the registration-consistent
estimate is null under the registered rule.

For comparison, the frozen classifier's stored estimate converts to d = 0.0055
(point, OR 1.01), with bounds d = −0.0055 (OR 0.99) and d = 0.0216 (OR 1.04).

---

## Record of every request

| # | Endpoint | Query or identifier | Run (UTC) |
|---|---|---|---|
| 1 | `esearch.fcgi` db=pubmed | `IL6R AND "mendelian randomization" AND (depression OR "major depressive disorder")` | 2026-09-22T18:13:31Z |
| 2 | `efetch.fcgi` db=pubmed | the 8 PMIDs from query 1 | 2026-09-22T18:13:41Z |
| 3 | `esearch.fcgi` db=pubmed | `C-reactive protein AND "mendelian randomization" AND (depression OR "depressive")` | 2026-09-22T18:14:47Z |
| 4 | `esearch.fcgi` db=pubmed | `("C-reactive protein" OR CRP) AND bidirectional AND "mendelian randomi*" AND depression` | 2026-09-22T18:14:48Z |
| 5 | `esearch.fcgi` db=pubmed | `CRP AND depression AND "UK Biobank" AND "mendelian randomi*"` | 2026-09-22T18:14:48Z |
| 6 | `efetch.fcgi` db=pubmed | the 42 PMIDs from queries 3–5 | 2026-09-22T18:14:58Z |
| 7 | Europe PMC `fullTextXML` | PMC9440889, PMC11081733 (HTTP 500, not open access), PMC12065825 | 2026-09-22T18:15:26Z |
| 8 | Europe PMC `search` | `EXT_ID:33631287 AND SRC:MED`, `EXT_ID:40348744 AND SRC:MED`, `EXT_ID:36057695 AND SRC:MED` (resultType=core) | 2026-09-22T18:15:46Z |
| 9 | Europe PMC `search` | `TITLE:"Depression and interleukin-6 signaling"` (checking for an open version; one record, not open access) | 2026-09-22T18:16:01Z |
| 10 | `efetch.fcgi` db=pmc | `id=11081733` (Kelly 2021 NIH author manuscript full text) | 2026-09-22T18:16:15Z |
| 11 | Europe PMC `fullTextXML` | PMC12895973, PMC8424591 | 2026-09-22T18:17:21Z |
