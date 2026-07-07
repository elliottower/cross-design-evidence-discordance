"""Geometric causal validation of the Mechanistic Validity framework.

Implements four analyses from the unification paper (tower2026unified)
applied to the neuroepidemiology evidence base:

1. Meta-regression: log|effect| ~ tier * stratum (formal interaction test)
2. Leave-one-out jackknife: robustness of tau to influential observations
3. Frechet variance realism test (Proposition 3.3): within-family convergence
   vs null baseline — T(C) << 1 licenses realism
4. Invariance depth (triangulation) with harmonic discounting

Usage:
    uv run --with pandas --with scipy --with statsmodels --with matplotlib \
        analysis/geometric_causal/geometric_validation.py data/effect_sizes_v10.csv
"""
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import statsmodels.api as sm
from datetime import datetime

csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/effect_sizes_v10.csv"
df = pd.read_csv(csv_path)

tier_map = {"T1": 1, "T1-T2": 1.5, "T2": 2, "T2-T3": 2.5, "T3": 3, "T3-T4": 3.5, "T4": 4}
df["tier_num"] = df["best_tier"].map(tier_map)

ratio_scales = {
    "odds ratio", "risk ratio", "hazard ratio",
    "hazard/rate ratio", "rate ratio", "relative risk",
}
risk = df[df.scale.isin(ratio_scales) & df.estimate.notna() & df.tier_num.notna()].copy()
risk["log_effect"] = np.log(risk["estimate"])
risk["log_mag"] = np.abs(risk["log_effect"])
risk["stratum"] = np.where(risk["design"] == "RCT", "therapeutic", "etiologic")
risk["is_therapeutic"] = (risk["stratum"] == "therapeutic").astype(float)
risk["has_ci"] = risk["ci_low"].notna() & risk["ci_high"].notna()

print("=" * 70)
print("GEOMETRIC CAUSAL VALIDATION")
print(f"Dataset: {csv_path}  |  n={len(risk)} ratio-scale rows")
print(f"Generated: {datetime.now().isoformat()}")
print("=" * 70)

# ────────────────────────────────────────────────────────────────────
# 1. META-REGRESSION: |log(effect)| ~ tier * stratum
# ────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("1. META-REGRESSION: |log(effect)| ~ tier × stratum")
print("─" * 70)

X = risk[["tier_num", "is_therapeutic"]].copy()
X["tier_x_ther"] = X["tier_num"] * X["is_therapeutic"]
X = sm.add_constant(X)
y = risk["log_mag"]

ols = sm.OLS(y, X).fit()
print(ols.summary2().tables[1].to_string())
print(f"\nR² = {ols.rsquared:.3f},  Adj-R² = {ols.rsquared_adj:.3f}")
print(f"F-stat = {ols.fvalue:.2f},  p(F) = {ols.f_pvalue:.6f}")

ci_mask = risk["has_ci"].values
if ci_mask.sum() >= 10:
    se_log = np.zeros(len(risk))
    se_log[ci_mask] = (
        (np.log(risk.loc[ci_mask.astype(bool) if isinstance(ci_mask, np.ndarray) else ci_mask, "ci_high"].values)
         - np.log(risk.loc[ci_mask.astype(bool) if isinstance(ci_mask, np.ndarray) else ci_mask, "ci_low"].values))
        / (2 * 1.96)
    )
    w = np.where(se_log > 0, 1.0 / se_log**2, 0)
    if w.sum() > 0:
        wls = sm.WLS(y[w > 0], X[w > 0], weights=w[w > 0]).fit()
        print(f"\nWLS (inverse-variance weighted, n={int((w>0).sum())} with CIs):")
        print(wls.summary2().tables[1].to_string())
        print(f"R² = {wls.rsquared:.3f}")

# ────────────────────────────────────────────────────────────────────
# 2. LEAVE-ONE-OUT JACKKNIFE
# ────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("2. LEAVE-ONE-OUT JACKKNIFE: tau stability")
print("─" * 70)

taus_combined, taus_etio, taus_ther = [], [], []
dropped_ids = []

