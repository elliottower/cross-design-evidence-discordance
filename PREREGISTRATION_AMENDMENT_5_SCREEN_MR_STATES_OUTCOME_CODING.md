# Pre-Registration Amendment 5: Candidate-Family Screen, Three-State MR Classification, Outcome Decomposition, Analysis-Set Table, and an Instrument Deviation

**Status:** FROZEN
**Date:** 2026-09-22
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9), PREREGISTRATION_AMENDMENT_2_BLIND.md (SHA: 12ea0ed), PREREGISTRATION_AMENDMENT_3_REFERENCE_CORRECTION.md, PREREGISTRATION_AMENDMENT_4_REVISED_PRIMARY_ANALYSIS.md (SHA: 38b8f33)
**Scope:** Four procedures fixed before they are run, and one deviation from Amendment 2 disclosed. None changes the registered classification rule, the registered scored set, or the registered accuracy figure. Each procedure produces descriptive quantities the manuscript will report.

**Commit SHA:** _pending_

---

## Foreknowledge

Everything below was seen before this amendment was written, and each item is stated so that no prediction here can be read as blind to it.

- All 32 registered outcomes and the 8 misses are known (24/32; misses: VitaminD-MS, CTLA-4-RA, TNF-a-RA, IL-17-psoriasis, IGF1-CRC, Estrogen-BC, Complement-GA, Serotonin-MDD).
- The Minikel et al. 2024 dataset (`paper/reference/minikel_data/table_s01.tsv`, 25,713 target-indication pairs) has been profiled to design the screen: 3,070 pairs have a combined maximum phase of Phase III or Launched; 279 of these carry a genetic association in Minikel's sense (`target_status = genetically supported target`); of the 279, `succ_3_a` is TRUE for 189, FALSE for 30, and blank for 60. Seventeen of the 32 scored families were matched to this dataset in the registered cross-tabulation (commit 22dbc7f). No family-level coverage count has been computed.
- The three-state MR rule below has not been applied to any family. Which families would move from "null" to "inconclusive" has not been computed.
- The outcome fields below have not been coded for any family.
- The analysis sets in Procedure 4 have been named but not scored, except the registered set (24/32) and the Amendment 4 set (23/28), both already reported.
- Seen in the supplementary table while writing this amendment: HDL/CETP and Niacin/HDL are identical on every evidence column; CRP and IL-1β-CVD, which Amendment 4 counts once, differ on the MR interval, the MR contrast and the outcome. The `drug_outcome` field takes five values (Approved, Failed, No benefit, Pending, Construct-limited).
- The Amyloid-AD drug holdout codes the anti-amyloid programs Failed on 12 of 14; two are approvals.
- Seven scored families carry an author-estimated observational value (listed in Procedure 4); all seven are known to fall on the non-trivial side, and three of the seven are misses under the registered rule (CTLA-4-RA, Complement-GA, Serotonin-MDD), four are hits (IL6-MDD, JAK-STAT-RA, CD20-RA, Eos/IL5-Asthma). By subtraction the source-extracted set is 20/25; the row is registered so that the figure is reported whatever the script returns.

## Disclosed deviation: the IL6-MDD genetic instrument

Amendment 2 declared family B1 (IL-6 signaling → MDD) with IL6R cis-pQTL instruments (rs2228145, rs4129267), CRP on a per-SD scale as the exposure readout, the outcome coded Failed on sirukumab's Phase II trial in treatment-resistant MDD (Boyle et al. 2020), and the prediction discordance → failure. Amendment 2 coded every outcome before any effect size was retrieved, by design, so the effect sizes for every extension family, this one included, were extracted with the outcome known. The estimate retrieved and used by the frozen classifier is a polygenic CRP Mendelian randomization estimate (OR 1.01, 95% CI 0.99–1.04 per unit CRP; classifier note: "genetically predicted CRP (>500 instruments) and depression, bidirectional MR, UK Biobank"): genome-wide CRP instruments in place of the IL6R-region instruments the declaration named. The supplementary table records `instrument_type = cis_pqtl` and `instrument_set = CRP GWAS`, which contradict each other, and the manuscript cites Elliott et al. 2009 (CRP loci and coronary heart disease) for the estimate, which is the wrong paper.

Two further facts about the family are stated here so that the whole deviation is in one place. Sirukumab neutralizes the IL-6 ligand; the declared instrument is variation at the IL-6 receptor; the estimate used is downstream CRP. Ligand blockade, receptor variation and CRP concentration are three different perturbations, and the family carries the alignment flag `instrument–target mismatch` in Procedure 2 under either instrument. The readout is Phase II, and the family inclusion rule requires a Phase III readout; Procedure 4 handles this as a set definition.

