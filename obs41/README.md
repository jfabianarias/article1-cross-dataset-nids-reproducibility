# Supplementary Software OBS41

This directory contains the public, license-safe reproducibility materials introduced for the OBS41 manuscript revision.

## Changes relative to OBS40
- Paired per-flow target resampling for the reproducible seed-42 uncertainty analysis.
- Wilson treatment for class-specific boundary rates.
- Continuous-score ROC-AUC diagnostics with explicit score orientation and thresholds.
- Budget-matched LODO controls.
- Class-weighting vs. random undersampling vs. size-matched prevalence controls.
- Representation ablations.
- Source-only model-selection and convergence checks.
- Stricter grouped within-domain partitions.
- Inductive CORAL sensitivity.
- Feature AUC uncertainty and reversal-threshold sensitivity.
- Comparable attack-family sensitivity.

## Data policy
Raw third-party datasets and harmonized NPZ arrays are not redistributed here. See `reproducibility/SHA256_DATA_MANIFEST_OBS41.csv` for exact input checksums and `processed_data_metadata/` for mappings and partition descriptions.

## Seeds
Primary five-seed benchmark: 42, 52, 62, 72, 82.

## Large prediction artifacts
Per-flow NPZ prediction artifacts used for paired uncertainty are distributed with the GitHub release asset rather than duplicated as ordinary Git objects.

## Scope
Several new balancing, representation, LODO, and CORAL controls are XGBoost diagnostics. Conclusions are limited to the configurations actually tested.
