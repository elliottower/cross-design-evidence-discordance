"""v26k -> v26l: readability pass on the abstract, Introduction, contributions and Conclusions, and the claim-level
fixes, all decided one by one by Elliot (writing_review_v26k/11_BATCH2_DECISIONS.md); Shapland 2024 and Shi 2025 cited.

Run:  uv run --no-project python paper/patches/patch_v26l_round4.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26k_round4.tex"
DST = HERE.parent / "paper_v26l_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


import re

# ---- abstract --------------------------------------------------------------------------------------
rep(r"""We tested a preregistered classification rule and, separately, read the families it misclassified for preliminary hypotheses about why it fails.""",
    r"""We tested a preregistered rule comparing observational and MR evidence against Phase~III outcomes and performed an exploratory analysis of the families it misclassified.""")
rep(r"""classified each family from the observational and MR evidence pattern.""",
    r"""classified each family from the observational and MR evidence pattern: a non-trivial observational association with null MR evidence was classified as an expected failure, and supportive MR evidence as an expected success.""")
mr = r"""MR-only and the cross-design rule produced identical classifications across all 32 scored families, because 31 of 32 have non-trivial observational support. """
rep(mr, "")
rep(r"""and not independent confirmation. A sensitivity analysis""", r"""and not independent confirmation. """ + mr + r"""A sensitivity analysis""")
rep(r"""excludes one indication-mismatched family and two association-only families and counts duplicated evidence once""",
    r"""excludes three families (one indication-mismatched, two association-only) and counts duplicated evidence once""")
rep(r"""The eight misses divide 5 and 3 by MR status, a split fixed by the rule; five finer boundary classes read from them are preliminary generative hypotheses.""",
    r"""The eight misclassified families split by MR status: five had null MR evidence yet an approved drug, and three had supportive MR evidence yet a failed drug.""")
rep(r"""Its contribution is diagnostic: the cross-design comparison generates mechanistic hypotheses about why the binary MR classification misses.""",
    r"""Its contribution is diagnostic: set against MR and trial evidence, it generates hypotheses about why an MR-based classification fails.""")

# ---- Introduction -----------------------------------------------------------------------------------
rep(r"""will reach approval \cite{nelson2015,minikel2024}. The standard tools for appraising evidence do not use it.""",
    r"""will reach approval \cite{nelson2015,minikel2024}, yet the standard tools for appraising evidence do not use it.""")
rep(r"""GRADE rates certainty and $I^2$ measures heterogeneity within one body of evidence, so they can say whether twelve randomized trials agree with each other, and they have no procedure for asking whether a trial result lines up with a genetic estimate, or whether an observational association is still present once tested by Mendelian randomization (MR).""",
    r"""GRADE and heterogeneity statistics such as $I^2$ show whether the studies within one body of evidence agree with each other, but they have no procedure for asking whether a trial result lines up with a genetic estimate, or whether an observational association persists when the same exposure is tested by Mendelian randomization (MR), which uses genetic variants as instruments for the exposure.""")
rep(r""" Alzheimer's disease (AD), where the drug failure rate exceeds 99\% \cite{cummings2014}, and multiple sclerosis (MS) are the domains the evidence catalog was built for, and they are described in the most detail.""", "")
rep(r"""Several independent findings establish that genetic evidence carries information about drug success. \citet{nelson2015}""", r"""\citet{nelson2015}""")
rep(r"""Triangulation \cite{lawlor2016,munafo2018} captures the intuition that multiple evidence types with independent biases should converge on a true effect. \citet{lawlor2016} state the requirement that the approaches compared have different and unrelated key sources of potential bias. The framework provides no standard quantitative test and does not distinguish \emph{types} of convergence failure.""",
    r"""Triangulation is the practice of integrating results from several approaches whose key sources of bias are different and unrelated, so that agreement among them strengthens confidence in a finding \cite{lawlor2016,munafo2018}. Most applications examine qualitatively whether studies agree on the presence of an effect, and recent work quantifies triangulation, either by pooling bias-adjusted estimates across designs into a single effect estimate \cite{shapland2024triangulation} or by scoring how consistently effect directions converge \cite{shi2025triangulator}. Neither distinguishes one kind of disagreement between designs from another.""")
