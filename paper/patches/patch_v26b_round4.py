"""v26 -> v26b: the numbers from Amendment 5 (commit fbc7d33) enter the manuscript.

Run:  uv run --no-project python paper/patches/patch_v26b_round4.py

Every edit is an exact-string replacement that must match once; the script aborts on the
first miss and writes nothing. v26 is not touched. Numbers come from
analysis/amendment5/{screen,mr_states,codebook,analysis_sets,il6_mdd}/ and are asserted
against those files at the bottom.

What enters:
  Methods   one regulatory definition of the recorded outcome; a "Registered sensitivity
            procedures" subsection (screen, three MR states, outcome decomposition, analysis
            sets, the IL6-MDD instrument); five association-leg families named
  Results   four Robustness paragraphs and the analysis-set table; instrument-type counts
            with IL6-MDD as biomarker GWAS; the four program-less families stated
  Narratives CANTOS sentence corrected (primary endpoint met at 150 mg, not approved);
            IL6-MDD cites Galan 2022 and Kelly 2021; APOE4 cites Belloy 2023; mepolizumab
            cites MENSA
  Tables    dagger removed from IL6-MDD and Serotonin-MDD (their values are meta-analytic);
            Table 5 translation-gap criterion no longer asserts a target-engagement record
  Limitations  author-estimated count 8 (5 scored); ascertainment paragraph carries the screen
  Back matter  Data Availability lists the new scripts and Supplementary Tables S2-S8;
            bibliography references_v10_r4.bib (v9_r3 + galan2022crpdepression, kelly2021il6r,
            belloy2023apoe, ortega2014mensa)
"""
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = HERE.parent / "paper_v26_round4.tex"
DST = HERE.parent / "paper_v26b_round4.tex"
A5 = ROOT / "analysis" / "amendment5"

text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old: str, new: str, count: int = 1) -> None:
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:160]}"
    text = text.replace(old, new)
    applied += 1


# ---- numbers, read from the files that produced them --------------------------------------
screen = json.loads((A5 / "screen" / "screen_results.json").read_text())
states = json.loads((A5 / "mr_states" / "mr_states_results.json").read_text())
sets = json.loads((A5 / "analysis_sets" / "analysis_sets.json").read_text())
il6 = json.loads((A5 / "il6_mdd" / "selected_estimate.json").read_text())
sample = list(csv.DictReader(open(A5 / "screen" / "mr_availability_sample_filled.csv", encoding="utf-8")))
codebook = {r["family"]: r for r in csv.DictReader(open(A5 / "codebook" / "outcome_codebook_all_41_families.csv", encoding="utf-8"))}
row = {t["set"]: t for t in sets["table"]}
assert screen["resolved_universe_n"] == 219 and screen["universe_n"] == 279
assert screen["exact_coverage"]["resolved_rows_covered"] == 0 and screen["expanded_coverage"]["resolved_rows_covered"] == 14
assert screen["families_by_match_status"] == {"polygenic": 5, "no record": 18, "broader indication": 8, "exact": 1}
n_elig = sum(r["mr_eligible"].strip().lower() == "yes" for r in sample)
assert n_elig == 4 and len(sample) == 25
st = states["scored_32_by_state"]
assert (st["supportive"]["n"], st["supportive"]["correct"]) == (15, 12)
assert (st["negligible_range"]["n"], st["negligible_range"]["correct"]) == (7, 6)
assert (st["inconclusive"]["n"], st["inconclusive"]["correct"]) == (10, 6)
assert states["registered_null_families_split"] == {"negligible_range": 7, "inconclusive": 10}
assert len(states["scale_unresolved_families"]) == 8
assert (row["registered"]["correct"], row["registered"]["n"]) == (24, 32)
assert (row["strict Phase III"]["correct"], row["strict Phase III"]["n"]) == (17, 25)
assert (row["Amyloid-AD scored"]["correct"], row["Amyloid-AD scored"]["n"]) == (24, 33)
assert (row["strict Phase III + Amyloid-AD"]["correct"], row["strict Phase III + Amyloid-AD"]["n"]) == (17, 26)
assert (row["MR-instrumented"]["correct"], row["MR-instrumented"]["n"]) == (22, 27)
assert (row["MR-instrumented (unresolved also removed)"]["correct"], row["MR-instrumented (unresolved also removed)"]["n"]) == (21, 26)
assert (row["registration-consistent instrument"]["correct"], row["registration-consistent instrument"]["n"]) == (24, 32)
assert (row["unique-evidence"]["correct"], row["unique-evidence"]["n"]) == (23, 31)
assert (row["source-extracted OBS"]["correct"], row["source-extracted OBS"]["n"]) == (20, 25)
assert (row["source-extracted OBS (classifier flags)"]["correct"], row["source-extracted OBS (classifier flags)"]["n"]) == (21, 27)
assert (row["Amendment 4"]["correct"], row["Amendment 4"]["n"]) == (23, 28)
assert il6["pmid"] == "33631287" and abs(float(il6["or"]) - 1.023) < 1e-6
assert codebook["IL6-MDD"]["trial_phase"] == "II"
assert all(codebook[f]["trial_phase"] == "not reported" for f in ("ModRisk-AD", "Smoking-MS/AD", "BMI-AD", "EBV-MS"))
assert codebook["CRP"]["efficacy_endpoint"] == "met" and codebook["IL-1b-CVD"]["efficacy_endpoint"] == "met"
assert all(codebook[f]["target_engagement"] == "not reported" for f in ("IGF1-CRC", "Complement-GA", "VitaminD-MS"))

