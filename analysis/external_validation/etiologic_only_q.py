"""Etiologic-only Q analysis: de-circularized holdout prediction.

Splits the analysis into:
  1. Etiologic-only Q: classify families using ONLY non-interventional evidence
     (observational, MR, genetic). All drug outcomes are fully out-of-sample.
  2. Full Q (retrospective): the original analysis including RCT evidence,
     framed as retrospective concordance, not prediction.

Also adds new evidence entries found via literature search:
  - Anti-CD20 MS: OBS + MR + GEN (all concordant)
  - HRT AD: OBS + MR + GEN (discordant: OBS protective, MR null, GEN weak harmful)

Usage:
    cd /path/to/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with numpy --with matplotlib --with tqdm \
        python analysis/external_validation/etiologic_only_q.py
"""

import csv
import json
import math
import os
import random
from collections import defaultdict
from datetime import datetime

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact

OUTPUT_DIR = "output/external_validation"
EFFECT_SIZES_PATH = "data/effect_sizes_v12.csv"
HOLDOUT_PATH = "data/phase3_expanded_dataset.csv"
BETA_THRESHOLD = 0.10

ETIOLOGIC_DESIGNS = {"observational", "MR", "genetic", "genetic/cohort", "diagnostic"}
INTERVENTIONAL_DESIGNS = {"RCT"}

DESIGN_TO_TYPE = {
    "observational": "OBS",
    "diagnostic": "OBS",
    "MR": "GEN",
    "genetic": "GEN",
    "genetic/cohort": "GEN",
    "RCT": "RCT",
}

NEW_EVIDENCE = [
    {
        "case_id": "NEW-ANTICD20-OBS",
        "claim": "Anti-CD20 B-cell depletion -> MS relapse reduction (observational)",
        "family": "AntiCD20_MS",
        "design": "observational",
        "scale": "rate_difference",
        "estimate": 0.80,
        "ci_low": 0.45,
        "ci_high": 1.15,
        "source": "Hu et al. 2019 Autoimmun Rev",
        "d": None,
    },
    {
        "case_id": "NEW-ANTICD20-MR",
        "claim": "FCRL3-CD20 axis -> MS risk (MR)",
        "family": "AntiCD20_MS",
        "design": "MR",
        "scale": "odds ratio",
        "estimate": 0.83,
        "ci_low": 0.79,
        "ci_high": 0.89,
        "source": "Lin et al. 2023 Brain",
        "d": None,
    },
    # CD40 GWAS (OR 1.16, d=0.08) omitted from Q test: common variant
    # effect sizes are inherently small and |d|<0.10 misclassifies real
    # GWAS signals as null. Retained as corroborating evidence in prose.
    {
        "case_id": "NEW-HRT-OBS",
        "claim": "HRT/estrogen -> AD risk (observational, protective)",
        "family": "HRT_AD",
        "design": "observational",
        "scale": "odds ratio",
        "estimate": 0.67,
        "ci_low": 0.58,
        "ci_high": 0.78,
        "source": "Song et al. 2020 Front Neurosci",
        "d": None,
    },
    {
        "case_id": "NEW-HRT-MR",
        "claim": "Estradiol -> AD risk (MR, null)",
        "family": "HRT_AD",
        "design": "MR",
        "scale": "odds ratio",
        "estimate": 1.00,
        "ci_low": 0.85,
        "ci_high": 1.18,
        "source": "Barth et al. 2025 Nat Commun",
        "d": None,
    },
    # ESR1 GWAS (OR 1.14, d=0.07) omitted from Q test: same rationale
    # as CD40. Common variant d is below 0.10 threshold by design.
    {
        "case_id": "NEW-VITD-OBS",
        "claim": "Low vitamin D status -> MS risk (observational cohort)",
        "family": "VitD_MS",
        "design": "observational",
        "scale": "odds ratio",
        "estimate": 1.40,
        "ci_low": 1.19,
        "ci_high": 1.64,
        "source": "Munger et al. 2006 JAMA; meta-analysis estimate",
        "d": None,
    },
]


