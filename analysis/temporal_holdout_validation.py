"""Temporal holdout validation: can pre-trial mechanistic tiers predict Phase III outcomes?

For the neuroepidemiology (MS/AD) domain. Uses Llama 3.1-8B via DeepInfra to
assign mechanistic validity tiers to drug mechanisms, then tests whether
higher tiers predict FDA approval.

Design:
  Phase 1 (Leakage check): Ask model if each drug was FDA-approved
  Phase 2 (Tier assignments): Condition B (mechanism only) and C (with evidence)
  Phase 3 (Analysis): Kendall tau and Mann-Whitney U on tiers vs outcomes

Adapted from psychiatric-validity-audit/analysis/temporal_holdout_validation.py

Usage:
    cd /Users/elliottower/Documents/GitHub/neuroepidemiology-validity-audit
    DEEPINFRA_API_KEY=... uv run --with pandas --with scipy --with numpy --with requests \
        python analysis/temporal_holdout_validation.py
"""

import json
import os
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from scipy.stats import kendalltau, mannwhitneyu

DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY", "")
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

TIER_MAP = {
    "proposed": 1,
    "causally suggestive": 2,
    "mechanistically supported": 3,
    "triangulated": 4,
    "validated": 5,
}

TIER_SYSTEM_PROMPT = """You are a scientific evidence evaluator. Classify the mechanistic validity of a proposed therapeutic mechanism for a neurological disease (multiple sclerosis or Alzheimer's disease).

Do NOT consider whether the drug was approved, succeeded, or failed in trials. Focus ONLY on: how well-established is the mechanistic claim itself, based on the scientific evidence?

Use exactly one of these tiers (respond with ONLY the tier name, nothing else):
- Proposed: Mechanism hypothesized based on indirect evidence only
- Causally Suggestive: Some direct evidence (genetic association, animal models, Mendelian randomization) but not confirmed in humans
- Mechanistically Supported: Multiple lines of human evidence supporting the mechanism
- Triangulated: Evidence from 3+ independent methods converging on the same mechanism
- Validated: Mechanism confirmed by convergent interventional and observational evidence"""


def call_model(messages, max_tokens=100, temperature=0.0):
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  API error after 3 attempts: {e}")
                return None


def parse_tier(text):
    if text is None:
        return None
    text_lower = text.lower()
    for tier_name, tier_num in sorted(TIER_MAP.items(), key=lambda x: -len(x[0])):
        if tier_name in text_lower:
            return tier_num
    return None


def run_leakage_check(row):
    drug = row["drug_name"]
    indication = row["indication"]
    actual_outcome = row["fda_outcome"]

    prompt = (
        f"Was the drug {drug} approved by the FDA for {indication}? "
        f"Answer ONLY 'Approved', 'Not approved', or 'Unknown'. One word/phrase only."
    )
    response = call_model([{"role": "user", "content": prompt}], max_tokens=20)
    if response is None:
        return None, False, True

    resp_lower = response.lower()
    if "unknown" in resp_lower or "not sure" in resp_lower or "i don" in resp_lower:
        return response, False, True

    model_says_approved = "approved" in resp_lower and "not" not in resp_lower
    actually_approved = actual_outcome == "Approved"

    is_correct = model_says_approved == actually_approved
    is_clean = not is_correct

    return response, is_correct, is_clean


