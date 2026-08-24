"""Build the reading packet for a revision and mirror it to iCloud.

Run:  uv run python reviews/packet/build_revision_packet.py [destination]

The packet is what gets read on a phone: the manuscript and the response letter
as EPUB and HTML beside the sources, the bibliography and supplementary CSV they
name, the reviewer audits, and the scripts that built and checked everything.

Three rules the script enforces rather than trusts:

1. The manuscript and letter are the newest versions, resolved from the
   directory. A pinned filename here would keep shipping the previous revision
   after a version bump, and the packet is exactly where that would go unnoticed.

2. The destination folder must not already exist. Packets are provenance -- an
   overwritten one destroys the copy that was read.

3. Pandoc exits 0 on a conversion it mangled, so every EPUB and HTML is checked
   by verify_mobile_formats.py before the packet is written. A failure aborts.

The README is not generated. It is written by hand at reviews/packet/README.md
and copied verbatim, because a templated summary of a revision says nothing.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MOBILE = REPO / "reviews" / "mobile"
ICLOUD = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
VERIFY = REPO / "reviews" / "verification" / "verify_mobile_formats.py"
README = REPO / "reviews" / "packet" / "README.md"

# Copied verbatim into the packet. Relative to the repository root.
ALSO = [
    "paper/submission/supplementary/cross_design_classification_all_41_families_v2.csv",
    "paper/references.resolved_v2.yaml",
    "reviews/REVIEWER1_AUDIT_v1.md",
    "reviews/REVIEWER3_AUDIT_v4.md",
]
# The scripts that built this revision and the ones that check it.
SCRIPTS = [
    "paper/patches/patch_v20_sigma_provenance_and_data_pin.py",
    "paper/patches/patch_v21_sigma_units.py",
    "paper/patches/patch_references_v7_audited.py",
    "paper/patches/patch_v22_audited_refs.py",
    "reviews/patches/patch_letter_v5_bibliography_audit.py",
    "reviews/verification/audit_bibliography.py",
    "reviews/verification/audit_bibliography_cli.py",
    "reviews/verification/verify_sigma_source.py",
    "reviews/verification/verify_v15_numbers.py",
    "reviews/verification/verify_letter_bibliography_claims.py",
    "reviews/verification/verify_mobile_formats.py",
    "reviews/verification/reconcile_supplement_to_accounting.py",
    "reviews/packet/build_revision_packet.py",
]


def newest(directory: Path, pattern: str, stem: str) -> Path:
    versions = sorted(
        ((int(re.match(stem, path.stem).group(1)), path)
         for path in directory.glob(pattern) if re.match(stem, path.stem)),
        key=lambda pair: pair[0])
    if not versions:
        raise FileNotFoundError(f"nothing matching {pattern} under {directory}")
    return versions[-1][1]


def convert(source: Path, bibliography: Path | None) -> tuple[Path, Path]:
    """Write source.html and source.epub into reviews/mobile/, and check both."""
    MOBILE.mkdir(parents=True, exist_ok=True)
    out_html = MOBILE / f"{source.stem}.html"
    out_epub = MOBILE / f"{source.stem}.epub"
    common = ["--standalone", "--toc", "--mathml", "--resource-path", str(source.parent)]
    if bibliography is not None:
        common += ["--citeproc", "--bibliography", str(bibliography)]
    for out in (out_html, out_epub):
        result = subprocess.run(["pandoc", str(source), *common, "-o", str(out)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"pandoc failed on {source.name} -> {out.suffix}:\n{result.stderr}",
                  file=sys.stderr)
            raise SystemExit(1)
    check = subprocess.run(
        [sys.executable, str(VERIFY), str(source), str(out_html), str(out_epub)],
        capture_output=True, text=True)
    print(check.stdout, end="")
    if check.returncode != 0:
        print(f"the conversion of {source.name} dropped content; packet not written",
              file=sys.stderr)
        raise SystemExit(1)
    return out_html, out_epub


def main() -> int:
    manuscript = newest(REPO / "paper", "paper_v*.tex", r"paper_v(\d+)")
    letter = newest(REPO / "reviews", "RESPONSE_TO_REVIEWERS_v*.md",
                    r"RESPONSE_TO_REVIEWERS_v(\d+)")
    cites = re.search(r"\\bibliography\{([^}]+)\}", manuscript.read_text())
    if cites is None:
        print(f"{manuscript.name} cites no bibliography", file=sys.stderr)
        return 1
    bibliography = REPO / "paper" / f"{cites.group(1)}.bib"
    if not bibliography.exists():
        print(f"{manuscript.name} cites {bibliography.name}, which does not exist",
              file=sys.stderr)
        return 1

    version = re.match(r"paper_v(\d+)", manuscript.stem).group(1)
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        ICLOUD / f"cross-design-evidence-v{version}-response")
    if destination.exists():
        print(f"{destination} already exists. Packets are not overwritten.",
              file=sys.stderr)
        return 1
    if not README.exists():
        print(f"write {README.relative_to(REPO)} first", file=sys.stderr)
        return 1

    print(f"manuscript   {manuscript.name}")
    print(f"letter       {letter.name}")
    print(f"bibliography {bibliography.name}\n")

    manuscript_formats = convert(manuscript, bibliography)
    print()
    letter_formats = convert(letter, None)

    destination.mkdir(parents=True)
    (destination / "scripts").mkdir()
    copied = [manuscript, letter, bibliography, *manuscript_formats, *letter_formats,
              *(REPO / name for name in ALSO)]
    pdf = manuscript.with_suffix(".pdf")
    if pdf.exists():
        copied.append(pdf)
    for path in copied:
        shutil.copy2(path, destination / path.name)
    for name in SCRIPTS:
        shutil.copy2(REPO / name, destination / "scripts" / Path(name).name)
    shutil.copy2(README, destination / "README.md")

    print(f"\n{len(copied) + len(SCRIPTS) + 1} files -> {destination}")
    if not pdf.exists():
        print(f"NOTE: {pdf.name} was not built, so the packet has no PDF.\n"
              f"      cd paper && latexmk -pdf {manuscript.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
