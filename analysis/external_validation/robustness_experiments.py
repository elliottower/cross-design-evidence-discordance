"""Robustness experiments for the Q-based discordance prediction.

Three experiments:
  1. Threshold sensitivity: sweep BETA_THRESHOLD from 0.05 to 0.25
  2. Leave-one-family-out cross-validation
  3. Bootstrap confidence intervals on OR and accuracy

Usage:
    cd /path/to/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with numpy --with matplotlib --with tqdm \
        python analysis/external_validation/robustness_experiments.py
"""

import json
import os
from datetime import datetime

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact
from tqdm import tqdm

Q_RESULTS_PATH = "output/h1_transportability_results.json"
EXPANDED_PATH = "data/phase3_expanded_dataset.csv"
OUTPUT_DIR = "output/external_validation"

THRESHOLDS = [0.05, 0.075, 0.10, 0.125, 0.15, 0.20, 0.25]
N_BOOTSTRAP = 10_000
RANDOM_SEED = None  # no fixed seed; reproducibility via large N


def load_q_data(q_path):
    """Load raw Q results with per-family type_details betas."""
    with open(q_path) as f:
        return json.load(f)


def classify_families(q_data, beta_threshold):
    """Classify each family at a given beta threshold.

    Returns dict mapping family name -> classification info.
    """
    classifications = {}
    for fam_name, fam_data in q_data["per_family"].items():
        cls = fam_data["classification"]
        discordance_type = "concordant"
        if cls == "NON-TRANSPORT":
            type_details = fam_data.get("type_details", {})
            betas = [v["beta"] for v in type_details.values()]
            if all(abs(b) >= beta_threshold for b in betas):
                discordance_type = "quantitative"
            else:
                discordance_type = "qualitative"

        classifications[fam_name] = {
            "classification": cls,
            "discordance_type": discordance_type,
        }
    return classifications


def predict_refined(cls_info):
    """Refined prediction: qualitative -> Fail, quantitative -> Approve."""
    if cls_info is None:
        return None
    if cls_info["classification"] == "TRANSPORT":
        return "Approve"
    if cls_info["discordance_type"] == "quantitative":
        return "Approve"
    return "Fail"


def compute_2x2(actual, predicted):
    """Build a 2x2 confusion table and compute OR + Fisher's p.

    Returns (tp, fp, tn, fn, accuracy, odds_ratio, p_fisher).
    """
    tp = sum(1 for a, p in zip(actual, predicted) if a == "Failed" and p == "Fail")
    fp = sum(1 for a, p in zip(actual, predicted) if a == "Approved" and p == "Fail")
    tn = sum(1 for a, p in zip(actual, predicted) if a == "Approved" and p == "Approve")
    fn = sum(1 for a, p in zip(actual, predicted) if a == "Failed" and p == "Approve")

    n = tp + fp + tn + fn
    accuracy = (tp + tn) / n if n > 0 else 0.0

    table = np.array([[tp, fp], [fn, tn]])
    odds_ratio, p_fisher = fisher_exact(table, alternative="two-sided")

    return {
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "n": int(n),
        "accuracy": float(accuracy),
        "odds_ratio": float(odds_ratio),
        "p_fisher": float(p_fisher),
    }


def wilson_ci(p_hat, n, z=1.96):
    """Wilson score 95% CI for a proportion."""
    if n == 0:
        return (0.0, 1.0)
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denom
    spread = z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - spread), min(1.0, center + spread))


# ──────────────────────────────────────────────────────────────────────
# Experiment 1: Threshold sensitivity
# ──────────────────────────────────────────────────────────────────────

