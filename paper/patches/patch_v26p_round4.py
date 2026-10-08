"""v26o -> v26p: abstract to 350 words counted as plain text with its headings (the Frontiers portal count).

Run:  uv run --no-project python paper/patches/patch_v26p_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26o_round4.tex"
DST = HERE.parent / "paper_v26p_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""were preregistered before their corresponding outcomes were examined""", r"""were preregistered before their outcomes were examined""")
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
