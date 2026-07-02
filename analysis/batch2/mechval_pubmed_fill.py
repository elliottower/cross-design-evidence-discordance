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

# candidate patterns for the primary/most-adjusted estimate + 95% CI
PAT = re.compile(
    r"(?:OR|HR|RR|odds ratio|hazard ratio|risk ratio)\s*[=:]?\s*"
    r"(\d+\.?\d*)\s*(?:\(|,|;|\s95%?\s*CI[^0-9]*)\s*(\d+\.?\d*)\s*[-\u2013to]+\s*(\d+\.?\d*)",
    re.IGNORECASE)

def parse_primary(text):
    m = PAT.search(text)
    if not m: return (None, None, None)
    return tuple(float(x) for x in m.groups())

def guess_design(text):
    t = text.lower()
    if "mendelian randomization" in t or "instrumental variable" in t: return "MR"
    if "randomi" in t and ("trial" in t or "placebo" in t): return "RCT"
    if "sensitivity" in t and "specificity" in t: return "diagnostic"
    if "genome-wide" in t or "allele" in t: return "genetic"
    return "observational"

def fill_gaps(csv_in="mechval_effect_sizes_v2.csv", csv_out="mechval_effect_sizes_v3.csv",
              search_terms=None):
    df = pd.read_csv(csv_in)
    search_terms = search_terms or {}   # {case_id: "pubmed query"}
    for i,row in df.iterrows():
        if pd.notna(row.get("estimate")): continue         # already have a number
        cid = row["case_id"]
        if cid not in search_terms: continue
        pmids = esearch(search_terms[cid], retmax=3)
        for pmid in pmids:
            abs_txt = efetch_abstract(pmid)
            est,lo,hi = parse_primary(abs_txt)
            if est is not None:
                df.loc[i,["estimate","ci_low","ci_high"]] = [est,lo,hi]
                df.loc[i,"design"] = guess_design(abs_txt)
                df.loc[i,"provenance"] = f"PMID:{pmid} (eutils auto)"
                df.loc[i,"gap_reason"] = ""          # cleared: number recovered
                df.loc[i,"extracted_by"] = "eutils auto-parse (needs biostat check)"
                break
        else:
            df.loc[i,"gap_reason"] = "no parseable primary estimate in top abstracts"
    df.to_csv(csv_out, index=False)
    n_num = df["estimate"].notna().sum()
    print(f"filled -> {csv_out} | numeric rows now: {n_num}")
    return df

# EXAMPLE term map — extend to every gap_reason case (MS 001-052, AD 001-010/C1-C3)
TERMS = {
  "MS-002":"iron rim lesion burden disability progression multiple sclerosis odds ratio",
  "MS-011":"ocrelizumab primary progressive multiple sclerosis disability hazard ratio",
}
if __name__ == "__main__":
    fill_gaps(search_terms=TERMS)