Registered here, before any recount: (1) the family's `instrument_type` is corrected to `biomarker_gwas`; (2) the accuracy-by-instrument-type table is recomputed with that single change and the manuscript reports the recomputed counts (expected: cis-pQTL 7/7, biomarker GWAS 7/12); (3) the source of the retrieved estimate is identified and cited, and if it cannot be identified the estimate is withdrawn from the family; (4) the family is additionally classified on the instrument Amendment 2 declared, selected by the rule below. The two classifications have fixed roles. The classifier's estimate is the frozen-implementation analysis and stays in the registered count (24/32). The IL6R-region estimate is the registration-consistent analysis, reported as a sensitivity analysis and as a row of the Procedure 4 table. Neither is chosen by which scores correctly.

**Selection rule for the registration-consistent estimate.** The PubMed query `IL6R AND "mendelian randomization" AND (depression OR "major depressive disorder")` is run on the date recorded in the log and every result is screened. A result is eligible if it reports an instrumental-variable estimate of IL6R-region variation (cis instruments only; soluble IL-6R, IL-6 or CRP as the exposure readout are all eligible when the instruments are IL6R-region) on depression with a 95% confidence interval. Among eligible results the estimate is chosen by, in order: (a) peer-reviewed article over preprint; (b) clinically defined MDD over a symptom score; (c) largest number of MDD cases; (d) most recent publication year; (e) lowest PMID. The estimate taken is the one the paper reports as primary. Its direction is recorded as the paper reports it, with a note of which direction indexes reduced IL6R signaling; the registered rule is sign-blind, so direction does not enter the classification. Every candidate and its rejection reason are recorded.

Foreknowledge for item (4), stated because it was seen while writing this amendment: published IL6R-instrumented MR estimates for depression are not uniformly null. Dardani et al. (bioRxiv 10.1101/712133, PGC MDD, 135,458 cases) report a causal effect of circulating IL-6 on MDD (OR 0.85 per natural-log increase, 95% CI 0.75–0.96, where higher circulating IL-6 under IL6R variants indexes lower receptor signaling), and Kelly et al. 2021 (*Brain Behav Immun*, PMID 33631287, UK Biobank n = 89,119) report soluble IL-6R on depression at OR 1.023 (95% CI 1.006–1.039). On the Chinn conversion these give d = 0.090 and d = 0.013, both below the 0.10 floor, so both would be null under the registered rule. Under criterion (a) a peer-reviewed estimate takes precedence over the Dardani preprint. Whether the estimate the rule returns is one of these two is not known. Palmos et al. 2023 (PMID 36712567) report cis-CRP variants on MDD at OR 1.03 (1.00–1.05) and 1.02 (0.97–1.06), neither of which is the 1.01 (0.99–1.04) the classifier holds, so the retrieved estimate's source remains unidentified at this writing. The family's registered score is unchanged only if the registration-consistent estimate is null at d = 0.10. If it is not, the family becomes concordant, predicts success, and scores as a miss against sirukumab's failure; the manuscript then reports the registered count as it stands (24/32, frozen implementation) beside the registration-consistent count (23/32).

**Maximum claim under this disclosure.** The manuscript may report the family under both instruments, say which the registration named, and say which the frozen classifier used. It may not choose between them on the basis of which scores correctly.

## Procedure 1: candidate-family screen

**What it measures.** How much of an auditable universe of genetically supported, Phase III-resolved target-indication pairs the paper's scored families cover. It is a coverage measurement against a fixed external universe, not an enumeration of every family the registered inclusion rule would admit; the manuscript says so.

**Universe.** Every row of `table_s01.tsv` with `combined_max_phase` in {Phase III, Launched} and `target_status = genetically supported target`. Expected size 279. Rows with `succ_3_a` blank are carried as "Phase III outcome pending"; the resolved universe is the 219 rows with `succ_3_a` TRUE or FALSE.

**Mapping.** A scored family covers a universe row when the family's gene target (`GENE_TARGET_MAP` in `paper/reference/reviewer_analyses.py`, committed 4b0a652) equals the row's `target` and the family's indication maps to the row's `indication_mesh_term` under `MINIKEL_INDICATION_MAP` in the same file. Both maps are frozen as they stand at this amendment's commit. Each family receives a match status: exact target and indication; exact target, broader indication; pathway proxy; polygenic, unmappable; no record. Two coverage counts are reported: exact coverage counts a universe row as covered only under the first status; expanded coverage also counts the second and third. Polygenic families cannot map and are reported as such.

