"""Build paper_v11_prospective_fix.tex from paper_v10_reviewer3.tex.

Run:  uv run python paper/patches/patch_v11_prospective_fix.py

Corrects the two prospective predictions, the IL-6R and Lp(a) table rows, the
Anti-CD20-MS margin and flip point, the Data Availability pin, and adds the
Sclerostin-Fracture directional case. v10 is not modified.

Sources for every number changed here:
  PREREGISTRATION.md:169-193      the two registered predictions
  paper/reference/classify_families.py   the frozen rule and its stored inputs
  paper/submission/supplementary/cross_design_classification_all_41_families.csv
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v10_reviewer3.tex"
DST = REPO / "paper" / "paper_v11_prospective_fix.tex"

EDITS: list[tuple[str, str, str]] = []


def edit(label: str, old: str, new: str) -> None:
    EDITS.append((label, old, new))


# ------------------------------------------------ tab:cardio, the two rows
edit(
    "Lp(a) row: Concordant -> Genetic-only (OBS d = 0.067 is trivial)",
    "Lp(a)$^\\text{g}$ & 1.13 & 0.94 (0.93--0.95) & Causal & \\emph{Pending} & Concordant & --- \\\\",
    "Lp(a)$^\\text{g}$ & 1.13 & 0.94 (0.93--0.95) & Causal & \\emph{Pending} & Genetic-only & --- \\\\",
)

edit(
    "IL-6R row: Causal/Concordant -> Null/Qual. disc. at the d = 0.10 threshold",
    "IL-6R$^\\text{h}$ & 1.25 & 0.95 (0.93--0.97) & Causal & \\emph{Pending} & Concordant & --- \\\\",
    "IL-6R$^\\text{h}$ & 1.25 & 0.95 (0.93--0.97) & Null & \\emph{Pending} & Qual.\\ disc. & --- \\\\",
)

edit(
    "Footnote g: state the per-SD rescaling and what the frozen classifier stores",
    "$^\\text{g}$OBS per 1 SD (ERFC); MR per 10 mg/dL lower \\cite{burgess2018lpa}.",
    "$^\\text{g}$OBS per 1 SD (ERFC); MR per 10 mg/dL lower \\cite{burgess2018lpa}. "
    "On the tabulated per-10 mg/dL contrast the Chinn $d$ is 0.034. Rescaling the MR estimate "
    "to the observational contrast (1~SD $\\approx$ 36 mg/dL) gives OR~0.80 per SD and "
    "$d = 0.123$, and the classification uses that rescaling, as registered. The frozen "
    "classifier stores the per-10 mg/dL estimate and applies rescaling only to IL-6R, so run "
    "on its stored inputs it returns null concordance for this family. Lp(a) has a pending "
    "trial outcome and enters no reported accuracy figure.",
)

edit(
    "Footnote h: correct the sigma bound, cite Swerdlow, state the resulting classification",
    "The tabulated OR~0.95 is the per-allele estimate, on which the Chinn $d$ is 0.028; "
    "classification uses the per-SD rescaling described in Materials and Methods, which "
    "clears $d = 0.10$ for any per-allele exposure SD $\\sigma \\le 0.283$.",
    "The tabulated OR~0.95 is the per-allele estimate, on which the Chinn $d$ is 0.028. "
    "The \\emph{IL6R} Asp358Ala variant shifts soluble IL-6R by $\\sigma = 0.34$~SD per allele "
    "\\cite{interleukin2012}, so the per-SD rescaling of Materials and Methods gives OR~0.86 and "
    "$d = 0.083$, below the $d = 0.10$ threshold. The MR signal is therefore null under the "
    "two-criterion rule and the family qualitatively discordant; at a threshold of $d = 0.08$ "
    "both would reverse.",
)

# ------------------------------------------ the prospective predictions paragraph
edit(
    "Prospective predictions: report what the preregistration actually registered",
    "Two cardiometabolic families have causal MR signals and Phase~III trials approaching "
    "readout. Lp(a)-lowering via pelacarsen (Lp(a)HORIZON, NCT04023552; $n = 8{,}323$; "
    "primary completion June 2026; topline results expected H2 2026) and IL-6 pathway "
    "inhibition via ziltivekimab (ZEUS, NCT05021835; $n = 6{,}376$; primary completion "
    "June 2026; readout expected Q3 2026) are classified as ``Approve'' by the frozen rule. "
    "A caveat: the IL-6R MR instrument uses variants in \\emph{IL6R}, while ziltivekimab "
    "targets the IL-6 ligand---the instrument and drug act on the same pathway but at "
    "different nodes. These predictions were registered before trial readout (frozen rule "
    "commit \\texttt{bf7f175}, July 2026). If either trial fails, the classification becomes "
    "a miss, the boundary class taxonomy should be updated, and the failure mode (translation "
    "gap, exposure mismatch, or a new category) should be characterized.",

    "Two cardiometabolic families have Phase~III trials approaching readout, and the "
    "preregistration fixed a prediction for each before any readout (frozen rule commit "
    "\\texttt{bf7f175}, July 2026).\n\n"
    "Lp(a)-lowering via pelacarsen (Lp(a)HORIZON, NCT04023552; $n = 8{,}323$; primary "
    "completion June 2026; topline expected H2 2026) is registered as a predicted success. "
    "The observational effect is trivial ($d_{\\text{OBS}} = 0.067$) and the MR effect, "
    "rescaled to the observational contrast, is causal ($d_{\\text{MR}} = 0.123$), which "
    "places the family in the genetic-only cell.\n\n"
    "IL-6 pathway inhibition via ziltivekimab (ZEUS, NCT05021835; $n = 6{,}376$; primary "
    "completion June 2026; readout expected Q3 2026) is the registered boundary case, and "
    "two predictions were fixed for it rather than one. The rescaled MR effect is "
    "$d_{\\text{MR}} = 0.083$. At the $d = 0.10$ threshold used throughout this paper the MR "
    "signal is null, the family is qualitatively discordant, and the registered prediction is "
    "failure. At a threshold of $d = 0.08$ the MR signal is causal, the family is concordant, "
    "and the registered prediction is success. ZEUS discriminates between the two thresholds: "
    "a positive trial favors 0.08, a negative trial favors 0.10. A caveat on "
    "instrument-target alignment applies under either reading---the MR instrument uses "
    "variants in \\emph{IL6R} while ziltivekimab targets the IL-6 ligand, so the instrument "
    "and the drug act on the same pathway at different nodes.\n\n"
    "If Lp(a)HORIZON fails, the genetic-only cell should predict ambiguity rather than "
    "success, and the failure mode (translation gap, exposure mismatch, or a new category) "
    "should be characterized.",
)

# --------------------------------------- Anti-CD20-MS margin and flip point
edit(
    "Results: Anti-CD20-MS margin is 0.0027, and the flip is counterfactual",
    "This family's MR $d = 0.103$ clears the threshold by 0.003; at $d = 0.099$ the "
    "classification would flip to discordance and predict failure for all four approved "
    "drugs. Nothing in the underlying evidence separates 0.103 from 0.099, so this family's "
    "classification is better read as undetermined than as a correct prediction, and the "
    "Limitations (\\S\\ref{sec:limitations}) treat it that way.",
    "This family's MR $d = 0.1027$ clears the threshold by 0.0027; had the estimate been "
    "0.099 the classification would flip to discordance and predict failure for all four "
    "approved drugs. Nothing in the underlying evidence separates 0.1027 from 0.099, so this "
    "family's classification is better read as undetermined than as a correct prediction, and "
    "the Limitations (\\S\\ref{sec:limitations}) treat it that way.",
)

edit(
    "Robustness: the flip point is 0.103, not 0.11",
    "Above $d = 0.11$, Anti-CD20-MS flips to discordant (predicting failure for four approved "
    "drugs), and accuracy degrades monotonically. Three families are threshold-sensitive: "
    "Anti-CD20-MS ($d = 0.103$, flips at $d = 0.11$), CTLA-4-RA ($d = 0.083$, flips at "
    "$d \\leq 0.08$), and JAK-STAT-RA ($d = 0.132$, flips at $d = 0.14$).",
    "Above $d = 0.1027$, Anti-CD20-MS flips to discordant (predicting failure for four "
    "approved drugs), and accuracy degrades monotonically. Three families are "
    "threshold-sensitive: Anti-CD20-MS ($d = 0.1027$, flips just above its own value), "
    "CTLA-4-RA ($d = 0.083$, flips at $d \\leq 0.08$), and JAK-STAT-RA ($d = 0.132$, flips at "
    "$d = 0.14$).",
)

edit(
    "Limitations: same margin and counterfactual wording",
    "its MR $d = 0.103$ (per-SD circulating FCRL3 protein) clears by 0.003. At $d = 0.099$ the "
    "classification flips to discordance, misclassifying four approved drugs.",
    "its MR $d = 0.1027$ (per-SD circulating FCRL3 protein) clears by 0.0027. At any threshold "
    "above 0.1027 the classification flips to discordance, misclassifying four approved drugs.",
)

# ----------------------------------------- the directional case (R3.4 support)
edit(
    "Effect direction: add the family where sign-blindness changes the score",
    "Recovering direction would require re-coding every family to a common exposure "
    "orientation, which the catalog does not currently record.",
    "Sclerostin-Fracture shows what the omission costs. The observational leg is a prospective "
    "cohort in which higher circulating sclerostin accompanies \\emph{fewer} fractures "
    "(HR~0.55, highest vs.\\ lowest tertile), a direction the source attributes to reverse "
    "causation; the MR leg is a \\emph{SOST} \\emph{cis}-pQTL estimate in which sclerostin "
    "inhibition also lowers fracture risk (OR~0.59). Both stored odds ratios fall below 1, so "
    "the family reads as directionally consistent and scores as concordance, while oriented to "
    "sclerostin the two legs oppose each other. Recovering direction would require re-coding "
    "every family to a common exposure orientation, which the catalog does not currently "
    "record.",
)

# ----------------------------------------------------- Data Availability pin
edit(
    "Data Availability: the 41-family dataset is not in commit bf7f175",
    "The deterministic classifier (\\texttt{classify\\_families.py}), robustness analysis code "
    "(\\texttt{robustness\\_analyses.py}), and the complete classification dataset (41 families "
    "with effect sizes, CIs, and sources) are available at "
    "\\url{https://github.com/elliottower/cross-design-evidence-discordance} (commit "
    "\\texttt{bf7f175}) with a permanent archive at Zenodo",
    "The deterministic classifier (\\texttt{classify\\_families.py}, frozen at commit "
    "\\texttt{bf7f175}), the robustness analysis code (\\texttt{robustness\\_analyses.py}), and "
    "the complete classification dataset (41 families with effect sizes, CIs, and sources) are "
    "available at \\url{https://github.com/elliottower/cross-design-evidence-discordance} "
    "with a permanent archive at Zenodo",
)


def main() -> int:
    text = SRC.read_text()
    failures = [(label, text.count(old)) for label, old, _ in EDITS if text.count(old) != 1]
    if failures:
        print("ABORT -- these targets did not match exactly once:\n", file=sys.stderr)
        for label, count in failures:
            print(f"  [{count} matches] {label}", file=sys.stderr)
        return 1
    for label, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"  applied: {label}")
    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
