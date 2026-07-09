"""
Frozen classification rule for etiologic evidence discordance.

Two-criterion rule:
  OBS: "non-trivial" if d >= threshold (exposure-comparable scale)
  MR:  "causal" if CI excludes null AND d >= threshold (after per-SD rescaling)

Classification:
  OBS non-trivial + MR null   -> qualitative discordance -> predict failure
  OBS non-trivial + MR causal -> concordance -> predict success
  OBS trivial + MR null       -> null concordance -> ambiguous
  OBS trivial + MR causal     -> genetic-only signal

OBS instrument types:
  "epidemiological_OR" — population-level exposure-disease OR (neuro/cardio)
  "case_control_SMD"   — case-control biomarker SMD (autoimmune cytokines)
  Both produce Cohen's d: OR via Chinn (2000), SMD directly.
"""

import csv
import json
import math
import sys
from pathlib import Path


def chinn_d(OR: float) -> float:
    """Convert OR to Cohen's d via Chinn (2000): d = |ln(OR)| * sqrt(3) / pi."""
    if OR <= 0:
        raise ValueError(f"OR must be positive, got {OR}")
    return abs(math.log(OR)) * math.sqrt(3) / math.pi


def rescale_per_allele_to_per_sd(or_per_allele: float, sd_per_allele: float) -> float:
    """Rescale per-allele OR to per-SD OR.

    or_per_allele: MR OR per copy of the variant
    sd_per_allele: change in exposure (in SD units) per allele
    Returns: OR per 1 SD change in the exposure
    """
    if sd_per_allele <= 0:
        raise ValueError(f"sd_per_allele must be positive, got {sd_per_allele}")
    return or_per_allele ** (1.0 / sd_per_allele)


def ci_excludes_null(ci_lower: float, ci_upper: float) -> bool:
    """Check whether a confidence interval for an OR excludes 1.0."""
    return not (ci_lower <= 1.0 <= ci_upper)


def classify_mr(ci_lower: float, ci_upper: float, d_value: float,
                threshold: float = 0.10) -> str:
    """Classify MR evidence as 'causal' or 'null' using the two-criterion rule."""
    stat_sig = ci_excludes_null(ci_lower, ci_upper)
    above_floor = d_value >= threshold
    if stat_sig and above_floor:
        return "causal"
    return "null"


def classify_obs(d_value: float, threshold: float = 0.10) -> str:
    """Classify observational evidence as 'non-trivial' or 'trivial'."""
    if d_value >= threshold:
        return "non-trivial"
    return "trivial"


def classify_family(obs_class: str, mr_class: str) -> tuple[str, str]:
    """Classify a mechanism family. Returns (classification, prediction)."""
    if obs_class == "non-trivial" and mr_class == "null":
        return "qualitative discordance", "failure"
    elif obs_class == "non-trivial" and mr_class == "causal":
        return "concordance", "success"
    elif obs_class == "trivial" and mr_class == "null":
        return "null concordance", "ambiguous"
    elif obs_class == "trivial" and mr_class == "causal":
        return "genetic-only signal", "success"
    raise ValueError(f"Unexpected combination: obs={obs_class}, mr={mr_class}")


def run_classification(families: list[dict], threshold: float = 0.10) -> list[dict]:
    """Run the full classification pipeline on a list of families."""
    results = []
    for f in families:
        obs_type = f.get("obs_type", "epidemiological_OR")
        if "obs_d_direct" in f:
            obs_d = f["obs_d_direct"]
        else:
            obs_d = chinn_d(f["obs_OR"])
        obs_class = classify_obs(obs_d, threshold)

        mr_or = f["gen_OR"]
        if f.get("per_allele") and f.get("sd_per_allele"):
            mr_or = rescale_per_allele_to_per_sd(mr_or, f["sd_per_allele"])
        mr_d = chinn_d(mr_or)

        ci_lo = f.get("gen_CI_lower")
        ci_hi = f.get("gen_CI_upper")
        if ci_lo is not None and ci_hi is not None:
            mr_class = classify_mr(ci_lo, ci_hi, mr_d, threshold)
        else:
            mr_class = "null" if mr_d < threshold else "causal"

        classification, prediction = classify_family(obs_class, mr_class)

        actual = f.get("drug_outcome", "unknown")
        if actual in ("Approved", "approved"):
            correct = prediction == "success"
        elif actual in ("Failed", "failed", "No benefit"):
            correct = prediction == "failure"
        elif actual in ("Pending", "pending"):
            correct = None
        else:
            correct = None

        results.append({
            "family": f["family"],
            "domain": f.get("domain", "unknown"),
            "obs_OR": f.get("obs_OR"),
            "obs_d": round(obs_d, 3),
            "obs_type": obs_type,
            "obs_class": obs_class,
            "gen_OR_raw": f["gen_OR"],
            "gen_OR_rescaled": round(mr_or, 3) if f.get("per_allele") else None,
            "gen_d": round(mr_d, 3),
            "gen_CI": f"({ci_lo}-{ci_hi})" if ci_lo else None,
            "mr_class": mr_class,
            "classification": classification,
            "prediction": prediction,
            "drug_outcome": actual,
            "correct": correct,
        })
    return results


