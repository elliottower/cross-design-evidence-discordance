# Family provenance ledger

Built by `analysis/provenance/build_family_provenance.py` at commit `6f08481` (working tree has uncommitted changes). 10 committed classifier versions and 8 committed supplement versions read. Regenerate; do not edit.

## Flags

| family | status | correct | flags |
|---|---|---|---|
| Metabolic-AD | pre-registered | True | catalog row AD-020 carries a CI (0.96-1.06) that the classifier dropped |
| ModRisk-AD | pre-registered | True | scored outcome has no drug program in the record; registered MR OR 1.1 matches no genetic row in the evidence catalog (catalog has 0.89, 1.04) |
| Smoking-MS/AD | pre-registered | True | scored outcome has no drug program in the record; catalog row MS-021 carries a CI (0.89-1.19) that the classifier dropped |
| BMI-AD | pre-registered | True | scored outcome has no drug program in the record |
| EBV-MS | pre-registered | True | frozen supplement gives no GEN value (None); classifier holds gen_OR 5.0; genetic-leg estimate not traced to any source; scored outcome has no drug program in the record; registered MR OR 5.0 matches no genetic row in the evidence catalog (catalog has 32.4) |
| CRP | pre-registered | True | primary endpoint met but registered outcome is failure (regulatory reading) |
| IL-23-psoriasis | pre-registered | True | genetic leg is a variant-disease association, not MR |
| CTLA-4-RA | pre-registered | False | genetic leg is a variant-disease association, not MR |
| IL-17-psoriasis | pre-registered | False | gen_OR changed across committed classifier versions |
| JAK-STAT-RA | pre-registered | True | genetic leg is a variant-disease association, not MR |
| IL-1b-CVD | pre-registered | True | primary endpoint met but registered outcome is failure (regulatory reading) |
| IL4Ra-Asthma | construct-limited | — | gen_OR changed across committed classifier versions; drug_outcome changed across committed classifier versions |
| IL6-MDD | extension | True | scored on a Phase II readout |
| Complement-GA | extension | False | genetic leg is a variant-disease association, not MR |
| Serotonin-MDD | extension | False | genetic leg is a variant-disease association, not MR |

## Metabolic-AD

Domain neuro; status pre-registered; registered: OBS d 0.234, MR OR 1.01 (no CI), MR d 0.005 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** catalog row AD-020 carries a CI (0.96-1.06) that the classifier dropped

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.01 (no CI) | 1.53 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.01, cohen_d=0.006, drug_outcome=Failed, classification=Qual. disc., source=MR of T2D and AD; evidence_type=OBS, study_design=observational, effect_size_original=1.53, cohen_d=0.234, drug_outcome=Failed, classification=Qual. disc., source=Observational cohorts T2D-AD |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.234, mr_or_raw=1.01, mr_d=0.005, mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- AD-005b, T2D -> AD (updated cohort meta), Metabolic_AD, observational, risk ratio, 1.53, 1.42, 1.63, multi, 2017 updated meta, PMID:28088029 (VERIFIED), Mechanistically Supported
- AD-020, T2D liability -> AD (MR, IVW), Metabolic_AD, MR, odds ratio, 1.01, 0.96, 1.06, Danish 1M / IGAP, PMID:32330418 Thomsen/Nordestgaard 2020, Disconfirmed, Disconfirmed
- AD-023, GLP-1 semaglutide CDR-SB (EVOKE), Metabolic_AD, RCT, pct_slowing, 0.0, 3808.0, EVOKE/EVOKE+, catalog_ad web980/974, Disconfirmed
- AD-005l, Diabetes (midlife) -> dementia (Deng), Metabolic_AD, observational, risk ratio, 1.69, 1.38, 2.07, multi, Deng 2019 meta, PMID:31902364 (VERIFIED), Mechanistically Supported
- AD-034, Semaglutide -> cognitive decline (EVOKE/EVOKE+), Metabolic_AD, RCT, hazard ratio, 1.0, 0.88, 1.14, early AD, EVOKE 2025 Novo Nordisk topline, Disconfirmed

### Readings

