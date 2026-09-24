"""One provenance ledger for every mechanism family: each value, where it came from, every commit
where it changed, and every reading of its coding.

Run:  uv run --no-project python analysis/provenance/build_family_provenance.py

Re-run after any change; the output is regenerated from the repository and its git history, so the
ledger cannot drift from the files. Nothing is typed in by hand except the list of source files.

Sources read
  git history  every committed version of the frozen classifier (paper/reference/classify_families.py,
               later analysis/classifier/classify_families.py): the dict literal for each family and the
               comment block above it (which is where the classifier records its sources)
  git history  every committed version of the family supplement (paper/supplementary_data.csv and
               cross_design_classification_all_41_families*.csv)
  working tree data/cross_design_classification_all_41_families_v3.csv   registered values and verdicts
               data/effect_sizes_v12.csv                                 the evidence catalog rows per family
               analysis/amendment5/mr_instrumented_audit.csv             genetic-leg source readings
               analysis/amendment5/codebook/outcome_codebook_all_41_families.csv  outcome readings
               analysis/amendment5/mr_states/mr_states_all_41.csv        three-state MR reading
               analysis/amendment5/analysis_sets/analysis_sets.json      set membership
               analysis/amendment5/il6_mdd/selected_estimate.json        IL6-MDD registered-instrument estimate

Outputs (analysis/provenance/)
  family_provenance.json          everything, one object per family
  family_provenance.md            the same, readable: one section per family
  family_provenance_summary.csv   one row per family with the flags
"""
import ast
import csv
import io
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip())
A5 = ROOT / "analysis" / "amendment5"
CLASSIFIER_PATHS = ["paper/reference/classify_families.py", "analysis/classifier/classify_families.py"]
SUPPLEMENT_PATHS = ["paper/supplementary_data.csv", "data/cross_design_classification_all_41_families_v2.csv",
                    "data/cross_design_classification_all_41_families_v3.csv",
                    "paper/submission/supplementary/cross_design_classification_all_41_families.csv"]
TRACKED_FIELDS = ["obs_OR", "obs_d_direct", "obs_sourcing", "gen_OR", "gen_CI_lower", "gen_CI_upper",
                  "per_allele", "sd_per_allele", "drug_outcome"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def norm(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def commits_touching(path):
    out = git("log", "--reverse", "--format=%h\t%ad\t%s", "--date=short", "--", path)
    return [dict(zip(("sha", "date", "subject"), line.split("\t", 2))) for line in out.splitlines() if line]


def families_in_source(src):
    """Every dict with a 'family' key inside a top-level list assignment, plus the comment block above it."""
    lines = src.splitlines()
    out = {}
    for node in ast.parse(src).body:
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.List)):
            continue
        for elt in node.value.elts:
            if not isinstance(elt, ast.Dict):
                continue
            try:
                d = ast.literal_eval(elt)
            except ValueError:
                continue
            if "family" not in d:
                continue
            comments, i = [], elt.lineno - 2
            while i >= 0 and lines[i].strip().startswith("#"):
                comments.insert(0, lines[i].strip().lstrip("#").strip())
                i -= 1
            out[d["family"]] = {"values": d, "comment": " ".join(comments)}
    return out


# ---- classifier history -------------------------------------------------------------------------
classifier_versions = []
for path in CLASSIFIER_PATHS:
    for c in commits_touching(path):
        try:
            src = git("show", f"{c['sha']}:{path}")
        except subprocess.CalledProcessError:
            continue
        classifier_versions.append({**c, "path": path, "families": families_in_source(src)})

# ---- supplement history -------------------------------------------------------------------------
supplement_versions = []
for path in SUPPLEMENT_PATHS:
    for c in commits_touching(path):
        try:
            text = git("show", f"{c['sha']}:{path}")
        except subprocess.CalledProcessError:
            continue
        rows = list(csv.DictReader(io.StringIO(text)))
        by_fam = {}
        for r in rows:
            by_fam.setdefault(r.get("family", ""), []).append(r)
        supplement_versions.append({**c, "path": path, "rows": by_fam})

# ---- working-tree readings ----------------------------------------------------------------------
def read_csv(p, key="family"):
    return {r[key]: r for r in csv.DictReader(open(p, encoding="utf-8"))} if p.exists() else {}