# =============================================================================
# Methods
# =============================================================================
rep(r"""acting on that mechanism. The recorded outcome is \emph{success} when a drug acting on the
mechanism is approved for the family's indication or met the primary efficacy endpoint of
its Phase~III program, and \emph{failure} when the Phase~III program did not meet its
primary endpoint or was discontinued for futility; a family whose class contains both
outcomes is coded on the majority of its programs. One scored family, IL6-MDD, is coded on
a Phase~II readout declared in advance (Amendment~2), against this criterion;
\S\ref{sec:robustness} reports the count without it.""",
    r"""acting on that mechanism. The recorded outcome is a development outcome: \emph{success}
when a drug acting on the mechanism holds regulatory approval for the family's indication,
and \emph{failure} when the Phase~III program on that mechanism did not lead to approval,
whether because the primary endpoint was not met or because no application followed. A
class containing both outcomes is coded on the majority of its programs. The outcome is
decomposed into its trial-level components in \S\ref{sec:procedures}. One scored family,
IL6-MDD, is coded on a Phase~II readout declared in advance (Amendment~2), against this
criterion, and four scored families (ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS) carry an
outcome assigned at the family level with no Phase~III program in the catalog behind it;
\S\ref{sec:analysis_sets} reports the count without them.""")

rep(r"""Two scored families carry a GEN leg drawn from a genetic association rather than an MR estimate---Complement-GA (\emph{CFH} Y402H per-allele OR) and Serotonin-MDD (5-HTTLPR)---so under the registered rule the pooling bears on exactly these two, both of which are misclassified. The GEN leg is called MR-supportive only for families instrumented by MR and associated for these two. The 28-family sensitivity analysis (\S\ref{sec:sensitivity_set}) sets both aside, so every family it scores has an MR estimate on the genetic leg.""",
    r"""Five scored families carry a GEN leg drawn from a variant--disease association rather than an instrumental-variable estimate: Complement-GA (\emph{CFH} Y402H), Serotonin-MDD (5-HTTLPR), IL-23-psoriasis (\emph{IL23R} R381Q), CTLA-4-RA (\emph{CTLA4}) and JAK-STAT-RA (\emph{STAT4} rs7574865), each read from its source's own description of its design (Supplementary Table~S8). Under the registered rule the pooling bears on these five, three of which are misclassified. The GEN leg is called MR-supportive only for families instrumented by MR and associated for these five. The 28-family sensitivity analysis (\S\ref{sec:sensitivity_set}) sets aside the two identified first; the MR-instrumented analysis set (\S\ref{sec:analysis_sets}) removes all five.""")

