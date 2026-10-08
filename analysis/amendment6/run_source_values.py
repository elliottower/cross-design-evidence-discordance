"""Amendment 6: the registered rule under source-reported values, and the published-MR-estimate set.

Registered at commit 3aacce6 (PREREGISTRATION_AMENDMENT_6_SOURCE_REPORTED_VALUES.md).

Procedure 1 re-applies the frozen classifier (analysis/classifier/classify_families.py, imported
and called unchanged) to the 32 scored families, replacing each mismatched input that has a
published figure with the figure the amendment's table fixes, and again under every other
candidate figure that table lists. Procedure 2 scores the 28 families whose MR input is a
published estimate, with the registered outcome-permutation test at family and instrument-cluster
level, and the same set without IL-23-psoriasis as one descriptive count with no test.

The run first reproduces the registered result (24/32 and both registered p-values) from the
unmodified classifier, and stops if it does not.

Outputs: analysis/amendment6/source_values_results.json, source_values_by_family.csv
Run:  uv run --no-project python analysis/amendment6/run_source_values.py
"""
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
import random
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLASSIFIER = os.path.join(ROOT, "analysis", "classifier", "classify_families.py")
FAMILIES_CSV = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v4.csv")
PRIOR = os.path.join(ROOT, "analysis", "revised_primary_analysis", "revised_primary_results.json")
# The classifier as committed at c047d39 (2 Sep 2026), unchanged since.
CLASSIFIER_SHA256 = "4b9a9caa516e358769f409d4051ba0235df4366745ab2bef70460aad2be13118"
N_PERM = 100_000
SEED = 20260913
EXPECTED = {"procedure_1": "24/32, 31 with non-trivial observational support", "procedure_2": "21/28", "without_il23_psoriasis": "20/27"}
INSTRUMENT_SET = {
    "HDL/CETP": "HDL-C GWAS (Voight 2012)", "Niacin/HDL": "HDL-C GWAS (Voight 2012)",
    "CRP": "CRP GWAS", "IL-1b-CVD": "CRP GWAS", "IL6-MDD": "CRP GWAS",
    "VitaminD-MS": "25(OH)D GWAS", "VitD-Cancer": "25(OH)D GWAS",
}
NO_PUBLISHED_MR = ("ModRisk-AD", "EBV-MS", "TNF-a-RA", "IL-1b-CVD")
NO_PUBLISHED_OBS = ("IL-23-psoriasis",)


class RegisteredResultNotReproduced(Exception):
    """The unmodified classifier does not return the registered result, so nothing else is run."""


class ClassifierChanged(Exception):
    """The classifier on disk is not the frozen file."""


class UnknownFamily(Exception):
    """A family named in this script is not one of the scored families."""


class NotBinary(Exception):
    """A test was asked to score an expected outcome that is neither success nor failure."""


def ci(beta, se):
    return round(math.exp(beta - 1.959964 * se), 2), round(math.exp(beta + 1.959964 * se), 2)


def pooled(*estimates):
    """Fixed-effect inverse-variance pool of (ratio, lower, upper) on the log scale."""
    terms = [(math.log(r), (math.log(hi) - math.log(lo)) / (2 * 1.959964)) for r, lo, hi in estimates]
    weight = sum(1 / s**2 for _, s in terms)
    beta = sum(b / s**2 for b, s in terms) / weight
    return round(math.exp(beta), 2)