for i in risk.index:
    sub = risk.drop(i)
    tau_c, _ = kendalltau(sub["tier_num"], sub["log_mag"])
    taus_combined.append(tau_c)
    dropped_ids.append(risk.loc[i, "case_id"])

    etio = sub[sub.stratum == "etiologic"]
    ther = sub[sub.stratum == "therapeutic"]
    tau_e, _ = kendalltau(etio["tier_num"], etio["log_mag"]) if len(etio) >= 4 else (np.nan, np.nan)
    tau_t, _ = kendalltau(ther["tier_num"], ther["log_mag"]) if len(ther) >= 4 else (np.nan, np.nan)
    taus_etio.append(tau_e)
    taus_ther.append(tau_t)

taus_combined = np.array(taus_combined)
taus_etio = np.array(taus_etio)
taus_ther = np.array(taus_ther)

full_tau, full_p = kendalltau(risk["tier_num"], risk["log_mag"])
print(f"Full dataset:      tau = {full_tau:+.4f}")
print(f"Jackknife range:   [{taus_combined.min():+.4f}, {taus_combined.max():+.4f}]")
print(f"Jackknife mean:    {taus_combined.mean():+.4f} ± {taus_combined.std():.4f}")

most_influential = np.argmin(taus_combined)
least_influential = np.argmax(taus_combined)
print(f"\nMost  influential: drop {dropped_ids[most_influential]:12s} → tau = {taus_combined[most_influential]:+.4f}"
      f"  (Δ = {taus_combined[most_influential] - full_tau:+.4f})")
print(f"Least influential: drop {dropped_ids[least_influential]:12s} → tau = {taus_combined[least_influential]:+.4f}"
      f"  (Δ = {taus_combined[least_influential] - full_tau:+.4f})")

print(f"\nEtiologic  jackknife: [{np.nanmin(taus_etio):+.4f}, {np.nanmax(taus_etio):+.4f}]")
print(f"Therapeutic jackknife: [{np.nanmin(taus_ther):+.4f}, {np.nanmax(taus_ther):+.4f}]")

sig_threshold = 0.05
all_sig = True
for i, (tid, tc) in enumerate(zip(dropped_ids, taus_combined)):
    _, p_i = kendalltau(risk.drop(risk.index[i])["tier_num"],
                         risk.drop(risk.index[i])["log_mag"])
    if p_i >= sig_threshold:
        print(f"  WARNING: dropping {tid} makes combined p={p_i:.4f} (non-sig)")
        all_sig = False
if all_sig:
    print(f"\n  ALL leave-one-out p-values remain < {sig_threshold} — robust.")

# ────────────────────────────────────────────────────────────────────
# 3. FRECHET VARIANCE REALISM TEST (Proposition 3.3)
# ────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("3. FRECHET VARIANCE REALISM TEST")
print("─" * 70)

