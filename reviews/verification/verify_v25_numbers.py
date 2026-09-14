"""Check every number the round-3 revision introduces against the analysis output.

Run:  uv run --no-project python reviews/verification/verify_v25_numbers.py

Reads analysis/revised_primary_analysis/revised_primary_results.json (written by
run_revised_primary.py) and asserts that each figure printed in
paper/paper_v25_round3.tex appears there, at the precision printed.
"""
import json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEX = (REPO / "paper" / "paper_v25_round3.tex").read_text()
R = json.loads((REPO / "analysis" / "revised_primary_analysis" / "revised_primary_results.json").read_text())

checks = []
def expect(label, cond, detail=""):
    checks.append((label, bool(cond), detail))

reg, rev = R["registered"], R["reviewer_specified"]
expect("registered 24/32", reg["correct"] == 24 and reg["n"] == 32)
expect("revised 23/28", rev["correct"] == 23 and rev["n"] == 28)
expect("revised accuracy 82.1%", round(rev["accuracy"] * 100, 1) == 82.1)
expect("registered accuracy 75.0%", round(reg["accuracy"] * 100, 1) == 75.0)
expect("registered permutation p = 0.005", round(reg["p_permutation_exact"], 3) == 0.005)
expect("revised permutation p = 0.0006", round(rev["p_permutation_exact"], 4) == 0.0006)
expect("revised binomial p < 0.001", rev["p_one_sided_exact_binomial_50pct"] < 0.001)
expect("registered binomial p = 0.004", round(reg["p_one_sided_exact_binomial_50pct"], 3) == 0.004)
expect("registered cluster p = 0.005 over 28", round(reg["p_permutation_cluster_level"], 3) == 0.005 and reg["n_instrument_clusters"] == 28)
expect("revised cluster p = 0.0002 over 25", round(rev["p_permutation_cluster_level"], 4) == 0.0002 and rev["n_instrument_clusters"] == 25)
expect("always-approve 17/32", round(reg["always_approve_accuracy"] * 32) == 17)
expect("always-approve 16/28", round(rev["always_approve_accuracy"] * 28) == 16)
tiers = R["by_tier"]
expect("registered tiers 18/22, 6/10", tiers["registered"]["pre-registered"]["correct"] == 18 and tiers["registered"]["extension"]["correct"] == 6 and tiers["registered"]["extension"]["n"] == 10)
expect("extension permutation p = 0.55", round(tiers["registered"]["extension"]["p_permutation_exact"], 2) == 0.55)
expect("extension binomial p = 0.38", round(tiers["registered"]["extension"]["p_one_sided_exact_binomial_50pct"], 2) == 0.38)
expect("revised tiers 17/21, 6/7", tiers["reviewer_specified"]["pre-registered"]["correct"] == 17 and tiers["reviewer_specified"]["pre-registered"]["n"] == 21 and tiers["reviewer_specified"]["extension"]["correct"] == 6 and tiers["reviewer_specified"]["extension"]["n"] == 7)
expect("revised extension permutation p = 0.14", round(tiers["reviewer_specified"]["extension"]["p_permutation_exact"], 2) == 0.14)
strata = {k: (v["correct"], v["n"]) for k, v in reg["by_mr_contrast"].items()}
expect("registered strata 13/16, 4/7, 5/5, 1/1, 1/3", strata == {"per_sd": (13, 16), "per_allele": (4, 7), "per_unit": (5, 5), "per_genotype": (1, 1), "null_signal": (1, 3)}, str(strata))
strata_r = {k: (v["correct"], v["n"]) for k, v in rev["by_mr_contrast"].items()}
expect("revised strata 13/15, 4/5, 5/5, 1/1, 0/2", strata_r == {"per_sd": (13, 15), "per_allele": (4, 5), "per_unit": (5, 5), "per_genotype": (1, 1), "null_signal": (0, 2)}, str(strata_r))
expect("misses under revised set are five", len(R["misses"]["reviewer_specified"]) == 5)

# The strings the manuscript prints.
for s in ["23/28 (82.1\\%", "24/32 (75.0\\%", "$p = 0.0006$", "$p = 0.005$", "17/21", "6/7",
          "13/16 per-SD, 4/7 per-allele, 5/5 per-unit, 1/1 per-genotype and 1/3",
          "13/15, 4/5, 5/5, 1/1 and 0/2", "$p = 0.005$ over 28 clusters", "$p = 0.0002$ over 25 clusters",
          "17/32 under the registered set and 16/28", "16 use per-SD MR effects",
          "\\label{tab:criteria}", "\\label{sec:revised_primary}", "\\label{sec:stats}",
          "fig1_flowchart_v6.pdf", "fig2_failure_modes_v2.pdf", "frontiers-revision-3",
          "cross\\_design\\_classification\\_all\\_41\\_families\\_v3.csv",
          "cluster-level $p = 0.0002$", "reported apart from MR-instrumented", "is reported as a robustness analysis", "6/7 in the blind extension", "Assoc. & Failed & Conc."]:
    expect(f"manuscript prints {s!r}", s in TEX)
expect("cluster-level p in abstract and body", TEX.count("cluster-level $p = 0.0002$") >= 2)
expect("no 'in order' criteria claim", "criteria in order" not in TEX and "read in this order" not in TEX)
expect("no review-process narration", not re.search(r"(?i)peer review|reviewer|during review|requested during", TEX))
expect("no 'zombie' in manuscript", not re.search(r"(?i)zombie", TEX))
expect("no 'Pre-Registered' in title", "Pre-Registered Evaluation" not in TEX)
words = len(re.sub(r"\\textbf\{[^}]*\}|\\[a-z]+|[${}\\]", " ",
                   re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", TEX, re.S).group(1)).split())
expect(f"abstract <= 350 words ({words})", words <= 350)

failed = [c for c in checks if not c[1]]
for label, ok, detail in checks:
    print(("PASS " if ok else "FAIL ") + label + (f"  {detail}" if detail and not ok else ""))
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
