# Amendment 5, Procedure 3: coding log for the neuro and cardio families

Date of lookups: 2026-09-22. Companion file: `codebook_neuro_cardio.csv` (19 rows).

Sources were located with PubMed E-utilities (esearch, esummary, efetch) and the
ClinicalTrials.gov API v2, with no email, key, or user-agent added to any request.
Quoted sentences are from PubMed abstracts or ClinicalTrials.gov records unless the
entry says otherwise. Every number in this file is quoted from the cited source or from
the manuscript; none is computed here. Full texts were not consulted; where a field needs the full
text, the field is `not reported` and the reason is given. The registered
`drug_outcome` column of `data/cross_design_classification_all_41_families_v3.csv`
was not changed.

Program identification followed the manuscript (`paper/paper_v25_round3.tex`) and
`analysis/classifier/classify_families.py`. The classifier carries no drug names for
the neuro or cardio families, so the manuscript is the only in-repo source of program
names. Four neuro families (ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS) have no program
named anywhere in the repository; Blood pressure and Triglycerides are named only as
"approved drug classes".

---

## Neuro

### Metabolic-AD (registered: Failed)

Sources consulted:
- PMID 41865758, DOI 10.1016/S0140-6736(26)00459-9, Cummings et al., Lancet 2026, evoke and evoke+ (NCT04777396, NCT04777409).
- PMID 34146512, DOI 10.1016/S1474-4422(21)00043-0, Burns et al., Lancet Neurol 2021, TOMMORROW (NCT01931566).
- ClinicalTrials.gov records NCT04777396, NCT04777409 (both PHASE3, COMPLETED, primary completion September 2025) and NCT01931566 (PHASE3, TERMINATED).

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "evoke and evoke+ were multicentre, randomised, double-blind, placebo-controlled phase 3 trials" (PMID 41865758); "In this phase 3, multicentre, randomised, double-blind, placebo-controlled, parallel-group study" (PMID 34146512) |
| target_engagement | unclear | Neither abstract reports a pharmacodynamic marker of GLP-1R or PPAR-gamma engagement in AD. The repository holdout note "despite biomarker improvements" (`data/phase3_holdout_dataset.csv`) has no source. |
| efficacy_endpoint | not met | "estimated difference -0.08 [95% CI -0.35 to 0.20], p=0.57 in evoke and 0.10 [-0.17 to 0.38], p=0.46 in evoke+" (PMID 41865758); "hazard ratio 0.80, 99% CI 0.45-1.40; p=0.307 ... Pioglitazone did not delay the onset of mild cognitive impairment" (PMID 34146512) |
| safety_outcome | acceptable | "Safety and tolerability of semaglutide in early Alzheimer's disease is consistent with studies in other indications" (PMID 41865758); "Lack of efficacy of the drug; no safety concern" (NCT01931566, whyStopped) |
| development_decision | discontinued | "both trials have been discontinued due to negative clinical outcome" (PMID 41865758); "The study was terminated in January, 2018, after failing to meet the non-futility threshold" (PMID 34146512) |
| regulatory_outcome | not submitted | No AD submission for either drug is recorded in any source consulted. |
| outcome_attribution | target | Single-coder reading: two molecules with different mechanisms both null on the family's pathway. |

### ModRisk-AD (registered: Failed)

Sources consulted: `paper/paper_v25_round3.tex` (Tables `tab:drugs_stage1`, `tab:stage2`), `analysis/classifier/classify_families.py`, `paper/supplementary_data.csv`, `data/effect_sizes_v12.csv`, `docs/NEURO_PAPER_DRAFT_V3.md`.

All seven fields `not reported`. The manuscript maps no holdout drug to this family
(`tab:drugs_stage1` lists Metabolic-AD, HRT-AD, Anti-CD20-MS, Vitamin D-MS only;
`tab:stage2` gives RCT d "---"). The supplementary source column reads "MR of
modifiable risk factors" and "Observational cohorts". No program, trial, or
regulatory record exists to code against. The registered Failed cannot be traced to
a readout.

### Anti-CD20-MS (registered: Approved)

