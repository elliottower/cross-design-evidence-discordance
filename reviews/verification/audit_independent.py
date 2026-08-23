"""Independent adversarial re-derivation of reviewer3 claims.

Does NOT import verify_reviewer3_claims.py. Recomputes everything from
paper/reference/classify_families.py plus hand arithmetic.
"""

import csv
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CLS_PATH = REPO / "paper" / "reference" / "classify_families.py"

spec = importlib.util.spec_from_file_location("frozen_classifier", CLS_PATH)
cf = importlib.util.module_from_spec(spec)
sys.modules["frozen_classifier"] = cf
spec.loader.exec_module(cf)


def hand_chinn(OR):
    return abs(math.log(OR)) * math.sqrt(3) / math.pi


print("=" * 78)
print("PART A: run_classification on CARDIO_FAMILIES at threshold 0.10")
print("=" * 78)
res = cf.run_classification(cf.CARDIO_FAMILIES, threshold=0.10)
for r in res:
    print(f"{r['family']:<16} obs_d={r['obs_d']:<7} obs={r['obs_class']:<12} "
          f"gen_raw={r['gen_OR_raw']:<6} gen_resc={r['gen_OR_rescaled']} "
          f"gen_d={r['gen_d']:<7} mr={r['mr_class']:<7} "
          f"class={r['classification']:<24} pred={r['prediction']}")

print()
print("Any prediction == 'success' among Lp(a)/IL-6R?")
for r in res:
    if r["family"] in ("Lp(a)", "IL-6R"):
        print(f"  {r['family']}: prediction={r['prediction']!r} "
              f"classification={r['classification']!r}")

print()
print("=" * 78)
print("PART B: hand arithmetic, no library")
print("=" * 78)
lpa_obs = hand_chinn(1.13)
lpa_gen = hand_chinn(0.94)
print(f"Lp(a)  obs OR 1.13 -> d = {lpa_obs:.6f}   (>=0.10? {lpa_obs >= 0.10})")
print(f"Lp(a)  gen OR 0.94 -> d = {lpa_gen:.6f}   (>=0.10? {lpa_gen >= 0.10})")
print(f"Lp(a)  CI (0.93,0.95) excludes null? {cf.ci_excludes_null(0.93, 0.95)}")

il6_obs = hand_chinn(1.25)
il6_resc = 0.95 ** (1.0 / 0.34)
il6_gen = hand_chinn(il6_resc)
il6_raw_d = hand_chinn(0.95)
print(f"IL-6R  obs OR 1.25 -> d = {il6_obs:.6f}   (>=0.10? {il6_obs >= 0.10})")
print(f"IL-6R  raw per-allele OR 0.95 -> d = {il6_raw_d:.6f}")
print(f"IL-6R  rescaled OR = 0.95**(1/0.34) = {il6_resc:.6f}")
print(f"IL-6R  rescaled d  = {il6_gen:.6f}   (>=0.10? {il6_gen >= 0.10})")
print(f"IL-6R  CI (0.93,0.97) excludes null? {cf.ci_excludes_null(0.93, 0.97)}")

print()
print("--- sigma at which rescaled d exactly equals 0.10 ---")
# d = |ln(0.95)|/sigma * sqrt(3)/pi = 0.10  ->  sigma = |ln 0.95|*sqrt(3)/(pi*0.10)
sigma_star = abs(math.log(0.95)) * math.sqrt(3) / (math.pi * 0.10)
print(f"sigma* = {sigma_star:.6f}")
for s in (0.283, 0.28, 0.30, 0.34):
    d = hand_chinn(0.95 ** (1.0 / s))
    print(f"  sigma={s}: rescaled OR={0.95**(1/s):.6f}  d={d:.6f}  "
          f"clears 0.10? {d >= 0.10}")

print()
print("=" * 78)
print("PART C: uric acid d values")
print("=" * 78)
for label, orv in (("OBS OR 1.07", 1.07), ("MR Egger OR 1.05", 1.05),
                   ("MR conventional OR 1.18", 1.18)):
    print(f"  {label}: d = {hand_chinn(orv):.6f}")

print()
print("=" * 78)
print("PART D: threshold sensitivity for cardio + neuro + autoimmune")
print("=" * 78)
allf = cf.NEURO_FAMILIES + cf.CARDIO_FAMILIES + cf.AUTOIMMUNE_FAMILIES + cf.EXTENSION_FAMILIES
base = {r["family"]: r for r in cf.run_classification(allf, threshold=0.10)}
for t in (0.08, 0.09, 0.12, 0.15):
    alt = {r["family"]: r for r in cf.run_classification(allf, threshold=t)}
    flips = [f for f in base
             if base[f]["classification"] != alt[f]["classification"]]
    print(f"  t={t}: flips vs 0.10 -> {flips}")

print()
print("families whose obs_d or gen_d lies within [0.08,0.12]:")
for f, r in base.items():
    if 0.08 <= r["obs_d"] <= 0.12 or 0.08 <= r["gen_d"] <= 0.12:
        print(f"  {f:<22} obs_d={r['obs_d']:<7} gen_d={r['gen_d']:<7} "
              f"mr={r['mr_class']:<7} class={r['classification']}")

print()
print("=" * 78)
print("PART E: supplementary_data.csv")
print("=" * 78)
sup = REPO / "paper" / "supplementary_data.csv"
with open(sup) as fh:
    rows = list(csv.DictReader(fh))
print(f"header: {list(rows[0].keys())}")
print(f"data rows: {len(rows)}")
fam_col = list(rows[0].keys())[0]
fams = [r[fam_col] for r in rows]
print(f"distinct values in first column: {len(set(fams))}")
dupes = [k for k, v in Counter(fams).items() if v > 1]
print(f"duplicated family names: {dupes}")
print()
for r in rows:
    print("  | ".join(f"{k}={v!r}" for k, v in r.items()))

print()
print("=" * 78)
print("PART F: Anti-CD20-MS obs")
print("=" * 78)
print(f"frozen obs_OR = {[f for f in cf.NEURO_FAMILIES if f['family']=='Anti-CD20-MS'][0]['obs_OR']}")
print(f"  d(2.23) = {hand_chinn(2.23):.6f}")
print(f"  d(0.14) = {hand_chinn(0.14):.6f}")
print(f"  d(1/0.14) = {hand_chinn(1/0.14):.6f}")
acd = base["Anti-CD20-MS"]
print(f"  frozen classification: {acd['classification']} / {acd['prediction']} "
      f"(obs_d={acd['obs_d']}, gen_d={acd['gen_d']})")
