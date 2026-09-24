"""v26d -> v26e: fixes from a [duh] check of every sentence added since v25 — errors first,
then tautologies, repeated qualifications and cadence. Reviewer-requested labels are kept where
the reviewer asked for them (abstract, failure-mode section, Conclusions, Methods).

Run:  uv run --no-project python paper/patches/patch_v26e_round4.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26d_round4.tex"
DST = HERE.parent / "paper_v26e_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


# ---- errors ----------------------------------------------------------------------------------
rep("eight further domains were added with the rule frozen.", "nine further domains were added with the rule frozen.")
rep(r"""The three boundary classes it relies on are post-hoc (Table~\ref{tab:provenance}), so the tree inherits their status.""",
    r"""Two of the three boundary classes it relies on are post-hoc and one was declared in advance (Table~\ref{tab:provenance}).""")
rep(r"""The boundary classes the tree relies on are post-hoc (Table~\ref{tab:provenance}).}""",
    r"""Two of the boundary classes the tree relies on are post-hoc (Table~\ref{tab:provenance}).}""")
rep(r"""Families where the fields disagree with the registered outcome are listed. A translation gap is read only where target engagement is recorded and the efficacy endpoint was not met.""",
    r"""Families where the fields disagree with the registered outcome are listed. The fields test the translation-gap reading, which requires recorded target engagement and an unmet efficacy endpoint.""")
rep(r"""The registered outcome variable is kept unchanged; the seven fields decompose it and do not redefine it.""",
    r"""The registered outcome variable is kept unchanged.""")
rep(r"""Each observational estimate, MR estimate and outcome used by the classifier was matched to a quoted passage in its source.""",
    r"""Each input value with a named source was compared against a quoted passage in that source.""")
rep(r"""The paragraphs below interpret individual families. They are the material the failure-mode reading (\S\ref{sec:two_modes}) is drawn from, and none of them enters an accuracy figure.

""", "")
rep(r"""the MR interval (CRP carries one; IL-1$\beta$-CVD does not), and drug outcome (no benefit; failed).""",
    r"""and the MR interval (CRP carries one; IL-1$\beta$-CVD does not).""")
rep(r"""IL-13, not IL-4, is the dominant lesional ligand. The boundary can be stated before a screen is run: soluble effector targets are expected to show null MR whatever the drug does, and risk-encoding loci are expected to show supportive MR.""",
    r"""IL-13, not IL-4, is the dominant lesional ligand.""")
rep(r"""MR finds no causal effect (OR~1.01, 95\% CI 0.96--1.06""", r"""MR is null (OR~1.01, 95\% CI 0.96--1.06""")
rep(r"""IGF-1 shows the translation-gap pattern: MR supports a causal effect on colorectal cancer risk (OR~1.22""",
    r"""IGF-1 shows the translation-gap pattern: MR is supportive for colorectal cancer risk (OR~1.22""")
rep(r"""MR supports a causal role for lifelong genetically determined vitamin~D status (OR~2.0, $d = 0.38$)""",
    r"""MR is supportive for lifelong genetically determined vitamin~D status (OR~2.0, $d = 0.38$)""")
rep(r"""The observational leg added no predictive information beyond MR status,""",
    r"""The observational leg added no information about outcomes beyond MR status,""")
rep(r"""exposure mismatches. Each demands a different pipeline response. Five finer-grained""",
    r"""exposure mismatches. Five finer-grained""")

# ---- tautologies -------------------------------------------------------------------------------
rep(r"""Every exclusion of a miss raises accuracy above the registered figure, and the only figure below it is the merge alone, which removes a hit. """, "")
rep(r"""The failure-mode assignments of the remaining misses are unchanged.""", "")
rep(r"""This two-way partition follows from the MR $d$ axis by construction: under a binary rule an MR-null miss is necessarily a clinical success and an MR-supportive miss necessarily a clinical failure. """, "")
rep(r"""show target engagement and a met endpoint (the drug worked),""", r"""show target engagement and a met endpoint,""")
rep(r"""Drugs whose family lacked classification received no classification.""", r"""Drugs in unclassified families were not scored.""")

# ---- repeated qualifications --------------------------------------------------------------------
rep(r"""The registered set is the primary analysis and no set is promoted on the basis of its accuracy. """, "")
rep(r"""; the sets differ by one to seven families, and none of the differences is a test.""", ".")
rep(r"""Both stored odds ratios fall below 1, so the rule returns concordance, although oriented to sclerostin the two legs oppose each other. The classification follows from sign-blindness (\S\ref{sec:accuracy}), not from agreement on direction.""",
    r"""Both stored odds ratios fall below 1, so the rule returns concordance, although oriented to sclerostin the two legs oppose each other (\S\ref{sec:accuracy}).""")
rep(r"""The instrument, the receptor variants the registration named, and the ligand the drug binds are three different perturbations of one pathway. """, "")
rep(r"""No registered classification changes; the states are reported for all 41 families in Supplementary Table~S2. The negligible-range state is not comparable across per-SD, per-unit and per-allele contrasts, and its range is the registered threshold, not a clinically validated margin.""",
    r"""The states are reported for all 41 families in Supplementary Table~S2.""")
rep(r"""The fields are a single coder's reading and the attribution column in particular is labeled as such.""", "")
rep(r"""and appear as separate families because the drug classes differ; merging them gives 23/31 (74.2\%).""",
    r"""and appear as separate families because the drug classes differ.""")
rep(r"""These accounts are preliminary generative hypotheses.""", "")

# ---- cadence -----------------------------------------------------------------------------------
rep(r"""Two features of the design bear on how these figures are read. The rule is blind""", r"""The rule is blind""")
rep(r"""it removes three misses and one duplicated hit, and it is reported after the registered count.""", r"""it removes three misses and one duplicated hit.""")
rep(r""" Whether the reading holds is a question for prospective readouts.""", "")
rep(r"""This provenance should calibrate how much weight each boundary class receives: the one pre-specified boundary was tested on one family; the post-hoc boundaries are hypotheses for future testing.""",
    r"""Mechanism-bypass was tested on one family; the post-hoc classes are untested.""")
rep(r"""The decision tree below is a hypothesis for prospective testing, not a validated tool, and nothing in this paper establishes that reading it before a Phase~III commitment would improve the decision.""",
    r"""The decision tree below is a hypothesis for prospective testing, not a validated tool.""")
rep(r"""are risk-encoding loci where the causal direction runs locus$\to$disease, which is what an MR instrument is built to capture.""",
    r"""are risk-encoding loci where the causal direction runs locus$\to$disease.""")
rep(r"""RCT $d = 0.04$ against etiologic $d > 0.80$ is the translation-gap pattern: the mechanism is involved in pathogenesis, and clearing amyloid at the stage of clinical disease does not reverse the downstream pathology; the reason is a hypothesis.""",
    r"""RCT $d = 0.04$ against etiologic $d > 0.80$ is the translation-gap pattern, consistent with the hypothesis that clearing amyloid at the stage of clinical disease does not reverse the downstream pathology.""")
rep(r"""are the questions the diagnostic reading raises, and the MR screen alone does not raise them.""",
    r"""are the questions the diagnostic reading raises.""")

# ---- checks --------------------------------------------------------------------------------------
for dead in ["eight further domains", "none of them enters an accuracy figure", "can be stated before a screen", "MR finds no causal effect",
             "MR supports a causal", "no predictive information", "demands a different pipeline", "(the drug worked)", "is a question for prospective"]:
    assert dead not in text, dead
text = re.sub(r"  +", " ", text)
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, words
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