Sources consulted:
- PMID 28002679, DOI 10.1056/NEJMoa1601277, Hauser et al., NEJM 2017, OPERA I/II (NCT01247324, NCT01412333).
- PMID 28002688, DOI 10.1056/NEJMoa1606468, Montalban et al., NEJM 2017, ORATORIO (NCT01194570).
- PMID 32757523, DOI 10.1056/NEJMoa1917246, Hauser et al., NEJM 2020, ASCLEPIOS I/II (NCT02792218, NCT02792231).
- PMID 36001711, DOI 10.1056/NEJMoa2201904, Steinman et al., NEJM 2022, ULTIMATE I/II (NCT03277261, NCT03277248).
- PMID 28523586, Frampton, Drugs 2017, "Ocrelizumab: First Global Approval".
- PMID 37556938, Coyle et al., Mult Scler Relat Disord 2023 (ofatumumab post-FDA-approval use).
- PMID 36920653, Lee, Drugs 2023, "Ublituximab: First Approval".
- ClinicalTrials.gov: all six NCT records PHASE3, COMPLETED, results posted.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "In two identical phase 3 trials" (PMID 28002679); "In this phase 3 trial" (PMID 28002688); "In two double-blind, double-dummy, phase 3 trials" (PMID 32757523); "In two identical, phase 3, double-blind, double-dummy trials" (PMID 36001711) |
| target_engagement | yes | "Ocrelizumab is a humanized monoclonal antibody that selectively depletes CD20+ B cells" (PMID 28002679); "The monoclonal antibody ublituximab enhances antibody-dependent cellular cytolysis and produces B-cell depletion" (PMID 36001711). B-cell counts are in the full reports, not the abstracts. |
| efficacy_endpoint | met | "The annualized relapse rate was lower with ocrelizumab than with interferon beta-1a in trial 1 (0.16 vs. 0.29; 46% lower rate with ocrelizumab; P<0.001)" (PMID 28002679); "12-week confirmed disability progression was 32.9% with ocrelizumab versus 39.3% with placebo (hazard ratio, 0.76 ...; P=0.03)" (PMID 28002688); "annualized relapse rates in the ofatumumab and teriflunomide groups were 0.11 and 0.22 ... P<0.001" (PMID 32757523); "the annualized relapse rate was 0.08 with ublituximab and 0.19 with teriflunomide (rate ratio, 0.41 ...; P<0.001)" (PMID 36001711) |
| safety_outcome | acceptable | "Serious infection occurred in 1.3% of the patients treated with ocrelizumab and in 2.9% of those treated with interferon beta-1a" (PMID 28002679); "there was no clinically significant difference between groups in the rates of serious adverse events and serious infections" (PMID 28002688) |
| development_decision | advanced | Three approvals below. |
| regulatory_outcome | approved | "In March 2017, ocrelizumab was approved in the USA for the treatment of patients with relapsing or primary progressive forms of MS" (PMID 28523586); "at least one prescription for ofatumumab between August 2020 and May 2021 ... Descriptive analyses were conducted 3, 6, and 9 months after FDA approval" (PMID 37556938); "In December 2022, ublituximab received its first global approval in the USA for the treatment of adults with relapsing forms of MS" (PMID 36920653) |
| outcome_attribution | target | Single-coder reading. |

### Smoking-MS/AD (registered: Failed)

Sources consulted: as for ModRisk-AD, plus `catalog_ms.md` Case 021.

All seven fields `not reported`. No holdout drug maps to the family; the exposure is
behavioral; no cessation trial with an MS or AD incidence endpoint is named anywhere
in the repository. The registered Failed cannot be traced to a readout.

### HRT-AD (registered: Failed)

