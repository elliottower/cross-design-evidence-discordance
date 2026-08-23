"""Rewrite bibliography metadata from the record each identifier resolves to.

Run:  uv run python paper/patches/rebuild_bib_from_records.py

Reads paper/references.bib and the payloads audit_bibliography.py cached, and
writes paper/references_v2_resolved.bib with author, year, volume, pages, and
journal taken from Crossref or PubMed wherever the audit found a disagreement.
The input file is not modified.

Fields are replaced only where the audit flagged them, so an entry the audit
passed comes through byte-identical. Titles are left alone: the bib versions
carry brace protection for capitalization that the source records do not, and
the four title disagreements are handled as named overrides below rather than
by overwriting.

Author lists are replaced only when the source list is at least as long as the
bib's. Crossref returns a single author for some older records, and rewriting a
correct three-name list down to one would be a regression dressed as a fix.
"""

import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIB = REPO / "paper" / "references.bib"
OUT = REPO / "paper" / "references_v2_resolved.bib"
CACHE = REPO / "reviews" / "verification" / "output" / "bib_audit_cache"
AUDIT = REPO / "reviews" / "verification" / "output" / "bibliography_audit__references.json"

ENTRY = re.compile(r"(@\w+\s*\{\s*([^,\s]+)\s*,)(.*?)(\n\})", re.DOTALL)
FIELD_LINE = re.compile(r"^(\s*)(\w+)(\s*=\s*)([{\"])(.*?)([}\"])(,?)\s*$", re.MULTILINE | re.DOTALL)

# Sentinel: drop the field entirely. A value of None means "leave alone".
DELETE = "\0delete"

# Entries the general rule must not touch, with the reason.
OVERRIDES: dict[str, dict[str, str | None]] = {
    # Crossref lists one author for this JAMA record; the bib's three names plus
    # "and others" is the better list.
    "elliott2009": {"author": None},
    # Crossref's title reads "complementary factor H", which is a typo in the
    # deposited metadata; the published title is "complement factor H".
    "thakkinstian2006": {"title": None},
    # Cochrane numbers volumes by year and issues 1-12; the bib's volume 11 with
    # year 2021 is the conventional rendering.
    "hu2019": {"volume": None},
    # The PMID on this entry resolves to an unrelated neurology paper and the
    # journal is wrong. Everything is replaced from the correct BMJ record.
    "li2019uratemr": {
        "journal": "The {BMJ}",
        "year": "2017",
        "volume": "357",
        "number": DELETE,
        "pages": "j2376",
        "pmid": "28592419",
        "doi": "10.1136/bmj.j2376",
        "author": "Li, Xue and Meng, Xiangrui and Timofeeva, Maria and Tzoulaki, Ioanna "
                  "and Tsilidis, Konstantinos K. and Ioannidis, John P. A. and others",
    },
    # The bib title drops the consensus-statement half of a two-part title.
    "ference2019ldl": {
        "title": "Low-density lipoproteins cause atherosclerotic cardiovascular disease. 1. "
                 "Evidence from genetic, epidemiologic, and clinical studies. A consensus "
                 "statement from the {European Atherosclerosis Society} {Consensus Panel}",
    },
    # The source reports 95% CI 0.26 to 0.76; the stored note said 0.22--0.88.
    "zheng2020sglt2mr": {
        "annote": "Drug-target MR: SGLT2 inhibition $\\to$ lower HF risk "
                  "(OR 0.44, 95\\% CI 0.26--0.76, $P$ = 0.003). But see paradox paper "
                  "for caveats.",
    },
}

REPLACEABLE = ("author", "year", "volume", "pages", "journal")


