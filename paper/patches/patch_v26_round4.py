"""v25 -> v26: text changes asked for by Reviewer 4 and Reviewer 5 (reports of 20 Sep 2026).

Run:  uv run --no-project python paper/patches/patch_v26_round4.py

Every edit is an exact-string replacement that must match the stated number of
times; the script aborts on the first miss and writes nothing. v25 is not touched.
Sections that report numbers from Amendment 5 (candidate-family screen, three-state
MR classification, outcome decomposition, analysis-set table) are NOT in this
patch; they are added by patch_v26b once the amendment is frozen and run.

What changes, by reviewer point:
  R5  registered analysis (24/32) is primary everywhere; the 28-family set is a
      sensitivity analysis reported second
  R5  five boundary classes are "preliminary generative hypotheses", out of the
      abstract's results and out of the Conclusions
  R5  sign-blindness and the selection of the original 27 families discussed in the
      Results (new "Accuracy across domains" subsection), not only in Limitations
  R5  "MR as a screening tool" toned down: a hypothesis for prospective testing
  R4  "MR causal" -> "MR-supportive" throughout (tables, algorithm, Figure 1 v7)
  R4  "prediction" reserved for the two prospective tests; "classification" elsewhere
  R4  "mechanism family" defined at first use (abstract, introduction)
  R4  Introduction first paragraph rewritten; "Our claim requires precision" and
      "rather than predictive" cut; why AD and MS are described in more detail stated
  R4  Results split: classifier results first, case narratives in their own
      subsection at the end, shortened
  R4  one definition of clinical success in Family selection
  R4  Amyloid-AD and IL6-MDD: stated in the text where each is scored or not
  R4  author-estimated values: the reversed-dependency sentence removed
  R4  funding / AI-use / data-availability statements made consistent
  R4  pages 43-44: placeins + FloatBarrier; wide tables allowed on their own page
  R4  "The contribution is diagnostic rather than predictive" -> "is diagnostic"
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v25_round3.tex"
DST = HERE.parent / "paper_v26_round4.tex"

text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old: str, new: str, count: int = 1) -> None:
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:160]}"
    text = text.replace(old, new)
    applied += 1


def cut(start: str, end: str) -> str:
    """Remove and return the block from `start` (inclusive) to `end` (exclusive)."""
    global text
    i = text.index(start)
    j = text.index(end, i)
    block = text[i:j]
    text = text[:i] + text[j:]
    return block


# =============================================================================
# Preamble: float control for the reviewer's pages 43-44
# =============================================================================
rep(r"\usepackage[affil-it]{authblk}", "\\usepackage[affil-it]{authblk}\n\\usepackage[section]{placeins}")

# =============================================================================
# Abstract (surgical: R5 emphasis, R4 definition and wording)
# =============================================================================
rep(r"We tested a preregistered classification rule and separately explored a diagnostic taxonomy for interpreting its errors.",
    r"We tested a preregistered classification rule and, separately, read the families it misclassified for preliminary hypotheses about why it fails.")
rep(r"We assembled 41 mechanism families across ten disease domains.",
    r"We assembled 41 mechanism families (a drug target or exposure paired with a disease indication) across ten disease domains.")
rep(r"""Under a revised primary analysis specified after the registered analysis, which excludes one indication-mismatched family and two association-only families and counts duplicated evidence once, 23/28 families were classified correctly (82.1\%; outcome-permutation $p = 0.0006$, cluster-level $p = 0.0002$). By tier, 17/21 in the original domains and 6/7 in the blind extension, the latter not significant alone (permutation $p = 0.14$) and not independent confirmation. The registered analysis, 24/32 (75.0\%; $p = 0.005$), is reported as a robustness analysis. The eight misses under the registered rule divide 5 and 3 by MR status; the direction is fixed by the rule, the mechanistic account of each side is not: translation gaps and exposure mismatch for the three causal-MR failures, effector-neutralization, small-effect and mechanism-bypass for the five null-MR successes. Five boundary classes are retrospective and hypothesis-generating.""",
    r"""Under the registered analysis, 24/32 families were classified correctly (75.0\%; outcome-permutation $p = 0.005$ at family and instrument-cluster level): 18/22 in the original domains and 6/10 in the blind extension, the latter not significant alone (permutation $p = 0.55$) and not independent confirmation. A sensitivity analysis specified after the registered analysis, with outcomes known, excludes one indication-mismatched family and two association-only families and counts duplicated evidence once: 23/28 (82.1\%; $p = 0.0006$). The eight misses divide 5 and 3 by MR status; the direction is fixed by the rule, the mechanistic account of each side is not: translation gaps and exposure mismatch for the three MR-supportive failures, effector-neutralization, small-effect and mechanism-bypass for the five MR-null successes. These five boundary classes are preliminary generative hypotheses.""")
rep(r"Its contribution is diagnostic: the cross-design comparison generates mechanistic hypotheses about why the binary MR classification misses, each implying a different pipeline response.",
    r"Its contribution is diagnostic: the cross-design comparison generates mechanistic hypotheses about why the binary MR classification misses.")

# =============================================================================
# Introduction
# =============================================================================
rep(r"""Drug development for Alzheimer's disease and multiple sclerosis consumes billions of dollars annually, with an overall AD drug failure rate exceeding 99\% \cite{cummings2014}. Standard tools for evaluating mechanistic evidence---GRADE for rating certainty, $I^2$ for measuring heterogeneity---operate within a single study design. They assess whether twelve RCTs agree, leaving cross-design consistency untested: whether RCT evidence agrees with genetic evidence, or whether observational signals survive Mendelian randomization.""",
    r"""Genetic evidence about a drug target carries information about whether a drug against that target will reach approval \cite{nelson2015,minikel2024}. The standard tools for appraising evidence do not use it. GRADE rates certainty and $I^2$ measures heterogeneity within one body of evidence, so they can say whether twelve randomized trials agree with each other, and they have no procedure for asking whether a trial result lines up with a genetic estimate, or whether an observational association is still present once tested by Mendelian randomization (MR). This paper asks whether a fixed rule that compares observational and MR evidence for a \emph{mechanism family}, a drug target or exposure paired with a disease indication, classifies Phase~III outcomes, and what the families it misclassifies have in common. Alzheimer's disease (AD), where the drug failure rate exceeds 99\% \cite{cummings2014}, and multiple sclerosis (MS) are the domains the evidence catalog was built for, and they are described in the most detail; eight further domains were added with the rule frozen.""")
rep(r"""Our claim requires precision. We do not argue that observational-RCT disagreement \emph{per se} is informative---the target trial literature shows it often is not. We argue that the pattern across three evidence types (observational, MR, RCT) at the \emph{mechanism-family} level diagnoses failure modes that no single type can identify. MR provides an evidence stream whose biases""",
    r"""We do not argue that observational-RCT disagreement \emph{per se} is informative; the target trial literature shows it often is not. We argue that the pattern across three evidence types (observational, MR, RCT) at the mechanism-family level separates failure modes that no single type can identify. MR provides an evidence stream whose biases""")
rep(r"""We operationalized this with an explicit decision rule and tested it across three disease domains. An ablation shows that MR evidence alone accounts for all predictive power---the observational leg adds zero classifications beyond what MR provides. The structural explanation: nearly every mechanism family reaching Phase~III has non-trivial observational support (31/32 scored families), so the observational variable is near-constant and carries no discriminative information.""",
    r"""We operationalized this with an explicit decision rule, tested it across three disease domains, and extended it to seven more under blind amendments to the registration. An ablation shows that MR status alone accounts for every classification: the observational leg changes none of them, because nearly every mechanism family reaching Phase~III has non-trivial observational support (31/32 scored families), so the observational variable is near-constant and carries no discriminative information.""")
rep(r"""The contribution is diagnostic rather than predictive. A two-stage analysis---first etiologic evidence only, then adding RCT outcomes---reveals three failure modes that MR alone cannot separate: MR-discordant mechanisms, translation gaps, and exposure mismatches. All produce failed drugs; what differs is \emph{why}. The framework is exploratory: the failure modes are read from the misses rather than predicted by the rule, and \S\ref{sec:two_modes} records which were declared before the miss they explain was observed.""",
    r"""The contribution is diagnostic. A two-stage analysis---first etiologic evidence only, then adding RCT outcomes---separates three failure modes that MR alone cannot: MR-discordant mechanisms, translation gaps, and exposure mismatches. All produce failed drugs; what differs is \emph{why}. The framework is exploratory: the failure modes are read from the misses rather than produced by the rule, and \S\ref{sec:two_modes} records which were declared before the miss they explain was observed.""")
rep(r"""The observational leg carries no predictive information; its value is diagnostic.""",
    r"""The observational leg carries no information about outcomes; its value is diagnostic.""")
rep(r"""The eight misclassified families split by MR $d$ into failures of targets lacking MR causal support and failures of targets carrying it""",
    r"""The eight misclassified families split by MR $d$ into failures of targets lacking MR support and failures of targets carrying it""")
rep(r"""Five finer-grained boundary classes are proposed as hypothesis-generating categories on $n = 8$ misses, with assignment criteria""",
    r"""Five finer-grained boundary classes are proposed as preliminary generative hypotheses on $n = 8$ misses, with assignment criteria""")
rep(r"""\item \textbf{Robustness (\S\ref{sec:robustness}).} Threshold sensitivity, leave-one-domain-out cross-validation, alternative granularity schemes, and instrument independence audit confirm the result is not driven by threshold choice, any single domain, or family-definition decisions.""",
    r"""\item \textbf{Robustness (\S\ref{sec:robustness}).} Threshold sensitivity, leave-one-domain-out cross-validation, alternative granularity schemes, an instrument independence audit, and a 28-family sensitivity analysis show that the result is not driven by threshold choice, any single domain, or family-definition decisions.""")

# =============================================================================
# Methods
# =============================================================================
# Family selection: one definition of clinical success (R4 point 1); registered set primary (R5)
rep(r"""interval extractable from the source, \emph{and} a Phase~III readout exists for a drug
acting on that mechanism, with approval or non-approval as the recorded outcome.""",
    r"""interval extractable from the source, \emph{and} a Phase~III readout exists for a drug
acting on that mechanism. The recorded outcome is \emph{success} when a drug acting on the
mechanism is approved for the family's indication or met the primary efficacy endpoint of
its Phase~III program, and \emph{failure} when the Phase~III program did not meet its
primary endpoint or was discontinued for futility; a family whose class contains both
outcomes is coded on the majority of its programs. One scored family, IL6-MDD, is coded on
a Phase~II readout declared in advance (Amendment~2), against this criterion;
\S\ref{sec:robustness} reports the count without it.""")
rep(r"""(4)~Every family satisfying (2) is scored under the registered rule. A revised primary analysis, specified after the registered analysis and after all outcomes were known, additionally excludes one family on indication mismatch and two whose genetic leg is an association rather than an MR estimate, and counts two families that share identical evidence once (\S\ref{sec:revised_primary}); the registered count is reported beside it throughout.""",
    r"""(4)~Every family satisfying (2) is scored under the registered rule, and none is dropped once its outcome is known; the registered count is the primary result. A sensitivity analysis specified after the registered analysis, with all outcomes known, additionally excludes one family on indication mismatch and two whose genetic leg is an association rather than an MR estimate, and counts two families that share identical evidence once (28 families; \S\ref{sec:sensitivity_set}). It is reported beside the registered count, not in place of it.""")
# Data: nothing further (AD/MS emphasis is now in the Introduction).
# Evidence classification: causal -> supportive; the two association families; Amyloid-AD stated
rep(r"""Accuracy is reported by instrument type in \S\ref{sec:robustness}, which makes the exposure auditable: all eight misclassifications fall in the coding-variant and biomarker-GWAS classes, while every family instrumented by a \emph{cis}-pQTL (8/8) or a polygenic score (5/5) is classified correctly. Two scored families carry a GEN leg drawn from a genetic association rather than an MR causal estimate---Complement-GA (\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---so under the registered rule the pooling bears on exactly these two, both of which are misclassified. The GEN leg is called causal only for families instrumented by MR and associated for these two. The revised primary analysis (\S\ref{sec:revised_primary}) sets both aside, so every family it scores has an MR estimate on the genetic leg and the pooling of association-only families does not enter it.""",
    r"""Accuracy is reported by instrument type in \S\ref{sec:robustness}, which makes the exposure auditable: all eight misclassifications fall in the coding-variant and biomarker-GWAS classes, while every family instrumented by a \emph{cis}-pQTL or a polygenic score is classified correctly. Two scored families carry a GEN leg drawn from a genetic association rather than an MR estimate---Complement-GA (\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---so under the registered rule the pooling bears on exactly these two, both of which are misclassified. The GEN leg is called MR-supportive only for families instrumented by MR and associated for these two. The 28-family sensitivity analysis (\S\ref{sec:sensitivity_set}) sets both aside, so every family it scores has an MR estimate on the genetic leg. One further family, Amyloid-AD, carries a genetic association (\emph{APOE4}) that qualifies as a GEN leg under this pooling and was not entered in the classified set; \S\ref{sec:amyloid} states its evidence, and \S\ref{sec:robustness} reports the registered count with it scored.""")
