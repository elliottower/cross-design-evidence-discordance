"""Reconcile the 41-family supplementary CSV against the manuscript's accounting table.

Run:  uv run python reviews/verification/reconcile_supplement_to_accounting.py [csv] [tex]

The manuscript's Table 1 states, per domain, how many families are total,
pending, construct-limited, ambiguous, scored and correct. The supplementary CSV
carries one row per family with its own status and correct columns. Nothing has
ever checked that the two agree, and a reviewer who downloads the CSV and counts
it is doing arithmetic the paper never did.

The table is parsed out of the .tex rather than restated here, so the check
cannot drift from the manuscript it is checking.

Exit 1 on any disagreement.
"""

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def newest_manuscript() -> Path:
    """The highest-numbered paper_vN.

    A pinned default goes stale at the next version bump, and a stale default
    here is worse than no default: the script reconciles a current table against
    a superseded one and reports disagreements that are its own.
    """
    versions = sorted(
        ((int(re.match(r"paper_v(\d+)", path.stem).group(1)), path)
         for path in (REPO / "paper").glob("paper_v*.tex")
         if re.match(r"paper_v\d+", path.stem)),
        key=lambda pair: pair[0])
    if not versions:
        raise FileNotFoundError(f"no paper_v*.tex under {REPO / 'paper'}")
    return versions[-1][1]


# The v2 copy is the corrected one: it carries Uric acid as ambiguous with a
# blank verdict. The original is kept beside it as provenance and disagrees with
# the accounting table by construction.
CSV = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (
    REPO / "paper" / "submission" / "supplementary"
    / "cross_design_classification_all_41_families_v2.csv")
TEX = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else newest_manuscript()

# The CSV's domain column against the accounting table's row labels.
DOMAIN = {
    "neuro": "Neuroepidemiology", "cardio": "Cardiometabolic", "autoimmune": "Autoimmune",
    "oncology": "Oncology", "respiratory": "Respiratory", "metabolic": "Metabolic/Endocrine",
    "psychiatry": "Psychiatry", "gastroenterology": "Gastroenterology",
    "ophthalmology": "Ophthalmology", "musculoskeletal": "Musculoskeletal",
}
# A row's status column says why it is out of the scored set, or that it is in.
EXCLUDED = {"pending": "pending", "construct-limited": "constr", "ambiguous": "ambig"}
SCORED = {"pre-registered", "extension"}


def accounting_rows(tex: str) -> dict[str, dict[str, int]]:
    """Domain -> {total, pending, constr, ambig, scored, correct} from Table 1."""
    block = tex.split(r"\label{tab:accounting}", 1)[1].split(r"\end{tabular}", 1)[0]
    out: dict[str, dict[str, int]] = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.split("&")]
        if len(cells) != 8:
            continue
        name = re.sub(r"\\emph\{|\}|\\", "", cells[0]).strip()
        numbers = []
        for cell in cells[1:7]:
            # A domain with nothing scored prints "---" for correct, which is 0,
            # not a parse failure.
            if cell.strip() == "---":
                numbers.append(0)
                continue
            digits = re.sub(r"[^\d]", "", re.sub(r"\$\^.*?\$", "", cell))
            numbers.append(int(digits) if digits else None)
        if any(n is None for n in numbers):
            continue
        out[name] = dict(zip(("total", "pending", "constr", "ambig", "scored", "correct"),
                             numbers))
    return out


def main() -> int:
    rows = list(csv.DictReader(CSV.open()))
    table = accounting_rows(TEX.read_text())
    failures: list[str] = []

    def check(label: str, got, want) -> None:
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  {label}: csv={got}"
              + ("" if ok else f"  table={want}"))
        if not ok:
            failures.append(label)

    print(f"{CSV.name}  ({len(rows)} rows)\n")
    unknown = sorted({r["domain"] for r in rows} - set(DOMAIN))
    if unknown:
        print(f"  FAIL  unmapped domain values: {unknown}")
        failures.append("domain mapping")

    print("Per domain")
    for key, name in DOMAIN.items():
        want = table.get(name)
        if want is None:
            print(f"  FAIL  {name}: no such row in the accounting table")
            failures.append(name)
            continue
        mine = [r for r in rows if r["domain"] == key]
        got = {
            "total": len(mine),
            "pending": sum(r["status"] == "pending" for r in mine),
            "constr": sum(r["status"] == "construct-limited" for r in mine),
            "ambig": sum(r["status"] == "ambiguous" for r in mine),
            "scored": sum(r["status"] in SCORED for r in mine),
            "correct": sum(r["status"] in SCORED and r["correct"] == "True" for r in mine),
        }
        check(name, got, want)

    print("\nTotals")
    total = table.get("Total", {})
    got = {
        "total": len(rows),
        "pending": sum(r["status"] == "pending" for r in rows),
        "constr": sum(r["status"] == "construct-limited" for r in rows),
        "ambig": sum(r["status"] == "ambiguous" for r in rows),
        "scored": sum(r["status"] in SCORED for r in rows),
        "correct": sum(r["status"] in SCORED and r["correct"] == "True" for r in rows),
    }
    check("Total", got, total)

    print("\nThe correct column")
    scored = [r for r in rows if r["status"] in SCORED]
    excluded = [r for r in rows if r["status"] not in SCORED]
    check("misses among scored", sum(r["correct"] == "False" for r in scored),
          total.get("scored", 0) - total.get("correct", 0))
    check("excluded rows leaving correct blank",
          sum(r["correct"] == "" for r in excluded), len(excluded))
    check("scored rows leaving correct blank",
          sum(r["correct"] == "" for r in scored), 0)

    print()
    if failures:
        print(f"{len(failures)} disagreement(s): " + "; ".join(failures))
        for r in rows:
            if (r["status"] in SCORED) != (r["correct"] in ("True", "False")):
                print(f"    {r['family']}: status={r['status']!r} correct={r['correct']!r}")
        return 1
    print("The supplementary CSV and the accounting table agree on every count.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
