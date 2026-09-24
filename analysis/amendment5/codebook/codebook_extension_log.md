# Codebook extension log: 14 extension families (Amendment 5, Procedure 3)

Companion to `codebook_extension.csv`. Families: every row of
`data/cross_design_classification_all_41_families_v3.csv` whose `domain` is oncology,
respiratory, metabolic, psychiatry, gastroenterology, ophthalmology or musculoskeletal.
The registered `drug_outcome` column was not changed or re-judged.

Coded 2026-09-22 by a single coder. Sources were retrieved through PubMed E-utilities
(esearch/efetch, no email or key), ClinicalTrials.gov API v2 (`/api/v2/studies/{NCT}`),
and openFDA (`drug/label` and `drug/drugsfda`, no key). Quoted sentences are from PubMed
abstracts, ClinicalTrials.gov registry fields, or FDA label sections as marked. Where a
field is coded from a source whose sentence could not be retrieved through these
endpoints, the entry says so.

Conventions: `trial_phase` is the phase of the readout on which `drug_outcome` was coded.
`regulatory_jurisdiction_year` is FDA only; the EMA was not queried. Efficacy-supplement
numbers from Drugs@FDA are matched to indications by approval date, and the supplement
text was not read; each such match is marked "by date".

---

## VitD-Cancer (oncology)

