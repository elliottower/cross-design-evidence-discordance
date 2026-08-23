"""Build paper_v10_reviewer3.tex from paper_v9_reviewer1.tex.

Run:  uv run python paper/patches/patch_v10_reviewer3.py

Every edit is an exact-match replacement. The script asserts that each target
string occurs exactly once in the source and aborts otherwise, so a silent
partial application is impossible. v9 is never modified.

Edits respond to Reviewer 3 (23 Aug 2026) and to four internal inconsistencies
found while checking Reviewer 3's points; see reviews/REVIEWER3_AUDIT_v1.md.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v9_reviewer1.tex"
DST = REPO / "paper" / "paper_v10_reviewer3.tex"

EDITS: list[tuple[str, str, str]] = []


def edit(label: str, old: str, new: str) -> None:
    EDITS.append((label, old, new))


# ---------------------------------------------------------------- R3.1 scale
edit(
    "R3.1a Methods: standardizing the number does not standardize the perturbation",
    "All other MR ORs enter without rescaling. The $d = 0.10$ threshold is applied uniformly across contrasts as a pragmatic choice; we identify threshold-sensitive families in the sensitivity analysis (\\S\\ref{sec:limitations}).",
    "All other MR ORs enter without rescaling. The $d = 0.10$ threshold is applied uniformly across contrasts. Standardizing a numerical estimate does not standardize the biological perturbation behind it: a per-SD shift in a circulating protein, a per-allele contrast at a coding variant, and a per-genotype contrast are different interventions, and equal Chinn $d$ values across them denote equal numbers rather than equal biological effects. The threshold acts as a magnitude filter within each family's own contrast, and for families near the boundary the classification depends on which contrast the source study reported as much as on the size of the underlying effect (\\S\\ref{sec:limitations}).",
)

# ------------------------------------------------------------ R3.4 direction
edit(
    "R3.4 Methods: new paragraph stating the rule is sign-blind",
    "\\textbf{MR classification.} Causal if (a) the confidence interval excludes the null \\emph{and} (b) $d_{\\text{MR}} \\geq 0.10$; null otherwise. Both criteria must be met---a statistically significant but negligible effect and a large but imprecise effect are both classified as null.",
    "\\textbf{MR classification.} Causal if (a) the confidence interval excludes the null \\emph{and} (b) $d_{\\text{MR}} \\geq 0.10$; null otherwise. Both criteria must be met---a statistically significant but negligible effect and a large but imprecise effect are both classified as null.\n\n"
    "\\textbf{Effect direction.} Equation~\\ref{eq:chinn} takes the absolute value of $\\ln(\\text{OR})$, and case-control SMDs enter as magnitudes, so the classification is blind to the sign of every estimate it reads. The rule asks whether each evidence type registers a non-trivial effect and never whether the two types agree on its direction. A sign comparison is unavailable from the assembled catalog because the OBS and GEN legs of a family are often oriented to different exposures: for IL-23-psoriasis the GEN leg is the protective \\emph{IL23R} R381Q coding variant (OR~0.62) while the OBS leg is elevated lesional IL-23, so opposite raw signs encode the same biology. Recovering direction would require re-coding every family to a common exposure orientation, which the catalog does not currently record. Directional concordance is a stronger criterion than the rule applies, and \\S\\ref{sec:limitations} states what implementing it would take.",
)

# ------------------------------------- R3.5 GWAS pooling / causal language
edit(
    "R3.5 Methods: name the two families whose GEN leg is associative",
    "The two evidence types in the classification are therefore OBS (observational and diagnostic studies) and GEN (MR and genetic association studies). Accuracy is reported by instrument type in \\S\\ref{sec:robustness}, which makes the exposure auditable: all eight misclassifications fall in the coding-variant and biomarker-GWAS classes, while every family instrumented by a \\emph{cis}-pQTL (8/8) or a polygenic score (5/5) is classified correctly.",
    "The two evidence types in the classification are therefore OBS (observational and diagnostic studies) and GEN (MR and genetic association studies). Accuracy is reported by instrument type in \\S\\ref{sec:robustness}, which makes the exposure auditable: all eight misclassifications fall in the coding-variant and biomarker-GWAS classes, while every family instrumented by a \\emph{cis}-pQTL (8/8) or a polygenic score (5/5) is classified correctly. Two scored families carry a GEN leg drawn from a genetic association rather than an MR causal estimate---Complement-GA (\\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---and the causal reading of the GEN leg applies to neither. Both are misclassified. Where this paper calls a pooled GEN signal causal, the term carries its MR sense for families instrumented by MR and an associational sense for these two.",
)

# ----------------------------------------- R3.2 Anti-CD20 threshold fragility
edit(
    "R3.2 Results: moderate the Anti-CD20-MS classification",
    "This family's MR $d = 0.103$ clears the threshold by 0.003; at $d = 0.099$ the classification would flip to discordance and predict failure for all four approved drugs. This threshold sensitivity is discussed in the Limitations (\\S\\ref{sec:limitations}).",
    "This family's MR $d = 0.103$ clears the threshold by 0.003; at $d = 0.099$ the classification would flip to discordance and predict failure for all four approved drugs. Nothing in the underlying evidence separates 0.103 from 0.099, so this family's classification is better read as undetermined than as a correct prediction, and the Limitations (\\S\\ref{sec:limitations}) treat it that way.\n\n"
    "Regulatory status and mechanistic support come apart here. Rituximab supplies the observational estimate used above and is widely used off-label in MS, with substantial clinical and registry evidence behind it, yet it carries no MS indication, while ocrelizumab, ofatumumab, and ublituximab do \\cite{brancati2021rituximab}. Health technology assessments of MS therapies in three European countries reach differing conclusions about therapeutic value for agents holding equivalent regulatory status \\cite{gozzo2023htams}. Approval is the outcome variable throughout this paper and indexes target validity only imperfectly: a family can carry strong mechanistic and clinical evidence for a compound that no sponsor takes through registration.",
)

# ------------------------------ R3.3 alternatives to a fixed numeric cutoff
edit(
    "R3.3 Discussion: new subsection on alternatives to a numeric threshold",
    "\\subsection{MR as a screening tool}",
    "\\subsection{Alternatives to a fixed numerical threshold}\n\n"
    "The $d = 0.10$ rule reduces each evidence leg to a magnitude and a significance test. Three instrument-level properties it ignores bear directly on whether an MR estimate speaks to a drug target: colocalization of the exposure and outcome association signals at the locus, which separates a shared causal variant from two variants in linkage disequilibrium; agreement in direction between the instrumented exposure and the pharmacological intervention; and target engagement, meaning that the instrument perturbs the protein the drug binds.\n\n"
    "Accuracy by instrument type (\\S\\ref{sec:robustness}) points the same way. Families instrumented by a \\emph{cis}-pQTL, where the instrument acts on the drug's proximal target protein, are classified correctly 8/8, and polygenic scores 5/5; coding variants reach 5/8 and biomarker GWAS 6/11, and all eight misclassifications fall in those two classes. Instrument-target proximity separates the correct classifications from the misses more cleanly than the effect-size threshold does, on cell sizes too small to test and confounded with domain. A rule keyed to colocalization and target engagement rather than to a Chinn $d$ cutoff is the natural next version of this framework; evaluating it requires colocalization statistics that the published MR literature reports unevenly, and assembling them for a family set of this size is a separate undertaking.\n\n"
    "\\subsection{MR as a screening tool}",
)

# ------------------------- Limitations: threshold paragraph, with fixes
edit(
    "R3.1b + internal: rewrite the mixed-contrasts limitation",
    "Universal rescaling to a common per-SD basis is infeasible: the conversion factors (SD of exposure per allele or per unit) are unavailable for most non-per-SD families. Only IL-6R is explicitly rescaled in this paper. The $d = 0.10$ threshold is therefore applied across incomparable scales---a pragmatic choice, since no universal rescaling exists.",
    "Universal rescaling to a common per-SD basis is infeasible: the conversion factors (SD of exposure per allele or per unit) are unavailable for most non-per-SD families, and IL-6R is the only family rescaled here (using $\\sigma = 0.34$~SD per allele). A single threshold across these contrasts compares numbers standing for different biological perturbations, so a family lying within a few thousandths of the boundary is sorted by which contrast its source study reported as much as by the size of the effect.",
)

edit(
    "Internal: reconcile the threshold-sensitive family list and correct two d values",
    "Anti-CD20-MS is threshold-sensitive and contrast-dependent: its MR $d = 0.103$ (per-SD circulating FCRL3 protein) clears by 0.003. At $d = 0.099$ the classification flips to discordance, misclassifying four approved drugs. At thresholds of $d = 0.08$ and $d = 0.12$, all other neuro/cardio classifications are unchanged (7/8 and 7/7 correct at both). Three additional families are threshold-sensitive at narrower ranges: IL-6R ($d = 0.083$) and CTLA-4-RA ($d = 0.083$) would flip from null to causal at a lower threshold; Uric acid ($d = 0.037$) is robustly null. The overall result is robust to perturbation but three individual classifications depend on the exact threshold.",
    "Anti-CD20-MS is threshold-sensitive and contrast-dependent: its MR $d = 0.103$ (per-SD circulating FCRL3 protein) clears by 0.003. At $d = 0.099$ the classification flips to discordance, misclassifying four approved drugs. At thresholds of $d = 0.08$ and $d = 0.12$, all other neuro and cardio classifications are unchanged (7/8 and 7/7 correct at both). Two further scored families lie close enough to the boundary to move: CTLA-4-RA ($d_{\\text{MR}} = 0.083$) becomes causal at a threshold of $0.08$, and JAK-STAT-RA ($d_{\\text{MR}} = 0.132$) becomes null at $0.14$. IL-6R sits at the same boundary (per-SD rescaled $d_{\\text{MR}} = 0.083$) and is unscored pending trial readout. Uric acid is robustly null on both legs ($d_{\\text{MR}} = 0.027$ from the pleiotropy-robust Egger estimate, $d_{\\text{OBS}} = 0.037$). Three of the 32 scored classifications therefore turn on the exact threshold while aggregate accuracy is stable across the tested range.",
)

edit(
    "Internal: JAK-STAT-RA d rounding in Robustness (0.131 -> 0.132)",
    "and JAK-STAT-RA ($d = 0.131$, flips at $d = 0.14$).",
    "and JAK-STAT-RA ($d = 0.132$, flips at $d = 0.14$).",
)

# ------------------------------------------- R3.6 zombie language moderation
edit(
    "R3.6a Methods taxonomy: drop 'statistical association, not a causal pathway'",
    "The observational signal reflects confounding or reverse causation; the mechanism is a statistical association, not a causal pathway. Drugs targeting zombies fail because there is nothing causal to intervene on.",
    "The observational signal is attributed to confounding or reverse causation, and drugs aimed at the mechanism are expected to fail because the evidence supplies no causal pathway to intervene on.",
)

edit(
    "R3.6b Unit of analysis: 'the pathway is non-causal' -> evidence pattern",
    "a ``zombie mechanism'' means the pathway is non-causal, regardless of which drug targets it",
    "a ``zombie mechanism'' names an evidence pattern attaching to the pathway, regardless of which drug targets it",
)

edit(
    "R3.6c Metabolic-AD: 'diagnoses confounding' -> consistent with confounding",
    "The 40-fold gap diagnoses confounding: shared risk factors (obesity, inflammation, vascular disease) explain the association without a causal metabolic pathway.",
    "The 40-fold gap is consistent with confounding by shared risk factors (obesity, inflammation, vascular disease), which would produce the observational association with no causal metabolic pathway.",
)

edit(
    "R3.6d two_modes: 'nothing causal to intervene on' softened",
    "Etiologic evidence alone diagnoses the failure, and drugs targeting the mechanism will fail because there is nothing causal to intervene on.",
    "Etiologic evidence alone flags the family, and drugs targeting the mechanism are expected to fail for want of a causal pathway to intervene on.",
)

edit(
    "R3.6e Oncology vitamin D: 'the mechanism was never real'",
    "This is a pure zombie: the mechanism was never real.",
    "The zombie pattern is present on both legs here: a stable observational signal against a null MR estimate in every cancer subtype tested.",
)

edit(
    "R3.6f Discussion: 'the target was never real'",
    "separates zombie mechanisms (confounded OBS, null MR---the target was never real) from",
    "separates zombie mechanisms (confounded OBS, null MR---no causal pathway is evidenced) from",
)

edit(
    "R3.6g Contributions: 'the target was never causal'",
    "The eight misclassified families split by MR $d$ into failures of non-mechanisms (null MR---the target was never causal) and failures of real mechanisms (causal MR---the target is real, the drug is insufficient or misaligned).",
    "The eight misclassified families split by MR $d$ into failures of targets lacking MR causal support and failures of targets carrying it (the target is real, and the drug is insufficient or misaligned).",
)

edit(
    "R3.6h Abstract conclusions: 'failures of non-mechanisms'",
    "Drug failures partition into two kinds---failures of non-mechanisms (null MR) and failures of real mechanisms (causal MR)---and the observational leg supplies",
    "Drug failures partition into two kinds---failures of targets lacking MR causal support and failures of targets carrying it---and the observational leg supplies",
)

# --------------------------------------------------------------------------
def main() -> int:
    text = SRC.read_text()
    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1

    failures = []
    for label, old, new in EDITS:
        count = text.count(old)
        if count != 1:
            failures.append((label, count))
    if failures:
        print("ABORT -- these targets did not match exactly once:\n", file=sys.stderr)
        for label, count in failures:
            print(f"  [{count} matches] {label}", file=sys.stderr)
        return 1

    for label, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"  applied: {label}")

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.")
    print(f"wrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
