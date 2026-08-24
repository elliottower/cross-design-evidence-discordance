"""Check every bibliography entry against the record its identifier resolves to,
through the `citations` CLI and the shared citation library.

Run:  uv run python reviews/verification/audit_bibliography_cli.py [bib]

The counterpart to audit_bibliography.py, which does the same comparison with
this repository's own fetch-and-compare code. Two implementations reading the
same registries should reach the same verdict on every entry; where they differ,
one of them has a bug and the disagreement is the finding worth chasing. This one
also caches into the shared library, so the payloads are available to every paper
that cites the same work.

`citations audit` fetches Crossref (or PubMed) for each entry's DOI and compares
the stored metadata field by field. It catches the failure no other check sees: a
correct DOI carrying a wrong author list, year, or title. A hallucinated
reference and a mistyped volume look identical to LaTeX and different here.

The tool reports raw disagreements. Most are the registry's, not the
bibliography's -- Crossref stores one author for consortium papers, truncates
subtitles, deposits XML markup inside title strings, and records Cochrane volumes
as years. Each such case is adjudicated below against the payload that produced
it, with the evidence for the adjudication in the reason. Anything not on that
list fails, and so does an adjudicated key that stops disagreeing, since a stale
allowlist hides the next real defect behind a name that used to be innocent.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LIBRARY = Path(os.environ.get(
    "CITATIONS_HOME", Path.home() / "Documents/GitHub/citations-library"))
# The `citations` shim on PATH resolves to an editable install whose interpreter
# has no pydantic, so the tool is run out of its own project instead.
TOOL = Path(os.environ.get(
    "CITATIONS_REPO", Path.home() / "Documents/GitHub/citations"))
OUT = REPO / "reviews" / "verification" / "output" / "citations_audit.json"

# key -> why the disagreement is the registry's and the bibliography is right.
ADJUDICATED: dict[str, str] = {
    "elliott2009":
        "Crossref's deposit for 10.1001/jama.2009.954 carries one author, Paul "
        "Elliott, for a consortium paper. The entry names Elliott, Chambers and "
        "Zhang and marks the rest with `and others`, which is what JAMA printed.",
    "hernan2008":
        "The registry title stops at the colon. The entry carries the published "
        "subtitle, `an application to postmenopausal hormone therapy and coronary "
        "heart disease`.",
    "hernan2016":
        "Crossref has appended the float caption `Table 1.` to the title string.",
    "hu2019":
        "Crossref records Cochrane volumes as the year, 2021. PubMed 34748215 "
        "gives volume 11, issue 11, which is what the entry carries.",
    "lawlor2016":
        "Crossref gives the e-locator dyw314 in the page field. The entry gives "
        "the print pagination, 1866--1886, of Int J Epidemiol 45(6).",
    "li2019uratemr":
        "The entry spells Ioannidis' given name `John P. A.` where the deposit "
        "abbreviates it to `P. A.`",
    "ogawa2014":
        "The registry title contains the small-caps markup `<scp>L</scp>` and its "
        "surrounding newlines.",
    "shumaker2003":
        "The registry title stops before the cohort name. The entry carries the "
        "published subtitle, `the Women's Health Initiative Memory Study`.",
    "thakkinstian2006":
        "The Crossref deposit misspells the exposure as `complementary factor H`. "
        "The published title in Am J Epidemiol reads `complement factor H`.",
}

# Entries with no fetchable identifier, and why none exists.
NO_IDENTIFIER: dict[str, str] = {
    "novonordisk2026zeus":
        "A Novo Nordisk company announcement filed as SEC Form 6-K, accession "
        "0001171843-26-005109. Regulatory filings carry no DOI; the entry pins "
        "the accession number and the sec.gov URL instead.",
}


def main() -> int:
    bib = (Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else
           REPO / "paper" / "references_v7_audited.bib")
    if not bib.exists():
        print(f"no such bibliography: {bib}", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # The shared cache means a rerun re-reads payloads instead of re-fetching
    # them, so this is runnable offline once it has been run once.
    run = subprocess.run(
        ["uv", "run", "--project", str(TOOL), "citations", "audit",
         "--bib", str(bib), "--cache", str(LIBRARY / ".audit-cache"),
         "--json", str(OUT), "--quiet"],
        capture_output=True, text=True)
    if not OUT.exists():
        print(run.stdout + run.stderr, file=sys.stderr)
        print("citations audit wrote no report", file=sys.stderr)
        return 1

    # papers.yaml pins one bibliography per paper. If it names a superseded
    # version, the library holds records for citations the manuscript no longer
    # makes, and every check here passes while measuring the wrong file.
    registered = re.search(
        r"^  cross-design-evidence-discordance:\n    bib: (.+)$",
        (LIBRARY / "papers.yaml").read_text(), re.M)
    stale = None
    if registered is None:
        stale = (f"the paper is not registered in {LIBRARY / 'papers.yaml'}, so "
                 f"none of its references are in the shared library")
    elif Path(registered.group(1)).resolve() != bib:
        stale = (f"papers.yaml registers {registered.group(1)}\n"
                 f"    but the manuscript cites {bib}")

    entries = json.loads(OUT.read_text())["entries"]
    mismatched = {k: v["problems"] for k, v in entries.items()
                  if v["status"] == "mismatch"}
    unidentified = [k for k, v in entries.items() if v["status"] == "no identifier"]

    failures: list[str] = [stale] if stale else []
    for key, problems in sorted(mismatched.items()):
        if key not in ADJUDICATED:
            failures.append(f"{key} disagrees with its registry record and is "
                            f"not adjudicated: {'; '.join(problems)}")
    for key in sorted(ADJUDICATED):
        if key not in entries:
            failures.append(f"{key} is adjudicated but no longer in the bibliography")
        elif key not in mismatched:
            failures.append(f"{key} is adjudicated but now agrees with its record "
                            f"-- drop it from ADJUDICATED so the next real "
                            f"disagreement on this key is not swallowed")
    for key in sorted(unidentified):
        if key not in NO_IDENTIFIER:
            failures.append(f"{key} has no fetchable identifier and no stated reason")
    for key in sorted(NO_IDENTIFIER):
        if key in entries and key not in unidentified:
            failures.append(f"{key} now carries an identifier -- drop it from "
                            f"NO_IDENTIFIER and let the audit check it")

    print(f"bibliography  {bib.relative_to(REPO)}")
    print(f"entries       {len(entries)}")
    print(f"agree         {sum(1 for v in entries.values() if v['status'] == 'ok')}")
    print(f"adjudicated   {len(mismatched)}  (registry-side, each with a stated reason)")
    print(f"no identifier {len(unidentified)}")
    print()
    for key, problems in sorted(mismatched.items()):
        print(f"  {key}")
        print(f"    tool  {problems[0]}")
        print(f"    why   {ADJUDICATED.get(key, 'UNADJUDICATED')}")
    for key in sorted(unidentified):
        print(f"  {key}")
        print(f"    why   {NO_IDENTIFIER.get(key, 'UNEXPLAINED')}")

    if failures:
        print("\nFAILED", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"\nEvery entry either matches its registry record or has a stated "
          f"reason it cannot.\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
