"""Build references_v6_checked.bib from references_v5_verified.bib.

Run:  uv run python paper/patches/patch_bib_v6_chinn_identifier.py

One entry, one field. chinn2000 gained the DOI
10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m in v4. Wiley issued
that DOI in the legacy SICI form, which contains angle brackets, and the
manuscript's font encoding typesets a bare < as an inverted exclamation mark: the
compiled reference list printed 19:22(3127::aid-sim784)3.0.co;2-m in angle
quotes, a string that does not resolve if a reader copies it.

Escaping the brackets as {\\textless} and {\\textgreater} typesets correctly but
puts LaTeX markup inside a field that identifier checkers read literally, which
trades a defect a reader sees for one a checker hits.

The entry therefore carries the PubMed identifier instead: 11113947, from an
esearch query returning exactly one record, whose title, journal, year, volume,
issue, pages, and sole author all match the entry. The bibliography style prints
neither DOIs it cannot typeset nor PubMed identifiers, so the reference reads as
it did before v4, and the audit can now check it.

references_v5_verified.bib is not modified.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "references_v5_verified.bib"
DST = REPO / "paper" / "references_v6_checked.bib"

KEY = "chinn2000"
OLD_DOI = r"10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m"
PMID = "11113947"

ENTRY = re.compile(r"(@\w+\s*\{\s*([^,\s]+)\s*,)(.*?)(\n\})", re.DOTALL)
DOI_LINE = re.compile(r"^([ \t]*)doi([ \t]*=[ \t]*)\{([^}]*)\}(,?)[ \t]*$", re.MULTILINE)


def main() -> int:
    text = SRC.read_text()
    match = next((m for m in ENTRY.finditer(text) if m.group(2) == KEY), None)
    if match is None:
        print(f"ABORT -- no entry {KEY}", file=sys.stderr)
        return 1
    body = match.group(3)
    lines = DOI_LINE.findall(body)
    if len(lines) != 1 or lines[0][2].strip() != OLD_DOI:
        print(f"ABORT -- {KEY} does not hold the DOI this patch replaces; "
              f"found {[l[2].strip() for l in lines]}", file=sys.stderr)
        return 1

    new_body = DOI_LINE.sub(
        lambda m: f"{m.group(1)}pmid{m.group(2)}{{{PMID}}}{m.group(4)}", body)
    rebuilt = text[:match.start()] + match.group(1) + new_body + match.group(4) + text[match.end():]

    assert rebuilt.count("@") == text.count("@"), "entry count changed"
    assert OLD_DOI not in rebuilt, "the legacy DOI survived"
    assert f"pmid    = {{{PMID}}}" in rebuilt or f"pmid = {{{PMID}}}" in rebuilt \
        or re.search(rf"pmid\s*=\s*\{{{PMID}\}}", rebuilt), "the PMID was not written"
    # Nothing outside this one entry may move.
    assert len(rebuilt) - len(text) == len("pmid") - len("doi") + len(PMID) - len(OLD_DOI), \
        "the edit changed more than the one field"

    DST.write_text(rebuilt)
    print(f"  {KEY}: doi {OLD_DOI}\n       -> pmid {PMID}")
    print(f"wrote {DST.relative_to(REPO)}  ({SRC.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
