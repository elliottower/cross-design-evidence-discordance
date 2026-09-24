"""v26f -> v26g: points from the external review of v26f that were checked against the manuscript and hold:
target-engagement caption, cis-pQTL proximity clause, Lp(a) rescaling, robustness claim, "predicts" in the abstract,
author contributions, IL6-MDD interval clause, circularity sentence, boundary-class hedges, neuro family count,
section-sign marker replaced by a double bar, one long sentence split.

Run:  uv run --no-project python paper/patches/patch_v26g_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26f_round4.tex"
DST = HERE.parent / "paper_v26g_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


# ---- contradictions -------------------------------------------------------------------------
rep(r"""No miss has a recorded target-engagement measure, so the translation-gap class rests on the efficacy readout alone.}""",
    r"""No MR-supportive miss has a recorded target-engagement measure, so the translation-gap class rests on the efficacy readout alone.}""")
rep(r"""Every family instrumented by a \emph{cis}-pQTL, where the instrument acts on the drug's proximal target protein, or by a polygenic score is classified correctly""",
    r"""Every family instrumented by a \emph{cis}-pQTL or by a polygenic score is classified correctly""")
rep(r"""Instrument-target proximity separates the correct classifications from the misses more cleanly""",
    r"""Instrument type separates the correct classifications from the misses more cleanly""")
rep(r"""All other MR ORs enter without rescaling.""",
    r"""The Lp(a) MR estimate, reported per 10~mg/dL, is rescaled to the observational per-SD contrast (Table~\ref{tab:cardio}, note~g). All other MR ORs enter without rescaling.""")
rep(r"""which places the family in the genetic-only cell.""",
    r"""which places the family in the genetic-only cell. The frozen classifier stores the per-10~mg/dL estimate and returns null concordance for this family (Table~\ref{tab:cardio}, note~g).""")
rep(r"""and a 28-family sensitivity analysis show that the result is not driven by threshold choice, any single domain, or family-definition decisions.""",
    r"""and a 28-family sensitivity analysis. Accuracy is 24--25/32 across the a priori threshold range and 68--80\% with any one domain removed; across the registered analysis-set table it runs from 17/26 to 23/28 (Table~\ref{tab:sets}).""")
rep(r"""Mendelian randomization (MR) evidence predicts drug success, but""",
    r"""Mendelian randomization (MR) evidence is associated with drug success, but""")
rep(r"""the MR screen alone cannot explain why""", r"""MR alone cannot explain why""")
rep(r"""designed and implemented the classification rule, performed and verified all analyses""",
    r"""designed the classification rule, directed its implementation, ran and verified all analyses""")
rep(r"""($d = 0.005$ and $d = 0.013$, the second with its whole interval below 0.10)""",
    r"""($d = 0.005$ and $d = 0.013$, each with its whole interval below 0.10)""")
rep(r"""claims across 24 mechanism families spanning AD and MS.""",
    r"""claims across 24 mechanism families spanning AD and MS, 9 of which have both observational and MR evidence.""")
rep(r"""bringing the total to 41 mechanism families""", r"""bringing the classified total to 41 mechanism families""")

# ---- claims stronger than the design supports ---------------------------------------------------
rep(r"""Etiologic evidence is independent of drug outcomes by construction: neither cohort studies nor MR analyses are causally downstream of whether a drug was approved, so""",
    r"""Etiologic evidence is not computed from drug outcomes: neither cohort studies nor MR analyses use whether a drug was approved, so""")
rep(r"""Our analysis supplies a mechanistic account for MR-null successes""", r"""The misses suggest a mechanistic account for MR-null successes""")
rep(r"""it is likely an effector.""", r"""the hypothesis classes it as an effector.""")
rep(r"""none exactly, and about one in six of the uncovered pairs""", r"""none exactly. About one in six of the uncovered pairs""")

# ---- marker: the section sign also marks section references ----------------------------------------
rep(r"""$^\S$""", r"""$^\|$""", count=19)

# ---- checks --------------------------------------------------------------------------------------
for dead in ["evidence predicts drug success", "proximal target protein, or by", "$^\\S$", "the second with its whole interval"]:
    assert dead not in text, dead
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