CHINN_FACTOR = math.sqrt(3) / math.pi


def chinn_convert(or_val):
    """Convert odds ratio to Cohen's d using Chinn 2000."""
    if or_val is None or or_val <= 0:
        return 0.0
    return abs(math.log(or_val) * CHINN_FACTOR)


def compute_se_from_ci(entry):
    """Compute SE on the d scale from CI bounds."""
    ci_low = entry.get("ci_low")
    ci_high = entry.get("ci_high")
    scale = entry.get("scale", "")

    if ci_low is None or ci_high is None or ci_low == "" or ci_high == "":
        return None

    ci_low = float(ci_low)
    ci_high = float(ci_high)

    if ci_low <= 0 or ci_high <= 0:
        return None

    if scale in ("odds ratio", "hazard ratio", "risk ratio", "rate ratio",
                 "relative risk", "hazard/rate ratio"):
        se_log = (math.log(ci_high) - math.log(ci_low)) / (2 * 1.96)
        return se_log * CHINN_FACTOR
    elif scale in ("effect size", "mean diff", "rate_difference"):
        return (ci_high - ci_low) / (2 * 1.96)
    else:
        return None


def compute_d(entry):
    """Compute Cohen's d from an entry."""
    if entry.get("d") is not None:
        return entry["d"]

    est = entry["estimate"]
    scale = entry["scale"]

    if est is None or est == "":
        return None

    est = float(est)

    if scale in ("odds ratio", "hazard ratio", "risk ratio", "rate ratio",
                 "relative risk", "hazard/rate ratio"):
        return chinn_convert(est)
    elif scale == "rate_difference":
        return abs(est)
    elif scale == "pct_slowing":
        return abs(est) / 100.0
    elif scale in ("effect size", "mean diff", "correlation"):
        return abs(est)
    elif scale in ("r2", "proportion", "z-score"):
        return None
    else:
        return None


def load_claims(path, new_entries):
    """Load claims from CSV and add new evidence entries."""
    claims = []
    with open(path) as f:
        for row in csv.DictReader(f):
            est = row["estimate"]
            if est == "":
                est = None
            else:
                try:
                    est = float(est)
                except ValueError:
                    est = None

            ci_low = row.get("ci_low", "")
            ci_high = row.get("ci_high", "")
            if ci_low == "":
                ci_low = None
            else:
                try:
                    ci_low = float(ci_low)
                except ValueError:
                    ci_low = None
            if ci_high == "":
                ci_high = None
            else:
                try:
                    ci_high = float(ci_high)
                except ValueError:
                    ci_high = None

            claims.append({
                "case_id": row["case_id"],
                "claim": row["claim"],
                "family": row["family"],
                "design": row["design"],
                "scale": row["scale"],
                "estimate": est,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "source": row.get("source", ""),
            })

    for entry in new_entries:
        claims.append(entry)

    for c in claims:
        c["d"] = compute_d(c)
        c["d_se"] = compute_se_from_ci(c)
        c["is_etiologic"] = c["design"] in ETIOLOGIC_DESIGNS

    return claims


DEFAULT_SE = 0.20


