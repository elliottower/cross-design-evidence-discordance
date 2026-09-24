"""v26c -> v26d: fixes from a blind read of v26c (internal consistency, narration, prose), and
section-sign markers on every tabulated value that differs from its source.

Run:  uv run --no-project --with pyyaml python paper/patches/patch_v26d_round4.py

Exact-match edits, each required to match once; v26c is not touched.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = HERE.parent / "paper_v26c_round4.tex"
DST = HERE.parent / "paper_v26d_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


vo = json.loads((ROOT / "analysis/provenance/value_origin_summary.json").read_text())
num = vo["numeric"]
assert num == {"quoted": 34, "replacement_citation": 5, "derived": 4, "author_estimated": 5, "coding_error": 14, "not_checked": 2}, num
assert (vo["numeric_agree"], vo["numeric_checked"]) == (43, 62)
S = r"$^\S$"

# ---- abstract, Methods ------------------------------------------------------------------------
rep(r"""Two genetic-association families are reported apart from MR-instrumented families.""",
    r"""Five families whose genetic leg is a variant--disease association are reported apart from MR-instrumented families.""")
rep(r"""Each input value was coded from its cited source with the assistance of Claude Code (Anthropic) and verified against a passage quoted from that source; Appendix~A reports the values that did not match.""",
    r"""Each input value was coded from its cited source with the assistance of Claude Code (Anthropic), and each value with a named source was verified against a passage quoted from that source; Appendix~A reports the values that do not match.""")
rep(r"""and MR for estradiol (null, OR~1.00, 95\% CI 0.85--1.18; \cite{barth2025}).""",
    r"""and MR for estradiol (null; \cite{barth2025}).""")
rep(r"""Observational cohort evidence for vitamin~D and MS risk \cite{munger2006}, added to the existing MR entry; the registered value is listed in Appendix~A.""",
    r"""Observational cohort evidence for vitamin~D and MS risk \cite{munger2006}, added to the existing MR entry. The registered value (OR~1.40, 1.19--1.64) is not the estimate this source reports (Appendix~A).""")
rep("""IL6-MDD, is coded on a Phase~II readout declared in advance (Amendment~2), against this
criterion,""", """IL6-MDD, is coded on a Phase~II readout declared in advance (Amendment~2), an exception to this
criterion,""")
rep(r"""and counts two families that share identical evidence once (28 families; \S\ref{sec:sensitivity_set}).""",
    r"""and counts CRP and IL-1$\beta$-CVD, which share the same observational estimate and null MR magnitude, once (28 families; \S\ref{sec:sensitivity_set}).""")
rep(r"""The 28-family sensitivity analysis (\S\ref{sec:sensitivity_set}) sets aside the two identified first; the MR-instrumented analysis set (\S\ref{sec:analysis_sets}) removes all five.""",
    r"""The 28-family sensitivity analysis (\S\ref{sec:sensitivity_set}) sets aside two of them (Complement-GA, Serotonin-MDD); the MR-instrumented analysis set (\S\ref{sec:analysis_sets}) removes all five.""")
rep(r"""\paragraph{Analysis sets.} One table reports the number scored and the number correct across sets, each defined by a rule named before scoring: the registered set; the registered families whose coded trial phase is III or post-marketing for the family's indication; the registered set plus Amyloid-AD, classified under the registered rule on its observational estimate and the \emph{APOE4} association; both changes together; the registered set without families whose genetic leg is a variant--disease association (audited from every cited source; a family whose estimate could not be traced stays in the set and is listed, and the set is also reported with it removed); the registered set with IL6-MDD classified on the estimate the registration named (below); families identical on every evidence field counted once; the registered set without the families whose observational value was author-estimated (reported twice, on the list the registration names and on the classifier's own flags, which differ for two families whose values are meta-analytic); and the 28-family sensitivity set.""",
    r"""\paragraph{Analysis sets.} One table reports the number scored and the number correct across sets, each defined by a rule named before scoring:
