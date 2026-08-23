"""Verification of every number changed between paper_v10_reviewer3.tex and paper_v11_prospective_fix.tex.

Run:  uv run python reviews/verification/verify_v11_numbers.py

Emits a report on stdout and a machine-readable record to
reviews/verification/output/v11_verification.json.

Nothing here re-analyzes data. Each check recomputes a Chinn conversion from
printed inputs, or reads a value out of a repository file, and compares it to
what v11 prints. Discrepancies are reported, not resolved.
"""

import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
V11 = REPO / "paper" / "paper_v11_prospective_fix.tex"
HELPER = REPO / "paper" / "reference" / "compute_cardio_d_values.py"
PREREG = REPO / "PREREGISTRATION.md"
OUT = Path(__file__).resolve().parent / "output" / "v11_verification.json"

CHINN = math.sqrt(3) / math.pi
THRESHOLD = 0.10

record: dict = {"checks": []}


def chinn_d(odds_ratio: float) -> float:
    """Chinn (2000) log-odds to Cohen's d. Direction-blind, as the paper's rule is."""
    return abs(math.log(odds_ratio)) * CHINN


def note(name: str, printed, recomputed, ok: bool, comment: str = "") -> None:
    record["checks"].append(
        {"check": name, "printed": printed, "recomputed": recomputed,
         "ok": bool(ok), "comment": comment}
    )
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}")
    print(f"       v11 prints : {printed}")
    print(f"       recomputed : {recomputed}")
    if comment:
        print(f"       {comment}")
    print()


tex = V11.read_text()


def in_tex(needle: str) -> bool:
    return needle in tex


# --- IL-6R: per-allele OR 0.95, sigma = 0.34 SD per allele -------------------
il6r_per_sd = 0.95 ** (1 / 0.34)
il6r_d = chinn_d(il6r_per_sd)
note("IL-6R per-SD odds ratio", "0.86", round(il6r_per_sd, 4),
     abs(il6r_per_sd - 0.86) < 0.005)
note("IL-6R per-SD Chinn d", "0.083", round(il6r_d, 4),
     abs(il6r_d - 0.083) < 0.0005,
     f"below the {THRESHOLD} floor: {il6r_d < THRESHOLD}; above a 0.08 floor: {il6r_d >= 0.08}")
note("IL-6R per-allele Chinn d", "0.028", round(chinn_d(0.95), 4),
     abs(chinn_d(0.95) - 0.028) < 0.0005)

# The dual prediction only exists if the two floors really do separate here.
note("IL-6R straddles the two registered floors", "0.10 fails, 0.08 passes",
     f"0.10 {'fails' if il6r_d < 0.10 else 'passes'}, "
     f"0.08 {'fails' if il6r_d < 0.08 else 'passes'}",
     il6r_d < 0.10 and il6r_d >= 0.08)

# --- Lp(a): OR 0.94 per 10 mg/dL, 1 SD ~ 36 mg/dL ---------------------------
lpa_per_sd = 0.94 ** 3.6
lpa_d = chinn_d(lpa_per_sd)
note("Lp(a) per-SD odds ratio", "0.80", round(lpa_per_sd, 4),
     abs(lpa_per_sd - 0.80) < 0.005)
note("Lp(a) per-SD Chinn d", "0.123", round(lpa_d, 4),
     abs(lpa_d - 0.123) < 0.0005,
     f"clears the {THRESHOLD} floor: {lpa_d >= THRESHOLD}")
note("Lp(a) per-10 mg/dL Chinn d", "0.034", round(chinn_d(0.94), 4),
     abs(chinn_d(0.94) - 0.034) < 0.0005)
note("Lp(a) observational Chinn d", "0.067", round(chinn_d(1.13), 4),
     abs(chinn_d(1.13) - 0.067) < 0.0005,
     "trivial, so with a causal MR leg the cell is genetic-only, not concordant")

# --- The sigma break point, which v9/v10 footnote h stated wrongly ----------
sigma_star = abs(math.log(0.95)) * math.sqrt(3) / (math.pi * THRESHOLD)
note("sigma break point for a per-allele OR of 0.95", "not stated in v11",
     round(sigma_star, 6),
     0.34 > sigma_star,
     f"IL-6R sigma = 0.34 exceeds it, so d < 0.10; at sigma = 0.283 exactly, "
     f"d = {chinn_d(0.95 ** (1 / 0.283)):.6f}, still short of 0.10")

# --- Anti-CD20-MS margin and flip point -------------------------------------
anti_cd20_d = 0.1027
note("Anti-CD20-MS margin above the floor", "0.0027",
     round(anti_cd20_d - THRESHOLD, 4),
     abs((anti_cd20_d - THRESHOLD) - 0.0027) < 0.00005)
note("Anti-CD20-MS flip point", "0.103", round(anti_cd20_d, 4),
     abs(anti_cd20_d - 0.103) < 0.0005,
     "the family reclassifies as MR-null at any floor above its own d")
note("v11 no longer prints the 0.11 flip point", "absent",
     "absent" if "0.11}$, Anti-CD20" not in tex else "present",
     "0.11}$, Anti-CD20" not in tex)

# --- JAK-STAT-RA rounding, carried from v10 ---------------------------------
note("JAK-STAT-RA d printed consistently", "0.132",
     sorted(set(re.findall(r"0\.13[0-9]", tex))),
     "0.131" not in tex)

# --- The helper script's classifier, which produced the wrong Lp(a) cell ----
helper = HELPER.read_text()
genetic_only_branch = "elif gen_d >= 0.10 and obs_d < 0.10:\n        cls = \"Concordant\""
note("helper mislabels the genetic-only cell as Concordant",
     "n/a (helper is not the frozen classifier)",
     "present" if genetic_only_branch in helper else "absent",
     genetic_only_branch in helper,
     "this branch is the origin of the Lp(a) row v11 corrects")

# --- The preregistration registered both IL-6R predictions ------------------
prereg = PREREG.read_text()
both_registered = ("**At d = 0.10 threshold:** predict FAILURE" in prereg
                   and "**At d = 0.08 threshold:** predict SUCCESS" in prereg)
note("preregistration fixes both IL-6R predictions", "both, per v11",
     "both present" if both_registered else "not both", both_registered)
note("preregistration classifies Lp(a) as genetic-only", "genetic-only",
     "genetic-only" if "genetic-only signal" in prereg else "other",
     "genetic-only signal" in prereg)

# --- v11 says what it should say --------------------------------------------
for phrase, label in [
    ("Genetic-only", "v11 table carries a Genetic-only verdict"),
    ("Qual.\\ disc.", "v11 table carries a qualitative-discordance verdict for IL-6R"),
    ("ZEUS discriminates between the two thresholds", "v11 states the discriminating test"),
]:
    note(label, "present", "present" if in_tex(phrase) else "ABSENT", in_tex(phrase))

failed = [c for c in record["checks"] if not c["ok"]]
record["n_checks"] = len(record["checks"])
record["n_failed"] = len(failed)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, indent=2) + "\n")

print("=" * 78)
print(f"{len(record['checks'])} checks, {len(failed)} failed")
for c in failed:
    print(f"  FAIL  {c['check']}: v11 prints {c['printed']}, recomputed {c['recomputed']}")
print(f"wrote {OUT.relative_to(REPO)}")
raise SystemExit(1 if failed else 0)
