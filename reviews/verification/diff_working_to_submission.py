"""Report what the Frontiers-formatted submission copy is missing.

Run:  uv run python reviews/verification/diff_working_to_submission.py

The working manuscript (paper/paper_vNN_*.tex) and the submission copy
(paper/submission/manuscript/*.tex) are two renderings of one paper. The
submission copy carries the Frontiers class and its own preamble; the working
copy carries the revision. Comparing them by counting landmark strings gives
false answers -- "23/31" appears in both and means a different sensitivity in
each -- so this compares paragraph by paragraph over the body only.

Output is a port list: every body paragraph present in the working copy and
absent from the submission copy, and every paragraph the submission copy has
that the working copy does not.
"""

import difflib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SUBMISSION = REPO / "paper" / "submission" / "manuscript" / \
    "drug_failures_partition_cross_design_evidence.tex"

BODY_START = r"\section{Introduction}"
BODY_END = r"\bibliography"

# Two paragraphs that differ only by these are the same paragraph in different
# renderings, not a missing edit.
NOISE = [
    (re.compile(r"\s+"), " "),
    (re.compile(r"~"), " "),
    (re.compile(r"\\label\{[^}]*\}"), ""),
]


def newest_working() -> Path:
    versions = sorted(
        (p for p in (REPO / "paper").glob("paper_v*.tex")),
        key=lambda p: int(re.match(r"paper_v(\d+)", p.name).group(1)),
    )
    if not versions:
        raise SystemExit("ABORT -- no paper_v*.tex in paper/")
    return versions[-1]


def body(path: Path) -> str:
    text = path.read_text()
    if BODY_START not in text:
        raise SystemExit(f"ABORT -- {path.name} has no {BODY_START}")
    text = text.split(BODY_START, 1)[1]
    return text.split(BODY_END, 1)[0] if BODY_END in text else text


def paragraphs(text: str) -> list[str]:
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("%"):
            continue
        out.append(chunk)
    return out


def normalize(paragraph: str) -> str:
    for pattern, replacement in NOISE:
        paragraph = pattern.sub(replacement, paragraph)
    return paragraph.strip()


def preview(paragraph: str, width: int = 150) -> str:
    flat = normalize(paragraph)
    return flat if len(flat) <= width else flat[: width - 1] + "\u2026"


def main() -> int:
    working = newest_working()
    print(f"working:    {working.relative_to(REPO)}")
    print(f"submission: {SUBMISSION.relative_to(REPO)}\n")

    left = paragraphs(body(SUBMISSION))
    right = paragraphs(body(working))
    left_norm = [normalize(p) for p in left]
    right_norm = [normalize(p) for p in right]
    print(f"{len(left)} body paragraphs in the submission copy, "
          f"{len(right)} in the working copy\n")

    matcher = difflib.SequenceMatcher(None, left_norm, right_norm, autojunk=False)
    rewritten = 0
    added = 0
    dropped: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        print(f"--- {tag.upper()} "
              f"(submission {i1}:{i2} -> working {j1}:{j2}) " + "-" * 30)
        for index in range(i1, i2):
            print(f"SUBMISSION  {preview(left[index])}\n")
        for index in range(j1, j2):
            print(f"WORKING     {preview(right[index])}\n")
        if tag == "replace":
            rewritten += max(i2 - i1, j2 - j1)
        elif tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            dropped.extend(left[index] for index in range(i1, i2))

    print("=" * 72)
    print(f"{rewritten} paragraph(s) rewritten between the two copies.")
    print(f"{added} paragraph(s) the working copy adds.")
    print(f"{len(dropped)} paragraph(s) the working copy DROPS -- "
          "content that exists only in the submission copy:")
    for paragraph in dropped:
        print(f"  DROPPED  {preview(paragraph)}")
    if not dropped:
        print("  (none -- the working copy is a superset, so the port is a replacement)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
