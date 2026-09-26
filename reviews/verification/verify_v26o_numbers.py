"""Check every Amendment 5 number printed in paper_v26o_round4.tex against the files that produced it.

Run:  uv run --no-project python reviews/verification/verify_v26b_numbers.py
Exit status is non-zero if any check fails. Also re-checks the v25 invariants that must survive
(no "zombie", no review narration, registered 24/32 primary, abstract <= 350 words).
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX = (ROOT / "paper" / "paper_v26o_round4.tex").read_text(encoding="utf-8")
A5 = ROOT / "analysis" / "amendment5"
screen = json.loads((A5 / "screen" / "screen_results.json").read_text())
states = json.loads((A5 / "mr_states" / "mr_states_results.json").read_text())
sets = {t["set"]: t for t in json.loads((A5 / "analysis_sets" / "analysis_sets.json").read_text())["table"]}
il6 = json.loads((A5 / "il6_mdd" / "selected_estimate.json").read_text())
prior = json.loads((ROOT / "analysis" / "revised_primary_analysis" / "revised_primary_results.json").read_text())
sample = list(csv.DictReader(open(A5 / "screen" / "mr_availability_sample_filled.csv", encoding="utf-8")))
codebook = {r["family"]: r for r in csv.DictReader(open(A5 / "codebook" / "outcome_codebook_all_41_families.csv", encoding="utf-8"))}
audit = {r["family"]: r["verdict"] for r in csv.DictReader(open(A5 / "mr_instrumented_audit.csv", encoding="utf-8"))}
fam = {r["family"]: r for r in csv.DictReader(open(ROOT / "data" / "cross_design_classification_all_41_families_v3.csv", encoding="utf-8"))}

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


def has(s):
    return s in TEX


# --- screen
check("universe 279 / 219 (189, 30)", screen["universe_n"] == 279 and screen["resolved_universe_n"] == 219
      and screen["resolved_outcome_split"] == {"TRUE": 189, "FALSE": 30} and has("279 genetically supported") and has("219 with a recorded"))
check("exact 0, expanded 14 (6.4%)", screen["exact_coverage"]["resolved_rows_covered"] == 0 and screen["expanded_coverage"]["resolved_rows_covered"] == 14
      and has("Exact coverage of the 219 resolved pairs is 0; expanded coverage is 14 (6.4\\%)"))
check("match statuses 1/8/5/18", screen["families_by_match_status"] == {"exact": 1, "broader indication": 8, "polygenic": 5, "no record": 18}
      and has("eight reach their gene under other indications") and has("18 have no record"))
n_elig = sum(r["mr_eligible"].strip().lower() == "yes" for r in sample)
n_zero = sum(r["n_results_read"].strip() in ("0", "") for r in sample)
check("sample 4/25 eligible, 13 zero-result", n_elig == 4 and len(sample) == 25 and n_zero == 13 and has("4 (16\\%) have a published MR estimate") and has("13 return no PubMed result"))
# --- MR states
st = states["scored_32_by_state"]
check("states 15/12, 7/6, 10/6", (st["supportive"]["n"], st["supportive"]["correct"]) == (15, 12) and (st["negligible_range"]["n"], st["negligible_range"]["correct"]) == (7, 6)
      and (st["inconclusive"]["n"], st["inconclusive"]["correct"]) == (10, 6) and has("15 are MR-supportive (12 correct), 7 have their whole interval within the negligible range (6 correct") and has("10 are inconclusive (6 correct)"))
check("null split 7/10", states["registered_null_families_split"] == {"negligible_range": 7, "inconclusive": 10} and has("divide 7 negligible-range to 10 inconclusive"))
check("negligible-range families named", set(st["negligible_range"]["families"]) == {"HRT-AD", "BMI-AD", "Homocysteine", "CRP", "VitD-Cancer", "Estrogen-BC", "IL6-MDD"})
check("scale-unresolved 8 of 41", len(states["scale_unresolved_families"]) == 8 and has("scale-unresolved (8 of 41 families are)"))
check("no CI families 6 scored", set(states["no_ci_families"]) & set(f for f in fam if fam[f]["correct"] in ("True", "False")) == {"Metabolic-AD", "ModRisk-AD", "Smoking-MS/AD", "TNF-a-RA", "IL-17-psoriasis", "IL-1b-CVD"} and has("six scored families with no confidence interval"))
check("urate cites Jordan 2019", len(re.findall(r"\\cite[tp]?\{jordan2019urate\}", TEX)) == 2 and r"\cite{li2019uratemr}" not in TEX)
flags = states["scored_32_by_alignment_flag"]
check("alignment flags 4 scored, 2 misses", flags["indication mismatch"]["n"] + flags["instrument-target mismatch"]["n"] == 4
      and (flags["indication mismatch"]["n"] - flags["indication mismatch"]["correct"]) + (flags["instrument-target mismatch"]["n"] - flags["instrument-target mismatch"]["correct"]) == 2)
# --- analysis sets, every printed row
expected = {"registered": (32, 24), "strict Phase III": (25, 17), "Amyloid-AD scored": (33, 24), "strict Phase III + Amyloid-AD": (26, 17),
            "MR-instrumented": (27, 22), "MR-instrumented (unresolved also removed)": (26, 21), "documented Phase III program": (28, 20), "registration-consistent instrument": (32, 24),
            "unique-evidence": (31, 23), "source-extracted OBS": (25, 20), "source-extracted OBS (classifier flags)": (27, 21), "Amendment 4": (28, 23)}
for name, (n, k) in expected.items():
    check(f"set {name} = {k}/{n}", (sets[name]["n"], sets[name]["correct"]) == (n, k))
tab = TEX[TEX.index(r"\label{tab:sets}"):TEX.index(r"\end{table}", TEX.index(r"\label{tab:sets}"))]
for n, k, pct in [(32, 24, "75.0"), (25, 17, "68.0"), (33, 24, "72.7"), (26, 17, "65.4"), (27, 22, "81.5"), (26, 21, "80.8"), (31, 23, "74.2"), (28, 20, "71.4"), (25, 20, "80.0"), (27, 21, "77.8"), (28, 23, "82.1")]:
    check(f"table row {k}/{n} {pct}%", f"& {n} & {k} & {pct}\\%" in tab and abs(round(100 * k / n, 1) - float(pct)) < 0.05)
check("strict Phase III removes the seven named", set(sets["strict Phase III"]["removed"].split("; ")) == {"IL6-MDD", "Blood pressure", "Triglycerides", "ModRisk-AD", "Smoking-MS/AD", "BMI-AD", "EBV-MS"})
check("association-leg families five", sorted(f for f, v in audit.items() if v == "association") == ["CTLA-4-RA", "Complement-GA", "IL-23-psoriasis", "JAK-STAT-RA", "Serotonin-MDD"] and has("Five scored families carry a GEN leg"))
check("unresolved one (EBV-MS)", sorted(f for f, v in audit.items() if v == "unresolved") == ["EBV-MS"])
check("p-values from prior file", str(prior["registered"]["p_permutation_exact"])[:5] == "0.005" and prior["reviewer_specified"]["p_permutation_exact"] == 0.0006 and has("permutation $p = 0.005$, cluster-level $p = 0.005$, binomial $p = 0.004$") and has("permutation $p = 0.0006$, cluster-level $p = 0.0002$"))
check("range 17/26 to 23/28 stated", has("runs from 17/26 (65.4\\%) to 23/28 (82.1\\%)") and has("the count runs from 17/26 to 23/28") and min(t["correct"]/t["n"] for t in sets.values()) == 17/26)
# --- IL6-MDD
check("Kelly 2021 OR 1.023 (1.006-1.039)", il6["pmid"] == "33631287" and abs(float(il6["or"]) - 1.023) < 1e-9 and has("OR 1.023 (95\\% CI 1.006--1.039) \\cite{kelly2021il6r}"))
check("Galan cited, Elliott only for CRP-CHD", TEX.count(r"\cite{galan2022crpdepression}") >= 2 and TEX.count(r"\cite{elliott2009}") == 1)
# --- codebook facts
check("CRP and IL-1b-CVD met, not approved", all(codebook[f]["efficacy_endpoint"] == "met" and codebook[f]["regulatory_outcome"] == "not approved" for f in ("CRP", "IL-1b-CVD")) and has("Two families have a met primary endpoint and no approval"))
check("four program-less families", all(codebook[f]["trial_phase"] == "not reported" for f in ("ModRisk-AD", "Smoking-MS/AD", "BMI-AD", "EBV-MS")))
check("IL6-MDD Phase II", codebook["IL6-MDD"]["trial_phase"] == "II")
misses = [f for f, r in fam.items() if r["correct"] == "False"]
check("MR-null misses engaged+met; MR-supportive misses no engagement",
      all(codebook[f]["target_engagement"] == "yes" and codebook[f]["efficacy_endpoint"] == "met" for f in misses if fam[f]["mr_class"] == "null")
      and all(codebook[f]["target_engagement"] == "not reported" for f in misses if fam[f]["mr_class"] == "causal"))
# --- instrument type recount
sc = [r for r in fam.values() if r["correct"] in ("True", "False")]
def itype(r): return "biomarker_gwas" if r["family"] == "IL6-MDD" else r["instrument_type"]
cnt = {}
for r in sc:
    t = itype(r); cnt.setdefault(t, [0, 0]); cnt[t][0] += 1; cnt[t][1] += r["correct"] == "True"
check("instrument types 7/7 5/5 5/8 7/12", cnt["cis_pqtl"] == [7, 7] and cnt["polygenic"] == [5, 5] and cnt["coding_variant"] == [8, 5] and cnt["biomarker_gwas"] == [12, 7]
      and has("(7/7 correct) and polygenic scores (5/5)") and has("biomarker GWAS (7/12, 58.3\\%)"))
# --- author-estimated
check("author-estimated 8 / 5 scored", has("Eight families across the autoimmune") and has("leaving five in the scored set") and has("21 of 27 families"))
check("no dagger on IL6-MDD / Serotonin-MDD rows", "IL6-MDD$^\\text{i}$ & Psych & 0.15 &" in TEX and "Serotonin-MDD$^\\text{j}$ & Psych & 0.45 &" in TEX)
# --- carried-over invariants
check("registered 24/32 primary in abstract", "Under the registered analysis, 24/32 families were classified correctly" in TEX)
for bad in ["zombie", "revised primary", "requested during", "peer review", "the reviewer", "this revision"]:
    check(f"no '{bad}'", bad.lower() not in TEX.lower())
check("no 'Pre-Registered' (title case)", "Pre-Registered" not in TEX)
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", TEX, re.S).group(1)
check("abstract <= 350 words", len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ", abstract).split()) <= 350)
check("bib is v10", r"\bibliography{references_v10_r4}" in TEX)

# --- v26c: source verification
import yaml, glob
vo = json.loads((ROOT / "analysis/provenance/value_origin_summary.json").read_text())
check("appendix agreement 43 of 62 (69%)", vo["numeric_agree"] == 43 and vo["numeric_checked"] == 62 and has("43 of the 62 (69\\%) agree with it"))
check("appendix counts 34/5/4/5/14", vo["numeric"] == {"quoted": 34, "replacement_citation": 5, "derived": 4, "author_estimated": 5, "coding_error": 14, "not_checked": 2} and has("34 appear in the source cited, 5 appear in a source other than the one the catalog recorded, and 4 are stated transformations") and has("A further 5 are author estimates") and has("14 values do not match"))
qf = [yaml.safe_load(open(f)) for f in glob.glob(str(ROOT / "claims/*.yaml"))]
nq = sum(sum(len(c.get("quotes", [])) for c in (d.get("claims") or {}).values()) for d in qf)
ns = sum(1 for d in qf if any(c.get("quotes") for c in (d.get("claims") or {}).values()))
check(f"appendix quotation count {nq} from {ns} sources", has(f"{nq} quotations from {ns} sources"))
check("20/28 sentence", has("Excluding them, the rule classifies 20/28 correctly (71.4\\%)"))
check("VitD-Cancer printed = frozen", "VitD-Cancer$^\\text{a}$ & Onco & 0.78 & 0.97 (0.88--1.07) & 0.017" in TEX)
check("Eos printed = frozen", "1.50 (1.23--1.83) & 0.224" in TEX)
tab = TEX[TEX.index(r"\label{tab:coding}"):TEX.index(r"\end{table}", TEX.index(r"\label{tab:coding}"))]
check("coding-error table has 14 rows", tab.count("\\\\") - 1 == 14)
import subprocess
v = subprocess.run(["citations", "verify", "--claims", "claims", "--strict"], cwd=ROOT, capture_output=True, text=True)
check("citations verify --strict passes", v.returncode == 0 and "all found" in v.stdout)
for bad in ["keum2014vitdobscancer", "ong2021vitdcancer", "han2020eosinophilasthma", "busse2019dupilumab", "rinaldi2019igfobs", "hammerton2021", "15.65", "pooled non-randomized"]:
    check(f"stale citation or value gone: {bad}", bad not in TEX)

check("double-bar markers >= 16 and note present", TEX.count(r"$^\|$") >= 16 and "Value differs from what its source reports" in TEX)
check("documented-program row marked post hoc", "Documented Phase~III program$^\\ast$" in TEX and "Set defined after the registered sets were scored" in TEX)
strict = sets["strict Phase III"]
kept = [f for f in ("Blood pressure", "Triglycerides") if codebook[f]["trial_phase"] == "mixed class" and fam[f]["correct"] == "True"]
check("strict Phase III with BP and TG kept: 19/27 (70.4%)", strict["n"] + len(kept) == 27 and strict["correct"] + len(kept) == 19
      and len(kept) == 2 and has("keeping them gives 19/27 (70.4\\%)"))
check("abstract names no boundary class", not re.search(r"effector-neutralization|mechanism-bypass|small-effect", TEX.split("\\end{abstract}")[0]))
failed = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(("PASS " if ok else "FAIL ") + n)
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
raise SystemExit(1 if failed else 0)
