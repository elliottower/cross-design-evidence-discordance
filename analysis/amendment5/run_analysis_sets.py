"""Amendment 5, Procedure 4: the analysis-set table.

Registered at commit fbc7d33 (PREREGISTRATION_AMENDMENT_5_SCREEN_MR_STATES_OUTCOME_CODING.md).
Nine sets, each defined by a rule; number scored and number correct for each; p-values only for
the two sets already tested (registered, Amendment 4), copied from
analysis/revised_primary_analysis/revised_primary_results.json. No test is run on any other set.

Inputs written by the other Procedure scripts and the literature agents (all must exist):
  data/cross_design_classification_all_41_families_v3.csv          registered rows
  analysis/classifier/classify_families.py                          obs_sourcing (author-estimated flag), parsed as literals
  analysis/amendment5/codebook/codebook_*.csv                       Procedure 3 trial_phase per family
  analysis/amendment5/mr_instrumented_audit.csv                     verdict per scored family
  analysis/amendment5/il6_mdd/selected_estimate.json                registration-consistent IL6-MDD estimate
Amyloid-AD row inputs: OBS amyloid-PET positivity -> AD conversion HR 3.74 (1.21-11.58), PMID 29625056;
GEN APOE4 heterozygous OR 3.46 (3.27-3.65), Belloy 2023 JAMA Neurol 80(12):1284, PMID 37930705 (the catalog row cites PMID 36622685, which is a different paper; data/effect_sizes_v12.csv,
rows AD-001 and AD-002a); drug outcome Failed on 12 of 14 programs (manuscript, Amyloid subanalysis).

Outputs: analysis/amendment5/analysis_sets/analysis_sets.json and analysis_sets.csv
Run:  uv run --no-project python analysis/amendment5/run_analysis_sets.py
"""
import ast
import csv
import glob
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FAMILIES_CSV = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v3.csv")
CLASSIFIER = os.path.join(ROOT, "analysis", "classifier", "classify_families.py")
PRIOR = os.path.join(ROOT, "analysis", "revised_primary_analysis", "revised_primary_results.json")
CODEBOOK = sorted(glob.glob(os.path.join(HERE, "codebook", "codebook_*.csv")))
AUDIT = os.path.join(HERE, "mr_instrumented_audit.csv")
IL6 = os.path.join(HERE, "il6_mdd", "selected_estimate.json")
OUT = os.path.join(HERE, "analysis_sets")
K = math.sqrt(3) / math.pi
THRESHOLD = 0.10

AMYLOID = {"family": "Amyloid-AD", "obs_or": 3.74, "obs_source": "PMID:29625056",
           "gen_or": 3.46, "gen_ci": (3.27, 3.65), "gen_source": "PMID:37930705 (Belloy 2023 JAMA Neurol; catalog PMID 36622685 is wrong)",
           "drug_outcome": "Failed", "outcome_note": "12 of 14 amyloid-targeting Phase III programs failed"}
UNIQUE_FIELDS = ("obs_d", "mr_or_raw", "mr_ci", "instrument_set", "drug_outcome")


def is_failure(outcome):
    return outcome in ("Failed", "No benefit")


def correct(row):
    return (row["prediction"] == "failure") == is_failure(row["drug_outcome"])


def classify(obs_d, gen_or, ci):
    obs = "non-trivial" if obs_d >= THRESHOLD else "trivial"
    d = abs(math.log(gen_or)) * K
    supportive = ci is not None and not (ci[0] <= 1.0 <= ci[1]) and d >= THRESHOLD
    if obs == "non-trivial":
        return ("qualitative discordance", "failure") if not supportive else ("concordance", "success")
    return ("null concordance", "ambiguous") if not supportive else ("genetic-only signal", "success")


def literal_list(source, name):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


rows = list(csv.DictReader(open(FAMILIES_CSV, encoding="utf-8")))
scored = [dict(r) for r in rows if r["correct"] in ("True", "False")]
assert len(scored) == 32
for r in scored:
    assert (r["correct"] == "True") == correct(r), r["family"]