# Rule
rep(r"""\textbf{MR classification.} Causal if (a) the confidence interval excludes the null \emph{and} (b) $d_{\text{MR}} \geq 0.10$; null otherwise. Both criteria must be met---a statistically significant but negligible effect and a large but imprecise effect are both classified as null.""",
    r"""\textbf{MR classification.} Supportive if (a) the confidence interval excludes the null \emph{and} (b) $d_{\text{MR}} \geq 0.10$; null otherwise. Both criteria must be met---a statistically significant but negligible effect and a large but imprecise effect are both classified as null. ``MR-supportive'' names the evidence pattern; it does not assert that the exposure is causal for the outcome.""")
rep(r"""\textbf{Qualitative discordance.} OBS non-trivial, MR null. The observational signal does not survive causal testing; the apparent association reflects confounding or reverse causation.""",
    r"""\textbf{Qualitative discordance.} OBS non-trivial, MR null. The observational signal does not survive the MR test; the apparent association is attributed to confounding or reverse causation. The family is classified as an expected failure.""")
rep(r"""\textbf{Concordance.} OBS non-trivial, MR causal. Both evidence types support the mechanism.""",
    r"""\textbf{Concordance.} OBS non-trivial, MR supportive. Both evidence types support the mechanism. Expected success.""")
rep(r"""\textbf{Null concordance.} OBS trivial, MR null. No evidence from either type; prediction is ambiguous.""",
    r"""\textbf{Null concordance.} OBS trivial, MR null. No evidence from either type; the family is ambiguous and unscored.""")
rep(r"""\textbf{Genetic-only signal.} OBS trivial, MR causal. Genetic support without observational confirmation.""",
    r"""\textbf{Genetic-only signal.} OBS trivial, MR supportive. Genetic support without observational confirmation. Expected success.""")
rep(r"""and classifies their \emph{agreement pattern} rather than testing whether their magnitudes are statistically distinguishable.""",
    r"""and classifies their \emph{agreement pattern} rather than testing whether their magnitudes are statistically distinguishable. The word ``prediction'' is reserved in this paper for the two families whose classification was registered before their trial read out (\S\ref{par:prospective}); every other classification was made with the outcome on record and is called a classification.""")
# Phase III holdout, two-stage design
rep(r"""Drugs whose family lacked classification received no prediction. The rule was mechanical: qualitative discordance (non-trivial OBS, null MR) classifies as failure; concordance (non-trivial OBS, causal MR) classifies as approval.""",
    r"""Drugs whose family lacked classification received no classification. The rule was mechanical: qualitative discordance (non-trivial OBS, null MR) classifies as expected failure; concordance (non-trivial OBS, MR supportive) classifies as expected approval.""")
rep(r"""\textbf{Stage~1 (de-circularized).} Classify families using only etiologic evidence. All drug outcomes are fully out of sample. This stage can use ``predicts'' language.""",
    r"""\textbf{Stage~1 (de-circularized).} Classify families using only etiologic evidence. No drug outcome enters the classification.""")
# Algorithm
rep(r"""  \STATE \textbf{MR:} \textsc{Causal} if $1.0 \notin (l, u)$ \textbf{and} $d_{\text{MR}} \geq 0.10$; else \textsc{Null}
  \IF{\textsc{Non-trivial} and \textsc{Null}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Qualitative Discordance} $\rightarrow$ predict \textsc{Failure}
  \ELSIF{\textsc{Non-trivial} and \textsc{Causal}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Concordance} $\rightarrow$ predict \textsc{Success}
  \ELSIF{\textsc{Trivial} and \textsc{Null}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Null Concordance} $\rightarrow$ \textsc{Ambiguous}
  \ELSIF{\textsc{Trivial} and \textsc{Causal}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Genetic-Only} $\rightarrow$ predict \textsc{Success}
  \ENDIF
\ENDFOR
\medskip
\ENSURE For each drug mapped to family $f_j$: predicted outcome $\in \{\textsc{Success}, \textsc{Failure}, \textsc{Ambiguous}\}$""",
    r"""  \STATE \textbf{MR:} \textsc{Supportive} if $1.0 \notin (l, u)$ \textbf{and} $d_{\text{MR}} \geq 0.10$; else \textsc{Null}
  \IF{\textsc{Non-trivial} and \textsc{Null}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Qualitative Discordance} $\rightarrow$ \textsc{Expected failure}
  \ELSIF{\textsc{Non-trivial} and \textsc{Supportive}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Concordance} $\rightarrow$ \textsc{Expected success}
  \ELSIF{\textsc{Trivial} and \textsc{Null}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Null Concordance} $\rightarrow$ \textsc{Ambiguous}
  \ELSIF{\textsc{Trivial} and \textsc{Supportive}}
    \STATE $\text{label}(f_j) \leftarrow$ \textsc{Genetic-Only} $\rightarrow$ \textsc{Expected success}
  \ENDIF
\ENDFOR
\medskip
\ENSURE For each drug mapped to family $f_j$: expected outcome $\in \{\textsc{Success}, \textsc{Failure}, \textsc{Ambiguous}\}$""")
# Statistical tests: registered primary; wording
rep(r"""The registered test is a one-sided exact binomial against 50\% chance accuracy, which treats each family as an independent Bernoulli trial carrying no information about its outcome. That null ignores the outcome base rate (17 approvals and 15 failures among the 32 scored families, so a rule that always predicts approval scores 53\%) and the dependence among families that share an MR instrument set. The primary test is therefore an outcome-permutation test with the classification held fixed:""",
    r"""The registered test is a one-sided exact binomial against 50\% chance accuracy, which treats each family as an independent Bernoulli trial carrying no information about its outcome. That null ignores the outcome base rate (17 approvals and 15 failures among the 32 scored families, so a rule that always expects approval scores 53\%) and the dependence among families that share an MR instrument set. The primary test is therefore an outcome-permutation test with the classification held fixed:""")
# Ablation design
rep(r"""\item \textbf{Always-fail}: predict failure for every family (base-rate baseline).
\item \textbf{MR-only}: predict failure if MR is null, success if MR is causal (ignore OBS).
\item \textbf{OBS-only}: predict success if OBS is non-trivial, failure if OBS is trivial (ignore MR).""",
    r"""\item \textbf{Always-fail}: expected failure for every family (base-rate baseline).
\item \textbf{MR-only}: expected failure if MR is null, expected success if MR is supportive (ignore OBS).
\item \textbf{OBS-only}: expected success if OBS is non-trivial, expected failure if OBS is trivial (ignore MR).""")
rep(r"""For each rule we report total accuracy, accuracy split by outcome (correct failures vs.\ correct approvals), and McNemar paired disagreements""",
    r"""For each rule we report total accuracy, accuracy split by outcome (failures and approvals classified correctly), and McNemar paired disagreements""")
# Figure 1: v7 (labels), caption
rep(r"\includegraphics[width=0.95\textwidth]{figures/fig1_flowchart_v6.pdf}",
    r"\includegraphics[width=0.95\textwidth]{figures/fig1_flowchart_v7.pdf}")
rep(r"""and the MR leg is causal if its confidence interval excludes the null and $d_{\text{MR}} \geq 0.10$. The family label is the OBS$\times$MR cell: qualitative discordance predicts failure, concordance and genetic-only predict success, and null concordance is ambiguous and unscored. Stage~1 uses etiologic evidence only; RCT outcomes enter in Stage~2, after classification, to score the prediction and to read the failure mode.}""",
    r"""and the MR leg is supportive if its confidence interval excludes the null and $d_{\text{MR}} \geq 0.10$. The family label is the OBS$\times$MR cell: qualitative discordance is an expected failure, concordance and genetic-only are expected successes, and null concordance is ambiguous and unscored. Stage~1 uses etiologic evidence only; RCT outcomes enter in Stage~2, after classification, to score the classification and to read the failure mode.}""")

# =============================================================================
# Results: block surgery. Cut the blocks that move, rewrite the narratives, reassemble.
# =============================================================================
# --- accounting caption
rep(r"""The revised primary analysis, specified after the registered analysis, scores 28 of these 32 families, 23 correctly (\S\ref{sec:revised_primary}).}""",
    r"""The registered count, 24/32, is the primary result; a 28-family sensitivity analysis specified after the registered analysis scores 23 correctly (\S\ref{sec:sensitivity_set}).}""")

# --- Stage 1 (neuro) : prediction wording, causal -> supportive in the table
rep(r"""Nine neuroepidemiology mechanism families had etiologic evidence from both OBS and MR types; one (BMI~$\to$~MS) is excluded from scoring as prediction pending.""",
    r"""Nine neuroepidemiology mechanism families had etiologic evidence from both OBS and MR types; one (BMI~$\to$~MS) is excluded from scoring because no trial tests the matching endpoint.""")
rep(r"""Three are concordant. BMI~$\to$~MS is excluded as prediction pending.""",
    r"""Three are concordant. BMI~$\to$~MS is excluded as pending.""")
rep(r"""Anti-CD20-MS & 0.103 & Yes & 1.084 & Non-triv. & Causal & Concordance \\""",
    r"""Anti-CD20-MS & 0.103 & Yes & 1.084 & Non-triv. & Supp. & Concordance \\""")
rep(r"""BMI-MS$^\dagger$ & 0.189 & Yes & 0.360 & Non-triv. & Causal & Pending \\
VitD-MS & 0.382 & Yes & 0.186 & Non-triv. & Causal & Concordance \\
EBV-MS & 0.887 & Yes & 0.293 & Non-triv. & Causal & Concordance \\""",
    r"""BMI-MS$^\dagger$ & 0.189 & Yes & 0.360 & Non-triv. & Supp. & Pending \\
VitD-MS & 0.382 & Yes & 0.186 & Non-triv. & Supp. & Concordance \\
EBV-MS & 0.887 & Yes & 0.293 & Non-triv. & Supp. & Concordance \\""")
rep(r"""Of 38 holdout AD/MS drugs (22 failed, 16 approved), 8 mapped to 4 families with etiologic classification (Table~\ref{tab:drugs_stage1}). An additional 14 drugs mapped to Amyloid-AD, which is analyzed separately (\S\ref{sec:amyloid}). The remaining 16 drugs mapped to families lacking full OBS$+$GEN evidence and received no prediction.""",
    r"""Of 38 holdout AD/MS drugs (22 failed, 16 approved), 8 mapped to 4 families with etiologic classification (Table~\ref{tab:drugs_stage1}). An additional 14 drugs mapped to Amyloid-AD, which has no MR estimate and is treated in \S\ref{sec:amyloid}. The remaining 16 drugs mapped to families lacking full OBS$+$GEN evidence and received no classification.""")
rep(r"""\caption{Etiologic-only drug classification. Accuracy: 7/8 (87.5\%, 95\% Wilson CI: 52.9--97.8\%). Discordant families predicted failure at 100\% (3/3); concordant families predicted approval at 80\% (4/5).""",
    r"""\caption{Etiologic-only drug classification. Accuracy: 7/8 (87.5\%, 95\% Wilson CI: 52.9--97.8\%). Discordant families matched the failed outcome in 3/3 drugs; concordant families matched approval in 4/5.""")
