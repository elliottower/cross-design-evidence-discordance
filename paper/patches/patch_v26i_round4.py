"""v26h -> v26i: points from the external review of the v26h letters that held when checked: abstract no longer
names the five boundary classes; Table 8 note on Blood pressure and Triglycerides in the strict Phase III set;
the proximity clause left in Robustness; two class statements hedged; Lp(a) prediction vs classifier output.

Run:  uv run --no-project python paper/patches/patch_v26i_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26h_round4.tex"
DST = HERE.parent / "paper_v26i_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""The eight misses divide 5 and 3 by MR status; the direction is fixed by the rule, the mechanistic account of each side is not: translation gaps and exposure mismatch for the three MR-supportive failures, effector-neutralization, small-effect and mechanism-bypass for the five MR-null successes. These five boundary classes are preliminary generative hypotheses.""",
    r"""The eight misses divide 5 and 3 by MR status, a split fixed by the rule; five finer boundary classes read from them are preliminary generative hypotheses.""")
rep(r"""The registered set is the primary analysis. $^\ast$Set defined after the registered sets were scored.}""",
    r"""The registered set is the primary analysis. Blood pressure and Triglycerides leave the strict Phase~III set because the outcome codebook records their trial phase as mixed class; both classes contain Phase~III programs (PROGRESS; REDUCE-IT), and keeping them gives 19/27 (70.4\%). $^\ast$Set defined after the registered sets were scored.}""")
rep(r"""The misclassifications concentrate in families where the MR instrument indexes a biomarker or coding variant rather than the drug's proximal target protein.""",
    r"""The misclassifications concentrate in the coding-variant and biomarker-GWAS instrument classes.""")
rep(r"""accuracy exceeds 68\% in every configuration.""", r"""accuracy is at least 68\% in every configuration.""")
rep(r"""This asymmetry explains the effector-neutralization boundary""", r"""This asymmetry is the proposed account of the effector-neutralization boundary""")
rep(r"""Etiologic concordance for amyloid is robust; interventional discordance reveals a translation gap invisible to etiologic or MR evidence alone.""",
    r"""Etiologic concordance for amyloid is robust; the interventional discordance is read as a translation gap, which etiologic or MR evidence alone would not show.""")
rep(r"""Lp(a)HORIZON remains open.""",
    r"""Lp(a)HORIZON remains open; its readout tests the registered prediction (expected success), not the frozen classifier's output on its stored inputs, which is null concordance (Table~\ref{tab:cardio}, note~g).""")

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
