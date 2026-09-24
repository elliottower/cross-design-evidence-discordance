# MR-availability sample: PubMed search log

Procedure: PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md, Procedure 1, "MR-availability sample" paragraph. Input: `analysis/amendment5/screen/mr_availability_sample.csv` (25 rows). Output: `analysis/amendment5/screen/mr_availability_sample_filled.csv`.

Method. For each row the `pubmed_query` string was submitted verbatim to E-utilities `esearch.fcgi` (db=pubmed, retmax=20, sort=relevance, retmode=json), and the returned PMIDs were fetched with `efetch.fcgi` (db=pubmed, retmode=xml). Every abstract returned was read in full; verdicts were not taken from titles. Calls were made with Python `urllib` under `uv run --no-project`, with no email, tool, API key or User-Agent parameter, and at least 0.4 s between calls. A first pass at 18:16 UTC hit HTTP 429 on the thirteenth row before any metadata was written and was discarded; the complete pass recorded below ran at 18:17–18:18 UTC with 1.0 s spacing and retry on 429. No row returned more than 20 results, so the number read equals the number returned in every row. Times are UTC, 2026-09-22.

Eligibility rule (frozen): a row is MR-eligible if any result reports an MR or drug-target MR estimate with a confidence interval for the target's exposure (the gene product, or the exposure it proxies) on that indication. Where an abstract reported an MR of the target on the indication but gave no numeric interval (IL12B / ankylosing spondylitis only), the open-access full text was fetched from PMC through E-utilities (`elink.fcgi` pubmed→pmc, then `efetch.fcgi` db=pmc) to check whether the paper reports a confidence interval; those calls are logged under that row.

Summary: 4 of 25 rows MR-eligible.

## ROS1-D002289 — ROS1 / Carcinoma, Non-Small-Cell Lung

- Query: `"ROS1"[All Fields] AND "mendelian randomization"[All Fields] AND ("Carcinoma, Non-Small-Cell Lung"[MeSH Terms] OR "Carcinoma, Non-Small-Cell Lung"[All Fields])`
- Run at: 2026-09-22T18:17:10+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## PPARA-D015228 — PPARA / Hypertriglyceridemia

- Query: `"PPARA"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hypertriglyceridemia"[MeSH Terms] OR "Hypertriglyceridemia"[All Fields])`
- Run at: 2026-09-22T18:17:11+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## RPE65-D057130 — RPE65 / Leber Congenital Amaurosis

- Query: `"RPE65"[All Fields] AND "mendelian randomization"[All Fields] AND ("Leber Congenital Amaurosis"[MeSH Terms] OR "Leber Congenital Amaurosis"[All Fields])`
- Run at: 2026-09-22T18:17:13+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## GRM3-D001008 — GRM3 / Anxiety Disorders

- Query: `"GRM3"[All Fields] AND "mendelian randomization"[All Fields] AND ("Anxiety Disorders"[MeSH Terms] OR "Anxiety Disorders"[All Fields])`
- Run at: 2026-09-22T18:17:14+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## CETP-D006938 — CETP / Hyperlipoproteinemia Type II

- Query: `"CETP"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hyperlipoproteinemia Type II"[MeSH Terms] OR "Hyperlipoproteinemia Type II"[All Fields])`
- Run at: 2026-09-22T18:17:15+00:00
- Results returned: 1; read: 1
- PMIDs returned (relevance order):
  - 34233476 (2021) Genome-Wide Association Study Identifies a Functional SIDT2 Variant Associated With HDL-C (High-Density Lipoprotein Cholesterol) Levels and Premature Coronary Artery Disease.
- MR-eligible: no
- Note: single result (PMID 34233476) is a GWAS of HDL-C that names CETP as a locus; it reports no MR estimate

## JAK2-D055728 — JAK2 / Primary Myelofibrosis

- Query: `"JAK2"[All Fields] AND "mendelian randomization"[All Fields] AND ("Primary Myelofibrosis"[MeSH Terms] OR "Primary Myelofibrosis"[All Fields])`
- Run at: 2026-09-22T18:17:18+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## ABCC8-D003924 — ABCC8 / Diabetes Mellitus, Type 2