rep(r"""The sample is underpowered for frequentist significance at $n = 8$ (Fisher's exact $p = 0.14$; permutation $p = 0.07$). The directional separation---discordant families producing 100\% drug failure versus 33\% in concordant---rests on eight families and is reported as a proof-of-concept result. Combined with the cardiometabolic replication (\S\ref{sec:cardio}), the rule classifies 14/15 unambiguous neuro+cardio outcomes correctly across two independent disease domains (combined permutation $p = 0.001$). A third domain (autoimmune) provides 4/7, with three misses that define the effector-neutralization boundary (\S\ref{sec:autoimmune}).

The single miss exemplifies \emph{exposure mismatch}: the MR instrument measures the causal effect of one exposure (lifelong genetically determined vitamin~D status), while the drug delivers a different one (adult oral supplementation). These are different interventions on the same pathway, and concordance between MR and observational evidence does not guarantee that the drug recapitulates the exposure the instrument captures. For vitamin~D-MS, MR supports a causal role for lifelong status (OR~2.0, $d = 0.38$) and observational evidence agrees (OR~1.40, $d = 0.19$), producing concordance and predicting approval. The trial failed because adult supplementation does not recapitulate lifelong exposure. This failure mode is predictable a priori whenever the MR instrument's exposure window diverges from the drug's mechanism of action---it is a structural property of the instrument-intervention mapping, not a quirk of one family.

\paragraph{Prediction pending: BMI and MS.}
BMI~$\to$~MS occupies a distinct category: the etiologic evidence supports causation, but no randomized trial has tested the corresponding clinical endpoint.""",
    r"""The sample is underpowered for frequentist significance at $n = 8$ (Fisher's exact $p = 0.14$; permutation $p = 0.07$). The directional separation---discordant families producing 100\% drug failure versus 33\% in concordant---rests on eight families and is reported as a proof-of-concept result. The single miss, vitamin~D-MS, is an \emph{exposure mismatch}: MR supports a causal role for lifelong genetically determined vitamin~D status (OR~2.0, $d = 0.38$), observational evidence agrees (OR~1.40, $d = 0.19$), and the trial delivered adult oral supplementation, a different intervention on the same pathway (\S\ref{sec:narratives}).

\paragraph{Pending: BMI and MS.}
BMI~$\to$~MS occupies a distinct category: the etiologic evidence supports causation, but no randomized trial has tested the corresponding clinical endpoint.""")
rep(r"""producing qualitative discordance and correctly predicting that weight-loss interventions would not prevent AD.""",
    r"""producing qualitative discordance, an expected failure, which the weight-loss trial record matches.""")

# --- cut the narrative blocks that move to the end of Results
neuro_cases = cut(r"\subsection{Cases etiologic evidence diagnoses}", r"\subsection{The case etiologic evidence cannot diagnose: amyloid}")
amyloid = cut(r"\subsection{The case etiologic evidence cannot diagnose: amyloid}", r"\subsection{Stage~2: Retrospective analysis including RCT evidence}")
stage2 = cut(r"\subsection{Stage~2: Retrospective analysis including RCT evidence}", r"\subsection{Amyloid subanalysis}")
amyloid_sub = cut(r"\subsection{Amyloid subanalysis}", r"\subsection{Failure-mode taxonomy}")
taxonomy = cut(r"\subsection{Failure-mode taxonomy}", r"\subsection{Cross-domain boundary test}")
boundary = cut(r"\subsection{Cross-domain boundary test}", r"\subsection{The investigation paradox}")
paradox = cut(r"\subsection{The investigation paradox}", r"\subsection{Cross-domain generalization: cardiometabolic mechanisms}")
del paradox  # two sentences with no data behind them; Reviewer 4 asked for the narratives to be shortened

# --- cardiometabolic: keep the table and the prospective tests; move the narrative out
rep(r"""\subsection{Cross-domain generalization: cardiometabolic mechanisms}
\label{sec:cardio}

The psychiatric boundary test (\S\ref{sec:boundary}) showed the method fails when families are defined at the diagnostic level. A stronger test asks: does it replicate in a disease domain where mechanism-level families are well-defined and ground truth is unambiguous? Cardiometabolic disease provides this test. MR is most mature in cardiology, trial outcomes are clear, and several textbook MR-discordant mechanisms have been documented independently of our framework.

We applied the same deterministic classification (Algorithm~\ref{alg:discordance}) to ten cardiometabolic mechanism families (Table~\ref{tab:cardio}). Effect sizes were drawn from published MR studies and meta-analyses; the decision rule, the $|d| = 0.10$ threshold, and the pooling procedure were frozen from the neuroepidemiology analysis. No parameters were re-estimated. The cardiometabolic families were defined at the mechanism level (e.g., ``HDL/CETP'' rather than ``lipids''), matching the granularity used in neuroepidemiology; the family definitions themselves are a degree of freedom, and we discuss this in the Limitations.

This analysis is a validation test, not a discovery. The cardiometabolic MR-discordant mechanisms (HDL, niacin, homocysteine, CRP, uric acid) are well-established in the MR literature, and their identification here recovers known results using our deterministic rule. The value is that the same frozen procedure, designed for neuroepidemiology, transfers without modification to a domain where ground truth is unambiguous.""",
    r"""\subsection{Cardiometabolic disease}
\label{sec:cardio}

We applied the same deterministic classification (Algorithm~\ref{alg:discordance}) to ten cardiometabolic mechanism families (Table~\ref{tab:cardio}), with the decision rule, the $d = 0.10$ threshold, and the pooling procedure frozen from the neuroepidemiology analysis. MR is most mature in cardiology and trial outcomes are clear, so the cardiometabolic MR-discordant mechanisms (HDL, niacin, homocysteine, CRP) are established results that the rule recovers rather than discoveries.""")
rep(r"""Family & OBS OR & MR OR (95\% CI) & MR & Trial & Class & Correct? \\""",
    r"""Family & OBS OR & MR OR (95\% CI) & MR & Trial & Class & Correct? \\""")
rep(r"""LDL / PCSK9$^\text{e}$ & 1.52 & 1.78 (1.58--2.01) & Causal & Approved & Concordant & \checkmark \\
Blood pressure$^\text{f}$ & 1.41 & 1.44 (1.35--1.55) & Causal & Approved & Concordant & \checkmark \\
Triglycerides$^\text{e}$ & 1.72 & 1.62 (1.24--2.11) & Causal & Approved & Concordant & \checkmark \\
\midrule
Lp(a)$^\text{g}$ & 1.13 & 0.94 (0.93--0.95) & Causal & \emph{Pending} & Genetic-only & --- \\""",
    r"""LDL / PCSK9$^\text{e}$ & 1.52 & 1.78 (1.58--2.01) & Supp. & Approved & Concordant & \checkmark \\
Blood pressure$^\text{f}$ & 1.41 & 1.44 (1.35--1.55) & Supp. & Approved & Concordant & \checkmark \\
Triglycerides$^\text{e}$ & 1.72 & 1.62 (1.24--2.11) & Supp. & Approved & Concordant & \checkmark \\
\midrule
Lp(a)$^\text{g}$ & 1.13 & 0.94 (0.93--0.95) & Supp. & \emph{Pending} & Genetic-only & --- \\""")
rep(r"""the parenthetical check mark records the registered prediction against the outcome and enters no accuracy figure.}""",
    r"""the parenthetical check mark records the registered prediction (\S\ref{par:prospective}) against the outcome and enters no accuracy figure.}""")
cardio_narr = cut(r"""Four MR-discordant mechanisms---HDL/CETP, niacin/HDL, homocysteine/B-vitamins, and CRP---each have moderate-to-strong observational associations""",
                  r"""\paragraph{Prospective predictions.}""")
rep(r"""If Lp(a)HORIZON fails, the genetic-only cell should predict ambiguity rather than success, and the failure mode (translation gap, exposure mismatch, or a new category) should be characterized.""",
    r"""If Lp(a)HORIZON fails, the genetic-only cell should be read as ambiguous rather than as an expected success, and the failure mode (translation gap, exposure mismatch, or a new category) should be characterized.""")
rep(r"""Lp(a)-lowering via pelacarsen (Lp(a)HORIZON, NCT04023552; $n = 8{,}323$; primary completion June 2026; topline expected H2 2026) is registered as a predicted success. The observational effect is trivial ($d_{\text{OBS}} = 0.067$) and the MR effect, rescaled to the observational contrast, is causal ($d_{\text{MR}} = 0.123$), which places the family in the genetic-only cell.""",
    r"""Lp(a)-lowering via pelacarsen (Lp(a)HORIZON, NCT04023552; $n = 8{,}323$; primary completion June 2026; topline expected H2 2026) is registered as a predicted success. The observational effect is trivial ($d_{\text{OBS}} = 0.067$) and the MR effect, rescaled to the observational contrast, is supportive ($d_{\text{MR}} = 0.123$), which places the family in the genetic-only cell.""")
rep(r"""At the $d = 0.10$ threshold used throughout this paper the MR signal is null, the family is qualitatively discordant, and the registered prediction is failure. At a threshold of $d = 0.08$ the MR signal is causal, the family is concordant, and the registered prediction is success.""",
    r"""At the $d = 0.10$ threshold used throughout this paper the MR signal is null, the family is qualitatively discordant, and the registered prediction is failure. At a threshold of $d = 0.08$ the MR signal is supportive, the family is concordant, and the registered prediction is success.""")

# --- ablation: move up (it is a classifier result), wording
ablation = cut(r"\subsection{Ablation of the observational leg}", r"\subsection{Autoimmune extension: the effector-neutralization boundary}")
ablation = ablation.replace(
    r"""and no family changes classification when the observational leg is added or removed. This identity is not a threshold artifact---the MR-only and cross-design rules produce zero McNemar disagreements at \emph{every} threshold from $d = 0.05$ to $d = 0.20$ (see \S\ref{sec:robustness}). The structural explanation is that 31 of 32 scored families have non-trivial OBS ($d \geq 0.10$); the sole exception (IGF1-CRC, $d_{\text{OBS}} = 0.063$) is classified as genetic-only under the cross-design rule, matching the MR-only prediction.""",
    r"""and no family changes classification when the observational leg is added or removed. This identity is not a threshold artifact---the MR-only and cross-design rules produce zero McNemar disagreements at \emph{every} threshold from $d = 0.05$ to $d = 0.20$ (see \S\ref{sec:robustness}). The structural explanation is that 31 of 32 scored families have non-trivial OBS ($d \geq 0.10$); the sole exception (IGF1-CRC, $d_{\text{OBS}} = 0.063$) is classified as genetic-only under the cross-design rule, matching the MR-only classification.""")
ablation = ablation.replace(
    r"""The OBS-only rule predicts success for all families with non-trivial OBS and failure for the one family (IGF1-CRC extension) where the scored set includes a trivial-OBS failure, producing 18/32 (56\%). Observational evidence alone has minimal discriminative power for drug outcomes in this sample, consistent with the confounding and reverse-causation problems that motivate MR.

The ablation establishes that the cross-design rule's \emph{predictive} contribution reduces to MR-null status; adding the observational leg improves prediction for no family at any threshold. The observational leg's value, where it has one, is \emph{diagnostic}: it enables the failure-mode taxonomy that MR alone cannot provide (\S\ref{sec:two_modes}). This predictive-diagnostic distinction structures the rest of the paper: the accuracy results depend on MR alone, while the boundary class analysis depends on the full cross-design framework.""",
    r"""The OBS-only rule expects success for all families with non-trivial OBS and failure for the one family (IGF1-CRC extension) where the scored set includes a trivial-OBS failure, producing 18/32 (56\%). Observational evidence alone has minimal discriminative power for drug outcomes in this sample, consistent with the confounding and reverse-causation problems that motivate MR.

The ablation establishes that the cross-design rule's classifications reduce to MR-null status; adding the observational leg changes no classification at any threshold. The observational leg's value, where it has one, is \emph{diagnostic}: it enables the failure-mode reading that MR alone cannot provide (\S\ref{sec:two_modes}). The accuracy results depend on MR alone, while the boundary-class reading depends on the full cross-design framework.""")
assert "MR-only classification" in ablation and "changes no classification" in ablation

# --- autoimmune: table stays, narrative moves
rep(r"""\subsection{Autoimmune extension: the effector-neutralization boundary}
\label{sec:autoimmune}

We extended the classification to eight autoimmune mechanism families across rheumatoid arthritis (RA), psoriasis, atopic dermatitis (AD), and cardiovascular disease (Table~\ref{tab:autoimmune}). The autoimmune domain uses case-control standardized mean differences (SMDs) as the OBS measure rather than epidemiological ORs, reflecting a different evidence construct; autoimmune accuracy is reported separately and never pooled with neuro or cardio.""",
    r"""\subsection{Autoimmune disease}
\label{sec:autoimmune}

We extended the classification to eight autoimmune mechanism families across rheumatoid arthritis (RA), psoriasis, atopic dermatitis (AD), and cardiovascular disease (Table~\ref{tab:autoimmune}). The autoimmune domain uses case-control standardized mean differences (SMDs) as the OBS measure rather than epidemiological ORs, reflecting a different evidence construct; autoimmune accuracy is reported separately and never pooled with neuro or cardio. The three misses share a target elevated as a consequence of active disease; \S\ref{sec:narratives} reads them as the effector-neutralization boundary.""")
rep(r"""The effector-neutralization boundary: approved drugs targeting disease effectors (TNF, IL-17, CTLA-4) show null MR and are misclassified; those targeting risk-encoding loci (IL-23R, STAT4, FCRL3) show causal MR and are correctly classified.}""",
    r"""The effector-neutralization boundary: approved drugs targeting disease effectors (TNF, IL-17, CTLA-4) show null MR and are misclassified; those targeting risk-encoding loci (IL-23R, STAT4, FCRL3) show supportive MR and are correctly classified.}""")
