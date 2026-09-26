"""v26i -> v26j: Data Availability cites the version DOI of the Zenodo release made from tag frontiers-revision-4.

Run:  uv run --no-project python paper/patches/patch_v26j_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26i_round4.tex"
DST = HERE.parent / "paper_v26j_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""zenodo.21227353""", r"""zenodo.22945779""")

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
