# Cross-Dataset NIDS Reproducibility Package

Reproducibility repository for the manuscript:

**Cross-Dataset Generalization of Intrusion Detection: Feature Stability and Transfer Across Four Network Benchmarks**

Datasets: UNSW-NB15, CICIDS2017, BoT-IoT, and TON_IoT.

This repository contains the public, license-safe reproducibility materials for software release **v1.0.1**. Raw third-party datasets and restricted derived partitions are not redistributed. Exact checksums, reconstruction metadata, scripts, seeds, and release artifacts are provided so that the analyses can be audited and recreated where source licenses permit.

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

The full release archive contains per-flow prediction artifacts used for paired uncertainty and ROC-AUC diagnostics. Large binary prediction artifacts are distributed as release assets rather than duplicated as ordinary Git objects.

## Archival release

- GitHub release: **v1.0.1**
- Zenodo version DOI: **10.5281/zenodo.23327656**
- Zenodo concept DOI (all versions): **10.5281/zenodo.23327655**

For exact reproducibility, cite the version-specific DOI above.

## Reproducibility scope

The primary cross-dataset benchmark uses five training seeds. Sampling uncertainty and training-seed variability are reported separately.

Some diagnostic controls are intentionally scoped to **XGBoost** and should not be generalized to every classifier family. CORAL conclusions are limited to the tested XGBoost-CORAL configurations.

## Citation

Use the metadata in `CITATION.cff` and cite the archived software release at DOI **10.5281/zenodo.23327656**.
