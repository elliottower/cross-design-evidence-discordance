# Codebook log: autoimmune families (Amendment 5, Procedure 3)

Date coded: 2026-09-22. Single coder. Families: the eight rows with `domain = autoimmune` in
`data/cross_design_classification_all_41_families_v3.csv`. The registered `drug_outcome` column was
read but not changed. Every number in this file is quoted from the cited abstract, registry entry
or FDA record; none is computed here, so no `results` claim is recorded for any of them.

## Source-lookup record

- PubMed E-utilities (`esearch`, `esummary`, `efetch` with `rettype=abstract`); no email, key or
  custom User-Agent on any request. Every PMID below was resolved by title/author/journal search
  and its abstract read in full before a sentence was quoted.
- ClinicalTrials.gov API v2 (`/api/v2/studies?query.term=` and `/api/v2/studies/{nctId}`), fields:
  phase, official title, conditions, interventions, primary outcomes.
- FDA: Drugs@FDA API (`api.fda.gov/drug/drugsfda.json`, no key) for application numbers,
  submission numbers and approval dates; openFDA label API (`api.fda.gov/drug/label.json`) for the
  current indication text. The approval letters listed in Drugs@FDA (accessdata.fda.gov) were
  requested once each with a plain client and every request returned an "excessive requests"
  abuse-detection page (HTTP 404, 420 bytes); no retry, no User-Agent change. Where a Drugs@FDA
  supplement row is cited, the row gives number, class and date but not the indication text; the
  indication is confirmed from the current label.
- EMA: no API used; no EMA year is coded. Every regulatory year is FDA.
- The manuscript (`paper/paper_v25_round3.tex`) and the classifier
  (`analysis/classifier/classify_families.py`) name no trial or regulatory source for any of the
  eight families (CANTOS is named in the cardio text without a citation; dupilumab is cited only
  for asthma, `busse2019dupilumab`). Every trial and regulatory source below is therefore an
  addition, not a source the manuscript already cites.

## Drug-program choices

The manuscript names no agent for six of the eight families. The rule applied: the first-approved
agent in the class for the family's indication, stated per family.

| family | program coded | why |
|---|---|---|
| IL-23-psoriasis | guselkumab (p19-selective), with ustekinumab (p40) as the earlier agent | genetic leg is IL23R; guselkumab is the first-approved selective IL-23 inhibitor; ustekinumab codes identically on every field |
| CTLA-4-RA | abatacept | only approved CTLA-4-pathway agent in RA |
| TNF-a-RA | etanercept (first approved for RA, 1998) and infliximab (RA supplement, 1999) | class coded with two agents; pivotal readouts are both Phase III for RA |
| IL-17-psoriasis | secukinumab | first-approved IL-17A antagonist for psoriasis |
| JAK-STAT-RA | tofacitinib | first-approved JAK inhibitor for RA |
| CD20-RA | rituximab | only anti-CD20 approved for RA |
| IL-4Ra-AD | dupilumab | named in the manuscript |
| IL-1b-CVD | canakinumab (CANTOS) | named in the manuscript |

## Per-family sources and supporting sentences

### IL-23-psoriasis

- PMID:28057360 (Blauvelt 2017, VOYAGE 1, J Am Acad Dermatol; DOI 10.1016/j.jaad.2016.11.041)
  - trial_phase III: title reads "Results from the phase III, double-blinded, placebo- and active comparator-controlled VOYAGE 1 trial."
  - efficacy met: "Guselkumab was superior (P < .001) to placebo at week 16 (85.1% vs 6.9% [Investigator Global Assessment score of 0/1 (cleared/minimal)] and 73.3% vs 2.9% [90% or greater improvement in PASI score from baseline (PASI 90)])."
  - safety acceptable: "Adverse event rates were comparable between treatments."
- PMID:28057361 (Reich 2017, VOYAGE 2)
  - efficacy met: "At week 16, more patients receiving guselkumab achieved an Investigator Global Assessment (IGA) score 0/1 (cleared/minimal) (84.1% vs 8.5%) and PASI 90 (70.0% vs 2.4%) versus placebo (coprimary end points)."
  - safety: "Adverse events were comparable among groups."