def run_threshold_sensitivity(q_data, holdout_df):
    """Sweep BETA_THRESHOLD and report metrics at each value."""
    print("\n" + "=" * 72)
    print("EXPERIMENT 1: THRESHOLD SENSITIVITY ANALYSIS")
    print("=" * 72)

    # Get NON-TRANSPORT families and their minimum |beta|
    non_transport_families = {}
    for fam_name, fam_data in q_data["per_family"].items():
        if fam_data["classification"] == "NON-TRANSPORT":
            betas = [v["beta"] for v in fam_data["type_details"].values()]
            min_beta = min(abs(b) for b in betas)
            non_transport_families[fam_name] = {
                "betas": {k: v["beta"] for k, v in fam_data["type_details"].items()},
                "min_abs_beta": min_beta,
            }

    print(f"\nNON-TRANSPORT families and their min |beta|:")
    for fam, info in sorted(non_transport_families.items(), key=lambda x: x[1]["min_abs_beta"]):
        betas_str = ", ".join(f"{k}={v:.4f}" for k, v in info["betas"].items())
        print(f"  {fam:20s}  min|beta|={info['min_abs_beta']:.4f}  ({betas_str})")

    known = holdout_df[holdout_df["fda_outcome"].isin(["Approved", "Failed"])].copy()

    results_per_threshold = []

    print(f"\n{'Threshold':>10s}  {'Acc':>6s}  {'OR':>8s}  {'p':>8s}  "
          f"{'TP':>3s} {'FP':>3s} {'TN':>3s} {'FN':>3s}  {'n_qual':>6s} {'n_quant':>7s}  "
          f"{'Changed families'}")
    print("-" * 110)

    baseline_classifications = classify_families(q_data, 0.10)

    for threshold in THRESHOLDS:
        classifications = classify_families(q_data, threshold)

        # Identify which families changed relative to the 0.10 baseline
        changed = []
        for fam in sorted(non_transport_families.keys()):
            old_type = baseline_classifications.get(fam, {}).get("discordance_type", "n/a")
            new_type = classifications.get(fam, {}).get("discordance_type", "n/a")
            if old_type != new_type:
                changed.append(f"{fam}: {old_type}->{new_type}")

        # Predict each drug
        actual = []
        predicted = []
        for _, row in known.iterrows():
            cls_info = classifications.get(row["family"])
            pred = predict_refined(cls_info)
            if pred is not None:
                actual.append(row["fda_outcome"])
                predicted.append(pred)

        metrics = compute_2x2(actual, predicted)

        # Count qualitative vs quantitative families (with drugs in holdout)
        holdout_families = set(known["family"].unique())
        n_qual = sum(1 for fam in holdout_families
                     if classifications.get(fam, {}).get("discordance_type") == "qualitative")
        n_quant = sum(1 for fam in holdout_families
                      if classifications.get(fam, {}).get("discordance_type") == "quantitative")

        changed_str = "; ".join(changed) if changed else "(none)"
        or_str = f"{metrics['odds_ratio']:.1f}" if np.isfinite(metrics["odds_ratio"]) else "inf"
        print(f"  {threshold:>8.3f}  {metrics['accuracy']:>5.1%}  {or_str:>8s}  "
              f"{metrics['p_fisher']:>8.4f}  "
              f"{metrics['tp']:>3d} {metrics['fp']:>3d} {metrics['tn']:>3d} {metrics['fn']:>3d}  "
              f"{n_qual:>6d} {n_quant:>7d}  {changed_str}")

        results_per_threshold.append({
            "threshold": threshold,
            "accuracy": metrics["accuracy"],
            "accuracy_ci": list(wilson_ci(metrics["accuracy"], metrics["n"])),
            "odds_ratio": metrics["odds_ratio"],
            "p_fisher": metrics["p_fisher"],
            "tp": metrics["tp"],
            "fp": metrics["fp"],
            "tn": metrics["tn"],
            "fn": metrics["fn"],
            "n": metrics["n"],
            "n_qualitative_families": n_qual,
            "n_quantitative_families": n_quant,
            "changed_from_baseline": changed,
        })

    # Identify the critical switching thresholds
    print(f"\nCritical switching thresholds (where families reclassify):")
    for fam, info in sorted(non_transport_families.items(), key=lambda x: x[1]["min_abs_beta"]):
        # The family switches from qualitative to quantitative at min_abs_beta
        # (when threshold drops below min_abs_beta, it becomes quantitative)
        # Actually: qualitative = some |beta| < threshold, quantitative = all |beta| >= threshold
        # So switching point is at min_abs_beta: below that threshold, family is quantitative
        print(f"  {fam:20s}  switches qual->quant at threshold <= {info['min_abs_beta']:.4f}")

    return results_per_threshold


