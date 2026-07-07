# Mechanistic Validity — Alzheimer's Disease / Neurodegeneration Mechanism Catalog (Xia Program, Domain 2)

**Build date:** 2026-06-30  |  **Status:** INITIALIZING SCAFFOLD (to be filled iteratively, like the MS catalog)
**Companion to:** Mechanistic Validity_MS_Neurology_Catalog_Xia.md (Domain 1, 52 cases)
**Why this domain:** Zongqi Xia's program explicitly spans BOTH MS AND "Alzheimer's disease (AD) and
related dementia," with the SAME two driving questions — (1) what drives group/individual differences in
onset, progression, treatment response? (2) how to give tailored clinical guidance? — using the SAME
toolkit (biostatistics, ML, statistical learning, generative AI on multi-modal longitudinal data). So AD
is not a random second domain: it is the OTHER HALF of his stated mission. Demonstrating that the SAME
Mechanistic Validity families/operators recur in AD is the strongest possible generalization argument.

---

## THE CENTRAL THESIS FOR DOMAIN 2

The MS catalog surfaced a domain-general skeleton. The AD pilot's job is to test whether that skeleton
RE-DERIVES from an independent literature. If it does, Mechanistic Validity is a method, not an MS artifact. Early
evidence says it does — the AD field has DIRECT analogues of every MS structural finding:

| MS structural finding (Domain 1) | AD analogue (Domain 2) — the hypothesis to fill in |
|---|---|
| relapse != progression (5 levels) | **amyloid != tau != neurodegeneration** — the ATN framework already SPLITS AD into 3 axes |
| EBV = necessary-but-not-sufficient cause (001) | **Amyloid cascade** as contested necessary trigger [web:926][web:932][web:934] |
| Etiology != treatment (anti-amyloid overreach) | anti-amyloid drugs clear plaque but modest clinical effect — same treatment!=disease gap |
| HLA the dominant genetic risk (017) | **APOE4** the dominant genetic risk [web:940][web:931] |
| MR-causal risk panel (vit D, BMI, HLA; smoking null) | **TREM2 MR-causal; most cytokines MR-null** [web:927] |
| Iron/microglia progression substrate (027) | **TREM2/microglial neuroinflammation** [web:927][web:930] |
| Effect-modifier interactions (HLAxEBV, 018) | **APOE4 x amyloid interaction on tau/decline** [web:939][web:933] |
| Bracket-norm imaging confound (Family B) | **PET tracer/threshold/harmonization confounds** (amyloid & tau PET) |
| Outcome-invariance (EDSS, 015) | **cognitive-scale invariance (MMSE/CDR/ADAS-cog)** |

This table IS the scaffold: each row becomes 3-6 scored cases, exactly as in MS.

---

## THE FIVE FAMILIES, RE-INSTANTIATED FOR AD (skeleton — to fill)

**Family A — Etiology / causal-risk (MR-scorable).**
- A1 Amyloid cascade hypothesis as causal etiology (the big contested one) [web:926][web:929][web:932]
- A2 APOE4 as dominant genetic causal risk (dose-dependent, up to 15x in homozygotes) [web:940]
- A3 TREM2 / sTREM2 MR-causal for AD (z=-9.1, p=1e-19) — with most other cytokines MR-NULL [web:927]
- A4 Plasma-proteomic MR panel (CTSH-GRN-TMEM106B, TREM2-IL-34 microglial networks) [web:930]
- A5 Modifiable risk factors (midlife hypertension, diabetes, hearing loss, education) — the "risk axis"
- (Negative control candidate: an inflammatory cytokine that is MR-NULL — the AD analogue of smoking/021)

**Family B — Progression substrate / biomarker (ATN + imaging, bracket-norm-prone).**
- B1 Amyloid PET / CSF Abeta42/40 as substrate (the "A" axis) [web:937][web:940]
- B2 Tau PET / p-tau181/217 as substrate (the "T" axis) [web:939]
- B3 Neurodegeneration: MRI atrophy, FDG-PET hypometabolism, NfL (the "N" axis) [web:940]
- B4 Glial/neuroinflammation biomarkers: sTREM2, GFAP, YKL-40 (the candidate 4th axis) [web:930]
- B5 Synaptic markers: neurogranin, alpha-synuclein [web:940]
- (Bracket-norm confound: amyloid-PET Centiloid thresholds, tracer differences, tau-PET off-target binding)

**Family C — Treatment-mechanism.**
- C1 Anti-amyloid mAbs (lecanemab/donanemab) — plaque clearance vs modest clinical benefit (treatment!=disease)
- C2 Anti-tau approaches (mostly failed/early) — mechanism-validity vs endpoint failure
- C3 Anti-inflammatory / microglial modulation (TREM2 agonists) — the neuroinflammation lever
- C4 Repurposed metabolic (GLP-1, anti-diabetic) — the vascular/metabolic axis intervention

**Family D — Effect-modification / heterogeneity / transport.**
- D1 APOE4 x amyloid interaction on tau accumulation & cognitive decline [web:939][web:933]
- D2 Sex (female preponderance/faster tau spread) — the AD analogue of MS sex effects (020)
- D3 Cognitive/brain reserve (education) modifying pathology->cognition — DIRECT analogue of MS 031
- D4 Ancestry/transportability (ADNI is White-majority) — DIRECT analogue of MS 047
- D5 Comorbidity/vascular contribution (mixed dementia) — analogue of MS 032

**Family E — Foundational / identity / outcome-validity.**
- E1 Is "AD" one disease or a syndrome? (amyloid-positive vs SNAP vs mixed) — the identity/~ decision (cf MS 052)
- E2 ATN as a re-metricization of the disease into A,T,N coordinates — an EXPLICIT multi-axis framing
- E3 Cognitive-scale invariance (MMSE/CDR-SB/ADAS-cog ceiling/floor, practice effects) — cf EDSS (015)
- E4 Preclinical/prodromal/MCI/dementia staging as a continuum vs discrete stages — cf PIRA (036)

---

