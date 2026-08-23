"""Build paper_v13_sclerostin_direction.tex from paper_v12_citation_fixes.tex.

Run:  uv run python paper/patches/patch_v13_sclerostin_direction.py

The Musculoskeletal paragraph described the SOST cis-MR estimate as showing that
"genetically lower sclerostin increases fracture risk (OR 0.59)". An odds ratio
of 0.59 is a reduction, so the sentence contradicted its own number, and it
contradicted the Effect direction paragraph added in v11, which reports the same
family as one whose two legs are oriented to opposite exposures.

The frozen classifier settles the direction: its stored MR input is scaled "per
0.09 g/cm2 BMD increase" (classify_families.py:447-450), a romosozumab-equivalent
contrast, on which sclerostin inhibition lowers fracture risk. The observational
leg runs the other way -- higher circulating sclerostin, fewer fractures -- which
is why the family scores as concordance only because the Chinn conversion drops
the sign.

Three edits: a label to reference, the corrected paragraph, and a header that
no longer asserts the verdict the paragraph withdraws.

v12 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v12_citation_fixes.tex"
DST = REPO / "paper" / "paper_v13_sclerostin_direction.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Label the rule subsection so the sclerostin paragraph can point at it",
        "\\subsection{Cross-design concordance rule}\n",
        "\\subsection{Cross-design concordance rule}\n\\label{sec:rule}\n",
    ),
    (
        "Musculoskeletal header: drop the verdict the paragraph no longer supports",
        "\\paragraph{Musculoskeletal: sclerostin as a clean concordance case.}",
        "\\paragraph{Musculoskeletal: sclerostin and fracture.}",
    ),
    (
        "Musculoskeletal paragraph: state the MR direction its own odds ratio encodes",
        "Higher circulating sclerostin associates with reduced fracture risk in the MINOS "
        "prospective cohort (HR 0.55; \\cite{szulc2014}). SOST cis-MR confirms the causal "
        "relationship: genetically lower sclerostin increases fracture risk (OR 0.59, "
        "CI 0.54--0.66, $d = 0.291$; \\cite{bovijn2020}). Concordance predicts success. "
        "Romosozumab (anti-sclerostin) reduces vertebral fractures by 48\\% (ARCH trial) "
        "and received FDA approval in 2019. The sclerostin family has tight "
        "instrument-target alignment---the MR instrument and the drug target the same "
        "protein---making it one of the cleanest concordance cases in the extension.",

        "Higher circulating sclerostin associates with reduced fracture risk in the MINOS "
        "prospective cohort (HR 0.55; \\cite{szulc2014}), a direction the source attributes "
        "to reverse causation. The \\emph{SOST} \\emph{cis}-MR estimate is scaled to a "
        "romosozumab-equivalent increase in bone mineral density, on which genetically "
        "proxied sclerostin inhibition lowers fracture risk (OR 0.59, CI 0.54--0.66, "
        "$d = 0.291$; \\cite{bovijn2020}). Both legs are non-trivial and both stored odds "
        "ratios fall below 1, so the rule returns concordance and predicts success. "
        "Romosozumab (anti-sclerostin) reduces vertebral fractures by 48\\% (ARCH trial) "
        "and received FDA approval in 2019. Instrument-target alignment is tight---the MR "
        "instrument and the drug target the same protein---but the two legs are oriented to "
        "opposite exposures, so the concordance follows from the sign-blindness of "
        "Equation~\\ref{eq:chinn} (\\S\\ref{sec:rule}) rather than from agreement about the "
        "direction of effect. A sign-aware rule would classify this family as qualitatively "
        "discordant and predict failure, which romosozumab's approval would contradict.",
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
    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