procedures = r"""
\subsection{Registered sensitivity procedures}
\label{sec:procedures}

Four procedures were registered before they were run (commit \texttt{fbc7d33}); each produces descriptive quantities and none changes the registered rule, scored set or accuracy.

\paragraph{Candidate-family screen.} The universe is every target--indication pair in the \citet{minikel2024} dataset with a combined maximum phase of Phase~III or Launched and a genetic association in that dataset's sense (279 pairs; 219 with a recorded Phase~III outcome, 189 launched and 30 failed). A scored family covers a pair when its gene target and indication match the pair's target and MeSH term under the mapping used for the cross-tabulation in \S\ref{sec:robustness} (commit \texttt{4b0a652}). Each family receives a match status: exact target and indication; exact target under a different indication only; polygenic, which cannot map; or no record. Exact coverage counts a pair as covered under the first status only; expanded coverage also counts the pairs a gene reaches under other indications. Because the universe admits any genetic association while the family rule requires a published MR estimate, 25 uncovered pairs with a recorded outcome were drawn at random (seed 20260922) and PubMed was searched for each with a fixed query for a Mendelian randomization estimate of the target's exposure on that indication; the fraction with such an estimate is reported.

\paragraph{Three MR states.} For reporting, the registered MR leg is split into three states. \emph{Supportive} is the registered class: the confidence interval excludes the null and $|d_{\text{MR}}| \geq 0.10$. \emph{Interval within the negligible range} holds when both interval bounds, converted to signed $d$, lie strictly inside $(-0.10, 0.10)$; the conversion is applied to each bound as to the point estimate, and per-allele families are rescaled first where a conversion factor is registered (IL-6R only). \emph{Inconclusive} is every other case, including a family whose MR estimate carries no confidence interval and a per-allele family without a conversion factor, whose unrescaled interval does not bound the per-SD effect (marked scale-unresolved). The source intervals are 95\% intervals, so the negligible-range state is stricter than the 90\% interval a two-one-sided-tests procedure uses at $\alpha = 0.05$; no equivalence test is claimed, and the range is the registered threshold rather than a clinically validated margin. Each family also carries an alignment flag (aligned; indication mismatch; instrument--target mismatch; construct-limited) taken from its status and the criteria of Table~\ref{tab:criteria}.

\paragraph{Outcome decomposition.} Seven fields were coded for each of the 41 families from the trial and regulatory record of the program the family is scored on: trial phase, target engagement, efficacy endpoint result, safety outcome, development decision, regulatory outcome with jurisdiction and year, and an attribution of the outcome (target, molecule, dose, design, indication, commercial, or uncertain), coded last and reported as a single coder's reading. Every value carries a source identifier (PMID, DOI, trial registry number, or FDA application number), and a field that the record does not carry is left as not reported. The registered outcome variable is kept unchanged; the seven fields decompose it and do not redefine it. Families where the fields disagree with the registered outcome are listed. A translation gap is read only where target engagement is recorded and the efficacy endpoint was not met.

\paragraph{Analysis sets.} One table reports the number scored and the number correct across sets, each defined by a rule named before scoring: the registered set; the registered families whose coded trial phase is III or post-marketing for the family's indication; the registered set plus Amyloid-AD, classified under the registered rule on its observational estimate and the \emph{APOE4} association; both changes together; the registered set without families whose genetic leg is a variant--disease association (audited from every cited source; a family whose estimate could not be traced stays in the set and is listed, and the set is also reported with it removed); the registered set with IL6-MDD classified on the estimate the registration named (below); families identical on every evidence field counted once; the registered set without the families whose observational value was author-estimated (reported twice, on the list the registration names and on the classifier's own flags, which differ for two families whose values are meta-analytic); and the 28-family sensitivity set. The registered binomial and permutation p-values are reported for the two sets already tested and no test is run on the others; the sets differ from the registered set by one to seven families, and 25 to 33 families cannot distinguish accuracies that differ by that much, so the comparisons are descriptive.

\paragraph{IL6-MDD instrument.} The registration declared IL6R-region instruments for this family (rs2228145, rs4129267) with CRP as the exposure readout. The estimate the frozen classifier holds is a polygenic CRP estimate, OR 1.01 (95\% CI 0.99--1.04) from a bidirectional two-sample MR of CRP and depression with 512 instruments \cite{galan2022crpdepression}. The family is therefore classified twice: on the classifier's estimate, which stays in the registered count, and on the estimate a fixed PubMed query and a deterministic selection rule return for the declared instruments. That query returned eight papers, one eligible: soluble IL-6R on depression in UK Biobank, instrumented by the IL6R \emph{cis} set headed by rs2228145, OR 1.023 (95\% CI 1.006--1.039) \cite{kelly2021il6r}. Both estimates are null under the registered rule ($d = 0.005$ and $d = 0.013$, the second with its whole interval below 0.10), so the family's classification and score are the same under either. Sirukumab neutralizes the IL-6 ligand, the declared instrument is the receptor, and the estimate used is downstream CRP; the family carries the instrument--target mismatch flag under either instrument.
"""
rep(r"""For each rule we report total accuracy, accuracy split by outcome (failures and approvals classified correctly), and McNemar paired disagreements between the cross-design and MR-only rules---naming the specific families where the rules diverge, if any.
""",
    r"""For each rule we report total accuracy, accuracy split by outcome (failures and approvals classified correctly), and McNemar paired disagreements between the cross-design and MR-only rules---naming the specific families where the rules diverge, if any.
""" + procedures)

