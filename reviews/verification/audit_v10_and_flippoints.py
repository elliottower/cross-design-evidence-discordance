"""Exact flip points, and whether paper_v10_reviewer3.tex fixes the v9 defects.

Independent of verify_reviewer3_claims.py. Loads the frozen classifier by path.
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

allf = (cf.NEURO_FAMILIES + cf.CARDIO_FAMILIES + cf.AUTOIMMUNE_FAMILIES
        + cf.EXTENSION_FAMILIES)
base = {r["family"]: r for r in cf.run_classification(allf, threshold=0.10)}

print("=" * 78)
print("EXACT unrounded d values and exact flip thresholds")
print("=" * 78)


def d(OR):
    return abs(math.log(OR)) * math.sqrt(3) / math.pi


for fam in ("Anti-CD20-MS", "CTLA-4-RA", "JAK-STAT-RA", "IL-6R", "Uric acid"):
    r = base[fam]
    print(f"{fam:<14} obs_d={r['obs_d']:<7} gen_d={r['gen_d']:<7} "
          f"class={r['classification']}")

print()
print(f"chinn_d(0.83)  Anti-CD20-MS MR, unrounded = {d(0.83):.9f}")
print(f"  paper says d = 0.103 and 'clears by 0.003'; actual margin over 0.10 "
      f"= {d(0.83) - 0.10:.9f}")
print(f"  rule is d >= threshold, so it flips for ANY threshold > {d(0.83):.6f}")
for t in (0.1027, 0.1028, 0.103, 0.104, 0.105, 0.11):
    res = {x["family"]: x for x in cf.run_classification(allf, threshold=t)}
    print(f"    t={t:<7} Anti-CD20-MS -> {res['Anti-CD20-MS']['classification']}")

print()
print(f"chinn_d(1.27)  JAK-STAT-RA MR, unrounded = {d(1.27):.9f}")
print(f"chinn_d(0.86)  CTLA-4-RA MR, unrounded  = {d(0.86):.9f}")

print()
print("=" * 78)
print("Uric acid: is it threshold-sensitive anywhere in 0.01-0.25?")
print("=" * 78)
prev = None
for i in range(49):
    t = round(0.01 + 0.005 * i, 4)
    res = {x["family"]: x for x in cf.run_classification(allf, threshold=t)}
    c = res["Uric acid"]["classification"]
    if c != prev:
        print(f"  t={t:<7} -> {c}")
        prev = c

print()
print("=" * 78)
print("v10 status of each v9 defect (string presence in the .tex)")
print("=" * 78)
v9 = (REPO / "paper" / "paper_v9_reviewer1.tex").read_text().splitlines()
v10 = (REPO / "paper" / "paper_v10_reviewer3.tex").read_text().splitlines()

probes = [
    ("CLAIM 1  'Approve' prospective line", "classified as ``Approve'' by the frozen rule"),
    ("CLAIM 2  footnote h sigma bound", "clears $d = 0.10$ for any per-allele exposure SD"),
    ("CLAIM 4/5 old Limitations list", "Uric acid ($d = 0.037$) is robustly null"),
    ("CLAIM 6  supplement description", "gene targets, instrument types, and classifications"),
    ("         27 families / three domains", "We assembled 27 mechanism families across three disease domains"),
    ("         41 families / ten domains", "41 mechanism families across ten disease domains"),
    ("CLAIM 3  sigma = 0.34 stated in paper", "0.34"),
]
for label, probe in probes:
    a = [i + 1 for i, l in enumerate(v9) if probe in l]
    b = [i + 1 for i, l in enumerate(v10) if probe in l]
    print(f"{label:<42} v9 lines={a}  v10 lines={b}")

print()
print("v10 Anti-CD20-MS row in tab:stage1:")
for i, l in enumerate(v10):
    if "Anti-CD20-MS &" in l:
        print(f"  {i+1}: {l.strip()}")