- **Genetic leg:** MR-instrumented — PMID 32326995. we investigated the associations between type-2 diabetes and Alzheimer's disease, vascular dementia, unspecified dementia and all-cause dementia, and whether observational associations were of a causal nature by applying a two-sample Mendelian randomisation strategy Note: Thomassen 2020 Epidemiol Psychiatr Sci; MR estimate for AD 1.04 (0.98-1.10). Classifier holds OR 1.01 with no CI. The repo ledger (data/effect_sizes_v12.csv, AD-020) cites PMID 32330418, which resolves to an unrelated TET2 genome-sequencing paper; the author-year (Thomsen/Nordestgaard 2020) and the stated sample (Danish 1M / IGAP) match PMID 32326995. / Stored OR 1.01 is Walter 2016 (PMID 26650880): "OR for the T2D polygenic score=1.01; 95% CI 0.96, 1.06" (verified on PubMed). The catalog row AD-020 cites PMID 32330418, which is a different paper.
- **Outcome codebook:** program semaglutide, oral (evoke / evoke+); pioglitazone (TOMMORROW); phase III; engagement unclear; efficacy not met; safety acceptable; decision discontinued; regulatory not submitted n/a (no submission for AD); attribution target. Sources: PMID:41865758;DOI:10.1016/S0140-6736(26)00459-9;NCT:NCT04777396;NCT:NCT04777409;PMID:34146512;DOI:10.1016/S1474-4422(21)00043-0;NCT:NCT01931566. Notes: Manuscript names semaglutide (EVOKE/EVOKE+) and pioglitazone. Target engagement coded unclear: the evoke/evoke+ abstract reports no pharmacodynamic marker of GLP-1R agonism in AD, and the repository holdout note 'biomarker improvements' carries no source. Efficacy: CDR-SB difference -0.08 (95% CI -0.35 to 0.20, p=0.57) and 0.10 (-0.17 to 0.38, p=0.46); TOMMORROW HR 0.80 (99% CI 0.45-1.40, p=0.307), terminated for futility. Development: 'both trials have been discontinued due to negative clinical outcome'; TOMMORROW terminated for 'Lack of efficacy of the drug; no safety concern' (CT.gov). Attribution to target is a single-coder reading: two molecules with distinct mechanisms (GLP-1R agonism, PPAR-gamma agonism) were both null on the family's pathway.
- **MR state:** inconclusive (signed d  / 0.0055 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## ModRisk-AD

Domain neuro; status pre-registered; registered: OBS d 0.209, MR OR 1.1 (no CI), MR d 0.053 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** scored outcome has no drug program in the record; registered MR OR 1.1 matches no genetic row in the evidence catalog (catalog has 0.89, 1.04)

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.1 (no CI) | 1.46 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.10, cohen_d=0.053, drug_outcome=Failed, classification=Qual. disc., source=MR of modifiable risk factors; evidence_type=OBS, study_design=observational, effect_size_original=1.46, cohen_d=0.209, drug_outcome=Failed, classification=Qual. disc., source=Observational cohorts |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.209, mr_or_raw=1.1, mr_d=0.053, mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- AD-021, Educational attainment -> AD (MR, IVW), ModRisk_AD, MR, odds ratio, 0.89, 0.84, 0.93, 17008.0, 37154.0, IGAP, PMID:29212772 Larsson 2017 BMJ, Mechanistically Supported, Mechanistically Supported
- AD-022, Systolic BP (10mmHg) -> AD (MR, IVW), ModRisk_AD, MR, odds ratio, 1.04, 0.95, 1.13, UKB / IGAP, PMID:31358969 Ou/Larsson 2019, Disconfirmed, Disconfirmed
- AD-005j, Hypercholesterolemia -> dementia, ModRisk_AD, observational, risk ratio, 1.57, 1.19, 2.07, multi, Deng 2019 meta, PMID:31902364 (VERIFIED), Mechanistically Supported
- AD-005k, Midlife hypertension -> dementia, ModRisk_AD, observational, risk ratio, 1.72, 1.25, 2.37, multi, Deng 2019 meta, PMID:31902364 (VERIFIED), Mechanistically Supported
- AD-005m, TBI -> dementia, ModRisk_AD, observational, odds ratio, 1.81, 1.53, 2.14, multi, 2021 TBI meta 25 studies, PMID:34818648 (VERIFIED), Mechanistically Supported
- AD-005m2, Mild TBI -> dementia, ModRisk_AD, observational, odds ratio, 1.96, 1.7, 2.26, multi, mTBI meta, PMID:33044182 (VERIFIED), Mechanistically Supported
- AD-005a, Hearing loss -> dementia, ModRisk_AD, observational, hazard ratio, 1.59, 1.37, 1.86, multi, 2021 hearing meta PMC8295986, PMID:34255721 (VERIFIED), Mechanistically Supported
- AD-005p, Heavy alcohol -> AD, ModRisk_AD, observational, relative risk, 1.29, 1.21, 1.36, multi, 2026 alcohol meta, Mechanistically Supported

### Readings

- **Genetic leg:** MR-instrumented — PMID 29212772. Design: Mendelian randomisation study using genetic variants associated with the modifiable risk factors as instrumental variables Note: Larsson 2017 BMJ; 24 exposures, each reported as an OR with a 95% CI per genetically predicted increase. The classifier's OR 1.10 (no CI) does not correspond to any single estimate in the abstract (education 0.89 (0.84-0.93); smoking quantity 0.69 (0.49-0.99)), so the family's point estimate is not traceable to a specific row of the cited source.
- **Outcome codebook:** program not reported; phase not reported; engagement not reported; efficacy not reported; safety not reported; decision not reported; regulatory not reported not reported; attribution not reported. Sources: —. Notes: Registered drug_outcome = Failed, but neither the manuscript (Tables tab:drugs_stage1 and tab:stage2: no holdout drug maps to the family, RCT d '---') nor analysis/classifier/classify_families.py names a program. The family is a polygenic composite (hearing loss, midlife hypertension, TBI, education; data/effect_sizes_v12.csv). No trial or regulatory record can be coded without a named program. Listed under disagreements: the registered outcome has no identifiable program.
- **MR state:** inconclusive (signed d  / 0.0525 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Anti-CD20-MS

Domain neuro; status pre-registered; registered: OBS d 1.084, MR OR 0.83 (0.79-0.89), MR d 0.103 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.83 (0.79–0.89) | 2.23 | Approved | — |
| `ceee705` | 2026-07-06 | per_allele, sd_per_allele | 0.83 (0.79–0.89) | 2.23 | Approved | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.83, CI_lower=0.79, CI_upper=0.89, cohen_d=0.103, drug_outcome=Approved, classification=Concordant, source=Lin 2023 FCRL3-CD20; evidence_type=OBS, study_design=observational, cohen_d=Approved, drug_outcome=Concordant, classification=Hu 2019 B-cell depletion efficacy (d~0.80) |
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.83, CI_lower=0.79, CI_upper=0.89, cohen_d=0.103, drug_outcome=Approved, classification=Concordant, source=Lin 2023 per-SD circulating FCRL3 protein on MS risk (PMC10393411); evidence_type=OBS, study_design=observational, cohen_d=Approved, drug_outcome=Concordant, classification=Hu 2019 B-cell depletion efficacy (d~0.80) |
| `31f6b6e` | 2026-07-07 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.83, CI_lower=0.79, CI_upper=0.89, cohen_d=0.103, drug_outcome=Approved, classification=Concordant, source=Lin 2023 per-SD circulating FCRL3 protein on MS risk (PMC10393411); evidence_type=OBS, study_design=observational, effect_size_original=2.23, cohen_d=0.442, drug_outcome=Approved, classification=Concordant, source=Hu 2019 B-cell count OR for MS (classifier uses OR=2.23 d=0.44) |
| `5d12b37` | 2026-08-23 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.83, CI_lower=0.79, CI_upper=0.89, cohen_d=0.103, drug_outcome=Approved, classification=Concordant, source=Lin 2023 per-SD circulating FCRL3 protein on MS risk (PMC10393411); evidence_type=OBS, study_design=observational, effect_size_original=0.14, CI_lower=0.05, CI_upper=0.39, cohen_d=1.084, drug_outcome=Approved, classification=Concordant, source=Filippini 2021 Cochrane CD013874.pub2, pooled NRSIs: rituximab vs interferon beta/glatiramer acetate, relapse HR 0.14 (0.05-0.39), 335 participants, moderate certainty |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=1.084, mr_or_raw=0.83, mr_d=0.103, mr_ci=(0.79-0.89), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |
| `0d4f881` | 2026-07-09 | paper/submission/supplementary/cross_design_classification_all_41_families.csv | obs_d=0.442, mr_or_raw=0.83, mr_d=0.103, mr_ci=(0.79-0.89), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |
| `5d12b37` | 2026-08-23 | paper/submission/supplementary/cross_design_classification_all_41_families.csv | obs_d=1.084, mr_or_raw=0.83, mr_d=0.103, mr_ci=(0.79-0.89), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- MS-011, Ocrelizumab PPMS progression benefit, AntiCD20_MS, RCT, hazard ratio, 0.7, 0.57, 0.86, ORATORIO-class, PMID:42208561 ORATORIO-HAND Lancet 2026 (eutils+verified), Triangulated
- MS-031, Ocrelizumab -> 12wk CDP (OPERA, vs IFN), AntiCD20_MS, RCT, hazard ratio, 0.6, 0.45, 0.81, 827.0, 829.0, RRMS, Hauser 2017 NEJM OPERA, PMID:28002679 (VERIFIED), Mechanistically Supported
- MS-032b, Ocrelizumab -> 12wk CDP (ORATORIO, PPMS), AntiCD20_MS, RCT, hazard ratio, 0.76, 0.59, 0.98, 488.0, 244.0, PPMS, Montalban 2017 NEJM ORATORIO, PMID:26981933 (VERIFIED), Mechanistically Supported

### Readings

- **Genetic leg:** MR-instrumented — PMID 36864689. We performed Mendelian randomization to explore potential drug targets for multiple sclerosis using summary statistics from the International Multiple Sclerosis Genetics Consortium ... Genetic instruments for 734 plasma and 154 CSF proteins were obtained from recently published genome-wide association studies Note: Lin 2023 Brain. FCRL3 OR 0.83 (95% CI 0.79-0.89) per SD matches the classifier exactly.
- **Outcome codebook:** program ocrelizumab (OPERA I/II; ORATORIO); ofatumumab (ASCLEPIOS I/II); ublituximab (ULTIMATE I/II); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2017 (ocrelizumab, relapsing and primary progressive MS); FDA 2020 (ofatumumab, relapsing MS); FDA 2022 (ublituximab, relapsing MS); attribution target. Sources: PMID:28002679;DOI:10.1056/NEJMoa1601277;NCT:NCT01247324;NCT:NCT01412333;PMID:28002688;DOI:10.1056/NEJMoa1606468;NCT:NCT01194570;PMID:32757523;DOI:10.1056/NEJMoa1917246;NCT:NCT02792218;NCT:NCT02792231;PMID:36001711;DOI:10.1056/NEJMoa2201904;NCT:NCT03277261;NCT:NCT03277248;PMID:28523586;PMID:37556938;PMID:36920653. Notes: Target engagement: CD20+ B-cell depletion is the stated mechanism in every pivotal report ('selectively depletes CD20+ B cells'; 'produces B-cell depletion'); B-cell counts are in the full reports, not the abstracts. Efficacy: ARR 46-47% lower vs interferon (OPERA), 12-week CDP HR 0.76 (ORATORIO), ARR 0.11 vs 0.22 and 0.10 vs 0.25 (ASCLEPIOS), rate ratios 0.41 and 0.51 (ULTIMATE). Approval dates: March 2017 (PMID 28523586), August 2020 (PMID 37556938: prescriptions 'between August 2020 and May 2021' post-approval), December 2022 (PMID 36920653). EMA approvals not sourced here. Rituximab, the source of the family's observational estimate, holds no MS indication (manuscript).
- **MR state:** supportive (signed d -0.13 / -0.1027 / -0.0642; scale-unresolved False; alignment instrument-target mismatch)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Smoking-MS/AD

Domain neuro; status pre-registered; registered: OBS d 0.209, MR OR 1.03 (no CI), MR d 0.016 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** scored outcome has no drug program in the record; catalog row MS-021 carries a CI (0.89-1.19) that the classifier dropped

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.03 (no CI) | 1.46 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.03, cohen_d=0.016, drug_outcome=Failed, classification=Qual. disc., source=MR of smoking and MS/AD; evidence_type=OBS, study_design=observational, effect_size_original=1.46, CI_lower=1.33, CI_upper=1.59, cohen_d=0.209, drug_outcome=Failed, classification=Qual. disc., source=Poorolajal 2017 meta-analysis ever vs never smoking and MS (PMID 27160862) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.209, mr_or_raw=1.03, mr_d=0.016, mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- MS-021, Smoking -> MS (MR negative control), Smoking_MSAD, MR, odds ratio, 1.03, 0.89, 1.19, IMSGC smoking MR, Perplexity sweep11 (VERIFIED), Disconfirmed
- AD-005i, Current smoking -> dementia, Smoking_MSAD, observational, risk ratio, 1.61, 1.32, 1.95, multi, Deng 2019 meta, PMID:31902364 (VERIFIED), Mechanistically Supported

### Readings

- **Genetic leg:** MR-instrumented — PMID 33253141. We used two-sample Mendelian randomization (MR) to examine whether this association is causal using genetic variants identified in genome-wide association studies (GWASs) as associated with smoking Note: Mitchell 2020 PLoS Biol; smoking initiation OR 1.03 (95% CI 0.92-1.61) on IMSGC MS, matching the classifier's 1.03 (classifier carries no CI). Vandebergh 2020 (PMID 32529581) is a second null smoking-MS MR; either is an IV design.
- **Outcome codebook:** program not reported; phase not reported; engagement not reported; efficacy not reported; safety not reported; decision not reported; regulatory not reported not reported; attribution not reported. Sources: —. Notes: Registered drug_outcome = Failed with no named program in the manuscript or classifier (no holdout drug maps to the family; RCT d '---' in tab:stage2). Smoking is a behavioral exposure; no drug program, trial, or regulatory record is identified for the family's indication. Listed under disagreements: the registered outcome has no identifiable program.
- **MR state:** inconclusive (signed d  / 0.0163 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## HRT-AD

Domain neuro; status pre-registered; registered: OBS d 0.221, MR OR 1.0 (0.85-1.18), MR d 0.0 (null); qualitative discordance → failure; outcome Failed; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (0.85–1.18) | 0.67 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.00, CI_lower=0.85, CI_upper=1.18, cohen_d=0.000, drug_outcome=Failed, classification=Qual. disc., source=Barth 2025 estradiol MR; evidence_type=OBS, study_design=observational, effect_size_original=0.67, CI_lower=0.58, CI_upper=0.78, cohen_d=0.220, drug_outcome=Failed, classification=Qual. disc., source=Song 2020 meta-analysis |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.221, mr_or_raw=1.0, mr_d=0.0, mr_ci=(0.85-1.18), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- AD-031, CEE+MPA (HRT) -> incident dementia (WHIMS), HRT_AD, RCT, hazard ratio, 2.05, 1.21, 3.48, 2229.0, 2303.0, women 65+, Shumaker 2003 WHIMS JAMA, PMID:12771112 (VERIFIED), Mechanistically Supported
- AD-031b, Pooled HRT -> probable dementia (WHIMS), HRT_AD, RCT, hazard ratio, 1.76, 1.19, 2.6, women 65+, WHIMS pooled 2004, PMID:15213206 (VERIFIED), Mechanistically Supported

### Readings

- **Genetic leg:** MR-instrumented — PMID 41350255. we perform two-sample Mendelian randomization ... We test for causal links between genetically-predicted factors related to estradiol exposure (estradiol levels in pre- and postmenopausal samples, reproductive span, age at menarche, age at menopause, number of childbirths) and brain age gap, Alzheimer's disease and depression as outcomes Note: Oppenheimer/Barth 2025 Nat Commun, cited as 'Barth 2025 estradiol MR' in paper/supplementary_data.csv. The specific OR 1.00 (0.85-1.18) is not in the abstract and was not verified against the full text. The classification table codes gene_target ESR1 / biomarker_gwas, but the cited estimate instruments estradiol exposure, not an ESR1 variant-disease OR.
- **Outcome codebook:** program conjugated equine estrogen 0.625 mg + medroxyprogesterone acetate 2.5 mg (WHIMS, ancillary to the WHI estrogen-plus-progestin trial); phase III; engagement unclear; efficacy not met; safety limiting; decision discontinued; regulatory not submitted n/a (no submission for dementia prevention); attribution target. Sources: PMID:12771112;DOI:10.1001/jama.289.20.2651;NCT:NCT00000611. Notes: Primary endpoint moved in the harmful direction: HR 2.05 (95% CI 1.21-3.48) for probable dementia. Target engagement unclear: WHIMS reports no pharmacodynamic marker of estrogen action; engagement is presumed from the intervention. Safety coded limiting because the parent WHI estrogen-plus-progestin trial drugs were discontinued on 8 July 2002 'because of certain increased health risks', which ended the program independently of the dementia readout. NCT00000611 is the WHI parent registration (CT.gov phase 3). Attribution to target is a single-coder reading; the alternative reading (late initiation, the 'timing hypothesis') would code design.
- **MR state:** negligible_range (signed d -0.0896 / 0.0 / 0.0913; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## BMI-MS

Domain neuro; status pending; registered: OBS d 0.36, MR OR 1.41 (1.2-1.66), MR d 0.189 (causal); concordance → success; outcome Pending; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.41 (1.2–1.66) | 1.92 | Pending | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.41, CI_lower=1.20, CI_upper=1.66, cohen_d=0.189, drug_outcome=Pending, classification=Prediction pending, source=Mokry 2016 IVW per 1 SD BMI; evidence_type=OBS, study_design=observational, effect_size_original=1.92, cohen_d=0.361, drug_outcome=Pending, classification=Prediction pending, source=Observational cohorts obesity-MS |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.36, mr_or_raw=1.41, mr_d=0.189, mr_ci=(1.2-1.66), mr_class=causal, classification=concordance, drug_outcome=Pending, status=pending |

### Readings

- **Outcome codebook:** program behavioral weight loss (MoDEMS); intermittent calorie restriction (Ghezzi 2025 iCR trial); phase not reported; engagement yes; efficacy not tested; safety acceptable; decision not reported; regulatory not submitted n/a; attribution not reported. Sources: PMID:38018409;DOI:10.1177/13524585231213241;PMID:39137977;DOI:10.1136/jnnp-2024-333465;NCT:NCT03539094. Notes: Pending family; the manuscript names MoDEMS and the iCR trial as the interventional literature. Neither is a drug program or a phase-labelled trial: MoDEMS (n=71) is behavioral with weight, mobility and quality-of-life outcomes; iCR (n=42) has serum leptin as primary. Target engagement yes: 'Mean percent weight loss in the treatment group was 8.6% compared to 0.7% in the TAU group' (PMID 38018409); leptin lowered (PMID 39137977). Efficacy not tested on any MS clinical endpoint (relapse, disability, incidence). Safety: 'no serious AEs were reported' (iCR). No sponsor development decision exists and there is no outcome to attribute.
- **MR state:** supportive (signed d 0.1005 / 0.1894 / 0.2794; scale-unresolved False; alignment aligned)

## BMI-AD

Domain neuro; status pre-registered; registered: OBS d 0.393, MR OR 1.03 (1.01-1.05), MR d 0.016 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** scored outcome has no drug program in the record

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.03 (1.01–1.05) | 2.04 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.03, CI_lower=1.01, CI_upper=1.05, cohen_d=0.016, drug_outcome=Failed, classification=Qual. disc., source=Life-course MR BMI-AD (near null); evidence_type=OBS, study_design=observational, effect_size_original=2.04, CI_lower=1.59, CI_upper=2.62, cohen_d=0.393, drug_outcome=Failed, classification=Qual. disc., source=Anstey 2011 midlife obese vs normal BMI meta-analysis (PMID 21348917) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.393, mr_or_raw=1.03, mr_d=0.016, mr_ci=(1.01-1.05), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID:34057091 (Li 2021, J Alzheimers Dis). "Genetically predicted 1-SD increase in adult BMI was significantly associated with higher risk of AD (IVW: OR = 1.03, 95% confidence interval [CI] = 1.01-1.05, p = 2.7x10-3)" (two-sample MR) Note: paper/supplementary_data.csv names the genetic leg only as 'Life-course MR BMI-AD (near null)'; no PMID or DOI appears anywhere in the repository for OR 1.03 (1.01-1.05). The closest published BMI-AD MR, Nordestgaard 2017 (PMID 28609829), reports 0.98 (0.77-1.23) per 1 kg/m2 and 1.02 (0.86-1.22) per SD, neither of which matches. PubMed and Europe PMC searches on BMI/adiposity x Alzheimer x Mendelian randomization returned no source reporting 1.03 (1.01-1.05). / Source located after the audit (literature search, abstract verified on PubMed 2026-09-22).
- **Outcome codebook:** program not reported; phase not reported; engagement not reported; efficacy not reported; safety not reported; decision not reported; regulatory not reported not reported; attribution not reported. Sources: —. Notes: Registered drug_outcome = Failed with no named program: the manuscript states that weight-loss interventions 'would not prevent AD' but cites no trial, and no holdout drug maps to the family (RCT d '---' in tab:stage2). Listed under disagreements: the registered outcome has no identifiable program.
- **MR state:** negligible_range (signed d 0.0055 / 0.0163 / 0.0269; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## VitaminD-MS

Domain neuro; status pre-registered; registered: OBS d 0.186, MR OR 2.0 (1.7-2.5), MR d 0.382 (causal); concordance → success; outcome Failed; correct False.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 2.0 (1.7–2.5) | 1.4 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=2.00, cohen_d=0.382, drug_outcome=Failed, classification=Concordant, source=MR of vitamin D and MS; evidence_type=OBS, study_design=observational, effect_size_original=1.40, CI_lower=1.19, CI_upper=1.64, cohen_d=0.186, drug_outcome=Failed, classification=Concordant, source=Munger 2006 |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.186, mr_or_raw=2.0, mr_d=0.382, mr_ci=(1.7-2.5), mr_class=causal, classification=concordance, drug_outcome=Failed, correct=False, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 26305103. We undertook a Mendelian randomization (MR) study to evaluate whether genetically lowered vitamin D level influences the risk of MS ... Alleles were weighted by their relative effect on 25OHD level, and sensitivity analyses were performed to test MR assumptions Note: Mokry 2015 PLoS Med; each genetically determined 1-SD decrease in log 25OHD confers OR 2.0 (95% CI 1.7-2.5) for MS, matching the classifier exactly.
- **Outcome codebook:** program vitamin D3 (cholecalciferol) supplementation: VIDAMS; D-Lay MS; SOLAR; CHOLINE; PrevANZ; phase III; engagement not reported; efficacy mixed; safety acceptable; decision not reported; regulatory not submitted n/a (supplement; no submission); attribution design. Sources: PMID:37125397;DOI:10.1016/j.eclinm.2023.101957;NCT:NCT01490502;PMID:40063041;DOI:10.1001/jama.2025.1604;NCT:NCT01817166;PMID:31594857;DOI:10.1212/WNL.0000000000008445;NCT:NCT01285401;PMID:31454777;DOI:10.1212/NXI.0000000000000597;NCT:NCT01198132;PMID:38085047;DOI:10.1093/brain/awad409. Notes: The manuscript names 'vitamin D supplementation' without a trial; the repository holdout row cites NCT01440062, which CT.gov identifies as EVIDIMS (Charite, phase 2, n=55, terminated), not VIDAMS (NCT01490502). Phase III readouts disagree: VIDAMS not met (relapse HR 1.17, 0.67-2.05) and D-Lay MS met (disease activity HR 0.66, 0.50-0.87; relapse alone HR 0.69, 0.42-1.16, not significant); the phase 2 add-on trials SOLAR and CHOLINE and the PrevANZ CIS trial did not meet their primary endpoints. Target engagement not reported: none of the abstracts consulted reports attained 25(OH)D; full texts not consulted. No sponsor program (academic trials; Merck KGaA ran SOLAR and CHOLINE as phase 2 add-on studies), so development decision not reported. Attribution 'design' is a single-coder reading: the positive trial is untreated early CIS on high-dose monotherapy, the null trials are add-on therapy in established RRMS. Listed under disagreements: registered Failed vs mixed efficacy.
- **MR state:** supportive (signed d 0.2926 / 0.3822 / 0.5052; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## EBV-MS

Domain neuro; status pre-registered; registered: OBS d 0.293, MR OR 5.0 (2.0-20.0), MR d 0.887 (causal); concordance → success; outcome Approved; correct True.

**Flags:** frozen supplement gives no GEN value (None); classifier holds gen_OR 5.0; genetic-leg estimate not traced to any source; scored outcome has no drug program in the record; registered MR OR 5.0 matches no genetic row in the evidence catalog (catalog has 32.4)

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 5.0 (2.0–20.0) | 1.7 | Approved | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, cohen_d=Approved, drug_outcome=Concordant, classification=MR of EBV and MS (d~1.92); evidence_type=OBS, study_design=observational, cohen_d=Approved, drug_outcome=Concordant, classification=Observational EBV-MS (d~0.53) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.293, mr_or_raw=5.0, mr_d=0.887, mr_ci=(2.0-20.0), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Evidence catalog rows (data/effect_sizes_v12.csv)

- MS-001, EBV seroconversion -> MS risk, EBV_MS, genetic/cohort, hazard/rate ratio, 32.4, 4.3, 245.0, 955.0, ~10M US military, White-majority, Bjornevik 2022 Science, PMID:35025605 Bjornevik 2022 Science (VERIFIED primary), Mechanistically Supported
- MS-018a, HLA-DRB1*15:01 x EBV additive interaction, EBV_MS, observational, synergy index, 1.43, 1.05, 1.95, multi, Xiao 2015 SciRep, PMID:26656273 (VERIFIED), Mechanistically Supported
- MS-018b, EBV seropositivity alone -> MS, EBV_MS, observational, odds ratio, 2.6, 1.48, 4.59, multi, Xiao 2015 SciRep, PMID:26656273 (VERIFIED), Mechanistically Supported

### Readings

- **Genetic leg:** unresolved — UNRESOLVED. (no source identifier in the repository) Note: No source in the repository reports OR 5.0 (95% CI 2.0-20.0). data/cross_design_classification_all_41_families_v3.csv codes the genetic leg instrument_type=coding_variant, gene_target=HLA, mr_contrast=per_allele, which describes a variant-disease association rather than an IV estimate; paper/supplementary_data.csv says 'MR of EBV and MS (d~1.92)' with every numeric field blank. The repository's own HLA-DRB1*15:01 meta-OR is 3.06 (2.30-4.08) (PMID 26656273) and its EBV cohort estimate is HR 32.4 (4.3-245) (PMID 35025605); neither matches. If the leg is the HLA-DRB1*15:01 association, the family fails the MR-instrumented rule. / Still unresolved after a second search: no paper reports 5.0 (2.0-20.0). Closest matches are observational (Marrie 2000 prior infectious mononucleosis OR 5.5, 1.5-19.7; an HLA-stratified IM meta-analysis 5.11, 2.00-13.03).
- **Outcome codebook:** program not reported; phase not reported; engagement not reported; efficacy not reported; safety not reported; decision not reported; regulatory not reported not reported; attribution not reported. Sources: NCT:NCT03283826;PMID:38104476;DOI:10.1016/j.msard.2023.105364. Notes: Registered drug_outcome = Approved, but the manuscript names no program for the family and no EBV-directed therapy holds an MS approval in the sources consulted. The only EBV-directed program with a controlled readout is ATA188 (EMBOLD, NCT03283826, phase 1/2, Atara), which CT.gov records as 'terminated as primary endpoint was not achieved' (see PMID 38104476, 'a failed anti-EBV trial in multiple sclerosis'). If the registered Approved was coded on anti-CD20 agents (B cells as the EBV reservoir), the manuscript does not say so and that would be a pathway-level substitution. Listed under disagreements.
- **MR state:** supportive (signed d 0.3822 / 0.8873 / 1.6516; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## HDL/CETP

Domain cardio; status pre-registered; registered: OBS d 0.264, MR OR 0.93 (0.68-1.26), MR d 0.04 (null); qualitative discordance → failure; outcome Failed; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.93 (0.68–1.26) | 0.62 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.93, CI_lower=0.68, CI_upper=1.26, cohen_d=0.040, drug_outcome=Failed, classification=Qual. disc., source=Voight 2012 14-SNP score per 1 SD HDL-C; evidence_type=OBS, study_design=observational, effect_size_original=0.62, cohen_d=0.264, drug_outcome=Failed, classification=Qual. disc., source=Voight 2012 observational per 1 SD HDL-C |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.264, mr_or_raw=0.93, mr_d=0.04, mr_ci=(0.68-1.26), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 22607825. Exploiting the fact that genotypes are randomly assigned at meiosis ... mendelian randomisation can be used to test the hypothesis that the association of a plasma biomarker with disease is causal ... we used as an instrument a genetic score consisting of 14 common SNPs that exclusively associate with HDL cholesterol Note: Voight 2012 Lancet; the 14-SNP HDL-C score MR. Classifier OR 0.93 (0.68-1.26).
- **Outcome codebook:** program torcetrapib (ILLUMINATE); dalcetrapib (dal-OUTCOMES); evacetrapib (ACCELERATE); class also includes anacetrapib (REVEAL), not named in the manuscript; phase III; engagement yes; efficacy mixed; safety acceptable; decision discontinued; regulatory not submitted n/a; for anacetrapib 'regulatory approval is not being sought' (PMID 30704580, 2019); attribution target. Sources: PMID:17984165;DOI:10.1056/NEJMoa0706628;NCT:NCT00134264;PMID:23126252;DOI:10.1056/NEJMoa1206797;NCT:NCT00658515;PMID:28514624;DOI:10.1056/NEJMoa1609581;NCT:NCT01687998;PMID:28847206;DOI:10.1056/NEJMoa1706444;NCT:NCT01252953;PMID:30704580;DOI:10.1016/j.jacc.2018.10.072;PMID:29018035;NCT:NCT05202509. Notes: The three manuscript-named programs all failed: ILLUMINATE terminated for excess CV events (HR 1.25) and death (HR 1.58); dal-OUTCOMES HR 1.04 (0.93-1.16), terminated for futility; ACCELERATE HR 1.01 (0.91-1.11), terminated for lack of efficacy. Anacetrapib (REVEAL) met its primary endpoint (rate ratio 0.91, 0.85-0.97), so efficacy is coded mixed at the class level; PMID 29018035 attributes that benefit to non-HDL-C lowering 'rather than increases in HDL-C'. Target engagement yes: HDL-C +72.1% (torcetrapib), +31-40% (dalcetrapib), +133.2% (evacetrapib), +104% (anacetrapib). Safety coded acceptable for the class because dalcetrapib and evacetrapib stopped for futility without a safety signal; torcetrapib alone was safety-limited by an off-target effect. Obicetrapib (PREVAIL, NCT05202509) is ongoing (primary completion 2026-11). Listed under disagreements (partial: REVEAL).
- **MR state:** inconclusive (signed d -0.2126 / -0.04 / 0.1274; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Niacin/HDL

Domain cardio; status pre-registered; registered: OBS d 0.264, MR OR 0.93 (0.68-1.26), MR d 0.04 (null); qualitative discordance → failure; outcome Failed; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.93 (0.68–1.26) | 0.62 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.93, CI_lower=0.68, CI_upper=1.26, cohen_d=0.040, drug_outcome=Failed, classification=Qual. disc., source=Voight 2012 (shared with HDL/CETP); evidence_type=OBS, study_design=observational, effect_size_original=0.62, cohen_d=0.264, drug_outcome=Failed, classification=Qual. disc., source=Voight 2012 observational per 1 SD HDL-C |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.264, mr_or_raw=0.93, mr_d=0.04, mr_ci=(0.68-1.26), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 22607825. Exploiting the fact that genotypes are randomly assigned at meiosis ... mendelian randomisation can be used to test the hypothesis that the association of a plasma biomarker with disease is causal ... we used as an instrument a genetic score consisting of 14 common SNPs that exclusively associate with HDL cholesterol Note: Same estimate as HDL/CETP; the two families are identical on every evidence column, as Amendment 5's foreknowledge section records.
- **Outcome codebook:** program extended-release niacin (AIM-HIGH); extended-release niacin/laropiprant (HPS2-THRIVE); phase III; engagement yes; efficacy not met; safety limiting; decision discontinued; regulatory not approved EMA 2013 (nicotinic acid/laropiprant suspended, PMID 24622598); FDA: no cardiovascular-event indication; the 2016 withdrawal of niacin/statin combination approvals was not retrievable via the APIs used; attribution target. Sources: PMID:22085343;DOI:10.1056/NEJMoa1107579;NCT:NCT00120289;PMID:25014686;DOI:10.1056/NEJMoa1300955;NCT:NCT00461630;PMID:24622598;DOI:10.1016/S2213-8587(13)70129-3;PMID:25178730. Notes: AIM-HIGH stopped 'owing to a lack of efficacy' (HR 1.02, 0.87-1.21; CT.gov: DSMB recommendation); HPS2-THRIVE rate ratio 0.96 (0.90-1.03) and the drug 'did increase the risk of serious adverse events', so safety is coded limiting alongside the efficacy failure. Target engagement: HDL-C raised in both (median 35 to 42 mg/dL; +6 mg/dL vs placebo). Development discontinued is supported by the EMA suspension of the laropiprant combination (PMID 24622598) and the post-HPS2-THRIVE recommendation against niacin for HDL raising (PMID 25178730). The MR leg is shared with HDL/CETP (Voight 2012).
- **MR state:** inconclusive (signed d -0.2126 / -0.04 / 0.1274; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Homocysteine

Domain cardio; status pre-registered; registered: OBS d 0.153, MR OR 1.02 (0.98-1.07), MR d 0.011 (null); qualitative discordance → failure; outcome Failed; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.02 (0.98–1.07) | 1.32 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.02, CI_lower=0.98, CI_upper=1.07, cohen_d=0.011, drug_outcome=Failed, classification=Qual. disc., source=Clarke 2012 MTHFR TT vs CC unpublished; evidence_type=OBS, study_design=observational, effect_size_original=1.32, cohen_d=0.153, drug_outcome=Failed, classification=Qual. disc., source=Homocysteine Studies Collaboration 2002 per 5 umol/L |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.153, mr_or_raw=1.02, mr_d=0.011, mr_ci=(0.98-1.07), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 22363213. When folate levels are low, the TT genotype of the common C677T polymorphism (rs1801133) of the methylene tetrahydrofolate reductase gene (MTHFR) appreciably increases homocysteine levels, so "Mendelian randomization" studies using this variant as an instrumental variable could help test causality Note: Clarke 2012 PLoS Med; OR 1.02 (0.98-1.07) TT vs CC matches the classifier exactly. The source frames and computes the design as MR with MTHFR C677T as the instrument for homocysteine (stating the expected ~20% higher homocysteine in TT), so it is not a bare genotype-disease association; the reported figure is nonetheless the unscaled TT-vs-CC genotype contrast, not an effect per unit homocysteine.
- **Outcome codebook:** program folic acid / vitamin B6 / vitamin B12 supplementation (HOPE-2; NORVIT; 8-trial meta-analysis of the B-Vitamin Treatment Trialists' Collaboration); phase III; engagement yes; efficacy not met; safety acceptable; decision not reported; regulatory not submitted n/a (vitamins; no submission); attribution target. Sources: PMID:20937919;DOI:10.1001/archinternmed.2010.348;PMID:16531613;DOI:10.1056/NEJMoa060900;NCT:NCT00106886;PMID:16531614;DOI:10.1056/NEJMoa055227;NCT:NCT00266487. Notes: The manuscript names 'B-vitamin supplementation trials' without a single program; coded on the pooled 8-trial meta-analysis (37,485 individuals) with HOPE-2 and NORVIT as exemplars. Target engagement yes: 'Folic acid allocation yielded an average 25% reduction in homocysteine levels'. Efficacy not met: rate ratio 1.01 (0.97-1.05) for major vascular events; HOPE-2 RR 0.95 (0.84-1.07); NORVIT RR 1.08 (0.93-1.25). Safety acceptable: no significant effect on cancer or all-cause mortality in the meta-analysis; NORVIT reported a trend to harm with combined B vitamins. Academic prevention trials with no sponsor development decision, so not reported. HOPE-2 is registered as phase 4 on CT.gov.
- **MR state:** negligible_range (signed d -0.0111 / 0.0109 / 0.0373; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## CRP

Domain cardio; status pre-registered; registered: OBS d 0.174, MR OR 1.0 (0.97-1.02), MR d 0.0 (null); qualitative discordance → failure; outcome No benefit; correct True.

**Flags:** primary endpoint met but registered outcome is failure (regulatory reading)

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (0.97–1.02) | 1.37 | No benefit | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.00, CI_lower=0.97, CI_upper=1.02, cohen_d=0.000, drug_outcome=No benefit, classification=Qual. disc., source=Elliott 2009 per 20% lower CRP; evidence_type=OBS, study_design=observational, effect_size_original=1.37, cohen_d=0.173, drug_outcome=No benefit, classification=Qual. disc., source=ERFC 2010 per 1 SD log CRP |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.174, mr_or_raw=1.0, mr_d=0.0, mr_ci=(0.97-1.02), mr_class=null, classification=qualitative discordance, drug_outcome=No benefit, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 19567438. We carried out a mendelian randomization study of the most closely associated single-nucleotide polymorphism (SNP) in the CRP locus and published data on other CRP variants involving a total of 28,112 cases and 100,823 controls, to investigate the association of CRP variants with coronary heart disease. We compared our finding with that predicted from meta-analysis of observational studies of CRP levels and risk of coronary heart disease Note: Elliott 2009 JAMA; classifier holds OR 1.00 (0.97-1.02) per 20% lower CRP.
- **Outcome codebook:** program canakinumab (CANTOS); phase III; engagement yes; efficacy met; safety unclear; decision not reported; regulatory not approved FDA (cardiovascular risk reduction; PMID 31882264); decision year not carried by the source consulted; attribution uncertain. Sources: PMID:28845751;DOI:10.1056/NEJMoa1707914;NCT:NCT01327846;PMID:31882264;DOI:10.1016/j.tcm.2019.11.013;PMID:29265905. Notes: The manuscript describes CANTOS as a 'null primary endpoint'; the trial report states that the 150 mg dose 'met the prespecified multiplicity-adjusted threshold for statistical significance for the primary end point' (HR 0.85, 0.74-0.98, p=0.021), so efficacy is coded met and the family is listed under disagreements with the registered 'No benefit'. Target engagement is coded yes for CRP (hsCRP reduced by 26-41 percentage points vs placebo), with the caveat that canakinumab binds IL-1beta and CRP is a downstream marker: the family's MR instrument (CRP) and the drug act at different nodes. Safety unclear: 'higher incidence of fatal infection than was placebo' with no difference in all-cause mortality; whether this determined the regulatory outcome is not stated in the sources consulted. Regulatory: 'the therapy was not approved by the Food and Drug Administration (FDA) for cardiovascular risk reduction' (PMID 31882264). The sponsor's development decision after the FDA action is not documented in the consulted record. Attribution uncertain: endpoint met at one dose with a modest effect and a safety signal, and the regulatory reasoning is not public in the consulted record.
- **MR state:** negligible_range (signed d -0.0168 / 0.0 / 0.0109; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Uric acid

Domain cardio; status ambiguous; registered: OBS d 0.037, MR OR 1.05 (0.92-1.2), MR d 0.027 (null); null concordance → ambiguous; outcome Failed; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.05 (0.92–1.2) | 1.07 | Failed | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.05, CI_lower=0.92, CI_upper=1.20, cohen_d=0.027, drug_outcome=Failed, classification=Ambiguous, source=White 2016 Egger MR per 1 SD urate; evidence_type=OBS, study_design=observational, effect_size_original=1.07, cohen_d=0.037, drug_outcome=Failed, classification=Ambiguous, source=White 2016 observational per 1 SD urate |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.037, mr_or_raw=1.05, mr_d=0.027, mr_ci=(0.92-1.2), mr_class=null, classification=null concordance, drug_outcome=Failed, status=ambiguous |
| `0d4f881` | 2026-07-09 | paper/submission/supplementary/cross_design_classification_all_41_families.csv | obs_d=0.037, mr_or_raw=1.05, mr_d=0.027, mr_ci=(0.92-1.2), mr_class=null, classification=null concordance, drug_outcome=Failed, correct=False, status=pre-registered |

### Readings

- **Outcome codebook:** program allopurinol (ALL-HEART); phase post-marketing; engagement not reported; efficacy not met; safety acceptable; decision not reported; regulatory not submitted n/a; attribution target. Sources: PMID:36216006;DOI:10.1016/S0140-6736(22)01657-9;PMID:38551218;DOI:10.3310/ATTM4092. Notes: ALL-HEART is a pragmatic, open-label, blinded-endpoint RCT of a marketed drug in a new indication (ISRCTN32017426; EudraCT 2013-003559-39; no NCT); no phase label is given, coded post-marketing. Efficacy not met: HR 1.04 (0.89-1.21), p=0.65. Target engagement not reported: the abstracts consulted do not report serum urate attainment; full text not consulted. Safety acceptable: no safety signal reported; 57.4% withdrew from randomised treatment (HTA report). NIHR-funded academic trial with no sponsor development decision. Registered as ambiguous (null concordance); the trial outcome is consistent with the registered Failed.
- **MR state:** inconclusive (signed d -0.046 / 0.0269 / 0.1005; scale-unresolved False; alignment aligned)

## LDL/PCSK9

Domain cardio; status pre-registered; registered: OBS d 0.231, MR OR 1.78 (1.58-2.01), MR d 0.318 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.78 (1.58–2.01) | 1.52 | Approved | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.78, CI_lower=1.58, CI_upper=2.01, cohen_d=0.318, drug_outcome=Approved, classification=Concordant, source=Holmes 2015 unrestricted MR per 1 mmol/L LDL; evidence_type=OBS, study_design=observational, effect_size_original=1.52, cohen_d=0.231, drug_outcome=Approved, classification=Concordant, source=Lewington 2007 PSC / Ference 2017 per 1 mmol/L LDL |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.231, mr_or_raw=1.78, mr_d=0.318, mr_ci=(1.58-2.01), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 24474739. To investigate the causal role of high-density lipoprotein cholesterol (HDL-C) and triglycerides in coronary heart disease (CHD) using multiple instrumental variables for Mendelian randomization Note: Holmes 2015 Eur Heart J; weighted allele scores as instruments. The abstract states that both the unrestricted and restricted LDL-C scores (42 and 19 SNPs) associated with CHD but does not print the classifier's 1.78 (1.58-2.01) per 1 mmol/L, which was not verified against the full text.
- **Outcome codebook:** program evolocumab (FOURIER); alirocumab (ODYSSEY OUTCOMES); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved EU 2015 and FDA 2015 for hypercholesterolaemia (PMID 26323342, PMID 26370210); FDA cardiovascular-event indications after FOURIER and ODYSSEY OUTCOMES (PMID 31882264); label-extension years not carried by the sources consulted; attribution target. Sources: PMID:28304224;DOI:10.1056/NEJMoa1615664;NCT:NCT01764633;PMID:30403574;DOI:10.1056/NEJMoa1801174;NCT:NCT01663402;PMID:26323342;PMID:26370210;PMID:31882264. Notes: Target engagement yes: LDL-C reduced 59% (FOURIER); alirocumab titrated to LDL-C 25-50 mg/dL. Efficacy met: HR 0.85 (0.79-0.92) FOURIER; HR 0.85 (0.78-0.93) ODYSSEY OUTCOMES. Safety acceptable: adverse events did not differ except injection-site reactions. The MR leg is LDL-C (Holmes 2015) and the drug class is PCSK9 inhibition. FDA/EMA document identifiers for the cardiovascular-risk-reduction label extensions were not retrieved via the APIs used.
- **MR state:** supportive (signed d 0.2522 / 0.3179 / 0.3849; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Blood pressure

Domain cardio; status pre-registered; registered: OBS d 0.189, MR OR 1.44 (1.35-1.55), MR d 0.201 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.44 (1.35–1.55) | 1.41 | Approved | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.44, CI_lower=1.35, CI_upper=1.55, cohen_d=0.201, drug_outcome=Approved, classification=Concordant, source=Georgakis 2020 per 10 mmHg SBP any stroke; evidence_type=OBS, study_design=observational, effect_size_original=1.41, cohen_d=0.189, drug_outcome=Approved, classification=Concordant, source=Lewington 2002 PSC per 10 mmHg SBP stroke mortality |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.189, mr_or_raw=1.44, mr_d=0.201, mr_ci=(1.35-1.55), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 32611631. We employed Mendelian randomization to explore whether the effects of blood pressure (BP) and BP-lowering through different antihypertensive drug classes on stroke risk vary by stroke etiology ... Applying 2-sample Mendelian randomization, we examined associations with any stroke (67,162 cases; 454,450 controls) Note: Georgakis 2020 Neurology; classifier holds OR 1.44 (1.35-1.55) per 10 mmHg SBP for any stroke, a figure not printed in the abstract.
- **Outcome codebook:** program antihypertensive drug classes (mixed class); PROGRESS (perindopril with or without indapamide) as the stroke-specific exemplar; BPLTTC individual-participant meta-analysis of 48 trials; phase mixed class; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA and EMA; hypertension indication held by every major class; no single approval year (class-level); attribution target. Sources: PMID:33933205;DOI:10.1016/S0140-6736(21)00590-0;PMID:11589932;DOI:10.1016/S0140-6736(01)06178-5. Notes: The manuscript names no program ('approved drug classes'); coded at class level and said so. Target engagement yes: PROGRESS 'active treatment reduced blood pressure by 9/4 mm Hg'; BPLTTC effects 'proportional to the intensity of systolic blood pressure reduction'. Efficacy met: PROGRESS stroke relative risk reduction 28% (17-38); BPLTTC HR 0.91 (0.89-0.94) per 5 mm Hg for major CV events. Safety acceptable at class level (no safety stop in the pooled trials is reported in the source). Regulatory approved rests on every drug in the 48 pooled trials being a marketed antihypertensive; no FDA/EMA document identifier is attached because there is no single event to cite.
- **MR state:** supportive (signed d 0.1655 / 0.201 / 0.2416; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Triglycerides

Domain cardio; status pre-registered; registered: OBS d 0.299, MR OR 1.62 (1.24-2.11), MR d 0.266 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.62 (1.24–2.11) | 1.72 | Approved | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.62, CI_lower=1.24, CI_upper=2.11, cohen_d=0.266, drug_outcome=Approved, classification=Concordant, source=Holmes 2015 unrestricted MR per 1 log-unit TG; evidence_type=OBS, study_design=observational, effect_size_original=1.72, CI_lower=1.56, CI_upper=1.90, cohen_d=0.299, drug_outcome=Approved, classification=Concordant, source=Sarwar 2007 top vs bottom tertile TG |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.299, mr_or_raw=1.62, mr_d=0.266, mr_ci=(1.24-2.11), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 24474739. To investigate the causal role of high-density lipoprotein cholesterol (HDL-C) and triglycerides in coronary heart disease (CHD) using multiple instrumental variables for Mendelian randomization Note: Holmes 2015 Eur Heart J; the unrestricted triglyceride allele score (67 SNPs) gives OR 1.62 (95% CI 1.24-2.11) per 1-log unit, matching the classifier exactly.
- **Outcome codebook:** program triglyceride-lowering classes (mixed class): icosapent ethyl (REDUCE-IT); pemafibrate (PROMINENT); omega-3 carboxylic acids (STRENGTH); fenofibrate (ACCORD-Lipid); phase mixed class; engagement yes; efficacy mixed; safety acceptable; decision not reported; regulatory approved FDA, icosapent ethyl label extension for cardiovascular risk reduction after REDUCE-IT (PMID 32959713, PMID 33888593; exact date not carried by the sources); fibrates and omega-3 products hold hypertriglyceridaemia indications only; attribution uncertain. Sources: PMID:30415628;DOI:10.1056/NEJMoa1812792;NCT:NCT01492361;PMID:36342113;DOI:10.1056/NEJMoa2210645;NCT:NCT03071692;PMID:33190147;DOI:10.1001/jama.2020.22258;NCT:NCT02104817;PMID:20228404;DOI:10.1056/NEJMoa1001282;NCT:NCT00000620;PMID:32959713;PMID:33888593. Notes: The manuscript names no program ('approved drug classes'); coded at class level and said so. Efficacy mixed: REDUCE-IT met (HR 0.75, 0.68-0.83); PROMINENT not met (HR 1.03, 0.91-1.15) despite triglycerides -26.2%; STRENGTH not met (HR 0.99, 0.90-1.09); ACCORD-Lipid not met (HR 0.92, 0.79-1.08). Target engagement yes: triglycerides lowered in every program. Safety acceptable: icosapent ethyl raised atrial fibrillation hospitalisation (3.1% vs 2.1%); pemafibrate raised renal events and venous thromboembolism; neither determined the outcome. Development decision differs by program (advanced for icosapent ethyl; PROMINENT and STRENGTH stopped for futility), so not reported as a single value. PMID 33888593 records that STRENGTH 'directly contradicts REDUCE-IT'. Attribution uncertain: the one positive program's benefit is not proportional to triglyceride lowering and the pure triglyceride-lowering programs failed, so the registered Approved may not index the instrumented exposure (triglycerides per Holmes 2015). Listed under disagreements.
- **MR state:** supportive (signed d 0.1186 / 0.266 / 0.4117; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Lp(a)

Domain cardio; status pending; registered: OBS d 0.067, MR OR 0.94 (0.93-0.95), MR d 0.034 (null); null concordance → ambiguous; outcome Pending; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.94 (0.93–0.95) | 1.13 | Pending | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.94, CI_lower=0.93, CI_upper=0.95, cohen_d=0.034, drug_outcome=Pending, classification=Concordant, source=Burgess 2018 per 10 mg/dL lower Lp(a); evidence_type=OBS, study_design=observational, effect_size_original=1.13, CI_lower=1.09, CI_upper=1.18, cohen_d=0.067, drug_outcome=Pending, classification=Concordant, source=Erqou/ERFC 2009 per 1 SD Lp(a) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.067, mr_or_raw=0.94, mr_d=0.034, mr_ci=(0.93-0.95), mr_class=null, classification=null concordance, drug_outcome=Pending, status=pending |

### Readings

- **Outcome codebook:** program pelacarsen (Lp(a)HORIZON); phase III; engagement yes; efficacy not reported; safety acceptable; decision ongoing; regulatory not submitted n/a (pending); attribution not reported. Sources: NCT:NCT04023552;PMID:31893580;DOI:10.1056/NEJMoa1905239;NCT:NCT03070782;PMID:42593611;DOI:10.1007/s11883-026-01453-9;PMID:42760802;DOI:10.1177/10742484261492865. Notes: CT.gov lists Lp(a)HORIZON as COMPLETED (primary completion 2026-07-16) with no results posted; no primary publication is indexed in PubMed as of 2026-09-22, and reviews dated August-September 2026 describe the results as 'due in late 2026' (PMID 42593611) or awaited (PMID 42675370). One 2026 commentary is titled 'Lipoprotein(a) After HORIZON: Causal Culprit, Risk Marker, or Unfulfilled Therapeutic Promise?' (PMID 42760802) with no abstract available; recorded as a lead, not a result. Efficacy therefore not reported. Target engagement yes from the phase 2 dose-ranging trial: Lp(a) reduced by up to 80% (PMID 31893580); safety acceptable on the same source (injection-site reactions only). Consistent with the registered Pending.
- **MR state:** negligible_range (signed d -0.04 / -0.0341 / -0.0283; scale-unresolved False; alignment aligned)

## IL-6R

Domain cardio; status pending; registered: OBS d 0.123, MR OR 0.95 (0.93-0.97), MR d 0.083 (null); qualitative discordance → failure; outcome Pending; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `b96d10a` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.95 (0.93–0.97) | 1.25 | Pending | — |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `b96d10a` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.95, CI_lower=0.93, CI_upper=0.97, cohen_d=0.028, drug_outcome=Pending, classification=Concordant, source=IL6R MR Consortium 2012 per allele; evidence_type=OBS, study_design=observational, effect_size_original=1.25, cohen_d=0.123, drug_outcome=Pending, classification=Concordant, source=Danesh 2008/ERFC per 1 SD log IL-6 |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.123, mr_or_raw=0.95, mr_d=0.083, mr_ci=(0.93-0.97), mr_class=null, classification=qualitative discordance, drug_outcome=Pending, status=pending |

### Readings

- **Outcome codebook:** program ziltivekimab (ZEUS); phase III; engagement yes; efficacy not met; safety unclear; decision not reported; regulatory not submitted n/a; attribution target. Sources: NCT:NCT05021835;PMID:41369941;DOI:10.1001/jamacardio.2025.4491;PMID:34015342;DOI:10.1016/S0140-6736(21)00520-1;NCT:NCT03926117;NCT:NCT05636176. Notes: Efficacy not met per the manuscript's cited sponsor announcement of 31 July 2026 (Novo Nordisk Form 6-K, SEC accession 0001171843-26-005109: HR 0.99, 95% CI 0.88-1.11; free IL-6 and hsCRP reduced). The announcement was not retrievable via the APIs used, so the values are taken from the manuscript's citation; no peer-reviewed primary report is indexed as of 2026-09-22 (CT.gov: COMPLETED, primary completion 2026-06-09, no results posted). Target engagement yes: phase 2 RESCUE reduced hsCRP by 77-92% (PMID 34015342) and the announcement reports the expected IL-6/hsCRP reductions. Safety unclear (not stated in the consulted record). Development decision not reported for the ASCVD program; the companion heart-failure outcomes trial HERMES (NCT05636176) is recorded as TERMINATED on CT.gov ('No longer looking for participants'). Instrument-target mismatch: the MR instrument is IL6R (receptor), the drug binds the IL-6 ligand. Registered drug_outcome = Pending; the fields read as a failure (efficacy not met); listed under disagreements. Amendment 5 already states the family remains unscored.
- **MR state:** inconclusive (signed d -0.1177 / -0.0832 / -0.0494; scale-unresolved False; alignment instrument-target mismatch)

## IL-23-psoriasis

Domain autoimmune; status pre-registered; registered: OBS d 0.66, MR OR 0.616 (0.563-0.674), MR d 0.267 (causal); concordance → success; outcome Approved; correct True.

**Flags:** genetic leg is a variant-disease association, not MR

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `55bac04` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.616 (0.563–0.674) | 3.0 | Approved | — |
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing | 0.616 (0.563–0.674) | d 0.66 | Approved | IL-23: serum SMD=0.66 (Dowlatshahi 2013, CI -0.25 to 1.58, NON-SIGNIFICANT); but tissue p19 22x elevated (Lee 2004 PMID 14707118). NOTE: OBS rests on tissue expression, not serum. Serum-vs-tissue switch must be stated explicitly in the paper. |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.616, CI_lower=0.563, CI_upper=0.674, cohen_d=0.267, drug_outcome=Approved, classification=Concordant, source=Zhu 2012 IL23R R381Q meta-analysis (PMID 22706445); evidence_type=OBS, study_design=tissue_expression, cohen_d=0.660, drug_outcome=Approved, classification=Concordant, source=Serum meta-analysis SMD=0.66 (Dowlatshahi 2013); tissue p19 22x (Lee 2004 PMID 14707118) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.66, mr_or_raw=0.616, mr_d=0.267, mr_ci=(0.563-0.674), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** association — PMID 22706445. We conducted a meta-analysis to examine the association between the IL23R rs11209026 (Q381R), rs7530511 (L310P), and rs2201841 polymorphisms and psoriasis/PsA Note: Zhu 2012 Inflamm Res. The value used, OR 0.616 (0.563-0.674), is the minor-allele OR of rs11209026 for psoriasis, quoted verbatim from the meta-analysis. No exposure is instrumented and no IV estimate is computed; the paper's conclusion is 'a significant association between IL23R gene polymorphisms and psoriasis/PsA'.
- **Outcome codebook:** program guselkumab (Tremfya; anti-IL-23 p19), first-approved selective IL-23 inhibitor for the indication; ustekinumab (Stelara; anti-IL-12/23 p40) is the earlier p40 agent; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2017 (BLA761061 ORIG-1 approved 2017-07-13); ustekinumab FDA 2009 (BLA125261 ORIG-1 approved 2009-09-25); attribution target. Sources: PMID:28057360;PMID:28057361;NCT:NCT02207231;NCT:NCT02207244;PMID:24679469;PMID:39114670;FDA:BLA761061;FDA:BLA125261;PMID:18486739;PMID:18486740;NCT:NCT00267969;NCT:NCT00307437. Notes: Manuscript names no drug for this family; coded guselkumab because the family's genetic leg is IL23R and guselkumab is the first-approved p19-selective agent (VOYAGE 1/2, Phase III, coprimary IGA 0/1 and PASI 90 at week 16 met, P<.001). Ustekinumab (PHOENIX 1/2, PASI 75 at week 12 met, p<0.0001; FDA 2009) gives the same values on every field. Target engagement: serum IL-17A reduction in the Phase I study (PMID 24679469) and serum IL-17A/IL-17F/IL-22 reductions in the VOYAGE 1 pharmacodynamic substudy (PMID 39114670). Safety: adverse event rates comparable to adalimumab and placebo.
- **MR state:** supportive (signed d -0.3167 / -0.2671 / -0.2175; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## CTLA-4-RA

Domain autoimmune; status pre-registered; registered: OBS d 0.5, MR OR 0.86 (0.78-0.95), MR d 0.083 (null); qualitative discordance → failure; outcome Approved; correct False.

**Flags:** genetic leg is a variant-disease association, not MR

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `55bac04` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.86 (0.78–0.95) | 1.5 | Approved | — |
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing | 0.86 (0.78–0.95) | d 0.5 | Approved | CTLA-4: sCTLA-4 elevated in RA p=0.005 (Liu 2012 PMID 22917707) 6.8 ng/mL vs controls; exact SMD not reported |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.86, CI_lower=0.78, CI_upper=0.95, cohen_d=0.083, drug_outcome=Approved, classification=Qual. disc., source=Barton 2009 CT60 (PMID 19404967); evidence_type=OBS, study_design=case_control_SMD, cohen_d=0.500, drug_outcome=Approved, classification=Qual. disc., source=sCTLA-4 elevated p=0.005 (Liu 2012 PMID 22917707); author-estimated SMD |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=0.86, mr_d=0.083, mr_ci=(0.78-0.95), mr_class=null, classification=qualitative discordance, drug_outcome=Approved, correct=False, status=pre-registered |

### Readings

- **Genetic leg:** association — PMID 19404967. The aim of the present study was to independently replicate 3 recently described RA susceptibility loci, STAT4, IL2/IL21, and CTLA4, in a large Dutch case-control cohort, and to perform a meta-analysis of all published studies to date Note: Daha 2009 Arthritis Rheum. A case-control replication plus allele-level meta-analysis of CTLA4 rs3087243; the abstract reports OR 0.87 (Dutch) and 0.91 (meta-analysis), against the classifier's 0.86 (0.78-0.95), which is not printed in the abstract. No exposure, no instrument, no IV estimate.
- **Outcome codebook:** program abatacept (Orencia; CTLA-4-Ig costimulation modulator), first-in-class; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2005 (BLA125118 ORIG-1 approved 2005-12-23); attribution target. Sources: PMID:16785475;PMID:16162882;NCT:NCT00048568;NCT:NCT00048581;PMID:17014006;FDA:BLA125118;PMID:17565924. Notes: Manuscript names no drug; abatacept is the only approved CTLA-4-pathway agent in RA. Pivotal Phase III: AIM (ACR20 at 6 months 67.9% vs 39.7%) and ATTAIN (ACR20 50.4% vs 19.5%, P<0.001). Target engagement is coded from the Phase II biomarker analysis (PMID 17014006: serum IL-6, soluble IL-2 receptor and CRP lower on abatacept 10 mg/kg vs placebo); the Phase III abstracts report no pharmacodynamic readout, and the evidence is downstream inflammatory markers rather than CD80/CD86 occupancy. Safety: similar overall adverse-event incidence, higher serious infections (2.5% vs 0.9%) and infusion reactions in AIM; approval followed. Registered classification predicted failure; fields agree with the registered Approved outcome.
- **MR state:** inconclusive (signed d -0.137 / -0.0832 / -0.0283; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, registration-consistent instrument, unique-evidence, Amendment 4

## TNF-a-RA

Domain autoimmune; status pre-registered; registered: OBS d 1.93, MR OR 1.0 (no CI), MR d 0.0 (null); qualitative discordance → failure; outcome Approved; correct False.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `55bac04` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (no CI) | 2.0 | Approved | — |
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing | 1.0 (no CI) | d 1.93 | Approved | TNF-a: meta-analysis of 14 studies, SMD=1.93 (CI 1.23-2.64) Wang 2015 PMC4694713; 890 RA vs 441 controls |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.00, cohen_d=0.000, drug_outcome=Approved, classification=Qual. disc., source=Li 2025 druggable-genome MR null (PMID 40618325); evidence_type=OBS, study_design=case_control_SMD, cohen_d=1.930, drug_outcome=Approved, classification=Qual. disc., source=Serum TNF-a meta-analysis 14 studies SMD=1.93 CI 1.23-2.64 (Wang 2015 PMC4694713) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=1.93, mr_or_raw=1.0, mr_d=0.0, mr_class=null, classification=qualitative discordance, drug_outcome=Approved, correct=False, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 40618325. A Mendelian randomization (MR) analysis was conducted to investigate the causal effects of druggable expression quantitative trait loci (eQTLs) in the blood on RA Note: Li/Liu 2025 Postgrad Med J; a druggable-genome MR. The classifier records OR 1.00 with no CI, i.e. a null read-off rather than a quoted interval: TNF is not among the five genes (CCR6, CTLA4, EDN3, FCRL3, STAT4) the paper reports as causally related to RA, and no TNF estimate with a CI is quoted in the classifier or the supplementary table.
- **Outcome codebook:** program anti-TNF class in RA: etanercept (Enbrel; TNFR2:Fc), first approved for RA; infliximab (Remicade; anti-TNF mAb) RA supplement one year later; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 1998 (etanercept BLA103795 ORIG-1 approved 1998-11-02); infliximab RA FDA 1999 (BLA103772 SUPPL-1004 approved 1999-11-10); attribution target. Sources: PMID:10075615;PMID:9219699;PMID:10622295;PMID:10415055;FDA:BLA103795;FDA:BLA103772;PMID:10375846. Notes: Manuscript names no drug; coded the class with etanercept as first-approved agent for RA and infliximab (ATTRACT, explicitly 'randomised phase III trial') as the second. Etanercept pivotal trial (PMID 10075615): ACR20 at 6 months 59% vs 11%, P<0.001; the abstract does not state a phase, ATTRACT does. Target engagement: infliximab program (PMID 10415055) shows rapid down-regulation of IL-6 and acute-phase proteins after anti-TNF; the etanercept pivotal abstracts report no pharmacodynamic marker. Safety: 'no dose-limiting toxic effects' (etanercept); 'well-tolerated' (infliximab). Registered classification predicted failure; fields agree with the registered Approved outcome.
- **MR state:** inconclusive (signed d  / 0.0 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## IL-17-psoriasis

Domain autoimmune; status pre-registered; registered: OBS d 0.47, MR OR 0.998 (no CI), MR d 0.001 (null); qualitative discordance → failure; outcome Approved; correct False.

**Flags:** gen_OR changed across committed classifier versions

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `55bac04` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (no CI) | 2.0 | Approved | — |
| `ceee705` | 2026-07-06 | gen_OR | 0.998 (no CI) | 2.0 | Approved | — |
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing | 0.998 (no CI) | d 0.47 | Approved | IL-17: meta-analysis of 8 studies, SMD=0.47 (CI 0.07-0.86) Zhou 2017 PMID 27925680 |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=0.998, cohen_d=0.001, drug_outcome=Approved, classification=Qual. disc., source=Wu 2021 IL-17 protective (PMID 33188428); evidence_type=OBS, study_design=case_control_SMD, cohen_d=0.470, drug_outcome=Approved, classification=Qual. disc., source=Serum IL-17 meta-analysis 8 studies SMD=0.47 CI 0.07-0.86 (Zhou 2017 PMID 27925680) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.47, mr_or_raw=0.998, mr_d=0.001, mr_class=null, classification=qualitative discordance, drug_outcome=Approved, correct=False, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 33188428. A two-sample Mendelian randomization (MR) analysis was performed using the inverse-variance weighted (IVW), weighted median and MR-Egger regression methods ... Single-nucleotide polymorphisms (SNPs) at genome-wide significance from GWASs on TNF-alpha, IL-12p70 and IL-17 were identified as the instrumental variables Note: Wu 2021 Rheumatology. The design is an IV analysis, but the source reports betas with standard errors (IVW beta = -0.00186 per allele, s.e. 0.00043), not an OR with a confidence interval, and the outcome is psoriatic arthritis rather than psoriasis. The classifier's 0.998 carries no CI, so the family fails the 'with a confidence interval' half of the Procedure 4 rule.
- **Outcome codebook:** program secukinumab (Cosentyx; anti-IL-17A), first-approved IL-17A antagonist; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2015 (BLA125504 ORIG-1 approved 2015-01-21); attribution target. Sources: PMID:25007392;NCT:NCT01365455;NCT:NCT01358578;PMID:31129129;PMID:20926833;FDA:BLA125504. Notes: Manuscript names no drug; secukinumab is the first-approved IL-17A antagonist for psoriasis. ERASURE and FIXTURE (Phase III): coprimary PASI 75 and modified IGA 0/1 at week 12 met, P<0.001 vs placebo and etanercept. Target engagement: mechanistic study at the approved dose (PMID 31129129, NCT01537432) shows reduction of 'the drug target IL-17A' and downstream beta-defensin 2 from week 1; not from the pivotal trials themselves. Safety: infection rates higher than placebo, similar to etanercept. The pivotal paper's own conclusion reads 'validating interleukin-17A as a therapeutic target'. Registered classification predicted failure; fields agree with the registered Approved outcome.
- **MR state:** inconclusive (signed d  / -0.0011 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## JAK-STAT-RA

Domain autoimmune; status pre-registered; registered: OBS d 0.5, MR OR 1.27 (1.2-1.34), MR d 0.132 (causal); concordance → success; outcome Approved; correct True.

**Flags:** genetic leg is a variant-disease association, not MR

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `ceee705` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.27 (1.2–1.34) | 2.0 | Approved | — |
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing | 1.27 (1.2–1.34) | d 0.5 | Approved | STAT4/JAK: serum STAT4 elevated in RA p=0.01 (Osman 2025 PMC12520596); STAT1/STAT4/Jak3 elevated in synovium (Walker 2006) |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.27, CI_lower=1.20, CI_upper=1.34, cohen_d=0.132, drug_outcome=Approved, classification=Concordant, source=STAT4 rs7574865 meta-analysis (PMID 19479340); evidence_type=OBS, study_design=case_control_SMD, cohen_d=0.500, drug_outcome=Approved, classification=Concordant, source=Serum STAT4 elevated p=0.01 (Osman 2025 PMC12520596); author-estimated SMD |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=1.27, mr_d=0.132, mr_ci=(1.2-1.34), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** association — PMID 19479340. we conducted a meta-analysis of all relevant reports published before September 2008. Studies on STAT4 rs7574865 single nucleotide polymorphism (SNP) of RA and SLE were identified using PubMed ... The overall ORs for the minor T allele of STAT4 rs7574865 SNP were 1.27 (95% CI 1.20-1.34) in RA Note: Lee 2010 Mol Biol Rep. The value used, OR 1.27 (1.20-1.34), is the minor-allele variant-disease OR, matching the classifier exactly. No exposure is instrumented.
- **Outcome codebook:** program tofacitinib (Xeljanz; JAK1/JAK3 inhibitor), first-approved JAK inhibitor for RA; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2012 (NDA203214 ORIG-1 approved 2012-11-06); attribution target. Sources: PMID:22873530;PMID:22873531;NCT:NCT00814307;NCT:NCT00853385;PMID:25398374;FDA:NDA203214. Notes: Manuscript names no drug; tofacitinib is the first-approved JAK inhibitor for RA. The family's genetic leg is STAT4; tofacitinib acts on JAK1/JAK3 upstream of STAT phosphorylation, so drug target and instrument sit at different nodes of one pathway. ORAL Solo (Phase III): ACR20 and HAQ-DI primaries met (P<0.001); the third co-primary, DAS28-4(ESR)<2.6, was not significant (P=0.62, 0.10). ORAL Standard (Phase III): all three primaries met. Coded 'met' because both trials met the lead primary and the programs do not disagree; the missed co-primary in ORAL Solo is recorded here. Target engagement from the Phase II synovial biopsy study (PMID 25398374): clinical improvement correlates with reductions in STAT1 and STAT3 phosphorylation. Safety: serious infections, two cases of pulmonary tuberculosis, LDL elevation and neutrophil reduction reported; approval followed with these on the label.
- **MR state:** supportive (signed d 0.1005 / 0.1318 / 0.1614; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, registration-consistent instrument, unique-evidence, Amendment 4

## CD20-RA

Domain autoimmune; status pre-registered; registered: OBS d 0.5, MR OR 1.291 (1.19-1.391), MR d 0.141 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.291 (1.19–1.391) | d 0.5 | Approved | CD20/B-cell: RF positivity 60-80% in RA; B-cell infiltration in synovium FCRL3 GWAS OR 2.15 (Kochi 2005, Nature Genetics) |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.291, CI_lower=1.190, CI_upper=1.391, cohen_d=0.141, drug_outcome=Approved, classification=Concordant, source=FCRL3 proteomics MR (SSRN 4709115); evidence_type=OBS, study_design=case_control_SMD, cohen_d=0.500, drug_outcome=Approved, classification=Concordant, source=RF positivity 60-80% in RA; B-cell synovial infiltration; author-estimated SMD |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=1.291, mr_d=0.141, mr_ci=(1.19-1.391), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — SSRN 4709115 (preprint, 2024). Located by literature search: "genetically predicted higher FCRL3 protein expression ... OR 1.291 (95% CI 1.190-1.391), p = 1.17e-10" (protein-expression MR with colocalization). Preprint not indexed in PubMed; number not verified by direct read. Note: The two repository files name different sources of different kinds: paper/supplementary_data.csv says 'FCRL3 proteomics MR (SSRN 4709115)', while the classifier comment in analysis/classifier/classify_families.py says 'FCRL3 GWAS OR 2.15 (Kochi 2005, Nature Genetics)'. The SSRN preprint is not indexed in PubMed or Europe PMC and publisher pages were out of scope for this audit; Kochi 2005's OR 2.15 does not match the value used, 1.291 (1.19-1.391). The design cannot be settled from the cited record. / Located after the audit by literature search; exposure is plasma FCRL3, not CD20 (MS4A1).
- **Outcome codebook:** program rituximab (Rituxan/MabThera; anti-CD20), first-approved B-cell-depleting agent for RA; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2006 (BLA103705 SUPPL-5211 efficacy supplement approved 2006-02-28; current label set-id b172773b-3905-4a1c-ad95-bab4b6126563 carries the RA indication); attribution target. Sources: PMID:16947627;NCT:NCT00468546;PMID:15201414;PMID:16649186;FDA:BLA103705. Notes: Manuscript names no drug for this family (rituximab is named only under Anti-CD20-MS). REFLEX (Phase III): ACR20 at week 24 51% vs 18%, P<0.0001. Target engagement stated in the pivotal abstract: 'Rituximab depleted peripheral CD20+ B cells'. Safety: most adverse events at first infusion, mild to moderate; serious infections 5.2 vs 3.7 per 100 patient-years. Regulatory: the Drugs@FDA row for SUPPL-5211 does not name the indication; it is the only non-orphan efficacy supplement approved in early 2006 for BLA103705 and the current label carries the RA indication; the approval letter (103705s5211_ltr.pdf) could not be retrieved because the FDA document server returned an abuse-detection block page.
- **MR state:** supportive (signed d 0.0959 / 0.1408 / 0.182; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, Amendment 4

## IL-4Ra-AD

Domain autoimmune; status construct-limited; registered: OBS d 0.15, MR OR 1.02 (no CI), MR d 0.011 (null); qualitative discordance → failure; outcome Construct-limited; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.02 (no CI) | d 0.15 | Construct-limited | IL-4Ra/AD: CONSTRUCT-LIMITED — IL-4 mRNA NOT dominant in AD lesions; IL-13 is 7x elevated (Hamid 1996 PMID 9158100; Jeong 2003 PMID 15014952). Dupilumab blocks IL-4Ra (shared receptor), works via IL-13. EXCLUDED FROM SCORING: construct-definition problem, not a clean miss. Drug outcome "Construct-limited" removes it from denominator. |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.02, cohen_d=0.011, drug_outcome=Approved, classification=Construct-limited, source=Weak/null IL4R MR for AD (systematic review PMID 37977498); evidence_type=OBS, study_design=case_control_SMD, cohen_d=0.150, drug_outcome=Approved, classification=Construct-limited, source=CONSTRUCT ISSUE: IL-4 not dominant in AD; IL-13 is 7x elevated (Hamid 1996 PMID 9158100; Jeong 2003 PMID 15014952) |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.15, mr_or_raw=1.02, mr_d=0.011, mr_class=null, classification=qualitative discordance, drug_outcome=Construct-limited, status=construct-limited |

### Readings

- **Outcome codebook:** program dupilumab (Dupixent; anti-IL-4R alpha), first-approved IL-4R alpha antagonist; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2017 (BLA761055 ORIG-1 approved 2017-03-28); attribution target. Sources: PMID:27690741;NCT:NCT02277743;NCT:NCT02277769;PMID:25006719;PMID:25482871;FDA:BLA761055. Notes: Manuscript names dupilumab. SOLO 1 and SOLO 2 (Phase III): primary IGA 0/1 with >=2-point reduction at week 16 met in both (38%/37% vs 10%; 36%/36% vs 8%; P<0.001). Target engagement from the Phase I/II program (PMID 25006719: dose-dependent improvements in biomarker levels and the transcriptome; PMID 25482871: TH2 chemokines CCL17/CCL18/CCL22/CCL26 inhibited), not from the pivotal trials. Safety: injection-site reactions and conjunctivitis more frequent than placebo. The registered drug_outcome is 'Construct-limited', which is an exclusion label about the observational construct (IL-4 vs IL-13), not a program outcome; the program itself reads as approved on every field.
- **MR state:** inconclusive (signed d  / 0.0109 / ; scale-unresolved False; alignment construct-limited)

## IL-1b-CVD

Domain autoimmune; status pre-registered; registered: OBS d 0.174, MR OR 1.0 (no CI), MR d 0.0 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** primary endpoint met but registered outcome is failure (regulatory reading)

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `bf7f175` | 2026-07-06 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (no CI) | 1.37 | Failed | IL-1b/CVD: CRP/IL-1 inflammatory axis observational OR 1.37 (ERFC 2010) Same construct as cardio CRP family |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `bf7f175` | 2026-07-06 | paper/supplementary_data.csv | evidence_type=GEN, study_design=MR, effect_size_original=1.00, cohen_d=0.000, drug_outcome=Failed, classification=Qual. disc., source=IL-1Ra MR: genetically higher IL-1Ra -> increased CAD OR 1.36 (PMID 32223966); null/adverse for IL-1 blockade; evidence_type=OBS, study_design=observational, effect_size_original=1.37, cohen_d=0.174, drug_outcome=Failed, classification=Qual. disc., source=CRP/IL-1 inflammatory axis (ERFC 2010); same construct as cardio CRP family |
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.174, mr_or_raw=1.0, mr_d=0.0, mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=pre-registered |

### Readings

- **Genetic leg:** MR-instrumented — PMID 32223966. We conducted a Mendelian randomization study to investigate the associations of circulating ILs with coronary artery disease (CAD), atrial fibrillation (AF), and ischemic stroke. Single-nucleotide polymorphisms associated with IL-1beta, IL-1 receptor antagonist (IL-1ra) ... were identified from genome-wide association studies Note: Yuan/Larsson 2020 Int J Cardiol. The cited source is an IV design reporting ORs with CIs (IL-1ra 1.36 (1.14-1.63) per SD), but the classifier holds OR 1.00 with no CI for this family and reports IL-1beta as not associated with any outcome, so the family carries no interval of its own.
- **Outcome codebook:** program canakinumab (Ilaris; anti-IL-1 beta), CANTOS; phase III; engagement yes; efficacy met; safety unclear; decision discontinued; regulatory not approved FDA, not approved for cardiovascular risk reduction (stated in PMID 31882264, published online 2019-12-06; decision year not given in the retrievable source); no cardiovascular indication on the current Ilaris label (set-id 7d271f3b-e4f9-4d80-8dcf-28d49123f80e, effective 2026-06-08) and no cardiovascular efficacy supplement in the Drugs@FDA record for BLA125319; attribution uncertain. Sources: PMID:28845751;NCT:NCT01327846;PMID:29146124;PMID:31882264;PMID:30649147;FDA:BLA125319. Notes: Manuscript names canakinumab/CANTOS in the cardio text. CANTOS (Phase III, event-driven, n=10,061): 'The 150-mg dose, but not the other doses, met the prespecified multiplicity-adjusted threshold for statistical significance for the primary end point' (HR 0.85, 95% CI 0.74-0.98, P=0.021); 50 mg and 300 mg did not, so 'met' rests on one of three doses. Target engagement: hsCRP reduced 26-41 percentage points more than placebo; on-treatment hsCRP <2 mg/L tracks event reduction (PMID 29146124). Safety: 'higher incidence of fatal infection than was placebo'; whether safety drove the regulatory outcome is not stated in any retrievable source, so 'unclear'. Development decision: no Phase III cardiovascular canakinumab trial other than CANTOS is registered on ClinicalTrials.gov as of 2026-09-22 and no cardiovascular indication exists on the label; the sponsor's own post-decision statement is not retrievable through the permitted sources, so 'discontinued' is inferred from the registry and label record. Attribution 'uncertain': engagement yes, efficacy met at one dose with a modest hazard ratio, excess fatal infections, poor cost-effectiveness at list price (PMID 30649147), and no public statement of the FDA's reasons. DISAGREEMENT with registered drug_outcome 'Failed': the primary endpoint was met at 150 mg; 'Failed' is defensible only as a regulatory/development composite.
- **MR state:** inconclusive (signed d  / 0.0 / ; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags)

## VitD-Cancer

Domain oncology; status extension; registered: OBS d 0.137, MR OR 0.97 (0.88-1.07), MR d 0.017 (null); qualitative discordance → failure; outcome Failed; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.97 (0.88–1.07) | 0.78 | Failed | --- ONCOLOGY --- O1: VitD-Cancer OBS = JNCI pooled 17 cohorts, Q5 vs Q3 (mid-quintile ref) 25(OH)D and CRC (McCullough 2019, PMID 29912394): RR 0.78 (0.65-0.94) MR = systematic review of MR studies, per-SD 25(OH)D and CRC (Lawler 2023, PMID 36678292): OR 0.97 (0.88-1.07), 80+ instruments Drug: VITAL trial — vitamin D supplementation, no CRC benefit (Manson 2019) |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.137, mr_or_raw=0.97, mr_d=0.017, mr_ci=(0.88-1.07), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 36678292. To mitigate confounding, genetic instrumental variables (IVs) have been used to estimate causal associations between 25-hydroxivtamin D and cancer risk via Mendelian randomization (MR). We provide a systematic review of 31 MR studies Note: Lawler 2023 Nutrients; colorectal cancer 0.97 (0.88-1.07) per 1-SD increase, matching the classifier exactly.
- **Outcome codebook:** program vitamin D3 2000 IU/day (VITAL; academic prevention trial, sponsor Brigham and Women's Hospital); phase III; engagement yes; efficacy not met; safety acceptable; decision not reported; regulatory not submitted FDA: none (no application); attribution target. Sources: PMID:30415629; DOI:10.1056/NEJMoa1809944; NCT:NCT01169259. Notes: Prevention trial of a supplement, not a sponsored development program, so development_decision is not reported (no sponsor action to record). Registered as Phase 3 on ClinicalTrials.gov. Primary endpoint (invasive cancer of any type) HR 0.96 (0.88-1.06); colorectal cancer, the family's indication, was a secondary endpoint, HR 1.09 (0.73-1.62). Target engagement (serum 25(OH)D rise in the vitamin D arm) is stated in the Results of the full text, not in the abstract; not verified from the abstract (see log). No excess hypercalcemia or other adverse events.
- **MR state:** negligible_range (signed d -0.0705 / -0.0168 / 0.0373; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## IGF1-CRC

Domain oncology; status extension; registered: OBS d 0.062, MR OR 1.22 (1.09-1.36), MR d 0.11 (causal); genetic-only signal → success; outcome Failed; correct False.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.22 (1.09–1.36) | 1.12 | Failed | O2: IGF1-CRC OBS = serologic analysis, per-quintile IGF-1 and CRC (Rinaldi 2019, PMID 31884076, Gastroenterology): OR ~1.12 MR = genetically predicted IGF-1 per SD and CRC, 416 SNPs (Larsson 2020, PMID 32717139, Cancer Medicine): OR 1.22 (1.09-1.36) [BioBank Japan] UK Biobank estimate is 1.11 (1.01-1.22); Japan chosen as larger sample for CRC Drugs: figitumumab (Langer 2014), ganitumab (Juergens 2 |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.062, mr_or_raw=1.22, mr_d=0.11, mr_ci=(1.09-1.36), mr_class=causal, classification=genetic-only signal, drug_outcome=Failed, correct=False, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 32717139. We used 416 single-nucleotide polymorphisms robustly associated with serum IGF-1 levels to assess the potential causal associations between this hormone and site-specific cancers through Mendelian randomization Note: Larsson 2020 Cancer Med; BioBank Japan colorectal OR 1.22 (1.09-1.36) per SD, matching the classifier exactly.
- **Outcome codebook:** program figitumumab (Pfizer; Phase III NSCLC) and ganitumab (COG AEWS1221 Ewing sarcoma; QUILT-2.014 pancreatic), as the manuscript names; phase III; engagement not reported; efficacy not met; safety limiting; decision discontinued; regulatory not submitted FDA: none (no application); attribution indication. Sources: PMID:24888810; DOI:10.1200/JCO.2013.54.4932; NCT:NCT00596830; PMID:36669140; DOI:10.1200/JCO.22.01815; NCT:NCT02306161; NCT:NCT01231347. Notes: INDICATION MISMATCH: neither named program has a Phase III readout in colorectal cancer; trial_phase III is the phase of the readouts on which drug_outcome was coded (NSCLC, Ewing, pancreatic). Under a strict reading of 'for the family's exact indication' this field would be not reported. Figitumumab NSCLC trial closed early by the DSMC for futility and increased serious adverse events and treatment-related deaths (safety limiting); ganitumab Ewing trial did not improve EFS (HR 1.00, 0.76-1.33), with possibly increased toxicity. Neither abstract reports a pharmacodynamic marker of IGF-1R engagement, so target_engagement is not reported. Attribution: indication (never tested in CRC) chosen over target; the manuscript's translation-gap reading is not contradicted by the record but is not supported by a reported engagement measure either. Figitumumab: 'Further clinical development of figitumumab is not being pursued.'
- **MR state:** supportive (signed d 0.0475 / 0.1096 / 0.1695; scale-unresolved False; alignment indication mismatch)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags)

## Estrogen-BC

Domain oncology; status extension; registered: OBS d 0.145, MR OR 1.03 (1.01-1.06), MR d 0.016 (null); qualitative discordance → failure; outcome Approved; correct False.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.03 (1.01–1.06) | 1.3 | Approved | O3: Estrogen-BC OBS = estrogen-only HRT and breast cancer (Million Women Study, Beral 2003, PMID 12927427, Lancet): RR 1.30 MR = estradiol per SD and overall breast cancer, 2 SNPs (CYP19A1-based) (Nounu 2022, PMID 36209141, Breast Cancer Research): OR 1.03 (1.01-1.06) Drug: tamoxifen approved for chemoprevention (Cuzick 2015) NOTE: MR CI excludes null but d=0.016 < 0.10 — pharmacological amplifica |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.145, mr_or_raw=1.03, mr_d=0.016, mr_ci=(1.01-1.06), mr_class=null, classification=qualitative discordance, drug_outcome=Approved, correct=False, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 36209141. We used a two-sample Mendelian randomization analysis to investigate this association ... Genetic instruments for nine sex steroid hormones and sex hormone-binding globulin (SHBG) were obtained from genome-wide association studies Note: Nounu 2022 Breast Cancer Res; estradiol per SD on overall breast cancer OR 1.03 (1.01-1.06), matching the classifier exactly.
- **Outcome codebook:** program tamoxifen (NSABP P-1 Breast Cancer Prevention Trial; Nolvadex NDA 017970), as the manuscript names; aromatase inhibitors not coded; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 1998 (Nolvadex NDA017970 efficacy supplements 39 and 40 approved 1998-10-29); attribution target. Sources: PMID:9747868; DOI:10.1093/jnci/90.18.1371; PMID:23639488; DOI:10.1016/S0140-6736(13)60140-3; FDA:NDA017970; FDA:NDA021807. Notes: Target engagement read from the ER-specific effect in P-1: invasive ER-positive tumors reduced 69% with no difference in ER-negative tumors. Safety: endometrial cancer (RR 2.53) and thromboembolic events increased; approved with a boxed warning (Soltamox label, NDA021807), so safety did not determine the outcome. Drugs@FDA lists two efficacy supplements approved 1998-10-29; that these are the risk-reduction indication is inferred from the date matching the P-1 publication year and the label section 14.4, not from the supplement text.
- **MR state:** negligible_range (signed d 0.0055 / 0.0163 / 0.0321; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Eos/IL5-Asthma

Domain respiratory; status extension; registered: OBS d 0.8, MR OR 1.5 (1.23-1.83), MR d 0.224 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.5 (1.23–1.83) | d 0.8 | Approved | --- RESPIRATORY --- R1: Eos/IL5-Asthma OBS = eosinophil count in severe vs mild asthma (Wagener 2022, estimated SMD ~0.80) MR = eosinophil count per SD and moderate-severe asthma, 151 variants (Guyatt 2023, Thorax; preprint 2020): weighted median OR 1.50 (1.23-1.83) Drugs: mepolizumab (Pavord 2012), benralizumab — both approved |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.8, mr_or_raw=1.5, mr_d=0.224, mr_ci=(1.23-1.83), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 35537820. We performed Mendelian randomisation (MR) using 151 variants from genome-wide association studies of blood eosinophils in UK Biobank/INTERVAL, and respiratory traits in UK Biobank/SpiroMeta Note: Guyatt 2023 Thorax; moderate-severe asthma weighted median OR 1.50 (1.23-1.83) per SD eosinophils, matching the classifier exactly.
- **Outcome codebook:** program mepolizumab (Nucala BLA 125526; MENSA pivotal Phase III; DREAM Phase IIb dose-ranging); benralizumab named in manuscript, not coded; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2015 (BLA125526 original approval 2015-11-04); attribution target. Sources: PMID:25199059; DOI:10.1056/NEJMoa1403290; NCT:NCT01691521; PMID:22901886; DOI:10.1016/S0140-6736(12)60988-X; NCT:NCT01000506; FDA:BLA125526. Notes: The manuscript cites DREAM (Pavord 2012) for the drug outcome; ClinicalTrials.gov registers DREAM as Phase 2 (NCT01000506). The Phase III readout is MENSA (NCT01691521): exacerbations reduced 47% (IV) and 53% (SC). Target engagement from the FDA label section 12.2: dose-dependent blood eosinophil reduction (64-90% at day 84). Safety profile similar to placebo in MENSA.
- **MR state:** supportive (signed d 0.1141 / 0.2235 / 0.3332; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, Amendment 4

## IL4Ra-Asthma

Domain respiratory; status construct-limited; registered: OBS d 0.5, MR OR 0.87 (0.82-0.93), MR d 0.077 (null); qualitative discordance → failure; outcome Construct-limited; correct —.

**Flags:** gen_OR changed across committed classifier versions; drug_outcome changed across committed classifier versions

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.02 (no CI) | d 0.5 | Construct-limited | R2: IL4Ra-Asthma OBS = IL-4/IL-13 pathway elevation in asthma (estimated SMD ~0.50) MR = proteome-wide MR identifies IL-4Ra as causal for asthma with colocalization, but no specific OR with CI available Drug: dupilumab approved (Busse 2019) CONSTRUCT-LIMITED: no MR OR meeting two-criterion rule |
| `5117419` | 2026-07-09 | obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, drug_outcome | 0.87 (0.82–0.93) | d 0.5 | Approved | R2: IL4Ra-Asthma OBS = IL-4/IL-13 pathway elevation in asthma (estimated SMD ~0.50) MR = cis-pQTL MR for soluble IL4R protein on asthma (Bretherick 2020, PMID 32628676, PLOS Genetics): OR ~0.87 (0.82-0.93) Direction: higher soluble IL4R (decoy receptor) = less asthma CAVEAT: pQTL measures soluble IL4R, not membrane-bound (drug target). Soluble acts as decoy sequestering IL-4; dupilumab blocks memb |
| `1312b52` | 2026-07-09 | obs_sourcing, drug_outcome | 0.87 (0.82–0.93) | d 0.5 | Construct-limited | R2: IL4Ra-Asthma OBS = IL-4/IL-13 pathway elevation in asthma (estimated SMD ~0.50) MR = cis-pQTL MR for soluble IL4R protein on asthma (Bretherick 2020, PMID 32628676, PLOS Genetics): OR ~0.87 (0.82-0.93) Direction: higher soluble IL4R (decoy receptor) = less asthma CAVEAT: pQTL measures soluble IL4R, not membrane-bound (drug target). Soluble acts as decoy sequestering IL-4; dupilumab blocks memb |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=0.87, mr_d=0.077, mr_ci=(0.82-0.93), mr_class=null, classification=qualitative discordance, drug_outcome=Construct-limited, status=construct-limited |

### Readings

- **Outcome codebook:** program dupilumab (Dupixent BLA 761055; LIBERTY ASTHMA QUEST); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2018 (BLA761055 efficacy supplement 7 approved 2018-10-19); attribution target. Sources: PMID:29782217; DOI:10.1056/NEJMoa1804092; NCT:NCT02414854; FDA:BLA761055. Notes: Registered drug_outcome is Construct-limited (exclusion status), not an outcome; the trial and regulatory record read approved. Coprimary endpoints met: severe exacerbation rate 47.7% lower, FEV1 +0.14 L vs placebo. Target engagement from label section 12.2: FeNO, eotaxin-3, total IgE, TARC and periostin decreased vs placebo in QUEST. Transient blood eosinophilia in 4.1% on dupilumab. Supplement 7 identified as the asthma indication by its date (2018-10-19); supplement text not read.
- **MR state:** inconclusive (signed d -0.1094 / -0.0768 / -0.04; scale-unresolved False; alignment construct-limited)

## TSLP-Asthma

Domain respiratory; status construct-limited; registered: OBS d 0.4, MR OR 1.02 (no CI), MR d 0.011 (null); qualitative discordance → failure; outcome Construct-limited; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.02 (no CI) | d 0.4 | Construct-limited | R3: TSLP-Asthma OBS = TSLP elevated in severe asthma (estimated SMD ~0.40) MR = no specific pQTL MR with OR and CI for TSLP and asthma Drug: tezepelumab approved (Menzies 2022) CONSTRUCT-LIMITED: no drug-target MR with specific effect size |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.4, mr_or_raw=1.02, mr_d=0.011, mr_class=null, classification=qualitative discordance, drug_outcome=Construct-limited, status=construct-limited |

### Readings

- **Outcome codebook:** program tezepelumab (Tezspire BLA 761224; NAVIGATOR); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2021 (BLA761224 original approval 2021-12-17); attribution target. Sources: PMID:33979488; DOI:10.1056/NEJMoa2034975; NCT:NCT03347279; FDA:BLA761224. Notes: Registered drug_outcome is Construct-limited (exclusion status); the record reads approved. Primary endpoint met: annualized exacerbation rate ratio 0.44 (0.37-0.53). Target engagement from label section 12.2: in NAVIGATOR, blood eosinophils, FeNO, IL-5 and IL-13 reduced vs placebo from week 2. Adverse events did not differ meaningfully between groups.
- **MR state:** inconclusive (signed d  / 0.0109 / ; scale-unresolved False; alignment construct-limited)

## SGLT2-HF

Domain metabolic; status extension; registered: OBS d 0.309, MR OR 0.44 (0.26-0.76), MR d 0.453 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.44 (0.26–0.76) | 1.75 | Approved | --- METABOLIC/ENDOCRINE --- M1: SGLT2-HF OBS = T2D and HF risk, meta-analysis of 47 cohorts, 12M individuals (Ohkuma 2019, PMID 31317230, Diabetologia): RR 1.74 (men) to 1.95 (women) MR = drug-target MR, SLC5A2 cis-eQTL, proteome-wide MR (PMC11079590, 2024 Frontiers): OR 0.44 (0.26-0.76), P=0.003 Drug: empagliflozin, dapagliflozin approved for HF |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.309, mr_or_raw=0.44, mr_d=0.453, mr_ci=(0.26-0.76), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 38725835. Applying a two-sample, two-step Mendelian Randomization (MR) analysis, we aimed to estimate: (1) the causal impact of SGLT2 inhibition on HF ... Genetic variants linked to SGLT2 inhibition derived from the previous studies Note: Luo 2024 Front Cardiovasc Med (PMC11079590, the identifier the classifier comment gives); drug-target MR, OR 0.44 (0.26-0.76), matching the classifier exactly.
- **Outcome codebook:** program dapagliflozin (Farxiga NDA 202293; DAPA-HF) and empagliflozin (Jardiance NDA 204629; EMPEROR-Reduced), as the manuscript names; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2020 (Farxiga NDA202293 efficacy supplement 20 approved 2020-05-05); FDA 2021 (Jardiance NDA204629 efficacy supplement 26 approved 2021-08-18); attribution target. Sources: PMID:31535829; DOI:10.1056/NEJMoa1911303; NCT:NCT03036124; PMID:32865377; DOI:10.1056/NEJMoa2022190; NCT:NCT03057977; FDA:NDA202293; FDA:NDA204629. Notes: Primary endpoints met in both trials: DAPA-HF HR 0.74 (0.65-0.85), EMPEROR-Reduced HR 0.75 (0.65-0.86). Target engagement is from the labels' section 12.2 (urinary glucose excretion in type 2 diabetes and healthy subjects), not from the HF trials, which report no SGLT2 pharmacodynamic marker; the HF mechanism is stated in DAPA-HF's abstract as 'possibly through glucose-independent mechanisms'. Supplements 20 and 26 identified as the HFrEF indications by date; supplement text not read. Later expansions: Jardiance supplement 33 (2022-02-24), Farxiga supplement 26 (2023-05-08).
- **MR state:** supportive (signed d -0.7427 / -0.4526 / -0.1513; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## GLP1R-T2D/Obesity

Domain metabolic; status construct-limited; registered: OBS d 0.0, MR OR 1.0 (no CI), MR d 0.0 (null); null concordance → ambiguous; outcome Construct-limited; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (no CI) | d 0.0 | Construct-limited | M2: GLP1R-T2D/Obesity (combined per pre-registration amendment) OBS = no natural observational exposure (GLP-1R is a drug receptor, not a naturally varying biomarker like LDL or urate) MR = drug-target cis-MR exists (OR 0.79, 0.75-0.85 for T2D from cis-eQTL studies), but OBS counterpart undefined Drug: semaglutide, liraglutide approved for T2D and obesity CONSTRUCT-LIMITED: no OBS-MR pair meeting  |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.0, mr_or_raw=1.0, mr_d=0.0, mr_class=null, classification=null concordance, drug_outcome=Construct-limited, status=construct-limited |

### Readings

- **Outcome codebook:** program semaglutide (Ozempic NDA 209637 for type 2 diabetes; Wegovy NDA 215256 for obesity; STEP 1 and SUSTAIN-6), coded as the manuscript's first-named agent; liraglutide not coded; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2017 (Ozempic NDA209637 original approval 2017-12-05); FDA 2021 (Wegovy NDA215256 original approval 2021-06-04); attribution target. Sources: PMID:33567185; DOI:10.1056/NEJMoa2032183; NCT:NCT03548935; PMID:27633186; DOI:10.1056/NEJMoa1607141; NCT:NCT01720446; FDA:NDA209637; FDA:NDA215256. Notes: Registered drug_outcome is Construct-limited (exclusion status); the record reads approved. STEP 1 coprimary endpoints met (-14.9% vs -2.4% body weight; 86.4% vs 31.5% achieving 5% loss). SUSTAIN-6 met its noninferiority primary (MACE HR 0.74) and is a cardiovascular-outcomes trial; the glycemic pivotal trials (SUSTAIN 1-5) are not individually cited here. Target engagement from the Ozempic label section 12.2 (fasting glucose -29 mg/dL, 2-h postprandial -74 mg/dL vs placebo) and the Wegovy label (reduced calorie intake, delayed gastric emptying). Safety: gastrointestinal events; boxed warning for thyroid C-cell tumors from rodent data.
- **MR state:** inconclusive (signed d  / 0.0 / ; scale-unresolved False; alignment construct-limited)

## Urate-Gout

Domain metabolic; status extension; registered: OBS d 0.641, MR OR 5.0 (3.5-8.0), MR d 0.887 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `1f300a9` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 5.0 (3.5–8.0) | 3.2 | Approved | M3: Urate-Gout OBS = serum urate and incident gout, longitudinal cohort (Robinson 2021, PMC8399746): HR 18.62 for >=7 vs <4 mg/dL; per-SD (SD ~1.2 mg/dL) HR ~3.2 derived from dose-response curve (not directly reported) MR = genetically predicted serum urate and gout, 26 SNPs (Li 2019, PMC6333326, PLOS Med): OR 3.41-6.04 per 1 mg/dL across 7 MR methods; rescaled to per-SD (1.2 mg/dL): ~5.0 (range 4 |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.641, mr_or_raw=5.0, mr_d=0.887, mr_ci=(3.5-8.0), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 30645594. We used Mendelian randomization (MR) methods to evaluate the presence of a causal effect ... the same MR approaches showed that SU has a causal effect on the risk of gout (OR estimates ranging from 3.41 to 6.04 per 1-mg/dl increase in SU, all P < 10-3), which served as a positive control of our approach Note: PMC6333326 is Jordan 2019 PLoS Med, not 'Li 2019' as the classifier comment states. The gout figures the classifier rescales (3.41-6.04 per 1 mg/dL) are the paper's positive control; the paper's own headline result is a null effect of urate on chronic kidney disease.
- **Outcome codebook:** program febuxostat (Uloric NDA 021856; FACT, CONFIRMS, CARES) coded as the program with a modern trial record; allopurinol (Zyloprim NDA 016084, approved 1966) is the manuscript's first-named agent and predates the registered-trial era; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2009 (Uloric NDA021856 original approval 2009-02-13); FDA 1966 (Zyloprim NDA016084 original approval 1966-08-19); attribution target. Sources: PMID:16339094; DOI:10.1056/NEJMoa050373; PMID:20370912; DOI:10.1186/ar2978; NCT:NCT00430248; PMID:29527974; DOI:10.1056/NEJMoa1710895; NCT:NCT01101035; FDA:NDA021856; FDA:NDA016084. Notes: Class family; the manuscript names allopurinol and febuxostat. The pivotal primary endpoint is a biomarker (serum urate <6.0 mg/dL), met in FACT (53-62% vs 21%) and CONFIRMS; it is also the target-engagement readout. Gout flares were not reduced relative to allopurinol over 52 weeks in FACT. Safety: CARES (post-marketing) found higher all-cause (HR 1.22) and cardiovascular (HR 1.34) mortality with febuxostat vs allopurinol; the label now carries a boxed warning and restricts use to allopurinol failure or intolerance (label supplement 13, 2019-02-21). Safety did not determine the development outcome, so coded acceptable, with the post-marketing restriction noted.
- **MR state:** supportive (signed d 0.6907 / 0.8873 / 1.1465; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## IL6-MDD

Domain psychiatry; status extension; registered: OBS d 0.15, MR OR 1.01 (0.99-1.04), MR d 0.005 (null); qualitative discordance → failure; outcome Failed; correct True.

**Flags:** scored on a Phase II readout

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `e9a2353` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.01 (0.99–1.04) | d 0.15 | Failed | B1: IL-6 signaling -> MDD OBS = CRP and depression, meta-analysis of 41 community+clinical studies (Howren 2009, Psychosom Med, PMID 19592519): CRP d=0.15 (0.10-0.21) MR = genetically predicted CRP (>500 instruments) and depression (bidirectional MR, UK Biobank): OR 1.01 (0.99-1.04) per SD CRP — null Khandaker IL6R-specific CRP->depression also null (OR ~0.95, CI incl null) Drug: sirukumab failed  |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.15, mr_or_raw=1.01, mr_d=0.005, mr_ci=(0.99-1.04), mr_class=null, classification=qualitative discordance, drug_outcome=Failed, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID:36057695 (Galan 2022, Sci Rep). "We did not find evidence for a reciprocal relationship between CRP levels (using > 500 genetic instruments for CRP) and depression (OR CRP-Dep = 1.01, 95% CI 0.99-1.04 ...)" (bidirectional two-sample MR; Table 3: CRP -> Depression, 512 SNPs, OR 1.01, 0.99-1.04) Note: Source identified after the audit by the Amendment 5 IL6-MDD search (analysis/amendment5/il6_mdd/); polygenic CRP MR, not the IL6R-region instrument Amendment 2 declared (that deviation is handled by the registration-consistent-instrument row).
- **Outcome codebook:** program sirukumab 50 mg SC adjunctive to a monoaminergic antidepressant (Janssen; NCT02473289); phase II; engagement not reported; efficacy not met; safety acceptable; decision discontinued; regulatory not submitted FDA: none (no application for MDD); attribution uncertain. Sources: NCT:NCT02473289. Notes: PHASE II readout (registry: Phase 2). Primary endpoint (HDRS-17 change at week 12) not met: LS-mean difference -0.8 (95% CI -2.77 to 1.10), p = 0.310; 193 randomized (99 placebo, 94 sirukumab), 169 completed. The registry records the trial as COMPLETED, which contradicts Amendment 2's 'terminated early for futility'. The registry posts no pharmacodynamic outcome (no CRP or IL-6 measure), so target_engagement is not reported. The publication Amendment 2 cites (Boyle et al. 2020, Mol Psychiatry) was not found on PubMed by author, drug, indication or NCT-number searches, and the manuscript carries no bib entry for the trial; the registry record is the only source coded. Safety: serious adverse events 3/94 vs 2/99, no deaths; efficacy futility, not safety, determined the outcome. Development: no later sirukumab depression trial is registered; discontinuation is inferred from that absence. Attribution uncertain: a single adjunctive Phase II cannot separate target from dose, design or indication.
- **MR state:** negligible_range (signed d -0.0055 / 0.0055 / 0.0216; scale-unresolved False; alignment instrument-target mismatch)
- **Registered instrument estimate:** PMID 33631287, OR 1.023 (1.006–1.039)
- **In analysis sets:** registered, Amyloid-AD scored, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS (classifier flags), Amendment 4

## IL23-Crohns

Domain gastroenterology; status construct-limited; registered: OBS d 0.5, MR OR 1.0 (no CI), MR d 0.0 (null); qualitative discordance → failure; outcome Construct-limited; correct —.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `e9a2353` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.0 (no CI) | d 0.5 | Construct-limited | B2: IL-23 -> Crohn's disease OBS = CONSTRUCT-LIMITED: no prospective population-level OBS estimate for circulating IL-23 predicting incident Crohn's. Case-control cytokine data exists (IBD patients IL-23 ~52 vs controls ~24 pg/mL; PMC8621192) but no meta-analytic SMD with CI. Cross-sectional, not prospective. MR = IL23R rs11209026 (R381Q) per allele, meta-analysis of 49 studies (Nie 2015, Sci Rep, |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=1.0, mr_d=0.0, mr_class=null, classification=qualitative discordance, drug_outcome=Construct-limited, status=construct-limited |

### Readings

- **Outcome codebook:** program risankizumab (Skyrizi BLA 761105; ADVANCE and MOTIVATE induction, FORTIFY maintenance); guselkumab named in the blind declaration, not coded; phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2022 (BLA761105 efficacy supplement 16 approved 2022-06-16); attribution target. Sources: PMID:35644154; DOI:10.1016/S0140-6736(22)00467-6; NCT:NCT03105128; NCT:NCT03104413; PMID:35644155; DOI:10.1016/S0140-6736(22)00466-4; NCT:NCT03105102; FDA:BLA761105. Notes: Registered drug_outcome is Construct-limited (exclusion status); the record reads approved. All coprimary endpoints (clinical remission and endoscopic response at week 12) met in both induction trials; FORTIFY week-52 coprimary endpoints met at 360 mg. Target engagement read from FORTIFY ('inflammatory biomarkers were consistent with a dose-response relationship'); the label states no formal pharmacodynamic studies were conducted. Supplement 16 identified as the Crohn's indication by date; supplement text not read.
- **MR state:** inconclusive (signed d  / 0.0 / ; scale-unresolved True; alignment construct-limited)

## Complement-GA

Domain ophthalmology; status extension; registered: OBS d 0.5, MR OR 2.5 (2.2-2.85), MR d 0.505 (causal); concordance → success; outcome Failed; correct False.

**Flags:** genetic leg is a variant-disease association, not MR

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `e9a2353` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 2.5 (2.2–2.85) | d 0.5 | Failed | B3: Complement pathway (Factor D) -> geographic atrophy OBS = complement activation products (C3a, C5a, Ba, C3d) significantly elevated in AMD patients vs controls (p<0.001 for Ba, C3d) (Reynolds 2009, PLOS ONE, PMID 18628698): n=112 AMD, n=67 controls Author-estimated SMD ~0.50 from p<0.001 at those sample sizes MR = CFH Y402H (rs1061170) per allele, meta-analysis of 8 studies (Thakkinstian 2006, |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.5, mr_or_raw=2.5, mr_d=0.505, mr_ci=(2.2-2.85), mr_class=causal, classification=concordance, drug_outcome=Failed, correct=False, status=extension |

### Readings

- **Genetic leg:** association — PMID 16905558. We performed a meta-analysis to estimate the magnitude of the gene effect and the possible mode of action. A meta-analysis of eight studies assessing association between the CFH Y402H polymorphism and AMD was performed Note: Thakkinstian 2006 Hum Mol Genet; a genotype-disease meta-analysis ('those having CC and TC genotypes being roughly six and 2.5 times more likely to have AMD than patients with TT genotype'). No exposure is instrumented, and Amendment 5 names this family as a known failure of the MR-instrumented rule.
- **Outcome codebook:** program lampalizumab, anti-complement factor D Fab (Roche; CHROMA and SPECTRI), the registered program; later same-indication approvals pegcetacoplan (anti-C3, Syfovre NDA 217171) and avacincaptad pegol (anti-C5, Izervay NDA 217225) recorded in notes; phase III; engagement not reported; efficacy not met; safety acceptable; decision discontinued; regulatory not submitted FDA: none for lampalizumab; same indication later approved for pegcetacoplan, FDA 2023 (NDA217171 original approval 2023-02-17), and avacincaptad pegol, FDA 2023 (NDA217225 original approval 2023-08-04); attribution uncertain. Sources: PMID:29801123; DOI:10.1001/jamaophthalmol.2018.1544; NCT:NCT02247479; NCT:NCT02247531; PMID:37865470; DOI:10.1016/S0140-6736(23)01520-9; NCT:NCT03525613; NCT:NCT03525600; PMID:37696275; DOI:10.1016/S0140-6736(23)01583-0; NCT:NCT04435366; FDA:NDA217171; FDA:NDA217225. Notes: Coded on lampalizumab. Primary endpoint (change in GA area at week 48) not met in either trial (differences -0.02 to 0.16 mm2, none favoring drug); both registry records TERMINATED. Neither the Phase III report's abstract nor the registry reports an ocular pharmacodynamic measure of factor D inhibition, so target_engagement is not reported; the manuscript's Table criteria sentence 'the trial reports target engagement without endpoint benefit' is not supported by the sources coded. Safety: endophthalmitis 0.4% of treated participants; safety did not determine the outcome. DISAGREEMENT VISIBLE: the same indication was later approved for two complement inhibitors at other nodes: pegcetacoplan (OAKS met its 12-month primary, DERBY did not; both met at 24 months; 'the first treatment approved by the US FDA for geographic atrophy') and avacincaptad pegol (GATHER2 primary met, 14% slower growth). EMA outcome for pegcetacoplan not queried (EMA not part of the API rules used). Attribution uncertain: the record cannot separate the target node (factor D) from the molecule (lampalizumab potency or intravitreal dosing interval).
- **MR state:** supportive (signed d 0.4347 / 0.5052 / 0.5774; scale-unresolved True; alignment instrument-target mismatch)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, registration-consistent instrument, unique-evidence

## Sclerostin-Fracture

Domain musculoskeletal; status extension; registered: OBS d 0.33, MR OR 0.59 (0.54-0.66), MR d 0.291 (causal); concordance → success; outcome Approved; correct True.

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `e9a2353` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 0.59 (0.54–0.66) | 0.55 | Approved | B4: Sclerostin -> osteoporotic fracture OBS = MINOS prospective cohort (men, n=725, 10yr follow-up) (Szulc 2014, PMID 23165952): HR 0.55 (0.31-0.96) per highest vs lowest sclerostin tertile — PROTECTIVE direction (reverse causation) NOTE: OFELY study in postmenopausal women found null association; Ardawi 2012 in Saudi women found positive association. Evidence is bidirectional; MINOS is largest pr |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.33, mr_or_raw=0.59, mr_d=0.291, mr_ci=(0.54-0.66), mr_class=causal, classification=concordance, drug_outcome=Approved, correct=True, status=extension |

### Readings

- **Genetic leg:** MR-instrumented — PMID 32581134. investigate whether genetic variants that mimic therapeutic inhibition of sclerostin are associated with higher risk of cardiovascular disease ... Scaled to the equivalent dose of romosozumab (210 milligrams per month; 0.09 grams per square centimeter of higher bone mineral density), the SOST genetic variants were associated with lower risk of fracture and osteoporosis Note: Bovijn 2020 Sci Transl Med; drug-target MR scaled to the romosozumab-equivalent dose. Classifier holds fracture OR 0.59 (0.54-0.66).
- **Outcome codebook:** program romosozumab (Evenity BLA 761062; FRAME and ARCH); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 2019 (BLA761062 original approval 2019-04-09); attribution target. Sources: PMID:27641143; DOI:10.1056/NEJMoa1607948; NCT:NCT01575834; PMID:28892457; DOI:10.1056/NEJMoa1708322; NCT:NCT01631214; FDA:BLA761062. Notes: Primary endpoints met: FRAME new vertebral fractures 73% lower at 12 months; ARCH 48% lower new vertebral and 27% lower clinical fractures vs alendronate. Target engagement from label section 12.2 (P1NP +145% and CTX -55% vs placebo at 2 weeks). Safety: ARCH reported more positively adjudicated serious cardiovascular events in year 1 (2.5% vs 1.9%); approved with a boxed warning for MI, stroke and cardiovascular death and a 12-dose limit. Safety shaped the label but did not determine the outcome, so coded acceptable.
- **MR state:** supportive (signed d -0.3397 / -0.2909 / -0.2291; scale-unresolved False; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, MR-instrumented, MR-instrumented (unresolved also removed), registration-consistent instrument, unique-evidence, source-extracted OBS, source-extracted OBS (classifier flags), Amendment 4

## Serotonin-MDD

Domain psychiatry; status extension; registered: OBS d 0.45, MR OR 1.08 (1.03-1.12), MR d 0.042 (null); qualitative discordance → failure; outcome Approved; correct False.

**Flags:** genetic leg is a variant-disease association, not MR

### Value history (committed classifier)

| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |
|---|---|---|---|---|---|---|
| `e9a2353` | 2026-07-09 | obs_OR, obs_d_direct, obs_sourcing, gen_OR, gen_CI_lower, gen_CI_upper, per_allele, sd_per_allele, drug_outcome | 1.08 (1.03–1.12) | d 0.45 | Approved | B5: Serotonin transporter -> MDD OBS = plasma tryptophan (serotonin precursor) in MDD vs controls (Ogawa 2014, J Clin Psychiatry, PMID 25295433): Hedges g=0.45 (0.84 in unmedicated patients). Plasma serotonin meta-analysis null (Moncrieff 2022). Tryptophan used as best serotonin-pathway proxy. MR = 5-HTTLPR (SLC6A4) short allele and unipolar depression (Clarke 2010, Psychol Med): OR 1.08 (1.03-1.1 |

### Supplement history

| commit | date | file | rows |
|---|---|---|---|
| `c047d39` | 2026-09-02 | data/cross_design_classification_all_41_families_v2.csv | obs_d=0.45, mr_or_raw=1.08, mr_d=0.042, mr_ci=(1.03-1.12), mr_class=null, classification=qualitative discordance, drug_outcome=Approved, correct=False, status=extension |

### Readings

- **Genetic leg:** association — PMID 20380781. We applied meta-analytic techniques to data from relevant published studies, and obtained an estimate of the likely magnitude of effect of any association ... Meta-analysis indicated evidence of a small but statistically significant association between the 5-HTTLPR polymorphism and unipolar depression [odds ratio (OR) 1.08, 95% confidence interval (CI) 1.03-1.12] Note: Clarke 2010 Psychol Med; matches the classifier exactly. A genotype-disease meta-analysis with no exposure instrumented; Amendment 5 names this family as a known failure of the MR-instrumented rule.
- **Outcome codebook:** program fluoxetine (Prozac NDA 018936) coded as the first SSRI approved for MDD; the manuscript names fluoxetine, sertraline and escitalopram (class); phase III; engagement yes; efficacy met; safety acceptable; decision advanced; regulatory approved FDA 1987 (Prozac NDA018936 original approval 1987-12-29); attribution uncertain. Sources: FDA:NDA018936; PMID:29477251; DOI:10.1016/S0140-6736(17)32802-7; PMID:15121647; DOI:10.1176/appi.ajp.161.5.826. Notes: Class family coded on fluoxetine, the earliest approval. Pre-registration-era program: the label states efficacy for MDD was established in 7 short-term and 2 long-term placebo-controlled trials; individual pivotal-trial PMIDs are not cited. Post-marketing confirmation: Cipriani 2018 network meta-analysis (all 21 antidepressants more effective than placebo; fluoxetine among the least efficacious in head-to-head trials). Target engagement: label section 12.2 (fluoxetine blocks platelet serotonin uptake at clinical doses) and Meyer 2004 PET (about 80% striatal 5-HTT occupancy at minimum therapeutic doses; added source). Attribution uncertain: efficacy is established but the mechanism through which SSRIs act is contested (manuscript's mechanism-bypass reading; Moncrieff 2022).
- **MR state:** inconclusive (signed d 0.0163 / 0.0424 / 0.0625; scale-unresolved True; alignment aligned)
- **In analysis sets:** registered, strict Phase III, Amyloid-AD scored, strict Phase III + Amyloid-AD, registration-consistent instrument, unique-evidence, source-extracted OBS (classifier flags)