(1)~the registered set;
(2)~the registered families whose coded trial phase is III or post-marketing for the family's indication;
(3)~the registered set plus Amyloid-AD, classified under the registered rule on its observational estimate and the \emph{APOE4} association;
(4)~changes (2) and (3) together;
(5)~the registered set without families whose genetic leg is a variant--disease association, audited from every cited source, and reported again with the one family whose design could not be established also removed;
(6)~the registered set with IL6-MDD classified on the estimate the registration named (below);
(7)~families identical on every evidence field counted once;
(8)~the registered set without the families whose observational value was author-estimated, reported on the list the registration names and on the classifier's own flags, which differ for two families whose values are meta-analytic;
(9)~the 28-family sensitivity set.
One further set, defined after the others were scored, removes the families whose outcome has no documented Phase~III program; it is marked in the table.""")

# ---- Results --------------------------------------------------------------------------------
rep(r"""observational evidence agrees (OR~1.40, $d = 0.19$), and the trial""",
    r"""observational evidence agrees (registered OR~1.40, $d = 0.19$; its source reports a different estimate, Appendix~A), and the trial""")
rep(r"""producing qualitative discordance, an expected failure, which the weight-loss trial record matches.""",
    r"""producing qualitative discordance, an expected failure.""")
rep(r"""of which 6 are correctly classified; 4 misses include the original 2 (IGF1-CRC, Estrogen-BC) plus Complement-GA (translation gap) and Serotonin-MDD (mechanism bypass).""",
    r"""of which 6 are correctly classified; the 4 misses are IGF1-CRC, Estrogen-BC, Complement-GA (translation gap) and Serotonin-MDD (mechanism bypass).""")
rep(r"""it removes three misses and no hit, so it cannot lower the figure, and it is reported after the registered count for that reason.""",
    r"""it removes three misses and one duplicated hit, and it is reported after the registered count.""")
rep(r"""the inconclusive group holds the six scored families with no confidence interval""",
    r"""the inconclusive group holds the six scored families with no confidence interval among the frozen inputs""")
rep(r"""Two families have a met primary endpoint and no approval: CRP and IL-1$\beta$-CVD, both scored on CANTOS,""",
    r"""Two families have a met primary endpoint and no approval, CRP and IL-1$\beta$-CVD, both scored on CANTOS,""")
rep(r"""the four program-less families are all hits under the registered rule, so this set carries the largest change.""",
    r"""the four program-less families are all hits under the registered rule.""")
rep(r"""removing also EBV-MS, the one family whose genetic-leg estimate (OR 5.0, 2.0--20.0) could not be traced to any source, removes one hit more (Supplementary Table~S8).""",
    r"""removing also EBV-MS, the one family whose genetic-leg design could not be established, removes one hit more (Supplementary Table~S8).""")
rep(r"""removes three misses and either four hits (the seven the registration names) or two (the five the classifier flags; IL6-MDD and Serotonin-MDD carry meta-analytic values).""",
    r"""removes three misses and four hits (the seven the registration names), or two misses and three hits (the five the classifier flags; IL6-MDD and Serotonin-MDD carry meta-analytic values).""")
rep(r"""Across the table the accuracy runs from 17/25 (68.0\%) to 23/28 (82.1\%);""",
    r"""Across the table the accuracy runs from 17/26 (65.4\%) to 23/28 (82.1\%);""")
rep(r"""Documented Phase~III program & removes ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS & 28 & 20 & 71.4\% \\""",
    r"""Documented Phase~III program$^\ast$ & removes ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS & 28 & 20 & 71.4\% \\""")
rep(r"""which differ from the registered set by one to seven families. The registered set is the primary analysis.}""",
    r"""which differ from the registered set by one to seven families. The registered set is the primary analysis. $^\ast$Set defined after the registered sets were scored.}""")
rep(r"""RCT $d = 0.04$ against etiologic $d > 0.80$ is the translation-gap pattern: the mechanism is involved in pathogenesis, and clearing amyloid at the stage of clinical disease does not reverse the downstream pathology. Why is a hypothesis; that the gap exists is what the data show.""",
    r"""RCT $d = 0.04$ against etiologic $d > 0.80$ is the translation-gap pattern: the mechanism is involved in pathogenesis, and clearing amyloid at the stage of clinical disease does not reverse the downstream pathology; the reason is a hypothesis.""")
rep(r"""and all four produced drug failures: torcetrapib, dalcetrapib, and evacetrapib (CETP inhibitors); AIM-HIGH and HPS2-THRIVE (niacin); B-vitamin trials; and canakinumab,""",
    r"""and none led to an approved drug for cardiovascular prevention: torcetrapib, dalcetrapib, and evacetrapib (CETP inhibitors); AIM-HIGH and HPS2-THRIVE (niacin); B-vitamin trials; and canakinumab,""")
rep(r"""A disorder-level version of this domain had failed earlier: applied to six disorder-level families (31 drugs, 24 classifiable), the rule reached 58\% with zero specificity,""",
    r"""Applied to six disorder-level families (31 drugs, 24 classifiable), the rule reaches 58\% with zero specificity,""")
rep(r"""The classes are preliminary generative hypotheses.}""",
    r"""The classes are preliminary generative hypotheses. No miss has a recorded target-engagement measure, so the translation-gap class rests on the efficacy readout alone.}""")

# ---- Limitations, Conclusions ----------------------------------------------------------------
rep(r"""CTLA-4-RA ($d_{\text{MR}} = 0.083$) becomes causal at a threshold of $0.08$""",
    r"""CTLA-4-RA ($d_{\text{MR}} = 0.083$) becomes supportive at a threshold of $0.08$""")
rep(r"""These entries are now reported qualitatively rather than as numerical SMDs, because a number implies a precision the sources do not supply. Nothing is lost by doing so: the classifier consumes""",
    r"""The classifier consumes""")
rep(r"""All eight fall on the non-trivial side, the closest at an estimated $0.15$ against a $0.10$ floor.""",
    r"""All eight fall on the non-trivial side, the lowest at an estimated $0.40$ against a $0.10$ floor.""")
rep(r"""The estimates and their sources remain in the supplementary classification file.""",
    r"""The estimates and their sources remain in the supplementary classification file. The registered rule requires an effect size and confidence interval extractable from the source; six scored families enter with no interval among the frozen inputs, and for two of them (TNF-$\alpha$-RA, IL-1$\beta$-CVD) the value 1.00 stands for a null result rather than a reported estimate (Appendix~A).""")
rep(r"""across the registered analysis-set table the count runs from 17/25 to 23/28 (Table~\ref{tab:sets}).""",
    r"""across the registered analysis-set table the count runs from 17/26 to 23/28 (Table~\ref{tab:sets}).""")

# ---- Appendix A -----------------------------------------------------------------------------
rep(r"""Of the 64 numeric input values of the 32 scored families, 62 were checked against a source. 48 of the 62 (77\%) agree with it: 34 appear in the source cited, 5 appear in a source other than the one previously cited, and 9 are stated transformations of a source value. The derivations are the Urate-Gout MR estimate (rescaled to 1~SD of serum urate), the Urate-Gout observational estimate (read from a dose-response curve), the Blood-pressure observational estimate ($\sqrt{2}$ from a twofold difference per 20~mmHg), the IL-17-psoriasis MR estimate ($\exp(\hat\beta)$ of the reported coefficient), and the five author-estimated observational values marked $^\dagger$ in the tables. 14 values do not match their source (Table~\ref{tab:coding}); the two observational values not checked (ModRisk-AD, EBV-MS) have no source named in the catalog.""",
    r"""Of the 64 numeric input values of the 32 scored families, 62 were checked against a source. 43 of the 62 (69\%) agree with it. Of these, 34 appear in the source cited, 5 appear in a source other than the one the catalog recorded, and 4 are stated transformations of a source value: the Urate-Gout MR estimate (rescaled to 1~SD of serum urate), the Urate-Gout observational estimate (read from a dose-response curve), the Blood-pressure observational estimate ($\sqrt{2}$ from a twofold difference per 20~mmHg), and the IL-17-psoriasis MR estimate ($\exp(\hat\beta)$ of the reported coefficient). A further 5 are author estimates, marked $^\dagger$ in the tables. 14 values do not match their source (Table~\ref{tab:coding}, marked $^\S$ in the tables); the two observational values not checked (ModRisk-AD, EBV-MS) have no source named in the catalog.""")
rep(r"""Under the source's own values, no family's expected outcome or score changes; one family's label changes (IGF1-CRC).""",
    r"""Among the values for which a source figure exists, applying the registered rule to the source's figure changes no family's expected outcome or score; one family's label changes (IGF1-CRC).""")