rep(r"""\multicolumn{8}{l}{\emph{Risk-encoding loci (MR causal --- hits)}} \\
IL-23-psoriasis & Psor. & 0.660 & 0.267 & Causal & Appr. & Conc. & $\checkmark$ \\
JAK-STAT-RA$^\dagger$ & RA & non-triv. & 0.132 & Causal & Appr. & Conc. & $\checkmark$ \\
CD20-RA$^\dagger$ & RA & non-triv. & 0.141 & Causal & Appr. & Conc. & $\checkmark$ \\""",
    r"""\multicolumn{8}{l}{\emph{Risk-encoding loci (MR supportive --- hits)}} \\
IL-23-psoriasis & Psor. & 0.660 & 0.267 & Supp. & Appr. & Conc. & $\checkmark$ \\
JAK-STAT-RA$^\dagger$ & RA & non-triv. & 0.132 & Supp. & Appr. & Conc. & $\checkmark$ \\
CD20-RA$^\dagger$ & RA & non-triv. & 0.141 & Supp. & Appr. & Conc. & $\checkmark$ \\""")
autoimmune_narr = cut(r"""The autoimmune results reveal a clean mechanistic boundary.""", r"""\subsection{Extension to oncology, respiratory, and metabolic disease}""")

# --- extension: domain selection shortened, table causal -> supp, narratives move
rep(r"""\subsection{Extension to oncology, respiratory, and metabolic disease}
\label{sec:extension}

The three original domains---neuroepidemiology, cardiometabolic, and autoimmune---share a common feature: well-characterized drug targets with mature MR evidence from genome-wide association studies. A stronger generalization test asks whether the classification transfers to domains where the mapping between MR instruments and drug mechanisms is less direct. We extended the analysis to fourteen additional mechanism families across seven disease domains (Table~\ref{tab:extension}).

\paragraph{Domain selection.} The first extension (Amendment~1) covered oncology, respiratory medicine, and metabolic/endocrine disease, selected because each contains at least one drug class with published drug-target MR evidence and unambiguous Phase~III outcomes. Oncology tests the framework on cancer-prevention targets, where germline risk factors are the relevant exposures. Respiratory medicine tests the eosinophilic inflammation pathway, where the same biological mediator (eosinophil count) has genetically determined baseline levels \emph{and} is elevated as a disease effector---contrasting with the autoimmune domain, where effector elevation is exclusively downstream of disease onset. Metabolic/endocrine disease tests drug-target MR with \emph{cis}-regulatory instruments (eQTLs and pQTLs near the drug's gene target), a newer methodology with specific pitfalls \cite{gill2024pitfalls}. A second extension (Amendment~2) added psychiatry, gastroenterology, ophthalmology, and musculoskeletal disease. Psychiatry tests a domain where diagnostic heterogeneity previously caused the framework to fail at the disorder level (\S\ref{sec:boundary}); mechanism-level families (IL-6/MDD, serotonin/MDD) bypass this problem. Ophthalmology provides the strongest known genetic association in human disease (CFH Y402H, OR 2.50) paired with a failed drug, testing the translation-gap boundary under maximal etiologic evidence. Musculoskeletal disease tests a clean concordance case with tight instrument-target alignment (SOST cis-MR and anti-sclerostin).""",
    r"""\subsection{Extension domains}
\label{sec:extension}

We extended the analysis to fourteen mechanism families across seven disease domains (Table~\ref{tab:extension}), declared in two blind amendments. The first (Amendment~1) covered oncology, respiratory medicine, and metabolic/endocrine disease: cancer-prevention targets where germline risk factors are the exposures; the eosinophil pathway, where the mediator is both genetically determined at baseline and elevated as a disease effector; and drug-target MR with \emph{cis}-regulatory instruments \cite{gill2024pitfalls}. The second (Amendment~2) added psychiatry, where disorder-level families had failed in a boundary test (\S\ref{sec:narratives}) and mechanism-level families were declared instead; gastroenterology; ophthalmology, where the strongest known disease association (\emph{CFH} Y402H, OR 2.50) is paired with a failed drug; and musculoskeletal disease, a concordance case with the instrument and the drug on the same protein.""")
rep(r"""IGF1-CRC$^\text{b}$ & Onco & 1.12 & 1.22 (1.09--1.36) & 0.110 & Causal & Failed & Gen.-only & $\times$ \\""",
    r"""IGF1-CRC$^\text{b}$ & Onco & 1.12 & 1.22 (1.09--1.36) & 0.110 & Supp. & Failed & Gen.-only & $\times$ \\""")
rep(r"""Eos/IL5-Asthma$^\text{d}$ & Resp & non-triv.$^\dagger$ & 1.50 (1.25--1.80) & 0.223 & Causal & Appr. & Conc. & $\checkmark$ \\""",
    r"""Eos/IL5-Asthma$^\text{d}$ & Resp & non-triv.$^\dagger$ & 1.50 (1.25--1.80) & 0.223 & Supp. & Appr. & Conc. & $\checkmark$ \\""")
rep(r"""SGLT2-HF$^\text{g}$ & Metab & 1.75 & 0.44 (0.26--0.76) & 0.452 & Causal$^\ddagger$ & Appr. & Conc. & $\checkmark$ \\
Urate-Gout$^\text{g2}$ & Metab & 3.20 & 5.00 (3.50--8.00) & 0.887 & Causal & Appr. & Conc. & $\checkmark$ \\""",
    r"""SGLT2-HF$^\text{g}$ & Metab & 1.75 & 0.44 (0.26--0.76) & 0.452 & Supp.$^\ddagger$ & Appr. & Conc. & $\checkmark$ \\
Urate-Gout$^\text{g2}$ & Metab & 3.20 & 5.00 (3.50--8.00) & 0.887 & Supp. & Appr. & Conc. & $\checkmark$ \\""")
rep(r"""Sclerostin-Frac$^\text{m}$ & MSK & 0.55 & 0.59 (0.54--0.66) & 0.291 & Causal & Appr. & Conc. & $\checkmark$ \\""",
    r"""Sclerostin-Frac$^\text{m}$ & MSK & 0.55 & 0.59 (0.54--0.66) & 0.291 & Supp. & Appr. & Conc. & $\checkmark$ \\""")
rep(r"""Drug: sirukumab (anti-IL-6) failed Phase~II for treatment-resistant MDD.""",
    r"""Drug: sirukumab (anti-IL-6) failed Phase~II for treatment-resistant MDD, the readout declared in advance (Amendment~2); the family is the one scored family without a Phase~III readout.""")
rep(r"""it meets both criteria of the rule and is scored in the registered analysis, and is set aside in the revised primary analysis.""",
    r"""it meets both criteria of the rule and is scored in the registered analysis, and is set aside in the 28-family sensitivity analysis.""")
extension_narr = cut(r"""\paragraph{Oncology: vitamin~D as a cancer-prevention MR-discordant mechanism.}""", r"""\paragraph{Extension summary.}""")
rep(r"""The extension adds 10 scored families and 4 construct-limited. Combined with the original 22, the registered rule classifies 24/32 scored families correctly (pre-registered: 18/22, 81.8\%, CI 61.5--92.7\%; combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$, cluster-level $p = 0.005$; \S\ref{sec:stats}). The extension classified 6/10 correctly (60.0\%, CI 31.3--83.2\%) and was not statistically significant when considered alone (binomial $p = 0.38$, permutation $p = 0.55$); it is therefore treated as an extension analysis rather than independent confirmation of the framework. The drop between tiers is not statistically significant (Fisher exact $p = 0.22$); the two tiers should be interpreted separately. The revised primary analysis, specified after the registered analysis, scores 23/28 (\S\ref{sec:revised_primary}). All eight misses under the registered rule are assigned to boundary classes by the criteria in Table~\ref{tab:criteria}; the classes are hypothesis-generating (Table~\ref{tab:provenance}).""",
    r"""The extension adds 10 scored families and 4 construct-limited. The extension classified 6/10 correctly (60.0\%, CI 31.3--83.2\%) and was not statistically significant when considered alone (binomial $p = 0.38$, permutation $p = 0.55$); it is therefore treated as an extension analysis rather than independent confirmation of the framework. The drop between tiers is not statistically significant (Fisher exact $p = 0.22$); the two tiers should be interpreted separately.""")

# --- new subsection: accuracy across domains, with the interpretation Reviewer 5 asked for
accuracy = r"""
\subsection{Accuracy across domains}
\label{sec:accuracy}

Under the registered rule, 24 of 32 scored families are classified correctly (75.0\%; one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$, cluster-level $p = 0.005$; \S\ref{sec:stats}): 18/22 in the original three domains (81.8\%, CI 61.5--92.7\%) and 6/10 in the blind extension. Across neuroepidemiology and cardiometabolic disease, which share the same OBS construct, 14 of 15 scored families are correct (permutation $p = 0.001$); autoimmune disease contributes 4/7. The 28-family sensitivity analysis specified after the registered analysis scores 23/28 (82.1\%; \S\ref{sec:sensitivity_set}); it removes three misses and no hit, so it cannot lower the figure, and it is reported after the registered count for that reason. All eight misses under the registered rule are assigned to boundary classes by the criteria in Table~\ref{tab:criteria}; the classes are preliminary generative hypotheses (Table~\ref{tab:provenance}).

Two features of the design bear on how these figures are read. The rule is blind to the sign of every estimate (\S\ref{sec:rule}): it asks whether each leg registers a non-trivial effect, never whether the two legs agree on direction. Sclerostin-Fracture shows what this costs. Its observational and MR legs are oriented to opposite exposures and score as concordant because both stored odds ratios fall below 1; a sign-aware rule would classify the family as discordant, predict failure, and be contradicted by romosozumab's approval, giving 23/32 (71.9\%). Second, the original 27 families were assembled from well-known development programs before the selection procedure was written down, with the trial outcomes public, so selection influenced by knowledge of outcomes cannot be excluded for that set. The 10 extension families were declared blind and are the only families protected against this, and on their own they do not reach significance. The overall figure therefore rests mainly on the tier whose selection was not blind. A candidate-family screen against an external universe (\S\ref{sec:robustness}) measures how much of that universe the scored families cover.
"""

# --- Stage 2 / taxonomy block edits (moved into the "Failure modes" subsection)
stage2 = stage2.replace(
    r"""\subsection{Stage~2: Retrospective analysis including RCT evidence}
\label{sec:stage2}

Adding RCT evidence to the etiologic classification reveals which concordant families nonetheless produce drug failures---the translation-gap signature. Amyloid-AD exemplifies this: concordant etiologic evidence, but RCT $d = 0.04$ against etiologic $d > 0.80$ (Table~\ref{tab:stage2}).""",
    r"""\subsection{Failure modes}
\label{sec:two_modes}

Adding RCT evidence to the etiologic classification (Stage~2) shows which concordant families nonetheless produce drug failures---the translation-gap signature. Amyloid-AD exemplifies this: concordant etiologic evidence, but RCT $d = 0.04$ against etiologic $d > 0.80$ (Table~\ref{tab:stage2}).""")
stage2 = stage2.replace(
    r"""The key revelation from adding RCT evidence: Amyloid-AD's near-zero RCT effect ($d = 0.04$) against its strong observational signal ($d = 0.86$) is the signature of a translation-gap mechanism. Etiologic concordance predicted success; 12 of 14 drugs failed. This gap between etiologic concordance and interventional failure is invisible without RCT evidence.

""", "")
assert r"\label{sec:two_modes}" in stage2 and "key revelation" not in stage2
taxonomy = taxonomy.replace(
    r"""\subsection{Failure-mode taxonomy}
\label{sec:two_modes}

The two-stage analysis distinguishes three ways mechanisms fail. Only mechanism-bypass was fully pre-specified before the corresponding miss was observed (Table~\ref{tab:provenance}), so the categories are hypothesis-generating rather than established mechanistic classifications:""",
    r"""The two-stage analysis distinguishes three ways mechanisms fail. Only mechanism-bypass was fully pre-specified before the corresponding miss was observed (Table~\ref{tab:provenance}), so the categories are preliminary generative hypotheses rather than established mechanistic classifications:""")