- NCT:NCT02207231 (VOYAGE 1) and NCT:NCT02207244 (VOYAGE 2): phase PHASE3, condition Psoriasis, primary outcomes IGA 0/1 and PASI 90 at week 16 vs placebo.
- PMID:24679469 (Sofen 2014, J Allergy Clin Immunol) — target engagement: "At week 12, significant reductions in psoriasis gene expression and serum IL-17A levels were observed in guselkumab-treated patients."
- PMID:39114670 (Blauvelt 2024, JID Innov, VOYAGE 1 substudy) — target engagement within the pivotal program: "Guselkumab provided rapid reductions in serum IL-17A, IL-17F, and IL-22 levels by week 4 versus at baseline, which were maintained through weeks 24 and 48 (P < .001)."
- FDA:BLA761061 (Tremfya) — Drugs@FDA: ORIG-1, TYPE 1, approved 2017-07-13, priority review. Current label (set-id 1e6dc9ae-1c4c-42d9-87aa-c315ecc51b56): "TREMFYA is an interleukin-23 antagonist indicated for the treatment of: adults and pediatric patients 6 years of age and older who also weigh at least 40 kg with moderate-to-severe plaque psoriasis".
- Ustekinumab, recorded as the earlier p40 agent: PMID:18486739 (PHOENIX 1, "171 (67.1%) patients receiving ustekinumab 45 mg, 170 (66.4%) receiving ustekinumab 90 mg, and eight (3.1%) receiving placebo achieved PASI 75 at week 12"), PMID:18486740 (PHOENIX 2), NCT:NCT00267969, NCT:NCT00307437; FDA:BLA125261 ORIG-1 approved 2009-09-25.
- development_decision advanced and outcome_attribution target follow from the above; no separate source.

### CTLA-4-RA

- PMID:16785475 (Kremer 2006, AIM, Ann Intern Med; DOI 10.7326/0003-4819-144-12-200606200-00003)
  - efficacy met: "6-month ACR 20, ACR 50, and ACR 70 responses were 67.9% for abatacept versus 39.7% for placebo (difference, 28.2 percentage points [95% CI, 19.8 to 36.7 percentage points])"; "At 1 year, abatacept statistically significantly slowed the progression of structural joint damage compared with placebo."
  - safety acceptable: "Abatacept-treated patients had a similar incidence of adverse events (87.3% vs. 84.0%...) and a higher incidence of prespecified serious infections (2.5% vs. 0.9%...) and infusion reactions".
- PMID:16162882 (Genovese 2005, ATTAIN, N Engl J Med; DOI 10.1056/NEJMoa050524)
  - trial_phase III: "We conducted a randomized, double-blind, phase 3 trial to evaluate the efficacy and safety of abatacept".
  - efficacy met: "After six months, the rates of ACR 20 responses were 50.4 percent in the abatacept group and 19.5 percent in the placebo group (P<0.001)".
  - safety: "The incidence of serious infections was 2.3 percent in each group."
- NCT:NCT00048568 (AIM; PHASE3; primary ACR20 at day 169, HAQ at day 365, erosion score at day 365) and NCT:NCT00048581 (ATTAIN; PHASE3; primary ACR20 at day 169, HAQ).
- PMID:17014006 (Weisman 2006, J Rheumatol) — target engagement: "Following 12 months' treatment, serum levels of interleukin 6 (IL-6), soluble IL-2 receptor, C-reactive protein, soluble E-selectin, and soluble intercellular adhesion molecule-1 were significantly lower in patients receiving abatacept 10 mg/kg versus placebo." This is the Phase II trial ("Data from a Phase II trial showed efficacy..."), and the markers are downstream of the CD80/CD86:CD28 target.
- FDA:BLA125118 (Orencia) — Drugs@FDA: ORIG-1, TYPE 1, approved 2005-12-23, priority. Current label (set-id 0836c6ac-ee37-5640-2fed-a3185a0b16eb): "ORENCIA is indicated for the treatment of adult patients with moderately to severely active rheumatoid arthritis (RA)".
- PMID:17565924 (Lundquist 2007, Adv Ther) — regulatory year corroboration: "In December 2005, abatacept became the first therapy to be approved by the US Food and Drug Administration for the treatment of adult patients with moderately to severely active RA".

### TNF-a-RA

- PMID:10075615 (Moreland 1999, Ann Intern Med; DOI 10.7326/0003-4819-130-6-199903160-00004) — etanercept pivotal trial
  - efficacy met: "At 6 months, 59% of the 25-mg group and 11% of the placebo group achieved a 20% ACR response (P < 0.001); 40% and 5%, respectively, achieved a 50% ACR response (P < 0.01)."
  - safety acceptable: "Etanercept was well tolerated, with no dose-limiting toxic effects."
  - The abstract does not state a phase; it opens "In a phase II study, etanercept ... To confirm the benefit of etanercept therapy of longer duration".
