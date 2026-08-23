"""Pin the ZEUS readout announcement into the citations library, artifact and all.

Run:  uv run python reviews/verification/pin_zeus_source.py

The manuscript's IL-6R paragraph rests on a company announcement, not a journal
article, so there is no DOI to resolve and `citations audit` has nothing to check
it against. What can be checked is the artifact: the announcement was filed with
the SEC as a Form 6-K the same day, and the filing is content-addressed here by
sha256 so the sentence in the paper stays tied to a byte-identical document.

Downloads the filing, verifies the two numbers the paper quotes appear in it,
writes the artifact into the library's pdfs/ directory under its slug, and writes
the record. Re-running is a no-op when the bytes are unchanged.
"""

import hashlib
import os
import re
import sys
import urllib.request
from pathlib import Path

import yaml

LIBRARY = Path(os.environ.get("CITATIONS_HOME", "")).expanduser()
URL = "https://www.sec.gov/Archives/edgar/data/353278/000117184326005109/f6k_073126.htm"
PROJECT = "cross-design-evidence-discordance"
BIB_KEY = "novonordisk2026zeus"
TITLE = ("Novo Nordisk provides update on the ZEUS phase 3 trial in people with "
         "ASCVD, CKD and inflammation")
AUTHOR = "Novo Nordisk A/S"

# The sentences the manuscript rests on. Checked against the fetched bytes before
# anything is written, so a filing that moved or changed cannot be pinned silently.
QUOTES = [
    "hazard ratio, 0.99; 95% confidence interval, 0.88 to 1.11",
    "did not translate into major adverse cardiovascular events (MACE) risk reduction",
    "ziltivekimab demonstrated target engagement and inhibition of the IL-6 pathway",
]


def slug_for(title: str, author: str) -> str:
    """The same identity `citations build` computes, so a rebuild will not duplicate this."""
    base = re.sub(r"[^a-z0-9]+", "", (title + author).lower())
    return "t-" + hashlib.sha256(base.encode()).hexdigest()[:16]


def visible_text(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    for entity, char in (("&nbsp;", " "), ("&#8217;", "’"), ("&amp;", "&"),
                         ("&#8220;", "“"), ("&#8221;", "”")):
        text = text.replace(entity, char)
    return " ".join(text.split())


def main() -> int:
    if not LIBRARY.is_dir():
        print(f"ABORT -- CITATIONS_HOME is not a directory: {LIBRARY}", file=sys.stderr)
        return 1

    request = urllib.request.Request(
        URL, headers={"User-Agent": "Elliot Tower elliot@elliottower.ai"})
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()

    text = visible_text(payload.decode("utf-8", "replace"))
    missing = [q for q in QUOTES if q not in text]
    if missing:
        print("ABORT -- the filing does not contain what the paper quotes:", file=sys.stderr)
        for quote in missing:
            print(f"    {quote!r}", file=sys.stderr)
        return 1
    print(f"{len(QUOTES)} quoted passages found in the filing")

    slug = slug_for(TITLE, AUTHOR)
    artifact = LIBRARY / "pdfs" / f"{slug}.htm"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(payload)

    record_path = LIBRARY / "records" / f"{slug}.yaml"
    record = yaml.safe_load(record_path.read_text()) if record_path.exists() else {}
    cited_by = record.get("cited_by") or {}
    cited_by[PROJECT] = {"key": BIB_KEY}
    record_path.write_text(yaml.safe_dump({
        "slug": slug,
        "title": TITLE,
        "authors": [AUTHOR],
        "year": "2026",
        "venue": "Novo Nordisk company announcement (SEC Form 6-K, "
                 "accession 0001171843-26-005109)",
        "doi": "",
        "arxiv": "",
        "et_al": False,
        "url": URL,
        "sha256": digest,
        "local": f"pdfs/{slug}.htm",
        "cited_by": cited_by,
    }, sort_keys=False, allow_unicode=True))

    print(f"slug    {slug}")
    print(f"sha256  {digest}")
    print(f"wrote   {record_path}")
    print(f"wrote   {artifact}  ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
