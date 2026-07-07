"""H^1 effect-modifier classification (transportability testing) for neuroepidemiology.

For each mechanism family, stratifies effect sizes by evidence type (study
design), then tests whether effect magnitudes are homogeneous across types
via Cochran's Q. Homogeneous families TRANSPORT; heterogeneous families
do not. Non-transporting families are further classified into obstruction
taxonomy categories and tested pairwise to locate the discordant evidence
type pair(s).

Adapted from psychiatric-validity-audit/analysis/geometric_causal/h1_transportability.py

Usage:
    cd /Users/elliottower/Documents/GitHub/neuroepidemiology-validity-audit
    uv run --with pandas --with scipy --with numpy --with matplotlib \
        python analysis/geometric_causal/h1_transportability.py
"""

import json
import math
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import chi2, mannwhitneyu

matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]

# ────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────

BASE_DIR = Path("/Users/elliottower/Documents/GitHub/neuroepidemiology-validity-audit")

TIER_MAP = {
    "Disconfirmed": 0,
    "Proposed": 1,
    "Underdetermined": 1,
    "Causally Suggestive": 2,
    "Triangulated": 3,
    "Mechanistically Supported": 4,
}

TIER_NAME_FROM_NUM = {v: k for k, v in TIER_MAP.items()}

RATIO_SCALES = {
    "odds ratio", "risk ratio", "hazard ratio", "rate ratio",
    "relative risk", "incidence rate ratio", "hazard/rate ratio",
}

SMD_SCALES = {"cohen d", "hedges g", "smd", "effect size", "mean diff"}

CORR_SCALES = {"correlation", "genetic correlation"}

# Neuro design strings to evidence type codes
DESIGN_TYPE_MAP = {
    "genetic/cohort": "GEN",
    "genetic": "GEN",
    "MR": "GEN",
    "observational": "OBS",
    "RCT": "RCT",
    "diagnostic": "DX",
}

EVIDENCE_TYPE_LABELS = {
    "META": "Meta-analysis",
    "RCT": "RCT / trial",
    "OBS": "Observational",
    "GEN": "Genetic / MR",
    "IMAGING": "Imaging",
    "DX": "Diagnostic",
    "OTHER": "Other",
}


# ────────────────────────────────────────────────────────────────────
# Evidence type classification
# ────────────────────────────────────────────────────────────────────

def classify_evidence_type(design: str) -> str:
    if design in DESIGN_TYPE_MAP:
        return DESIGN_TYPE_MAP[design]

    d = design.lower()

    if any(kw in d for kw in ["gwas", "genetic", "mendelian", "mr"]):
        return "GEN"
    if any(kw in d for kw in ["pet", "fmri", "mri", "imaging"]):
        return "IMAGING"
    if any(kw in d for kw in ["rct", "placebo", "open-label", "phase", "trial"]):
        return "RCT"
    if any(kw in d for kw in ["meta", "mega", "systematic"]):
        return "META"
    if any(kw in d for kw in ["cohort", "observational", "longitudinal"]):
        return "OBS"
    if "diagnostic" in d or "biomarker" in d:
        return "DX"
    return "OTHER"


# ────────────────────────────────────────────────────────────────────
# Effect magnitude and SE computation
# ────────────────────────────────────────────────────────────────────

def is_convertible_scale(scale: str) -> bool:
    s = scale.lower().strip()
    return (
        any(kw in s for kw in ["cohen d", "hedges g", "smd", "effect size", "mean diff"])
        or any(kw in s for kw in ["odds ratio", "risk ratio", "hazard ratio",
                                   "rate ratio", "relative risk", "incidence rate ratio"])
        or "correlation" in s
    )


def to_d_magnitude(estimate: float, scale: str) -> float:
    s = scale.lower().strip()

    if any(kw in s for kw in ["cohen d", "hedges g", "smd", "effect size", "mean diff"]):
        return abs(estimate)

    if any(kw in s for kw in ["odds ratio", "risk ratio", "hazard ratio",
                               "rate ratio", "relative risk", "incidence rate ratio"]):
        if estimate <= 0:
            return float("nan")
        return abs(math.log(estimate) * math.sqrt(3) / math.pi)

    if "correlation" in s:
        r = min(abs(estimate), 0.999)
        return abs(2 * r / math.sqrt(1 - r * r))

    return float("nan")


