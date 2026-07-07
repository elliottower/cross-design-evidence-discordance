#!/usr/bin/env python3
"""
mechval_meta.py  — Phase 2 DerSimonian-Laird random-effects pooling.
Pools ONLY within homogeneous (domain, design, ratio-scale) clusters.
Requires CIs to weight studies; rows without CIs are excluded + flagged.
Reports pooled est, 95% CI, I2, tau2, 95% prediction interval.
Egger's test auto-runs when k>=10. Run after eutils fill so CIs are present.
"""
import numpy as np, pandas as pd
from scipy.stats import t, linregress

def _dl(yi, vi):
    wi=1/vi; fe=np.sum(wi*yi)/np.sum(wi); Q=np.sum(wi*(yi-fe)**2); dfree=len(yi)-1
    C=np.sum(wi)-np.sum(wi**2)/np.sum(wi); tau2=max(0.0,(Q-dfree)/C) if C>0 else 0.0
    w=1/(vi+tau2); m=np.sum(w*yi)/np.sum(w); se=np.sqrt(1/np.sum(w))
    I2=max(0.0,(Q-dfree)/Q)*100 if Q>0 else 0.0
    mult=t.ppf(0.975,dfree) if dfree>0 else 1.96
    pi=(m-mult*np.sqrt(se**2+tau2), m+mult*np.sqrt(se**2+tau2))
    return m,se,tau2,I2,Q,pi

def egger(yi, vi):
    if len(yi)<10: return None
    se=np.sqrt(vi); res=linregress(1/se, yi/se)   # precision vs standardized effect
    return {"intercept":res.intercept,"p":res.pvalue}

def pool(df, ratio_scales=("odds ratio","risk ratio","hazard ratio","hazard/rate ratio","rate ratio","relative risk")):
    df=df.copy(); df["domain"]=np.where(df.case_id.str.startswith("AD"),"AD","MS")
    out=[]
    for (dom,design,scale),sub in df.groupby(["domain","design","scale"]):
        if scale not in ratio_scales: continue
        sub=sub[sub.estimate.notna() & sub.ci_low.notna() & sub.ci_high.notna() & (sub.ci_low>0)]
        if len(sub)<2:
            out.append({"cluster":f"{dom}|{design}|{scale}","k":len(sub),
                        "note":"n<2 with CI -> report separately"}); continue
        yi=np.log(sub.estimate.values)
        vi=((np.log(sub.ci_high)-np.log(sub.ci_low))/(2*1.96))**2
        m,se,tau2,I2,Q,pi=_dl(yi,vi.values)
        row={"cluster":f"{dom}|{design}|{scale}","k":len(sub),
             "pooled":np.exp(m),"ci_low":np.exp(m-1.96*se),"ci_high":np.exp(m+1.96*se),
             "I2":round(I2,1),"tau2":round(tau2,3),
             "PI_low":np.exp(pi[0]),"PI_high":np.exp(pi[1])}
        e=egger(yi,vi.values)
        if e: row["egger_p"]=round(e["p"],3)
        out.append(row)
    return pd.DataFrame(out)

if __name__=="__main__":
    import sys
    csv_in = sys.argv[1] if len(sys.argv) > 1 else "data/effect_sizes_v3.csv"
    csv_out = sys.argv[2] if len(sys.argv) > 2 else "data/pooled_estimates_v3.csv"
    df=pd.read_csv(csv_in)
    res=pool(df); res.to_csv(csv_out,index=False); print(res.to_string(index=False))
    print(f"\nSaved {csv_out}")
