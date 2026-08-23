"""Build paper_v19_checked_bibliography.tex from paper_v18_verified_bibliography.tex.

Run:  uv run python paper/patches/patch_v19_checked_bibliography.py

One change: the manuscript compiles against references_v6_checked.bib instead of
references_v5_verified.bib. The two differ in one field of one entry, where
chinn2000 carries a PubMed identifier in place of a legacy Wiley DOI the font
encoding could not typeset. See patch_bib_v6_chinn_identifier.py.

Every numeric check that passed on v17 and v18 must pass on v19 unchanged.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v18_verified_bibliography.tex"
DST = REPO / "paper" / "paper_v19_checked_bibliography.tex"
BIB = REPO / "paper" / "references_v6_checked.bib"

OLD = r"\bibliography{references_v5_verified}"
NEW = r"\bibliography{references_v6_checked}"

CITE = re.compile(r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear)\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def main() -> int:
    text = SRC.read_text()
    if text.count(OLD) != 1:
        print(f"ABORT -- {OLD} appears {text.count(OLD)} times", file=sys.stderr)
        return 1
    rebuilt = text.replace(OLD, NEW)

    cited = {k.strip() for group in CITE.findall(rebuilt) for k in group.split(",") if k.strip()}
    available = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", BIB.read_text()))
    missing = sorted(cited - available)
    if missing:
        print(f"ABORT -- {len(missing)} cited keys absent from {BIB.name}:", file=sys.stderr)
        for key in missing:
            print(f"  {key}", file=sys.stderr)
        return 1

    assert text.replace(OLD, "") == rebuilt.replace(NEW, ""), \
        "something other than the bibliography line changed"

    DST.write_text(rebuilt)
    print(f"  {OLD}\n  -> {NEW}")
    print(f"\n{len(cited)} cited keys, all present in {BIB.name} "
          f"({len(available)} entries, {len(available - cited)} uncited)")
    print(f"wrote {DST.relative_to(REPO)}  ({SRC.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