# The amendment's table "Values fixed here". Each entry replaces fields of the frozen family record.
SOURCE_VALUES = {
    "HRT-AD": {"gen_OR": round(math.exp(0.43), 2), "gen_CI_lower": 0.98, "gen_CI_upper": 2.41},
    "Anti-CD20-MS": {"obs_OR": 0.14},
    "VitaminD-MS": {"obs_OR": 0.59},
    "LDL/PCSK9": {"obs_OR": 1.54},
    "Blood pressure": {"gen_OR": 1.39, "gen_CI_lower": 1.33, "gen_CI_upper": 1.44},
    "CTLA-4-RA": {"gen_OR": 0.86, "gen_CI_lower": 0.78, "gen_CI_upper": 0.96},
    "IGF1-CRC": {"obs_OR": 1.11},
    "SGLT2-HF": {"obs_OR": pooled((1.95, 1.70, 2.22), (1.74, 1.55, 1.95))},
    "Complement-GA": {"gen_OR": 2.50, "gen_CI_lower": 1.96, "gen_CI_upper": 3.30},
}
# How each figure of the amendment's table is read; carried to the appendix table.
CONVERSION = {
    "HRT-AD": "coefficient read as a log odds ratio",
    "Anti-CD20-MS": "hazard ratio treated as an odds ratio, magnitude of ln",
    "VitaminD-MS": "odds ratio, magnitude of ln",
    "LDL/PCSK9": "odds ratio per standard deviation",
    "Blood pressure": "odds ratio per 10 mmHg systolic",
    "CTLA-4-RA": "odds ratio",
    "IGF1-CRC": "hazard ratio treated as an odds ratio, per standard deviation",
    "SGLT2-HF": "fixed-effect inverse-variance pool of two risk ratios on the log scale, treated as an odds ratio",
    "Complement-GA": "pooled odds ratio",
}
# The other candidate figures the amendment lists, per family; used for the bound only.
CANDIDATES = {
    "HRT-AD": [
        {"label": "stratum b -0.04 (se 0.13)", "gen_OR": round(math.exp(-0.04), 2), "gen_CI_lower": ci(-0.04, 0.13)[0], "gen_CI_upper": ci(-0.04, 0.13)[1]},
        {"label": "stratum b 0.16 (se 0.25)", "gen_OR": round(math.exp(0.16), 2), "gen_CI_lower": ci(0.16, 0.25)[0], "gen_CI_upper": ci(0.16, 0.25)[1]},
        {"label": "stratum b 0.06 (se 0.11)", "gen_OR": round(math.exp(0.06), 2), "gen_CI_lower": ci(0.06, 0.11)[0], "gen_CI_upper": ci(0.06, 0.11)[1]},
    ],
    "Blood pressure": [{"label": "ischemic stroke", "gen_OR": 1.41, "gen_CI_lower": 1.35, "gen_CI_upper": 1.47}],
    "IGF1-CRC": [
        {"label": "colorectal per SD, Model 1", "obs_OR": 1.07},
        {"label": "colorectal highest vs lowest fifth, Model 1", "obs_OR": 1.24},
        {"label": "colorectal highest vs lowest fifth, Model 2", "obs_OR": 1.34},
    ],
    "SGLT2-HF": [{"label": "women", "obs_OR": 1.95}, {"label": "men", "obs_OR": 1.74}],
}


