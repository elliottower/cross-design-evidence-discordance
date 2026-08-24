"""Check every bibliography entry against the record its identifier resolves to.

Run:  uv run python reviews/verification/audit_bibliography.py

For each entry in paper/references.bib carrying a DOI, fetch the Crossref record;
for each carrying a PMID, fetch the PubMed record. Compare title, journal, year,
volume, pages, and the author list. Author given names are compared only where
the source supplies them (Crossref sometimes does not), so a mismatch reported on
a name is a real disagreement and not a gap in the source record.

Two failure modes motivate this. A fabricated author list attached to a real DOI
resolves cleanly in any DOI checker and is invisible to `citations verify`, which
checks quoted passages rather than metadata. A truncated author list without an
`and others` marker looks complete and is not.

Responses are cached under reviews/verification/output/bib_audit_cache/ so reruns
are offline and the audit is reproducible from the cached payloads.

Exits non-zero if any entry mismatches or fails to resolve.
"""

import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIB = REPO / "paper" / "references.bib"
CACHE = Path(__file__).resolve().parent / "output" / "bib_audit_cache"
REPORTS = Path(__file__).resolve().parent / "output"
MAILTO = "elliot@elliottower.ai"
DELAY = 0.34

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.DOTALL)
FIELD = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\n\s*\w+\s*=|\Z)", re.DOTALL)


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for _etype, key, body in ENTRY.findall(text):
        out[key] = {name.lower(): " ".join(value.split())
                    for name, value in FIELD.findall(body)}
    return out


def fold(text: str) -> str:
    """Lowercase, strip accents, LaTeX and XML markup, and punctuation, for comparison only."""
    # Crossref deposits titles with the entities double-escaped, so a Greek letter
    # arrives as `&amp;alpha;` and needs two passes to become the character the
    # journal printed. Left encoded, every such title reads as a mismatch.
    for _ in range(2):
        text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def fold_name(text: str) -> str:
    """Fold a personal name to bare alphanumerics.

    A BibTeX accent is a backslash-punctuation pair (Munaf{\\'o}), which survives
    the LaTeX-command strip and then splits the name in two once punctuation
    becomes a space. Dropping separators entirely makes 'Munaf o' and 'Munafo'
    compare equal, and equally makes 'Glade Bender' and 'gladebender' compare
    equal, which is what a family-name check wants.
    """
    return fold(text).replace(" ", "")


def split_authors(field: str) -> tuple[list[tuple[str, str]], bool]:
    """Split a BibTeX author field into (family, given) pairs, plus a truncation flag."""
    parts = [p.strip() for p in re.split(r"\s+and\s+", field) if p.strip()]
    truncated = bool(parts) and fold(parts[-1]) == "others"
    if truncated:
        parts = parts[:-1]
    people: list[tuple[str, str]] = []
    for part in parts:
        if "," in part:
            family, given = part.split(",", 1)
        else:
            words = part.split()
            family, given = (words[-1], " ".join(words[:-1])) if len(words) > 1 else (part, "")
        people.append((fold_name(family), fold_name(given)))
    return people, truncated


def fetch(url: str, name: str) -> str | None:
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / name
    if cached.exists():
        return cached.read_text() or None
    request = urllib.request.Request(
        url, headers={"User-Agent": f"cross-design-evidence bib audit (mailto:{MAILTO})"})
    time.sleep(DELAY)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read().decode("utf-8", "replace")
    except Exception as exc:                                    # network or 404
        print(f"    fetch failed ({name}): {exc}", file=sys.stderr)
        return None
    cached.write_text(body)
    return body


