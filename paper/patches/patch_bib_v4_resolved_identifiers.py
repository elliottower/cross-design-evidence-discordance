"""Build references_v4_resolved_ids.bib from references_v3_zeus.bib.

Run:  uv run python paper/patches/patch_bib_v4_resolved_identifiers.py

Two changes, both prompted by Reviewer 1's checklist answer that the reference
list is not adequate.

Twelve entries carried no DOI and no PMID, so no checker could confirm they point
at the paper they name. Eleven were resolved by
reviews/verification/resolve_missing_identifiers.py, which accepts a Crossref
candidate only when title similarity, year, and first-author surname agree
independently; all eleven matched at a title similarity of 1.000. The twelfth,
shumaker2003, was rejected by that script at 0.91 similarity because JAMA
records the subtitle after a period where the entry uses a colon, and the top
candidate was a journal-club digest rather than the trial report. Its DOI is
adopted here after checking the JAMA record against the entry on journal,
volume, first page, year, and the first three authors, all of which agree.

One entry is removed. liu2024tg names Lipids in Health and Disease 23:55 (2024)
by Liu Dong-Jing; no such record appears in Crossref under a journal-scoped title
search or in PubMed under a title-field search, and the nearest match by title is
a different paper, in Clinical Research in Cardiology, by different authors. The
entry is not cited anywhere in the manuscript, so it never reached the printed
reference list and no claim depends on it, but it would ship inside the .bib.

The remaining nine uncited entries carry identifiers that resolve to the record
they name and are left in place; an uncited entry is not an error.

references_v3_zeus.bib is not modified.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "references_v3_zeus.bib"
DST = REPO / "paper" / "references_v4_resolved_ids.bib"
RESOLVED = (REPO / "reviews" / "verification" / "output"
            / "resolved_identifiers__references_v3_zeus.json")

# Verified by hand against the JAMA record; see the module docstring.
HAND_VERIFIED = {"shumaker2003": "10.1001/jama.289.20.2651"}

DROP = {"liu2024tg"}

ENTRY = re.compile(r"(@\w+\s*\{\s*([^,\s]+)\s*,)(.*?)(\n\})", re.DOTALL)


def main() -> int:
    if not RESOLVED.exists():
        print(f"ABORT -- no resolver output at {RESOLVED.relative_to(REPO)}.\n"
              "Run: uv run python reviews/verification/resolve_missing_identifiers.py",
              file=sys.stderr)
        return 1
    dois: dict[str, str] = {**json.loads(RESOLVED.read_text()), **HAND_VERIFIED}
    text = SRC.read_text()
    added: list[tuple[str, str]] = []
    dropped: list[str] = []

    def rewrite(match: re.Match) -> str:
        header, key, body, closer = match.groups()
        if key in DROP:
            dropped.append(key)
            return ""
        if key not in dois:
            return match.group(0)
        if re.search(r"\bdoi\s*=", body):
            raise AssertionError(f"{key} already has a DOI; the resolver should not have run on it")
        added.append((key, dois[key]))
        return f"{header}{body.rstrip().rstrip(',')},\n  doi     = {{{dois[key]}}},{closer}"

    rebuilt = ENTRY.sub(rewrite, text)
    rebuilt = re.sub(r"\n{3,}", "\n\n", rebuilt)

    assert len(dropped) == len(DROP), f"expected to drop {DROP}, dropped {dropped}"
    assert len(added) == len(dois), f"{len(dois)} identifiers to add, added {len(added)}"
    before = len(re.findall(r"^@", text, re.M))
    after = len(re.findall(r"^@", rebuilt, re.M))
    assert after == before - len(DROP), f"entry count went {before} -> {after}"
    for key in DROP:
        assert f"{{{key}," not in rebuilt.replace(" ", ""), f"{key} survived"

    DST.write_text(rebuilt)
    for key, doi in sorted(added):
        print(f"  + doi  {key:<26} {doi}")
    for key in dropped:
        print(f"  - drop {key:<26} resolves to no record in Crossref or PubMed")
    print(f"\n{after} entries ({before} in {SRC.name}); "
          f"{len(added)} identifiers added, {len(dropped)} entry removed")
    print(f"wrote {DST.relative_to(REPO)}  ({SRC.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