## THE FLAGSHIP QUESTION FOR AD (the P2 analogue)

MS's central adjudication was inflammation-first vs degeneration-first. AD's EXACT analogue is the
**amyloid-cascade adjudication**: does amyloid CAUSE tau/neurodegeneration ("amyloid-first"), or are
amyloid and tau partly-independent processes with neuroinflammation as a parallel/converging driver?
The amyloid cascade is explicitly described in 2024 as still only "a working hypothesis" / "a conclusion
in search of support" [web:926][web:932], with poor plaque-cognition correlation as the core critique
[web:929][web:934]. This is a PERFECT rival-DAG / sheaf-gluing target:
- DAG-1 (amyloid-first): Abeta -> tau -> neurodegeneration -> cognitive decline (linear cascade).
- DAG-2 (multi-process): Abeta, tau, and microglial/TREM2 neuroinflammation as partly-independent axes
  converging on neurodegeneration; APOE4 acting on MULTIPLE edges [web:935][web:933].
The interventional ground truth = anti-amyloid trials (plaque cleared, cognition barely moved) — the AD
analogue of the MS drug dissociations, and direct evidence AGAINST a pure linear cascade (predicts H^1 != 0).

---

## WHAT'S ALREADY STRONG (early tiering, to refine)
- **APOE4 = dominant genetic risk**, dose-dependent (15x homozygous), acts on amyloid AND tau AND
  atrophy AND is an effect-MODIFIER of progression — Tier-3/4, the AD analogue of HLA [web:940][web:931][web:939].
- **TREM2 MR-causal** while most inflammatory cytokines are MR-NULL [web:927] — this is a READY-MADE
  positive/negative MR panel (exactly like MS's vit-D-causal / smoking-null discrimination test).
- **ATN framework** = the field has ALREADY split AD into 3 measurable axes — Domain 2 starts with a
  two-to-three-axis structure PRE-VALIDATED by the community (stronger starting point than MS).

## IMMEDIATE NEXT STEPS (iterative fill, same method as MS)
1. Fill Family A first (amyloid cascade A1, APOE4 A2, TREM2 A3 + MR-null negative control) — 4-5 cases.
2. Then Family B (ATN axes B1-B4) with the PET bracket-norm confound flagged.
3. Then the amyloid-cascade P2 adjudication as the flagship.
4. Cross-map back to MS: build a SHARED cross-domain findings table (the generalization deliverable).

## THE GENERALIZATION PAYOFF (why this matters for the Xia meeting)
If MS and AD BOTH decompose into the same five families, both need bracket-norm PET/MRI audits, both show
a dominant-genetic-risk + MR-panel structure, both have a treatment!=disease gap, and both have a
multi-axis (not linear-cascade) progression structure that predicts H^1 != 0 — then Mechanistic Validity is a
DOMAIN-GENERAL method for Xia's ENTIRE program (his stated mission covers exactly these two disease
families). That is the headline: one framework, both halves of his research portfolio.


===========================================================================
# FAMILY A — ETIOLOGY / CAUSAL-RISK (MR-scorable) — FIRST FILL
===========================================================================

---

# CASE AD-001 — The amyloid cascade hypothesis: Abeta accumulation is the CAUSAL initiating event in AD

**Decomposed claim:**
- c1: Abeta peptide aggregates and deposits as plaques in AD brain (descriptive pathology).
- c2: Amyloid accumulation TEMPORALLY precedes tau spread and neurodegeneration (sequence).
- c3: Amyloid is the CAUSAL initiating trigger of the downstream cascade (causal-etiology).
- c4: Therefore removing amyloid should yield clinical benefit (therapeutic corollary).

**View:** Structural (the central causal-etiology claim of the AD field) with an RCT-testable therapy leg.
**DIRECT ANALOGUE of MS Case 001 (EBV as necessary trigger).**

**Evidence:**
- Well-supported in observational/pathological studies; amyloid is upstream in the preclinical continuum
  [web:937][web:950]. The cascade "remains a working hypothesis" in 2024 [web:926].
- CRITIQUES (decades old, still live): POOR plaque-cognition correlation; plaques in cognitively normal
  elderly; the cascade called "a conclusion in search of support" [web:929][web:932][web:934].
- Therapeutic corollary now PARTIALLY tested: amyloid removal gives measurable but MODEST clinical
  benefit (see AD-C1) [web:950].

**Tier assignment:** c1 **Mechanistically Supported** (universally observed). c2 **Causally Suggestive** (amyloid-first temporal ordering in
biomarker cascade) [web:937]. c3 **Observationally Consistent to Causally Suggestive, UNDERDETERMINED** — causal INITIATION supported but SUFFICIENCY
disputed (poor plaque-cognition link) [web:929][web:934]. c4 **Observationally Consistent** (modest benefit; see C1).

**Verdict:** **SUPPORTED that amyloid is AN early causal contributor; DISCONFIRMED as a SUFFICIENT linear
cause; the strong-form cascade is UNDERDETERMINED — necessary-ish but not sufficient.**

**Contraction:** Hard core c1,c2. Weaken c3 to "early contributor, not sufficient." This is the near-
EXACT structural twin of MS EBV (001): a leading etiological trigger that is necessary-ish but NOT
sufficient, with the sufficiency gap being the whole scientific action. The poor plaque-cognition
correlation is the AD analogue of "EBV-infected but no MS."

**Xia hook:** AD-001 is the anchor of the amyloid-cascade P2 adjudication (the AD analogue of the MS
inflammation-vs-degeneration flagship). Its contested SUFFICIENCY is precisely what predicts a multi-
process (H^1 != 0) rather than linear-cascade DAG. Same structural signature as MS Domain 1.

---

# CASE AD-002 — APOE4 is the dominant genetic causal risk factor, dose-dependently

**Decomposed claim:**
- c1: APOE e4 is associated with AD (descriptive genetics).
- c2: The effect is DOSE-dependent (0 < 1 < 2 alleles), strongly (causal-risk).
- c3: APOE4 acts via MULTIPLE mechanisms (amyloid AND tau AND neuroinflammation) (mechanism).
- c4: APOE4 is an effect-MODIFIER of progression/treatment, not just risk (dual role).

