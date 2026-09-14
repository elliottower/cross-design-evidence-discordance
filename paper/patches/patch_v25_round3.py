"""v24 -> v25: answer Reviewer 1's round-3 report (9 Sep 2026), all twelve points.

Run:  uv run --no-project python paper/patches/patch_v25_round3.py

Every edit is an exact-string replacement that must match exactly once in the
source; the script aborts on the first miss and writes nothing. v24 is not
touched. Numbers come from analysis/revised_primary_analysis/revised_primary_results.json.

What changes, by reviewer point:
  1  framing: "exploratory diagnostic framework"; observational leg adds no prediction
  2  Table tab:criteria gives observable assignment criteria; categories hypothesis-generating
  3  accuracy stratified by MR contrast; contrast column added to Supplementary Table S1
  4  GEN leg called causal only for MR-instrumented families; two association families set aside
  5  IGF1-CRC excluded from the revised primary analysis
  6  CRP and IL-1b-CVD counted once; cluster-level permutation test
  7  outcome-permutation test (exact, hypergeometric) is primary; 50% binomial retained beside it
  8  Figure 1 redrawn as Algorithm 1 (figures/fig1_flowchart_v2.tex)
  9  "Pre-Registered" dropped from the title; what was and was not registered stated in the abstract
 10  extension tier reported as an extension analysis, not confirmation
 11  "zombie mechanism" -> "MR-discordant mechanism" everywhere, figures included
 12  conclusions: exploratory proof of concept requiring prospective validation
Also: the Limitations said 15 per-SD families where the registered scale table gives 16.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v24_round2.tex"
DST = HERE.parent / "paper_v25_round3.tex"

text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old: str, new: str, count: int = 1) -> None:
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:120]}"
    text = text.replace(old, new)
    applied += 1


# ---- title (point 9) -------------------------------------------------------
rep(r"""\title{Diagnosing Drug Failure Modes from Cross-Design Evidence:
A Pre-Registered Evaluation Across Ten Disease Domains}""",
    r"""\title{Diagnosing Drug Failure Modes from Cross-Design Evidence Across Ten Disease Domains}""")

# ---- abstract (points 1, 9, 10, 12): the v24 abstract with the reviewer's
# four requests folded in. v24 sat at the 350-word cap, so three v24 clauses
# that the new sentences make redundant are dropped: the near-constant-variable
# clause, the two-stage-design sentence, and the partition sentence.
rep(r"""\begin{abstract}
\textbf{Background:}
Mendelian randomization (MR) evidence predicts drug success, but when a drug fails despite genetic support---or succeeds without it---the MR screen alone cannot explain why. We asked whether comparing observational, MR, and RCT evidence can diagnose distinct failure modes.

\textbf{Methods:}
We assembled 41 mechanism families across ten disease domains. Observational and MR effect sizes were standardized to Cohen's $d$ with a fixed $d = 0.10$ threshold. A deterministic rule classified each family by the agreement pattern between observational and MR evidence. A two-stage design separated diagnostic from predictive content by assembling etiologic evidence before examining RCT outcomes.

\textbf{Results:}
MR-only and the cross-design rule produced identical classifications with zero McNemar disagreements across all 32 scored families, because 31 of 32 have non-trivial observational support, making the observational variable near-constant. The pre-registered rule classified 18/22 families correctly (81.8\%, 95\% Wilson CI 61.5--92.7\%; one-sided exact binomial against 50\% chance accuracy, $p = 0.002$). A blind extension added 14 families in seven domains (6/10 correct, 60.0\%, CI 31.3--83.2\%, $p = 0.38$); combined 24/32 ($p = 0.004$). The eight misses divide 5 and 3 by MR status. The direction follows from the binary rule---a miss under null MR is a clinical success, a miss under causal MR is a clinical failure---so the split itself carries no independent evidence. The mechanistic account of each side does: translation gaps and exposure mismatch for the three causal-MR failures, effector-neutralization and mechanism-bypass for the five null-MR successes. Five boundary classes offer mechanistic hypotheses.

\textbf{Conclusions:}
The cross-design framework's contribution is diagnostic, not predictive. MR-null status accounts for all predictive power, replicating the genetic-support finding of Nelson et al.\ and Minikel et al. The observational leg adds failure-mode resolution: translation gaps, exposure mismatches, and effector-neutralizations each demand different pipeline responses. Drug failures partition into targets lacking MR causal support and targets carrying it, and the observational leg supplies the mechanistic account of each. On 32 families with a taxonomy fitted to eight misses, this is proof of concept: the extension tier does not reach significance alone, and prospective validation on unseen readouts is required.
\end{abstract}""",
    r"""\begin{abstract}
\textbf{Background:}
Mendelian randomization (MR) evidence predicts drug success, but when a drug fails despite genetic support---or succeeds without it---the MR screen alone cannot explain why. We tested a preregistered classification rule and separately explored a diagnostic taxonomy for interpreting its errors.

\textbf{Methods:}
We assembled 41 mechanism families across ten disease domains. Observational and MR effect sizes were standardized to Cohen's $d$ with a fixed $d = 0.10$ threshold, and a deterministic rule classified each family from the observational and MR evidence pattern. The rule and threshold, the extension families, and two prospective predictions were preregistered before their corresponding outcomes were examined; selection of the original 27 families and the failure-mode taxonomy were not. Genetic-association families were analyzed separately from MR families.

\textbf{Results:}
MR-only and the cross-design rule produced identical classifications with zero McNemar disagreements across all 32 scored families, because 31 of 32 have non-trivial observational support. Under the registered analysis the rule classified 24/32 families correctly (75.0\%; outcome-permutation $p = 0.005$): 18/22 in the original domains (81.8\%, 95\% CI 61.5--92.7\%) and 6/10 in the blind extension (60.0\%, CI 31.3--83.2\%), the latter not significant alone and not independent confirmation. Under the revised primary analysis requested during peer review, which excludes one indication-mismatched family and two association-only families and counts duplicated evidence once, 23/28 were classified correctly (82.1\%; $p = 0.0006$). The eight misses under the registered rule divide 5 and 3 by MR status; the direction is fixed by the rule, the mechanistic account of each side is not: translation gaps and exposure mismatch for the three causal-MR failures, effector-neutralization and mechanism-bypass for the five null-MR successes. Five boundary classes are retrospective and hypothesis-generating.

