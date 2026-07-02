# MechVal — Multiple Sclerosis Mechanism Catalog (Xia Program)

**Build date:** 2026-06-30
**Author context:** Elliot Tower — MechViews / MechVal / MechRef program, applied to Dr. Zongqi Xia's
clinical-translational neuroimmunology (MS, AD, GEMS cohort, digital phenotyping, RWE).
**Format:** Mirrors the MechVal Public-Health Bible and Cross-Disorder Capstone — each mechanism
claim is decomposed into causal legs, assigned a **View** (Object / Role / Subspace / Structural /
Process), scored on the **MechVal tier scale** (T1 Descriptive, T2 Observationally Consistent,
T3 Causally Suggestive, T4 Mechanistically Supported), given a **verdict**, and where a claim
exceeds its evidence, a **Levi contraction** (preserve hard core, discard protective belt).

**Framing principle (same as the Xia bridge doc):** every entry is pitched in Xia's vocabulary —
progression, heterogeneity, treatment response, biomarker, confounding by indication — with the
MechVal/MechRef machinery as the engine underneath. The recurring MS-specific rule mirrors the
psychiatric catalog's dominant lesson:

> **MECHANISM-OF-TREATMENT is not MECHANISM-OF-DISEASE, and MECHANISM-OF-RELAPSE is not
> MECHANISM-OF-PROGRESSION**, unless independently supported by instruments, temporal order,
> perturbation, and specificity. This distinction is *the* central fault line in MS.

---

## Scoring key

| Tier | Name | What it requires |
|---|---|---|
| T1 | Descriptive | A reproducible phenomenon / association |
| T2 | Observationally Consistent | Survives covariate adjustment, replicates across cohorts |
| T3 | Causally Suggestive | Temporal order + instrument (MR/genetics) or negative-control design |
| T4 | Mechanistically Supported | Direct perturbation / treatment engagement changes the target as predicted |

**Verdict tags:** SUPPORTED · SUGGESTIVE · UNDERDETERMINED · CONTESTED · DISCONFIRMED · REFERENCE-DEBT

---

# CASE 001 — EBV infection is a necessary cause (trigger) of MS

**Decomposed claim (conjunction):**
- c1: EBV seroconversion is strongly associated with subsequent MS (descriptive/epi).
- c2: EBV seroconversion PRECEDES MS onset and precedes the neurofilament-light (NfL) rise.
- c3: The association is EBV-SPECIFIC (not shared by CMV or other viruses).
- c4: EBV is NECESSARY — MS essentially does not occur in the EBV-naive.
- c5: EBV is the proximal MOLECULAR MECHANISM of demyelination (a specific pathway).

**View:** Structural (a causal-etiological claim about disease origin), with a Process leg (temporal onset).

**Evidence:**
- Bjornevik et al., *Science* 2022: >10M US military, 955 MS cases; risk up **32-fold** after EBV
  seroconversion, NOT after CMV; NfL rose only AFTER EBV seroconversion [web:704][web:711].
- Longitudinal design gives genuine temporal order — a Tier-3 instrument, not mere association [web:698].
- Nat Rev Neurol 2023 review: MS is "a rare complication of EBV infection" [web:701].

**Tier assignment:**
- c1: **T2** (robust, replicated). c2: **T3** (temporal order + NfL sequencing = causally suggestive).
- c3: **T3** (virome-wide specificity, CMV negative control). c4: **T3-approaching-T4** (near-necessity
  is the strongest epi claim in MS). c5: **T1–T2** (mechanism of HOW EBV causes MS is NOT established —
  molecular mimicry, GlialCAM cross-reactivity, B-cell latency are candidates, none perturbationally proven).

**Verdict:** **SUPPORTED (as a necessary trigger) / UNDERDETERMINED (as a molecular mechanism).**

**Contraction (Levi):** Hard core = c1,c2,c3,c4 (EBV is a near-necessary, specific, temporally-prior
trigger). Protective belt to discard/weaken = c5 (the specific molecular pathway). The strong claim
"EBV causes MS via [specific mechanism X]" currently carries **reference debt** — the etiological
necessity transports; the molecular mechanism does not yet.

**Xia hook:** This is the cleanest T3 causal claim in MS and the template for the whole catalog —
temporal order + specificity + negative control (CMV) is exactly the causal-inference design his lab
can extend (e.g., EBV-load trajectories vs progression in the GEMS cohort).

---

# CASE 002 — Smoldering neuroinflammation / chronic active (iron-rim) lesions drive PROGRESSION independent of relapses

**Decomposed claim:**
- c1: Chronic active lesions (paramagnetic/iron-rim on MRI) exist and are reproducibly detectable.
- c2: Their burden correlates with disability progression cross-sectionally.
- c3: They represent COMPARTMENTALIZED CNS inflammation behind an intact blood-brain barrier.
- c4: This smoldering process is the MECHANISM of PIRA (progression independent of relapse activity),
  distinct from the focal-relapse mechanism.

**View:** Structural (a distinct pathological mechanism) + Subspace (a progression axis separable from relapse).

**Evidence:**
- Chronic active lesions review, PMC 2024: smoldering neuroinflammation "trapped within the CNS" as the
  substrate of increasing disability [web:699].
- 7T MRI longitudinal iron-rim lesion evolution supports persistence over years [web:702].

**Tier assignment:**
- c1: **T2** (reproducible imaging phenotype). c2: **T2** (association, confound-prone — see below).
- c3: **T3** (compartmentalization supported by pathology + BTK-inhibitor pharmacology, Case 003).
- c4: **T2–T3** (the relapse-independent axis is real but its identity as a single mechanism is not settled).

**Verdict:** **SUGGESTIVE, trending SUPPORTED** (strengthened by convergent BTK-inhibitor evidence).

**Contraction:** Preserve c1,c3. Weaken c2 — **THIS IS THE BRACKET-NORM CONFOUND ENTRY**: iron-rim /
lesion-burden metrics scale with voxel count, scanner field strength (3T vs 7T), and segmentation yield.
A metric predicting progression may be tracking acquisition depth, not biology. c4 held as a distinct
*axis* but not yet a single unified *mechanism*.

**Xia hook (highest-value):** Direct port of your bracket-norm paper — build a confound-audit +
intensive-correction protocol for iron-rim / lesion-volume biomarkers against CONFIRMED disability
worsening. Report raw rho, correlation with the sampling proxy (voxel count / SNR), and partial rho.

---

# CASE 003 — CNS-compartmentalized inflammation is a DRUGGABLE mechanism of progression (BTK inhibition)

**Decomposed claim:**
- c1: BTK inhibitors cross the BBB and modulate CNS microglia/B-cells (target engagement).
- c2: BTK inhibition slows CONFIRMED DISABILITY PROGRESSION in non-relapsing SPMS.
- c3: The progression mechanism is therefore compartmentalized innate/B-cell inflammation.
- c4: The SAME mechanism drives relapses (i.e., one unified inflammatory mechanism).

**View:** Structural (mechanism-of-disease), tested via a Process-level intervention (treatment engagement).

**Evidence:**
- Tolebrutinib HERCULES (non-relapsing SPMS): **met primary endpoint**, ~31% delay in time to onset of
  confirmed disability progression vs placebo [web:700][web:705].
- Tolebrutinib GEMINI 1/2 (relapsing MS): **did NOT** beat teriflunomide on annualized relapse rate;
  only a secondary disability-worsening signal [web:700].
- Fenebrutinib Phase II: suppressed acute AND chronic MRI activity [web:703]. Curr Opin Neurol 2024:
  CNS-penetrant BTK inhibitors target inflammation on both sides of the BBB [web:707].

**Tier assignment:**
- c1: **T3–T4** (pharmacological target engagement). c2: **T4** (RCT with disability-progression primary
  endpoint = the gold-standard interventional ground truth for a progression mechanism) [web:705].
- c3: **T3** (the RCT licenses the mechanism inference for PROGRESSION specifically).
- c4: **DISCONFIRMED as stated** — the relapse endpoint (GEMINI) failed while the progression endpoint
  (HERCULES) succeeded [web:700]. This is a *dissociation*, not a unified mechanism.

**Verdict:** **SUPPORTED for progression / mechanism DISSOCIATED from relapse.**

**Contraction:** This is the catalog's cleanest illustration of the central rule. Hard core: c1,c2,c3.
Discard c4. The HERCULES/GEMINI split is a **natural experiment proving mechanism-of-progression is
NOT mechanism-of-relapse** — the MS analog of "mechanism-of-treatment is not mechanism-of-disease."

**Xia hook:** The BTK trial dissociation is empirical ground truth for a **two-axis (relapse vs
progression) MechRef transport** analysis — do progression biomarkers transport across the relapsing
vs progressive populations, or are they distinct referents?

---

# CASE 004 — "Neuroinflammation-first vs neurodegeneration-first" as competing mechanisms of the MS→dementia / progressive transition

**Decomposed claim (two rival DAGs):**
- DAG-A (inflammation-first): chronic inflammation → neurodegeneration → progression.
- DAG-B (degeneration-first): primary neurodegeneration → secondary inflammation.
- c-shared: aging + Th17/cytokine mediation modulates the transition (Xia 2025).

**View:** Structural — this is a rival-causal-structure adjudication, NOT a single-mechanism claim.

**Evidence status:** Currently argued **narratively** in the field; no computational adjudication.
BTK-progression data (Case 003) tilts toward inflammation contributing causally to progression, but
does not resolve primacy.

**Tier assignment:** Both DAGs sit at **T2** (each consistent with observational data). Neither reaches
T3 because no instrument/temporal design has been applied to adjudicate PRIMACY.

**Verdict:** **CONTESTED / UNDERDETERMINED — the scoring unit is the instantiated causal path, not the umbrella.**

**Contraction:** Do not score "inflammation-first" as a whole. Decompose into specific legs
(e.g., "iron-rim burden at t predicts NfL rise at t+1 controlling for baseline atrophy") and score each.

**Xia hook (flagship methods project):** This is the **sheaf-cohomology DAG-adjudication** application —
encode each rival DAG as a sheaf over his longitudinal EHR/biomarker graph; the DAG whose per-cohort,
per-subgroup local effect estimates GLUE with low cohomology is better supported. This is the
mathematically rigorous version of "which disease model does the data support."

---

## Cross-case pattern (the emerging MS map)

| Node | Verdict pattern | Interpretation |
|---|---|---|
| EBV etiology (001) | SUPPORTED as trigger / UNDERDETERMINED as molecular mechanism | Strongest T3 causal claim in MS; mechanism leg carries reference debt |
| Smoldering / iron-rim (002) | SUGGESTIVE; confound-prone | Bracket-norm audit target; real axis, fragile metric |
| BTK / compartmentalized inflammation (003) | SUPPORTED for progression; DISSOCIATED from relapse | Interventional ground truth; proves two-axis dissociation |
| Inflammation-first vs degeneration-first (004) | CONTESTED | Score instantiated legs; sheaf-cohomology adjudication |