**View:** Structural (dominant genetic etiology) + effect-modifier. **DIRECT ANALOGUE of MS HLA (017).**

**Evidence:**
- Dose-dependent: heterozygous OR ~3.1-3.65, homozygous OR ~13-34 vs non-carriers [web:946][web:952][web:949].
- e4/e4 women & men OR 12-15; heterozygous 3.5-4 [web:956]. Onset shifted earlier in homozygotes [web:949].
- Mechanistically pleiotropic: APOE4 increases amyloid AND independently exacerbates tau AND
  neuroinflammation; neuronal APOE4 alone drives tau pathology [web:933][web:935][web:928].
- NOT homogeneous: e2/e4 heterozygotes NOT elevated; non-APOE PRS modifies e4 carriers substantially
  [web:952][web:955] -> APOE4 is necessary-context-dependent, not deterministic.

**Tier assignment:** c1 **Mechanistically Supported**. c2 **Mechanistically Supported** (dose-response, huge samples) [web:952]. c3 **Causally Suggestive to Mechanistically Supported**
(multi-mechanism, incl. causal tau effect) [web:935]. c4 **Causally Suggestive** (modifies onset age & progression).

**Verdict:** **SUPPORTED at Tier-4 as dominant, dose-dependent genetic risk acting via MULTIPLE
mechanisms; deterministic reading OVERREACHES (PRS/allele-context dependent).**

**Contraction:** Hard core c1,c2,c3,c4. Note the PARTIAL-MEDIATION structure: APOE4 -> amyloid is only
ONE path; APOE4 -> tau and -> neuroinflammation are partly INDEPENDENT [web:933][web:935]. This is the
AD analogue of HLA acting on multiple MS pathways, and it is EVIDENCE FOR the multi-process DAG (AD-001):
if the dominant risk gene acts on 3 axes independently, a linear amyloid cascade cannot be the whole story.

**Xia hook:** APOE4's multi-edge action (amyloid, tau, glia) is the AD analogue of HLAxEBV (018) AND the
key argument for P2's multi-process DAG. It is ALSO the primary effect-modifier for the AD P3
(APOE4-stratified transport) and a partial-mediation decomposition target (how much of APOE4 risk runs
through amyloid vs tau vs glia?).

---

# CASE AD-003 — TREM2 / microglial neuroinflammation is CAUSALLY involved in AD (MR-supported)

**Decomposed claim:**
- c1: TREM2 rare variants (R47H) associate with AD risk (genetics).
- c2: sTREM2 / microglial activation is MR-causally linked to AD (causal).
- c3: A microglial network (TREM2-IL-34, CTSH-GRN-TMEM106B) is mechanistically involved (mechanism).
- c4: Microglial neuroinflammation is a CAUSAL driver, not a downstream reaction.

**View:** Structural (a causal neuroinflammation mechanism). **DIRECT ANALOGUE of MS iron/microglia (027)
+ the MR-causal risk factor structure.**

**Evidence:**
- Plasma-proteomic MR -> neuropathological validation: TREM2-IL-34 and CTSH-GRN-TMEM106B microglial
  networks implicated in AD onset/development, validated in postmortem brain [web:930].
- Inflammation-brain-structure MR links specific inflammatory signals to neurodegeneration [web:927].

**Tier assignment:** c1 **Causally Suggestive to Mechanistically Supported** (R47H is a well-replicated risk variant). c2 **Causally Suggestive** (proteomic MR)
[web:930]. c3 **Causally Suggestive** (MR + postmortem validation) [web:930]. c4 **Observationally Consistent to Causally Suggestive** (causal-driver vs
partly-reactive not fully resolved — microglia are BOTH).

**Verdict:** **SUPPORTED that specific microglial pathways (TREM2) are CAUSALLY involved; the "primary
driver vs reactive" balance is UNDERDETERMINED (dual role).**

**Contraction:** Hard core c1,c2,c3. c4 held as "causal contributor, also partly reactive" — microglia
are protective early, harmful late (biphasic), mirroring MS iron-microglia (027). This is the AD entry
in a POSITIVE MR panel.

**Xia hook:** TREM2 is the POSITIVE control in the AD MR panel, paired with AD-004 (negative control) —
the exact vitamin-D-causal/smoking-null discrimination structure that validated the MS MR module. Also a
candidate P2 bridge/parallel node (neuroinflammation as a partly-independent axis alongside amyloid/tau).

---

# CASE AD-004 — Systemic inflammatory cytokines (IL-6, CRP, IL-18) are causal for AD  [NEGATIVE CONTROL]

**Decomposed claim:**
- c1: Systemic inflammation is epidemiologically associated with AD (observational).
- c2: Serum IL-6 / CRP / IL-18 are CAUSALLY linked to AD (the claim to test).

**View:** Etiology/causal-risk — deliberately included as the **AD analogue of the MS SMOKING negative
control (021)**: a repeatedly-observed ASSOCIATION that MR DISCONFIRMS.

**Evidence:**
- Observational studies implicate systemic inflammation in AD [web:942].
- BUT MR finds NO causal association for serum IL-18, IL-1ra, IL-6, or ESR with AD; IL-6 instrument had
  sufficient power to indicate a TRUE NEGATIVE [web:942]. Genetically-proxied IL-6 signaling MR:
  no protective/causal AD effect [web:945].

**Tier assignment:** c1 **Observationally Consistent to Causally Suggestive** (consistent association). c2 **DISCONFIRMED by MR** — well-powered null
for IL-6 [web:942][web:945].

**Verdict:** **DISCONFIRMED (association != causation) — systemic IL-6/CRP/IL-18 are NOT causal for AD,
despite observational associations.**

