"""v26j -> v26k: the Anti-CD20-MS observational cell prints the value the classifier used (OR 2.23, d = 0.442), as
every other marked cell does; the source's HR 0.14 stays in the case narrative and in Appendix A.

Run:  uv run --no-project python paper/patches/patch_v26k_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26j_round4.tex"
DST = HERE.parent / "paper_v26k_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""Anti-CD20-MS & 0.103 & Yes & 1.084$^\|$ & Non-triv.""", r"""Anti-CD20-MS & 0.103 & Yes & 0.442$^\|$ & Non-triv.""")
rep(r"""Anti-CD20-MS & 1.08 & 0.103 & 0.20 & --- (success) \\""", r"""Anti-CD20-MS & 0.44 & 0.103 & 0.20 & --- (success) \\""")
rep(r"""the source reports HR 0.14 (0.05--0.39), the value printed in the tables &""", r"""the source reports HR 0.14 (0.05--0.39) &""")

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
