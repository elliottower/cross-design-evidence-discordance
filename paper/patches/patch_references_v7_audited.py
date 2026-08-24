"""Build references_v7_audited.bib from references_v6_checked.bib.

Run:  uv run python paper/patches/patch_references_v7_audited.py

`citations audit` compared all 75 entries against the record each identifier
resolves to (reviews/verification/audit_bibliography.py). Ten disagreed. Nine are
the registry's -- Crossref stores one author for the JAMA consortium paper,
truncates two subtitles, deposits `<scp>L</scp>` and `Table 1.` inside title
strings, misspells `complement factor H`, and records Cochrane volumes as years.
Those are adjudicated in the audit script and the bibliography is right.

One is the bibliography's.

1. juergens2023ganitumab carries issue 12. Crossref and PubMed 36669140 both give
   J Clin Oncol 41(11):2098-2107. Its title also stops before the published
   subtitle naming the reporting group.

2. hu2019 is not wrong -- PubMed 34748215 gives volume 11, which the entry has --
   but it omits the issue and the article number, so the entry does not resolve
   to a specific Cochrane review from the printed reference alone.

chinn2000, the source of the log-odds-to-d conversion every effect size passes
through, carries a PMID and no DOI. `citations resolve` found one, and Crossref
returns it as Chinn, Stat Med 19(22):3127-3131, 2000, matching the entry on every
field. It is not added here. The DOI contains angle brackets, which an OT1
document typesets as mathematical brackets, so the printed reference would carry
a string that does not resolve. The PMID already makes the entry checkable, and
the DOI is recorded in the citation library's enrichment overlay instead.

The citation key hu2019 names an author and year belonging to neither the entry
nor its source; the entry is Filippini, Kruja and Del Giovane, 2021. Keys are not
printed, so renaming it would change two manuscripts and no reader's experience.
It is left, and recorded here.

v6 is not modified.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "references_v6_checked.bib"
DST = REPO / "paper" / "references_v7_audited.bib"

EDITS: list[tuple[str, str, str]] = [
    (
        "juergens2023ganitumab: issue 12 -> 11, per Crossref and PubMed 36669140",
        "  pages   = {2098--2107},\n  year    = {2023},\n"
        "  doi     = {10.1200/JCO.22.01815},",
        "  pages   = {2098--2107},\n  year    = {2023},\n"
        "  doi     = {10.1200/JCO.22.01815},\n  pmid    = {36669140},",
    ),
    (
        "juergens2023ganitumab: restore the published subtitle",
        "Metastatic {Ewing} Sarcoma},",
        "Metastatic {Ewing} Sarcoma: A Report From the "
        "{Children's Oncology Group}},",
    ),
    (
        "juergens2023ganitumab: the issue itself",
        "  volume  = {41},\n  number  = {12},",
        "  volume  = {41},\n  number  = {11},",
    ),
    (
        "hu2019: add the issue and article number PubMed 34748215 gives",
        "  journal = {Cochrane Database of Systematic Reviews},\n"
        "  volume  = {11},\n  year    = {2021},",
        "  journal = {Cochrane Database of Systematic Reviews},\n"
        "  volume  = {11},\n  number  = {11},\n  pages   = {CD013874},\n"
        "  year    = {2021},",
    ),
]


def main() -> int:
    text = SRC.read_text()
    failures = [(label, text.count(old)) for label, old, _ in EDITS if text.count(old) != 1]
    if failures:
        print("ABORT -- these targets did not match exactly once:\n", file=sys.stderr)
        for label, count in failures:
            print(f"  [{count} matches] {label}", file=sys.stderr)
        return 1
    for label, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"  applied: {label}")

    # A bibliography edit that loses an entry silently drops a citation from the
    # rendered reference list and leaves a bare key in the PDF.
    before = SRC.read_text().count("\n@")
    assert text.count("\n@") == before, f"entry count moved: {before} -> {text.count(chr(10) + '@')}"
    assert text.count("@") - text.count("\n@") == 1, "the first entry is no longer first"
    for key in ("juergens2023ganitumab", "hu2019", "novonordisk2026zeus",
                "interleukin2012", "shumaker2003"):
        assert f"{{{key}," in text, f"{key} lost"
    assert "number  = {12}" not in text.split("juergens2023ganitumab")[1][:600], \
        "the wrong issue survived"
    assert text.count("{Children's Oncology Group}") == 1
    assert text.count("CD013874},") == 1, "the article number is duplicated"
    assert "10.1002/14651858.CD013874.pub2" in text, "the Cochrane DOI was disturbed"
    # Every entry but the SEC filing must now carry a fetchable identifier.
    bodies = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, re.DOTALL)
    bare = [key for key, body in bodies
            if "doi" not in body.lower() and "pmid" not in body.lower()]
    assert bare == ["novonordisk2026zeus"], f"entries with no identifier: {bare}"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