CLAIM_FAMILIES = {
    "vitD_MS": {
        "label": "Vitamin D → MS",
        "members": [
            ("MS-007", -1),      # MR: low-D → MS risk. Flip: high-D protective
            ("MS-007b", +1),     # RCT: supp → disease activity HR=0.66
            ("MS-007c", +1),     # RCT meta: supp OR=0.66
            ("MS-007d", +1),     # RCT null: HR=1.17
            ("MS-030", +1),      # RCT null: OR=0.98
        ],
        "evidence_types": {
            "MS-007": "MR", "MS-007b": "RCT", "MS-007c": "RCT",
            "MS-007d": "RCT", "MS-030": "RCT",
        },
    },
    "APOE4_AD": {
        "label": "APOE4 → AD",
        "members": [
            ("AD-002a", +1),     # het OR=3.46
            ("AD-002b", +1),     # hom OR=23.5
            ("AD-002c", +1),     # women OR=13.5
        ],
        "evidence_types": {
            "AD-002a": "genetic", "AD-002b": "genetic", "AD-002c": "genetic",
        },
    },
    "social_dementia": {
        "label": "Social isolation → dementia",
        "members": [
            ("AD-005n", +1),     # loneliness HR=1.31
            ("AD-005n2", +1),    # loneliness→AD HR=1.39
            ("AD-005o", +1),     # low social contact RR=1.57
            ("AD-005o2", +1),    # poor network RR=1.59
        ],
        "evidence_types": {
            "AD-005n": "observational", "AD-005n2": "observational",
            "AD-005o": "observational", "AD-005o2": "observational",
        },
    },
    "ocrelizumab_MS": {
        "label": "Ocrelizumab → MS progression",
        "members": [
            ("MS-011", +1),      # PPMS HR=0.70
            ("MS-031", +1),      # OPERA RRMS HR=0.60
            ("MS-032b", +1),     # ORATORIO PPMS HR=0.76
        ],
        "evidence_types": {
            "MS-011": "RCT", "MS-031": "RCT", "MS-032b": "RCT",
        },
    },
    "failed_AD_RCT": {
        "label": "Failed AD therapeutics (null cluster)",
        "members": [
            ("AD-032", +1),      # solanezumab A4 HR=1.08
            ("AD-033", +1),      # solanezumab EXPEDITION3 RR=0.95
            ("AD-034", +1),      # semaglutide HR=1.0
            ("AD-035", +1),      # semagacestat RR=1.10
            ("AD-036", +1),      # aducanumab ENGAGE RR=1.02
            ("AD-037", +1),      # verubecestat HR=1.05
        ],
        "evidence_types": {
            "AD-032": "RCT", "AD-033": "RCT", "AD-034": "RCT",
            "AD-035": "RCT", "AD-036": "RCT", "AD-037": "RCT",
        },
    },
    "amyloid_conversion": {
        "label": "Amyloid-PET+ → AD conversion",
        "members": [
            ("AD-001", +1),      # HR=3.74
            ("AD-001b", +1),     # HR=10.2
            ("AD-009c", +1),     # p-tau217 HR=7.81 (related biomarker)
        ],
        "evidence_types": {
            "AD-001": "observational", "AD-001b": "observational",
            "AD-009c": "biomarker",
        },
    },
}

sigma2_null = risk["log_mag"].var()
print(f"Null variance (σ²_null = marginal Var of |log(effect)|): {sigma2_null:.4f}")
print(f"Null σ: {np.sqrt(sigma2_null):.4f}\n")

frechet_results = []
for fam_id, fam in CLAIM_FAMILIES.items():
    ids = [m[0] for m in fam["members"]]
    dirs = {m[0]: m[1] for m in fam["members"]}

    fam_rows = risk[risk.case_id.isin(ids)].copy()
    if len(fam_rows) < 2:
        print(f"  {fam['label']:40s}  SKIP (n={len(fam_rows)} < 2)")
        continue

    aligned_log = []
    for _, row in fam_rows.iterrows():
        d = dirs.get(row["case_id"], +1)
        if d == -1:
            aligned_log.append(-row["log_effect"])
        else:
            aligned_log.append(row["log_effect"])
    aligned_log = np.array(aligned_log)

    frechet_mean = aligned_log.mean()
    var_f = np.mean((aligned_log - frechet_mean) ** 2)
    T_stat = var_f / sigma2_null if sigma2_null > 0 else np.inf

    n_types = len(set(fam["evidence_types"].values()))
    F = len(aligned_log)

    # concentration bound (1D version of Prop 3.3c)
    if sigma2_null > 0 and var_f < sigma2_null:
        p_convergence = (var_f / sigma2_null) ** ((F - 1) / 2)
    else:
        p_convergence = 1.0

    realism = "REALISM" if T_stat < 0.25 else ("PARTIAL" if T_stat < 0.5 else "FRAGMENTED")

    print(f"  {fam['label']:40s}  F={F}  types={n_types}  "
          f"Var_F={var_f:.4f}  T={T_stat:.4f}  p_conv={p_convergence:.4f}  → {realism}")
    for _, row in fam_rows.iterrows():
        d = dirs.get(row["case_id"], +1)
        val = -row["log_effect"] if d == -1 else row["log_effect"]
        ci_str = f"({row['ci_low']:.2f}-{row['ci_high']:.2f})" if row["has_ci"] else "(no CI)"
        print(f"    {row['case_id']:12s}  est={row['estimate']:.2f} {ci_str}  "
              f"log={val:+.3f}  type={fam['evidence_types'].get(row['case_id'], '?')}")

    frechet_results.append({
        "family": fam_id, "label": fam["label"], "F": F,
        "n_evidence_types": n_types, "Var_F": var_f, "T_stat": T_stat,
        "p_convergence": p_convergence, "verdict": realism,
        "frechet_mean_exp": np.exp(frechet_mean),
    })

