"""Export the manuscript's abstract and main sections as plain text for the Frontiers portal.

Run:  uv run --no-project python scripts/export_frontiers_plaintext.py paper/paper_v25_round3.tex

Reads the compiled .aux beside the .tex for citation numbers, section, table,
figure and equation numbers, so the plain text carries "[13]", "Section 2.4",
"Table 5" the way the PDF does. Subsections are numbered. The two display
equations are written out in words. Tables and figures are dropped (the portal
takes them as uploads); Algorithm 1 is written out as numbered lines. Output
goes to paper/frontiers_plaintext_<version>_portal/, never overwriting.
"""
import re, subprocess, sys
from pathlib import Path

src = Path(sys.argv[1]).resolve()
aux = src.with_suffix(".aux")
version = re.match(r"paper_(v\d+)", src.stem).group(1)
out = src.parent / f"frontiers_plaintext_{version}_portal"
if out.exists():
    raise SystemExit(f"{out} exists; exports are not overwritten")
text = src.read_text(encoding="utf-8")
auxt = aux.read_text(encoding="utf-8")

def _bibcites(auxt):
    """\\bibcite{key}{{n}{year}{{authors}}{{}}}; authors may hold accent braces."""
    out = {}
    for line in auxt.splitlines():
        if not line.startswith("\\bibcite{"):
            continue
        key = line[len("\\bibcite{"):line.index("}")]
        rest = line[line.index("}") + 1:]
        groups, depth, cur = [], 0, ""
        for ch in rest[1:-1]:  # inside the outer {...}
            if ch == "{":
                depth += 1
                if depth == 1: cur = ""; continue
            if ch == "}":
                depth -= 1
                if depth == 0: groups.append(cur); continue
            if depth >= 1: cur += ch
        n, authors = groups[0], groups[2].strip("{}")
        authors = re.sub(r"\{\\.([A-Za-z])\}", r"\1", authors).replace("{", "").replace("}", "").replace("~", " ")
        out[key] = (n, authors)
    return out
cites = _bibcites(auxt)
labels = {m[0]: m[1] for m in re.findall(r"\\newlabel\{([^}]*)\}\{\{([0-9.]+)\}\{", auxt)}

def cite_num(keys):
    return "[" + ", ".join(cites[k.strip()][0] for k in keys.split(",")) + "]"
def citet(m):
    k = m.group(1).strip()
    return f"{cites[k][1]} {cite_num(k)}"
text = re.sub(r"\\citet\{([^}]*)\}", citet, text)
text = re.sub(r"\\citep?\{([^}]*)\}", lambda m: cite_num(m.group(1)), text)

def ref(m):
    lab = m.group(1)
    kind = lab.split(":")[0]
    n = labels.get(lab, "?")
    return {"sec": f"Section {n}", "par": f"Section {n}", "tab": f"Table {n}",
            "fig": f"Figure {n}", "alg": f"Algorithm {n}", "eq": f"Equation {n}"}.get(kind, n)
text = re.sub(r"\\S\\ref\{([^}]*)\}--\\S\\ref\{([^}]*)\}", lambda m: f"Sections {labels[m.group(1)]}-{labels[m.group(2)]}", text)
text = re.sub(r"\\S\\ref\{([^}]*)\}", ref, text)
text = re.sub(r"(Table|Figure|Algorithm|Equation)~\\ref\{([^}]*)\}", lambda m: ref(re.match(r"(.*)", m.group(2))), text)
text = re.sub(r"\\ref\{([^}]*)\}", ref, text)

# the two display equations, written out as on the 2 Sep form
text = text.replace(r"""\begin{equation}
d = \frac{|\ln(\text{OR})| \cdot \sqrt{3}}{\pi}, \qquad
\text{SE}_d = \frac{(\ln\text{CI}_{\text{upper}} - \ln\text{CI}_{\text{lower}})}{2 \times 1.96} \cdot \frac{\sqrt{3}}{\pi}.
\label{eq:chinn}
\end{equation}""",
"\n\nd = absolute value of ln(OR) multiplied by sqrt(3) / pi\n\nSE_d = [ln(CI_upper) - ln(CI_lower)] / [2 x 1.96] multiplied by sqrt(3) / pi\n\n")