Sources consulted:
- PMID 12771112, DOI 10.1001/jama.289.20.2651, Shumaker et al., JAMA 2003, WHIMS (the manuscript's `shumaker2003`).
- ClinicalTrials.gov NCT00000611 (Women's Health Initiative parent record; PHASE3; interventions include estrogens and progestins).

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | NCT00000611 phases: PHASE3 (WHI parent registration; WHIMS is the ancillary memory study of the estrogen-plus-progestin trial). |
| target_engagement | unclear | The abstract reports no hormone-level or other pharmacodynamic measure; engagement is presumed from the intervention. |
| efficacy_endpoint | not met | "The hazard ratio (HR) for probable dementia was 2.05 (95% confidence interval [CI], 1.21-3.48 ...; P =.01)" and "estrogen plus progestin therapy did not prevent mild cognitive impairment" |
| safety_outcome | limiting | "On July 8, 2002, the study drugs, estrogen plus progestin, in the Women's Health Initiative (WHI) trial were discontinued because of certain increased health risks in women receiving combined hormone therapy" |
| development_decision | discontinued | Same sentence; "the risks of estrogen plus progestin outweigh the benefits" |
| regulatory_outcome | not submitted | No dementia-prevention submission is recorded in any source consulted. |
| outcome_attribution | target | Single-coder reading; the "timing hypothesis" alternative would code design. |

### BMI-MS (registered: Pending)

Sources consulted:
- PMID 38018409, DOI 10.1177/13524585231213241, Bruce et al., Mult Scler 2023, MoDEMS (the manuscript's `bruce2023modems`).
- PMID 39137977, DOI 10.1136/jnnp-2024-333465, Ghezzi et al., JNNP 2025, iCR trial (NCT03539094; the manuscript's `ghezzi2025icr`).

| field | value | supporting sentence |
|---|---|---|
| trial_phase | not reported | Neither trial is phase-labelled or tests the registered construct; MoDEMS: "Seventy-one pwMS were randomized"; iCR: "Forty-two pwMS were randomised" |
| target_engagement | yes | "Mean percent weight loss in the treatment group was 8.6% compared to 0.7% in the TAU group (p < .001)" (PMID 38018409); "Leptin serum levels at 12 weeks were significantly lower in the iCR versus the control group" (PMID 39137977) |
| efficacy_endpoint | not tested | Primary outcomes are weight loss (MoDEMS) and serum leptin (iCR); "measure mobility, fatigue, and quality of life rather than relapse rate, disability accrual, or incidence" (manuscript) |
| safety_outcome | acceptable | "no serious AEs were reported" (PMID 39137977) |
| development_decision | not reported | No sponsor program. |
| regulatory_outcome | not submitted | No drug. |
| outcome_attribution | not reported | No outcome to attribute. |

### BMI-AD (registered: Failed)

Sources consulted: as for ModRisk-AD.

All seven fields `not reported`. The manuscript says the classification "correctly
predict[s] that weight-loss interventions would not prevent AD" and cites no trial;
no holdout drug maps to the family. The registered Failed cannot be traced to a
readout.

### VitaminD-MS (registered: Failed)

Sources consulted:
- PMID 37125397, DOI 10.1016/j.eclinm.2023.101957, Cassard et al., EClinicalMedicine 2023, VIDAMS (NCT01490502; CT.gov PHASE3, COMPLETED, results posted).
- PMID 40063041, DOI 10.1001/jama.2025.1604, Thouvenot et al., JAMA 2025, D-Lay MS (NCT01817166; CT.gov PHASE3, COMPLETED).
- PMID 31594857, Hupperts et al., Neurology 2019, SOLAR (NCT01285401; CT.gov PHASE2).
- PMID 31454777, Camu et al., Neurol Neuroimmunol Neuroinflamm 2019, CHOLINE (NCT01198132; CT.gov PHASE2).
- PMID 38085047, DOI 10.1093/brain/awad409, Butzkueven et al., Brain 2024, PrevANZ.
- ClinicalTrials.gov NCT01440062, the identifier in `data/phase3_holdout_dataset.csv`: "Efficacy of Vitamin D Supplementation in Multiple Sclerosis (EVIDIMS)", Charite, PHASE2, n=55, TERMINATED. This is not VIDAMS.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "VIDAMS is a randomised, phase 3, double-blind, multi-centre, controlled trial" (PMID 37125397); NCT01817166 phases: PHASE3 |
| target_engagement | not reported | None of the five abstracts reports attained serum 25(OH)D; full texts not consulted. |
| efficacy_endpoint | mixed | VIDAMS: "the proportion experiencing confirmed relapse did not differ between LDVD and HDVD [at 96 weeks: 32% vs. 34%, p = 0.60; hazard ratio (HR): 1.17 (0.67, 2.05), p = 0.57]"; D-Lay MS: "Disease activity was observed in 94 patients (60.3%) in the vitamin D group and 109 patients (74.1%) in the placebo group (hazard ratio [HR], 0.66 [95% CI, 0.50-0.87]; P = .004)"; SOLAR: "without a statistically significant difference in NEDA-3 status between groups"; CHOLINE: "The primary end point was not met"; PrevANZ: "We did not demonstrate reduction in multiple sclerosis disease activity by vitamin D3 supplementation" |
| safety_outcome | acceptable | "There was no hypercalcaemia" (VIDAMS); "Severe adverse events occurred in 17 patients in the vitamin D group and 13 in the placebo group, none of which were related to cholecalciferol" (D-Lay MS); "Vitamin D3 supplementation was safe and well tolerated" (PrevANZ) |
| development_decision | not reported | Academic trials; SOLAR and CHOLINE were Merck KGaA phase 2 add-on studies with no recorded follow-on. |
| regulatory_outcome | not submitted | Supplement; no submission recorded. |
| outcome_attribution | design | Single-coder reading: monotherapy in untreated early CIS (positive) versus add-on in established RRMS (null). |

### EBV-MS (registered: Approved)

Sources consulted:
- ClinicalTrials.gov NCT03283826, EMBOLD, ATA188, Atara Biotherapeutics, phases PHASE1/PHASE2, TERMINATED: "Study was terminated as primary endpoint was not achieved".
- PMID 38104476, DOI 10.1016/j.msard.2023.105364, Giovannoni, Mult Scler Relat Disord 2024, "Emboldened or not: The potential fall-out of a failed anti-EBV trial in multiple sclerosis" (title only; no abstract).
- `paper/paper_v25_round3.tex`, `paper/supplementary_data.csv` (EBV-MS rows: "MR of EBV and MS (d~1.92)", "Observational EBV-MS (d~0.53)", no drug named), `catalog_ms.md` Case 035 ("the etiology->therapy transport is UNPROVEN").

All seven fields `not reported`. No EBV-directed therapy holds an MS approval in any
source consulted; the only EBV-directed program with a controlled readout was
terminated at phase 1/2 for not meeting its primary endpoint. The registered Approved
has no identifiable EBV-directed program. If it was coded on anti-CD20 agents (B cells
as the EBV reservoir), the manuscript does not say so.

---

## Cardio

### HDL/CETP (registered: Failed)

Sources consulted:
- PMID 17984165, DOI 10.1056/NEJMoa0706628, Barter et al., NEJM 2007, ILLUMINATE (NCT00134264).
- PMID 23126252, DOI 10.1056/NEJMoa1206797, Schwartz et al., NEJM 2012, dal-OUTCOMES (NCT00658515).
- PMID 28514624, DOI 10.1056/NEJMoa1609581, Lincoff et al., NEJM 2017, ACCELERATE (NCT01687998).
- PMID 28847206, DOI 10.1056/NEJMoa1706444, HPS3/TIMI55-REVEAL, NEJM 2017 (NCT01252953).
- PMID 30704580, DOI 10.1016/j.jacc.2018.10.072, Armitage et al., JACC 2019 (class review).
- PMID 29018035, Tall and Rader, Circ Res 2018 (class review).
- ClinicalTrials.gov NCT05202509, PREVAIL (obicetrapib), PHASE3, ACTIVE_NOT_RECRUITING, primary completion 2026-11.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "To date, 4 CETP inhibitors have entered phase 3 cardiovascular outcome trials" (PMID 30704580); ACCELERATE: "randomized, double-blind, placebo-controlled phase 3 trial" |
| target_engagement | yes | "there was an increase of 72.1% in high-density lipoprotein cholesterol" (torcetrapib); "HDL cholesterol levels increased ... by 31 to 40% in the dalcetrapib group"; "a 133.2% increase in the mean HDL cholesterol level was seen with evacetrapib"; "the mean level of HDL cholesterol was higher by 43 mg per deciliter ... (a relative difference of 104%)" (anacetrapib) |
| efficacy_endpoint | mixed | Named programs all not met: "increased risk of cardiovascular events (hazard ratio, 1.25 ...)" (torcetrapib); "dalcetrapib did not alter the risk of the primary end point (... hazard ratio with dalcetrapib, 1.04; 95% confidence interval, 0.93 to 1.16; P=0.52)"; "a primary end-point event occurred in 12.9% of the patients in the evacetrapib group and in 12.8% of those in the placebo group (hazard ratio, 1.01 ...)". REVEAL met: "the primary outcome occurred in significantly fewer patients in the anacetrapib group than in the placebo group (... rate ratio, 0.91; 95% confidence interval, 0.85 to 0.97; P=0.004)" |
| safety_outcome | acceptable | "Torcetrapib was withdrawn due to unanticipated off-target effects that increased risk of death, and major trials of dalcetrapib and evacetrapib were terminated early for futility" (PMID 30704580); "There were no significant between-group differences in the risk of death, cancer, or other serious adverse events" (REVEAL). Coded acceptable for the class; torcetrapib alone was safety-limited. |
| development_decision | discontinued | "anaceptrapib was found to accumulate in adipose tissue, and regulatory approval is not being sought" (PMID 30704580); dal-OUTCOMES and ACCELERATE terminated (above) |
| regulatory_outcome | not submitted | Same sentence (PMID 30704580); "no cholesterol ester transfer protein inhibitor has yet been approved for clinical use" (PMID 28611186, 2017) |
| outcome_attribution | target | "The benefit of anacetrapib seems to be largely explained by lowering of non-HDL-C ... rather than increases in HDL-C" (PMID 29018035). Single-coder reading: HDL raising per se did not translate. |

### Niacin/HDL (registered: Failed)

Sources consulted:
- PMID 22085343, DOI 10.1056/NEJMoa1107579, AIM-HIGH Investigators, NEJM 2011 (NCT00120289; CT.gov PHASE3, TERMINATED: "stopped on the recommendation of the DSMB because of lack of efficacy of niacin in preventing primary outcome events").
- PMID 25014686, DOI 10.1056/NEJMoa1300955, HPS2-THRIVE Collaborative Group, NEJM 2014 (NCT00461630; CT.gov PHASE3).
- PMID 24622598, DOI 10.1016/S2213-8587(13)70129-3, Mayor, Lancet Diabetes Endocrinol 2013, "Nicotinic acid plus laropiprant suspended for dyslipidaemia" (title only).
- PMID 25178730, Tuteja and Rader, Nat Rev Endocrinol 2014.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | CT.gov phases PHASE3 for both trials. |
| target_engagement | yes | "niacin therapy had significantly increased the median HDL cholesterol level from 35 mg per deciliter ... to 42 mg per deciliter" (AIM-HIGH); "an HDL cholesterol level that was an average of 6 mg per deciliter ... higher than the levels in those assigned to placebo" (HPS2-THRIVE) |
| efficacy_endpoint | not met | "The trial was stopped after a mean follow-up period of 3 years owing to a lack of efficacy ... (hazard ratio, 1.02; 95% confidence interval, 0.87 to 1.21; P=0.79 ...)" (AIM-HIGH); "had no significant effect on the incidence of major vascular events (... rate ratio, 0.96; 95% confidence interval [CI], 0.90 to 1.03; P=0.29)" (HPS2-THRIVE) |
| safety_outcome | limiting | "did not significantly reduce the risk of major vascular events but did increase the risk of serious adverse events" (HPS2-THRIVE) |
| development_decision | discontinued | Suspension of the laropiprant combination (PMID 24622598, title); "the use of niacin to increase levels of HDL cholesterol is not recommended" (PMID 25178730) |
| regulatory_outcome | not approved | EMA suspension of nicotinic acid/laropiprant (PMID 24622598, 2013). The 2016 FDA withdrawal of niacin-ER/statin combination approvals is a known event that no PubMed or CT.gov record retrieved here documents; it is not cited. |
| outcome_attribution | target | Single-coder reading. |

### Homocysteine (registered: Failed)

Sources consulted:
- PMID 20937919, DOI 10.1001/archinternmed.2010.348, Clarke et al. (B-Vitamin Treatment Trialists' Collaboration), Arch Intern Med 2010, 8-trial individual-participant meta-analysis.
- PMID 16531613, DOI 10.1056/NEJMoa060900, Lonn et al., NEJM 2006, HOPE-2 (NCT00106886; CT.gov PHASE4).
- PMID 16531614, DOI 10.1056/NEJMoa055227, Bonaa et al., NEJM 2006, NORVIT (NCT00266487).

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "8 large, randomized, placebo-controlled trials of folic acid supplementation involving 37 485 individuals at increased risk of cardiovascular disease" (PMID 20937919). HOPE-2 is registered as phase 4; the trials are event-driven prevention RCTs of licensed vitamins, coded III as the readout phase. |
| target_engagement | yes | "Folic acid allocation yielded an average 25% reduction in homocysteine levels" (PMID 20937919); "The mean total homocysteine level was lowered by 27 percent" (NORVIT) |
| efficacy_endpoint | not met | "folic acid allocation had no significant effects on vascular outcomes, with rate ratios (95% confidence intervals) of 1.01 (0.97-1.05) for major vascular events" (PMID 20937919); HOPE-2 "relative risk, 0.95; 95 percent confidence interval, 0.84 to 1.07; P=0.41"; NORVIT "risk ratio, 1.08; 95 percent confidence interval, 0.93 to 1.25; P=0.31" |
| safety_outcome | acceptable | "There was no significant effect on the rate ratios ... for overall cancer incidence ... or all-cause mortality" (PMID 20937919); NORVIT: "A harmful effect from combined B vitamin treatment was suggested" (trend, not decisive) |
| development_decision | not reported | Academic prevention trials; no sponsor decision. |
| regulatory_outcome | not submitted | Vitamins; no submission recorded. |
| outcome_attribution | target | Single-coder reading. |

### CRP (registered: No benefit)

Sources consulted:
- PMID 28845751, DOI 10.1056/NEJMoa1707914, Ridker et al., NEJM 2017, CANTOS (NCT01327846; CT.gov PHASE3, COMPLETED, results posted).
- PMID 31882264, DOI 10.1016/j.tcm.2019.11.013, Wong et al., Trends Cardiovasc Med 2021.
- PMID 29265905, Capodanno and Angiolillo, Expert Opin Biol Ther 2018.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | CT.gov phases PHASE3. |
| target_engagement | yes | "the median reduction from baseline in the high-sensitivity C-reactive protein level was 26 percentage points greater in the group that received the 50-mg dose of canakinumab, 37 percentage points greater in the 150-mg group, and 41 percentage points greater in the 300-mg group than in the placebo group". Caveat: "canakinumab, a therapeutic monoclonal antibody targeting interleukin-1beta"; CRP is downstream of the drug target. |
| efficacy_endpoint | met | "in the 150-mg group, 0.85 (95% CI, 0.74 to 0.98; P=0.021) ... The 150-mg dose, but not the other doses, met the prespecified multiplicity-adjusted threshold for statistical significance for the primary end point" |
| safety_outcome | unclear | "Canakinumab was associated with a higher incidence of fatal infection than was placebo. There was no significant difference in all-cause mortality" |
| development_decision | not reported | The sponsor's decision after the FDA action is not in any source consulted. |
| regulatory_outcome | not approved | "the Canakinumab Anti-Inflammatory Thrombosis Outcomes Study (CANTOS) using canakinumab, despite the fact the therapy was not approved by the Food and Drug Administration (FDA) for cardiovascular risk reduction" (PMID 31882264). Year not carried by the source. |
| outcome_attribution | uncertain | Endpoint met at one dose, modest effect, safety signal; regulatory reasoning not public in the consulted record. |

Manuscript sentence at variance with the record: "canakinumab's null primary endpoint in CANTOS despite reducing CRP" (`paper_v25_round3.tex`, cardio results paragraph).

### Uric acid (registered: Failed; status ambiguous)

Sources consulted:
- PMID 36216006, DOI 10.1016/S0140-6736(22)01657-9, Mackenzie et al., Lancet 2022, ALL-HEART (ISRCTN32017426; EudraCT 2013-003559-39; no NCT).
- PMID 38551218, DOI 10.3310/ATTM4092, Mackenzie et al., Health Technol Assess 2024.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | post-marketing | "a multicentre, prospective, randomised, open-label, blinded-endpoint trial" of "Allopurinol ... a urate-lowering therapy used to treat patients with gout" in a new indication; no phase label given. |
| target_engagement | not reported | Neither abstract reports serum urate attainment; full text not consulted. |
| efficacy_endpoint | not met | "hazard ratio [HR] 1.04 [95% CI 0.89-1.21], p=0.65" |
| safety_outcome | acceptable | No safety signal reported; "One thousand six hundred and thirty-seven participants (57.4%) in the allopurinol arm withdrew from randomised treatment" (PMID 38551218) |
| development_decision | not reported | NIHR-funded academic trial; no sponsor decision. |
| regulatory_outcome | not submitted | No submission recorded. |
| outcome_attribution | target | Single-coder reading. |

### LDL/PCSK9 (registered: Approved)

Sources consulted:
- PMID 28304224, DOI 10.1056/NEJMoa1615664, Sabatine et al., NEJM 2017, FOURIER (NCT01764633; CT.gov PHASE3).
- PMID 30403574, DOI 10.1056/NEJMoa1801174, Schwartz et al., NEJM 2018, ODYSSEY OUTCOMES (NCT01663402; CT.gov PHASE3).
- PMID 26323342, Markham, Drugs 2015, "Evolocumab: First Global Approval"; PMID 26370210, Markham, Drugs 2015, "Alirocumab: First Global Approval".
- PMID 31882264, Wong et al., 2021.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | CT.gov phases PHASE3 for both trials. |
| target_engagement | yes | "the least-squares mean percentage reduction in LDL cholesterol levels with evolocumab, as compared with placebo, was 59%" (FOURIER); "The dose of alirocumab was adjusted under blinded conditions to target an LDL cholesterol level of 25 to 50 mg per deciliter" (ODYSSEY) |
| efficacy_endpoint | met | "evolocumab treatment significantly reduced the risk of the primary end point (... hazard ratio, 0.85; 95% confidence interval [CI], 0.79 to 0.92; P<0.001)"; "A composite primary end-point event occurred in 903 patients (9.5%) in the alirocumab group and in 1052 patients (11.1%) in the placebo group (hazard ratio, 0.85; 95% confidence interval [CI], 0.78 to 0.93; P<0.001)" |
| safety_outcome | acceptable | "There was no significant difference between the study groups with regard to adverse events ..., with the exception of injection-site reactions" (FOURIER); "The incidence of adverse events was similar in the two groups, with the exception of local injection-site reactions" (ODYSSEY) |
| development_decision | advanced | Approvals below. |
| regulatory_outcome | approved | "Evolocumab (Repatha) ... has been approved as a treatment for hypercholesterolaemia in the EU, and is awaiting approval in the USA and Japan" (PMID 26323342, 2015); "Alirocumab (Praluent) ... has been approved in the US as an adjunct to diet and maximally tolerated statin therapy" (PMID 26370210, 2015); "providing further evidence-based therapy for additional reduction of ASCVD risk beyond statin therapy" (PMID 31882264). Label-extension identifiers not retrieved. |
| outcome_attribution | target | Single-coder reading. |

### Blood pressure (registered: Approved)

Sources consulted:
- PMID 33933205, DOI 10.1016/S0140-6736(21)00590-0, Blood Pressure Lowering Treatment Trialists' Collaboration, Lancet 2021 (48 trials, 344,716 participants).
- PMID 11589932, DOI 10.1016/S0140-6736(01)06178-5, PROGRESS Collaborative Group, Lancet 2001.

The manuscript names no program ("approved drug classes"); the family is coded as a
mixed class on the pooled trials with PROGRESS as the stroke exemplar.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | mixed class | "48 randomised trials of pharmacological blood pressure lowering medications versus placebo or other classes" (PMID 33933205) |
| target_engagement | yes | "active treatment reduced blood pressure by 9/4 mm Hg" (PROGRESS); "The relative effects of blood pressure-lowering treatment were proportional to the intensity of systolic blood pressure reduction" (BPLTTC) |
| efficacy_endpoint | met | "307 (10%) individuals assigned active treatment suffered a stroke, compared with 420 (14%) assigned placebo (relative risk reduction 28% [95% CI 17-38], p<0.0001)" (PROGRESS); "a 5 mm Hg reduction of systolic blood pressure reduced the risk of major cardiovascular events by about 10%" (BPLTTC) |
| safety_outcome | acceptable | No safety-driven termination reported in either source. |
| development_decision | advanced | Class-level. |
| regulatory_outcome | approved | Every pooled trial drug is a marketed antihypertensive; no single FDA/EMA event exists to cite. |
| outcome_attribution | target | Single-coder reading. |

### Triglycerides (registered: Approved)

Sources consulted:
- PMID 30415628, DOI 10.1056/NEJMoa1812792, Bhatt et al., NEJM 2019, REDUCE-IT (NCT01492361; CT.gov PHASE3).
- PMID 36342113, DOI 10.1056/NEJMoa2210645, Das Pradhan et al., NEJM 2022, PROMINENT (NCT03071692; CT.gov PHASE3, TERMINATED: "stopped for futility based on efficacy results at the interim analysis; no unexpected safety findings").
- PMID 33190147, DOI 10.1001/jama.2020.22258, Nicholls et al., JAMA 2020, STRENGTH (NCT02104817).
- PMID 20228404, DOI 10.1056/NEJMoa1001282, ACCORD Study Group, NEJM 2010, ACCORD-Lipid (NCT00000620).
- PMID 32959713, Boden, Future Cardiol 2021; PMID 33888593, Curfman, Open Heart 2021.

The manuscript names no program ("approved drug classes"); coded as a mixed class.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | mixed class | Four phase 3 outcome trials across three classes (CT.gov phases PHASE3 for REDUCE-IT and PROMINENT). |
| target_engagement | yes | "the effects of pemafibrate on lipid levels at 4 months were -26.2% for triglycerides" (PROMINENT); "Icosapent ethyl ... lowers triglyceride levels" (REDUCE-IT) |
| efficacy_endpoint | mixed | REDUCE-IT: "A primary end-point event occurred in 17.2% of the patients in the icosapent ethyl group, as compared with 22.0% of the patients in the placebo group (hazard ratio, 0.75; 95% confidence interval [CI], 0.68 to 0.83; P<0.001)"; PROMINENT: "hazard ratio, 1.03; 95% confidence interval, 0.91 to 1.15"; STRENGTH: "hazard ratio, 0.99 [95% CI, 0.90-1.09]; P = .84"; ACCORD-Lipid: "hazard ratio in the fenofibrate group, 0.92; 95% confidence interval [CI], 0.79 to 1.08; P=0.32" |
| safety_outcome | acceptable | "A larger percentage of patients in the icosapent ethyl group than in the placebo group were hospitalized for atrial fibrillation or flutter (3.1% vs. 2.1%, P=0.004)"; "pemafibrate was associated with a higher incidence of adverse renal events and venous thromboembolism"; neither determined the outcome |
| development_decision | not reported | Differs by program (advanced for icosapent ethyl; futility stops for PROMINENT and STRENGTH). |
| regulatory_outcome | approved | "leading to an expanded indication in the USA. IPE is now approved as an adjunct to maximally tolerated statins to reduce CVD event risk in adults with triglyceride (TG) levels >=150 mg/dl" (PMID 32959713); "the agency later granted a label extension to include the additional indication of a reduction in risk of cardiovascular events" (PMID 33888593). Exact approval date not carried by the sources. |
| outcome_attribution | uncertain | "STRENGTH ..., that directly contradicts REDUCE-IT and calls into question whether icosapent ethyl is actually effective" (PMID 33888593); the pure triglyceride-lowering programs failed. |

### Lp(a) (registered: Pending)

Sources consulted:
- ClinicalTrials.gov NCT04023552, Lp(a)HORIZON, pelacarsen (TQJ230), Novartis, PHASE3, n=8323, overallStatus COMPLETED, primary completion 2026-07-16, hasResults false, no results posted.
- PMID 31893580, DOI 10.1056/NEJMoa1905239, Tsimikas et al., NEJM 2020, phase 2 dose-ranging (NCT03070782).
- PMID 42593611, DOI 10.1007/s11883-026-01453-9, Ebubechukwu et al., Curr Atheroscler Rep, August 2026; PMID 42675370, Gonzalez et al., Am J Cardiovasc Drugs, August 2026; PMID 42761946, Bene-Alhasan et al., 2026.
- PMID 42760802, DOI 10.1177/10742484261492865, Borovac, J Cardiovasc Pharmacol Ther 2026, "Lipoprotein(a) After HORIZON: Causal Culprit, Risk Marker, or Unfulfilled Therapeutic Promise?" (title only; no abstract in PubMed).
- PubMed searches for a pelacarsen or Lp(a)HORIZON primary result (2026, with outcome terms) returned no trial report.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | CT.gov phases PHASE3. |
| target_engagement | yes | "Administration of APO(a)-LRx resulted in dose-dependent decreases in lipoprotein(a) levels, with mean percent decreases of ... 80% at 20 mg every week" (PMID 31893580) |
| efficacy_endpoint | not reported | "Pelacarsen ... is the subject of the phase 3 Lp(a) HORIZON trial, with results due in late 2026" (PMID 42593611); "definitive proof of clinical benefit awaits ongoing randomized cardiovascular outcomes trials, including Lp(a)HORIZON (pelacarsen)" (PMID 42675370). The Borovac title is recorded as a lead, not a result. |
| safety_outcome | acceptable | "There were no significant differences between any APO(a)-LRx dose and placebo with respect to platelet counts, liver and renal measures, or influenza-like symptoms. The most common adverse events were injection-site reactions" (PMID 31893580) |
| development_decision | ongoing | CT.gov COMPLETED without posted results; readout awaited per the 2026 reviews. |
| regulatory_outcome | not submitted | "Novel unapproved therapies, including an antisense oligonucleotide (pelacarsen)" (PMID 42761946, 2026) |
| outcome_attribution | not reported | No outcome. |

### IL-6R (registered: Pending)

Sources consulted:
- ClinicalTrials.gov NCT05021835, ZEUS, ziltivekimab, Novo Nordisk, PHASE3, n=6385, COMPLETED, primary completion 2026-06-09, no results posted.
- PMID 41369941, DOI 10.1001/jamacardio.2025.4491, Ridker et al., JAMA Cardiol 2026 (ZEUS design and baseline).
- PMID 34015342, DOI 10.1016/S0140-6736(21)00520-1, Ridker et al., Lancet 2021, RESCUE phase 2 (NCT03926117).
- ClinicalTrials.gov NCT05636176, HERMES (ziltivekimab, HFpEF/HFmrEF), PHASE3, TERMINATED: "No longer looking for participants"; PMID 42106986 (ATHENA/HERMES design).
- Manuscript citation `novonordisk2026zeus`: Novo Nordisk company announcement, 31 July 2026, Form 6-K, SEC accession 0001171843-26-005109. Not retrievable via the APIs used; the values below are as the manuscript reports them.
- PubMed searches for a ZEUS primary result (2026, with outcome terms) returned no trial report.

| field | value | supporting sentence |
|---|---|---|
| trial_phase | III | "ZEUS is a multinational, double-blind, placebo-controlled, event-driven, randomized clinical trial inclusive of 6376 participants" (PMID 41369941); CT.gov PHASE3 |
| target_engagement | yes | "median high-sensitivity CRP levels were reduced by 77% for the 7.5 mg group, 88% for the 15 mg group, and 92% for the 30 mg group compared with 4% for the placebo group" (PMID 34015342); manuscript: "while producing the expected reductions in free IL-6 and high-sensitivity C-reactive protein" (citing the 6-K) |
| efficacy_endpoint | not met | Manuscript: "Ziltivekimab did not reduce major adverse cardiovascular events (HR 0.99, 95% CI 0.88-1.11)" (citing the 6-K) |
| safety_outcome | unclear | Not stated in the manuscript's citation or any indexed source. |
| development_decision | not reported | ASCVD program decision not in the consulted record; HERMES TERMINATED per CT.gov. |
| regulatory_outcome | not submitted | No submission recorded. |
| outcome_attribution | target | Single-coder reading: target engaged, endpoint unmoved; instrument (IL6R) and drug (IL-6 ligand) act at different nodes. |

---

## Families with any field `not reported`

ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS (all seven fields: no program named);
BMI-MS (trial_phase, development_decision, outcome_attribution); VitaminD-MS
(target_engagement, development_decision); Homocysteine (development_decision); CRP
(development_decision); Uric acid (target_engagement, development_decision);
Triglycerides (development_decision); Lp(a) (efficacy_endpoint, outcome_attribution);
IL-6R (development_decision).

## Families where the coded fields disagree with the registered `drug_outcome`

- CRP: registered "No benefit"; CANTOS met its primary endpoint at 150 mg (HR 0.85, p=0.021) and the drug was not approved for the indication. The manuscript's "null primary endpoint" wording is at variance with PMID 28845751.
- VitaminD-MS: registered Failed; phase 3 readouts are mixed (VIDAMS not met, D-Lay MS met on disease activity; relapse alone not significant in D-Lay MS).
- Triglycerides: registered Approved; class-level efficacy is mixed (one positive program, three null), and the approval rests on a drug whose benefit is contested as a triglyceride effect.
- HDL/CETP: registered Failed; the three named programs failed, but the fourth CETP inhibitor (anacetrapib, REVEAL) met its primary endpoint and was not filed. Partial disagreement at class level.
- IL-6R: registered Pending; ZEUS read out null on 31 July 2026 per the manuscript's own citation, so the fields read as a failure. Amendment 5 already records the family as unscored.
- EBV-MS: registered Approved; no EBV-directed program has an approval, and the only controlled EBV-directed readout (EMBOLD) was terminated for not meeting its primary endpoint.
- ModRisk-AD, Smoking-MS/AD, BMI-AD: registered Failed; no program, trial, or regulatory record is identified anywhere in the repository, so the registered outcome cannot be traced to a readout.

Not a disagreement, recorded for completeness: Lp(a) remains pending in every indexed
source, but a 2026 commentary title ("After HORIZON ... Unfulfilled Therapeutic
Promise?") suggests a readout that PubMed does not yet carry as a trial report.

## Identifier corrections found in repository files (not edited)

- `data/phase3_holdout_dataset.csv` and `data/phase3_expanded_dataset.csv` give NCT01440062 for vitamin D supplementation in MS; that record is EVIDIMS (Charite, phase 2, n=55, terminated). VIDAMS is NCT01490502.
- `paper/paper_v25_round3.tex` describes CANTOS as having a "null primary endpoint"; the trial met its primary endpoint at the 150 mg dose (PMID 28845751).
