"""Exclusion sensitivity analyses for Frontiers 1933481.

Reviewer 1 asked for two exclusions to be tested:
  IGF1-CRC, on indication mismatch (MR is colorectal cancer risk; the
        Phase III programmes were NSCLC, Ewing sarcoma and pancreatic cancer).
  Complement-GA and Serotonin-MDD, whose genetic leg is a conventional
        association rather than a Mendelian randomization estimate.

The registered analysis is primary. Each exclusion is reported beside it.
Test throughout: one-sided exact binomial against 50 per cent chance accuracy,
the same test the registered analysis uses.
"""
import csv, json, io, os
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = "cross_design_classification_all_41_families_v2.csv"
# Beside this script (as distributed in the supplement), else in the repository.
_candidates = [os.path.join(HERE, CSV),
               os.path.join(HERE, "..", "..", "data", CSV),
               os.path.join(HERE, "..", "..", "paper", "submission", "supplementary", CSV)]
DATA = next((p for p in _candidates if os.path.exists(p)), _candidates[0])
OUT = os.path.join(HERE, "sensitivity_results.json")


def binom_p(k, n, p=0.5):
    """One-sided exact binomial, P(X >= k)."""
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


def score(rows):
    correct = sum(1 for r in rows if r["correct"] == "True")
    n = len(rows)
    return {"n": n, "correct": correct,
            "accuracy": round(correct / n, 4),
            "p_one_sided_exact_binomial": round(binom_p(correct, n), 5)}


rows = list(csv.DictReader(io.open(DATA, encoding="utf-8")))
scored = [r for r in rows if r["correct"] in ("True", "False")]

results = {
    "registered": score(scored),
    "excluding_IGF1-CRC": score([r for r in scored if r["family"] != "IGF1-CRC"]),
    "excluding_non_MR_genetic": score(
        [r for r in scored if r["family"] not in ("Complement-GA", "Serotonin-MDD")]),
    "excluding_both": score(
        [r for r in scored if r["family"] not in
         ("IGF1-CRC", "Complement-GA", "Serotonin-MDD")]),
    "misses_registered": sorted(r["family"] for r in scored if r["correct"] == "False"),
}
results["by_instrument_type"] = {
    t: score([r for r in scored if r["instrument_type"] == t])
    for t in sorted({r["instrument_type"] for r in scored})
}

json.dump(results, open(OUT, "w"), indent=2)

print("registered              %(correct)2d/%(n)2d = %(accuracy).3f  p = %(p_one_sided_exact_binomial)s" % results["registered"])
for k in ("excluding_IGF1-CRC", "excluding_non_MR_genetic", "excluding_both"):
    print("%-23s %(correct)2d/%(n)2d = %(accuracy).3f  p = %(p_one_sided_exact_binomial)s" % (k, ) if False else
          "%-23s %2d/%2d = %.3f  p = %s" % (k, results[k]["correct"], results[k]["n"],
                                            results[k]["accuracy"],
                                            results[k]["p_one_sided_exact_binomial"]))
print("\nby instrument type")
for t, v in results["by_instrument_type"].items():
    print("  %-16s %2d/%2d" % (t, v["correct"], v["n"]))
print("\nmisses:", ", ".join(results["misses_registered"]))
print("\nwrote", OUT)