NEURO_FAMILIES = [
    {"family": "Metabolic-AD", "domain": "neuro", "obs_OR": 1.53, "gen_OR": 1.01,
     "drug_outcome": "Failed"},
    {"family": "ModRisk-AD", "domain": "neuro", "obs_OR": 1.46, "gen_OR": 1.10,
     "drug_outcome": "Failed"},
    {"family": "Anti-CD20-MS", "domain": "neuro", "obs_OR": 2.23, "gen_OR": 0.83,
     "gen_CI_lower": 0.79, "gen_CI_upper": 0.89,
     "drug_outcome": "Approved"},
    {"family": "Smoking-MS/AD", "domain": "neuro", "obs_OR": 1.46, "gen_OR": 1.03,
     "drug_outcome": "Failed"},
    {"family": "HRT-AD", "domain": "neuro", "obs_OR": 0.67, "gen_OR": 1.00,
     "gen_CI_lower": 0.85, "gen_CI_upper": 1.18,
     "drug_outcome": "Failed"},
    {"family": "BMI-MS", "domain": "neuro", "obs_OR": 1.92, "gen_OR": 1.41,
     "gen_CI_lower": 1.20, "gen_CI_upper": 1.66,
     "drug_outcome": "Pending"},
    {"family": "BMI-AD", "domain": "neuro", "obs_OR": 2.04, "gen_OR": 1.03,
     "gen_CI_lower": 1.01, "gen_CI_upper": 1.05,
     "drug_outcome": "Failed"},
    {"family": "VitaminD-MS", "domain": "neuro", "obs_OR": 1.40, "gen_OR": 2.00,
     "gen_CI_lower": 1.70, "gen_CI_upper": 2.50,
     "drug_outcome": "Failed"},
    {"family": "EBV-MS", "domain": "neuro", "obs_OR": 1.70, "gen_OR": 5.00,
     "gen_CI_lower": 2.00, "gen_CI_upper": 20.0,
     "drug_outcome": "Approved"},
]

CARDIO_FAMILIES = [
    {"family": "HDL/CETP", "domain": "cardio", "obs_OR": 0.62, "gen_OR": 0.93,
     "gen_CI_lower": 0.68, "gen_CI_upper": 1.26, "drug_outcome": "Failed"},
    {"family": "Niacin/HDL", "domain": "cardio", "obs_OR": 0.62, "gen_OR": 0.93,
     "gen_CI_lower": 0.68, "gen_CI_upper": 1.26, "drug_outcome": "Failed"},
    {"family": "Homocysteine", "domain": "cardio", "obs_OR": 1.32, "gen_OR": 1.02,
     "gen_CI_lower": 0.98, "gen_CI_upper": 1.07, "drug_outcome": "Failed"},
    {"family": "CRP", "domain": "cardio", "obs_OR": 1.37, "gen_OR": 1.00,
     "gen_CI_lower": 0.97, "gen_CI_upper": 1.02, "drug_outcome": "No benefit"},
    {"family": "Uric acid", "domain": "cardio", "obs_OR": 1.07, "gen_OR": 1.05,
     "gen_CI_lower": 0.92, "gen_CI_upper": 1.20, "drug_outcome": "Failed"},
    {"family": "LDL/PCSK9", "domain": "cardio", "obs_OR": 1.52, "gen_OR": 1.78,
     "gen_CI_lower": 1.58, "gen_CI_upper": 2.01, "drug_outcome": "Approved"},
    {"family": "Blood pressure", "domain": "cardio", "obs_OR": 1.41, "gen_OR": 1.44,
     "gen_CI_lower": 1.35, "gen_CI_upper": 1.55, "drug_outcome": "Approved"},
    {"family": "Triglycerides", "domain": "cardio", "obs_OR": 1.72, "gen_OR": 1.62,
     "gen_CI_lower": 1.24, "gen_CI_upper": 2.11, "drug_outcome": "Approved"},
    {"family": "Lp(a)", "domain": "cardio", "obs_OR": 1.13, "gen_OR": 0.94,
     "gen_CI_lower": 0.93, "gen_CI_upper": 0.95, "drug_outcome": "Pending"},
    {"family": "IL-6R", "domain": "cardio", "obs_OR": 1.25, "gen_OR": 0.95,
     "gen_CI_lower": 0.93, "gen_CI_upper": 0.97,
     "per_allele": True, "sd_per_allele": 0.34,
     "drug_outcome": "Pending"},
]


