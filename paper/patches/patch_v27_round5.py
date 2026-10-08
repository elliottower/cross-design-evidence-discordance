"""v26p -> v27: title and abstract on the MR-status result; Amendment 6 results (source-reported values,
published-MR-estimate set) in the abstract, Results, analysis-set table and Appendix A; supplement v5.

Run:  uv run --no-project python paper/patches/patch_v27_round5.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "paper_v26p_round4.tex"
DST = HERE.parent / "paper_v27_round5.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


# ------------------------------------------------------------------ title
rep(r"""\title{Diagnosing Drug Failure Modes from Cross-Design Evidence Across Ten Disease Domains}""",
    r"""\title{Cross-Design Evidence: Mendelian Randomization Status Alone Explains the Classification of Phase~III Drug Outcomes Across Ten Disease Domains}""")

# ------------------------------------------------------------------ abstract
rep(r"""Mendelian randomization (MR) evidence is associated with drug success, but when a drug fails despite genetic support---or succeeds without it---MR alone cannot explain why. We tested a preregistered rule comparing observational and MR evidence against Phase~III outcomes and performed an exploratory analysis of the families it misclassified.""",
    r"""Mendelian randomization (MR) evidence is associated with drug success. We tested whether observational evidence adds to MR status in classifying Phase~III outcomes, using a preregistered rule comparing the two evidence types, and performed an exploratory analysis of the misclassified families.""")
rep(r"""selection of the original 27 families and the failure-mode taxonomy were not.""",
    r"""selection of the original 27 families and the exploratory failure-mode taxonomy were not.""")
rep(r"""A sensitivity analysis specified after the registered analysis, with outcomes known, excludes three families (one indication-mismatched, two association-only) and counts duplicated evidence once: 23/28 (82.1\%; $p = 0.0006$).""",
    r"""Repeating the analysis with source-reported values changed no classification (24/32). Excluding four families whose MR value is not a published estimate, a set specified with outcomes known, gave 21/28 (75.0\%; descriptive permutation $p = 0.011$).""")
rep(r"""Its contribution is diagnostic: set against MR and trial evidence, it generates hypotheses about why an MR-based classification fails.""",
    r"""Set against MR and trial evidence, the observational leg yields exploratory hypotheses about why an MR-based classification fails.""")
rep(r"""evidence triangulation, failure-mode diagnosis, Phase~III trials""",
    r"""evidence triangulation, observational evidence, Phase~III trials""")

# ------------------------------------------------------------------ Results: paragraph before the analysis-set table
rep(r"""Across the table the accuracy runs from 17/26 (65.4\%) to 23/28 (82.1\%).

\begin{table}[htbp]
\centering
\caption{Registered analysis-set table (Amendment~5).""",
    r"""Across the table the accuracy runs from 17/26 (65.4\%) to 23/28 (82.1\%).

\paragraph{Source-reported input values.}
\label{sec:source_values}
Fourteen input values differ from what their source reports (Appendix~A, Table~\ref{tab:coding}). Two procedures registered before they were run (Amendment~6) address them. Nine of the 14 have a figure in the source. With each of the nine replaced by the source's figure, the registered rule classifies 24/32 correctly (75.0\%): no family's classification, expected outcome or score changes, and 31 of 32 families keep non-trivial observational support. The other five values have no published figure to substitute: four MR values (ModRisk-AD, EBV-MS, TNF-$\alpha$-RA, IL-1$\beta$-CVD) and the observational value of IL-23-psoriasis (Table~\ref{tab:sets}). Without those four families the rule classifies 21/28 correctly (75.0\%; outcome-permutation $p = 0.011$, cluster-level $p = 0.008$ over 25 clusters): 15/18 in the original domains and 6/10 in the blind extension, with 27 of 28 families carrying non-trivial observational support and identical classifications under the MR-only rule. This published-MR-estimate set was defined after the registered analysis, with outcomes known, and its p-values are descriptive. The registered 24/32 remains the primary result.

\begin{table}[htbp]
\centering
\caption{Registered analysis-set table (Amendment~5).""")
rep(r"""Permutation and binomial p-values are given only for the two sets tested before this table was registered; no test is run on the other sets, which differ from the registered set by one to seven families.""",
    r"""Permutation and binomial p-values are given for the two sets tested before this table was registered and, as descriptive values, for the published-MR-estimate set; no test is run on the other sets, which differ from the registered set by one to seven families.""")
rep(r"""$^\ast$Set defined after the registered sets were scored.}
\label{tab:sets}""",
    r"""$^\ast$Set defined after the registered sets were scored. $^\ddagger$Registered in Amendment~6 before it was run, with outcomes known (\S\ref{sec:source_values}).}
