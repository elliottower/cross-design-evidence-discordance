"""v26b -> v26c: source verification of every input value.

Run:  uv run --no-project --with pyyaml python paper/patches/patch_v26c_round4.py

Every edit is an exact-string replacement that must match exactly once; the script aborts on
the first miss and writes nothing. v26b is not touched. Counts are read from
analysis/provenance/value_origin_summary.json, analysis/amendment5/analysis_sets/analysis_sets.json
and the claims/ directory, and asserted.

What changes:
  Methods    coding clause (Claude Code, verification by quotation); class-level outcome coding
  Results    20/28 sentence (families with a documented Phase III program) and its table row
  Tables     printed values restored to the frozen inputs (VitD-Cancer, Eos/IL5-Asthma);
             footnotes re-cited to the sources that report each value
  Narratives re-citations (McCullough, Lawler, Guyatt, Murphy, Shumaker 2004, Castro, Delgado,
             FDA label, Wald, ERFC, Sarwar, Lewington, Ohkuma); APOE4 13.04; one NRSI not pooled;
             quintiles not tertiles; TG per log-unit
  Intro/Disc re-citations for pitfalls, triangulation, lifelong exposure, target trial emulation;
             unsupported Ference sentence removed; Gill 2021 stated as the source states it
  Appendix A Source Verification of Input Values: counts, derivations, coding-error table
  Back matter Acknowledgements and Data Availability name the coding tool, claims/ and the verify command
"""
import glob
import json
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = HERE.parent / "paper_v26b_round4.tex"
DST = HERE.parent / "paper_v26c_round4.tex"
text = SRC.read_text(encoding="utf-8")
applied = 0


def rep(old, new, count=1):
    global text, applied
    n = text.count(old)
    assert n == count, f"expected {count} match(es), found {n}:\n{old[:200]}"
    text = text.replace(old, new)
    applied += 1