def load_classifier():
    with open(CLASSIFIER, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != CLASSIFIER_SHA256:
        raise ClassifierChanged(f"{CLASSIFIER}: sha256 {digest}")
    spec = importlib.util.spec_from_file_location("classify_families", CLASSIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_failure(outcome):
    return outcome in ("Failed", "No benefit")


def correct(row):
    """Scored as the frozen classifier scores it: an ambiguous expected outcome is never correct."""
    if is_failure(row["drug_outcome"]):
        return row["prediction"] == "failure"
    return row["prediction"] == "success"


def binary(rows):
    """The permutation tests treat every expected outcome as success or failure; refuse anything else."""
    other = [r["family"] for r in rows if r["prediction"] not in ("success", "failure")]
    if other:
        raise NotBinary(f"expected outcome is neither success nor failure for {other}")
    return rows


def mr_only_identical(rows):
    """Whether an MR-only rule gives every family the expected outcome the two-evidence rule gives.

    The two rules differ only where the two-evidence rule returns `ambiguous` (trivial observational
    evidence with null MR), which an MR-only rule calls a failure. Such a row makes this False.
    """
    return all(r["prediction"] in ("success", "failure")
               and (r["mr_class"] == "causal") == (r["prediction"] == "success") for r in rows)


def accuracy(rows):
    return sum(correct(r) for r in rows)


def hypergeometric_p(rows):
    """P(accuracy >= observed) when outcomes are permuted and classifications held fixed (one-sided, upper tail)."""
    n = len(binary(rows))
    failures = sum(is_failure(r["drug_outcome"]) for r in rows)
    predicted = sum(r["prediction"] == "failure" for r in rows)
    observed = accuracy(rows)
    total = comb(n, failures)
    p = 0.0
    for k in range(max(0, failures + predicted - n), min(failures, predicted) + 1):
        if n - failures - predicted + 2 * k >= observed:
            p += comb(predicted, k) * comb(n - predicted, failures - k) / total
    return p


def cluster_permutation_p(rows):
    """The registered cluster-level test: outcome labels permuted across instrument clusters."""
    clusters = {}
    for r in binary(rows):
        clusters.setdefault(INSTRUMENT_SET.get(r["family"], r["family"]), []).append(r)
    labels = []
    for name, members in clusters.items():
        outcomes = {is_failure(m["drug_outcome"]) for m in members}
        assert len(outcomes) == 1, f"mixed outcomes in cluster {name}"
        labels.append(outcomes.pop())
    predictions = [[m["prediction"] == "failure" for m in members] for members in clusters.values()]
    observed = accuracy(rows)
    rng = random.Random(SEED)
    hits = 0
    for _ in range(N_PERM):
        rng.shuffle(labels)
        if sum(p == label for label, ps in zip(labels, predictions) for p in ps) >= observed:
            hits += 1
    return hits / N_PERM, len(clusters)


def summarize(rows):
    k = accuracy(rows)
    return {"n": len(rows), "correct": k, "accuracy": round(k / len(rows), 4),
            "obs_non_trivial": sum(r["obs_class"] == "non-trivial" for r in rows),
            "misses": sorted(r["family"] for r in rows if not correct(r))}


def main():
    classifier = load_classifier()
    frozen = classifier.NEURO_FAMILIES + classifier.CARDIO_FAMILIES + classifier.AUTOIMMUNE_FAMILIES + classifier.EXTENSION_FAMILIES
    with open(FAMILIES_CSV, encoding="utf-8") as fh:
        released = {r["family"]: r for r in csv.DictReader(fh)}
    scored_names = [name for name, r in released.items() if r["correct"] in ("True", "False")]
    unknown = [name for name in (*SOURCE_VALUES, *CANDIDATES, *CONVERSION, *NO_PUBLISHED_MR, *NO_PUBLISHED_OBS) if name not in scored_names]
    if unknown:
        raise UnknownFamily(f"not scored families: {sorted(set(unknown))}")

    def classify(families):
        by_name = {r["family"]: r for r in classifier.run_classification(families)}
        return [by_name[name] for name in scored_names]

    # Wiring check: the unmodified classifier must return the registered result before anything else is trusted.
    registered = classify(copy.deepcopy(frozen))
    prior = json.load(open(PRIOR, encoding="utf-8"))["registered"]
    mismatched = [
        r["family"] for r in registered
        if r["prediction"] != released[r["family"]]["prediction"]
        or r["obs_class"] != released[r["family"]]["obs_class"]
        or r["mr_class"] != released[r["family"]]["mr_class"]
        or str(correct(r)) != released[r["family"]]["correct"]
    ]
    p_family = round(hypergeometric_p(registered), 5)
    p_cluster, n_clusters = cluster_permutation_p(registered)
    if (len(registered), accuracy(registered)) != (32, 24) or mismatched or p_family != prior["p_permutation_exact"] \
            or round(p_cluster, 5) != prior["p_permutation_cluster_level"]:
        raise RegisteredResultNotReproduced(
            f"{accuracy(registered)}/{len(registered)}, p {p_family} (registered {prior['p_permutation_exact']}), "
            f"cluster p {round(p_cluster, 5)} (registered {prior['p_permutation_cluster_level']}), differing: {mismatched}")

    # Procedure 1.
    replaced = copy.deepcopy(frozen)
    for family in replaced:
        family.update(SOURCE_VALUES.get(family["family"], {}))
    source = classify(replaced)
    registered_by = {r["family"]: r for r in registered}
    per_family = []
    for row in source:
        name, before = row["family"], registered_by[row["family"]]
        value_used = "source" if name in SOURCE_VALUES else \
            "registered_no_source" if name in NO_PUBLISHED_MR + NO_PUBLISHED_OBS else "registered"
        bound = []
        for candidate in CANDIDATES.get(name, []):
            trial = copy.deepcopy(frozen)
            for family in trial:
                family.update(SOURCE_VALUES.get(family["family"], {}))
                if family["family"] == name:
                    family.update({k: v for k, v in candidate.items() if k != "label"})
            result = next(r for r in classify(trial) if r["family"] == name)
            bound.append({"candidate": candidate["label"], "obs_class": result["obs_class"], "mr_class": result["mr_class"],
                          "classification": result["classification"], "prediction": result["prediction"]})
        per_family.append({
            "family": name, "value_used": value_used, "drug_outcome": row["drug_outcome"],
            "source_figure": json.dumps(SOURCE_VALUES[name]) if name in SOURCE_VALUES else "",
            "conversion": CONVERSION.get(name, ""),
            "registered_obs_class": before["obs_class"], "registered_mr_class": before["mr_class"],
            "registered_classification": before["classification"], "registered_prediction": before["prediction"],
            "source_obs_d": row["obs_d"], "source_gen_d": row["gen_d"],
            "source_obs_class": row["obs_class"], "source_mr_class": row["mr_class"],
            "source_classification": row["classification"], "source_prediction": row["prediction"],
            "prediction_changed": row["prediction"] != before["prediction"],
            "label_changed": row["classification"] != before["classification"],
            "correct_under_source": correct(row),
            "bound": bound,
            "prediction_changes_in_bound": any(b["prediction"] != row["prediction"] for b in bound),
            "label_changes_in_bound": any(b["classification"] != row["classification"] for b in bound),
        })

    # Procedure 2.
    set28 = [r for r in source if r["family"] not in NO_PUBLISHED_MR]
    set27 = [r for r in set28 if r["family"] not in NO_PUBLISHED_OBS]
    assert (len(source), len(set28), len(set27)) == (32, 28, 27), (len(source), len(set28), len(set27))
    p28 = hypergeometric_p(set28)
    p28_cluster, clusters28 = cluster_permutation_p(set28)
    domain = {name: ("blind extension" if released[name]["status"] == "extension" else "original domains") for name in scored_names}

    results = {
        "registration": "Amendment 6, commit 3aacce6",
        "inputs": {"classifier": os.path.relpath(CLASSIFIER, ROOT), "families": os.path.relpath(FAMILIES_CSV, ROOT),
                   "source_values": SOURCE_VALUES, "candidates": CANDIDATES,
                   "no_published_mr_estimate": list(NO_PUBLISHED_MR), "no_published_obs_estimate": list(NO_PUBLISHED_OBS),
                   "n_perm": N_PERM, "seed": SEED},
        "expected_from_amendment": EXPECTED,
        "wiring_check": {"n": len(registered), "correct": accuracy(registered), "families_differing_from_released_file": mismatched,
                         "p_permutation_exact": p_family, "registered_p_permutation_exact": prior["p_permutation_exact"],
                         "p_permutation_cluster_level": round(p_cluster, 5),
                         "registered_p_permutation_cluster_level": prior["p_permutation_cluster_level"],
                         "n_instrument_clusters": n_clusters, "classifier_sha256": CLASSIFIER_SHA256},
        "procedure_1_source_reported_values": {
            **summarize(source),
            "predictions_changed": [f["family"] for f in per_family if f["prediction_changed"]],
            "labels_changed": [f["family"] for f in per_family if f["label_changed"]],
            "predictions_changing_within_bound": [f["family"] for f in per_family if f["prediction_changes_in_bound"]],
            "labels_changing_within_bound": [f["family"] for f in per_family if f["label_changes_in_bound"]],
            "mr_only_rule_identical": mr_only_identical(source),
        },
        "procedure_2_published_mr_estimate_set": {
            **summarize(set28), "removed": list(NO_PUBLISHED_MR),
            "p_permutation_exact_descriptive": round(p28, 5),
            "p_permutation_cluster_level_descriptive": round(p28_cluster, 5), "n_instrument_clusters": clusters28,
            "by_tier": {tier: {"n": sum(domain[r["family"]] == tier for r in set28),
                               "correct": sum(correct(r) for r in set28 if domain[r["family"]] == tier)}
                        for tier in ("original domains", "blind extension")},
            "mr_only_rule_identical": mr_only_identical(set28),
        },
        "descriptive_row_without_il23_psoriasis": {**summarize(set27), "removed": list(NO_PUBLISHED_MR + NO_PUBLISHED_OBS), "test": "none"},
        "per_family": per_family,
    }
    with open(os.path.join(HERE, "source_values_results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    with open(os.path.join(HERE, "source_values_by_family.csv"), "w", newline="", encoding="utf-8") as fh:
        fields = [k for k in per_family[0] if k != "bound"]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: f[k] for k in fields} for f in per_family)

    for key in ("procedure_1_source_reported_values", "procedure_2_published_mr_estimate_set", "descriptive_row_without_il23_psoriasis"):
        block = results[key]
        print(f"{key}: {block['correct']}/{block['n']} = {block['accuracy']:.3f}")
    print("wrote", HERE)


if __name__ == "__main__":
    main()