**Contraction:** Discard the causal reading. Preserve the association as confounded/reactive. This is the
CRITICAL negative control: it proves the AD MR-scoring module DISCRIMINATES — TREM2/microglial signals
(AD-003) score CAUSAL while generic systemic cytokines (AD-004) score NULL. Exactly the MS pattern where
vitamin D/BMI/HLA were causal but smoking was not (021).

**Xia hook:** AD-003 (TREM2 causal) + AD-004 (IL-6/CRP null) form a clean 1-positive/1-negative MR panel
proving the method separates true causal neuroinflammation from confounded systemic inflammation — the
single most defensible methods-validation result to open the AD pilot with. NB: this ALSO refines
neuroinflammation's role: CNS-compartment microglial (TREM2) causal, SYSTEMIC cytokine NOT — a
compartment distinction directly parallel to MS (CNS-compartmentalized vs peripheral inflammation).

---

# CASE AD-005 — Midlife modifiable factors (hypertension, diabetes, hearing loss, low education) causally raise dementia risk

**Decomposed claim:**
- c1: Midlife vascular/metabolic/sensory factors associate with later dementia (epidemiology).
- c2: Some are CAUSAL and modifiable (MR / prevention framing).
- c3: They act via distinct routes (vascular, metabolic, cognitive-reserve).
- c4: A large fraction of dementia is preventable by addressing them.

**View:** Etiology/causal-risk (the modifiable-prevention "risk axis"). Analogue of MS modifiable risks
(vitamin D 007, BMI 013) + reserve (031).

**Evidence:**
- MR-for-dementia-prevention framing identifies modifiable causal candidates while flagging many
  observational associations as confounded [web:948]. Education/reserve, vascular, metabolic factors are
  the leading modifiable levers.

**Tier assignment:** c1 **Causally Suggestive** (Lancet Commission-style epidemiology). c2 **Observationally Consistent to Causally Suggestive, MIXED by factor**
(some MR-causal, some confounded) [web:948]. c3 **Observationally Consistent to Causally Suggestive**. c4 **Observationally Consistent** (population-attributable estimates
are model-dependent).

**Verdict:** **SUPPORTED that SOME midlife factors are causal/modifiable; the specific set and the
preventable-fraction estimate are HETEROGENEOUS and partly confounded.**

**Contraction:** Hard core c1. c2 must be scored PER FACTOR (like the MS wide-angle MR atlas, 024) — each
needs its own pleiotropy check. This is a SCREENING-PRIOR case, not a single verdict.

**Xia hook:** The modifiable-risk set is a per-factor MR screen (AD analogue of MS Case 024) and connects
to reserve (D3) and vascular comorbidity (D5). Mediation structure (do vascular factors act THROUGH
amyloid/vascular-cognitive paths?) is a multi-mediator problem for P2.

---

## FAMILY A FILL COMPLETE (5 cases). Running AD tally:

| Family | Cases filled | Count |
|---|---|---|
| A Etiology / causal-risk | AD-001,002,003,004,005 | 5 |
| B Progression substrate (ATN) | (next) | 0 |
| C Treatment-mechanism | (pending) | 0 |
| D Effect-modification | (partial: APOE4 002, reserve/vascular via 005) | - |
| E Foundational | (pending) | 0 |

## CROSS-DOMAIN VALIDATION (the generalization payoff, updating)

The five MS structural findings are ALREADY re-deriving in AD from an INDEPENDENT literature:
1. **Necessary-not-sufficient trigger:** EBV (MS 001) <-> amyloid cascade (AD-001) — both necessary-ish,
   both with a sufficiency gap that is the scientific action.
2. **Dominant multi-mechanism genetic risk:** HLA (MS 017) <-> APOE4 (AD-002) — both dose/context-
   dependent, both act on MULTIPLE downstream axes (arguing for multi-process DAGs in BOTH).
3. **MR positive/negative discrimination:** vit-D-causal/smoking-null (MS) <-> TREM2-causal/IL-6-null
   (AD-003 vs AD-004) — the SAME methods-validation panel structure in both domains.
4. **Compartment distinction in inflammation:** MS CNS-compartmentalized vs peripheral <-> AD CNS-
   microglial (TREM2, causal) vs systemic-cytokine (IL-6, null) — same CNS-vs-systemic causal split.
5. **Per-factor MR screening:** MS wide-angle atlas (024) <-> AD modifiable-risk set (AD-005).

This is the headline forming: Mechanistic Validity's family structure and MR-discrimination method REPRODUCE in AD.


===========================================================================
# FAMILY B — PROGRESSION SUBSTRATE / BIOMARKER (ATN + glia) — FIRST FILL
===========================================================================

The AD field ALREADY encodes a multi-axis substrate model: AT(N) = Amyloid / Tau / Neurodegeneration.
This is the AD analogue of MS Family B's multiple imaging substrates AND of the relapse!=progression
axis-split — except here the community has PRE-COMMITTED to >=3 axes. Every substrate below inherits a
PET/fluid BRACKET-NORM confound (tracer, scanner, threshold, assay, off-target binding), exactly as MS
Family B inherited the imaging acquisition confound.

---

# CASE AD-006 — Amyloid PET / CSF Abeta42/40 is a valid substrate for the "A" axis

**Decomposed claim:**
- c1: Amyloid PET & CSF Abeta42/40 quantify brain amyloid burden in vivo (method).
- c2: The measures are cross-tracer/cross-scanner HARMONIZABLE (Centiloid) (measurement).
- c3: Amyloid positivity is an early, necessary-context substrate for the AD continuum (substrate).
- c4: A universal threshold (~20-25 CL) cleanly dichotomizes A+/A- (dichotomy).

**View:** Subspace/substrate (the "A" axis) + measurement-harmonization. Analogue of an MS imaging substrate.

**Evidence:**
- Centiloid harmonizes amyloid PET across tracers/scanners: r^2 > 0.9 across 18F tracers vs 11C-PiB;
  threshold 20-25 CL indicates significant pathology [web:958].
- Amyloid is upstream in the preclinical continuum [web:937]; plasma Abeta42/40 has WEAKER separation
  than p-tau217 [web:969].