**Outputs, all reported.** (1) The resolved universe size and its outcome split. (2) The number of universe rows covered by a scored family under exact and under expanded coverage, and the number of scored families with each match status. (3) The full list of uncovered rows, by target and indication, as a supplementary table.

**MR-availability sample.** Twenty-five uncovered rows are drawn at random from the resolved universe with seed 20260922, and for each the author searches PubMed with the fixed query `"<target>"[All Fields] AND "mendelian randomization"[All Fields] AND ("<indication_mesh_term>"[MeSH Terms] OR "<indication_mesh_term>"[All Fields])`, reading up to the first 20 results. A row is "MR-eligible" if any result reports an MR or drug-target MR estimate with a confidence interval for the target's exposure on that indication. The fraction MR-eligible in the sample estimates the fraction of the uncovered universe the registered inclusion rule would have admitted. Search results and verdicts are recorded per row.

**Maximum claim under Procedure 1.** The manuscript may state the size of the resolved universe, the exact and expanded fractions of it the scored families cover, the match status of each family, and a sample-based estimate of how much of the uncovered universe would be eligible. It may not state that the scored families are a random or representative sample of eligible families, and it may not report a coverage percentage of "all eligible families"; the screen measures the gap against one external universe.

## Procedure 2: three-state MR classification

The registered rule has two MR states. A third is added for reporting, without changing the registered rule or any registered figure.

- **Supportive:** the confidence interval excludes the null and $|d_{\text{MR}}| \geq 0.10$ (the registered "causal").
- **Interval within the negligible range:** both interval bounds, converted to signed $d$, lie strictly inside $(-0.10, 0.10)$: $-0.10 < d_{\text{lower}}$ and $d_{\text{upper}} < 0.10$. A bound at exactly $\pm 0.10$ fails the containment.
- **Inconclusive:** every other case, including any family whose MR estimate carries no confidence interval and any family whose interval reaches $\pm 0.10$.

Conversion is applied to the point estimate and both bounds alike: $d_j = \ln(\text{OR}_j)\,\sqrt{3}/\pi$ for $j \in \{\text{lower}, \text{point}, \text{upper}\}$. Per-allele families with a registered conversion factor $s$ (SD of exposure per allele; the frozen classifier holds one, IL-6R, $s = 0.34$, `sd_per_allele` in `analysis/classifier/classify_families.py`) use $d_j = \ln(\text{OR}_j)\,\sqrt{3}/(\pi s)$, with $s$ treated as fixed. Per-allele families without a conversion factor enter unrescaled, as they did in the registered classification, and are marked `scale-unresolved`: they can be supportive or inconclusive but not within the negligible range, because an unrescaled per-allele interval inside $(-0.10, 0.10)$ does not bound the per-SD effect. The source intervals are 95% intervals; a 95% interval inside the range is a stricter condition than the 90% interval the two-one-sided-tests procedure uses at $\alpha = 0.05$, and no equivalence test is claimed. The state is reported for all 41 families as a supplement column, beside an alignment flag (`aligned` / `indication mismatch` / `instrument–target mismatch` / `construct-limited`) taken from the family's existing status and the Table 5 criteria, and accuracy is reported by state. No family's registered classification or scored outcome changes.

**Maximum claim under Procedure 2.** The manuscript may report how many "null" families have an interval within the negligible range, how many are inconclusive, how many are scale-unresolved, how many carry an alignment flag, and the accuracy within each. It may not reassign a miss on this basis, and it may not call the negligible-range state an equivalence-test result. The range is the registered threshold, not a clinically validated margin, and the states are not comparable across per-SD, per-unit and per-allele contrasts; the manuscript says both.

## Procedure 3: outcome decomposition

Seven fields are coded for each of the 41 families from the trial or regulatory sources already cited for that family, adding a source where the cited one does not carry the field. Every value carries its source identifier (PMID, DOI, or trial registry number).

| field | values | rule |
|---|---|---|
| trial phase | II / III / post-marketing / mixed class | the phase of the readout on which `drug_outcome` was coded, for the family's exact indication |
| target engagement | yes / no / unclear / not measured | pharmacodynamic or biomarker evidence that the intended target was modulated |
| efficacy endpoint | met / not met / mixed / not tested | the primary endpoint of the pivotal program; mixed if programs disagree |
| safety outcome | acceptable / limiting / unclear | whether safety or tolerability determined the development outcome |
| development decision | advanced / discontinued / ongoing / sponsor withdrawal | the sponsor's action, separated from the evidence |
| regulatory outcome | approved / not approved / not submitted / pending | for the family's indication, FDA or EMA, with jurisdiction and year |
| outcome attribution | target / molecule / dose / design / indication / commercial / uncertain | the author's reading, coded last and labeled as a reading |

