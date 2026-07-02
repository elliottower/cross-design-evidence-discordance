# MechVal Quantitative Analysis — EXTENSION SPEC (Next Steps)

**Companion to:** mechval_analysis_suite.py (the working code file)
**Current state:** 16 effect-size rows (cited subset), tier-calibration Kendall tau=0.89 (p=0.009,
DESCRIPTIVE, n=7 risk ORs), cross-domain forest plot, and a runnable real-GWAS MR module.
**Goal of extension:** move from a *proof-of-concept on the cited subset* to a *properly-powered,
defensible cross-domain meta-analysis* — the analytical centerpiece for the Xia meeting + Astro site.

---

## GUARDRAILS (carry forward — these are what make it credible)
1. NEVER fabricate an estimate. Missing = NaN + a `gap_reason`. A biostatistician will check.
2. Provenance on every row (PMID/DOI, table/figure number, extracted-by, date).
3. Never pool across incompatible scales (ratio vs proportion vs percent-slowing vs r2).
4. Label small-n / non-systematic analyses DESCRIPTIVE; only call something inferential after a
   pre-registered, systematic extraction.
5. Distinguish MR estimates (causal) from observational associations (confounded) in a `design` column.

---

## PHASE 1 — Scale the extraction (turns tau=0.89 from anecdote into a result)
**Target:** 40-60 rows spanning ALL quantitative cases in both catalogs (currently 16).
**Tasks:**
- Add columns: `design` (MR|RCT|observational|genetic|diagnostic), `n_cases`, `n_controls`,
  `population` (ancestry), `pmid`, `extracted_by`, `extract_date`, `gap_reason`.
- Systematically pull estimates for every MS case 001-052 and AD case 001-010/C1-C3 that reports a
  number. Prioritize: all MR cases, all HLA/APOE/GWAS ORs, all biomarker HRs, all DMT/anti-amyloid RCTs.
- Data sources: the already-cited papers first; then for gaps, PubMed (eutils, reachable) + the trial
  registries. One estimate per case per outcome (the primary/most-adjusted).
**Deliverable:** mechval_effect_sizes_v2.csv (>=40 numeric rows), a QC report of gap_reasons.
**Analysis unlocked:** re-run tier_calibration() with n~30 risk ORs -> if tau holds, it is now a
powered meta-scientific claim ("expert tiering is calibrated to effect magnitude, tau=X, p<0.05, n=30").

## PHASE 2 — Proper random-effects meta-analysis within comparable clusters
**Target:** pooled estimates + heterogeneity, per homogeneous cluster (NOT across everything).
**Clusters (examples):** {MS MR risk factors}, {AD MR risk factors}, {AD anti-amyloid RCTs CDR-SB},
{p-tau217 diagnostic accuracy studies}.
**Tasks:**
- Use `statsmodels` or `PythonMeta`/`metafor`(R) for DerSimonian-Laird random-effects pooling.
- Report pooled effect, 95% CI, I^2, tau^2, prediction interval, and Egger's test for small-study bias
  where >=10 studies.
- For diagnostic markers (p-tau217): bivariate SROC (sensitivity/specificity) meta-analysis, NOT simple pooling.
**Deliverable:** forest plot + funnel plot per cluster; a pooled-estimates table.
**Guardrail:** only pool when clinically/methodologically homogeneous; otherwise report separately.

## PHASE 3 — Real re-analysis on open data (the "we re-ran it" credibility)
**3a. Mendelian randomization (script already drafted -> productionize):**
- Replace the simplified IVW with the full `TwoSampleMR` R pipeline (harmonization, MR-Egger,
  weighted median, MR-PRESSO outlier removal, Steiger directionality).
- Cases: BMI, vitamin D, smoking(neg), IL-6(neg), + add education, T2D, lipids for AD; + all MS MR cases.
- Verify OpenGWAS IDs are current; cache summary stats locally.
- **Success metric:** reproduce catalog signs/magnitudes AND the negative-control nulls. Nulls passing =
  the method-validation headline.
**3b. ADNI re-analysis (AD substrate cases):**
- Apply for ADNI access (adni.loni.usc.edu — public on application, ~1-2 wk).
- Reproduce: (i) APOE4 dose -> amyloid/tau PET; (ii) plasma p-tau217 -> progression (Cox on CU->MCI);
  (iii) ATN axis (in)dependence via factor analysis / PCA (the P1 matroid-rank / axis-count question).
- **This directly tests the "how many independent axes?" structural claim numerically.**
**3c. (MS analogue) open MS cohorts:** OpenMS / published NfL & atrophy datasets for the relapse!=progression
axis test (factor analysis of relapse-weighted vs progression-weighted markers).

## PHASE 4 — The structural / cross-domain analyses (the novel contribution)
**4a. Axis-count (P1 matroid-rank):** on any multi-substrate dataset (ADNI ATN+I, or MS multi-metric),
run factor analysis / parallel analysis to estimate the NUMBER of independent substrate dimensions.
Prediction to test: ATN "collapses" to fewer independent axes than 4 (glial/inflammation loads on both).
**4b. Tier-transport (T_tier):** quantify how effect estimates SHIFT across evidence tiers for the SAME
mechanism (e.g., EBV necessity vs mimicry-mechanism vs therapy; amyloid genetics vs RCT). A
mechanism-by-tier matrix; the "shift" is the T_tier operator made numeric.
**4c. Cross-domain shared-node test:** for shared analytes (NfL, GFAP) and shared node (iron), compare
effect direction/magnitude MS vs AD. Formal transportability check (does the estimate transport across
DISEASE?). This is the empirical version of the H^1 obstruction.

## PHASE 5 — Presentation layer (Astro site)
- Data source = mechval_effect_sizes_v2.csv (single source of truth).
- Pages: (1) filterable case table (family/tier/verdict/domain); (2) interactive forest plots per cluster;
  (3) the tier-calibration figure; (4) cross-domain shared-node view (MS<->AD); (5) the ATN axis-count result.
- Use Plotly (interactive) exported from the same pipeline; keep the CSV as the contract between
  analysis and site so they never drift.

---

## PRIORITY ORDER (highest leverage first)
1. **Phase 1** (scale extraction) — cheap, unlocks everything, makes tau=0.89 real. DO FIRST.
2. **Phase 3a** (productionize MR) — real re-analysis, negative controls = the credibility win.
3. **Phase 2** (meta-analysis clusters) — standard, defensible, forest/funnel figures.
4. **Phase 3b** (ADNI) — highest scientific value, longest lead time (start access request NOW in parallel).
5. **Phase 4** (structural) — the novel contribution; depends on 3b data.
6. **Phase 5** (site) — presentation, last.

## WHAT TO TELL XIA ABOUT LIMITS (say this explicitly)
- The tiering-calibration is currently descriptive (small cited subset); Phase 1 makes it inferential.
- Patient-level re-analysis is limited to open cohorts (ADNI, GWAS summary stats); most trial IPD is not public.
- Meta-analytic pooling is valid only within homogeneous clusters; cross-domain comparison is
  transportability testing, not pooling.
- This is evidence-synthesis + targeted re-analysis, not a claim of new primary data collection.