def run_tier_assignment_no_context(row):
    mechanism = row["target_mechanism"]
    indication = row["indication"]

    prompt = (
        f"Classify the mechanistic validity of: {mechanism} for {indication}. "
        f"Respond with ONLY the tier name."
    )
    response = call_model([
        {"role": "system", "content": TIER_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ], max_tokens=30)
    tier = parse_tier(response)
    return response, tier


def run_tier_assignment_with_context(row):
    mechanism = row["target_mechanism"]
    indication = row["indication"]
    claim = row["mechanistic_claim"]
    mechanism_class = row["mechanism_class"]

    prompt = (
        f"Classify the mechanistic validity of: {mechanism} for {indication}.\n\n"
        f"Mechanism class: {mechanism_class}\n\n"
        f"Evidence summary: {claim}\n\n"
        f"Based on this evidence, respond with ONLY the tier name."
    )
    response = call_model([
        {"role": "system", "content": TIER_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ], max_tokens=30)
    tier = parse_tier(response)
    return response, tier


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/phase3_holdout_dataset.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    if not DEEPINFRA_API_KEY:
        print("ERROR: DEEPINFRA_API_KEY not set")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    print("=" * 72)
    print("TEMPORAL HOLDOUT VALIDATION — NEUROEPIDEMIOLOGY (MS / AD)")
    print(f"Model: {MODEL}")
    print(f"Dataset: {csv_path} ({len(df)} entries)")
    print(f"Generated: {datetime.now().isoformat()}")
    print("=" * 72)

    known_outcome = df[df["fda_outcome"].isin(["Approved", "Failed"])].copy()
    print(f"\nDrugs with known outcomes: {len(known_outcome)}")
    print(f"  Approved: {(known_outcome['fda_outcome'] == 'Approved').sum()}")
    print(f"  Failed: {(known_outcome['fda_outcome'] == 'Failed').sum()}")

    # Show by family
    print(f"\nBy mechanism family:")
    for fam in sorted(known_outcome["family"].unique()):
        sub = known_outcome[known_outcome["family"] == fam]
        a = (sub["fda_outcome"] == "Approved").sum()
        f = (sub["fda_outcome"] == "Failed").sum()
        print(f"  {fam:20s}: {a} approved, {f} failed")

    # ── Phase 1: Leakage check ──
    print("\n" + "=" * 72)
    print("PHASE 1: LEAKAGE CHECK")
    print("=" * 72)

    leakage_results = []
    for i, (idx, row) in enumerate(known_outcome.iterrows()):
        response, is_correct, is_clean = run_leakage_check(row)
        status = "LEAKED" if not is_clean else "CLEAN"
        print(f"  [{i+1:2d}/{len(known_outcome)}] {row['drug_name']:25s} "
              f"({row['fda_outcome']:8s}) -> model: {str(response):20s} [{status}]")
        leakage_results.append({
            "drug": row["drug_name"],
            "indication": row["indication"],
            "family": row["family"],
            "actual_outcome": row["fda_outcome"],
            "model_response": response,
            "model_correct": is_correct,
            "is_clean": is_clean,
            "discordance_edge": row.get("discordance_edge", ""),
        })
        time.sleep(0.2)

    n_clean = sum(r["is_clean"] for r in leakage_results)
    n_leaked = sum(not r["is_clean"] for r in leakage_results)
    print(f"\nLeakage summary: {n_clean} clean, {n_leaked} leaked")

    clean_drugs = {r["drug"] + "|" + r["indication"] for r in leakage_results if r["is_clean"]}

    # ── Phase 2: Tier assignments ──
    print("\n" + "=" * 72)
    print("PHASE 2: TIER ASSIGNMENTS (all drugs with known outcomes)")
    print("=" * 72)

    tier_results = []
    for i, (idx, row) in enumerate(known_outcome.iterrows()):
        drug_key = row["drug_name"] + "|" + row["indication"]
        is_clean = drug_key in clean_drugs

        resp_b, tier_b = run_tier_assignment_no_context(row)
        time.sleep(0.15)
        resp_c, tier_c = run_tier_assignment_with_context(row)
        time.sleep(0.15)

        tag = "CLEAN" if is_clean else "leaked"
        print(f"  [{i+1:2d}/{len(known_outcome)}] {row['drug_name']:25s} "
              f"({row['fda_outcome']:8s}) no_ctx={tier_b} with_ctx={tier_c} [{tag}]")

        tier_results.append({
            "drug": row["drug_name"],
            "brand": row.get("brand_name", ""),
            "indication": row["indication"],
            "mechanism": row["target_mechanism"],
            "mechanism_class": row["mechanism_class"],
            "family": row["family"],
            "actual_outcome": row["fda_outcome"],
            "is_clean": is_clean,
            "tier_no_context": tier_b,
            "tier_with_context": tier_c,
            "response_no_context": resp_b,
            "response_with_context": resp_c,
            "discordance_edge": row.get("discordance_edge", ""),
        })

    # ── Phase 3: Analysis ──
    print("\n" + "=" * 72)
    print("PHASE 3: ANALYSIS")
    print("=" * 72)

    results_df = pd.DataFrame(tier_results)

    analysis_results = {}

    for label, subset in [("ALL drugs", results_df),
                          ("CLEAN drugs only", results_df[results_df["is_clean"]])]:
        print(f"\n--- {label} (n={len(subset)}) ---")
        if len(subset) < 4:
            print("  Too few drugs for analysis")
            continue

        approved = subset[subset["actual_outcome"] == "Approved"]
        failed = subset[subset["actual_outcome"] == "Failed"]
        print(f"  Approved: {len(approved)}, Failed: {len(failed)}")

        label_key = label.lower().replace(" ", "_")
        analysis_results[label_key] = {}

        for tier_col, cond_name in [("tier_no_context", "No context"),
                                     ("tier_with_context", "With context")]:
            valid = subset[subset[tier_col].notna()]
            if len(valid) < 4:
                print(f"  {cond_name}: too few valid tiers")
                continue

            appr_tiers = valid[valid["actual_outcome"] == "Approved"][tier_col].values
            fail_tiers = valid[valid["actual_outcome"] == "Failed"][tier_col].values

            if len(appr_tiers) > 0 and len(fail_tiers) > 0:
                mean_a = np.mean(appr_tiers)
                mean_f = np.mean(fail_tiers)

                outcome_binary = (valid["actual_outcome"] == "Approved").astype(int).values
                tiers = valid[tier_col].values
                tau, p_tau = kendalltau(tiers, outcome_binary)

                try:
                    U, p_u = mannwhitneyu(appr_tiers, fail_tiers, alternative="greater")
                except ValueError:
                    U, p_u = np.nan, np.nan

                print(f"\n  {cond_name}:")
                print(f"    Approved mean tier: {mean_a:.2f} (n={len(appr_tiers)})")
                print(f"    Failed mean tier:   {mean_f:.2f} (n={len(fail_tiers)})")
                print(f"    Difference:         {mean_a - mean_f:+.2f}")
                print(f"    Kendall tau:        {tau:+.3f} (p={p_tau:.4f})")
                print(f"    Mann-Whitney U:     {U:.1f} (p={p_u:.4f}, one-sided: approved > failed)")

                print(f"    Approved tiers: {sorted(appr_tiers)}")
                print(f"    Failed tiers:   {sorted(fail_tiers)}")

                cond_key = cond_name.lower().replace(" ", "_")
                analysis_results[label_key][cond_key] = {
                    "n": len(valid),
                    "n_approved": len(appr_tiers),
                    "n_failed": len(fail_tiers),
                    "mean_approved": float(mean_a),
                    "mean_failed": float(mean_f),
                    "tau": float(tau),
                    "p_tau": float(p_tau),
                    "U": float(U) if not np.isnan(U) else None,
                    "p_U": float(p_u) if not np.isnan(p_u) else None,
                }

    # ── Discordance edge analysis ──
    print("\n" + "=" * 72)
    print("DISCORDANCE EDGE vs OUTCOME")
    print("=" * 72)

    disc_df = results_df[results_df["discordance_edge"].notna() & (results_df["discordance_edge"] != "")].copy()
    if len(disc_df) > 0:
        # Classify discordance as concordant vs discordant
        disc_df["is_discordant"] = disc_df["discordance_edge"].str.contains("null|harmful|mixed", case=False)
        disc_df["is_approved"] = disc_df["actual_outcome"] == "Approved"

        print(f"\nDrugs with discordance edge annotations: {len(disc_df)}")
        concordant_approved = disc_df[~disc_df["is_discordant"] & disc_df["is_approved"]]
        concordant_failed = disc_df[~disc_df["is_discordant"] & ~disc_df["is_approved"]]
        discordant_approved = disc_df[disc_df["is_discordant"] & disc_df["is_approved"]]
        discordant_failed = disc_df[disc_df["is_discordant"] & ~disc_df["is_approved"]]

        print(f"\n  2x2 contingency table:")
        print(f"                    Approved  Failed")
        print(f"  Concordant edge:  {len(concordant_approved):8d}  {len(concordant_failed):6d}")
        print(f"  Discordant edge:  {len(discordant_approved):8d}  {len(discordant_failed):6d}")

        # Success rate by discordance
        conc_total = len(concordant_approved) + len(concordant_failed)
        disc_total = len(discordant_approved) + len(discordant_failed)
        if conc_total > 0 and disc_total > 0:
            conc_rate = len(concordant_approved) / conc_total
            disc_rate = len(discordant_approved) / disc_total
            print(f"\n  Concordant success rate: {conc_rate:.1%} ({len(concordant_approved)}/{conc_total})")
            print(f"  Discordant success rate: {disc_rate:.1%} ({len(discordant_approved)}/{disc_total})")
            print(f"  Ratio: {conc_rate/disc_rate:.1f}x" if disc_rate > 0 else "  Ratio: inf")

        # Per-drug detail
        print(f"\n  Per-drug discordance detail:")
        for _, row in disc_df.iterrows():
            print(f"    {row['drug']:20s} {row['actual_outcome']:8s}  edge={row['discordance_edge']}")

    # ── Save results ──
    os.makedirs(output_dir, exist_ok=True)
    output = {
        "generated": datetime.now().isoformat(),
        "model": MODEL,
        "domain": "neuroepidemiology (MS / AD)",
        "csv_path": csv_path,
        "n_drugs": len(known_outcome),
        "leakage_check": leakage_results,
        "tier_assignments": tier_results,
        "analysis": analysis_results,
        "summary": {
            "n_clean": n_clean,
            "n_leaked": n_leaked,
            "clean_drugs": sorted(clean_drugs),
        },
    }

    json_path = os.path.join(output_dir, "temporal_holdout_results.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nSaved: {json_path}")

    csv_out_path = os.path.join(output_dir, "temporal_holdout_tiers.csv")
    results_df.to_csv(csv_out_path, index=False)
    print(f"Saved: {csv_out_path}")


if __name__ == "__main__":
    main()
