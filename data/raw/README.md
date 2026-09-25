# Raw data

CSV exports from the IRED-88 enzyme engineering campaign at Novartis,
published as the supporting information of:

> Ma, E. J.; Siirola, E.; Moore, C.; et al. **Machine-Directed Evolution of
> an Imine Reductase for Activity and Stereoselectivity.** *ACS Catal.* 2021,
> *11* (20), 12433-12445. DOI:
> [10.1021/acscatal.1c02786](https://pubs.acs.org/doi/abs/10.1021/acscatal.1c02786)

Use these files for demos and teaching; cite the paper for any external use
of the raw tables and respect applicable terms from the original study.

## Files

| File | Contents |
|------|----------|
| `cs1c02786_si_002.csv` | Per-mutation activity summaries: `mutation`, `mean` (activity), `alpha`, `beta`, `ratio`, `count` (n measurements), `date`, `hash` (batch fingerprint). 11,305 rows; 4,720 strict single mutants. |
| `cs1c02786_si_003.csv` | Enantioselectivity (R-ee) and conversion (`ratio`) per variant, with the strategy that produced it (`experiment`: DMS, EPPCR1-3, ML, SGM, LowN, FragLib). |
| `ired-master-table.csv` | Row-level variant records: sample id, layout code, plate position, mutation string, full protein sequence, plate code. 33,534 rows; wild-type rows have an empty `mutation`. |
| `layouts.csv` | Plate layout metadata: layout id/code, experiment, plate size. |

## Quick orientation

- Wild-type IRED-88 is 304 residues; single-mutant notation is `A111C`
  (WT residue, 1-based position, mutant residue), positions 2-304, stop
  codons appear as `*`.
- Position 249 is the only position with no single mutants measured.
- The crystallized construct adds a 21-residue N-terminal tag; see
  `ired_88_research_copilot/structure.py` for the DMS-to-PDB mapping.