\textbf{Conclusions:}
The observational leg added no predictive information beyond MR status, consistent with the genetic-support findings of Nelson et al.\ and Minikel et al. Its contribution is diagnostic: the cross-design comparison generates mechanistic hypotheses about why the binary MR classification misses, each implying a different pipeline response. The framework is an exploratory proof of concept requiring prospective validation on unseen readouts before use in drug-development decisions.
\end{abstract}""")

# ---- introduction and contributions (points 1, 2, 11) ----------------------
rep(r"""reveals three failure modes that MR alone cannot separate: zombie mechanisms, translation gaps, and exposure mismatches. All produce failed drugs; what differs is \emph{why}.""",
    r"""reveals three failure modes that MR alone cannot separate: MR-discordant mechanisms, translation gaps, and exposure mismatches. All produce failed drugs; what differs is \emph{why}. The framework is exploratory: the failure modes are read from the misses rather than predicted by the rule, and \S\ref{sec:two_modes} records which were declared before the miss they explain was observed.""")

rep("a three-way diagnostic taxonomy emerges from the two-stage analysis: zombie mechanisms, translation gaps, and exposure mismatches.",
    "a three-way diagnostic taxonomy is read from the two-stage analysis: MR-discordant mechanisms, translation gaps, and exposure mismatches.")

rep(r"Five finer-grained boundary classes are proposed as mechanistic hypotheses on $n = 8$ misses (Table~\ref{tab:provenance}).",
    r"Five finer-grained boundary classes are proposed as hypothesis-generating categories on $n = 8$ misses, with assignment criteria in Table~\ref{tab:criteria} and provenance in Table~\ref{tab:provenance}.")

rep("Threshold sensitivity, leave-one-domain-out cross-validation, alternative granularity schemes, and instrument independence audit confirm the result is not driven by threshold choice, any single domain, or family-definition decisions.",
    "Threshold sensitivity, leave-one-domain-out cross-validation, alternative granularity schemes, and instrument independence audit confirm the result is not driven by threshold choice, any single domain, or family-definition decisions. A revised primary analysis requested during peer review, which excludes three families and counts two once, gives 23/28 and is reported beside the registered 24/32 throughout.")

# ---- family selection (points 4, 5, 6) --------------------------------------
rep("(4)~Every family satisfying (2) is scored, and none is dropped once its outcome is known.",
    r"(4)~Every family satisfying (2) is scored under the registered rule. A revised primary analysis, requested during peer review after outcomes were known, additionally excludes one family on indication mismatch and two whose genetic leg is an association rather than an MR estimate, and counts two families that share identical evidence once (\S\ref{sec:revised_primary}); the registered count is reported beside it throughout, and the departure from the registration is recorded in Amendment~4.")

# ---- evidence classification (point 4) --------------------------------------
rep("Within etiologic evidence, MR and GWAS studies were pooled into a single ``genetic/causal'' (GEN) evidence type for the concordance rule.",
    "Within etiologic evidence, MR and GWAS studies were pooled into a single genetic (GEN) evidence type for the registered concordance rule.")
rep("Both are misclassified. Where this paper calls a pooled GEN signal causal, the term carries its MR sense for families instrumented by MR and an associational sense for these two.",
    r"Both are misclassified. The GEN leg is called causal only for families instrumented by MR; for these two families it is called associated, and the revised primary analysis (\S\ref{sec:revised_primary}) sets them aside so that every family it scores has an MR estimate on the genetic leg.")

# ---- MR scaling (point 3) ---------------------------------------------------
rep(r"depends on which contrast the source study reported as much as on the size of the underlying effect (\S\ref{sec:limitations}).",
    r"depends on which contrast the source study reported as much as on the size of the underlying effect (\S\ref{sec:limitations}). The contrast of every scored family is a column of Supplementary Table~S1, and accuracy stratified by contrast is reported in \S\ref{sec:robustness}.")

# ---- unit of analysis (points 6, 11) ----------------------------------------
rep("a ``zombie mechanism'' names an evidence pattern attaching to the pathway, regardless of which drug targets it.",
    "an ``MR-discordant mechanism'' names an evidence pattern attaching to the pathway, regardless of which drug targets it.")
rep(r"(merging Niacin/HDL into HDL/CETP, splitting Amyloid-AD by sub-mechanism) in the robustness analyses (\S\ref{sec:robustness}).",
    r"(merging Niacin/HDL into HDL/CETP, splitting Amyloid-AD by sub-mechanism) in the robustness analyses (\S\ref{sec:robustness}). Families that share an MR instrument set are not independent observations; the permutation test in \S\ref{sec:stats} permutes outcomes at the level of the instrument cluster.")

# ---- failure taxonomy (points 2, 11) ----------------------------------------
rep("Three mechanistically defined failure modes follow from the two-stage analysis:",
    r"Three failure modes are read from the two-stage analysis. They are pharmacological interpretations of the misses rather than outputs of Algorithm~\ref{alg:discordance}; Table~\ref{tab:criteria} gives the observable criteria by which each miss is assigned, and Table~\ref{tab:provenance} records which classes were declared before the miss they explain was observed.")
rep(r"\textbf{Zombie mechanism}, formally an \emph{MR-discordant mechanism} (the informal name records that the observational association persists where the MR signal does not). Etiologic evidence is qualitatively discordant",
    r"\textbf{MR-discordant mechanism.} Etiologic evidence is qualitatively discordant")

# ---- new Methods subsection: statistical tests (points 6, 7) ---------------
rep(r"""\subsection{Ablation design}""",
    r"""\subsection{Statistical tests}
\label{sec:stats}

Accuracy is tested against two nulls. The registered test is a one-sided exact binomial against 50\% chance accuracy, which treats each family as an independent Bernoulli trial carrying no information about its outcome. That null ignores the outcome base rate (17 approvals and 15 failures among the 32 scored families, so a rule that always predicts approval scores 53\%) and the dependence among families that share an MR instrument set. The primary test in this revision is therefore an outcome-permutation test with the classification held fixed: drug outcomes are permuted across families, accuracy is recomputed, and the p-value is the fraction of permutations with accuracy at least the observed value. With the numbers of predicted and actual failures fixed, the null distribution is hypergeometric and the p-value is computed exactly; a Monte Carlo run of $10^5$ permutations is reported beside it. A cluster-level variant permutes one outcome label per instrument set, so families sharing an instrument move together. The binomial p-values are retained for comparison with the registered analysis. The analysis code is \texttt{run\_revised\_primary.py}.