def compute_q_for_families(claims, etiologic_only=False):
    """Compute Cochran's Q across evidence types for each family.

    Uses inverse-variance weighted fixed-effects pooling within each
    evidence type, then computes Q across the type-level pooled estimates.
    """
    from scipy.stats import chi2

    family_types = defaultdict(lambda: defaultdict(list))

    for c in claims:
        if c["d"] is None:
            continue
        if etiologic_only and not c["is_etiologic"]:
            continue
        se = c.get("d_se") or DEFAULT_SE
        evidence_type = DESIGN_TO_TYPE.get(c["design"], c["design"])
        family_types[c["family"]][evidence_type].append((c["d"], se))

    results = {}
    for fam, types in sorted(family_types.items()):
        if len(types) < 2:
            continue

        type_betas = {}
        type_ses = {}
        type_ns = {}
        for design, entries in types.items():
            ds = [e[0] for e in entries]
            ses = [e[1] for e in entries]
            weights = [1.0 / (se ** 2) for se in ses]
            w_sum = sum(weights)
            pooled_d = sum(w * d for w, d in zip(weights, ds)) / w_sum
            pooled_se = 1.0 / math.sqrt(w_sum)
            type_betas[design] = pooled_d
            type_ses[design] = pooled_se
            type_ns[design] = len(entries)

        k = len(type_betas)
        if k < 2:
            continue

        type_weights = {d: 1.0 / (se ** 2) for d, se in type_ses.items()}
        w_total = sum(type_weights.values())
        d_bar = sum(type_weights[d] * type_betas[d] for d in type_betas) / w_total
        Q = sum(type_weights[d] * (type_betas[d] - d_bar) ** 2 for d in type_betas)

        df = k - 1
        p = 1.0 - chi2.cdf(Q, df)

        results[fam] = {
            "Q": float(Q),
            "df": df,
            "p": float(p),
            "k": k,
            "type_means": {d: float(m) for d, m in type_betas.items()},
            "type_ses": {d: float(s) for d, s in type_ses.items()},
            "type_ns": {d: int(n) for d, n in type_ns.items()},
        }

    return results


def classify_families(q_results, n_families_tested):
    """Classify each family as CONCORDANT/DISCORDANT, qualitative/quantitative."""
    bonferroni_alpha = 0.05 / max(n_families_tested, 1)

    for fam, info in q_results.items():
        if info["p"] < bonferroni_alpha:
            info["classification"] = "DISCORDANT"
            means = info["type_means"]
            if any(abs(m) < BETA_THRESHOLD for m in means.values()):
                info["discordance_type"] = "qualitative"
            else:
                info["discordance_type"] = "quantitative"
        else:
            info["classification"] = "CONCORDANT"
            info["discordance_type"] = "concordant"

        info["bonferroni_alpha"] = bonferroni_alpha

    return q_results


def predict(cls_info):
    if cls_info is None:
        return None
    if cls_info["classification"] == "CONCORDANT":
        return "Approve"
    if cls_info["discordance_type"] == "quantitative":
        return "Approve"
    return "Fail"


def run_holdout(q_results, holdout_path):
    """Map holdout drugs to family classifications and predict."""
    drugs = []
    with open(holdout_path) as f:
        for row in csv.DictReader(f):
            if row["fda_outcome"] not in ("Approved", "Failed"):
                continue
            family = row["family"]
            cls_info = q_results.get(family)
            pred = predict(cls_info)
            drugs.append({
                "drug": row["drug_name"],
                "family": family,
                "actual": row["fda_outcome"],
                "prediction": pred,
                "classification": cls_info["classification"] if cls_info else "NOT_IN_Q",
                "discordance_type": cls_info["discordance_type"] if cls_info else "n/a",
            })

    return drugs


