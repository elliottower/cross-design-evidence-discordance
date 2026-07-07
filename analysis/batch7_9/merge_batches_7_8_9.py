"""Merge batches 7-9 into v8 from v7 base.

Handles:
- MS-001 CI update (primary source verified values)
- 16 new rows from batches 7/8/9
- Dedup: skip MS-013b (still no CI), AD-007 (still no ratio-scale)
- Column mapping from batch format to main CSV format
"""
import pandas as pd
import sys

V7 = "data/effect_sizes_v7.csv"
V8 = "data/effect_sizes_v8.csv"
BATCHES = [
    "data/batch7_biomarker_social.csv",
    "data/batch8_ms_anchors.csv",
    "data/batch9_ms_dmt.csv",
]

main_cols = [
    "case_id", "claim", "design", "scale", "estimate", "ci_low", "ci_high",
    "n_cases", "n_controls", "population", "source", "provenance", "verdict",
    "best_tier", "gap_reason", "extracted_by", "extract_date",
]

df = pd.read_csv(V7)

rows_to_add = []
ms001_updated = False

for bpath in BATCHES:
    batch = pd.read_csv(bpath)
    for _, r in batch.iterrows():
        cid = r["case_id"]

        if cid == "MS-001" and not ms001_updated:
            idx = df.index[df.case_id == "MS-001"]
            if len(idx):
                i = idx[0]
                df.at[i, "estimate"] = 32.4
                df.at[i, "ci_low"] = 4.3
                df.at[i, "ci_high"] = 245.0
                df.at[i, "provenance"] = "PMID:35025605 Bjornevik 2022 Science (VERIFIED primary)"
                df.at[i, "gap_reason"] = "UPDATED: HR 32.4(4.3-245) from primary paper"
                ms001_updated = True
            continue

        if cid == "MS-013b":
            continue
        if cid == "AD-007" and pd.isna(r.get("estimate")):
            continue
        if cid == "MS-022" and r.get("scale") == "na":
            continue

        if cid in df.case_id.values:
            continue

        pmid = r.get("PMID", "")
        pmid_str = f"PMID:{int(pmid)} (VERIFIED)" if pd.notna(pmid) and pmid != "" else ""
        source = r.get("source_paper", "")
        notes = r.get("notes", "")
        verdict = r.get("verdict_suggestion", "")
        extracted = r.get("extracted_by", "")

        tier = "T3"
        if verdict == "DISCONFIRMED":
            tier = "T1-T2"
        elif verdict == "CONFLICTED":
            tier = "T2-T3"
        elif "T4" in str(notes):
            tier = "T4"

        new_row = {
            "case_id": cid,
            "claim": r["claim"],
            "design": r["design"],
            "scale": r["scale"] if r.get("scale") != "na" else "",
            "estimate": r.get("estimate"),
            "ci_low": r.get("ci_low"),
            "ci_high": r.get("ci_high"),
            "n_cases": r.get("n_cases"),
            "n_controls": r.get("n_controls"),
            "population": r.get("population", ""),
            "source": source,
            "provenance": pmid_str,
            "verdict": verdict,
            "best_tier": tier,
            "gap_reason": notes,
            "extracted_by": f"{extracted} verified" if "VERIFIED" in str(notes) else extracted,
            "extract_date": r.get("extract_date", "2026-07-02"),
        }
        rows_to_add.append(new_row)

if rows_to_add:
    new_df = pd.DataFrame(rows_to_add, columns=main_cols)
    df = pd.concat([df, new_df], ignore_index=True)

df.to_csv(V8, index=False)

ratio_scales = {"odds ratio", "risk ratio", "hazard ratio", "hazard/rate ratio", "rate ratio", "relative risk"}
ratio = df[df.scale.isin(ratio_scales) & df.estimate.notna()]
has_ci = ratio.ci_low.notna() & ratio.ci_high.notna()
print(f"v8: {len(df)} total rows, {len(ratio)} ratio-scale with estimates, {has_ci.sum()} with CIs")
print(f"New rows added: {len(rows_to_add)}")
print(f"MS-001 CI updated: {ms001_updated}")
for r in rows_to_add:
    ci_tag = f"({r['ci_low']}-{r['ci_high']})" if pd.notna(r.get('ci_low')) else "(no CI)"
    print(f"  + {r['case_id']}: {r['claim'][:40]}  est={r['estimate']} {ci_tag}")
