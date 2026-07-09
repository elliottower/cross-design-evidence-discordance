"""
Reviewer-requested analyses for Frontiers in Pharmacology submission.

Analyses:
  R1: Minikel cross-tabulation — match our 41 families to Minikel 2024 genetic support
  R2: Contrast-type sensitivity — accuracy by MR instrument type
  R3: Power calculation — what n is needed for the 2-way split
  R4: Ascertainment estimate — what fraction of scorable families we cover

Pre-registration note: Matching rules for R1 are specified in GENE_TARGET_MAP
below. This file should be committed BEFORE running against Minikel data.

Usage:
  cd paper/reference && uv run --with scipy python reviewer_analyses.py
"""

import math
from collections import Counter

from classify_families import (
    AUTOIMMUNE_FAMILIES,
    CARDIO_FAMILIES,
    EXTENSION_FAMILIES,
    NEURO_FAMILIES,
    run_classification,
)

ALL_FAMILIES = NEURO_FAMILIES + CARDIO_FAMILIES + AUTOIMMUNE_FAMILIES + EXTENSION_FAMILIES

# ============================================================
# R1: Minikel cross-tabulation
# ============================================================
# Map our mechanism families to gene targets that would appear in the
# Minikel 2024 dataset (gene name + indication).
# Rules: use the primary MR instrument gene. If the MR instrument is a
# biomarker (e.g., CRP, homocysteine), use the gene encoding the target
# protein or the primary GWAS hit.
#
# Format: family_name -> {gene: str, indication: str, instrument_type: str}
# instrument_type: "cis_pqtl", "coding_variant", "polygenic", "biomarker_gwas"

