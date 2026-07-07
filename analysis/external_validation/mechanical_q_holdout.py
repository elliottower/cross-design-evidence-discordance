"""Mechanical Q-based discordance prediction for Phase III holdout.

Replaces hand-labeled discordance_edge annotations with purely mechanical
Q-based classification. For each holdout drug, looks up its mechanism
family's Cochran Q classification (TRANSPORT vs NON-TRANSPORT) from the
H1 transportability analysis, then predicts trial outcome.

Two prediction rules tested:
  BASIC:
    TRANSPORT → predict Approve
    NON-TRANSPORT → predict Fail
  REFINED (qualitative vs quantitative discordance):
    TRANSPORT → predict Approve
    NON-TRANSPORT + qualitative (one evidence type null) → predict Fail
    NON-TRANSPORT + quantitative (both types positive) → predict Approve

Drugs whose family is not in Q analysis get no prediction (reported separately).

Usage:
    cd /path/to/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with numpy --with matplotlib \
        python analysis/external_validation/mechanical_q_holdout.py
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

Q_RESULTS_PATH = "output/h1_transportability_results.json"
HOLDOUT_PATH = "data/phase3_holdout_dataset.csv"
OUTPUT_DIR = "output/external_validation"
BETA_THRESHOLD = 0.10


def load_q_classifications(q_path):
    with open(q_path) as f:
        q_data = json.load(f)

    classifications = {}
    for fam_name, fam_data in q_data["per_family"].items():
        cls = fam_data["classification"]

        discordance_type = "concordant"
        if cls == "NON-TRANSPORT":
            type_details = fam_data.get("type_details", {})
            betas = [v["beta"] for v in type_details.values()]
            if all(abs(b) >= BETA_THRESHOLD for b in betas):
                discordance_type = "quantitative"
            else:
                discordance_type = "qualitative"

        classifications[fam_name] = {
            "classification": cls,
            "discordance_type": discordance_type,
            "Q": fam_data["Q"],
            "p": fam_data["p"],
            "evidence_types": fam_data["evidence_types"],
            "type_betas": {k: v["beta"] for k, v in fam_data.get("type_details", {}).items()},
        }

    return classifications, q_data["summary"]


def predict_basic(cls_info):
    if cls_info is None:
        return None
    return "Approve" if cls_info["classification"] == "TRANSPORT" else "Fail"


def predict_refined(cls_info):
    if cls_info is None:
        return None
    if cls_info["classification"] == "TRANSPORT":
        return "Approve"
    if cls_info["discordance_type"] == "quantitative":
        return "Approve"
    return "Fail"


def compute_metrics(actual, predicted):
    tp = sum(1 for a, p in zip(actual, predicted) if a == "Failed" and p == "Fail")
    fp = sum(1 for a, p in zip(actual, predicted) if a == "Approved" and p == "Fail")
    tn = sum(1 for a, p in zip(actual, predicted) if a == "Approved" and p == "Approve")
    fn = sum(1 for a, p in zip(actual, predicted) if a == "Failed" and p == "Approve")

    accuracy = (tp + tn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) > 0 else 0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0

    table = np.array([[tp, fp], [fn, tn]])
    odds_ratio, p_fisher = fisher_exact(table, alternative="two-sided")

    return {
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "accuracy": accuracy,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "ppv": ppv,
        "npv": npv,
        "odds_ratio": float(odds_ratio),
        "p_fisher": float(p_fisher),
        "n": tp + fp + tn + fn,
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    classifications, q_summary = load_q_classifications(Q_RESULTS_PATH)
    holdout = pd.read_csv(HOLDOUT_PATH)

    print("=" * 72)
    print("MECHANICAL Q-BASED DISCORDANCE PREDICTION")
    print(f"Generated: {datetime.now().isoformat()}")
    print("=" * 72)

    print(f"\nQ classifications loaded ({len(classifications)} families):")
    for fam, info in sorted(classifications.items()):
        betas_str = ", ".join(f"{k}={v:.3f}" for k, v in info["type_betas"].items())
        print(f"  {fam:20s}  {info['classification']:15s}  {info['discordance_type']:13s}  "
              f"Q={info['Q']:.1f}  [{betas_str}]")

    print(f"\nHoldout drugs: {len(holdout)}")
    known = holdout[holdout["fda_outcome"].isin(["Approved", "Failed"])].copy()
    print(f"  With known outcomes: {len(known)}")

    # Map each drug to its family's Q classification
    results = []
    for _, row in known.iterrows():
        family = row["family"]
        cls_info = classifications.get(family)

        pred_basic = predict_basic(cls_info)
        pred_refined = predict_refined(cls_info)

        results.append({
            "drug": row["drug_name"],
            "indication": row["indication"],
            "family": family,
            "actual": row["fda_outcome"],
            "q_classification": cls_info["classification"] if cls_info else "NOT_IN_Q",
            "discordance_type": cls_info["discordance_type"] if cls_info else "n/a",
            "pred_basic": pred_basic,
            "pred_refined": pred_refined,
            "Q": cls_info["Q"] if cls_info else None,
            "evidence_types": cls_info["evidence_types"] if cls_info else None,
            "hand_label": row.get("discordance_edge", ""),
        })

    results_df = pd.DataFrame(results)

    # Separate predictable vs unpredictable
    predictable = results_df[results_df["pred_basic"].notna()]
    unpredictable = results_df[results_df["pred_basic"].isna()]

    print(f"\n  Drugs with Q-based prediction: {len(predictable)}")
    print(f"  Drugs without Q data (no prediction): {len(unpredictable)}")

    if len(unpredictable) > 0:
        print(f"\n  Unpredictable drugs (family not in Q analysis):")
        for _, row in unpredictable.iterrows():
            print(f"    {row['drug']:25s}  family={row['family']:15s}  actual={row['actual']}")

    # Basic prediction results
    print("\n" + "=" * 72)
    print("BASIC PREDICTION: TRANSPORT→Approve, NON-TRANSPORT→Fail")
    print("=" * 72)

    actual_basic = predictable["actual"].tolist()
    pred_basic = predictable["pred_basic"].tolist()
    m_basic = compute_metrics(actual_basic, pred_basic)

    print(f"\n  2x2 table (failure prediction):")
    print(f"                    Predicted Fail  Predicted Approve")
    print(f"  Actually Failed:  {m_basic['tp']:14d}  {m_basic['fn']:17d}")
    print(f"  Actually Approved:{m_basic['fp']:14d}  {m_basic['tn']:17d}")
    print(f"\n  Accuracy:    {m_basic['accuracy']:.1%}")
    print(f"  Sensitivity: {m_basic['sensitivity']:.1%} (P(predict Fail | actually Failed))")
    print(f"  Specificity: {m_basic['specificity']:.1%} (P(predict Approve | actually Approved))")
    print(f"  PPV:         {m_basic['ppv']:.1%} (P(actually Failed | predict Fail))")
    print(f"  NPV:         {m_basic['npv']:.1%} (P(actually Approved | predict Approve))")
    print(f"  Fisher exact: OR={m_basic['odds_ratio']:.2f}, p={m_basic['p_fisher']:.4f}")

    print(f"\n  Per-drug detail:")
    for _, row in predictable.iterrows():
        correct = "OK" if (row["actual"] == "Failed") == (row["pred_basic"] == "Fail") else "MISS"
        print(f"    {row['drug']:25s}  {row['actual']:8s}  pred={row['pred_basic']:7s}  "
              f"family={row['family']:15s}  [{correct}]")

    # Refined prediction results
    print("\n" + "=" * 72)
    print("REFINED PREDICTION: qualitative discordance→Fail, quantitative→Approve")
    print("=" * 72)

    actual_refined = predictable["actual"].tolist()
    pred_refined = predictable["pred_refined"].tolist()
    m_refined = compute_metrics(actual_refined, pred_refined)

    print(f"\n  2x2 table (failure prediction):")
    print(f"                    Predicted Fail  Predicted Approve")
    print(f"  Actually Failed:  {m_refined['tp']:14d}  {m_refined['fn']:17d}")
    print(f"  Actually Approved:{m_refined['fp']:14d}  {m_refined['tn']:17d}")
    print(f"\n  Accuracy:    {m_refined['accuracy']:.1%}")
    print(f"  Sensitivity: {m_refined['sensitivity']:.1%}")
    print(f"  Specificity: {m_refined['specificity']:.1%}")
    print(f"  PPV:         {m_refined['ppv']:.1%}")
    print(f"  NPV:         {m_refined['npv']:.1%}")
    print(f"  Fisher exact: OR={m_refined['odds_ratio']:.2f}, p={m_refined['p_fisher']:.4f}")

    print(f"\n  Per-drug detail:")
    for _, row in predictable.iterrows():
        correct = "OK" if (row["actual"] == "Failed") == (row["pred_refined"] == "Fail") else "MISS"
        print(f"    {row['drug']:25s}  {row['actual']:8s}  pred={row['pred_refined']:7s}  "
              f"type={row['discordance_type']:13s}  [{correct}]")

    # Failure rate by classification
    print("\n" + "=" * 72)
    print("FAILURE RATE BY Q CLASSIFICATION")
    print("=" * 72)
    for cls_type in ["TRANSPORT", "NON-TRANSPORT", "NOT_IN_Q"]:
        subset = results_df[results_df["q_classification"] == cls_type]
        if len(subset) == 0:
            continue
        n_fail = (subset["actual"] == "Failed").sum()
        n_total = len(subset)
        rate = n_fail / n_total
        print(f"  {cls_type:15s}: {n_fail}/{n_total} failed ({rate:.1%})")

    for disc_type in ["qualitative", "quantitative"]:
        subset = results_df[results_df["discordance_type"] == disc_type]
        if len(subset) == 0:
            continue
        n_fail = (subset["actual"] == "Failed").sum()
        n_total = len(subset)
        rate = n_fail / n_total
        print(f"  {disc_type:15s}: {n_fail}/{n_total} failed ({rate:.1%})")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, (label, metrics) in zip(axes, [("Basic", m_basic), ("Refined", m_refined)]):
        table = np.array([[metrics["tp"], metrics["fn"]], [metrics["fp"], metrics["tn"]]])
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
        ax.set_title(f"{label} Prediction\n"
                     f"Acc={metrics['accuracy']:.0%}  Sens={metrics['sensitivity']:.0%}  "
                     f"Spec={metrics['specificity']:.0%}\n"
                     f"Fisher p={metrics['p_fisher']:.4f}",
                     fontsize=11)

    fig.suptitle("Mechanical Q-Based Discordance Prediction\n"
                 "Phase III Drug Outcomes (Neuroepidemiology)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()

    fig_path = os.path.join(OUTPUT_DIR, "mechanical_q_prediction.png")
    plt.savefig(fig_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {fig_path}")

    # Save JSON
    output = {
        "generated": datetime.now().isoformat(),
        "method": "Mechanical Q-based discordance prediction",
        "q_results_path": Q_RESULTS_PATH,
        "holdout_path": HOLDOUT_PATH,
        "beta_threshold": BETA_THRESHOLD,
        "n_holdout": len(known),
        "n_predictable": len(predictable),
        "n_unpredictable": len(unpredictable),
        "family_classifications": classifications,
        "basic_prediction": m_basic,
        "refined_prediction": m_refined,
        "per_drug": results,
    }

    json_path = os.path.join(OUTPUT_DIR, "mechanical_q_prediction.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
