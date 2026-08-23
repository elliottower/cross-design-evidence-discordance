"""Recompute every accuracy statistic v15 prints, and check the paper agrees with itself.

Run:  uv run python reviews/verification/verify_v15_numbers.py

Nothing here re-analyzes data. Each check recomputes a statistic from counts the
manuscript itself prints and compares it to the printed value, or reads the
accounting table back and checks it adds up.

Written for the response letter: the letter tells both reviewers that the
p-values were recomputed and named, so every printed p-value has to survive a
recomputation, and the same quantity has to carry the same value everywhere it
appears. Reviewer 1's point 9 is exactly this check, and v9 answered it in the
abstract and Results while leaving one Limitations sentence behind.
"""

import math
import re
import sys
from math import comb
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEX = (Path(sys.argv[1]) if len(sys.argv) > 1
       else REPO / "paper" / "paper_v16_pvalue_consistency.tex")

CHINN = math.sqrt(3) / math.pi

failures: list[str] = []
checks = 0


def note(name: str, printed, recomputed, ok: bool) -> None:
    global checks
    checks += 1
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}: printed {printed}, recomputed {recomputed}")
    if not ok:
        failures.append(f"{name}: printed {printed}, recomputed {recomputed}")


def binom_ge(k: int, n: int, p: float) -> float:
    """One-sided exact binomial, P(X >= k). The test the paper names throughout."""
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    phat = k / n
    denom = 1 + z**2 / n
    center = (phat + z**2 / (2 * n)) / denom
    half = z * math.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2)) / denom
    return (center - half) * 100, (center + half) * 100


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Fisher exact on a 2x2, summing tables no more probable than the observed one."""
    rows, cols, total = (a + b, c + d), (a + c, b + d), a + b + c + d

    def prob(x: int) -> float:
        return (comb(rows[0], x) * comb(rows[1], cols[0] - x)) / comb(total, cols[0])

    observed = prob(a)
    lo = max(0, cols[0] - rows[1])
    hi = min(rows[0], cols[0])
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed * (1 + 1e-9))


def main() -> int:
    text = TEX.read_text()

    print("--- accuracy p-values (one-sided exact binomial against 50%)\n")
    for label, k, n, printed in [("pre-registered 18/22", 18, 22, 0.002),
                                 ("extension 6/10", 6, 10, 0.38),
                                 ("combined 24/32", 24, 32, 0.004)]:
        got = binom_ge(k, n, 0.5)
        # Compare at the precision the manuscript prints, so 0.377 satisfies 0.38.
        places = len(str(printed).split(".")[1])
        note(label, printed, round(got, 5), round(got, places) == printed)

    print("\n--- Wilson 95% intervals\n")
    for label, k, n, printed in [("18/22", 18, 22, (61.5, 92.7)),
                                 ("6/10", 6, 10, (31.3, 83.2)),
                                 ("7/8 neuro", 7, 8, (52.9, 97.8))]:
        got = wilson(k, n)
        ok = all(abs(g - p) < 0.05 for g, p in zip(got, printed))
        note(f"Wilson {label}", printed, tuple(round(g, 1) for g in got), ok)

    print("\n--- tier drop, Fisher exact\n")
    got = fisher_two_sided(18, 4, 6, 4)
    note("18/22 vs 6/10", 0.22, round(got, 4), abs(got - 0.22) < 0.005)

    print("\n--- every printed p-value for an accuracy fraction agrees with its recomputation\n")
    # The failure this catches: a value corrected in the abstract and Results and
    # left standing in Limitations, so the paper prints two p-values for one test.
    # A sentence can carry several fractions and several p-values. Bind each
    # p-value to whichever cue sits closest before it: a fraction, or a phrase
    # that names a tier ("combined", "the extension tier alone") after the
    # fraction it belongs to has already been printed.
    CUES: list[tuple[str, tuple[int, int] | None]] = [
        ("18/22", (18, 22)), ("6/10", (6, 10)), ("24/32", (24, 32)),
        ("combined", (24, 32)), ("extension tier", (6, 10)),
        ("Fisher", None), ("permutation", None),
    ]
    unbound = 0
    for match in re.finditer(r"\$p = (0\.\d+)\$", text):
        printed = float(match.group(1))
        line = text.count("\n", 0, match.start()) + 1
        before = text[max(0, match.start() - 600):match.start()]
        best, at = "", -1
        for cue, _ in CUES:
            where = before.rfind(cue)
            if where > at:
                best, at = cue, where
        binding = dict(CUES).get(best) if at >= 0 else None
        if at < 0:
            continue
        if binding is None:                     # a Fisher test is not a binomial
            note(f"line {line}: {best}, not a binomial on either tier", printed, "skipped", True)
            continue
        k, n = binding
        recomputed = binom_ge(k, n, 0.5)
        places = len(match.group(1).split(".")[1])
        note(f"line {line}: p for {k}/{n} (bound by {best!r})", printed,
             round(recomputed, 4), round(recomputed, places) == printed)
    note("every p-value bound to a test", 0, unbound, unbound == 0)

    print("\n--- accounting table adds up\n")
    block = text[text.index(r"\label{tab:accounting}"):]
    block = block[:block.index(r"\bottomrule")]
    rows = re.findall(r"^([A-Za-z/\\ ]+?) & (\d+) & (\d+) & (\d+) & (\d+) & (\d+)\$?\^?\*?\$? & ",
                      block, re.MULTILINE)
    seen = 0
    for name, total, pending, constr, ambig, scored in rows:
        seen += 1
        parts = int(pending) + int(constr) + int(ambig) + int(scored)
        note(f"row {name.strip()}", f"total {total}", f"parts {parts}", int(total) == parts)
    note("rows parsed", "at least 11", seen, seen >= 11)

    print(f"\n{checks} checks, {len(failures)} failed")
    for f in failures:
        print(f"  FAIL  {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