Program coded: vitamin D3 2000 IU/day, VITAL (NCT01169259). Prevention trial; academic
sponsor (Brigham and Women's Hospital).

Sources consulted
- PMID:30415629 / DOI:10.1056/NEJMoa1809944 — Manson et al. 2019, N Engl J Med (manuscript's cited source).
- NCT:NCT01169259 — ClinicalTrials.gov: `phases: ['PHASE3']`; primary outcomes "Number of Participants With Invasive Cancer of Any Type" and "Number of Participants With a Major Cardiovascular Event".

Field support
- trial_phase = III: registry `phases: ['PHASE3']`.
- target_engagement = yes: the rise in serum 25(OH)D in the vitamin D arm is reported in the Results of the full text, not in the abstract. Not verified through E-utilities; the value rests on the coder's reading of the paper and should be checked against the full text before the supplement is finalized.
- efficacy_endpoint = not met: "Supplementation with vitamin D was not associated with a lower risk of either of the primary end points. During a median follow-up of 5.3 years, cancer was diagnosed in 1617 participants (793 in the vitamin D group and 824 in the placebo group; hazard ratio, 0.96; 95% confidence interval [CI], 0.88 to 1.06; P=0.47)." Family indication (colorectal cancer) was a secondary endpoint: "for colorectal cancer, 1.09 (95% CI, 0.73 to 1.62)".
- safety_outcome = acceptable: "No excess risks of hypercalcemia or other adverse events were identified."
- development_decision = not reported: no sponsor development program exists for a supplement in a prevention trial; there is no sponsor action to code.
- regulatory_outcome = not submitted: no application exists for vitamin D in colorectal cancer prevention (Amendment 1: "FDA has not approved vitamin D supplementation for colorectal cancer prevention").
- outcome_attribution = target (reading): the null RCT sits beside the null MR estimate for the same exposure.

## IGF1-CRC (oncology)

Programs coded: figitumumab (Pfizer) and ganitumab (Amgen/NCI), as named in the manuscript and Amendment 1.

Sources consulted
- PMID:24888810 / DOI:10.1200/JCO.2013.54.4932 — Langer et al. 2014, J Clin Oncol, figitumumab NSCLC (cited).
- NCT:NCT00596830 — registry: `PHASE3`, `TERMINATED`, primary "Overall Survival (OS)".
- PMID:36669140 / DOI:10.1200/JCO.22.01815 — DuBois et al. 2023, J Clin Oncol, ganitumab Ewing sarcoma (cited as juergens2023ganitumab).
- NCT:NCT02306161 — registry: `PHASE3`, primary "Event-free Survival".
- NCT:NCT01231347 — registry: QUILT-2.014 ganitumab plus gemcitabine, metastatic pancreatic adenocarcinoma, `PHASE3`, `COMPLETED`, primary overall survival.

Field support
- trial_phase = III: registry `PHASE3` for all three trials. None is in colorectal cancer; see the CSV note on the indication mismatch. Under a strict reading of "for the family's exact indication" the field would be `not reported`.
- target_engagement = not reported: neither abstract reports a pharmacodynamic or biomarker measure of IGF-1R modulation.
- efficacy_endpoint = not met: figitumumab, "Median OS was 8.6 months for figitumumab plus chemotherapy and 9.8 months for chemotherapy alone (hazard ratio [HR], 1.18; 95% CI, 0.99 to 1.40; P = .06)"; ganitumab, "stratified EFS-event hazard ratio for experimental arm 1.00; 95% CI, 0.76 to 1.33; 1-sided, P = .50".
- safety_outcome = limiting: "The study was closed early by an independent Data Safety Monitoring Committee because of futility and an increased incidence of serious adverse events (SAEs) and treatment-related deaths with figitumumab." Ganitumab: "The addition of ganitumab may be associated with increased toxicity."
- development_decision = discontinued: "Further clinical development of figitumumab is not being pursued."
- regulatory_outcome = not submitted: Amendment 1, "No IGF-1R inhibitor has received FDA approval for CRC or any solid tumor"; no application located.
- outcome_attribution = indication (reading): the programs were never tested in the family's indication; the manuscript's translation-gap class rests on an engagement measure the sources do not report.

## Estrogen-BC (oncology)

Program coded: tamoxifen, NSABP P-1 (Breast Cancer Prevention Trial); Nolvadex NDA 017970.

Sources consulted
- PMID:9747868 / DOI:10.1093/jnci/90.18.1371 — Fisher et al. 1998, J Natl Cancer Inst (added: the pivotal risk-reduction trial).
- PMID:23639488 / DOI:10.1016/S0140-6736(13)60140-3 — Cuzick et al. 2013, Lancet (manuscript's cited source, bib key cuzick2015tamoxifen).
- FDA:NDA017970 — Drugs@FDA: ORIG approved 1977-12-30; efficacy supplements 39 and 40 approved 1998-10-29 (matched to the risk-reduction indication by date).
- FDA:NDA021807 — Soltamox label, section 14.4: "The Breast Cancer Prevention Trial (NSABP P-1) was a double-blind, randomized, placebo-controlled trial with a primary objective to determine whether 5 years of another formulation of tamoxifen therapy (20 mg per day) reduced the incidence of invasive breast cancer in women at high risk for the disease."

Field support
- trial_phase = III: P-1 randomized 13,388 women; the label lists it as the basis of indication 1.4.
- target_engagement = yes: "Tamoxifen reduced the occurrence of estrogen receptor-positive tumors by 69%, but no difference in the occurrence of estrogen receptor-negative tumors was seen."
- efficacy_endpoint = met: "Tamoxifen reduced the risk of invasive breast cancer by 49% (two-sided P<.00001)". Cuzick 2013: "Overall, we noted a 38% reduction (hazard ratio [HR] 0·62, 95% CI 0·56-0·69) in breast cancer incidence".
- safety_outcome = acceptable: "The rate of endometrial cancer was increased in the tamoxifen group (risk ratio = 2.53; 95% confidence interval = 1.35-4.97)"; "The rates of stroke, pulmonary embolism, and deep-vein thrombosis were elevated in the tamoxifen group"; approved with a boxed warning (Soltamox label).
- development_decision = advanced; regulatory_outcome = approved; FDA 1998 (supplements 39/40, 1998-10-29, by date).
- outcome_attribution = target (reading).

## Eos/IL5-Asthma (respiratory)

Program coded: mepolizumab, Nucala BLA 125526. MENSA is the Phase III readout; DREAM, which the manuscript cites, is Phase 2 on the registry.

Sources consulted
- PMID:25199059 / DOI:10.1056/NEJMoa1403290 — Ortega et al. 2014, N Engl J Med, MENSA (added).
- NCT:NCT01691521 — registry: `PHASE3`, primary "Number of Clinically Significant Exacerbations of Asthma Per Year".
- PMID:22901886 / DOI:10.1016/S0140-6736(12)60988-X — Pavord et al. 2012, Lancet, DREAM (cited).
- NCT:NCT01000506 — registry: `PHASE2`, "Dose Ranging Efficacy And Safety With Mepolizumab in Severe Asthma".
- FDA:BLA125526 — Drugs@FDA ORIG approved 2015-11-04; label section 12.2.

Field support
- trial_phase = III: MENSA registry `PHASE3`. Note: DREAM (cited) is `PHASE2`.
- target_engagement = yes: label 12.2, "Compared with baseline levels, blood eosinophils decreased in a dose-dependent manner ... the observed geometric mean reduction from baseline in blood eosinophils was 64%, 78%, 84%, and 90%".
- efficacy_endpoint = met: MENSA, "The rate of exacerbations was reduced by 47% (95% confidence interval [CI], 29 to 61) among patients receiving intravenous mepolizumab and by 53% (95% CI, 37 to 65) among those receiving subcutaneous mepolizumab, as compared with those receiving placebo (P<0.001 for both comparisons)."
- safety_outcome = acceptable: "The safety profile of mepolizumab was similar to that of placebo."
- development_decision = advanced; regulatory_outcome = approved; FDA 2015. Label indication 1.1: "severe asthma and with an eosinophilic phenotype".
- outcome_attribution = target (reading).

## IL4Ra-Asthma (respiratory)

Program coded: dupilumab, Dupixent BLA 761055, LIBERTY ASTHMA QUEST.

Sources consulted
- PMID:29782217 / DOI:10.1056/NEJMoa1804092 — Castro et al. 2018, N Engl J Med (the QUEST results paper; the manuscript's bib key busse2019dupilumab resolves to the QUEST design paper in Adv Ther, DOI:10.1007/s12325-018-0702-4).
- NCT:NCT02414854 — registry: `PHASE3`; primary outcomes annualized severe exacerbation rate and FEV1 change at week 12.
- FDA:BLA761055 — Drugs@FDA ORIG 2017-03-28 (atopic dermatitis); efficacy supplement 7 approved 2018-10-19 (asthma, by date); label sections 1.2 and 12.2.

Field support
- trial_phase = III: registry `PHASE3`.
- target_engagement = yes: label 12.2, "In asthma subjects, fractional exhaled nitric oxide (FeNO) and circulating concentrations of eotaxin-3, total IgE, allergen specific IgE, TARC, and periostin were decreased relative to placebo."
- efficacy_endpoint = met: "The annualized rate of severe asthma exacerbations was 0.46 ... among patients assigned to 200 mg of dupilumab every 2 weeks and 0.87 ... among those assigned to a matched placebo, for a 47.7% lower rate with dupilumab than with placebo (P<0.001)"; "At week 12, the FEV1 had increased by 0.32 liters ... (difference vs. matched placebo, 0.14 liters; P<0.001)".
- safety_outcome = acceptable: "Blood eosinophilia occurred after the start of the intervention in 52 patients (4.1%) who received dupilumab as compared with 4 patients (0.6%) who received placebo."; approved.
- development_decision = advanced; regulatory_outcome = approved; FDA 2018. Label 1.2: "moderate-to-severe asthma characterized by an eosinophilic phenotype or with oral corticosteroid dependent asthma".
- outcome_attribution = target (reading).
- Registered drug_outcome is Construct-limited (an exclusion status); the coded fields read approved.

## TSLP-Asthma (respiratory)

Program coded: tezepelumab, Tezspire BLA 761224, NAVIGATOR.

Sources consulted
- PMID:33979488 / DOI:10.1056/NEJMoa2034975 — Menzies-Gow et al. 2021, N Engl J Med (cited).
- NCT:NCT03347279 — registry: `PHASE3`; primary "Annual Asthma Exacerbation Rate".
- FDA:BLA761224 — Drugs@FDA ORIG approved 2021-12-17; label sections 1.1 and 12.2.

Field support
- trial_phase = III: registry `PHASE3`; abstract "We conducted a phase 3, multicenter, randomized, double-blind, placebo-controlled trial."
- target_engagement = yes: label 12.2, "In NAVIGATOR, administration of TEZSPIRE 210 mg subcutaneously every 4 weeks (n=528) reduced blood eosinophils counts, FeNO, IL-5 concentration and IL-13 concentration from baseline compared with placebo (n=531)".
- efficacy_endpoint = met: "The annualized rate of asthma exacerbations was 0.93 ... with tezepelumab and 2.10 ... with placebo (rate ratio, 0.44; 95% CI, 0.37 to 0.53; P<0.001)."
- safety_outcome = acceptable: "The frequencies and types of adverse events did not differ meaningfully between the two groups."
- development_decision = advanced; regulatory_outcome = approved; FDA 2021. Label 1.1: "severe asthma" without a biomarker restriction.
- outcome_attribution = target (reading).
- Registered drug_outcome is Construct-limited; the coded fields read approved.

## SGLT2-HF (metabolic)

Programs coded: dapagliflozin (Farxiga NDA 202293, DAPA-HF) and empagliflozin (Jardiance NDA 204629, EMPEROR-Reduced).

Sources consulted
- PMID:31535829 / DOI:10.1056/NEJMoa1911303 — McMurray et al. 2019, N Engl J Med, DAPA-HF (added; the manuscript's drug sentence carries no trial citation).
- NCT:NCT03036124 — registry: `PHASE3`.
- PMID:32865377 / DOI:10.1056/NEJMoa2022190 — Packer et al. 2020, N Engl J Med, EMPEROR-Reduced (added).
- NCT:NCT03057977 — registry: `PHASE3`.
- FDA:NDA202293 — Drugs@FDA efficacy supplement 20 approved 2020-05-05 (HFrEF, by date); supplement 26 approved 2023-05-08 (HF across EF, by date); label 12.2.
- FDA:NDA204629 — Drugs@FDA efficacy supplement 26 approved 2021-08-18 (HFrEF, by date); supplement 33 approved 2022-02-24 (HF across EF, by date); label 12.2.

Field support
- trial_phase = III: DAPA-HF abstract "In this phase 3, placebo-controlled trial"; both registry records `PHASE3`.
- target_engagement = yes, from the labels rather than the HF trials: Farxiga 12.2, "Dapagliflozin doses of 5 or 10 mg per day in patients with type 2 diabetes mellitus for 12 weeks resulted in excretion of approximately 70 grams of glucose in the urine per day at Week 12"; Jardiance 12.2, "urinary glucose excretion increased immediately following a dose of empagliflozin". The HF trials report no SGLT2 pharmacodynamic marker; DAPA-HF: "possibly through glucose-independent mechanisms".
- efficacy_endpoint = met: DAPA-HF "hazard ratio, 0.74; 95% confidence interval [CI], 0.65 to 0.85; P<0.001"; EMPEROR-Reduced "hazard ratio for cardiovascular death or hospitalization for heart failure, 0.75; 95% confidence interval [CI], 0.65 to 0.86; P<0.001".
- safety_outcome = acceptable: DAPA-HF "The frequency of adverse events related to volume depletion, renal dysfunction, and hypoglycemia did not differ between treatment groups."; EMPEROR-Reduced "Uncomplicated genital tract infection was reported more frequently with empagliflozin."
- development_decision = advanced; regulatory_outcome = approved; FDA 2020 (dapagliflozin) and 2021 (empagliflozin). Jardiance label: "to reduce the risk of cardiovascular death and hospitalization for heart failure in adults with heart failure."
- outcome_attribution = target (reading).

## GLP1R-T2D/Obesity (metabolic)

Program coded: semaglutide (Ozempic NDA 209637 for type 2 diabetes; Wegovy NDA 215256 for obesity), the manuscript's first-named agent. Liraglutide not coded.

Sources consulted
- PMID:33567185 / DOI:10.1056/NEJMoa2032183 — Wilding et al. 2021, N Engl J Med, STEP 1 (added).
- NCT:NCT03548935 — registry: `PHASE3`; coprimary body-weight endpoints.
- PMID:27633186 / DOI:10.1056/NEJMoa1607141 — Marso et al. 2016, N Engl J Med, SUSTAIN-6 (added).
- NCT:NCT01720446 — registry: `PHASE3`; primary MACE.
- FDA:NDA209637 — Drugs@FDA ORIG approved 2017-12-05; Ozempic label 12.2.
- FDA:NDA215256 — Drugs@FDA ORIG approved 2021-06-04; Wegovy label 12.2 and boxed warning.

Field support
- trial_phase = III: both registry records `PHASE3`.
- target_engagement = yes: Ozempic label 12.2, "treatment with semaglutide 1 mg resulted in reductions in glucose in terms of absolute change from baseline and relative reduction compared to placebo of 29 mg/dL (22%) for fasting glucose, 74 mg/dL (36%) for 2-hour postprandial glucose"; Wegovy 12.2, "Semaglutide decreases calorie intake. ... Semaglutide delays gastric emptying."
- efficacy_endpoint = met: STEP 1, "The mean change in body weight from baseline to week 68 was -14.9% in the semaglutide group as compared with -2.4% with placebo, for an estimated treatment difference of -12.4 percentage points (95% confidence interval [CI], -13.4 to -11.5; P<0.001)"; SUSTAIN-6, "hazard ratio, 0.74; 95% confidence interval [CI], 0.58 to 0.95; P<0.001 for noninferiority".
- safety_outcome = acceptable: STEP 1, "Nausea and diarrhea were the most common adverse events with semaglutide; they were typically transient and mild-to-moderate in severity"; Wegovy boxed warning concerns rodent thyroid C-cell tumors.
- development_decision = advanced; regulatory_outcome = approved; FDA 2017 (T2D) and 2021 (obesity).
- outcome_attribution = target (reading).
- Registered drug_outcome is Construct-limited; the coded fields read approved.

## Urate-Gout (metabolic)

Program coded: febuxostat (Uloric NDA 021856; FACT, CONFIRMS, CARES), the manuscript's second-named agent and the one with a modern trial record. Allopurinol (Zyloprim NDA 016084) is the first-named agent; its 1966 approval predates registered trials.

Sources consulted
- PMID:16339094 / DOI:10.1056/NEJMoa050373 — Becker et al. 2005, N Engl J Med, FACT (added).
- PMID:20370912 / DOI:10.1186/ar2978 — Becker et al. 2010, Arthritis Res Ther, CONFIRMS (added).
- NCT:NCT00430248 — registry: `PHASE3`; primary "Percentage of Subjects Whose Serum Urate Level is <6.0 Milligrams Per Deciliter (mg/dL) at the Final Visit."
- PMID:29527974 / DOI:10.1056/NEJMoa1710895 — White et al. 2018, N Engl J Med, CARES (added, post-marketing safety).
- NCT:NCT01101035 — registry: `PHASE3`, CARES.
- FDA:NDA021856 — Drugs@FDA ORIG approved 2009-02-13; efficacy supplement 13 approved 2019-02-21 (label restriction, by date); label boxed warning and 12.2.
- FDA:NDA016084 — Drugs@FDA ORIG approved 1966-08-19.

Field support
- trial_phase = III: CONFIRMS registry `PHASE3`; FACT randomized 762 patients.
- target_engagement = yes: label 12.2, "Percent reduction in 24-hour mean serum uric acid concentrations was between 40% and 55% at the exposure levels of 40 mg and 80 mg daily doses."
- efficacy_endpoint = met: FACT, "The primary end point was reached in 53 percent of patients receiving 80 mg of febuxostat, 62 percent of those receiving 120 mg of febuxostat, and 21 percent of those receiving allopurinol (P<0.001 ...)". The primary endpoint is serum urate, a biomarker; gout flares: "the overall incidence during weeks 9 through 52 was similar in all groups".
- safety_outcome = acceptable at approval; post-marketing CARES: "All-cause mortality and cardiovascular mortality were higher with febuxostat than with allopurinol (hazard ratio for death from any cause, 1.22 [95% CI, 1.01 to 1.47]; hazard ratio for cardiovascular death, 1.34 [95% CI, 1.03 to 1.73])." Label boxed warning: "Gout patients with established cardiovascular (CV) disease treated with ULORIC had a higher rate of CV death compared to those treated with allopurinol".
- development_decision = advanced; regulatory_outcome = approved; FDA 2009 (febuxostat), FDA 1966 (allopurinol).
- outcome_attribution = target (reading).

## IL6-MDD (psychiatry)

Program coded: sirukumab 50 mg SC adjunctive, Janssen, NCT02473289. Amendment 2 codes the outcome on "Boyle et al. 2020, Mol Psychiatry".

Sources consulted
- NCT:NCT02473289 — registry with posted results: `phases: ['PHASE2']`, `overallStatus: COMPLETED`, enrollment 193 actual, arms sirukumab 50 mg (94) and placebo (99); primary "Change From Baseline in Hamilton Depression Rating Scale (HDRS-17) Total Score at Week 12".
- PubMed searches that returned no matching trial paper: `sirukumab[tiab] AND depress*[tiab] AND randomized`; `sirukumab[tiab] AND (depressive[tiab] OR depression[tiab]) AND placebo[tiab]`; `sirukumab[tiab] AND (depression[tiab] OR depressive[tiab])` (4 hits, all post hoc analyses or reviews: PMID 28676350, 27913990, 27713619, 38959503); `Salvadore G[au] AND sirukumab`; `Boyle CC[au] AND 2020[dp] AND Mol Psychiatry[ta]`; `NCT02473289[si]`; `NCT02473289[All Fields]`. The manuscript has no bib entry for the trial (grep of paper/references.bib for "sirukumab" and "boyle" returns nothing).
- ClinicalTrials.gov search `sirukumab AND (depression OR depressive)`: the only depression trial is NCT02473289.

Field support
- trial_phase = II: registry `PHASE2`.
- target_engagement = not reported: the registry lists no pharmacodynamic outcome (no CRP or IL-6 measure among the nine posted outcomes).
- efficacy_endpoint = not met: registry results, HDRS-17 change at week 12, placebo -10.6 (SE 1.43) vs sirukumab -11.4 (SE 1.52); "Difference of Least Square (LS) Means -0.8", 95% CI -2.77 to 1.10, p = 0.310. Remission 19.0% vs 15.9%; response 33.3% vs 34.1%.
- safety_outcome = acceptable: registry adverse events, serious 3/94 (sirukumab) vs 2/99 (placebo), deaths 0/0.
- development_decision = discontinued: inferred from the absence of any later sirukumab depression trial on the registry; no sponsor statement located.
- regulatory_outcome = not submitted: no application for MDD (Amendment 2: "No anti-IL-6 or anti-IL-6R agent has received FDA approval for any psychiatric indication").
- outcome_attribution = uncertain (reading).
- Contradiction with the registration: Amendment 2 says "The trial was terminated early for futility"; the registry records COMPLETED with 169 of 193 completing.

## Serotonin-MDD (psychiatry)

Program coded: fluoxetine, Prozac NDA 018936, the first SSRI approved for MDD. The manuscript names fluoxetine, sertraline and escitalopram (class).

Sources consulted
- FDA:NDA018936 — Drugs@FDA ORIG approved 1987-12-29; label sections 12.1, 12.2, 14.
- PMID:29477251 / DOI:10.1016/S0140-6736(17)32802-7 — Cipriani et al. 2018, Lancet (cited in Amendment 2).
- PMID:15121647 / DOI:10.1176/appi.ajp.161.5.826 — Meyer et al. 2004, Am J Psychiatry (added, for target engagement).

Field support
- trial_phase = III: label section 14, "Efficacy for PROZAC was established for the: Acute and maintenance treatment of Major Depressive Disorder in adults, and children and adolescents (8 to 18 years) in 7 short-term and 2 long-term, placebo-controlled trials". Pre-registration era; individual trial identifiers not available.
- target_engagement = yes: label 12.2, "Studies at clinically relevant doses in man have demonstrated that fluoxetine blocks the uptake of serotonin into human platelets."; Meyer 2004, "Occupancy of 80% across five SSRIs occurs at minimum therapeutic doses."
- efficacy_endpoint = met: Cipriani 2018, "all antidepressants were more effective than placebo, with ORs ranging between 2·13 ... for amitriptyline and 1·37 ... for reboxetine"; also "fluoxetine, fluvoxamine, reboxetine, and trazodone were the least efficacious drugs" in head-to-head trials.
- safety_outcome = acceptable: approved; boxed warning for suicidality in patients under 25 added post-marketing.
- development_decision = advanced; regulatory_outcome = approved; FDA 1987.
- outcome_attribution = uncertain (reading): label 12.1, "Although the exact mechanism of PROZAC is unknown, it is presumed to be linked to its inhibition of CNS neuronal uptake of serotonin."

## IL23-Crohns (gastroenterology)

Program coded: risankizumab, Skyrizi BLA 761105; ADVANCE, MOTIVATE (induction), FORTIFY (maintenance).

Sources consulted
- PMID:35644154 / DOI:10.1016/S0140-6736(22)00467-6 — D'Haens et al. 2022, Lancet (added).
- NCT:NCT03105128, NCT:NCT03104413 — registry: `PHASE3`; coprimary CDAI clinical remission and endoscopic response at week 12.
- PMID:35644155 / DOI:10.1016/S0140-6736(22)00466-4 — Ferrante et al. 2022, Lancet, FORTIFY (added).
- NCT:NCT03105102 — registry: `PHASE3`.
- FDA:BLA761105 — Drugs@FDA ORIG 2019-04-23 (psoriasis); efficacy supplement 16 approved 2022-06-16 (Crohn's disease, by date); label 1.3 and 12.2.

Field support
- trial_phase = III: "ADVANCE and MOTIVATE were randomised, double-masked, placebo-controlled, phase 3 induction studies."
- target_engagement = yes: FORTIFY, "Results for more stringent endoscopic and composite endpoints and inflammatory biomarkers were consistent with a dose-response relationship." Label 12.2 states "No formal pharmacodynamics studies have been conducted with risankizumab-rzaa."
- efficacy_endpoint = met: "All coprimary endpoints at week 12 were met in both trials with both doses of risankizumab (p values ≤0·0001)."
- safety_outcome = acceptable: "The overall incidence of treatment-emergent adverse events was similar among the treatment groups in both trials."
- development_decision = advanced; regulatory_outcome = approved; FDA 2022. Label 1.3: "moderately to severely active Crohn's disease in adults".
- outcome_attribution = target (reading).
- Registered drug_outcome is Construct-limited; the coded fields read approved.

## Complement-GA (ophthalmology)

Program coded: lampalizumab (Roche), CHROMA and SPECTRI, as registered. Later same-indication approvals recorded: pegcetacoplan (Syfovre NDA 217171) and avacincaptad pegol (Izervay NDA 217225).

Sources consulted
- PMID:29801123 / DOI:10.1001/jamaophthalmol.2018.1544 — Holz et al. 2018, JAMA Ophthalmol (added; the manuscript names the trials without a citation).
- NCT:NCT02247479, NCT:NCT02247531 — registry: `PHASE3`, `TERMINATED` (whyStopped blank), primary "Change From Baseline in Geographic Atrophy (GA) Area, as Assessed by Fundus Autofluoresence (FAF) at Week 48".
- PMID:37865470 / DOI:10.1016/S0140-6736(23)01520-9 — Heier et al. 2023, Lancet, OAKS and DERBY (added).
- NCT:NCT03525613, NCT:NCT03525600 — registry: `PHASE3`, `COMPLETED`.
- PMID:37696275 / DOI:10.1016/S0140-6736(23)01583-0 — Khanani et al. 2023, Lancet, GATHER2 (added).
- NCT:NCT04435366 — registry: `PHASE3`, `COMPLETED`.
- FDA:NDA217171 — Drugs@FDA ORIG approved 2023-02-17; label 1: "SYFOVRE is indicated for the treatment of geographic atrophy (GA) secondary to age-related macular degeneration (AMD)."
- FDA:NDA217225 — Drugs@FDA ORIG approved 2023-08-04 (Astellas, Izervay).

Field support
- trial_phase = III: "Two identically designed phase 3 double-masked, randomized, sham-controlled clinical trials, Chroma and Spectri".
- target_engagement = not reported: neither the abstract nor the registry reports an ocular pharmacodynamic measure of factor D inhibition. The manuscript's Table of boundary criteria says of this class "the trial reports target engagement without endpoint benefit"; the sources coded do not carry that sentence.
- efficacy_endpoint = not met: "Differences in adjusted mean change in GA lesion area (lampalizumab minus sham) were -0.02 mm2 (95% CI, -0.21 to 0.16 mm2; P = .80) for lampalizumab every 4 weeks in Chroma, 0.16 mm2 (95% CI, 0.00-0.31 mm2; P = .048) for lampalizumab every 4 weeks in Spectri, 0.05 mm2 ... in Chroma, and 0.09 mm2 ... in Spectri."; "lampalizumab did not reduce GA enlargement vs sham during 48 weeks of treatment."
- safety_outcome = acceptable: "Endophthalmitis occurred after 5 of 12 447 injections (0.04%) or in 5 of 1252 treated participants (0.4%) through week 48."
- development_decision = discontinued: both registry records `TERMINATED`.
- regulatory_outcome = not submitted (lampalizumab). Later approvals for the same indication: pegcetacoplan, "the first treatment approved by the US Food and Drug Administration for geographic atrophy", OAKS monthly "significantly slowed geographic atrophy lesion growth by 21% ... p=0·0004" at 12 months while DERBY "did not reach significance" at 12 months and both met at 24 months; avacincaptad pegol, "a difference in growth of 0·056 mm/year (95% CI 0·016-0·096; p=0·0064), representing a 14% difference".
- outcome_attribution = uncertain (reading): target node versus molecule cannot be separated from the record.

## Sclerostin-Fracture (musculoskeletal)

Program coded: romosozumab, Evenity BLA 761062; FRAME and ARCH.

Sources consulted
- PMID:27641143 / DOI:10.1056/NEJMoa1607948 — Cosman et al. 2016, N Engl J Med, FRAME (added).
- NCT:NCT01575834 — registry: `PHASE3`; primary new vertebral fracture at 12 and 24 months.
- PMID:28892457 / DOI:10.1056/NEJMoa1708322 — Saag et al. 2017, N Engl J Med, ARCH (the manuscript cites "ARCH trial" without a key).
- NCT:NCT01631214 — registry: `PHASE3`.
- FDA:BLA761062 — Drugs@FDA ORIG approved 2019-04-09; label boxed warning, 1.1, 12.2, 14.1 ("Study 1 (NCT01575834)").

Field support
- trial_phase = III: both registry records `PHASE3`.
- target_engagement = yes: label 12.2, "EVENITY increased the bone formation marker procollagen type 1 N-telopeptide (P1NP) with a peak increase from baseline of approximately 145% compared to placebo 2 weeks after initiating treatment" and "decreased the bone resorption marker type 1 collagen C-telopeptide (CTX) with a maximal reduction from baseline of approximately 55% compared to placebo".
- efficacy_endpoint = met: FRAME, "new vertebral fractures had occurred in 16 of 3321 patients (0.5%) in the romosozumab group, as compared with 59 of 3322 (1.8%) in the placebo group (representing a 73% lower risk with romosozumab; P<0.001)"; ARCH, "a 48% lower risk of new vertebral fractures was observed in the romosozumab-to-alendronate group ... (P<0.001)" and "a 27% lower risk" of clinical fracture.
- safety_outcome = acceptable: ARCH, "During year 1, positively adjudicated serious cardiovascular adverse events were observed more often with romosozumab than with alendronate (50 of 2040 patients [2.5%] vs. 38 of 2014 patients [1.9%])."; label boxed warning "EVENITY may increase the risk of myocardial infarction, stroke, and cardiovascular death"; approved with a 12-dose limit.
- development_decision = advanced; regulatory_outcome = approved; FDA 2019. Label 1.1: "osteoporosis in postmenopausal women at high risk for fracture".
- outcome_attribution = target (reading).

---

## Summary flags

- `not reported` fields: VitD-Cancer (development_decision); IGF1-CRC (target_engagement); IL6-MDD (target_engagement); Complement-GA (target_engagement).
- trial_phase not III or post-marketing: IL6-MDD (II). IGF1-CRC is III in indications other than the family's; see its entry.
- Coded fields differ in value from the registered `drug_outcome`: IL4Ra-Asthma, TSLP-Asthma, GLP1R-T2D/Obesity, IL23-Crohns (registered Construct-limited, an exclusion status; the record reads approved). No family coded Failed or Approved in the registered column reads the other way in the trial or regulatory record.
- Source discrepancies found while coding: IL6-MDD (registration's cited paper not locatable; "terminated early for futility" contradicted by the registry); Eos/IL5-Asthma (the cited DREAM trial is Phase 2 on the registry; MENSA is the Phase III readout); Complement-GA (the manuscript's criterion sentence on reported target engagement is unsupported by the sources coded); IGF1-CRC (no Phase III in the family's indication).
