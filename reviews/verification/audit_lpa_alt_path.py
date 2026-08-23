"""Does ANY code path reproduce the manuscript's 'Approve' for Lp(a) or IL-6R?

Tests the alternative gen_OR = 1.22 that paper/reference/compute_cardio_d_values.py
uses for Lp(a) (per-SD inversion of Burgess 2018), against the frozen rule.
"""

import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "frozen_classifier", REPO / "paper" / "reference" / "classify_families.py")
cf = importlib.util.module_from_spec(spec)
sys.modules["frozen_classifier"] = cf
spec.loader.exec_module(cf)


def d(OR):
    return abs(math.log(OR)) * math.sqrt(3) / math.pi


print("Chinn d of every Lp(a) MR value that appears anywhere in the repo:")
for label, orv in (("frozen classify_families.py gen_OR", 0.94),
                   ("Burgess 2018 raw, per 10 mg/dL", 0.942),
                   ("inverted per 10 mg/dL", 1 / 0.942),
                   ("compute_cardio_d_values.py per-SD", 1.22)):
    print(f"  {label:<38} OR={orv:.4f}  d={d(orv):.6f}  >=0.10? {d(orv) >= 0.10}")

print()
print("Frozen rule applied to Lp(a) with gen_OR replaced by 1.22:")
alt = {"family": "Lp(a) [alt gen_OR=1.22]", "domain": "cardio", "obs_OR": 1.13,
       "gen_OR": 1.22, "gen_CI_lower": 1.05, "gen_CI_upper": 1.42,
       "drug_outcome": "Pending"}
for r in cf.run_classification([alt], threshold=0.10):
    print(f"  obs_d={r['obs_d']} obs={r['obs_class']} gen_d={r['gen_d']} "
          f"mr={r['mr_class']} -> {r['classification']} / {r['prediction']}")

print()
print("Frozen rule applied to Lp(a) with the PREREGISTRATION's per-SD rescaling")
print("(prereg says Lp(a) is classified 'after per-SD rescaling'; the frozen")
print("code sets no per_allele flag for Lp(a), so no rescaling is applied):")
lpa_frozen = [f for f in cf.CARDIO_FAMILIES if f["family"] == "Lp(a)"][0]
print(f"  frozen dict: {lpa_frozen}")
print(f"  'per_allele' key present? {'per_allele' in lpa_frozen}")

print()
print("compute_cardio_d_values.py classification rule, transcribed:")
print("""  if   gen_d < 0.10 and obs_d >= 0.10: 'Qual. disc.'
  elif gen_d >= 0.10 and obs_d >= 0.10: 'Concordant' if |obs_d-gen_d|<0.05 else 'Quant. disc.'
  elif gen_d >= 0.10 and obs_d <  0.10: 'Concordant'
  else:                                  'Concordant'   <-- catch-all""")
for fam, obs_or, gen_or in (("Lp(a)", 1.13, 1.22), ("IL-6R", 1.25, 0.95)):
    od, gd = d(obs_or), d(gen_or)
    if gd < 0.10 and od >= 0.10:
        cls = "Qual. disc."
    elif gd >= 0.10 and od >= 0.10:
        cls = "Concordant" if abs(od - gd) < 0.05 else "Quant. disc."
    else:
        cls = "Concordant"
    print(f"  {fam:<8} obs_d={od:.3f} gen_d={gd:.3f} -> {cls}")