# ---- counts, read from the files ------------------------------------------------------------
vo = json.loads((ROOT / "analysis/provenance/value_origin_summary.json").read_text())
num = vo["numeric"]
N_NUM = sum(num.values())
N_CHECKED = vo["numeric_checked"]
N_AGREE = vo["numeric_agree"]
assert (N_NUM, N_CHECKED, N_AGREE) == (64, 62, 48), (N_NUM, N_CHECKED, N_AGREE)
assert num == {"quoted": 34, "replacement_citation": 5, "derived": 9, "coding_error": 14, "not_checked": 2}, num
assert vo["counts"]["outcome_documented"] == 28 and vo["counts"]["outcome_no_program"] == 4
sets = {t["set"]: t for t in json.loads((ROOT / "analysis/amendment5/analysis_sets/analysis_sets.json").read_text())["table"]}
assert (sets["documented Phase III program"]["correct"], sets["documented Phase III program"]["n"]) == (20, 28)
n_files = n_quotes = n_pdf = n_abs = n_html = 0
for f in glob.glob(str(ROOT / "claims/*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    q = sum(len(c.get("quotes", [])) for c in (d.get("claims") or {}).values())
    if not q:
        continue
    n_files += 1
    n_quotes += q
    loc = d["source"].get("local", "")
    n_pdf += loc.endswith(".pdf")
    n_abs += loc.endswith(".abstract.txt")
    n_html += not (loc.endswith(".pdf") or loc.endswith(".abstract.txt"))
assert n_quotes >= 169 and n_files >= 88, (n_files, n_quotes)
PCT = f"{100 * N_AGREE / N_CHECKED:.0f}"

rep(r"\usepackage[section]{placeins}", "\\usepackage[section]{placeins}\n\\usepackage{array}")

# =============================================================================================
# Methods
# =============================================================================================
rep(r"""Sources were published systematic reviews, meta-analyses, MR studies, and landmark RCTs.""",
    r"""Sources were published systematic reviews, meta-analyses, MR studies, and landmark RCTs. Each input value was coded from its cited source with the assistance of Claude Code (Anthropic) and verified against a passage quoted from that source; Appendix~A reports the values that did not match.""")
rep("class containing both outcomes is coded on the majority of its programs. The outcome is",
    "class containing both outcomes is coded on the majority of its programs, and two families without a single\nprogram (Blood pressure, Triglycerides) are coded on the drug class. The outcome is")

# =============================================================================================
# Results: the documented-program set
# =============================================================================================
rep(r"""All eight misses under the registered rule are assigned to boundary classes by the criteria in Table~\ref{tab:criteria}; the classes are preliminary generative hypotheses (Table~\ref{tab:provenance}).""",
    r"""All eight misses under the registered rule are assigned to boundary classes by the criteria in Table~\ref{tab:criteria}; the classes are preliminary generative hypotheses (Table~\ref{tab:provenance}). Four scored families (ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS) carry an outcome with no documented Phase~III program. Excluding them, the rule classifies 20/28 correctly (71.4\%).""")
rep(r"""Unique evidence & HDL/CETP and Niacin/HDL counted once & 31 & 23 & 74.2\% \\""",
    r"""Unique evidence & HDL/CETP and Niacin/HDL counted once & 31 & 23 & 74.2\% \\
Documented Phase~III program & removes ModRisk-AD, Smoking-MS/AD, BMI-AD, EBV-MS & 28 & 20 & 71.4\% \\""")

# =============================================================================================
# Tables: printed values = frozen inputs; footnotes cite the sources that report them
# =============================================================================================
rep(r"""VitD-Cancer$^\text{a}$ & Onco & 0.80 & 1.00 (0.93--1.08) & 0.00 & Null & Failed & Disc. & $\checkmark$ \\""",
    r"""VitD-Cancer$^\text{a}$ & Onco & 0.78 & 0.97 (0.88--1.07) & 0.017 & Null & Failed & Disc. & $\checkmark$ \\""")
rep(r"""Eos/IL5-Asthma$^\text{d}$ & Resp & non-triv.$^\dagger$ & 1.50 (1.25--1.80) & 0.223 & Supp. & Appr. & Conc. & $\checkmark$ \\""",
    r"""Eos/IL5-Asthma$^\text{d}$ & Resp & non-triv.$^\dagger$ & 1.50 (1.23--1.83) & 0.224 & Supp. & Appr. & Conc. & $\checkmark$ \\""")
rep(r"""$^\text{a}$OBS: highest vs.\ lowest quintile 25(OH)D and colorectal cancer; OR from prospective meta-analysis \cite{keum2014vitdobscancer}. MR: 80+ instruments, null for total cancer \cite{ong2021vitdcancer}.""",
    r"""$^\text{a}$OBS: 25(OH)D and colorectal cancer, top vs.\ middle quintile, pooled 17 cohorts, RR 0.78 (0.65--0.94) \cite{mccullough2019vitd}. MR: per SD 25(OH)D and colorectal cancer, systematic review of MR studies \cite{lawler2023vitd}.""")
rep(r"""$^\text{b}$OBS: highest vs.\ lowest quintile IGF-1 and CRC; pooled prospective OR \cite{rinaldi2019igfobs}.""",
    r"""$^\text{b}$OBS: circulating IGF-1, UK Biobank \cite{murphy2020igf}; the registered value is the source's per-SD estimate for distal colon cancer, and its colorectal highest-vs.-lowest-quintile estimates are given in Appendix~A.""")
rep(r"""MR: eosinophil count per SD and moderate-severe asthma \cite{han2020eosinophilasthma}.""",
    r"""MR: eosinophil count per SD and moderate-severe asthma, weighted median \cite{guyatt2023eos}.""")
rep(r"""Dupilumab approved \cite{busse2019dupilumab}. Excluded as construct-limited.""",
    r"""Dupilumab reduced severe exacerbations by 47.7\% in QUEST \cite{castro2018quest}. Excluded as construct-limited.""")
rep(r"""$^\text{g}$OBS: T2D and HF risk \cite{ference2019}.""",
    r"""$^\text{g}$OBS: T2D and HF risk, meta-analysis of cohorts \cite{ohkuma2019diabetesHF} (sex-specific RRs; Appendix~A).""")
rep(r"""$^\text{g2}$OBS: serum urate and incident gout, longitudinal cohort; per-SD HR 3.2 from dose-response curve \cite{robinson2021urate}. MR: 26 SNPs, OR 5.0 per SD (range 4.4--8.7 across methods) \cite{jordan2019urate}.""",
    r"""$^\text{g2}$OBS: serum urate and incident gout, longitudinal cohort; per-SD HR 3.2 read from the dose-response curve of \citet{robinson2021urate}, which reports band-wise hazard ratios only. MR: OR 5.0 per SD, rescaled from the per-mg/dL range of 3.41--6.04 across seven MR methods in \citet{jordan2019urate} to 1 SD of serum urate (1.2~mg/dL); the interval 3.5--8.0 is the rescaled range, not a confidence interval.""")
rep(r"""$^\text{b}$OBS per 5 $\mu$mol/L; MR is MTHFR TT vs CC \cite{clarke2012}.""",
    r"""$^\text{b}$OBS per 5 $\mu$mol/L, prospective studies \cite{wald2002homocysteine}; MR is MTHFR TT vs CC \cite{clarke2012}.""")
rep(r"""$^\text{c}$OBS per 1 SD log CRP (ERFC); MR per 20\% lower CRP \cite{elliott2009}.""",
    r"""$^\text{c}$OBS per 1 SD log CRP \cite{kaptoge2010crp}; MR per 20\% lower CRP \cite{elliott2009}.""")
rep(r"""$^\text{e}$Per 1 mmol/L. LDL OBS from prospective meta-analyses \cite{ference2019ldl}; LDL MR from \citet{holmes2015}. TG OBS from Sarwar 2007 (top vs.\ bottom tertile); TG MR from \citet{holmes2015} unrestricted score.""",
    r"""$^\text{e}$LDL per 1 mmol/L: OBS from prospective meta-analyses \cite{ference2019ldl}, MR from \citet{holmes2015}. TG: OBS top vs.\ bottom tertile \cite{sarwar2007tg}; MR per 1 log-unit, unrestricted score \cite{holmes2015}.""")
rep(r"""$^\text{f}$Per 10 mmHg SBP for stroke; OBS from Lewington 2002 (PSC); MR from \citet{georgakis2020}.""",
    r"""$^\text{f}$Per 10 mmHg SBP for stroke. OBS 1.41 is $\sqrt{2}$, from the twofold difference in stroke death per 20 mmHg reported by \citet{lewington2002bp}; MR from \citet{georgakis2020}.""")
rep(r"""$^\text{m}$OBS: Szulc 2013 MINOS prospective cohort \cite{szulc2014}.""",
    r"""$^\text{m}$OBS: MINOS prospective cohort, two highest vs.\ three lowest quintiles \cite{szulc2014}.""")

# =============================================================================================
# Narratives
# =============================================================================================
rep(r"""an inverse observational association with colorectal cancer (highest vs.\ lowest quintile OR~0.80; \cite{keum2014vitdobscancer}), null MR across cancer subtypes with 80+ instruments \cite{ong2021vitdcancer}, and""",
    r"""an inverse observational association with colorectal cancer (top vs.\ middle quintile RR~0.78, 0.65--0.94; \cite{mccullough2019vitd}), a null MR estimate for colorectal cancer (OR~0.97, 0.88--1.07; \cite{lawler2023vitd}), and""")
rep(r"""(OR~1.50 per SD; \cite{han2020eosinophilasthma})""", r"""(OR~1.50 per SD, 1.23--1.83; \cite{guyatt2023eos})""")
rep(r"""IL-4R$\alpha$ (dupilumab \cite{busse2019dupilumab})""", r"""IL-4R$\alpha$ (dupilumab \cite{castro2018quest})""")
rep(r"""with a trivial observational leg ($d_{\text{OBS}} = 0.063$; \cite{rinaldi2019igfobs})""",
    r"""with a trivial observational leg as registered ($d_{\text{OBS}} = 0.063$; \cite{murphy2020igf}; the same source's colorectal highest-vs.-lowest-quintile estimates give $d = 0.12$--$0.16$, Appendix~A)""")
rep(r"""MR for estradiol is null (OR~1.00; \cite{barth2025}); WHIMS found HRT \emph{increased} dementia risk (HR~1.76; \cite{shumaker2003}). The protective observational signal is the healthy-user bias that \citet{hernan2008} identified in the HRT-cardiovascular discrepancy, and the rule flags the family from etiologic evidence alone.""",
    r"""MR for estradiol is null \cite{barth2025}; WHIMS found HRT \emph{increased} dementia risk (pooled HR~1.76, 1.19--2.60; \cite{shumaker2004whims}). The pattern parallels the HRT-cardiovascular discrepancy that \citet{hernan2008} resolved by emulating the trial, and the rule flags the family from etiologic evidence alone.""")
rep(r"""pooled non-randomized studies give a relapse hazard ratio of 0.14""", r"""a non-randomized study gives a relapse hazard ratio of 0.14""")
rep(r"""Rituximab supplies the observational estimate and is widely used off-label in MS, with substantial clinical and registry evidence behind it,""",
    r"""Rituximab supplies the observational estimate and is widely used off-label in MS, with substantial clinical and registry evidence behind it \cite{brancati2021rituximab},""")
rep(r"""while ocrelizumab, ofatumumab, and ublituximab do \cite{brancati2021rituximab}.""",
    r"""while ocrelizumab, ofatumumab, and ublituximab do \cite{delgado2024antiCD20,fda2022briumvi}.""")
rep(r"""homozygous OR~15.65 \cite{belloy2023apoe}""", r"""homozygous OR~13.04 \cite{belloy2023apoe}""")
rep(r"""(OR~3.46 per allele)""", r"""(OR~3.46 for one copy)""")
rep(r"""T2D associates with AD in observational cohorts (RR~1.53, $d = 0.24$);""",
    r"""T2D associates with AD in observational cohorts (RR~1.53, 1.42--1.63, $d = 0.24$; \cite{zhang2017t2dad});""")
rep(r"""(HR~0.55, highest vs.\ lowest tertile)""", r"""(HR~0.55, two highest vs.\ three lowest quintiles)""")
rep(r"""Observational cohort evidence for low vitamin~D and MS risk (OR~1.40, 95\% CI 1.19--1.64; \cite{munger2006}), added to the existing MR entry.""",
    r"""Observational cohort evidence for vitamin~D and MS risk \cite{munger2006}, added to the existing MR entry; the registered value is listed in Appendix~A.""")

# =============================================================================================
# Introduction and Discussion
# =============================================================================================
rep(r"""\citet{gill2021} showed that MR concordance with RCTs predicts drug approval. \citet{ference2019} demonstrated that MR-derived causal estimates for cardiovascular targets match RCT efficacy. """,
    r"""\citet{gill2021} review how variation in the genes that encode drug targets can be used in MR to anticipate mechanism-based efficacy and adverse effects. """)
rep(r"""\citet{hammerton2021} formalized the requirement that evidence streams must have unrelated sources of bias for triangulation to strengthen causal inference.""",
    r"""\citet{lawlor2016} state the requirement that the approaches compared have different and unrelated key sources of potential bias.""")
rep(r"""This resolved the HRT-cardiovascular discrepancy: the Nurses' Health Study's protective signal was an artifact of prevalent-user bias, reconciled with the WHI trial's harmful result via target trial emulation \cite{hernan2008}.""",
    r"""This resolved the HRT-cardiovascular discrepancy: re-analyzed as an emulation of the WHI trial, the Nurses' Health Study data agreed with the trial's result \cite{hernan2008}, and the comparison of prevalent users is the bias that emulation removes \cite{hernan2016}.""")
rep(r"""MR provides an evidence stream whose biases (pleiotropy, weak instruments, population stratification; \cite{daveysmith2014,gill2024pitfalls}) are largely independent of observational biases (confounding, selection, reverse causation), satisfying the triangulation independence condition \cite{hammerton2021}.""",
    r"""MR provides an evidence stream whose biases (pleiotropy \cite{gill2024pitfalls}, weak instruments \cite{burgess2011weak}, population stratification \cite{brumpton2020withinfamily}) are largely independent of observational biases (confounding, selection, reverse causation), satisfying the triangulation independence condition \cite{lawlor2016}.""")
rep(r"""and \citet{hammerton2021} formalized the independence condition.""", r"""and \citet{lawlor2016} state the independence condition.""")
rep(r"""compares evidence \emph{types} whose biases are independent \cite{daveysmith2014,gill2024pitfalls,munafo2018}.""",
    r"""compares evidence \emph{types} whose biases are independent \cite{gill2024pitfalls,munafo2018}.""")
rep(r"""revealing that the protective signal was an artifact of prevalent-user bias.""",
    r"""which brought the observational estimate in line with the trial; comparing prevalent users is the bias emulation removes \cite{hernan2016}.""")
rep(r"""\citet{gill2024pitfalls} catalog common pitfalls: horizontal pleiotropy (the instrument affects the outcome through pathways other than the target), weak-instrument bias (amplifying confounding when the genetic variant explains little exposure variance), proxy exposure misspecification (the measured protein may not reflect the biologically active form), and population stratification (ancestry-correlated allele frequencies mimicking causal effects).""",
    r"""Common pitfalls include horizontal pleiotropy (the instrument affects the outcome through pathways other than the target) and proxy exposure misspecification (the measured protein may not reflect the biologically active form) \cite{gill2024pitfalls}, weak-instrument bias, which moves estimates toward the confounded observational association \cite{burgess2011weak}, and population stratification (ancestry correlated with both genotype and outcome) \cite{brumpton2020withinfamily}.""")
rep(r"""\citet{daveysmith2014} emphasized that MR estimates reflect lifelong genetically determined exposure levels, creating a fundamental asymmetry with pharmacological interventions that act over months to years.""",
    r"""Genetic variants proxying a drug target represent the cumulative lifelong effect of a small perturbation, whereas a pharmacological intervention in later life typically has a larger effect over a shorter period \cite{gill2022drugmr}.""")

# =============================================================================================
# Appendix A
# =============================================================================================
appendix = rf"""
\section*{{Appendix A. Source Verification of Input Values}}

Each observational estimate, MR estimate and outcome used by the classifier was matched to a quoted passage in its source. The quotations are recorded with the \texttt{{citations}} tool \cite{{tower2026reproducible}} in the repository's \texttt{{claims/}} directory, one file per source with the artifact's SHA-256 hash; \texttt{{citations verify --claims claims --strict}} re-checks every quotation against its artifact. {n_quotes} quotations from {n_files} sources are recorded ({n_pdf} full texts, {n_abs} abstracts, {n_html} web pages).

Of the {N_NUM} numeric input values of the 32 scored families, {N_CHECKED} were checked against a source. {N_AGREE} of the {N_CHECKED} ({PCT}\%) agree with it: {num['quoted']} appear in the source cited, {num['replacement_citation']} appear in a source other than the one previously cited, and {num['derived']} are stated transformations of a source value. The derivations are the Urate-Gout MR estimate (rescaled to 1~SD of serum urate), the Urate-Gout observational estimate (read from a dose-response curve), the Blood-pressure observational estimate ($\sqrt{{2}}$ from a twofold difference per 20~mmHg), the IL-17-psoriasis MR estimate ($\exp(\hat\beta)$ of the reported coefficient), and the five author-estimated observational values marked $^\dagger$ in the tables. {num['coding_error']} values do not match their source (Table~\ref{{tab:coding}}); the two observational values not checked (ModRisk-AD, EBV-MS) have no source named in the catalog. Of the 32 outcomes, 28 match a documented program and regulatory record; the remaining four are the families without a documented Phase~III program. Under the source's own values, no family's expected outcome or score changes; one family's label changes (IGF1-CRC).

\begin{{table}}[htbp]
\centering
\caption{{Input values that do not match their source. Registered values are those of the frozen classifier; the source column gives what the source reports. The classification column applies the registered rule to the source's value.}}
\label{{tab:coding}}
\footnotesize
\begin{{tabular}}{{>{{\raggedright\arraybackslash}}p{{2.2cm}}>{{\raggedright\arraybackslash}}p{{2.4cm}}>{{\raggedright\arraybackslash}}p{{6.3cm}}>{{\raggedright\arraybackslash}}p{{3.3cm}}}}
\toprule
Family, leg & Registered value & Source reports & Classification \\
\midrule
ModRisk-AD, MR & OR 1.10 & no published estimate matches; a 2023 MR of modifiable risk factors reports several estimates of 1.10 for single traits & excluded (no program) \\
EBV-MS, MR & OR 5.0 (2.0--20.0) & no published estimate matches; nearest are observational (infectious mononucleosis, OR 5.5, 1.5--19.7) & excluded (no program) \\
HRT-AD, MR & OR 1.00 (0.85--1.18) & \citet{{barth2025}}: IVW coefficients only; converted, OR 0.96 to 1.54, every interval including 1 & unchanged (null) \\
Anti-CD20-MS, OBS & OR 2.23 & the source reports HR 0.14 (0.05--0.39), the value printed in the tables & unchanged (non-trivial) \\
VitaminD-MS, OBS & OR 1.40 (1.19--1.64) & \citet{{munger2006}}: OR 0.59 (0.36--0.97) per 50~nmol/L; quintile ORs 0.57, 0.57, 0.74, 0.38 & unchanged (non-trivial) \\
LDL/PCSK9, OBS & OR 1.52 & no numeric estimate in the cited text; \citet{{voight2012}} give 1.54 (1.45--1.63) & unchanged (non-trivial) \\
Blood pressure, MR & OR 1.44 (1.35--1.55) & \citet{{georgakis2020}}: any stroke 1.39 (1.33--1.44), ischemic 1.41 (1.35--1.47) & unchanged (supportive) \\
IL-23-psoriasis, OBS & SMD 0.66 & the cited meta-analysis reports no IL-23 estimate; the leg rests on tissue p19 expression & unchanged (non-trivial) \\
CTLA-4-RA, MR & OR 0.86 (0.78--0.95) & \citet{{daha2009ctla4}}: 0.86 (0.78--0.96) & unchanged (null) \\
TNF-$\alpha$-RA, MR & OR 1.00 & no TNF estimate reported; 1.00 stands for a null result & unchanged (null) \\
IL-1$\beta$-CVD, MR & OR 1.00 & no IL-1$\beta$ estimate exists for coronary disease; 1.00 stands for a null result & unchanged (null) \\
IGF1-CRC, OBS & OR 1.12 & \citet{{murphy2020igf}}: 1.12 (1.01--1.24) is the per-SD HR for distal colon cancer; colorectal Q5 vs.\ Q1 HR 1.24 (1.10--1.40) and 1.34 (1.18--1.52) & label changes (genetic-only to concordance); expected success and miss unchanged \\
SGLT2-HF, OBS & RR 1.75 & \citet{{ohkuma2019diabetesHF}}: 1.74 (1.55--1.95) men, 1.95 (1.70--2.22) women & unchanged (non-trivial) \\
Complement-GA, MR & OR 2.50 (2.20--2.85) & \citet{{thakkinstian2006}}: pooled 2.50 (1.96--3.30) & unchanged (association) \\
\bottomrule
\end{{tabular}}
\end{{table}}
"""
rep(r"""\section*{Abbreviations}""", "\\FloatBarrier" + appendix + "\n\\FloatBarrier\n\\section*{Abbreviations}")

# =============================================================================================
# Back matter
# =============================================================================================
rep(r"""was used to draft and edit manuscript text, to write and debug analysis code, and to prepare submission materials.""",
    r"""was used to draft and edit manuscript text, to code input values from published sources, to write and debug analysis code, and to prepare submission materials.""")
rep(r"""are documented in the repository. No novel datasets were generated.""",
    r"""are documented in the repository. The quotation that supports each input value is recorded in \texttt{claims/}, and \texttt{citations verify --claims claims --strict} re-checks them against the source artifacts (Appendix~A). No novel datasets were generated.""")

rep(r"""(41 families with effect sizes, CIs, sources, MR contrast and instrument set; \texttt{cross\_design\_classification\_all\_41\_families\_v3.csv})""",
    r"""(41 families with effect sizes, CIs, sources, MR contrast, instrument set, and the origin and source of each input value; \texttt{cross\_design\_classification\_all\_41\_families\_v4.csv})""")

# =============================================================================================
# Checks
# =============================================================================================
for dead in ["keum2014vitdobscancer", "ong2021vitdcancer", "han2020eosinophilasthma", "busse2019dupilumab", "rinaldi2019igfobs",
             "hammerton2021", "shumaker2003}", "citet{ference2019}", "cite{ference2019}", "15.65", "OR~3.46 per allele", "pooled non-randomized",
             "highest vs.\\ lowest tertile", "0.80 & 1.00 (0.93", "1.25--1.80", "daveysmith2014}", "Lewington 2002 (PSC)", "Sarwar 2007 ("]:
    assert dead not in text, dead
bib = (HERE.parent / "references_v10_r4.bib").read_text(encoding="utf-8")
for key in set(k.strip() for grp in re.findall(r"\\cite[tp]?\{([^}]*)\}", text) for k in grp.split(",")):
    assert re.search(r"@\w+\{" + re.escape(key) + ",", bib), f"cited key missing from bib: {key}"
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split())
assert words <= 350, words
DST.write_text(text, encoding="utf-8")
print(f"{applied} edits applied; abstract {words} words; {n_quotes} quotations from {n_files} sources; wrote {DST.name}")
