# Publication gate — cross-dataset NIDS research (2026-11-06)

**Status:** locally validated public release candidate, NOT yet GitHub-published, DOI NOT issued.

## Reverified in a clean extraction on 2026-11-06

- 320 individual private NPZ SHA-256 checks: pass (private bundle separately stored; never upload it to the public repository).
- 16 Figure 2 five-seed paired stratified bootstrap rows: exact CSV byte comparison passed (2,000 resamples; seed 20261105).
- 48 external model/source/target intervals: exact CSV byte comparison passed (20,000 resamples; seed 20261105).
- Nominal intervals below BA 50%: 25/48; Bonferroni-adjusted: 24/48.
- Public ZIP has no NPZ, NPY, parquet, joblib, pickle, or private key entries.

## Canonical SHA-256 checker

Use `python verify_current_release.py`, which verifies the single manifest `SHA256_CURRENT_RELEASE.csv`. The older SHA256SUMS.txt and prior dated manifests are **retained as historical snapshots**; they may not match the current edited main.tex.

## Rebuild from private predictions (never publish the private archive)

```bash
python verify_320_prediction_hashes.py --private /local/private_predictions
python supplementary/P3_OBS2_Figure2_Rebuilt_5Seed_2026-11-05/paired_five_seed_bootstrap.py --private /local/private_predictions --archive supplementary/P3_OBS2_full_320_evaluations.csv --out /tmp/fig2 --replicates 2000 --rng-seed 20261105
python verify_48_model_cis_portable.py --private /local/private_predictions --output /tmp/48.csv --replicates 20000 --rng-seed 20261105
```

## Scientific release boundaries

- Newly specified flow-bootstrap intervals, not exact historical RNG draw streams. Conditional on observed test flows and five fitted seeds; not host/session cluster-robust.
- LODO and undersampling were independently rerun but not bitwise historical reproductions.
- Historical supplementary scripts with hard-coded local paths are archived for provenance, not guaranteed clean-environment entrypoints.
- Confirm article authorship/affiliations, dataset licenses, and artifact publication scope with the authors before public deposit.

## Next deployment actions

1. Review the 96-page paper and public ZIP.
2. Commit reviewed public files on a new versioned branch; avoid rewriting `v1.0.1`.
3. Freeze a new tag and release, verify the exact public ZIP SHA-256 on the release asset.
4. Deposit the immutable public bundle in Zenodo or a comparable archive and record the DOI actually issued.
