"""Stop internal working notes from printing in the bibliography.

Run:  uv run python paper/patches/demote_bib_notes.py

43 entries in paper/references.bib carry a `note` field holding working
annotations -- effect sizes, sample sizes, caveats, and two instructions to
self beginning "VERIFY". unsrtnat.bst declares `note` in its ENTRY list and
prints it, so every one of those annotations appears in the compiled reference
list. `annote` is not in that ENTRY list, so BibTeX ignores it.

This renames the field, which keeps the annotations in the file and takes them
out of the PDF. The transformation is exactly invertible. The input is copied
to references_pre_note_demotion.bib first.
"""

import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIB = REPO / "paper" / "references.bib"
BACKUP = REPO / "paper" / "references_pre_note_demotion.bib"

FIELD = re.compile(r"^(\s*)note(\s*=\s*)", re.MULTILINE)


def main() -> int:
    text = BIB.read_text()
    n = len(FIELD.findall(text))
    if n == 0:
        print("nothing to do: no `note` fields found", file=sys.stderr)
        return 1
    if "annote" in text:
        print("ABORT -- the file already contains an `annote` field", file=sys.stderr)
        return 1

    shutil.copy2(BIB, BACKUP)
    BIB.write_text(FIELD.sub(r"\1annote\2", text))

    check = BIB.read_text()
    if len(re.findall(r"^\s*annote\s*=", check, re.MULTILINE)) != n:
        print("ABORT -- rename did not round-trip", file=sys.stderr)
        return 1
    if re.search(r"^\s*note\s*=", check, re.MULTILINE):
        print("ABORT -- a `note` field survived the rename", file=sys.stderr)
        return 1

    print(f"renamed {n} note fields to annote")
    print(f"input preserved at {BACKUP.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