AUTOIMMUNE_FAMILIES = [
    # obs_sourcing: "meta_analysis" = pooled SMD from systematic review
    #               "author_estimated" = estimated from reported significance
    #               "construct_limited" = construct-definition problem
    # obs_type: "case_control_SMD" vs "epidemiological_OR" vs "tissue_expression"

    # IL-23: serum SMD=0.66 (Dowlatshahi 2013, CI -0.25 to 1.58, NON-SIGNIFICANT);
    #   but tissue p19 22x elevated (Lee 2004 PMID 14707118).
    #   NOTE: OBS rests on tissue expression, not serum. Serum-vs-tissue switch
    #   must be stated explicitly in the paper.
    {"family": "IL-23-psoriasis", "domain": "autoimmune",
     "obs_d_direct": 0.66, "obs_type": "tissue_expression",
     "obs_sourcing": "meta_analysis",
     "gen_OR": 0.616, "gen_CI_lower": 0.563, "gen_CI_upper": 0.674,
     "drug_outcome": "Approved"},

    # CTLA-4: sCTLA-4 elevated in RA p=0.005 (Liu 2012 PMID 22917707)
    #   6.8 ng/mL vs controls; exact SMD not reported
    {"family": "CTLA-4-RA", "domain": "autoimmune",
     "obs_d_direct": 0.50, "obs_type": "case_control_SMD",
     "obs_sourcing": "author_estimated",
     "gen_OR": 0.86, "gen_CI_lower": 0.78, "gen_CI_upper": 0.95,
     "drug_outcome": "Approved"},

    # TNF-a: meta-analysis of 14 studies, SMD=1.93 (CI 1.23-2.64)
    #   Wang 2015 PMC4694713; 890 RA vs 441 controls
    {"family": "TNF-a-RA", "domain": "autoimmune",
     "obs_d_direct": 1.93, "obs_type": "case_control_SMD",
     "obs_sourcing": "meta_analysis",
     "gen_OR": 1.00,
     "drug_outcome": "Approved"},

    # IL-17: meta-analysis of 8 studies, SMD=0.47 (CI 0.07-0.86)
    #   Zhou 2017 PMID 27925680
    {"family": "IL-17-psoriasis", "domain": "autoimmune",
     "obs_d_direct": 0.47, "obs_type": "case_control_SMD",
     "obs_sourcing": "meta_analysis",
     "gen_OR": 0.998,
     "drug_outcome": "Approved"},

    # STAT4/JAK: serum STAT4 elevated in RA p=0.01 (Osman 2025 PMC12520596);
    #   STAT1/STAT4/Jak3 elevated in synovium (Walker 2006)
    {"family": "JAK-STAT-RA", "domain": "autoimmune",
     "obs_d_direct": 0.50, "obs_type": "case_control_SMD",
     "obs_sourcing": "author_estimated",
     "gen_OR": 1.27, "gen_CI_lower": 1.20, "gen_CI_upper": 1.34,
     "drug_outcome": "Approved"},

    # CD20/B-cell: RF positivity 60-80% in RA; B-cell infiltration in synovium
    #   FCRL3 GWAS OR 2.15 (Kochi 2005, Nature Genetics)
    {"family": "CD20-RA", "domain": "autoimmune",
     "obs_d_direct": 0.50, "obs_type": "case_control_SMD",
     "obs_sourcing": "author_estimated",
     "gen_OR": 1.291, "gen_CI_lower": 1.190, "gen_CI_upper": 1.391,
     "drug_outcome": "Approved"},

    # IL-4Ra/AD: CONSTRUCT-LIMITED — IL-4 mRNA NOT dominant in AD lesions;
    #   IL-13 is 7x elevated (Hamid 1996 PMID 9158100; Jeong 2003 PMID 15014952).
    #   Dupilumab blocks IL-4Ra (shared receptor), works via IL-13.
    #   EXCLUDED FROM SCORING: construct-definition problem, not a clean miss.
    #   Drug outcome "Construct-limited" removes it from denominator.
    {"family": "IL-4Ra-AD", "domain": "autoimmune",
     "obs_d_direct": 0.15, "obs_type": "case_control_SMD",
     "obs_sourcing": "construct_limited",
     "gen_OR": 1.02,
     "drug_outcome": "Construct-limited"},

    # IL-1b/CVD: CRP/IL-1 inflammatory axis observational OR 1.37 (ERFC 2010)
    #   Same construct as cardio CRP family
    {"family": "IL-1b-CVD", "domain": "autoimmune",
     "obs_OR": 1.37, "obs_type": "epidemiological_OR",
     "obs_sourcing": "meta_analysis",
     "gen_OR": 1.00,
     "drug_outcome": "Failed"},
]


