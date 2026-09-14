"""Revised primary analysis for Frontiers 1933481: the registered scored set with three post-hoc changes.

Reviewer 1 (9 Sep 2026) asked that the primary analysis (a) exclude IGF1-CRC,
whose MR estimate is for colorectal cancer while the Phase III programmes
were in other cancers; (b) set aside Complement-GA and Serotonin-MDD, whose
genetic leg is a conventional association rather than an MR estimate; (c)
count CRP and IL-1b-CVD once, since they carry identical evidence on every
field; and (d) justify or replace the 50 per cent binomial null.

This script scores the registered set and the reviewer-specified set, and
tests each two ways: the one-sided exact binomial against 50 per cent, and an
outcome-permutation test with the classification held fixed. The permutation
null is the distribution of accuracy when drug outcomes are shuffled across
families and predictions are unchanged. With margins fixed it is
hypergeometric, so the p-value is computed exactly and a Monte Carlo run is
kept beside it as a check.
"""
import csv, io, json, os, random
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = "cross_design_classification_all_41_families_v2.csv"
_candidates = [os.path.join(HERE, CSV),
               os.path.join(HERE, "..", "..", "data", CSV),
               os.path.join(HERE, "..", "..", "paper", "submission", "supplementary", CSV)]
DATA = next((p for p in _candidates if os.path.exists(p)), _candidates[0])
OUT = os.path.join(HERE, "revised_primary_results.json")

EXCLUDE_INDICATION = ("IGF1-CRC",)
EXCLUDE_ASSOCIATION = ("Complement-GA", "Serotonin-MDD")
MERGE = ("CRP", "IL-1b-CVD")          # identical evidence; keep the first row
N_PERM = 100_000
SEED = 20260913


def binom_p(k, n, p=0.5):
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


def is_failure(outcome):
    return outcome in ("Failed", "No benefit")


def accuracy(rows):
    return sum(1 for r in rows if (r["prediction"] == "failure") == is_failure(r["drug_outcome"]))


def hypergeometric_p(rows):
    """P(accuracy >= observed) when outcomes are permuted and predictions fixed.

    Let n families, F actual failures, f predicted failures. A permutation
    assigns the F failure labels uniformly to families; accuracy is
    n - F - f + 2k where k is the number of predicted-failure families that
    receive a failure label, and k is hypergeometric(n, F, f).
    """
    n = len(rows)
    F = sum(1 for r in rows if is_failure(r["drug_outcome"]))
    f = sum(1 for r in rows if r["prediction"] == "failure")
    obs = accuracy(rows)
    total = comb(n, F)
    p = 0.0
    for k in range(max(0, F + f - n), min(F, f) + 1):
        acc = n - F - f + 2 * k
        if acc >= obs:
            p += comb(f, k) * comb(n - f, F - k) / total
    return p


def monte_carlo_p(rows, n_perm=N_PERM, seed=SEED):
    rng = random.Random(seed)
    outcomes = [r["drug_outcome"] for r in rows]
    preds = [r["prediction"] == "failure" for r in rows]
    obs = accuracy(rows)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(outcomes)
        acc = sum(1 for p, o in zip(preds, outcomes) if p == is_failure(o))
        if acc >= obs:
            hits += 1
    return hits / n_perm


def score(rows):
    n, k = len(rows), accuracy(rows)
    approvals = sum(1 for r in rows if not is_failure(r["drug_outcome"]))
    return {
        "n": n, "correct": k, "accuracy": round(k / n, 4),
        "p_one_sided_exact_binomial_50pct": round(binom_p(k, n), 5),
        "p_permutation_exact": round(hypergeometric_p(rows), 5),
        "p_permutation_monte_carlo": round(monte_carlo_p(rows), 5),
        "always_approve_accuracy": round(approvals / n, 4),
        "always_fail_accuracy": round((n - approvals) / n, 4),
    }


rows = list(csv.DictReader(io.open(DATA, encoding="utf-8")))
scored = [r for r in rows if r["correct"] in ("True", "False")]
for r in scored:  # the CSV's own verdict must agree with the recomputed one
    assert (r["correct"] == "True") == ((r["prediction"] == "failure") == is_failure(r["drug_outcome"])), r["family"]

reviewer = [r for r in scored
            if r["family"] not in EXCLUDE_INDICATION + EXCLUDE_ASSOCIATION
            and r["family"] != MERGE[1]]
assert len(reviewer) == len(scored) - 4

results = {
    "registered": score(scored),
    "reviewer_specified": score(reviewer),
    "reviewer_specified_definition": {
        "excluded_indication_mismatch": list(EXCLUDE_INDICATION),
        "excluded_association_only": list(EXCLUDE_ASSOCIATION),
        "merged_identical_evidence": list(MERGE),
    },
    "by_tier": {
        "registered": {t: score([r for r in scored if r["status"] == t])
                       for t in ("pre-registered", "extension")},
        "reviewer_specified": {t: score([r for r in reviewer if r["status"] == t])
                               for t in ("pre-registered", "extension")},
    },
    "misses": {
        "registered": sorted(r["family"] for r in scored if r["correct"] == "False"),
        "reviewer_specified": sorted(r["family"] for r in reviewer if r["correct"] == "False"),
    },
    "n_permutations": N_PERM, "seed": SEED, "data": os.path.basename(DATA),
}
json.dump(results, open(OUT, "w"), indent=2)

