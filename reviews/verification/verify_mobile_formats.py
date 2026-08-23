"""Check that a pandoc EPUB and HTML carry the same content as their Markdown source.

Run:  uv run python reviews/verification/verify_mobile_formats.py <source.md> <out.html> <out.epub>

Conversion failures are quiet. Pandoc exits 0 on a document whose tables it
mangled, whose headers it dropped, or whose math it swallowed, so the only way
to know a mobile copy is readable is to look for the content in it.

The comparison is deliberately tolerant. Pandoc rewraps lines, converts ASCII
punctuation to typographic punctuation, and renders emphasis as tags, so both
sides are folded to lowercase alphanumerics and single spaces before matching.
A phrase that survives that fold and is still missing is genuinely absent.

Checked, per output format:
  - every ATX header in the source appears as text
  - every numeric token in the source appears, including every accuracy
    fraction, confidence bound, p-value, and trial identifier
  - the document's own delimiters survive, so a truncated conversion is visible

The numeric tokens are read out of the source rather than listed here. A
hand-written list of figures to look for tests the list, and drifts the first
time the document is revised.
"""

import html
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

# Numbers a table drop or a truncated conversion would take with it, and that a
# reader on a phone would have no way to notice were gone. Accuracy fractions
# (24/32), decimals (0.083), and identifiers (NCT05021835) all match this.
NUMERIC = re.compile(r"(?:NCT\d+|\d[\d,]*(?:\.\d+)?(?:/\d[\d,]*(?:\.\d+)?)?)")

# Landmarks near the end of a document. A conversion that stopped early keeps
# every early check passing, so at least one of these has to be late in the text.
DELIMITERS = ["BEGIN LETTER", "END LETTER", "PART A", "Reviewer 1", "Reviewer 3",
              "Limitations", "References"]


def fold(text: str) -> str:
    """Lowercase alphanumerics and single spaces, so wrapping cannot cause a miss."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def strip_markup(markup: str) -> str:
    markup = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.DOTALL | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", markup))


def epub_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.endswith((".xhtml", ".html"))]
        return " ".join(strip_markup(archive.read(n).decode("utf-8", "replace"))
                        for n in sorted(names))


SECTION = re.compile(r"\\(?:sub){0,2}section\*?\{((?:[^{}]|\{[^{}]*\})*)\}")


def source_headers(source: str, is_tex: bool) -> list[str]:
    if is_tex:
        return [re.sub(r"\\[a-zA-Z]+|[{}$]", "", h).strip()
                for h in SECTION.findall(source)]
    return [re.sub(r"[*_`]", "", line.lstrip("# ").strip())
            for line in source.splitlines() if line.startswith("#")]


def source_numbers(source: str) -> list[str]:
    """Every distinct numeric token in the source, longest first.

    Bare one- and two-digit numbers are dropped: they are list markers and
    section numbers, they appear everywhere, and they cannot distinguish a
    faithful conversion from a mangled one.
    """
    tokens = {t for t in NUMERIC.findall(source)
              if "/" in t or "." in t or t.startswith("NCT") or len(t) > 2}
    return sorted(tokens, key=lambda t: (-len(t), t))


def tex_body(source: str) -> str:
    """The part of a .tex file that reaches the page.

    Preamble, comments, labels, and cross-reference keys carry numbers that are
    never typeset -- a \\label{tab:accounting} or a 95\\% in a comment -- and
    demanding them in the HTML would fail every run for the wrong reason.
    """
    body = source.split(r"\begin{document}", 1)[-1]
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"\\(?:label|ref|cite[a-zA-Z]*|input|include|bibliography(?:style)?)\s*\{[^{}]*\}", " ", body)
    return body


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__.split("\n")[2].strip(), file=sys.stderr)
        return 2
    source, html_out, epub_out = (Path(a) for a in sys.argv[1:4])
    raw = source.read_text()
    is_tex = source.suffix == ".tex"
    headers = source_headers(raw, is_tex)
    searchable = tex_body(raw) if is_tex else raw
    numbers = source_numbers(searchable)
    delimiters = [d for d in DELIMITERS if fold(d) in fold(searchable)]
    wanted = headers + numbers + delimiters

    failed = 0
    for label, body in (("html", strip_markup(html_out.read_text())),
                        ("epub", epub_text(epub_out))):
        folded = fold(body)
        missing = [w for w in wanted if fold(w) and fold(w) not in folded]
        words = len(folded.split())
        if missing:
            failed += 1
            print(f"{label}: {len(wanted) - len(missing)}/{len(wanted)} present, "
                  f"{words} words -- MISSING:")
            for item in missing:
                print(f"    {item}")
        else:
            print(f"{label}: all {len(wanted)} checks present, {words} words")

    source_words = len(fold(raw).split())
    print(f"\nsource: {len(headers)} headers, {len(numbers)} numeric tokens, "
          f"{source_words} words")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