# ────────────────────────────────────────────────────────────────────
# 4. INVARIANCE DEPTH (Triangulation with harmonic discounting)
# ────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("4. INVARIANCE DEPTH (δ) — Triangulation scoring")
print("─" * 70)

EVIDENCE_FAMILY_MAP = {
    "observational": "OBS",
    "genetic": "GEN",
    "genetic/cohort": "GEN",
    "MR": "MR",
    "RCT": "RCT",
    "diagnostic": "DX",
}

CLAIM_GROUPS = {
    "EBV_MS":       ["MS-001", "MS-018b"],
    "HLA_MS":       ["MS-017", "MS-018a"],
    "vitD_MS":      ["MS-007", "MS-007b", "MS-007c", "MS-007d", "MS-030"],
    "BMI_MS":       ["MS-013a", "MS-013b"],
    "sNfL_MS":      ["MS-005a", "MS-005b", "MS-005c"],
    "OCB_MS":       ["MS-006a", "MS-006b"],
    "DMT_MS":       ["MS-028", "MS-029", "MS-031", "MS-032b", "MS-011",
                     "MS-033", "MS-033b", "MS-034", "MS-035", "MS-036"],
    "APOE_AD":      ["AD-002a", "AD-002b", "AD-002c"],
    "amyloid_AD":   ["AD-001", "AD-001b", "AD-009c"],
    "T2D_AD":       ["AD-005b", "AD-005l"],
    "social_AD":    ["AD-005n", "AD-005n2", "AD-005o", "AD-005o2"],
    "obesity_AD":   ["AD-005h", "AD-005h2"],
    "failed_AD":    ["AD-030", "AD-032", "AD-033", "AD-034", "AD-035",
                     "AD-036", "AD-037"],
    "WHIMS":        ["AD-031", "AD-031b"],
    "TBI_AD":       ["AD-005m", "AD-005m2"],
    "smoking_MS":   ["MS-021"],
    "IL6_AD":       ["AD-004"],
    "iron_MS":      ["MS-002"],
}

print(f"\n{'Claim group':20s}  {'δ':>6s}  {'n':>3s}  {'families':>8s}  evidence types")
print("-" * 80)

depth_results = []
for group_id, member_ids in CLAIM_GROUPS.items():
    members = df[df.case_id.isin(member_ids)]
    if len(members) == 0:
        continue

    families_seen = {}
    for _, row in members.iterrows():
        fam = EVIDENCE_FAMILY_MAP.get(row["design"], "OTHER")
        if fam not in families_seen:
            families_seen[fam] = 0
        families_seen[fam] += 1

    delta = 0.0
    for fam, count in families_seen.items():
        for k in range(1, count + 1):
            delta += 1.0 / k

    best_tier = members["best_tier"].map(tier_map).max()
    family_str = ", ".join(f"{f}({c})" for f, c in sorted(families_seen.items()))

    print(f"  {group_id:20s}  {delta:6.2f}  {len(members):3d}  {len(families_seen):>8d}  {family_str}")
    depth_results.append({
        "group": group_id, "delta": delta, "n_members": len(members),
        "n_families": len(families_seen), "best_tier": best_tier,
    })

depth_df = pd.DataFrame(depth_results)
if len(depth_df) >= 4:
    tau_depth, p_depth = kendalltau(depth_df["best_tier"], depth_df["delta"])
    print(f"\nKendall tau(best_tier, δ) = {tau_depth:+.3f}, p = {p_depth:.4f}")
    print(f"Realism threshold δ ≥ 3 (independent families): "
          f"{(depth_df['delta'] >= 3).sum()}/{len(depth_df)} groups pass")

# ────────────────────────────────────────────────────────────────────
# 5. TRANSPORT OBSTRUCTION CLASSIFICATION (Proposition 3.4)
# ────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("5. TRANSPORT OBSTRUCTION — Failure mode classification")
print("─" * 70)

