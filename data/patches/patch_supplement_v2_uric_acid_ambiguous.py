"""Build the v2 classification CSVs: Uric acid recorded as ambiguous, not as a miss.

Run:  uv run python data/patches/patch_supplement_v2_uric_acid_ambiguous.py

The manuscript excludes Uric acid from the scored set as ambiguous -- conventional
MR gives OR 1.18 (1.08--1.29) while pleiotropy-robust Egger MR is null, so the
estimate depends on the method -- and Table 1 counts it in the Ambig. column.
The shipped CSV instead carried status "pre-registered" and correct "False",
which scores it as a miss. That gives 24/33 with nine misses against the
manuscript's 24/32 with eight, a contradiction anyone who counts the CSV finds.

One row, two fields. Every other byte comes through unchanged, so a diff against
the input shows exactly this change and nothing else.

The supplementary and Zenodo copies are byte-identical inputs and are written as
a matched pair; shipping the correction to one and not the other would reproduce
the same contradiction in the archive.

The input files are not modified.
"""

import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATASET = "cross_design_classification_all_41_families"
COPIES = [REPO / "paper" / "submission" / d / f"{DATASET}.csv"
          for d in ("supplementary", "zenodo")]

FAMILY = "Uric acid"
EXPECTED = {"status": "pre-registered", "correct": "False"}
CORRECTED = {"status": "ambiguous", "correct": ""}


def patch(raw: str) -> str:
    rows = list(csv.DictReader(raw.splitlines()))
    fields = list(rows[0].keys())

    targets = [r for r in rows if r["family"] == FAMILY]
    if len(targets) != 1:
        raise SystemExit(f"ABORT -- {len(targets)} rows named {FAMILY!r}, expected exactly 1")
    row = targets[0]
    for field, value in EXPECTED.items():
        if row[field] != value:
            raise SystemExit(
                f"ABORT -- {FAMILY}.{field} is {row[field]!r}, expected {value!r}. "
                "The input is not the file this patch was written against.")
    row.update(CORRECTED)

    # lineterminator="\n": the inputs are LF and must stay LF, or every line
    # reads as changed in a diff and the one real change is buried.
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def main() -> int:
    for field, value in CORRECTED.items():
        print(f"  {FAMILY}.{field}: {EXPECTED[field]!r} -> {value!r}")

    for src in COPIES:
        raw = src.read_text()
        out = patch(raw)
        dst = src.with_name(f"{DATASET}_v2.csv")

        # Byte-level, not read_text(): universal newlines would hide a CRLF
        # rewrite by normalizing it away before the comparison.
        before, after = raw.encode().split(b"\n"), out.encode().split(b"\n")
        assert b"\r" not in out.encode(), "the writer introduced carriage returns"
        assert len(before) == len(after), f"line count moved in {src.name}"
        differing = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
        assert len(differing) == 1, f"{len(differing)} lines differ in {src.name}, expected 1"

        rows = list(csv.DictReader(out.splitlines()))
        assert len(rows) == 41, f"{len(rows)} families, expected 41"
        scored = [r for r in rows if r["status"] in {"pre-registered", "extension"}]
        assert len(scored) == 32, f"{len(scored)} scored, expected 32"
        assert sum(r["correct"] == "True" for r in scored) == 24, "correct count moved"
        assert sum(r["correct"] == "False" for r in scored) == 8, "miss count is not 8"
        assert sum(r["correct"] == "" for r in scored) == 0, "a scored row has no verdict"

        dst.write_text(out)
        print(f"  wrote {dst.relative_to(REPO)}")

    print("\n41 families, 32 scored, 24 correct, 8 misses, Uric acid ambiguous")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
