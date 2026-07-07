"""Tier calibration analysis: Kendall tau between validity tier and effect magnitude.

Runs on the risk-ratio cluster (OR/RR/HR) only — never pools across incompatible scales.
"""
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

import sys
csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/effect_sizes_v2.csv"
df = pd.read_csv(csv_path)

tier_map = {"T1": 1, "T1-T2": 1.5, "T2": 2, "T2-T3": 2.5, "T3": 3, "T3-T4": 3.5, "T4": 4}
df["tier_num"] = df["best_tier"].map(tier_map)

risk_scales = {"odds ratio", "risk ratio", "hazard ratio", "hazard/rate ratio", "rate ratio", "relative risk"}
risk = df[df.scale.isin(risk_scales) & df.estimate.notna()].copy()
risk["log_mag"] = np.abs(np.log(risk["estimate"]))

tau, p = kendalltau(risk["tier_num"], risk["log_mag"])
n = len(risk)
print(f"Risk-OR cluster: n={n}  Kendall tau={tau:.3f}  p={p:.4f}")
print(f"Spec target was n>=30 -> {'ACHIEVED' if n >= 30 else 'NOT YET'} n={n} (DESCRIPTIVE)")

risk_sorted = risk.sort_values("estimate")
fig, ax = plt.subplots(figsize=(9, max(7, 0.4 * len(risk_sorted))))
y = np.arange(len(risk_sorted))
has_ci = risk_sorted["ci_low"].notna() & risk_sorted["ci_high"].notna()
if has_ci.any():
    ci_rows = risk_sorted[has_ci]
    ci_y = y[has_ci.values]
    ax.hlines(ci_y, ci_rows["ci_low"], ci_rows["ci_high"],
              color="#2b6cb0", alpha=0.4, linewidth=2, zorder=2)
ax.scatter(risk_sorted["estimate"], y, s=60, color="#2b6cb0", zorder=3)
ax.axvline(1.0, color="grey", ls="--", lw=1)
ax.set_xscale("log")
ax.set_yticks(y)
ax.set_yticklabels(
    risk_sorted["case_id"] + "  " + risk_sorted["claim"].str.slice(0, 34),
    fontsize=8,
)
n_ci = has_ci.sum()
ax.set_xlabel("Effect estimate (log scale, ratio)")
ax.set_title(
    f"Cross-domain risk-ratio forest (n={n}, {n_ci} with CIs)\n"
    f"Kendall tau(tier, |log effect|) = {tau:.2f}, p = {p:.3f} — DESCRIPTIVE",
    fontsize=10,
)
for xi, yi, t in zip(risk_sorted["estimate"], y, risk_sorted["best_tier"]):
    ax.annotate(t, (xi, yi), textcoords="offset points", xytext=(6, 4), fontsize=7, color="#555")
plt.tight_layout()
import re as _re
_ver = _re.search(r'v(\d+)', csv_path)
out_name = f"output/risk_forest_v{_ver.group(1)}.png" if _ver else "output/risk_forest.png"
plt.savefig(out_name, dpi=150, bbox_inches="tight")
print(f"Saved {out_name}")