rep(r"""agreed with the trial's result \cite{hernan2008}, and the comparison of prevalent users is the bias that emulation removes \cite{hernan2016}.""",
    r"""agreed with the trial's result \cite{hernan2008}, because emulation removes the bias of comparing prevalent users \cite{hernan2016}.""")
rep(r"""We do not argue that observational-RCT disagreement \emph{per se} is informative; the target trial literature shows it often is not. We argue""", r"""We argue""")
rep(r"""at the mechanism-family level separates failure modes that no single type can identify.""",
    r"""at the mechanism-family level suggests distinct failure modes that no single type can identify.""")
rep(r"""are largely independent of observational biases (confounding, selection, reverse causation), satisfying the triangulation independence condition \cite{lawlor2016}.""",
    r"""are largely unrelated to observational biases (confounding, selection, reverse causation), as triangulation requires \cite{lawlor2016}.""")
rep(r"""and extended it to seven more under blind amendments to the registration.""",
    r"""and extended it to seven more under blind amendments to the registration. The evidence catalog initially covered only Alzheimer's disease (AD), where the drug failure rate exceeds 99\% \cite{cummings2014}, and multiple sclerosis (MS), and in these two domains we classify individual drugs as well as mechanism families (\S\ref{sec:drugclass}).""")
rep(r"""The framework is exploratory: the failure modes are read from the misses rather than produced by the rule, and""",
    r"""The framework is exploratory: the failure modes were identified from the misclassified families, not produced by the rule, and""")

# ---- contributions ----------------------------------------------------------------------------------
m = re.findall(r"\\item \\textbf\{Two-way failure partition[^\n]*\n", text)
assert len(m) == 1
text = text.replace(m[0], ""); applied += 1
rep(r"""Within the two-way split, a three-way diagnostic taxonomy is read from the two-stage analysis: MR-discordant mechanisms, translation gaps, and exposure mismatches.""",
    r"""Comparing each family's observational and genetic evidence (Stage~1) with its trial outcomes (Stage~2) gives a taxonomy of three failure modes: MR-discordant mechanisms, where the observational association has no MR support; translation gaps, where both support the target and the trial is null; and exposure mismatches, where the drug does not reproduce the exposure the genetic variants index.""")

# ---- claim-level fixes (items 1, 2, 3, 5, 6; item 4 reduced to one word) ------------------------
rep(r"""The observational signal does not survive the MR test; the apparent association is attributed to confounding or reverse causation. The family is classified as an expected failure.""",
    r"""The observational association has no MR support. Confounding or reverse causation is the usual explanation; weak, underpowered or misaligned instruments are others (\S\ref{sec:limitations}). The family is classified as an expected failure.""")
rep(r"""The observational signal is attributed to confounding or reverse causation, and drugs aimed at the mechanism are expected to fail because the evidence supplies no causal pathway to intervene on.""",
    r"""Confounding or reverse causation is the usual explanation for the observational signal, and drugs aimed at the mechanism are expected to fail because the evidence supplies no support for a causal pathway to intervene on.""")
rep(r"""The observational association is attributed to confounding or reverse causation. Etiologic evidence alone flags the family""",
    r"""Confounding or reverse causation is the usual explanation for the observational association. Etiologic evidence alone flags the family""")
rep(r"""for Metabolic-AD) is attributed to confounding or reverse causation;""", r"""for Metabolic-AD) is most plausibly explained by confounding or reverse causation;""")
rep(r"""evidence confirm the pathway is real (Amyloid-AD""", r"""evidence both support a causal role for the pathway (Amyloid-AD""")
rep(r"""the pharmaceutical industry does not develop drugs against targets lacking epidemiological support""", r"""the pharmaceutical industry rarely develops drugs against targets lacking epidemiological support""")
rep(r"""(translation gaps and exposure mismatches: the target is real, and the drug is insufficient or misaligned)""",
    r"""(translation gaps and exposure mismatches: MR supports a causal role, and the drug is insufficient or misaligned)""")