def compute_se_d(estimate, ci_low, ci_high, n_total, scale: str) -> float:
    s = scale.lower().strip()
    is_ratio = any(kw in s for kw in ["odds ratio", "risk ratio", "hazard ratio",
                                       "rate ratio", "relative risk", "incidence rate ratio"])
    is_corr = "correlation" in s
    chinn = math.sqrt(3) / math.pi

    if not pd.isna(ci_low) and not pd.isna(ci_high):
        if is_ratio:
            if ci_low > 0 and ci_high > 0:
                se_log = (math.log(ci_high) - math.log(ci_low)) / (2 * 1.96)
                return max(se_log * chinn, 1e-6)
        elif is_corr:
            se_r = (ci_high - ci_low) / (2 * 1.96)
            r = min(abs(estimate), 0.999)
            return max(se_r * 2 / (1 - r * r) ** 1.5, 1e-6)
        else:
            se = (ci_high - ci_low) / (2 * 1.96)
            return max(se, 1e-6)

    if not pd.isna(n_total) and n_total > 0:
        if is_ratio and estimate > 0:
            se_log = 1.81 / math.sqrt(n_total)
            return max(se_log * chinn, 1e-6)
        elif is_corr:
            se_r = 1.0 / math.sqrt(n_total - 3) if n_total > 3 else 0.3
            r = min(abs(estimate), 0.999)
            return max(se_r * 2 / (1 - r * r) ** 1.5, 1e-6)
        else:
            d = abs(estimate) if estimate else 0.3
            return max(math.sqrt(4.0 / n_total + d ** 2 / (2.0 * n_total)), 1e-6)

    d_mag = to_d_magnitude(estimate, scale)
    if not math.isnan(d_mag) and d_mag > 0:
        return d_mag / 1.96
    return 0.30


# ────────────────────────────────────────────────────────────────────
# Cochran's Q and pooling
# ────────────────────────────────────────────────────────────────────

def cochran_q(betas: np.ndarray, ses: np.ndarray) -> dict:
    betas = np.asarray(betas, dtype=float)
    ses = np.asarray(ses, dtype=float)

    valid = (ses > 0) & np.isfinite(ses) & np.isfinite(betas)
    betas = betas[valid]
    ses = ses[valid]

    k = len(betas)
    if k < 2:
        return None

    w = 1.0 / (ses ** 2)
    beta_pooled = float(np.sum(w * betas) / np.sum(w))
    Q = float(np.sum(w * (betas - beta_pooled) ** 2))
    df = k - 1
    p = float(1.0 - chi2.cdf(Q, df))
    I2 = float(max(0.0, (Q - df) / Q)) * 100.0 if Q > 0 else 0.0

    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = float(max(0.0, (Q - df) / C)) if C > 0 else 0.0

    return {
        "Q": Q, "df": df, "p": p, "I2": I2,
        "tau2": tau2, "beta_pooled": beta_pooled, "k": k,
    }


def pool_within_type(magnitudes: np.ndarray, ses: np.ndarray):
    magnitudes = np.asarray(magnitudes, dtype=float)
    ses = np.asarray(ses, dtype=float)

    valid = (ses > 0) & np.isfinite(ses) & np.isfinite(magnitudes)
    magnitudes = magnitudes[valid]
    ses = ses[valid]

    if len(magnitudes) == 0:
        return None, None
    if len(magnitudes) == 1:
        return float(magnitudes[0]), float(ses[0])

    w = 1.0 / (ses ** 2)
    pooled = float(np.sum(w * magnitudes) / np.sum(w))
    pooled_se = float(np.sqrt(1.0 / np.sum(w)))
    return pooled, pooled_se


# ────────────────────────────────────────────────────────────────────
# Data loading
# ────────────────────────────────────────────────────────────────────