taxonomy = taxonomy.replace(
    r"""The concordance rule classifies these as concordant (predicting success); only interventional evidence reveals the gap. Example: Amyloid-AD.""",
    r"""The concordance rule classifies these as concordant (expected success); only interventional evidence reveals the gap. Example: Amyloid-AD.""")
taxonomy = taxonomy.replace(
    r"""The classes remain hypothesis-generating.}""",
    r"""The classes are preliminary generative hypotheses.}""")
taxonomy = taxonomy.replace(
    r"""Small effect & Null by criterion (b) only & Approved""",
    r"""Small effect & Null by criterion (b) only & Approved""")
taxonomy = taxonomy.replace(
    r"""Exposure mismatch & Causal & Failed & Instrument indexes""",
    r"""Exposure mismatch & Supp. & Failed & Instrument indexes""")
taxonomy = taxonomy.replace(
    r"""Translation gap & Causal & Failed & Instrument and drug act""",
    r"""Translation gap & Supp. & Failed & Instrument and drug act""")
taxonomy = taxonomy.replace(
    r"""The practical implication: a null MR signal for a risk-encoding drug target is a strong negative signal, since the observational association has no causal support. A positive MR signal is necessary but insufficient---the mechanism is real, but translation is not guaranteed, and the match between the MR instrument and the drug's mechanism of action must be evaluated separately.""",
    r"""On this reading, a null MR signal for a risk-encoding drug target is a negative signal, since the observational association has no causal support, and a supportive MR signal is necessary but insufficient: the mechanism is real, translation is not guaranteed, and the match between the MR instrument and the drug's mechanism of action has to be assessed separately. Whether the reading holds is a question for prospective readouts.""")
assert "Supp. & Failed & Instrument indexes" in taxonomy and "preliminary generative hypotheses.}" in taxonomy and "On this reading" in taxonomy

# provenance table and the two-way-split paragraph move from Robustness into Failure modes
provenance = cut(r"""\paragraph{Boundary class provenance.}""", r"""\paragraph{Accuracy by MR instrument type.}""")
provenance = provenance.replace(
    r"""The five named sub-classes are interpretive proposals on $n = 8$.""",
    r"""The five named sub-classes are preliminary generative hypotheses on $n = 8$.""")
provenance = provenance.replace(
    r"""This provenance should calibrate how much weight each boundary class receives: pre-specified boundaries are confirmatory evidence; post-hoc boundaries are hypotheses for future testing.""",
    r"""This provenance should calibrate how much weight each boundary class receives: the one pre-specified boundary was tested on one family; the post-hoc boundaries are hypotheses for future testing.""")
assert "preliminary generative hypotheses on $n = 8$" in provenance and "tested on one family" in provenance
two_way = cut(r"""\paragraph{Status of the two-way split.}""", r"""\section{Discussion}""")

# --- robustness paragraph edits
rep(r"""The $d = 0.10$ threshold is not optimal on the scored set---it sits at the lower edge of a stable plateau---but it was chosen a priori on Cohen's grounds and we do not move it. The lower end of that plateau has since been tested out of sample and was not supported: IL-6R was registered in advance as causal at $d = 0.08$ and null at $d = 0.10$, and ZEUS failed (\S\ref{par:prospective}). Above $d = 0.1027$, Anti-CD20-MS flips to discordant (predicting failure for four approved drugs), and accuracy degrades monotonically.""",
    r"""The $d = 0.10$ threshold is not optimal on the scored set---it sits at the lower edge of a stable plateau---but it was chosen a priori on Cohen's grounds and we do not move it. The lower end of that plateau has since been tested out of sample and was not supported: IL-6R was registered in advance as supportive at $d = 0.08$ and null at $d = 0.10$, and ZEUS failed (\S\ref{par:prospective}). Above $d = 0.1027$, Anti-CD20-MS flips to discordant (an expected failure for four approved drugs), and accuracy degrades monotonically.""")
rep(r"""accuracy under the registered rule is 13/16 per-SD, 4/7 per-allele, 5/5 per-unit, 1/1 per-genotype and 1/3 for null signals where the contrast is irrelevant; under the revised primary analysis, 13/15, 4/5, 5/5, 1/1 and 0/2.""",
    r"""accuracy under the registered rule is 13/16 per-SD, 4/7 per-allele, 5/5 per-unit, 1/1 per-genotype and 1/3 for null signals where the contrast is irrelevant; under the 28-family sensitivity analysis, 13/15, 4/5, 5/5, 1/1 and 0/2.""")
rep(r"""is classified as genetic-only rather than concordant, but both rules predict success for this family, so the invariance holds.""",
    r"""is classified as genetic-only rather than concordant, but both rules expect success for this family, so the invariance holds.""")
rep(r"""and differ only in domain, gene target, instrument label, and drug outcome. Two of the 24 correct classifications are therefore one piece of evidence counted in two domains; merging the families gives 23/31 (74.2\%). The permutation test and the cross-domain comparison treat families as distinct observations, which these two are not.""",
    r"""and differ in domain, gene target, instrument label, the MR interval (CRP carries one; IL-1$\beta$-CVD does not), and drug outcome (no benefit; failed). Two of the 24 correct classifications rest on the same observational estimate and the same null MR magnitude; merging the families gives 23/31 (74.2\%). HDL/CETP and Niacin/HDL are identical on every evidence field and are merged in the granularity analysis above. The permutation test and the cross-domain comparison treat families as distinct observations, which these pairs are not.""")
rep(r"""gives $p = 0.005$ over 28 clusters under the registered rule and $p = 0.0002$ over 25 clusters under the revised primary analysis.""",
    r"""gives $p = 0.005$ over 28 clusters under the registered rule and $p = 0.0002$ over 25 clusters under the 28-family sensitivity analysis.""")
rep(r"""\paragraph{Accuracy by MR instrument type.} Families using \emph{cis}-pQTL instruments (8/8 correct, 100\%) and polygenic scores (5/5 correct, 100\%) outperform those using coding variants (5/8, 62.5\%) and biomarker GWAS (6/11, 54.5\%).""",
    r"""\paragraph{Accuracy by MR instrument type.} Families using \emph{cis}-pQTL instruments and polygenic scores (5/5 correct) outperform those using coding variants (5/8, 62.5\%) and biomarker GWAS; the \emph{cis}-pQTL and biomarker-GWAS counts are reported in Supplementary Table~S1 with the IL6-MDD instrument recorded as biomarker GWAS.""")
rep(r"""\paragraph{Revised primary analysis.}
\label{sec:revised_primary}
Three changes to the scored set were specified after the registered analysis, each after the outcomes were known: excluding IGF1-CRC, whose MR estimate is for colorectal cancer risk while the Phase~III programs treated non-small-cell lung cancer, Ewing sarcoma and pancreatic cancer; setting aside Complement-GA and Serotonin-MDD, whose genetic leg is an association rather than an MR estimate; and counting CRP and IL-1$\beta$-CVD, which carry identical evidence on every field, once. Applied together they define the revised primary analysis: 23/28 (82.1\%; exact outcome-permutation $p = 0.0006$, cluster-level $p = 0.0002$, one-sided exact binomial $p < 0.001$; 17/21 in the original domains and 6/7 in the extension, the latter not significant alone at permutation $p = 0.14$). Each change alone gives 24/31 (77.4\%), 24/30 (80.0\%) and 23/31 (74.2\%). The registered analysis, 24/32 (75.0\%; permutation $p = 0.005$ at family and cluster level, binomial $p = 0.004$), is retained as a prespecified robustness analysis; every exclusion of a miss raises accuracy above it, and the only figure below it is the merge alone, which removes a hit. An always-approve rule scores 17/32 under the registered set and 16/28 under the revised set, which is why the permutation test rather than the 50\% binomial is primary (\S\ref{sec:stats}).

None of the three excluded families meets the registered exclusion criterion of construct limitation, under which instrument and drug act on different molecular entities, and the registration states that no qualifying family is removed once its outcome is known. Both analyses are therefore reported rather than one replacing the other, and the departure is recorded as Amendment~4 to the registration. The three excluded families are all misclassifications under the registered rule, so the change removes misses rather than hits, and the failure-mode assignments of the remaining misses are unchanged.""",
    r"""\paragraph{Sensitivity analysis: the 28-family set.}
\label{sec:sensitivity_set}
Three changes to the scored set were specified after the registered analysis, each with the outcomes known: excluding IGF1-CRC, whose MR estimate is for colorectal cancer risk while the Phase~III programs treated non-small-cell lung cancer, Ewing sarcoma and pancreatic cancer; setting aside Complement-GA and Serotonin-MDD, whose genetic leg is an association rather than an MR estimate; and counting CRP and IL-1$\beta$-CVD once. Applied together they define a 28-family set: 23/28 (82.1\%; exact outcome-permutation $p = 0.0006$, cluster-level $p = 0.0002$, one-sided exact binomial $p < 0.001$; 17/21 in the original domains and 6/7 in the extension, the latter not significant alone at permutation $p = 0.14$). Each change alone gives 24/31 (77.4\%), 24/30 (80.0\%) and 23/31 (74.2\%). None of the three excluded families meets the registered exclusion criterion of construct limitation, and the registration states that no qualifying family is removed once its outcome is known, so the registered analysis (24/32) is the primary result and this set is a sensitivity analysis. Every exclusion of a miss raises accuracy above the registered figure, and the only figure below it is the merge alone, which removes a hit. An always-approve rule scores 17/32 under the registered set and 16/28 under this one, which is why the permutation test rather than the 50\% binomial is primary (\S\ref{sec:stats}). The failure-mode assignments of the remaining misses are unchanged.""")

