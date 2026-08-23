"""Build references_v5_verified.bib from references_v4_resolved_ids.bib.

Run:  uv run python paper/patches/patch_bib_v5_metadata_corrections.py

Adding an identifier to an entry makes it checkable, and four of the twelve
entries that gained one in v4 turned out to disagree with the record they name.
Each correction below was confirmed against the Crossref record for the DOI, on
every field the entry carries.

ference2019 named European Heart Journal 40(23):1927-1935. The Ference ACLY
Mendelian randomization study is New England Journal of Medicine 2019;380:1033-
1042. The identifier the resolver first proposed, 10.1056/nejmc1908496, is
correspondence in the same journal carrying the same title, which is why title,
year, and first-author checks all passed on it; the article DOI is used here.

gill2021 named JAMA Network Open 4(9):e2124540. The paper is Wellcome Open
Research 2021;6:16, with the author list the entry gives.

han2020eosinophilasthma rendered three given names that do not match the source:
the first three authors of Nature Communications 11:1776 are Yi Han, Qiong Jia,
and Pedram Shafiei Jahani.

munger2006 gave the second author as Lindsey I. Levin; JAMA 296:2832 records
Lynn I. Levin.

Entries whose audit flags are the source's own deposit formatting -- Crossref
HTML entities in cheng2014 and thakkinstian2006, subtitles the publisher records
and the entry omits in hernan2008, hernan2016, juergens2023ganitumab, ogawa2014,
and shumaker2003, Cochrane's year-as-volume convention in hu2019, the article id
in place of the printed page range in lawlor2016, and the initials of John P. A.
Ioannidis in li2019uratemr -- are left as they are. Rewriting a correct entry to
match a publisher's rendering is not a correction.

references_v4_resolved_ids.bib is not modified.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "references_v4_resolved_ids.bib"
DST = REPO / "paper" / "references_v5_verified.bib"

# (bibtex key, field, expected current value, corrected value). A field set to
# None is removed. Every value was read off the Crossref record for the entry's
# DOI, not inferred from the entry.
CORRECTIONS: list[tuple[str, str, str, str | None]] = [
    ("ference2019", "journal", "European Heart Journal", "New England Journal of Medicine"),
    ("ference2019", "volume", "40", "380"),
    ("ference2019", "number", "23", None),
    ("ference2019", "pages", "1927--1935", "1033--1042"),
    ("ference2019", "doi", "10.1056/nejmc1908496", "10.1056/NEJMoa1806747"),
    ("gill2021", "journal", "JAMA Network Open", "Wellcome Open Research"),
    ("gill2021", "volume", "4", "6"),
    ("gill2021", "number", "9", None),
    ("gill2021", "pages", "e2124540", "16"),
    ("han2020eosinophilasthma", "author",
     "Han, Yunhui and Jia, Qifeng and Jahani, Parisa S. and others",
     "Han, Yi and Jia, Qiong and Jahani, Pedram Shafiei and others"),
    ("munger2006", "author",
     "Munger, Kassandra L. and Levin, Lindsey I. and Hollis, Bruce W. and "
     "Howard, Noel S. and Ascherio, Alberto",
     "Munger, Kassandra L. and Levin, Lynn I. and Hollis, Bruce W. and "
     "Howard, Noel S. and Ascherio, Alberto"),
]

ENTRY = re.compile(r"(@\w+\s*\{\s*([^,\s]+)\s*,)(.*?)(\n\})", re.DOTALL)


def field_pattern(name: str) -> re.Pattern:
    return re.compile(rf"^([ \t]*){name}([ \t]*=[ \t]*)\{{(.*?)\}}(,?)[ \t]*$",
                      re.MULTILINE | re.DOTALL)


def main() -> int:
    text = SRC.read_text()
    entries = {key: body for _h, key, body, _c in
               ((m.group(1), m.group(2), m.group(3), m.group(4)) for m in ENTRY.finditer(text))}

    # Refuse to guess. Every correction must find its field, exactly once, holding
    # exactly the value it claims to be replacing.
    problems: list[str] = []
    for key, field, expected, _new in CORRECTIONS:
        if key not in entries:
            problems.append(f"{key}: entry absent")
            continue
        found = field_pattern(field).findall(entries[key])
        if len(found) != 1:
            problems.append(f"{key}.{field}: {len(found)} matches")
        elif " ".join(found[0][2].split()) != " ".join(expected.split()):
            problems.append(f"{key}.{field}: holds {found[0][2].strip()!r}, "
                            f"expected {expected!r}")
    if problems:
        print("ABORT -- the source does not hold what these corrections assume:\n",
              file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    def rewrite(match: re.Match) -> str:
        header, key, body, closer = match.groups()
        for entry_key, field, _expected, new in CORRECTIONS:
            if entry_key != key:
                continue
            if new is None:
                body = field_pattern(field).sub("", body)
                body = re.sub(r"\n[ \t]*\n", "\n", body)
            else:
                body = field_pattern(field).sub(
                    lambda m, v=new: f"{m.group(1)}{field}{m.group(2)}{{{v}}}{m.group(4)}", body)
        return f"{header}{body}{closer}"

    rebuilt = ENTRY.sub(rewrite, text)

    assert rebuilt.count("@") == text.count("@"), "entry count changed"
    for key, field, expected, new in CORRECTIONS:
        block = next(m.group(3) for m in ENTRY.finditer(rebuilt) if m.group(2) == key)
        found = field_pattern(field).findall(block)
        if new is None:
            assert not found, f"{key}.{field} survived removal"
        else:
            assert len(found) == 1 and " ".join(found[0][2].split()) == " ".join(new.split()), \
                f"{key}.{field} did not take the new value"

    DST.write_text(rebuilt)
    for key, field, expected, new in CORRECTIONS:
        shown = "(removed)" if new is None else new
        print(f"  {key}.{field}")
        print(f"      was: {expected[:100]}")
        print(f"      now: {shown[:100]}")
    print(f"\n{len(CORRECTIONS)} fields corrected across "
          f"{len({c[0] for c in CORRECTIONS})} entries")
    print(f"wrote {DST.relative_to(REPO)}  ({SRC.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
