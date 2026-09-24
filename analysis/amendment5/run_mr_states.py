"""Amendment 5, Procedure 2: three-state MR classification for all 41 families.

Registered at commit fbc7d33 (PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md).

States, computed from the frozen classifier's stored inputs (analysis/classifier/classify_families.py,
parsed as literals, not imported):
  supportive        CI excludes 1 and |d_MR| >= 0.10   (the registered "causal")
  negligible_range  both interval bounds, converted to signed d, lie strictly inside (-0.10, 0.10)
  inconclusive      everything else: no CI, interval reaching +/-0.10, or scale-unresolved
Conversion is bound-wise, d_j = ln(OR_j) * sqrt(3)/pi. Per-allele families with a registered
conversion factor s (only IL-6R, s = 0.34) use ln(OR_j)/s. Per-allele families without one enter
unrescaled, are marked scale_unresolved, and cannot be negligible_range. Families with no CI are
inconclusive. The registered classification and score of every family are unchanged.

Alignment flag: construct-limited (drug_outcome == Construct-limited); indication mismatch
(Table 5 criteria: IGF1-CRC); instrument-target mismatch (families the manuscript states as
instrument and drug acting at different nodes: Anti-CD20-MS, IL-6R, IL6-MDD, Complement-GA);
aligned otherwise. The source sentence for each non-aligned flag is in ALIGNMENT_SOURCE.

Outputs (analysis/amendment5/mr_states/): mr_states_results.json, mr_states_all_41.csv
Run:  uv run --no-project python analysis/amendment5/run_mr_states.py
"""
import ast
import csv
import json
import math
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLASSIFIER = os.path.join(ROOT, "analysis", "classifier", "classify_families.py")
FAMILIES_CSV = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v3.csv")
OUT = os.path.join(HERE, "mr_states")
THRESHOLD = 0.10
K = math.sqrt(3) / math.pi

PER_ALLELE = {"EBV-MS", "IL-23-psoriasis", "CTLA-4-RA", "JAK-STAT-RA", "CD20-RA",
              "Serotonin-MDD", "IL23-Crohns", "Complement-GA", "IL-6R"}   # MR_CONTRAST_TYPES, commit 4b0a652; IL-6R is per-allele rescaled
ALIGNMENT_SOURCE = {
    "IGF1-CRC": ("indication mismatch", "the MR estimate is for colorectal cancer risk, while the Phase III programs treated non-small-cell lung cancer, Ewing sarcoma, and pancreatic cancer"),
    "Anti-CD20-MS": ("instrument-target mismatch", "the MR instrument captures circulating FCRL3-mediated B-cell biology, while ocrelizumab depletes CD20+ B cells via antibody-dependent cellular cytotoxicity"),
    "IL-6R": ("instrument-target mismatch", "the MR instrument uses variants in IL6R while ziltivekimab targets the IL-6 ligand"),
    "IL6-MDD": ("instrument-target mismatch", "sirukumab neutralizes the IL-6 ligand; the declared instrument is the IL-6 receptor; the estimate used is downstream CRP (Amendment 5)"),
    "Complement-GA": ("instrument-target mismatch", "MR instruments complement pathway broadly (CFH); drug targeted Factor D specifically (classifier note)"),
}


def literal_list(source: str, name: str) -> list:
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


src = open(CLASSIFIER, encoding="utf-8").read()
fams = sum((literal_list(src, n) for n in ("NEURO_FAMILIES", "CARDIO_FAMILIES", "AUTOIMMUNE_FAMILIES", "EXTENSION_FAMILIES")), [])
assert len(fams) == 41, len(fams)
csv_rows = {r["family"]: r for r in csv.DictReader(open(FAMILIES_CSV, encoding="utf-8"))}
assert set(csv_rows) == {f["family"] for f in fams}


def signed_d(or_value: float, s: float | None) -> float:
    d = math.log(or_value) * K
    return d / s if s else d


