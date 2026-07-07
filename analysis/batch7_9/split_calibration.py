"""Split calibration: etiologic vs therapeutic strata.

Hypothesis: Kendall tau(tier, |log effect|) is significant within each
stratum but washes out when pooled, because etiologic claims (risk factors,
genetic associations) and therapeutic claims (RCT DMTs) occupy different
magnitude regimes on the same axis.

Etiologic: observational, MR, genetic — "does X cause Y?"
Therapeutic: RCT — "does treatment reduce Y?"

Reports tau, p, n for: combined, etiologic-only, therapeutic-only.
Produces split forest plot with strata colored differently.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/effect_sizes_v8.csv"
df = pd.read_csv(csv_path)

tier_map = {"T1": 1, "T1-T2": 1.5, "T2": 2, "T2-T3": 2.5, "T3": 3, "T3-T4": 3.5, "T4": 4}
df["tier_num"] = df["best_tier"].map(tier_map)

ratio_scales = {"odds ratio", "risk ratio", "hazard ratio", "hazard/rate ratio", "rate ratio", "relative risk"}
risk = df[df.scale.isin(ratio_scales) & df.estimate.notna() & df.tier_num.notna()].copy()
risk["log_mag"] = np.abs(np.log(risk["estimate"]))

risk["stratum"] = np.where(risk["design"] == "RCT", "therapeutic", "etiologic")

print("=" * 60)
print("SPLIT CALIBRATION: etiologic vs therapeutic")
print("=" * 60)

tau_all, p_all = kendalltau(risk["tier_num"], risk["log_mag"])
print(f"\nCOMBINED:     n={len(risk):3d}  tau={tau_all:+.3f}  p={p_all:.4f}")

for stratum in ["etiologic", "therapeutic"]:
    sub = risk[risk.stratum == stratum]
    if len(sub) < 4:
        print(f"{stratum.upper():14s}: n={len(sub):3d}  TOO FEW for tau")
        continue
    tau, p = kendalltau(sub["tier_num"], sub["log_mag"])
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"{stratum.upper():14s}: n={len(sub):3d}  tau={tau:+.3f}  p={p:.4f} {sig}")

    tiers = sorted(sub["tier_num"].unique())
    print(f"  Tier distribution: {dict(sub['tier_num'].value_counts().sort_index())}")
    print(f"  Median |log(est)|: {sub['log_mag'].median():.3f}  (median est={np.exp(sub['log_mag'].median()):.2f}x)")

print(f"\nTier distribution by stratum:")
ct = pd.crosstab(risk["stratum"], risk["best_tier"])
print(ct.to_string())

colors = {"etiologic": "#2b6cb0", "therapeutic": "#c53030"}
markers = {"etiologic": "o", "therapeutic": "s"}

risk_sorted = risk.sort_values(["stratum", "estimate"], ascending=[True, True])
fig, ax = plt.subplots(figsize=(10, max(8, 0.4 * len(risk_sorted))))
y = np.arange(len(risk_sorted))

for stratum in ["etiologic", "therapeutic"]:
    mask = risk_sorted["stratum"] == stratum
    sub = risk_sorted[mask]
    sub_y = y[mask.values]
    c = colors[stratum]

    has_ci = sub["ci_low"].notna() & sub["ci_high"].notna()
    if has_ci.any():
        ci_rows = sub[has_ci]
        ci_y = sub_y[has_ci.values]
        ax.hlines(ci_y, ci_rows["ci_low"], ci_rows["ci_high"],
                  color=c, alpha=0.35, linewidth=2, zorder=2)
    ax.scatter(sub["estimate"], sub_y, s=60, color=c, marker=markers[stratum],
               zorder=3, label=stratum)

ax.axvline(1.0, color="grey", ls="--", lw=1)
ax.set_xscale("log")
ax.set_yticks(y)
ax.set_yticklabels(
    risk_sorted["case_id"] + "  " + risk_sorted["claim"].str.slice(0, 34),
    fontsize=7,
)

for xi, yi, t, s in zip(risk_sorted["estimate"], y, risk_sorted["best_tier"], risk_sorted["stratum"]):
    ax.annotate(t, (xi, yi), textcoords="offset points", xytext=(6, 4),
                fontsize=6, color=colors[s], alpha=0.7)

etio = risk[risk.stratum == "etiologic"]
ther = risk[risk.stratum == "therapeutic"]
tau_e, p_e = kendalltau(etio["tier_num"], etio["log_mag"]) if len(etio) >= 4 else (float("nan"), float("nan"))
tau_t, p_t = kendalltau(ther["tier_num"], ther["log_mag"]) if len(ther) >= 4 else (float("nan"), float("nan"))

n_ci = (risk_sorted.ci_low.notna() & risk_sorted.ci_high.notna()).sum()
ax.set_xlabel("Effect estimate (log scale, ratio)")
ax.set_title(
    f"Split calibration forest (n={len(risk)}, {n_ci} with CIs)\n"
    f"Etiologic: tau={tau_e:+.2f}, p={p_e:.3f} (n={len(etio)})  |  "
    f"Therapeutic: tau={tau_t:+.2f}, p={p_t:.3f} (n={len(ther)})\n"
    f"Combined: tau={tau_all:+.2f}, p={p_all:.3f}",
    fontsize=9,
)
ax.legend(loc="lower right", fontsize=9)
plt.tight_layout()

import re
ver = re.search(r'v(\d+)', csv_path)
out_name = f"output/split_calibration_v{ver.group(1)}.png" if ver else "output/split_calibration.png"
plt.savefig(out_name, dpi=150, bbox_inches="tight")
print(f"\nSaved {out_name}")

fig2, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax2, (stratum, sub) in zip(axes, risk.groupby("stratum")):
    tiers = sub["tier_num"]
    mags = sub["log_mag"]
    tau, p = kendalltau(tiers, mags)
    ax2.scatter(tiers, mags, s=50, color=colors[stratum], alpha=0.7)
    for _, r in sub.iterrows():
        ax2.annotate(r["case_id"], (r["tier_num"], r["log_mag"]),
                     fontsize=5, alpha=0.6, xytext=(3, 3), textcoords="offset points")
    z = np.polyfit(tiers, mags, 1)
    xline = np.linspace(tiers.min(), tiers.max(), 50)
    ax2.plot(xline, np.polyval(z, xline), "--", color=colors[stratum], alpha=0.5)
    ax2.set_xlabel("Validity tier (numeric)")
    ax2.set_ylabel("|log(effect estimate)|")
    ax2.set_title(f"{stratum.capitalize()} (n={len(sub)})\ntau={tau:+.3f}, p={p:.4f}")
    ax2.set_xticks([1, 1.5, 2, 2.5, 3, 3.5, 4])
    ax2.set_xticklabels(["T1", "", "T2", "", "T3", "", "T4"], fontsize=8)
plt.tight_layout()
scatter_name = out_name.replace("split_calibration", "split_scatter")
plt.savefig(scatter_name, dpi=150, bbox_inches="tight")
print(f"Saved {scatter_name}")
