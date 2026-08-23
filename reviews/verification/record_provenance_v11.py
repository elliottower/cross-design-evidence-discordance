"""Record the v11 revision round in the local results-cli ledger.

Run:  uv run python reviews/verification/record_provenance_v11.py

The ledger lives in .results/ and is gitignored -- hashes stay on this machine.
Re-running appends a second identical set of events; it does not de-duplicate.
Run once per round.

Every claim here is recorded as exploratory, which is what it is. The Reviewer 3
report was read before any of these checks ran, and the report names families
and effect sizes, so nothing in this round is blind to the manuscript's results.
The v10 round recorded its claims as confirmatory; results-cli 0.2.0 now refuses
that ordering, and `results verify` recomputes it from timestamps, so the v10
events are flagged in the ledger rather than rewritten.

Chain recorded:
  seal   v10, the preregistration, the shipped 41-family supplement, the frozen
         rule, the table-building helper, and the two scripts that produced v11
  access the preregistration's prospective-predictions section (outcomes seen)
  run    verify-v11   -> v11_verification.json
  run    build-v11    -> paper_v11_prospective_fix.{tex,pdf}
  run    build-audit-v11 -> REVIEWER3_AUDIT_v2.md
  claim  each value v11 changed, and each defect the audit reports
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def run(*args: str) -> None:
    print(f"$ results {' '.join(args)}")
    proc = subprocess.run(["results", *args], cwd=REPO, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"results {args[0]} failed with exit {proc.returncode}")


SEALS = [
    ("script", [
        "reviews/verification/verify_v11_numbers.py",
        "paper/patches/patch_v11_prospective_fix.py",
        "reviews/patches/build_audit_v2.py",
        "paper/reference/compute_cardio_d_values.py",
    ]),
    ("input", [
        "paper/paper_v10_reviewer3.tex",
        "PREREGISTRATION.md",
        "paper/submission/supplementary/cross_design_classification_all_41_families.csv",
    ]),
]

RUNS = [
    (
        "verify-v11",
        "Recomputed every number that differs between v10 and v11: the IL-6R and Lp(a) "
        "per-SD rescalings, the sigma break point, the Anti-CD20-MS margin and flip "
        "point, and the two registered predictions as written in the preregistration. "
        "19 checks, 0 failed.",
        ["reviews/verification/output/v11_verification.json"],
    ),
    (
        "build-v11",
        "Applied 10 exact-match edits to paper_v10_reviewer3.tex: corrected the Lp(a) and "
        "IL-6R table rows, rewrote footnotes g and h, replaced the prospective-predictions "
        "paragraph with the pair of predictions the preregistration actually fixed, "
        "corrected the Anti-CD20-MS margin and flip point, added Sclerostin-Fracture to the "
        "effect-direction discussion, and narrowed the Data Availability commit pin. "
        "Compiled to 40 pages, no undefined references.",
        ["paper/paper_v11_prospective_fix.tex", "paper/paper_v11_prospective_fix.pdf"],
    ),
    (
        "build-audit-v11",
        "Rebuilt the point-by-point audit. Sections R3.1-R3.8 carried from v1 verbatim; "
        "C1 corrected (the Lp(a) defect is in the code, not the manuscript), C5 retracted "
        "and replaced (v1 described the wrong file), and four findings added: the "
        "Anti-CD20-MS margin, Sclerostin-Fracture's opposed legs, the CRP/IL-1b-CVD "
        "duplicate, and the supplement scoring a family the manuscript excludes.",
        ["reviews/REVIEWER3_AUDIT_v2.md"],
    ),
]

CLAIMS = [
    ("verify-v11",
     "The IL6R Asp358Ala variant shifts soluble IL-6R by sigma = 0.34 SD per allele, "
     "so per-SD rescaling gives OR 0.86 and $d = 0.083$, below the $d = 0.10$ threshold",
     "Table 4 footnote h"),
    ("verify-v11",
     "At the $d = 0.10$ threshold the registered IL-6R prediction is failure; at "
     "$d = 0.08$ it is success; ZEUS discriminates between the two thresholds",
     "Results, Prospective predictions"),
    ("verify-v11",
     "Rescaling the Lp(a) MR estimate to the observational contrast (1 SD approx "
     "36 mg/dL) gives OR 0.80 per SD and $d = 0.123$, placing the family in the "
     "genetic-only cell",
     "Table 4 footnote g; Results, Prospective predictions"),
    ("verify-v11",
     "The frozen classifier stores the per-10 mg/dL Lp(a) estimate and applies "
     "rescaling only to IL-6R, so run on its stored inputs it returns null "
     "concordance for Lp(a)",
     "Table 4 footnote g"),
    ("verify-v11",
     "Anti-CD20-MS clears the effect floor by 0.0027 and reclassifies as MR-null at "
     "any threshold above $d = 0.103$",
     "Results, Anti-CD20-MS; Robustness; Limitations"),
    ("verify-v11",
     "Sclerostin-Fracture scores as concordance because both stored odds ratios fall "
     "below 1, while oriented to sclerostin the observational and MR legs oppose "
     "each other",
     "Materials and Methods, Effect direction"),
    ("build-audit-v11",
     "CRP and IL-1b-CVD are identical on every evidence field in Supplementary "
     "Table S1 and are both scored correct, so two of the 24 correct classifications "
     "are the same evidence counted twice",
     "Audit C9 -- not stated in the manuscript"),
    ("build-audit-v11",
     "Supplementary Table S1 assigns a correctness value to 33 families while the "
     "manuscript reports 24/32; the extra family is Uric acid, which the manuscript "
     "excludes as ambiguous",
     "Audit C5a -- not stated in the manuscript"),
]


def main() -> int:
    for role, files in SEALS:
        run("seal", "--role", role, *files)

    run("access", "--level", "outcomes seen",
        "Read PREREGISTRATION.md lines 160-200, the prospective-predictions section, "
        "while checking the Reviewer 3 response. The section states both registered "
        "IL-6R predictions and the Lp(a) classification, so every claim recorded in "
        "this round is exploratory with respect to it.")

    for run_id, note, outputs in RUNS:
        run("run", "--run-id", run_id, "--note", note, *outputs)

    for run_id, text, location in CLAIMS:
        run("claim", "--run-id", run_id, "--location", location, text)

    run("verify", "--files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
