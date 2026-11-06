# Checklist for publishing v1.1.0

Branch: `release/v1.1.0-review-20261106` (review only, not a version tag).

## Frozen public asset

Filename: `NIDS_Overleaf_Candidato_Publicacao_Validado_2026-11-06.zip`

Size: 6,653,161 bytes

SHA-256: `88bd9470512eda3bc920e8ac8d227024f7abca4f8ca090eb15d7063f8bd851ba`

This archive is an **Overleaf supplementary project**, not a substitute for committing versioned source files into the GitHub repository. Keep the separately retained 320 NPZ prediction archive private.

## Before tagging

- [ ] Review the final manuscript and author order, affiliations, article title and release metadata.
- [ ] Confirm third-party dataset terms and that restricted partitions/predictions are excluded.
- [ ] Add the reviewed public source and supplementary material to the GitHub repository; ensure essential scripts and checksums are committed.
- [ ] Run `python verify_current_release.py` inside the extracted public archive.
- [ ] With the private files available locally, rerun `verify_320_prediction_hashes.py`, the paired five-seed bootstrap, and `verify_48_model_cis_portable.py`; never upload the private inputs.
- [ ] Review README and CITATION.cff: change to version 1.1.0, do **not** assign a version DOI before Zenodo issues it.
- [ ] Verify archive digest on the exact final asset; any edit creates a new SHA-256.

## Tag and DOI

- [ ] Tag the final verified Git commit with `v1.1.0`, preserving `v1.0.1`.
- [ ] Publish GitHub release `v1.1.0`; attach the validated public ZIP as an asset.
- [ ] Confirm the existing Zenodo-GitHub integration archives the *new* version. GitHub release asset handling may differ from the automatically archived Git source snapshot; use a separate Zenodo deposition if essential binary artifacts need to be preserved.
- [ ] Record the newly minted **version-specific** Zenodo DOI and metadata; update manuscript and CITATION.cff in a traceable post-deposit change if necessary.

Previous version DOI: `10.5281/zenodo.23327656`.
Existing concept DOI: `10.5281/zenodo.23327655`.
**Neither should be presented as the new version-specific DOI.**

## Reproducibility limitations that must remain visible

- Five-seed flow-bootstrap intervals were newly specified and verified; exact historical draw-by-draw identity is not claimed.
- Bootstrap does not account for host/session clustering.
- LODO and balancing independent reruns are not bitwise historical replicas.
- Some archived supplementary scripts have hard-coded historical local paths and are not portable.

## Ready-to-publish decision

This branch is ready for review of its notes, not yet ready to tag. The complete reviewed source tree and public archive must be put in their final GitHub/Zenodo destinations and validated there before release.