# =============================================================================
# Results
# =============================================================================
rep(r"""A candidate-family screen against an external universe (\S\ref{sec:robustness}) measures how much of that universe the scored families cover.""",
    r"""A candidate-family screen against an external universe (\S\ref{sec:screen_results}) measures how much of that universe the scored families cover, and the registered analysis-set table (\S\ref{sec:analysis_sets}) reports the count under every rule-consistent definition of the scored set.""")

rep(r"""\paragraph{Accuracy by MR instrument type.} Families using \emph{cis}-pQTL instruments and polygenic scores (5/5 correct) outperform those using coding variants (5/8, 62.5\%) and biomarker GWAS; the \emph{cis}-pQTL and biomarker-GWAS counts are reported in Supplementary Table~S1 with the IL6-MDD instrument recorded as biomarker GWAS.""",
    r"""\paragraph{Accuracy by MR instrument type.} Families using \emph{cis}-pQTL instruments (7/7 correct) and polygenic scores (5/5) outperform those using coding variants (5/8, 62.5\%) and biomarker GWAS (7/12, 58.3\%); IL6-MDD, whose estimate is a polygenic CRP estimate, is counted as biomarker GWAS (Supplementary Table~S1).""")

new_results = r"""

\paragraph{Candidate-family screen.}
\label{sec:screen_results}
The universe holds 279 genetically supported target--indication pairs at Phase~III or Launched, 219 with a recorded outcome (189 launched, 30 failed). Of the 32 scored families, one maps exactly onto a universe pair (IL-23-psoriasis, whose pair is outcome-pending), eight reach their gene under other indications (HRT-AD, HDL/CETP, Niacin/HDL, LDL/PCSK9, Triglycerides, IL-1$\beta$-CVD, IL6-MDD, Serotonin-MDD), five are polygenic and cannot map, and 18 have no record in the universe (Supplementary Table~S7). Exact coverage of the 219 resolved pairs is 0; expanded coverage is 14 (6.4\%). Two causes are visible in the data: the frozen mapping sends the cardiometabolic families to the MeSH term Cardiovascular Diseases, under which the dataset's rows for \emph{CETP}, \emph{PCSK9} and \emph{LPL} are preclinical, and several launched targets in the scored set (\emph{TNF}, \emph{IL17A}, \emph{SLC5A2}, \emph{SLC6A4}) are unsupported in the dataset's sense and so outside the universe by definition. The scored families and the universe are largely different populations: the families were assembled from the MR literature, the universe from a pharmaceutical pipeline database with a genetic-association annotation. Of the 25 uncovered pairs sampled, 4 (16\%) have a published MR estimate with a confidence interval for the target's exposure on the indication (VEGFA and myopia, \emph{KCNJ11} and type~2 diabetes under two MeSH headings, \emph{IL12B} and ankylosing spondylitis; 3 under a narrow reading of the first, whose MR outcome is refractive error), and 13 return no PubMed result at all (Supplementary Table~S6). The 219 uncovered pairs are listed in Supplementary Table~S5. The screen measures the gap between the scored families and one external universe; it does not enumerate every family the inclusion rule would admit, and the scored families are not a random sample of eligible families.

\paragraph{Three MR states.}
Of the 32 scored families, 15 are MR-supportive (12 correct), 7 have their whole interval within the negligible range (6 correct: HRT-AD, BMI-AD, Homocysteine, CRP, VitD-Cancer, IL6-MDD, and Estrogen-BC, the miss), and 10 are inconclusive (6 correct). The 17 families the registered rule calls null therefore divide 7 negligible-range to 10 inconclusive; the inconclusive group holds the six scored families with no confidence interval (Metabolic-AD, ModRisk-AD, Smoking-MS/AD, TNF-$\alpha$-RA, IL-17-psoriasis, IL-1$\beta$-CVD), two whose interval reaches $\pm 0.10$ (HDL/CETP, Niacin/HDL), and two per-allele families without a conversion factor (CTLA-4-RA, Serotonin-MDD), which are scale-unresolved (8 of 41 families are). Four scored families carry an alignment flag (IGF1-CRC, indication mismatch; Anti-CD20-MS, IL6-MDD and Complement-GA, instrument--target mismatch), of which two are misses. No registered classification changes; the states are reported for all 41 families in Supplementary Table~S2. The negligible-range state is not comparable across per-SD, per-unit and per-allele contrasts, and its range is the registered threshold, not a clinically validated margin.

\paragraph{Outcome decomposition.}
The seven fields are reported for all 41 families in Supplementary Table~S3. Two families have a met primary endpoint and no approval: CRP and IL-1$\beta$-CVD, both scored on CANTOS, where canakinumab 150~mg met the prespecified threshold (HR 0.85, 95\% CI 0.74--0.98) and was not approved for cardiovascular risk reduction; their registered outcomes (no benefit; failed) hold as development outcomes and not as efficacy readouts. Vitamin~D-MS has mixed Phase~III readouts (VIDAMS not met; D-Lay MS met), HDL/CETP and Triglycerides are mixed at class level (anacetrapib met its endpoint and was not submitted; icosapent ethyl is approved while three other programs were not met), and Blood pressure and Triglycerides are coded as classes rather than programs. IL6-MDD is the one scored family whose readout is Phase~II, and its trial is recorded on the registry as completed with the primary endpoint not met. Four scored families (ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS) have no drug program named anywhere in the catalog: no holdout drug maps to them, their outcome was assigned at the family level, and every field is not reported. Among the eight misses, the five MR-null misses show target engagement and a met endpoint (the drug worked), and the three MR-supportive misses have no target-engagement measure in their pivotal reports, so the translation-gap criterion's engagement clause is satisfied by none of them on the record and the class rests on the efficacy readout alone. No miss shows engagement with an unmet endpoint; three scored families do (Niacin/HDL, Homocysteine, VitD-Cancer), all MR-null and all correctly classified, as does IL-6R, which is unscored. The fields are a single coder's reading and the attribution column in particular is labeled as such.

\paragraph{Analysis sets.}
\label{sec:analysis_sets}
Table~\ref{tab:sets} reports the registered analysis-set table. The registered set is the primary analysis and no set is promoted on the basis of its accuracy. The strict Phase~III set removes seven families: IL6-MDD, Blood pressure and Triglycerides (coded as classes), and the four program-less families, and scores 17/25; the four program-less families are all hits under the registered rule, so this set carries the largest change. Scoring Amyloid-AD on its observational estimate and the \emph{APOE4} association (OR 3.46, 95\% CI 3.27--3.65; \cite{belloy2023apoe}) adds one miss. Removing the five association-leg families removes three misses and two hits; removing also EBV-MS, the one family whose genetic-leg estimate (OR 5.0, 2.0--20.0) could not be traced to any source, removes one hit more (Supplementary Table~S8). Reclassifying IL6-MDD on the registration's instrument changes nothing. Collapsing the one pair of families identical on every evidence field (HDL/CETP and Niacin/HDL) removes a hit. Removing the families with author-estimated observational values removes three misses and either four hits (the seven the registration names) or two (the five the classifier flags; IL6-MDD and Serotonin-MDD carry meta-analytic values). Across the table the accuracy runs from 17/25 (68.0\%) to 23/28 (82.1\%); the sets differ by one to seven families, and none of the differences is a test.

\begin{table}[htbp]
\centering
\caption{Registered analysis-set table (Amendment~5). Number scored and number correct under each rule-consistent definition of the scored set. Permutation and binomial p-values are given only for the two sets tested before this table was registered; no test is run on the other sets, which differ from the registered set by one to seven families. The registered set is the primary analysis.}
\label{tab:sets}
\small
\begin{tabular}{p{5.6cm}p{5.8cm}rrr}
\toprule
Set & Definition & $n$ & Correct & Accuracy \\
\midrule
Registered & the 32 scored families (permutation $p = 0.005$, cluster-level $p = 0.005$, binomial $p = 0.004$) & 32 & 24 & 75.0\% \\
Strict Phase~III & trial phase III or post-marketing for the indication; removes IL6-MDD, Blood pressure, Triglycerides, ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS & 25 & 17 & 68.0\% \\
Amyloid-AD scored & registered set plus Amyloid-AD (concordance; failed) & 33 & 24 & 72.7\% \\
Strict Phase~III + Amyloid-AD & both changes & 26 & 17 & 65.4\% \\
MR-instrumented & removes the five association-leg families & 27 & 22 & 81.5\% \\
MR-instrumented, untraced removed & also removes EBV-MS & 26 & 21 & 80.8\% \\
Registration-consistent instrument & IL6-MDD on the declared IL6R instrument \cite{kelly2021il6r} & 32 & 24 & 75.0\% \\
Unique evidence & HDL/CETP and Niacin/HDL counted once & 31 & 23 & 74.2\% \\
Source-extracted OBS, registered list & removes the seven families the registration names & 25 & 20 & 80.0\% \\
Source-extracted OBS, classifier flags & removes the five families flagged author-estimated & 27 & 21 & 77.8\% \\
28-family sensitivity set & \S\ref{sec:sensitivity_set} (permutation $p = 0.0006$, cluster-level $p = 0.0002$, binomial $p < 0.001$) & 28 & 23 & 82.1\% \\
\bottomrule
\end{tabular}
\end{table}
"""
rep(r"""The failure-mode assignments of the remaining misses are unchanged.

\subsection{Failure modes}""",
    r"""The failure-mode assignments of the remaining misses are unchanged.""" + new_results + r"""
\subsection{Failure modes}""")