- Query: `"ABCC8"[All Fields] AND "mendelian randomization"[All Fields] AND ("Diabetes Mellitus, Type 2"[MeSH Terms] OR "Diabetes Mellitus, Type 2"[All Fields])`
- Run at: 2026-09-22T18:17:28+00:00
- Results returned: 4; read: 4
- PMIDs returned (relevance order):
  - 37171501 (2023) Genetically proxied glucose-lowering drug target perturbation and risk of cancer: a Mendelian randomisation analysis.
  - 40452211 (2025) Novel Insights into the Causal Relationship between Antidiabetic Drugs and Adverse Perinatal Outcomes: A Mendelian Randomization Study.
  - 40023995 (2025) Genetic variation in targets of antihyperglycemic drugs and inflammatory bowel disease' risk: A mendelian randomization study.
  - 42328113 (2026) Genetic Evidence for the Benefits and Risks of Glucose-Lowering Drugs on Cardiovascular-Kidney-Metabolic Syndrome: A Drug-Target Mendelian Randomization Study.
- MR-eligible: no
- Note: all 4 results are drug-target MR papers with ABCC8 as the exposure and cancer, perinatal, IBD or cardiovascular-kidney-metabolic endpoints as outcomes; type 2 diabetes enters only as the GWAS used to select instruments, never as the outcome

## KCNH2-D001281 — KCNH2 / Atrial Fibrillation

- Query: `"KCNH2"[All Fields] AND "mendelian randomization"[All Fields] AND ("Atrial Fibrillation"[MeSH Terms] OR "Atrial Fibrillation"[All Fields])`
- Run at: 2026-09-22T18:17:31+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## AR-D011471 — AR / Prostatic Neoplasms

- Query: `"AR"[All Fields] AND "mendelian randomization"[All Fields] AND ("Prostatic Neoplasms"[MeSH Terms] OR "Prostatic Neoplasms"[All Fields])`
- Run at: 2026-09-22T18:17:32+00:00
- Results returned: 2; read: 2
- PMIDs returned (relevance order):
  - 40068042 (2025) The association between benign and malignant prostatic hyperplastic diseases and blood and urine biomarkers: A Mendelian randomization study.
  - 40102900 (2025) Wnt5a augments intracellular free cholesterol levels and promotes castration resistance in prostate cancer.
- MR-eligible: no
- Note: 2 results: MR of blood/urine biomarkers on prostate cancer (PMID 40068042) and a drug-target MR of PCSK9 on prostate cancer inside a Wnt5a cell study (PMID 40102900); neither has AR as the exposure

## MC4R-D009765 — MC4R / Obesity

- Query: `"MC4R"[All Fields] AND "mendelian randomization"[All Fields] AND ("Obesity"[MeSH Terms] OR "Obesity"[All Fields])`
- Run at: 2026-09-22T18:17:35+00:00
- Results returned: 11; read: 11
- PMIDs returned (relevance order):
  - 34672391 (2022) Robust estimates of heritable coronary disease risk in individuals with type 2 diabetes.
  - 24762112 (2014) Increased body mass index, elevated C-reactive protein, and short telomere length.
  - 31609059 (2019) Depression increases the genetic susceptibility to high body mass index: Evidence from UK Biobank.
  - 38754426 (2024) An integrative framework to prioritize genes in more than 500 loci associated with body mass index.
  - 25656382 (2015) Revisiting Mendelian randomization studies of the effect of body mass index on depression.
  - 19016587 (2009) How does body fat influence bone mass in childhood? A Mendelian randomization approach.
  - 40692977 (2025) Advances in Mendelian Randomization Studies of Obesity Over the Past Decade: Uncovering Key Genetic Mechanisms.
  - 23775818 (2013) Elevated body mass index as a causal risk factor for symptomatic gallstone disease: a Mendelian randomization study.
  - 23869090 (2013) Association of plasma uric acid with ischaemic heart disease and blood pressure: mendelian randomisation analysis of two large cohorts.
  - 22563304 (2012) The effect of elevated body mass index on ischemic heart disease risk: causal estimates from a Mendelian randomisation approach.
  - 26050256 (2015) Using genetics to test the causal relationship of total adiposity and periodontitis: Mendelian randomization analyses in the Gene-Lifestyle Interactions and Dental Endpoints (GLIDE) Consortium.