# --- Rewrite the narratives, shortened, into one subsection ---------------------------------
narratives = r"""
\subsection{Case narratives}
\label{sec:narratives}

The paragraphs below interpret individual families. They are the material the failure-mode reading (\S\ref{sec:two_modes}) is drawn from, and none of them enters an accuracy figure.

\paragraph{Metabolic-AD (MR-discordant mechanism).} T2D associates with AD in observational cohorts (RR~1.53, $d = 0.24$); MR finds no causal effect (OR~1.01, $d = 0.006$). The gap is consistent with confounding by shared risk factors (obesity, inflammation, vascular disease). Semaglutide (EVOKE/EVOKE+) and pioglitazone failed.

\paragraph{HRT-AD (MR-discordant mechanism).} A meta-analysis of 16 observational studies shows HRT protective against AD (OR~0.67, $d = 0.22$; \cite{song2020}); MR for estradiol is null (OR~1.00; \cite{barth2025}); WHIMS found HRT \emph{increased} dementia risk (HR~1.76; \cite{shumaker2003}). The protective observational signal is the healthy-user bias that \citet{hernan2008} identified in the HRT-cardiovascular discrepancy, and the rule flags the family from etiologic evidence alone.

\paragraph{Anti-CD20-MS (concordance).} Per-SD higher circulating FCRL3 is protective against MS on MR (OR~0.83, $d = 0.103$; \cite{lin2023}); pooled non-randomized studies give a relapse hazard ratio of 0.14 for rituximab against interferon beta or glatiramer acetate ($d = 1.084$; \cite{hu2019}), an estimate plausibly inflated by natalizumab-switch cohorts. All four anti-CD20 drugs in the holdout were approved. Two caveats attach. The instrument captures circulating FCRL3-mediated B-cell biology, while ocrelizumab depletes CD20$^+$ B cells by antibody-dependent cellular cytotoxicity, a related but distinct mechanism. And the MR $d = 0.1027$ clears the threshold by 0.0027; nothing in the evidence separates 0.1027 from 0.099, so the classification is better read as undetermined than as correct (\S\ref{sec:limitations}).

Regulatory status and mechanistic support come apart here. Rituximab supplies the observational estimate and is widely used off-label in MS, with substantial clinical and registry evidence behind it, yet it carries no MS indication, while ocrelizumab, ofatumumab, and ublituximab do \cite{brancati2021rituximab}. Health technology assessments in three European countries reach differing conclusions about therapeutic value for agents holding equivalent regulatory status \cite{gozzo2023htams}. Approval is the outcome variable throughout this paper and indexes target validity only imperfectly: a family can carry strong mechanistic and clinical evidence for a compound that no sponsor takes through registration. The same applies in the other direction: Complement-GA is scored on lampalizumab's failure while pegcetacoplan and avacincaptad pegol were approved for the same indication, and Amyloid-AD contains two approvals among fourteen programs.

\paragraph{Amyloid-AD (translation gap).}
\label{sec:amyloid}
Amyloid-AD carries observational evidence (amyloid PET positivity predicts AD conversion; HR~3.74 and 10.2) and genetic evidence (\emph{APOE4} heterozygous OR~3.46, homozygous OR~15.65; \emph{APP}/\emph{PSEN} mutations cause autosomal dominant AD) but no MR estimate. The \emph{APOE4} association qualifies as a GEN leg under the pooling rule of \S\ref{sec:rule}, and the family was not entered in the classified set; scored on that leg it is concordant, an expected success, against a Phase~III record in which 12 of 14 amyloid-targeting drugs failed, so it would be a miss (\S\ref{sec:robustness} reports the count). Within the family, production-pathway inhibitors (BACE and gamma-secretase) failed 8/8; immunotherapy failed 4/6, and the two approvals (lecanemab, donanemab) slowed decline on CDR-SB by 27--35\%. RCT $d = 0.04$ against etiologic $d > 0.80$ is the translation-gap pattern: the mechanism is involved in pathogenesis, and clearing amyloid at the stage of clinical disease does not reverse the downstream pathology. Why is a hypothesis; that the gap exists is what the data show.

\paragraph{Cardiometabolic MR-discordant mechanisms.} HDL/CETP, niacin/HDL, homocysteine/B-vitamins, and CRP each have moderate-to-strong observational associations with cardiovascular risk and null MR estimates, and all four produced drug failures: torcetrapib, dalcetrapib, and evacetrapib (CETP inhibitors); AIM-HIGH and HPS2-THRIVE (niacin); B-vitamin trials; and canakinumab's null primary endpoint in CANTOS despite lowering CRP. Niacin/HDL and HDL/CETP share the same MR evidence \cite{voight2012} and appear as separate families because the drug classes differ; merging them gives 23/31 (74.2\%). Uric acid is ambiguous: the observational association is weak (OR 1.07 per SD, $d = 0.04$), conventional MR suggests an effect (OR 1.18, 1.08--1.29) while pleiotropy-robust Egger MR does not (OR 1.05, 0.92--1.20; \cite{white2016}), and allopurinol found no cardiovascular benefit in ALL-HEART. A null-concordance rule (both legs negligible $\to$ expected failure) would handle this case.

\paragraph{Autoimmune effector targets.} The three autoimmune misses, TNF-$\alpha$, IL-17, and CTLA-4, each target a cytokine or receptor elevated as a consequence of active disease, not a germline-encoded risk factor. MR instruments capture lifetime genetic predisposition and are null for these effectors because the elevation is downstream of onset; the drugs work because they suppress active-disease pathology. The three hits, IL-23R, JAK/STAT4, and FCRL3, are risk-encoding loci where the causal direction runs locus$\to$disease, which is what an MR instrument is built to capture. IL-4R$\alpha$-AD is construct-limited: dupilumab blocks the shared IL-4/IL-13 receptor, and IL-13, not IL-4, is the dominant lesional ligand. The boundary can be stated before a screen is run: soluble effector targets are expected to show null MR whatever the drug does, and risk-encoding loci are expected to show supportive MR.

\paragraph{Oncology.} Vitamin~D is the cleanest MR-discordant mechanism in the set: an inverse observational association with colorectal cancer (highest vs.\ lowest quintile OR~0.80; \cite{keum2014vitdobscancer}), null MR across cancer subtypes with 80+ instruments \cite{ong2021vitdcancer}, and no reduction in cancer incidence in VITAL (HR~0.96; \cite{manson2019vital}). The exposure is the same as in vitamin~D-MS; the MR leg differs, supportive for MS and null for cancer. IGF-1 shows the translation-gap pattern: MR supports a causal effect on colorectal cancer risk (OR~1.22, $d_{\text{MR}} = 0.110$; \cite{larsson2020igfcancer}) with a trivial observational leg ($d_{\text{OBS}} = 0.063$; \cite{rinaldi2019igfobs}), and IGF-1R inhibitors failed Phase~III in non-small-cell lung cancer \cite{langer2014figitumumab}, Ewing sarcoma \cite{juergens2023ganitumab} and pancreatic cancer. The MR estimate and the trials concern different indications, and either the indication mismatch or the translation gap would produce the miss. Estrogen and breast cancer define the small-effect boundary: the MR effect is real but small per SD of estradiol (OR~1.03, 1.01--1.06; \cite{shi2023estradiolBC}), below the $d = 0.10$ floor, while tamoxifen's complete receptor blockade is a far larger perturbation and is approved for chemoprevention \cite{cuzick2015tamoxifen}.

\paragraph{Respiratory.} Eosinophil count is elevated in severe asthma (estimated SMD~$\approx$~0.80; \cite{wagener2022eosinophils}) and genetically determined count raises asthma risk on MR (OR~1.50 per SD; \cite{han2020eosinophilasthma}); mepolizumab and benralizumab are approved \cite{pavord2012dream}. Unlike TNF in RA, eosinophils are both a risk factor and a disease effector, and the risk-encoding component is what the instrument captures. IL-4R$\alpha$ (dupilumab \cite{busse2019dupilumab}) and TSLP (tezepelumab \cite{menzies2022tezepelumab}) are construct-limited for want of a drug-target MR estimate with a confidence interval.

\paragraph{Metabolic and endocrine disease.} SGLT2-HF is concordant on a \emph{cis}-eQTL drug-target MR estimate (OR~0.44; \cite{zheng2020sglt2mr}) and empagliflozin and dapagliflozin are approved, but the MR evidence is inconsistent across instrument selections \cite{sglt2paradox2025}: the classification would flip under alternative instruments, and accuracy is 23/31 with the family excluded. GLP-1R is construct-limited because published drug-target MR reports mediation through BMI and T2D rather than a direct estimate for the approved indications. Urate-gout is a clean concordance case with the instrument and the drug on the same pathway (MR OR~5.0 per SD; \cite{li2019uratemr}; allopurinol and febuxostat approved).

\paragraph{Psychiatry.} IL-6/MDD: CRP elevation associates with depression (SMD 0.15; \cite{howren2009}) and the MR estimate on general CRP instruments is null (OR 1.01, 0.99--1.04); sirukumab, which neutralizes the IL-6 ligand, failed Phase~II for treatment-resistant MDD. The instrument, the receptor variants the registration named, and the ligand the drug binds are three different perturbations of one pathway. Serotonin/MDD defines the mechanism-bypass boundary, declared in advance: 5-HTTLPR associates with depression (OR 1.08; \cite{clarke2010serotonin}) below the threshold, the umbrella review of \citet{moncrieff2022} finds no consistent support for the serotonin hypothesis, and SSRIs are approved, working through pathways the instrument does not index. A disorder-level version of this domain had failed earlier: applied to six disorder-level families (31 drugs, 24 classifiable), the rule reached 58\% with zero specificity, because Depression and Schizophrenia each contain eight to nine mechanism classes and are both discordant at the disorder level. The framework requires mechanism-level families.

\paragraph{Ophthalmology.} \emph{CFH} Y402H is among the strongest disease-variant associations known (per-allele OR 2.50; \cite{thakkinstian2006}) and complement activation products are elevated in AMD \cite{reynolds2009}. Lampalizumab, against Factor~D, failed both Phase~III trials, while pegcetacoplan (C3) and avacincaptad pegol (C5) were approved for the same indication in 2023: the pathway is druggable at another node, which is the translation-gap pattern declared in advance for this family.

\paragraph{Musculoskeletal disease.} Higher circulating sclerostin accompanies fewer fractures in the MINOS cohort (HR 0.55; \cite{szulc2014}), a direction the source attributes to reverse causation; the \emph{SOST} \emph{cis}-MR estimate for genetically proxied sclerostin inhibition lowers fracture risk (OR 0.59; \cite{bovijn2020}); romosozumab is approved. Both stored odds ratios fall below 1, so the rule returns concordance, although oriented to sclerostin the two legs oppose each other. The classification follows from sign-blindness (\S\ref{sec:accuracy}), not from agreement on direction.
"""

# --- reassemble Results: insert accuracy + ablation + (robustness stays) + failure modes + narratives
# Ablation goes right after the extension summary; then accuracy; robustness (already in place); then failure modes; then narratives.
rep(r"""\subsection{Robustness analyses}
\label{sec:robustness}""",
    accuracy.rstrip("\n") + "\n\n" + ablation.rstrip("\n") + "\n\n" + r"""\subsection{Robustness analyses}
\label{sec:robustness}""")
failure_modes = (stage2.rstrip("\n") + "\n\n" + amyloid_sub.split("\n", 2)[2].strip() if False else stage2.rstrip("\n")) + "\n\n" + taxonomy.rstrip("\n") + "\n\n" + provenance.rstrip("\n") + "\n\n" + two_way.rstrip("\n") + "\n"
del amyloid, amyloid_sub, neuro_cases, boundary, cardio_narr, autoimmune_narr, extension_narr  # rewritten above
rep(r"""\section{Discussion}""", failure_modes + "\n" + narratives.rstrip("\n") + "\n\n\\FloatBarrier\n\\section{Discussion}")

# =============================================================================
# Discussion
# =============================================================================
rep(r"""Our ablation result is consistent with and extends this body of work. Stripped to its predictive core, the cross-design rule reduces to MR-null status---recovering the Nelson/Minikel finding on a different family set organized by mechanism rather than by indication. The key differences are scope and resolution. Nelson et al.\ and Minikel et al.\ operate at the program level (does genetic support predict approval?) using binary classification (genetic support present or absent). Our analysis operates at the mechanism-family level and adds a second stage: after prediction, diagnosis. Three specific extensions follow.""",
    r"""Our ablation result is consistent with and extends this body of work. Stripped to its classifying core, the cross-design rule reduces to MR-null status---recovering the Nelson/Minikel finding on a different family set organized by mechanism rather than by indication. The differences are scope and resolution. Nelson et al.\ and Minikel et al.\ operate at the program level (does genetic support predict approval?) using binary classification (genetic support present or absent). Our analysis operates at the mechanism-family level and adds a second stage: after classification, diagnosis. Three specific extensions follow.""")
rep(r"""Our analysis supplies a mechanistic account for null-MR successes (effector-neutralization and mechanism-bypass: the drug works through pathways the MR instrument does not capture) and for causal-MR failures (translation gaps and exposure mismatches: the target is real, and the drug is insufficient or misaligned). Each category implies a different pipeline response.""",
    r"""Our analysis supplies a mechanistic account for MR-null successes (effector-neutralization and mechanism-bypass: the drug works through pathways the MR instrument does not capture) and for MR-supportive failures (translation gaps and exposure mismatches: the target is real, and the drug is insufficient or misaligned). These accounts are preliminary generative hypotheses.""")
rep(r"""Third, the boundary classes identify where MR-based screening is expected to produce systematic errors, rather than random misclassification. Effector-neutralization targets (soluble cytokines elevated in active disease) will always show null MR regardless of drug efficacy; mechanism-bypass targets (SSRIs acting through neuroplasticity rather than serotonin transport) operate outside the instrument's causal window. These are not failures of the genetic evidence paradigm---they are predictable scope limitations that can be flagged before a screening decision is made.""",
    r"""Third, the boundary classes propose where MR-based screening would produce systematic rather than random errors. Effector-neutralization targets (soluble cytokines elevated in active disease) are expected to show null MR regardless of drug efficacy; mechanism-bypass targets (SSRIs acting through neuroplasticity rather than serotonin transport) operate outside the instrument's causal window. If the proposals hold, these are scope limitations that can be flagged before a screening decision is made.""")
