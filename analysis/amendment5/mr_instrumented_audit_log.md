# MR-instrumented audit log

Audit of the `MR-instrumented` row of the Procedure 4 analysis-set table in
`PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md`: "registered families
whose genetic leg is an instrumental-variable estimate (MR or drug-target MR) with a
confidence interval, audited for all 32 from the cited source; families whose genetic
leg is a variant--disease association are removed and listed."

Date run: 2026-09-22. Output: `analysis/amendment5/mr_instrumented_audit.csv`.

## Scored set

The 32 rows of `data/cross_design_classification_all_41_families_v3.csv` whose `status`
is `pre-registered` or `extension`, whose `classification` is not `null concordance`, and
whose `correct` column is `True` or `False`: 22 pre-registered plus 10 extension. Count
verified programmatically against the audit file; the two sets are identical with no
family missing and none extra. `Uric acid` (null concordance), `Lp(a)`, `BMI-MS` and
`IL-6R` (pending) and the five construct-limited families are outside the set.

## Sources and method

Each family's genetic-leg source was taken from `paper/supplementary_data.csv` (the
`GEN` row's `source` field) for the pre-registered families and from the dict comments in
`analysis/classifier/classify_families.py` for the extension families, cross-checked
against `data/effect_sizes_v12.csv` and `paper/references.bib`. Sources cited by
author-year were resolved to a PMID by title or author search; every resolution is listed
below. Design quotes are from the source's own abstract as returned by the Europe PMC REST
API (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<pmid>%20AND%20SRC:MED&resultType=core&format=json`),
with PubMed E-utilities `esearch`/`esummary` used for searches. No email address, `email=`,
`mailto` or API key was sent in any request; no browser was driven and no User-Agent
was spoofed; no publisher page was fetched.

## Author-year resolutions

| cited as | resolved to | how |
|---|---|---|
| Voight 2012 (HDL/CETP, Niacin/HDL) | PMID 22607825, Lancet 2012 | Europe PMC title search, `TITLE:"Plasma HDL cholesterol and risk of myocardial infarction: a mendelian randomisation study"` |
| Clarke 2012 (Homocysteine) | PMID 22363213, PLoS Med 2012 | Europe PMC, `TITLE:"Homocysteine and coronary heart disease" AND TITLE:"MTHFR"` |
| Elliott 2009 (CRP) | PMID 19567438, JAMA 2009 | Europe PMC title search |
| Holmes 2015 (LDL/PCSK9, Triglycerides) | PMID 24474739, Eur Heart J 2015 | Europe PMC title search |
| Georgakis 2020 (Blood pressure) | PMID 32611631, Neurology 2020 | Europe PMC, `TITLE:"antihypertensive drug classes" AND TITLE:"stroke" AND AUTH:"Georgakis"` |
| Thomsen/Nordestgaard 2020 (Metabolic-AD) | PMID 32326995, Epidemiol Psychiatr Sci 2020 (Thomassen JQ et al.) | Europe PMC, `TITLE:"type-2 diabetes" AND TITLE:"dementia" AND TITLE:"Mendelian"`; matched on the "1 million individuals" sample the ledger records as "Danish 1M / IGAP" |
| MR of modifiable risk factors (ModRisk-AD) | PMID 29212772, BMJ 2017 (Larsson SC et al.) | named in `data/effect_sizes_v12.csv` row AD-021; abstract confirms the design |
| MR of smoking (Smoking-MS/AD) | PMID 33253141, PLoS Biol 2020 (Mitchell RE et al.) | PubMed `smoking[ti] AND multiple sclerosis[ti] AND Mendelian randomization`; matched on OR 1.03 and the IMSGC 14,802/26,703 sample. Vandebergh 2020 (PMID 32529581) is a second null smoking-MS MR |
| Barth 2025 (HRT-AD) | PMID 41350255, Nat Commun 2025 (Oppenheimer H et al.) | PMID carried in `paper/references.bib` key `barth2025` |
| Lin 2023 (Anti-CD20-MS) | PMID 36864689, Brain 2023 | `paper/references.bib` key `lin2023`; FCRL3 OR 0.83 (0.79--0.89) matches |
| Guyatt 2023 (Eos/IL5-Asthma) | PMID 35537820, Thorax 2023 | Europe PMC, eosinophils + asthma + `JOURNAL:"Thorax"` |
| PMC11079590 (SGLT2-HF) | PMID 38725835, Front Cardiovasc Med 2024 (Luo J et al.) | Europe PMC `PMCID:PMC11079590` |
| PMC6333326, cited as "Li 2019" (Urate-Gout) | PMID 30645594, PLoS Med 2019 (Jordan DM et al.) | Europe PMC `PMCID:PMC6333326`; the record is Jordan et al., not Li |
| Clarke 2010 (Serotonin-MDD) | PMID 20380781, Psychol Med 2010 | Europe PMC title search |
| Thakkinstian 2006 (Complement-GA) | PMID 16905558 | PMID carried in the bibliography |
| Zhu 2012 / Daha 2009 / Lee 2010 / Wu 2021 / Li 2025 / Yuan 2020 | PMIDs 22706445, 19404967, 19479340, 33188428, 40618325, 32223966 | PMIDs carried in `paper/supplementary_data.csv` and the bibliography; abstracts fetched to confirm design |

## Verdicts

23 MR-instrumented, 5 association, 4 unresolved.

### Association (5)

Each of the five is a variant--disease odds ratio: the source instruments no exposure,
computes no IV estimate, and describes its own design as an association study or
association meta-analysis.

**IL-23-psoriasis** (PMID 22706445, Zhu 2012): "We conducted a meta-analysis to examine
the association between the IL23R rs11209026 (Q381R), rs7530511 (L310P), and rs2201841
polymorphisms and psoriasis/PsA." The value used, 0.616 (0.563--0.674), is the minor-allele
OR of rs11209026 for psoriasis.

**CTLA-4-RA** (PMID 19404967, Daha 2009): "The aim of the present study was to
independently replicate 3 recently described RA susceptibility loci, STAT4, IL2/IL21, and
CTLA4, in a large Dutch case-control cohort, and to perform a meta-analysis of all
published studies to date." CTLA4 rs3087243, reported at OR 0.87 (Dutch cohort) and 0.91
(meta-analysis); the classifier's 0.86 (0.78--0.95) is not printed in the abstract.

**JAK-STAT-RA** (PMID 19479340, Lee 2010): "Studies on STAT4 rs7574865 single nucleotide
polymorphism (SNP) of RA and SLE were identified using PubMed... The overall ORs for the
minor T allele of STAT4 rs7574865 SNP were 1.27 (95% CI 1.20--1.34) in RA." Matches the
classifier exactly.

**Complement-GA** (PMID 16905558, Thakkinstian 2006): "A meta-analysis of eight studies
assessing association between the CFH Y402H polymorphism and AMD was performed," with
"those having CC and TC genotypes being roughly six and 2.5 times more likely to have AMD
than patients with TT genotype." Named in Amendment 5 as a known failure of this rule.

**Serotonin-MDD** (PMID 20380781, Clarke 2010): "Meta-analysis indicated evidence of a
small but statistically significant association between the 5-HTTLPR polymorphism and
unipolar depression [odds ratio (OR) 1.08, 95% confidence interval (CI) 1.03--1.12]."
Matches the classifier exactly. Named in Amendment 5 as a known failure of this rule.

### Unresolved (4)

**BMI-AD.** `paper/supplementary_data.csv` names the genetic leg only as "Life-course MR
BMI-AD (near null)". No PMID or DOI for OR 1.03 (1.01--1.05) appears anywhere in the
repository. Nordestgaard 2017 (PMID 28609829), the closest published BMI--AD MR, reports
0.98 (0.77--1.23) per 1 kg/m² and 1.02 (0.86--1.22) per SD. PubMed and Europe PMC searches
on BMI / obesity / adiposity × Alzheimer × Mendelian randomization returned no source
reporting 1.03 (1.01--1.05).

**EBV-MS.** No source in the repository reports OR 5.0 (95% CI 2.0--20.0).
`data/cross_design_classification_all_41_families_v3.csv` codes the genetic leg
`instrument_type = coding_variant`, `gene_target = HLA`, `mr_contrast = per_allele`, which
describes a variant--disease association; `paper/supplementary_data.csv` says "MR of EBV
and MS (d~1.92)" with every numeric field blank. The repository's own HLA-DRB1*15:01
meta-OR is 3.06 (2.30--4.08) (PMID 26656273) and its EBV estimate is HR 32.4 (4.3--245)
(PMID 35025605); neither matches the value used. If the leg is the HLA-DRB1*15:01
association, the family fails the MR-instrumented rule.

**CD20-RA.** The two repository files name different sources of different kinds:
`paper/supplementary_data.csv` gives "FCRL3 proteomics MR (SSRN 4709115)", the classifier
comment gives "FCRL3 GWAS OR 2.15 (Kochi 2005, Nature Genetics)". The SSRN preprint is not
indexed in PubMed or Europe PMC, and publisher pages were out of scope; Kochi 2005's 2.15
does not match the value used, 1.291 (1.19--1.391).

**IL6-MDD.** Amendment 5's disclosed deviation already records that the source of the
estimate the classifier holds, OR 1.01 (0.99--1.04), is unidentified: the manuscript cites
Elliott 2009 (CRP loci and coronary heart disease), which is the wrong paper, and Palmos
2023 (PMID 36712567) reports 1.03 (1.00--1.05) and 1.02 (0.97--1.06). A Europe PMC search
for a bidirectional UK Biobank CRP--depression MR matching 1.01 (0.99--1.04) returned no
such record.

## Two families that turn on how the rule is read

**Homocysteine** (PMID 22363213) reports a TT-vs-CC genotype OR, 1.02 (0.98--1.07), the
shape the audit brief flags as an association. The source nonetheless frames and computes
the design as instrumental-variable: "the TT genotype of the common C677T polymorphism
(rs1801133) of the methylene tetrahydrofolate reductase gene (MTHFR) appreciably increases
homocysteine levels, so 'Mendelian randomization' studies using this variant as an
instrumental variable could help test causality," and it states the exposure contrast the
genotype stands for (~20% higher homocysteine in TT). Scored MR-instrumented, with the
caveat that the reported figure is the unscaled genotype contrast rather than an effect per
unit homocysteine.

**IL-17-psoriasis** (PMID 33188428) is an IV design — "SNPs at genome-wide significance
from GWASs on TNF-α, IL-12p70 and IL-17 were identified as the instrumental variables" —
but reports betas with standard errors rather than an OR with a confidence interval, and
its outcome is psoriatic arthritis rather than psoriasis. The classifier's 0.998 carries no
CI. Scored MR-instrumented on design; it fails the "with a confidence interval" half of
the rule as stated.

## Citation defects found while auditing

- `data/effect_sizes_v12.csv` row AD-020 cites PMID 32330418 for the T2D→AD MR estimate.
  That PMID resolves to "Non-coding and Loss-of-Function Coding Variants in TET2 are
  Associated with Multiple Neurodegenerative Diseases" (Am J Hum Genet 2020), an unrelated
  rare-variant burden study. The intended source is PMID 32326995.
- The classifier comment for Urate-Gout attributes PMC6333326 to "Li 2019, PLOS Med". The
  record is Jordan DM et al. 2019, and the gout figures used (OR 3.41--6.04 per 1 mg/dL)
  are that paper's positive control, not its headline result, which is a null effect of
  urate on chronic kidney disease.
- `paper/references.bib` key `li2019uratemr` points to PMID 28592419, a 2017 umbrella
  review of serum urate and multiple health outcomes, not the MR the Urate-Gout family
  uses.
- `paper/references.bib` key `nie2015il23r` carries PMID 20485703 (2010) under a 2015
  author-year. The family it serves, IL23-Crohns, is construct-limited and outside the
  scored set.
- Several families' point estimates are not printed in the abstract of the source they
  cite and were not verified against full text: ModRisk-AD (1.10, no CI, against 24
  reported exposures), HRT-AD (1.00, 0.85--1.18), LDL/PCSK9 (1.78, 1.58--2.01) and Blood
  pressure (1.44, 1.35--1.55). Each source's design is unambiguously MR; the specific
  number's provenance is not established by this audit.

## Post-audit resolution (same day)

IL6-MDD: the stored estimate OR 1.01 (0.99–1.04) was identified by the Amendment 5 IL6-MDD search as Galan et al. 2022, *Sci Rep*, PMID 36057695 (bidirectional two-sample MR, 512 CRP instruments, UK Biobank; Table 3, CRP → Depression). It is an instrumental-variable estimate with a confidence interval; verdict changed from unresolved to MR-instrumented in `mr_instrumented_audit.csv`. See `analysis/amendment5/il6_mdd/il6_mdd_source_and_selection.md`.

## Second resolution pass (2026-09-22, literature search, checked on PubMed)

- BMI-AD: Li et al. 2021, J Alzheimers Dis 82(2):503-512, PMID 34057091. Abstract: "Genetically predicted 1-SD increase in adult BMI was significantly associated with higher risk of AD (IVW: OR = 1.03, 95% confidence interval [CI] = 1.01-1.05, p = 2.7×10-3)". Verdict: MR-instrumented.
- CD20-RA: SSRN 4709115 (2024 preprint), OR 1.291 (1.190-1.391) for genetically predicted plasma FCRL3 on RA, as reported by the search; not in PubMed, not read directly. Verdict: MR-instrumented, provenance flagged.
- Metabolic-AD: stored OR 1.01 matches Walter et al. 2016, Alzheimer Dis Assoc Disord 30(1):15-20, PMID 26650880: "OR for the T2D polygenic score=1.01; 95% confidence interval (CI), 0.96, 1.06". Verdict unchanged (MR-instrumented); catalog PMID corrected in notes.
- EBV-MS: unresolved. No source reports 5.0 (2.0-20.0); nearest are observational infectious-mononucleosis estimates.
