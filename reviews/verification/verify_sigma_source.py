"""Check what interleukin2012 reports for the IL-6R per-allele shift in soluble IL-6R.

Run:  uv run python reviews/verification/verify_sigma_source.py [paper.tex]

The manuscript rescales the IL-6R per-allele MR odds ratio to a per-SD contrast
using sigma, the per-allele shift in the exposure in SD units. The preregistration
fixes sigma = 0.34 and attributes it to "Swerdlow et al. 2012 Int J Epidemiol".
No such paper exists. The bibliography entry the manuscript cites is the Lancet
paper, 379(9822):1214-1224, doi 10.1016/S0140-6736(12)60110-X.

This resolves that DOI through NCBI, pulls the open-access full text from Europe
PMC, and prints every figure the source gives for the soluble IL-6R contrast. It
does not argue from a term count: the summary-effects table row and the Figure 2
legend -- the two places an SD-unit per-allele figure would appear if the paper
had one -- are extracted and printed whole, so the reader sees the source rather
than a verdict about it.

What the source gives, and why the manuscript hedges it: the table reports 14.87
ng/mL per allele; the Figure 2 legend calls 0.75 a standardised mean difference
and then prints it in ng/mL, a unit that cannot belong to a standardised mean
difference. The source is internally inconsistent here, so the manuscript reports
both figures and the inconsistency rather than presenting 0.75 as sigma.

Writes reviews/verification/output/sigma_source_evidence.json.

Exit 1 if the source no longer gives the figures the manuscript attributes to it,
or if the manuscript states 0.75 without the source's unit label on it.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEX = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    REPO / "paper" / "paper_v21_sigma_units.tex")
OUT = REPO / "reviews" / "verification" / "output" / "sigma_source_evidence.json"

DOI = "10.1016/S0140-6736(12)60110-X"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"

# The Lancet sets decimal points as middle dots, so a plain "0.34" search against
# its full text finds nothing and shows nothing. Both conventions are counted.
FORMS = ("0.34", "0·34")


def get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(xml: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", xml))


def main() -> int:
    hit = re.search(r"<Id>(\d+)</Id>", get(
        f"{EUTILS}/esearch.fcgi?db=pubmed&term={urllib.parse.quote(DOI)}[doi]"))
    if not hit:
        print(f"ABORT -- {DOI} does not resolve to a PMID", file=sys.stderr)
        return 1
    pmid = hit.group(1)

    # elink returns one LinkSetDb per link type, and the citedby sets run to
    # hundreds of ids. Take the block named pubmed_pmc; the first <Id> in the
    # whole response is the query pmid echoed back, not a PMC id.
    link = get(f"{EUTILS}/elink.fcgi?dbfrom=pubmed&db=pmc&id={pmid}")
    block = re.search(
        r"<LinkName>pubmed_pmc</LinkName>(.*?)</LinkSetDb>", link, re.S)
    hit = re.search(r"<Id>(\d+)</Id>", block.group(1)) if block else None
    if not hit:
        print(f"ABORT -- PMID {pmid} has no pubmed_pmc link to read", file=sys.stderr)
        return 1
    pmcid = f"PMC{hit.group(1)}"

    text = strip_tags(get(f"{EPMC}/{pmcid}/fullTextXML"))
    print(f"{DOI}\n  PMID {pmid}\n  {pmcid}\n  {len(text.split())} words of full text\n")

    row = re.search(r"Soluble IL6R \(ng/mL\).{0,120}", text)
    legend = re.search(r"Estimates for soluble interleukin-6 receptor.{0,320}", text)

    evidence = {
        "doi": DOI, "pmid": pmid, "pmcid": pmcid,
        "occurrences_of_0_34": {f: text.count(f) for f in FORMS},
        "summary_table_row": row.group(0) if row else None,
        "figure_2_legend": legend.group(0) if legend else None,
    }

    print("Occurrences of 0.34, in both decimal conventions")
    for form, n in evidence["occurrences_of_0_34"].items():
        print(f"  {form!r}: {n}")
    print("\nSummary-effects table, soluble IL6R row")
    print(f"  {row.group(0) if row else '(row not found)'}")
    print("\nFigure 2 legend, the soluble IL-6R sentence")
    print(f"  {legend.group(0) if legend else '(legend not found)'}")

    failures = []
    if row is None or "14·87 (13·07 to 16·66)" not in row.group(0):
        failures.append("the table no longer gives 14.87 (13.07 to 16.66) ng/mL per allele")
    if legend is None or "0·75 (95% CI 0·59–0·91) ng/mL" not in legend.group(0):
        failures.append("the legend no longer gives 0.75 (0.59-0.91) with a ng/mL label")

    tex = TEX.read_text()
    for figure in ("14.87~ng/mL (13.07--16.66)", "0.75 (0.59--0.91)", "$d = 0.038$"):
        if figure not in tex:
            failures.append(f"{TEX.name} does not state {figure!r}")
    # The source prints a unit on 0.75 that cannot belong to a standardized
    # quantity. A manuscript that repeats 0.75 as sigma without that caveat
    # states as settled something its own source leaves inconsistent.
    if "0.75 (0.59--0.91)" in tex and "ng/mL" not in tex.split("0.75 (0.59--0.91)")[1][:400]:
        failures.append(f"{TEX.name} reports 0.75 without the source's unit label")
    stale = "shifts soluble IL-6R by $\\sigma = 0.34$~SD per allele \\cite{interleukin2012}"
    if stale in tex:
        failures.append(f"{TEX.name} still attributes sigma to the cited source")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {OUT.relative_to(REPO)}")

    if failures:
        print("\nFAILED:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1
    print("\nThe manuscript states the figures this source gives, with the unit "
          "inconsistency the source carries, and attributes sigma to the "
          "preregistration rather than to it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