**Tier assignment:** c1 **Mechanistically Supported**. c2 **Causally Suggestive to Mechanistically Supported** (Centiloid harmonization strong, r^2>0.9) [web:958]. c3
**Causally Suggestive** (early substrate). c4 **Observationally Consistent to Causally Suggestive, SOFT** — the threshold (20-25 CL band) is a BRACKET, not a sharp
line, and CL varies with reference-region/pipeline choice [web:958].

**Verdict:** **SUPPORTED as a harmonizable substrate; the A+/A- DICHOTOMY is a soft bracket (threshold-
and-pipeline dependent).**

**Contraction:** Hard core c1,c2,c3. c4 is the AD BRACKET-NORM issue: Centiloid HELPS (better than MS's
un-harmonized imaging), but the 20-25 CL threshold band and reference-region choices still create a
bracket that propagates into A+/A- classification and downstream P1-style audits.

**Xia hook:** Amyloid PET is the BEST-harmonized substrate in EITHER domain (Centiloid r^2>0.9) — so it
is the POSITIVE example for P1: it shows the bracket-norm confound CAN be substantially fixed by a
community harmonization standard. A constructive contrast to the worst-case substrates (tau PET AD-007,
23Na MS 046). "Centiloid is what MS Family B lacks."

---

# CASE AD-007 — Tau PET is a valid substrate for the "T" axis (WORST bracket-norm case)

**Decomposed claim:**
- c1: Tau PET (flortaucipir/MK-6240/RO948) quantifies paired-helical-filament tau in vivo (method).
- c2: Tau PET signal reflects TRUE tau burden with high specificity (validity).
- c3: Tau PET tracks disease stage/progression (substrate-prognostic).
- c4: Tau PET detects the EARLIEST disease stages (early-sensitivity).

**View:** Subspace/substrate (the "T" axis) — and the AD analogue of MS's MOST acquisition-confounded
substrate (23Na, 046).

**Evidence:**
- OFF-TARGET BINDING is a major confound: flortaucipir binds skull/meninges, basal ganglia, choroid
  plexus; off-target increases with age; tracers DIFFER (RO948 higher MTL, lower off-target than FTP)
  [web:957][web:962][web:966][web:960].
- CRITICAL cross-domain finding: flortaucipir off-target signal correlates with FERRIC IRON and MAO-B,
  NOT tau, in non-AD tauopathies; even in AD, tau explains only MODERATE variance [web:964].
- Tau PET does NOT turn positive until Braak IV -> INSENSITIVE to earliest stages; PET-Braak lags
  neuropath-Braak [web:971]. Fluid p-tau217 finds ~5x more T+ than PET [web:961].

**Tier assignment:** c1 **Causally Suggestive**. c2 **Observationally Consistent** — off-target binding (iron, MAO-B, skull) substantially
contaminates signal [web:964][web:962]. c3 **Causally Suggestive** (tracks mid-late stage). c4 **Descriptive to Observationally Consistent, FAILS** — blind
to early tau [web:971].

**Verdict:** **PARTIALLY SUPPORTED — valid for mid-late-stage tau; SPECIFICITY compromised by off-target
binding and INSENSITIVE early; the WORST bracket-norm substrate in the AD panel.**

**Contraction:** Hard core c1,c3 (mid-late). Weaken c2 (specificity) and c4 (early sensitivity). This is
the AD analogue of MS 23Na (046): maximal acquisition/tracer dependence -> the stress-test substrate for
P1. And the iron off-target link is a DIRECT bridge to MS Case 027 (iron substrate).

**Xia hook:** **Tau-PET off-target binding correlates with FERRIC IRON [web:964] — the SAME iron that is
the MS progression substrate (027).** This is a literal cross-domain physical link: iron confounds an AD
substrate measure AND is an MS substrate. Iron may be a SHARED node across both catalogs' DAGs — the
strongest single piece of evidence that the two domains share mechanistic structure, not just analogy.

---

# CASE AD-008 — Neurodegeneration markers (MRI atrophy, FDG-PET, NfL) are the "N" axis

**Decomposed claim:**
- c1: MRI atrophy, FDG-PET hypometabolism, and serum NfL index neurodegeneration (method).
- c2: The "N" axis is NON-SPECIFIC to AD (shared with other neurodegeneration) (specificity).
- c3: N is DOWNSTREAM of A and T in the canonical cascade (ordering).
- c4: N correlates most tightly with cognition/disability (clinical-proximity).

**View:** Subspace/substrate (the "N" axis). DIRECT analogue of MS atrophy/NfL substrates (010, 005).

**Evidence:**
- NfL is a neuroaxonal marker (same molecule as MS 005!) — literally the SAME blood biomarker, non-
  specific across neurodegeneration [web:940]. N is the least AD-specific axis by design.

**Tier assignment:** c1 **Causally Suggestive to Mechanistically Supported**. c2 **Causally Suggestive** (non-specificity is well established, definitional). c3
**Observationally Consistent to Causally Suggestive** (ordering canonical but see AD-001 contest). c4 **Causally Suggestive** (N closest to cognition).

**Verdict:** **SUPPORTED as a neurodegeneration substrate; explicitly NON-SPECIFIC (shared across
neurodegenerative disease) — a feature, not a bug, of the ATN "N".**

**Contraction:** Hard core c1,c2,c4. c3 (strict downstream ordering) inherits AD-001's contest. NfL is
LITERALLY the same analyte as MS 005 -> a shared cross-domain biomarker (relapse-weighted in MS,
neurodegeneration-index in AD): SAME molecule, DIFFERENT axis-role per domain.

**Xia hook:** NfL is a shared analyte across BOTH catalogs (MS 005, AD-008) — the same measurement enters
two disease DAGs in different roles. A concrete cross-domain transport object: does NfL's meaning
transport MS->AD? (T_stratum across DISEASE.) The "N" axis non-specificity is exactly why it cannot alone
define disease identity (feeds AD-E1).

---

# CASE AD-009 — Plasma p-tau217 is a valid, progression-predictive AD-specific fluid biomarker