\subsection{Ablation design}""")

# ---- Figure 1 (point 8) -----------------------------------------------------
rep(r"""\begin{figure}[t]
\centering
\includegraphics[width=0.85\textwidth]{figures/fig1_flowchart.pdf}""",
    r"""\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{figures/fig1_flowchart_v6.pdf}""")
rep(r"""\caption{\textbf{Classification procedure.}
For each mechanism family, observational and MR effect sizes are
standardized to Cohen's $d$ and classified independently against the
$d = 0.10$ threshold. The family-level classification follows from the
OBS$\times$MR combination: qualitative discordance (non-trivial OBS,
null MR) predicts failure; concordance predicts success.
Stage~1 uses etiologic evidence only; Stage~2 adds RCT outcomes to
diagnose failure modes.}""",
    r"""\caption{\textbf{Classification procedure (Algorithm~\ref{alg:discordance}).}
Each leg is standardized to Cohen's $d$ (Equation~\ref{eq:chinn}; per-allele MR estimates rescaled to per-SD) and classified on its own: the observational leg is non-trivial if $d_{\text{OBS}} \geq 0.10$, and the MR leg is causal if its confidence interval excludes the null and $d_{\text{MR}} \geq 0.10$. The family label is the OBS$\times$MR cell: qualitative discordance predicts failure, concordance and genetic-only predict success, and null concordance is ambiguous and unscored. No pooling or heterogeneity test enters the rule. Stage~1 uses etiologic evidence only; RCT outcomes enter in Stage~2, after classification, to score the prediction and to read the failure mode.}""")

# ---- accounting table caption (points 5, 6) ---------------------------------
rep(r"Extension domains (\S\ref{sec:extension}) add 14 families across seven disease domains in two blind amendments.}",
    r"Extension domains (\S\ref{sec:extension}) add 14 families across seven disease domains in two blind amendments. The revised primary analysis requested during peer review scores 28 of these 32 families, 23 correctly (\S\ref{sec:revised_primary}).}")

# ---- zombie -> MR-discordant, Results (point 11) ----------------------------
rep(r"\paragraph{Metabolic-AD (zombie mechanism).}", r"\paragraph{Metabolic-AD (MR-discordant mechanism).}")
rep(r"\paragraph{HRT-AD (zombie mechanism).}", r"\paragraph{HRT-AD (MR-discordant mechanism).}")
rep(r"& Zombie \\", r"& MR-disc. \\", count=5)
rep("is the strongest zombie signature in the dataset.", "is the strongest MR-discordant signature in the dataset.")
rep(r"\textbf{Zombie mechanisms} (caught by the concordance rule): the MR signal is null. The observational association reflects confounding or reverse causation.",
    r"\textbf{MR-discordant mechanisms} (caught by the concordance rule): the MR signal is null. The observational association is attributed to confounding or reverse causation.")
rep("The practical implication: a null MR signal for a drug target is a strong negative signal---the mechanism is likely a zombie.",
    "The practical implication: a null MR signal for a risk-encoding drug target is a strong negative signal---the evidence pattern is MR-discordant.")

# ---- criteria table (point 2), inserted before "The practical implication" --
rep("The practical implication: a null MR signal for a risk-encoding drug target",
    r"""\begin{table}[t]
\centering
\caption{Assignment criteria for the boundary classes. Each of the eight misses under the registered rule is assigned by reading the criteria in order, using fields of Supplementary Table~S1 (MR class, confidence interval, $d_{\text{MR}}$, instrument type) and the trial record. Two misses satisfy more than one criterion; the class the manuscript uses for each is the one declared in advance (Serotonin-MDD, Amendment~2) or read at the time of the miss (CTLA-4-RA), and the second criterion met is listed. The criteria make the assignment reproducible; they do not establish the classes, which remain hypothesis-generating.}
\label{tab:criteria}
\small
\begin{tabular}{p{2.6cm}p{1.7cm}p{1.4cm}p{6.0cm}p{2.8cm}}
\toprule
Class & MR class & Outcome & Criterion, read in this order & Misses \\
\midrule
Exposure mismatch & Causal & Failed & Instrument indexes lifelong exposure level; the intervention supplies the same exposure in adulthood & VitD-MS \\
Translation gap & Causal & Failed & Instrument and drug act on the same pathway in the same window; the trial reports target engagement without endpoint benefit. Indication mismatch between the MR estimate and the trial is flagged where present & IGF1-CRC (indication mismatch), Complement-GA \\
Small effect & Null by criterion (b) only & Approved & MR confidence interval excludes the null and $d_{\text{MR}} < 0.10$ & Estrogen-BC; also met by CTLA-4-RA and Serotonin-MDD \\
Effector neutralization & Null & Approved & Drug target is a mediator elevated in active disease, and the instrument is a biomarker-level or coding variant at the effector locus & TNF-$\alpha$-RA, IL-17-psoriasis, CTLA-4-RA \\
Mechanism bypass & Null & Approved & Declared in advance: the drug's efficacy is attributed in its own literature to pathways the instrumented exposure does not index & Serotonin-MDD \\
\bottomrule
\end{tabular}
\end{table}

The practical implication: a null MR signal for a risk-encoding drug target""")

# ---- Figure 2 (point 11) ----------------------------------------------------
rep(r"\includegraphics[width=\textwidth]{figures/fig2_failure_modes.pdf}",
    r"\includegraphics[width=\textwidth]{figures/fig2_failure_modes_v2.pdf}")
rep(r"""\textbf{a},~Zombie mechanisms: the observational association ($d = 0.24$
for Metabolic-AD) reflects confounding; the MR/genetic signal is null
($d = 0.006$).""",
    r"""\textbf{a},~MR-discordant mechanisms: the observational association ($d = 0.24$
for Metabolic-AD) is attributed to confounding or reverse causation; the MR/genetic signal is null
($d = 0.006$).""")

# ---- cardiometabolic section ------------------------------------------------
rep("several textbook ``zombie'' mechanisms have been documented independently of our framework.",
    "several textbook MR-discordant mechanisms have been documented independently of our framework.")
rep("The cardiometabolic zombie mechanisms (HDL, niacin, homocysteine, CRP, uric acid)",
    "The cardiometabolic MR-discordant mechanisms (HDL, niacin, homocysteine, CRP, uric acid)")
rep("Four zombie mechanisms---HDL/CETP, niacin/HDL, homocysteine/B-vitamins, and CRP---",
    "Four MR-discordant mechanisms---HDL/CETP, niacin/HDL, homocysteine/B-vitamins, and CRP---")
rep(r"bringing the total to 24/32 (75\%) across ten domains.",
    r"bringing the total to 24/32 (75\%) across ten domains under the registered rule and 23/28 (82.1\%) under the revised primary analysis (\S\ref{sec:revised_primary}).")

# ---- ablation (point 1) -----------------------------------------------------
rep(r"The ablation establishes that the cross-design rule's \emph{predictive} contribution reduces to MR-null status. The observational leg's value is \emph{diagnostic}:",
    r"The ablation establishes that the cross-design rule's \emph{predictive} contribution reduces to MR-null status; adding the observational leg improves prediction for no family at any threshold. The observational leg's value, where it has one, is \emph{diagnostic}:")

# ---- autoimmune -------------------------------------------------------------
rep(r"This is structurally different from zombie mechanisms: MR-discordant families target associations for which the genetic evidence supplies no causal support; effector-neutralization drugs",
    r"This is structurally different from MR-discordant mechanisms, where the observational association has no MR support; effector-neutralization drugs")

# ---- extension paragraphs ---------------------------------------------------
rep(r"""\paragraph{Oncology: vitamin~D as a cancer-prevention zombie.}
Vitamin~D is the cleanest oncology zombie.""",
    r"""\paragraph{Oncology: vitamin~D as a cancer-prevention MR-discordant mechanism.}
Vitamin~D is the cleanest MR-discordant mechanism in the oncology set.""")
rep("The pattern replicates the vitamin~D-MS zombie from the neuroepidemiology domain",
    "The pattern replicates the vitamin~D-MS miss from the neuroepidemiology domain")
rep("The zombie pattern is present on both legs here", "The MR-discordant pattern is present on both legs here")
rep(r"\paragraph{Psychiatry: IL-6 as a psychiatric zombie.}", r"\paragraph{Psychiatry: IL-6 as an MR-discordant mechanism.}")
rep("replicates the zombie pattern in a new disease domain.", "replicates the MR-discordant pattern in a new disease domain.")

# ---- extension summary (points 7, 10) ---------------------------------------
rep(r"""Combined with the original 22, the method classifies 24/32 scored families correctly (pre-registered: 18/22, 81.8\%, CI 61.5--92.7\%; extension: 6/10, 60.0\%, CI 31.3--83.2\%; combined $p = 0.004$). All accuracy $p$-values are one-sided exact binomial tests against a 50\% chance-accuracy null, computed as reported in Materials and Methods; the extension tier alone does not reach significance ($p = 0.38$). The drop between tiers is not statistically significant (Fisher exact $p = 0.22$); the two tiers should be interpreted separately. All eight misses across all domains fall into mechanistically predictable boundary classes (Table~\ref{tab:provenance}).""",
    r"""Combined with the original 22, the registered rule classifies 24/32 scored families correctly (pre-registered: 18/22, 81.8\%, CI 61.5--92.7\%; extension: 6/10, 60.0\%, CI 31.3--83.2\%; combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$; \S\ref{sec:stats}). The extension classified 6/10 correctly and was not significant when considered alone (binomial $p = 0.38$, permutation $p = 0.55$); it is therefore treated as an extension analysis rather than independent confirmation of the framework. The drop between tiers is not statistically significant (Fisher exact $p = 0.22$); the two tiers should be interpreted separately. The revised primary analysis requested during peer review scores 23/28 (\S\ref{sec:revised_primary}). All eight misses under the registered rule are assigned to boundary classes by the criteria in Table~\ref{tab:criteria}; the classes are hypothesis-generating (Table~\ref{tab:provenance}).""")

# ---- robustness: contrast stratification (point 3) --------------------------
rep(r"and JAK-STAT-RA ($d = 0.132$, flips at $d = 0.14$).",
    r"and JAK-STAT-RA ($d = 0.132$, flips at $d = 0.14$). Stratified by the contrast on which the MR estimate enters (Supplementary Table~S1, column \texttt{mr\_contrast}), accuracy under the registered rule is 13/16 per-SD, 4/7 per-allele, 5/5 per-unit, 1/1 per-genotype and 1/3 for null signals where the contrast is irrelevant; under the revised primary analysis, 13/15, 4/5, 5/5, 1/1 and 0/2. The per-allele and null-signal strata carry five of the eight misses, and the per-allele stratum is the one in which a fixed $d$ threshold is least interpretable; the cell sizes do not support a test.")

# ---- robustness: instrument independence (point 6) --------------------------
rep(r"the classification is unaffected, since $d = 0$ is null under criterion~(b) either way.",
    r"the classification is unaffected, since $d = 0$ is null under criterion~(b) either way. The cluster-level permutation test (\S\ref{sec:stats}), which moves the outcomes of families sharing an instrument set together, gives $p = 0.005$ over 28 clusters under the registered rule and $p = 0.0002$ over 25 clusters under the revised primary analysis.")

# ---- revised primary analysis replaces exclusion sensitivity (points 4-7) ---
rep(r"""\paragraph{Exclusion sensitivity.} Two exclusions bear on the scored set, neither registered, and both would raise accuracy. Registered: 24/32 (75.0\%, $p = 0.004$). Excluding IGF1-CRC on indication mismatch: 24/31 (77.4\%, $p = 0.002$). Excluding Complement-GA and Serotonin-MDD, whose genetic leg is an association rather than an MR estimate: 24/30 (80.0\%, $p < 0.001$). Both: 24/29 (82.8\%, $p < 0.001$). The registered figure is the most conservative of the four.""",
    r"""\paragraph{Revised primary analysis.}
\label{sec:revised_primary}
Three changes to the scored set were requested during peer review, each after the outcomes were known: excluding IGF1-CRC, whose MR estimate is for colorectal cancer risk while the Phase~III programs treated non-small-cell lung cancer, Ewing sarcoma and pancreatic cancer; setting aside Complement-GA and Serotonin-MDD, whose genetic leg is an association rather than an MR estimate; and counting CRP and IL-1$\beta$-CVD, which carry identical evidence on every field, once. Applied together they define the revised primary analysis: 23/28 (82.1\%; exact outcome-permutation $p = 0.0006$, one-sided exact binomial $p < 0.001$; 17/21 in the original domains and 6/7 in the extension, the latter not significant alone at permutation $p = 0.14$). Each change alone gives 24/31 (77.4\%), 24/30 (80.0\%) and 23/31 (74.2\%). The registered analysis, 24/32 (75.0\%; permutation $p = 0.005$, binomial $p = 0.004$), is retained as a prespecified robustness analysis and is the most conservative of these figures. An always-approve rule scores 17/32 under the registered set and 16/28 under the revised set, which is why the permutation test rather than the 50\% binomial is primary (\S\ref{sec:stats}).""")
rep(r"""IGF1-CRC pairs an MR estimate for colorectal cancer risk with Phase~III programs in non-small-cell lung cancer, Ewing sarcoma and pancreatic cancer. The registered exclusion criterion is construct limitation---instrument and drug acting on different molecular entities---which none of the three families meets, and applying a new criterion to a family after observing that it misses is the adjustment the two-stage design exists to prevent. All three are therefore retained. The failure-mode assignments are unchanged in each case: all three are misclassifications under the registered rule, so removing them removes misses rather than hits. Tests are one-sided exact binomial against 50\% chance accuracy throughout.""",
    r"""None of the three excluded families meets the registered exclusion criterion of construct limitation, under which instrument and drug act on different molecular entities, and the registration states that no qualifying family is removed once its outcome is known. The revision therefore reports both analyses rather than replacing one with the other, and the departure is recorded as Amendment~4 to the registration. The three excluded families are all misclassifications under the registered rule, so the change removes misses rather than hits, and the failure-mode assignments of the remaining misses are unchanged.""")

# ---- discussion -------------------------------------------------------------
rep(r"The cross-design framework's contribution is diagnostic, not predictive. MR-only says ``this target will fail''; it cannot say \emph{why}.",
    r"The cross-design framework's contribution is diagnostic and exploratory, not predictive. MR-only says ``this target will fail''; it cannot say \emph{why}.")
rep("separates zombie mechanisms (confounded OBS, null MR---no causal pathway is evidenced) from translation-gap mechanisms",
    "separates MR-discordant mechanisms (non-trivial OBS, null MR) from translation-gap mechanisms")
rep("zombies should be retired from pipelines,", "MR-discordant targets should be deprioritized,")
rep("but the concordance rule reaches the correct classification (zombie mechanism) because",
    "but the concordance rule reaches the correct classification (MR-discordant mechanism) because")
rep("a null MR signal is informative for risk-encoding targets (the mechanism is likely a zombie) and uninformative for effector targets.",
    "a null MR signal is informative for risk-encoding targets (the evidence pattern is MR-discordant) and uninformative for effector targets.")
rep("The ablation result points toward a practical screening role for MR in drug development. Before committing to Phase~III for a novel target:",
    "The ablation result suggests a screening role for MR in drug development; the decision tree below is a hypothesis for prospective testing, not a validated tool. Before committing to Phase~III for a novel target, the pattern would be read as follows:")
rep(r"$\to$ the mechanism is likely a zombie $\to$ high Phase~III failure risk.",
    r"$\to$ the evidence pattern is MR-discordant $\to$ elevated Phase~III failure risk for a risk-encoding target.")
rep(r"$\to$ MR-null classification does not indicate a zombie $\to$", r"$\to$ MR-null classification does not indicate an MR-discordant mechanism $\to$")
rep(r"$\to$ this is a mechanism-bypass boundary, not a zombie.", r"$\to$ this is a mechanism-bypass boundary, not an MR-discordant mechanism.")
rep(r"(zombie) {\textbf{Zombie}\\Retire target};", r"(disc) {\textbf{MR-discordant}\\Deprioritize target};")
rep(r"{No} (zombie);", r"{No} (disc);")
rep("A null MR signal indicates a zombie mechanism for risk-encoding targets,", "A null MR signal indicates an MR-discordant mechanism for risk-encoding targets,")
rep("than zombie-targeting drugs that reached market through non-MR-supported pathways",
    "than drugs against MR-discordant targets that reached market through non-MR-supported pathways")

# ---- limitations ------------------------------------------------------------
rep("Of 32 scored families, 15 use per-SD MR effects, 7 use per-allele, 5 use per-unit, 1 per-genotype, and 3 have null signals",
    "Of 32 scored families, 16 use per-SD MR effects, 7 use per-allele, 5 use per-unit, 1 per-genotype, and 3 have null signals")
rep("For zombie mechanisms, the mismatch is immaterial", "For MR-discordant mechanisms, the mismatch is immaterial")
rep("should be interpreted as a replication exercise mapping boundary conditions, not as a standalone confirmatory result.",
    "should be interpreted as a replication exercise mapping boundary conditions, not as a standalone confirmatory result or as independent confirmation of the framework.")

# ---- conclusions (points 1, 12) ---------------------------------------------
rep("The cross-design framework's contribution is diagnostic: for the eight misclassified families it supplies the mechanistic account of each miss, which the MR screen does not carry.",
    "The cross-design framework's contribution is diagnostic and exploratory: for the eight misclassified families it proposes a mechanistic account of each miss, which the MR screen does not carry.")
rep(r"""A null MR signal is a strong negative indicator---the evidence pattern is that of a zombie mechanism. A positive MR signal is necessary but insufficient: developers should ask whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation. Answering these questions requires the diagnostic framework; the MR screen alone cannot. These results rest on 32 scored families, of which 10 were added in a blind extension that does not reach significance on its own, and on a boundary taxonomy fitted to eight misses. They establish proof of concept for cross-design failure diagnosis. Prospective external validation on unseen Phase~III readouts is required before the framework informs development decisions.""",
    r"""A null MR signal is a strong negative indicator for a risk-encoding target---the evidence pattern is MR-discordant. A positive MR signal is necessary but insufficient: whether the target is a disease effector, whether the drug recapitulates the instrumented exposure, and whether the pharmacological perturbation exceeds the scale of genetic variation are the questions the diagnostic reading raises, and the MR screen alone does not raise them. These results rest on 32 scored families under the registered rule and 28 under the revised primary analysis, of which 10 (7 under the revised analysis) were added in a blind extension that does not reach significance on its own, and on a boundary taxonomy fitted to eight misses. The taxonomy is retrospective and hypothesis-generating. The framework is an exploratory proof of concept requiring prospective validation on unseen Phase~III readouts before it informs development decisions.""")

# ---- data availability ------------------------------------------------------
rep(r"the exclusion sensitivity analysis (\texttt{run\_sensitivity.py}), and the complete classification dataset (41 families with effect sizes, CIs, and sources; \texttt{cross\_design\_classification\_all\_41\_families\_v2.csv}) are available at \url{https://github.com/elliottower/cross-design-evidence-discordance} at tag \texttt{frontiers-revision-2}, the repository state underlying this revision,",
    r"the exclusion sensitivity analysis (\texttt{run\_sensitivity.py}), the revised primary analysis with its permutation tests (\texttt{run\_revised\_primary.py}), and the complete classification dataset (41 families with effect sizes, CIs, sources, MR contrast and instrument set; \texttt{cross\_design\_classification\_all\_41\_families\_v3.csv}) are available at \url{https://github.com/elliottower/cross-design-evidence-discordance} at tag \texttt{frontiers-revision-3}, the repository state underlying this revision,")
rep("Pre-registration commits with SHAs are documented in the repository.",
    "Pre-registration commits with SHAs, and the amendment recording the revised primary analysis, are documented in the repository.")

# ---- layout: Figure 3 leaves overlapped and ran off the page; Table 5 columns --
rep(r"""\begin{tikzpicture}[
    node distance=1.2cm and 2.0cm,""",
    r"""\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance=1.2cm and 2.0cm,""")
rep(r"""\end{tikzpicture}
\caption{Screening decision tree""",
    r"""\end{tikzpicture}}
\caption{Screening decision tree""")
rep(r"below left=1.4cm and 2.5cm of mr] (effector)", r"below left=1.4cm and 4.2cm of mr] (effector)")
rep(r"below right=1.4cm and 2.5cm of mr] (rct)", r"below right=1.4cm and 4.2cm of mr] (rct)")
rep(r"below left=1.2cm and 1.0cm of effector]", r"below left=1.2cm and 1.5cm of effector]")
rep(r"below right=1.2cm and 1.0cm of effector]", r"below right=1.2cm and 1.5cm of effector]")
rep(r"below left=1.2cm and 1.0cm of rct]", r"below left=1.2cm and 1.5cm of rct]")
rep(r"below right=1.2cm and 1.0cm of rct]", r"below right=1.2cm and 1.5cm of rct]")
rep(r"\begin{tabular}{p{2.6cm}p{1.7cm}p{1.4cm}p{6.0cm}p{2.8cm}}", r"\begin{tabular}{p{3.0cm}p{2.0cm}p{1.4cm}p{5.4cm}p{2.9cm}}")

# ---- after a sentence-level [duh] pass on the changed passages (13 Sep) --------
# 1. "most conservative" was false: the merge alone gives 23/31 = 74.2% < 75.0%.
rep(r"is retained as a prespecified robustness analysis and is the most conservative of these figures.",
    r"is retained as a prespecified robustness analysis; every exclusion of a miss raises accuracy above it, and the only figure below it is the merge alone, which removes a hit.")
# 2. The term swap turned "the mechanism is likely a zombie" into a tautology, and two
#    screening items used "MR-discordant" as a mechanism claim against its own definition.
rep("a strong negative signal---the evidence pattern is MR-discordant.",
    "a strong negative signal: the observational association has no causal support.")
rep("(the evidence pattern is MR-discordant) and uninformative for effector targets.",
    "(the observational association lacks causal support) and uninformative for effector targets.")
rep(r"$\to$ the evidence pattern is MR-discordant $\to$ elevated Phase~III failure risk for a risk-encoding target.",
    r"$\to$ the observational association lacks causal support $\to$ elevated Phase~III failure risk for a risk-encoding target.")
rep(r"$\to$ MR-null classification does not indicate an MR-discordant mechanism $\to$",
    r"$\to$ the MR-null classification reflects scale rather than the absence of a causal pathway $\to$")
rep(r"$\to$ this is a mechanism-bypass boundary, not an MR-discordant mechanism.",
    r"$\to$ this is a mechanism-bypass boundary, not evidence against the pathway.")
rep("A null MR signal is a strong negative indicator for a risk-encoding target---the evidence pattern is MR-discordant.",
    "A null MR signal is a strong negative indicator for a risk-encoding target: the observational association lacks causal support.")
# 3. Two reworded sentences lost their content.
rep("This is structurally different from MR-discordant mechanisms, where the observational association has no MR support; effector-neutralization drugs",
    "This is structurally different from MR-discordant mechanisms, where the observational association is attributed to confounding or reverse causation and no causal pathway is evidenced; effector-neutralization drugs")
rep("The pattern replicates the vitamin~D-MS miss from the neuroepidemiology domain, but with a critical difference:",
    "The exposure is the same as in the vitamin~D-MS family from the neuroepidemiology domain, but the MR leg differs:")
# 4. Two of my own additions that only repeat what the Data Availability statement and the abstract say.
rep(" A revised primary analysis requested during peer review, which excludes three families and counts two once, gives 23/28 and is reported beside the registered 24/32 throughout.", "")
rep(r" The analysis code is \texttt{run\_revised\_primary.py}.", "")

# ---- pooling scope and the extension sentence matched to the reviewer's wording --
rep(r"""Two scored families carry a GEN leg drawn from a genetic association rather than an MR causal estimate---Complement-GA (\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---and the causal reading of the GEN leg applies to neither. Both are misclassified. The GEN leg is called causal only for families instrumented by MR; for these two families it is called associated, and the revised primary analysis (\S\ref{sec:revised_primary}) sets them aside so that every family it scores has an MR estimate on the genetic leg.""",
    r"""Two scored families carry a GEN leg drawn from a genetic association rather than an MR causal estimate---Complement-GA (\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---so under the registered rule the pooling bears on exactly these two, both of which are misclassified. The GEN leg is called causal only for families instrumented by MR and associated for these two. The revised primary analysis (\S\ref{sec:revised_primary}) sets both aside, so every family it scores has an MR estimate on the genetic leg and the pooling of association-only families does not enter it.""")
rep(r"""(pre-registered: 18/22, 81.8\%, CI 61.5--92.7\%; extension: 6/10, 60.0\%, CI 31.3--83.2\%; combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$; \S\ref{sec:stats}). The extension classified 6/10 correctly and was not significant when considered alone (binomial $p = 0.38$, permutation $p = 0.55$); it is therefore treated""",
    r"""(pre-registered: 18/22, 81.8\%, CI 61.5--92.7\%; combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$; \S\ref{sec:stats}). The extension classified 6/10 correctly (60.0\%, CI 31.3--83.2\%) and was not statistically significant when considered alone (binomial $p = 0.38$, permutation $p = 0.55$); it is therefore treated""")

# ---- after the second-pass consistency audit (13 Sep) ---------------------------
# Table 5: criteria are not mutually exclusive, and "in order" contradicted the assignment.
rep("Each of the eight misses under the registered rule is assigned by reading the criteria in order, using fields of",
    "Each of the eight misses under the registered rule is assigned by the criteria below, which are not mutually exclusive, using fields of")
rep(r"Class & MR class & Outcome & Criterion, read in this order & Misses \\", r"Class & MR class & Outcome & Criterion & Misses \\")
# Extension provenance: three declared families are now dropped from the revised analysis.
rep("Every declared family was scored regardless of outcome; none were dropped post hoc.",
    "Every declared family was scored regardless of outcome under the registered rule, and none was dropped from it post hoc.")
# Complement-GA and Serotonin-MDD: the genetic leg is an association, and the table said MR.
rep(r"Complement-GA$^\text{l}$ & Ophth & non-triv.$^\dagger$ & 2.50 (2.20--2.85) & 0.505 & Causal & Failed & Conc. & $\times$ \\",
    r"Complement-GA$^\text{l}$ & Ophth & non-triv.$^\dagger$ & 2.50 (2.20--2.85) & 0.505 & Assoc. & Failed & Conc. & $\times$ \\")
rep(r"$^\text{l}$OBS: complement activation case-control data \cite{reynolds2009}. MR: CFH Y402H per-allele OR \cite{thakkinstian2006}.",
    r"$^\text{l}$OBS: complement activation case-control data \cite{reynolds2009}. Genetic association, not MR: CFH Y402H per-allele OR \cite{thakkinstian2006}; it meets both criteria of the rule and enters the registered analysis as causal, and is set aside in the revised primary analysis.")
rep(r"$^\text{j}$OBS: plasma tryptophan SMD from \citet{ogawa2014}. MR: 5-HT transporter-linked polymorphic region (5-HTTLPR) OR from \citet{clarke2010serotonin};",
    r"$^\text{j}$OBS: plasma tryptophan SMD from \citet{ogawa2014}. Genetic association, not MR: 5-HT transporter-linked polymorphic region (5-HTTLPR) OR from \citet{clarke2010serotonin};")
# Abstract: no separate analysis of the association families exists; the cluster-level test joins the primary result.
rep("Genetic-association families were analyzed separately from MR families.",
    "Two genetic-association families are reported apart from MR-instrumented families.")
rep("produced identical classifications with zero McNemar disagreements across all 32 scored families, because 31 of 32 have non-trivial observational support. Under the registered analysis",
    "produced identical classifications across all 32 scored families, because 31 of 32 have non-trivial observational support. Under the registered analysis")
rep(r"23/28 were classified correctly (82.1\%; $p = 0.0006$).", r"23/28 were classified correctly (82.1\%; $p = 0.0006$, cluster-level $p = 0.0002$).")
# Small-effect is one of the five null-MR successes.
rep("effector-neutralization and mechanism-bypass for the five null-MR successes.",
    "effector-neutralization, small-effect and mechanism-bypass for the five null-MR successes.")
rep("Five families have null MR signals yet succeed clinically (effector-neutralization and mechanism-bypass).",
    "Five families have null MR signals yet succeed clinically (effector-neutralization, small-effect and mechanism-bypass).")
# Instrument-type sentence vs the CSV: CTLA-4-RA is a coding variant.
rep("effector-neutralization targets (TNF, IL-17, CTLA-4) use biomarker-level instruments that cannot capture post-onset therapeutic effects",
    "effector-neutralization targets (TNF, IL-17, CTLA-4) use biomarker-level or coding-variant instruments that cannot capture post-onset therapeutic effects")
rep("Only mechanism-bypass was pre-specified before the corresponding miss was observed",
    "Only mechanism-bypass was fully pre-specified before the corresponding miss was observed")
# Statistical tests: cluster-level test joins the primary report; Monte Carlo stated accurately; drug-level tests distinguished.
rep(r"a Monte Carlo run of $10^5$ permutations is reported beside it. A cluster-level variant permutes one outcome label per instrument set, so families sharing an instrument move together. The binomial p-values are retained for comparison with the registered analysis.",
    r"a Monte Carlo run of $10^5$ permutations reproduces each exact value to within 0.0002 and is recorded in the supplementary results file. Because families sharing an MR instrument set are not independent, a cluster-level test that permutes one outcome label per instrument set, so that families sharing an instrument move together, is reported beside the family-level test wherever the primary result appears. The binomial p-values are retained for comparison with the registered analysis. The permutation tests reported with the neuroepidemiology drug-level result (\S\ref{sec:stage1}) shuffle outcomes across drugs and are distinct from the family-level test.")
rep(r"23/28 (82.1\%; exact outcome-permutation $p = 0.0006$, one-sided exact binomial $p < 0.001$;",
    r"23/28 (82.1\%; exact outcome-permutation $p = 0.0006$, cluster-level $p = 0.0002$, one-sided exact binomial $p < 0.001$;")
rep(r"The registered analysis, 24/32 (75.0\%; permutation $p = 0.005$, binomial $p = 0.004$), is retained",
    r"The registered analysis, 24/32 (75.0\%; permutation $p = 0.005$ at family and cluster level, binomial $p = 0.004$), is retained")
rep(r"combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$; \S\ref{sec:stats}).",
    r"combined one-sided exact binomial $p = 0.004$, exact outcome-permutation $p = 0.005$, cluster-level $p = 0.005$; \S\ref{sec:stats}).")

# ---- no review-process narration in the manuscript (lab-notebook rule) --------
rep("Under the revised primary analysis requested during peer review, which excludes",
    "Under a revised primary analysis specified after the registered analysis, which excludes")
rep("A revised primary analysis, requested during peer review after outcomes were known, additionally excludes",
    "A revised primary analysis, specified after the registered analysis and after all outcomes were known, additionally excludes")
rep("The primary test in this revision is therefore an outcome-permutation test",
    "The primary test is therefore an outcome-permutation test")
rep(r"The revised primary analysis requested during peer review scores 28 of these 32 families, 23 correctly (\S\ref{sec:revised_primary}).}",
    r"The revised primary analysis, specified after the registered analysis, scores 28 of these 32 families, 23 correctly (\S\ref{sec:revised_primary}).}")
rep("ZEUS read out on 31 July 2026, after the preregistration was frozen and before this revision was written.",
    "ZEUS read out on 31 July 2026, after the preregistration was frozen and after the scored set was fixed.")
rep(r"The revised primary analysis requested during peer review scores 23/28 (\S\ref{sec:revised_primary}).",
    r"The revised primary analysis, specified after the registered analysis, scores 23/28 (\S\ref{sec:revised_primary}).")
rep("Three changes to the scored set were requested during peer review, each after the outcomes were known:",
    "Three changes to the scored set were specified after the registered analysis, each after the outcomes were known:")
rep("The revision therefore reports both analyses rather than replacing one with the other, and the departure is recorded as Amendment~4 to the registration.",
    "Both analyses are therefore reported rather than one replacing the other, and the departure is recorded as Amendment~4 to the registration.")
assert not re.search(r"(?i)peer review|reviewer|during review|this revision was", text), "process narration survives"

# ---- after the change-by-change audit against the reviewer's points (14 Sep) ------
# Two sentences graded the paper's own rigor or spoke to the reviewer rather than the reader.
rep("The criteria make the assignment reproducible; they do not establish the classes, which remain hypothesis-generating.}",
    "The classes remain hypothesis-generating.}")
rep(" No pooling or heterogeneity test enters the rule. Stage~1 uses etiologic evidence only;",
    " Stage~1 uses etiologic evidence only;")
# Point 4: no causal wording on an association, even in a footnote.
rep("it meets both criteria of the rule and enters the registered analysis as causal, and is set aside in the revised primary analysis.",
    "it meets both criteria of the rule and is scored in the registered analysis, and is set aside in the revised primary analysis.")
# Double colon introduced by the rename.
rep("The practical implication: a null MR signal for a risk-encoding drug target is a strong negative signal: the observational association has no causal support.",
    "The practical implication: a null MR signal for a risk-encoding drug target is a strong negative signal, since the observational association has no causal support.")
# Amendment 4 named once in the body, not twice.
rep(r"the registered count is reported beside it throughout, and the departure from the registration is recorded in Amendment~4.",
    r"the registered count is reported beside it throughout.")
# Point 10: extension families are not "replications" of the framework.
rep("replicates the MR-discordant pattern in a new disease domain.", "shows the MR-discordant pattern in a new disease domain.")
rep(r"\paragraph{Ophthalmology: complement and the translation-gap replication.}", r"\paragraph{Ophthalmology: complement and the translation-gap pattern.}")
rep("This replicates the translation-gap pattern from amyloid and IGF-1:", "This shows the same translation-gap pattern as amyloid and IGF-1:")
# Points 5 and 6: the revised primary analysis leads in the abstract; the registered one follows.
rep(r"""Under the registered analysis the rule classified 24/32 families correctly (75.0\%; outcome-permutation $p = 0.005$): 18/22 in the original domains (81.8\%, 95\% CI 61.5--92.7\%) and 6/10 in the blind extension (60.0\%, CI 31.3--83.2\%), the latter not significant alone and not independent confirmation. Under a revised primary analysis specified after the registered analysis, which excludes one indication-mismatched family and two association-only families and counts duplicated evidence once, 23/28 were classified correctly (82.1\%; $p = 0.0006$, cluster-level $p = 0.0002$).""",
    r"""Under a revised primary analysis specified after the registered analysis, which excludes one indication-mismatched family and two association-only families and counts duplicated evidence once, 23/28 families were classified correctly (82.1\%; outcome-permutation $p = 0.0006$, cluster-level $p = 0.0002$). By tier, 17/21 in the original domains and 6/7 in the blind extension, the latter not significant alone (permutation $p = 0.14$) and not independent confirmation. The registered analysis, 24/32 (75.0\%; $p = 0.005$), is reported as a robustness analysis.""")

# ---- the extension count stated once, in the sentence that answers point 10 ------
rep("The extension adds 10 scored families (6 correct, 4 misses) and 4 construct-limited. Combined with the original 22,",
    "The extension adds 10 scored families and 4 construct-limited. Combined with the original 22,")

# ---- checks -----------------------------------------------------------------
leftover = [m.start() for m in re.finditer(r"(?i)zombie", text)]
assert not leftover, f"'zombie' survives at offsets {leftover}"
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, f"abstract is {words} words"
assert text.count(r"\ref{tab:criteria}") >= 3 and text.count(r"\label{tab:criteria}") == 1
assert text.count(r"\ref{sec:revised_primary}") >= 4 and text.count(r"\label{sec:revised_primary}") == 1
assert text.count(r"\ref{sec:stats}") >= 3 and text.count(r"\label{sec:stats}") == 1

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