for name in ("registered", "reviewer_specified"):
    s = results[name]
    print(f"{name:<20} {s['correct']}/{s['n']} = {s['accuracy']:.3f}  binomial p = {s['p_one_sided_exact_binomial_50pct']}  "
          f"permutation p = {s['p_permutation_exact']} (MC {s['p_permutation_monte_carlo']})  "
          f"always-approve = {s['always_approve_accuracy']:.3f}")
    for t, v in results["by_tier"][name].items():
        print(f"    {t:<16} {v['correct']}/{v['n']}  binomial p = {v['p_one_sided_exact_binomial_50pct']}  permutation p = {v['p_permutation_exact']}")
print("misses (reviewer set):", ", ".join(results["misses"]["reviewer_specified"]))
print("wrote", OUT)


# ---------------------------------------------------------------------------
# Stratification by MR contrast scale (reviewer point 3) and clustering of
# shared instruments (point 6). The contrast per family is the registered
# table in paper/reference/reviewer_analyses.py (MR_CONTRAST_TYPES, commit
# 4b0a652); the instrument sets are INSTRUMENT_MAP in
# analysis/classifier/robustness_analyses.py. Both are copied here so the
# supplement can carry them as columns.
# ---------------------------------------------------------------------------
MR_CONTRAST = {
    "Metabolic-AD": "per_sd", "ModRisk-AD": "per_sd", "Anti-CD20-MS": "per_sd",
    "Smoking-MS/AD": "per_sd", "HRT-AD": "per_sd", "BMI-AD": "per_sd",
    "VitaminD-MS": "per_sd", "EBV-MS": "per_allele",
    "HDL/CETP": "per_sd", "Niacin/HDL": "per_sd", "Homocysteine": "per_genotype",
    "CRP": "per_unit", "LDL/PCSK9": "per_unit", "Blood pressure": "per_unit",
    "Triglycerides": "per_unit",
    "IL-23-psoriasis": "per_allele", "CTLA-4-RA": "per_allele", "TNF-a-RA": "null_signal",
    "IL-17-psoriasis": "null_signal", "JAK-STAT-RA": "per_allele", "CD20-RA": "per_allele",
    "IL-1b-CVD": "null_signal",
    "VitD-Cancer": "per_sd", "IGF1-CRC": "per_sd", "Estrogen-BC": "per_sd",
    "Eos/IL5-Asthma": "per_sd", "SGLT2-HF": "per_sd", "Urate-Gout": "per_sd",
    "IL6-MDD": "per_unit", "Serotonin-MDD": "per_allele", "Complement-GA": "per_allele",
    "Sclerostin-Fracture": "per_sd",
}
INSTRUMENT_SET = {
    "HDL/CETP": "HDL-C GWAS (Voight 2012)", "Niacin/HDL": "HDL-C GWAS (Voight 2012)",
    "CRP": "CRP GWAS", "IL-1b-CVD": "CRP GWAS", "IL6-MDD": "CRP GWAS",
    "VitaminD-MS": "25(OH)D GWAS", "VitD-Cancer": "25(OH)D GWAS",
}


def cluster_of(r):
    return INSTRUMENT_SET.get(r["family"], r["family"])


def cluster_permutation_p(rows, n_perm=N_PERM, seed=SEED):
    """Permute outcome labels across instrument clusters, classification fixed.

    Every cluster in the data has one outcome for all its members, so a
    cluster carries one label; accuracy is still counted per family.
    """
    clusters = {}
    for r in rows:
        clusters.setdefault(cluster_of(r), []).append(r)
    labels = []
    for members in clusters.values():
        outs = {is_failure(m["drug_outcome"]) for m in members}
        assert len(outs) == 1, f"mixed outcomes in cluster {cluster_of(members[0])}"
        labels.append(outs.pop())
    preds = [[m["prediction"] == "failure" for m in members] for members in clusters.values()]
    obs = accuracy(rows)
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(labels)
        acc = sum(p == lab for lab, ps in zip(labels, preds) for p in ps)
        if acc >= obs:
            hits += 1
    return hits / n_perm, len(clusters)


for name, subset in (("registered", scored), ("reviewer_specified", reviewer)):
    p, n_clusters = cluster_permutation_p(subset)
    results[name]["p_permutation_cluster_level"] = round(p, 5)
    results[name]["n_instrument_clusters"] = n_clusters
    results[name]["by_mr_contrast"] = {
        c: {"n": len(g), "correct": accuracy(g),
            "families": [r["family"] for r in g]}
        for c in ("per_sd", "per_allele", "per_unit", "per_genotype", "null_signal")
        if (g := [r for r in subset if MR_CONTRAST[r["family"]] == c])
    }

# Supplement v3: the released CSV plus the two columns the analyses above need.
CSV_OUT = os.path.join(HERE, "cross_design_classification_all_41_families_v3.csv")
with io.open(CSV_OUT, "w", encoding="utf-8", newline="") as fh:
    fields = list(rows[0].keys()) + ["mr_contrast", "instrument_set", "revised_primary_set"]
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    in_reviewer = {r["family"] for r in reviewer}
    for r in rows:
        w.writerow({**r,
                    "mr_contrast": MR_CONTRAST.get(r["family"], ""),
                    "instrument_set": INSTRUMENT_SET.get(r["family"], ""),
                    "revised_primary_set": "True" if r["family"] in in_reviewer else ""})
results["supplement_v3"] = os.path.basename(CSV_OUT)
json.dump(results, open(OUT, "w"), indent=2)

for name in ("registered", "reviewer_specified"):
    s = results[name]
    print(f"\n{name}: cluster-level permutation p = {s['p_permutation_cluster_level']} over {s['n_instrument_clusters']} clusters")
    for c, v in s["by_mr_contrast"].items():
        print(f"    {c:<13} {v['correct']}/{v['n']}")
print("wrote", CSV_OUT)