out_rows = []
for f in fams:
    name = f["family"]
    lo, hi = f.get("gen_CI_lower"), f.get("gen_CI_upper")
    s = f.get("sd_per_allele") if f.get("per_allele") else None
    scale_unresolved = name in PER_ALLELE and s is None
    d_point = signed_d(f["gen_OR"], s)
    if lo is not None and hi is not None:
        d_lo, d_hi = signed_d(lo, s), signed_d(hi, s)
        excludes_null = not (lo <= 1.0 <= hi)
        if excludes_null and abs(d_point) >= THRESHOLD:
            state = "supportive"
        elif -THRESHOLD < d_lo and d_hi < THRESHOLD and not scale_unresolved:
            state = "negligible_range"
        else:
            state = "inconclusive"
    else:
        d_lo = d_hi = None
        excludes_null = None
        state = "inconclusive"   # no confidence interval: inconclusive by definition (Procedure 2)
    c = csv_rows[name]
    registered_mr = c["mr_class"]
    # consistency with the registered rule: supportive here <=> causal there
    assert (state == "supportive") == (registered_mr == "causal"), (name, state, registered_mr)
    if c["drug_outcome"] == "Construct-limited":
        flag, flag_src = "construct-limited", "drug_outcome"
    elif name in ALIGNMENT_SOURCE:
        flag, flag_src = ALIGNMENT_SOURCE[name]
    else:
        flag, flag_src = "aligned", ""
    out_rows.append({
        "family": name, "domain": f.get("domain", ""),
        "mr_or": f["gen_OR"], "mr_ci_low": lo if lo is not None else "", "mr_ci_high": hi if hi is not None else "",
        "conversion_factor_s": s if s else "",
        "d_lower_signed": round(d_lo, 4) if d_lo is not None else "",
        "d_point_signed": round(d_point, 4),
        "d_upper_signed": round(d_hi, 4) if d_hi is not None else "",
        "ci_excludes_null": "" if excludes_null is None else str(excludes_null),
        "scale_unresolved": str(scale_unresolved),
        "mr_state": state,
        "registered_mr_class": registered_mr,
        "alignment_flag": flag, "alignment_source": flag_src,
        "registered_classification": c["classification"], "drug_outcome": c["drug_outcome"],
        "registered_correct": c["correct"], "status": c["status"],
    })

scored = [r for r in out_rows if r["registered_correct"] in ("True", "False")]
assert len(scored) == 32
by_state = {st: {"n": len(g), "correct": sum(r["registered_correct"] == "True" for r in g),
                  "families": [r["family"] for r in g]}
            for st in ("supportive", "negligible_range", "inconclusive")
            if (g := [r for r in scored if r["mr_state"] == st])}
null_split = Counter(r["mr_state"] for r in scored if r["registered_mr_class"] == "null")
by_flag = {fl: {"n": len(g), "correct": sum(r["registered_correct"] == "True" for r in g), "families": [r["family"] for r in g]}
           for fl in ("aligned", "indication mismatch", "instrument-target mismatch")
           if (g := [r for r in scored if r["alignment_flag"] == fl])}
results = {
    "registration": "Amendment 5, commit fbc7d33", "threshold": THRESHOLD,
    "all_41_by_state": dict(Counter(r["mr_state"] for r in out_rows)),
    "scored_32_by_state": by_state,
    "registered_null_families_split": dict(null_split),
    "scale_unresolved_families": [r["family"] for r in out_rows if r["scale_unresolved"] == "True"],
    "scored_32_by_alignment_flag": by_flag,
    "no_ci_families": [r["family"] for r in out_rows if r["mr_ci_low"] == ""],
    "registered_classifications_changed": 0,
}
os.makedirs(OUT, exist_ok=True)
json.dump(results, open(os.path.join(OUT, "mr_states_results.json"), "w"), indent=2)
with open(os.path.join(OUT, "mr_states_all_41.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys())); w.writeheader(); w.writerows(out_rows)
print(json.dumps({k: results[k] for k in ("scored_32_by_state", "registered_null_families_split", "scale_unresolved_families", "scored_32_by_alignment_flag", "no_ci_families")}, indent=2))
print("wrote", OUT)
