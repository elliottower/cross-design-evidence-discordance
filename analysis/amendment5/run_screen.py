"""Amendment 5, Procedure 1: candidate-family screen against the Minikel 2024 universe.

Registered at commit fbc7d33 (PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md).

Universe: every row of table_s01.tsv with combined_max_phase in {Phase III, Launched}
and target_status = "genetically supported target" (expected 279); resolved universe =
rows with succ_3_a TRUE or FALSE (expected 219); blank succ_3_a = Phase III outcome pending.

Mapping: a scored family covers a universe row when GENE_TARGET_MAP[family]["gene"] equals
the row's `target` and MINIKEL_INDICATION_MAP[indication] equals the row's
`indication_mesh_term`. Both maps are read from paper/reference/reviewer_analyses.py as
frozen (commit 4b0a652); this script parses the dict literals and does not import the module.

Match status per family:
  exact                 (gene, mesh term) is a universe row
  broader indication    gene is in the universe under a different indication only
  polygenic             GENE_TARGET_MAP gene == "multiple"; cannot map
  no record             gene absent from the universe
Exact coverage counts a universe row covered under `exact` only; expanded coverage also
counts the rows a `broader indication` family reaches (all universe rows for that gene).
Families whose mapped gene is a biomarker or pathway proxy rather than the drug's target
(GENE_TARGET_MAP notes / instrument_type biomarker_gwas) are flagged `pathway_proxy` in a
separate column; the flag does not change the coverage arithmetic.

Outputs (analysis/amendment5/screen/):
  screen_results.json          all counts, the universe definition, the seed
  family_match_status.csv      one row per scored family
  uncovered_universe_rows.csv  the resolved universe rows no scored family covers
  mr_availability_sample.csv   25 uncovered resolved rows, seed 20260922, for the PubMed check

Run:  uv run --no-project python analysis/amendment5/run_screen.py
"""
import ast
import csv
import json
import os
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MINIKEL = os.path.join(ROOT, "paper", "reference", "minikel_data", "table_s01.tsv")
MAPS_SRC = os.path.join(ROOT, "paper", "reference", "reviewer_analyses.py")
FAMILIES = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v3.csv")
OUT = os.path.join(HERE, "screen")
SEED = 20260922
N_SAMPLE = 25


def dict_literal(source: str, name: str) -> dict:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


src = open(MAPS_SRC, encoding="utf-8").read()
GENE_TARGET_MAP = dict_literal(src, "GENE_TARGET_MAP")
MINIKEL_INDICATION_MAP = dict_literal(src, "MINIKEL_INDICATION_MAP")

rows = list(csv.DictReader(open(MINIKEL, encoding="utf-8"), delimiter="\t"))
assert len({r["ti_uid"] for r in rows}) == len(rows)
universe = [r for r in rows if r["combined_max_phase"] in ("Phase III", "Launched")
            and r["target_status"] == "genetically supported target"]
assert len(universe) == 279, len(universe)
resolved = [r for r in universe if r["succ_3_a"] in ("TRUE", "FALSE")]
assert len(resolved) == 219, len(resolved)
by_key = {(r["target"], r["indication_mesh_term"]): r for r in universe}
genes_in_universe = {r["target"] for r in universe}

families = list(csv.DictReader(open(FAMILIES, encoding="utf-8")))
scored = [f for f in families if f["correct"] in ("True", "False")]
assert len(scored) == 32, len(scored)

status_rows = []
covered_exact = set()      # ti_uid
covered_expanded = set()
for f in scored:
    info = GENE_TARGET_MAP[f["family"]]
    gene, indication = info["gene"], info["indication"]
    mesh = MINIKEL_INDICATION_MAP[indication]
    proxy = info["instrument_type"] == "biomarker_gwas" or "notes" in info
    if gene == "multiple":
        status = "polygenic"
        hit_uids = []
    elif (gene, mesh) in by_key:
        status = "exact"
        hit_uids = [by_key[(gene, mesh)]["ti_uid"]]
        covered_exact.add(hit_uids[0])
    elif gene in genes_in_universe:
        status = "broader indication"
        hit_uids = [r["ti_uid"] for r in universe if r["target"] == gene]
    else:
        status = "no record"
        hit_uids = []
    covered_expanded.update(hit_uids)
    status_rows.append({
        "family": f["family"], "gene": gene, "indication": indication, "minikel_mesh_term": mesh,
        "match_status": status, "pathway_proxy": "yes" if proxy else "no",
        "universe_rows_reached": len(hit_uids),
        "minikel_indications_for_gene": "; ".join(sorted({r["indication_mesh_term"] for r in universe if r["target"] == gene})),
        "registered_correct": f["correct"],
    })

