"""Verification of every numerical claim made in the Reviewer 3 response.

Run:  uv run --with pandas python reviews/verification/verify_reviewer3_claims.py

Emits a human-readable report on stdout and a machine-readable record to
reviews/verification/output/reviewer3_verification.json.

Nothing here re-analyzes data. Every check either (a) recomputes a published
conversion from the printed inputs, or (b) executes the frozen classifier
shipped at paper/reference/classify_families.py and compares its output to
what the manuscript prints. Discrepancies are reported, not resolved.
"""

import importlib.util
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CLASSIFIER = REPO / "paper" / "reference" / "classify_families.py"
SUPPLEMENT = REPO / "paper" / "supplementary_data.csv"
OUT = Path(__file__).resolve().parent / "output" / "reviewer3_verification.json"

CHINN = math.sqrt(3) / math.pi
THRESHOLD = 0.10

record: dict = {"checks": []}


def note(name: str, expected, observed, ok: bool, comment: str = "") -> None:
    record["checks"].append(
        {"check": name, "expected": expected, "observed": observed,
         "ok": bool(ok), "comment": comment}
    )
    flag = "OK  " if ok else "FAIL"
    print(f"[{flag}] {name}")
    print(f"       manuscript says : {expected}")
    print(f"       recomputed      : {observed}")
    if comment:
        print(f"       {comment}")
    print()


def chinn_d(odds_ratio: float) -> float:
    """Chinn (2000): d = |ln(OR)| * sqrt(3) / pi. Note the absolute value."""
    return abs(math.log(odds_ratio)) * CHINN