OBSTRUCTIONS = [
    {
        "claim": "Vitamin D → MS",
        "mode": "Evidence misfire",
        "cocycle": "c_τ < 0 (tier drops under transport)",
        "evidence": "MR: OR=2.0, T3 (causal) → RCT: HR=0.98-1.17, T1-T2 (null)",
        "interpretation": "Etiologic causation confirmed; therapeutic translation fails. "
                          "The identity (vitamin D ↔ MS) is preserved but the tier collapses "
                          "under design transport MR→RCT.",
        "rows": ["MS-007", "MS-007d", "MS-030"],
    },
    {
        "claim": "Anti-tau CSF engagement",
        "mode": "Mimic mechanism",
        "cocycle": "c_id non-trivial, c_τ = 0",
        "evidence": "99% CSF target engagement but 0% clinical benefit",
        "interpretation": "The measured quantity (CSF tau) retains its tier (good measurement) "
                          "but the identity referent rotates: pharmacological engagement ≠ "
                          "disease-modifying mechanism. Same name, different fiber element.",
        "rows": ["AD-C2"],
    },
    {
        "claim": "APOE4 → AD across ancestries",
        "mode": "Reference debt",
        "cocycle": "π₀(N(G')) ≠ * (nerve not path-connected)",
        "evidence": "White OR=3.46, East Asian OR=4.54, Black OR=2.18, Hispanic OR=1.90",
        "interpretation": "The claim 'APOE4 causes AD' cannot be transported across ancestry "
                          "contexts without specifying which population. The transport category "
                          "has disconnected components — no single global section exists.",
        "rows": ["AD-002a"],
    },
    {
        "claim": "Smoking → MS",
        "mode": "Evidence misfire (confound exposure)",
        "cocycle": "c_τ < 0",
        "evidence": "Observational: positive association → MR IVW: OR=1.03 (0.89-1.19) null",
        "interpretation": "Observational T3 collapses to MR T1. The causal claim does not "
                          "survive instrument-variable transport. Confound signature: obs "
                          "positive, MR null.",
        "rows": ["MS-021"],
    },
    {
        "claim": "Fingolimod relapse vs progression",
        "mode": "Mimic mechanism (outcome-dependent)",
        "cocycle": "c_id non-trivial under outcome transport",
        "evidence": "ARR rate ratio 0.52 (T3) vs CDP HR 0.83 null (T1-T2)",
        "interpretation": "Same drug, same trial, but transporting from relapse→progression "
                          "endpoint rotates the identity. The 'fingolimod mechanism' that "
                          "reduces relapses is not the mechanism needed to slow progression.",
        "rows": ["MS-033", "MS-033b"],
    },
    {
        "claim": "TBI → dementia vs TBI → AD",
        "mode": "Mimic mechanism (outcome-specificity)",
        "cocycle": "c_id non-trivial under outcome refinement",
        "evidence": "TBI→dementia OR=1.81 (1.53-2.14) vs TBI→AD specifically OR=1.02 null",
        "interpretation": "Transporting from broad (dementia) to narrow (AD) outcome rotates "
                          "the identity. TBI causes vascular/mixed dementia, not Alzheimer's.",
        "rows": ["AD-005m"],
    },
]

for obs in OBSTRUCTIONS:
    print(f"\n  [{obs['mode'].upper()}] {obs['claim']}")
    print(f"  Cocycle: {obs['cocycle']}")
    print(f"  Evidence: {obs['evidence']}")
    print(f"  → {obs['interpretation']}")

# ────────────────────────────────────────────────────────────────────
# SUMMARY FIGURE
# ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# (a) Meta-regression scatter
ax = axes[0, 0]
colors = {"etiologic": "#2b6cb0", "therapeutic": "#c53030"}
for stratum in ["etiologic", "therapeutic"]:
    sub = risk[risk.stratum == stratum]
    ax.scatter(sub["tier_num"], sub["log_mag"], s=40, alpha=0.6,
               color=colors[stratum], label=stratum)
    z = np.polyfit(sub["tier_num"], sub["log_mag"], 1)
    xline = np.linspace(sub["tier_num"].min(), sub["tier_num"].max(), 50)
    ax.plot(xline, np.polyval(z, xline), "--", color=colors[stratum], alpha=0.5, lw=2)
