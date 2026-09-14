# Pre-Registration Amendment 4: Revised Primary Analysis Requested During Peer Review

**Status:** DEVIATION, recorded after outcomes were known
**Date:** 2026-09-13
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9), PREREGISTRATION_AMENDMENT_2_BLIND.md (SHA: 12ea0ed), PREREGISTRATION_AMENDMENT_3_REFERENCE_CORRECTION.md
**Scope:** Records a change to the scored set and to the primary test statistic made at the request of a peer reviewer, after every drug outcome in the scored set was known. The registered analysis is unchanged and is reported beside the revised one.

**Commit SHA:** _pending_

---

## What prompted this

Reviewer 1 of *Frontiers in Pharmacology* manuscript 1933481, in a third
report dated 9 September 2026, asked that the primary analysis (a) exclude
IGF1-CRC, whose MR estimate concerns colorectal cancer risk while the Phase III
programmes scored against it were in non-small-cell lung cancer, Ewing sarcoma
and pancreatic cancer; (b) not pool conventional genetic associations with MR
estimates, which removes Complement-GA (CFH Y402H) and Serotonin-MDD (5-HTTLPR)
from the MR-instrumented set; (c) count CRP and IL-1β-CVD once, since the two
families carry identical values on every evidence field; and (d) replace or
justify the 50 per cent chance-accuracy null.

## What the registration says

`PREREGISTRATION.md` line 313: pre-specified families for which no estimate
could be found are excluded; exploratory families are labeled and excluded from
the primary hit rate; nothing else is removed. The manuscript's Family selection
section, item 4, restated this as "none is dropped once its outcome is known."
The registered exclusion criterion is construct limitation (instrument and drug
acting on different molecular entities), which none of the three families
meets.

## The deviation

A **revised primary analysis** is defined as the registered scored set with
IGF1-CRC excluded, Complement-GA and Serotonin-MDD set aside, and CRP and
IL-1β-CVD counted once: 28 families. Its primary test is an exact
outcome-permutation test with the classification held fixed (hypergeometric
null; Monte Carlo check with 10^5 permutations; a cluster-level variant that
permutes one label per shared MR instrument set). The one-sided exact binomial
against 50 per cent, which the registration specified, is reported beside it.

| analysis | scored | correct | accuracy | permutation p | binomial p |
|---|---|---|---|---|---|
| registered | 32 | 24 | 75.0% | 0.0054 | 0.0035 |
| revised primary | 28 | 23 | 82.1% | 0.0006 | 0.0005 |

All three excluded families are misclassifications under the registered rule,
so the change removes misses and no hits. Every exclusion raises accuracy; the
registered figure is the most conservative one reported.

## What is and is not changed

- The registered analysis, its denominators (27, 22, 32, 24/32) and its
  failure-mode assignments are unchanged and remain in the manuscript.
- The classification rule, the d = 0.10 threshold, the per-allele rescaling,
  and the frozen classifier commit (bf7f175) are unchanged.
- The revised primary analysis is a reviewer-requested departure from the
  registration, made with all outcomes known. It is labeled as such wherever
  it appears, and the registered analysis is reported beside it. It is not
  presented as a registered result.
- The failure-mode taxonomy was never registered (only mechanism-bypass and
  the Complement-GA replication of translation-gap were declared in advance,
  in Amendment 2) and is labeled hypothesis-generating throughout.

## Code

`analysis/revised_primary_analysis/run_revised_primary.py` computes both analyses,
the permutation tests, the contrast-stratified accuracies, and writes the
supplement `cross_design_classification_all_41_families_v3.csv`, which adds
the columns `mr_contrast`, `instrument_set` and `revised_primary_set` to the
released v2 file. Output: `revised_primary_results.json`.