The registered `drug_outcome` field is kept unchanged. It combines regulatory status, efficacy readouts and development decisions; the seven fields decompose that composite and do not redefine it. They are reported beside it in a supplementary table; a translation gap is read only where engagement is yes and efficacy is not met. Families where the fields disagree with the registered outcome are listed. The author codes alone; that is stated, and the attribution column is labeled as a single-coder reading.

**Maximum claim under Procedure 3.** The manuscript may report the seven fields per family and how many misses show engagement without efficacy. The registered accuracy is unchanged; the decomposition describes the misses, it does not rescore them.

## Procedure 4: analysis-set table

One table reports the number scored and the number correct across the following sets, all named here before scoring. The registered binomial and outcome-permutation p-values are reported for the registered set and the Amendment 4 set, where they already exist; no test is run on the other sets.

| set | definition |
|---|---|
| registered | the 32 scored families, as registered (24/32, already reported) |
| strict Phase III | registered families whose Procedure 3 trial-phase field is III or post-marketing for the family's indication; every family the rule removes is listed. IL6-MDD is the one Phase II readout known at this writing; any other Procedure 3 finds is removed by the same rule |
| Amyloid-AD scored | the registered set plus Amyloid-AD, its observational estimate and the APOE4 association (manuscript §3.5) classified under the registered rule and scored against the drug holdout's coding of the anti-amyloid programs (Failed, on 12 of 14) |
| strict Phase III + Amyloid-AD | both changes together |
| MR-instrumented | registered families whose genetic leg is an instrumental-variable estimate (MR or drug-target MR) with a confidence interval, audited for all 32 from the cited source; families whose genetic leg is a variant–disease association are removed and listed. Complement-GA and Serotonin-MDD are known to fail this; whether any other family does is decided by the audit |
| registration-consistent instrument | the registered set with IL6-MDD classified on the estimate the selection rule above returns |
| unique-evidence | families identical on `obs_d`, `mr_or_raw`, `mr_ci`, `instrument_set` and `drug_outcome` counted once. HDL/CETP and Niacin/HDL are identical on all five; CRP and IL-1β-CVD, counted once in Amendment 4, differ on `mr_ci` and `drug_outcome` and are not collapsed by this rule |
| Amendment 4 | the set Amendment 4 defines (23/28, already reported) |
| source-extracted OBS | registered families whose observational value was extracted from a published source; the seven scored families whose observational value is author-estimated (dagger-marked in the manuscript's tables: CTLA-4-RA, JAK-STAT-RA, CD20-RA, Eos/IL5-Asthma, Complement-GA, Serotonin-MDD, IL6-MDD) are removed |

Each row states which families differ from the registered set. The registered set remains the primary analysis; the table is reported whole, and no set is promoted on the basis of its accuracy. The rows differ from the registered set by one to seven families, and 25 to 33 families cannot distinguish accuracies that differ by that much; the manuscript states that the analysis-set and subgroup comparisons are descriptive and underpowered.

**Maximum claim under Procedure 4.** The manuscript may report the table and say which choices move the accuracy and by how much. It may not select a set after seeing the table, and it may not report a significance test on any set other than the two already tested.

## What this amendment does not do

It does not change the registered classification rule, threshold, scored set, or any accuracy figure. It does not register a hypothesis; each procedure is descriptive, and the numbers it produces are reported whatever they are, including a coverage fraction or an analysis set that embarrasses the registered result.

## Log

Append only.

```
2026-09-22  drafted; nothing run                                   nothing run
2026-09-22  redrafted after external review: signed bounds in Procedure 2, alignment flag, seven-field codebook for all 41 families, Procedure 4 analysis-set table, IL6-MDD instrument deviation disclosed   nothing run
2026-09-22  source-extracted-OBS analysis set added to Procedure 4 (seven author-estimated families removed)   nothing run
2026-09-22  second external review: |d| in the supportive state, bound-wise rescaling with scale-unresolved handling, deterministic selection rule and fixed roles for the two IL6-MDD instruments, ligand/receptor/CRP alignment and Phase II stated in the deviation, drug_outcome described as a composite, Procedure 4 sets defined algorithmically and split (strict Phase III, Amyloid-AD, MR-instrumented, registration-consistent instrument, unique-evidence), exact and expanded coverage, covered-versus-uncovered outcome comparison and p-values on new sets dropped   nothing run
```