# ──────────────────────────────────────────────────────────────────────
# Experiment 2: Leave-one-family-out cross-validation
# ──────────────────────────────────────────────────────────────────────

def run_lofo_cv(q_data, holdout_df):
    """Leave-one-family-out CV: remove each family, re-predict rest."""
    print("\n" + "=" * 72)
    print("EXPERIMENT 2: LEAVE-ONE-FAMILY-OUT CROSS-VALIDATION")
    print("=" * 72)

    known = holdout_df[holdout_df["fda_outcome"].isin(["Approved", "Failed"])].copy()
    classifications = classify_families(q_data, 0.10)

    # Families that are both in Q analysis and have drugs in holdout
    holdout_families = set(known["family"].unique())
    q_families = set(q_data["per_family"].keys())
    overlap_families = sorted(holdout_families & q_families)

    print(f"\nFamilies in both Q analysis and holdout ({len(overlap_families)}):")
    for fam in overlap_families:
        n_drugs = len(known[known["family"] == fam])
        disc = classifications.get(fam, {}).get("discordance_type", "n/a")
        cls = classifications.get(fam, {}).get("classification", "n/a")
        print(f"  {fam:20s}  {n_drugs:2d} drugs  {cls:15s}  {disc}")

    fold_results = []

    print(f"\n{'Left out':>20s}  {'Acc':>6s}  {'OR':>8s}  {'p':>8s}  "
          f"{'TP':>3s} {'FP':>3s} {'TN':>3s} {'FN':>3s}  {'n':>3s}")
    print("-" * 80)

    for leave_out in overlap_families:
        # Remove the left-out family's drugs from prediction
        remaining = known[known["family"] != leave_out]

        actual = []
        predicted = []
        for _, row in remaining.iterrows():
            cls_info = classifications.get(row["family"])
            pred = predict_refined(cls_info)
            if pred is not None:
                actual.append(row["fda_outcome"])
                predicted.append(pred)

        if len(actual) == 0:
            print(f"  {leave_out:>20s}  (no predictable drugs remaining)")
            fold_results.append({
                "left_out": leave_out,
                "n_removed": len(known[known["family"] == leave_out]),
                "n_remaining": 0,
                "accuracy": None,
                "odds_ratio": None,
                "p_fisher": None,
            })
            continue

        metrics = compute_2x2(actual, predicted)

        or_str = f"{metrics['odds_ratio']:.1f}" if np.isfinite(metrics["odds_ratio"]) else "inf"
        print(f"  {leave_out:>20s}  {metrics['accuracy']:>5.1%}  {or_str:>8s}  "
              f"{metrics['p_fisher']:>8.4f}  "
              f"{metrics['tp']:>3d} {metrics['fp']:>3d} {metrics['tn']:>3d} {metrics['fn']:>3d}  "
              f"{metrics['n']:>3d}")

        fold_results.append({
            "left_out": leave_out,
            "n_removed": int(len(known[known["family"] == leave_out])),
            "n_remaining": metrics["n"],
            "accuracy": metrics["accuracy"],
            "odds_ratio": metrics["odds_ratio"],
            "p_fisher": metrics["p_fisher"],
            "tp": metrics["tp"],
            "fp": metrics["fp"],
            "tn": metrics["tn"],
            "fn": metrics["fn"],
        })

    # Summary statistics
    valid_accs = [f["accuracy"] for f in fold_results if f["accuracy"] is not None]
    if valid_accs:
        mean_acc = np.mean(valid_accs)
        min_acc = np.min(valid_accs)
        max_acc = np.max(valid_accs)
        print(f"\n  Mean LOFO accuracy: {mean_acc:.1%}")
        print(f"  Range: {min_acc:.1%} - {max_acc:.1%}")
        print(f"  Folds with p < 0.05: {sum(1 for f in fold_results if f['p_fisher'] is not None and f['p_fisher'] < 0.05)}/{len(valid_accs)}")

    lofo_summary = {
        "n_folds": len(overlap_families),
        "mean_accuracy": float(mean_acc) if valid_accs else None,
        "min_accuracy": float(min_acc) if valid_accs else None,
        "max_accuracy": float(max_acc) if valid_accs else None,
    }

    return fold_results, lofo_summary


