"""Meta-regression with tier x stratum interaction for neuroepidemiology.

Implements:
1. Effect magnitude computation (|log(est)| for ratio scales, |d| for SMD)
2. Three regressions: simple, additive, full interaction (OLS + WLS)
3. Split Kendall tau by stratum (etiologic vs therapeutic)
4. External ground truth analysis with invariance depth and partial correlations
5. 2x2 panel figure

Adapted from psychiatric-validity-audit/analysis/geometric_causal/meta_regression.py

Usage:
    cd /Users/elliottower/Documents/GitHub/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with statsmodels --with numpy --with matplotlib \
        python analysis/geometric_causal/meta_regression.py
"""

import json
import os

import matplotlib
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import kendalltau

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import statsmodels.api as sm

# ────────────────────────────────────────────────────────────────────
# LOAD DATA
# ────────────────────────────────────────────────────────────────────

df = pd.read_csv("data/effect_sizes_v12.csv")
ext = pd.read_csv("data/external_ground_truth.csv")

tier_map = {
    "Disconfirmed": 0,
    "Proposed": 1,
    "Causally Suggestive": 2,
    "Triangulated": 3,
    "Mechanistically Supported": 4,
}
df["tier_num"] = df["best_tier"].map(tier_map)
ext["tier_num"] = ext["best_tier"].map(tier_map)

# ────────────────────────────────────────────────────────────────────
# EFFECT MAGNITUDE COMPUTATION
# ────────────────────────────────────────────────────────────────────

ratio_scales = {"odds ratio", "risk ratio", "hazard ratio", "rate ratio",
                "relative risk", "incidence rate ratio", "hazard/rate ratio"}
d_scales = {"effect size", "mean diff"}


def compute_effect_mag(row):
    scale = str(row["scale"]).lower().strip() if pd.notna(row["scale"]) else ""
    est = row["estimate"]
    if pd.isna(est):
        return np.nan

    if any(kw in scale for kw in ["odds ratio", "risk ratio", "hazard ratio",
                                    "rate ratio", "relative risk", "incidence rate ratio"]):
        if est <= 0:
            return np.nan
        return abs(np.log(est))

    if any(kw in scale for kw in ["cohen d", "hedges g", "smd", "effect size", "mean diff"]):
        return abs(est)

    if "correlation" in scale:
        return abs(est)

    return np.nan


df["effect_mag"] = df.apply(compute_effect_mag, axis=1)

# ────────────────────────────────────────────────────────────────────
# STRATUM CLASSIFICATION
# ────────────────────────────────────────────────────────────────────

therapeutic_keywords = [
    "ocrelizumab", "natalizumab", "cladribine", "fingolimod",
    "dimethyl fumarate", "simvastatin", "biotin", "md1003",
    "lecanemab", "solanezumab", "semaglutide", "ginkgo",
    "hrt", "hormone", "aducanumab", "verubecestat", "semagacestat",
    "tolebrutinib", "vit-d suppl", "vitamin d suppl",
    "treatment", "therapy", "therapeutic", "drug", "intervention",
    "relapse", "progression benefit", "disability",
    "cdp", "arr", "cdr-sb", "slowing",
]


def classify_stratum(row):
    claim = str(row["claim"]).lower()
    design = str(row["design"]).lower()
    if "rct" in design:
        return "therapeutic"
    for kw in therapeutic_keywords:
        if kw.lower() in claim:
            return "therapeutic"
    return "etiologic"


df["stratum"] = df.apply(classify_stratum, axis=1)
df["is_therapeutic"] = (df["stratum"] == "therapeutic").astype(float)

# Compute n_total for WLS weights
for col in ("n_cases", "n_controls"):
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
df["n_total"] = df.get("n_cases", pd.Series(dtype=float)).fillna(0) + \
                df.get("n_controls", pd.Series(dtype=float)).fillna(0)
df.loc[df["n_total"] == 0, "n_total"] = np.nan

reg_df = df[df.effect_mag.notna() & df.tier_num.notna()].copy()

