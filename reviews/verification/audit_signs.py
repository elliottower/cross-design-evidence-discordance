"""CLAIM 7: sign-blindness of the rule, and whether any family has OBS and GEN
pointing in opposite directions.

Caveat carried through: the frozen data dicts store obs_OR / gen_OR on whatever
orientation the source study reported. There is no orientation / exposure-direction
field, so a raw side-of-1.0 comparison is NOT a harmonized directional test.
"""

import importlib.util
import inspect
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CLS = REPO / "paper" / "reference" / "classify_families.py"
spec = importlib.util.spec_from_file_location("frozen_classifier", CLS)
cf = importlib.util.module_from_spec(spec)
sys.modules["frozen_classifier"] = cf
spec.loader.exec_module(cf)

print("=" * 78)
print("A. Does any classification function inspect sign?")
print("=" * 78)
for fn in (cf.chinn_d, cf.classify_obs, cf.classify_mr, cf.classify_family,
           cf.ci_excludes_null, cf.rescale_per_allele_to_per_sd):
    src = inspect.getsource(fn)
    signs = re.findall(r"(?:< *1\.0|> *1\.0|direction|sign|protective|harmful)",
                       src, flags=re.I)
    print(f"{fn.__name__:<28} sign-ish tokens: {signs or 'NONE'}")
print()
print("chinn_d body:")
print(inspect.getsource(cf.chinn_d))

print("=" * 78)
print("B. Fields present in the frozen data dicts (union over all families)")
print("=" * 78)
allf = (cf.NEURO_FAMILIES + cf.CARDIO_FAMILIES + cf.AUTOIMMUNE_FAMILIES
        + cf.EXTENSION_FAMILIES)
keys = sorted({k for f in allf for k in f})
print(keys)
print(f"\nany orientation/direction field? "
      f"{[k for k in keys if 'dir' in k.lower() or 'orient' in k.lower()] or 'NO'}")

print()
print("=" * 78)
print("C. Raw side-of-1.0 disagreement (NOT harmonized -- see module docstring)")
print("=" * 78)
for f in allf:
    o, g = f.get("obs_OR"), f.get("gen_OR")
    if o is None or g is None:
        continue
    if (o - 1.0) * (g - 1.0) < 0:
        r = [x for x in cf.run_classification([f], threshold=0.10)][0]
        print(f"  {f['family']:<22} obs_OR={o:<6} gen_OR={g:<6} "
              f"obs_d={r['obs_d']:<6} gen_d={r['gen_d']:<6} -> "
              f"{r['classification']} / {r['prediction']}")

print()
print("=" * 78)
print("D. In-source comments that record an orientation")
print("=" * 78)
src = CLS.read_text().splitlines()
for i, line in enumerate(src, 1):
    if re.search(r"protectiv|reverse causation|harmful|opposite|direction",
                 line, flags=re.I):
        print(f"  {i}: {line.strip()}")
