r"""Build paper_v20_sigma_provenance.tex from paper_v19_checked_bibliography.tex.

Run:  uv run python paper/patches/patch_v20_sigma_provenance_and_data_pin.py

Three edits closing the two defects that block the revision.

1+2. The rescaling constant sigma = 0.34 SD per allele. v19 attributes it to
   \cite{interleukin2012} (Swerdlow et al., Lancet 379:1214-1224). The value is
   not in that paper. Its main-text table gives the per-allele effect on soluble
   IL-6R as 14.87 ng/mL (13.07-16.66); its figure 2 legend gives the standardized
   figure as 0.75 (0.59-0.91). The full text (PMC3316968) and the 6,077-line
   appendix were read; 0.34 appears once, in an unlabeled numeric column. The
   preregistration attributes it to "Swerdlow et al. 2012 Int J Epidemiol", which
   does not exist.

   sigma = 0.34 stays. It is a frozen classifier input
   (classify_families.py:184, "sd_per_allele": 0.34) from which both registered
   IL-6R predictions were computed; substituting a different constant after the
   ZEUS readout would be changing a registered input to fit an outcome. The
   footnote instead states sigma as the registered value it is, reports what the
   cited source gives, and carries the arithmetic at both. The classification is
   MR-null either way -- d = 0.083 at 0.34, d = 0.038 at 0.75, both under the
   0.10 floor -- so no reported figure moves. What does depend on the constant is
   the registered d = 0.08 branch, which exists only at sigma = 0.34, and the
   Limitations say so.

3. Data availability. The statement points at a branch URL. The classification
   dataset is not in commit bf7f175, which the statement names for the classifier.
   The dataset is named by filename and the repository pinned to a tag.

No headline number moves. 24/32, 18/22, 6/10 and both sensitivities are unchanged.

v19 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v19_checked_bibliography.tex"
DST = REPO / "paper" / "paper_v20_sigma_provenance.tex"

TAG = "frontiers-revision-1"

EDITS: list[tuple[str, str, str]] = [
    (
        "Table footnote h: sigma stated as the registered input, with what the "
        "cited source actually reports and the arithmetic at both values",
        "The \\emph{IL6R} Asp358Ala variant shifts soluble IL-6R by "
        "$\\sigma = 0.34$~SD per allele \\cite{interleukin2012}, so the per-SD "
        "rescaling of Materials and Methods gives OR~0.86 and $d = 0.083$, below "
        "the $d = 0.10$ threshold. The MR signal is therefore null under the "
        "two-criterion rule and the family qualitatively discordant; at a "
        "threshold of $d = 0.08$ both would reverse.",

        "The preregistration fixes the \\emph{IL6R} Asp358Ala shift in soluble "
        "IL-6R at $\\sigma = 0.34$~SD per allele, and the per-SD rescaling of "
        "Materials and Methods gives OR~0.86 and $d = 0.083$, below the "
        "$d = 0.10$ threshold. \\citet{interleukin2012} gives that shift as "
        "14.87~ng/mL (13.07--16.66) per allele, standardized to 0.75 "
        "(0.59--0.91); at $\\sigma = 0.75$ the same rescaling gives OR~0.93 and "
        "$d = 0.038$. The MR signal is null under the two-criterion rule at "
        "either value and the family qualitatively discordant; the registered "
        "branch at $d = 0.08$ exists only at $\\sigma = 0.34$ "
        "(\\S\\ref{sec:limitations}).",
    ),
    (
        "Limitations, threshold sensitivity: the provenance of the conversion "
        "factor and what depends on it",
        "A single threshold across these contrasts compares numbers standing for "
        "different biological perturbations, so a family lying within a few "
        "thousandths of the boundary is sorted by which contrast its source study "
        "reported as much as by the size of the effect.",

        "A single threshold across these contrasts compares numbers standing for "
        "different biological perturbations, so a family lying within a few "
        "thousandths of the boundary is sorted by which contrast its source study "
        "reported as much as by the size of the effect. The IL-6R conversion "
        "factor is itself a registered input, and its provenance is weaker than "
        "the estimate it rescales: the preregistration fixes $\\sigma = 0.34$~SD "
        "per allele and attributes it to a source that could not be located, "
        "while \\citet{interleukin2012}, from which the MR estimate is taken, "
        "gives the per-allele shift in soluble IL-6R as 14.87~ng/mL "
        "(13.07--16.66), standardized to 0.75 (0.59--0.91). The family is MR-null "
        "at either value, so no reported figure depends on the choice; the "
        "registered $d = 0.08$ branch, against which the ZEUS readout "
        "discriminates, exists only at $\\sigma = 0.34$.",
    ),
    (
        "Data availability: the dataset named by filename, the repository pinned "
        "to a tag rather than a branch",
        "the complete classification dataset (41 families with effect sizes, CIs, "
        "and sources) are available at "
        "\\url{https://github.com/elliottower/cross-design-evidence-discordance} "
        "with a permanent archive at Zenodo",

        "the complete classification dataset (41 families with effect sizes, CIs, "
        "and sources; \\texttt{cross\\_design\\_classification\\_all\\_41\\_"
        "families\\_v2.csv}) are available at "
        "\\url{https://github.com/elliottower/cross-design-evidence-discordance} "
        f"at tag \\texttt{{{TAG}}}, the repository state underlying this "
        "revision, with a permanent archive at Zenodo",
    ),
]


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

    # No reported figure may move. The two sensitivities are printed beside the
    # headline numbers and must survive with them.
    for figure in ("24/32", "18/22", "6/10", "23/32", "23/31", "25/34",
                   "41 mechanism families", "\\texttt{bf7f175}"):
        assert figure in text, f"{figure} lost"

    # The registered constant stays, and the sourced one is now stated beside it.
    # Twice in footnote h (the registered value, the branch condition) and three
    # times in Limitations (the existing parenthetical, the provenance sentence,
    # the branch condition).
    assert text.count("\\sigma = 0.34") == 5, \
        f"sigma = 0.34 appears {text.count(chr(92)+chr(92))} times, expected 5"
    assert text.count("0.75 (0.59--0.91)") == 2, "the sourced standardized figure " \
        "belongs in both the footnote and the Limitations"
    assert "$d = 0.038$" in text, "the arithmetic at the sourced value is missing"
    assert text.count(TAG) == 1, "the tag should be named once, in Data Availability"
    assert "families\\_v2.csv" in text, "the dataset filename is missing"

    # A paper states what is true and never narrates its own revision history.
    # Counted against the source, not in absolute terms: v19 already says drug
    # outcomes "are no longer independent" of the stage-2 classification, which is
    # a statement about the design and not about this paper's own history.
    source = SRC.read_text()
    for tell in ("we previously", "an earlier version", "no longer", "we withdraw",
                 "had described", "is withdrawn", "we retract", "previously reported"):
        added = text.lower().count(tell) - source.lower().count(tell)
        assert added == 0, f"the edits introduced lab-notebook prose: {tell!r}"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