registered = read_csv(ROOT / "data" / "cross_design_classification_all_41_families_v3.csv")
audit = read_csv(A5 / "mr_instrumented_audit.csv")
codebook = read_csv(A5 / "codebook" / "outcome_codebook_all_41_families.csv")
mr_states = read_csv(A5 / "mr_states" / "mr_states_all_41.csv")
sets = json.loads((A5 / "analysis_sets" / "analysis_sets.json").read_text()) if (A5 / "analysis_sets" / "analysis_sets.json").exists() else {"table": []}
il6 = json.loads((A5 / "il6_mdd" / "selected_estimate.json").read_text()) if (A5 / "il6_mdd" / "selected_estimate.json").exists() else None
catalog = list(csv.DictReader(open(ROOT / "data" / "effect_sizes_v12.csv", encoding="utf-8")))
catalog_fam_col = next(k for k in catalog[0] if k and catalog[0][k] and "_" in catalog[0][k] and k not in ("claim_id",)) if catalog else None

ledger = {}
for fam, reg in registered.items():
    # value history: record a row each time a tracked field changes
    history, last = [], None
    for v in classifier_versions:
        f = v["families"].get(fam)
        if f is None:
            continue
        snap = {k: f["values"].get(k) for k in TRACKED_FIELDS}
        if snap != last:
            changed = [k for k in TRACKED_FIELDS if last is None or snap.get(k) != last.get(k)]
            history.append({"commit": v["sha"], "date": v["date"], "subject": v["subject"], "file": v["path"],
                            "changed": changed, "values": snap, "source_comment": f["comment"]})
            last = snap
    supp_history, last_s = [], None
    for v in supplement_versions:
        rs = v["rows"].get(fam)
        if not rs:
            continue
        slim = [{k: r.get(k) for k in r if k in ("evidence_type", "study_design", "effect_size_original", "CI_lower", "CI_upper",
                                               "cohen_d", "drug_outcome", "source", "obs_d", "mr_or_raw", "mr_d", "mr_ci", "mr_class",
                                               "classification", "correct", "status")} for r in rs]
        if slim != last_s:
            supp_history.append({"commit": v["sha"], "date": v["date"], "file": v["path"], "rows": slim})
            last_s = slim
    cat_rows = [r for r in catalog if catalog_fam_col and norm(r.get(catalog_fam_col, "")) == norm(fam)]
    in_sets = [t["set"] for t in sets["table"] if fam not in (t.get("removed") or "").split("; ")
               and not (t["set"] == "Amyloid-AD scored" and False)] if reg["correct"] in ("True", "False") else []

    # flags, each derived from the data above
    flags = []
    first = history[0] if history else None
    frozen_supp = next((s for s in supp_history if first and s["commit"] == first["commit"]), None)
    if first and frozen_supp:
        for r in frozen_supp["rows"]:
            orig = r.get("effect_size_original")
            if r.get("evidence_type") == "GEN" and first["values"].get("gen_OR") is not None:
                if not orig:
                    flags.append(f"frozen supplement gives no GEN value ({r.get('source')}); classifier holds gen_OR {first['values']['gen_OR']}")
                elif abs(float(orig) - float(first["values"]["gen_OR"])) > 1e-9:
                    flags.append(f"frozen supplement GEN {orig} != classifier gen_OR {first['values']['gen_OR']}")
    a = audit.get(fam, {})
    if a.get("verdict") == "unresolved":
        flags.append("genetic-leg estimate not traced to any source")
    if a.get("verdict") == "association":
        flags.append("genetic leg is a variant-disease association, not MR")
    cb = codebook.get(fam, {})
    if reg["correct"] in ("True", "False") and cb.get("trial_phase") == "not reported":
        flags.append("scored outcome has no drug program in the record")
    if reg["correct"] in ("True", "False") and cb.get("trial_phase") == "II":
        flags.append("scored on a Phase II readout")
    if cb.get("efficacy_endpoint") == "met" and reg["drug_outcome"] in ("Failed", "No benefit"):
        flags.append("primary endpoint met but registered outcome is failure (regulatory reading)")
    gen_rows = [c for c in cat_rows if (c.get("design") or "").lower() in ("mr", "genetic", "genetic/cohort", "gwas")]
    if gen_rows and reg["mr_or_raw"]:
        match = [c for c in gen_rows if c.get("estimate") and abs(float(c["estimate"]) - float(reg["mr_or_raw"])) < 1e-9]
        if not match:
            flags.append(f"registered MR OR {reg['mr_or_raw']} matches no genetic row in the evidence catalog "
                         f"(catalog has {', '.join(sorted({c['estimate'] for c in gen_rows if c.get('estimate')}))})")
        elif not reg["mr_ci"] and any(c.get("ci_low") for c in match):
            m = next(c for c in match if c.get("ci_low"))
            flags.append(f"catalog row {m['case_id']} carries a CI ({m['ci_low']}-{m['ci_high']}) that the classifier dropped")
    if len({h['values'].get('gen_OR') for h in history}) > 1:
        flags.append("gen_OR changed across committed classifier versions")
    if len({h['values'].get('drug_outcome') for h in history}) > 1:
        flags.append("drug_outcome changed across committed classifier versions")

    ledger[fam] = {
        "family": fam, "domain": reg["domain"], "status": reg["status"],
        "registered": {k: reg[k] for k in ("obs_d", "obs_type", "mr_or_raw", "mr_d", "mr_ci", "mr_class", "classification",
                                           "prediction", "drug_outcome", "correct", "instrument_type", "mr_contrast", "instrument_set")},
        "classifier_history": history,
        "supplement_history": supp_history,
        "catalog_rows": [{k: r[k] for k in r if k} for r in cat_rows],
        "readings": {
            "genetic_leg_audit": a or None,
            "outcome_codebook": cb or None,
            "mr_state": {k: mr_states.get(fam, {}).get(k) for k in ("mr_state", "d_lower_signed", "d_point_signed", "d_upper_signed",
                                                                   "scale_unresolved", "alignment_flag")} if fam in mr_states else None,
            "il6_registered_instrument": il6 if fam == "IL6-MDD" else None,
        },
        "analysis_sets_including": in_sets,
        "flags": flags,
    }