rep(r"""& excluded (no program) \\
EBV-MS, MR""", r"""& scored hit in the registered set; outside the documented-program set \\
EBV-MS, MR""")
rep(r"""nearest are observational (infectious mononucleosis, OR 5.5, 1.5--19.7) & excluded (no program) \\""",
    r"""nearest are observational (infectious mononucleosis, OR 5.5, 1.5--19.7) & scored hit in the registered set; outside the documented-program set \\""")

# ---- section-sign markers on tabulated values that differ from the source -------------------
note = r"$^\S$Value differs from what its source reports; Appendix~A, Table~\ref{tab:coding}."
rep(r"""Anti-CD20-MS & 0.103 & Yes & 1.084 & Non-triv.""", rf"""Anti-CD20-MS & 0.103 & Yes & 1.084{S} & Non-triv.""")
rep(r"""HRT-AD & 0.000 & No & 0.221 & Non-triv.""", rf"""HRT-AD & 0.000{S} & No & 0.221 & Non-triv.""")
rep(r"""ModRisk-AD & 0.053 & --- & 0.209 & Non-triv.""", rf"""ModRisk-AD & 0.053{S} & --- & 0.209 & Non-triv.""")
rep(r"""EBV-MS & 0.887 & Yes & 0.293 & Non-triv.""", rf"""EBV-MS & 0.887{S} & Yes & 0.293 & Non-triv.""")
rep(r"""VitD-MS & 0.382 & Yes & 0.186 & Non-triv.""", rf"""VitD-MS & 0.382 & Yes & 0.186{S} & Non-triv.""")
rep(r"""{\footnotesize $^*$BMI-AD: CI excludes null (1.01--1.05) but $d = 0.016 < 0.10$, so MR is classified as null under the two-criterion rule.\\""",
    r"""{\footnotesize $^*$BMI-AD: CI excludes null (1.01--1.05) but $d = 0.016 < 0.10$, so MR is classified as null under the two-criterion rule. """ + note + r"""\\""")