- MR-eligible: no
- Note: all 11 results use the MC4R rs17782313 variant as an instrument for BMI (obesity as the exposure) on other outcomes, or are gene-prioritization or review papers; no MR estimate with obesity as the outcome of an MC4R exposure

## PKLR-D000746 — PKLR / Anemia, Hemolytic, Congenital Nonspherocytic

- Query: `"PKLR"[All Fields] AND "mendelian randomization"[All Fields] AND ("Anemia, Hemolytic, Congenital Nonspherocytic"[MeSH Terms] OR "Anemia, Hemolytic, Congenital Nonspherocytic"[All Fields])`
- Run at: 2026-09-22T18:17:37+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## VEGFA-D009216 — VEGFA / Myopia

- Query: `"VEGFA"[All Fields] AND "mendelian randomization"[All Fields] AND ("Myopia"[MeSH Terms] OR "Myopia"[All Fields])`
- Run at: 2026-09-22T18:17:39+00:00
- Results returned: 1; read: 1
- PMIDs returned (relevance order):
  - 39094556 (2025) Mendelian randomization supports causal effects of inflammatory biomarkers on myopic refractive errors.
- MR-eligible: yes
- Evidence PMID: 39094556
- Supporting sentence (abstract): "Mendelian randomization analyses showed that each unit increase in VEGF-A, CD6, MCP-2 were causally related to a more myopic refractive errors of 0.040 D/pg.mL-1 (95% confidence interval 0.019 to 0.062; P = 2.031 × 10-4), 0.042 D/pg.mL-1 (0.027 to 0.057; P = 7.361 × 10-8) and 0.016 D/pg.mL-1 (0.004 to 0.028; P = 0.009), and each unit increase in TWEAK was causally related to a less myopic refractive errors of 0.104 D/pg.mL-1 (-0.152 to -0.055; P = 2.878 × 10-5)."
- Note: MR of plasma VEGF-A on spherical-equivalent refractive error (continuous myopic refractive error), not on a myopia diagnosis; two-sample MR, NSPHS exposure and UK Biobank outcome

## KCNJ11-D003924 — KCNJ11 / Diabetes Mellitus, Type 2

- Query: `"KCNJ11"[All Fields] AND "mendelian randomization"[All Fields] AND ("Diabetes Mellitus, Type 2"[MeSH Terms] OR "Diabetes Mellitus, Type 2"[All Fields])`
- Run at: 2026-09-22T18:17:44+00:00
- Results returned: 7; read: 7
- PMIDs returned (relevance order):
  - 38915894 (2024) Based on systematic druggable genome-wide Mendelian randomization identifies therapeutic targets for diabetes.
  - 37341850 (2023) Sex differences of the shared genetic landscapes between type 2 diabetes and peripheral artery disease in East Asians and Europeans.
  - 40204939 (2025) Identification and validation of five novel protein targets for type 2 diabetes mellitus.
  - 39821516 (2025) Dissecting Causal Relationships Between Antihypertensive Drug, Gut Microbiota, and Type 2 Diabetes Mellitus and Its Complications: A Mendelian Randomization Study.
  - 36042491 (2022) Genetic evidence for a causal relationship between type 2 diabetes and peripheral artery disease in both Europeans and East Asians.
  - 38750544 (2024) Genetic variations in anti-diabetic drug targets and COPD risk: evidence from mendelian randomization.
  - 42328113 (2026) Genetic Evidence for the Benefits and Risks of Glucose-Lowering Drugs on Cardiovascular-Kidney-Metabolic Syndrome: A Drug-Target Mendelian Randomization Study.