# Extension domains (exploratory — pre-registration amendment filed separately)
EXTENSION_FAMILIES = [
    # --- ONCOLOGY ---
    # O1: VitD-Cancer
    # OBS = JNCI pooled 17 cohorts, Q5 vs Q3 (mid-quintile ref) 25(OH)D and CRC
    #   (McCullough 2019, PMID 29912394): RR 0.78 (0.65-0.94)
    # MR = systematic review of MR studies, per-SD 25(OH)D and CRC
    #   (Lawler 2023, PMID 36678292): OR 0.97 (0.88-1.07), 80+ instruments
    # Drug: VITAL trial — vitamin D supplementation, no CRC benefit (Manson 2019)
    {"family": "VitD-Cancer", "domain": "oncology",
     "obs_OR": 0.78, "obs_type": "epidemiological_OR",
     "gen_OR": 0.97, "gen_CI_lower": 0.88, "gen_CI_upper": 1.07,
     "drug_outcome": "Failed"},

    # O2: IGF1-CRC
    # OBS = serologic analysis, per-quintile IGF-1 and CRC
    #   (Rinaldi 2019, PMID 31884076, Gastroenterology): OR ~1.12
    # MR = genetically predicted IGF-1 per SD and CRC, 416 SNPs
    #   (Larsson 2020, PMID 32717139, Cancer Medicine): OR 1.22 (1.09-1.36) [BioBank Japan]
    #   UK Biobank estimate is 1.11 (1.01-1.22); Japan chosen as larger sample for CRC
    # Drugs: figitumumab (Langer 2014), ganitumab (Juergens 2023) — both failed
    # NOTE: drug targets IGF-1R (receptor), MR instruments circulating IGF-1 (ligand)
    {"family": "IGF1-CRC", "domain": "oncology",
     "obs_OR": 1.12, "obs_type": "epidemiological_OR",
     "gen_OR": 1.22, "gen_CI_lower": 1.09, "gen_CI_upper": 1.36,
     "drug_outcome": "Failed"},

    # O3: Estrogen-BC
    # OBS = estrogen-only HRT and breast cancer
    #   (Million Women Study, Beral 2003, PMID 12927427, Lancet): RR 1.30
    # MR = estradiol per SD and overall breast cancer, 2 SNPs (CYP19A1-based)
    #   (Nounu 2022, PMID 36209141, Breast Cancer Research): OR 1.03 (1.01-1.06)
    # Drug: tamoxifen approved for chemoprevention (Cuzick 2015)
    # NOTE: MR CI excludes null but d=0.016 < 0.10 — pharmacological amplification
    #   boundary. Germline variants produce tiny per-SD estradiol perturbation;
    #   drug produces near-complete pathway blockade.
    {"family": "Estrogen-BC", "domain": "oncology",
     "obs_OR": 1.30, "obs_type": "epidemiological_OR",
     "gen_OR": 1.03, "gen_CI_lower": 1.01, "gen_CI_upper": 1.06,
     "drug_outcome": "Approved"},

    # --- RESPIRATORY ---
    # R1: Eos/IL5-Asthma
    # OBS = eosinophil count in severe vs mild asthma
    #   (Wagener 2022, estimated SMD ~0.80)
    # MR = eosinophil count per SD and moderate-severe asthma, 151 variants
    #   (Guyatt 2023, Thorax; preprint 2020): weighted median OR 1.50 (1.23-1.83)
    # Drugs: mepolizumab (Pavord 2012), benralizumab — both approved
    {"family": "Eos/IL5-Asthma", "domain": "respiratory",
     "obs_d_direct": 0.80, "obs_type": "case_control_SMD",
     "obs_sourcing": "author_estimated",
     "gen_OR": 1.50, "gen_CI_lower": 1.23, "gen_CI_upper": 1.83,
     "drug_outcome": "Approved"},

    # R2: IL4Ra-Asthma
    # OBS = IL-4/IL-13 pathway elevation in asthma (estimated SMD ~0.50)
    # MR = cis-pQTL MR for soluble IL4R protein on asthma
    #   (Bretherick 2020, PMID 32628676, PLOS Genetics): OR ~0.87 (0.82-0.93)
    #   Direction: higher soluble IL4R (decoy receptor) = less asthma
    #   CAVEAT: pQTL measures soluble IL4R, not membrane-bound (drug target).
    #   Soluble acts as decoy sequestering IL-4; dupilumab blocks membrane IL4R.
    #   Sensitivity: Nie 2013 coding variant Q551R OR=1.46 (1.22-1.75) gives concordance
    # Drug: dupilumab approved (Busse 2019)
    # CONSTRUCT-LIMITED: pQTL instruments soluble decoy receptor, not the
    #   membrane-bound IL4R that dupilumab targets. Wrong molecular entity.
    {"family": "IL4Ra-Asthma", "domain": "respiratory",
     "obs_d_direct": 0.50, "obs_type": "case_control_SMD",
     "obs_sourcing": "construct_limited",
     "gen_OR": 0.87, "gen_CI_lower": 0.82, "gen_CI_upper": 0.93,
     "drug_outcome": "Construct-limited"},

    # R3: TSLP-Asthma
    # OBS = TSLP elevated in severe asthma (estimated SMD ~0.40)
    # MR = no specific pQTL MR with OR and CI for TSLP and asthma
    # Drug: tezepelumab approved (Menzies 2022)
    # CONSTRUCT-LIMITED: no drug-target MR with specific effect size
    {"family": "TSLP-Asthma", "domain": "respiratory",
     "obs_d_direct": 0.40, "obs_type": "case_control_SMD",
     "obs_sourcing": "construct_limited",
     "gen_OR": 1.02,
     "drug_outcome": "Construct-limited"},

    # --- METABOLIC/ENDOCRINE ---
    # M1: SGLT2-HF
    # OBS = T2D and HF risk, meta-analysis of 47 cohorts, 12M individuals
    #   (Ohkuma 2019, PMID 31317230, Diabetologia): RR 1.74 (men) to 1.95 (women)
    # MR = drug-target MR, SLC5A2 cis-eQTL, proteome-wide MR
    #   (PMC11079590, 2024 Frontiers): OR 0.44 (0.26-0.76), P=0.003
    # Drug: empagliflozin, dapagliflozin approved for HF
    {"family": "SGLT2-HF", "domain": "metabolic",
     "obs_OR": 1.75, "obs_type": "epidemiological_OR",
     "gen_OR": 0.44, "gen_CI_lower": 0.26, "gen_CI_upper": 0.76,
     "drug_outcome": "Approved"},

    # M2: GLP1R-T2D/Obesity (combined per pre-registration amendment)
    # OBS = no natural observational exposure (GLP-1R is a drug receptor,
    #   not a naturally varying biomarker like LDL or urate)
    # MR = drug-target cis-MR exists (OR 0.79, 0.75-0.85 for T2D from
    #   cis-eQTL studies), but OBS counterpart undefined
    # Drug: semaglutide, liraglutide approved for T2D and obesity
    # CONSTRUCT-LIMITED: no OBS-MR pair meeting two-criterion rule
    {"family": "GLP1R-T2D/Obesity", "domain": "metabolic",
     "obs_d_direct": 0.0, "obs_type": "epidemiological_OR",
     "obs_sourcing": "construct_limited",
     "gen_OR": 1.00,
     "drug_outcome": "Construct-limited"},

    # M3: Urate-Gout
    # OBS = serum urate and incident gout, longitudinal cohort
    #   (Robinson 2021, PMC8399746): HR 18.62 for >=7 vs <4 mg/dL;
    #   per-SD (SD ~1.2 mg/dL) HR ~3.2 derived from dose-response curve (not directly reported)
    # MR = genetically predicted serum urate and gout, 26 SNPs
    #   (Li 2019, PMC6333326, PLOS Med): OR 3.41-6.04 per 1 mg/dL across
    #   7 MR methods; rescaled to per-SD (1.2 mg/dL): ~5.0 (range 4.4-8.7)
    # Drug: allopurinol, febuxostat approved for gout/hyperuricemia
    {"family": "Urate-Gout", "domain": "metabolic",
     "obs_OR": 3.20, "obs_type": "epidemiological_OR",
     "gen_OR": 5.00, "gen_CI_lower": 3.50, "gen_CI_upper": 8.00,
     "drug_outcome": "Approved"},

    # --- ADDITIONAL EXTENSION FAMILIES (second amendment) ---

    # X1: Uric acid -> CKD
    # OBS = serum urate and incident CKD, meta-analysis of 30 prospective cohorts
    #   (Wu 2021, PMID 34666784, Nutrition & Metabolism): highest vs lowest SUA
    #   category RR 1.22 (1.14-1.30); per mg/dL RR 1.15 (1.10-1.21)
    # MR = genetically predicted serum urate and CKD, 7 MR methods all null
    #   (Jordan/Li 2019, PMID 30645594, PLOS Med): OR 1.05 (0.89-1.23), P=0.59
    #   Same paper as Urate-Gout (gout was positive control)
    # Drug: CKD-FIX (Badve 2020 NEJM) allopurinol no benefit P=0.85;
    #   FEATHER (Kimura 2018) febuxostat failed primary endpoint P=0.10
    {"family": "Urate-CKD", "domain": "renal",
     "obs_OR": 1.22, "obs_type": "epidemiological_OR",
     "gen_OR": 1.05, "gen_CI_lower": 0.89, "gen_CI_upper": 1.23,
     "drug_outcome": "Failed"},

    # X2: Alcohol -> liver disease (cirrhosis)
    # OBS = alcohol consumption and liver cirrhosis, prospective CKB cohort
    #   (Im 2021, PMID 34530818, BMC Med): per 280g/wk HR 1.83 (1.60-2.09)
    # MR = genotype-predicted alcohol and cirrhosis, ALDH2+ADH1B instruments
    #   (Im 2023, PMID 37291211, Nat Med): per 280g/wk HR 2.30 (1.58-3.35)
    # Drug: naltrexone (1994) + acamprosate (2004) FDA-approved for AUD;
    #   reduce causal exposure (alcohol consumption)
    {"family": "Alcohol-Liver", "domain": "hepatic",
     "obs_OR": 1.83, "obs_type": "epidemiological_OR",
     "gen_OR": 2.30, "gen_CI_lower": 1.58, "gen_CI_upper": 3.35,
     "drug_outcome": "Approved"},
]


