"""Fetch an open-access PDF for every source the manuscript cites, into the shared citations library.

Run:  uv run --no-project --with pyyaml python analysis/provenance/fetch_source_pdfs.py

For each \\cite key in the manuscript: take its DOI (or PMID) from the .bib, ask OpenAlex for the
best open-access PDF location, then Europe PMC's rendered PDF for a PMC id, and save the file as
$CITATIONS_HOME/pdfs/<record slug>.pdf (the library's own naming; the directory is gitignored there).
A download is kept only if `file` says it is a PDF. Nothing is sent but the identifier: no email,
no API key, no User-Agent override. Writes analysis/provenance/source_pdf_status.csv, one row per key:
have / fetched / paywalled (no OA copy found) / failed, with the URL tried.
"""
import csv
import glob
import json
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LIB = Path(os.environ["CITATIONS_HOME"])
TEX = ROOT / "paper" / "paper_v26b_round4.tex"
BIB = ROOT / "paper" / "references_v10_r4.bib"
PROJECT = "cross-design-evidence-discordance"


def get(url, timeout=40):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def is_pdf(path):
    return "PDF document" in subprocess.run(["file", "-b", str(path)], capture_output=True, text=True).stdout


def slugify_doi(doi):
    return "doi-" + re.sub(r"[^a-z0-9]+", "-", doi.lower()).strip("-")


tex = TEX.read_text(encoding="utf-8")
cited = sorted({k.strip() for grp in re.findall(r"\\cite[tp]?\{([^}]*)\}", tex) for k in grp.split(",")})
bib = BIB.read_text(encoding="utf-8")
entries = {k.strip(): body for k, body in re.findall(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S)}

records_by_key, records_by_doi = {}, {}
for p in LIB.glob("records/*.yaml"):
    try:
        r = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(r, dict):
        continue
    cb = (r.get("cited_by") or {}).get(PROJECT)
    if cb:
        records_by_key[cb.get("key")] = r
    if r.get("doi"):
        records_by_doi[r["doi"].lower()] = r

rows = []
for key in cited:
    body = entries.get(key, "")
    m = re.search(r"\bdoi\s*=\s*\{([^}]*)\}", body, re.I)
    doi = m.group(1).strip() if m else ""
    m = re.search(r"PMID:?\s*(\d+)|\bpmid\s*=\s*\{(\d+)\}", body, re.I)
    pmid = (m.group(1) or m.group(2)) if m else ""
    rec = records_by_key.get(key) or (records_by_doi.get(doi.lower()) if doi else None)
    slug = rec["slug"] if rec else (slugify_doi(doi) if doi else f"key-{key}")
    have = [f for f in glob.glob(str(LIB / "pdfs" / f"{slug}.*")) if f.endswith(".pdf") and is_pdf(f)]
    row = {"key": key, "slug": slug, "doi": doi, "pmid": pmid, "has_record": bool(rec), "status": "", "url_tried": "", "path": ""}
    if have:
        row.update(status="have", path=have[0]); rows.append(row); continue
    ident = f"doi:{doi}" if doi else (f"pmid:{pmid}" if pmid else "")
    urls = []
    if ident:
        try:
            w = json.loads(get("https://api.openalex.org/works/" + urllib.parse.quote(ident, safe=":/")))
            for loc in [w.get("best_oa_location")] + (w.get("oa_locations") or []):
                if loc and loc.get("pdf_url"):
                    urls.append(loc["pdf_url"])
            pmcid = (w.get("ids") or {}).get("pmcid", "")
            if pmcid:
                pmc = pmcid.rstrip("/").split("/")[-1]
                urls.append(f"https://europepmc.org/articles/{pmc}?pdf=render")
        except Exception as e:
            row["url_tried"] = f"openalex error {e.__class__.__name__}"
        time.sleep(0.3)
    dest = LIB / "pdfs" / f"{slug}.pdf"
    for u in dict.fromkeys(urls):
        try:
            data = get(u, timeout=60)
            dest.write_bytes(data)
            if is_pdf(dest):
                row.update(status="fetched", url_tried=u, path=str(dest)); break
            dest.unlink()
        except Exception:
            if dest.exists():
                dest.unlink()
        row["url_tried"] = u
        time.sleep(0.5)
    if not row["status"]:
        row["status"] = "paywalled" if not urls else "failed"
    rows.append(row)
    print(f"{row['status']:<10} {key}", flush=True)

with open(HERE / "source_pdf_status.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
from collections import Counter
print(dict(Counter(r["status"] for r in rows)), "->", (HERE / "source_pdf_status.csv").relative_to(ROOT))