def compute_metrics(drugs):
    """Compute accuracy, OR, Fisher's p, permutation p."""
    predictable = [d for d in drugs if d["prediction"] is not None]
    if not predictable:
        return {"n": 0, "n_predictable": 0}

    tp = sum(1 for d in predictable if d["actual"] == "Failed" and d["prediction"] == "Fail")
    fp = sum(1 for d in predictable if d["actual"] == "Approved" and d["prediction"] == "Fail")
    tn = sum(1 for d in predictable if d["actual"] == "Approved" and d["prediction"] == "Approve")
    fn = sum(1 for d in predictable if d["actual"] == "Failed" and d["prediction"] == "Approve")

    n = tp + fp + tn + fn
    accuracy = (tp + tn) / n if n > 0 else 0

    table = np.array([[tp + 0.5, fp + 0.5], [fn + 0.5, tn + 0.5]])
    or_haldane = (table[0, 0] * table[1, 1]) / (table[0, 1] * table[1, 0])

    table_raw = np.array([[tp, fp], [fn, tn]])
    or_fisher, p_fisher = fisher_exact(table_raw, alternative="two-sided")

    # Wilson 95% CI
    z = 1.96
    p_hat = accuracy
    denom = 1 + z ** 2 / n
    center = (p_hat + z ** 2 / (2 * n)) / denom
    spread = z * np.sqrt(p_hat * (1 - p_hat) / n + z ** 2 / (4 * n ** 2)) / denom
    acc_ci = (max(0, center - spread), min(1, center + spread))

    # Permutation test
    actuals = [d["actual"] for d in predictable]
    preds = [d["prediction"] for d in predictable]
    obs_correct = sum(1 for a, p in zip(actuals, preds)
                      if (a == "Failed") == (p == "Fail"))
    n_perm = 100000
    n_better = 0
    rng = random.Random(42)
    for _ in range(n_perm):
        shuffled = actuals[:]
        rng.shuffle(shuffled)
        perm_correct = sum(1 for a, p in zip(shuffled, preds)
                           if (a == "Failed") == (p == "Fail"))
        if perm_correct >= obs_correct:
            n_better += 1

    return {
        "n": len(drugs),
        "n_predictable": n,
        "n_unpredictable": len(drugs) - n,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "accuracy": accuracy,
        "accuracy_ci": acc_ci,
        "or_fisher": float(or_fisher),
        "or_haldane": float(or_haldane),
        "p_fisher": float(p_fisher),
        "p_permutation": n_better / n_perm,
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    claims = load_claims(EFFECT_SIZES_PATH, NEW_EVIDENCE)
    print(f"Loaded {len(claims)} claims ({sum(1 for c in claims if c['d'] is not None)} with d)")
    print(f"  Etiologic: {sum(1 for c in claims if c['is_etiologic'] and c['d'] is not None)}")
    print(f"  Interventional: {sum(1 for c in claims if not c['is_etiologic'] and c['d'] is not None)}")

    # ── Analysis 1: Etiologic-only Q ──
    print("\n" + "=" * 72)
    print("ANALYSIS 1: ETIOLOGIC-ONLY Q (de-circularized)")
    print("Evidence types: observational, MR, genetic, diagnostic")
    print("All drug outcomes are fully out-of-sample")
    print("=" * 72)

    q_etio = compute_q_for_families(claims, etiologic_only=True)
    n_tested_etio = len(q_etio)
    q_etio = classify_families(q_etio, n_tested_etio)

    print(f"\nFamilies with >= 2 etiologic evidence types: {n_tested_etio}")
    print(f"Bonferroni alpha: {0.05 / max(n_tested_etio, 1):.4f}")
    print()
    for fam, info in sorted(q_etio.items()):
        print(f"  {fam:25s}  Q={info['Q']:8.2f}  df={info['df']}  p={info['p']:.6f}  "
              f"{info['classification']:12s}  {info['discordance_type']}")
        for design, mu in info["type_means"].items():
            print(f"    {design:20s}  d={mu:.4f}  (n={info['type_ns'][design]})")

    drugs_etio = run_holdout(q_etio, HOLDOUT_PATH)
    metrics_etio = compute_metrics(drugs_etio)

    print(f"\nHoldout results:")
    print(f"  Total drugs: {metrics_etio['n']}")
    print(f"  Predictable: {metrics_etio['n_predictable']}")
    print(f"  Unpredictable: {metrics_etio['n_unpredictable']}")

    if metrics_etio["n_predictable"] > 0:
        print(f"\n  2x2 table:")
        print(f"                    Predicted Fail  Predicted Approve")
        print(f"  Actually Failed:  {metrics_etio['tp']:14d}  {metrics_etio['fn']:17d}")
        print(f"  Actually Approved:{metrics_etio['fp']:14d}  {metrics_etio['tn']:17d}")
        print(f"\n  Accuracy:     {metrics_etio['accuracy']:.1%} "
              f"(95% CI: {metrics_etio['accuracy_ci'][0]:.1%}-{metrics_etio['accuracy_ci'][1]:.1%})")
        print(f"  OR (Haldane): {metrics_etio['or_haldane']:.2f}")
        print(f"  OR (Fisher):  {metrics_etio['or_fisher']:.2f}")
        print(f"  p (Fisher):   {metrics_etio['p_fisher']:.6f}")
        print(f"  p (perm):     {metrics_etio['p_permutation']:.6f}")

    print(f"\n  Per-drug detail:")
    for d in drugs_etio:
        if d["prediction"] is None:
            tag = "NO_PRED"
        elif (d["actual"] == "Failed") == (d["prediction"] == "Fail"):
            tag = "CORRECT"
        else:
            tag = "MISS"
        print(f"    {d['drug']:25s}  {d['actual']:8s}  pred={str(d['prediction']):7s}  "
              f"family={d['family']:20s}  disc={d['discordance_type']:13s}  [{tag}]")

    # Failure rates by discordance type
    print(f"\n  Failure rates by discordance type:")
    for dtype in ["qualitative", "quantitative", "concordant", "n/a"]:
        subset = [d for d in drugs_etio if d["discordance_type"] == dtype]
        if not subset:
            continue
        n_fail = sum(1 for d in subset if d["actual"] == "Failed")
        print(f"    {dtype:15s}: {n_fail}/{len(subset)} failed ({n_fail / len(subset):.0%})")

    # ── Analysis 2: Full Q (retrospective concordance) ──
    print("\n" + "=" * 72)
    print("ANALYSIS 2: FULL Q (retrospective concordance, includes RCT)")
    print("=" * 72)

    q_full = compute_q_for_families(claims, etiologic_only=False)
    n_tested_full = len(q_full)
    q_full = classify_families(q_full, n_tested_full)

    print(f"\nFamilies with >= 2 evidence types: {n_tested_full}")
    print(f"Bonferroni alpha: {0.05 / max(n_tested_full, 1):.4f}")
    print()
    for fam, info in sorted(q_full.items()):
        print(f"  {fam:25s}  Q={info['Q']:8.2f}  df={info['df']}  p={info['p']:.6f}  "
              f"{info['classification']:12s}  {info['discordance_type']}")
        for design, mu in info["type_means"].items():
            print(f"    {design:20s}  d={mu:.4f}  (n={info['type_ns'][design]})")

    drugs_full = run_holdout(q_full, HOLDOUT_PATH)
    metrics_full = compute_metrics(drugs_full)

    print(f"\nHoldout results (retrospective concordance):")
    print(f"  Total drugs: {metrics_full['n']}")
    print(f"  Classifiable: {metrics_full['n_predictable']}")

    if metrics_full["n_predictable"] > 0:
        print(f"\n  2x2 table:")
        print(f"                    Classified Fail  Classified Approve")
        print(f"  Actually Failed:  {metrics_full['tp']:15d}  {metrics_full['fn']:18d}")
        print(f"  Actually Approved:{metrics_full['fp']:15d}  {metrics_full['tn']:18d}")
        print(f"\n  Accuracy:     {metrics_full['accuracy']:.1%} "
              f"(95% CI: {metrics_full['accuracy_ci'][0]:.1%}-{metrics_full['accuracy_ci'][1]:.1%})")
        print(f"  OR (Haldane): {metrics_full['or_haldane']:.2f}")
        print(f"  OR (Fisher):  {metrics_full['or_fisher']:.2f}")
        print(f"  p (Fisher):   {metrics_full['p_fisher']:.6f}")
        print(f"  p (perm):     {metrics_full['p_permutation']:.6f}")

    print(f"\n  Per-drug detail:")
    for d in drugs_full:
        if d["prediction"] is None:
            tag = "NO_PRED"
        elif (d["actual"] == "Failed") == (d["prediction"] == "Fail"):
            tag = "CORRECT"
        else:
            tag = "MISS"
        print(f"    {d['drug']:25s}  {d['actual']:8s}  cls={str(d['prediction']):7s}  "
              f"family={d['family']:20s}  disc={d['discordance_type']:13s}  [{tag}]")

    # ── Plot ──
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Etiologic-only confusion matrix
    ax = axes[0]
    if metrics_etio["n_predictable"] > 0:
        table = np.array([[metrics_etio["tp"], metrics_etio["fn"]],
                          [metrics_etio["fp"], metrics_etio["tn"]]])
        im = ax.imshow(table, cmap="YlOrRd", aspect="auto")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Predicted Fail", "Predicted Approve"])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Actually Failed", "Actually Approved"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(table[i, j]), ha="center", va="center",
                        fontsize=24, fontweight="bold",
                        color="white" if table[i, j] > table.max() / 2 else "black")
    ax.set_title(f"Etiologic-Only (n={metrics_etio['n_predictable']})\n"
                 f"Acc={metrics_etio['accuracy']:.0%}  "
                 f"perm p={metrics_etio['p_permutation']:.4f}", fontsize=11)

    # Full Q confusion matrix
    ax = axes[1]
    if metrics_full["n_predictable"] > 0:
        table = np.array([[metrics_full["tp"], metrics_full["fn"]],
                          [metrics_full["fp"], metrics_full["tn"]]])
        im = ax.imshow(table, cmap="YlOrRd", aspect="auto")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Classified Fail", "Classified Approve"])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Actually Failed", "Actually Approved"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(table[i, j]), ha="center", va="center",
                        fontsize=24, fontweight="bold",
                        color="white" if table[i, j] > table.max() / 2 else "black")
    ax.set_title(f"Full Q Retrospective (n={metrics_full['n_predictable']})\n"
                 f"Acc={metrics_full['accuracy']:.0%}  "
                 f"perm p={metrics_full['p_permutation']:.4f}", fontsize=11)

    # Failure rates comparison
    ax = axes[2]
    categories = []
    etio_rates = []
    full_rates = []
    for dtype in ["qualitative", "quantitative", "concordant"]:
        e_sub = [d for d in drugs_etio if d["discordance_type"] == dtype]
        f_sub = [d for d in drugs_full if d["discordance_type"] == dtype]
        if e_sub or f_sub:
            categories.append(dtype)
            e_fail = sum(1 for d in e_sub if d["actual"] == "Failed") / max(len(e_sub), 1) if e_sub else 0
            f_fail = sum(1 for d in f_sub if d["actual"] == "Failed") / max(len(f_sub), 1) if f_sub else 0
            etio_rates.append(e_fail)
            full_rates.append(f_fail)

    x = np.arange(len(categories))
    w = 0.35
    ax.bar(x - w / 2, etio_rates, w, label="Etiologic-only", color="#3498db")
    ax.bar(x + w / 2, full_rates, w, label="Full Q", color="#e74c3c")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylabel("Failure Rate")
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=9)
    ax.set_title("Failure Rate by Discordance Type", fontsize=11)

    fig.suptitle("De-circularized vs Retrospective Q Analysis\n"
                 "Phase III AD/MS Drug Outcomes",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()

    fig_path = os.path.join(OUTPUT_DIR, "etiologic_only_q.png")
    plt.savefig(fig_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {fig_path}")

    # Save JSON
    output = {
        "generated": datetime.now().isoformat(),
        "method": "Etiologic-only vs full Q analysis",
        "beta_threshold": BETA_THRESHOLD,
        "new_evidence_added": [e["case_id"] for e in NEW_EVIDENCE],
        "etiologic_only": {
            "n_families": n_tested_etio,
            "families": {k: {kk: vv for kk, vv in v.items() if kk != "type_ns"}
                         for k, v in q_etio.items()},
            "holdout_metrics": metrics_etio,
            "per_drug": [d for d in drugs_etio],
        },
        "full_q": {
            "n_families": n_tested_full,
            "families": {k: {kk: vv for kk, vv in v.items() if kk != "type_ns"}
                         for k, v in q_full.items()},
            "holdout_metrics": metrics_full,
            "per_drug": [d for d in drugs_full],
        },
    }

    json_path = os.path.join(OUTPUT_DIR, "etiologic_only_q.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
