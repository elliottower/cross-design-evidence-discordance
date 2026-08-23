"""Build paper_v15_zeus_readout.tex from paper_v14_resolved_references.tex.

Run:  uv run python paper/patches/patch_v15_zeus_readout.py

ZEUS (NCT05021835) read out on 31 July 2026. Ziltivekimab did not reduce major
adverse cardiovascular events (HR 0.99, 95% CI 0.88--1.11) while producing the
expected reductions in free IL-6 and hsCRP. Source: Novo Nordisk company
announcement, filed with the SEC as a Form 6-K the same day.

The preregistration registered two predictions for this family rather than one,
and named ZEUS as the trial that discriminates between them: at the paper's
d = 0.10 threshold the IL-6R MR signal is null and the registered prediction is
failure; at d = 0.08 it is causal and the registered prediction is success. The
trial failed, so the threshold the paper actually uses is the one the readout
supports.

IL-6R was registered as unscored and stays unscored. Every denominator in the
paper is the one fixed before the readout: 27 families, 22 scored in neuro and
cardio, 32 scored across ten domains, 24/32 correct. Moving a family into the
scored set after seeing its outcome would buy one correct prediction at the cost
of the design, so the readout is recorded as a parenthetical check mark in
Table 2 -- the convention uric acid already uses -- and counted nowhere.

The readout was public three weeks before the reviewer reports arrived, and the
manuscript says so rather than implying the prediction was scored in advance.

The bibliography moves to references_v3_zeus.bib, which is references_v2_resolved
plus the announcement, and with two primes repaired. Crossref deposits the Russian
soft sign in two names of sokolova2013 as U+2032, which pdflatex refuses under
inputenc; the same entry already renders the same sign as a plain apostrophe in
Yur'eva. v14 does not compile for this reason. v14 and its bibliography are not
modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v14_resolved_references.tex"
DST = REPO / "paper" / "paper_v15_zeus_readout.tex"
SRC_BIB = REPO / "paper" / "references_v2_resolved.bib"
DST_BIB = REPO / "paper" / "references_v3_zeus.bib"

ZEUS_ENTRY = """
@misc{novonordisk2026zeus,
  author  = {{Novo Nordisk A/S}},
  title   = {Novo {Nordisk} provides update on the {ZEUS} phase 3 trial in people
             with {ASCVD}, {CKD} and inflammation},
  year    = {2026},
  month   = {7},
  note    = {Company announcement, 31 July 2026. Filed with the U.S. Securities and
             Exchange Commission as a Form 6-K, accession 0001171843-26-005109},
  url     = {https://www.sec.gov/Archives/edgar/data/353278/000117184326005109/f6k_073126.htm},
}
"""

# A prime is not an apostrophe to pdflatex. Both names transliterate the Russian
# soft sign, which the same entry writes as an apostrophe in Yur'eva.
BIB_FIXES: list[tuple[str, str]] = [
    ("Aref\u2032eva", "Aref'eva"),
    ("El\u2032chaninova", "El'chaninova"),
]

EDITS: list[tuple[str, str, str]] = [
    (
        "Bibliography points at the file carrying the ZEUS announcement",
        "\\bibliography{references_v2_resolved}",
        "\\bibliography{references_v3_zeus}",
    ),
    (
        "Ablation setup: exclusion is by status when the scored set was fixed. "
        "IL-6R now has a known outcome, so 'known drug outcomes, excluding pending' "
        "contradicted itself",
        "we compared four classification rules on all scored families (those with known "
        "drug outcomes, excluding pending and construct-limited):",
        "we compared four classification rules on all scored families (those whose drug "
        "outcome was known when the scored set was fixed, excluding pending, "
        "construct-limited, and ambiguous):",
    ),
    (
        "Family accounting: IL-6R is no longer pending",
        "Five are excluded from the scored set: three with pending trial outcomes "
        "(BMI-MS, Lp(a), IL-6R), one construct-limited",
        "Five are excluded from the scored set: two with pending trial outcomes "
        "(BMI-MS, Lp(a)), one whose registered trial read out after the scored set was "
        "fixed (IL-6R, \\S\\ref{par:prospective}), one construct-limited",
    ),
    (
        "Table 2 caption: state the outcome and that it enters no accuracy figure",
        "uric acid is excluded as ambiguous (see text); two families have pending trial "
        "outcomes.}",
        "uric acid is excluded as ambiguous (see text); Lp(a) has a pending trial outcome. "
        "IL-6R was registered as unscored before its trial read out and remains unscored; "
        "the parenthetical check mark records the registered prediction against the "
        "outcome and enters no accuracy figure.}",
    ),
    (
        "Table 2, IL-6R row: Pending becomes Failed, with a parenthetical mark",
        "IL-6R$^\\text{h}$ & 1.25 & 0.95 (0.93--0.97) & Null & \\emph{Pending} & "
        "Qual.\\ disc. & --- \\\\",
        "IL-6R$^\\text{h}$ & 1.25 & 0.95 (0.93--0.97) & Null & Failed & "
        "Qual.\\ disc. & ($\\checkmark$) \\\\",
    ),
    (
        "Footnote h: the readout, both registered branches, and why the family stays unscored",
        "IL-6R has a pending trial outcome and is excluded from the scored set, so this "
        "family enters no reported accuracy figure.",
        "ZEUS read out null on 31 July 2026 (HR 0.99, 95\\%~CI 0.88--1.11; "
        "\\cite{novonordisk2026zeus}), matching the prediction registered at $d = 0.10$ "
        "and contradicting the one registered at $d = 0.08$. The family was registered as "
        "unscored before the readout and remains unscored, so it enters no reported "
        "accuracy figure.",
    ),
    (
        "Cardiometabolic summary: only Lp(a) is still pending",
        "(Uric acid excluded as ambiguous; two families pending)",
        "(Uric acid excluded as ambiguous; Lp(a) pending, IL-6R unscored)",
    ),
    (
        "Label the prospective-predictions paragraph so other sections can point at it",
        "\\paragraph{Prospective predictions.}\nTwo cardiometabolic families have Phase~III "
        "trials approaching readout, and the preregistration fixed a prediction for each "
        "before any readout (frozen rule commit \\texttt{bf7f175}, July 2026).",
        "\\paragraph{Prospective predictions.}\n\\label{par:prospective}\nTwo cardiometabolic "
        "families had Phase~III trials approaching readout when the preregistration fixed a "
        "prediction for each (frozen rule commit \\texttt{bf7f175}, July 2026). One has since "
        "read out.",
    ),
    (
        "ZEUS paragraph: report the readout against the two registered branches",
        "IL-6 pathway inhibition via ziltivekimab (ZEUS, NCT05021835; $n = 6{,}376$; primary "
        "completion June 2026; readout expected Q3 2026) is the registered boundary case, and "
        "two predictions were fixed for it rather than one. The rescaled MR effect is "
        "$d_{\\text{MR}} = 0.083$. At the $d = 0.10$ threshold used throughout this paper the "
        "MR signal is null, the family is qualitatively discordant, and the registered "
        "prediction is failure. At a threshold of $d = 0.08$ the MR signal is causal, the "
        "family is concordant, and the registered prediction is success. ZEUS discriminates "
        "between the two thresholds: a positive trial favors 0.08, a negative trial favors "
        "0.10. A caveat on instrument-target alignment applies under either reading---the MR "
        "instrument uses variants in \\emph{IL6R} while ziltivekimab targets the IL-6 ligand, "
        "so the instrument and the drug act on the same pathway at different nodes.",

        "IL-6 pathway inhibition via ziltivekimab (ZEUS, NCT05021835; $n = 6{,}376$) is the "
        "registered boundary case, and two predictions were fixed for it rather than one. The "
        "rescaled MR effect is $d_{\\text{MR}} = 0.083$. At the $d = 0.10$ threshold used "
        "throughout this paper the MR signal is null, the family is qualitatively discordant, "
        "and the registered prediction is failure. At a threshold of $d = 0.08$ the MR signal "
        "is causal, the family is concordant, and the registered prediction is success. The "
        "registration named ZEUS as the trial that separates the two thresholds: a positive "
        "trial favors 0.08, a negative trial favors 0.10.\n\n"
        "ZEUS read out on 31 July 2026, after the preregistration was frozen and before this "
        "revision was written. Ziltivekimab did not reduce major adverse cardiovascular events "
        "(HR 0.99, 95\\%~CI 0.88--1.11) in people with atherosclerotic cardiovascular disease, "
        "chronic kidney disease and inflammation, while producing the expected reductions in "
        "free IL-6 and high-sensitivity C-reactive protein \\cite{novonordisk2026zeus}. The "
        "drug engaged its target and the clinical endpoint did not move, which is the failure "
        "mode a null MR signal is meant to anticipate. The outcome matches the prediction "
        "registered at $d = 0.10$ and contradicts the prediction registered at $d = 0.08$. "
        "IL-6R was registered as unscored and remains unscored: it enters no accuracy figure, "
        "and every denominator reported here was fixed before the readout. A caveat on "
        "instrument-target alignment applies to the comparison---the MR instrument uses "
        "variants in \\emph{IL6R} while ziltivekimab targets the IL-6 ligand, so the "
        "instrument and the drug act on the same pathway at different nodes.",
    ),
    (
        "Ablation table setup: same exclusion wording as the ablation section",
        "across all 32 scored families (all ten domains with known outcomes, excluding "
        "pending and construct-limited families).",
        "across all 32 scored families (all ten domains, excluding families that were "
        "pending, construct-limited, or ambiguous when the scored set was fixed).",
    ),
    (
        "Threshold sweep: the lower end of the plateau has now been tested out of sample",
        "The $d = 0.10$ threshold is not optimal---it sits at the lower edge of a stable "
        "plateau---but it was chosen a priori on Cohen's grounds and we do not move it.",
        "The $d = 0.10$ threshold is not optimal on the scored set---it sits at the lower "
        "edge of a stable plateau---but it was chosen a priori on Cohen's grounds and we do "
        "not move it. The lower end of that plateau has since been tested out of sample and "
        "was not supported: IL-6R was registered in advance as causal at $d = 0.08$ and null "
        "at $d = 0.10$, and ZEUS failed (\\S\\ref{par:prospective}).",
    ),
    (
        "Limitations, threshold sensitivity: IL-6R is no longer awaiting a readout",
        "IL-6R sits at the same boundary (per-SD rescaled $d_{\\text{MR}} = 0.083$) and is "
        "unscored pending trial readout.",
        "IL-6R sits at the same boundary (per-SD rescaled $d_{\\text{MR}} = 0.083$) and is "
        "unscored; its registered trial failed, which is the outcome $d = 0.10$ predicts and "
        "$d = 0.08$ does not.",
    ),
    (
        "Ascertainment: one of the two prospective tests has resolved",
        "The prospective predictions (Lp(a), IL-6) and pre-registered extensions mitigate "
        "this concern. Prospective validation at trial readout is the definitive test.",
        "The prospective predictions (Lp(a), IL-6) and pre-registered extensions mitigate "
        "this concern. The IL-6 prediction has resolved in the direction registered under "
        "this paper's threshold; Lp(a)HORIZON remains open.",
    ),
]


def main() -> int:
    text = SRC.read_text()
    failures = [(label, text.count(old)) for label, old, _ in EDITS if text.count(old) != 1]
    if failures:
        print("ABORT -- these targets did not match exactly once:\n", file=sys.stderr)
        for label, count in failures:
            print(f"  [{count} matches] {label}", file=sys.stderr)
        return 1
    for label, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"  applied: {label}")

    # Nothing in the paper may still describe the IL-6R outcome as awaited.
    for stale in ("readout expected Q3 2026", "unscored pending trial readout",
                  "two families have pending trial outcomes", "two families pending"):
        assert stale not in text, f"stale pending language survived: {stale!r}"
    # The denominators are the ones fixed before the readout.
    for fixed in ("24/32", "32 scored families", "27 mechanism families"):
        assert fixed in text, f"a pre-readout denominator changed: {fixed!r}"
    assert text.count("novonordisk2026zeus") == 2, "announcement cited twice, once per site"

    bib = SRC_BIB.read_text()
    assert "novonordisk2026zeus" not in bib, "entry already present in the source bibliography"
    for old, new in BIB_FIXES:
        assert bib.count(old) == 1, f"prime repair {old!r} did not match exactly once"
        bib = bib.replace(old, new, 1)
        print(f"  bibliography: {old!r} -> {new!r}")
    bib = bib.rstrip("\n") + "\n" + ZEUS_ENTRY
    assert "\u2032" not in bib, "a prime survived"
    DST_BIB.write_text(bib)
    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.")
    print(f"wrote {DST.relative_to(REPO)}")
    print(f"wrote {DST_BIB.relative_to(REPO)}  (+1 entry; {SRC_BIB.name} unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