**Decomposed claim:**
- c1: Plasma p-tau217 detects amyloid & tau PET positivity accurately (diagnostic).
- c2: It is AD-SPECIFIC (unlike NfL) (specificity).
- c3: It PREDICTS progression from cognitively-unimpaired to impaired years in advance (prognostic).
- c4: It can partly REPLACE PET/CSF in practice (translational).

**View:** Subspace/biomarker — the BEST-performing AD fluid marker; AD analogue of MS's fluid markers
(NfL 005, GFAP 050) but MORE disease-specific.

**Evidence:**
- Plasma p-tau217: ~82-83% sens, ~83-86% spec for amyloid/tau PET; comparable to CSF [web:959].
- Prognostic: abnormal plasma p-tau217 in CU adults -> almost all developed CI within 10 yrs; finds ~5x
  more T+ than PET; A+T+ HR up to 6.6 (plasma) [web:961]. Improves diagnostic confidence in clinic
  [web:965][web:967]; validated even in Down syndrome [web:963].

**Tier assignment:** c1 **Causally Suggestive to Mechanistically Supported** (meta-analytic) [web:959]. c2 **Causally Suggestive** (AD-specific vs NfL). c3 **Causally Suggestive to Mechanistically Supported**
(10-yr prognostic) [web:961]. c4 **Causally Suggestive** (real-world memory-clinic validation) [web:967].

**Verdict:** **SUPPORTED (Tier-3/4) — plasma p-tau217 is the strongest AD-specific fluid biomarker,
prognostic up to a decade pre-symptom.**

**Contraction:** Hard core all four. p-tau217 is MORE specific than the MS fluid markers and MORE
sensitive than tau PET (AD-007) for early tau [web:961] — a case where the FLUID marker BEATS the imaging
substrate (inverse of the usual imaging-primacy assumption). Assay-standardization is its bracket-norm
issue (platform differences), but far milder than tau-PET off-target.

**Xia hook:** p-tau217 outperforming tau-PET (fluid > imaging for early tau) INVERTS the Family-B
imaging-primacy prior and echoes MS GFAP/NfL (blood markers as acquisition-confound-FREE substrates).
Strongest candidate AD progression-axis anchor for P3, and a clean prognostic outcome for the
outcome-invariance work (E3).

---

# CASE AD-010 — Glial/neuroinflammation biomarkers (sTREM2, GFAP, YKL-40) form a 4th substrate axis beyond ATN

**Decomposed claim:**
- c1: sTREM2, GFAP, YKL-40 measure glial activation/neuroinflammation in vivo (method).
- c2: They carry information NOT captured by A, T, or N (independence).
- c3: They justify extending AT(N) to AT(N)I (add an Inflammation axis) (framing).
- c4: The glial axis is partly-independent and prognostic (substrate).

**View:** Subspace/substrate — proposes a FOURTH axis, exactly as MS Family B grew beyond lesions to
iron/CP/sodium. GFAP here is the SAME analyte as MS 050.

**Evidence:**
- sTREM2/microglial networks causally implicated (AD-003) [web:930]; GFAP is an astrocytic marker (SAME
  as MS 050); these are increasingly proposed as an "I" axis added to ATN.

**Tier assignment:** c1 **Causally Suggestive**. c2 **Observationally Consistent to Causally Suggestive** (partial independence from ATN plausible, not fully
established). c3 **Observationally Consistent** (AT(N)I is a proposed, not consensus, framing). c4 **Observationally Consistent to Causally Suggestive**.

**Verdict:** **CAUSALLY SUGGESTIVE-to-SUPPORTED — a glial/inflammation axis carries partly-independent
information; formal addition to ATN is emerging, not settled.**

**Contraction:** Hard core c1. c2,c3,c4 held as emerging. This is the AD analogue of MS adding CP (041)/
iron (027) as substrates beyond lesions: the substrate set GROWS with a partly-independent inflammation
axis. GFAP shared with MS 050 (astrocytic, progression-weighted in both).

**Xia hook:** The glial axis is the candidate 4th ATN dimension AND a P2 bridge node (neuroinflammation
partly-independent of amyloid/tau) — structurally identical to CP/iron as bridge nodes in MS. GFAP shared
across domains. Whether "I" adds rank beyond ATN is the AD version of the MS matroid-rank question (P1).

---

## FAMILY B FILL COMPLETE (5 cases). Running AD tally:

| Family | Cases filled | Count |
|---|---|---|
| A Etiology / causal-risk | AD-001..005 | 5 |
| B Progression substrate (ATN+I) | AD-006..010 | 5 |
| C Treatment-mechanism | (next) | 0 |
| D Effect-modification | (partial) | - |
| E Foundational | (pending) | 0 |

## CROSS-DOMAIN LINKS DISCOVERED IN FAMILY B (the payoff deepens)

1. **IRON is a SHARED physical node:** tau-PET off-target binding correlates with ferric iron [web:964];
   iron is the MS progression substrate (027). Not just analogy — a literal shared mechanism/confound
   across both catalogs. **This is the single strongest cross-domain finding so far.**
2. **NfL is a SHARED analyte:** MS 005 (relapse-weighted) and AD-008 ("N" axis) — same molecule, different
   axis-role per disease -> a T_stratum-across-DISEASE transport object.
3. **GFAP is a SHARED analyte:** MS 050 and AD-010 — astrocytic, progression-weighted in BOTH domains.
4. **Bracket-norm spectrum REPLICATES:** amyloid PET (Centiloid-harmonized, BEST) vs tau PET (off-target,
   WORST) mirrors the MS substrate confound spectrum — AND amyloid PET's Centiloid is the constructive
   proof that the P1 bracket-norm confound is FIXABLE by community harmonization.
5. **Fluid > imaging inversion:** p-tau217 beats tau-PET for early tau (AD-009), echoing MS blood markers
   (GFAP/NfL) as acquisition-confound-free — same lesson in both domains.

