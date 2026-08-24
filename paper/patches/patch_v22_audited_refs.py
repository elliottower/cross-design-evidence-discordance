"""Build paper_v22_audited_refs.tex from paper_v21_sigma_units.tex.

Run:  uv run python paper/patches/patch_v22_audited_refs.py

One edit. The bibliography moves to references_v7_audited.bib, where every entry
has been compared against the record its identifier resolves to
(reviews/verification/audit_bibliography.py). The change a reader sees is in two
reference-list lines: the ganitumab trial's issue number, corrected from 12 to
11, and its subtitle, restored.

No claim, statistic or citation key moves. v21 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v21_sigma_units.tex"
DST = REPO / "paper" / "paper_v22_audited_refs.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Bibliography: the audited bibliography",
        "\\bibliography{references_v6_checked}",
        "\\bibliography{references_v7_audited}",
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

    # Nothing but the bibliography pointer may move, so the two files must differ
    # by exactly the one line.
    source = SRC.read_text()
    differing = [i for i, (a, b) in enumerate(
        zip(source.splitlines(), text.splitlines())) if a != b]
    assert len(differing) == 1, f"{len(differing)} lines changed, expected 1"
    assert len(source.splitlines()) == len(text.splitlines()), "line count moved"
    for figure in ("24/32", "18/22", "6/10", "23/32", "23/31", "25/34",
                   "41 mechanism families", "\\sigma = 0.34",
                   "frontiers-revision-1", "families\\_v2.csv"):
        assert figure in text, f"{figure} lost"
    assert "references_v6_checked" not in text, "the superseded bibliography survived"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