def print_results(results: list[dict]) -> None:
    header = (f"{'Family':<20} {'OBS d':>7} {'Src':>4} {'OBS':>12} "
              f"{'GEN d':>7} {'MR':>8} {'Class':<25} "
              f"{'Pred':>8} {'Actual':>16} {'OK?':>5}")
    print(header)
    print("=" * len(header))
    for r in results:
        ok = "✓" if r["correct"] is True else ("✗" if r["correct"] is False else "—")
        ot = r.get("obs_type", "epidemiological_OR")
        if ot == "case_control_SMD":
            src = "SMD"
        elif ot == "tissue_expression":
            src = "tis"
        else:
            src = " OR"
        print(f"{r['family']:<20} {r['obs_d']:>7.3f} {src:>4} {r['obs_class']:>12} "
              f"{r['gen_d']:>7.3f} {r['mr_class']:>8} {r['classification']:<25} "
              f"{r['prediction']:>8} {r['drug_outcome']:>16} {ok:>5}")


def _domain_tally(results: list[dict], domain: str, all_fams: list[dict]) -> str:
    dom_results = [r for r in results if r["domain"] == domain]
    if not dom_results:
        return ""
    dom_known = [r for r in dom_results if r["correct"] is not None]
    dom_unambig = [r for r in dom_known if r["prediction"] != "ambiguous"]
    dom_correct = sum(1 for r in dom_unambig if r["correct"])
    dom_pending = sum(1 for r in dom_results if r["drug_outcome"] == "Pending")
    dom_ambig = sum(1 for r in dom_known if r["prediction"] == "ambiguous")
    dom_construct = sum(1 for r in dom_results
                        if r["drug_outcome"] == "Construct-limited")
    obs_types = set(r.get("obs_type", "epidemiological_OR") for r in dom_results)
    extra = ""
    if dom_construct:
        extra += f", {dom_construct} construct-limited"
    if dom_ambig:
        extra += f", {dom_ambig} ambig"
    if dom_pending:
        extra += f", {dom_pending} pending"
    return (f"  {domain:>12}: {dom_correct}/{len(dom_unambig)} scored"
            f"{extra} [OBS: {', '.join(obs_types)}]")