rep(r"""\subsection{MR predicts outcomes; cross-design evidence diagnoses failure modes}

The cross-design framework's contribution is diagnostic and exploratory, not predictive. MR-only says ``this target will fail''; it cannot say \emph{why}.""",
    r"""\subsection{Classification and diagnosis}

The cross-design framework's contribution is diagnostic and exploratory. MR-only says ``this target is expected to fail''; it cannot say \emph{why}.""")
rep(r"""Each has direct practical consequences: MR-discordant targets should be deprioritized, translation gaps call for different therapeutic strategies, and exposure mismatches call for interventions that recapitulate the causal exposure window.""",
    r"""Each would have a different practical consequence if the reading were validated: MR-discordant targets deprioritized, translation gaps met with different therapeutic strategies, and exposure mismatches met with interventions that recapitulate the causal exposure window.""")
rep(r"""These limitations reinforce the one-sided screening interpretation: a null MR signal is informative for risk-encoding targets (the observational association lacks causal support) and uninformative for effector targets. A positive MR signal is necessary for confidence in a risk-encoding target and irrelevant for effector targets.""",
    r"""These limitations reinforce the one-sided screening reading: a null MR signal is informative for risk-encoding targets (the observational association lacks causal support) and uninformative for effector targets. A supportive MR signal is necessary for confidence in a risk-encoding target and irrelevant for effector targets.""")
rep(r"""Accuracy by instrument type (\S\ref{sec:robustness}) points the same way. Families instrumented by a \emph{cis}-pQTL, where the instrument acts on the drug's proximal target protein, are classified correctly 8/8, and polygenic scores 5/5; coding variants reach 5/8 and biomarker GWAS 6/11, and all eight misclassifications fall in those two classes.""",
    r"""Accuracy by instrument type (\S\ref{sec:robustness}) points the same way. Every family instrumented by a \emph{cis}-pQTL, where the instrument acts on the drug's proximal target protein, or by a polygenic score is classified correctly; coding variants reach 5/8, and all eight misclassifications fall in the coding-variant and biomarker-GWAS classes.""")
# Screening tool: toned down
rep(r"""\subsection{MR as a screening tool}

The ablation result suggests a screening role for MR in drug development; the decision tree below is a hypothesis for prospective testing, not a validated tool. Before committing to Phase~III for a novel target, the pattern would be read as follows:

\begin{enumerate}
\item If the MR causal signal is null while the observational association is positive $\to$ the observational association lacks causal support $\to$ elevated Phase~III failure risk for a risk-encoding target.
\item If MR evidence is causal $\to$ the mechanism is likely real $\to$ proceed, but causal MR does not guarantee interventional success (amyloid-AD, IGF-1-CRC).
\item If the target is a soluble disease effector (cytokine, receptor elevated in active disease) $\to$ MR is expected to be null regardless of drug efficacy $\to$ do not use MR as a negative screen.
\item If the per-SD MR effect is small ($d < 0.10$) but statistically significant, and the drug produces a pharmacological perturbation much larger than one SD of the genetic exposure $\to$ the MR-null classification reflects scale rather than the absence of a causal pathway $\to$ assess instrument-drug scale alignment before screening.
\item If the drug's mechanism of action operates through pathways the MR instrument does not capture (e.g., SSRIs acting via neuroplasticity rather than serotonin transport) $\to$ MR is uninformative $\to$ this is a mechanism-bypass boundary, not evidence against the pathway.
\end{enumerate}

This is a one-sided screen with three caveats: a null MR signal is a strong negative indicator for risk-encoding targets, but it is uninformative for effector-neutralization targets, for small-effect causal pathways where the drug acts at a different scale than the genetic instrument, and for mechanism-bypass targets where the drug acts through pathways the instrument does not capture. Figure~\ref{fig:screening} presents this decision tree as a flowchart.

The pre-screening step---distinguishing effector from risk-encoding targets---can be operationalized using existing databases.""",
    r"""\subsection{A screening hypothesis for prospective testing}

The ablation result is consistent with a screening role for MR in drug development. The decision tree below is a hypothesis for prospective testing, not a validated tool, and nothing in this paper establishes that reading it before a Phase~III commitment would improve the decision. If it were tested, the pattern would be read as follows:

\begin{enumerate}
\item If the MR signal is null while the observational association is positive $\to$ the observational association lacks causal support $\to$ the hypothesis expects elevated Phase~III failure risk for a risk-encoding target.
\item If MR evidence is supportive $\to$ the mechanism is likely real $\to$ supportive MR does not guarantee interventional success (amyloid-AD, IGF-1-CRC).
\item If the target is a soluble disease effector (cytokine, receptor elevated in active disease) $\to$ MR is expected to be null regardless of drug efficacy $\to$ MR would not serve as a negative screen.
\item If the per-SD MR effect is small ($d < 0.10$) but statistically significant, and the drug produces a pharmacological perturbation much larger than one SD of the genetic exposure $\to$ the MR-null classification reflects scale rather than the absence of a causal pathway $\to$ instrument-drug scale alignment would be assessed first.
\item If the drug's mechanism of action operates through pathways the MR instrument does not capture (e.g., SSRIs acting via neuroplasticity rather than serotonin transport) $\to$ MR is uninformative $\to$ this is a mechanism-bypass boundary, not evidence against the pathway.
\end{enumerate}

The hypothesis is one-sided, with three caveats: a null MR signal would be a negative indicator for risk-encoding targets, and uninformative for effector-neutralization targets, for small-effect causal pathways where the drug acts at a different scale than the genetic instrument, and for mechanism-bypass targets where the drug acts through pathways the instrument does not capture. Figure~\ref{fig:screening} presents the decision tree as a flowchart. The three boundary classes it relies on are post-hoc (Table~\ref{tab:provenance}), so the tree inherits their status.

The pre-screening step---distinguishing effector from risk-encoding targets---could be operationalized using existing databases.""")
rep(r"""\caption{Screening decision tree for MR-based drug-target evaluation. A null MR signal indicates an MR-discordant mechanism for risk-encoding targets, but is uninformative for effector-neutralization and mechanism-bypass targets. A causal MR signal is necessary but insufficient---translation-gap targets have real mechanisms but therapeutically insufficient drugs.}""",
    r"""\caption{Screening decision tree, stated as a hypothesis for prospective testing. Under the hypothesis, a null MR signal indicates an MR-discordant mechanism for risk-encoding targets and is uninformative for effector-neutralization and mechanism-bypass targets; a supportive MR signal is necessary but insufficient, since translation-gap targets have real mechanisms and therapeutically insufficient drugs. The boundary classes the tree relies on are post-hoc (Table~\ref{tab:provenance}).}""")
rep(r"""The boundary classes identified here---specifying where MR screening fails---could inform future regulatory frameworks for genetics-informed target selection.""",
    r"""The boundary classes proposed here---specifying where MR screening would fail---could, if validated, inform future regulatory frameworks for genetics-informed target selection.""")
# Figure 3 tikz labels: "causal"
rep(r"""\node[decision] (mr) {MR signal\\causal?};""", r"""\node[decision] (mr) {MR signal\\supportive?};""")
rep(r"""\draw[arr] (mr) -- node[above right, font=\footnotesize] {Causal} (rct);""", r"""\draw[arr] (mr) -- node[above right, font=\footnotesize] {Supportive} (rct);""")
# Etiologic concordance section: "Drugs targeting amyloid clearance mostly fail" ok. Nothing.
# Limitations: author-estimated values (R4), ascertainment, extension provenance, revised -> sensitivity
rep(r"""The etiologic-only analysis classifies 8 of 38 holdout drugs---the remainder fall in families without multi-type etiologic evidence. The analysis is powered to demonstrate proof-of-concept (7/8 correct), not to establish population-level accuracy. The retrospective analysis including RCT evidence is circular for families whose RCT arm derives from holdout drugs---it should be interpreted as concordance, not prediction.""",
    r"""The etiologic-only analysis classifies 8 of 38 holdout drugs---the remainder fall in families without multi-type etiologic evidence. The analysis is powered to demonstrate proof-of-concept (7/8 correct), not to establish population-level accuracy. The retrospective analysis including RCT evidence is circular for families whose RCT arm derives from holdout drugs---it should be interpreted as concordance, not as a test of the rule.""")
rep(r"""All ten fall on the non-trivial side, the closest at an estimated $0.15$ against a $0.10$ floor. The invariance result independently establishes that the observational leg carries no discriminative information, so these entries cannot affect a classification even in principle. The estimates and their sources remain in the supplementary classification file.""",
    r"""All ten fall on the non-trivial side, the closest at an estimated $0.15$ against a $0.10$ floor. The invariance result rests on the near-constancy of the observational class, and in seven scored families that class rests on these estimates: had any of the seven been read as trivial, the family would have moved to the null-concordance or genetic-only cell. The invariance is therefore established on the estimates as made, not independently of them. The estimates and their sources remain in the supplementary classification file.""")
rep(r"""\paragraph{Ascertainment.} Mechanism families were selected from well-known programs, introducing possible outcome-influenced selection. The prospective predictions (Lp(a), IL-6) and pre-registered extensions mitigate this concern. The IL-6 prediction has resolved in the direction registered under this paper's threshold; Lp(a)HORIZON remains open.""",
    r"""\paragraph{Ascertainment.} The original 27 mechanism families were selected from well-known programs with the trial outcomes public, introducing possible outcome-influenced selection, and no systematic enumeration of candidate families preceded that selection. The prospective predictions (Lp(a), IL-6) and the blind extensions are the parts of the design protected against it, and the extension does not reach significance on its own (\S\ref{sec:accuracy}). The IL-6 prediction has resolved in the direction registered under this paper's threshold; Lp(a)HORIZON remains open.""")
rep(r"""\paragraph{Family-level vs.\ drug-level accuracy.} The 24/32 (75\%) accuracy is computed at the mechanism-family level. Families contain different numbers of drugs: Anti-CD20-MS maps to four approved drugs; Amyloid-AD maps to fourteen (twelve failed, two approved). A misclassified family with many drugs produces more incorrect drug-level predictions than one with a single drug.""",
    r"""\paragraph{Family-level vs.\ drug-level accuracy.} The 24/32 (75\%) accuracy is computed at the mechanism-family level. Families contain different numbers of drugs: Anti-CD20-MS maps to four approved drugs; Amyloid-AD maps to fourteen (twelve failed, two approved). A misclassified family with many drugs produces more incorrect drug-level classifications than one with a single drug.""")
rep(r"""Every declared family was scored regardless of outcome under the registered rule, and none was dropped from it post hoc. The extension accuracy (6/10, 60\%) does not reach statistical significance in isolation""",
    r"""Every declared family was scored regardless of outcome under the registered rule, and none was dropped from it. The extension accuracy (6/10, 60\%) does not reach statistical significance in isolation""")

# =============================================================================
# Conclusions (R5: taxonomy out; registered primary)
# =============================================================================
rep(r"""The predictive work reduces to MR-null status. The cross-design framework's contribution is diagnostic and exploratory: for the eight misclassified families it proposes a mechanistic account of each miss, which the MR screen does not carry.

Five families have null MR signals yet succeed clinically (effector-neutralization, small-effect and mechanism-bypass). Three families have causal MR signals yet fail clinically (translation gaps and exposure mismatches). This two-way partition follows from the MR $d$ axis by construction: under a binary rule a null-MR miss is necessarily a clinical success and a causal-MR miss necessarily a clinical failure. The finer five-class taxonomy---effector-neutralization, small-effect, translation-gap, exposure-mismatch, and mechanism-bypass---offers mechanistic hypotheses for each type of miss. These labels are proposals on $n = 8$, grounded in pharmacological reasoning but requiring prospective replication (Table~\ref{tab:provenance}).

A null MR signal is a strong negative indicator for a risk-encoding target: the observational association lacks causal support. A positive MR signal is necessary but insufficient: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises, and the MR screen alone does not raise them. These results rest on 32 scored families under the registered rule and 28 under the revised primary analysis, of which 10 (7 under the revised analysis) were added in a blind extension that does not reach significance on its own, and on a boundary taxonomy fitted to eight misses. The taxonomy is retrospective and hypothesis-generating. The framework is an exploratory proof of concept requiring prospective validation on unseen Phase~III readouts before it informs development decisions.""",
    r"""The classifying work reduces to MR-null status. The cross-design framework's contribution is diagnostic and exploratory: for the eight misclassified families it proposes a mechanistic account of each miss, which the MR screen does not carry.

Five families have null MR signals yet succeed clinically, and three have supportive MR signals yet fail. This two-way partition follows from the MR $d$ axis by construction: under a binary rule an MR-null miss is necessarily a clinical success and an MR-supportive miss necessarily a clinical failure. The five finer boundary classes read from these misses (\S\ref{sec:two_modes}) are preliminary generative hypotheses on $n = 8$ and are not among the conclusions of this paper.

A null MR signal is a negative indicator for a risk-encoding target: the observational association lacks causal support. A supportive MR signal is necessary but insufficient: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises, and the MR screen alone does not raise them. These results rest on 32 scored families under the registered rule, 27 of them selected before the selection procedure was written down and 10 added in a blind extension that does not reach significance on its own; a 28-family sensitivity analysis gives the same reading. The framework is an exploratory proof of concept requiring prospective validation on unseen Phase~III readouts before it informs development decisions.""")
rep(r"""The MR-only and cross-design rules produce identical classifications across all 32 scored families---an invariance that holds at every threshold tested ($d = 0.05$ to $0.20$) and reflects a selection effect: mechanisms reaching Phase~III have non-trivial observational support by construction.""",
    r"""The MR-only and cross-design rules produce identical classifications across all 32 scored families---an invariance that holds at every threshold tested ($d = 0.05$ to $0.20$) and reflects a selection effect: mechanisms reaching Phase~III have non-trivial observational support by construction. The rule classifies 24 of 32 correctly under the registered analysis.""")

