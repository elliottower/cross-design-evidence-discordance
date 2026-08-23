"""Build paper_v12_citation_fixes.tex from paper_v11_prospective_fix.tex.

Run:  uv run python paper/patches/patch_v12_citation_fixes.py

One edit. The observational source for Sclerostin-Fracture is named "Szulc 2014"
in the table footnote, but the resolved reference is Szulc et al., J Bone Miner
Res 28(4):855-864, 2013 (PMID 23165952 -- the same PMID the frozen classifier's
comment attaches to the 2014 label). The printed citation already renders as
2013 from the bibliography, so the inline year contradicted the reference list.

v11 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v11_prospective_fix.tex"
DST = REPO / "paper" / "paper_v12_citation_fixes.tex"

EDITS: list[tuple[str, str, str]] = [
    (
        "Sclerostin-Fracture footnote: the OBS source is Szulc 2013, not 2014",
        "$^\\text{m}$OBS: Szulc 2014 MINOS prospective cohort",
        "$^\\text{m}$OBS: Szulc 2013 MINOS prospective cohort",
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
    print(f"\n{len(EDITS)} edit(s) applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