rep(r"""(concordant OBS and MR, but RCT null---the target is real, the drug is insufficient)""",
    r"""(concordant OBS and MR, but RCT null: MR supports a causal role and the drug is insufficient)""")
rep(r"""GRADE's five dimensions operate within a single study design. Cross-design concordance adds a sixth: does the evidence hold up across designs?""",
    r"""GRADE assesses certainty on five domains for a body of evidence that may include both randomized and observational studies, but no domain compares estimates obtained under different designs, such as an observational association with an MR estimate for the same mechanism. Cross-design concordance makes that comparison.""")
rep(r"""the concordance rule is about \emph{divergence} diagnosing failure mode.""",
    r"""the concordance rule is about \emph{divergence} diagnosing failure mode.

Quantitative triangulation and our concordance rule ask different questions of the same evidence: \citet{shapland2024triangulation} ask what the effect is, and answer by adjusting each design's estimate for its assessed bias and pooling the estimates, whereas our rule asks what kind of mechanism the pattern of agreement between designs indicates. For beta-carotene and coronary heart disease, where both approaches can be applied, they agree. Observational studies suggest protection (RR 0.83) while trials and MR show no effect (RR 1.00 and 1.02); bias adjustment brings the three designs to a common null estimate (RR 1.01), and our rule would classify the same evidence as an MR-discordant mechanism and an expected failure, which matches the null trial results.""")
rep(r"""and a supportive MR signal is necessary but insufficient: the mechanism is real, translation is not guaranteed,""",
    r"""and a supportive MR signal does not guarantee success: MR supports a causal role, translation is not guaranteed,""")
rep(r"""a supportive MR signal is necessary but insufficient, since translation-gap targets have real mechanisms and therapeutically insufficient drugs.""",
    r"""a supportive MR signal does not guarantee success, since for translation-gap targets MR supports a causal role and the drugs were therapeutically insufficient.""")
rep(r"""\subsection{Why etiologic concordance is necessary but insufficient}""", r"""\subsection{Why etiologic concordance does not guarantee treatment success}""")
rep(r"""For MR-discordant mechanisms, the mismatch is immaterial---the MR signal is null on any estimand.""",
    r"""For MR-discordant mechanisms the classification does not depend on which estimand the observational study targets: it requires only a non-trivial observational effect and a null MR estimate.""")
rep(r"""SHA = git commit hash, a unique cryptographic identifier proving when the classification was frozen.""",
    r"""SHA: cryptographic hash identifying the timestamped version of the public repository in which each classification was frozen.""")
rep(r"""\subsection{Etiologic-only drug classification}""", r"""\subsection{Etiologic-only drug classification}
\label{sec:drugclass}""")

# ---- Conclusions -----------------------------------------------------------------------------------
rep(r"""A null MR signal is a negative indicator for a risk-encoding target: the observational association lacks causal support. A supportive MR signal is necessary but insufficient: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises.""",
    r"""A supportive MR signal does not guarantee success: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises. A null MR signal argues against a risk-encoding target, except where the drug's perturbation far exceeds the genetic one (Estrogen-BC) or the drug acts through a pathway the instrument does not index (Serotonin-MDD).""")
rep(r"""27 of them selected before the selection procedure was written down and 10 added in a blind extension""",
    r"""22 of them from the original families assembled before the selection procedure was written down and 10 from a blind extension""")

rep(r"""169 quotations from 88 sources are recorded (51 full texts, 33 abstracts, 4 web pages)""",
    r"""175 quotations from 90 sources are recorded (53 full texts, 33 abstracts, 4 web pages)""")

for dead in ["twelve randomized", "necessary but insufficient", "Two-way failure partition", "separates failure modes that", "on any estimand", "proving when", "27 of them selected", "does not develop drugs"]:
    assert dead not in text, dead
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, words
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