HERE.mkdir(parents=True, exist_ok=True)
head = git("rev-parse", "--short", "HEAD").strip()
dirty = bool(git("status", "--porcelain", "--", "data", "analysis", "paper/reference").strip())
meta = {"built_at_commit": head, "working_tree_dirty": dirty, "classifier_versions": len(classifier_versions),
        "supplement_versions": len(supplement_versions), "families": len(ledger)}
json.dump({"meta": meta, "families": ledger}, open(HERE / "family_provenance.json", "w"), indent=2, default=str)

with open(HERE / "family_provenance_summary.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["family", "domain", "status", "registered_correct", "drug_outcome", "gen_or", "gen_ci", "gen_leg_verdict",
                "gen_leg_source", "outcome_program", "trial_phase", "efficacy_endpoint", "regulatory_outcome",
                "classifier_versions_with_changes", "n_flags", "flags"])
    for f in ledger.values():
        a = f["readings"]["genetic_leg_audit"] or {}
        cb = f["readings"]["outcome_codebook"] or {}
        w.writerow([f["family"], f["domain"], f["status"], f["registered"]["correct"], f["registered"]["drug_outcome"],
                    f["registered"]["mr_or_raw"], f["registered"]["mr_ci"], a.get("verdict", ""), a.get("genetic_leg_source", ""),
                    cb.get("drug_program", ""), cb.get("trial_phase", ""), cb.get("efficacy_endpoint", ""), cb.get("regulatory_outcome", ""),
                    len(f["classifier_history"]), len(f["flags"]), " | ".join(f["flags"])])


def md_cell(x):
    return str(x if x not in (None, "") else "—").replace("|", "/").replace("\n", " ")


out = [f"# Family provenance ledger\n\nBuilt by `analysis/provenance/build_family_provenance.py` at commit `{head}`"
       f"{' (working tree has uncommitted changes)' if dirty else ''}. {meta['classifier_versions']} committed classifier versions and "
       f"{meta['supplement_versions']} committed supplement versions read. Regenerate; do not edit.\n",
       "## Flags\n", "| family | status | correct | flags |", "|---|---|---|---|"]
for f in ledger.values():
    if f["flags"]:
        out.append(f"| {f['family']} | {f['status']} | {f['registered']['correct'] or '—'} | {md_cell('; '.join(f['flags']))} |")
