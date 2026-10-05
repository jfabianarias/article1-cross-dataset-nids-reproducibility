# Dataset licences and redistribution status

This repository uses four third-party cybersecurity datasets. The terms below were checked against the official provider pages on 2026-10-05.

| Dataset | Provider terms | Commercial use | Public redistribution of processed partitions |
|---|---|---|---|
| UNSW-NB15 | Provider-specific copyright grant: free use for academic research purposes in perpetuity; required dataset-paper citations. The authors assert copyright. | Requires agreement with the authors. | **Not explicitly authorised by the published terms.** This repository therefore does not publicly redistribute derived processed partitions without separate written permission. |
| BoT-IoT | Provider-specific copyright grant: free use for academic research purposes in perpetuity; required dataset-paper citations. The authors assert copyright. | Requires agreement with the authors. | **Not explicitly authorised by the published terms.** This repository therefore does not publicly redistribute derived processed partitions without separate written permission. |
| TON_IoT | Provider-specific copyright grant: free use for academic research purposes in perpetuity; required dataset-paper citations. The author asserts copyright. | Permitted only after asking the author. | **Not explicitly authorised by the published terms.** This repository therefore does not publicly redistribute derived processed partitions without separate written permission. |
| CICIDS2017 | Canadian Institute for Cybersecurity (UNB) dataset terms. CIC states that its datasets may be redistributed, republished, and mirrored in any form, provided the dataset and listed research paper are cited. | CIC states the same citation condition for commercial use/redistribution. | **Yes, explicitly permitted with citation.** |

## Official sources

- UNSW-NB15: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- BoT-IoT: https://research.unsw.edu.au/projects/bot-iot-dataset
- TON_IoT: https://research.unsw.edu.au/projects/toniot-datasets
- CICIDS2017 dataset page: https://www.unb.ca/cic/datasets/ids-2017.html
- CIC dataset licensing FAQ: https://www.unb.ca/cic/datasets/

## Release policy used here

The public GitHub repository contains analysis code, feature-mapping specifications, experiment metadata, exact machine-readable result summaries, seeds, environment information, and audit files. It does **not** publish the derived UNSW-NB15, BoT-IoT, or TON_IoT processed partitions because the provider pages grant academic use but do not explicitly grant redistribution.

The internally validated S1 archive used during manuscript QA contained the exact processed partitions in order to verify clean-start execution. That internal validation fact does not override the upstream dataset terms and should not be interpreted as permission to publish those derived partitions.

Before a Zenodo deposit, either:
1. obtain explicit written redistribution permission from the relevant UNSW dataset authors; or
2. deposit a licence-safe release that excludes those derived partitions and provides acquisition/preprocessing instructions and integrity metadata instead.

This is a conservative compliance interpretation, not legal advice.
