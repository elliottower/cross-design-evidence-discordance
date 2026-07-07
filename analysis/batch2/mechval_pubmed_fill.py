#!/usr/bin/env python3
"""
mechval_pubmed_fill.py
Auto-fill gap_reason rows in mechval_effect_sizes_v2.csv toward n>=30.
Run OUTSIDE the sandbox (needs internet). Honors extension_spec guardrails:
  - never fabricate: if no numeric estimate parsed -> leave NaN + gap_reason
  - one estimate per case per outcome (primary/most-adjusted)
  - tag design (MR/RCT/observational/genetic/diagnostic)
Requires: requests, pandas. Set NCBI_API_KEY env var for 10 req/s.
"""
import os, re, time, requests, pandas as pd

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
API_KEY = os.environ.get("NCBI_API_KEY", "")
DELAY = 0.11 if API_KEY else 0.34   # respect NCBI rate limits

def esearch(term, retmax=5):
    p = {"db":"pubmed","term":term,"retmax":retmax,"retmode":"json"}
    if API_KEY: p["api_key"]=API_KEY
    r = requests.get(f"{EUTILS}/esearch.fcgi", params=p, timeout=30)
    time.sleep(DELAY)
    return r.json().get("esearchresult",{}).get("idlist",[])

def efetch_abstract(pmid):
    p = {"db":"pubmed","id":pmid,"rettype":"abstract","retmode":"text"}
    if API_KEY: p["api_key"]=API_KEY
    r = requests.get(f"{EUTILS}/efetch.fcgi", params=p, timeout=30)
    time.sleep(DELAY)
    return r.text

NUM = r'(\d+[.\u00b7]?\d*)'

PATTERNS = [
    # "ratio, 95% CI 0\u00b770 0\u00b757-0\u00b786" (Lancet: all 3 nums after CI marker)
    re.compile(
        r"(?:OR|HR|RR|odds\s*ratio|hazard\s*ratio|risk\s*ratio)"
        r"[^0-9]{0,15}"
        r"(?:95\s*%?\s*(?:CI|confidence\s*interval))[^0-9]{0,10}"
        + NUM + r"\s+" + NUM + r"\s*[-\u2013to]+\s*" + NUM,
        re.IGNORECASE),
    # "HR 0\u00b770, 95% CI 0\u00b757-0\u00b786" (estimate before CI marker)
    re.compile(
        r"(?:OR|HR|RR|odds\s*ratio|hazard\s*ratio|risk\s*ratio)"
        r"[^0-9]{0,15}" + NUM + r"[^0-9]{0,30}"
        r"(?:95\s*%?\s*(?:CI|confidence\s*interval))[^0-9]{0,10}"
        + NUM + r"\s*[-\u2013to]+\s*" + NUM,
        re.IGNORECASE),
    # "[odds ratio (OR) = 1.10, 95% confidence interval (CI) 0.8-1.5"
    re.compile(
        r"(?:OR|HR|RR|odds\s*ratio|hazard\s*ratio|risk\s*ratio)"
        r"[^0-9]{0,20}" + NUM + r"[^0-9]{0,50}"
        r"(?:95\s*%?\s*(?:CI|confidence\s*interval))[^0-9]{0,15}"
        + NUM + r"\s*[-\u2013to]+\s*" + NUM,
        re.IGNORECASE),
    # "OR = 3.06 (2.81-3.33)" parenthesized CI
    re.compile(
        r"(?:OR|HR|RR|odds\s*ratio|hazard\s*ratio|risk\s*ratio)"
        r"[^0-9]{0,15}" + NUM + r"\s*\(\s*"
        + NUM + r"\s*[-\u2013to]+\s*" + NUM + r"\s*\)",
        re.IGNORECASE),
]

def _norm_num(s):
    return float(s.replace('\u00b7', '.'))

def parse_primary(text):
    for pat in PATTERNS:
        m = pat.search(text)
        if m:
            return tuple(_norm_num(x) for x in m.groups())
    return (None, None, None)

def guess_design(text):
    t = text.lower()
    if "mendelian randomization" in t or "instrumental variable" in t: return "MR"
    if "randomi" in t and ("trial" in t or "placebo" in t): return "RCT"
    if "sensitivity" in t and "specificity" in t: return "diagnostic"
    if "genome-wide" in t or "allele" in t: return "genetic"
    return "observational"

def parse_ci_only(text):
    """Parse just a CI from abstract text (for rows that already have estimates)."""
    m = PAT.search(text)
    if not m: return (None, None)
    _, lo, hi = (float(x) for x in m.groups())
    return (lo, hi)