def load_classifier():
    spec = importlib.util.spec_from_file_location("classify_families", CLASSIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 1 -- Chinn conversions for families the manuscript calls")
print("            threshold-sensitive (Limitations, 'Threshold sensitivity')")
print("=" * 74)
print()

note("Chinn constant sqrt(3)/pi", 0.551329, round(CHINN, 6),
     abs(CHINN - 0.551329) < 5e-7)

note("IL-6R Chinn d on the PER-ALLELE OR 0.95 (v9 footnote h)",
     0.028, round(chinn_d(0.95), 4),
     abs(chinn_d(0.95) - 0.028) < 5e-4,
     "This is the raw per-allele value, before any per-SD rescaling.")

note("CTLA-4-RA Chinn d on OR 0.86 (Table tab:autoimmune)",
     0.083, round(chinn_d(0.86), 4),
     abs(chinn_d(0.86) - 0.083) < 5e-4)

note("Anti-CD20-MS Chinn d on MR OR 0.83 (Table tab:stage1)",
     0.103, round(chinn_d(0.83), 4),
     abs(chinn_d(0.83) - 0.103) < 5e-4,
     f"Clears the {THRESHOLD} threshold by {chinn_d(0.83) - THRESHOLD:.4f} "
     "-- Reviewer 3 states 0.003.")

note("JAK-STAT-RA Chinn d on MR OR 1.27",
     "0.132 in Table tab:autoimmune / 0.131 in Limitations prose",
     round(chinn_d(1.27), 4),
     abs(chinn_d(1.27) - 0.132) < 5e-4,
     "Table rounds correctly; the Limitations prose says 0.131. Unify to 0.132.")

note("Uric acid MR (Egger, pleiotropy-robust) d on OR 1.05",
     "Limitations prose lists 'Uric acid (d = 0.037)'",
     round(chinn_d(1.05), 4),
     abs(chinn_d(1.05) - 0.037) < 5e-4,
     "MISMATCH: 0.037 is the OBSERVATIONAL d (OR 1.07), not the MR d. "
     f"OBS d = {chinn_d(1.07):.4f}; MR Egger d = {chinn_d(1.05):.4f}.")

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 2 -- The IL-6R per-SD rescaling")
print("=" * 74)
print()

clf = load_classifier()
il6r = next(f for f in clf.CARDIO_FAMILIES if f["family"] == "IL-6R")
sigma = il6r["sd_per_allele"]
or_rescaled = clf.rescale_per_allele_to_per_sd(il6r["gen_OR"], sigma)
d_rescaled = chinn_d(or_rescaled)

print(f"sigma recorded in the frozen classifier: sd_per_allele = {sigma}")
print(f"OR_per-SD = {il6r['gen_OR']} ** (1/{sigma}) = {or_rescaled:.4f}")
print(f"Chinn d on the rescaled OR              = {d_rescaled:.4f}")
print()

# The v9 footnote asserted the rescaling CLEARS the threshold for sigma <= 0.283.
sigma_break = abs(math.log(il6r["gen_OR"])) * CHINN / THRESHOLD
note("v9 footnote h: 'clears d = 0.10 for any per-allele exposure SD sigma <= 0.283'",
     "sigma <= 0.283 clears the threshold",
     f"sigma <= {sigma_break:.4f} clears it; classifier uses sigma = {sigma}",
     sigma <= sigma_break,
     "FAILS: the sigma actually used (0.34) is ABOVE the break point, so the "
     f"rescaled d = {d_rescaled:.4f} does NOT clear 0.10. The v9 footnote is "
     "arithmetically right about the break point but wrong about this family.")

note("IL-6R rescaled d vs the Limitations prose value",
     "Limitations prose lists 'IL-6R (d = 0.083)'",
     round(d_rescaled, 4),
     abs(d_rescaled - 0.083) < 5e-4,
     "The Limitations prose is CORRECT -- it quotes the rescaled d. "
     "Reviewer 1 read 0.083 off this line and attributed it to the table.")

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 3 -- Frozen classifier output vs. what the manuscript prints")
print("=" * 74)
print()

families = clf.NEURO_FAMILIES + clf.CARDIO_FAMILIES
results = clf.run_classification(families, threshold=THRESHOLD)
by_family = {r["family"]: r for r in results}

header = (f"{'family':16s} {'obs_d':>6s} {'obs':>11s} {'gen_d':>6s} "
          f"{'mr':>6s} {'classification':>23s} {'prediction':>10s}")
print(header)
print("-" * len(header))
for r in results:
    print(f"{r['family']:16s} {r['obs_d']:6.3f} {r['obs_class']:>11s} "
          f"{r['gen_d']:6.3f} {r['mr_class']:>6s} "
          f"{r['classification']:>23s} {str(r['prediction']):>10s}")
print()
record["frozen_classifier_output"] = results

# Manuscript claims for the two prospective families.
MANUSCRIPT = {
    "Lp(a)": {"table_mr": "Causal", "table_class": "Concordant",
              "prose": "classified as 'Approve' by the frozen rule"},
    "IL-6R": {"table_mr": "Causal", "table_class": "Concordant",
              "prose": "classified as 'Approve' by the frozen rule"},
}

for fam, claim in MANUSCRIPT.items():
    r = by_family[fam]
    code_says = f"{r['classification']} -> predict {r['prediction']}"
    paper_says = f"{claim['table_class']} -> {claim['prose']}"
    agrees = (r["prediction"] == "success")
    note(f"{fam}: manuscript prospective prediction vs frozen classifier",
         paper_says, code_says, agrees,
         f"obs_d = {r['obs_d']} ({r['obs_class']}), "
         f"gen_d = {r['gen_d']} ({r['mr_class']} under the two-criterion rule).")

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 4 -- Is the two-criterion rule applied consistently?")
print("=" * 74)
print()
print("The manuscript footnotes three families whose CI excludes null but whose")
print("d < 0.10, and classifies each as MR-null under the two-criterion rule:")
print("  BMI-AD        (d = 0.016) -- footnoted in Table tab:stage1")
print("  Estrogen-BC   (d = 0.016) -- footnoted in Table tab:extension")
print("  Serotonin-MDD (d = 0.042) -- footnoted in Table tab:extension")
print()
print("Lp(a) (d = 0.034) and IL-6R (rescaled d = 0.083) are the same situation")
print("and are NOT footnoted; both are printed as 'Causal' and 'Concordant'.")
print()
same_situation = []
for fam in ("Lp(a)", "IL-6R"):
    r = by_family[fam]
    ci_excludes = clf.ci_excludes_null(
        next(f for f in families if f["family"] == fam)["gen_CI_lower"],
        next(f for f in families if f["family"] == fam)["gen_CI_upper"])
    same_situation.append(
        {"family": fam, "ci_excludes_null": ci_excludes,
         "gen_d": r["gen_d"], "below_threshold": r["gen_d"] < THRESHOLD,
         "two_criterion_mr_class": r["mr_class"]})
record["inconsistent_footnoting"] = same_situation
print(json.dumps(same_situation, indent=2))
print()

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 5 -- Does the rule use effect DIRECTION? (Reviewer 3, point 4)")
print("=" * 74)
print()
# Structural check: chinn_d discards sign; a protective and a harmful OR of
# equal magnitude must map to the same d.
d_protective = chinn_d(0.67)
d_harmful = chinn_d(1.0 / 0.67)
note("Direction is discarded by the Chinn conversion",
     "sign-blind (|ln(OR)| in Eq. 1)",
     f"d(OR=0.67) = {d_protective:.4f}; d(OR=1.49) = {d_harmful:.4f}",
     abs(d_protective - d_harmful) < 1e-12,
     "A protective and a harmful OR of reciprocal magnitude are indistinguishable "
     "to the classifier. Neither classify_obs nor classify_family inspects sign.")

# HRT-AD is the paper's own sign-reversal example.
hrt = by_family["HRT-AD"]
print("HRT-AD is the manuscript's stated sign-reversal case:")
print(f"  OBS OR 0.67 (protective)  -> d = {chinn_d(0.67):.4f}")
print("  MR  OR 1.00 (null)")
print("  RCT HR 1.76 (harmful, WHIMS)")
print(f"  classifier output: {hrt['classification']} -> {hrt['prediction']}")
print("  The reversal is between OBS and RCT. The MR leg is null, so no two")
print("  non-null etiologic estimates conflict here. The rule never saw a sign.")
print()

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 6 -- Does the shipped supplement match its description?")
print("=" * 74)
print()
import csv as _csv
with open(SUPPLEMENT) as fh:
    rows = list(_csv.DictReader(fh))
fam_names = sorted({r["family"] for r in rows})
cols = list(rows[0].keys())
note("Supplementary Table S1 family count",
     "'all 41 families' (Materials and Methods, Data)",
     f"{len(fam_names)} distinct families, {len(rows)} rows",
     len(fam_names) == 41,
     "Extension-domain families and Amyloid-AD are absent from the shipped file.")

note("Supplementary Table S1 columns",
     "effect sizes, confidence intervals, gene targets, instrument types, classifications",
     ", ".join(cols),
     ("gene_target" in cols and "instrument_type" in cols),
     "No gene-target or instrument-type column is present.")

malformed = [r for r in rows if r["cohen_d"] in ("Approved", "Failed", "Pending")]
note("Supplementary Table S1 row integrity",
     "no shifted rows",
     f"{len(malformed)} rows with a drug outcome in the cohen_d column: "
     + ", ".join(sorted({r['family'] for r in malformed})),
     len(malformed) == 0,
     "Column shift: outcome text has landed in cohen_d and the source note in "
     "classification.")

# --------------------------------------------------------------------------
print("=" * 74)
print("SECTION 7 -- Classifier inputs vs manuscript inputs (record check)")
print("=" * 74)
print()
acd = next(f for f in families if f["family"] == "Anti-CD20-MS")
note("Anti-CD20-MS observational input",
     "HR 0.14 (Hu 2019), d = 1.084 (Table tab:stage1 and supplement)",
     f"obs_OR = {acd['obs_OR']} in the frozen classifier, d = {chinn_d(acd['obs_OR']):.3f}",
     abs(chinn_d(acd["obs_OR"]) - 1.084) < 5e-3,
     "Different input, same classification: both are far above 0.10, so OBS is "
     "non-trivial either way and no classification moves.")

# --------------------------------------------------------------------------
failed = [c for c in record["checks"] if not c["ok"]]
record["summary"] = {"total": len(record["checks"]),
                     "passed": len(record["checks"]) - len(failed),
                     "failed": len(failed),
                     "failed_checks": [c["check"] for c in failed]}

print("=" * 74)
print(f"SUMMARY: {record['summary']['passed']}/{record['summary']['total']} checks reproduce.")
print("=" * 74)
for c in failed:
    print(f"  DISCREPANCY: {c['check']}")
print()

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, indent=2, default=str))
print(f"Machine-readable record written to {OUT.relative_to(REPO)}")