def fold(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def latex_escape_name(name: str) -> str:
    """Render a Unicode personal name as BibTeX, preserving accents."""
    accents = {"\u0301": "'", "\u0300": "`", "\u0308": '"', "\u0302": "^",
               "\u0303": "~", "\u030c": "v", "\u0327": "c", "\u0306": "u"}
    out = []
    for char in unicodedata.normalize("NFD", name):
        if unicodedata.combining(char):
            if out and char in accents:
                # Brace the argument: \c{c} is a cedilla, \cc is an undefined
                # control sequence that stops the LaTeX run.
                out[-1] = f"{{\\{accents[char]}{{{out[-1]}}}}}"
            continue
        out.append(char)
    return "".join(out).replace("&", r"\&")


def merge_authors(source: list[tuple[str, str]], bib_field: str) -> list[str]:
    """Render a source author list, keeping bib given names the source omits.

    Crossref sometimes deposits a family name with no given name. Overwriting a
    correct bib entry with the bare surname would lose information the audit
    never disputed, so the bib rendering is kept whenever the families agree and
    the source has nothing to add.
    """
    bib_parts = [p.strip() for p in re.split(r"\s+and\s+", bib_field) if p.strip()]
    out = []
    for index, (family, given) in enumerate(source):
        if not given and index < len(bib_parts):
            bib_family = bib_parts[index].split(",")[0].strip()
            if fold(bib_family) == fold(family):
                out.append(bib_parts[index])
                continue
        out.append(f"{family}, {given}" if given else family)
    return out


def crossref_authors(doi: str) -> list[tuple[str, str]]:
    path = CACHE / f"crossref_{re.sub(r'[^A-Za-z0-9]', '_', doi)}.json"
    if not path.exists():
        return []
    message = json.loads(path.read_text())["message"]
    return [(latex_escape_name(p["family"]), latex_escape_name(p.get("given") or ""))
            for p in message.get("author", []) if p.get("family")]


def crossref_fields(doi: str) -> dict[str, str]:
    path = CACHE / f"crossref_{re.sub(r'[^A-Za-z0-9]', '_', doi)}.json"
    if not path.exists():
        return {}
    message = json.loads(path.read_text())["message"]
    years = []
    for field in ("published-print", "published-online", "issued"):
        parts = (message.get(field) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            years.append(str(parts[0][0]))
    pages = message.get("page") or message.get("article-number") or ""
    return {
        "journal": (message.get("container-title") or [""])[0],
        "year": years[0] if years else "",
        "volume": str(message.get("volume") or ""),
        "pages": pages.replace("-", "--") if "-" in pages else pages,
    }


def pubmed_authors(pmid: str) -> list[tuple[str, str]]:
    path = CACHE / f"pubmed_{pmid}.xml"
    if not path.exists():
        return []
    article = ET.fromstring(path.read_text()).find(".//PubmedArticle")
    if article is None:
        return []
    return [(latex_escape_name(p.findtext("LastName")),
             latex_escape_name(p.findtext("ForeName") or ""))
            for p in article.findall(".//Author") if p.findtext("LastName")]


def main() -> int:
    if not AUDIT.exists():
        print(f"ABORT -- no audit report at {AUDIT.relative_to(REPO)}.\n"
              "Run: uv run python reviews/verification/audit_bibliography.py",
              file=sys.stderr)
        return 1
    audit = json.loads(AUDIT.read_text())
    text = BIB.read_text()
    changes: list[tuple[str, str, str, str]] = []

    def rewrite_entry(match: re.Match) -> str:
        header, key, body, closer = match.groups()
        report = audit.get(key, {})
        problems = report.get("problems", [])
        doi_match = re.search(r"doi\s*=\s*[{\"]([^}\"]+)", body)
        pmid_match = re.search(r"pmid\s*=\s*[{\"]([^}\"]+)", body)
        doi = doi_match.group(1).strip() if doi_match else ""
        pmid = pmid_match.group(1).strip() if pmid_match else ""

        wanted: dict[str, str] = {}
        if problems:
            source = crossref_fields(doi) if doi else {}
            for field in ("year", "volume", "pages", "journal"):
                if any(p.startswith(f"{field}:") for p in problems) and source.get(field):
                    wanted[field] = source[field]
            if any(p.startswith("pages:") for p in problems) and source.get("pages"):
                wanted["pages"] = source["pages"]
            if any("family:" in p or "given:" in p or "initial:" in p or "and others" in p
                   for p in problems):
                names = crossref_authors(doi) if doi else pubmed_authors(pmid)
                bib_author = re.search(r"author\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", body, re.DOTALL)
                bib_field = " ".join(bib_author.group(1).split()) if bib_author else ""
                bib_count = len(re.split(r"\s+and\s+", bib_field)) if bib_field else 0
                if names and len(names) >= bib_count:
                    wanted["author"] = " and ".join(merge_authors(names, bib_field))

        overrides = OVERRIDES.get(key, {})
        for field, value in overrides.items():
            if value is None:
                wanted.pop(field, None)
            else:
                wanted[field] = value

        if not wanted:
            return match.group(0)

        seen: set[str] = set()

        def rewrite_field(line: re.Match) -> str:
            indent, name, equals, open_b, value, close_b, comma = line.groups()
            lower = name.lower()
            if lower not in wanted:
                return line.group(0)
            seen.add(lower)
            new = wanted[lower]
            if new == DELETE:
                changes.append((key, lower, " ".join(value.split()), "(removed)"))
                return ""
            if " ".join(value.split()) != " ".join(new.split()):
                changes.append((key, lower, " ".join(value.split()), " ".join(new.split())))
            return f"{indent}{name}{equals}{open_b}{new}{close_b}{comma}"

        new_body = FIELD_LINE.sub(rewrite_field, body)
        for field in wanted:
            if field not in seen and wanted[field] and wanted[field] != DELETE:
                changes.append((key, field, "(absent)", wanted[field]))
                new_body = new_body.rstrip().rstrip(",") + f",\n  {field:<7} = {{{wanted[field]}}}"
        return f"{header}{new_body}{closer}"

    rebuilt = ENTRY.sub(rewrite_entry, text)
    # A removed field leaves an empty line inside the entry; BibTeX tolerates
    # it and a human reading the file should not have to.
    rebuilt = re.sub(r"\n[ \t]*\n(?=[ \t]*\w+\s*=)", "\n", rebuilt)

    assert rebuilt.count("@") == text.count("@"), "entry count changed"
    for key in audit:
        assert f"{{{key}," in rebuilt.replace(" ", ""), f"entry {key} lost"

    OUT.write_text(rebuilt)
    by_entry: dict[str, list[tuple[str, str, str]]] = {}
    for key, field, old, new in changes:
        by_entry.setdefault(key, []).append((field, old, new))
    for key in sorted(by_entry):
        print(f"{key}")
        for field, old, new in by_entry[key]:
            print(f"    {field}:")
            print(f"        was: {old[:150]}")
            print(f"        now: {new[:150]}")
    print(f"\n{len(by_entry)} entries rewritten, {len(changes)} fields changed")
    print(f"wrote {OUT.relative_to(REPO)}  (input {BIB.relative_to(REPO)} unchanged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