# Table 5 translation-gap criterion: the record carries no engagement measure for these families
rep(r"""Translation gap & Supp. & Failed & Instrument and drug act on the same pathway in the same window; the trial reports target engagement without endpoint benefit. Indication mismatch between the MR estimate and the trial is flagged where present & IGF1-CRC (indication mismatch), Complement-GA \\""",
    r"""Translation gap & Supp. & Failed & Instrument and drug act on the same pathway in the same window; the Phase~III program did not meet its endpoint. Target engagement is recorded where the report carries it (Supplementary Table~S3; none of these reports does). Indication mismatch between the MR estimate and the trial is flagged where present & IGF1-CRC (indication mismatch), Complement-GA \\""")

# Narratives
rep(r"""canakinumab's null primary endpoint in CANTOS despite lowering CRP.""",
    r"""canakinumab, which met its primary endpoint at 150~mg in CANTOS (HR 0.85) and was not approved for cardiovascular risk reduction.""")
rep(r"""\paragraph{Psychiatry.} IL-6/MDD: CRP elevation associates with depression (SMD 0.15; \cite{howren2009}) and the MR estimate on general CRP instruments is null (OR 1.01, 0.99--1.04); sirukumab, which neutralizes the IL-6 ligand, failed Phase~II for treatment-resistant MDD.""",
    r"""\paragraph{Psychiatry.} IL-6/MDD: CRP elevation associates with depression (SMD 0.15; \cite{howren2009}) and the MR estimate on polygenic CRP instruments is null (OR 1.01, 0.99--1.04; \cite{galan2022crpdepression}), as is the estimate on the IL6R \emph{cis} instruments the registration named (OR 1.023, 1.006--1.039; \cite{kelly2021il6r}); sirukumab, which neutralizes the IL-6 ligand, did not meet its primary endpoint in Phase~II for treatment-resistant MDD.""")
