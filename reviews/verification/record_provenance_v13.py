"""Record the v12/v13 revision steps and the bibliography fix in the local ledger.

Run:  uv run python reviews/verification/record_provenance_v13.py

The ledger lives in .results/ and is gitignored. Re-running appends; it does not
de-duplicate. Run once per round.

Every claim here is exploratory. The reviewer reports and the preregistration's
prospective-predictions section were both read before these checks ran.

Chain recorded:
  seal   the three new scripts and the preserved pre-fix bibliography
  run    demote-bib-notes -> references.bib
  run    build-v12        -> paper_v12_citation_fixes.{tex,pdf}
  run    build-v13        -> paper_v13_sclerostin_direction.{tex,pdf}
  run    build-audit-v13  -> REVIEWER3_AUDIT_v3.md
  claim  the three defects these steps fix
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
        "paper/patches/demote_bib_notes.py",
        "paper/patches/patch_v12_citation_fixes.py",
        "paper/patches/patch_v13_sclerostin_direction.py",
        "reviews/patches/build_audit_v3.py",
        "reviews/verification/verify_bib_unmangled.py",
    ]),
    ("input", [
        "paper/references_pre_note_demotion.bib",
    ]),
]

RUNS = [
    (
        "demote-bib-notes",
        "Renamed 43 `note` fields to `annote` in references.bib. unsrtnat.bst declares "
        "`note` in its ENTRY list and printed all 43 working annotations in the compiled "
        "reference list, including two instructions to self beginning VERIFY. `annote` is "
        "not in that ENTRY list. The annotations stay in the file; the bibliography lost a "
        "page and BibTeX now runs with zero warnings.",
        ["paper/references.bib"],
    ),
    (
        "build-v12",
        "One edit to paper_v11_prospective_fix.tex: the Sclerostin-Fracture observational "
        "source is Szulc 2013 (J Bone Miner Res 28(4):855-864, PMID 23165952), not Szulc "
        "2014. The printed citation already rendered as 2013.",
        ["paper/paper_v12_citation_fixes.tex", "paper/paper_v12_citation_fixes.pdf"],
    ),
    (
        "build-v13",
        "Three edits to paper_v12_citation_fixes.tex. The Musculoskeletal paragraph "
        "described the SOST cis-MR estimate as showing that genetically lower sclerostin "
        "increases fracture risk at OR 0.59, which is a reduction, and which contradicted "
        "the Effect direction paragraph added in v11. Restated the direction the stored "
        "input encodes, retitled the paragraph, and stated what a sign-aware rule would do "
        "with the family. Compiled to 39 pages, no undefined references.",
        ["paper/paper_v13_sclerostin_direction.tex", "paper/paper_v13_sclerostin_direction.pdf"],
    ),
    (
        "build-audit-v13",
        "Rebuilt the point-by-point audit from v1. R3.1-R3.8 carried verbatim; C1 and C5 "
        "corrected; C7-C12 added. Twelve internal problems, nine fixed, three open.",
        ["reviews/REVIEWER3_AUDIT_v3.md"],
    ),
]

CLAIMS = [
    ("demote-bib-notes",
     "43 bibliography entries printed internal working annotations in the compiled "
     "reference list, including two reading VERIFY",
     "Audit C10 -- defect in every version of the manuscript, now fixed"),
    ("build-v12",
     "The Sclerostin-Fracture observational source is Szulc et al., J Bone Miner Res "
     "28(4):855-864, 2013, PMID 23165952",
     "Table 5 footnote m"),
    ("build-v13",
     "The SOST cis-MR estimate is scaled to a romosozumab-equivalent increase in bone "
     "mineral density, on which sclerostin inhibition lowers fracture risk (OR 0.59), "
     "so the two legs are oriented to opposite exposures and the concordance follows "
     "from sign-blindness",
     "Results, Musculoskeletal; Materials and Methods, Effect direction"),
]


def main() -> int:
    for role, files in SEALS:
        run("seal", "--role", role, *files)

    for run_id, note, outputs in RUNS:
        run("run", "--run-id", run_id, "--note", note, *outputs)

    for run_id, text, location in CLAIMS:
        run("claim", "--run-id", run_id, "--location", location, text)

    run("verify", "--files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
