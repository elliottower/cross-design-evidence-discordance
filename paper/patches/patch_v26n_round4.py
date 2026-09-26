"""v26m -> v26n: Figure 2 caption panel b states what is known about the amyloid cascade rather than asserting
irreversibility, which Discussion 4.7 treats as a hypothesis.

Run:  uv run --no-project python paper/patches/patch_v26n_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26m_round4.tex"
DST = HERE.parent / "paper_v26n_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""but the downstream neurodegenerative cascade is irreversible by the time
of intervention.""", r"""but the downstream neurodegenerative cascade has not been shown to be reversible at the stage
of intervention.""")
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