def load_effect_sizes(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    for col in ("estimate", "ci_low", "ci_high", "n_cases", "n_controls"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Combine n_cases + n_controls for SE estimation
    df["n_total"] = df.get("n_cases", pd.Series(dtype=float)).fillna(0) + \
                    df.get("n_controls", pd.Series(dtype=float)).fillna(0)
    df.loc[df["n_total"] == 0, "n_total"] = np.nan

    df["evidence_type"] = df["design"].apply(classify_evidence_type)
    df["convertible"] = df["scale"].apply(
        lambda s: is_convertible_scale(s) if pd.notna(s) else False
    )

    d_mags = []
    d_ses = []
    for _, row in df.iterrows():
        if row["convertible"] and pd.notna(row["estimate"]):
            d_mags.append(to_d_magnitude(row["estimate"], row["scale"]))
            d_ses.append(compute_se_d(
                row["estimate"], row["ci_low"], row["ci_high"],
                row["n_total"], row["scale"],
            ))
        else:
            d_mags.append(float("nan"))
            d_ses.append(float("nan"))

    df["d_magnitude"] = d_mags
    df["d_se"] = d_ses
    df["tier_num"] = df["best_tier"].map(TIER_MAP)

    return df


def load_ground_truth(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


# ────────────────────────────────────────────────────────────────────
# Obstruction taxonomy
# ────────────────────────────────────────────────────────────────────

def classify_obstruction(family_name: str, family_df: pd.DataFrame,
                         gt_df: pd.DataFrame) -> str:
    family_gt = gt_df[gt_df["family"] == family_name]

    has_disconfirmed = (
        (family_df["best_tier"] == "Disconfirmed").any()
        or (family_df.get("verdict", pd.Series(dtype=str)) == "Disconfirmed").any()
    )
    has_effective_rct = (
        (family_gt["rct_verdict"] == "positive").any()
        if "rct_verdict" in family_gt.columns and len(family_gt) > 0
        else False
    )

    meta_mask = family_df["evidence_type"] == "META"
    meta_d = family_df.loc[meta_mask, "d_magnitude"].dropna()
    has_contradictory_metas = False
    if len(meta_d) >= 2:
        d_min, d_max = meta_d.min(), meta_d.max()
        if d_max > 3 * d_min + 0.1:
            has_contradictory_metas = True

    has_high_tier = family_df["best_tier"].isin(
        ["Mechanistically Supported", "Triangulated"]
    ).any()

    if has_disconfirmed and has_effective_rct:
        return "MIMIC_MECHANISM"
    if has_contradictory_metas:
        return "EVIDENCE_MISFIRE"
    if not has_high_tier and len(family_df) >= 3:
        return "ZOMBIE_MECHANISM"
    return "UNCLASSIFIED"


# ────────────────────────────────────────────────────────────────────
# Main pipeline
# ────────────────────────────────────────────────────────────────────

def run_h1_transportability():
    ts = lambda: f"[{datetime.now():%H:%M:%S}]"

    print(f"{ts()} H^1 effect-modifier classification (transportability testing)")
    print(f"{ts()} Domain: Neuroepidemiology (MS / AD)")
    print("=" * 72)

    effects_path = BASE_DIR / "data" / "effect_sizes_v12.csv"
    gt_path = BASE_DIR / "data" / "external_ground_truth.csv"

    df = load_effect_sizes(effects_path)
    gt_df = load_ground_truth(gt_path)

    usable = df["d_magnitude"].notna() & df["d_se"].notna()
    print(f"{ts()} Loaded {len(df)} effect size entries, {len(gt_df)} ground truth entries")
    print(f"{ts()} Usable for Q test: {usable.sum()}/{len(df)} entries")

    print(f"\nEvidence type distribution (usable entries):")
    for et in sorted(df.loc[usable, "evidence_type"].unique()):
        count = (df.loc[usable, "evidence_type"] == et).sum()
        label = EVIDENCE_TYPE_LABELS.get(et, et)
        print(f"  {et:8s} ({label:20s}): {count}")

    # Non-convertible scales summary
    non_conv = df[~df["convertible"] & df["estimate"].notna()]
    if len(non_conv) > 0:
        print(f"\nNon-convertible scales excluded ({len(non_conv)} entries):")
        for s in sorted(non_conv["scale"].unique()):
            n = (non_conv["scale"] == s).sum()
            print(f"  {s}: {n}")

    # ────────────────────────────────────────────────────────────────
    # Step 1: Group by family, filter qualifying families
    # ────────────────────────────────────────────────────────────────
    # Relaxed threshold: >= 2 entries, >= 2 evidence types (neuro has fewer entries per family)
    print(f"\n{ts()} Identifying qualifying families (>= 2 entries, >= 2 evidence types)")

    qualifying = {}
    for family_name in sorted(df["family"].dropna().unique()):
        fam_df = df[(df["family"] == family_name) & usable].copy()
        types = fam_df["evidence_type"].unique()
        if len(fam_df) >= 2 and len(types) >= 2:
            qualifying[family_name] = fam_df
            type_str = ", ".join(sorted(types))
            print(f"  {family_name:20s}: {len(fam_df)} entries, "
                  f"{len(types)} types ({type_str})")

    n_families = len(qualifying)
    if n_families == 0:
        print("No qualifying families found.")
        return

    alpha_bonferroni = 0.05 / n_families
    print(f"\n{ts()} Bonferroni-corrected alpha: 0.05 / {n_families} = {alpha_bonferroni:.5f}")

    # ────────────────────────────────────────────────────────────────
    # Step 2: Per-family Cochran's Q across evidence types
    # ────────────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print("PER-FAMILY H^1 TRANSPORTABILITY CLASSIFICATION")
    print(f"{'='*72}")

    family_results = {}

    for fam, fam_df in qualifying.items():
        by_type = {}
        for et, et_df in fam_df.groupby("evidence_type"):
            mags = et_df["d_magnitude"].values
            ses = et_df["d_se"].values
            pooled_mag, pooled_se = pool_within_type(mags, ses)
            if pooled_mag is not None and pooled_se is not None:
                by_type[et] = {
                    "beta": pooled_mag,
                    "se": pooled_se,
                    "k": len(et_df),
                    "entries": [
                        {
                            "case_id": r["case_id"],
                            "claim": r["claim"][:80],
                            "d_magnitude": round(r["d_magnitude"], 4),
                            "d_se": round(r["d_se"], 4),
                            "original_scale": r["scale"],
                            "original_estimate": r["estimate"],
                        }
                        for _, r in et_df.iterrows()
                    ],
                }

        if len(by_type) < 2:
            continue

        type_names = sorted(by_type.keys())
        pooled_betas = np.array([by_type[t]["beta"] for t in type_names])
        pooled_ses = np.array([by_type[t]["se"] for t in type_names])

        q_result = cochran_q(pooled_betas, pooled_ses)
        if q_result is None:
            continue

        is_transport = q_result["p"] >= alpha_bonferroni
        classification = "TRANSPORT" if is_transport else "NON-TRANSPORT"

        all_fam = df[df["family"] == fam]
        tier_vals = all_fam["tier_num"].dropna().values
        mean_tier = float(np.mean(tier_vals)) if len(tier_vals) > 0 else float("nan")
        modal_tier_name = all_fam["best_tier"].mode().iloc[0] if len(all_fam) > 0 else "Unknown"

        result = {
            "family": fam,
            "n_entries": len(fam_df),
            "n_evidence_types": len(type_names),
            "evidence_types": type_names,
            "Q": q_result["Q"],
            "df": q_result["df"],
            "p": q_result["p"],
            "I2": q_result["I2"],
            "tau2": q_result["tau2"],
            "beta_pooled": q_result["beta_pooled"],
            "alpha_bonferroni": alpha_bonferroni,
            "classification": classification,
            "mean_tier": mean_tier,
            "modal_tier": modal_tier_name,
            "type_details": {
                t: {"beta": round(by_type[t]["beta"], 4),
                    "se": round(by_type[t]["se"], 4),
                    "k": by_type[t]["k"],
                    "entries": by_type[t]["entries"]}
                for t in type_names
            },
        }

        # Pairwise Q for NON-TRANSPORT families
        pairwise = {}
        if not is_transport and len(type_names) >= 2:
            for i in range(len(type_names)):
                for j in range(i + 1, len(type_names)):
                    ti, tj = type_names[i], type_names[j]
                    pair_betas = np.array([by_type[ti]["beta"], by_type[tj]["beta"]])
                    pair_ses = np.array([by_type[ti]["se"], by_type[tj]["se"]])
                    pair_q = cochran_q(pair_betas, pair_ses)
                    if pair_q is not None:
                        pair_key = f"{ti} vs {tj}"
                        pairwise[pair_key] = {
                            "Q": round(pair_q["Q"], 4),
                            "p": pair_q["p"],
                            "significant": pair_q["p"] < 0.05,
                            "delta_d": round(abs(by_type[ti]["beta"] - by_type[tj]["beta"]), 4),
                            "types": [ti, tj],
                            "type_betas": [round(by_type[ti]["beta"], 4),
                                           round(by_type[tj]["beta"], 4)],
                        }
            result["pairwise_q"] = pairwise

            discordant = [k for k, v in pairwise.items() if v["significant"]]
            result["discordant_pairs"] = discordant

        if not is_transport:
            result["obstruction_taxonomy"] = classify_obstruction(
                fam, fam_df, gt_df,
            )

        family_results[fam] = result

        p_str = f"p={result['p']:.4f}" if result["p"] >= 0.001 else f"p={result['p']:.1e}"
        strata_str = ", ".join(
            f"{t}(k={by_type[t]['k']}, d={by_type[t]['beta']:.3f})"
            for t in type_names
        )
        print(f"\n  {fam:20s}  [{classification:14s}]  "
              f"Q={result['Q']:.3f}  df={result['df']}  {p_str}  "
              f"I2={result['I2']:.1f}%  tier={modal_tier_name}")
        print(f"    Strata: {strata_str}")

        if not is_transport and pairwise:
            for pk, pv in pairwise.items():
                sig = " ***" if pv["significant"] else ""
                print(f"    Pairwise: {pk}: Q={pv['Q']:.3f}, p={pv['p']:.4f}, "
                      f"delta_d={pv['delta_d']:.3f}{sig}")
            if "obstruction_taxonomy" in result:
                print(f"    Obstruction: {result['obstruction_taxonomy']}")

    # ────────────────────────────────────────────────────────────────
    # Step 3: Tier hypothesis test (Mann-Whitney U)
    # ────────────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print("TIER HYPOTHESIS TEST: TRANSPORT vs NON-TRANSPORT")
    print(f"{'='*72}")

    transport_tiers = [
        r["mean_tier"] for r in family_results.values()
        if r["classification"] == "TRANSPORT" and not math.isnan(r["mean_tier"])
    ]
    non_transport_tiers = [
        r["mean_tier"] for r in family_results.values()
        if r["classification"] == "NON-TRANSPORT" and not math.isnan(r["mean_tier"])
    ]

    hypothesis_test = {}

    print(f"\n  TRANSPORT families (n={len(transport_tiers)}):")
    for fam, r in family_results.items():
        if r["classification"] == "TRANSPORT":
            print(f"    {fam:20s}  mean_tier={r['mean_tier']:.2f}  "
                  f"({r['modal_tier']})  Q={r['Q']:.3f}")

    print(f"\n  NON-TRANSPORT families (n={len(non_transport_tiers)}):")
    for fam, r in family_results.items():
        if r["classification"] == "NON-TRANSPORT":
            tax = r.get("obstruction_taxonomy", "")
            print(f"    {fam:20s}  mean_tier={r['mean_tier']:.2f}  "
                  f"({r['modal_tier']})  Q={r['Q']:.3f}  [{tax}]")

    if len(transport_tiers) >= 1 and len(non_transport_tiers) >= 1:
        mean_t = float(np.mean(transport_tiers))
        mean_nt = float(np.mean(non_transport_tiers))

        U, p_mw = mannwhitneyu(
            transport_tiers, non_transport_tiers, alternative="greater",
        )
        n1, n2 = len(transport_tiers), len(non_transport_tiers)
        r_rb = 1 - 2 * U / (n1 * n2) if (n1 * n2) > 0 else 0.0

        hypothesis_test = {
            "transport_mean_tier": mean_t,
            "transport_tier_name": TIER_NAME_FROM_NUM.get(round(mean_t), ""),
            "non_transport_mean_tier": mean_nt,
            "non_transport_tier_name": TIER_NAME_FROM_NUM.get(round(mean_nt), ""),
            "transport_n": n1,
            "non_transport_n": n2,
            "U_statistic": float(U),
            "p_value": float(p_mw),
            "rank_biserial_r": float(r_rb),
            "hypothesis_supported": p_mw < 0.05,
            "transport_families": [
                f for f, r in family_results.items()
                if r["classification"] == "TRANSPORT"
            ],
            "non_transport_families": [
                f for f, r in family_results.items()
                if r["classification"] == "NON-TRANSPORT"
            ],
        }

        print(f"\n  Mean tier TRANSPORT:     {mean_t:.2f} (~{TIER_NAME_FROM_NUM.get(round(mean_t), '')})")
        print(f"  Mean tier NON-TRANSPORT: {mean_nt:.2f} (~{TIER_NAME_FROM_NUM.get(round(mean_nt), '')})")
        print(f"  Difference:             {mean_t - mean_nt:+.2f}")
        print(f"  Mann-Whitney U = {U:.1f}, p = {p_mw:.4f} (one-sided)")
        print(f"  Rank-biserial r = {r_rb:.3f}")
        if p_mw < 0.05:
            print("  --> TRANSPORT families have significantly higher tiers")
        else:
            print("  --> No significant difference in tier between groups")

        q_transport = [r["Q"] for f, r in family_results.items()
                       if r["classification"] == "TRANSPORT"]
        q_non_transport = [r["Q"] for f, r in family_results.items()
                           if r["classification"] == "NON-TRANSPORT"]
        if q_transport and q_non_transport:
            max_t_q = max(q_transport)
            min_nt_q = min(q_non_transport)
            gap = min_nt_q / max_t_q if max_t_q > 0 else float("inf")
            print(f"\n  Q bimodal separation:")
            print(f"    TRANSPORT Q range:     [{min(q_transport):.3f}, {max_t_q:.3f}]")
            print(f"    NON-TRANSPORT Q range: [{min_nt_q:.3f}, {max(q_non_transport):.3f}]")
            print(f"    Gap ratio (min_NT / max_T): {gap:.1f}x")
    else:
        print("  Cannot test: need at least 1 family in each group")
        hypothesis_test = {"error": "insufficient groups for comparison"}

    # ────────────────────────────────────────────────────────────────
    # Step 4: Save results
    # ────────────────────────────────────────────────────────────────
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "domain": "neuroepidemiology (MS / AD)",
            "method": "H^1 effect-modifier classification (transportability)",
            "data_source": str(effects_path),
            "n_total_entries": int(len(df)),
            "n_usable": int(usable.sum()),
            "n_qualifying_families": n_families,
            "alpha": 0.05,
            "alpha_bonferroni": alpha_bonferroni,
        },
        "per_family": {},
        "summary": {
            "n_transport": sum(
                1 for r in family_results.values()
                if r["classification"] == "TRANSPORT"
            ),
            "n_non_transport": sum(
                1 for r in family_results.values()
                if r["classification"] == "NON-TRANSPORT"
            ),
            "transport_families": [
                f for f, r in family_results.items()
                if r["classification"] == "TRANSPORT"
            ],
            "non_transport_families": [
                f for f, r in family_results.items()
                if r["classification"] == "NON-TRANSPORT"
            ],
        },
        "tier_hypothesis_test": hypothesis_test,
    }

    for fam, res in family_results.items():
        serialized = {}
        for k, v in res.items():
            if isinstance(v, (np.integer,)):
                serialized[k] = int(v)
            elif isinstance(v, (np.floating,)):
                serialized[k] = float(v)
            elif isinstance(v, np.ndarray):
                serialized[k] = v.tolist()
            else:
                serialized[k] = v
        output["per_family"][fam] = serialized

    results_path = output_dir / "h1_transportability_results.json"
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n{ts()} Saved results to {results_path}")

    # ────────────────────────────────────────────────────────────────
    # Step 5: Visualization
    # ────────────────────────────────────────────────────────────────
    fig_path = output_dir / "h1_transportability.png"
    plot_transportability(family_results, alpha_bonferroni, fig_path)
    print(f"{ts()} Saved figure to {fig_path}")

    # Summary
    print(f"\n{'='*72}")
    print("SUMMARY")
    print(f"{'='*72}")
    n_t = output["summary"]["n_transport"]
    n_nt = output["summary"]["n_non_transport"]
    print(f"  Qualifying families: {n_families}")
    print(f"  TRANSPORT:           {n_t}  {output['summary']['transport_families']}")
    print(f"  NON-TRANSPORT:       {n_nt}  {output['summary']['non_transport_families']}")

    if hypothesis_test and "p_value" in hypothesis_test:
        p = hypothesis_test["p_value"]
        r = hypothesis_test["rank_biserial_r"]
        print(f"  Tier test:           U={hypothesis_test['U_statistic']:.0f}, "
              f"p={p:.4f}, r_rb={r:.3f}")

    print(f"\n{ts()} Done.")
    return output


# ────────────────────────────────────────────────────────────────────
# Visualization
# ────────────────────────────────────────────────────────────────────

def plot_transportability(family_results: dict, alpha_bonf: float,
                          output_path: Path):
    testable = [
        (fam, res) for fam, res in family_results.items()
        if res["classification"] in ("TRANSPORT", "NON-TRANSPORT")
    ]
    if not testable:
        print("No testable families to plot.")
        return

    testable.sort(key=lambda x: x[1]["Q"], reverse=True)

    fig, axes = plt.subplots(
        1, 2,
        figsize=(14, max(5, len(testable) * 0.55 + 1.5)),
        gridspec_kw={"width_ratios": [2.2, 1]},
    )
    fig.suptitle(
        r"$H^1$ Effect-Modifier Classification: Transportability by Mechanism Family"
        "\n(Neuroepidemiology: MS / AD)",
        fontsize=13, fontweight="bold", y=0.98,
    )

    ax = axes[0]
    y_pos = np.arange(len(testable))

    q_vals = []
    colors = []
    labels = []
    for fam, res in testable:
        q_vals.append(max(res["Q"], 1e-3))
        c = "#c53030" if res["classification"] == "NON-TRANSPORT" else "#2b6cb0"
        colors.append(c)

        tier_short = res["modal_tier"]
        n_types = res["n_evidence_types"]
        labels.append(f"{fam}  ({n_types} types, {tier_short})")

    ax.barh(y_pos, q_vals, color=colors, alpha=0.80, height=0.65,
            edgecolor="white", linewidth=0.5)
    ax.set_xscale("log")

    dfs = [res["df"] for _, res in testable]
    median_df = int(np.median(dfs))
    q_crit = float(chi2.ppf(1 - alpha_bonf, median_df))
    ax.axvline(q_crit, color="#718096", ls="--", lw=1.5, zorder=5,
               label=f"$Q_{{crit}}$ (df={median_df}, "
                     f"$\\alpha_{{Bonf}}$={alpha_bonf:.4f}) = {q_crit:.1f}")

    for i, (fam, res) in enumerate(testable):
        p_str = f"p={res['p']:.3f}" if res["p"] >= 0.001 else f"p={res['p']:.1e}"
        x_pos = max(res["Q"], 1e-3)
        ax.text(x_pos * 1.2, i, f" Q={res['Q']:.2f}, {p_str}, I²={res['I2']:.0f}%",
                va="center", fontsize=7.5, color="#2d3748")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Cochran's Q statistic (log scale)", fontsize=10)
    ax.set_title("(a) Q statistic by mechanism family", fontsize=11)
    ax.invert_yaxis()

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D

    legend_elems = [
        Patch(facecolor="#2b6cb0", alpha=0.80, label="TRANSPORT"),
        Patch(facecolor="#c53030", alpha=0.80, label="NON-TRANSPORT"),
        Line2D([0], [0], color="#718096", ls="--", lw=1.5,
               label=f"$Q_{{crit}}$ (Bonferroni)"),
    ]
    ax.legend(handles=legend_elems, loc="lower right", fontsize=8,
              framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]

    transport_tiers = [
        res["mean_tier"] for _, res in testable
        if res["classification"] == "TRANSPORT" and not math.isnan(res["mean_tier"])
    ]
    non_transport_tiers = [
        res["mean_tier"] for _, res in testable
        if res["classification"] == "NON-TRANSPORT" and not math.isnan(res["mean_tier"])
    ]

    tier_labels_short = ["Disc.", "Prop.", "Caus.\nSugg.", "Triang.", "Mech.\nSupp."]
    tier_range = range(5)

    t_counts = [sum(1 for t in transport_tiers if round(t) == i) for i in tier_range]
    nt_counts = [sum(1 for t in non_transport_tiers if round(t) == i) for i in tier_range]

    x = np.arange(5)
    width = 0.35
    ax.bar(x - width / 2, t_counts, width, color="#2b6cb0", alpha=0.80,
           label="TRANSPORT")
    ax.bar(x + width / 2, nt_counts, width, color="#c53030", alpha=0.80,
           label="NON-TRANSPORT")

    ax.set_xticks(x)
    ax.set_xticklabels(tier_labels_short, fontsize=7.5, rotation=25, ha="right")
    ax.set_ylabel("Count of families", fontsize=10)
    ax.set_title("(b) Validity tier distribution", fontsize=11)
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if transport_tiers and non_transport_tiers:
        mean_t = np.mean(transport_tiers)
        mean_nt = np.mean(non_transport_tiers)
        ax.text(
            0.95, 0.95,
            f"Mean tier\n  T: {mean_t:.2f}\n  NT: {mean_nt:.2f}",
            transform=ax.transAxes, fontsize=8, va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="#cbd5e0", alpha=0.9),
        )

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    run_h1_transportability()
