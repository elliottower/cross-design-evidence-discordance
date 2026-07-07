"""Permutation test on invariance depth -- tier correlation for neuroepidemiology.

Computes an exact empirical p-value via 10,000 permutations of the tier
labels for the Kendall tau between best_tier and invariance depth (delta)
across mechanism families.

Adapted from psychiatric-validity-audit/analysis/geometric_causal/permutation_test.py

Usage:
    cd /Users/elliottower/Documents/GitHub/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with matplotlib --with numpy \
        python analysis/geometric_causal/permutation_test.py
"""

import json
import os

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

CSV_PATH = "data/effect_sizes_v12.csv"
N_PERMUTATIONS = 10_000
SEED = 42

TIER_MAP = {
    "Proposed": 1,
    "Causally Suggestive": 2,
    "Triangulated": 3,
    "Mechanistically Supported": 4,
    "Validated": 5,
    "Underdetermined": np.nan,
    "Disconfirmed": 0,
}

DESIGN_FAMILY_MAP = {
    "genetic/cohort": "GEN",
    "genetic": "GEN",
    "MR": "GEN",
    "observational": "OBS",
    "RCT": "RCT",
    "diagnostic": "DX",
}


def design_to_evidence_type(design):
    if design in DESIGN_FAMILY_MAP:
        return DESIGN_FAMILY_MAP[design]
    d = design.lower()
    if any(kw in d for kw in ["gwas", "genetic", "mendelian", "mr"]):
        return "GEN"
    if any(kw in d for kw in ["pet", "fmri", "mri", "imaging"]):
        return "IMAGING"
    if any(kw in d for kw in ["rct", "placebo", "trial"]):
        return "RCT"
    if any(kw in d for kw in ["meta", "mega", "systematic"]):
        return "META"
    if any(kw in d for kw in ["cohort", "observational", "longitudinal"]):
        return "OBS"
    if "diagnostic" in d or "biomarker" in d:
        return "DX"
    return "OTHER"


df = pd.read_csv(CSV_PATH)
df["tier_num"] = df["best_tier"].map(TIER_MAP)


def compute_depth_table(df):
    results = []
    for fam_name in sorted(df["family"].dropna().unique()):
        members = df[df["family"] == fam_name]
        if len(members) == 0:
            continue

        type_counts = {}
        for _, row in members.iterrows():
            ef = design_to_evidence_type(str(row["design"]).strip())
            type_counts[ef] = type_counts.get(ef, 0) + 1

        delta = 0.0
        for fam, count in type_counts.items():
            for k in range(1, count + 1):
                delta += 1.0 / k

        tier_vals = members["best_tier"].map(TIER_MAP).dropna()
        tier_vals = tier_vals[tier_vals > 0]
        best_tier = tier_vals.max() if len(tier_vals) > 0 else np.nan

        results.append({
            "family": fam_name,
            "delta": delta,
            "best_tier": best_tier,
        })

    return pd.DataFrame(results)


depth_df = compute_depth_table(df)
valid = depth_df[depth_df["best_tier"].notna()].copy()

print(f"Mechanism families with valid tier: {len(valid)}")
print(f"\n{'Family':25s}  {'best_tier':>10s}  {'delta':>8s}")
print("-" * 50)
for _, row in valid.iterrows():
    print(f"  {row['family']:25s}  {row['best_tier']:10.1f}  {row['delta']:8.2f}")

observed_tau, parametric_p = kendalltau(valid["best_tier"], valid["delta"])
print(f"\nObserved Kendall tau = {observed_tau:+.4f}")
print(f"Parametric p-value  = {parametric_p:.4f}")
print(f"n = {len(valid)}")

rng = np.random.default_rng(SEED)
tiers = valid["best_tier"].values.copy()
deltas = valid["delta"].values.copy()

null_taus = np.empty(N_PERMUTATIONS)
for i in range(N_PERMUTATIONS):
    perm_tiers = rng.permutation(tiers)
    null_taus[i], _ = kendalltau(perm_tiers, deltas)

empirical_p_twosided = np.mean(np.abs(null_taus) >= np.abs(observed_tau))
empirical_p_onesided = np.mean(null_taus >= observed_tau)

print(f"\nPermutation test ({N_PERMUTATIONS:,d} permutations):")
print(f"  Empirical p (two-sided, |tau| >= |observed|): {empirical_p_twosided:.4f}")
print(f"  Empirical p (one-sided, tau >= observed):     {empirical_p_onesided:.4f}")
print(f"  Null tau mean:  {null_taus.mean():+.4f}")
print(f"  Null tau std:   {null_taus.std():.4f}")
print(f"  Null tau range: [{null_taus.min():+.4f}, {null_taus.max():+.4f}]")
print(f"  Observed tau z-score: {(observed_tau - null_taus.mean()) / null_taus.std():.2f}")

os.makedirs("output", exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(null_taus, bins=50, color="#718096", alpha=0.7, edgecolor="white",
        label=f"Null distribution (n={N_PERMUTATIONS:,d})")
ax.axvline(observed_tau, color="#c53030", ls="--", lw=2.5,
           label=f"Observed tau = {observed_tau:+.3f}")
ax.axvline(-observed_tau, color="#c53030", ls=":", lw=1.5, alpha=0.5,
           label=f"-Observed tau = {-observed_tau:+.3f}")

x_reject = null_taus[np.abs(null_taus) >= np.abs(observed_tau)]
if len(x_reject) > 0:
    ax.hist(x_reject, bins=50, color="#c53030", alpha=0.3, edgecolor="white",
            label=f"p = {empirical_p_twosided:.4f} (two-sided)")

ax.set_xlabel("Kendall tau (permuted)", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title(
    f"Permutation Test: Invariance Depth vs Best Tier\n"
    f"Neuroepidemiology audit (n={len(valid)} families, {N_PERMUTATIONS:,d} permutations)\n"
    f"Observed tau = {observed_tau:+.3f}, empirical p = {empirical_p_twosided:.4f} (two-sided)",
    fontsize=11,
)
ax.legend(fontsize=9, loc="upper left")
plt.tight_layout()

fig_path = "output/permutation_null_distribution.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
print(f"\nSaved {fig_path}")

results = {
    "domain": "neuroepidemiology (MS / AD)",
    "observed_tau": float(observed_tau),
    "parametric_p": float(parametric_p),
    "empirical_p_twosided": float(empirical_p_twosided),
    "empirical_p_onesided": float(empirical_p_onesided),
    "n_families": int(len(valid)),
    "n_permutations": N_PERMUTATIONS,
    "null_mean": float(null_taus.mean()),
    "null_std": float(null_taus.std()),
    "null_range": [float(null_taus.min()), float(null_taus.max())],
    "z_score": float((observed_tau - null_taus.mean()) / null_taus.std()),
    "families": [
        {"family": row["family"], "best_tier": float(row["best_tier"]), "delta": float(row["delta"])}
        for _, row in valid.iterrows()
    ],
}

json_path = "output/permutation_test_results.json"
with open(json_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"Saved {json_path}")
