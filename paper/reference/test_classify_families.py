import math

import pytest

from classify_families import (
    AUTOIMMUNE_FAMILIES,
    CARDIO_FAMILIES,
    NEURO_FAMILIES,
    chinn_d,
    ci_excludes_null,
    classify_family,
    classify_mr,
    classify_obs,
    rescale_per_allele_to_per_sd,
    run_classification,
)


class TestChinnD:
    def test_or_1_gives_zero(self):
        assert chinn_d(1.0) == pytest.approx(0.0)

    def test_known_conversion(self):
        assert chinn_d(2.0) == pytest.approx(abs(math.log(2)) * math.sqrt(3) / math.pi)

    def test_symmetric_around_1(self):
        assert chinn_d(0.5) == pytest.approx(chinn_d(2.0))

    def test_ctla4_or_086_gives_0083(self):
        assert chinn_d(0.86) == pytest.approx(0.083, abs=0.001)

    def test_ctla4_or_091_gives_0052(self):
        assert chinn_d(0.91) == pytest.approx(0.052, abs=0.001)

    def test_ctla4_or_086_below_threshold(self):
        assert chinn_d(0.86) < 0.10

    def test_ctla4_or_091_below_threshold(self):
        assert chinn_d(0.91) < 0.10

    def test_anti_cd20_or_083_above_threshold(self):
        assert chinn_d(0.83) == pytest.approx(0.103, abs=0.001)
        assert chinn_d(0.83) >= 0.10

    def test_negative_or_raises(self):
        with pytest.raises(ValueError):
            chinn_d(-1.0)

    def test_zero_or_raises(self):
        with pytest.raises(ValueError):
            chinn_d(0.0)


class TestCIExcludesNull:
    def test_excludes_when_both_above_1(self):
        assert ci_excludes_null(1.05, 1.20) is True

    def test_excludes_when_both_below_1(self):
        assert ci_excludes_null(0.70, 0.95) is True

    def test_includes_when_spanning_1(self):
        assert ci_excludes_null(0.85, 1.18) is False

    def test_boundary_at_1(self):
        assert ci_excludes_null(1.0, 1.5) is False
        assert ci_excludes_null(0.5, 1.0) is False


class TestClassifyMR:
    def test_causal_requires_both_criteria(self):
        assert classify_mr(1.05, 1.20, d_value=0.15) == "causal"

    def test_null_when_ci_includes_null(self):
        assert classify_mr(0.85, 1.18, d_value=0.15) == "null"

    def test_null_when_d_below_threshold(self):
        assert classify_mr(1.05, 1.20, d_value=0.05) == "null"

    def test_null_when_both_fail(self):
        assert classify_mr(0.85, 1.18, d_value=0.05) == "null"

    def test_ctla4_is_null_at_010(self):
        d = chinn_d(0.86)
        assert classify_mr(0.78, 0.95, d, threshold=0.10) == "null"

    def test_anti_cd20_ms_is_causal_at_010(self):
        d = chinn_d(0.83)
        assert classify_mr(0.79, 0.89, d, threshold=0.10) == "causal"


class TestClassifyObs:
    def test_non_trivial_above_threshold(self):
        assert classify_obs(0.15) == "non-trivial"

    def test_trivial_below_threshold(self):
        assert classify_obs(0.05) == "trivial"

    def test_boundary(self):
        assert classify_obs(0.10) == "non-trivial"
        assert classify_obs(0.099) == "trivial"


class TestClassifyFamily:
    def test_discordance(self):
        assert classify_family("non-trivial", "null") == (
            "qualitative discordance", "failure")

    def test_concordance(self):
        assert classify_family("non-trivial", "causal") == (
            "concordance", "success")

    def test_null_concordance(self):
        assert classify_family("trivial", "null") == (
            "null concordance", "ambiguous")

    def test_genetic_only(self):
        assert classify_family("trivial", "causal") == (
            "genetic-only signal", "success")


class TestRescalePerAllele:
    def test_identity_at_sd_1(self):
        assert rescale_per_allele_to_per_sd(1.5, 1.0) == pytest.approx(1.5)

    def test_amplifies_small_sd(self):
        rescaled = rescale_per_allele_to_per_sd(0.95, 0.34)
        assert rescaled < 0.95

    def test_il6r_rescaling(self):
        rescaled = rescale_per_allele_to_per_sd(0.95, 0.34)
        d = chinn_d(rescaled)
        assert d == pytest.approx(0.083, abs=0.005)

    def test_negative_sd_raises(self):
        with pytest.raises(ValueError):
            rescale_per_allele_to_per_sd(1.5, -0.1)


class TestFullClassification:
    def test_neuro_cardio_all_or_based(self):
        results = run_classification(NEURO_FAMILIES + CARDIO_FAMILIES)
        for r in results:
            assert r["obs_type"] == "epidemiological_OR"

    def test_autoimmune_has_mixed_obs_types(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        obs_types = {r["obs_type"] for r in results}
        assert len(obs_types) > 1

    def test_il4ra_is_construct_limited(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        il4ra = [r for r in results if r["family"] == "IL-4Ra-AD"][0]
        assert il4ra["drug_outcome"] == "Construct-limited"
        assert il4ra["correct"] is None

    def test_il1b_cvd_is_hit(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        il1b = [r for r in results if r["family"] == "IL-1b-CVD"][0]
        assert il1b["prediction"] == "failure"
        assert il1b["drug_outcome"] == "Failed"
        assert il1b["correct"] is True

    def test_neuro_accuracy(self):
        results = run_classification(NEURO_FAMILIES)
        scored = [r for r in results
                  if r["correct"] is not None and r["prediction"] != "ambiguous"]
        correct = sum(1 for r in scored if r["correct"])
        assert correct == 7
        assert len(scored) == 8

    def test_cardio_accuracy(self):
        results = run_classification(CARDIO_FAMILIES)
        scored = [r for r in results
                  if r["correct"] is not None and r["prediction"] != "ambiguous"]
        correct = sum(1 for r in scored if r["correct"])
        assert correct == 7
        assert len(scored) == 7

    def test_autoimmune_accuracy(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        scored = [r for r in results
                  if r["correct"] is not None and r["prediction"] != "ambiguous"]
        correct = sum(1 for r in scored if r["correct"])
        assert correct == 4
        assert len(scored) == 7

    def test_obs_d_direct_bypasses_chinn(self):
        family = [{"family": "test", "obs_d_direct": 0.50,
                   "obs_type": "case_control_SMD", "gen_OR": 1.0,
                   "drug_outcome": "Failed"}]
        results = run_classification(family)
        assert results[0]["obs_d"] == pytest.approx(0.50)

    def test_vitamin_d_is_the_only_neuro_miss(self):
        results = run_classification(NEURO_FAMILIES)
        misses = [r for r in results if r["correct"] is False]
        assert len(misses) == 1
        assert misses[0]["family"] == "VitaminD-MS"

    def test_effector_biologics_all_miss(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        effectors = ["TNF-a-RA", "IL-17-psoriasis", "CTLA-4-RA"]
        for name in effectors:
            r = [x for x in results if x["family"] == name][0]
            assert r["correct"] is False, f"{name} should be a miss"

    def test_risk_encoding_loci_all_hit(self):
        results = run_classification(AUTOIMMUNE_FAMILIES)
        risk_loci = ["IL-23-psoriasis", "JAK-STAT-RA", "CD20-RA"]
        for name in risk_loci:
            r = [x for x in results if x["family"] == name][0]
            assert r["correct"] is True, f"{name} should be a hit"
