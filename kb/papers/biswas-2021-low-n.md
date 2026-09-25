---
title: "Low-N protein engineering with data-efficient deep learning"
authors: "Biswas, S.; Khimulya, G.; Alley, E. C.; Church, G. M."
year: 2021
doi: 10.1038/s41592-021-01100-y
url: https://doi.org/10.1038/s41592-021-01100-y
tags: [low-n, machine-learning, sample-efficiency, machine-directed-evolution]
---

## Key claims

- Demonstrates data-efficient protein engineering: guided exploration of
  sequence space with only tens of supervised measurements (the canonical
  workflow trains on ~24 variants per round), using learned sequence
  representations rather than large labeled datasets.
- The Ma et al. 2021 paper ran a Low-N-style arm on IRED-88: pretending the
  DMS did not exist, training on 24 random DMS mutants, then prioritizing
  24 more. It shifted the activity distribution, though less dramatically
  than the full machine-directed evolution round.

## Relevance to the demo questions

- Q3: explains the "LowN" rows in `data/raw/cs1c02786_si_003.csv`.
- Q5: bounds expectations for how far a small-data loop can move IRED-88's
  activity; relevant if the demo discusses what to do with a fresh enzyme
  and no DMS budget.