src = open(CLASSIFIER, encoding="utf-8").read()
fams = sum((literal_list(src, n) for n in ("NEURO_FAMILIES", "CARDIO_FAMILIES", "AUTOIMMUNE_FAMILIES", "EXTENSION_FAMILIES")), [])
# Amendment 5 names seven scored families as author-estimated (the manuscript's dagger marks). The frozen
# classifier flags five of them `author_estimated`; IL6-MDD (Howren 2009, d = 0.15) and Serotonin-MDD
# (Ogawa 2014, g = 0.45) carry `meta_analysis` there. Both readings are reported; neither is promoted.
REGISTERED_AUTHOR_ESTIMATED = {"CTLA-4-RA", "JAK-STAT-RA", "CD20-RA", "Eos/IL5-Asthma", "Complement-GA", "Serotonin-MDD", "IL6-MDD"}
classifier_author_estimated = {f["family"] for f in fams if f.get("obs_sourcing") == "author_estimated"}
assert classifier_author_estimated == {"CTLA-4-RA", "JAK-STAT-RA", "CD20-RA", "Eos/IL5-Asthma", "Complement-GA"}, classifier_author_estimated
author_estimated = REGISTERED_AUTHOR_ESTIMATED

phase = {}
for path in CODEBOOK:
    for r in csv.DictReader(open(path, encoding="utf-8")):
        phase[r["family"]] = r["trial_phase"].strip()
missing = [r["family"] for r in scored if r["family"] not in phase]
assert not missing, f"codebook missing trial_phase for {missing}"

audit = {r["family"]: r["verdict"].strip() for r in csv.DictReader(open(AUDIT, encoding="utf-8"))}
missing = [r["family"] for r in scored if r["family"] not in audit]
assert not missing, f"audit missing verdict for {missing}"

il6 = json.load(open(IL6, encoding="utf-8"))
il6_row = next(r for r in scored if r["family"] == "IL6-MDD")
il6_class, il6_pred = classify(float(il6_row["obs_d"]), float(il6["or"]), (float(il6["ci_low"]), float(il6["ci_high"])))

amy_obs_d = abs(math.log(AMYLOID["obs_or"])) * K
amy_class, amy_pred = classify(amy_obs_d, AMYLOID["gen_or"], AMYLOID["gen_ci"])
amyloid_row = {"family": "Amyloid-AD", "prediction": amy_pred, "drug_outcome": AMYLOID["drug_outcome"],
               "classification": amy_class, "status": "added under Procedure 4"}


def by_name(names):
    return [r for r in scored if r["family"] in names]


def without(names):
    return [r for r in scored if r["family"] not in names]


phase_ok = {f for f, p in phase.items() if p in ("III", "post-marketing")}
strict = [r for r in scored if r["family"] in phase_ok]
# The rule removes families whose genetic leg is a variant-disease association. Families the audit could not
# resolve are neither shown to be associations nor confirmed as IV estimates; they stay in the row and are listed.
mr_instr = [r for r in scored if audit[r["family"]] != "association"]
mr_instr_strict = [r for r in scored if audit[r["family"]] == "MR-instrumented"]
seen, unique = set(), []
for r in scored:
    key = tuple(r[k] for k in UNIQUE_FIELDS)
    if key in seen:
        continue
    seen.add(key); unique.append(r)
reg_instrument = [dict(r, prediction=il6_pred, classification=il6_class) if r["family"] == "IL6-MDD" else r for r in scored]
amend4 = [r for r in scored if r["revised_primary_set"] == "True"]
assert len(amend4) == 28