rep(r"""LDL / PCSK9$^\text{e}$ & 1.52 &""", rf"""LDL / PCSK9$^\text{{e}}$ & 1.52{S} &""")
rep(r"""Blood pressure$^\text{f}$ & 1.41 & 1.44 (1.35--1.55) &""", rf"""Blood pressure$^\text{{f}}$ & 1.41 & 1.44 (1.35--1.55){S} &""")
rep(r"""$^\text{f}$Per 10 mmHg SBP for stroke.""", note + r""" $^\text{f}$Per 10 mmHg SBP for stroke.""")
rep(r"""IL-23-psoriasis & Psor. & 0.660 & 0.267""", rf"""IL-23-psoriasis & Psor. & 0.660{S} & 0.267""")
rep(r"""CTLA-4-RA$^\dagger$ & RA & non-triv. & 0.083 &""", rf"""CTLA-4-RA$^\dagger$ & RA & non-triv. & 0.083{S} &""")
rep(r"""TNF-$\alpha$-RA & RA & 1.930 & 0.000 & Null""", rf"""TNF-$\alpha$-RA & RA & 1.930 & 0.000{S} & Null""")
rep(r"""IL-1$\beta$-CVD & CVD & 0.174 & 0.000 & Null""", rf"""IL-1$\beta$-CVD & CVD & 0.174 & 0.000{S} & Null""")
rep(r"""show supportive MR and are correctly classified.}""", r"""show supportive MR and are correctly classified. """ + note + "}")
rep(r"""IGF1-CRC$^\text{b}$ & Onco & 1.12 &""", rf"""IGF1-CRC$^\text{{b}}$ & Onco & 1.12{S} &""")
rep(r"""SGLT2-HF$^\text{g}$ & Metab & 1.75 &""", rf"""SGLT2-HF$^\text{{g}}$ & Metab & 1.75{S} &""")
rep(r"""& 2.50 (2.20--2.85) & 0.505 & Assoc.""", rf"""& 2.50 (2.20--2.85){S} & 0.505 & Assoc.""")
rep(r"""\noindent{\footnotesize \textit{Notes to Table~\ref{tab:extension}.} """, r"""\noindent{\footnotesize \textit{Notes to Table~\ref{tab:extension}.} """ + note + " ")

# ---- checks -----------------------------------------------------------------------------------
for dead in ["no hit, so it cannot lower", "17/25 (68.0", "17/25 to 23/28", "the two identified first", "had failed earlier",
             "becomes causal", "Nothing is lost", "estimated $0.15$", "previously cited", "Why is a hypothesis", "Two genetic-association families",
             "which the weight-loss trial record matches", "OR~1.00, 95\\% CI 0.85"]:
    assert dead not in text, dead
assert text.count(r"$^\S$") >= 16
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, words
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; wrote {DST.name}")
