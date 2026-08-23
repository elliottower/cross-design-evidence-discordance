"""Build paper_v17_selection_criteria.tex from paper_v16_pvalue_consistency.tex.

Run:  uv run python paper/patches/patch_v17_response_letter_claims.py

Four edits, each one a claim the response letter makes that v16 does not yet
support. A response letter that describes a change the manuscript does not
contain is the one defect a reviewer is guaranteed to find, because checking it
is the first thing a reviewer does.

1. Reviewer 1's point 8 asked for the family-selection criteria as a procedure a
   third party could apply. No rewording satisfies that request, so the procedure
   is written out as a new Methods subsection, with the residual exposure on the
   original 27 families stated rather than argued away.

2. Reviewer 1's point 7 is right that the IGF-1 etiologic evidence concerns
   colorectal cancer while the drug programs treated three other cancers. The
   family is retained -- excluding it would move 24/32 to 24/31 and would need a
   preregistration amendment, since the construct-limited criterion was frozen --
   and the indication mismatch is named where the family is presented.

3. Reviewer 3's point 4 surfaced Sclerostin-Fracture, which scores correct on two
   legs that oppose each other once oriented to sclerostin. v13 said a sign-aware
   rule would predict failure and printed no accuracy figure. The figure is 23/32.

4. CRP and IL-1b-CVD carry identical values on every evidence field, so two of
   the 24 correct classifications are one piece of evidence counted in two
   domains. The paper disclosed instrument sharing in general terms and named a
   different pair as its example.

No headline number moves. 24/32, 18/22 and 6/10 are unchanged; the two
alternative figures are reported as sensitivities beside them.

v16 is not modified.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "paper" / "paper_v16_pvalue_consistency.tex"
DST = REPO / "paper" / "paper_v17_selection_criteria.tex"

SELECTION = r"""\subsection{Family selection}
\label{sec:selection}

Families enter the catalog by the following procedure, applied domain by domain.
(1)~A disease domain is declared before its families are enumerated, and qualifies if
it contains at least one drug class with published drug-target MR or genetic evidence
and at least one unambiguous Phase~III outcome.
(2)~Within a declared domain, a mechanism family qualifies if a published MR or
drug-target genetic estimate exists for the exposure with an effect size and confidence
interval extractable from the source, \emph{and} a Phase~III readout exists for a drug
acting on that mechanism, with approval or non-approval as the recorded outcome.
(3)~A family meeting the first requirement but not the second is recorded as
\emph{pending}; one whose MR instrument and drug act on different molecular entities is
recorded as \emph{construct-limited}; one whose MR estimate reverses with the estimation
method is recorded as \emph{ambiguous}. All three are declared and excluded before drug
outcomes are examined, and all appear in Table~\ref{tab:accounting}.
(4)~Every family satisfying (2) is scored, and none is dropped once its outcome is known.

The extension domains were declared under this procedure in two blind preregistration
amendments, each frozen before effect sizes were retrieved (Amendment~1, commit
\texttt{1f300a9}; Amendment~2, commit \texttt{12ea0ed}). The author selected extension
families with access to the framework rules and the existing domain coverage, and
without access to classifier code, accuracy statistics, or prior classification results.
The original 27 families were assembled from well-known development programs before the
procedure was written down, and selection influenced by knowledge of outcomes cannot be
excluded for that set (\S\ref{sec:limitations}).

"""

EDITS: list[tuple[str, str, str]] = [
    (
        "Methods: family-selection criteria as a reproducible procedure (Reviewer 1, point 8)",
        "\\subsection{Evidence classification: etiologic versus interventional}",
        SELECTION + "\\subsection{Evidence classification: etiologic versus interventional}",
    ),
    (
        "Oncology, IGF-1: the indication mismatch named where the family is presented "
        "(Reviewer 1, point 7)",
        "This parallels the amyloid translation gap: a mechanism can be etiologically "
        "valid and therapeutically insufficient.",
        "This parallels the amyloid translation gap: a mechanism can be etiologically "
        "valid and therapeutically insufficient. The two legs also concern different "
        "indications: the MR estimate is for colorectal cancer risk, while the "
        "Phase~III programs treated non-small-cell lung cancer, Ewing sarcoma, and "
        "pancreatic cancer. Indication mismatch is a second boundary condition in this "
        "family alongside the translation gap, and either alone would be sufficient to "
        "produce the miss.",
    ),
    (
        "Musculoskeletal, sclerostin: the accuracy a sign-aware rule would give "
        "(Reviewer 3, point 4)",
        "A sign-aware rule would classify this family as qualitatively discordant and "
        "predict failure, which romosozumab's approval would contradict.",
        "A sign-aware rule would classify this family as qualitatively discordant and "
        "predict failure, which romosozumab's approval would contradict; scored that "
        "way, overall accuracy would be 23/32 (71.9\\%).",
    ),
    (
        "Robustness, instrument independence: the two families carrying identical evidence",
        "The ten domains are not fully independent evidence sets.",
        "The ten domains are not fully independent evidence sets. Two families go "
        "further than sharing an instrument: CRP (cardiometabolic) and IL-1$\\beta$-CVD "
        "(autoimmune) carry identical values on every evidence field---"
        "$d_{\\text{OBS}} = 0.174$, MR OR~1.00, $d_{\\text{MR}} = 0.000$, null MR, "
        "qualitative discordance, predicted failure, scored correct---and differ only in "
        "domain, gene target, instrument label, and drug outcome. Two of the 24 correct "
        "classifications are therefore one piece of evidence counted in two domains; "
        "merging the families gives 23/31 (74.2\\%). The permutation test and the "
        "cross-domain comparison treat families as distinct observations, which these "
        "two are not. IL-1$\\beta$-CVD also carries an MR odds ratio of 1.00 with no "
        "confidence interval and no cited MR source, so criterion~(a) of the "
        "two-criterion rule cannot be evaluated from its stored inputs; the "
        "classification is unaffected, since $d = 0$ is null under criterion~(b) either "
        "way.",
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

    # Every denominator the paper reports must survive unchanged. The two
    # alternative figures are sensitivities printed beside them, not replacements.
    for denominator in ("24/32", "18/22", "6/10", "41 mechanism families",
                        "27 mechanism families"):
        assert denominator in text, f"{denominator} lost"
    assert text.count("23/32") == 1, "the sign-aware figure should appear exactly once"
    assert text.count("$p = 0.17$") == 0, "the superseded p-value reappeared"
    assert text.count("\\label{sec:selection}") == 1, "duplicate selection label"

    DST.write_text(text)
    print(f"\n{len(EDITS)} edits applied.\nwrote {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
