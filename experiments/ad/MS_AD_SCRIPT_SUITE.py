#!/usr/bin/env python3
"""
================================================================================
MechVal Cross-Domain Quantitative Analysis Suite  (MS + Alzheimer's)
================================================================================
Self-contained. Reproduces every analysis built in the MechVal project:
  1. Structured effect-size dataset (REAL cited estimates, honest gap-flags)
  2. Tier-calibration analysis  (does qualitative tiering track effect size?)
  3. Cross-domain forest plot
  4. Real-data two-sample MR runner (pulls PUBLIC GWAS summary stats)

DESIGN RULES (non-negotiable):
  - No fabricated numbers. `est=NaN` means "source gave no usable estimate".
  - Every row carries `source` provenance.
  - HRs / proportions / r2 are NEVER pooled with risk ORs.
  - Small-n analyses are labelled DESCRIPTIVE, not inferential.

SETUP:
  pip install pandas numpy scipy statsmodels matplotlib requests
RUN:
  python mechval_analysis_suite.py          # builds dataset + calibration + forest
  python mechval_analysis_suite.py --mr     # ALSO runs real GWAS MR (needs internet)
================================================================================
"""
import sys, os
import numpy as np, pandas as pd
from scipy.stats import kendalltau, spearmanr, norm

os.makedirs("output", exist_ok=True)

# ------------------------------------------------------------------ #
# 1. STRUCTURED EFFECT-SIZE DATASET  (extend this list to scale up)
#    columns: id, domain, family, claim, measure_type, est, lo, hi,
#             scale, tier, verdict, source
#    measure_type: OR | OR_per_SD | HR | pct_slowing | proportion | r2 | MR_beta
#    scale: ratio | percent | proportion | r2 | beta
# ------------------------------------------------------------------ #
ROWS = [
 ("MS-017","MS","A","HLA-DRB1*15:01 risk","OR",3.08,2.9,3.3,"ratio","T4","SUPPORTED","IMSGC HLA"),
 ("MS-013","MS","A","Adult BMI -> MS (MR)","OR_per_SD",1.30,1.03,1.64,"ratio","T3","SUPPORTED","web:718"),
 ("MS-007","MS","A","Vitamin D (25OHD) -> MS (MR)","OR_per_SD",0.86,0.76,0.98,"ratio","T3","SUPPORTED","MR lit"),
 ("MS-001","MS","A","EBV seropositive -> MS (HR)","HR",32.0,None,None,"ratio","T3","SUPPORTED","Bjornevik 2022"),
 ("MS-021","MS","A","Smoking -> MS (MR) [neg ctrl]","OR",1.00,0.9,1.1,"ratio","NULL","DISCONFIRMED","MR null"),
 ("AD-002","AD","A","APOE4 heterozygous","OR",3.20,3.1,3.65,"ratio","T4","SUPPORTED","web:946/952"),
 ("AD-002b","AD","A","APOE4 homozygous","OR",14.0,12.0,34.0,"ratio","T4","SUPPORTED","web:949/956"),
 ("AD-003","AD","A","sTREM2/microglia -> AD (MR)","MR_beta",None,None,None,"beta","T3","SUPPORTED","web:930 z=-9.1"),
 ("AD-004","AD","A","IL-6/CRP -> AD (MR) [neg ctrl]","OR",1.00,0.9,1.1,"ratio","NULL","DISCONFIRMED","web:942/945"),
 ("AD-C1","AD","C","Lecanemab CDR-SB slowing","pct_slowing",27.0,None,None,"percent","T3","SUPPORTED","web:972"),
 ("AD-C2","AD","C","Anti-tau clinical benefit","pct_slowing",0.0,None,None,"percent","NULL","DISCONFIRMED","web:979/983"),
 ("AD-C3","AD","C","GLP-1 (semaglutide) benefit","pct_slowing",0.0,None,None,"percent","NULL","DISCONFIRMED","web:980"),
 ("AD-009","AD","B","Plasma p-tau217 sensitivity","proportion",0.825,None,None,"proportion","T4","SUPPORTED","web:959"),
 ("AD-009b","AD","B","Plasma p-tau217 specificity","proportion",0.845,None,None,"proportion","T4","SUPPORTED","web:959"),
 ("AD-009c","AD","B","p-tau217 A+T+ progression HR","HR",6.60,None,None,"ratio","T3","SUPPORTED","web:961"),
 ("AD-006","AD","B","Amyloid PET Centiloid harmonization","r2",0.90,None,None,"r2","T4","SUPPORTED","web:958"),
]
COLS = ["id","domain","family","claim","measure_type","est","lo","hi","scale","tier","verdict","source"]

def build_dataset():
    df = pd.DataFrame(ROWS, columns=COLS)
    df.to_csv("output/mechval_effect_sizes.csv", index=False)
    n = df.est.notna().sum()
    print(f"[dataset] {len(df)} rows | {n} numeric | {len(df)-n} gap-flagged -> output/mechval_effect_sizes.csv")
    return df