for f in ledger.values():
    r = f["registered"]
    out += [f"\n## {f['family']}\n", f"Domain {f['domain']}; status {f['status']}; registered: OBS d {r['obs_d']}, MR OR {r['mr_or_raw']} "
            f"{r['mr_ci'] or '(no CI)'}, MR d {r['mr_d']} ({r['mr_class']}); {r['classification']} → {r['prediction']}; outcome "
            f"{r['drug_outcome']}; correct {r['correct'] or '—'}.\n"]
    if f["flags"]:
        out.append("**Flags:** " + "; ".join(f["flags"]) + "\n")
    out += ["### Value history (committed classifier)\n", "| commit | date | changed | gen_OR (CI) | obs | outcome | source note in the classifier |",
            "|---|---|---|---|---|---|---|"]
    for h in f["classifier_history"]:
        v = h["values"]
        ci = f"({v['gen_CI_lower']}–{v['gen_CI_upper']})" if v.get("gen_CI_lower") is not None else "(no CI)"
        obs = v.get("obs_OR") if v.get("obs_OR") is not None else f"d {v.get('obs_d_direct')}"
        out.append(f"| `{h['commit']}` | {h['date']} | {md_cell(', '.join(h['changed']))} | {v.get('gen_OR')} {ci} | {obs} | "
                   f"{v.get('drug_outcome')} | {md_cell(h['source_comment'][:400])} |")
    if f["supplement_history"]:
        out += ["\n### Supplement history\n", "| commit | date | file | rows |", "|---|---|---|---|"]
        for s in f["supplement_history"]:
            rows = "; ".join(", ".join(f"{k}={v}" for k, v in row.items() if v) for row in s["rows"])
            out.append(f"| `{s['commit']}` | {s['date']} | {s['file']} | {md_cell(rows[:600])} |")
    if f["catalog_rows"]:
        out += ["\n### Evidence catalog rows (data/effect_sizes_v12.csv)\n"]
        for c in f["catalog_rows"]:
            vals = list(c.values())
            out.append("- " + md_cell(", ".join(str(x) for x in vals[:14] if x)))
    rd = f["readings"]
    out.append("\n### Readings\n")
    if rd["genetic_leg_audit"]:
        a = rd["genetic_leg_audit"]
        out.append(f"- **Genetic leg:** {a.get('verdict')} — {md_cell(a.get('genetic_leg_source'))}. {md_cell(a.get('design_as_stated'))} "
                   f"Note: {md_cell(a.get('note'))}")
    if rd["outcome_codebook"]:
        c = rd["outcome_codebook"]
        out.append(f"- **Outcome codebook:** program {md_cell(c.get('drug_program'))}; phase {c.get('trial_phase')}; engagement "
                   f"{c.get('target_engagement')}; efficacy {c.get('efficacy_endpoint')}; safety {c.get('safety_outcome')}; decision "
                   f"{c.get('development_decision')}; regulatory {c.get('regulatory_outcome')} {md_cell(c.get('regulatory_jurisdiction_year'))}; "
                   f"attribution {c.get('outcome_attribution')}. Sources: {md_cell(c.get('source_ids'))}. Notes: {md_cell(c.get('notes'))}")
    if rd["mr_state"]:
        m = rd["mr_state"]
        out.append(f"- **MR state:** {m['mr_state']} (signed d {m['d_lower_signed']} / {m['d_point_signed']} / {m['d_upper_signed']}; "
                   f"scale-unresolved {m['scale_unresolved']}; alignment {m['alignment_flag']})")
    if rd["il6_registered_instrument"]:
        i = rd["il6_registered_instrument"]
        out.append(f"- **Registered instrument estimate:** PMID {i.get('pmid')}, OR {i.get('or')} ({i.get('ci_low')}–{i.get('ci_high')})")
    if f["analysis_sets_including"]:
        out.append(f"- **In analysis sets:** {', '.join(f['analysis_sets_including'])}")
(HERE / "family_provenance.md").write_text("\n".join(out) + "\n", encoding="utf-8")

n_flag = sum(1 for f in ledger.values() if f["flags"])
print(f"{len(ledger)} families; {meta['classifier_versions']} classifier versions; {meta['supplement_versions']} supplement versions; "
      f"{n_flag} families flagged -> {HERE.relative_to(ROOT)}/")