rep(r"""(\emph{APOE4} heterozygous OR~3.46, homozygous OR~15.65; \emph{APP}/\emph{PSEN} mutations cause autosomal dominant AD)""",
    r"""(\emph{APOE4} heterozygous OR~3.46, homozygous OR~15.65 \cite{belloy2023apoe}; \emph{APP}/\emph{PSEN} mutations cause autosomal dominant AD)""")
rep(r"""mepolizumab and benralizumab are approved \cite{pavord2012dream}.""",
    r"""mepolizumab (MENSA; \cite{ortega2014mensa}) and benralizumab are approved.""")

# Extension table: IL6-MDD and Serotonin-MDD values are meta-analytic, not author-estimated
rep(r"""IL6-MDD$^\text{i}$ & Psych & non-triv.$^\dagger$ & 1.01 (0.99--1.04)""",
    r"""IL6-MDD$^\text{i}$ & Psych & 0.15 & 1.01 (0.99--1.04)""")
rep(r"""Serotonin-MDD$^\text{j}$ & Psych & non-triv.$^\dagger$ & 1.08 (1.03--1.12)""",
    r"""Serotonin-MDD$^\text{j}$ & Psych & 0.45 & 1.08 (1.03--1.12)""")
rep(r"""MR: general CRP instruments, null for depression \cite{elliott2009}.""",
    r"""MR: polygenic CRP instruments, null for depression \cite{galan2022crpdepression}; on the IL6R \emph{cis} instruments the registration named, OR 1.023 (1.006--1.039) \cite{kelly2021il6r}, also null.""")

