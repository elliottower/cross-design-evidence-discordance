"""Build the repository snapshot that ships with the Zenodo deposit.

Run:  uv run --no-project --python 3.12 python scripts/build_zenodo_deposit.py

The snapshot is the working tree, so it carries the state that produced the
manuscript rather than the last commit. Five kinds of thing are held out:

  paper/         the whole directory. It mixes analysis-relevant sources with a
                 cover letter, per-reviewer manuscript versions, and patch
                 scripts named for a response letter. The manuscript is
                 deposited as its own PDF, so nothing here is lost by omitting
                 the directory, and no filtering rule has to be trusted to
                 catch the next submission file that lands in it.
  peer review    reviews/, SUBMISSIONS/ and SUBMISSION_STATUS.md hold reviewer
                 reports, response letters and editor correspondence.
  build output   LaTeX leaves .aux/.log/.out beside every manuscript version.
  archives       a deposit that nests last deposit's zip inside this one.
  caches         .git, __pycache__, .venv, .DS_Store, and .results, which holds
                 sealed run hashes that stay local.

An existing archive is never overwritten: each deposit keeps its own file, so
the zip that was actually uploaded stays recoverable.
"""

import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEST = REPO / "paper" / "submission" / "zenodo" / "cross_design_evidence_discordance_repo_v3.zip"

EXCLUDED_DIRS = {
    ".git", "__pycache__", ".venv", ".pytest_cache", ".ruff_cache",
    "paper", "reviews", "SUBMISSIONS", ".results",
}
EXCLUDED_PATHS = {
    Path("SUBMISSION_STATUS.md"),
    Path("TODO.md"),
    Path("SPEC_TIER_PREDICTS_OUTCOME.md"),
    Path("TODO_POTENTIALLY_REANCHOR_LEDGER.md"),
}
EXCLUDED_SUFFIXES = {
    ".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".bbl", ".blg",
    ".synctex.gz", ".toc", ".zip", ".pyc",
}
EXCLUDED_NAMES = {".DS_Store"}


def excluded(relative: Path) -> bool:
    if EXCLUDED_DIRS & set(relative.parts):
        return True
    if any(relative == path or path in relative.parents for path in EXCLUDED_PATHS):
        return True
    return relative.suffix in EXCLUDED_SUFFIXES or relative.name in EXCLUDED_NAMES


def main() -> int:
    if DEST.exists():
        raise FileExistsError(f"{DEST.name} exists; name the next deposit _v3")

    members = sorted(
        path for path in REPO.rglob("*")
        if path.is_file() and not excluded(path.relative_to(REPO))
    )
    with zipfile.ZipFile(DEST, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in members:
            archive.write(path, path.relative_to(REPO))

    names = [str(path.relative_to(REPO)) for path in members]
    assert not any(name.startswith("paper/") for name in names), "paper/ leaked in"

    top = sorted({Path(name).parts[0] for name in names})
    print(f"wrote {DEST.relative_to(REPO)}")
    print(f"  {len(members)} files, {DEST.stat().st_size / 1e6:.1f} MB")
    print(f"  top level: {', '.join(top)}")
    for held_out in sorted(EXCLUDED_DIRS - {".git", "__pycache__", ".venv",
                                            ".pytest_cache", ".ruff_cache"}):
        print(f"  held out: {held_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
