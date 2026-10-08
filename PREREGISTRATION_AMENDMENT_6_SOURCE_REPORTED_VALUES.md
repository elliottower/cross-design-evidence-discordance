# Pre-Registration Amendment 6: Source-Reported Input Values and the Published-MR-Estimate Set

**Status:** FROZEN
**Date:** 2026-10-07
**Parent documents:** PREREGISTRATION.md, PREREGISTRATION_AMENDMENT_EXPLORATORY.md, PREREGISTRATION_AMENDMENT_2_BLIND.md, PREREGISTRATION_AMENDMENT_3_REFERENCE_CORRECTION.md, PREREGISTRATION_AMENDMENT_4_REVISED_PRIMARY_ANALYSIS.md, PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md (SHA: fbc7d33)
**Scope:** Two procedures fixed before they are run. Neither changes the registered classification rule, the registered scored set or the registered accuracy (24/32), which stays the primary result. Procedure 1 repeats the analysis with source-reported values for the ten mismatched inputs that have a published figure. Procedure 2 removes the four families whose MR input has none. These are the two remedies available, and they apply to disjoint sets of values.

**Commit SHA:** 3aacce6

---

## Foreknowledge

Everything below was seen before this amendment was written.

- All 32 registered outcomes and the 8 misses are known (24/32).
- The source verification of Amendment 5 is complete. `analysis/provenance/value_origin.csv` (sha256 `e1448c4ea7bb…`) records, for each of the 64 input values, the registered value, what its source reports and the class under the source's figure. Of the 62 values checked, 43 agree with a source, 5 are author estimates and 14 do not match their source; 2 observational values (ModRisk-AD, EBV-MS) have no source named, and both belong to families Procedure 2 removes.
- That file's last column was filled by hand for each mismatched value. It reads "unchanged" for every expected outcome, and a changed label for one family (IGF1-CRC) under one of its candidate values. No script has applied the rule to source values, and no count has been computed for any set below.
- By arithmetic on the registered file, removing ModRisk-AD, EBV-MS, TNF-α-RA and IL-1β-CVD removes three hits and one miss: 21/28.
- A request made in peer review named those four families and asked that the analysis be repeated with source-reported values or without them.

## Procedure 1: the registered rule applied to source-reported values

**What it measures.** Whether any classification, expected outcome or score changes when each mismatched input is replaced by the figure its source reports.

**Scope.** The 32 registered scored families. A mismatched value with no published figure to substitute keeps its registered value here and is flagged; Procedure 2 removes those families.

**Which figure is used, where a source reports several.** In order:

1. the estimate for the exposure and outcome the family is defined on (colorectal cancer, not a subsite; any stroke, not a subtype; the pooled sample, not a stratum);
2. on the contrast of the registered value (per standard deviation where the registered value is per standard deviation);
3. from the most fully adjusted model reported;
4. where only stratum-specific estimates exist, their fixed-effect inverse-variance pooled estimate on the log scale.

The classification is also computed under each candidate figure listed in the table below, and the range of classes is reported as a bound. No figure not listed there is used, and nothing is selected from the range.

**Values fixed here.**

