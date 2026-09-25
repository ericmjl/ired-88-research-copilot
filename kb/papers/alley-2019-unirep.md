---
title: "Unified rational protein engineering with sequence-based deep representation learning"
authors: "Alley, E. C.; Khimulya, G.; Biswas, S.; AlQuraishi, M.; Church, G. M."
year: 2019
doi: 10.1038/s41592-019-0598-1
url: https://doi.org/10.1038/s41592-019-0598-1
tags: [unirep, machine-learning, representations, machine-directed-evolution]
---

## Key claims

- A recurrent neural network trained on ~24 million UniRef50 sequences
  distills proteins into a fixed-length numerical representation (UniRep)
  that is "semantically rich and structurally, evolutionarily and
  biophysically grounded".
- Simple models built on UniRep predict stability of natural and de novo
  proteins and quantitative function of diverse mutants; the paper claims a
  two-order-of-magnitude efficiency improvement in one protein engineering
  task.
- The Low-N engineering idea (small supervised datasets on top of UniRep
  features) originates in this line of work.

## Relevance to the demo questions

- Q3: this is the representation used in the Ma et al. 2021 paper: the team
  reimplemented UniRep in JAX and trained a random forest on top for
  machine-directed evolution.
- Q5: when proposing new variants, the KB says feature-based ML was already
  shown to work here; our demo's KB-grounded shortlist is the cheap,
  transparent baseline to beat.
