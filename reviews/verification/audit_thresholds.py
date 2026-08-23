"""Fine-grained threshold sweep to test the two competing threshold-sensitivity lists."""

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

allf = (cf.NEURO_FAMILIES + cf.CARDIO_FAMILIES + cf.AUTOIMMUNE_FAMILIES
        + cf.EXTENSION_FAMILIES)

base = {r["family"]: r for r in cf.run_classification(allf, threshold=0.10)}

print("threshold sweep 0.01 .. 0.25 step 0.005 -- families that change class")
flip_thresholds = {}
prev = base
grid = [round(0.01 + 0.005 * i, 4) for i in range(49)]
for t in grid:
    cur = {r["family"]: r for r in cf.run_classification(allf, threshold=t)}
    for fam in cur:
        if cur[fam]["classification"] != base[fam]["classification"]:
            flip_thresholds.setdefault(fam, []).append(t)

for fam, ts in sorted(flip_thresholds.items()):
    print(f"  {fam:<22} differs from t=0.10 at thresholds: "
          f"min={min(ts)} max={max(ts)}  n={len(ts)}  "
          f"(obs_d={base[fam]['obs_d']}, gen_d={base[fam]['gen_d']})")

print()
print("families NOT appearing in the sweep (classification invariant 0.01-0.25):")
inv = [f for f in base if f not in flip_thresholds]
print("  " + ", ".join(sorted(inv)))

print()
print("--- specific manuscript claims ---")
for fam in ("Anti-CD20-MS", "CTLA-4-RA", "JAK-STAT-RA", "IL-6R", "Uric acid"):
    r = base[fam]
    ts = flip_thresholds.get(fam, [])
    print(f"  {fam:<14} obs_d={r['obs_d']:<6} gen_d={r['gen_d']:<6} "
          f"class@0.10={r['classification']:<24} "
          f"flip range={('%s..%s' % (min(ts), max(ts))) if ts else 'never in 0.01-0.25'}")

print()
print("exact gen_d values, unrounded:")
for fam, orv in (("JAK-STAT-RA", 1.27), ("Anti-CD20-MS", 0.83),
                 ("CTLA-4-RA", 0.86)):
    print(f"  {fam}: chinn_d({orv}) = {abs(math.log(orv))*math.sqrt(3)/math.pi:.6f}")
