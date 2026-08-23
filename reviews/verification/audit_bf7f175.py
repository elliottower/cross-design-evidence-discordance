"""Run the bf7f175 version of the classifier (the commit the manuscript cites)."""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
src = subprocess.run(
    ["git", "-C", str(REPO), "show", "bf7f175:paper/reference/classify_families.py"],
    capture_output=True, text=True, check=True).stdout

with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "cf_bf7f175.py"
    p.write_text(src)
    spec = importlib.util.spec_from_file_location("cf_bf7f175", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules["cf_bf7f175"] = m
    spec.loader.exec_module(m)

    print("bf7f175 CARDIO at threshold 0.10:")
    for r in m.run_classification(m.CARDIO_FAMILIES, threshold=0.10):
        if r["family"] in ("Lp(a)", "IL-6R"):
            print(f"  {r['family']:<8} obs_d={r['obs_d']} obs={r['obs_class']} "
                  f"gen_d={r['gen_d']} mr={r['mr_class']} "
                  f"-> {r['classification']} / {r['prediction']}")

    print()
    print("bf7f175 raw dict entries:")
    for f in m.CARDIO_FAMILIES:
        if f["family"] in ("Lp(a)", "IL-6R"):
            print(f"  {f}")

    print()
    print("Search every module-level family list at bf7f175 for a 'success' "
          "prediction on Lp(a)/IL-6R at any threshold 0.01-0.30:")
    for t in [round(0.01 + 0.01 * i, 3) for i in range(30)]:
        for r in m.run_classification(m.CARDIO_FAMILIES, threshold=t):
            if r["family"] in ("Lp(a)", "IL-6R") and r["prediction"] == "success":
                print(f"  t={t}: {r['family']} -> {r['prediction']} "
                      f"({r['classification']})")