print("=" * 70)
print("META-REGRESSION: NEUROEPIDEMIOLOGY AUDIT (MS / AD)")
print(f"Dataset: data/effect_sizes_v12.csv  |  n_total={len(df)}, n_regression={len(reg_df)}")
print(f"  Etiologic: {(reg_df.stratum == 'etiologic').sum()}, "
      f"Therapeutic: {(reg_df.stratum == 'therapeutic').sum()}")
print(f"Generated: {datetime.now().isoformat()}")
print("=" * 70)

print("\nTier x Stratum crosstab:")
ct = pd.crosstab(reg_df["best_tier"], reg_df["stratum"])
print(ct.to_string())
print(f"\nEffect magnitude summary:")
print(reg_df.groupby(["best_tier", "stratum"])["effect_mag"].describe()[["count", "mean", "std", "min", "max"]].to_string())

# ────────────────────────────────────────────────────────────────────
# 1. META-REGRESSION: THREE MODELS
# ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("1. META-REGRESSION MODELS")
print("=" * 70)

y = reg_df["effect_mag"].values

X_a = sm.add_constant(reg_df[["tier_num"]])
ols_a = sm.OLS(y, X_a).fit()
print(f"\n--- Model (a): effect_mag ~ tier_num ---")
print(ols_a.summary2().tables[1].to_string())
print(f"R² = {ols_a.rsquared:.4f}, Adj-R² = {ols_a.rsquared_adj:.4f}, "
      f"F = {ols_a.fvalue:.3f}, p(F) = {ols_a.f_pvalue:.6f}")

X_b = sm.add_constant(reg_df[["tier_num", "is_therapeutic"]])
ols_b = sm.OLS(y, X_b).fit()
print(f"\n--- Model (b): effect_mag ~ tier_num + is_therapeutic ---")
print(ols_b.summary2().tables[1].to_string())
print(f"R² = {ols_b.rsquared:.4f}, Adj-R² = {ols_b.rsquared_adj:.4f}, "
      f"F = {ols_b.fvalue:.3f}, p(F) = {ols_b.f_pvalue:.6f}")

X_c = reg_df[["tier_num", "is_therapeutic"]].copy()
X_c["tier_x_ther"] = X_c["tier_num"] * X_c["is_therapeutic"]
X_c = sm.add_constant(X_c)
ols_c = sm.OLS(y, X_c).fit()
print(f"\n--- Model (c): effect_mag ~ tier_num * is_therapeutic ---")
print(ols_c.summary2().tables[1].to_string())
print(f"R² = {ols_c.rsquared:.4f}, Adj-R² = {ols_c.rsquared_adj:.4f}, "
      f"F = {ols_c.fvalue:.3f}, p(F) = {ols_c.f_pvalue:.6f}")

# WLS: weight = n_total if available, else 1
w = reg_df["n_total"].fillna(1).values.astype(float)
w = np.maximum(w, 1)

wls_a = sm.WLS(y, X_a, weights=w).fit()
wls_b = sm.WLS(y, X_b, weights=w).fit()
wls_c = sm.WLS(y, X_c, weights=w).fit()

print(f"\n--- WLS Model (a): R² = {wls_a.rsquared:.4f} ---")
print(wls_a.summary2().tables[1].to_string())

print(f"\n--- WLS Model (b): R² = {wls_b.rsquared:.4f} ---")
print(wls_b.summary2().tables[1].to_string())

print(f"\n--- WLS Model (c): R² = {wls_c.rsquared:.4f} ---")
print(wls_c.summary2().tables[1].to_string())
print(f"WLS interaction p = {wls_c.pvalues['tier_x_ther']:.6f}")

# ────────────────────────────────────────────────────────────────────
# 2. SPLIT KENDALL TAU
# ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("2. SPLIT KENDALL TAU")
print("=" * 70)

tau_all, p_all = kendalltau(reg_df["tier_num"], reg_df["effect_mag"])
print(f"\nCOMBINED:     n={len(reg_df):3d}  tau={tau_all:+.4f}  p={p_all:.6f}")

