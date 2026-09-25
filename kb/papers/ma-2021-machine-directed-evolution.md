---
title: "Machine-Directed Evolution of an Imine Reductase for Activity and Stereoselectivity"
authors: "Ma, E. J.; Siirola, E.; Moore, C.; Kummer, A.; Stoeckli, M.; Faller, M.; et al."
year: 2021
doi: 10.1021/acscatal.1c02786
url: https://pubs.acs.org/doi/abs/10.1021/acscatal.1c02786
tags: [ired-88, dms, machine-directed-evolution, anchor-paper, structure]
---

The anchor paper for this repo. Everything in `data/raw/` comes from its
supporting information; the crystal structure in `data/external/7OG3.pdb`
(PDB 7OG3, 1.90 A) was deposited with it.

## Key claims

- IRED-88 is a "kinda middling" imine reductase used to compare traditional
  directed evolution against machine-learning-guided evolution
  ("machine-directed evolution") on two axes: substrate conversion and
  (R)-enantioselectivity. The reaction makes the H4 receptor antagonist
  ZPL389; the final variant achieved full conversion, >99% ee (R), 72% yield
  at gram scale.
- A deep mutational scan (DMS) covered ~81% of the ~6000+ possible single
  mutants; activity was measured for these, and enantioselectivity for a
  subset of high-activity mutants.
- Within one cycle, machine-directed evolution produced a library with a
  dramatically shifted activity distribution compared to traditional
  directed evolution.
- Structure-guided analysis showed that **linear additivity** of mutation
  effects can explain why combining mutations works, especially for distal
  positions; additivity is harder to predict for active-site mutations.
- Mapping DMS positions onto the crystal structure revealed that part of the
  N- and C-termini are absent from the solved structure, yet C-terminal
  mutations were beneficial. A DMS can therefore surface good mutants that
  a structure alone would never suggest.
- Sequence representations came from UniRep (reimplemented in JAX) with a
  random forest on top; a Low-N-inspired arm trained on only 24 variants.

## Relevance to the demo questions

- Q1-Q2: the DMS table (SI-002) and ee table (SI-003) are the raw material.
- Q2: residue-level mapping to 7OG3 + NADP distance classification.
- Q4: the unresolved C-terminal tail (positions 283-304) is exactly where
  the structure is blind and the DMS still has signal.
- Q5: the paper's winning variant Q194L/S220T/H230Y came from epPCR on the
  S220T backbone; ML+structure-guided variants included M129L/A156S/Y177W.

## First-person summary

Eric's layman's summary (written 2021-09-12):
<https://ericmjl.github.io/blog/2021/9/12/machine-directed-evolution/>
