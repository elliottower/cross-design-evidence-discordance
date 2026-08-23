"""Record the v10 revision round in the local results-cli ledger.

Run:  uv run python reviews/verification/record_provenance_v10.py

The ledger lives in .results/ and is gitignored -- hashes stay on this machine.
This script is idempotent only in the sense that re-running it appends a second
identical set of events; it does not de-duplicate. Run once per round.

Chain recorded:
  seal   the frozen rule, its inputs, v9, and the two scripts that produced v10
  access the Reviewer 3 report (outcomes seen -- the reviewer reports results)
  run    verify-reviewer3   -> reviewer3_verification.{json,txt}
  run    build-v10          -> paper_v10_reviewer3.{tex,pdf}, references.bib
  claim  each numeric value in v10 that this round changed or checked
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
        "paper/reference/classify_families.py",
        "reviews/verification/verify_reviewer3_claims.py",
        "paper/patches/patch_v10_reviewer3.py",
        "paper/patches/add_reviewer3_refs.py",
    ]),
    ("input", [
        "paper/paper_v9_reviewer1.tex",
        "paper/supplementary_data.csv",
    ]),
]

RUNS = [
    (
        "verify-reviewer3",
        "Recomputed every numeric claim Reviewer 3 questioned, plus the frozen "
        "classifier's own output for all families, from paper/reference/classify_families.py. "
        "7 of 15 checks reproduce the manuscript; 8 do not.",
        [
            "reviews/verification/output/reviewer3_verification.json",
            "reviews/verification/output/reviewer3_verification.txt",
        ],
    ),
    (
        "build-v10",
        "Applied 16 exact-match edits to paper_v9_reviewer1.tex answering Reviewer 3 "
        "points 1-7 and correcting four internal inconsistencies found while checking them. "
        "Added two Crossref-fetched references. Compiled to 39 pages, no undefined references.",
        [
            "paper/paper_v10_reviewer3.tex",
            "paper/paper_v10_reviewer3.pdf",
            "paper/references.bib",
        ],
    ),
]

CLAIMS = [
    ("verify-reviewer3",
     "Anti-CD20-MS MR $d = 0.103$ clears the threshold by 0.003",
     "Results, Anti-CD20-MS paragraph; Limitations, threshold sensitivity"),
    ("verify-reviewer3",
     "CTLA-4-RA ($d_{MR} = 0.083$) becomes causal at a threshold of 0.08",
     "Limitations, threshold sensitivity"),
    ("verify-reviewer3",
     "JAK-STAT-RA ($d_{MR} = 0.132$) becomes null at 0.14",
     "Robustness; Limitations, threshold sensitivity"),
    ("verify-reviewer3",
     "Uric acid is robustly null on both legs ($d_{MR} = 0.027$ from the "
     "pleiotropy-robust Egger estimate, $d_{OBS} = 0.037$)",
     "Limitations, threshold sensitivity"),
    ("verify-reviewer3",
     "IL-6R sits at the same boundary (per-SD rescaled $d_{MR} = 0.083$), "
     "rescaled using sigma = 0.34 SD per allele",
     "Limitations, threshold sensitivity and mixed contrasts"),
    ("verify-reviewer3",
     "Equation 1 takes the absolute value of ln(OR), so the classification is "
     "blind to the sign of every estimate it reads",
     "Materials and Methods, Effect direction"),
]


def main() -> int:
    for role, files in SEALS:
        run("seal", "--role", role, *files)

    run("access", "--level", "outcomes seen",
        "Reviewer 3 report received 2026-08-23 via the Frontiers portal (MS 1933481). "
        "Reviewer reports name specific families and effect sizes, so this round is "
        "not blind to the manuscript's own results.")

    for run_id, note, outputs in RUNS:
        run("run", "--run-id", run_id, "--note", note, *outputs)

    for run_id, text, location in CLAIMS:
        run("claim", "--run-id", run_id, "--confirmatory", "--location", location, text)

    run("verify", "--files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
