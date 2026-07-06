"""
Frozen classification rule for etiologic evidence discordance.

Two-criterion rule:
  OBS: "non-trivial" if d >= threshold (exposure-comparable scale)
  MR:  "causal" if CI excludes null AND d >= threshold (after per-SD rescaling)

Classification:
  OBS non-trivial + MR null   -> qualitative discordance -> predict failure
  OBS non-trivial + MR causal -> concordance -> predict success
  OBS trivial + MR null       -> null concordance -> ambiguous
  OBS trivial + MR causal     -> genetic-only signal
"""

import csv
import json
import math
import sys
from pathlib import Path


def chinn_d(OR: float) -> float:
    """Convert OR to Cohen's d via Chinn (2000): d = |ln(OR)| * sqrt(3) / pi."""
    if OR <= 0:
        raise ValueError(f"OR must be positive, got {OR}")
    return abs(math.log(OR)) * math.sqrt(3) / math.pi


def rescale_per_allele_to_per_sd(or_per_allele: float, sd_per_allele: float) -> float:
    """Rescale per-allele OR to per-SD OR.

    or_per_allele: MR OR per copy of the variant
    sd_per_allele: change in exposure (in SD units) per allele
    Returns: OR per 1 SD change in the exposure
    """
    if sd_per_allele <= 0:
        raise ValueError(f"sd_per_allele must be positive, got {sd_per_allele}")
    return or_per_allele ** (1.0 / sd_per_allele)


def ci_excludes_null(ci_lower: float, ci_upper: float) -> bool:
    """Check whether a confidence interval for an OR excludes 1.0."""
    return not (ci_lower <= 1.0 <= ci_upper)


def classify_mr(ci_lower: float, ci_upper: float, d_value: float,
                threshold: float = 0.10) -> str:
    """Classify MR evidence as 'causal' or 'null' using the two-criterion rule."""
    stat_sig = ci_excludes_null(ci_lower, ci_upper)
    above_floor = d_value >= threshold
    if stat_sig and above_floor:
        return "causal"
    return "null"


def classify_obs(d_value: float, threshold: float = 0.10) -> str:
    """Classify observational evidence as 'non-trivial' or 'trivial'."""
    if d_value >= threshold:
        return "non-trivial"
    return "trivial"


def classify_family(obs_class: str, mr_class: str) -> tuple[str, str]:
    """Classify a mechanism family. Returns (classification, prediction)."""
    if obs_class == "non-trivial" and mr_class == "null":
        return "qualitative discordance", "failure"
    elif obs_class == "non-trivial" and mr_class == "causal":
        return "concordance", "success"
    elif obs_class == "trivial" and mr_class == "null":
        return "null concordance", "ambiguous"
    elif obs_class == "trivial" and mr_class == "causal":
        return "genetic-only signal", "success"
    raise ValueError(f"Unexpected combination: obs={obs_class}, mr={mr_class}")


def run_classification(families: list[dict], threshold: float = 0.10) -> list[dict]:
    """Run the full classification pipeline on a list of families."""
    results = []
    for f in families:
        obs_d = chinn_d(f["obs_OR"])
        obs_class = classify_obs(obs_d, threshold)

        mr_or = f["gen_OR"]
        if f.get("per_allele") and f.get("sd_per_allele"):
            mr_or = rescale_per_allele_to_per_sd(mr_or, f["sd_per_allele"])
        mr_d = chinn_d(mr_or)

        ci_lo = f.get("gen_CI_lower")
        ci_hi = f.get("gen_CI_upper")
        if ci_lo is not None and ci_hi is not None:
            mr_class = classify_mr(ci_lo, ci_hi, mr_d, threshold)
        else:
            mr_class = "null" if mr_d < threshold else "causal"

        classification, prediction = classify_family(obs_class, mr_class)

        actual = f.get("drug_outcome", "unknown")
        if actual in ("Approved", "approved"):
            correct = prediction == "success"
        elif actual in ("Failed", "failed", "No benefit"):
            correct = prediction == "failure"
        elif actual in ("Pending", "pending"):
            correct = None
        else:
            correct = None

        results.append({
            "family": f["family"],
            "domain": f.get("domain", "unknown"),
            "obs_OR": f["obs_OR"],
            "obs_d": round(obs_d, 3),
            "obs_class": obs_class,
            "gen_OR_raw": f["gen_OR"],
            "gen_OR_rescaled": round(mr_or, 3) if f.get("per_allele") else None,
            "gen_d": round(mr_d, 3),
            "gen_CI": f"({ci_lo}-{ci_hi})" if ci_lo else None,
            "mr_class": mr_class,
            "classification": classification,
            "prediction": prediction,
            "drug_outcome": actual,
            "correct": correct,
        })
    return results