- MR-eligible: yes
- Evidence PMID: 40204939
- Supporting sentence (abstract): "Among them, CLSTN1 (OR = 0.80, 95% CI: 0.70-0.90), KCNJ11 (OR = 0.66, 95% CI: 0.60-0.73), and MLX (OR = 0.73, 95% CI: 0.65-0.82) were negatively associated with T2DM, while DLD (OR = 1.38, 95% CI: 1.15-1.65), RELA (OR = 1.90, 95% CI: 1.41-2.55), and ULK1 (OR = 1.42, 95% CI: 1.17-1.71) were positively associated with T2DM."
- Note: cis-eQTL MR of KCNJ11 expression on T2DM with colocalization support; PMID 38915894 also names KCNJ11 as a druggable-genome MR hit for T2DM but its abstract gives no estimate or CI

## ADRB2-D006973 — ADRB2 / Hypertension

- Query: `"ADRB2"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hypertension"[MeSH Terms] OR "Hypertension"[All Fields])`
- Run at: 2026-09-22T18:17:47+00:00
- Results returned: 2; read: 2
- PMIDs returned (relevance order):
  - 37964359 (2023) Nonselective beta-adrenoceptor blocker use and risk of Parkinson's disease: from multiple real-world evidence.
  - 42765498 (2026) Antihypertensive drug targets and pancreatitis reporting signals: An integrative mendelian randomization and FAERS pharmacovigilance study.
- MR-eligible: no
- Note: 2 results are MR of ADRB2 expression on Parkinson's disease (PMID 37964359) and on pancreatic outcomes (PMID 42765498); hypertension appears only as the drug-class context, never as the outcome

## APOC3-D008072 — APOC3 / Hyperlipoproteinemia Type I

- Query: `"APOC3"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hyperlipoproteinemia Type I"[MeSH Terms] OR "Hyperlipoproteinemia Type I"[All Fields])`
- Run at: 2026-09-22T18:17:49+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## RYR1-D008305 — RYR1 / Malignant Hyperthermia

- Query: `"RYR1"[All Fields] AND "mendelian randomization"[All Fields] AND ("Malignant Hyperthermia"[MeSH Terms] OR "Malignant Hyperthermia"[All Fields])`
- Run at: 2026-09-22T18:17:51+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## PPARG-D006949 — PPARG / Hyperlipidemias

- Query: `"PPARG"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hyperlipidemias"[MeSH Terms] OR "Hyperlipidemias"[All Fields])`
- Run at: 2026-09-22T18:17:52+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## NR3C1-D001249 — NR3C1 / Asthma

- Query: `"NR3C1"[All Fields] AND "mendelian randomization"[All Fields] AND ("Asthma"[MeSH Terms] OR "Asthma"[All Fields])`
- Run at: 2026-09-22T18:17:53+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## IL6R-D013167 — IL6R / Spondylitis, Ankylosing

- Query: `"IL6R"[All Fields] AND "mendelian randomization"[All Fields] AND ("Spondylitis, Ankylosing"[MeSH Terms] OR "Spondylitis, Ankylosing"[All Fields])`
- Run at: 2026-09-22T18:17:54+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query

## PPARA-D009765 — PPARA / Obesity

- Query: `"PPARA"[All Fields] AND "mendelian randomization"[All Fields] AND ("Obesity"[MeSH Terms] OR "Obesity"[All Fields])`
- Run at: 2026-09-22T18:17:56+00:00
- Results returned: 1; read: 1
- PMIDs returned (relevance order):
  - 37224770 (2023) Cross-tissue omics analysis discovers ten adipose genes encoding secreted proteins in obesity-related non-alcoholic fatty liver disease.
- MR-eligible: no
- Note: single result (PMID 37224770) is an MR of serum triglycerides on NAFLD in obese individuals; PPARA appears only as a downstream expression readout, and obesity is the cohort, not the outcome

## IL12B-D013167 — IL12B / Spondylitis, Ankylosing

- Query: `"IL12B"[All Fields] AND "mendelian randomization"[All Fields] AND ("Spondylitis, Ankylosing"[MeSH Terms] OR "Spondylitis, Ankylosing"[All Fields])`
- Run at: 2026-09-22T18:17:58+00:00
- Results returned: 2; read: 2
- PMIDs returned (relevance order):
  - 39707330 (2024) Identifying prioritization of therapeutic targets for ankylosing spondylitis: a multi-omics Mendelian randomization study.
  - 39185422 (2024) Investigating potential novel therapeutic targets and biomarkers for ankylosing spondylitis using plasma protein screening.
