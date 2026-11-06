# Cross-Dataset NIDS Reproducibility Package

> **Current archival release: [v1.1.0](https://github.com/jfabianarias/article1-cross-dataset-nids-reproducibility/releases/tag/v1.1.0)** (2026-11-06). **Zenodo version DOI: [10.5281/zenodo.24014711](https://doi.org/10.5281/zenodo.24014711)**. Validated public results, the five-seed Figure 2, verification scripts and SHA-256 manifests are available under [`v1.1.0-public-artifacts/`](v1.1.0-public-artifacts/). To validate the public artifacts, run `cd v1.1.0-public-artifacts && python scripts/verify_current_release.py`. The full Overleaf supplementary ZIP is attached to the release; private per-flow predictions and restricted derived datasets are not public.

Reproducibility repository for the manuscript:

**Cross-Dataset Generalization of Intrusion Detection: Feature Stability and Transfer Across Four Network Benchmarks**

Datasets: UNSW-NB15, CICIDS2017, BoT-IoT, and TON_IoT.

This repository contains the public, license-safe reproducibility materials for software release **v1.1.0**. Raw third-party datasets and restricted derived partitions are not redistributed. Exact checksums, reconstruction metadata, scripts, seeds, and release artifacts are provided so that the analyses can be audited and recreated where source licenses permit.

## Methodological coverage

The release includes:

- paired per-flow target resampling for sampling uncertainty;
- Wilson intervals for class-specific boundary rates;
- external ROC-AUC with explicit score orientation and decision thresholds;
- budget-matched LODO controls;
- class-weighted, undersampled, and size-matched balancing controls;
- source-only model-selection and MLP convergence diagnostics;
- stricter grouped/temporal within-domain partition sensitivity;
- five-base-feature, full 11-feature, and direction-invariant representation ablations;
- inductive CORAL sensitivity with untouched target evaluation;
- feature-by-dataset AUC uncertainty and reversal-threshold sensitivity;
- comparable attack-family sensitivity analyses;
- operational false-alert and prevalence interpretation;
- explicit separation of training-seed variability from target-sample uncertainty.

## Repository structure

- `scripts/`: baseline reproducibility and validation scripts.
- `study_artifacts/scripts/`: scripts supporting the expanded analyses.
- `study_artifacts/processed_data_metadata/`: dataset mapping and partition metadata.
- `study_artifacts/reproducibility/`: environment and checksum manifests.
- `config/`: protocol constants and seeds.
- `requirements.txt`: pinned Python dependencies.
- `DATASET_LICENSES.md`: redistribution policy for the four source datasets.
- `CITATION.cff`: citation metadata for the software release.

## Environment

Validated with Python 3.13.5.

Key versions:
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0
- scikit-learn 1.8.0
- XGBoost 3.1.3
- Matplotlib 3.10.8

Primary model seeds: **42, 52, 62, 72, 82**.

## Data and licensing

The public repository does **not** redistribute the raw datasets. Where exact processed arrays cannot be redistributed, the release provides raw-file checksums, harmonization metadata, sampling and split rules, seeds, reconstruction scripts, and stable machine-readable result tables.

See `DATASET_LICENSES.md` and `study_artifacts/reproducibility/SHA256_DATA_MANIFEST.csv`.

## Prediction artifacts

The 320 per-flow prediction arrays supporting paired uncertainty analyses are retained privately and are **not** included in the public GitHub repository, release asset, or Zenodo record. The public materials include aggregate results, scripts, and SHA-256 provenance manifests; access to licensed source datasets is required for independent full reruns.

## Archival release

- **Latest GitHub release:** [v1.1.0](https://github.com/jfabianarias/article1-cross-dataset-nids-reproducibility/releases/tag/v1.1.0)
- **Zenodo v1.1.0 version DOI:** [10.5281/zenodo.24014711](https://doi.org/10.5281/zenodo.24014711)
- **Zenodo concept DOI (all versions):** [10.5281/zenodo.23327655](https://doi.org/10.5281/zenodo.23327655)
- Previous v1.0.1 version DOI: [10.5281/zenodo.23327656](https://doi.org/10.5281/zenodo.23327656)

For exact reproducibility, cite the version-specific DOI of the version used. These README and CITATION.cff updates were committed **after** the v1.1.0 tag was published, so the archived v1.1.0 source snapshot remains unchanged.

## Reproducibility scope

The primary cross-dataset benchmark uses five training seeds. Sampling uncertainty and training-seed variability are reported separately.

Some diagnostic controls are intentionally scoped to **XGBoost** and should not be generalized to every classifier family. CORAL conclusions are limited to the tested XGBoost-CORAL configurations.

## Citation

Use the metadata in `CITATION.cff` and cite the v1.1.0 archived software release at DOI **10.5281/zenodo.24014711**.
