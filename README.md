# Cross-Dataset NIDS Reproducibility Package

Supplementary Software S1 for the article **“Cross-Dataset Generalization of Machine-Learning Intrusion Detection Across Heterogeneous Conventional and Internet-of-Things Network Environments”** by Jaime Arias Aguilar and Everton Gomede.

Repository: https://github.com/jfabianarias/article1-cross-dataset-nids-reproducibility

This repository accompanies the manuscript and provides the executable reproducibility material for the final Block 10 / OBS28 analysis. The canonical archive is named `Article1_Supplementary_Code_and_Results.zip`.

## Reproducibility contents

- `scripts/`: path-portable analysis, validation, figure-regeneration, and orchestration scripts.
- `results/`: exact machine-readable outputs used by the manuscript.
- `config/seeds.json`: authoritative seeds and protocol constants.
- `requirements.txt`: pinned Python dependencies.
- `processed_data/`: metadata for the harmonized datasets; the complete canonical ZIP contains the processed `.npz` partitions.
- `audits/`: consistency, seed, figure, bibliographic, and methodological audit files.
- `CITATION.cff`: citation metadata prepared for GitHub/Zenodo.
- `MANIFEST_SHA256.csv`: integrity manifest for the canonical S1 archive.

## Clean-start environment

Validated with **Python 3.13.5**.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Pinned dependencies: NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, XGBoost 3.1.3, SciPy 1.17.0, Matplotlib 3.10.8, and Pillow 12.3.0.

## Fast validation

From the extracted canonical archive:

```bash
python scripts/validate_release.py
python scripts/smoke_test.py
```

Expected final lines:

```text
VALIDATION PASSED
SMOKE TEST PASSED
```

A one-command smoke check is also available:

```bash
python scripts/run_all.py --mode smoke
```

## Full reproduction

```bash
python scripts/run_all.py --mode full
```

Full mode writes fresh outputs under `results/reproduced/` and executes the five-seed benchmark, direct-transfer uncertainty analysis, normalized metrics, feature-stability analysis, LODO control, CORAL-XGBoost control, class-balanced sensitivity analysis, and figure regeneration. It does not overwrite the archived manuscript results.

## Seeds and fixed protocol

Authoritative values are stored in `config/seeds.json`:

- Model seeds: **42, 52, 62, 72, 82**
- Direct-transfer bootstrap RNG seed: **20261004**
- CORAL interval RNG seed: **20261005**
- Bootstrap replicates: **10,000**
- LODO cap: **25,000** training flows from each eligible source domain per seed
- CORAL regularization: **1e-3**

## Final benchmark scope

Datasets: UNSW-NB15, CICIDS2017, BoT-IoT, and TON_IoT.

The primary benchmark preserves source class prevalence and does not use class weighting. Target-derived scaling statistics, target-label feature selection, target threshold tuning, and target-domain refitting are prohibited in the source-only protocol. CORAL is reported separately because it intentionally uses unlabeled target covariates.

## Data note

Raw public datasets are not redistributed. The complete canonical S1 ZIP contains the corrected harmonized processed partitions used for the final experiments. The ZIP is the recommended artifact for exact reproduction and archival deposit.

## DOI / archival status

This repository is prepared for a GitHub release and Zenodo archival deposit. **No DOI is claimed until an actual Zenodo (or equivalent) deposition is completed.** Once assigned, the DOI will be added to this README, `CITATION.cff`, and the manuscript Data and Code Availability section.

## Release status

OBS28 reproducibility audit completed: clean-start instructions, pinned requirements, explicit seed configuration, portable scripts, smoke validation, full orchestration workflow, citation metadata, and integrity checks are included.