- MR-eligible: yes
- Evidence PMID: 39185422
- Supporting sentence (full text (PMC11341372), results section; abstract sentence: "Elevated levels of IL7R, IL12B, CCL8, IL18R1, IL23R, and ERAP1 increased AS risk, whereas elevated TYMP and TNFAIP6 levels decreased AS risk."): "Specifically, elevated IL7R (OR = 1.04, 95% CI: 1.01–1.06, P = 7.12e−03), IL12B (OR = 1.08, 95% CI: 1.05–1.11, P = 3.28e−06), CCL8 (OR = 1.03, 95% CI: 1.01–1.04, P = 1.39e−02), IL18R1 (OR = 1.01, 95% CI: 1.00–1.03, P = 4.21e−02), IL23R (OR = 1.26, 95% CI: 1.20–1.31, P = 1.01e−23), and ERAP1 (OR = 1.07, 95% CI: 1.06–1.08, P"
- Full-text fetch: PMID 39185422 → PMC11341372, elink at 2026-09-22T18:19:48+00:00, efetch at 2026-09-22T18:19:49+00:00
- Full-text fetch: PMID 39707330 → PMC11662797, elink at 2026-09-22T18:19:49+00:00, efetch at 2026-09-22T18:19:51+00:00
- PMID 39707330 full text (PMC11662797), results text: "However, FCGR2A (OR: 1.021, 95% CI 1.014–1.027), FCGR2B (OR: 1.053, 95% CI 1.036–1.071), IL12B (OR: 1.061, 95%CI: 1.038–1.085), TNFRSF1A (OR: 1.565, 95% CI 1.289–1.900) and ERAP1 (OR: 1.306, 95% CI 1.094–1.558) were positively associated with AS."
- Note: cis-pQTL MR of plasma IL12B on ankylosing spondylitis; the abstract states the direction only, and the OR with 95% CI is taken from the results text and Table 1 of the PMC full text (PMC11341372); PMID 39707330 (SMR, PMC11662797) independently reports IL12B OR 1.061 (95% CI 1.038-1.085)

## PPARG-D009765 — PPARG / Obesity

- Query: `"PPARG"[All Fields] AND "mendelian randomization"[All Fields] AND ("Obesity"[MeSH Terms] OR "Obesity"[All Fields])`
- Run at: 2026-09-22T18:18:01+00:00
- Results returned: 4; read: 4
- PMIDs returned (relevance order):
  - 38991381 (2024) Single nucleus RNA-sequencing integrated into risk variant colocalization discovers 17 cell-type-specific abdominal obesity genes for metabolic dysfunction-associated steatotic liver disease.
  - 42668868 (2026) Body Mass Index and Facial Aging: Mendelian Randomization and Exploratory Target Prioritization.
  - 37302664 (2023) Gene network based analysis identifies a coexpression module involved in regulating plasma lipids with high-fat diet response.
  - 42629059 (2026) Polygonatum kingianum polysaccharides ameliorate cognitive impairments in alcohol-exposed obese mice in a sex-specific manner by regulating the gut microbiome and metabolome.
- MR-eligible: no
- Note: 4 results: MR of abdominal obesity on MASLD (PMID 38991381), MR of BMI on perceived facial aging (PMID 42668868), a mouse liver coexpression study (PMID 37302664) and a mouse polysaccharide study (PMID 42629059); PPARG appears only as a prioritized or downstream gene, never as the MR exposure

## APOB-D006938 — APOB / Hyperlipoproteinemia Type II

