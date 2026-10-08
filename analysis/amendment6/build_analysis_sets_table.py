"""The analysis-set table with the three Amendment 6 rows appended.

Reads the registered table of Amendment 5 (analysis/amendment5/analysis_sets/analysis_sets.csv) and the
Amendment 6 results (source_values_results.json), and writes analysis_sets_with_amendment6.csv beside
this script: the twelve Amendment 5 rows unchanged, then the registered rule under source-reported
values, the published-MR-estimate set, and that set without IL-23-psoriasis. The p-values of the
published-MR-estimate set are descriptive; no test is run on the last row.

Run:  uv run --no-project python analysis/amendment6/build_analysis_sets_table.py
"""
import csv
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
A5_TABLE = os.path.join(ROOT, "analysis", "amendment5", "analysis_sets", "analysis_sets.csv")
A6_RESULTS = os.path.join(HERE, "source_values_results.json")
OUT = os.path.join(HERE, "analysis_sets_with_amendment6.csv")


class UnexpectedInput(Exception):
    """The Amendment 5 table or the Amendment 6 results are not the files this script was written for."""


class OutputExists(Exception):
    """The output is already on disk with different bytes; it is not overwritten."""


def main():
    with open(A5_TABLE, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    fields = list(rows[0].keys())
    if len(rows) != 12 or (rows[0]["set"], rows[0]["n"], rows[0]["correct"]) != ("registered", "32", "24"):
        raise UnexpectedInput(os.path.relpath(A5_TABLE, ROOT))
    with open(A6_RESULTS, encoding="utf-8") as handle:
        a6 = json.load(handle)
    p1 = a6["procedure_1_source_reported_values"]
    p2 = a6["procedure_2_published_mr_estimate_set"]
    p3 = a6["descriptive_row_without_il23_psoriasis"]
    if (p1["n"], p2["n"], p3["n"], p3["test"]) != (32, 28, 27, "none"):
        raise UnexpectedInput(os.path.relpath(A6_RESULTS, ROOT))

    replaced = "; ".join(sorted(a6["inputs"]["source_values"]))
    blank = dict.fromkeys(fields, "")
    rows += [
        {**blank, "set": "source-reported values (Amendment 6)",
         "definition": "registered set, each mismatched input with a published figure replaced by that figure",
         "n": p1["n"], "correct": p1["correct"], "accuracy": round(p1["accuracy"], 4), "reclassified": "",
         "added": "", "removed": "", "p_permutation_exact": "", "p_permutation_cluster_level": "", "p_binomial": ""},
        {**blank, "set": "published MR estimate (Amendment 6)",
         "definition": "registered families whose MR input is a published estimate, on source-reported values; "
                       "p-values descriptive, set defined with outcomes known",
         "n": p2["n"], "correct": p2["correct"], "accuracy": round(p2["accuracy"], 4),
         "removed": "; ".join(sorted(p2["removed"])),
         "p_permutation_exact": round(p2["p_permutation_exact_descriptive"], 5),
         "p_permutation_cluster_level": round(p2["p_permutation_cluster_level_descriptive"], 5)},
        {**blank, "set": "published MR estimate, IL-23-psoriasis removed (Amendment 6)",
         "definition": "also removes the family whose observational value has no published figure; no test",
         "n": p3["n"], "correct": p3["correct"], "accuracy": round(p3["accuracy"], 4),
         "removed": "; ".join(sorted(p3["removed"]))},
    ]
    assert [(int(r["n"]), int(r["correct"])) for r in rows[-3:]] == [(32, 24), (28, 21), (27, 20)]
    assert len(replaced.split("; ")) == 9

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    out = buf.getvalue().encode()
    if os.path.exists(OUT):
        with open(OUT, "rb") as handle:
            if handle.read() != out:
                raise OutputExists(os.path.relpath(OUT, ROOT))
    with open(OUT, "wb") as handle:
        handle.write(out)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(rows)} rows")
    for r in rows[-3:]:
        print(f"  {r['set']:<62} {r['correct']}/{r['n']} = {r['accuracy']}  p {r['p_permutation_exact'] or '-'} / {r['p_permutation_cluster_level'] or '-'}")


if __name__ == "__main__":
    main()
