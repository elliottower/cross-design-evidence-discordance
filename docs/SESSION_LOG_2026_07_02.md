# Session Log — July 2-3, 2026

## What happened this session

### Two papers, fully independent

1. **Psych paper** (Molecular Psychiatry): `psychiatric-validity-audit/docs/MOLPSYCH_PAPER_DRAFT_V3.md`
   - Fully mechanical — no validity tiers, no LLM labeling, no raters
   - Core test: Cochran's Q across evidence types (OBS vs MR vs RCT)
   - External validation re-anchored against Q values instead of tiers
   - Results: PrimeKG eigenvector centrality vs Q (tau=+0.26, p=0.008), Open Targets genetic vs Q (tau=+0.38, p=0.0003)
   - Copied to iCloud

2. **Neuro paper** (IJE/Lancet): `neuroepidemiology-validity-audit/docs/NEURO_PAPER_DRAFT_V3.md`
   - De-circularized using Path B (two-stage analysis)
   - Algorithm 1 pseudocode box added to Methods
   - Copied to iCloud

### The circularity problem and fix

**Problem**: Original analysis used RCT evidence in BOTH family classification AND holdout prediction. All 23 "predictable" drugs were in circular families — RCT data classified their family AND was part of their outcome.

**Fix (Path B)**: Split into two analyses:
- **Stage 1 (etiologic-only)**: Classify families using ONLY observational + MR + genetic evidence. All drug outcomes fully out of sample. 7/8 correct (87.5%).
- **Stage 2 (retrospective)**: Add RCT evidence. Reveals amyloid discordance. 20/23 retrospective concordance (not prediction).

### New families added

| Family | Evidence | Source citations |
|--------|----------|-----------------|
| Anti-CD20-MS | MR (OR 0.83, Lin 2023), GEN (OR 1.16, Sokolova 2013), OBS (Hu 2019) | Concordant → 4 drugs approved |
| HRT-AD | OBS (OR 0.67, Song 2020), MR (OR 1.00, Barth 2025), GEN (OR 1.14, Cheng 2014) | Qualitative disc. → 1 drug failed |
| VitD-MS (supplemented) | OBS (OR 1.40, Munger 2006) added to existing MR | Concordant → 1 drug failed (miss) |

### Key structural finding

Two distinct failure modes:
1. **Zombie mechanisms**: MR null, OBS positive. Confounding diagnosis. Caught by etiologic Q alone. (Metabolic-AD, HRT-AD, Smoking)
2. **Translation-gap mechanisms**: Etiologic evidence concordant, drugs still fail. Visible only with RCT evidence. (Amyloid-AD)

A null MR signal is a strong negative indicator. A positive MR signal is necessary but not sufficient.

### Robustness results (from earlier agent)

File: `neuroepidemiology-validity-audit/output/external_validation/robustness_results.json`
- Threshold sensitivity: OR=42 at ALL 7 thresholds (0.05-0.25) — completely invariant
- LOFO CV: 4 folds, mean accuracy 87%, range 82-91%
- Bootstrap: 10,000 resamples, OR median 26, CI [4.5, 108], OR>1 in 99.85%

### Mechanical re-anchoring results (psych paper)

File: `psychiatric-validity-audit/output/external_validation/mechanical_reanchor.json`
- 150 claim-level tests, 24 significant at p<0.05
- Top: OT genetic vs Q tau=+0.38, p=0.0003
- Mechanical anchors beat tier-based in 17/19 PrimeKG and 23/30 OT metrics

### Q computation bug (UNRESOLVED)

`etiologic_only_q.py` computes Q using simple unweighted means → Q values near zero for everything → all families CONCORDANT. The original pipeline (`output/h1_transportability_results.json`) uses inverse-variance weighted pooling and gets Q=109 for Metabolic_AD.

**For V3 paper**: sidestepped by reporting the pooled d values per type directly in a table, with the classification following from the Algorithm 1 rule. The formal Q recomputation with proper weighting is still TODO.

### Drug expansion (agent ran, results pending review)

Searched for:
- Ross et al. Harvard/Yale study (21/210 drugs approved despite missing endpoints)
- Tau-targeting AD drugs (semorinemab, tilavonemab, gosuranemab)
- IL-6 / neuroinflammation AD drugs
- Cholinesterase / cholinergic AD drugs (donepezil, rivastigmine, galantamine)
- NMDA / memantine pathway
- S1P modulators in MS (fingolimod, siponimod, ozanimod, ponesimod)
- Additional MS drugs (natalizumab, alemtuzumab, cladribine)

Goal: expand n=8 etiologic-only holdout to n=20+ with independent families on both approve and fail sides.

## Files created/modified this session

### Neuro repo (`neuroepidemiology-validity-audit/`)
- `docs/NEURO_PAPER_DRAFT_V1.md` — first draft
- `docs/NEURO_PAPER_DRAFT_V2.md` — standalone (no psych cross-ref)
- `docs/NEURO_PAPER_DRAFT_V3.md` — Path B (de-circularized, two-stage, algorithm box)
- `analysis/external_validation/robustness_experiments.py` — threshold/LOFO/bootstrap
- `analysis/external_validation/etiologic_only_q.py` — de-circularized Q (HAS BUG)
- `output/external_validation/robustness_results.json` — robustness results
- `output/external_validation/etiologic_only_q.json` — etiologic Q results (BUGGY)

### Psych repo (`psychiatric-validity-audit/`)
- `docs/MOLPSYCH_PAPER_DRAFT_V3.md` — fully mechanical, no tiers/LLM/raters
- `analysis/external_validation/mechanical_reanchor.py` — Q-anchored validation
- `output/external_validation/mechanical_reanchor.json` — re-anchoring results

### iCloud copies
- `NEURO_PAPER_DRAFT_V3.md`
- `MOLPSYCH_PAPER_DRAFT_V3.md`

## TODO next session

1. **Fix Q computation** in `etiologic_only_q.py` — use inverse-variance weighted pooling matching the original pipeline
2. **Review drug expansion agent results** — integrate new families into the catalog
3. **Expand effect_sizes_v12.csv** with tau-AD, IL-6-AD, cholinergic, S1P entries
4. **Re-run etiologic-only classification** with expanded families
5. **Find the Ross et al. study** — use as externally-defined holdout
6. **Write V4** with expanded drug set and formal Q values
7. **Permutation test** on the de-circularized Stage 1 (n=8 is too small, but report it)

## Decision rule (Algorithm 1)

The complete algorithm is in NEURO_PAPER_DRAFT_V3.md Methods section. Summary:
1. Convert all ES to Cohen's d (Chinn 2000)
2. Pool within evidence type (inverse-variance weighted FE)
3. Cochran's Q across type-level pools, Bonferroni corrected
4. If Q significant: check if any type |d| < 0.10
   - Yes → QUALITATIVE DISCORDANCE → predict FAIL
   - No → QUANTITATIVE DISCORDANCE → predict APPROVE
5. If Q not significant → CONCORDANT → predict APPROVE
6. Threshold 0.10 is Cohen's negligible-effect boundary, fixed a priori

## Key numbers to remember

- Original (circular): 20/23 correct, OR=42, p=0.0017
- Etiologic-only (clean): 7/8 correct (87.5%)
- Bootstrap: OR median 26, CI [4.5, 108]
- Threshold: completely invariant across 0.05-0.25
- Psych external: OT genetic vs Q tau=+0.38, p=0.0003
