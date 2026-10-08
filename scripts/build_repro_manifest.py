"""Write repro.yaml: each headline number of the manuscript, addressed in the results file that holds it.

Run:  uv run --no-project --with pyyaml==6.0.2 python scripts/build_repro_manifest.py
Then: repro verify

Every claim carries one metric assertion: the value the manuscript prints, and the JSON pointer of
the stored value in a pinned results file. The manuscript source is not in this repository, so the
manifest pins the results files and not the text; reviews/verification/verify_v27_numbers.py checks
the printed sentences against the same files.

The pinned files are the ones the repository stores byte for byte or with LF endings, so the digests
hold in a fresh clone.
"""
import hashlib
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "repro.yaml")

ARTIFACTS = {
    "registered": "analysis/revised_primary_analysis/revised_primary_results.json",
    "analysis-sets": "analysis/amendment5/analysis_sets/analysis_sets.json",
    "amendment6": "analysis/amendment6/source_values_results.json",
}
A6 = "Amendment 6 (commit 3aacce6), registered before it was run, with outcomes known"
A5 = "Amendment 5 (commit fbc7d33), registered analysis-set table"
P1 = "/procedure_1_source_reported_values"
P2 = "/procedure_2_published_mr_estimate_set"
P3 = "/descriptive_row_without_il23_psoriasis"

# id, where, sentence, artifact, pointer, value the manuscript prints, registration, note
CLAIMS = [
    ("registered-correct", "Abstract; Results", "Under the registered analysis, 24/32 families were classified correctly", "registered", "/registered/correct", "24", "confirmatory", "PREREGISTRATION.md, frozen two-criterion rule"),
    ("registered-n", "Abstract; Results", "32 scored families", "registered", "/registered/n", "32", "confirmatory", "PREREGISTRATION.md"),
    ("registered-accuracy", "Abstract; Results", "75.0%", "registered", "/registered/accuracy", "0.75", "confirmatory", "PREREGISTRATION.md"),
    ("registered-p-permutation", "Abstract; Results", "outcome-permutation p = 0.005 at family level", "registered", "/registered/p_permutation_exact", "0.00544", "exploratory", "permutation test specified in Amendment 4, after the registered binomial test"),
    ("registered-p-cluster", "Abstract; Results", "p = 0.005 at instrument-cluster level", "registered", "/registered/p_permutation_cluster_level", "0.00498", "exploratory", "Amendment 4"),
    ("registered-p-binomial", "Results; analysis-set table", "one-sided exact binomial p = 0.004", "registered", "/registered/p_one_sided_exact_binomial_50pct", "0.0035", "confirmatory", "the registered test"),
    ("original-domains", "Abstract", "18/22 in the original domains", "registered", "/by_tier/registered/pre-registered/correct", "18", "confirmatory", "PREREGISTRATION.md"),
    ("blind-extension", "Abstract", "6/10 in the blind extension", "registered", "/by_tier/registered/extension/correct", "6", "confirmatory", "Amendments 1 and 2"),
    ("sensitivity-28", "analysis-set table", "28-family sensitivity set: 23 of 28", "registered", "/reviewer_specified/correct", "23", "exploratory", "Amendment 4, specified with outcomes known"),
    ("strict-phase-iii", "analysis-set table", "Strict Phase III: 17 of 25", "analysis-sets", "/table/1/correct", "17", "exploratory", A5),
    ("amyloid-scored", "analysis-set table", "Amyloid-AD scored: 24 of 33", "analysis-sets", "/table/2/correct", "24", "exploratory", A5),
    ("mr-instrumented", "analysis-set table", "MR-instrumented: 22 of 27", "analysis-sets", "/table/4/correct", "22", "exploratory", A5),
    ("unique-evidence", "analysis-set table", "Unique evidence: 23 of 31", "analysis-sets", "/table/7/correct", "23", "exploratory", A5),
    ("documented-program", "Results; analysis-set table", "Documented Phase III program: 20 of 28", "analysis-sets", "/table/10/correct", "20", "exploratory", "set defined after the registered sets were scored"),
    ("source-values-correct", "Abstract; Results; analysis-set table", "With each of the nine replaced by the source's figure, the registered rule classifies 24/32 correctly", "amendment6", P1 + "/correct", "24", "exploratory", A6),
    ("source-values-n", "Results", "24/32", "amendment6", P1 + "/n", "32", "exploratory", A6),
    ("source-values-obs", "Results", "31 of 32 families keep non-trivial observational support", "amendment6", P1 + "/obs_non_trivial", "31", "exploratory", A6),
    ("published-mr-correct", "Abstract; Results; analysis-set table", "the rule classifies 21/28 correctly", "amendment6", P2 + "/correct", "21", "exploratory", A6),
    ("published-mr-n", "Abstract; Results", "21/28", "amendment6", P2 + "/n", "28", "exploratory", A6),
    ("published-mr-accuracy", "Abstract; Results", "75.0%", "amendment6", P2 + "/accuracy", "0.75", "exploratory", A6),
    ("published-mr-p", "Abstract; Results", "descriptive permutation p = 0.011", "amendment6", P2 + "/p_permutation_exact_descriptive", "0.01065", "exploratory", A6),
    ("published-mr-p-cluster", "Results; analysis-set table", "cluster-level p = 0.008", "amendment6", P2 + "/p_permutation_cluster_level_descriptive", "0.00773", "exploratory", A6),
    ("published-mr-clusters", "Results", "over 25 clusters", "amendment6", P2 + "/n_instrument_clusters", "25", "exploratory", A6),
    ("published-mr-original", "Results", "15/18 in the original domains", "amendment6", P2 + "/by_tier/original domains/correct", "15", "exploratory", A6),
    ("published-mr-extension", "Results", "6/10 in the blind extension", "amendment6", P2 + "/by_tier/blind extension/correct", "6", "exploratory", A6),
    ("published-mr-obs", "Results", "27 of 28 families carrying non-trivial observational support", "amendment6", P2 + "/obs_non_trivial", "27", "exploratory", A6),
    ("without-il23-correct", "analysis-set table", "Published MR estimate, IL-23-psoriasis removed: 20 of 27", "amendment6", P3 + "/correct", "20", "exploratory", A6),
    ("without-il23-n", "analysis-set table", "27 scored", "amendment6", P3 + "/n", "27", "exploratory", A6),
]


def sha256(path):
    with open(os.path.join(ROOT, path), "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main():
    manifest = {
        "schema_version": "repro/1",
        "project": "cross-design evidence and Phase III drug outcomes",
        "provenance": {"generated_by": "scripts/build_repro_manifest.py"},
        "artifacts": [
            {"id": key, "path": path, "media_type": "application/json", "digest": {"algorithm": "sha256", "value": sha256(path)}}
            for key, path in ARTIFACTS.items()
        ],
        "claims": [
            {"id": cid, "registration": registration, "registration_note": note, "where": where, "text": text,
             "evidence": [{"kind": "metric", "artifact": artifact, "name": cid, "reported": reported, "pointer": pointer}]}
            for cid, where, text, artifact, pointer, reported, registration, note in CLAIMS
        ],
    }
    with open(OUT, "w", encoding="utf-8") as handle:
        yaml.safe_dump(manifest, handle, sort_keys=False, allow_unicode=True, width=1000)
    print(f"wrote repro.yaml: {len(ARTIFACTS)} artifacts, {len(CLAIMS)} claims")


if __name__ == "__main__":
    main()