etio = reg_df[reg_df.stratum == "etiologic"]
ther = reg_df[reg_df.stratum == "therapeutic"]

tau_e, p_e = kendalltau(etio["tier_num"], etio["effect_mag"]) if len(etio) >= 4 else (np.nan, np.nan)
tau_t, p_t = kendalltau(ther["tier_num"], ther["effect_mag"]) if len(ther) >= 4 else (np.nan, np.nan)

print(f"ETIOLOGIC:    n={len(etio):3d}  tau={tau_e:+.4f}  p={p_e:.6f}")
print(f"THERAPEUTIC:  n={len(ther):3d}  tau={tau_t:+.4f}  p={p_t:.6f}")

print(f"\nEtiologic tier distribution: {dict(etio['best_tier'].value_counts().sort_index())}")
print(f"Therapeutic tier distribution: {dict(ther['best_tier'].value_counts().sort_index())}")
print(f"Etiologic median effect_mag: {etio['effect_mag'].median():.4f}")
print(f"Therapeutic median effect_mag: {ther['effect_mag'].median():.4f}")

# ────────────────────────────────────────────────────────────────────
# 3. EXTERNAL GROUND TRUTH + INVARIANCE DEPTH
# ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("3. EXTERNAL GROUND TRUTH + INVARIANCE DEPTH")
print("=" * 70)

ext_valid = ext[ext.tier_num.notna() & ext.external_score.notna()].copy()

tau_ext, p_ext = kendalltau(ext_valid["tier_num"], ext_valid["external_score"])
print(f"\ntau(tier, external_score) = {tau_ext:+.4f}, p = {p_ext:.6f}, n = {len(ext_valid)}")

# Invariance depth per family
def design_to_evidence_type(design):
    d = str(design).lower()
    if d in ("mr", "genetic", "genetic/cohort"):
        return "GEN"
    if "rct" in d:
        return "RCT"
    if any(kw in d for kw in ["pet", "fmri", "mri", "imaging"]):
        return "IMAGING"
    if any(kw in d for kw in ["meta", "mega"]):
        return "META"
    if any(kw in d for kw in ["observational", "longitudinal", "cohort"]):
        return "OBS"
    if "diagnostic" in d:
        return "DX"
    return "OTHER"


family_groups = {}
for _, row in df.iterrows():
    fam = row["family"]
    if pd.isna(fam):
        continue
    if fam not in family_groups:
        family_groups[fam] = []
    family_groups[fam].append({"case_id": row["case_id"], "design": str(row["design"]).strip()})

family_deltas = {}
for fam, members in family_groups.items():
    type_counts = {}
    for m in members:
        etype = design_to_evidence_type(m["design"])
        type_counts[etype] = type_counts.get(etype, 0) + 1

    delta = 0.0
    for etype, count in type_counts.items():
        for k in range(1, count + 1):
            delta += 1.0 / k
    family_deltas[fam] = delta

df["inv_depth"] = df["family"].map(family_deltas)

ext_valid = ext_valid.merge(
    df[["case_id", "inv_depth"]].drop_duplicates("case_id"),
    on="case_id",
    how="left",
)
ext_depth = ext_valid[ext_valid.inv_depth.notna()].copy()

print(f"\nInvariance depth per family:")
for fam in sorted(family_deltas, key=lambda x: family_deltas[x], reverse=True):
    print(f"  {fam:20s}  delta = {family_deltas[fam]:.2f}")

tau_depth, p_depth = kendalltau(ext_depth["tier_num"], ext_depth["inv_depth"])
print(f"\ntau(tier, inv_depth) = {tau_depth:+.4f}, p = {p_depth:.6f}, n = {len(ext_depth)}")