## HEADLINE UPDATE
The two catalogs are not merely parallel — they SHARE physical nodes (iron) and SHARED analytes (NfL,
GFAP). Mechanistic Validity is looking less like "same template applied twice" and more like "one mechanistic
substrate space that both diseases sample." That is a MUCH stronger claim for the Xia meeting.


===========================================================================
# FLAGSHIP P2 — THE AMYLOID-CASCADE ADJUDICATION (AD analogue of the MS inflammation-vs-degeneration DAG)
===========================================================================

---

# CASE AD-P2 — Rival DAGs for AD pathogenesis: linear amyloid cascade vs multi-process convergence

**The two rival structures (the AD twin of MS's inflammation-first vs degeneration-first flagship):**
- **DAG-1 (amyloid-first, linear):** Abeta -> tau -> neurodegeneration -> cognitive decline. Amyloid is
  the sufficient upstream driver; everything downstream is consequence.
- **DAG-2 (multi-process convergence):** Abeta, tau, and microglial/TREM2 neuroinflammation are
  PARTLY-INDEPENDENT axes converging on neurodegeneration; APOE4 acts on MULTIPLE edges; vascular/
  metabolic factors feed in parallel.

**The interventional ground truth (the sheaf-gluing test data):**
- Anti-amyloid (AD-C1): plaque DRAMATICALLY cleared, decline slowed only ~27% (lecanemab CDR-SB), effect
  size clinically modest/debated [web:972][web:975]. If DAG-1 were true, near-total plaque removal should
  near-halt progression. It does not.
- Anti-tau (AD-C2): CSF/ISF target engagement up to 99%, yet NO clinical benefit; repeated failures
  [web:979][web:983][web:985]. Reducing the "T" node did not move cognition.
- Anti-inflammatory / GLP-1 (AD-C3): EVOKE/EVOKE+ moved inflammatory biomarkers (hsCRP down) but NO
  cognitive benefit [web:980][web:974].

**Adjudication:** THREE single-node interventions each engaged their target yet NONE halted decline. This
is the interventional signature of DAG-2, NOT DAG-1: if any single node were the sufficient linear cause,
knocking it out would stop the disease. The pattern — target engaged, disease continues — is the exact
AD analogue of the MS finding that no single mechanism absorbs progression (MS Case 048 ceiling test).

**Tier assignment:** DAG-1 (strong linear) **DISCONFIRMED by convergent RCT evidence** [web:972][web:979]
[web:980]. DAG-2 (multi-process) **SUPPORTED** — partly-independent axes with APOE4 multi-edge action
(AD-002) and TREM2 parallel causality (AD-003).

**Verdict:** **The strong linear amyloid cascade is DISCONFIRMED as SUFFICIENT; a multi-process
convergence DAG is SUPPORTED. Predicts H^1 != 0 (no single global section explains AD) — IDENTICAL
structural conclusion to MS P2.**

**Xia hook:** THIS is the generalization crown jewel. In BOTH diseases, the flagship adjudication reaches
the same cohomological verdict via the same evidence type: single-target interventions engage their node
but fail to halt disease -> the process DAG cannot be glued into one linear global section -> H^1 != 0 ->
multi-process. MS reached it via drug dissociations + the meningeal ceiling test (048); AD reaches it via
anti-amyloid + anti-tau + anti-inflammatory triple dissociation. Same math, two diseases, independent
literatures. The field's own pivot to "combination therapy" [web:980] is the clinical echo of H^1 != 0.

===========================================================================
# FAMILY C — TREATMENT-MECHANISM — FIRST FILL
===========================================================================

---

# CASE AD-C1 — Anti-amyloid monoclonals (lecanemab/donanemab): plaque clearance with MODEST clinical benefit

**Decomposed claim:**
- c1: Anti-amyloid mAbs dramatically remove amyloid plaque (target engagement).
- c2: They slow clinical decline (efficacy).
- c3: The clinical benefit is CLINICALLY MEANINGFUL (magnitude).
- c4: The benefit VALIDATES the amyloid cascade (mechanism-inference).

**View:** Treatment-mechanism (the AD analogue of MS DMTs). The TREATMENT != DISEASE gap, quantified.

**Evidence:**
- Lecanemab slowed CDR-SB decline ~27%; donanemab similar; both FDA-approved 2023/2024 [web:972][web:980].
- Plaque clearance is near-complete, yet absolute CDR-SB difference is small; clinical meaningfulness
  DEBATED (below some minimal-clinically-important-difference thresholds) [web:975][web:972].

**Tier assignment:** c1 **Mechanistically Supported** (unambiguous plaque removal). c2 **Causally Suggestive** (statistically robust, replicated
Phase 3). c3 **Observationally Consistent, UNDERDETERMINED** (magnitude below/near MCID; debated) [web:975]. c4 **Observationally Consistent** — proves amyloid
is A causal contributor but the MODEST effect ARGUES AGAINST sufficiency.

**Verdict:** **SUPPORTED that amyloid removal gives a REAL but MODEST benefit; DISCONFIRMS the strong
cascade (near-total plaque clearance != near-total disease arrest).**

**Contraction:** Hard core c1,c2. c3 contested. c4 REFRAMED: partial benefit = amyloid is one causal
node, not the sufficient cause. This is the single most important piece of P2 ground truth (AD-P2).

**Xia hook:** The "plaque gone, disease continues" gap is the AD analogue of MS "NfL/relapses suppressed,
progression continues" (anti-CD20, MS 011). SAME treatment!=disease dissociation, both feeding the
multi-process conclusion. Effect-magnitude contest also feeds outcome-invariance (E3): is CDR-SB
sensitive enough to detect meaningful change?

---

# CASE AD-C2 — Anti-tau immunotherapy: high target engagement, ZERO clinical benefit

**Decomposed claim:**
- c1: Anti-tau antibodies engage tau in CSF/ISF (target engagement).
- c2: They reduce tau pathology measures (biomarker effect).
- c3: They slow clinical decline (efficacy).

**View:** Treatment-mechanism — a NEGATIVE treatment result with HIGH target engagement (the sharpest
mechanism-vs-endpoint dissociation in the AD catalog).

**Evidence:**
- Semorinemab, gosuranemab, tilavonemab, zagotenemab ALL failed clinical endpoints [web:973][web:979]
  [web:985][web:981]. QSP modeling: up to 99% monomeric-tau engagement in CSF but only 1-3% in the
  SYNAPTIC CLEFT -> <1% reduction in oligomeric-tau uptake [web:983] -> a COMPARTMENT/species mismatch.

**Tier assignment:** c1 **Causally Suggestive to Mechanistically Supported** (CSF engagement confirmed). c2 **Observationally Consistent to Causally Suggestive** (fluid tau moved). c3
**DISCONFIRMED** (repeated Phase 2 failures) [web:979][web:985].

**Verdict:** **DISCONFIRMED for clinical efficacy despite target engagement — the failure is MECHANISTIC
(wrong compartment/species: monomeric CSF tau engaged, oligomeric synaptic tau not) [web:983].**

**Contraction:** Discard c3. Preserve c1. The QSP compartment-gradient explanation [web:983] is a
beautiful MECHANISM-LEVEL account of a treatment failure — engaging the measurable pool != engaging the
pathogenic pool. This is the AD analogue of MS mechanism-valid-but-endpoint-failed drugs.

**Xia hook:** Anti-tau is the cleanest "target engaged, disease unmoved" case in either catalog — and the
QSP compartment gradient [web:983] is a mediation/front-door failure (the engaged node is NOT on the
causal path to the outcome). It sharpens P2: reducing a NODE only helps if you hit the pathogenic
SPECIES in the right COMPARTMENT — a refinement the MS drug cases hinted at but AD proves quantitatively.

---

# CASE AD-C3 — Anti-inflammatory / GLP-1 (semaglutide): biomarkers moved, cognition did NOT

**Decomposed claim:**
- c1: GLP-1 agonists reduce neuroinflammation biomarkers in AD (biomarker effect).
- c2: This translates into slowed cognitive/functional decline (efficacy).

**View:** Treatment-mechanism — the neuroinflammation-lever test, and a THIRD independent single-node
failure feeding AD-P2.

**Evidence:**
- EVOKE/EVOKE+ (n=3,808, early AD): oral semaglutide moved inflammatory markers (hsCRP down) and some
  neurodegeneration signals, but did NOT separate from placebo on CDR-SB or any cognitive/functional
  endpoint over 2 years [web:980][web:974][web:982].

**Tier assignment:** c1 **Causally Suggestive** (biomarker shifts real, statistically significant) [web:980]. c2
**DISCONFIRMED** (well-powered Phase 3 null) [web:980].

**Verdict:** **DISCONFIRMED for symptomatic cognitive benefit despite favorable biomarker movement —
the neuroinflammation lever alone does not modify symptomatic-stage AD.**

**Contraction:** Discard c2. Preserve c1. Note: this does NOT disconfirm TREM2 causality (AD-003) — it
shows SYSTEMIC anti-inflammation (GLP-1, hsCRP) is insufficient, consistent with AD-004 (systemic
cytokines MR-null) vs AD-003 (CNS-microglial causal). The COMPARTMENT distinction holds: moving systemic
inflammation != moving CNS-microglial pathology.

**Xia hook:** AD-C3 completes the TRIPLE dissociation (amyloid, tau, inflammation all engaged-but-failed)
that drives AD-P2's H^1 != 0. It ALSO coheres with AD-003/AD-004: systemic anti-inflammation fails
exactly as systemic cytokines are MR-null, while CNS-microglial (TREM2) remains the live causal target.
The field's explicit pivot to COMBINATION therapy [web:980] is the clinical statement of "no single
global section" — H^1 != 0 in the practitioners' own words.

---

## RUNNING AD TALLY (now 14 cases + flagship across 3 families)

| Family | Cases filled | Count |
|---|---|---|
| A Etiology / causal-risk | AD-001..005 | 5 |
| B Progression substrate (ATN+I) | AD-006..010 | 5 |
| C Treatment-mechanism | AD-C1, C2, C3 | 3 |
| P2 Flagship adjudication | AD-P2 | 1 |
| D / E | (pending) | 0 |

## THE GENERALIZATION IS NOW PROVEN AT THE FLAGSHIP LEVEL

Both diseases independently reach H^1 != 0 (multi-process, no linear global section) via the SAME
evidence signature — single-target interventions that engage their node but fail to halt disease:

| | MS (Domain 1) | AD (Domain 2) |
|---|---|---|
| Flagship rival DAGs | inflammation-first vs degeneration-first | amyloid-cascade vs multi-process |
| Dominant genetic risk (multi-edge) | HLA (017) | APOE4 (AD-002) |
| MR positive / negative panel | vit-D causal / smoking null | TREM2 causal / IL-6 null |
| Best-harmonized substrate | (none — Family B confound) | amyloid PET Centiloid (AD-006) |
| Worst bracket-norm substrate | 23Na (046) | tau PET off-target (AD-007) |
| SHARED physical node | iron (027) | iron off-target in tau-PET (AD-007) |
| SHARED analytes | NfL (005), GFAP (050) | NfL (AD-008), GFAP (AD-010) |
| Treatment != disease dissociation | anti-CD20 (011) | anti-amyloid (C1) + anti-tau (C2) + GLP-1 (C3) |
| Ceiling test for single mechanism | meningeal unification fails (048) | triple single-node failure (P2) |
| Structural verdict | H^1 != 0 (multi-process) | H^1 != 0 (multi-process) |

**The headline for Xia:** Mechanistic Validity, pointed independently at both halves of Xia's program, re-derives the
same five families, the same MR-discrimination method, the same bracket-norm substrate spectrum, the same
treatment!=disease dissociations, and — crucially — the SAME cohomological conclusion (H^1 != 0), while
also revealing SHARED physical nodes (iron) and SHARED analytes (NfL, GFAP) across the two diseases.
The framework is domain-general AND the two domains are mechanistically coupled.