NEURO_FAMILIES = [
    {"family": "Metabolic-AD", "domain": "neuro", "obs_OR": 1.53, "gen_OR": 1.01,
     "drug_outcome": "Failed"},
    {"family": "ModRisk-AD", "domain": "neuro", "obs_OR": 1.46, "gen_OR": 1.10,
     "drug_outcome": "Failed"},
    {"family": "Anti-CD20-MS", "domain": "neuro", "obs_OR": 2.23, "gen_OR": 0.83,
     "gen_CI_lower": 0.79, "gen_CI_upper": 0.89,
     "per_allele": True, "sd_per_allele": 0.40,
     "drug_outcome": "Approved"},
    {"family": "Smoking-MS/AD", "domain": "neuro", "obs_OR": 1.46, "gen_OR": 1.03,
     "drug_outcome": "Failed"},
    {"family": "HRT-AD", "domain": "neuro", "obs_OR": 0.67, "gen_OR": 1.00,
     "gen_CI_lower": 0.85, "gen_CI_upper": 1.18,
     "drug_outcome": "Failed"},
    {"family": "BMI-MS", "domain": "neuro", "obs_OR": 1.92, "gen_OR": 1.41,
     "gen_CI_lower": 1.20, "gen_CI_upper": 1.66,
     "drug_outcome": "Pending"},
    {"family": "BMI-AD", "domain": "neuro", "obs_OR": 2.04, "gen_OR": 1.03,
     "gen_CI_lower": 1.01, "gen_CI_upper": 1.05,
     "drug_outcome": "Failed"},
    {"family": "VitaminD-MS", "domain": "neuro", "obs_OR": 1.40, "gen_OR": 2.00,
     "gen_CI_lower": 1.70, "gen_CI_upper": 2.50,
     "drug_outcome": "Failed"},
    {"family": "EBV-MS", "domain": "neuro", "obs_OR": 1.70, "gen_OR": 5.00,
     "gen_CI_lower": 2.00, "gen_CI_upper": 20.0,
     "drug_outcome": "Approved"},
]

CARDIO_FAMILIES = [
    {"family": "HDL/CETP", "domain": "cardio", "obs_OR": 0.62, "gen_OR": 0.93,
     "gen_CI_lower": 0.68, "gen_CI_upper": 1.26, "drug_outcome": "Failed"},
    {"family": "Niacin/HDL", "domain": "cardio", "obs_OR": 0.62, "gen_OR": 0.93,
     "gen_CI_lower": 0.68, "gen_CI_upper": 1.26, "drug_outcome": "Failed"},
    {"family": "Homocysteine", "domain": "cardio", "obs_OR": 1.32, "gen_OR": 1.02,
     "gen_CI_lower": 0.98, "gen_CI_upper": 1.07, "drug_outcome": "Failed"},
    {"family": "CRP", "domain": "cardio", "obs_OR": 1.37, "gen_OR": 1.00,
     "gen_CI_lower": 0.97, "gen_CI_upper": 1.02, "drug_outcome": "No benefit"},
    {"family": "Uric acid", "domain": "cardio", "obs_OR": 1.07, "gen_OR": 1.05,
     "gen_CI_lower": 0.92, "gen_CI_upper": 1.20, "drug_outcome": "Failed"},
    {"family": "LDL/PCSK9", "domain": "cardio", "obs_OR": 1.52, "gen_OR": 1.78,
     "gen_CI_lower": 1.58, "gen_CI_upper": 2.01, "drug_outcome": "Approved"},
    {"family": "Blood pressure", "domain": "cardio", "obs_OR": 1.41, "gen_OR": 1.44,
     "gen_CI_lower": 1.35, "gen_CI_upper": 1.55, "drug_outcome": "Approved"},
    {"family": "Triglycerides", "domain": "cardio", "obs_OR": 1.72, "gen_OR": 1.62,
     "gen_CI_lower": 1.24, "gen_CI_upper": 2.11, "drug_outcome": "Approved"},
    {"family": "Lp(a)", "domain": "cardio", "obs_OR": 1.13, "gen_OR": 0.94,
     "gen_CI_lower": 0.93, "gen_CI_upper": 0.95, "drug_outcome": "Pending"},
    {"family": "IL-6R", "domain": "cardio", "obs_OR": 1.25, "gen_OR": 0.95,
     "gen_CI_lower": 0.93, "gen_CI_upper": 0.97,
     "per_allele": True, "sd_per_allele": 0.34,
     "drug_outcome": "Pending"},
]


