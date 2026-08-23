"""Find a DOI for each bibliography entry that carries none, by verified match.

Run:  uv run python reviews/verification/resolve_missing_identifiers.py [bib]

Queries Crossref with the entry's own title, journal, and year, then accepts a
candidate only when three independent things agree: the normalized title is at
least 92% similar, the year is within one, and the first author's surname
matches. A title search that returns a real paper by the wrong authors is the
failure this guards against -- it resolves cleanly in any DOI checker and is
invisible to a reader.

Nothing is written into the bibliography. The script prints each accepted match
with the title it matched against, so a person can read the pair before any
identifier is adopted, and writes the accepted mapping to
output/resolved_identifiers__<stem>.json for a patch script to consume.

Rejections are printed too, with the reason and the best candidate seen, since a
rejected entry is a thing to look up by hand rather than a thing to ignore.
"""

import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "output"
CACHE = OUT / "bib_audit_cache"
MAILTO = "elliot@elliottower.ai"
DELAY = 0.34

TITLE_FLOOR = 0.92
YEAR_SLACK = 1

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.DOTALL)
FIELD = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\n\s*\w+\s*=|\Z)", re.DOTALL)


def fold(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for etype, key, body in ENTRY.findall(text):
        fields = {n.lower(): " ".join(v.split()) for n, v in FIELD.findall(body)}
        fields["_type"] = etype.lower()
        out[key] = fields
    return out


def first_surname(author_field: str) -> str:
    first = re.split(r"\s+and\s+", author_field)[0].strip()
    if "," in first:
        return fold(first.split(",")[0])
    return fold(first.split()[-1]) if first.split() else ""


def crossref_search(title: str, journal: str, year: str) -> list[dict]:
    """Ask Crossref for candidates, caching the response by the query itself."""
    query = urllib.parse.urlencode({
        "query.bibliographic": f"{title} {journal} {year}".strip(),
        "rows": "5",
        "select": "DOI,title,author,container-title,issued,published-print",
        "mailto": MAILTO,
    })
    stamp = re.sub(r"[^A-Za-z0-9]", "_", fold(title))[:120]
    path = CACHE / f"crossref_search_{stamp}.json"
    if path.exists():
        return json.loads(path.read_text()).get("message", {}).get("items", [])
    url = f"https://api.crossref.org/works?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": f"cdd-resolver ({MAILTO})"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode())
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))
    time.sleep(DELAY)
    return payload.get("message", {}).get("items", [])


def candidate_year(item: dict) -> str:
    for field in ("published-print", "issued"):
        parts = (item.get(field) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return ""


def assess(entry: dict, item: dict) -> tuple[bool, str, float]:
    """Accept only on title, year, and first author agreeing independently."""
    source_title = (item.get("title") or [""])[0]
    ratio = difflib.SequenceMatcher(None, fold(entry.get("title", "")),
                                    fold(source_title)).ratio()
    if ratio < TITLE_FLOOR:
        return False, f"title similarity {ratio:.2f} below {TITLE_FLOOR}", ratio
    source_year, bib_year = candidate_year(item), entry.get("year", "")
    if source_year and bib_year and abs(int(source_year) - int(bib_year)) > YEAR_SLACK:
        return False, f"year {source_year} against bib {bib_year}", ratio
    authors = [a for a in item.get("author", []) if a.get("family")]
    wanted = first_surname(entry.get("author", ""))
    if wanted and authors and fold(authors[0]["family"]) != wanted:
        return False, f"first author {authors[0]['family']} against bib {wanted}", ratio
    return True, "", ratio


def main() -> int:
    bib = (Path(sys.argv[1]).resolve() if len(sys.argv) > 1
           else REPO / "paper" / "references_v3_zeus.bib")
    entries = parse_bib(bib.read_text())
    targets = {k: e for k, e in entries.items()
               if e["_type"] == "article" and "doi" not in e and "pmid" not in e}
    print(f"{bib.relative_to(REPO)}: {len(entries)} entries, "
          f"{len(targets)} articles without an identifier\n")

    accepted: dict[str, str] = {}
    for key, entry in sorted(targets.items()):
        items = crossref_search(entry.get("title", ""), entry.get("journal", ""),
                                entry.get("year", ""))
        best: tuple[float, str, dict] = (0.0, "no candidates returned", {})
        for item in items:
            ok, reason, ratio = assess(entry, item)
            if ok:
                doi = item["DOI"]
                accepted[key] = doi
                print(f"ACCEPT  {key}")
                print(f"    bib    {entry.get('title', '')[:110]}")
                print(f"    source {(item.get('title') or [''])[0][:110]}")
                print(f"    doi    {doi}   (title {ratio:.3f}, "
                      f"{candidate_year(item)}, {(item.get('container-title') or [''])[0][:60]})")
                break
            if ratio > best[0]:
                best = (ratio, reason, item)
        else:
            ratio, reason, item = best
            print(f"REJECT  {key}  -- {reason}")
            print(f"    bib    {entry.get('title', '')[:110]}")
            if item:
                print(f"    best   {(item.get('title') or [''])[0][:110]}")
                print(f"    doi    {item.get('DOI', '')}")
        print()

    report = OUT / f"resolved_identifiers__{bib.stem}.json"
    report.write_text(json.dumps(accepted, indent=2, sort_keys=True) + "\n")
    print(f"{len(accepted)}/{len(targets)} resolved to a verified DOI")
    print(f"wrote {report.relative_to(REPO)}  ({bib.name} unmodified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
