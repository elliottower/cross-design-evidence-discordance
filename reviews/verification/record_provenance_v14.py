"""Record the bibliography audit, the rebuild, and v14 in the local ledger.

Run:  uv run python reviews/verification/record_provenance_v14.py

The ledger lives in .results/ and is gitignored. Re-running appends; it does not
de-duplicate. Run once per round.

Every claim here is exploratory. The reviewer reports were read before these
checks ran, and the bibliography audit was written to answer a question C10
raised rather than registered in advance.

Chain recorded:
  seal   the audit, the rebuilder, the v14 patch, the audit-v4 builder
  seal   references.bib as the input the rebuild reads
  run    audit-bibliography   -> bibliography_audit__references.json
  run    rebuild-bibliography -> references_v2_resolved.bib + its re-audit
  run    build-v14            -> paper_v14_resolved_references.{tex,pdf}
  run    build-audit-v14      -> REVIEWER3_AUDIT_v4.md
  claim  what the audit found and what v14 changes
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
        "reviews/verification/audit_bibliography.py",
        "paper/patches/rebuild_bib_from_records.py",
        "paper/patches/patch_v14_resolved_references.py",
        "reviews/patches/build_audit_v4.py",
    ]),
    ("input", [
        "paper/references.bib",
    ]),
]

RUNS = [
    (
        "audit-bibliography",
        "Resolved every DOI in references.bib against Crossref and every PMID against "
        "PubMed, then compared title, journal, year, volume, pages and the author list "
        "name by name. 75 entries; 62 carry an identifier; 27 disagreed with the record "
        "that identifier resolves to; 0 failed to resolve; 13 carry no identifier and "
        "were not checked. Responses are cached so the audit reruns offline.",
        ["reviews/verification/output/bibliography_audit__references.json"],
    ),
    (
        "rebuild-bibliography",
        "Rewrote author, year, volume, pages and journal from the cached Crossref or "
        "PubMed payload wherever the audit flagged a disagreement, into a new file. "
        "23 entries rewritten, 38 fields; entries the audit passed come through "
        "byte-identical; references.bib is not modified. Re-auditing the output leaves "
        "9 flags, all properties of the source record (Crossref HTML entities, "
        "subtitle-only titles, a deposited typo, an incomplete author list, initials "
        "only, and the Cochrane volume-by-year convention).",
        [
            "paper/references_v2_resolved.bib",
            "reviews/verification/output/bibliography_audit__references_v2_resolved.json",
        ],
    ),
    (
        "build-v14",
        "Three edits to paper_v13_sclerostin_direction.tex: point the bibliography at "
        "references_v2_resolved.bib, and correct the SGLT2-heart failure confidence "
        "interval in Table 2 and in the Metabolic paragraph from 0.22-0.88 to the "
        "0.26-0.76 the source reports. Compiled to 40 pages with no undefined control "
        "sequences, no undefined citations and no BibTeX warnings.",
        [
            "paper/paper_v14_resolved_references.tex",
            "paper/paper_v14_resolved_references.pdf",
        ],
    ),
    (
        "build-audit-v14",
        "Rebuilt the point-by-point audit from v3. R3.1-R3.8 and C1-C12 carried "
        "verbatim, with C10's open VERIFY sentence replaced; C13 and C14 added; the "
        "open-decisions list rewritten. The C13 counts are read from the audit reports "
        "rather than typed. Fourteen internal problems, eleven fixed, three open.",
        ["reviews/REVIEWER3_AUDIT_v4.md"],
    ),
]

CLAIMS = [
    ("audit-bibliography",
     "27 of the 62 bibliography entries carrying an identifier disagreed with the "
     "record that identifier resolves to: 9 with a wrong family name, 16 with a wrong "
     "given name, 4 truncated with no 'and others' marker, 6 with a wrong volume or "
     "page range, 2 with a wrong year, and 1 whose PMID resolves to an unrelated paper",
     "Audit C13 -- defect in every version of the manuscript, now fixed"),
    ("audit-bibliography",
     "Four entries carried an author list belonging to nobody on the paper: "
     "zheng2020sglt2mr (Luo, Shi, Liu), shi2023estradiolBC (Nounu, Kar, Relton), "
     "juergens2023ganitumab (DuBois, Krailo, Glade-Bender) and wagener2022eosinophils "
     "(Benson, Hartl, Barnes). Every identifier still points at the correct paper, and "
     "every estimate checked against source text was right",
     "Audit C13"),
    ("audit-bibliography",
     "Bovijn et al. report a 41% lower risk of fracture, OR 0.59, 95% CI 0.54 to 0.66, "
     "P = 1.4e-24, scaled to the 0.09 g/cm2 lumbar-spine bone mineral density increase "
     "romosozumab produces at 12 months; the estimate appears in Results, not in the "
     "abstract",
     "Table 5; Results, Musculoskeletal; Materials and Methods, Effect direction"),
    ("build-v14",
     "The SGLT2 inhibition to heart failure Mendelian randomization estimate is "
     "OR 0.44, 95% CI 0.26 to 0.76, P = 0.003. Chinn d is a function of the point "
     "estimate alone, so d = 0.452, the Causal verdict, the family's Concordant class "
     "and the 24/32 accuracy are unchanged by the correction",
     "Table 2, SGLT2-HF row; Results, Metabolic"),
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
