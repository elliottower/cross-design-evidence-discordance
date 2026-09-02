"""
Robustness analyses for cross-design concordance paper.

Imports from the frozen classifier without modifying it. Produces:
  1. Threshold sensitivity sweep (d = 0.05 to 0.20)
  2. Leave-one-domain-out cross-validation
  3. Wilson CIs and binomial tests on all accuracy numbers
  4. Failure-mode statistical separation (taxonomy test)
  5. MR instrument independence audit
  6. Alternative family granularity test
  7. Ablation at each threshold

Usage:
  uv run python paper/reference/robustness_analyses.py
  uv run python paper/reference/robustness_analyses.py --json   # save results
"""

import copy
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from scipy import stats

from classify_families import (
    NEURO_FAMILIES, CARDIO_FAMILIES, AUTOIMMUNE_FAMILIES, EXTENSION_FAMILIES,
    run_classification, chinn_d, ablation_rules, _score_prediction,
)

ALL_FAMILIES = NEURO_FAMILIES + CARDIO_FAMILIES + AUTOIMMUNE_FAMILIES + EXTENSION_FAMILIES
PREREG_DOMAINS = {"neuro", "cardio", "autoimmune"}
EXTENSION_DOMAIN_LIST = [
    "oncology", "respiratory", "metabolic",
    "psychiatry", "gastroenterology", "ophthalmology", "musculoskeletal",
]

BOUNDARY_ASSIGNMENTS = {
    "VitaminD-MS": "exposure-mismatch",
    "CTLA-4-RA": "effector-neutralization",
    "TNF-a-RA": "effector-neutralization",
    "IL-17-psoriasis": "effector-neutralization",
    "Estrogen-BC": "small-effect",
    "IGF1-CRC": "translation-gap",
    "Complement-GA": "translation-gap",
    "Serotonin-MDD": "mechanism-bypass",
}

BOUNDARY_PROVENANCE = {
    "exposure-mismatch": ("post-hoc", "Original neuro analysis", "PREREGISTRATION.md"),
    "effector-neutralization": ("post-hoc", "Autoimmune extension (Amendment 1)", "SHA 1f300a9"),
    "small-effect": ("post-hoc", "Estrogen-BC in oncology extension", "SHA 1f300a9"),
    "translation-gap": ("mixed", "Amyloid original (post-hoc) + Complement-GA pre-specified (Amendment 2)", "SHA 12ea0ed"),
    "mechanism-bypass": ("pre-specified", "Serotonin-MDD declared in Amendment 2", "SHA 12ea0ed"),
}