# ──────────────────────────────────────────────────────────────────────
# Experiment 3: Bootstrap CI on OR
# ──────────────────────────────────────────────────────────────────────

def run_bootstrap_ci(q_data, holdout_df):
    """Bootstrap the 23 predictable drugs to get CI on OR and accuracy."""
    print("\n" + "=" * 72)
    print("EXPERIMENT 3: BOOTSTRAP CONFIDENCE INTERVALS (n=10,000)")
    print("=" * 72)

    known = holdout_df[holdout_df["fda_outcome"].isin(["Approved", "Failed"])].copy()
    classifications = classify_families(q_data, 0.10)

    # Build the predictable dataset
    predictable_drugs = []
    for _, row in known.iterrows():
        cls_info = classifications.get(row["family"])
        pred = predict_refined(cls_info)
        if pred is not None:
            predictable_drugs.append({
                "actual": row["fda_outcome"],
                "predicted": pred,
                "family": row["family"],
                "drug": row["drug_name"],
            })

    predictable_df = pd.DataFrame(predictable_drugs)
    n = len(predictable_df)
    print(f"\n  Predictable drugs: {n}")
    print(f"  Bootstrap samples: {N_BOOTSTRAP}")

    rng = np.random.default_rng()

    bootstrap_ors = []
    bootstrap_accs = []
    bootstrap_ps = []
    n_or_gt1 = 0
    n_sig = 0
    n_inf = 0

    actual_arr = predictable_df["actual"].values
    pred_arr = predictable_df["predicted"].values

    for _ in tqdm(range(N_BOOTSTRAP), desc="  Bootstrap"):
        idx = rng.integers(0, n, size=n)
        boot_actual = actual_arr[idx]
        boot_pred = pred_arr[idx]

        tp = np.sum((boot_actual == "Failed") & (boot_pred == "Fail"))
        fp = np.sum((boot_actual == "Approved") & (boot_pred == "Fail"))
        tn = np.sum((boot_actual == "Approved") & (boot_pred == "Approve"))
        fn = np.sum((boot_actual == "Failed") & (boot_pred == "Approve"))

        acc = (tp + tn) / n if n > 0 else 0.0
        bootstrap_accs.append(acc)

        table = np.array([[int(tp), int(fp)], [int(fn), int(tn)]])
        odds_ratio, p_fisher = fisher_exact(table, alternative="two-sided")

        bootstrap_ors.append(float(odds_ratio))
        bootstrap_ps.append(float(p_fisher))

        if odds_ratio > 1:
            n_or_gt1 += 1
        if np.isinf(odds_ratio):
            n_inf += 1
        if p_fisher < 0.05:
            n_sig += 1

    bootstrap_ors = np.array(bootstrap_ors)
    bootstrap_accs = np.array(bootstrap_accs)
    bootstrap_ps = np.array(bootstrap_ps)

    # Handle inf values for OR percentiles
    finite_ors = bootstrap_ors[np.isfinite(bootstrap_ors)]

    or_ci_lo = float(np.percentile(finite_ors, 2.5)) if len(finite_ors) > 0 else float("inf")
    or_ci_hi = float(np.percentile(finite_ors, 97.5)) if len(finite_ors) > 0 else float("inf")
    or_median = float(np.median(finite_ors)) if len(finite_ors) > 0 else float("inf")

    acc_ci_lo = float(np.percentile(bootstrap_accs, 2.5))
    acc_ci_hi = float(np.percentile(bootstrap_accs, 97.5))
    acc_median = float(np.median(bootstrap_accs))

    print(f"\n  Results:")
    print(f"    OR median:        {or_median:.1f}")
    print(f"    OR 95% CI:        [{or_ci_lo:.1f}, {or_ci_hi:.1f}]")
    print(f"    OR = inf:         {n_inf}/{N_BOOTSTRAP} ({n_inf/N_BOOTSTRAP:.1%})")
    print(f"    OR > 1:           {n_or_gt1}/{N_BOOTSTRAP} ({n_or_gt1/N_BOOTSTRAP:.1%})")
    print(f"    p < 0.05:         {n_sig}/{N_BOOTSTRAP} ({n_sig/N_BOOTSTRAP:.1%})")
    print(f"")
    print(f"    Accuracy median:  {acc_median:.1%}")
    print(f"    Accuracy 95% CI:  [{acc_ci_lo:.1%}, {acc_ci_hi:.1%}]")

    # Percentile table
    print(f"\n  OR percentiles:")
    for pct in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
        val = np.percentile(finite_ors, pct) if len(finite_ors) > 0 else float("inf")
        print(f"    {pct:3d}th: {val:.1f}")

    bootstrap_result = {
        "n_drugs": int(n),
        "n_bootstrap": N_BOOTSTRAP,
        "or_median": or_median,
        "or_ci_95": [or_ci_lo, or_ci_hi],
        "or_mean_finite": float(np.mean(finite_ors)) if len(finite_ors) > 0 else None,
        "n_or_inf": int(n_inf),
        "frac_or_gt1": float(n_or_gt1 / N_BOOTSTRAP),
        "frac_p_lt_05": float(n_sig / N_BOOTSTRAP),
        "accuracy_median": acc_median,
        "accuracy_ci_95": [acc_ci_lo, acc_ci_hi],
        "accuracy_mean": float(np.mean(bootstrap_accs)),
    }

    return bootstrap_result, bootstrap_ors, bootstrap_accs, bootstrap_ps


