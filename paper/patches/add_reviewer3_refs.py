"""Append the two Reviewer 3 suggested references to references.bib.

Run:  uv run python paper/patches/add_reviewer3_refs.py

Metadata is fetched live from Crossref by DOI. Nothing is typed from memory.
The script refuses to run twice (it checks for the keys first).
"""

import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIB = REPO / "paper" / "references.bib"

TARGETS = [
    ("brancati2021rituximab", "10.3389/fimmu.2021.661882"),
    ("gozzo2023htams", "10.3389/fphar.2023.1169400"),
]

UA = "cross-design-evidence/1.0 (mailto:elliot@elliottower.ai)"


def crossref(doi: str) -> dict:
    req = urllib.request.Request(
        f"https://api.crossref.org/works/{doi}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=30) as fh:
        return json.load(fh)["message"]


def author_field(msg: dict) -> str:
    parts = []
    for a in msg.get("author", []):
        given, family = a.get("given", ""), a.get("family", "")
        parts.append(f"{family}, {given}".strip(", "))
    return " and ".join(parts)


def to_bibtex(key: str, msg: dict) -> str:
    year = msg["issued"]["date-parts"][0][0]
    fields = [
        ("author", author_field(msg)),
        ("title", "{" + msg["title"][0] + "}"),
        ("journal", msg.get("container-title", [""])[0]),
        ("year", str(year)),
        ("volume", msg.get("volume", "")),
        ("pages", msg.get("page", "") or msg.get("article-number", "")),
        ("doi", msg.get("DOI", "")),
    ]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@article{{{key},\n{body}\n}}\n"


def main() -> int:
    text = BIB.read_text()
    new_entries = []
    for key, doi in TARGETS:
        if f"@article{{{key}," in text or f"{{{key}," in text:
            print(f"  already present, skipping: {key}")
            continue
        msg = crossref(doi)
        entry = to_bibtex(key, msg)
        new_entries.append(entry)
        print(f"  fetched {doi}")
        print(f"    title: {msg['title'][0]}")
        print(f"    journal: {msg.get('container-title', [''])[0]} "
              f"{msg.get('volume', '')} ({msg['issued']['date-parts'][0][0]})")
        print(f"    authors: {author_field(msg)}")
    if not new_entries:
        print("nothing to add")
        return 0
    if not text.endswith("\n"):
        text += "\n"
    BIB.write_text(text + "\n" + "\n".join(new_entries))
    print(f"\nappended {len(new_entries)} entries to {BIB.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
