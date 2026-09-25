# External structure data

Bundled structural reference files for the demo.

| File | Contents |
|------|----------|
| `7OG3.pdb` | Crystal structure of wild-type IRED-88 (X-ray, 1.90 A, chains A/B, NADP ligands), deposited with Ma et al. 2021 by M. Faller and E. Koch. Source: <https://www.rcsb.org/structure/7OG3>. |
| `ired88_wt.fasta` | The 304-residue wild-type IRED-88 sequence (DMS numbering, no expression tag). |
| `ired88_esmfold.pdb` | ESMFold prediction of the wild-type sequence (via the public ESM Fold API, <https://esmatlas.com>), all 304 residues including the C-terminal tail missing from the crystal. B-factors hold per-residue pLDDT **divided by 100** (multiply by 100 for the usual 0-100 score). Regenerate with `scripts/predict_structure_esmfold.py`. |

## Numbering

7OG3's SEQRES carries a 21-residue N-terminal expression tag, but the ATOM
records are numbered by the wild-type protein sequence itself:
**PDB residue number = DMS position** (validated residue-by-residue,
290/290 match). The crystal resolves DMS positions 12-301; positions 1-11
(N-terminus) and 302-304 (C-terminal tail) are disordered and absent from
the coordinates. The NADP cofactor appears under residue name `NDP`
(residues 501-502 per chain).
