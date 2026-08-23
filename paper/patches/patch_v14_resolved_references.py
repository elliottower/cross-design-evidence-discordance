"""Build paper_v14_resolved_references.tex from paper_v13_sclerostin_direction.tex.

Run:  uv run python paper/patches/patch_v14_resolved_references.py

Two changes, both traceable to audit_bibliography.py.

The bibliography moves to references_v2_resolved.bib, in which author lists,
years, volumes, and page ranges are taken from the record each DOI or PMID
resolves to. Twenty-three entries differed from their own identifier; four
carried an author list belonging to nobody on the paper, and one carried a PMID
for an unrelated neurology article.

The SGLT2-HF confidence interval is corrected. The source reports OR 0.44, 95%
CI 0.26 to 0.76, P = 0.003; the manuscript printed 0.22--0.88. Chinn d is a
function of the point estimate alone, so d = 0.452, the Causal verdict, the
family's Concordant class, and the 24/32 accuracy are all unchanged -- both
intervals exclude the null. The printed interval was wrong on its own terms.

v13 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v13_sclerostin_direction.tex"
DST = REPO / "paper" / "paper_v14_resolved_references.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Point the bibliography at the identifier-resolved reference file",
        "\\bibliography{references}",
        "\\bibliography{references_v2_resolved}",
    ),
    (
        "Table 2, SGLT2-HF row: confidence interval as the source reports it",
        "0.44 (0.22--0.88)",
        "0.44 (0.26--0.76)",
    ),
    (
        "Metabolic paragraph: confidence interval as the source reports it",
        "OR~0.44, 95\\%~CI 0.22--0.88",
        "OR~0.44, 95\\%~CI 0.26--0.76",
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
    assert "0.22--0.88" not in text, "an uncorrected interval survived"
    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
