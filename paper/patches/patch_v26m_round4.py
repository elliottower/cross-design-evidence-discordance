"""v26l -> v26m: Figure 2 caption panel b restored to the v25 wording (which also removes a doubled "both");
the three original domains named in Introduction ¶5; §4.3 names the rule's output correctly.

Run:  uv run --no-project python paper/patches/patch_v26m_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26l_round4.tex"
DST = HERE.parent / "paper_v26m_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""both observational and genetic
evidence both support a causal role for the pathway (Amyloid-AD""", r"""both observational and genetic
evidence confirm the pathway is real (Amyloid-AD""")
rep(r"""tested it across three disease domains, and extended""",
    r"""tested it across three disease domains (neuroepidemiology, cardiometabolic and autoimmune disease), and extended""")
rep(r"""our rule would classify the same evidence as an MR-discordant mechanism and an expected failure, which matches the null trial results.""",
    r"""our rule would classify the same evidence as an expected failure, the pattern the paper calls an MR-discordant mechanism, which matches the null trial results.""")
assert "evidence both support" not in text
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