ax.set_xlabel("Validity tier")
ax.set_ylabel("|log(effect)|")
ax.set_title(f"(a) Meta-regression\nR²={ols.rsquared:.3f}, interaction p={ols.pvalues['tier_x_ther']:.4f}")
ax.set_xticks([1, 1.5, 2, 2.5, 3, 3.5, 4])
ax.set_xticklabels(["T1", "", "T2", "", "T3", "", "T4"], fontsize=8)
ax.legend(fontsize=8)

# (b) Jackknife stability
ax = axes[0, 1]
sort_idx = np.argsort(taus_combined)
ax.barh(range(len(taus_combined)), taus_combined[sort_idx], color="#718096", alpha=0.6, height=0.8)
ax.axvline(full_tau, color="#c53030", ls="--", lw=2, label=f"Full tau={full_tau:.3f}")
ax.set_xlabel("Kendall tau (combined)")
ax.set_ylabel("Leave-one-out index")
ax.set_title(f"(b) Jackknife stability\nrange [{taus_combined.min():.3f}, {taus_combined.max():.3f}]")
ax.legend(fontsize=8)
ax.set_yticks([])

# (c) Frechet variance
ax = axes[1, 0]
if frechet_results:
    fr_df = pd.DataFrame(frechet_results)
    y_pos = range(len(fr_df))
    bar_colors = ["#38a169" if r["verdict"] == "REALISM" else
                  "#d69e2e" if r["verdict"] == "PARTIAL" else "#e53e3e"
                  for r in frechet_results]
    ax.barh(list(y_pos), fr_df["T_stat"], color=bar_colors, alpha=0.7)
    ax.axvline(0.25, color="#38a169", ls=":", lw=1.5, label="Realism threshold")
    ax.axvline(0.50, color="#d69e2e", ls=":", lw=1.5, label="Partial threshold")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(fr_df["label"], fontsize=8)
    ax.set_xlabel("T(C) = Var_F / σ²_null")
    ax.set_title("(c) Frechet variance realism test\nT << 1 = convergence beyond chance")
    ax.legend(fontsize=7, loc="lower right")

# (d) Invariance depth vs tier
ax = axes[1, 1]
if len(depth_df) >= 4:
    ax.scatter(depth_df["best_tier"], depth_df["delta"], s=60, color="#2b6cb0", alpha=0.7)
    for _, row in depth_df.iterrows():
        ax.annotate(row["group"], (row["best_tier"], row["delta"]),
                     fontsize=5, alpha=0.7, xytext=(3, 3), textcoords="offset points")
    ax.axhline(3.0, color="#38a169", ls=":", lw=1.5, label="δ ≥ 3 (realism)")
    ax.set_xlabel("Best tier (numeric)")
    ax.set_ylabel("Invariance depth δ")
    ax.set_title(f"(d) Triangulation depth\ntau(tier, δ) = {tau_depth:+.3f}, p = {p_depth:.4f}")
    ax.set_xticks([1, 1.5, 2, 2.5, 3, 3.5, 4])
    ax.set_xticklabels(["T1", "", "T2", "", "T3", "", "T4"], fontsize=8)
    ax.legend(fontsize=8)

plt.tight_layout()
import re
ver = re.search(r'v(\d+)', csv_path)
out_base = f"v{ver.group(1)}" if ver else "latest"
fig_path = f"output/geometric_validation_{out_base}.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
print(f"\nSaved {fig_path}")

json_path = f"output/geometric_validation_{out_base}.json"
results = {
    "meta_regression": {
        "R2": ols.rsquared,
        "interaction_p": ols.pvalues["tier_x_ther"],
        "tier_coef": ols.params["tier_num"],
        "stratum_coef": ols.params["is_therapeutic"],
        "interaction_coef": ols.params["tier_x_ther"],
    },
    "jackknife": {
        "full_tau": full_tau,
        "range": [float(taus_combined.min()), float(taus_combined.max())],
        "mean": float(taus_combined.mean()),
        "std": float(taus_combined.std()),
        "all_significant": all_sig,
    },
    "frechet": frechet_results,
    "invariance_depth": depth_results,
    "n_rows": len(risk),
    "n_with_ci": int(risk["has_ci"].sum()),
}
with open(json_path, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"Saved {json_path}")