AUTOIMMUNE_FAMILIES = [
    {"family": "IL-23-psoriasis", "domain": "autoimmune", "obs_OR": 3.00,
     "gen_OR": 0.616, "gen_CI_lower": 0.563, "gen_CI_upper": 0.674,
     "drug_outcome": "Approved"},
    {"family": "CTLA-4-RA", "domain": "autoimmune", "obs_OR": 1.50,
     "gen_OR": 0.86, "gen_CI_lower": 0.78, "gen_CI_upper": 0.95,
     "drug_outcome": "Approved"},
    {"family": "TNF-a-RA", "domain": "autoimmune", "obs_OR": 2.00,
     "gen_OR": 1.00,
     "drug_outcome": "Approved"},
    {"family": "IL-17-psoriasis", "domain": "autoimmune", "obs_OR": 2.00,
     "gen_OR": 1.00,
     "drug_outcome": "Approved"},
]


def print_results(results: list[dict]) -> None:
    header = f"{'Family':<20} {'OBS d':>7} {'OBS':>12} {'GEN d':>7} {'MR':>8} {'Class':<25} {'Pred':>8} {'Actual':>12} {'OK?':>5}"
    print(header)
    print("=" * len(header))
    for r in results:
        ok = "✓" if r["correct"] is True else ("✗" if r["correct"] is False else "—")
        print(f"{r['family']:<20} {r['obs_d']:>7.3f} {r['obs_class']:>12} "
              f"{r['gen_d']:>7.3f} {r['mr_class']:>8} {r['classification']:<25} "
              f"{r['prediction']:>8} {r['drug_outcome']:>12} {ok:>5}")


def main():
    thresholds = [0.08, 0.10, 0.12, 0.15] if "--sensitivity" in sys.argv else [0.10]
    all_families = NEURO_FAMILIES + CARDIO_FAMILIES + AUTOIMMUNE_FAMILIES

    for t in thresholds:
        print(f"\n{'='*80}")
        print(f"THRESHOLD d = {t:.2f}")
        print(f"{'='*80}")
        results = run_classification(all_families, threshold=t)

        print(f"\n--- Neuro ---")
        print_results([r for r in results if r["domain"] == "neuro"])
        print(f"\n--- Cardio ---")
        print_results([r for r in results if r["domain"] == "cardio"])
        print(f"\n--- Autoimmune ---")
        print_results([r for r in results if r["domain"] == "autoimmune"])

        known = [r for r in results if r["correct"] is not None]
        correct = sum(1 for r in known if r["correct"])
        ambig_known = [r for r in known if r["prediction"] == "ambiguous"]
        unambig = [r for r in known if r["prediction"] != "ambiguous"]
        correct_unambig = sum(1 for r in unambig if r["correct"])
        pending = sum(1 for r in results if r["drug_outcome"] == "Pending")
        print(f"\nAll known outcomes: {correct}/{len(known)} correct")
        print(f"Excluding ambiguous: {correct_unambig}/{len(unambig)} correct "
              f"({len(ambig_known)} ambiguous, {pending} pending)")
        print(f"Sensitivity: headline is {correct_unambig}/{len(unambig)} "
              f"or {correct}/{len(known)} depending on ambiguous adjudication")

    if "--json" in sys.argv:
        results = run_classification(all_families, threshold=0.10)
        out_path = Path(__file__).parent / "classification_results.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