- Query: `"APOB"[All Fields] AND "mendelian randomization"[All Fields] AND ("Hyperlipoproteinemia Type II"[MeSH Terms] OR "Hyperlipoproteinemia Type II"[All Fields])`
- Run at: 2026-09-22T18:18:03+00:00
- Results returned: 4; read: 4
- PMIDs returned (relevance order):
  - 38107516 (2023) Causal effects of circulating lipids and lipid-lowering drugs on the risk of urinary stones: a Mendelian randomization study.
  - 29593013 (2018) Relationship of Familial Hypercholesterolemia and High Low-Density Lipoprotein Cholesterol to Ischemic Stroke: Copenhagen General Population Study.
  - 34233476 (2021) Genome-Wide Association Study Identifies a Functional SIDT2 Variant Associated With HDL-C (High-Density Lipoprotein Cholesterol) Levels and Premature Coronary Artery Disease.
  - 42512800 (2026) From Phenotype to Genotype and Beyond: Insights into Familial Hypercholesterolemia and Familial Hypertriglyceridemia.
- MR-eligible: no
- Note: 4 results: MR of circulating apoB on urinary stones (PMID 38107516), MR of LDL-C with APOB R3500Q among the instruments on ischemic stroke (PMID 29593013), a GWAS of HDL-C (PMID 34233476) and a narrative review (PMID 42512800); no MR estimate with familial hypercholesterolemia as the outcome

## KCNJ11-D003920 — KCNJ11 / Diabetes Mellitus

- Query: `"KCNJ11"[All Fields] AND "mendelian randomization"[All Fields] AND ("Diabetes Mellitus"[MeSH Terms] OR "Diabetes Mellitus"[All Fields])`
- Run at: 2026-09-22T18:18:06+00:00
- Results returned: 9; read: 9
- PMIDs returned (relevance order):
  - 37341850 (2023) Sex differences of the shared genetic landscapes between type 2 diabetes and peripheral artery disease in East Asians and Europeans.
  - 38915894 (2024) Based on systematic druggable genome-wide Mendelian randomization identifies therapeutic targets for diabetes.
  - 40204939 (2025) Identification and validation of five novel protein targets for type 2 diabetes mellitus.
  - 39821516 (2025) Dissecting Causal Relationships Between Antihypertensive Drug, Gut Microbiota, and Type 2 Diabetes Mellitus and Its Complications: A Mendelian Randomization Study.
  - 36042491 (2022) Genetic evidence for a causal relationship between type 2 diabetes and peripheral artery disease in both Europeans and East Asians.
  - 42227366 (2026) Target Perturbation of Genetically Proxied Antidiabetic Drug Targets and Pneumonia Risk: A Mendelian Randomization Analysis.
  - 41815369 (2026) Exploration of the association of antidiabetic drugs with urolithiasis: A drug-targeted Mendelian randomization study.
  - 38750544 (2024) Genetic variations in anti-diabetic drug targets and COPD risk: evidence from mendelian randomization.
  - 42328113 (2026) Genetic Evidence for the Benefits and Risks of Glucose-Lowering Drugs on Cardiovascular-Kidney-Metabolic Syndrome: A Drug-Target Mendelian Randomization Study.
- MR-eligible: yes
- Evidence PMID: 40204939
- Supporting sentence (abstract): "Among them, CLSTN1 (OR = 0.80, 95% CI: 0.70-0.90), KCNJ11 (OR = 0.66, 95% CI: 0.60-0.73), and MLX (OR = 0.73, 95% CI: 0.65-0.82) were negatively associated with T2DM, while DLD (OR = 1.38, 95% CI: 1.15-1.65), RELA (OR = 1.90, 95% CI: 1.41-2.55), and ULK1 (OR = 1.42, 95% CI: 1.17-1.71) were positively associated with T2DM."
- Note: same paper as the KCNJ11 / type 2 diabetes row; the outcome is type 2 diabetes mellitus, a subtype under the Diabetes Mellitus heading

## NR1H4-D008105 — NR1H4 / Liver Cirrhosis, Biliary

- Query: `"NR1H4"[All Fields] AND "mendelian randomization"[All Fields] AND ("Liver Cirrhosis, Biliary"[MeSH Terms] OR "Liver Cirrhosis, Biliary"[All Fields])`
- Run at: 2026-09-22T18:18:08+00:00
- Results returned: 0; read: 0
- MR-eligible: no
- Note: no results returned by the fixed query
