"""Write the revised submission copy from the newest working manuscript.

Run:  uv run python paper/submission/patches/port_revision_to_submission.py

The submission copy and the working manuscript are one document under two
filenames: identical preamble, identical figure paths, identical backmatter,
differing only in body prose and in the bibliography they name. A paragraph-level
comparison (reviews/verification/diff_working_to_submission.py) shows the working
copy is a strict superset -- it drops nothing the submission copy carries -- so
the port is a copy, not a merge.

The file submitted on 2026-07-09 is left in place. The revision is written beside
it as ..._r1.tex, matching the tag frontiers-revision-1.
"""

import difflib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MANUSCRIPT_DIR = REPO / "paper" / "submission" / "manuscript"
SUBMITTED = MANUSCRIPT_DIR / "drug_failures_partition_cross_design_evidence.tex"
DST_TEX = MANUSCRIPT_DIR / "drug_failures_partition_cross_design_evidence_r1.tex"
DST_BIB = MANUSCRIPT_DIR / "references_r1.bib"

OLD_BIBLIOGRAPHY = r"\bibliography{references_v7_audited}"
NEW_BIBLIOGRAPHY = r"\bibliography{references_r1}"


def newest(directory: Path, pattern: str, prefix: str) -> Path:
    versions = sorted(
        directory.glob(pattern),
        key=lambda p: int(re.match(prefix + r"_v(\d+)", p.name).group(1)),
    )
    if not versions:
        raise SystemExit(f"ABORT -- nothing matching {pattern} in {directory}")
    return versions[-1]


def main() -> int:
    source_tex = newest(REPO / "paper", "paper_v*.tex", "paper")
    source_bib = newest(REPO / "paper", "references_v*.bib", "references")
    print(f"manuscript: {source_tex.relative_to(REPO)}")
    print(f"bibliography: {source_bib.relative_to(REPO)}\n")

    text = source_tex.read_text()
    if text.count(OLD_BIBLIOGRAPHY) != 1:
        print(f"ABORT -- {source_tex.name} names {OLD_BIBLIOGRAPHY} "
              f"{text.count(OLD_BIBLIOGRAPHY)} times, expected once", file=sys.stderr)
        return 1
    ported = text.replace(OLD_BIBLIOGRAPHY, NEW_BIBLIOGRAPHY, 1)

    # The port must be the working manuscript verbatim apart from the one line
    # naming the bibliography. Any second difference is a defect in this script.
    changed = [
        line for line in difflib.unified_diff(
            text.splitlines(), ported.splitlines(), lineterm="", n=0)
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    ]
    assert changed == [f"-{OLD_BIBLIOGRAPHY}", f"+{NEW_BIBLIOGRAPHY}"], \
        f"the port changed more than the bibliography name: {changed}"

    # Every claim the response letter makes about the manuscript has to be in the
    # file the editor receives, not only in the working copy.
    for landmark in ("24/32", "18/22", "6/10", "23/32", "23/31", "25/34",
                     "\\label{sec:selection}", "\\subsection{Family selection}",
                     "frontiers-revision-1", "$p = 0.002$", "1.084",
                     "\\subsection{Alternatives to a fixed numerical threshold}",
                     "0.038", "ambiguous"):
        assert landmark in ported, f"{landmark} missing from the ported manuscript"
    for stale in ("earns its keep", "$d = 0.442$", "$p < 0.001$",
                  "references_v7_audited"):
        assert stale not in ported, f"the ported manuscript still carries {stale}"

    # The submitted file is the record of what the editor already has.
    assert SUBMITTED.exists(), f"{SUBMITTED.name} is missing -- do not overwrite the record"

    bibliography = source_bib.read_text()
    for entry in ("juergens2023ganitumab", "hu2019"):
        assert f"@article{{{entry}," in bibliography or f"@Article{{{entry}," in bibliography, \
            f"{entry} is not in {source_bib.name}"
    assert "A Report From the {Children's Oncology Group}" in bibliography, \
        "the juergens subtitle correction is not in the bibliography being shipped"
    assert "CD013874" in bibliography, "the hu2019 article identifier is not in the bibliography"

    DST_TEX.write_text(ported)
    DST_BIB.write_text(bibliography)
    print(f"wrote {DST_TEX.relative_to(REPO)}")
    print(f"wrote {DST_BIB.relative_to(REPO)}")
    print(f"\n{SUBMITTED.name} is unchanged -- it is the record of the 2026-07-09 submission.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