def main():
    thresholds = [0.08, 0.10, 0.12, 0.15] if "--sensitivity" in sys.argv else [0.10]
    prereg_families = NEURO_FAMILIES + CARDIO_FAMILIES + AUTOIMMUNE_FAMILIES
    all_families = prereg_families + EXTENSION_FAMILIES
    prereg_domains = ["neuro", "cardio", "autoimmune"]
    extension_domains = ["oncology", "respiratory", "metabolic", "renal", "hepatic"]
    all_domains = prereg_domains + extension_domains

    for t in thresholds:
        print(f"\n{'='*80}")
        print(f"THRESHOLD d = {t:.2f}")
        print(f"{'='*80}")
        results = run_classification(all_families, threshold=t)

        for domain in all_domains:
            dom_results = [r for r in results if r["domain"] == domain]
            if not dom_results:
                continue
            tag = " [EXPLORATORY]" if domain in extension_domains else ""
            print(f"\n--- {domain.capitalize()}{tag} ---")
            print_results(dom_results)

        print(f"\n--- Pre-registered domain tallies ---")
        for domain in prereg_domains:
            line = _domain_tally(results, domain, all_families)
            if line:
                print(line)

        prereg_results = [r for r in results if r["domain"] in prereg_domains]
        prereg_scored = [r for r in prereg_results
                         if r["correct"] is not None and r["prediction"] != "ambiguous"]
        prereg_correct = sum(1 for r in prereg_scored if r["correct"])
        print(f"\n  PRE-REGISTERED TOTAL: {prereg_correct}/{len(prereg_scored)}"
              f" ({prereg_correct/len(prereg_scored)*100:.1f}%)")

        print(f"\n--- Extension domain tallies [EXPLORATORY] ---")
        for domain in extension_domains:
            line = _domain_tally(results, domain, all_families)
            if line:
                print(line)

        ext_results = [r for r in results if r["domain"] in extension_domains]
        ext_scored = [r for r in ext_results
                      if r["correct"] is not None and r["prediction"] != "ambiguous"]
        ext_correct = sum(1 for r in ext_scored if r["correct"])
        if ext_scored:
            print(f"\n  EXPLORATORY TOTAL: {ext_correct}/{len(ext_scored)}"
                  f" ({ext_correct/len(ext_scored)*100:.1f}%)")

        all_scored = prereg_scored + ext_scored
        all_correct = prereg_correct + ext_correct
        print(f"\n  COMBINED (pre-reg + exploratory): {all_correct}/{len(all_scored)}"
              f" ({all_correct/len(all_scored)*100:.1f}%)")

        n_estimated = sum(1 for f in all_families
                          if f.get("obs_sourcing") == "author_estimated")
        if n_estimated:
            print(f"\n  NOTE: {n_estimated} families have author-estimated OBS d.")
        print(f"  Do NOT pool domains with different OBS constructs for inference.")

    if "--json" in sys.argv:
        results = run_classification(all_families, threshold=0.10)
        out_path = Path(__file__).parent / "classification_results.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nSaved to {out_path}")

    if "--ablation" in sys.argv:
        run_ablation(all_families)