\label{tab:sets}""")
rep(r"""28-family sensitivity set & \S\ref{sec:sensitivity_set} (permutation $p = 0.0006$, cluster-level $p = 0.0002$, binomial $p < 0.001$) & 28 & 23 & 82.1\% \\
\bottomrule""",
    r"""28-family sensitivity set & \S\ref{sec:sensitivity_set} (permutation $p = 0.0006$, cluster-level $p = 0.0002$, binomial $p < 0.001$) & 28 & 23 & 82.1\% \\
Source-reported values$^\ddagger$ & registered set, each of the nine mismatched inputs with a published figure replaced by that figure & 32 & 24 & 75.0\% \\
Published MR estimate$^\ddagger$ & removes ModRisk-AD, EBV-MS, TNF-$\alpha$-RA, IL-1$\beta$-CVD (descriptive permutation $p = 0.011$, cluster-level $p = 0.008$) & 28 & 21 & 75.0\% \\
Published MR estimate, IL-23-psoriasis removed$^\ddagger$ & also removes the family whose observational value has no published figure & 27 & 20 & 74.1\% \\
\bottomrule""")

# ------------------------------------------------------------------ Appendix A
rep(r"""Among the values for which a source figure exists, applying the registered rule to the source's figure changes no family's expected outcome or score; one family's label changes (IGF1-CRC).""",
    r"""Nine of the 14 have a figure in the source, and Table~\ref{tab:coding} gives the figure used for each and its conversion. Where a source reports several figures, the figure used is the estimate for the exposure and outcome the family is defined on, on the contrast of the registered value, from the most fully adjusted model; where only stratum estimates exist, their fixed-effect inverse-variance pooled estimate is used (Amendment~6). Applying the registered rule to the nine figures changes no family's classification, expected outcome or score (\S\ref{sec:source_values}). Among the other figures the sources report, two change one family's label and not its expected outcome (IGF1-CRC, highest against lowest fifth). The other five values have no published figure and keep the registered value.""")
rep(r"""\caption{Input values that do not match their source. Registered values are those of the frozen classifier; the source column gives what the source reports. The classification column applies the registered rule to the source's value.}
\label{tab:coding}
\footnotesize
\begin{tabular}{>{\raggedright\arraybackslash}p{2.2cm}>{\raggedright\arraybackslash}p{2.4cm}>{\raggedright\arraybackslash}p{6.3cm}>{\raggedright\arraybackslash}p{3.3cm}}
\toprule
Family, leg & Registered value & Source reports & Classification \\
\midrule""",
    r"""\caption{Input values that do not match their source. Registered values are those of the frozen classifier; the source column gives what the source reports. The figure used is the source figure to which the registered rule was re-applied (Amendment~6), with its conversion to the scale of the rule; hazard and risk ratios are treated as odds ratios and converted on $|\ln \mathrm{OR}|$, as registered. The classification column applies the registered rule to the figure used.}
\label{tab:coding}
\scriptsize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{0.95}
\begin{tabular}{>{\raggedright\arraybackslash}p{1.7cm}>{\raggedright\arraybackslash}p{1.7cm}>{\raggedright\arraybackslash}p{4.5cm}>{\raggedright\arraybackslash}p{2.1cm}>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{2.6cm}}
\toprule
Family, leg & Registered value & Source reports & Figure used & Conversion & Classification \\
\midrule""")

NONE = r"none published & --- &"
rep(r"""a 2023 MR of modifiable risk factors reports several estimates of 1.10 for single traits & scored""",
    r"""a 2023 MR of modifiable risk factors reports several estimates of 1.10 for single traits & """ + NONE + " scored")
rep(r"""nearest are observational (infectious mononucleosis, OR 5.5, 1.5--19.7) & scored""",
    r"""nearest are observational (infectious mononucleosis, OR 5.5, 1.5--19.7) & """ + NONE + " scored")
rep(r"""converted, OR 0.96 to 1.54, every interval including 1 & unchanged (null)""",
    r"""converted, OR 0.96 to 1.54, every interval including 1 & OR 1.54 (0.98--2.41), combined sample & $\exp$ of the coefficient 0.43, read as a log odds ratio & unchanged (null)""")
