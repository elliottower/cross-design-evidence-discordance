# Pre-Registration Amendment 3: Reference Correction

**Status:** FROZEN (pending commit SHA)
**Date:** 2026-08-07
**Parent documents:** PREREGISTRATION.md (SHA: b96d10a), PREREGISTRATION_AMENDMENT_EXPLORATORY.md (SHA: 1f300a9), PREREGISTRATION_AMENDMENT_2_BLIND.md (SHA: 12ea0ed)
**Scope:** Corrects bibliographic errors found in an audit of the reference list. One correction changes an input effect size; no classification changes.

**Commit SHA:** _pending_

---

## What prompted this

Every DOI, PMID and arXiv identifier in the bibliography was resolved against
Crossref, OpenAlex, PubMed and Europe PMC. Thirteen of 73 entries carried
identifiers that did not resolve, or resolved to a different paper. Each was
traced to its real source. Twelve were metadata errors — wrong journal, wrong
volume, wrong article number, wrong first author, paraphrased title — with no
effect on any number used in the analysis.

The thirteenth changed an input, and is the reason this amendment exists.

## The substantive correction: `hu2019` → Filippini et al. 2021

**What the frozen record says.** `PREREGISTRATION.md` records Anti-CD20-MS with
$d_{\mathrm{OBS}} = 0.442$. The supplementary data recorded the source as "Hu
2019 B-cell count OR for MS," with OR = 2.23, no confidence interval.

**What the audit found.** No paper matching that citation exists. There is no
article at *Autoimmunity Reviews* 18(5):525–530, and no matching title in
PubMed, Crossref or OpenAlex.

**A second problem, independent of the first.** The recorded quantity was a
*B-cell count* association with MS risk. The manuscript describes this slot as
"observational B-cell depletion efficacy." Those are different quantities: an
etiologic exposure–outcome association is not a treatment-effect estimate. The
frozen number was therefore mismatched to the construct the analysis claims to
use, whatever its source.

**The replacement, and how it was chosen.** The selection rule was fixed before
computing any effect size:

> Take the pooled observational (non-randomized) estimate of anti-CD20 therapy
> against a comparator **outside** the anti-CD20 class, for relapse, from the
> highest available certainty tier.

The rule excludes two classes of candidate the audit surfaced first, and it
excludes them on design grounds rather than on their numbers:

- **Randomized-trial meta-analyses** (e.g. Wu et al. 2022, *CNS Drugs*, ten RCTs)
  are ineligible. This framework treats observational, MR and RCT evidence as
  three distinct types; using an RCT synthesis in the observational slot
  collapses two of the three categories the analysis rests on.
- **Within-class comparisons** (e.g. Roos et al. 2023, *JAMA Neurology*,
  rituximab vs ocrelizumab) are ineligible. These estimate which anti-CD20 agent
  performs better, not whether B-cell depletion works, and so do not speak to the
  mechanism the MR leg estimates.

The rule selects:

> Filippini G, Kruja J, Del Giovane C. "Rituximab for people with multiple
> sclerosis." *Cochrane Database of Systematic Reviews* 2021;11:CD013874.
> doi:10.1002/14651858.CD013874.pub2. PMID 34748215.
>
> Pooled non-randomized studies of intervention. Rituximab vs interferon beta or
> glatiramer acetate, relapses: **HR 0.14 (95% CI 0.05–0.39)**, 335 participants,
> moderate-certainty evidence.

Chinn conversion, unchanged from the frozen protocol:
$d = |\ln(0.14)| \cdot \sqrt{3}/\pi = \mathbf{1.084}$ (SE 0.289).

**Population caveat, declared here rather than after the fact.** Several cohorts
contributing to this pooled estimate are natalizumab-switch populations enriched
for JC-virus positivity. That is a narrower and higher-effect population than a
general-population initiator design, so 1.084 plausibly overstates what an
unselected observational comparison would give. Studies in unselected
populations report effects near the null. This is stated because it cuts against
the direction the correction moves the number.

## What changed, and what did not

| | frozen record | corrected |
|---|---|---|
| $d_{\mathrm{OBS}}$ | 0.442 | 1.084 |
| observational class | non-trivial | non-trivial |
| MR $d$ | 0.103 | 0.103 |
| classification | concordance | concordance |
| prediction | success | success |
| outcome | Approved | Approved |
| scored correct | yes | yes |

**No analysis was re-run, because there is nothing to re-run.** The
classification procedure is a deterministic rule over published effect sizes with
no fitted parameters. $d_{\mathrm{OBS}}$ enters only through the threshold test
$d \geq 0.10$. Both values satisfy it, so every downstream quantity —
family classification, predicted outcome, accuracy count, the MR-only ablation,
the McNemar comparison — is unchanged. The corrected value sits further from the
decision boundary than the frozen one.

The threshold-sensitivity caveat reported for this family concerns its **MR** leg
($d = 0.103$, clearing by 0.003) and is untouched by this amendment.

## Metadata-only corrections

Traced to the real source; no analysis input affected.

| key | frozen record | corrected |
|---|---|---|
| `song2020` | *Front Neurosci* 14:573 | 14:157, doi 10.3389/fnins.2020.00157. Song YJ is first author. Study is **estrogen** replacement therapy and pools **21** articles, not 16. OR 0.672 (0.581–0.779) confirmed |
| `robinson2021urate` | *Nat Rev Rheumatol* 17:649–662, PMID 34497383 | *BMC Rheumatology* 5:33, doi 10.1186/s41927-021-00204-4, PMID 34452645. HR 18.62 confirmed |
| `barth2025` | "Barth D," *Nat Commun* | Oppenheimer H et al.; Barth C is senior author. doi 10.1038/s41467-025-65878-7 |
| `cheng2014` | *Molecular Neurobiology* | *Clinical Interventions in Aging* 9:1031–1038, doi 10.2147/cia.s65921 |
| `sokolova2013` | *PLoS ONE* 8(6):e65616 | 8(4):e61032, doi 10.1371/journal.pone.0061032 |
| `szulc2014` | 2014, doi 10.1002/jbmr.2017 | 2013, *JBMR* 28(4):855–864, doi 10.1002/jbmr.1823 |
| `bovijn2020` | *Nature Medicine* | *Science Translational Medicine* 12(549):eaay6570 |
| `sglt2paradox2025` | "Zhang" et al., doi …177113 | Huang H et al., *Eur J Pharmacol* 1003:177957 |
| `nie2015il23r` | "Nie & Zhao," *Human Genetics* 135:529–541 | Cotterill L et al., *Can J Gastroenterol* 24(5):297–302, doi 10.1155/2010/480458. OR 0.41 (0.37–0.46) across 26 studies — an exact match to the recorded figure |

Two entries carry statistics that remain unverified against the source text and
are flagged in the bibliography rather than quoted as confirmed: `bovijn2020`
(OR 0.59 per SD, absent from the abstract) and the author list of
`sglt2paradox2025`.

## Reproducing the audit

`resolve_refs.py` resolves every identifier in a `.bib` or `\bibitem` list against
Crossref and arXiv, and searches Crossref then OpenAlex by title where no
identifier is present. It writes `references.resolved.yaml` beside the source, one
record per entry with a verdict. Re-running rewrites the file, so it states the
current condition of the bibliography rather than accumulating a log.

At the time of this amendment: 70 of 73 entries resolve. The three remaining are
`ference2019`, `ference2019ldl` and `ogawa2014`, which are the correct papers;
the registry returns markup (`<i>ACLY</i>`, `<scp>L</scp>`) inside their titles
and the string comparison fails on it.