# Partial correlations
if len(ext_depth) >= 6:
    tier_vals = ext_depth["tier_num"].values
    ext_score_vals = ext_depth["external_score"].values
    depth_vals = ext_depth["inv_depth"].values

    res_tier_on_depth = sm.OLS(tier_vals, sm.add_constant(depth_vals)).fit().resid
    res_ext_on_depth = sm.OLS(ext_score_vals, sm.add_constant(depth_vals)).fit().resid
    tau_partial_ext, p_partial_ext = kendalltau(res_tier_on_depth, res_ext_on_depth)

    res_tier_on_ext = sm.OLS(tier_vals, sm.add_constant(ext_score_vals)).fit().resid
    res_depth_on_ext = sm.OLS(depth_vals, sm.add_constant(ext_score_vals)).fit().resid
    tau_partial_depth, p_partial_depth = kendalltau(res_tier_on_ext, res_depth_on_ext)

    print(f"\nPartial tau(tier, external_score | inv_depth) = {tau_partial_ext:+.4f}, p = {p_partial_ext:.6f}")
    print(f"Partial tau(tier, inv_depth | external_score) = {tau_partial_depth:+.4f}, p = {p_partial_depth:.6f}")

    X_combined = sm.add_constant(ext_depth[["external_score", "inv_depth"]])
    ols_combined = sm.OLS(tier_vals, X_combined).fit()
    print(f"\nCombined OLS: tier ~ external_score + inv_depth")
    print(ols_combined.summary2().tables[1].to_string())
    print(f"R² = {ols_combined.rsquared:.4f}, Adj-R² = {ols_combined.rsquared_adj:.4f}")
else:
    tau_partial_ext = np.nan
    p_partial_ext = np.nan
    tau_partial_depth = np.nan
    p_partial_depth = np.nan
    ols_combined = None
    print("\nToo few rows for partial correlation analysis.")

# ────────────────────────────────────────────────────────────────────
# 4. FIGURE: 2x2 PANEL
# ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("4. GENERATING FIGURE")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# (a) Top-left: scatter of effect_mag vs tier with regression lines
ax = axes[0, 0]
colors = {"etiologic": "#2b6cb0", "therapeutic": "#c53030"}
for stratum_name in ["etiologic", "therapeutic"]:
    sub = reg_df[reg_df.stratum == stratum_name]
    jitter = np.random.default_rng(42).uniform(-0.08, 0.08, len(sub))
    ax.scatter(sub["tier_num"] + jitter, sub["effect_mag"], s=45, alpha=0.6,
               color=colors[stratum_name], label=stratum_name, zorder=3)
    if len(sub) >= 2:
        z = np.polyfit(sub["tier_num"], sub["effect_mag"], 1)
        xline = np.linspace(sub["tier_num"].min(), sub["tier_num"].max(), 50)
        ax.plot(xline, np.polyval(z, xline), "--", color=colors[stratum_name],
                alpha=0.7, lw=2, zorder=2)

interaction_p_str = (f"p={ols_c.pvalues['tier_x_ther']:.4f}"
                     if "tier_x_ther" in ols_c.pvalues else "N/A")
ax.set_xlabel("Validity tier (ordinal)")
ax.set_ylabel("Effect magnitude")
ax.set_title(f"(a) Meta-regression: effect ~ tier x stratum\n"
             f"OLS R²={ols_c.rsquared:.3f}, interaction {interaction_p_str}")

# Build tick labels from tiers actually present
present_tiers = sorted(reg_df["tier_num"].unique())
tier_label_map = {0: "Disc.", 1: "Prop.", 2: "Caus.\nSugg.", 3: "Triang.", 4: "Mech.\nSupp."}
ax.set_xticks(present_tiers)
ax.set_xticklabels([tier_label_map.get(t, str(t)) for t in present_tiers], fontsize=8)
ax.legend(fontsize=9, loc="upper left")

# (b) Top-right: split Kendall tau bar chart
ax = axes[0, 1]
tau_labels = ["Combined", "Etiologic", "Therapeutic"]
tau_values = [tau_all, tau_e, tau_t]
p_values = [p_all, p_e, p_t]
bar_colors = ["#718096", "#2b6cb0", "#c53030"]
bars = ax.bar(tau_labels, tau_values, color=bar_colors, alpha=0.75, edgecolor="black", linewidth=0.8)
for bar, tv, pv in zip(bars, tau_values, p_values):
    sig = "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else "n.s."
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
            f"tau={tv:+.3f}\n{sig}", ha="center", va="bottom", fontsize=8)
