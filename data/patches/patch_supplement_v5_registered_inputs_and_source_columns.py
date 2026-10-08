"""Build the v5 classification CSV: registered inputs in the main columns, source-reported values beside them.

Run:  uv run --no-project python data/patches/patch_supplement_v5_registered_inputs_and_source_columns.py

Two changes to v4, and no others.

1. Anti-CD20-MS, observational leg. v4 printed d = 1.084, the figure the source reports
   (hazard ratio 0.14, Amendment 3). The frozen classifier holds OR 2.23, d = 0.442, and that is
   the input the registered result was computed from. For every other family whose input differs
   from its source, the main columns already carry the registered input. v5 does the same here:
   obs_d 0.442, obs_type epidemiological_OR. Both values are non-trivial, so obs_class,
   classification, prediction and correct are the same in v4 and v5.

2. Ten columns are appended for the 32 scored families, copied from the Amendment 6 run
   (analysis/amendment6/source_values_by_family.csv): which values that run used, the source
   figure and its conversion, and d, class, classification, prediction and score under
   source-reported values. Anti-CD20-MS has 1.084 there.

The script then checks every scored family's obs_d and mr_d against the frozen classifier, so a
main-column value that the classifier did not use cannot ship again.

The input files are not modified.
"""
import csv
import hashlib
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLASSIFIER = os.path.join(ROOT, "analysis", "classifier", "classify_families.py")
V4 = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v4.csv")
V5 = os.path.join(ROOT, "data", "cross_design_classification_all_41_families_v5.csv")
BY_FAMILY = os.path.join(ROOT, "analysis", "amendment6", "source_values_by_family.csv")
SHA256 = {
    CLASSIFIER: "4b9a9caa516e358769f409d4051ba0235df4366745ab2bef70460aad2be13118",
    V4: "03aca6edb84aa7ad37339f5023b213ca37e036b1ab9e4c582f38d1f421b46742",
    BY_FAMILY: "64ea25e0f261920e9c35d1ef3c039ceab369e36fe6e4e68e0f81ddf2f2d9a854",
}
FAMILY = "Anti-CD20-MS"
V4_CELLS = {"obs_d": "1.084", "obs_type": "pooled_NRSI_HR"}
SCORED = ("pre-registered", "extension")
# v5 column <- column of the Amendment 6 per-family output
SOURCE_COLUMNS = {
    "amendment6_values_used": "value_used",
    "source_figure": "source_figure",
    "source_conversion": "conversion",
    "source_obs_d": "source_obs_d",
    "source_mr_d": "source_gen_d",
    "source_obs_class": "source_obs_class",
    "source_mr_class": "source_mr_class",
    "source_classification": "source_classification",
    "source_prediction": "source_prediction",
    "source_correct": "correct_under_source",
}


class InputChanged(Exception):
    """An input is not the file this patch was written against."""


class SupplementDisagreesWithClassifier(Exception):
    """A main-column value is not the value the frozen classifier holds."""


class OutputExists(Exception):
    """v5 is already on disk with different bytes; it is not overwritten."""


def read(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    if hashlib.sha256(raw).hexdigest() != SHA256[path]:
        raise InputChanged(os.path.relpath(path, ROOT))
    return raw.decode()


def load_classifier():
    read(CLASSIFIER)
    spec = importlib.util.spec_from_file_location("classify_families", CLASSIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def registered_d(clf):
    """(obs_d, mr_d) for every family, computed by the frozen classifier's own functions."""
    out = {}
    for fam in clf.NEURO_FAMILIES + clf.CARDIO_FAMILIES + clf.AUTOIMMUNE_FAMILIES + clf.EXTENSION_FAMILIES:
        obs = fam["obs_d_direct"] if fam.get("obs_d_direct") is not None else clf.chinn_d(fam["obs_OR"])
        gen = fam["gen_OR"]
        if fam.get("per_allele"):
            gen = clf.rescale_per_allele_to_per_sd(gen, fam["sd_per_allele"])
        out[fam["family"]] = (obs, clf.chinn_d(gen))
    return out


def main():
    clf = load_classifier()
    registered = registered_d(clf)
    rows = list(csv.DictReader(read(V4).splitlines()))
    v4_fields = list(rows[0].keys())
    source = {r["family"]: r for r in csv.DictReader(read(BY_FAMILY).splitlines())}

    target = [r for r in rows if r["family"] == FAMILY]
    if len(target) != 1 or any(target[0][k] != v for k, v in V4_CELLS.items()):
        raise InputChanged(f"{FAMILY} is not the row this patch was written against")
    before = [dict(r) for r in rows]
    target[0]["obs_d"] = f"{registered[FAMILY][0]:.3f}"
    target[0]["obs_type"] = "epidemiological_OR"

    scored = [r for r in rows if r["status"] in SCORED]
    if sorted(r["family"] for r in scored) != sorted(source):
        raise InputChanged("the scored families are not the families of the Amendment 6 run")
    for row in rows:
        src = source.get(row["family"])
        for new, old in SOURCE_COLUMNS.items():
            row[new] = src[old] if src else ""

    # One row, two cells, among the v4 columns.
    changed = [(a["family"], k) for a, b in zip(before, rows) for k in v4_fields if a[k] != b[k]]
    assert changed == [(FAMILY, "obs_d"), (FAMILY, "obs_type")], changed

    # Every scored family's main-column d is the classifier's.
    for row in scored:
        obs, gen = registered[row["family"]]
        if abs(float(row["obs_d"]) - obs) > 0.0015 or abs(float(row["mr_d"]) - gen) > 0.0015:
            raise SupplementDisagreesWithClassifier(row["family"])
        if row["obs_class"] != source[row["family"]]["registered_obs_class"]:
            raise SupplementDisagreesWithClassifier(row["family"])

    assert len(rows) == 41 and len(scored) == 32
    assert sum(r["correct"] == "True" for r in scored) == 24
    assert sum(r["source_correct"] == "True" for r in scored) == 24
    assert target[0]["source_obs_d"] == V4_CELLS["obs_d"]

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=v4_fields + list(SOURCE_COLUMNS), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    out = buf.getvalue().encode()
    if os.path.exists(V5):
        with open(V5, "rb") as handle:
            if handle.read() != out:
                raise OutputExists(os.path.relpath(V5, ROOT))
    with open(V5, "wb") as handle:
        handle.write(out)

    print(f"wrote {os.path.relpath(V5, ROOT)}  sha256 {hashlib.sha256(out).hexdigest()}")
    print(f"{FAMILY}: obs_d {V4_CELLS['obs_d']} -> {target[0]['obs_d']}, obs_type {V4_CELLS['obs_type']} -> {target[0]['obs_type']}")
    print("41 families, 32 scored, 24 correct on registered inputs, 24 correct on source-reported values")


if __name__ == "__main__":
    main()
