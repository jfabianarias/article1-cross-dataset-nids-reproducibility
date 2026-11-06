# Priority 3 / Observation 2 — Independent five-seed flow-bootstrap reproduction

**Date:** 2026-11-05. **Scope:** numerical reproduction and evidence pack, not GitHub publication.

## Verified results
- 80 source-model-seed fits and 320 held-out evaluations were independently regenerated from four frozen harmonized NPZ datasets.
- All **320/320 TN, FP, FN, TP quadruples exactly match** the archived benchmark summaries.
- All 320 private per-flow prediction arrays have aligned target-test positional indices and target labels. Their private SHA-256 manifest is available outside the public project.
- Recalculated 16/16 source-target directions with 2,000 class-stratified nonparametric flow bootstrap resamples, pairing all 20 (four models × five seeds) predictions per target flow within direction.
- 48 external source-target-model cells analyzed using 20,000 paired-flow stratified resamples each: **25/48** nominal 95% and **24/48** two-sided Bonferroni-adjusted intervals lie entirely below BA=50%; new results confirm the counts reported earlier.
- Deterministic rerun of the 16-direction bootstrap CSV produced an exact byte-for-byte match.
- Figure 2 vector PDF regenerated and compiled into the revised **96-page manuscript**.

## Scientific boundary
This is a fresh independently specified five-seed paired bootstrap, not a bitwise rerun of the unavailable historical bootstrap random draw stream or seed-nesting. Source test positions are not physical host/session identifiers. The 95% flow-bootstrap intervals condition on fixed test partitions and fixed models/seeds; they do not account for correlations among flows within network sessions or hosts. Direction-specific intervals do not establish significance of differences between directions. Original LODO/balancing independent reruns have separately documented differences. No persistent DOI or immutable GitHub release is asserted.

## Reproduction
Private dataset input: four harmonized NPZs in a local data folder; private prediction output is never placed into the public Overleaf ZIP. Run `rebuild_predictions.py` on all four sources, four model families and five seeds, then `paired_five_seed_bootstrap.py` on its `private_predictions` directory and `compute_48_model_cis.py` for 48 cells. Exact CLI and input hashes should be recorded for any frozen publication release.

Environment: Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, XGBoost 3.1.3, SciPy 1.17.0, platform Linux-6.18.57-x86_64-with-glibc2.41.