# =============================================================================
# Back matter (R4: statements consistent)
# =============================================================================
rep(r"""are available at \url{https://github.com/elliottower/cross-design-evidence-discordance} at tag \texttt{frontiers-revision-3}, the repository state underlying this revision, with a permanent archive at Zenodo (DOI: \url{https://doi.org/10.5281/zenodo.21227354}). Pre-registration commits with SHAs, and the amendment recording the revised primary analysis, are documented in the repository. No novel datasets were generated.""",
    r"""are available at \url{https://github.com/elliottower/cross-design-evidence-discordance} at tag \texttt{frontiers-revision-4}, with a permanent archive at Zenodo (DOI: \url{https://doi.org/10.5281/zenodo.21227354}). Pre-registration commits with SHAs, and the amendments recording the sensitivity analysis and the procedures reported in \S\ref{sec:robustness}, are documented in the repository. No novel datasets were generated.""")
rep(r"""\subsection*{Funding}
This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.""",
    r"""\subsection*{Funding}
The author declares that no financial support was received for the research or publication of this article.""")
rep(r"""\subsection*{Acknowledgements}
Not applicable.

\subsection*{Conflict of Interest Statement}
The author declares no competing interests.

\subsection*{Use of AI-Assisted Technologies}
Claude (Anthropic) was used as a writing and analysis assistant during manuscript preparation. The author directed all analytical decisions, verified all numerical results against source data, and takes full responsibility for the content. The classification rule, effect-size data, and all reported results were independently validated by the author. No AI tool is listed as an author.""",
    r"""\subsection*{Acknowledgements}
Claude Code (Anthropic, \url{https://claude.ai/code}; versions 2.1.207 to 2.1.280, running the models Claude Opus 4.6, Claude Opus 5, Claude Fable 5 and Claude Fable 5.1) was used to draft and edit manuscript text, to write and debug analysis code, and to prepare submission materials. Perplexity (Perplexity AI, \url{https://www.perplexity.ai}, web application) was used to check the statistical design of the preregistration amendments before they were frozen, and for literature search; every source it returned was retrieved and read before citation. The author made all methodological and analytical decisions, reviewed the generated code and its outputs, checked the reported numbers, quotations, citations and references against their sources, and takes full responsibility for the content. All hypotheses, pre-registered predictions, interpretations and conclusions are the author's own. No AI tool is listed as an author, and no AI-generated content was used as a primary data source.

\subsection*{Conflict of Interest Statement}
The author declares no competing interests.""")

rep(r"""the revised primary analysis with its permutation tests (\texttt{run\_revised\_primary.py}),""",
    r"""the 28-family sensitivity analysis with its permutation tests (\texttt{run\_revised\_primary.py}),""")

# =============================================================================
# Residual "predict" wording in text that survived the block moves
# =============================================================================
rep(r"""\caption{Ablation analysis. Four rules applied to all 32 scored families across ten domains. ``Fail $\checkmark$'' = failures correctly predicted; ``Appr $\checkmark$'' = approvals correctly predicted.""",
    r"""\caption{Ablation analysis. Four rules applied to all 32 scored families across ten domains. ``Fail $\checkmark$'' = failures correctly classified; ``Appr $\checkmark$'' = approvals correctly classified.""")
rep(r"""For MR-discordant mechanisms, the mismatch is immaterial---the MR signal is null on any estimand.""",
    r"""For MR-discordant mechanisms, the mismatch is immaterial---the MR signal is null on any estimand.""")
rep(r"""This holds at every threshold tested ($d = 0.05$ to $0.20$). The observational leg carries no information about outcomes; its value is diagnostic.""",
    r"""This holds at every threshold tested ($d = 0.05$ to $0.20$). The observational leg carries no information about outcomes; its value is diagnostic.""")

rep(r"""With the numbers of predicted and actual failures fixed, the null distribution is hypergeometric""",
    r"""With the numbers of expected and actual failures fixed, the null distribution is hypergeometric""")
rep(r"""To test whether the observational leg contributes predictive power beyond MR alone, we compared four classification rules""",
    r"""To test whether the observational leg changes any classification beyond MR alone, we compared four classification rules""")
rep(r"""a sign-aware rule would classify the family as discordant, predict failure, and be contradicted by romosozumab's approval""",
    r"""a sign-aware rule would classify the family as discordant, an expected failure, and be contradicted by romosozumab's approval""")
rep(r"""CRP (cardiometabolic) and IL-1$\beta$-CVD (autoimmune) carry identical values on every evidence field---$d_{\text{OBS}} = 0.174$, MR OR~1.00, $d_{\text{MR}} = 0.000$, null MR, qualitative discordance, predicted failure, scored correct---and differ in domain""",
    r"""CRP (cardiometabolic) and IL-1$\beta$-CVD (autoimmune) carry the same values on every field the rule reads---$d_{\text{OBS}} = 0.174$, MR OR~1.00, $d_{\text{MR}} = 0.000$, null MR, qualitative discordance, expected failure, scored correct---and differ in domain""")
rep(r"""The coarse two-way split (null-MR misses vs.\ causal-MR misses) follows from the binary decision rule by construction.""",
    r"""The coarse two-way split (MR-null misses vs.\ MR-supportive misses) follows from the binary decision rule by construction.""")
rep(r"""Every null-MR miss is a clinical success and every causal-MR miss is a clinical failure. This correspondence is an identity rather than a measurement: under a binary rule a null-MR family is predicted to fail, so a misclassified one must have succeeded, and the converse holds for causal-MR families.""",
    r"""Every MR-null miss is a clinical success and every MR-supportive miss is a clinical failure. This correspondence is an identity rather than a measurement: under a binary rule an MR-null family is expected to fail, so a misclassified one must have succeeded, and the converse holds for MR-supportive families.""")

# ---- float placement (Reviewer 4: pages 43-44 mis-compiled). Every table was a top-only float;
# the cardio table landed six pages after its text and the extension table ran off the margin.
rep(r"\begin{table}[t]", r"\begin{table}[htbp]", count=text.count(r"\begin{table}[t]"))
rep(r"\begin{figure}[t]", r"\begin{figure}[htbp]", count=text.count(r"\begin{figure}[t]"))
rep(r"""\label{tab:extension}
\small
\begin{tabular}{llllllllc}""", r"""\label{tab:extension}
\footnotesize
\resizebox{\textwidth}{!}{%
\begin{tabular}{llllllllc}""")
rep(r"""Sclerostin-Frac$^\text{m}$ & MSK & 0.55 & 0.59 (0.54--0.66) & 0.291 & Supp. & Appr. & Conc. & $\checkmark$ \\
\bottomrule
\end{tabular}""", r"""Sclerostin-Frac$^\text{m}$ & MSK & 0.55 & 0.59 (0.54--0.66) & 0.291 & Supp. & Appr. & Conc. & $\checkmark$ \\
\bottomrule
\end{tabular}}""")
rep(r"""\label{tab:cardio}
\small""", r"""\label{tab:cardio}
\footnotesize""")
rep(r"""\subsection{Accuracy across domains}""", "\\FloatBarrier\n\\subsection{Accuracy across domains}")
rep(r"""\subsection{Case narratives}""", "\\FloatBarrier\n\\subsection{Case narratives}")

# ---- extension table: the source notes made the float taller than a page; they become a notes
# paragraph directly after the float. Provenance table: SHA column ran off the margin.
i = text.index(r"\label{tab:extension}")
j = text.index(r"\end{tabular}}", i) + len(r"\end{tabular}}")
k = text.index(r"\end{table}", j)
notes = text[j:k]
assert notes.strip().startswith(r"\vspace{1mm}") and notes.strip().endswith("}"), notes[:80]
body = notes.strip()[len(r"\vspace{1mm}"):].strip()
assert body.startswith(r"{\footnotesize") and body.endswith("}")
body = body[len(r"{\footnotesize"):-1].strip()
text = text[:j] + "\n" + text[k:]
end_float = text.index(r"\end{table}", j) + len(r"\end{table}")
text = text[:end_float] + "\n\n\\noindent{\\footnotesize \\textit{Notes to Table~\\ref{tab:extension}.} " + body + "}\n" + text[end_float:]
applied += 1
rep(r"""\label{tab:provenance}
\small
\begin{tabular}{lllll}""", r"""\label{tab:provenance}
\footnotesize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lllll}""")
rep(r"""Mechanism-bypass & Pre-specified & Amendment~2 blind declaration & Serotonin-MDD & \texttt{12ea0ed} \\
\bottomrule
\end{tabular}""", r"""Mechanism-bypass & Pre-specified & Amendment~2 blind declaration & Serotonin-MDD & \texttt{12ea0ed} \\
\bottomrule
\end{tabular}}""")

# Frontiers: AI use is acknowledged "in the acknowledgements section ... and the methods section if applicable".
rep(r"""The procedure is deterministic, requires no training data, and can be executed by hand with a calculator.""",
    r"""The procedure is deterministic, requires no training data, and can be executed by hand with a calculator. The analysis code implementing it was written with Claude Code (see Use of AI-Assisted Technologies) and was inspected, tested and run by the author.""")

rep(r"""ET conceived the study, assembled the evidence catalog, designed and implemented the classification rule, performed all analyses, and wrote the manuscript.""",
    r"""ET conceived the study, assembled the evidence catalog, designed and implemented the classification rule, performed and verified all analyses, and wrote the manuscript.""")
rep(r"""(see Use of AI-Assisted Technologies)""", r"""(see Acknowledgements)""")

# =============================================================================
# Checks
# =============================================================================
for bad in ["zombie", "revised primary", "requested during", "peer review", "the reviewer", "reviewer 1", "reviewer 4", "reviewer 5", "reviewers", "this revision", "sec:revised_primary", "sec:stage2}"]:
    hits = [m.start() for m in re.finditer(re.escape(bad), text, re.I)]
    assert not hits, f"{bad!r} survives at offsets {hits[:5]}"
for bad in ["Pre-Registered"]:
    hits = [m.start() for m in re.finditer(re.escape(bad), text)]
    assert not hits, f"{bad!r} survives at offsets {hits[:5]}"
for lab in ["sec:two_modes", "sec:amyloid", "sec:narratives", "sec:accuracy", "sec:sensitivity_set", "sec:robustness", "sec:ablation", "sec:autoimmune", "sec:extension", "sec:cardio", "sec:stage1", "par:prospective", "tab:provenance", "tab:criteria", "tab:stage2"]:
    assert text.count(f"\\label{{{lab}}}") == 1, lab
    assert text.count(f"\\ref{{{lab}}}") >= 1, f"no ref to {lab}"
assert text.count(r"\label{sec:boundary}") == 0 and text.count(r"\ref{sec:boundary}") == 0
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, f"abstract is {words} words"
# every \cite key that survived must still be cited in the bib (checked by bibtex at build); every \cite in v25 that was
# in a cut block is either re-used in the narratives or listed here as intentionally dropped.
dropped_ok = set()
v25 = SRC.read_text(encoding="utf-8")
old_keys = set(re.findall(r"\\cite[tp]?\{([^}]*)\}", v25))
new_keys = set(re.findall(r"\\cite[tp]?\{([^}]*)\}", text))
lost = {k for grp in old_keys - new_keys for k in grp.split(",")} - {k for grp in new_keys for k in grp.split(",")} - dropped_ok
assert not lost, f"citations lost in the cut: {sorted(lost)}"

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
