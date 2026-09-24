"""v26e -> v26f: errors introduced by the v26e cuts (orphaned "Second,", domain count, boundary-class
provenance) and the cross-tabulation unmatched-family count, recounted by rerunning r1_minikel_cross_tab.

Run:  uv run --no-project python paper/patches/patch_v26f_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26e_round4.tex"
DST = HERE.parent / "paper_v26f_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


# ---- errors from the v26e cuts --------------------------------------------------------------
rep(r"""Second, the original 27 families""", r"""The original 27 families""")
rep(r"""and they are described in the most detail; nine further domains were added with the rule frozen.""",
    r"""and they are described in the most detail.""")
rep(r"""Two of the three boundary classes it relies on are post-hoc and one was declared in advance (Table~\ref{tab:provenance}).""",
    r"""Of the three boundary classes it relies on, mechanism-bypass was declared in advance, translation-gap has one post-hoc and one pre-specified instance, and effector-neutralization is post-hoc (Table~\ref{tab:provenance}).""")
rep(r"""Two of the boundary classes the tree relies on are post-hoc (Table~\ref{tab:provenance}).}""",
    r"""Table~\ref{tab:provenance} gives the provenance of each boundary class.}""")
rep(r"""Mechanism-bypass was tested on one family; the post-hoc classes are untested.""",
    r"""Mechanism-bypass and translation-gap were each tested on one family declared in advance (Serotonin-MDD, Complement-GA); the other three classes are untested.""")
rep(r"""The 10 extension families were declared blind and are the only families protected against this""",
    r"""The 10 scored extension families were declared blind and are the only scored families protected against this""")

# ---- A9: cross-tabulation counts and mapping commit ----------------------------------------------
rep(r"""Fifteen families were unmatchable (6 polygenic, 9 with gene targets absent from the Minikel dataset).""",
    r"""Fifteen families were unmatched: five polygenic, six whose gene target is absent from the dataset, and four whose gene appears only under other indications (JAK-STAT-RA, IGF1-CRC, IL6-MDD, Sclerostin-Fracture).""")
rep(r"""We matched 17 of our 32 scored families to the \citet{minikel2024} dataset by gene target and indication""",
    r"""We matched 17 of our 32 scored families to the \citet{minikel2024} dataset, at any phase, by gene target and indication""")
rep(r"""in \S\ref{sec:robustness} (commit \texttt{4b0a652}).""",
    r"""in \S\ref{sec:robustness} (commit \texttt{22dbc7f}; unchanged at \texttt{4b0a652}, the commit Amendment~5 names).""")

# ---- checks --------------------------------------------------------------------------------------
for dead in ["Second, the original", "nine further domains", "the post-hoc classes are untested", "6 polygenic, 9 with"]:
    assert dead not in text, dead
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