GENE_TARGET_MAP = {
    # Neuro
    "Metabolic-AD":     {"gene": "multiple", "indication": "Alzheimer's disease",
                         "instrument_type": "polygenic", "notes": "T2D polygenic score"},
    "ModRisk-AD":       {"gene": "multiple", "indication": "Alzheimer's disease",
                         "instrument_type": "polygenic", "notes": "Modifiable risk factors"},
    "Anti-CD20-MS":     {"gene": "FCRL3", "indication": "Multiple sclerosis",
                         "instrument_type": "cis_pqtl"},
    "Smoking-MS/AD":    {"gene": "multiple", "indication": "Multiple sclerosis",
                         "instrument_type": "polygenic", "notes": "Smoking polygenic score"},
    "HRT-AD":           {"gene": "ESR1", "indication": "Alzheimer's disease",
                         "instrument_type": "biomarker_gwas", "notes": "Estradiol"},
    "BMI-MS":           {"gene": "multiple", "indication": "Multiple sclerosis",
                         "instrument_type": "polygenic"},
    "BMI-AD":           {"gene": "multiple", "indication": "Alzheimer's disease",
                         "instrument_type": "polygenic"},
    "VitaminD-MS":      {"gene": "CYP2R1", "indication": "Multiple sclerosis",
                         "instrument_type": "biomarker_gwas", "notes": "25(OH)D"},
    "EBV-MS":           {"gene": "HLA", "indication": "Multiple sclerosis",
                         "instrument_type": "coding_variant", "notes": "HLA-DRB1*15:01"},
    # Cardio
    "HDL/CETP":         {"gene": "CETP", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl"},
    "Niacin/HDL":       {"gene": "CETP", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl", "notes": "Shared with HDL/CETP"},
    "Homocysteine":     {"gene": "MTHFR", "indication": "Coronary heart disease",
                         "instrument_type": "coding_variant", "notes": "C677T"},
    "CRP":              {"gene": "CRP", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl"},
    "Uric acid":        {"gene": "SLC2A9", "indication": "Coronary heart disease",
                         "instrument_type": "biomarker_gwas"},
    "LDL/PCSK9":        {"gene": "PCSK9", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl"},
    "Blood pressure":   {"gene": "multiple", "indication": "Coronary heart disease",
                         "instrument_type": "polygenic"},
    "Triglycerides":    {"gene": "LPL", "indication": "Coronary heart disease",
                         "instrument_type": "biomarker_gwas"},
    "Lp(a)":            {"gene": "LPA", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl"},
    "IL-6R":            {"gene": "IL6R", "indication": "Coronary heart disease",
                         "instrument_type": "cis_pqtl"},
    # Autoimmune
    "IL-23-psoriasis":  {"gene": "IL23R", "indication": "Psoriasis",
                         "instrument_type": "coding_variant"},
    "CTLA-4-RA":        {"gene": "CTLA4", "indication": "Rheumatoid arthritis",
                         "instrument_type": "coding_variant"},
    "TNF-a-RA":         {"gene": "TNF", "indication": "Rheumatoid arthritis",
                         "instrument_type": "biomarker_gwas"},
    "IL-17-psoriasis":  {"gene": "IL17A", "indication": "Psoriasis",
                         "instrument_type": "biomarker_gwas"},
    "JAK-STAT-RA":      {"gene": "STAT4", "indication": "Rheumatoid arthritis",
                         "instrument_type": "coding_variant"},
    "CD20-RA":          {"gene": "FCRL3", "indication": "Rheumatoid arthritis",
                         "instrument_type": "coding_variant"},
    "IL-4Ra-AD":        {"gene": "IL4R", "indication": "Atopic dermatitis",
                         "instrument_type": "cis_pqtl"},
    "IL-1b-CVD":        {"gene": "IL1B", "indication": "Coronary heart disease",
                         "instrument_type": "biomarker_gwas"},
    # Extension
    "VitD-Cancer":      {"gene": "CYP2R1", "indication": "Colorectal cancer",
                         "instrument_type": "biomarker_gwas"},
    "IGF1-CRC":         {"gene": "IGF1", "indication": "Colorectal cancer",
                         "instrument_type": "biomarker_gwas"},
    "Estrogen-BC":      {"gene": "CYP19A1", "indication": "Breast cancer",
                         "instrument_type": "biomarker_gwas"},
    "Eos/IL5-Asthma":   {"gene": "IL5", "indication": "Asthma",
                         "instrument_type": "biomarker_gwas"},
    "IL4Ra-Asthma":     {"gene": "IL4R", "indication": "Asthma",
                         "instrument_type": "cis_pqtl"},
    "TSLP-Asthma":      {"gene": "TSLP", "indication": "Asthma",
                         "instrument_type": "cis_pqtl"},
    "SGLT2-HF":         {"gene": "SLC5A2", "indication": "Heart failure",
                         "instrument_type": "cis_pqtl"},
    "GLP1R-T2D/Obesity":{"gene": "GLP1R", "indication": "Type 2 diabetes",
                         "instrument_type": "cis_pqtl"},
    "Urate-Gout":       {"gene": "SLC2A9", "indication": "Gout",
                         "instrument_type": "biomarker_gwas"},
    "IL6-MDD":          {"gene": "IL6R", "indication": "Major depressive disorder",
                         "instrument_type": "cis_pqtl"},
    "IL23-Crohns":      {"gene": "IL23R", "indication": "Crohn's disease",
                         "instrument_type": "coding_variant"},
    "Complement-GA":    {"gene": "CFH", "indication": "Age-related macular degeneration",
                         "instrument_type": "coding_variant"},
    "Sclerostin-Fracture": {"gene": "SOST", "indication": "Osteoporotic fracture",
                         "instrument_type": "cis_pqtl"},
    "Serotonin-MDD":    {"gene": "SLC6A4", "indication": "Major depressive disorder",
                         "instrument_type": "coding_variant"},
}


# Map our gene targets to Minikel MeSH indication terms
# These are the EXACT MeSH terms used in Minikel's table_s01.tsv
MINIKEL_INDICATION_MAP = {
    "Alzheimer's disease": "Alzheimer Disease",
    "Multiple sclerosis": "Multiple Sclerosis",
    "Coronary heart disease": "Cardiovascular Diseases",
    "Psoriasis": "Psoriasis",
    "Rheumatoid arthritis": "Arthritis, Rheumatoid",
    "Atopic dermatitis": "Dermatitis, Atopic",
    "Colorectal cancer": "Colorectal Neoplasms",
    "Breast cancer": "Breast Neoplasms",
    "Asthma": "Asthma",
    "Heart failure": "Heart Failure",
    "Type 2 diabetes": "Diabetes Mellitus, Type 2",
    "Gout": "Gout",
    "Major depressive disorder": "Depressive Disorder, Major",
    "Crohn's disease": "Crohn Disease",
    "Age-related macular degeneration": "Macular Degeneration",
    "Osteoporotic fracture": "Osteoporotic Fractures",
}


def r1_minikel_cross_tab():
    """Cross-tabulate our families against Minikel 2024 genetic support."""
    import csv
    from pathlib import Path

    print("\n" + "=" * 70)
    print("R1: MINIKEL 2024 CROSS-TABULATION")
    print("=" * 70)

    minikel_path = Path(__file__).parent / "minikel_data" / "table_s01.tsv"
    if not minikel_path.exists():
        print("  ERROR: Minikel data not found. Download from GitHub first.")
        return

    # Load Minikel data into lookup: (gene, mesh_term) -> target_status
    minikel_lookup = {}
    with open(minikel_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            key = (row["target"], row["indication_mesh_term"])
            minikel_lookup[key] = row["target_status"]

    # Match our families
    results = run_classification(ALL_FAMILIES, threshold=0.10)
    scored = [r for r in results
              if r["correct"] is not None and r["prediction"] != "ambiguous"]

    matched = []
    unmatched = []
    for r in scored:
        family = r["family"]
        if family not in GENE_TARGET_MAP:
            unmatched.append((family, "no gene target map"))
            continue

        info = GENE_TARGET_MAP[family]
        gene = info["gene"]
        indication = info["indication"]

        if gene == "multiple":
            unmatched.append((family, "polygenic — no single gene target"))
            continue

        mesh_term = MINIKEL_INDICATION_MAP.get(indication)
        if mesh_term is None:
            unmatched.append((family, f"no MeSH mapping for '{indication}'"))
            continue

        key = (gene, mesh_term)
        minikel_status = minikel_lookup.get(key)

        if minikel_status is None:
            # Try broader search — maybe the gene appears under a related indication
            gene_entries = [(k, v) for k, v in minikel_lookup.items() if k[0] == gene]
            if gene_entries:
                closest = min(gene_entries,
                              key=lambda x: abs(len(x[0][1]) - len(mesh_term)))
                unmatched.append((family,
                    f"{gene}+{mesh_term} not found; "
                    f"closest: {gene}+{closest[0][1]} = {closest[1]}"))
            else:
                unmatched.append((family, f"{gene} not in Minikel dataset"))
            continue

        our_concordant = r["classification"] == "concordance"
        minikel_supported = minikel_status == "genetically supported target"

        matched.append({
            "family": family,
            "gene": gene,
            "indication": mesh_term,
            "our_class": r["classification"],
            "our_correct": r["correct"],
            "minikel_status": minikel_status,
            "our_concordant": our_concordant,
            "minikel_supported": minikel_supported,
            "agree": our_concordant == minikel_supported,
        })

    # Print results
    print(f"\n  Matched: {len(matched)}/{len(scored)} scored families")
    print(f"  Unmatched: {len(unmatched)}")

    print(f"\n  {'Family':<25} {'Gene':<10} {'Our class':<25} "
          f"{'Minikel':<25} {'Agree':>6}")
    print("  " + "-" * 95)
    for m in matched:
        agree_str = "✓" if m["agree"] else "✗"
        print(f"  {m['family']:<25} {m['gene']:<10} {m['our_class']:<25} "
              f"{m['minikel_status']:<25} {agree_str:>6}")

    # 2x2 table
    a = sum(1 for m in matched if m["our_concordant"] and m["minikel_supported"])
    b = sum(1 for m in matched if m["our_concordant"] and not m["minikel_supported"])
    c = sum(1 for m in matched if not m["our_concordant"] and m["minikel_supported"])
    d = sum(1 for m in matched if not m["our_concordant"] and not m["minikel_supported"])

    print(f"\n  2x2 Cross-tabulation:")
    print(f"  {'':>25} Minikel supported  Minikel unsupported")
    print(f"  {'Our concordant':<25} {a:>18} {b:>20}")
    print(f"  {'Our discordant':<25} {c:>18} {d:>20}")

    total = a + b + c + d
    agreement = a + d
    if total > 0:
        print(f"\n  Agreement: {agreement}/{total} = {agreement/total:.1%}")
        from scipy import stats
        _, fisher_p = stats.fisher_exact([[a, b], [c, d]])
        print(f"  Fisher exact p = {fisher_p:.4f}")

    if unmatched:
        print(f"\n  Unmatched families:")
        for fam, reason in unmatched:
            print(f"    - {fam}: {reason}")


def r1_instrument_type_summary():
    """Summarize instrument types across all families."""
    print("\n" + "=" * 70)
    print("R1b: GENE TARGET MAP — INSTRUMENT TYPE SUMMARY")
    print("=" * 70)

    type_counts = Counter()
    for family, info in GENE_TARGET_MAP.items():
        type_counts[info["instrument_type"]] += 1

    for itype, count in type_counts.most_common():
        families = [f for f, info in GENE_TARGET_MAP.items()
                    if info["instrument_type"] == itype]
        print(f"\n  {itype} ({count} families):")
        for f in families:
            print(f"    - {f} -> {GENE_TARGET_MAP[f]['gene']}")

    n_single_gene = sum(1 for info in GENE_TARGET_MAP.values()
                        if info["gene"] != "multiple")
    print(f"\n  Single-gene targets: {n_single_gene}/{len(GENE_TARGET_MAP)}")
    print(f"  Polygenic scores: {type_counts.get('polygenic', 0)}")


# ============================================================
# R2: Contrast-type sensitivity
# ============================================================

def r2_contrast_type_sensitivity():
    """Check whether accuracy varies by MR instrument type."""
    print("\n" + "=" * 70)
    print("R2: ACCURACY BY MR INSTRUMENT TYPE")
    print("=" * 70)

    results = run_classification(ALL_FAMILIES, threshold=0.10)
    scored = [r for r in results
              if r["correct"] is not None and r["prediction"] != "ambiguous"]

    type_results = {}
    for r in scored:
        family = r["family"]
        if family not in GENE_TARGET_MAP:
            continue
        itype = GENE_TARGET_MAP[family]["instrument_type"]
        if itype not in type_results:
            type_results[itype] = {"correct": 0, "total": 0, "families": []}
        type_results[itype]["total"] += 1
        if r["correct"]:
            type_results[itype]["correct"] += 1
        type_results[itype]["families"].append(
            (family, "✓" if r["correct"] else "✗"))

    print(f"\n  {'Type':<20} {'Correct':>8} {'Total':>6} {'Accuracy':>10}")
    print("  " + "-" * 48)
    for itype in ["cis_pqtl", "coding_variant", "biomarker_gwas", "polygenic"]:
        if itype not in type_results:
            continue
        tr = type_results[itype]
        acc = tr["correct"] / tr["total"] if tr["total"] else 0
        print(f"  {itype:<20} {tr['correct']:>8} {tr['total']:>6} {acc:>10.1%}")
        for fam, ok in tr["families"]:
            print(f"    {ok} {fam}")

    print("\n  NOTE: Accuracy differences by instrument type should be interpreted")
    print("  cautiously — cell sizes are small and confounded with domain.")


# ============================================================
# R3: Power calculation for the 2-way split
# ============================================================

def r3_power_calculation():
    """How many misses needed to distinguish null-MR from causal-MR at 80% power?"""
    from scipy import stats

    print("\n" + "=" * 70)
    print("R3: POWER CALCULATION FOR TWO-WAY SPLIT")
    print("=" * 70)

    # Current data: 8 misses split 5 (null-MR) vs 3 (causal-MR)
    # Under H0: misses are equally likely to be null-MR or causal-MR (p=0.5)
    # Under H1: true split is 5/8 = 0.625 null-MR
    # More conservative: what if true split is 0.7 (70% null-MR)?

    observed_p = 5 / 8
    print(f"\n  Observed split: 5/8 = {observed_p:.3f} null-MR")
    print(f"  H0: p = 0.5 (equal probability)")

    # Current power with n=8
    # Exact binomial test: reject H0 if k >= critical value
    for n in [8, 15, 20, 30, 50]:
        for true_p in [0.625, 0.70, 0.75]:
            # Find critical value for alpha=0.05 one-sided
            for k in range(n + 1):
                pval = 1 - stats.binom.cdf(k - 1, n, 0.5)
                if pval <= 0.05:
                    crit = k
                    break
            else:
                crit = n + 1

            # Power = P(k >= crit | true_p)
            power = 1 - stats.binom.cdf(crit - 1, n, true_p)
            if n == 8 or (true_p == 0.70 and power >= 0.79):
                print(f"  n={n:>3}, true_p={true_p:.3f}: "
                      f"crit_k={crit}, power={power:.3f}")

    print("\n  To detect a 70/30 split at 80% power (alpha=0.05):")
    # Find minimum n for 80% power at true_p=0.70
    for n in range(8, 100):
        for k in range(n + 1):
            pval = 1 - stats.binom.cdf(k - 1, n, 0.5)
            if pval <= 0.05:
                crit = k
                break
        else:
            continue
        power = 1 - stats.binom.cdf(crit - 1, n, 0.70)
        if power >= 0.80:
            print(f"  Minimum n = {n} misses (critical k = {crit}, power = {power:.3f})")
            break

    # Fisher exact test on the 2x2 (null-MR success vs failure, causal-MR success vs failure)
    print("\n  Fisher exact test on current 2x2:")
    print("              Success  Failure")
    print("  Null-MR:       5        0     (all succeed despite null MR)")
    print("  Causal-MR:     0        3     (all fail despite causal MR)")
    # This is actually a 2x2: null-MR misses are all successes, causal-MR misses are all failures
    # That's a perfect separation
    _, fisher_p = stats.fisher_exact([[5, 0], [0, 3]])
    print(f"  Fisher exact p = {fisher_p:.4f}")
    print("  The split is perfectly clean — every null-MR miss is a success,")
    print("  every causal-MR miss is a failure. The question is sample size,")
    print("  not effect size.")


# ============================================================
# R4: Ascertainment estimate
# ============================================================

def r4_ascertainment_estimate():
    """Estimate what fraction of scorable mechanism families we cover."""
    print("\n" + "=" * 70)
    print("R4: ASCERTAINMENT ESTIMATE")
    print("=" * 70)

    # Count our families by status
    results = run_classification(ALL_FAMILIES, threshold=0.10)
    scored = [r for r in results
              if r["correct"] is not None and r["prediction"] != "ambiguous"]
    pending = [r for r in results if r["drug_outcome"] == "Pending"]
    construct = [r for r in results if r["drug_outcome"] == "Construct-limited"]

    print(f"\n  Our dataset:")
    print(f"    Scored:            {len(scored)}")
    print(f"    Pending:           {len(pending)}")
    print(f"    Construct-limited: {len(construct)}")
    print(f"    Total:             {len(results)}")

    # Estimate of universe: Minikel 2024 reports genetic support analysis
    # for ~30,000 target-indication pairs. Of these, ~3,000 have been in
    # clinical trials. We operate at the mechanism-family level, which is
    # coarser. Rough estimate of mechanism families with both published MR
    # AND unambiguous Phase III outcomes:
    print(f"\n  Estimated universe of scorable mechanism families:")
    print(f"    Minikel 2024 analyzed ~30,000 target-indication pairs")
    print(f"    Of which ~3,000 have been in clinical trials")
    print(f"    At mechanism-family granularity (coarser than target-indication),")
    print(f"    ~100-200 families have BOTH published drug-target MR evidence")
    print(f"    AND unambiguous Phase III outcomes.")
    print(f"    Our 41 families represent roughly 20-40% of this universe.")
    print(f"    Our 32 scored families represent ~15-30%.")
    print(f"\n  Key ascertainment biases:")
    print(f"    1. Overrepresents well-studied pathways (amyloid, LDL, B-cell)")
    print(f"    2. Overrepresents domains with strong MR traditions (cardio, neuro)")
    print(f"    3. Underrepresents rare diseases, pediatric indications, CNS beyond AD/MS")
    print(f"    4. Extension domains partially mitigate bias (7 new domains)")

    # Domains covered vs possible
    domains_covered = set(r["domain"] for r in results)
    print(f"\n  Domains covered: {len(domains_covered)} ({', '.join(sorted(domains_covered))})")
    print(f"  Major domains NOT covered: infectious disease, hematology,")
    print(f"    nephrology, hepatology, dermatology (beyond psoriasis)")


# ============================================================
# R5: Supplementary CSV generation
# ============================================================

def r5_generate_csv():
    """Generate machine-readable CSV of all effect sizes."""
    import csv
    from pathlib import Path

    print("\n" + "=" * 70)
    print("R5: GENERATING SUPPLEMENTARY CSV")
    print("=" * 70)

    results = run_classification(ALL_FAMILIES, threshold=0.10)

    fieldnames = [
        "family", "domain", "gene_target", "instrument_type",
        "obs_d", "obs_type", "obs_class",
        "mr_or_raw", "mr_d", "mr_ci", "mr_class",
        "classification", "prediction", "drug_outcome", "correct",
        "status",
    ]

    out_path = Path(__file__).parent / "supplementary_table_S1.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            gene_info = GENE_TARGET_MAP.get(r["family"], {})
            status = "pre-registered" if r["domain"] in ["neuro", "cardio", "autoimmune"] else "extension"
            if r["drug_outcome"] in ("Pending", "Construct-limited"):
                status = r["drug_outcome"].lower()
            writer.writerow({
                "family": r["family"],
                "domain": r["domain"],
                "gene_target": gene_info.get("gene", ""),
                "instrument_type": gene_info.get("instrument_type", ""),
                "obs_d": r["obs_d"],
                "obs_type": r["obs_type"],
                "obs_class": r["obs_class"],
                "mr_or_raw": r["gen_OR_raw"],
                "mr_d": r["gen_d"],
                "mr_ci": r["gen_CI"],
                "mr_class": r["mr_class"],
                "classification": r["classification"],
                "prediction": r["prediction"],
                "drug_outcome": r["drug_outcome"],
                "correct": r["correct"],
                "status": status,
            })

    print(f"  Saved to {out_path}")
    print(f"  {len(results)} rows, {len(fieldnames)} columns")


# ============================================================
# R6: MR contrast-scale sensitivity
# ============================================================
# Reviewer M2: The d=0.10 threshold is applied uniformly across MR
# effect sizes on different contrasts (per-SD, per-allele, per-unit,
# per-genotype). This analysis documents:
#   1. What contrast each scored family's MR d is expressed in
#   2. Which families are within 0.03 of the threshold (threshold-sensitive)
#   3. Whether per-SD rescaling is feasible and what it would change
#
# Pre-registration: This analysis committed before execution.
# The key question: does the contrast type systematically affect
# which side of d=0.10 a family falls on?

# MR contrast type for each family, derived from the source papers.
# "per_sd" = MR OR expressed per 1 SD of the exposure
# "per_allele" = MR OR per copy of a specific allele
# "per_unit" = MR OR per fixed-unit change (e.g., per 5 umol/L, per 10 mmHg)
# "per_genotype" = MR OR comparing homozygous genotypes (e.g., MTHFR TT vs CC)
# "null_signal" = MR OR effectively 1.00, contrast type irrelevant
MR_CONTRAST_TYPES = {
    # Neuro
    "Metabolic-AD": "per_sd",
    "ModRisk-AD": "per_sd",
    "Anti-CD20-MS": "per_sd",        # per-SD circulating FCRL3
    "Smoking-MS/AD": "per_sd",
    "HRT-AD": "per_sd",             # per-SD estradiol
    "BMI-MS": "per_sd",             # per-SD BMI
    "BMI-AD": "per_sd",             # per-SD BMI
    "VitaminD-MS": "per_sd",        # per-SD 25(OH)D
    "EBV-MS": "per_allele",         # HLA-DRB1*15:01 carrier status
    # Cardio
    "HDL/CETP": "per_sd",           # per-SD HDL-C
    "Niacin/HDL": "per_sd",
    "Homocysteine": "per_genotype", # MTHFR TT vs CC
    "CRP": "per_unit",              # per 20% lower CRP
    "Uric acid": "per_sd",
    "LDL/PCSK9": "per_unit",        # per 1 mmol/L LDL
    "Blood pressure": "per_unit",   # per 10 mmHg SBP
    "Triglycerides": "per_unit",    # per 1 mmol/L TG
    "Lp(a)": "per_unit",            # per 10 mg/dL Lp(a)
    "IL-6R": "per_sd",              # rescaled from per-allele to per-SD
    # Autoimmune
    "IL-23-psoriasis": "per_allele",
    "CTLA-4-RA": "per_allele",
    "TNF-a-RA": "null_signal",      # OR = 1.00
    "IL-17-psoriasis": "null_signal",
    "JAK-STAT-RA": "per_allele",
    "CD20-RA": "per_allele",
    "IL-4Ra-AD": "null_signal",
    "IL-1b-CVD": "null_signal",
    # Extension
    "VitD-Cancer": "per_sd",
    "IGF1-CRC": "per_sd",           # per-SD circulating IGF-1
    "Estrogen-BC": "per_sd",        # per-SD estradiol
    "Eos/IL5-Asthma": "per_sd",     # per-SD eosinophil count
    "IL4Ra-Asthma": "unknown",
    "TSLP-Asthma": "unknown",
    "SGLT2-HF": "per_sd",           # drug-target MR cis-eQTL
    "Urate-Gout": "per_sd",
    "GLP1R-T2D/Obesity": "unknown",
    "IL6-MDD": "per_unit",          # per 20% lower CRP
    "Serotonin-MDD": "per_allele",  # 5-HTTLPR
    "IL23-Crohns": "per_allele",
    "Complement-GA": "per_allele",  # CFH Y402H
    "Sclerostin-Frac": "per_sd",    # SOST cis-MR
}


def r6_scale_sensitivity():
    """Analyze how MR contrast type affects threshold classifications."""
    print("\n" + "=" * 70)
    print("R6: MR CONTRAST-SCALE SENSITIVITY")
    print("=" * 70)

    results = run_classification(ALL_FAMILIES, threshold=0.10)
    scored = [r for r in results
              if r["correct"] is not None and r["prediction"] != "ambiguous"]

    print(f"\n  Scored families by MR contrast type:")
    print(f"  {'Family':<25} {'MR d':>8} {'MR class':>10} {'Contrast':>15} "
          f"{'Thresh-sens':>12} {'Correct':>8}")
    print("  " + "-" * 82)

    contrast_counts = {}
    threshold_sensitive = []

    for r in scored:
        family = r["family"]
        contrast = MR_CONTRAST_TYPES.get(family, "unknown")
        d = r["gen_d"]
        sensitive = abs(d - 0.10) < 0.03 and d > 0  # within 0.03 of threshold
        ok = "✓" if r["correct"] else "✗"

        if contrast not in contrast_counts:
            contrast_counts[contrast] = {"total": 0, "correct": 0, "families": []}
        contrast_counts[contrast]["total"] += 1
        if r["correct"]:
            contrast_counts[contrast]["correct"] += 1
        contrast_counts[contrast]["families"].append(family)

        if sensitive:
            threshold_sensitive.append((family, d, contrast, r["correct"]))

        print(f"  {family:<25} {d:>8.3f} {r['mr_class']:>10} {contrast:>15} "
              f"{'YES' if sensitive else '':>12} {ok:>8}")

    print(f"\n  Summary by contrast type:")
    print(f"  {'Contrast':<15} {'Correct':>8} {'Total':>6} {'Accuracy':>10}")
    print("  " + "-" * 42)
    for ctype in ["per_sd", "per_allele", "per_unit", "per_genotype", "null_signal"]:
        if ctype not in contrast_counts:
            continue
        cc = contrast_counts[ctype]
        acc = cc["correct"] / cc["total"] if cc["total"] else 0
        print(f"  {ctype:<15} {cc['correct']:>8} {cc['total']:>6} {acc:>10.1%}")

    print(f"\n  Threshold-sensitive families (MR d within 0.03 of 0.10):")
    if threshold_sensitive:
        for fam, d, contrast, correct in threshold_sensitive:
            ok = "✓" if correct else "✗"
            # What rescaling factor would flip this family?
            if d > 0.10:
                flip_factor = 0.10 / d
                print(f"  {ok} {fam}: d={d:.3f} ({contrast}), "
                      f"would flip to null if rescaled by {flip_factor:.2f}x")
            elif d > 0:
                flip_factor = 0.10 / d
                print(f"  {ok} {fam}: d={d:.3f} ({contrast}), "
                      f"would flip to causal if rescaled by {flip_factor:.2f}x")
    else:
        print("  (none)")

    # Key finding: can we rescale all to per-SD?
    print(f"\n  Rescaling feasibility:")
    n_per_sd = sum(1 for r in scored
                   if MR_CONTRAST_TYPES.get(r["family"]) == "per_sd")
    n_other = len(scored) - n_per_sd
    n_null = sum(1 for r in scored
                 if MR_CONTRAST_TYPES.get(r["family"]) == "null_signal")
    print(f"  Per-SD MR effects: {n_per_sd}/{len(scored)} scored families")
    print(f"  Null signals (contrast irrelevant): {n_null}/{len(scored)}")
    print(f"  Non-per-SD, non-null: {n_other - n_null}/{len(scored)}")
    print(f"  Universal per-SD rescaling is NOT feasible: conversion factors")
    print(f"  (SD of exposure per allele/unit) are not available for most")
    print(f"  non-per-SD families. Only IL-6R is explicitly rescaled in the paper.")


def main():
    r1_minikel_cross_tab()
    r1_instrument_type_summary()
    r2_contrast_type_sensitivity()
    r3_power_calculation()
    r4_ascertainment_estimate()
    r5_generate_csv()
    r6_scale_sensitivity()


if __name__ == "__main__":
    main()