prior = json.load(open(PRIOR, encoding="utf-8"))
sets = [
    ("registered", scored, "the 32 scored families, as registered",
     {"p_permutation_exact": prior["registered"]["p_permutation_exact"],
      "p_permutation_cluster_level": prior["registered"]["p_permutation_cluster_level"],
      "p_binomial": prior["registered"]["p_one_sided_exact_binomial_50pct"]}),
    ("strict Phase III", strict, "registered families whose Procedure 3 trial_phase is III or post-marketing", None),
    ("Amyloid-AD scored", scored + [amyloid_row], "registered set plus Amyloid-AD classified under the registered rule", None),
    ("strict Phase III + Amyloid-AD", strict + [amyloid_row], "both changes", None),
    ("MR-instrumented", mr_instr, "registered set without the families whose genetic leg the audit finds to be a variant-disease association", None),
    ("MR-instrumented (unresolved also removed)", mr_instr_strict, "registered families the audit confirms as instrumental-variable estimates with a CI", None),
    ("registration-consistent instrument", reg_instrument, "registered set with IL6-MDD classified on the estimate the selection rule returns", None),
    ("unique-evidence", unique, "families identical on obs_d, mr_or_raw, mr_ci, instrument_set, drug_outcome counted once", None),
    ("source-extracted OBS", without(REGISTERED_AUTHOR_ESTIMATED), "registered set without the seven families Amendment 5 names as author-estimated", None),
    ("source-extracted OBS (classifier flags)", without(classifier_author_estimated), "registered set without the five families the frozen classifier flags author_estimated", None),
    ("documented Phase III program", [r for r in scored if phase.get(r["family"]) != "not reported"],
     "registered families whose outcome traces to a documented drug program (Procedure 3 trial_phase not 'not reported')", None),
    ("Amendment 4", amend4, "the set Amendment 4 defines",
     {"p_permutation_exact": prior["reviewer_specified"]["p_permutation_exact"],
      "p_permutation_cluster_level": prior["reviewer_specified"]["p_permutation_cluster_level"],
      "p_binomial": prior["reviewer_specified"]["p_one_sided_exact_binomial_50pct"]}),
]

registered_names = {r["family"] for r in scored}
table = []
for name, members, definition, tests in sets:
    names = [m["family"] for m in members]
    k = sum(correct(m) for m in members)
    removed = sorted(registered_names - set(names))
    added = [n for n in names if n not in registered_names]
    changed = [m["family"] for m in members if m["family"] in registered_names
               and m["prediction"] != next(r["prediction"] for r in scored if r["family"] == m["family"])]
    table.append({"set": name, "definition": definition, "n": len(members), "correct": k,
                  "accuracy": round(k / len(members), 4), "removed": "; ".join(removed), "added": "; ".join(added),
                  "reclassified": "; ".join(changed), **(tests or {})})

results = {
    "registration": "Amendment 5, commit fbc7d33",
    "table": table,
    "inputs": {
        "trial_phase_by_family": phase, "families_removed_by_strict_phase_III": sorted(registered_names - phase_ok),
        "mr_instrumented_verdicts": audit,
        "association_families_removed": sorted(f for f, v in audit.items() if v == "association"),
        "audit_unresolved_families": sorted(f for f, v in audit.items() if v not in ("association", "MR-instrumented")),
        "il6_mdd_registration_consistent": {**il6, "classification": il6_class, "prediction": il6_pred,
                                             "registered_classification": il6_row["classification"]},
        "amyloid_ad": {**AMYLOID, "obs_d": round(amy_obs_d, 3), "gen_d": round(abs(math.log(AMYLOID["gen_or"])) * K, 3),
                        "classification": amy_class, "prediction": amy_pred, "gen_ci": list(AMYLOID["gen_ci"])},
        "unique_evidence_collapsed": sorted(registered_names - {r["family"] for r in unique}),
        "author_estimated_removed_registered_list": sorted(REGISTERED_AUTHOR_ESTIMATED),
        "author_estimated_removed_classifier_flags": sorted(classifier_author_estimated),
        "obs_sourcing_by_family": {f["family"]: f.get("obs_sourcing", "meta_analysis or published OR") for f in fams},
        "p_values_source": os.path.relpath(PRIOR, ROOT),
    },
}
os.makedirs(OUT, exist_ok=True)
json.dump(results, open(os.path.join(OUT, "analysis_sets.json"), "w"), indent=2)
fields = ["set", "definition", "n", "correct", "accuracy", "removed", "added", "reclassified",
          "p_permutation_exact", "p_permutation_cluster_level", "p_binomial"]
with open(os.path.join(OUT, "analysis_sets.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(table)
for t in table:
    print(f"{t['set']:<36} {t['correct']:>2}/{t['n']:<2} = {t['accuracy']:.3f}   removed: {t['removed'] or '-'}   added: {t['added'] or '-'}   reclassified: {t['reclassified'] or '-'}")
print("wrote", OUT)