# Limitations
rep(r"""Ten families across the autoimmune and extension sets carry author-estimated rather than meta-analysis-sourced observational values, marked $^\dagger$ in Tables~\ref{tab:autoimmune} and~\ref{tab:extension}: CTLA-4-RA, JAK-STAT-RA, CD20-RA, Eos/IL5-Asthma, IL-4R$\alpha$-Asthma, TSLP-Asthma, IL23-Crohns, Complement-GA, Serotonin-MDD and IL6-MDD. Three are construct-limited and unscored, leaving seven in the scored set.""",
    r"""Eight families across the autoimmune and extension sets carry author-estimated rather than meta-analysis-sourced observational values, marked $^\dagger$ in Tables~\ref{tab:autoimmune} and~\ref{tab:extension}: CTLA-4-RA, JAK-STAT-RA, CD20-RA, Eos/IL5-Asthma, IL-4R$\alpha$-Asthma, TSLP-Asthma, IL23-Crohns and Complement-GA. Three are construct-limited and unscored, leaving five in the scored set.""")
rep(r"""All ten fall on the non-trivial side, the closest at an estimated $0.15$ against a $0.10$ floor. The invariance result rests on the near-constancy of the observational class, and in seven scored families that class rests on these estimates: had any of the seven been read as trivial, the family would have moved to the null-concordance or genetic-only cell. The invariance is therefore established on the estimates as made, not independently of them.""",
    r"""All eight fall on the non-trivial side, the closest at an estimated $0.15$ against a $0.10$ floor. The invariance result rests on the near-constancy of the observational class, and in five scored families that class rests on these estimates: had any of the five been read as trivial, the family would have moved to the null-concordance or genetic-only cell. The invariance is therefore established on the estimates as made, not independently of them; without the five, 21 of 27 families are classified correctly (Table~\ref{tab:sets}).""")
rep(r"""\paragraph{Ascertainment.} The original 27 mechanism families were selected from well-known programs with the trial outcomes public, introducing possible outcome-influenced selection, and no systematic enumeration of candidate families preceded that selection.""",
    r"""\paragraph{Ascertainment.} The original 27 mechanism families were selected from well-known programs with the trial outcomes public, introducing possible outcome-influenced selection, and no systematic enumeration of candidate families preceded that selection. Against an external universe of 219 genetically supported target--indication pairs with a Phase~III outcome, the scored families cover 14 under the widest mapping and none exactly, and about one in six of the uncovered pairs has an MR estimate the inclusion rule would have admitted (\S\ref{sec:screen_results}); the reported accuracy is a property of the assembled families, not of that universe.""")