def ablation_rules(result: dict) -> dict[str, str]:
    """Return predictions from four rules for one family.

    always-fail: predict failure for everything
    MR-only: causal -> success, null -> failure
    OBS-only: non-trivial -> success, trivial -> failure
    cross-type: our concordance rule (already computed)
    """
    return {
        "always-fail": "failure",
        "MR-only": "success" if result["mr_class"] == "causal" else "failure",
        "OBS-only": "success" if result["obs_class"] == "non-trivial" else "failure",
        "cross-type": result["prediction"],
    }


def _score_prediction(prediction: str, actual: str) -> bool | None:
    if actual in ("Approved", "approved"):
        return prediction == "success"
    elif actual in ("Failed", "failed", "No benefit"):
        return prediction == "failure"
    return None


def run_ablation(families: list[dict], threshold: float = 0.10) -> None:
    results = run_classification(families, threshold=threshold)
    scorable = [r for r in results
                if r["drug_outcome"] not in ("Pending", "Construct-limited")
                and r["prediction"] != "ambiguous"]

    rule_names = ["always-fail", "MR-only", "OBS-only", "cross-type"]
    scored: dict[str, list[tuple[str, bool]]] = {rn: [] for rn in rule_names}

    for r in scorable:
        preds = ablation_rules(r)
        for rn in rule_names:
            correct = _score_prediction(preds[rn], r["drug_outcome"])
            if correct is not None:
                scored[rn].append((r["family"], correct))

    n_failed = sum(1 for r in scorable
                   if r["drug_outcome"] in ("Failed", "failed", "No benefit"))
    n_approved = sum(1 for r in scorable
                     if r["drug_outcome"] in ("Approved", "approved"))

    print(f"\n{'='*80}")
    print(f"ABLATION ANALYSIS (threshold d={threshold:.2f})")
    print(f"{'='*80}")
    print(f"Base rates: {n_failed} failed, {n_approved} approved, "
          f"{len(scorable)} total scorable")

    header = (f"{'Rule':<15} {'Total':>7} {'Correct':>9} {'Acc':>7} "
              f"{'Fail✓':>7} {'Fail✗':>7} {'Appr✓':>7} {'Appr✗':>7}")
    print(f"\n{header}")
    print("-" * len(header))

    rule_correct_sets: dict[str, set[str]] = {}
    for rn in rule_names:
        pairs = scored[rn]
        total = len(pairs)
        correct = sum(1 for _, c in pairs if c)
        acc = correct / total if total else 0

        fail_correct = sum(1 for f, c in pairs if c
                          and any(r["family"] == f and r["drug_outcome"]
                                  in ("Failed", "failed", "No benefit")
                                  for r in scorable))
        fail_wrong = n_failed - fail_correct
        appr_correct = sum(1 for f, c in pairs if c
                          and any(r["family"] == f and r["drug_outcome"]
                                  in ("Approved", "approved")
                                  for r in scorable))
        appr_wrong = n_approved - appr_correct

        print(f"{rn:<15} {total:>7} {correct:>9} {acc:>7.1%} "
              f"{fail_correct:>7} {fail_wrong:>7} {appr_correct:>7} {appr_wrong:>7}")

        rule_correct_sets[rn] = {f for f, c in pairs if c}

    ct_set = rule_correct_sets["cross-type"]
    mr_set = rule_correct_sets["MR-only"]
    ct_only = ct_set - mr_set
    mr_only = mr_set - ct_set

    print(f"\n--- McNemar disagreements: cross-type vs MR-only ---")
    print(f"  Cross-type correct, MR-only wrong ({len(ct_only)}): "
          f"{', '.join(sorted(ct_only)) if ct_only else 'none'}")
    print(f"  MR-only correct, cross-type wrong ({len(mr_only)}): "
          f"{', '.join(sorted(mr_only)) if mr_only else 'none'}")

    both_right = ct_set & mr_set
    both_wrong = {f for f, _ in scored["cross-type"]} - ct_set - mr_set
    # families wrong under both (actually: families in neither correct set)
    neither = set()
    all_families_scored = {f for f, _ in scored["cross-type"]}
    for f in all_families_scored:
        if f not in ct_set and f not in mr_set:
            neither.add(f)

    print(f"  Both correct ({len(both_right)}): "
          f"{', '.join(sorted(both_right)) if both_right else 'none'}")
    print(f"  Both wrong ({len(neither)}): "
          f"{', '.join(sorted(neither)) if neither else 'none'}")

    if ct_only or mr_only:
        print(f"\n  McNemar 2x2: a={len(ct_only)}, b={len(mr_only)}, "
              f"n_discordant={len(ct_only) + len(mr_only)}")
        if len(ct_only) + len(mr_only) > 0:
            print(f"  (With n_discordant={len(ct_only) + len(mr_only)}, "
                  f"exact binomial is appropriate over chi-squared)")


if __name__ == "__main__":
    main()