# inline math to words
inline = [
 (r"\$d_\{\\text\{OBS\}\} \\geq 0\.10\$", "d_OBS is greater than or equal to 0.10"),
 (r"\$d_\{\\text\{MR\}\} \\geq 0\.10\$", "d_MR is greater than or equal to 0.10"),
 (r"\$d_\{\\text\{MR\}\} < 0\.10\$", "d_MR is less than 0.10"),
 (r"\$d_\{\\text\{OBS\}\}\$", "d_OBS"), (r"\$d_\{\\text\{MR\}\}\$", "d_MR"), (r"\$d_\{\\mathrm\{OBS\}\}\$", "d_OBS"), (r"\$d_\{\\mathrm\{MR\}\}\$", "d_MR"),
 (r"\$\\text\{OR\}_\{\\text\{per-SD\}\} = \\text\{OR\}_\{\\text\{per-allele\}\}\^\{1/\\sigma\}\$", "OR_per-SD = OR_per-allele raised to the power of 1 / sigma"),
 (r"\$< 5\\%\$", "below 5%"),
 (r"\$d = \|\\ln\(0\.83\)\| \\times \\sqrt\{3\}/\\pi = 0\.103\$", "d = absolute value of ln(0.83) multiplied by sqrt(3) / pi = 0.103"),
 (r"\$\\sigma\$", "sigma"), (r"\$\\sigma = ([0-9.]+)\$", r"sigma = \1"), (r"\$\\geq\$", "greater than or equal to"),
 (r"\$\\to\$", "->"), (r"\$\\times\$", "x"), (r"\$10\^5\$", "100,000"), (r"\$10\^\{5\}\$", "100,000"),
 (r"\$\\alpha = ([0-9.]+)\$", r"alpha = \1"), (r"\$I\^2\$", "I-squared"), (r"\$n = ([0-9,{}]+)\$", lambda m: "n = " + m.group(1).replace("{","").replace("}","")),
 (r"\$p ([<=]) ([0-9.]+)\$", r"p \1 \2"), (r"\$p\$", "p"), (r"\$d ([<=>]|\\geq|\\leq) ([0-9.]+)\$", lambda m: "d " + {"\\geq":">=","\\leq":"<="}.get(m.group(1), m.group(1)) + " " + m.group(2)),
 (r"\$d = ([0-9.]+)\$", r"d = \1"), (r"\$d\$", "d"), (r"\$d_\{\\text\{(OBS|MR)\}\} = ([0-9.]+)\$", r"d_\1 = \2"),
 (r"\$\|d\| = 0\.10\$", "|d| = 0.10"), (r"\$\\pm\$", "+/-"), (r"\$\\sim\$", "~"),
]
for pat, rep in inline:
    text = re.sub(pat, rep, text)
text = text.replace("\\emph{cis}", "cis").replace("\\emph{cis}-", "cis-")

abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S).group(1)
body = text[text.index(r"\section{Introduction}"):text.index(r"\section*{Abbreviations}")]

# number the section and subsection headings
secn = 0; subn = 0
def head(m):
    global secn, subn
    if m.group(1) == "section":
        secn += 1; subn = 0
        return f"\\section{{{secn} {m.group(2)}}}"
    subn += 1
    return f"\\subsection{{{secn}.{subn} {m.group(2)}}}"
body = re.sub(r"\\(section|subsection)\{([^}]*)\}", head, body)

ALGO = """Algorithm 1: Cross-design concordance classification

Required input: Mechanism families F = {f1, ..., fm}; for each family fj, effect sizes d_OBS and d_MR and the MR confidence interval (l, u).

1. Standardize. Convert odds ratios to d using Equation 1; enter SMDs directly.

2. Rescale. If the MR odds ratio is reported per allele, rescale it to a per-SD contrast before conversion.

3. For each family fj:

4. Classify OBS as non-trivial if d_OBS is greater than or equal to 0.10; otherwise classify it as trivial.

5. Classify MR as causal if 1.0 is not within the confidence interval (l, u) and d_MR is greater than or equal to 0.10; otherwise classify it as null.

6. If OBS is non-trivial and MR is null:

7. Label fj as qualitative discordance and predict failure.

8. Otherwise, if OBS is non-trivial and MR is causal:

9. Label fj as concordance and predict success.

10. Otherwise, if OBS is trivial and MR is null:

11. Label fj as null concordance and return an ambiguous prediction.

12. Otherwise, if OBS is trivial and MR is causal:

13. Label fj as genetic-only and predict success.

14. End if.

15. End for.

Output: For every drug mapped to family fj, the predicted outcome is success, failure, or ambiguous.
"""
body = re.sub(r"\\begin\{algorithm\}.*?\\end\{algorithm\}", "ALGORITHMPLACEHOLDER", body, flags=re.S)
body = re.sub(r"\\begin\{(table|figure)\}.*?\\end\{\1\}", "", body, flags=re.S)

parts = re.split(r"(?=\\section\{)", body)
sections = {}
for p in parts:
    m = re.match(r"\\section\{\d+ ([^}]*)\}", p)
    if m: sections[m.group(1)] = p

def to_plain(s):
    r = subprocess.run(["pandoc", "-f", "latex", "-t", "plain", "--wrap=none"], input=s, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    t = r.stdout
    t = t.replace("ALGORITHMPLACEHOLDER", "\n" + ALGO)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() + "\n"

out.mkdir()
files = [("00_abstract.txt", abstract)] + [
    (f"{i+1:02d}_{name.lower().replace(' ', '_')}.txt", sections[name])
    for i, name in enumerate(["Introduction", "Materials and Methods", "Results", "Discussion", "Conclusions"])]
for name, content in files:
    (out / name).write_text(to_plain(content), encoding="utf-8")
    t = (out / name).read_text()
    leftovers = re.findall(r"\\[a-zA-Z]+|\[[a-z]+:[a-z_]+\]|\$", t)
    print(name, len(t.split()), "words", ("LEFTOVER TeX: " + ", ".join(sorted(set(leftovers))[:8])) if leftovers else "clean")
print("wrote", out)
