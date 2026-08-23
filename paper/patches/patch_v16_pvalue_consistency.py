"""Build paper_v16_pvalue_consistency.tex from paper_v15_zeus_readout.tex.

Run:  uv run python paper/patches/patch_v16_pvalue_consistency.py

Two edits, both found by reviews/verification/verify_v15_numbers.py.

The extension tier's p-value is corrected in Limitations. Reviewer 1's point 9
asked for the accuracy p-values to be rechecked and the test named; v9 corrected
the abstract and the Results and left this sentence carrying the submitted
value, so v15 printed p = 0.38 in two places and p = 0.17 in a third for the
same test. The one-sided exact binomial on 6/10 against 50% is 0.3770. Nothing
moves: the extension tier was described as not reaching significance under
either value.

The accounting caption is amended because IL-6R is counted in the Pending
column, which the caption defined as no Phase III readout, while the prospective
paragraph now reports that ZEUS read out. The column is a denominator device and
every denominator is fixed before the readout, so the caption says what Pending
counts rather than moving the family.

v15 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v15_zeus_readout.tex"
DST = REPO / "paper" / "paper_v16_pvalue_consistency.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Limitations, extension provenance: the p-value the abstract already carries",
        r"(one-sided binomial $p = 0.17$ against chance)",
        r"(one-sided exact binomial $p = 0.38$ against chance)",
    ),
    (
        "Accounting caption: what the Pending column counts, now that IL-6R has read out",
        r"``Pending'' = no Phase~III readout;",
        r"``Pending'' = no Phase~III readout when the scored set was fixed; IL-6R has "
        r"since read out (\S\ref{par:prospective}) and remains unscored;",
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

    assert "$p = 0.17$" not in text, "the stale extension p-value survived"
    assert text.count("$p = 0.38$") == 3, "the corrected value should now stand in three places"
    for fixed in ("24/32", "18/22", "6/10", "27 mechanism families"):
        assert fixed in text, f"a denominator changed: {fixed!r}"
    assert text.count("novonordisk2026zeus") == 2, "the ZEUS citation should be untouched"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
