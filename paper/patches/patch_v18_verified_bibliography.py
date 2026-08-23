"""Build paper_v18_verified_bibliography.tex from paper_v17_selection_criteria.tex.

Run:  uv run python paper/patches/patch_v18_verified_bibliography.py

One change: the manuscript compiles against references_v5_verified.bib instead of
references_v3_zeus.bib.

The v5 bibliography differs from v3 in three ways, all of them answering
Reviewer 1's checklist answer that the reference list is not adequate.
Twelve entries that carried no DOI or PMID now carry a DOI verified against
Crossref on title, year, and first author. Four entries whose metadata that
verification exposed as wrong -- a journal, two volumes, two page ranges, three
given names, and one identifier pointing at correspondence rather than at the
article -- are corrected against the record each names. One uncited entry that
matches no record in Crossref or PubMed is removed.

No text, number, table, or citation key in the manuscript changes, so every
numeric check that passed on v17 must pass on v18 unchanged.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v17_selection_criteria.tex"
DST = REPO / "paper" / "paper_v18_verified_bibliography.tex"
BIB = REPO / "paper" / "references_v5_verified.bib"

OLD = r"\bibliography{references_v3_zeus}"
NEW = r"\bibliography{references_v5_verified}"

CITE = re.compile(r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear)\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def main() -> int:
    text = SRC.read_text()
    if text.count(OLD) != 1:
        print(f"ABORT -- {OLD} appears {text.count(OLD)} times", file=sys.stderr)
        return 1
    rebuilt = text.replace(OLD, NEW)

    # A bibliography swap is only safe if every key the manuscript cites is still
    # there. BibTeX reports a missing key as a warning and typesets [?].
    cited = {k.strip() for group in CITE.findall(rebuilt) for k in group.split(",") if k.strip()}
    available = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", BIB.read_text()))
    missing = sorted(cited - available)
    if missing:
        print(f"ABORT -- {len(missing)} cited keys absent from {BIB.name}:", file=sys.stderr)
        for key in missing:
            print(f"  {key}", file=sys.stderr)
        return 1

    body_before = text.replace(OLD, "")
    body_after = rebuilt.replace(NEW, "")
    assert body_before == body_after, "something other than the bibliography line changed"

    DST.write_text(rebuilt)
    print(f"  {OLD}\n  -> {NEW}")
    print(f"\n{len(cited)} cited keys, all present in {BIB.name} "
          f"({len(available)} entries, {len(available - cited)} uncited)")
    print(f"wrote {DST.relative_to(REPO)}  ({SRC.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
