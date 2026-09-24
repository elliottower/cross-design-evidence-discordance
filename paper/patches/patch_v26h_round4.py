"""v26g -> v26h: AI-use statement brought up to date (Claude Opus 5.5; Claude Code through 2.1.281), and the
Zenodo DOI in Data Availability changed from the v1 version DOI to the concept DOI, which resolves to the latest version.

Run:  uv run --no-project python paper/patches/patch_v26h_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26g_round4.tex"
DST = HERE.parent / "paper_v26h_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""versions 2.1.207 to 2.1.280, running the models Claude Opus 4.6, Claude Opus 5, Claude Fable 5 and Claude Fable 5.1)""",
    r"""versions 2.1.207 to 2.1.281, running the models Claude Opus 4.6, Claude Opus 5, Claude Opus 5.5, Claude Fable 5 and Claude Fable 5.1)""")
rep(r"""zenodo.21227354""", r"""zenodo.21227353""")

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
