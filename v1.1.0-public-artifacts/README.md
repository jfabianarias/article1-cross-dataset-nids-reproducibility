# NIDS v1.1.0 public verification artifacts

This directory accompanies the review branch for reproducibility of the NIDS manuscript.

## Contents
- `scripts/`: validation and bootstrap scripts (some expect private datasets/predictions in a locally supplied directory).
- `results/`: verified numerical CSV outputs.
- `figures/`: rebuilt vector Figure 2.
- `provenance/`: hashes, execution metadata, and validation records.
- `docs/`: methodological documentation.

**Do not commit** the 320 private NPZ predictions, harmonized dataset partitions, or the private prediction ZIP. Historical supplementary scripts elsewhere in the full Overleaf project may contain absolute local paths.

This folder is supplemental and does not by itself represent the complete manuscript or the final release attachment. The standalone Overleaf ZIP is intended as a release asset, not to be committed as a ZIP to the Git tree.

The previous version DOI (10.5281/zenodo.23327656) is NOT the v1.1.0 DOI.

## Local validation

From this directory, run `python scripts/verify_current_release.py`. This checks the 20 listed public artifacts against `SHA256SUMS.txt` and flags private binary files. The verifier does not require the separate private prediction archive.