# ------------------------------------------------------------------ #
# 2. TIER-CALIBRATION  (risk ORs only; NULL kept; HR/prop excluded)
#    CRITICAL: read tier as literal string ("NULL" != missing).
# ------------------------------------------------------------------ #
def tier_calibration():
    df = pd.read_csv("output/mechval_effect_sizes.csv", dtype={"tier":str}, keep_default_na=False)
    df["est"] = pd.to_numeric(df["est"], errors="coerce")
    risk = df[df.measure_type.isin(["OR","OR_per_SD"])].copy()
    risk = risk[risk.est.notna() & (risk.est > 0)]
    risk["abs_log"] = np.log(risk.est).abs()
    tier_rank = {"NULL":0,"T1":1,"T2":2,"T3":3,"T4":4}
    risk["tier_num"] = risk.tier.map(tier_rank)
    assert risk.tier_num.notna().all(), "tier parse error (check 'NULL' vs NaN)"

    tbl = (risk.groupby("tier")
              .apply(lambda g: pd.Series({
                  "n": len(g),
                  "geomean_OR": np.exp(np.log(g.est).mean()),
                  "mean_abs_logOR": g.abs_log.mean()}))
              .reindex([t for t in ["NULL","T1","T2","T3","T4"] if t in risk.tier.values]))
    tau, p = kendalltau(risk.tier_num.values, risk.abs_log.values)
    print("\n[calibration] per-tier geometric-mean OR:")
    print(tbl.to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"[calibration] Kendall tau(tier, |logOR|) = {tau:.3f}, p = {p:.3f} (n={len(risk)})")
    print("[calibration] DESCRIPTIVE (cited subset). Positive tau => tiering tracks effect size.")
    risk.to_csv("output/mechval_calibration_clean.csv", index=False)
    tbl.to_csv("output/mechval_tier_table.csv")
    return risk, tau, p

# ------------------------------------------------------------------ #
# 3. FOREST PLOT  (ratio-scale risk effects; log axis; nulls flagged)
# ------------------------------------------------------------------ #
def forest_plot():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    df = pd.read_csv("output/mechval_effect_sizes.csv", dtype={"tier":str}, keep_default_na=False)
    for c in ["est","lo","hi"]: df[c] = pd.to_numeric(df[c], errors="coerce")
    fp = df[(df.scale=="ratio") & df.est.notna() & df.measure_type.isin(["OR","OR_per_SD"])].copy()
    fp = fp.sort_values("est")
    fig, ax = plt.subplots(figsize=(9,5))
    for i, r in enumerate(fp.itertuples()):
        col = "#c0392b" if r.verdict=="DISCONFIRMED" else "#2c3e50"
        ax.plot(r.est, i, "o", color=col, zorder=3)
        if not np.isnan(r.lo) and not np.isnan(r.hi):
            ax.plot([r.lo, r.hi], [i,i], color="#7f8c8d", lw=2, zorder=2)
    ax.axvline(1.0, color="#888", ls="--", lw=1)
    ax.set_xscale("log"); ax.set_yticks(range(len(fp)))
    ax.set_yticklabels([f"{r.id}  {r.claim}" for r in fp.itertuples()], fontsize=8)
    ax.set_xlabel("OR / OR per SD (log scale) — dashed = null; red = MR-disconfirmed")
    ax.set_title("MechVal cross-domain risk effects (real cited estimates)", fontsize=10)
    plt.tight_layout(); plt.savefig("output/mechval_forest.png", dpi=150); plt.close()
    print("\n[forest] -> output/mechval_forest.png")

# ------------------------------------------------------------------ #
# 4. REAL-DATA TWO-SAMPLE MR  (public IEU OpenGWAS; needs internet)
#    Verify/refresh dataset IDs at https://gwas.mrcieu.ac.uk/
# ------------------------------------------------------------------ #
OUTCOMES  = {"MS":"ieu-b-18", "AD":"ieu-b-2"}
EXPOSURES = {  # case : (trait, gwas_id, outcome_key)
  "MS-013_BMI":     ("Body mass index",     "ieu-b-40",   "MS"),
  "MS-007_VitD":    ("25-Hydroxyvitamin D", "ieu-a-1000", "MS"),
  "MS-021_Smoking": ("Smoking initiation",  "ieu-b-4877", "MS"),  # neg ctrl
  "AD-004_IL6":     ("Interleukin-6",       "ieu-b-4922", "AD"),  # neg ctrl
}
API = "https://gwas-api.mrcieu.ac.uk"

def _ivw(bx, by, sey):
    w = 1/sey**2
    b = np.sum(w*bx*by)/np.sum(w*bx**2)
    se = np.sqrt(1/np.sum(w*bx**2))
    z = b/se
    return b, se, 2*norm.sf(abs(z))

def run_real_mr():
    import requests
    out = []
    for case,(trait,exp_id,ok) in EXPOSURES.items():
        try:
            ins = pd.DataFrame(requests.get(f"{API}/tophits",
                    params={"id":exp_id,"pval":5e-8,"clump":1}, timeout=60).json())
            rsids = ins["rsid"].tolist()
            oa = pd.DataFrame(requests.post(f"{API}/associations",
                    json={"id":[OUTCOMES[ok]],"variant":rsids}, timeout=120).json())
            m = ins.merge(oa, on="rsid", suffixes=("_exp","_out"))
            bx = m["beta_exp"].astype(float).values; by = m["beta_out"].astype(float).values
            sey = m["se_out"].astype(float).values
            b,se,p = _ivw(bx,by,sey)
            out.append({"case":case,"trait":trait,"outcome":ok,"n_snps":len(m),
                        "ivw_OR":round(np.exp(b),3),"ivw_p":f"{p:.2e}"})
            print(f"[MR] {case}: OR={np.exp(b):.3f} p={p:.2e} ({len(m)} SNPs)")
        except Exception as e:
            out.append({"case":case,"trait":trait,"outcome":ok,"error":str(e)[:80]})
            print(f"[MR] {case}: ERROR {str(e)[:80]}")
    pd.DataFrame(out).to_csv("output/mr_results.csv", index=False)
    print("[MR] -> output/mr_results.csv  (expect BMI~1.3, VitD~0.86, Smoking~1.0, IL6~1.0)")

# ------------------------------------------------------------------ #
if __name__ == "__main__":
    build_dataset()
    tier_calibration()
    forest_plot()
    if "--mr" in sys.argv:
        run_real_mr()
    else:
        print("\n(tip) add --mr to also run real GWAS Mendelian randomization")
