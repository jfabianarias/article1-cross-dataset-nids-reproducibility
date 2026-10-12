# Cross-Dataset NIDS Study Artifacts

This directory contains the public, license-safe reproducibility materials for the study:

**Cross-Dataset Generalization of Intrusion Detection: Feature Stability and Transfer Across Four Network Benchmarks**

## Included analyses

- Paired per-flow target resampling for sampling uncertainty.
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

Raw third-party datasets and harmonized NPZ arrays are not redistributed here. See `reproducibility/SHA256_DATA_MANIFEST.csv` for exact input checksums and `processed_data_metadata/` for mappings and partition descriptions.

## Seeds

Primary five-seed benchmark: 42, 52, 62, 72, 82.

## Large prediction artifacts

Per-flow NPZ prediction artifacts used for paired uncertainty are distributed with the GitHub release asset rather than duplicated as ordinary Git objects.

## Scope

Several balancing, representation, LODO, and CORAL controls are XGBoost diagnostics. Conclusions are limited to the configurations actually tested.
