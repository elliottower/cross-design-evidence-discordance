# Analysis code

The four artifacts named in the manuscript's Data Availability Statement, and
what each produces.

| Artifact | Path | Produces |
|---|---|---|
| `classify_families.py` | `analysis/classifier/` | Family classifications and headline accuracy: 18/22 pre-registered, 6/10 blind extension, 24/32 combined |
| `robustness_analyses.py` | `analysis/classifier/` | Threshold sensitivity, leave-one-domain-out, granularity, instrument independence, and the boundary-class provenance of Table 9 |
| `run_sensitivity.py` | `analysis/exclusion_sensitivity/` | The four exclusion scorings and accuracy by MR instrument type |
| `cross_design_classification_all_41_families_v2.csv` | `data/` | 41 families with effect sizes, confidence intervals, gene targets, instrument types, and classifications |

`robustness_analyses.py` imports from `classify_families.py`, so the two must
stay in the same directory.

## Running

```
pip install -r requirements.txt          # scipy, for robustness_analyses.py only
python analysis/classifier/classify_families.py
python analysis/classifier/robustness_analyses.py
python analysis/exclusion_sensitivity/run_sensitivity.py
```

`classify_families.py` and `robustness_analyses.py` carry their inputs inline and
take no arguments. `run_sensitivity.py` reads the classification CSV, looking for
it beside the script first (where the supplement puts it), then in `data/`.

Each script writes its results to a JSON file next to itself.
