"""v26n -> v26o: Conclusions keep the boundary classes as hypotheses without stating their content (Reviewer 5):
¶2 frames them as proposed for prospective testing; ¶3 states the open questions for MR in general and the null-MR
exceptions as a count; §4.3 describes a null MR estimate as null.

Run:  uv run --no-project python paper/patches/patch_v26o_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26n_round4.tex"
DST = HERE.parent / "paper_v26o_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


rep(r"""are preliminary generative hypotheses on $n = 8$ and are not among the conclusions of this paper.""",
    r"""are preliminary generative hypotheses on $n = 8$, proposed for prospective testing.""")
rep(r"""A supportive MR signal does not guarantee success: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises. A null MR signal argues against a risk-encoding target, except where the drug's perturbation far exceeds the genetic one (Estrogen-BC) or the drug acts through a pathway the instrument does not index (Serotonin-MDD).""",
    r"""A supportive MR signal does not guarantee success: whether a target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation remain open questions for any MR-based classification. A null MR signal counts against a target but does not exclude clinical success, as the five null-MR families with approved drugs show.""")
rep(r"""When MR finds no causal pathway (OR~1.01 for T2D-AD)""", r"""When the MR estimate is null (OR~1.01 for T2D-AD)""")
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