rep(r"""the source reports HR 0.14 (0.05--0.39) & unchanged (non-trivial)""",
    r"""the source reports HR 0.14 (0.05--0.39) & HR 0.14 & hazard ratio; registered value in the opposite direction & unchanged (non-trivial)""")
rep(r"""quintile ORs 0.57, 0.57, 0.74, 0.38 & unchanged (non-trivial)""",
    r"""quintile ORs 0.57, 0.57, 0.74, 0.38 & OR 0.59 & odds ratio per 50~nmol/L; registered value in the opposite direction & unchanged (non-trivial)""")
rep(r"""\citet{voight2012} give 1.54 (1.45--1.63) & unchanged (non-trivial)""",
    r"""\citet{voight2012} give 1.54 (1.45--1.63) & OR 1.54 & odds ratio per SD & unchanged (non-trivial)""")
rep(r"""any stroke 1.39 (1.33--1.44), ischemic 1.41 (1.35--1.47) & unchanged (supportive)""",
    r"""any stroke 1.39 (1.33--1.44), ischemic 1.41 (1.35--1.47) & OR 1.39 (1.33--1.44), any stroke & odds ratio per 10~mmHg systolic & unchanged (supportive)""")
rep(r"""the leg rests on tissue p19 expression & unchanged (non-trivial)""",
    r"""the leg rests on tissue p19 expression & """ + NONE + " unchanged (non-trivial)")
rep(r"""\citet{daha2009ctla4}: 0.86 (0.78--0.96) & unchanged (null)""",
    r"""\citet{daha2009ctla4}: 0.86 (0.78--0.96) & OR 0.86 (0.78--0.96) & odds ratio & unchanged (null)""")
rep(r"""no TNF estimate reported; 1.00 stands for a null result & unchanged (null)""",
    r"""no TNF estimate reported; 1.00 stands for a null result & """ + NONE + " unchanged (null)")
rep(r"""no IL-1$\beta$ estimate exists for coronary disease; 1.00 stands for a null result & unchanged (null)""",
    r"""no IL-1$\beta$ estimate exists for coronary disease; 1.00 stands for a null result & """ + NONE + " unchanged (null)")
rep(r"""is the per-SD HR for distal colon cancer; colorectal Q5 vs.\ Q1 HR 1.24 (1.10--1.40) and 1.34 (1.18--1.52) & label changes (genetic-only to concordance); expected success and miss unchanged""",
    r"""is the per-SD HR for distal colon cancer; colorectal per-SD HR 1.07 (1.02--1.13) and, with further adjustment, 1.11 (1.05--1.17); colorectal Q5 vs.\ Q1 HR 1.24 (1.10--1.40) and 1.34 (1.18--1.52) & HR 1.11 (1.05--1.17), colorectal, per SD & hazard ratio per SD & unchanged (trivial); the label changes under the Q5 vs.\ Q1 figures""")
rep(r"""1.74 (1.55--1.95) men, 1.95 (1.70--2.22) women & unchanged (non-trivial)""",
    r"""1.74 (1.55--1.95) men, 1.95 (1.70--2.22) women & RR 1.83 (1.67--1.99) & fixed-effect inverse-variance pool of the two risk ratios, log scale & unchanged (non-trivial)""")
rep(r"""\citet{thakkinstian2006}: pooled 2.50 (1.96--3.30) & unchanged (association)""",
    r"""\citet{thakkinstian2006}: pooled 2.50 (1.96--3.30) & OR 2.50 (1.96--3.30) & pooled odds ratio & unchanged (association)""")

# ------------------------------------------------------------------ Data Availability
rep(r"""the outcome codebook with its source log, the MR-instrumented audit and the IL6-MDD search record), the complete""",
    r"""the outcome codebook with its source log, the MR-instrumented audit and the IL6-MDD search record), the source-reported-value analysis of \S\ref{sec:source_values} (\texttt{analysis/amendment6/run\_source\_values.py}), the complete""")
rep(r"""and the origin and source of each input value; \texttt{cross\_design\_classification\_all\_41\_families\_v4.csv})""",
    r"""the origin and source of each input value, and the class and score under source-reported values; \texttt{cross\_design\_classification\_all\_41\_families\_v5.csv})""")
rep(r"""at tag \texttt{frontiers-revision-4}""", r"""at tag \texttt{frontiers-revision-5}""")

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; wrote {DST.name}")
