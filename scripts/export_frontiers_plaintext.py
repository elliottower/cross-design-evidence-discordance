"""Export the manuscript's abstract and main sections as plain text for the Frontiers portal.

Run:  uv run --no-project python scripts/export_frontiers_plaintext.py paper/paper_v25_round3.tex

Writes one file per section into paper/frontiers_plaintext_<version>/, never
overwriting an existing export. Each section is converted with pandoc from the
LaTeX source; tables, figures and the algorithm float are dropped, since the
portal takes those as separate uploads.
"""
import re, subprocess, sys
from pathlib import Path

src = Path(sys.argv[1]).resolve()
version = re.match(r"paper_(v\d+)", src.stem).group(1)
out = src.parent / f"frontiers_plaintext_{version}"
if out.exists():
    raise SystemExit(f"{out} exists; exports are not overwritten")
text = src.read_text(encoding="utf-8")

abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
body = text[text.index(r"\section{Introduction}"):text.index(r"\section*{Abbreviations}")]
parts = re.split(r"(?=\\section\{)", body)
sections = {re.match(r"\\section\{([^}]*)\}", p).group(1): p for p in parts if p.strip()}

def strip_floats(s):
    s = re.sub(r"\\begin\{(table|figure|algorithm)\}.*?\\end\{\1\}", "", s, flags=re.S)
    return s

def to_plain(s):
    r = subprocess.run(["pandoc", "-f", "latex", "-t", "plain", "--wrap=none"],
                       input=s, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    return r.stdout.strip() + "\n"

out.mkdir()
files = [("00_abstract.txt", abstract)] + [
    (f"{i+1:02d}_{name.lower().replace(' ', '_')}.txt", strip_floats(sections[name]))
    for i, name in enumerate(["Introduction", "Materials and Methods", "Results", "Discussion", "Conclusions"])]
for name, content in files:
    (out / name).write_text(to_plain(content), encoding="utf-8")
    print(name, len((out / name).read_text().split()), "words")
print("wrote", out)