resolved_uids = {r["ti_uid"] for r in resolved}
exact_resolved = covered_exact & resolved_uids
expanded_resolved = covered_expanded & resolved_uids
uncovered = [r for r in resolved if r["ti_uid"] not in covered_expanded]
uncovered_exact_def = [r for r in resolved if r["ti_uid"] not in covered_exact]

rng = random.Random(SEED)
sample = rng.sample(sorted(uncovered_exact_def, key=lambda r: r["ti_uid"]), N_SAMPLE)

results = {
    "registration": "PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md, commit fbc7d33",
    "universe_definition": "combined_max_phase in {Phase III, Launched} and target_status == 'genetically supported target'",
    "universe_n": len(universe),
    "universe_outcome_split": dict(Counter(r["succ_3_a"] or "pending" for r in universe)),
    "resolved_universe_n": len(resolved),
    "resolved_outcome_split": dict(Counter(r["succ_3_a"] for r in resolved)),
    "scored_families_n": len(scored),
    "families_by_match_status": dict(Counter(s["match_status"] for s in status_rows)),
    "families_pathway_proxy": sorted(s["family"] for s in status_rows if s["pathway_proxy"] == "yes"),
    "exact_coverage": {"resolved_rows_covered": len(exact_resolved), "of": len(resolved),
                        "fraction": round(len(exact_resolved) / len(resolved), 4),
                        "universe_rows_covered_incl_pending": len(covered_exact)},
    "expanded_coverage": {"resolved_rows_covered": len(expanded_resolved), "of": len(resolved),
                           "fraction": round(len(expanded_resolved) / len(resolved), 4),
                           "universe_rows_covered_incl_pending": len(covered_expanded)},
    "uncovered_resolved_rows_exact_definition": len(uncovered_exact_def),
    "uncovered_resolved_rows_expanded_definition": len(uncovered),
    "mr_availability_sample": {"n": N_SAMPLE, "seed": SEED,
                                "drawn_from": "resolved rows not covered under the exact definition, sorted by ti_uid"},
    "maps_source": "paper/reference/reviewer_analyses.py (GENE_TARGET_MAP, MINIKEL_INDICATION_MAP), frozen at 4b0a652",
    "minikel_file": os.path.relpath(MINIKEL, ROOT),
}

os.makedirs(OUT, exist_ok=True)
json.dump(results, open(os.path.join(OUT, "screen_results.json"), "w"), indent=2)
with open(os.path.join(OUT, "family_match_status.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(status_rows[0].keys())); w.writeheader(); w.writerows(status_rows)
unc_fields = ["ti_uid", "target", "indication_mesh_term", "combined_max_phase", "succ_3_a", "year_launch", "areas", "assoc_source"]
with open(os.path.join(OUT, "uncovered_universe_rows.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=unc_fields, extrasaction="ignore"); w.writeheader(); w.writerows(uncovered_exact_def)
with open(os.path.join(OUT, "mr_availability_sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=unc_fields + ["pubmed_query", "n_results_read", "mr_eligible", "evidence_pmid", "note"], extrasaction="ignore")
    w.writeheader()
    for r in sample:
        q = (f'"{r["target"]}"[All Fields] AND "mendelian randomization"[All Fields] AND '
             f'("{r["indication_mesh_term"]}"[MeSH Terms] OR "{r["indication_mesh_term"]}"[All Fields])')
        w.writerow({**r, "pubmed_query": q, "n_results_read": "", "mr_eligible": "", "evidence_pmid": "", "note": ""})

print(json.dumps({k: results[k] for k in ("universe_n", "resolved_universe_n", "resolved_outcome_split",
                                          "families_by_match_status", "exact_coverage", "expanded_coverage")}, indent=2))
for s in status_rows:
    print(f"{s['family']:<22} {s['gene']:<8} {s['match_status']:<19} proxy={s['pathway_proxy']:<3} reached={s['universe_rows_reached']}")
print("wrote", OUT)