# Conclusions
rep(r"""a 28-family sensitivity analysis gives the same reading.""",
    r"""across the registered analysis-set table the count runs from 17/25 to 23/28 (Table~\ref{tab:sets}).""")

# Discussion, alternatives to a fixed threshold
rep(r"""or by a polygenic score is classified correctly; coding variants reach 5/8, and all eight misclassifications fall in the coding-variant and biomarker-GWAS classes.""",
    r"""or by a polygenic score is classified correctly (7/7 and 5/5); coding variants reach 5/8 and biomarker GWAS 7/12, and all eight misclassifications fall in those two classes.""")

# Back matter
rep(r"""the 28-family sensitivity analysis with its permutation tests (\texttt{run\_revised\_primary.py}), and the complete classification dataset (41 families with effect sizes, CIs, sources, MR contrast and instrument set; \texttt{cross\_design\_classification\_all\_41\_families\_v3.csv}) are available at""",
    r"""the 28-family sensitivity analysis with its permutation tests (\texttt{run\_revised\_primary.py}), the registered procedures of \S\ref{sec:procedures} (\texttt{analysis/amendment5/}: \texttt{run\_screen.py}, \texttt{run\_mr\_states.py}, \texttt{run\_analysis\_sets.py}, the outcome codebook with its source log, the MR-instrumented audit and the IL6-MDD search record), the complete classification dataset (41 families with effect sizes, CIs, sources, MR contrast and instrument set; \texttt{cross\_design\_classification\_all\_41\_families\_v3.csv}) and Supplementary Tables~S2--S8 (MR states, outcome codebook, analysis sets, uncovered universe pairs, MR-availability sample, family match status, MR-instrumented audit) are available at""")
rep(r"\bibliography{references_v9_r3}", r"\bibliography{references_v10_r4}")

# Citation corrections found by the MR-instrumented audit: the urate-gout MR numbers (26 SNPs, OR 3.41-6.04
# per mg/dL across 7 methods) are Jordan et al. 2019, PLoS Med (PMID 30645594), not the 2017 umbrella review.
rep(r"""\cite{li2019uratemr}""", r"""\cite{jordan2019urate}""", count=2)

# The IL23R R381Q entry the bibliography prints is Cotterill et al. 2010 (rs11209026, 26 studies, OR 0.46);
# the footnote carried a number from a record that could not be located. Construct-limited family, unscored.
# nie2015il23r: source reports OR 0.41 (0.37-0.46); v26 already prints 0.41, no edit.

# Metabolic-AD: the stored OR 1.01 is Walter et al. 2016 (PMID 26650880), 1.01 (0.96-1.06).
rep(r"""T2D associates with AD in observational cohorts (RR~1.53, $d = 0.24$); MR finds no causal effect (OR~1.01, $d = 0.006$).""",
    r"""T2D associates with AD in observational cohorts (RR~1.53, $d = 0.24$); MR finds no causal effect (OR~1.01, 95\% CI 0.96--1.06, $d = 0.006$; \cite{walter2016t2dad}).""")

# =============================================================================
# Checks
# =============================================================================
for bad in ["zombie", "revised primary", "requested during", "peer review", "the reviewer", "reviewer 1", "reviewer 4", "reviewer 5", "this revision", "non-triv.$^\\dagger$ & 1.01", "non-triv.$^\\dagger$ & 1.08"]:
    assert bad.lower() not in text.lower(), bad
for lab in ["sec:procedures", "sec:screen_results", "sec:analysis_sets", "tab:sets"]:
    assert text.count(f"\\label{{{lab}}}") == 1 and text.count(f"\\ref{{{lab}}}") >= 1, lab
for key in ["galan2022crpdepression", "kelly2021il6r", "belloy2023apoe", "ortega2014mensa", "jordan2019urate", "walter2016t2dad"]:
    pass
for key in ["galan2022crpdepression", "kelly2021il6r", "belloy2023apoe", "ortega2014mensa", "jordan2019urate", "walter2016t2dad"]:
    assert key in text, key
    assert key in (HERE.parent / "references_v10_r4.bib").read_text(encoding="utf-8"), key
assert text.count(r"\cite{elliott2009}") == 1   # the CRP-CHD family only
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, words

DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