def fill_gaps(csv_in, csv_out, estimate_terms=None, ci_terms=None):
    """Two-pass fill: (1) missing estimates, (2) missing CIs on existing estimates."""
    df = pd.read_csv(csv_in)
    estimate_terms = estimate_terms or {}
    ci_terms = ci_terms or {}
    filled_est, filled_ci, failed = 0, 0, 0

    # Pass 1: fill missing estimates
    for i, row in df.iterrows():
        if pd.notna(row.get("estimate")):
            continue
        cid = row["case_id"]
        if cid not in estimate_terms:
            continue
        print(f"  [{cid}] searching for estimate...")
        pmids = esearch(estimate_terms[cid], retmax=5)
        for pmid in pmids:
            abs_txt = efetch_abstract(pmid)
            est, lo, hi = parse_primary(abs_txt)
            if est is not None:
                df.loc[i, ["estimate", "ci_low", "ci_high"]] = [est, lo, hi]
                df.loc[i, "design"] = guess_design(abs_txt)
                df.loc[i, "provenance"] = f"PMID:{pmid} (eutils auto)"
                df.loc[i, "gap_reason"] = ""
                df.loc[i, "extracted_by"] = "eutils auto-parse (needs biostat check)"
                filled_est += 1
                print(f"    -> FOUND: est={est}, CI=({lo}, {hi}) from PMID:{pmid}")
                break
        else:
            df.loc[i, "gap_reason"] = "no parseable primary estimate in top abstracts"
            failed += 1
            print(f"    -> MISS: no parseable estimate in {len(pmids)} abstracts")

    # Pass 2: fill missing CIs on rows that already have estimates
    for i, row in df.iterrows():
        if pd.isna(row.get("estimate")):
            continue
        if pd.notna(row.get("ci_low")) and pd.notna(row.get("ci_high")):
            continue
        cid = row["case_id"]
        if cid not in ci_terms:
            continue
        known_est = float(row["estimate"])
        print(f"  [{cid}] searching for CI (estimate={known_est})...")
        pmids = esearch(ci_terms[cid], retmax=5)
        found = False
        for pmid in pmids:
            abs_txt = efetch_abstract(pmid)
            for pat in PATTERNS:
                for m in pat.finditer(abs_txt):
                    vals = tuple(_norm_num(x) for x in m.groups())
                    if len(vals) == 3:
                        est, lo, hi = vals
                        # the abstract's point estimate must match ours (15% or 0.3 tolerance)
                        est_tol = max(0.15 * abs(known_est), 0.3)
                        if abs(est - known_est) <= est_tol and lo <= est and hi >= est:
                            df.loc[i, ["ci_low", "ci_high"]] = [lo, hi]
                            old_prov = str(df.loc[i, "provenance"])
                            df.loc[i, "provenance"] = f"{old_prov}; CI from PMID:{pmid}"
                            df.loc[i, "extracted_by"] = "eutils auto-parse (needs biostat check)"
                            filled_ci += 1
                            print(f"    -> CI FOUND: ({lo}, {hi}) est_in_abstract={est} from PMID:{pmid}")
                            found = True
                            break
                if found:
                    break
            if found:
                break
        if not found:
            failed += 1
            print(f"    -> CI MISS: no CI containing est={known_est} in {len(pmids)} abstracts")

    df.to_csv(csv_out, index=False)
    n_num = df["estimate"].notna().sum()
    n_ci = (df["ci_low"].notna() & df["ci_high"].notna()).sum()
    print(f"\n=== RESULTS ===")
    print(f"filled -> {csv_out}")
    print(f"  numeric estimates: {n_num}")
    print(f"  rows with CIs:    {n_ci}")
    print(f"  new estimates:     {filled_est}")
    print(f"  new CIs:           {filled_ci}")
    print(f"  failed lookups:    {failed}")
    return df


# --- Search terms for missing estimates ---
ESTIMATE_TERMS = {
    "MS-002": "paramagnetic rim lesion disability multiple sclerosis",
    "MS-011": "ocrelizumab PPMS ORATORIO hazard ratio",
}

# --- Search terms for missing CIs (rows that have estimates but no confidence intervals) ---
# Shorter, broader terms to maximize PubMed hits. Multiple variants for hard cases.
CI_TERMS = {
    "MS-001": "Bjornevik Epstein-Barr virus multiple sclerosis risk",
    "MS-005a": "neurofilament light EDSS multiple sclerosis odds ratio",
    "MS-005b": "neurofilament light progressive multiple sclerosis odds ratio",
    "MS-005c": "neurofilament light rising progression multiple sclerosis",
    "MS-007": "vitamin D Mendelian randomization multiple sclerosis",
    "MS-010": "gray matter volume disability progression multiple sclerosis hazard ratio",
    "MS-013a": "childhood BMI Mendelian randomization multiple sclerosis",
    "MS-013b": "adult BMI Mendelian randomization multiple sclerosis IMSGC",
    "MS-017": "HLA-DRB1 multiple sclerosis odds ratio meta-analysis",
    "AD-002a": "APOE4 heterozygous Alzheimer odds ratio meta-analysis",
    "AD-002b": "APOE4 homozygous Alzheimer odds ratio",
    "AD-002c": "APOE4 women sex Alzheimer odds ratio",
    "AD-004": "interleukin-6 Mendelian randomization Alzheimer",
    "AD-009c": "p-tau217 cognitively unimpaired progression hazard ratio",
}

if __name__ == "__main__":
    import sys
    csv_in = sys.argv[1] if len(sys.argv) > 1 else "../../data/effect_sizes_v2.csv"
    csv_out = sys.argv[2] if len(sys.argv) > 2 else "../../data/effect_sizes_v3.csv"
    fill_gaps(csv_in, csv_out, estimate_terms=ESTIMATE_TERMS, ci_terms=CI_TERMS)