- PMID:9219699 (Moreland 1997, N Engl J Med; DOI 10.1056/NEJM199707173370301) — the Phase II dose-ranging trial: "At three months, 75 percent of the patients in the group assigned to 16 mg of TNFR:Fc per square meter had improvement of 20 percent or more in symptoms, as compared with 14 percent in the placebo group (P<0.001)."
- PMID:10622295 (Maini 1999, ATTRACT, Lancet; DOI 10.1016/s0140-6736(99)05246-0)
  - trial_phase III: "In an international double-blind placebo-controlled phase III clinical trial, 428 patients..."
  - efficacy met: "the American College of Rheumatology (20) response criteria ... were achieved in 53, 50, 58, and 52% of patients receiving [infliximab] ... compared with 20% of patients receiving placebo plus methotrexate (p<0.001 for each of the four infliximab regimens vs placebo)."
  - safety: "Infliximab was well-tolerated; withdrawals for adverse events as well as the occurrence of serious adverse events or serious infections did not exceed those in the placebo group."
- PMID:10415055 (Charles 1999, J Immunol) — target engagement (infliximab program): "in vivo administration of anti-TNF-alpha Ab ... results in the rapid down-regulation of a spectrum of cytokines, cytokine inhibitors, and acute-phase proteins"; "IL-6, which reached normal levels within 24 h."
- FDA:BLA103795 (Enbrel) — Drugs@FDA: ORIG-1, TYPE 1, approved 1998-11-02, priority. Current label (set-id a002b40c-097d-47a5-957f-7a7b1807af7f): "Enbrel is indicated for reducing signs and symptoms, inducing major clinical response, inhibiting the progression of structural damage, and improving physical function in patients with moderately to severely active rheumatoid arthritis (RA)".
- FDA:BLA103772 (Remicade) — Drugs@FDA: SUPPL-1004, EFFICACY, approved 1999-11-10 (the first efficacy supplement after the 1998-08-24 original Crohn's approval). Current label (set-id a0a046c1-056d-45a9-bfd9-13b47c24f257): "REMICADE, in combination with methotrexate, is indicated for reducing signs and symptoms, inhibiting the progression of structural damage, and improving physical function in adult patients with moderately to severely active rheumatoid arthritis (RA)".
- PMID:10375846 (Moreland 1999, Cleve Clin J Med) — regulatory corroboration: "Infliximab and etanercept, both approved by the FDA in 1998 ... Infliximab is approved for Crohn disease and etanercept for rheumatoid arthritis."

### IL-17-psoriasis

- PMID:25007392 (Langley 2014, N Engl J Med; DOI 10.1056/NEJMoa1314258)
  - trial_phase III: "In two phase 3, double-blind, 52-week trials, ERASURE ... and FIXTURE ..."
  - efficacy met: "The proportion of patients who met the criterion for PASI 75 at week 12 was higher with each secukinumab dose than with placebo or etanercept: in the ERASURE study, the rates were 81.6% with 300 mg of secukinumab, 71.6% with 150 mg of secukinumab, and 4.5% with placebo; in the FIXTURE study, the rates were 77.1% ..., 67.0% ..., 44.0% with etanercept, and 4.9% with placebo (P<0.001 for each secukinumab dose vs. comparators)." Coprimary IGA 0/1 likewise met.
  - safety acceptable: "The rates of infection were higher with secukinumab than with placebo in both studies and were similar to those with etanercept."
  - attribution target: "Secukinumab was effective for psoriasis in two randomized trials, validating interleukin-17A as a therapeutic target."
- NCT:NCT01365455 (ERASURE; PHASE3; primary PASI 75 and IGA 0/1 at 12 weeks) and NCT:NCT01358578 (FIXTURE; PHASE3; same primaries, etanercept comparator).
- PMID:31129129 (Krueger 2019, J Allergy Clin Immunol; NCT01537432) — target engagement: "Suppression of the IL-23/IL-17 axis by secukinumab was evident at week 1 and continued through week 12, including reductions in levels of the upstream cytokine IL-23, the drug target IL-17A, and downstream targets, including beta-defensin 2." Mechanistic study at "the clinically approved dose", not one of the pivotal trials.
- PMID:20926833 (Hueber 2010, Sci Transl Med) — proof-of-concept: "AIN457 treatment induced clinically relevant responses of variable magnitude in patients suffering from each of these diverse immune-mediated diseases."
- FDA:BLA125504 (Cosentyx) — Drugs@FDA: ORIG-1, TYPE 1, approved 2015-01-21. Current label (set-id 77c4b13e-7df3-42d4-81db-3d0cddb7f67a): "COSENTYX is indicated for the treatment of moderate to severe plaque psoriasis (PsO) in adults and pediatric patients 6 years and older who are candidates for systemic therapy or phototherapy".

### JAK-STAT-RA

- PMID:22873530 (Fleischmann 2012, ORAL Solo, N Engl J Med; DOI 10.1056/NEJMoa1109071)
  - trial_phase III: "In this phase 3, double-blind, placebo-controlled, parallel-group, 6-month study, 611 patients were randomly assigned".
  - efficacy: "At month 3, a higher percentage of patients in the tofacitinib groups than in the placebo groups met the criteria for an ACR 20 response (59.8% in the 5-mg tofacitinib group and 65.7% in the 10-mg tofacitinib group vs. 26.7% in the combined placebo groups, P<0.001 for both comparisons)"; "The percentage of patients with a DAS28-4(ESR) of less than 2.6 was not significantly higher with tofacitinib than with placebo (... P=0.62 and P=0.10 for the two comparisons)."
  - safety: "Serious infections developed in six patients who were receiving tofacitinib."; "Tofacitinib treatment was associated with elevations in low-density lipoprotein cholesterol levels and reductions in neutrophil counts."
- PMID:22873531 (van Vollenhoven 2012, ORAL Standard, N Engl J Med; DOI 10.1056/NEJMoa1112072)
  - trial_phase III: "In this 12-month, phase 3 trial, 717 patients..."
  - efficacy met: "At month 6, ACR 20 response rates were higher among patients receiving 5 mg or 10 mg of tofacitinib (51.5% and 52.6%, respectively) and among those receiving adalimumab (47.2%) than among those receiving placebo (28.3%) (P<0.001 for all comparisons). There were also greater reductions in the HAQ-DI score at month 3 and higher percentages of patients with a DAS28-4(ESR) below 2.6 at month 6 in the active-treatment groups than in the placebo group."
  - safety: "Adverse events occurred more frequently with tofacitinib than with placebo, and pulmonary tuberculosis developed in two patients in the 10-mg tofacitinib group."
- NCT:NCT00814307 (ORAL Solo; PHASE3; primaries ACR20, HAQ-DI, DAS28-4(ESR)<2.6 at month 3) and NCT:NCT00853385 (ORAL Standard; PHASE3; primaries ACR20 at month 6, HAQ-DI at month 3, DAS28<2.6 at month 6).
- PMID:25398374 (Boyle 2015, Ann Rheum Dis; NCT00976599, Phase II) — target engagement: "Changes in synovial phosphorylation of signal transducer and activator of transcription 1 (STAT1) and STAT3 strongly correlated with 4-month clinical responses (p<0.002)."
- FDA:NDA203214 (Xeljanz) — Drugs@FDA: ORIG-1, TYPE 1, approved 2012-11-06. Current label (set-id 68e3d6b2-7838-4d2d-a417-09d919b43e13): "XELJANZ tablets and XELJANZ XR (extended-release tablets) are indicated for the treatment of adult patients with moderately to severely active rheumatoid arthritis (RA), who have had an inadequate response or intolerance to one or more TNF blockers" (the 2026 label restricts to TNF-blocker-inadequate responders; the 2012 original approval was for methotrexate-inadequate responders, which the Drugs@FDA row does not state and the 2012 letter could not be retrieved).

### CD20-RA

- PMID:16947627 (Cohen 2006, REFLEX, Arthritis Rheum; DOI 10.1002/art.22025)
  - trial_phase III: "a 2-year, multicenter, randomized, double-blind, placebo-controlled, phase III study of rituximab therapy."
  - efficacy met: "At week 24, significantly more (P < 0.0001) rituximab-treated patients than placebo-treated patients demonstrated ACR20 (51% versus 18%), ACR50 (27% versus 5%), and ACR70 (12% versus 1%) responses".
  - target engagement yes: "Rituximab depleted peripheral CD20+ B cells, but the mean immunoglobulin levels (IgG, IgM, and IgA) remained within normal ranges."
  - safety acceptable: "Most adverse events occurred with the first rituximab infusion and were of mild-to-moderate severity. The rate of serious infections was 5.2 per 100 patient-years in the rituximab group and 3.7 per 100 patient-years in the placebo group."
- NCT:NCT00468546 (REFLEX; PHASE3; primary ACR20 at week 24).
- PMID:15201414 (Edwards 2004, N Engl J Med) — earlier randomized trial: "the proportion of patients with 50 percent improvement ... the primary end point, was significantly greater with the rituximab-methotrexate combination (43 percent, P=0.005) ... than with methotrexate alone (13 percent)."
- PMID:16649186 (Emery 2006, DANCER, Phase IIb): "Significantly more patients who received 2 500-mg or 2 1,000-mg infusions of rituximab met the American College of Rheumatology 20% improvement criteria ... at week 24 (55% and 54%, respectively) compared with placebo (28%; P < 0.0001)."
- FDA:BLA103705 (Rituxan) — Drugs@FDA: SUPPL-5211, EFFICACY, priority, approved 2006-02-28 (letter 103705s5211_ltr.pdf listed but not retrievable, see above). The row carries no indication text; SUPPL-5209/5230/5231 in the same year carry the Orphan property (oncology) and SUPPL-5211 does not. Current IV label (set-id b172773b-3905-4a1c-ad95-bab4b6126563, effective 2025-01-06): "RITUXAN, in combination with methotrexate, is indicated for the treatment of adult patients with moderately- to severely-active rheumatoid arthritis who have had an inadequate response to one or more TNF antagonist therapies".

### IL-4Ra-AD

- PMID:27690741 (Simpson 2016, SOLO 1 and SOLO 2, N Engl J Med; DOI 10.1056/NEJMoa1610020)
  - trial_phase III: "In two randomized, placebo-controlled, phase 3 trials of identical design (SOLO 1 and SOLO 2)".
  - efficacy met: "In SOLO 1, the primary outcome occurred in 85 patients (38%) who received dupilumab every other week and in 83 (37%) who received dupilumab weekly, as compared with 23 (10%) who received placebo (P<0.001 for both comparisons with placebo). The results were similar in SOLO 2, with the primary outcome occurring in 84 patients (36%) ... and in 87 (36%) ..., as compared with 20 (8%) who received placebo (P<0.001 for both comparisons)."
  - safety acceptable: "Injection-site reactions and conjunctivitis were more frequent in the dupilumab groups than in the placebo groups."
- NCT:NCT02277743 (SOLO 1) and NCT:NCT02277769 (SOLO 2): PHASE3; primary IGA 0/1 with >=2-point reduction at week 16.
- PMID:25006719 (Beck 2014, N Engl J Med) — target engagement (Phase I/II program): "In the 4-week monotherapy studies, dupilumab resulted in rapid and dose-dependent improvements in clinical indexes, biomarker levels, and the transcriptome."
- PMID:25482871 (Hamilton 2014, J Allergy Clin Immunol) — target engagement: "potent inhibition of TH2-associated chemokines (CCL17, CCL18, CCL22, and CCL26) were noted without significant modulation of TH1-associated genes (IFNG)."
- FDA:BLA761055 (Dupixent) — Drugs@FDA: ORIG-1, TYPE 1, approved 2017-03-28, priority. Current label (set-id 595f437d-2729-40bb-9c62-c8ece1f82780): "DUPIXENT is indicated for the treatment of adult and pediatric patients aged 6 months and older with moderate-to-severe atopic dermatitis (AD) whose disease is not adequately controlled with topical prescription therapies".

### IL-1b-CVD

- PMID:28845751 (Ridker 2017, CANTOS, N Engl J Med; DOI 10.1056/NEJMoa1707914)
  - trial_phase III: registry entry NCT01327846 is PHASE3 ("A Randomized, Double-blind, Placebo-controlled, Event-driven Trial of Quarterly Subcutaneous Canakinumab in the Prevention of Recurrent Cardiovascular Events Among Stable Post-myocardial Infarction Patients With Elevated hsCRP"; primary outcome "First CEC Confirmed Major Adverse Cardiovascular Events (MACE)"); the abstract describes "a randomized, double-blind trial ... involving 10,061 patients".
  - target engagement yes: "At 48 months, the median reduction from baseline in the high-sensitivity C-reactive protein level was 26 percentage points greater in the group that received the 50-mg dose of canakinumab, 37 percentage points greater in the 150-mg group, and 41 percentage points greater in the 300-mg group than in the placebo group."
  - efficacy met (one dose): "The 150-mg dose, but not the other doses, met the prespecified multiplicity-adjusted threshold for statistical significance for the primary end point and the secondary end point"; hazard ratios "in the 50-mg group, 0.93 (95% confidence interval [CI], 0.80 to 1.07; P=0.30); in the 150-mg group, 0.85 (95% CI, 0.74 to 0.98; P=0.021); and in the 300-mg group, 0.86 (95% CI, 0.75 to 0.99; P=0.031)."
  - safety: "Canakinumab was associated with a higher incidence of fatal infection than was placebo. There was no significant difference in all-cause mortality".
- PMID:29146124 (Ridker 2018, Lancet) — engagement-to-outcome relation: "trial participants allocated to canakinumab who achieved hsCRP concentrations less than 2 mg/L had a 25% reduction in major adverse cardiovascular events (multivariable adjusted hazard ratio [HRadj]=0.75, 95% CI 0.66-0.85, p<0.0001)".
- PMID:31882264 (Wong 2021, Trends Cardiovasc Med, epub 2019-12-06) — regulatory outcome: "The past decade also ushered in confirmation of the inflammation hypothesis of atherosclerosis with the Canakinumab Anti-Inflammatory Thrombosis Outcomes Study (CANTOS) using canakinumab, despite the fact the therapy was not approved by the Food and Drug Administration (FDA) for cardiovascular risk reduction."
- FDA:BLA125319 (Ilaris) — Drugs@FDA lists no cardiovascular efficacy supplement (efficacy supplements approved: 2013-05-09, 2016-07-21, 2016-09-23 x3, 2020-06-16, 2023-08-25). Current label (set-id 7d271f3b-e4f9-4d80-8dcf-28d49123f80e, effective 2026-06-08) indications: periodic fever syndromes, Still's disease, gout flares; no cardiovascular indication. A complete response letter is not a published Drugs@FDA document, so the decision year is not carried by any retrievable source.
- ClinicalTrials.gov: query for canakinumab, Phase 3, cardiovascular/atherosclerosis/myocardial infarction returns only NCT01327846 (CANTOS, completed 2017-03-28). Basis for development_decision = discontinued, together with the label; the sponsor's own statement is not retrievable through the permitted sources.
- PMID:30649147 (Sehested 2019, JAMA Cardiol) — context for attribution: "Canakinumab is not cost-effective at current US prices for prevention of recurrent cardiovascular events in patients with a prior MI."

## Fields coded `not reported`

None. Two values rest on inference rather than a direct statement and are flagged in the CSV
notes: IL-1b-CVD `development_decision = discontinued` (registry absence plus label) and the
IL-1b-CVD regulatory decision year (not stated in the retrievable source).

## Families whose fields disagree with the registered `drug_outcome`

- IL-1b-CVD: registered `Failed`. Coded target_engagement yes, efficacy_endpoint met (150 mg dose
  only), regulatory_outcome not approved. `Failed` holds as a regulatory/development composite and
  not as a trial-efficacy reading. Under Procedure 3 this family is engagement-yes, efficacy-met,
  so it is not a translation gap by the amendment's definition.
- IL-4Ra-AD: registered `Construct-limited`, which is an exclusion label rather than a program
  outcome; every program field reads as an approval. Listed as a kind mismatch, not a contradiction.
- CTLA-4-RA, TNF-a-RA, IL-17-psoriasis (registered `Approved`, registered classification predicted
  failure): the fields agree with `Approved`; the misses are classification misses, not outcome
  coding disagreements.
- IL-23-psoriasis, JAK-STAT-RA, CD20-RA: fields agree with `Approved`.

## Notes on target-engagement scope

The amendment asks for engagement evidence "in the pivotal program". For CD20-RA and IL-1b-CVD the
pivotal abstract itself carries the pharmacodynamic sentence. For IL-23-psoriasis the VOYAGE 1
substudy (PMID 39114670) is within the pivotal trial. For CTLA-4-RA, JAK-STAT-RA, IL-4Ra-AD and
IL-17-psoriasis the evidence is from the same drug's Phase I/II or mechanistic studies, not the
Phase III trials, and the CSV notes say so. For TNF-a-RA the evidence is from the infliximab program
(Charles 1999); the etanercept pivotal abstracts report no biomarker.