| Family, leg | Registered | Figure used | Rule |
|---|---|---|---|
| HRT-AD, MR | OR 1.00 (0.85–1.18) | exp(0.43) = 1.54 (0.98–2.41), estradiol on Alzheimer's disease, combined sample | 1; coefficient read as a log odds ratio. Other candidates: the stratum coefficients −0.04 (se 0.13), 0.16 (se 0.25), 0.06 (se 0.11), giving OR 0.96, 1.17, 1.06, each interval including 1 |
| Anti-CD20-MS, OBS | OR 2.23 | HR 0.14 (0.05–0.39) | 1; direction below |
| VitaminD-MS, OBS | OR 1.40 | OR 0.59 (0.36–0.97) per 50 nmol/L | 1; direction below |
| LDL/PCSK9, OBS | OR 1.52 | OR 1.54 (1.45–1.63) per SD, from the paper that reports it; the citation is corrected | 1 |
| Blood pressure, MR | OR 1.44 (1.35–1.55), coded per unit | any stroke, 1.39 (1.33–1.44) per 10 mmHg systolic | 1. Other candidate: ischemic stroke 1.41 (1.35–1.47) |
| CTLA-4-RA, MR | OR 0.86 (0.78–0.95) | 0.86 (0.78–0.96) | 1 |
| IGF1-CRC, OBS | OR 1.12, per SD (the source's figure for distal colon) | colorectal, per SD, Model 2: HR 1.11 (1.05–1.17) | 1, 2, 3. Other candidates: colorectal per SD Model 1, 1.07 (1.02–1.13), excluded by step 3; colorectal highest against lowest fifth, 1.24 (Model 1) and 1.34 (Model 2), excluded by step 2 because the registered value is per SD. Under 1.24 or 1.34 the observational leg becomes non-trivial and the family's label changes; its expected outcome does not. This is reported in the bound |
| SGLT2-HF, OBS | RR 1.75 | fixed-effect pooled on the log scale from women 1.95 (1.70–2.22) and men 1.74 (1.55–1.95): RR 1.83 (1.67–1.99) | 4. Other candidates: the two sex-specific figures |
| Complement-GA, MR | OR 2.50 (2.20–2.85) | pooled 2.50 (1.96–3.30) | 1 |
| IL-23-psoriasis, OBS | SMD 0.66 | none published; registered value kept and flagged | — |
| ModRisk-AD, EBV-MS, TNF-α-RA, IL-1β-CVD, MR | as registered | none published; registered value kept and flagged | — |

**Direction.** The registered rule classifies on the magnitude of the standardized effect. A hazard or odds ratio below 1 for a protective exposure is converted on |ln OR|, as the registered conversion does. Two registered values (Anti-CD20-MS, VitaminD-MS) are written in the opposite direction from their source; the appendix table labels them direction errors.

**Classification.** Unchanged from PREREGISTRATION.md, "Frozen classification rule (two-criterion)": an odds, hazard or risk ratio is converted as d = |ln(ratio)| × √3/π, hazard and risk ratios being treated as odds ratios; the MR leg is supportive when its confidence interval excludes 1 and d ≥ 0.10; the observational leg is non-trivial when d ≥ 0.10. Under this conversion the IGF1-CRC observational value is trivial at 1.12 (d 0.062) and at 1.11 (d 0.058), and the CTLA-4-RA MR value 0.86 is null (d 0.083).

**Prediction, and what is reported if it fails.** Every expected outcome and every score is expected to be unchanged, 24/32, with 31 of 32 families keeping non-trivial observational support. The output file marks each replaced value in a column `value_used` (`registered`, `source`, or `registered_no_source`). If any expected outcome changes, both counts are reported with the family named, and the registered count stays primary.

## Procedure 2: the published-MR-estimate set

**What it measures.** The registered accuracy on the families whose MR input is a published estimate.

**Set.** The 32 registered families without ModRisk-AD, EBV-MS, TNF-α-RA and IL-1β-CVD, using Procedure 1's figures for the 28 kept. Expected by arithmetic on the registered file: 21 correct of 28.

The criterion is applied to the MR leg, which is the leg that decides the classification. Observational values that are author estimates are already the subject of two rows of the registered analysis-set table (Amendment 5). One further observational value, IL-23-psoriasis, has no published figure. The count without that family as well (27 families; 20 correct expected by the same arithmetic) is reported as one descriptive row of the analysis-set table, with no test, and appears nowhere else in the manuscript.

**Test.** The registered outcome-permutation test (exact hypergeometric, one-sided, upper tail: the probability of an accuracy at least as high as observed when outcomes are permuted and classifications held fixed) is reported for this set at family level and at instrument-cluster level. Instrument clusters are those of the registration restricted to the 28 families; a cluster that loses all its families is dropped. It is labeled as specified after the registered analysis, with outcomes known, in a registered amendment, and as descriptive. Its membership is fixed by whether a published figure exists, not by any family's outcome. No conclusion depends on that p-value crossing 0.05; a smaller set at the same accuracy gives a larger p-value.

**Statement amended.** The analysis-set table says no test is run on sets defined after the registered analysis. It will read: no test is run on those sets except the published-MR-estimate set of this amendment.

## Reporting

- The registered 24/32 (75.0%) stays the primary result and is stated first wherever accuracy is stated.
- The published-estimate set is stated in the next sentence in the abstract and the Results. The 28-family sensitivity set of Amendment 4 (23/28) leaves the abstract and stays in the analysis-set table, so the abstract names one 28-family set.
- The analysis-set table gains three rows (Procedure 1; the published-MR-estimate set; that set without IL-23-psoriasis).
- The appendix table of mismatched values gains a column for the figure used and one for the conversion applied.
- In the Results, for the published-MR-estimate set: the count of families with non-trivial observational support, the counts in the original domains and in the blind extension, and whether the MR-only rule and the two-evidence rule give identical classifications, each recomputed and not carried over. The abstract keeps these statements for the registered set.

## Maximum claim under this amendment

With each mismatched input replaced by the figure its source reports, the registered rule gives a stated count on the 32 registered families; on the 28 families whose MR input is a published estimate it gives a stated count and a descriptive permutation p-value. The manuscript may say whether any expected outcome changed. It may not present the published-MR-estimate set as the primary analysis or call it preregistered, and may not say the result is robust, confirmed or validated by it: the set was defined with outcomes known. It may say the registered result is unchanged under source-reported values if that is what Procedure 1 returns. If Procedure 1 changes any expected outcome, the changed count is reported beside 24/32, not in place of it.

## What this amendment does not do

It does not change the registered values in the frozen classifier, which remain the record of what was registered. It does not re-derive any outcome. It does not add or remove a family from the registered scored set.

## Log

Append only.

```
2026-10-07  drafted after external review of the plan; nothing run
2026-10-07  one descriptive table row added (published-MR-estimate set without IL-23-psoriasis, no test); nothing run
2026-10-07  second external review: scope sentence, conversion formula and its source, candidate figures listed per family, pooled SGLT2-HF figure written in, test sidedness and cluster rule stated, set renamed, maximum claim extended; nothing run
2026-10-07  frozen at 3aacce6; nothing run
```
