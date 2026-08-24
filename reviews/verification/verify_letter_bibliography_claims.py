"""Check every bibliography figure in the response letter against its artifact.

Run:  uv run python reviews/verification/verify_letter_bibliography_claims.py

The letter's reference-list section states counts (75 entries, 74 identified, 66
cited, 14 originally unidentified, 9 publisher-deposit flags) and six specific
metadata corrections. Each is checked here against the .bib files, the audit
report, and the compiled .aux -- not against the letter's own prose. A letter
that miscounts the bibliography it ships is worse than one that says nothing,
because a reviewer can check the count in a minute.

Exit 1 on any disagreement.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
def newest_letter() -> Path:
    """The highest-numbered RESPONSE_TO_REVIEWERS_vN.md.

    A pinned default goes stale at the next version bump, and then this script
    checks a superseded letter's counts against the current artifacts and
    reports failures that belong to a file nobody is sending.
    """
    versions = sorted(
        ((int(re.match(r"RESPONSE_TO_REVIEWERS_v(\d+)", path.stem).group(1)), path)
         for path in (REPO / "reviews").glob("RESPONSE_TO_REVIEWERS_v*.md")
         if re.match(r"RESPONSE_TO_REVIEWERS_v\d+", path.stem)),
        key=lambda pair: pair[0])
    if not versions:
        raise FileNotFoundError(f"no RESPONSE_TO_REVIEWERS_v*.md under {REPO / 'reviews'}")
    return versions[-1][1]


LETTER = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else newest_letter()
BIB_OLD = REPO / "paper" / "references_v3_zeus.bib"
BIB_NEW = REPO / "paper" / "references_v7_audited.bib"
MANUSCRIPT = REPO / "paper" / "paper_v22_audited_refs.tex"
AUX = MANUSCRIPT.with_suffix(".aux")
AUDIT = REPO / "reviews" / "verification" / "output" / \
    "bibliography_audit__references_v7_audited.json"

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.DOTALL)

# What the letter says was wrong, and what it says is right. Field values are
# checked as substrings of the entry body so brace protection does not matter.
CORRECTIONS = {
    "ference2019": {"journal": "New England Journal of Medicine",
                    "volume": "380", "pages": "1033--1042"},
    "gill2021": {"journal": "Wellcome Open Research", "volume": "6", "pages": "16"},
    "han2020eosinophilasthma": {"author": "Han, Yi and Jia, Qiong and Jahani, Pedram Shafiei"},
    "munger2006": {"author": "Levin, Lynn I."},
    # The two the second audit pass found. juergens carried an issue number
    # neither registry gives; hu2019 carried no issue and no article identifier.
    "juergens2023ganitumab": {"volume": "41", "number": "11", "pages": "2098--2107"},
    "hu2019": {"volume": "11", "number": "11", "pages": "CD013874"},
}
SUPERSEDED = {
    "ference2019": ["European Heart Journal", "1927--1935", "10.1056/nejmc1908496"],
    "gill2021": ["JAMA Network Open", "e2124540"],
    "han2020eosinophilasthma": ["Yunhui", "Qifeng", "Parisa"],
    "munger2006": ["Lindsey"],
    "juergens2023ganitumab": ["number  = {12}"],
    "hu2019": [],
}
# The subtitle both registries give and the entry had dropped.
SUBTITLE = "A Report From the {Children's Oncology Group}"


def entries(path: Path) -> dict[str, str]:
    return {key: body for _, key, body in ENTRY.findall(path.read_text())}


def has_identifier(body: str) -> bool:
    return bool(re.search(r"\n\s*(doi|pmid)\s*=", body))


def field(body: str, name: str) -> str:
    match = re.search(rf"\n\s*{name}\s*=\s*\{{(.*?)\}},?\s*\n", body, re.DOTALL)
    return " ".join(match.group(1).split()) if match else ""


def main() -> int:
    # A letter checked against a superseded artifact passes every count below
    # while measuring a file nobody is sending. The manuscript must be the one
    # that cites the bibliography being checked, and the .aux must be its own.
    cites = re.search(r"\\bibliography\{([^}]+)\}", MANUSCRIPT.read_text())
    if cites is None or cites.group(1) != BIB_NEW.stem:
        named = cites.group(1) if cites else "no bibliography"
        print(f"ABORT -- {MANUSCRIPT.name} cites {named}, not {BIB_NEW.stem}", file=sys.stderr)
        return 1
    if not AUX.exists():
        print(f"ABORT -- {AUX.name} does not exist (.aux is gitignored). Build it with:\n"
              f"    cd paper && latexmk -pdf {MANUSCRIPT.name}", file=sys.stderr)
        return 1

    failures: list[str] = []

    def check(label: str, got, want) -> None:
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  {label}: {got}" + ("" if ok else f"  (letter says {want})"))
        if not ok:
            failures.append(label)

    old, new = entries(BIB_OLD), entries(BIB_NEW)
    audit = json.loads(AUDIT.read_text())
    cited = set(re.findall(r"\\bibcite\{([^}]+)\}", AUX.read_text()))

    print("Bibliography counts")
    check("entries in the shipped bibliography", len(new), 75)
    check("entries carrying a DOI or PMID", sum(has_identifier(b) for b in new.values()), 74)
    unidentified = sorted(k for k, b in new.items() if not has_identifier(b))
    check("the entry without one", unidentified, ["novonordisk2026zeus"])
    check("entries the manuscript cites", len(cited), 66)
    check("entries with no identifier before this pass",
          sum(not has_identifier(b) for b in old.values()), 14)
    check("audit flags remaining", sum(1 for r in audit.values() if r.get("problems")), 9)

    print("\nRemoved entry")
    check("liu2024tg was in the previous bibliography", "liu2024tg" in old, True)
    check("liu2024tg is gone from the shipped one", "liu2024tg" in new, False)
    check("liu2024tg is cited nowhere", "liu2024tg" in cited, False)
    check("nothing else was dropped", sorted(set(old) - set(new)), ["liu2024tg"])

    print("\nEvery cited key resolves in the shipped bibliography")
    check("cited keys missing from the .bib", sorted(cited - set(new)), [])
    # The ZEUS announcement is cited and has no DOI by nature; it is pinned to
    # an SEC accession instead. 65 of the 66 cited entries carry a DOI or PMID.
    check("cited keys carrying an identifier", sum(has_identifier(new[k]) for k in cited), 65)
    check("the cited entry without one",
          sorted(k for k in cited if not has_identifier(new[k])), ["novonordisk2026zeus"])

    print("\nThe four corrections")
    for key, wanted in CORRECTIONS.items():
        body = new.get(key, "")
        for name, value in wanted.items():
            check(f"{key}.{name}", field(body, name) if name != "author"
                  else (value if value in field(body, "author") else field(body, "author")), value)
        for stale in SUPERSEDED[key]:
            check(f"{key} no longer carries {stale!r}", stale in body, False)

    print("\nThe dropped subtitle")
    check("juergens2023ganitumab carries the reporting group",
          SUBTITLE in new["juergens2023ganitumab"], True)

    print("\nThe letter states the same figures")
    text = LETTER.read_text()
    for phrase in ("75 entries", "74 of which carry an identifier", "Of the 66 entries the manuscript cites, 65 resolve",
                   "Fourteen entries carried no identifier", "Nine entries carry an audit flag",
                   "Twelve of the thirteen articles", "Two further entries are corrected",
                   "issue 11", "11(11):CD013874", "references_v7_audited.bib"):
        check(f"letter says {phrase!r}", phrase in text, True)

    print()
    if failures:
        print(f"{len(failures)} disagreement(s): " + "; ".join(failures))
        return 1
    print("Every bibliography figure in the letter matches the artifact it names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