# ──────────────────────────────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────────────────────────────

def make_plots(threshold_results, lofo_results, bootstrap_ors, bootstrap_accs):
    """3-panel figure: threshold curve, LOFO bars, bootstrap OR histogram."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    # ── Panel 1: Threshold sensitivity ──
    ax = axes[0]
    thresholds = [r["threshold"] for r in threshold_results]
    accuracies = [r["accuracy"] for r in threshold_results]
    ors = [r["odds_ratio"] for r in threshold_results]
    ps = [r["p_fisher"] for r in threshold_results]
    ci_los = [r["accuracy_ci"][0] for r in threshold_results]
    ci_his = [r["accuracy_ci"][1] for r in threshold_results]

    color_acc = "#2c3e50"
    color_or = "#c0392b"

    ax.fill_between(thresholds, ci_los, ci_his, alpha=0.15, color=color_acc)
    ax.plot(thresholds, accuracies, "o-", color=color_acc, linewidth=2, markersize=7,
            label="Accuracy", zorder=3)
    ax.axvline(0.10, color="#7f8c8d", linestyle="--", alpha=0.6, label="Paper threshold (0.10)")
    ax.set_xlabel("Beta threshold |d|", fontsize=11)
    ax.set_ylabel("Prediction accuracy", fontsize=11, color=color_acc)
    ax.set_ylim(0.4, 1.05)
    ax.tick_params(axis="y", labelcolor=color_acc)

    # Secondary y-axis for OR
    ax2 = ax.twinx()
    # Cap infinite ORs for display
    or_display = [min(o, 200) for o in ors]
    ax2.plot(thresholds, or_display, "s--", color=color_or, linewidth=1.5, markersize=6,
             label="Odds ratio", zorder=2)
    ax2.set_ylabel("Odds ratio", fontsize=11, color=color_or)
    ax2.tick_params(axis="y", labelcolor=color_or)

    # Mark significant p-values
    for t, acc, p in zip(thresholds, accuracies, ps):
        if p < 0.05:
            ax.plot(t, acc, "o", color="#27ae60", markersize=12, markerfacecolor="none",
                    linewidth=2, zorder=4)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="lower left", fontsize=8)
    ax.set_title("Threshold sensitivity\n(green ring = p < 0.05)", fontsize=11)

    # ── Panel 2: LOFO accuracy bars ──
    ax = axes[1]
    valid_folds = [f for f in lofo_results if f["accuracy"] is not None]
    families = [f["left_out"] for f in valid_folds]
    accs = [f["accuracy"] for f in valid_folds]
    n_remaining = [f["n_remaining"] for f in valid_folds]
    sig = [f["p_fisher"] < 0.05 for f in valid_folds]

    # Sort by accuracy
    order = np.argsort(accs)[::-1]
    families = [families[i] for i in order]
    accs = [accs[i] for i in order]
    n_remaining = [n_remaining[i] for i in order]
    sig = [sig[i] for i in order]

    colors = ["#27ae60" if s else "#e74c3c" for s in sig]
    bars = ax.barh(range(len(families)), accs, color=colors, edgecolor="white", linewidth=0.8)

    # Full-model baseline
    ax.axvline(0.8696, color="#2c3e50", linestyle="--", linewidth=1.5, alpha=0.7,
               label="Full model (87.0%)")

    ax.set_yticks(range(len(families)))
    ax.set_yticklabels([f"{fam}\n(n={n})" for fam, n in zip(families, n_remaining)], fontsize=8)
    ax.set_xlabel("Accuracy (leave-one-out)", fontsize=11)
    ax.set_xlim(0, 1.15)
    ax.invert_yaxis()

    for i, (acc, n) in enumerate(zip(accs, n_remaining)):
        ax.text(acc + 0.02, i, f"{acc:.0%}", va="center", fontsize=9)

    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Leave-one-family-out CV\n(green = p < 0.05)", fontsize=11)

    # ── Panel 3: Bootstrap OR distribution ──
    ax = axes[2]
    finite_ors = bootstrap_ors[np.isfinite(bootstrap_ors)]

    # Use log scale for display
    log_ors = np.log10(np.clip(finite_ors, 0.01, None))
    ax.hist(log_ors, bins=60, color="#2980b9", edgecolor="white", linewidth=0.5, alpha=0.85,
            density=True)

    # Mark the observed OR=42
    ax.axvline(np.log10(42), color="#c0392b", linestyle="-", linewidth=2.5,
               label=f"Observed OR = 42")
    ax.axvline(np.log10(1), color="#7f8c8d", linestyle="--", linewidth=1.5, alpha=0.7,
               label="OR = 1 (null)")

    # Mark 95% CI
    or_ci_lo = np.percentile(finite_ors, 2.5)
    or_ci_hi = np.percentile(finite_ors, 97.5)
    ax.axvline(np.log10(max(or_ci_lo, 0.01)), color="#27ae60", linestyle=":", linewidth=1.5)
    ax.axvline(np.log10(max(or_ci_hi, 0.01)), color="#27ae60", linestyle=":", linewidth=1.5,
               label=f"95% CI [{or_ci_lo:.1f}, {or_ci_hi:.1f}]")

    n_inf = np.sum(np.isinf(bootstrap_ors))
    frac_gt1 = np.mean(bootstrap_ors > 1) * 100
    frac_sig = np.mean(
        np.array([1 for o in bootstrap_ors]) *  # placeholder; we pass ps separately
        1  # filled later
    )

    ax.set_xlabel("log$_{10}$(Odds Ratio)", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)

    # Custom x-tick labels showing actual OR values
    tick_positions = [np.log10(x) for x in [0.1, 1, 5, 10, 50, 100]]
    tick_labels = ["0.1", "1", "5", "10", "50", "100"]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    n_inf_pct = n_inf / len(bootstrap_ors) * 100
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title(f"Bootstrap OR distribution\n"
                 f"({frac_gt1:.0f}% > 1; {n_inf_pct:.0f}% = inf)",
                 fontsize=11)

    fig.suptitle("Robustness experiments: Q-based discordance prediction\n"
                 "(38 Phase III AD/MS trials, 23 with Q-based predictions)",
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    return fig


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    q_data = load_q_data(Q_RESULTS_PATH)
    holdout_df = pd.read_csv(EXPANDED_PATH)

    print("=" * 72)
    print("ROBUSTNESS EXPERIMENTS: Q-BASED DISCORDANCE PREDICTION")
    print(f"Generated: {datetime.now().isoformat()}")
    print("=" * 72)

    known = holdout_df[holdout_df["fda_outcome"].isin(["Approved", "Failed"])]
    print(f"\nDataset: {len(known)} drugs with known outcomes")

    # ── Experiment 1 ──
    threshold_results = run_threshold_sensitivity(q_data, holdout_df)

    # ── Experiment 2 ──
    lofo_results, lofo_summary = run_lofo_cv(q_data, holdout_df)

    # ── Experiment 3 ──
    bootstrap_result, bootstrap_ors, bootstrap_accs, bootstrap_ps = run_bootstrap_ci(
        q_data, holdout_df
    )

    # ── Summary ──
    print("\n" + "=" * 72)
    print("OVERALL ROBUSTNESS SUMMARY")
    print("=" * 72)

    # Threshold stability
    sig_thresholds = [r for r in threshold_results if r["p_fisher"] < 0.05]
    high_acc_thresholds = [r for r in threshold_results if r["accuracy"] >= 0.80]
    print(f"\n  Threshold sensitivity:")
    print(f"    Significant (p < 0.05) at {len(sig_thresholds)}/{len(threshold_results)} thresholds")
    print(f"    Accuracy >= 80% at {len(high_acc_thresholds)}/{len(threshold_results)} thresholds")
    acc_range = (min(r["accuracy"] for r in threshold_results),
                 max(r["accuracy"] for r in threshold_results))
    print(f"    Accuracy range: {acc_range[0]:.1%} - {acc_range[1]:.1%}")

    print(f"\n  Leave-one-family-out CV:")
    print(f"    Mean accuracy: {lofo_summary['mean_accuracy']:.1%}")
    print(f"    Range: {lofo_summary['min_accuracy']:.1%} - {lofo_summary['max_accuracy']:.1%}")

    print(f"\n  Bootstrap (n={N_BOOTSTRAP}):")
    print(f"    OR 95% CI: [{bootstrap_result['or_ci_95'][0]:.1f}, "
          f"{bootstrap_result['or_ci_95'][1]:.1f}]")
    print(f"    Accuracy 95% CI: [{bootstrap_result['accuracy_ci_95'][0]:.1%}, "
          f"{bootstrap_result['accuracy_ci_95'][1]:.1%}]")
    print(f"    OR > 1 in {bootstrap_result['frac_or_gt1']:.1%} of samples")
    print(f"    p < 0.05 in {bootstrap_result['frac_p_lt_05']:.1%} of samples")

    # ── Plots ──
    fig = make_plots(threshold_results, lofo_results, bootstrap_ors, bootstrap_accs)
    plot_path = os.path.join(OUTPUT_DIR, "robustness_plots.png")
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved: {plot_path}")

    # ── Save JSON ──
    output = {
        "generated": datetime.now().isoformat(),
        "method": "Robustness experiments for Q-based discordance prediction",
        "dataset": EXPANDED_PATH,
        "experiment_1_threshold_sensitivity": {
            "thresholds_tested": THRESHOLDS,
            "results": threshold_results,
            "n_significant": len(sig_thresholds),
            "accuracy_range": list(acc_range),
        },
        "experiment_2_lofo_cv": {
            "n_folds": lofo_summary["n_folds"],
            "summary": lofo_summary,
            "per_fold": lofo_results,
        },
        "experiment_3_bootstrap": bootstrap_result,
    }

    json_path = os.path.join(OUTPUT_DIR, "robustness_results.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
