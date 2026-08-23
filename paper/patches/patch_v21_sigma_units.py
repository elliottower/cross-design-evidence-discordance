r"""Build paper_v21_sigma_units.tex from paper_v20_sigma_provenance.tex.

Run:  uv run python paper/patches/patch_v21_sigma_units.py

v20 states that \citet{interleukin2012} gives the per-allele shift in soluble
IL-6R as 14.87 ng/mL, "standardized to 0.75 (0.59--0.91)". Reading the source
settles that it does not say that. The summary-effects table gives 14.87 ng/mL
(13.07 to 16.66) per allele. The Figure 2 legend gives, for the same contrast:

  "standardised mean differences were 0.75 (95% CI 0.59-0.91) ng/mL per minor
   allele for rs7529229, and 93.67 (95% CI 90.27-97.06) ng/mL for tocilizumab
   8 mg/kg versus placebo"

-- a figure called a standardized mean difference and printed in ng/mL, a unit
that cannot belong to one. The source is inconsistent at the exact point the
manuscript leans on it, so v20 presents as settled something its own source
leaves open.

Two edits, both reporting what the source prints instead of resolving it. No
number moves: the family is MR-null at sigma = 0.34 and at sigma = 0.75, is
unscored either way, and enters no accuracy figure.

Checked by reviews/verification/verify_sigma_source.py, which reads the source
over the network and fails if the manuscript states 0.75 without the unit label
the source attaches to it.

v20 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v20_sigma_provenance.tex"
DST = REPO / "paper" / "paper_v21_sigma_units.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Table footnote h: report the legend figure with the unit the source prints on it",
        "\\citet{interleukin2012} gives that shift as 14.87~ng/mL (13.07--16.66) per "
        "allele, standardized to 0.75 (0.59--0.91); at $\\sigma = 0.75$ the same "
        "rescaling gives OR~0.93 and $d = 0.038$.",
        "\\citet{interleukin2012} gives that shift as 14.87~ng/mL (13.07--16.66) per "
        "allele; its Figure~2 legend gives 0.75 (0.59--0.91) for the same contrast, "
        "described there as a standardized mean difference and printed in ng/mL. Read "
        "as an SD-unit figure, $\\sigma = 0.75$ gives OR~0.93 and $d = 0.038$ under the "
        "same rescaling.",
    ),
    (
        "Limitations: name both figures the source gives and where each appears",
        "gives the per-allele shift in soluble IL-6R as 14.87~ng/mL (13.07--16.66), "
        "standardized to 0.75 (0.59--0.91). The family is MR-null at either value, so "
        "no reported figure depends on the choice;",
        "gives the per-allele shift in soluble IL-6R as 14.87~ng/mL (13.07--16.66) in "
        "its summary table and 0.75 (0.59--0.91) in its Figure~2 legend, the second "
        "described there as a standardized mean difference and printed in ng/mL. The "
        "family is MR-null at $\\sigma = 0.34$ and at $\\sigma = 0.75$, so no reported "
        "figure depends on the choice;",
    ),
]


def main() -> int:
    source = SRC.read_text()
    text = source
    failures = [(label, text.count(old)) for label, old, _ in EDITS if text.count(old) != 1]
    if failures:
        print("ABORT -- these targets did not match exactly once:\n", file=sys.stderr)
        for label, count in failures:
            print(f"  [{count} matches] {label}", file=sys.stderr)
        return 1
    for label, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"  applied: {label}")

    for figure in ("24/32", "18/22", "6/10", "23/32", "23/31", "25/34",
                   "41 mechanism families", "\\texttt{bf7f175}",
                   "frontiers-revision-1", "families\\_v2.csv"):
        assert figure in text, f"{figure} lost"

    # The Limitations edit spells out both values where v20 wrote "either value",
    # which is one more occurrence of the registered constant and no fewer.
    assert text.count("\\sigma = 0.34") == source.count("\\sigma = 0.34") + 1, \
        "the count of the registered constant moved by something other than the edit"
    assert text.count("0.75 (0.59--0.91)") == 2, \
        "the legend figure belongs in both the footnote and the Limitations"
    assert text.count("$d = 0.038$") == 1, "the arithmetic at the legend value is missing"
    # Both places that give 0.75 must carry the unit the source prints on it.
    for chunk in text.split("0.75 (0.59--0.91)")[1:]:
        assert "ng/mL" in chunk[:400], "0.75 is stated without the source's unit label"
    assert "standardized to 0.75" not in text, "the superseded reading survived"

    # A paper states what is true and never narrates its own revision history.
    for tell in ("we previously", "an earlier version", "no longer", "we withdraw",
                 "had described", "is withdrawn", "we retract", "previously reported"):
        added = text.lower().count(tell) - source.lower().count(tell)
        assert added == 0, f"the edits introduced lab-notebook prose: {tell!r}"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