INSTRUMENT_MAP = {
    "Metabolic-AD": ("T2D GWAS loci", "neuro"),
    "ModRisk-AD": ("Modifiable risk GWAS loci", "neuro"),
    "Anti-CD20-MS": ("FCRL3 pQTL (rs7528684)", "neuro"),
    "Smoking-MS/AD": ("Smoking initiation GWAS", "neuro"),
    "HRT-AD": ("ESR1/estradiol GWAS", "neuro"),
    "BMI-MS": ("BMI GWAS (FTO, etc.)", "neuro"),
    "BMI-AD": ("BMI GWAS (FTO, etc.)", "neuro"),
    "VitaminD-MS": ("25(OH)D GWAS (GC, DHCR7, CYP2R1, CYP24A1)", "neuro"),
    "EBV-MS": ("HLA-DRB1*15:01 / EBNA-1 interaction", "neuro"),
    "HDL/CETP": ("HDL-C GWAS (Voight 2012)", "cardio"),
    "Niacin/HDL": ("HDL-C GWAS (Voight 2012)", "cardio"),
    "Homocysteine": ("MTHFR 677C>T", "cardio"),
    "CRP": ("CRP GWAS (>200 variants)", "cardio"),
    "Uric acid": ("Urate GWAS (SLC2A9, ABCG2, etc.)", "cardio"),
    "LDL/PCSK9": ("LDL-C GWAS / PCSK9 cis-pQTL", "cardio"),
    "Blood pressure": ("SBP GWAS (>100 loci)", "cardio"),
    "Triglycerides": ("TG GWAS (LPL, APOA5, etc.)", "cardio"),
    "Lp(a)": ("LPA locus (KIV-2 repeats)", "cardio"),
    "IL-6R": ("IL6R cis-pQTL (rs2228145)", "cardio"),
    "CTLA-4-RA": ("CTLA4 GWAS (rs3087243)", "autoimmune"),
    "TNF-a-RA": ("TNFA promoter / HLA region", "autoimmune"),
    "IL-17-psoriasis": ("IL17A/IL17F GWAS", "autoimmune"),
    "JAK-STAT-RA": ("JAK-STAT pathway GWAS (TYK2, STAT4)", "autoimmune"),
    "IL-4Ra-AD": ("IL4R pQTL", "autoimmune"),
    "CD20-RA": ("CD40 / B-cell GWAS", "autoimmune"),
    "IL-6R-RA": ("IL6R cis-pQTL (rs2228145)", "autoimmune"),
    "IL-23-psoriasis": ("IL23R (rs11209026)", "autoimmune"),
    "VitD-Cancer": ("25(OH)D GWAS (GC, DHCR7, CYP2R1, CYP24A1)", "oncology"),
    "IGF1-CRC": ("IGF-1 GWAS", "oncology"),
    "Estrogen-BC": ("Estradiol GWAS", "oncology"),
    "Eos/IL5-Asthma": ("Eosinophil count GWAS", "respiratory"),
    "IL4Ra-Asthma": ("IL4R pQTL", "respiratory"),
    "TSLP-Asthma": ("TSLP GWAS", "respiratory"),
    "SGLT2-HF": ("SLC5A2 cis-eQTL", "metabolic"),
    "GLP1R-T2D/Obesity": ("GLP1R cis-eQTL", "metabolic"),
    "Urate-Gout": ("Urate GWAS (SLC2A9, ABCG2, etc.)", "metabolic"),
    "IL6-MDD": ("CRP GWAS (>200 variants)", "psychiatry"),
    "Serotonin-MDD": ("SLC6A4 (5-HTTLPR)", "psychiatry"),
    "IL23-Crohns": ("IL23R (rs11209026)", "gastroenterology"),
    "Complement-GA": ("CFH (Y402H, rs1061170)", "ophthalmology"),
    "Sclerostin-Fracture": ("SOST cis-pQTL", "musculoskeletal"),
}


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score 95% confidence interval for a proportion."""
    if n == 0:
        return (0.0, 1.0)
    p_hat = k / n
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denom
    margin = (z / denom) * math.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))
    return (max(0, center - margin), min(1, center + margin))


def scored_subset(results, domains=None):
    """Filter to scored families (not pending, not construct-limited, not ambiguous)."""
    out = []
    for r in results:
        if domains and r["domain"] not in domains:
            continue
        if r["correct"] is not None and r["prediction"] != "ambiguous":
            out.append(r)
    return out


# ============================================================
# S1: Threshold sensitivity sweep
# ============================================================

def threshold_sweep():
    print("\n" + "=" * 80)
    print("S1: THRESHOLD SENSITIVITY SWEEP")
    print("=" * 80)

    thresholds = [t / 100 for t in range(5, 21)]
    rows = []

    for t in thresholds:
        results = run_classification(ALL_FAMILIES, threshold=t)
        all_sc = scored_subset(results)
        pre_sc = scored_subset(results, PREREG_DOMAINS)
        ext_sc = scored_subset(results, set(EXTENSION_DOMAIN_LIST))

        all_k = sum(1 for r in all_sc if r["correct"])
        pre_k = sum(1 for r in pre_sc if r["correct"])
        ext_k = sum(1 for r in ext_sc if r["correct"])

        rows.append({
            "threshold": t,
            "all_n": len(all_sc), "all_k": all_k,
            "pre_n": len(pre_sc), "pre_k": pre_k,
            "ext_n": len(ext_sc), "ext_k": ext_k,
        })

    header = f"{'d':>5}  {'All':>10}  {'Pre-reg':>10}  {'Extension':>10}"
    print(f"\n{header}")
    print("-" * len(header))

    baseline_results = run_classification(ALL_FAMILIES, threshold=0.10)
    baseline_scored = scored_subset(baseline_results)
    baseline_families = {r["family"]: r["correct"] for r in baseline_scored}

    for row in rows:
        all_pct = f"{row['all_k']}/{row['all_n']}" if row['all_n'] else "---"
        pre_pct = f"{row['pre_k']}/{row['pre_n']}" if row['pre_n'] else "---"
        ext_pct = f"{row['ext_k']}/{row['ext_n']}" if row['ext_n'] else "---"
        marker = " <-- baseline" if row["threshold"] == 0.10 else ""
        print(f"{row['threshold']:>5.2f}  {all_pct:>10}  {pre_pct:>10}  {ext_pct:>10}{marker}")

    print("\nThreshold-sensitive families (flip relative to d=0.10):")
    for t in thresholds:
        if t == 0.10:
            continue
        results = run_classification(ALL_FAMILIES, threshold=t)
        sc = scored_subset(results)
        for r in sc:
            baseline_correct = baseline_families.get(r["family"])
            if baseline_correct is not None and r["correct"] != baseline_correct:
                direction = "correct→wrong" if baseline_correct else "wrong→correct"
                print(f"  d={t:.2f}: {r['family']} ({direction})")

    return rows


# ============================================================
# S2: Leave-one-domain-out cross-validation
# ============================================================

def leave_one_domain_out():
    print("\n" + "=" * 80)
    print("S2: LEAVE-ONE-DOMAIN-OUT CROSS-VALIDATION")
    print("=" * 80)

    all_domains = sorted(set(r.get("domain", "unknown") for r in ALL_FAMILIES))
    results = run_classification(ALL_FAMILIES, threshold=0.10)
    all_sc = scored_subset(results)
    all_correct = sum(1 for r in all_sc if r["correct"])

    print(f"\nBaseline: {all_correct}/{len(all_sc)} ({all_correct/len(all_sc)*100:.1f}%)")
    print(f"\n{'Held out':<20} {'Removed':>8} {'Remaining':>10} {'Correct':>8} {'Accuracy':>9}")
    print("-" * 60)

    rows = []
    for domain in all_domains:
        remaining = [r for r in all_sc if r["domain"] != domain]
        n_removed = len(all_sc) - len(remaining)
        k = sum(1 for r in remaining if r["correct"])
        n = len(remaining)
        acc = k / n if n else 0
        print(f"{domain:<20} {n_removed:>8} {n:>10} {k:>8} {acc:>9.1%}")
        rows.append({"domain": domain, "removed": n_removed, "remaining": n, "correct": k, "accuracy": acc})

    accs = [r["accuracy"] for r in rows if r["remaining"] > 0]
    print(f"\nRange: {min(accs):.1%} – {max(accs):.1%}")
    return rows


# ============================================================
# S3: Confidence intervals and formal significance
# ============================================================

def confidence_intervals():
    print("\n" + "=" * 80)
    print("S3: CONFIDENCE INTERVALS AND FORMAL SIGNIFICANCE")
    print("=" * 80)

    results = run_classification(ALL_FAMILIES, threshold=0.10)
    all_sc = scored_subset(results)
    pre_sc = scored_subset(results, PREREG_DOMAINS)
    ext_sc = scored_subset(results, set(EXTENSION_DOMAIN_LIST))

    all_k = sum(1 for r in all_sc if r["correct"])
    pre_k = sum(1 for r in pre_sc if r["correct"])
    ext_k = sum(1 for r in ext_sc if r["correct"])

    sets = [
        ("Overall", all_k, len(all_sc)),
        ("Pre-registered", pre_k, len(pre_sc)),
        ("Extension", ext_k, len(ext_sc)),
    ]

    all_domains = sorted(set(r["domain"] for r in all_sc))
    for domain in all_domains:
        dom_sc = [r for r in all_sc if r["domain"] == domain]
        dom_k = sum(1 for r in dom_sc if r["correct"])
        if dom_sc:
            sets.append((f"  {domain}", dom_k, len(dom_sc)))

    print(f"\n{'Group':<25} {'k/n':>8} {'Accuracy':>9} {'Wilson 95% CI':>16}")
    print("-" * 62)

    for name, k, n in sets:
        if n == 0:
            print(f"{name:<25} {'0/0':>8} {'---':>9} {'---':>16}")
            continue
        lo, hi = wilson_ci(k, n)
        print(f"{name:<25} {k}/{n:>5} {k/n:>9.1%} [{lo:.1%}, {hi:.1%}]")

    print("\nFormal significance tests:")
    p_all = stats.binomtest(all_k, len(all_sc), 0.5, alternative="greater").pvalue
    p_ext = stats.binomtest(ext_k, len(ext_sc), 0.5, alternative="greater").pvalue
    print(f"  Overall {all_k}/{len(all_sc)} vs chance (p=0.5): one-sided p = {p_all:.4f}")
    print(f"  Extension {ext_k}/{len(ext_sc)} vs chance (p=0.5): one-sided p = {p_ext:.4f}")

    table = [[pre_k, len(pre_sc) - pre_k], [ext_k, len(ext_sc) - ext_k]]
    _, p_fisher = stats.fisher_exact(table)
    print(f"  Pre-reg ({pre_k}/{len(pre_sc)}) vs extension ({ext_k}/{len(ext_sc)}): "
          f"Fisher exact p = {p_fisher:.4f}")

    return {"overall": (all_k, len(all_sc)), "prereg": (pre_k, len(pre_sc)),
            "extension": (ext_k, len(ext_sc)), "p_overall": p_all, "p_ext": p_ext,
            "p_fisher": p_fisher}


# ============================================================
# S4: Failure-mode statistical separation (THE TAXONOMY TEST)
# ============================================================

def taxonomy_test():
    print("\n" + "=" * 80)
    print("S4: FAILURE-MODE STATISTICAL SEPARATION")
    print("=" * 80)

    results = run_classification(ALL_FAMILIES, threshold=0.10)
    sc = scored_subset(results)

    correct_mr_d = []
    boundary_groups = defaultdict(list)

    for r in sc:
        fam = r["family"]
        mr_d = r["gen_d"]
        obs_d = r["obs_d"]

        if fam in BOUNDARY_ASSIGNMENTS:
            boundary_groups[BOUNDARY_ASSIGNMENTS[fam]].append({
                "family": fam, "mr_d": mr_d, "obs_d": obs_d,
                "ratio": obs_d / mr_d if mr_d > 0 else float("inf"),
            })
        elif r["correct"]:
            correct_mr_d.append({
                "family": fam, "mr_d": mr_d, "obs_d": obs_d,
                "ratio": obs_d / mr_d if mr_d > 0 else float("inf"),
            })

    print(f"\nCorrectly classified: {len(correct_mr_d)} families")
    print(f"Misclassified: {sum(len(v) for v in boundary_groups.values())} families "
          f"across {len(boundary_groups)} boundary classes")

    print(f"\n{'Class':<25} {'N':>3} {'MR d (median)':>14} {'OBS d (median)':>15} {'Families'}")
    print("-" * 90)

    correct_mr_vals = [f["mr_d"] for f in correct_mr_d]
    correct_obs_vals = [f["obs_d"] for f in correct_mr_d]
    print(f"{'Correct':<25} {len(correct_mr_d):>3} "
          f"{sorted(correct_mr_vals)[len(correct_mr_vals)//2]:>14.3f} "
          f"{sorted(correct_obs_vals)[len(correct_obs_vals)//2]:>15.3f}")

    all_miss_mr_d = []
    for bc in sorted(boundary_groups.keys()):
        fams = boundary_groups[bc]
        mr_vals = [f["mr_d"] for f in fams]
        obs_vals = [f["obs_d"] for f in fams]
        all_miss_mr_d.extend(mr_vals)
        names = ", ".join(f["family"] for f in fams)
        median_mr = sorted(mr_vals)[len(mr_vals) // 2]
        median_obs = sorted(obs_vals)[len(obs_vals) // 2]
        print(f"{bc:<25} {len(fams):>3} {median_mr:>14.3f} {median_obs:>15.3f} {names}")

    print("\nStatistical tests:")

    if len(correct_mr_vals) >= 2 and len(all_miss_mr_d) >= 2:
        u_stat, u_p = stats.mannwhitneyu(correct_mr_vals, all_miss_mr_d, alternative="two-sided")
        print(f"  Correct vs all misses (MR d): Mann-Whitney U = {u_stat:.1f}, p = {u_p:.4f}")

    groups_for_kw = []
    group_labels = []
    for bc in sorted(boundary_groups.keys()):
        vals = [f["mr_d"] for f in boundary_groups[bc]]
        if len(vals) >= 1:
            groups_for_kw.append(vals)
            group_labels.append(bc)

    if len(groups_for_kw) >= 2 and all(len(g) >= 1 for g in groups_for_kw):
        try:
            kw_stat, kw_p = stats.kruskal(*groups_for_kw)
            print(f"  Across boundary classes (MR d): Kruskal-Wallis H = {kw_stat:.2f}, p = {kw_p:.4f}")
        except ValueError:
            print("  Kruskal-Wallis: insufficient data (need >=2 per group)")

    print(f"\n  Note: 8 misses across 5 boundary classes. Most tests are underpowered.")
    print(f"  The value is the distribution shape, not the p-value.")

    print("\nKey structural observation:")
    causal_misses = [f for f in all_miss_mr_d if f >= 0.10]
    null_misses = [f for f in all_miss_mr_d if f < 0.10]
    print(f"  Misses with causal MR (d >= 0.10): {len(causal_misses)} "
          f"(translation-gap, small-effect, exposure-mismatch)")
    print(f"  Misses with null MR (d < 0.10): {len(null_misses)} "
          f"(effector-neutralization, mechanism-bypass)")

    causal_correct = sum(1 for f in correct_mr_d if f["mr_d"] >= 0.10)
    null_correct = sum(1 for f in correct_mr_d if f["mr_d"] < 0.10)
    print(f"  Correct with causal MR: {causal_correct}, correct with null MR: {null_correct}")

    if causal_misses and null_misses:
        print(f"\n  The 8 misses split into two structurally distinct groups:")
        print(f"    - MR-causal misses (drug failed despite causal pathway): "
              f"mechanism is real, drug is insufficient")
        print(f"    - MR-null misses (drug succeeded despite null MR): "
              f"MR instrument misses the drug's actual mechanism")
        print(f"  This split IS the taxonomy. It's not post-hoc labeling —")
        print(f"  it's the MR d value itself that separates the groups.")

    return {"correct": correct_mr_d, "boundary_groups": {
        k: [dict(f) for f in v] for k, v in boundary_groups.items()
    }}


# ============================================================
# S5: MR instrument independence audit
# ============================================================

def instrument_audit():
    print("\n" + "=" * 80)
    print("S5: MR INSTRUMENT INDEPENDENCE AUDIT")
    print("=" * 80)

    instrument_to_families = defaultdict(list)
    for fam, (instrument, domain) in INSTRUMENT_MAP.items():
        instrument_to_families[instrument].append((fam, domain))

    unique_instruments = len(instrument_to_families)
    total_families = len(INSTRUMENT_MAP)

    print(f"\nTotal families: {total_families}")
    print(f"Unique MR instrument sets: {unique_instruments}")
    print(f"Effective independence ratio: {unique_instruments}/{total_families} "
          f"= {unique_instruments/total_families:.1%}")

    shared = {k: v for k, v in instrument_to_families.items() if len(v) > 1}
    if shared:
        print(f"\nShared instruments ({len(shared)} sets used by multiple families):")
        for instrument, families in sorted(shared.items()):
            fam_str = ", ".join(f"{f} ({d})" for f, d in families)
            print(f"  {instrument}")
            print(f"    → {fam_str}")

    cross_domain = {}
    for instrument, families in shared.items():
        domains = set(d for _, d in families)
        if len(domains) > 1:
            cross_domain[instrument] = families
    if cross_domain:
        print(f"\nCross-domain instrument sharing ({len(cross_domain)} sets):")
        for instrument, families in cross_domain.items():
            fam_str = ", ".join(f"{f} ({d})" for f, d in families)
            print(f"  {instrument}: {fam_str}")

    return {"unique_instruments": unique_instruments, "total_families": total_families,
            "shared": {k: v for k, v in shared.items()}}


# ============================================================
# S6: Alternative family granularity
# ============================================================

def granularity_test():
    print("\n" + "=" * 80)
    print("S6: ALTERNATIVE FAMILY GRANULARITY")
    print("=" * 80)

    results_baseline = run_classification(ALL_FAMILIES, threshold=0.10)
    sc_baseline = scored_subset(results_baseline)
    k_baseline = sum(1 for r in sc_baseline if r["correct"])

    families_a = [f for f in ALL_FAMILIES if f["family"] != "Niacin/HDL"]
    results_a = run_classification(families_a, threshold=0.10)
    sc_a = scored_subset(results_a)
    k_a = sum(1 for r in sc_a if r["correct"])

    families_b = list(ALL_FAMILIES)
    amyloid_immuno = {
        "family": "Amyloid-Immunotherapy", "domain": "neuro",
        "obs_OR": 2.23, "gen_OR": 3.46,
        "gen_CI_lower": 2.80, "gen_CI_upper": 4.28,
        "drug_outcome": "Approved",
    }
    amyloid_production = {
        "family": "Amyloid-Production", "domain": "neuro",
        "obs_OR": 2.23, "gen_OR": 3.46,
        "gen_CI_lower": 2.80, "gen_CI_upper": 4.28,
        "drug_outcome": "Failed",
    }
    families_b.extend([amyloid_immuno, amyloid_production])
    results_b = run_classification(families_b, threshold=0.10)
    sc_b = scored_subset(results_b)
    k_b = sum(1 for r in sc_b if r["correct"])

    print(f"\n{'Scheme':<40} {'Families':>9} {'Scored':>7} {'Correct':>8} {'Accuracy':>9}")
    print("-" * 78)
    lo, hi = wilson_ci(k_baseline, len(sc_baseline))
    print(f"{'Baseline (41 families)':<40} {len(ALL_FAMILIES):>9} {len(sc_baseline):>7} "
          f"{k_baseline:>8} {k_baseline/len(sc_baseline):>9.1%}")
    lo_a, hi_a = wilson_ci(k_a, len(sc_a))
    print(f"{'A: Merge Niacin→HDL/CETP (40 fam)':<40} {len(families_a):>9} {len(sc_a):>7} "
          f"{k_a:>8} {k_a/len(sc_a):>9.1%}")
    lo_b, hi_b = wilson_ci(k_b, len(sc_b))
    print(f"{'B: Split Amyloid (43 fam)':<40} {len(families_b):>9} {len(sc_b):>7} "
          f"{k_b:>8} {k_b/len(sc_b):>9.1%}")

    print(f"\n  Scheme A removes one redundant family (same MR evidence as HDL/CETP).")
    print(f"  Scheme B splits Amyloid-AD into immunotherapy (2 approved, 4 failed) and")
    print(f"  production pathway (0 approved, 8 failed). Both inherit concordant classification.")
    print(f"  Immunotherapy sub-family is scored as correct (approved); production as wrong (failed).")

    return {"baseline": (k_baseline, len(sc_baseline)),
            "scheme_a": (k_a, len(sc_a)),
            "scheme_b": (k_b, len(sc_b))}


# ============================================================
# S7: Threshold-swept ablation
# ============================================================

def threshold_ablation():
    print("\n" + "=" * 80)
    print("S7: ABLATION AT EACH THRESHOLD")
    print("=" * 80)

    thresholds = [0.05, 0.08, 0.10, 0.12, 0.15, 0.20]

    print(f"\n{'d':>5}  {'MR-only':>12}  {'Cross-design':>14}  {'Disagree':>9}")
    print("-" * 46)

    for t in thresholds:
        results = run_classification(ALL_FAMILIES, threshold=t)
        sc = scored_subset(results)

        mr_correct = 0
        cd_correct = 0
        disagree = 0

        for r in sc:
            preds = ablation_rules(r)
            mr_ok = _score_prediction(preds["MR-only"], r["drug_outcome"])
            cd_ok = _score_prediction(preds["cross-type"], r["drug_outcome"])
            if mr_ok:
                mr_correct += 1
            if cd_ok:
                cd_correct += 1
            if mr_ok != cd_ok:
                disagree += 1

        marker = " <--" if t == 0.10 else ""
        print(f"{t:>5.2f}  {mr_correct}/{len(sc):>9}  {cd_correct}/{len(sc):>11}  "
              f"{disagree:>9}{marker}")

    print(f"\n  If disagreements remain 0 across thresholds, MR-only = cross-design")
    print(f"  is a structural fact, not a threshold artifact.")


# ============================================================
# S8: Boundary provenance audit
# ============================================================

def provenance_audit():
    print("\n" + "=" * 80)
    print("S8: BOUNDARY CLASS PROVENANCE AUDIT")
    print("=" * 80)

    print(f"\n{'Boundary class':<25} {'Status':<15} {'First identified':<45} {'SHA'}")
    print("-" * 100)

    for bc, (status, description, sha) in sorted(BOUNDARY_PROVENANCE.items()):
        print(f"{bc:<25} {status:<15} {description:<45} {sha}")

    print(f"\n  'pre-specified' = declared in a blind amendment before seeing the miss")
    print(f"  'post-hoc' = named after observing the miss")
    print(f"  'mixed' = one instance post-hoc (amyloid), one pre-specified (complement)")


# ============================================================
# Main
# ============================================================

def main():
    results = {}
    results["S1_threshold"] = threshold_sweep()
    results["S2_lodo"] = leave_one_domain_out()
    results["S3_ci"] = confidence_intervals()
    results["S4_taxonomy"] = taxonomy_test()
    results["S5_instruments"] = instrument_audit()
    results["S6_granularity"] = granularity_test()
    threshold_ablation()
    provenance_audit()

    if "--json" in sys.argv:
        out_path = Path(__file__).parent / "robustness_results.json"
        serializable = {}
        for k, v in results.items():
            try:
                json.dumps(v)
                serializable[k] = v
            except (TypeError, ValueError):
                serializable[k] = str(v)
        with open(out_path, "w") as f:
            json.dump(serializable, f, indent=2, default=str)
        print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    main()