ax.set_ylabel("Kendall tau")
ax.set_title("(b) Split Kendall tau: tier vs effect magnitude")
ax.axhline(0, color="grey", lw=0.8, ls="--")

# (c) Bottom-left: external_score vs tier boxplot
ax = axes[1, 0]
if len(ext_valid) > 0:
    tier_groups = ext_valid.groupby("tier_num")["external_score"].apply(list)
    positions = sorted(tier_groups.index)
    data_for_box = [tier_groups[pos] for pos in positions]
    tick_labels = []
    for pos in positions:
        name = tier_label_map.get(int(pos), str(pos))
        tick_labels.append(name)
    bp = ax.boxplot(data_for_box, positions=positions, widths=0.5, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("#cbd5e0")
        patch.set_alpha(0.7)
    rng = np.random.default_rng(17)
    for pos, vals in zip(positions, data_for_box):
        jitter = rng.uniform(-0.12, 0.12, len(vals))
        ax.scatter([pos + j for j in jitter], vals, s=30, color="#2b6cb0", alpha=0.5, zorder=3)
    ax.set_xticks(positions)
    ax.set_xticklabels(tick_labels, fontsize=8)
    ax.set_xlabel("Validity tier")
    ax.set_ylabel("External score")
    ax.set_title(f"(c) External ground truth vs tier\n"
                 f"tau={tau_ext:+.3f}, p={p_ext:.4f}")

# (d) Bottom-right: invariance_depth vs tier scatter
ax = axes[1, 1]
if len(ext_depth) > 0:
    jitter = np.random.default_rng(99).uniform(-0.08, 0.08, len(ext_depth))
    ax.scatter(ext_depth["tier_num"] + jitter, ext_depth["inv_depth"],
               s=50, color="#2b6cb0", alpha=0.6, zorder=3)
    for _, row in ext_depth.iterrows():
        ax.annotate(row["case_id"], (row["tier_num"], row["inv_depth"]),
                    fontsize=5, alpha=0.6, xytext=(3, 3), textcoords="offset points")
    if len(ext_depth) >= 2:
        z = np.polyfit(ext_depth["tier_num"], ext_depth["inv_depth"], 1)
        xline = np.linspace(ext_depth["tier_num"].min(), ext_depth["tier_num"].max(), 50)
        ax.plot(xline, np.polyval(z, xline), "--", color="#2b6cb0", alpha=0.5, lw=2)
    ax.set_xlabel("Validity tier")
    ax.set_ylabel("Invariance depth (delta)")
    present_ext = sorted(ext_depth["tier_num"].unique())
    ax.set_xticks(present_ext)
    ax.set_xticklabels([tier_label_map.get(int(t), str(t)) for t in present_ext], fontsize=8)
    ax.set_title(f"(d) Invariance depth vs tier\n"
                 f"tau={tau_depth:+.3f}, p={p_depth:.4f}")

plt.suptitle("Neuroepidemiology Audit: Meta-Regression Panel", fontsize=14, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])

os.makedirs("output", exist_ok=True)
fig_path = "output/meta_regression_panel.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
print(f"Saved {fig_path}")

# ────────────────────────────────────────────────────────────────────
# 5. SAVE RESULTS JSON
# ────────────────────────────────────────────────────────────────────