def crossref(doi: str) -> dict | None:
    safe = urllib.parse.quote(doi, safe="")
    body = fetch(f"https://api.crossref.org/works/{safe}",
                 f"crossref_{re.sub(r'[^A-Za-z0-9]', '_', doi)}.json")
    if not body:
        return None
    try:
        message = json.loads(body)["message"]
    except Exception:
        return None
    authors = [(fold_name(a.get("family", "")), fold_name(a.get("given", "")))
               for a in message.get("author", []) if a.get("family")]
    # A journal that publishes online ahead of print carries two legitimate
    # years. Accept either, so an online-first date is not reported as an error.
    years = []
    for field in ("published-print", "published-online", "issued", "created"):
        parts = (message.get(field) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            years.append(str(parts[0][0]))
    return {
        "title": (message.get("title") or [""])[0],
        "journal": (message.get("container-title") or [""])[0],
        "year": years[0] if years else "",
        "years": years,
        "volume": message.get("volume") or "",
        "pages": message.get("page") or message.get("article-number") or "",
        "authors": authors,
        "source": "crossref",
    }


def pubmed(pmid: str) -> dict | None:
    body = fetch(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={urllib.parse.quote(pmid)}&retmode=xml",
        f"pubmed_{pmid}.xml")
    if not body:
        return None
    try:
        article = ET.fromstring(body).find(".//PubmedArticle")
    except ET.ParseError:
        return None
    if article is None:
        return None
    title_node = article.find(".//ArticleTitle")
    journal = article.find(".//Journal")
    authors = []
    for person in article.findall(".//Author"):
        family = person.findtext("LastName")
        if family:
            authors.append((fold_name(family), fold_name(person.findtext("ForeName") or "")))
    return {
        "title": "".join(title_node.itertext()) if title_node is not None else "",
        "journal": (journal.findtext("ISOAbbreviation") or journal.findtext("Title") or ""),
        "year": (journal.findtext(".//Year") or ""),
        "volume": (journal.findtext(".//Volume") or ""),
        "pages": (article.findtext(".//MedlinePgn") or ""),
        "authors": authors,
        "years": [(journal.findtext(".//Year") or "")],
        "source": "pubmed",
    }


def compare(key: str, fields: dict[str, str], record: dict) -> list[str]:
    problems: list[str] = []
    bib_title, src_title = fold(fields.get("title", "")), fold(record["title"].rstrip("."))
    if bib_title and src_title and bib_title != src_title:
        if src_title.startswith(bib_title) or bib_title.startswith(src_title):
            problems.append(f"title (subtitle only): source reads {record['title']!r}")
        else:
            problems.append(f"title: bib {fields['title']!r} vs source {record['title']!r}")

    bib_year = fields.get("year", "").strip()
    src_years = [y for y in record.get("years", []) if y]
    if bib_year and src_years and bib_year not in src_years:
        problems.append(f"year: bib {bib_year} vs source {'/'.join(dict.fromkeys(src_years))}")

    bib_vol, src_vol = fields.get("volume", "").strip(), str(record["volume"]).strip()
    if bib_vol and src_vol and bib_vol != src_vol:
        problems.append(f"volume: bib {bib_vol} vs source {src_vol}")

    # Pages: BibTeX uses en-dash ranges, PubMed uses abbreviated end pages
    # (1214-24 for 1214-1224), so compare on the start page alone.
    bib_pages = re.sub(r"[^0-9a-zA-Z]", "", fields.get("pages", "").split("-")[0])
    src_pages = re.sub(r"[^0-9a-zA-Z]", "", str(record["pages"]).split("-")[0])
    if bib_pages and src_pages and bib_pages != src_pages:
        problems.append(f"pages: bib {fields.get('pages')!r} vs source {record['pages']!r}")

    bib_authors, truncated = split_authors(fields.get("author", ""))
    src_authors = record["authors"]
    if bib_authors and src_authors:
        for index, (bib_person, src_person) in enumerate(zip(bib_authors, src_authors)):
            if bib_person[0] != src_person[0]:
                problems.append(
                    f"author {index + 1} family: bib {bib_person[0]!r} vs source {src_person[0]!r}")
                continue
            # Compare only what both sides supply: initials against initials.
            bib_given, src_given = bib_person[1], src_person[1]
            if bib_given and src_given:
                if len(bib_given) <= 2 or len(src_given) <= 2:
                    if bib_given[:1] != src_given[:1]:
                        problems.append(
                            f"author {index + 1} initial: bib {bib_given!r} vs source {src_given!r}")
                elif bib_given != src_given:
                    problems.append(
                        f"author {index + 1} given: bib {bib_given!r} vs source {src_given!r}")
        if len(bib_authors) < len(src_authors) and not truncated:
            problems.append(
                f"author list stops at {len(bib_authors)} of {len(src_authors)} "
                "with no 'and others' marker")
        if len(bib_authors) > len(src_authors):
            problems.append(
                f"author list has {len(bib_authors)} names, source has {len(src_authors)}")
    return problems


def main() -> int:
    bib = Path(sys.argv[1]) if len(sys.argv) > 1 else BIB
    # The report is the rebuilder's input. Naming it after the file audited keeps
    # a run against a rebuilt bibliography from overwriting the original's report,
    # which would silently reduce the rebuild to a no-op.
    report = REPORTS / f"bibliography_audit__{bib.stem}.json"
    print(f"auditing {bib}\n")
    entries = parse_bib(bib.read_text())
    results: dict[str, dict] = {}
    unresolved: list[str] = []
    mismatched: list[str] = []
    unidentified: list[str] = []

    for key in sorted(entries):
        fields = entries[key]
        doi, pmid = fields.get("doi", "").strip(), fields.get("pmid", "").strip()
        if not doi and not pmid:
            unidentified.append(key)
            results[key] = {"status": "no identifier"}
            continue
        record = crossref(doi) if doi else None
        if record is None and pmid:
            record = pubmed(pmid)
        if record is None:
            unresolved.append(key)
            results[key] = {"status": "unresolved", "doi": doi, "pmid": pmid}
            continue
        problems = compare(key, fields, record)
        results[key] = {
            "status": "mismatch" if problems else "ok",
            "checked_against": record["source"],
            "doi": doi, "pmid": pmid,
            "problems": problems,
        }
        if problems:
            mismatched.append(key)

    for key in mismatched:
        print(f"MISMATCH  {key}  (vs {results[key]['checked_against']})")
        for problem in results[key]["problems"]:
            print(f"    {problem}")
    if unresolved:
        print("\nUNRESOLVED (identifier did not fetch; no measurement made):")
        for key in unresolved:
            print(f"    {key}")
    if unidentified:
        print("\nNO IDENTIFIER (not checkable by this script):")
        for key in unidentified:
            print(f"    {key}")

    checked = len(entries) - len(unidentified) - len(unresolved)
    print(f"\n{len(entries)} entries; {checked} checked; "
          f"{checked - len(mismatched)} clean; {len(mismatched)} mismatched; "
          f"{len(unresolved)} unresolved; {len(unidentified)} without an identifier")

    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(f"wrote {report.relative_to(REPO)}")
    return 1 if mismatched or unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