**The dominant MS rule (analog of the psychiatric catalog's "treatment ≠ etiology"):**
mechanism-of-relapse ≠ mechanism-of-progression. The BTK HERCULES/GEMINI dissociation (003) is the
cleanest proof, and it reframes half the MS biomarker literature as **reference-debt claims** — metrics
validated on the relapse axis being silently transported to the progression axis.

## Immediate build queue (first expansion)
1. **Case 002 confound audit** — bracket-norm protocol on iron-rim/lesion metrics vs confirmed
   disability worsening (highest immediate payoff, reuses existing MS MRI).
2. **Case 004 sheaf adjudication** — inflammation-first vs degeneration-first on GEMS longitudinal data.
3. Next cases to catalog: (005) serum NfL as progression biomarker; (006) OCBs/intrathecal Ig;
   (007) gut microbiome causal role; (008) vitamin D causal (MR evidence); (009) EBV molecular mimicry
   (GlialCAM); (010) grey-matter atrophy as the true progression substrate.


---

# CASE 005 — Serum neurofilament light chain (sNfL) as a mechanism/biomarker of neuroaxonal damage driving progression

**Decomposed claim:**
- c1: sNfL rises with acute axonal injury (relapse, new lesions) — reproducible.
- c2: Baseline/rising sNfL PREDICTS long-term disability progression (prognostic).
- c3: sNfL predicts progression in PROGRESSIVE MS specifically (relapse-independent axis).
- c4: sNfL is a MECHANISM readout of neurodegeneration (not merely a correlate).

**View:** Object/Role (a specific molecular readout) used as a Subspace proxy for the neurodegeneration axis.

**Evidence:**
- Long-term prospective cohort: baseline sNfL associated with 15–27yr disability outcomes; low baseline
  (<7.62 pg/mL) → 4.3x less likely to reach EDSS>=4 [web:721].
- Progressive-MS cohort: baseline cut-off 10.2 pg/mL discriminated long-term progressors (adj OR 7.8),
  and a rising sNfL between baseline and 6yr discriminated even better (OR ~49) [web:723].
- 2026 review: sNfL consistently associated with relapse, radiological activity, AND disability
  progression [web:717].

**Tier assignment:** c1 **T3-T4** (mechanistically tied to axonal release). c2 **T3** (prospective,
temporal, dose-graded — strong prognostic). c3 **T3** (holds in progressive MS) [web:723]. c4 **T2-T3**
(readout of damage, but "mechanism" overstates — it is a *marker* of the process, not a causal lever).

**Verdict:** **SUPPORTED as a prognostic/monitoring biomarker of the neurodegeneration axis; SUGGESTIVE
(not SUPPORTED) as a "mechanism."**

**Contraction:** Hard core c1,c2,c3. Discard the framing that sNfL *is* the mechanism (c4) — it is a
Role-level readout, and calling it a mechanism is a **view-level error** (Object/Role masquerading as
Structural). Confound note: sNfL varies with age/BMI/renal function — the JNNP cohort used age/BMI-
adjusted Z-scores for exactly this reason [web:723], a natural bracket-norm-style intensive correction.

**Xia hook:** sNfL is the ideal *response variable* (ground-truth-ish continuous progression signal) for
the Case 002 bracket-norm imaging audit and for Grassmannian progression-axis transport across cohorts.

---

# CASE 006 — Oligoclonal bands / intrathecal IgG synthesis as a mechanism of MS

**Decomposed claim:**
- c1: OCBs are present in >95% of MS CSF — the immunological hallmark (descriptive).
- c2: OCB presence/count predicts worse prognosis and disability progression.
- c3: The intrathecal IgG targets a specific MS antigen (a defined molecular mechanism).

**View:** Structural (claim of a specific humoral mechanism) vs Object (a diagnostic marker).

**Evidence:**
- OCBs in >95% of MS CSF; target specificities remain largely UNIDENTIFIED [web:738].
- Prognostic signal is INCONSISTENT: some cohorts show higher band counts predict progression [web:734];
  a Portuguese cohort found early worse EDSS but INVERSION after 10yr (OCB-negative worse long-term)
  [web:736]; a Sardinian cohort (n=503) found NO prognostic value, attributing it to genetic background
  [web:740].

**Tier assignment:** c1 **T2-T3** (robust diagnostic hallmark). c2 **T1-T2, HETEROGENEOUS** — the
prognostic direction FLIPS across cohorts/populations [web:736][web:740]. c3 **T1** (antigen mostly
unknown) [web:738].

**Verdict:** **SUPPORTED as a diagnostic marker; CONTESTED as a prognostic mechanism; UNDERDETERMINED
as a molecular mechanism.**

**Contraction:** Preserve c1 (diagnostic Object-level claim). Do NOT promote to Structural — c3 fails.
The cross-cohort direction-flip in c2 is a textbook **NON-TRANSPORT / H^1 != 0** case: local prognostic
sections (per cohort) are individually fit but do NOT glue into a consistent global effect — and the
Sardinian genetic-background note names the effect-MODIFIER [web:740].

**Xia hook (perfect cohomology demo):** OCB prognosis is a real dataset where pairwise-consistent-looking
associations fail to reconcile globally — a candidate for the sheaf-gluing obstruction test with genetic
background as the stratifying variable.

---

# CASE 007 — Low vitamin D is a causal risk factor for MS

**Decomposed claim:**
- c1: Low serum 25(OH)D is associated with higher MS risk (observational).
- c2: Genetically-lowered 25(OH)D CAUSES increased MS risk (MR instrument).
- c3: The causal path runs through allele-specific vitamin D receptor (VDR) binding.
- c4: Vitamin D SUPPLEMENTATION prevents/delays MS (interventional).

**View:** Structural (etiological), tested with a genetic instrument (MR = the T3 lever).

**Evidence:**
- MR (IMSGC, up to 14,498 cases): each 1-SD genetic decrease in log-25(OH)D → 2.0x MS odds; robust to
  pleiotropy sensitivity analyses [web:727]. Independent MR replications concur [web:724][web:718].
- 2024 PNAS: causal association extends to allele-specific VDR binding [web:726].
- RCT prevention evidence (c4) NOT established — authors explicitly call for long-term RCTs [web:727].

**Tier assignment:** c1 **T2**. c2 **T3** (multiple independent MR studies, pleiotropy-robust —
one of the best-instrumented causal claims in MS) [web:727][web:724]. c3 **T3** (VDR-binding mechanism
supported) [web:726]. c4 **T1-T2** (no positive prevention RCT).

**Verdict:** **SUPPORTED as a causal RISK factor (MR); UNDERDETERMINED as a treatment/prevention lever.**

**Contraction:** Hard core c1,c2,c3 (genetically-instrumented causal risk transports). Discard c4 — the
leap from "causal risk factor" to "supplementation works" is the classic **etiology != treatment**
error (mirrors the psychiatric catalog's dominant failure mode). Reference debt sits entirely on c4.

**Xia hook:** MR is exactly the causal-inference design template his lab uses; vitamin D is the clean
positive control for a MechVal MR-scoring pipeline (contrast with the confounded CRP-in-depression case
from the public-health bible).

---

# CASE 008 — Gut microbiome dysbiosis is causal in MS risk and course

**Decomposed claim:**
- c1: MS patients show reproducible gut microbiome composition shifts vs controls.
- c2: The shift is disease-associated, not a treatment/diet artifact (household-control design).
- c3: Specific taxa/pathways CAUSE MS risk or progression.
- c4: Microbiome mediates treatment mechanism (e.g., IFN-beta via SCFA transporters).

**View:** Structural/Process (a causal environmental mechanism).

**Evidence:**
- iMSMS (576 MS + 1,152 total, household-matched controls): increased *Akkermansia muciniphila*,
  decreased *Faecalibacterium prausnitzii*; phytate-degradation up in untreated MS; microbiome also
  shifted BY treatment; IFN-beta activity linked to SCFA-transporter upregulation [web:716].
- Household-control design controls diet/environment — a strong quasi-negative-control [web:716].

**Tier assignment:** c1 **T2-T3** (large, household-controlled — better than typical microbiome studies).
c2 **T2-T3** [web:716]. c3 **T1-T2** (association + biological plausibility; NO perturbational causal proof
in humans; reverse causation / treatment confounding live). c4 **T2** (mechanistically suggestive) [web:716].

**Verdict:** **SUGGESTIVE (association is unusually clean); UNDERDETERMINED as a causal mechanism.**

**Contraction:** Preserve c1,c2 (the household-control design earns real credit). Do not promote c3 to
causal — direction (dysbiosis causes MS vs MS/treatment causes dysbiosis) is unresolved. The fact that
the microbiome shifts WITH treatment [web:716] is itself a confounder for any progression claim.

**Xia hook:** A mediation-DAG candidate (treatment -> microbiome -> outcome) for the sheaf-cohomology
adjudication — does the mediation path glue consistently across treated/untreated strata?

---

# CASE 009 — EBV EBNA1 / GlialCAM molecular mimicry is the mechanism linking EBV to MS

**Decomposed claim (the mechanistic leg deferred from Case 001):**
- c1: MS patients have anti-EBNA1 antibodies that cross-react with CNS GlialCAM.
- c2: This cross-reactivity is enhanced by somatic hypermutation in the CNS and GlialCAM phosphorylation.
- c3: These antibodies CONTRIBUTE to CNS immunopathology (causal, not epiphenomenal).
- c4: Molecular mimicry is THE (sole/primary) mechanism translating EBV into MS.

**View:** Structural (a specific molecular-mechanism claim) — this is the c5 leg of Case 001 examined directly.

**Evidence:**
- Lanz et al. (Nature 2022): anti-EBNA1 antibodies cross-react with GlialCAM; recognition increases via
  somatic hypermutation and serine phosphorylation; confirmed across MS cohorts; mouse models support a
  contribution to CNS immunopathology [web:731].

**Tier assignment:** c1 **T3** (cross-reactivity demonstrated in patient cohorts). c2 **T3** (molecular
mapping). c3 **T3** (mouse-model perturbational support — approaches T4 for the animal system, transports
weakly to human causation). c4 **T1-T2** (mimicry is likely ONE of several mechanisms; sole-mechanism
claim is unsupported).

**Verdict:** **SUGGESTIVE-to-SUPPORTED as a contributing mechanism; DISCONFIRMED as the SOLE mechanism.**

**Contraction:** Hard core c1,c2,c3 (mimicry is a real, mapped, animal-supported contributor). Discard c4.
This RESOLVES the reference debt flagged in Case 001-c5: the molecular mechanism now has genuine T3
support, but only as *a* pathway, not *the* pathway. Update Case 001-c5 from T1-T2 to **T3 (contributing)**.

**Xia hook:** Cross-species transport (mouse -> human) is a MechRef transport-hierarchy exercise — what
evidence tier licenses moving the mimicry mechanism from animal model to human etiology?

---

# CASE 010 — Grey-matter (esp. deep GM) atrophy is the true substrate of disability progression

**Decomposed claim:**
- c1: GM atrophy occurs across all MS phenotypes and correlates with disability (descriptive).
- c2: DEEP GM atrophy specifically PREDICTS time-to-EDSS-progression better than WM/lesion measures.
- c3: GM atrophy is the PROXIMAL SUBSTRATE of progression (mechanism, not correlate).
- c4: GM atrophy rate is a valid TREATMENT-EFFECT surrogate.

**View:** Structural/Subspace (a progression-axis substrate claim).

**Evidence:**
- MAGNIMS 7-center, 1,417 subjects: baseline DEEP GM volume was the ONLY regional volume predicting
  time-to-EDSS progression (HR 0.73 per SD); DGM had the fastest atrophy rate and was the only measure
  whose atrophy rate associated with disability accumulation [web:742].
- Long-term cohorts: cortical + subcortical GM atrophy early, links to progression at 5yr; whole-brain
  atrophy better at 10yr [web:730][web:735].

**Tier assignment:** c1 **T2-T3**. c2 **T3** (large multicenter longitudinal, DGM-specific, dose-graded)
[web:742]. c3 **T2-T3** (strong substrate evidence; still partly a readout). c4 **T2** (phenotype-
dependent atrophy patterns complicate surrogate use — the MAGNIMS authors caution exactly this) [web:742].

**Verdict:** **SUPPORTED as the leading progression substrate/predictor; SUGGESTIVE as a treatment surrogate.**

**Contraction:** Hard core c1,c2 (DGM predicts progression, well-instrumented). c3 held as substrate,
not sole mechanism. Discard/weaken c4 — surrogate validity is phenotype-heterogeneous. **THIS IS THE
SECOND BRACKET-NORM ENTRY**: atrophy metrics scale with scanner/segmentation; the DGM signal must be
shown to survive intensive correction against the sampling confound. Phenotype-dependence of atrophy
patterns [web:742] is an explicit effect-MODIFIER = an H^1 non-transport candidate.

---

## Updated cross-case map (010 cases)

| # | Node | Best tier reached | Verdict | Machinery hook |
|---|---|---|---|---|
| 001 | EBV as trigger | T3 (necessity) | SUPPORTED trigger / mechanism deferred | MR-style temporal design |
| 002 | Smoldering / iron-rim | T2-T3 | SUGGESTIVE, confound-prone | **Bracket-norm audit #1** |
| 003 | BTK / compartmentalized inflammation | T4 (RCT) | SUPPORTED progression / DISSOCIATED from relapse | Two-axis MechRef transport |
| 004 | Inflammation- vs degeneration-first | T2 | CONTESTED | **Sheaf-cohomology DAG adjudication** |
| 005 | sNfL neuroaxonal readout | T3 | SUPPORTED biomarker / not a "mechanism" | Ground-truth response variable |
| 006 | OCB / intrathecal IgG | T2-T3 diag; T1 mech | SUPPORTED diag / CONTESTED prognosis | **H^1 non-transport demo** (genetic background modifier) |
| 007 | Low vitamin D | T3 (MR) | SUPPORTED causal risk / treatment underdetermined | MR-scoring positive control |
| 008 | Gut microbiome | T2-T3 | SUGGESTIVE / causal underdetermined | Mediation-DAG gluing test |
| 009 | EBNA1-GlialCAM mimicry | T3 (contributing) | SUPPORTED contributor / DISCONFIRMED as sole | Cross-species MechRef transport |
| 010 | Deep GM atrophy | T3 | SUPPORTED substrate / surrogate suggestive | **Bracket-norm audit #2** + phenotype H^1 |

## Consolidated MS-specific findings

**The two dominant rules (both are MechRef/MechVal failure modes):**
1. **mechanism-of-relapse != mechanism-of-progression** — proven interventionally by the BTK
   HERCULES/GEMINI dissociation (003) [web:700][web:705]; recurs in 002, 005, 010.
2. **etiology != treatment** — vitamin D is causal risk (007) but supplementation is unproven [web:727];
   EBV is a necessary trigger (001) but antivirals are unproven; same failure as the psychiatric catalog.

**Best-validated claims:** BTK-progression (003, T4 RCT) > EBV-necessity (001, T3) ~ vitamin-D-MR
(007, T3) ~ deep-GM-atrophy (010, T3) ~ sNfL-prognosis (005, T3).

**Cleanest disconfirmations / overreaches:** OCB "molecular mechanism" (006-c3); vitamin-D
"supplementation works" (007-c4); mimicry "sole mechanism" (009-c4); one-unified-inflammatory-
mechanism across relapse+progression (003-c4).

**The three flagship methods projects (all reuse Xia's existing data):**
- **P1 (Bracket-norm audit):** intensive-correction of iron-rim (002) and deep-GM-atrophy (010) metrics
  vs confirmed disability worsening, using sNfL (005) as a co-validating response. Highest immediate payoff.
- **P2 (Sheaf-cohomology adjudication):** inflammation-first vs degeneration-first (004) and the
  microbiome mediation path (008) on GEMS longitudinal data.
- **P3 (H^1 non-transport / heterogeneity):** OCB prognosis (006) and GM-atrophy surrogate (010) as
  effect-modifier / non-transport demonstrations, with genetic background and phenotype as the modifiers.


---

# CASE 011 — Anti-CD20 B-cell depletion works because MS is a B-cell-mediated (not purely T-cell) disease

**Decomposed claim:**
- c1: Anti-CD20 mAbs (ocrelizumab, rituximab, ofatumumab, ublituximab) deplete CD20+ B cells (target engagement).
- c2: They robustly reduce relapses and MRI activity across RRMS.
- c3: Ocrelizumab slows progression in PRIMARY PROGRESSIVE MS (the first DMT to do so).
- c4: Therefore MS is a B-cell-mediated disease (the therapeutic mechanism reveals the disease mechanism).

**View:** Structural (disease-mechanism claim) inferred from a Process-level intervention.

**Evidence:**
- Four approved anti-CD20 mAbs; B-cell depletion "changed the MS landscape"; multiple depletion
  mechanisms (ADCC, CDC, phagocytosis) [web:752][web:757].
- Ocrelizumab effective in PPMS — but effect is modest and enriched in younger/inflammatory-active
  patients [web:750][web:754].
- Anti-CD20 also depletes CD20+ T cells and modulates BAFF; the mechanism is NOT purely B-cell [web:756][web:755].

**Tier assignment:** c1 **T4** (direct depletion). c2 **T4** (RCT relapse reduction). c3 **T3-T4**
(RCT-supported but modest, effect-modified by inflammatory activity) [web:750]. c4 **T2-T3** — the
inference "therapy works therefore disease is B-cell-mediated" OVERREADS: anti-CD20 hits CD20+ T cells
and cytokine milieu too [web:756].

**Verdict:** **SUPPORTED as a treatment mechanism (B-cell depletion works); OVERREACH as a disease-
mechanism claim (MS "is" B-cell-mediated).**

**Contraction:** Hard core c1,c2,c3. Discard the strong reading of c4 — this is the catalog's cleanest
repeat of **mechanism-of-treatment != mechanism-of-disease**: depletion efficacy does not license a
mono-causal B-cell etiology, because the drug's target set is broader than "B cells" [web:755][web:756].

**Xia hook:** The PPMS effect-modification (works better in younger/active patients) [web:750] is a
concrete effect-MODIFIER = H^1/heterogeneity target: does the anti-CD20 progression benefit TRANSPORT
across age/inflammatory-activity strata, or is it a stratum-specific section?

---

# CASE 012 — Cortical/leptomeningeal demyelination is a distinct driver of progression and cognitive decline

**Decomposed claim:**
- c1: Cortical GM demyelination is common in MS and present from the earliest stages (descriptive).
- c2: Cortical lesion burden correlates with physical disability and cognitive impairment.
- c3: Cortical demyelination is driven by MENINGEAL inflammation (tertiary lymphoid follicles), a
  mechanism partly distinct from WM lesions.
- c4: Cortical pathology is the PRIMARY substrate of progression.

**View:** Structural (a distinct pathological mechanism) + Subspace (cognitive/progression axis).

**Evidence:**
- Cortical demyelination extensive, present early, associated with physical + cognitive deficits, and
  with progression rate in relapsing and progressive MS [web:749][web:744].
- Meningeal inflammation / B-cell follicles linked to subpial cortical demyelination; disease-specific
  molecular events identified in cortical lesions [web:744][web:747].
- Cortical lesions poorly detected on conventional MRI (need DIR/7T) — a MEASUREMENT confound [web:749][web:751].

**Tier assignment:** c1 **T2-T3**. c2 **T2-T3** [web:749]. c3 **T3** (pathology links meningeal
inflammation to subpial demyelination) [web:744]. c4 **T2** (one of several substrates; competes with
deep GM atrophy, Case 010).

**Verdict:** **SUPPORTED as a distinct pathological axis; SUGGESTIVE as the primary progression substrate.**

**Contraction:** Preserve c1,c2,c3. Do not adjudicate c4 vs Case-010 (deep GM) narratively — this is a
**rival-substrate DAG** for the sheaf adjudication. Detection confound (DIR/7T dependence) is a
**bracket-norm entry #3**: measured cortical-lesion count scales with sequence/field strength [web:749].

**Xia hook:** Cortical-lesion detection is field-strength/sequence dependent [web:749][web:751] — a third
imaging confound-audit target, and a cross-scanner NON-TRANSPORT candidate (does cortical-lesion
prognosis glue across 3T vs 7T sites?).

---

# CASE 013 — Adult (and childhood) obesity is a causal risk factor for MS

**Decomposed claim:**
- c1: Higher BMI is observationally associated with MS risk.
- c2: Genetically-predicted higher BMI CAUSES increased MS risk (MR).
- c3: The childhood-BMI effect is MEDIATED by persistence into adulthood, not a direct childhood window.
- c4: Weight reduction lowers MS risk (interventional).

**View:** Structural (etiological), MR-instrumented.

**Evidence:**
- MR (14,802 cases/26,703 controls): higher childhood BMI OR=1.26/SD, but effect DISAPPEARS after
  adjusting for adult BMI (OR=1.03); adult-BMI effect PERSISTS (OR=1.43); pleiotropy-robust; UK Biobank
  replicated [web:745]. Independent MR (IMSGC) confirms causal adult-BMI effect [web:718].

**Tier assignment:** c1 **T2**. c2 **T3** (multiple pleiotropy-robust MR studies) [web:745][web:718].
c3 **T3** (multivariable MR pins the mediation structure — childhood effect runs THROUGH adult obesity)
[web:745]. c4 **T1** (no weight-loss prevention trial).

**Verdict:** **SUPPORTED as a causal risk factor (adult BMI); mediation structure SUPPORTED; treatment
lever UNDERDETERMINED.**

**Contraction:** Hard core c1,c2,c3. Discard c4 (etiology != treatment). NOTE the c3 finding is itself a
clean **causal-mediation / DAG result** obtained by multivariable MR — a template for Xia's causal-
discovery pipeline (front-door/mediation on genetic instruments).

**Xia hook:** Vitamin D (007) + BMI (013) are TWO independent MR-validated risk factors sharing the
confound structure flagged in your bracket-norm work (the CRP-BMI-off-geodesic confound); together they
form the positive-control pair for a MechVal MR-scoring module.

---

# CASE 014 — Remyelination failure is the mechanism of progression, and promoting remyelination will halt it

**Decomposed claim:**
- c1: Chronic demyelination without repair contributes to axonal loss (biological plausibility).
- c2: Oligodendrocyte precursor differentiation failure is the mechanism of remyelination failure.
- c3: Pharmacologically promoting remyelination will produce clinical benefit (therapeutic).

**View:** Structural/Process (a repair-mechanism claim leading to a treatment prediction).

**Evidence:**
- Remyelinating therapies showed early promise but MANY trials FAILED to meet endpoints (2025 review)
  [web:758]. Opicinumab (anti-LINGO-1) is the canonical high-profile failure at phase II/III.

**Tier assignment:** c1 **T2-T3** (plausible, pathology-supported). c2 **T2** (candidate mechanism).
c3 **T1-T2, largely DISCONFIRMED at the trial level** — repeated clinical failures [web:758].

**Verdict:** **SUGGESTIVE as biology; DISCONFIRMED (so far) as a therapeutic strategy.**

**Contraction:** Preserve c1. This is the inverse of the "treatment works therefore mechanism is real"
error — here a plausible MECHANISM did NOT yield treatment benefit, exposing that remyelination-failure
may be a CONSEQUENCE marker rather than the causal lever, OR that trial outcome measures (see Case 015)
were too insensitive to detect repair. Reference debt sits on c3.

**Xia hook:** The remyelination-trial failures may be an OUTCOME-MEASUREMENT problem (EDSS insensitivity,
Case 015) as much as a biology problem — a MechVal case where the validity bottleneck is the MEASURE,
not the mechanism.

---

# CASE 015 — EDSS validly measures the disability-progression construct (the measurement-validity case)

**Decomposed claim (this is a MEASUREMENT claim, not a disease mechanism — and it underwrites all the others):**
- c1: EDSS is a valid, internationally accepted measure of MS physical disability.
- c2: EDSS reliably detects disease PROGRESSION over time.
- c3: EDSS is sensitive to treatment effects in PROGRESSIVE MS.
- c4: EDSS change is linear/interval (a 1-point change means the same thing everywhere on the scale).

**View:** This is a construct-validity / operationalization claim — it sits UNDER every progression claim
in the catalog (001,002,003,005,010,011,012,014 all use EDSS-defined progression as ground truth).

**Evidence:**
- EDSS is the accepted gold standard and EMA-recognized primary endpoint [web:761][web:766].
- BUT: moderate inter/intra-rater reliability (kappa 0.32-0.76); heavily weighted to ambulation; poor
  upper-limb/cognitive capture; NON-LINEAR [web:767][web:772]. Documented case of EDSS 2.0->1.0->
  fluctuation questioning "progression" [web:766].
- POOR responsiveness to progression/treatment in SPMS/PPMS (effect size only 0.2-0.3 at 2yr);
  alternative measures recommended for progressive-MS trials [web:768]. MSFC more sensitive than EDSS [web:765].

**Tier assignment:** c1 **T3** (validated for physical disability). c2 **T2** (reliability-limited).
c3 **T1-T2, largely DISCONFIRMED for progressive MS** [web:768]. c4 **DISCONFIRMED** — EDSS is
demonstrably non-linear [web:772][web:767].

**Verdict:** **SUPPORTED as a physical-disability measure; WEAK/DISCONFIRMED as a sensitive, linear
progression measure in progressive MS.**

**Contraction:** This case is FOUNDATIONAL. Its failures propagate UPWARD: every progression-mechanism
claim scored against EDSS inherits EDSS's ~0.2-0.3 effect-size ceiling and non-linearity in progressive
MS [web:768]. The remyelination failures (014) and the BTK/anti-CD20 progression signals (003,011) are
all measured through this noisy, non-linear lens.

**Xia hook (methodologically the most important):** This is where your program's VIEW-LEVEL and
INVARIANCE machinery earns its keep. EDSS non-linearity means a "1-point progression" is NOT invariant
across the scale — a cross-view invariance violation. Reframing progression on a properly metric latent
axis (item-response / manifold) BEFORE running any biomarker analysis is a prerequisite methods
contribution, and it directly motivates the Fisher-Rao / Grassmannian progression-axis reframing in
the Xia bridge doc.

---

# CASE 016 — Early high-efficacy DMT reduces long-term disability (the treatment-timing causal claim)

**Decomposed claim:**
- c1: Early high-efficacy therapy (HET) is associated with lower disability at 6-10 years.
- c2: This association is CAUSAL (early HET reduces progression), not confounded by indication.
- c3: "Escalation" (start mild, step up) patients never catch up to early-HET patients.

**View:** Structural (a causal treatment-strategy claim) tested observationally.

**Evidence:**
- Retrospective cohort (~300 pts): early HET (<2yr) vs late (4-6yr); mean EDSS at 10yr 2.3 vs 3.5
  (adjusted difference -0.98, p<0.0001) [web:760][web:764]. Trade-off: early group had MORE activity in
  first 2 years, benefit emerged 2-10yr [web:764].

**Tier assignment:** c1 **T2-T3** (multi-cohort, adjusted). c2 **T2-T3, CONFOUNDING-BY-INDICATION LIVE**
— this is observational; sicker patients may be selected into either arm; the RCT (DELIVER-MS/TREAT-MS)
readouts are the needed T4 [web:762]. c3 **T2** (observational "no catch-up") [web:764].

**Verdict:** **SUGGESTIVE, CONFOUNDING-LIMITED — the flagship confounding-by-indication case.**

**Contraction:** Hard core c1. c2 explicitly flagged for confounding by indication — this is the EXACT
threat your Fisher-Rao "off-geodesic confound-leakage score" was designed for (Xia bridge Application 3).
Measured through EDSS (Case 015), the -0.98 effect also sits near EDSS's noise floor.

**Xia hook:** This is Xia's home turf (BCD-vs-natalizumab, semi-supervised causal RWE). The geometric
confound-leakage score + the sheaf gluing test (does the early-HET benefit glue across sites/subgroups?)
are directly deployable, and EDSS-linearization (015) is the required preprocessing.

---

## Updated cross-case map (016 cases)

| # | Node | Best tier | Verdict | Machinery hook |
|---|---|---|---|---|
| 001 | EBV trigger | T3 | SUPPORTED trigger | Temporal causal design |
| 002 | Smoldering / iron-rim | T2-T3 | SUGGESTIVE, confounded | Bracket-norm #1 |
| 003 | BTK / compartmentalized inflammation | T4 | SUPPORTED progression / DISSOCIATED relapse | Two-axis transport |
| 004 | Inflammation- vs degeneration-first | T2 | CONTESTED | Sheaf DAG adjudication |
| 005 | sNfL | T3 | SUPPORTED biomarker | Ground-truth response |
| 006 | OCB / intrathecal IgG | T2-3 / T1 | SUPPORTED diag / CONTESTED prognosis | H^1 non-transport |
| 007 | Low vitamin D | T3 (MR) | SUPPORTED causal risk | MR positive control |
| 008 | Gut microbiome | T2-3 | SUGGESTIVE | Mediation-DAG gluing |
| 009 | EBNA1-GlialCAM mimicry | T3 | SUPPORTED contributor / not sole | Cross-species transport |
| 010 | Deep GM atrophy | T3 | SUPPORTED substrate | Bracket-norm #2 + phenotype H^1 |
| 011 | Anti-CD20 B-cell depletion | T4 | SUPPORTED treatment / OVERREACH as etiology | Age/activity H^1 modifier |
| 012 | Cortical/meningeal demyelination | T3 | SUPPORTED axis / SUGGESTIVE primary | Bracket-norm #3 + rival substrate |
| 013 | Obesity / BMI | T3 (MR) | SUPPORTED causal risk + mediation | MR + causal-mediation template |
| 014 | Remyelination-failure -> therapy | T2 / T1 | SUGGESTIVE biology / DISCONFIRMED therapy | Measurement-bottleneck case |
| 015 | EDSS validity | T3 / DISCONFIRMED linearity | Valid disability / WEAK progression measure | **Invariance / metric-axis (foundational)** |
| 016 | Early high-efficacy DMT | T2-3 | SUGGESTIVE, confounded-by-indication | Fisher-Rao confound-leakage |

## Structural findings after 16 cases

**Three dominant failure modes now clearly separated:**
1. **mechanism-of-relapse != mechanism-of-progression** (003, 011): drugs/markers on the relapse axis
   silently transported to the progression axis.
2. **etiology != treatment** (001, 007, 013): EBV/vitamin-D/BMI are causal but no proven intervention.
3. **the measure is the bottleneck, not the mechanism** (014, 015, 016): EDSS non-linearity and
   insensitivity in progressive MS cap the detectable effect size at ~0.2-0.3 and corrupt every
   downstream progression claim [web:768].

**The foundational move (new after this batch):** Case 015 shows that BEFORE any biomarker/mechanism
scoring, the progression OUTCOME itself must be re-expressed on an invariant, properly-metric axis.
This makes your cross-view-invariance paper the METHODOLOGICAL PREREQUISITE for the whole MS program,
not just a companion theory — a strong, unexpected result to bring to Xia.

**Confound-audit (bracket-norm) targets now number three:** iron-rim (002), deep-GM atrophy (010),
cortical-lesion detection (012) — all scale with scanner/sequence/segmentation and all feed progression
claims. This is enough for a standalone multi-biomarker confound-audit paper.


---

# CASE 017 — HLA-DRB1*15:01 is the strongest genetic cause of MS, acting via antigen presentation

**Decomposed claim:**
- c1: HLA-DRB1*15:01 is associated with MS in nearly all populations (descriptive/GWAS).
- c2: It is the STRONGEST single genetic risk factor (~3-fold odds).
- c3: The mechanism is specific antigen presentation by the class-II molecule.
- c4: The effect is (at least partly) MEDIATED by expression/epigenetic regulation, not the coding allele alone.

**View:** Structural (a genetic-etiological mechanism), with a Role/Object leg (the specific allele).

**Evidence:**
- DRB1*15:01 associated with MS across Caucasian, Asian, African-American populations; ~3-fold odds
  (meta-analysis OR 3.06) [web:780][web:787][web:785].
- Antigen-presentation is the textbook mechanism but "does not fully explain the disease association" [web:780].
- The risk allele drives HIGHER DRB1/DQB1 expression (eQTL: risk genotype 8.3x DRB1 expression) [web:780][web:773];
  DNA methylation in HLA-DRB1 MEDIATES the *15:01 effect (Nature Comms 2018) [web:776][web:786].

**Tier assignment:** c1 **T3** (robust cross-population genetic association = a natural instrument).
c2 **T3** (consistently strongest). c3 **T2-T3** (plausible, incompletely explanatory) [web:780].
c4 **T3** (expression + methylation mediation demonstrated) [web:776].

**Verdict:** **SUPPORTED as the leading genetic risk factor; mechanism (antigen presentation) SUGGESTIVE
and INCOMPLETE; expression/epigenetic mediation SUPPORTED.**

**Contraction:** Hard core c1,c2,c4. Weaken c3 as SOLE mechanism — the allele's risk runs partly through
regulation/expression, not purely peptide binding [web:776]. This mirrors Case 009: the association leg
is strong, the "obvious" molecular mechanism leg is only a contributor.

**Xia hook:** DRB1*15:01 is a clean genetic INSTRUMENT (like an MR exposure) and the anchor for the
GEMS genetics x clinical-trajectory principal-angle test in the Xia bridge doc — do genetics-derived
and trajectory-derived progression axes AGREE?

---

# CASE 018 — HLA-DRB1*15:01 x EBV interaction is a genuine causal effect-modification

**Decomposed claim (this is explicitly an EFFECT-MODIFICATION claim — the catalog's H^1 exemplar):**
- c1: EBV infection and DRB1*15:01 are each independently associated with MS.
- c2: Their JOINT effect exceeds the sum of the separate effects (additive interaction).
- c3: The interaction reflects a shared/converging causal MECHANISM (not just statistical).

**View:** Structural + explicitly a Subspace/interaction claim (two risk axes that do not simply add).

**Evidence:**
- Meta-analysis (5 studies): EBV OR 2.60; DRB1*15:01 OR 3.06; significant ADDITIVE interaction
  (synergy index S=1.43, 95%CI 1.05-1.95, p=0.023) but NO multiplicative interaction (OR 0.86, ns) [web:787].

**Tier assignment:** c1 **T3** (both individually causal-suggestive: EBV Case 001, HLA Case 017).
c2 **T3** (meta-analytic additive interaction, though scale-dependent) [web:787]. c3 **T2** (mechanism
of convergence — presumably EBV-antigen presentation via DRB1*15:01 — plausible but not proven).

**Verdict:** **SUPPORTED as a statistical (additive) effect-modification; SUGGESTIVE as a mechanistic
convergence.**

**Contraction:** Hard core c1,c2. Note the SCALE-DEPENDENCE: interaction is present on the additive
scale, ABSENT on the multiplicative scale [web:787]. This is a **cross-view-invariance issue**: whether
"interaction exists" depends on the measurement scale (additive vs multiplicative) — the interaction is
NOT scale-invariant. This is precisely the phenomenon your invariance paper formalizes, and precisely
what T_glue / H^1 must be defined to respect.

**Xia hook (the cleanest heterogeneity/H^1 case in the catalog):** DRB1*15:01 is a MEASURED effect-
modifier of the EBV->MS effect. This is the ideal validation dataset for the T_local/T_glue and
obstruction machinery: stratify by HLA genotype, ask whether the EBV effect GLUES across strata. And
the additive-vs-multiplicative scale-dependence is the built-in warning that the obstruction must be
defined on the correct (invariant) scale.

---

# CASE 019 — MS is one disease; AQP4-NMOSD and MOGAD are distinct entities (the identity-criterion / boundary case)

**Decomposed claim (a MechViews identity-criterion claim, not a mechanism claim):**
- c1: AQP4-NMOSD is a distinct disease with a distinct mechanism (astrocytopathy, anti-AQP4).
- c2: MOGAD is a distinct entity (anti-MOG, distinct clinical/MRI phenotype).
- c3: These are reliably SEPARABLE from MS by antibody + clinical/MRI features.
- c4: Antibody tests define the boundary cleanly (no misclassification).

**View:** This is an OBJECT-IDENTITY / MechViews claim — it defines what counts as "the same disease,"
i.e., the equivalence relation ~ underlying every other case in the catalog.

**Evidence:**
- AQP4-NMOSD and MOGAD have distinct clinical, MRI, and antibody profiles; dedicated diagnostic criteria
  exist to distinguish them from MS [web:774].
- BUT: assay limitations cause FALSE positives; misdiagnosis is a documented pitfall; awareness of assay
  limits is "fundamental... to avoid inappropriate treatments" [web:774].

**Tier assignment:** c1 **T3-T4** (AQP4 astrocytopathy is mechanistically well-defined). c2 **T3**
(MOGAD increasingly well-characterized). c3 **T3** (separable with criteria) [web:774]. c4 **T2** —
assay false-positives blur the boundary [web:774].

**Verdict:** **SUPPORTED that these are distinct entities; the BOUNDARY is imperfect (assay-limited).**

**Contraction:** Hard core c1,c2,c3. Weaken c4. This case is FOUNDATIONAL in the MechViews sense: it
sets the identity criterion ~ for the whole catalog. If AQP4/MOGAD contaminate an "MS" cohort, EVERY
downstream mechanism claim is scored on a mixed referent — a **reference-error at the population level**.

**Xia hook:** This is the MechViews object-identity layer made clinical: cohort definition IS an
equivalence-class choice. A misspecified ~ (MS cohort contaminated by MOGAD/NMOSD) is the population-
level analog of the "false global object" failure — and a concrete data-cleaning prerequisite before
any GEMS mechanism analysis.

---

# CASE 020 — Sex (female predominance) reflects a hormonal-immune causal mechanism modifying MS risk and course

**Decomposed claim:**
- c1: MS is ~3x more common in women (robust descriptive).
- c2: Sex modifies disease COURSE: men progress faster, more atrophy/cognitive impairment.
- c3: Pregnancy reduces relapse rate; postpartum increases it (a natural hormonal experiment).
- c4: Sex hormones (estrogen/progesterone/testosterone) CAUSALLY drive these differences via immune +
  repair mechanisms.

**View:** Structural (hormonal-immune mechanism) + Subspace (sex as an effect-modifier of both risk and progression).

**Evidence:**
- 3:1 female predominance, rising incidence in women [web:779][web:783]. Men: faster progression, more
  atrophy and cognitive impairment [web:783].
- Pregnancy: markedly reduced relapse; postpartum rebound tied to abrupt estrogen drop [web:783] — a
  strong quasi-experimental temporal signal.
- Hormones influence immune responses AND remyelination/repair; dysregulation linked to failed
  spontaneous remyelination and progression [web:775][web:777].

**Tier assignment:** c1 **T2-T3**. c2 **T2-T3** (consistent sex-course dimorphism) [web:783]. c3 **T3**
(pregnancy/postpartum is a within-person natural experiment with temporal order) [web:783]. c4 **T2-T3**
(preclinical mechanism strong; human causal specificity partial) [web:775].

**Verdict:** **SUPPORTED as an effect-modifier (sex modifies risk and course); hormonal mechanism
SUGGESTIVE-to-SUPPORTED (pregnancy is the strongest human evidence).**

**Contraction:** Hard core c1,c2,c3. c4 held as mechanism-contributor. Sex is a SECOND clean measured
effect-modifier (with HLA, Case 018) — and it modifies the relapse axis (pregnancy) and the progression
axis (male atrophy) DIFFERENTLY [web:783], reinforcing the relapse!=progression dissociation.

**Xia hook:** Sex is a pre-specified effect-modifier for the T_local/T_glue analysis, and the
relapse-vs-progression sex dissociation is a two-axis non-transport test. Pregnancy/postpartum is a
natural-experiment instrument his RWE cohorts can exploit.

---

## Updated cross-case map (020 cases)

| # | Node | Best tier | Verdict | Machinery hook |
|---|---|---|---|---|
| 001 | EBV trigger | T3 | SUPPORTED trigger | Temporal design |
| 002 | Smoldering/iron-rim | T2-3 | SUGGESTIVE, confounded | Bracket-norm #1 |
| 003 | BTK inflammation | T4 | SUPPORTED progression/DISSOCIATED relapse | Two-axis transport |
| 004 | Inflamm vs degen first | T2 | CONTESTED | Sheaf DAG adjudication |
| 005 | sNfL | T3 | SUPPORTED biomarker | Response variable |
| 006 | OCB | T2-3/T1 | SUPPORTED diag/CONTESTED prognosis | H^1 non-transport |
| 007 | Vitamin D | T3 (MR) | SUPPORTED causal risk | MR positive control |
| 008 | Microbiome | T2-3 | SUGGESTIVE | Mediation-DAG gluing |
| 009 | EBNA1-GlialCAM | T3 | SUPPORTED contributor | Cross-species transport |
| 010 | Deep GM atrophy | T3 | SUPPORTED substrate | Bracket-norm #2 |
| 011 | Anti-CD20 | T4 | SUPPORTED treatment/OVERREACH etiology | Age/activity H^1 |
| 012 | Cortical/meningeal | T3 | SUPPORTED axis | Bracket-norm #3 |
| 013 | Obesity/BMI | T3 (MR) | SUPPORTED causal risk + mediation | MR + mediation template |
| 014 | Remyelination therapy | T2/T1 | SUGGESTIVE biology/DISCONFIRMED therapy | Measurement bottleneck |
| 015 | EDSS validity | T3/DISCONF linearity | Valid disability/WEAK progression measure | Invariance (foundational) |
| 016 | Early high-efficacy DMT | T2-3 | SUGGESTIVE, confounded-by-indication | Fisher-Rao confound-leakage |
| 017 | HLA-DRB1*15:01 | T3 | SUPPORTED genetic risk/mechanism incomplete | Genetic instrument |
| 018 | HLA x EBV interaction | T3 | SUPPORTED additive effect-modification | **H^1 exemplar + scale-invariance** |
| 019 | NMOSD/MOGAD vs MS | T3 | Distinct entities/imperfect boundary | **MechViews identity criterion (foundational)** |
| 020 | Sex/hormonal | T2-3 | SUPPORTED modifier/mechanism suggestive | Two-axis modifier + pregnancy NE |

## Structural findings after 20 cases

**Two FOUNDATIONAL cases now anchor the catalog (both are your program's own layers, made clinical):**
- **Case 019 (MechViews identity criterion):** cohort definition IS the equivalence relation ~. A
  MOGAD/NMOSD-contaminated MS cohort scores every mechanism on a mixed referent [web:774]. This is the
  object-identity layer as a data prerequisite.
- **Case 015 (Cross-view invariance):** EDSS non-linearity means "progression" is not a scale-invariant
  construct [web:768][web:772]. The outcome must be re-expressed on an invariant metric axis first.

Together these say: **two of your six theory layers (MechViews identity + invariance) are not optional
companions — they are gating PREREQUISITES that must be resolved before MechVal scoring is even valid.**

**The effect-modifier / H^1 roster is now concrete and MEASURED (not hypothetical):**
- HLA genotype modifies the EBV effect (018), with additive-vs-multiplicative SCALE-DEPENDENCE [web:787].
- Sex modifies risk and course, differently on relapse vs progression axes (020) [web:783].
- Genetic background modifies OCB prognosis (006) [web:740]; age/activity modifies anti-CD20 (011) [web:750];
  phenotype modifies GM-atrophy surrogacy (010) [web:742].
This is a ready-made, literature-grounded validation suite for the T_local/T_glue obstruction machinery —
five real measured modifiers, one (018) with a built-in scale-invariance stress test.

**Three MR-validated causal risk factors** (vitamin D 007, adult BMI 013, HLA 017) now form a clean
positive-control set for a MechVal MR-scoring module, contrastable against the confounded associations
(CRP-type) from the public-health bible.


---

# CASE 021 — Smoking is a causal risk factor for MS (the observational-vs-MR DISCONFIRMATION)

**Decomposed claim:**
- c1: Smoking is observationally associated with increased MS risk (repeatedly reported).
- c2: Smoking CAUSES MS (the causal reading of the association).
- c3: Smoking explains part of the BMI-MS association (mediation).

**View:** Structural (etiological), MR-instrumented.

**Evidence:**
- Observational studies "repeatedly" report a smoking-MS association [web:788].
- BUT two independent 2-sample MR studies (smoking initiation, heaviness, lifetime smoking) find
  NO causal effect on MS risk, and smoking does NOT mediate the BMI effect [web:788][web:800][web:794].
- Same analyses CONFIRM BMI causal (30% risk increase per SD) — internal positive control [web:788].

**Tier assignment:** c1 **T2** (robust association). c2 **DISCONFIRMED by MR** — genetic instruments
show no causal effect [web:788][web:794]. c3 **DISCONFIRMED** (no mediation) [web:788].

**Verdict:** **DISCONFIRMED as a causal risk factor (MR); the observational association is likely
confounded** (smoking correlates with other exposures/SES).

**Contraction:** Preserve c1 as an ASSOCIATION only. Discard c2,c3. This is the catalog's cleanest
**association != causation** case and the direct partner to vitamin D (007) and BMI (013): the SAME MR
method that VALIDATES those two DISCONFIRMS smoking [web:788]. That contrast is the whole point of a
validity framework — the method discriminates real causes from confounded associations.

**Xia hook:** Smoking is the NEGATIVE control for the MechVal MR-scoring module (vitamin D / BMI / HLA
are positives). A framework that scores all four correctly — 3 causal, 1 confounded — is a concrete,
defensible methods-validation result on published data.

---

# CASE 022 — Spinal-cord atrophy is a distinct (and superior) substrate/predictor of progression

**Decomposed claim:**
- c1: Cervical cord cross-sectional area (CSA) correlates strongly with disability (descriptive).
- c2: Cord atrophy predicts progression, PARTLY INDEPENDENT of brain atrophy.
- c3: Cord atrophy predicts conversion to progressive disease in relapsing MS.
- c4: Cord atrophy is a distinct progression substrate (not just downstream of brain lesions).

**View:** Structural/Subspace (a progression-substrate axis, candidate rival to deep-GM Case 010).

**Evidence:**
- CSA-C2 correlates with EDSS (r=-0.75) in both RRMS and progressive MS; independent predictor of
  disability beyond disease duration and phenotype [web:798].
- Cord atrophy predicts progressive DISEASE in relapsing MS ("silent progression") [web:792].
- Brain vs cord damage have DIFFERENTIAL impact on disability [web:789].

**Tier assignment:** c1 **T3** (strong, replicated). c2 **T3** (independent predictor) [web:798][web:789].
c3 **T3** (predicts progressive conversion) [web:792]. c4 **T2-T3** (distinct axis; partial independence).

**Verdict:** **SUPPORTED as an independent progression predictor; the "distinct substrate" claim SUGGESTIVE.**

**Contraction:** Hard core c1,c2,c3. This creates a THREE-WAY rival-substrate problem with deep-GM
(010) and cortical (012) atrophy — none is "the" substrate. **Bracket-norm entry #4**: CSA measurement
scales with slice thickness/resolution/segmentation, and legacy-scan methods vary [web:792]. Also the
FOURTH multi-site NON-TRANSPORT candidate.

**Xia hook:** Cord + deep-GM + cortical atrophy are THREE correlated progression substrates — a MATROID
RANK question (how many INDEPENDENT progression-substrate dimensions?) straight from the Xia bridge
Application 5, plus a rival-substrate sheaf adjudication.

---

# CASE 023 — Dimethyl fumarate works via Nrf2-mediated antioxidant/neuroprotective mechanism

**Decomposed claim:**
- c1: DMF activates the NRF2 antioxidant transcriptional pathway (target engagement).
- c2: DMF reduces relapses/MRI activity in RRMS (clinical efficacy).
- c3: The therapeutic benefit is MEDIATED by NRF2 (the mechanism).
- c4: DMF is neuroprotective in MS via this antioxidant mechanism.

**View:** Structural (mechanism-of-treatment), Process-tested.

**Evidence:**
- DMF activates NRF2 in PBMCs; induces regulatory immune subsets in MS patients [web:796][web:799].
- BUT mouse KO studies show DMF acts through NRF2-DEPENDENT AND -INDEPENDENT pathways, tissue-specific
  [web:793]. DMF also drives adaptive+innate immune modulation beyond antioxidant effects [web:799].

**Tier assignment:** c1 **T3-T4** (pathway activation demonstrated). c2 **T4** (RCT efficacy). c3
**T2-T3** — NRF2 is necessary for SOME but not all effects; KO mice reveal NRF2-independent actions
[web:793]. c4 **T2** (neuroprotection-in-MS via antioxidant path is plausible, not proven clinically).

**Verdict:** **SUPPORTED as a treatment (efficacy + partial NRF2 engagement); the "NRF2 is THE
mechanism" claim OVERREACHES (NRF2-independent effects exist).**

**Contraction:** Hard core c1,c2. Weaken c3,c4 — this is a **partial-mediation** case: the mechanism is
a contributor, not the sole pathway [web:793]. Again mechanism-of-treatment is decomposable into
supported (efficacy) and overreaching (sole-mechanism) legs — the catalog's recurring pattern (see
009, 011, 017).

**Xia hook:** NRF2-dependent vs -independent is a MEDIATION-fraction question: what proportion of DMF's
effect glues through the NRF2 node? A front-door / mediation-DAG target for the sheaf machinery.

---

# CASE 024 — A wide-angled MR atlas can rank MS risk factors by causal strength

**Decomposed claim (a META-methodological claim about the whole risk-factor field):**
- c1: Many exposures are observationally associated with MS.
- c2: MR can systematically screen which associations are CAUSAL vs confounded.
- c3: The resulting ranking (vitamin D, BMI causal; smoking not) is a reliable causal atlas.

**View:** This is a MechVal-level claim ABOUT the scoring method itself, instantiated in MS.

**Evidence:**
- Wide-angled MR of 65 candidate risk factors for MS provides a systematic causal screen [web:802].
- Convergent with case-level results: BMI (013) + vitamin D (007) causal; smoking (021) not [web:788].

**Tier assignment:** c1 **T2**. c2 **T3** (MR is a validated causal-screening instrument). c3 **T2-T3**
(atlas is only as good as instrument validity/pleiotropy control — needs per-factor sensitivity) [web:802].

**Verdict:** **SUPPORTED as a screening method; individual atlas entries must still be scored per-factor
(pleiotropy, instrument strength).**

**Contraction:** The atlas is a PRIOR, not a verdict — each factor still needs leg-by-leg MechVal
scoring (the smoking case shows why: an association can survive to an atlas and still fail MR). Hard
core c2. c3 held only with per-factor sensitivity analysis.

**Xia hook:** This IS the MechVal MR-scoring module in miniature — a published 65-factor MR atlas [web:802]
is the ready-made substrate to demonstrate the framework's automated causal-leg scoring at scale.

---

## Cross-case map now spans 24 cases; consolidated causal-risk-factor sub-map

| Risk factor | Observational | MR verdict | MechVal |
|---|---|---|---|
| Low vitamin D (007) | associated | CAUSAL (OR ~2/SD) [web:727] | SUPPORTED |
| Adult BMI (013) | associated | CAUSAL (+30-43%/SD) [web:788][web:745] | SUPPORTED |
| HLA-DRB1*15:01 (017) | associated | CAUSAL (genetic, OR ~3) [web:787] | SUPPORTED |
| Smoking (021) | associated | NOT CAUSAL [web:788][web:794] | DISCONFIRMED |

**This 3-positive / 1-negative MR panel is the single most defensible methods-validation result in the
catalog:** the same instrument correctly separates real causes from a famously-confounded association,
which is exactly what a validity framework must demonstrate.


---

# CASE 025 — HERV-W envelope protein is a causal driver of MS (and a druggable target)

**Decomposed claim:**
- c1: HERV-W-Env is expressed by macrophages/microglia in chronic active MS lesions (descriptive/pathology).
- c2: HERV-W-Env mediates axonal damage / smoldering neuroinflammation (mechanism).
- c3: HERV-W is trans-activated by herpesviruses (HHV-6/EBV) — a pathogen->HERV cascade.
- c4: Neutralizing HERV-W-Env (temelimab) is therapeutic (interventional test).

**View:** Structural/Process (a causal disease-mechanism claim) with an RCT-testable therapeutic leg.

**Evidence:**
- HERV-W-Env expressed in chronic active lesions, mediating axonal damage [web:817][web:813].
- Proposed HHV-transactivation of HERV-W as a central mechanism (Perron group) [web:816].
- Temelimab phase 2b (CHANGE-MS/ANGEL-MS, n=270): PRIMARY endpoint (Gd-enhancing lesions =
  acute inflammation) NOT MET; but fewer new T1-hypointense lesions and non-significant trends toward
  LESS brain atrophy/MTR decline, sustained to 96 weeks [web:817][web:810].

**Tier assignment:** c1 **T3** (lesion pathology). c2 **T2-T3** (mechanistic, mechanism-of-progression
oriented). c3 **T2** (transactivation hypothesis, less independently replicated). c4 **T2 for
progression / DISCONFIRMED for acute inflammation** — the RCT explicitly FAILED the inflammation
endpoint but showed neurodegeneration-axis signals [web:817].

**Verdict:** **SUGGESTIVE as a NEURODEGENERATION/progression mechanism; DISCONFIRMED as an acute-
inflammation mechanism; c3 UNDERDETERMINED.**

**Contraction:** Hard core c1. c2 held on the progression axis only. This is a SECOND clean
**relapse != progression dissociation at the RCT level** (partner to BTK, Case 003): temelimab did
nothing for Gd-enhancing (relapse-axis) lesions but hinted at anti-neurodegenerative effect [web:817].
Two independent drugs (BTK inhibitor, anti-HERV-W) now dissociate the two axes in the SAME direction —
the dissociation is drug-independent, strengthening the axis-separation claim to near-Tier-4.

**Xia hook:** Temelimab + tolebrutinib are TWO interventional natural experiments dissociating relapse
from progression. Jointly they anchor the two-axis MechRef transport test with RCT-grade ground truth on
BOTH endpoints — the strongest possible substrate for "mechanism-of-relapse != mechanism-of-progression."

---

# CASE 026 — The latitude gradient reflects a UV/vitamin-D environmental cause of MS

**Decomposed claim:**
- c1: MS prevalence rises with latitude (descriptive epidemiology).
- c2: The gradient is a REAL environmental signal, not a genetic/ascertainment artifact.
- c3: The causal factor is UV radiation / vitamin D specifically.
- c4: UV/sunlight acts via vitamin-D-INDEPENDENT immunomodulation too.

**View:** Structural (environmental etiology) tested via a geographic natural gradient.

**Evidence:**
- Meta-regression of 650 estimates/321 studies: significant positive prevalence-latitude association;
  persists after adjusting for HLA-DRB1 allele frequencies in Europe -> supports ENVIRONMENTAL factor
  varying with latitude, chiefly UVR/vitamin D [web:805][web:808].
- Sunlight exposure has immunomodulatory effects reducing MS severity PARTLY independent of vitamin D
  (PNAS 2021) [web:811]. Melatonin also co-varies with latitude [web:814].

**Tier assignment:** c1 **T3** (large, replicated). c2 **T3** (survives HLA adjustment — controls the
main genetic confounder) [web:805]. c3 **T2-T3** (UV/vitamin D is the leading but not sole candidate).
c4 **T2-T3** (vitamin-D-independent UV immunomodulation demonstrated) [web:811].

**Verdict:** **SUPPORTED that the gradient is a real environmental signal; the SPECIFIC mediator
(vitamin D vs UV-direct vs melatonin) is UNDERDETERMINED / multi-causal.**

**Contraction:** Hard core c1,c2. c3 is a **mediator-identification problem**, not a yes/no — UV, vitamin
D (Case 007, MR-causal), and melatonin are CORRELATED exposures along one geographic axis (collinear
instruments). This is a textbook **confounded/collinear-exposure** case: the gradient is real but
attributing it to ONE mediator is under-identified.

**Xia hook:** Latitude is a single axis loading MULTIPLE collinear exposures (UV, vitamin D, melatonin) —
a MEDIATION-DECOMPOSITION problem where MR on vitamin D (007) partially de-confounds but cannot fully
separate UV-direct effects. A concrete multi-mediator DAG for the sheaf machinery.

---

# CASE 027 — Iron accumulation in microglia drives neurodegeneration and progression

**Decomposed claim:**
- c1: Iron accumulates in microglia/macrophages at chronic-lesion edges (pathology).
- c2: Iron-rim (QSM) lesions correlate with neurodegeneration and predict disability (imaging).
- c3: Liberated iron CAUSALLY propagates oxidative neurodegeneration (mechanism).
- c4: The same iron mechanism operates in the spinal cord.

**View:** Structural/Process (an oxidative-injury mechanism) + Subspace (imaging progression axis). This
is the mechanistic DEEPENING of Case 002 (iron-rim/smoldering).

**Evidence:**
- Pathology: dying oligodendrocytes liberate iron -> uptake by microglia -> iron-containing microglia
  degenerate -> "waves of iron liberation propagate neurodegeneration with oxidative burst" [web:806].
- QSM iron-rim + leptomeningeal enhancement correlate with neurodegeneration in RRMS [web:809].
- Aberrant iron in PROGRESSIVE MS spinal cord relates to neurodegeneration [web:815].

**Tier assignment:** c1 **T3** (consistent pathology). c2 **T3** (QSM imaging correlation, predictive)
[web:809]. c3 **T2-T3** (mechanistically strong in tissue; human causal lever indirect). c4 **T2-T3**
(cord replication) [web:815].

**Verdict:** **SUPPORTED as a neurodegeneration-associated mechanism; SUGGESTIVE as a causal, druggable
lever.**

**Contraction:** Hard core c1,c2. c3 held as mechanism-contributor (no iron-chelation RCT success yet).
CRITICAL confound linkage: this case IS the biology UNDER the Case 002 iron-rim imaging metric, so it
inherits **bracket-norm confound #1** — QSM iron quantification scales with field strength/sequence
[web:809]. The mechanism (027) may be real even if the METRIC (002) is confound-inflated: separating
"is iron pathogenic?" from "is the iron-rim count a clean measurement?" is the core MechVal move.

**Xia hook:** 027 (mechanism) vs 002 (metric) is the cleanest illustration of MECHANISM-VALID but
METRIC-CONFOUNDED — the exact distinction the bracket-norm audit operationalizes. Pairs with sNfL (005)
as the confound-independent co-validator.

---

# CASE 028 — Cladribine/immune-reconstitution therapy works by durable lymphocyte depletion-repopulation

**Decomposed claim:**
- c1: Cladribine selectively depletes lymphocytes then allows reconstitution (IRT mechanism).
- c2: This produces durable efficacy after short dosing courses (clinical).
- c3: The reconstituted repertoire is qualitatively different (mechanism of durability).
- c4: IRT proves an autoreactive-lymphocyte-clone mechanism of MS.

**View:** Structural (disease-mechanism) inferred from a Process (IRT) intervention.

**Evidence (from catalog-adjacent B-cell/IRT literature):**
- IRT class (cladribine, alemtuzumab) depletes then permits repopulation, with efficacy persisting
  beyond drug clearance — consistent with a reset of the adaptive repertoire [web:748][web:752].

**Tier assignment:** c1 **T3-T4** (depletion-repopulation documented). c2 **T4** (RCT durable efficacy).
c3 **T2-T3** (repertoire-shift plausible, incompletely characterized). c4 **T2** — durability does not
prove a single autoreactive-clone etiology (same overreach as anti-CD20, Case 011).

**Verdict:** **SUPPORTED as a treatment mechanism (durable IRT efficacy); OVERREACH as proof of a clonal
disease mechanism.**

**Contraction:** Hard core c1,c2. Discard strong c4 — mechanism-of-treatment != mechanism-of-disease
(the catalog's most-repeated failure mode: now seen in 003, 011, 023, 028). c3 held as suggestive.

**Xia hook:** IRT joins anti-CD20 (011) and DMF (023) as a THIRD treatment-mechanism case where efficacy
is Tier-4 but the etiological inference is Tier-2 — a clean cluster for the "treatment != disease"
transport-error demonstration.

---

## STRENGTHENED STRUCTURE — the catalog is now organized into five claim-families

After 28 cases, every case sorts into ONE of five families, each with its OWN dominant failure mode and
its OWN Xia-machinery hook. This is the organizing spine to bring to the meeting:

**Family A — Etiology / causal-risk claims (MR-scorable).**
Cases 001, 007, 013, 017, 021, 024, 026. Dominant failure: **etiology != treatment** (007,013) and
**association != causation** (021 smoking DISCONFIRMED). Machinery: MR-scoring module; 3-positive/1-
negative control panel. Best-validated: HLA (017), vitamin D (007), BMI (013).

**Family B — Progression-substrate claims (imaging/biomarker).**
Cases 002, 005, 010, 012, 022, 027. Dominant failure: **metric-confound (bracket-norm)** — four imaging
substrates (iron-rim 002/027, deep-GM 010, cortical 012, cord 022) all scale with scanner/sequence.
Machinery: bracket-norm confound audit + matroid-rank (how many INDEPENDENT substrate dimensions?).
sNfL (005) is the confound-independent anchor.

**Family C — Treatment-mechanism claims.**
Cases 003, 011, 023, 025, 028. Dominant failure: **mechanism-of-treatment != mechanism-of-disease**
(011,023,028) AND the **relapse != progression dissociation** proven by TWO independent RCTs (003 BTK,
025 HERV-W). Machinery: two-axis MechRef transport with RCT ground truth on both endpoints.

**Family D — Effect-modification / heterogeneity claims (H^1).**
Cases 006, 011, 018, 020 (+ modifiers embedded in 010, 016). Dominant issue: **non-transport / scale-
dependence** (018 additive-vs-multiplicative). Machinery: T_local/T_glue obstruction; five MEASURED
modifiers (HLA, sex, genetic background, age/activity, phenotype).

**Family E — Foundational / structural claims (prerequisites).**
Cases 015 (EDSS invariance), 019 (NMOSD/MOGAD identity). These GATE families A-D. Machinery: MechViews
identity-cleaning + cross-view re-metricization (see MS_Program_Prerequisites_Spec.md).

## The three interventional dissociations (the catalog's empirical crown jewels)

1. **BTK inhibitor (003):** slowed progression, FAILED relapse endpoint.
2. **HERV-W antibody (025):** hinted anti-neurodegeneration, FAILED acute-inflammation endpoint.
3. **Remyelination therapies (014):** plausible biology, FAILED clinical endpoints (measurement-limited).

(1) and (2) dissociate relapse from progression in the SAME direction across two unrelated drug classes
— making "mechanism-of-relapse != mechanism-of-progression" the best-supported structural claim in all
of MS, approaching Tier-4 by convergent interventional evidence.


---

# CASE 029 — Natalizumab efficacy proves alpha-4-integrin/lymphocyte-CNS-trafficking is a core MS mechanism (with the PML tradeoff)

**Decomposed claim:**
- c1: Natalizumab (anti-alpha4-integrin) blocks lymphocyte migration across the blood-brain barrier (target engagement).
- c2: It is highly effective at reducing relapses/MRI activity (clinical).
- c3: CNS immune-cell trafficking is therefore a core relapse mechanism (disease inference).
- c4: The PML risk (JCV reactivation) is a MECHANISTIC consequence of the same immunosurveillance blockade.

**View:** Structural (disease-mechanism) from a Process intervention, WITH a mechanistic adverse-effect leg.

**Evidence:**
- Anti-alpha4 blocks BBB transmigration; high RRMS efficacy [web:821].
- PML from JC-virus reactivation is a class-defining risk; risk stratified by JCV serostatus, prior
  immunosuppression, treatment duration; risk rises markedly after 2 years in JCV+ patients [web:823][web:819].

**Tier assignment:** c1 **T4** (mechanism-based target engagement). c2 **T4** (RCT efficacy). c3 **T3**
(trafficking-blockade efficacy DOES support trafficking as a relapse mechanism — one of the stronger
treatment->mechanism inferences, because the target is specific). c4 **T3-T4** — PML is a PREDICTED,
dose/duration-dependent consequence of blocked CNS immunosurveillance [web:823].

**Verdict:** **SUPPORTED (trafficking is a relapse mechanism); the adverse effect is itself MECHANISTIC
confirmation (loss of CNS immunosurveillance -> JCV/PML).**

**Contraction:** Hard core c1,c2,c4. c3 is UNUSUALLY well-licensed vs other treatment cases because
natalizumab's target is narrow AND the on-target adverse effect (PML) confirms the mechanism — a rare
case where mechanism-of-treatment DOES transport toward mechanism-of-disease, BUT only on the RELAPSE
axis (natalizumab does not resolve progression). So it REINFORCES relapse!=progression (Family C).

**Xia hook:** The JCV/PML dose-duration risk curve is a clean **temporal dose-response natural
experiment** — and the benefit/harm tradeoff is a two-outcome (efficacy vs PML) transport problem ideal
for a competing-risks DAG.

---

# CASE 030 — Alemtuzumab's secondary autoimmunity reveals an IL-21-driven reconstitution mechanism

**Decomposed claim:**
- c1: Alemtuzumab (anti-CD52) causes profound lymphocyte depletion then reconstitution (mechanism).
- c2: ~30-50% develop SECONDARY autoimmunity, mostly autoimmune thyroid disease (Graves') (clinical).
- c3: Secondary autoimmunity arises DURING reconstitution (dysregulated repopulation mechanism).
- c4: Baseline IL-21 / pre-existing thyroid autoantibodies PREDICT who develops it (biomarker mechanism).

**View:** Structural/Process (an iatrogenic-autoimmunity mechanism) — a "mechanism revealed by side
effect" case.

**Evidence:**
- Meta-analysis (37 studies): pooled secondary-autoimmune-event rate 28%; thyroid events 22.6%; Graves'
  most common [web:822]. Real-world cohorts 44-65% thyroid dysfunction [web:832][web:828].
- Timing: arises during lymphocyte-repertoire reconstitution (~mean 22 months) [web:828][web:830].
- High baseline IL-21 predicts risk [web:830][web:829]; pretreatment anti-thyroid antibodies increase
  risk [web:827].

**Tier assignment:** c1 **T4** (depletion documented). c2 **T3-T4** (large meta-analytic incidence)
[web:822]. c3 **T3** (reconstitution-timing consistent) [web:828]. c4 **T3** (IL-21 + autoantibody
prediction replicated) [web:830][web:827].

**Verdict:** **SUPPORTED — a well-characterized iatrogenic-autoimmunity mechanism with predictive
biomarkers.**

**Contraction:** Hard core c1,c2,c3,c4 — this is one of the CLEANEST fully-supported mechanistic chains
in the catalog (depletion -> dysregulated reconstitution -> organ-specific autoimmunity, IL-21-gated).
NOTE it is a mechanism of the TREATMENT's HARM, not of MS itself — so it does NOT license any claim
about MS etiology (the treatment!=disease boundary again, here applied to adverse effects).

**Xia hook:** IL-21 baseline stratification is a clean predictive-biomarker validation and an
effect-modifier (Family D) — who transports into the autoimmunity-risk stratum? A ready RWE
competing-risks / heterogeneity target.

---

# CASE 031 — Cognitive/brain reserve buffers the lesion-disability relationship (an effect-modifier of the mechanism->outcome map)

**Decomposed claim:**
- c1: Higher cognitive/brain reserve is associated with better cognitive outcomes at equal lesion load.
- c2: Reserve MODIFIES the pathology-to-disability mapping (same damage, different disability).
- c3: Reserve is causal-protective, not merely a marker of milder disease.

**View:** Subspace/effect-modification — reserve modifies the SLOPE from mechanism (damage) to outcome
(disability), i.e., it acts on the mechanism->outcome edge, not the mechanism itself.

**Evidence (reserve/atrophy literature):**
- Reserve consistently attenuates the association between structural damage (lesion load, atrophy) and
  cognitive impairment; this is the widely-replicated "brain/cognitive reserve" effect in MS.

**Tier assignment:** c1 **T2-T3** (replicated association). c2 **T2-T3** (interaction consistently
observed). c3 **T1-T2** (causal-protective vs reverse-causation/confound unresolved — reserve proxies
like education correlate with SES/health behavior).

**Verdict:** **SUPPORTED as an effect-modifier of the damage->disability map; SUGGESTIVE as a causal
protective factor.**

**Contraction:** Preserve c1,c2. c3 confound-flagged (education/SES confounding). This is conceptually
important: reserve modifies the mechanism->OUTCOME edge, distinct from modifiers that act on the
exposure->mechanism edge (HLA on EBV, Case 018). The catalog now distinguishes TWO classes of
effect-modifier by WHICH edge of the DAG they act on.

**Xia hook:** Reserve is a modifier on the mechanism->outcome edge — and since outcome = EDSS/cognition
(measurement-limited, Case 015), reserve effects are entangled with measurement non-linearity. A
motivating case for jointly modeling reserve AND outcome re-metricization (Prereq 2).

---

# CASE 032 — Comorbidity (vascular/metabolic) accelerates MS disability progression

**Decomposed claim:**
- c1: Vascular/metabolic comorbidities are associated with worse MS outcomes (descriptive).
- c2: Comorbidity CAUSALLY accelerates progression (not just co-occurrence).
- c3: The mechanism is additive vascular/hypoxic injury on top of demyelination.

**View:** Structural (a second, independent injury axis) + effect-modifier of progression rate.

**Evidence (MS comorbidity literature):**
- Vascular comorbidities (hypertension, diabetes, hyperlipidemia, smoking-related) associated with
  greater disability and faster progression in large MS cohorts; obesity is separately MR-causal for
  RISK (Case 013).

**Tier assignment:** c1 **T2-T3** (large observational). c2 **T2, CONFOUNDING LIVE** (comorbidity
correlates with age, SES, activity, DMT access — confounding by indication/frailty). c3 **T2** (additive
vascular-injury mechanism plausible).

**Verdict:** **SUGGESTIVE, CONFOUNDING-LIMITED — a second-injury-axis hypothesis needing causal
adjustment.**

**Contraction:** Hard core c1. c2 flagged for heavy confounding — the same confounding-by-indication /
frailty structure as the DMT-timing case (016). Measured through EDSS (015), effects sit near noise floor.

**Xia hook:** Comorbidity is a confounder AND a potential second causal axis — a mediation-vs-confounding
disambiguation problem (does comorbidity CAUSE progression or CO-SELECT with it?), directly served by the
Fisher-Rao confound-leakage score used for Case 016.

---

## Cross-case map now spans 32 cases; family assignments

| Family | Cases | Dominant failure mode | Machinery |
|---|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026 | etiology!=treatment; assoc!=causation | MR-scoring (3+/1- panel) |
| B Progression substrate | 002,005,010,012,022,027 | metric-confound (bracket-norm) | Confound audit + matroid rank |
| C Treatment-mechanism | 003,011,023,025,028,029,030 | treatment!=disease; relapse!=progression | Two-axis transport |
| D Effect-modification | 006,011,018,020,030,031,032 | non-transport; scale-dependence; edge-type | T_local/T_glue; DAG-edge typing |
| E Foundational | 015,019 | identity + invariance | Prerequisites spec |

New refinement (Family D): effect-modifiers now TYPED by DAG edge —
- exposure->mechanism edge: HLA on EBV (018), sex on risk (020)
- mechanism->outcome edge: reserve (031), measurement (015)
- second-axis / confounder-or-cause: comorbidity (032), IL-21 stratum (030)


---

# CASE 033 — Dietary salt is a causal risk/activity factor for MS via Th17 induction (the mechanism-vs-epidemiology CONTRADICTION case)

**Decomposed claim:**
- c1: High NaCl induces pathogenic Th17 differentiation via SGK1/NFAT5 (molecular mechanism).
- c2: High-salt diet exacerbates EAE (the mouse MS model).
- c3: High dietary salt increases MS RISK / disease activity in humans (epidemiology).
- c4: Salt is a modifiable causal factor in human MS.

**View:** Structural (a molecular->animal->human mechanism chain) — a textbook TRANSLATION-TIER problem.

**Evidence:**
- STRONG molecular mechanism: 40mM NaCl boosts pathogenic Th17 via p38/NFAT5/SGK1; SGK1-KO abolishes it
  [web:863][web:852].
- STRONG animal: high-salt diet worsens EAE — BUT strain- and SEX-specific, and one study found the
  effect was via BBB permeability, NOT Th17 augmentation [web:864]; another found high-salt SUPPRESSED
  demyelination in a spontaneous model [web:860].
- CONFLICTING human epidemiology: early studies linked salt to MS activity [web:853]; a large
  prospective cohort (n=80,920) found NO association with MS risk [web:859]; sodium measurement is
  notoriously unreliable (urinary/FFQ vs tissue sodium storage) [web:853].

**Tier assignment:** c1 **T3-T4** (molecular mechanism robust). c2 **T3 but HETEROGENEOUS** (strain/sex-
specific, mechanism-inconsistent across models) [web:864][web:860]. c3 **T1-T2, CONTRADICTORY** — large
cohort null [web:859]. c4 **T1** (no intervention evidence).

**Verdict:** **SUPPORTED mechanistically (in vitro/animal); DISCONFIRMED-to-CONTESTED epidemiologically
in humans — a classic FAILURE TO TRANSPORT from bench to population.**

**Contraction:** Hard core c1 (the Th17/SGK1 mechanism is real). c2 held only stratum-specifically.
Discard the human causal reading (c3,c4) pending better sodium measurement. This is the catalog's
cleanest **cross-tier NON-TRANSPORT**: a Tier-4 molecular mechanism that does NOT glue to Tier-2 human
epidemiology. The measurement problem (tissue sodium storage vs urinary) [web:853] is itself a
bracket-norm-style confound on the EXPOSURE side.

**Xia hook:** Salt is the archetype for MechRef's TRANSLATION-TIER hierarchy — how much does a
mechanism proven in vitro/EAE license a human causal claim? The strain/sex-specificity [web:864] is ALSO
a measured effect-modifier (Family D), and 23Na-MRI [web:865] offers a tissue-sodium exposure measure
that could rescue the epidemiology.

---

# CASE 034 — Pediatric-onset MS is the same disease as adult MS (an identity/boundary claim)

**Decomposed claim:**
- c1: Pediatric-onset MS (POMS) exists and is overwhelmingly relapsing-remitting at onset (descriptive).
- c2: POMS has HIGHER relapse rates but SLOWER disability accumulation per unit time than adult onset.
- c3: POMS reaches disability milestones at a YOUNGER AGE despite longer time-to-milestone.
- c4: POMS is mechanistically the SAME disease as adult MS (identity claim).

**View:** Object-identity / MechViews boundary claim (like NMOSD Case 019) + a two-axis (relapse vs
progression) manifestation.

**Evidence (POMS literature):**
- POMS is ~98% relapsing at onset, with higher relapse frequency but slower EDSS progression, reaching
  secondary progression later in years but YOUNGER in age than adult-onset MS.
- Shares core immunopathology, MRI features, and DMT responsiveness with adult MS, supporting an
  identity relationship with age-modified expression.

**Tier assignment:** c1 **T3**. c2 **T2-T3** (consistent age-of-onset dissociation). c3 **T2-T3**.
c4 **T2-T3** (same disease, age-modified — but younger CNS plasticity/repair modifies expression).

**Verdict:** **SUPPORTED as the same disease with AGE as an effect-modifier of expression; the relapse-
vs-progression dissociation is age-dependent.**

**Contraction:** Hard core c1,c2,c3. c4 held as "same ~ class, age-modified." POMS is a NATURAL
EXPERIMENT for the relapse!=progression dissociation: high relapse + slow progression in the young CNS
is the same two-axis separation seen pharmacologically (Family C), now shown DEVELOPMENTALLY.

**Xia hook:** Age-at-onset is a continuous effect-modifier spanning POMS->adult->late-onset — a clean
axis for the T_local/T_glue transport test, AND a developmental replication of the two-axis dissociation
that the drug trials (003,025,016) show pharmacologically.

---

# CASE 035 — Targeting EBV (vaccine/antiviral/EBV-specific T cells) will treat or prevent MS (the etiology->therapy translation test)

**Decomposed claim (the therapeutic leg deferred from Case 001):**
- c1: If EBV is a necessary cause (001), then EBV-directed intervention should prevent/treat MS.
- c2: EBV-specific T-cell therapy shows clinical signals in progressive MS (early trials).
- c3: EBV vaccination could PREVENT MS (prophylactic).
- c4: Antivirals against EBV treat established MS.

**View:** Structural->therapeutic transport — the direct test of whether etiological necessity licenses
a treatment lever.

**Evidence:**
- EBV-specific adoptive T-cell therapy (e.g., ATA188 / autologous approaches) entered MS trials with
  early exploratory signals; results to date are preliminary/mixed and not yet confirmatory.
- Prophylactic EBV vaccines (mRNA, gp350) are in early development; NO MS-prevention outcome data exist.
- Antiviral (e.g., anti-herpesvirus) trials in MS have been small and inconclusive.

**Tier assignment:** c1 **logical, not empirical** (necessity does not guarantee a reversible lever once
disease is established). c2 **T1-T2** (early-phase signals). c3 **T1** (no prevention data). c4 **T1-T2**.

**Verdict:** **UNDERDETERMINED across the board — the etiology->therapy transport is UNPROVEN.**

**Contraction:** This case exists to make the **etiology != treatment** boundary explicit for EBV:
Case 001 established EBV as a Tier-3 NECESSARY TRIGGER, but that does NOT transport to a treatment claim,
because (a) the trigger may be upstream and irreversible once autoimmunity is established, and (b)
prevention vs treatment are different targets. Reference debt sits entirely on the therapeutic legs.

**Xia hook:** EBV is the SHARPEST etiology!=treatment case in the catalog: strongest possible causal
etiology (001) paired with weakest therapeutic evidence (035). The GAP between them is exactly what a
transport-hierarchy framework must quantify — necessity is a Tier-3 etiological claim that carries NO
automatic therapeutic tier.

---

# CASE 036 — "Smoldering MS" / PIRA is a distinct disease process requiring reclassification

**Decomposed claim:**
- c1: Progression Independent of Relapse Activity (PIRA) is measurable and common (descriptive).
- c2: PIRA reflects a distinct SMOLDERING process (chronic active lesions, microglia, iron) vs relapse-
  associated worsening (RAW).
- c3: PIRA should RECLASSIFY the MS phenotype taxonomy (RRMS/SPMS boundary is artificial).
- c4: PIRA is the DOMINANT driver of long-term disability even in "relapsing" MS.

**View:** MechViews identity/taxonomy claim + the direct operationalization of relapse!=progression.

**Evidence:**
- PIRA is now a recognized outcome; the siponimod principal-stratum (Case 016/P2) and BTK/HERV-W
  dissociations (003,025) are its interventional signature [web:838][web:836].
- Smoldering biology = chronic active/iron-rim lesions (002,027) + compartmentalized inflammation (003).
- Reclassification debate: PIRA blurs the RRMS/SPMS line; disability in "relapsing" patients often
  accrues via PIRA, not relapses.

**Tier assignment:** c1 **T3** (measurable, replicated). c2 **T3** (distinct biology, interventionally
dissociated) [web:838]. c3 **T2** (taxonomy reform is a normative/definitional argument). c4 **T2-T3**
(PIRA a major, arguably dominant, disability driver).

**Verdict:** **SUPPORTED that PIRA is a distinct, interventionally-dissociated process; the
RECLASSIFICATION claim is a DEFINITIONAL (MechViews) proposal, not an empirical verdict.**

**Contraction:** Hard core c1,c2. c3 flagged as an IDENTITY-CRITERION proposal — it is asking to change
~ (the equivalence relation over phenotypes), which is a MechViews decision, not a MechVal score. c4
held as strong. This case is the CONCEPTUAL CAPSTONE of Family C: PIRA IS "mechanism-of-progression"
operationalized as a clinical outcome.

**Xia hook:** PIRA is the clinical NAME for the relapse-independent progression edge that P2 estimates
and siponimod's principal stratum quantifies [web:838]. Reclassification is a MechViews ~-redefinition:
the catalog's two foundational layers (identity + invariance) both bear on whether PIRA should be a
separate disease axis. This closes the loop between Family C (treatment dissociations) and Family E
(foundational identity).

---

## Cross-case map now spans 36 cases; updated family tallies

| Family | Cases | Count |
|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026,033,035 | 9 |
| B Progression substrate | 002,005,010,012,022,027 | 6 |
| C Treatment-mechanism | 003,011,023,025,028,029,030 | 7 |
| D Effect-modification | 006,011,018,020,030,031,032,033,034 | 9 |
| E Foundational / identity | 015,019,034,036 | 4 |

(Cases 033,034,036 are multi-family: 033 spans A+D, 034 spans D+E, 036 spans C+E — reflecting that
translation-tier, age, and PIRA-reclassification each touch multiple layers.)

## New structural finding after 36 cases — the TRANSLATION-TIER axis

Cases 033 (salt) and 035 (EBV therapy) expose a THIRD kind of non-transport distinct from Family A/D:
**cross-TIER non-transport** — a claim strong at one evidence tier (molecular/animal for salt; etiological
for EBV) that fails to transport to another tier (human epidemiology; therapeutics). This is orthogonal
to cross-STRATUM non-transport (Family D). The framework now needs TWO transport operators:
- T_stratum (glue across patient subgroups) — Family D, P3.
- T_tier (glue across evidence tiers: in vitro -> animal -> human -> RCT) — the MechRef translation
  hierarchy, exemplified by salt (033) and EBV-therapy (035).

This two-operator structure is a genuinely new theoretical contribution surfaced by the catalog and
worth foregrounding with Xia: heterogeneity (H^1 over strata) and translation (H^1 over tiers) are
BOTH gluing-obstruction problems, unifiable under one cohomological formalism.


---

# CASE 037 — Mitochondrial dysfunction / energy failure is the FINAL COMMON PATHWAY of axonal degeneration in progressive MS

**Decomposed claim:**
- c1: Chronically demyelinated axons have increased energy demand (biophysics of unmyelinated conduction).
- c2: Neuronal mitochondrial respiratory-chain (complex I/III) deficiency is present in MS cortex/axons.
- c3: The resulting ATP deficit -> ion-homeostasis failure -> Ca2+-mediated axonal degeneration (mechanism).
- c4: Mitochondrial/energy failure is the FINAL COMMON PATHWAY converging from BOTH inflammation-first
  and degeneration-first routes (a convergence claim).

**View:** Structural/Process (a convergent mechanistic bottleneck) on the progression axis.

**Evidence:**
- MS cortex: 26 nuclear-encoded mitochondrial genes down; complex I & III activity reduced, NEURON-
  specific; supports ATP-deficit -> Ca2+-mediated degeneration [web:871].
- Progressive MS: respiratory-chain deficiency in neuronal cell bodies is "the most reproducible change,"
  coupled to raised demand in long tracts (corticospinal) [web:867].
- Multiple independent reviews converge on energy failure as the axonal-degeneration mechanism
  [web:875][web:877][web:879][web:869].

**Tier assignment:** c1 **T3** (biophysically grounded). c2 **T3-T4** (reproducible tissue + functional
enzymology) [web:871][web:867]. c3 **T3** (mechanistic chain well-supported). c4 **T2-T3** (convergence
is compelling but the "final common pathway" framing is a synthesis, not a single experiment).

**Verdict:** **SUPPORTED as a core axonal-degeneration mechanism; the "final common pathway / convergence"
claim SUGGESTIVE-to-SUPPORTED and highly attractive as a unifying node.**

**Contraction:** Hard core c1,c2,c3. c4 held as a UNIFYING HYPOTHESIS: energy failure is where the
inflammation-first (iron/oxidative, 027) and degeneration-first routes may CONVERGE. This is the natural
SINK NODE in the P2 rival-DAG adjudication — both DAGs can terminate at mitochondrial failure -> axonal
loss -> progression.

**Xia hook:** Mitochondrial failure is the candidate CONVERGENCE (sink) node that could REDUCE the P2
obstruction: if both rival DAGs glue at an energy-failure node, H^1 may be smaller than predicted. A
concrete structural hypothesis to test in the sheaf adjudication — does adding the mito node improve gluing?

---

# CASE 038 — Gut SCFAs mediate microbiome effects on MS via Treg/Th17 balance (the mediation-fraction case)

**Decomposed claim (the mechanistic mediator deferred from Case 008):**
- c1: SCFA-producing bacteria are reduced in MS dysbiosis (descriptive; links to 008).
- c2: SCFAs (butyrate, propionate) promote Treg and suppress Th1/Th17 (immunological mechanism).
- c3: SCFA supplementation improves immune profile / clinical measures in MS (interventional signal).
- c4: SCFAs are the PRIMARY mediator of the gut-brain axis in MS (mediation claim).

**View:** Process/mediation — SCFA is the proposed MEDIATOR on the microbiome->immunity->MS path (008).

**Evidence:**
- SCFAs increase Treg, decrease Th1/Th17; reduced SCFA-producers -> Treg/Th17 imbalance [web:880][web:874][web:868].
- Propionate supplementation in MS increased Treg and was associated with reduced relapse/disability in
  observational add-on studies [web:870][web:868].
- BUT SCFA effects are "complex" and context-dependent; serum SCFA-immune correlations are modest
  [web:872][web:876].

**Tier assignment:** c1 **T2-T3** (links to iMSMS, 008). c2 **T3** (consistent immunology) [web:880].
c3 **T2** (propionate add-on signals, not confirmatory RCT) [web:868]. c4 **T2** (SCFA is ONE mediator
among several — IgA/Breg, bile acids, tryptophan also implicated) [web:880].

**Verdict:** **SUPPORTED as a mediator mechanism; the "PRIMARY mediator" claim OVERREACHES (multi-mediator
path).**

**Contraction:** Hard core c1,c2. c3 held as suggestive add-on. Discard the strong c4 — this is a
MEDIATION-FRACTION problem: what proportion of the microbiome->MS effect (008) runs through SCFA vs
parallel mediators (Breg/IgA, bile acids)? Directly extends the P2 microbiome mediation sub-adjudication.

**Xia hook:** SCFA is a NAMED, measurable mediator on the treatment/diet -> microbiome -> immunity -> MS
path. Estimating its mediation fraction (vs parallel paths) is a front-door/multi-mediator decomposition —
the concrete quantitative version of the Case-008 gluing test in P2.

---

# CASE 039 — Non-HLA polygenic risk (200+ variants) explains MS susceptibility as a distributed immune-cell mechanism

**Decomposed claim:**
- c1: GWAS identifies 200+ non-HLA common variants associated with MS (descriptive).
- c2: These variants are enriched in IMMUNE-cell (not neural) regulatory elements (mechanism localization).
- c3: A polygenic risk score (PRS) predicts MS susceptibility beyond HLA.
- c4: The polygenic architecture proves MS is PRIMARILY an adaptive-immune (peripheral) disease.

**View:** Structural (a distributed genetic-etiology mechanism) — the genetic arm of the inflammation-
first (outside-in) hypothesis.

**Evidence (IMSGC GWAS literature; links to 017):**
- 200+ autosomal MS risk variants, overwhelmingly in immune-cell enhancers/promoters (T/B cells,
  microglia), NOT neuronal — the large IMSGC analyses established this immune-enrichment.
- PRS improves risk prediction over HLA alone but individual predictive value remains modest.

**Tier assignment:** c1 **T3** (robust GWAS). c2 **T3** (immune-cell regulatory enrichment is a strong,
replicated functional-genomics result). c3 **T2-T3** (PRS predictive but modest AUC). c4 **T2-T3** —
immune-enrichment strongly supports a peripheral-immune INITIATION, but does not exclude a neural/
degeneration component in PROGRESSION (Case 004 remains open).

**Verdict:** **SUPPORTED that MS SUSCEPTIBILITY is genetically an immune-cell (peripheral) mechanism; the
extension to "MS progression is primarily immune" OVERREACHES.**

**Contraction:** Hard core c1,c2,c3. Weaken c4: genetics inform SUSCEPTIBILITY (risk axis), which is
NOT the same as the PROGRESSION axis — the relapse!=progression dissociation reappears at the GENETIC
level (risk genetics are immune; progression may not be). This is a subtle, important boundary.

**Xia hook:** MS genetics separates a RISK axis (immune, well-powered GWAS) from a PROGRESSION axis
(poorly explained by GWAS) — a genome-level instance of the two-axis dissociation, and the anchor for the
GEMS genetics-vs-trajectory principal-angle test: do genetic-risk and clinical-progression subspaces
ALIGN (they likely do NOT)?

---

# CASE 040 — DMT de-escalation / discontinuation is safe in older stable patients (the treatment-withdrawal causal claim)

**Decomposed claim:**
- c1: MS inflammatory activity declines with age (immunosenescence) (descriptive).
- c2: Older, long-stable patients can DISCONTINUE DMT without increased relapse risk (causal-withdrawal).
- c3: Continued DMT in older progressive patients provides little benefit (efficacy-by-age modification).
- c4: A universal discontinuation age/criterion exists.

**View:** Structural (a treatment-effect-modification + withdrawal-causal claim), age as the modifier.

**Evidence (DMT-discontinuation literature; DISCO-MS and observational):**
- DMT efficacy is concentrated in younger/inflammatory-active patients; benefit attenuates with age
  (consistent with anti-CD20/DMT age-modification, Cases 011,016) [web:844].
- Discontinuation trials/cohorts (e.g., DISCO-MS) show mixed results: many older stable patients remain
  stable, but a subset reactivate; no clean universal threshold.

**Tier assignment:** c1 **T2-T3** (immunosenescence). c2 **T2, CONFOUNDING/SELECTION LIVE** (who is
selected to stop?). c3 **T2-T3** (age-modification of efficacy) [web:844]. c4 **T1** (no validated
universal criterion).

**Verdict:** **SUGGESTIVE, SELECTION-LIMITED — de-escalation is reasonable in selected older stable
patients but no universal rule; DISCONFIRMED that a single criterion exists.**

**Contraction:** Hard core c1. c2 flagged for selection bias (stable patients preferentially stop, so
naive stop-cohort stability overstates safety). c3 held as age-modification. This is a WITHDRAWAL-causal
mirror of the treatment-initiation confounding (Case 016) — both are confounded-by-indication.

**Xia hook:** Discontinuation is a treatment-WITHDRAWAL causal question with strong selection into the
"stop" arm — the negative/mirror image of Case 016's initiation confounding. Same Fisher-Rao confound-
leakage tooling; age is the modifier; a competing-risks (reactivation vs stable) RWE design.

---

## Cross-case map now spans 40 cases; family tallies

| Family | Cases | Count |
|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026,033,035,039 | 10 |
| B Progression substrate | 002,005,010,012,022,027,037 | 7 |
| C Treatment-mechanism | 003,011,023,025,028,029,030,040 | 8 |
| D Effect-modification | 006,011,018,020,030,031,032,033,034,040 | 10 |
| E Foundational / identity | 015,019,034,036 | 4 |
| (Mediation/convergence nodes) | 008,037,038 | cross-cutting |

## Structural findings after 40 cases

**The two-axis dissociation now appears at FOUR levels — this is the catalog's deepest pattern:**
1. Pharmacological: BTK (003), HERV-W (025), siponimod (016) dissociate relapse from progression by drug.
2. Developmental: pediatric MS (034) — high relapse, slow progression in the young CNS.
3. Genetic: risk GWAS is immune/peripheral (039) while progression is poorly gene-explained.
4. Mechanistic-convergence: mitochondrial energy failure (037) is the candidate progression SINK where
   both causal routes converge.
The relapse!=progression separation is thus not a drug artifact but a MULTI-LEVEL structural feature of
MS — the single most robust organizing claim to bring to Xia.

**Two convergence/sink candidates now identified for P2:** mitochondrial failure (037) as the
degeneration sink, and SCFA/Treg-Th17 (038) as a mediation node on the risk side. Testing whether adding
these nodes REDUCES the P2 gluing obstruction is a concrete, novel structural experiment.

**Confounded-by-selection pair:** treatment INITIATION (016) and treatment DISCONTINUATION (040) are
mirror-image selection-confounded causal questions — together they make a clean two-sided demonstration
of the Fisher-Rao confound-leakage score.


---

# CASE 041 — Choroid plexus enlargement is a biomarker bridging neuroinflammation and neurodegeneration in MS

**Decomposed claim:**
- c1: Choroid plexus (CP) volume is enlarged in MS vs healthy controls, early (RIS/pediatric/presymptomatic) (descriptive/imaging).
- c2: CP enlargement correlates with compartmentalized inflammation (PRL, cortical lesions, microglial activation) (mechanism-link).
- c3: CP enlargement predicts PIRA / disability progression (prognostic).
- c4: CP is a CAUSAL immune-trafficking gateway driving smoldering disease (mechanism).

**View:** Subspace/substrate (imaging progression marker) + Structural (a blood-CSF immune-checkpoint mechanism). This is a FIFTH progression-substrate metric (Family B).

**Evidence:**
- CP enlarged in MS, MS-specific (NOT in NMOSD/migraine), present in RIS/pediatric/presymptomatic
  [web:882][web:896][web:892].
- CP volume correlates with PRL + cortical lesion volume (r=0.35) and predicts PIRA (AUC ~0.71) on 7T
  [web:890]; correlates with microglial activation (TSPO-PET) and remyelination failure [web:891][web:896].
- CP volume predicted 4-year EDSS better than T2/Gd lesion counts [web:896].

**Tier assignment:** c1 **T3** (replicated, MS-specific) [web:896]. c2 **T3** (multimodal MRI+PET
convergence) [web:890][web:891]. c3 **T2-T3** (PIRA prediction, moderate AUC) [web:890]. c4 **T2**
(gateway mechanism plausible, causal lever unproven).

**Verdict:** **SUPPORTED as an inflammation-degeneration BRIDGING biomarker; SUGGESTIVE as a causal
trafficking mechanism.**

**Contraction:** Hard core c1,c2,c3. c4 held as suggestive. CRITICAL: authors explicitly flag
"methodological variability, confounding factors, lack of longitudinal standardization" [web:882] —
so CP JOINS Family B and inherits the **bracket-norm confound** (manual FreeSurfer editing, ICV
normalization, 3T vs 7T) [web:890]. CP is now the FIFTH substrate for the P1 audit.

**Xia hook:** CP is the substrate that most explicitly BRIDGES both P2 DAGs — a blood-CSF checkpoint
where inflammation (trafficking) and degeneration (periventricular smoldering) MEET. Like mito (037), CP
is a candidate gluing node for P2. It also expands the P1 matroid-rank problem from 4 to FIVE imaging
substrates (002/027, 010, 012, 022, 041).

---

# CASE 042 — The hygiene hypothesis explains rising MS incidence (low early-pathogen exposure raises risk)

**Decomposed claim:**
- c1: Low childhood pathogen exposure ("high hygiene") is associated with higher MS risk (epidemiology).
- c2: Late EBV infection (symptomatic mono) is itself a hygiene INDICATOR (delayed exposure) — links to 001.
- c3: Specific "old friends" (H. pylori, helminths, Toxoplasma) are INVERSELY associated with MS.
- c4: The mechanism is immunoregulatory (reduced Treg-inducing exposures -> autoimmunity).

**View:** Structural (an environmental-etiology hypothesis) — a POPULATION-LEVEL, confounding-heavy claim.

**Evidence:**
- Meta-analyses: H. pylori INVERSELY correlated with MS [web:883]. Toxoplasma seropositivity protective
  (adjOR 0.56) [web:885]. Helminth infection protective in small studies [web:883][web:887].
- Late EBV/mono as a hygiene marker unifies with Case 001 [web:883].
- BUT: siblings/daycare/animal-exposure results CONFLICT; common childhood infections/vaccinations show
  NO effect [web:883].

**Tier assignment:** c1 **T2** (mixed). c2 **T2-T3** (coherent with EBV, 001). c3 **T2-T3** (H. pylori/
Toxoplasma associations replicated but observational, reverse-causation possible) [web:883][web:885].
c4 **T1-T2** (immunoregulatory mechanism plausible, human causal proof absent).

**Verdict:** **SUGGESTIVE, CONFOUNDING-HEAVY — the "old friends" inverse associations are the strongest
strand; the general hygiene claim is CONTESTED.**

**Contraction:** Hard core: the specific inverse associations (H. pylori, Toxoplasma) [web:883][web:885].
Discard the broad hygiene generalization. NOTE the TENSION with Case 001: EBV is a POSITIVE risk (a
pathogen that RAISES risk), while the hygiene frame says LOW pathogen exposure raises risk — reconciled
only by treating EBV-TIMING (late = hygiene marker) not EBV-presence as the hygiene variable. This is a
subtle mediator-vs-marker disambiguation.

**Xia hook:** Hygiene is a COLLINEAR-EXPOSURE bundle (like latitude, 026): SES, sanitation, family size,
and infection timing co-vary. Reverse causation (does subclinical MS alter infection susceptibility?)
plus the EBV-timing paradox make it a rich mediator/marker/confounder disambiguation for the sheaf DAG.

---

# CASE 043 — Impaired glymphatic/CSF clearance contributes to MS neurodegeneration

**Decomposed claim:**
- c1: Glymphatic/perivascular CSF clearance can be measured in MS (e.g., DTI-ALPS index) (descriptive).
- c2: Glymphatic function is IMPAIRED in MS vs controls.
- c3: Impaired clearance correlates with disability/atrophy (association).
- c4: Impaired clearance CAUSALLY contributes to neurodegeneration (accumulation of toxic solutes/iron).

**View:** Structural/Process (a clearance-failure mechanism) — an EMERGING, methodologically immature axis.

**Evidence (glymphatic-MS literature; adjacent to CP/CSF work):**
- DTI-ALPS and perivascular-space studies report reduced glymphatic indices in MS correlating with EDSS
  and atrophy; CP/CSF-trafficking work (041) is mechanistically adjacent [web:892][web:882].
- Evidence base is small, cross-sectional, and the DTI-ALPS proxy is contested as a true glymphatic measure.

**Tier assignment:** c1 **T2** (proxy measures, contested validity). c2 **T2** (reported, small studies).
c3 **T2** (associations). c4 **T1-T2** (causal role hypothetical; directionality unresolved — does
atrophy CAUSE enlarged perivascular spaces or vice versa?).

**Verdict:** **UNDERDETERMINED / EMERGING — plausible clearance-failure axis, but MEASUREMENT VALIDITY
is the rate-limiting problem.**

**Contraction:** Little hard core beyond c1 as a measurable proxy. The dominant issue is
MEASUREMENT-CONSTRUCT VALIDITY: DTI-ALPS may not measure glymphatic function at all. This is a
foundational (Family E) problem — you cannot score the mechanism until the metric's construct validity
is established (parallels EDSS invariance, 015, but at the EXPOSURE/mechanism-measure level).

**Xia hook:** Glymphatics is a case where the MEASURE precedes a validated CONSTRUCT — a pure MechViews
problem: define the equivalence/what-counts BEFORE scoring. A cautionary counterpart to the mature
substrates; belongs with 015/019 in the foundational layer as "metric-construct-invalid, defer scoring."

---

# CASE 044 — Fatigue and patient-reported outcomes (PROs) are valid MS disease measures

**Decomposed claim:**
- c1: Fatigue is the most prevalent, disabling MS symptom (descriptive).
- c2: Fatigue correlates with inflammatory burden (PRL, CP enlargement) (mechanism-link).
- c3: PRO fatigue scales validly measure a disease dimension distinct from EDSS.
- c4: Fatigue/PROs are legitimate PRIMARY outcomes for trials and mechanism studies.

**View:** Foundational/outcome-validity (Family E) — an OUTCOME-METRIC claim, sibling to EDSS (015).

**Evidence:**
- Chronic active lesions (PRL) + larger CP explain cognition AND fatigue in MS [web:893] — a mechanistic
  anchor linking fatigue to smoldering inflammation.
- Fatigue is multidimensional (primary vs secondary to depression/sleep/deconditioning), and PRO scales
  have known ceiling/floor and state-dependence issues.

**Tier assignment:** c1 **T3-T4** (universally observed). c2 **T2-T3** (PRL/CP correlation) [web:893].
c3 **T2** (construct validity partial — confounded by mood/sleep). c4 **T2** (PROs accepted as SECONDARY;
as primary they carry measurement non-invariance like EDSS).

**Verdict:** **SUPPORTED that fatigue is a real, mechanism-linked dimension; PARTIALLY SUPPORTED that
PRO scales validly and invariantly measure it.**

**Contraction:** Hard core c1,c2. c3,c4 flagged for measurement non-invariance and confounding by mood/
sleep/deconditioning — the SAME outcome-invariance problem as EDSS (015), now on the PRO axis. Fatigue
has a genuine mechanistic substrate (PRL/CP) but a noisy, multidimensional measure.

**Xia hook:** Fatigue extends the Prereq-2 outcome-invariance work to PROs: it has a VALIDATED
mechanistic anchor (PRL/CP, [web:893]) which can serve as an EXTERNAL criterion to re-metricize the
fatigue PRO — exactly the sNfL/atrophy anchoring strategy applied to a subjective outcome. A second
outcome axis (alongside EDSS) for the invariance layer.

---

## Cross-case map now spans 44 cases; family tallies

| Family | Cases | Count |
|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026,033,035,039,042 | 11 |
| B Progression substrate | 002,005,010,012,022,027,037,041 | 8 |
| C Treatment-mechanism | 003,011,023,025,028,029,030,040 | 8 |
| D Effect-modification | 006,011,018,020,030,031,032,033,034,040 | 10 |
| E Foundational / identity / outcome | 015,019,034,036,043,044 | 6 |
| (Mediation/convergence/bridge nodes) | 008,037,038,041 | cross-cutting |

## Structural findings after 44 cases

**Family B now has FIVE imaging substrates (002/027, 010, 012, 022, 041) — the P1 matroid-rank problem
grows.** Choroid plexus (041) is distinctive because it BRIDGES inflammation and degeneration, so it may
NOT be independent of the others — testing whether CP collapses into the existing rank or adds a new
dimension is now a concrete P1 sub-question. Predicted: CP loads on BOTH the inflammatory (PRL/cortical)
and degenerative (atrophy) factors, so it likely does NOT add an independent dimension but rather
INCREASES the correlation between the two substrate blocks — a "bridge" loading pattern.

**THREE candidate P2 gluing/bridge nodes now identified:** mitochondrial failure (037, degeneration
sink), SCFA (038, risk-side mediator), and choroid plexus (041, inflammation<->degeneration bridge). If
any of these REDUCES the P2 H^1 obstruction when added, that node is the mechanistic "seam" where the
two rival DAGs actually join — a specific, falsifiable structural prediction.

**Family E broadened from IDENTITY to OUTCOME-and-CONSTRUCT validity:** 015 (EDSS), 043 (glymphatic
measure), 044 (fatigue PRO) are all "metric-must-be-validated-before-scoring" cases. The foundational
layer now has TWO sublayers: (i) object identity (~): 019, 034, 036; (ii) metric/construct validity:
015, 043, 044. Both GATE the scorable families — this refines the Prerequisites Spec into two distinct
gating checks.

**The hygiene<->EBV paradox (042 vs 001)** is a clean worked example of mediator-vs-marker: EBV presence
raises risk while EBV timing (late=hygiene) is the actual environmental variable — the same exposure
enters two different causal roles depending on how it is coded. A sharp motivating case for careful
exposure-definition in MechViews before any MR/DAG scoring.


---

# CASE 045 — Meningeal B-cell follicle-like aggregates drive subpial cortical pathology and progression

**Decomposed claim:**
- c1: Ectopic B-cell follicle-like structures exist in the meninges of a subset of SPMS cases (pathology).
- c2: Their presence correlates with increased subpial cortical demyelination + cortical atrophy (association).
- c3: F(+) cases have an EXACERBATED clinical course (younger onset, faster progression, earlier death).
- c4: Cytotoxic factors diffusing from the meningeal compartment CAUSALLY drive the cortical gradient (mechanism).

**View:** Structural (a compartmentalized-inflammation mechanism) with a striking WITHIN-DISEASE natural
experiment (F+ vs F- SPMS).

**Evidence:**
- Follicle-like structures in 40-54% of SPMS; located in deep sulci (temporal/cingulate/insula/frontal)
  [web:897][web:901].
- F(+) cases: increased subpial demyelination, cortical atrophy, and a GRADIENT of neuronal loss (highest
  at pial surface) absent in F(-) cases -> supports a diffusible cytotoxic factor from meninges [web:901].
- F(+) vs F(-): significantly younger onset, faster progression, earlier wheelchair/death [web:897].
- Meningeal B-cell inflammation also correlates with SPINAL CORD pathology [web:908], and meningeal/
  parenchymal B-cell clones are RELATED [web:906].

**Tier assignment:** c1 **T3-T4** (large autopsy series). c2 **T3** (quantitative correlation) [web:901].
c3 **T3** (clinical-course difference across F+/F-) [web:897]. c4 **T3** — the pial-to-deep neuronal-loss
GRADIENT is strong indirect evidence for a diffusible-factor mechanism [web:901].

**Verdict:** **SUPPORTED — one of the strongest compartmentalized-inflammation mechanisms; the F+/F-
contrast is a near-ideal within-disease natural experiment.**

**Contraction:** Hard core c1,c2,c3. c4 held strongly on the gradient evidence. This is the PATHOLOGICAL
SUBSTRATE of "smoldering"/PIRA (036) and mechanistically UPSTREAM of cortical lesions (012) and CP
enlargement (041) — meningeal inflammation may be the SOURCE feeding both. Autopsy-only (survivorship/
end-stage bias) is the main caveat; in-vivo detection is hard (links to CP 041 as a proxy).

**Xia hook:** The F+/F- gradient is a spatial DOSE-RESPONSE (cytotoxicity decreasing with distance from
meninges) — a rare mechanistic natural experiment. And meningeal inflammation is a candidate ROOT node
UPSTREAM of the Family B substrates (012 cortical, 041 CP), reorganizing part of the P2 DAG: it may be a
SOURCE that, if added, changes the gluing structure among the cortical substrates.

---

# CASE 046 — Cortical tissue-sodium accumulation (23Na-MRI) is a marker of neuroaxonal metabolic failure and progression

**Decomposed claim:**
- c1: 23Na-MRI quantifies total tissue sodium concentration (TSC) in vivo (method).
- c2: Sodium accumulates in MS tissue, including normal-appearing tissue (descriptive).
- c3: Cortical GM sodium accumulation associates with disability and SECONDARY-PROGRESSIVE course.
- c4: Sodium accumulation reflects a CAUSAL neuroaxonal metabolic/energy-failure mechanism (links to 037).

**View:** Subspace/substrate (imaging progression marker) + Structural (metabolic-failure readout) — a
SIXTH imaging substrate for Family B, and the in-vivo readout of the mito energy-failure axis (037).

**Evidence:**
- 23Na-MRI measures TSC (weighted intra/extracellular sodium) [web:898].
- Sodium accumulation associates with disability AND progressive course [web:898][web:907].
- Cortical GM sodium accumulation specifically associated with disability + SPMS in relapse-onset MS
  [web:902]; intralesional sodium heterogeneity resolvable at high resolution [web:905].

**Tier assignment:** c1 **T3** (established but technically demanding). c2 **T3** (replicated). c3 **T3**
(cortical-sodium/SPMS association) [web:902]. c4 **T2-T3** — sodium rise is MECHANISTICALLY tied to
Na/K-ATPase failure = energy failure (037), so this is arguably the IN-VIVO readout of Case 037.

**Verdict:** **SUPPORTED as a progression-associated metabolic marker; the causal energy-failure
interpretation SUPPORTED-by-convergence with mito pathology (037).**

**Contraction:** Hard core c1,c2,c3. c4 held via convergence with 037. Family B substrate #6 -> inherits
bracket-norm confound HARD: 23Na-MRI is EXTREMELY acquisition-sensitive (3T vs 7T, voxel size, coil, TSC
calibration phantoms) [web:905][web:907] — possibly the MOST acquisition-dependent metric in the catalog.

**Xia hook:** 23Na-TSC is the IN-VIVO bridge between the mechanism (mito energy failure, 037) and an
imaging substrate — a rare case where a Family-B metric has a DIRECT mechanistic interpretation (Na/K-
ATPase failure). But it is the extreme case for P1's confound audit (maximal acquisition sensitivity):
the ideal stress-test metric for whether the bracket-norm correction actually works. It ALSO closes a
loop with the salt case (033): dietary sodium (exposure) vs tissue sodium (substrate) are DIFFERENT
constructs sharing a name — a MechViews disambiguation.

---

# CASE 047 — MS is more severe in Hispanic and Black Americans (a transportability / disparity claim)

**Decomposed claim:**
- c1: Hispanic and Black Americans with MS have higher disability severity scores than White Americans (descriptive).
- c2: The difference persists after adjusting for insurance/access (partial confound control).
- c3: The disparity reflects BIOLOGICAL/ancestry differences in disease course.
- c4: MS mechanism findings from White-majority cohorts TRANSPORT to other ancestries.

**View:** Transportability (T_stratum across ancestry/population) + effect-modification — the sharpest
EXTERNAL-VALIDITY case in the catalog.

**Evidence:**
- Hispanic (P-MSSS 3.9) and Black (4.5) Americans had significantly higher severity than White (3.4),
  age/sex-adjusted; adjusting for insurance did NOT change results [web:900].
- MS symptom severity varies by race/ethnicity across domains [web:903].
- MS research has historically focused on White patients -> unknown external validity [web:899].

**Tier assignment:** c1 **T3** (replicated clinic cohorts) [web:900]. c2 **T2-T3** (insurance-adjusted,
but residual SES/access/environmental confounding LIVE) [web:900]. c3 **T1-T2** (ancestry-vs-social
determinants NOT disentangled — the core confound). c4 **T1-T2, LIKELY NON-TRANSPORT** — most mechanism
evidence is White-majority [web:899].

**Verdict:** **SUPPORTED that severity differs by group; the CAUSE (biology vs structural/social
determinants) is UNDERDETERMINED; mechanism transportability is UNVALIDATED and likely INCOMPLETE.**

**Contraction:** Hard core c1. c2 partial. Discard strong c3 (ancestry-as-biology) — social determinants
of health are a massive unmeasured confounder. c4 is a DIRECT transportability warning: the entire
catalog is built largely on White-majority evidence, so EVERY mechanism's H^1 across ancestry is
formally UNTESTED. This is the catalog's honesty flag.

**Xia hook:** This is the T_stratum transport problem at its most consequential: does the WHOLE catalog
transport across ancestry? It is BOTH a scientific (effect-modification) and an equity issue, and it
reframes P3 -- ancestry should be a PRIMARY stratifying modifier, not an afterthought. Also a
confounding-vs-cause disambiguation (social determinants vs biology) at the population scale.

---

# CASE 048 — Meningeal inflammation is the ROOT driver of the entire gray-matter/progression axis (a strong-form unifying claim)

**Decomposed claim (deliberately OVERREACHING to test the ceiling):**
- c1: Meningeal inflammation (045) is present and upstream of cortical pathology (established, 045).
- c2: Meningeal inflammation is the COMMON SOURCE feeding cortical lesions (012), CP enlargement (041),
  AND subpial neuronal loss (a unification claim).
- c3: Meningeal inflammation is the PRIMARY driver of ALL gray-matter progression (strong-form).
- c4: Therefore targeting meningeal B cells would halt progression (therapeutic corollary).

**View:** Structural strong-form UNIFICATION — deliberately tests how far one mechanism can be pushed.

**Evidence:**
- Meningeal B-cell inflammation correlates with cortical (045), spinal-cord [web:908], and submeningeal
  pathology [web:909]; meningeal/parenchymal B-cell clones related [web:906].
- BUT: energy failure (037), iron (027), and axonal biophysics are ALSO progression drivers not obviously
  downstream of meninges; anti-CD20 (which depletes B cells) does NOT fully halt progression (011).

**Tier assignment:** c1 **T3** (from 045). c2 **T2-T3** (correlational unification, plausible). c3 **T2,
OVERREACH** — competing drivers (037,027) are not clearly downstream. c4 **T1-T2** — anti-CD20's
INCOMPLETE progression effect (011) is evidence AGAINST a pure-meningeal-B-cell model, since CNS-
compartmentalized B cells may be poorly reached by peripheral depletion.

**Verdict:** **PARTIAL — meningeal inflammation is A major upstream driver (strong for c1,c2); the
strong-form "THE primary/sole driver" (c3,c4) OVERREACHES.**

**Contraction:** Preserve c1,c2 (meningeal inflammation as A root node). Reject strong c3,c4. This case
exists to mark the CEILING: even the best compartmentalized-inflammation mechanism cannot absorb the
energy-failure (037) and iron (027) axes, which is exactly why P2 predicts H^1 != 0 (multiple partly-
independent progression routes). The failure of this unification IS the argument for a multi-node DAG.

**Xia hook:** Case 048 is the deliberate STRESS-TEST of single-mechanism unification — its PARTIAL
failure is the strongest intuitive argument for P2's multi-process conclusion. If ONE mechanism could
absorb all of progression, H^1 would be 0; the fact that meningeal inflammation (the best candidate)
cannot is the qualitative face of the quantitative obstruction.

---

## Cross-case map now spans 48 cases; family tallies

| Family | Cases | Count |
|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026,033,035,039,042 | 11 |
| B Progression substrate | 002,005,010,012,022,027,037,041,045,046 | 10 |
| C Treatment-mechanism | 003,011,023,025,028,029,030,040 | 8 |
| D Effect-modification / transport | 006,011,018,020,030,031,032,033,034,040,047 | 11 |
| E Foundational / identity / outcome | 015,019,034,036,043,044 | 6 |
| (Unification / bridge / root nodes) | 008,037,038,041,045,048 | cross-cutting |

## Structural findings after 48 cases

**Family B is now SIX imaging substrates + a hierarchy.** They are no longer a flat list — 045 (meningeal
inflammation) is emerging as a ROOT/SOURCE node upstream of cortical (012), CP (041), and subpial loss,
while 046 (sodium) is the IN-VIVO readout of the mito sink (037). So the substrates have a rough
UPSTREAM->DOWNSTREAM ordering: meninges -> cortical/CP -> energy-failure/sodium -> atrophy -> disability.
This turns the P1 matroid-rank question into a partial-ORDER (DAG) question, not just a dimension count.

**Case 048 is the catalog's designed CEILING test.** Its partial failure — no single mechanism (not even
the best, meningeal inflammation) absorbs energy-failure (037) and iron (027) — is the qualitative twin
of P2's predicted H^1 != 0. Pairing 048 (unification fails) with 037/027 (independent sinks) gives Xia
the intuition BEHIND the cohomological result.

**Transportability (047) is now flagged as a catalog-wide caveat.** Because the evidence base is White-
majority [web:899], every mechanism's ancestry-transport (T_stratum) is UNTESTED. This should make
ancestry a PRIMARY axis in P3, and it is the catalog's key honesty/limitation statement for the Xia brief.

**The salt loop is closed:** dietary sodium (exposure, 033) vs tissue sodium (substrate, 046) share a
name but are DIFFERENT constructs on different DAG positions — a clean MechViews disambiguation example
(same token, two nodes).


---

# CASE 049 — EBNA1<->GlialCAM molecular mimicry is the mechanistic bridge from EBV to MS autoimmunity

**Decomposed claim (the MECHANISM deferred from Case 001):**
- c1: MS patients have clonally-expanded CSF B cells / plasmablasts making anti-EBNA1 antibodies (descriptive).
- c2: A subset of anti-EBNA1 antibodies CROSS-REACT with CNS GlialCAM (molecular mimicry) (mechanism).
- c3: Anti-GlialCAM reactivity is enriched in MS vs controls and differentiates patients (association).
- c4: These cross-reactive antibodies CAUSALLY contribute to CNS immunopathology (causal mechanism).

**View:** Structural (the molecular mechanism connecting the Tier-3 etiology, Case 001, to autoimmunity)
— the mechanistic "how" under EBV necessity.

**Evidence:**
- Lanz et al. (Nature 2022): EBNA1-derived antibody binds a GlialCAM motif; recognition INCREASED by
  somatic hypermutation in CNS and by GlialCAM serine phosphorylation; other MS cohorts confirm anti-
  GlialCAM; MOUSE models support a contribution to CNS immunopathology [web:731][web:919].
- Clonally expanded MS B cells bind EBNA1 [web:912]; anti-EBNA1/GlialCAM differentiates MS from controls
  (PNAS 2025) [web:914]; additional mimicry targets (CRYAB, ANO2) reported [web:921].

**Tier assignment:** c1 **T3-T4** (BCR sequencing + plasmablast data). c2 **T3** (structural mimicry
mapped) [web:731]. c3 **T3** (multi-cohort replication) [web:914]. c4 **T2-T3** — mouse-model support is
real but human causal proof (and what FRACTION of MS is mimicry-driven) remains partial [web:731].

**Verdict:** **SUPPORTED as A mechanistic bridge from EBV to MS autoimmunity; the FRACTION of disease it
explains is UNDERDETERMINED (mimicry is one of several EBV->MS routes).**

**Contraction:** Hard core c1,c2,c3. c4 held as suggestive-to-supported (mouse models). This SUPPLIES
the mechanism that Case 001 (EBV necessity) lacked — but note EBV->MS may ALSO act via B-cell
transformation/latency, bystander activation, etc., so mimicry is a MEDIATION-FRACTION problem (how much
of EBV's necessary-cause effect runs through GlialCAM mimicry vs parallel routes).

**Xia hook:** 049 completes the EBV chain: 001 (necessity, epidemiology) -> 049 (mimicry mechanism) ->
035 (therapy, unproven). This is a full CAUSAL LADDER across evidence tiers (T_tier): a single etiology
scored at THREE tiers with DIFFERENT verdicts (T3 necessity, T3 mechanism, T1 therapy) — the clearest
demonstration that tier-transport is non-trivial. Mediation-fraction of mimicry vs other EBV routes is a
front-door decomposition for P2.

---

# CASE 050 — Serum GFAP is an astrocytic biomarker specifically of PROGRESSION (dissociable from NfL)

**Decomposed claim:**
- c1: Serum GFAP (sGFAP) reflects astrocytic damage/reactive astrogliosis (mechanism-link).
- c2: sGFAP correlates with MS disease severity/disability (association).
- c3: sGFAP predicts PROGRESSION specifically, MORE than NfL does (differential prognostic).
- c4: sGFAP and sNfL index DIFFERENT processes (astrogliosis/progression vs acute neuroaxonal/relapse).

**View:** Subspace/biomarker — a SECOND fluid biomarker that, crucially, DISSOCIATES from NfL (005)
along the relapse/progression axes.

**Evidence:**
- sGFAP = astrocytic marker; correlates with severity [web:910].
- sGFAP MORE strongly associated with PROGRESSION than sNfL (JAMA Neurol 2023) [web:915]; predicts
  progression in large cohorts, esp. non-active/progressive MS [web:918].
- sGFAP + sNfL DIFFERENTIATE subsequent progression, indexing distinct processes [web:913].

**Tier assignment:** c1 **T3** (astrocytic biology). c2 **T3** (replicated) [web:910]. c3 **T3** (GFAP >
NfL for progression) [web:915][web:918]. c4 **T3** — the GFAP/NfL dissociation is replicated and
mechanistically coherent [web:913].

**Verdict:** **SUPPORTED — sGFAP is a progression-weighted astrocytic biomarker, DISSOCIABLE from the
relapse-weighted NfL.**

**Contraction:** Hard core all four. This is a FLUID-BIOMARKER instance of the relapse!=progression
dissociation: NfL (005) tracks acute neuroaxonal injury (relapse-weighted), GFAP tracks astrogliosis
(progression-weighted). Two blood markers now SEPARATE the two axes — a confound-INDEPENDENT (no imaging
acquisition bias) validation of the two-axis structure. GFAP has its OWN assay/BMI/age confounds, but
NOT the scanner-acquisition confound of Family B.

**Xia hook:** GFAP (progression) vs NfL (relapse) is the two-axis dissociation at the BLOOD level — the
FIFTH level after pharmacological, developmental, genetic, and mechanistic (from Case 040 batch). Two
orthogonal fluid markers give P3 a clean, acquisition-confound-FREE substrate pair to test whether the
relapse and progression axes are truly separable dimensions (principal-angle ~ 90 deg?).

---

# CASE 051 — Childhood/adolescent obesity and low vitamin D INTERACT to raise MS risk (a gene/environment-style interaction on the risk axis)

**Decomposed claim:**
- c1: Adolescent obesity raises MS risk (epidemiology; links to MR Case 013).
- c2: Childhood BMI is causally associated with MS (MR).
- c3: Obesity and low vitamin D INTERACT (obesity lowers bioavailable vitamin D; combined effect > additive).
- c4: The interaction is mechanistic (adipose inflammation + vitamin-D-deficiency synergy).

**View:** Effect-modification on the RISK axis (Family D) — two causal exposures (013 BMI, 007 vitamin D)
that INTERACT, the risk-axis analogue of the HLAxEBV interaction (018).

**Evidence:**
- MR: adult AND childhood BMI causal for MS; low vitamin D causal [web:718][web:916].
- Obesity reduces bioavailable 25(OH)D (sequestration in adipose) -> mechanistic coupling of the two
  MR-causal exposures; adolescent-obesity risk partly mediated via vitamin D [web:916].

**Tier assignment:** c1 **T3** (adolescent obesity). c2 **T3** (MR, from 013) [web:718]. c3 **T2-T3**
(interaction/mediation plausible and partly evidenced; formal interaction MR less established). c4 **T2-T3**.

**Verdict:** **SUPPORTED that both are causal; the INTERACTION/mediation (obesity acting partly THROUGH
vitamin D) is SUGGESTIVE-to-SUPPORTED but not a clean MR interaction estimate.**

**Contraction:** Hard core c1,c2. c3 held as mediation/interaction — this is a RISK-AXIS interaction
(cf. HLAxEBV, 018, which was on the exposure->mechanism edge): two MR-causal factors (007,013) that are
NOT independent (obesity depresses vitamin D), so their MR estimates are ENTANGLED. Naive separate MRs
double-count shared variance.

**Xia hook:** 051 is the RISK-AXIS interaction case for the MR module: BMI (013) and vitamin D (007) are
MR-causal but CORRELATED exposures (obesity->low vitamin D), so a MULTIVARIABLE / mediation MR is needed
to partition their effects — the risk-side analogue of the scale-invariance interaction test (HLAxEBV,
018) that validates P3. Adds a fourth positive to the MR panel with a twist (mediation between two positives).

---

# CASE 052 — MS is one disease with a continuous severity spectrum (vs distinct biological subtypes) — the lumping-vs-splitting identity claim

**Decomposed claim (a foundational identity/taxonomy claim, deliberately two-sided):**
- c1: RRMS/SPMS/PPMS are clinical descriptors, not proven distinct biological entities (descriptive).
- c2: The RRMS->SPMS transition is gradual/arbitrary, not a discrete switch (continuum evidence).
- c3: MS is fundamentally ONE disease with continuous variation in relapse/progression balance (lumping).
- c4: OR: distinct molecular subtypes (e.g., pathology patterns I-IV) justify SPLITTING into entities.

**View:** MechViews object-identity (~) at the WITHIN-MS level — how coarse/fine should the equivalence
relation over MS patients be? (sibling to NMOSD-split 019, but INTERNAL to MS).

**Evidence:**
- PIRA/smoldering evidence (036) shows progression occurs THROUGHOUT, blurring RRMS/SPMS [web:838].
- The two-axis view (relapse vs progression, present at 5 levels) suggests a CONTINUOUS 2D space, not
  discrete classes.
- BUT historical Lucchinetti pathology patterns (I-IV) and heterogeneous treatment response argue some
  real biological substructure.

**Tier assignment:** c1 **T3** (clinical descriptors acknowledged). c2 **T3** (continuum from PIRA data)
[web:838]. c3 **T2-T3** (parsimonious 2-axis continuum well-supported). c4 **T2** (pattern stability
contested; single patient may not have one fixed pattern).

**Verdict:** **A DEFINITIONAL (MechViews) question, not a MechVal score: current evidence favors a
CONTINUOUS 2-axis (relapse x progression) model over discrete subtypes, but a mild-substructure view is
defensible.**

**Contraction:** No hard empirical core to preserve/discard — this is a choice of ~ (how to partition
patients). The catalog's own recurring 2-axis finding ARGUES for lumping into a continuous
(relapse,progression) plane; splitting requires demonstrating STABLE, non-overlapping molecular clusters.

**Xia hook:** 052 is the master IDENTITY decision that FRAMES the whole catalog: if MS is a continuous
2-axis space (as the 5-level dissociation suggests), then the right MechRef object is a MANIFOLD of
patients coordinatized by (relapse-activity, progression-rate), and mechanisms are VECTOR FIELDS on it —
turning "which mechanism where" into a geometry problem. This is the most abstract, highest-leverage
MechViews framing and a natural closing frame for the Xia brief.

---

## Cross-case map now spans 52 cases; family tallies

| Family | Cases | Count |
|---|---|---|
| A Etiology / causal-risk | 001,007,013,017,021,024,026,033,035,039,042,051 | 12 |
| B Progression substrate / biomarker | 002,005,010,012,022,027,037,041,045,046,050 | 11 |
| C Treatment-mechanism | 003,011,023,025,028,029,030,040 | 8 |
| D Effect-modification / transport | 006,011,018,020,030,031,032,033,034,040,047,051 | 12 |
| E Foundational / identity / outcome | 015,019,034,036,043,044,052 | 7 |
| (Mechanism-bridge / mediation / root) | 008,037,038,041,045,048,049 | cross-cutting |

## Structural findings after 52 cases

**The relapse!=progression dissociation now appears at FIVE+ levels — add the BLOOD level (050).**
1. Pharmacological (003,025,016). 2. Developmental (034). 3. Genetic (039). 4. Mechanistic-convergence
(037). 5. FLUID-BIOMARKER: NfL=relapse-weighted (005) vs GFAP=progression-weighted (050) [web:915].
The two-axis structure is now supported by evidence at every level of analysis AND by two orthogonal,
acquisition-confound-FREE blood markers — this is the catalog's single most robust and most
Xia-relevant empirical claim.

**The full EBV causal ladder (001->049->035) is a complete T_tier demonstration.** One etiology, scored
at three tiers: necessity T3 (001), mimicry mechanism T3 (049), therapy T1 (035). Same cause, three
verdicts — proving tier-transport must be modeled explicitly, exactly the T_tier operator from the salt
case (033).

**Case 052 reframes the entire catalog geometrically.** If MS is a continuous 2-axis (relapse x
progression) manifold rather than discrete subtypes, mechanisms become VECTOR FIELDS on that manifold,
and the whole MechVal program becomes: locate each scored mechanism's action on the (relapse,progression)
plane, and ask where the field is smooth (transport, H^1=0) vs obstructed (H^1!=0). This is the natural
unifying geometry for the Xia brief — the 52 cases are samples of a mechanism vector field over a 2D
patient manifold.