results = {
    "domain": "neuroepidemiology (MS / AD)",
    "generated": datetime.now().isoformat(),
    "n_total_rows": len(df),
    "n_regression_rows": len(reg_df),
    "n_etiologic": int((reg_df.stratum == "etiologic").sum()),
    "n_therapeutic": int((reg_df.stratum == "therapeutic").sum()),
    "ols_models": {
        "simple": {
            "R2": float(ols_a.rsquared),
            "adj_R2": float(ols_a.rsquared_adj),
            "F": float(ols_a.fvalue),
            "p_F": float(ols_a.f_pvalue),
            "tier_coef": float(ols_a.params["tier_num"]),
            "tier_p": float(ols_a.pvalues["tier_num"]),
        },
        "additive": {
            "R2": float(ols_b.rsquared),
            "adj_R2": float(ols_b.rsquared_adj),
            "F": float(ols_b.fvalue),
            "p_F": float(ols_b.f_pvalue),
            "tier_coef": float(ols_b.params["tier_num"]),
            "tier_p": float(ols_b.pvalues["tier_num"]),
            "ther_coef": float(ols_b.params["is_therapeutic"]),
            "ther_p": float(ols_b.pvalues["is_therapeutic"]),
        },
        "interaction": {
            "R2": float(ols_c.rsquared),
            "adj_R2": float(ols_c.rsquared_adj),
            "F": float(ols_c.fvalue),
            "p_F": float(ols_c.f_pvalue),
            "tier_coef": float(ols_c.params["tier_num"]),
            "tier_p": float(ols_c.pvalues["tier_num"]),
            "ther_coef": float(ols_c.params["is_therapeutic"]),
            "ther_p": float(ols_c.pvalues["is_therapeutic"]),
            "interaction_coef": float(ols_c.params["tier_x_ther"]),
            "interaction_p": float(ols_c.pvalues["tier_x_ther"]),
        },
    },
    "wls_models": {
        "simple": {"R2": float(wls_a.rsquared)},
        "additive": {"R2": float(wls_b.rsquared)},
        "interaction": {
            "R2": float(wls_c.rsquared),
            "interaction_coef": float(wls_c.params["tier_x_ther"]),
            "interaction_p": float(wls_c.pvalues["tier_x_ther"]),
        },
    },
    "kendall_tau": {
        "combined": {"tau": float(tau_all), "p": float(p_all), "n": len(reg_df)},
        "etiologic": {"tau": float(tau_e), "p": float(p_e), "n": len(etio)},
        "therapeutic": {"tau": float(tau_t), "p": float(p_t), "n": len(ther)},
    },
    "external_ground_truth": {
        "tau_ext_score": float(tau_ext),
        "p_ext_score": float(p_ext),
        "n_ext": len(ext_valid),
        "tau_inv_depth": float(tau_depth),
        "p_inv_depth": float(p_depth),
        "n_depth": len(ext_depth),
        "partial_tau_ext_given_depth": float(tau_partial_ext),
        "partial_p_ext_given_depth": float(p_partial_ext),
        "partial_tau_depth_given_ext": float(tau_partial_depth),
        "partial_p_depth_given_ext": float(p_partial_depth),
    },
    "invariance_depth_by_family": {
        fam: float(delta) for fam, delta in sorted(family_deltas.items(), key=lambda x: -x[1])
    },
}

if ols_combined is not None:
    results["external_ground_truth"]["combined_ols"] = {
        "R2": float(ols_combined.rsquared),
        "adj_R2": float(ols_combined.rsquared_adj),
        "ext_score_coef": float(ols_combined.params["external_score"]),
        "ext_score_p": float(ols_combined.pvalues["external_score"]),
        "inv_depth_coef": float(ols_combined.params["inv_depth"]),
        "inv_depth_p": float(ols_combined.pvalues["inv_depth"]),
    }

json_path = "output/meta_regression_results.json"
with open(json_path, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"Saved {json_path}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"OLS interaction model R² = {ols_c.rsquared:.4f}, interaction p = {ols_c.pvalues.get('tier_x_ther', float('nan')):.4f}")
print(f"WLS interaction model R² = {wls_c.rsquared:.4f}, interaction p = {wls_c.pvalues.get('tier_x_ther', float('nan')):.4f}")
print(f"Kendall tau (combined) = {tau_all:+.4f} (p={p_all:.4f})")
print(f"Kendall tau (etiologic) = {tau_e:+.4f} (p={p_e:.4f})")
print(f"Kendall tau (therapeutic) = {tau_t:+.4f} (p={p_t:.4f})")
print(f"External score tau = {tau_ext:+.4f}")
print(f"Invariance depth tau = {tau_depth:+.4f}")
