#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Predict the BacRedAm structure with the public ESM Fold API.

BacRedAm is the metagenomic bacterial reductive aminase in Aleku et al.
2024, Table S1 (DOI 10.1016/j.checat.2024.101160), GenBank PZN88780.1.
NCBI titles that record with the source annotation
"6-phosphogluconate dehydrogenase". AlphaFold DB has no model for this
accession, and no experimental structure is deposited.

The script writes ``data/external/bacredam.fasta`` and posts the sequence
to the ESM Metagenomic Atlas folding endpoint. The PDB B-factor column
holds per-residue pLDDT divided by 100.

Run from the repo root:

    uv run scripts/predict_bacredam_esmfold.py
"""

import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FASTA = HERE / "data" / "external" / "bacredam.fasta"
OUT = HERE / "data" / "external" / "bacredam_esmfold.pdb"
ENDPOINT = "https://api.esmatlas.com/foldSequence/v1/pdb"

#: 307-residue BacRedAm sequence, GenBank PZN88780.1.
BACREDAM_SEQUENCE = (
    "MREPIVSAHTERAVESRGADRGSAVTVIGLGSMGSALAGAVLEAGYPTTVWNRTAGKAEPLVRRGAARAA"
    "TVAEAVSASPTVIACVLDYRALREILSTAGDALAGRTVVNLTNGTPTEARETAAWVEGHGARYLDGGIMA"
    "VPEMIGGAESLVLYSGSAEAFETVEPVLRRFGSAMYLGADPGLASLHDLALLAGMYGLFAGFLHAVALVG"
    "TEGVRATEFTSSLLIPWLQAMTATLPEAAAQIDAGDYAATGSRLDMQAVALANIVEASRSQGIRPDLMLP"
    "IQALVERRVAKGGGGEDIAAVVEEVRG"
)


def main() -> None:
    """Write the BacRedAm sequence and save its ESMFold prediction."""
    FASTA.parent.mkdir(parents=True, exist_ok=True)
    FASTA.write_text(f">PZN88780.1 BacRedAm\n{BACREDAM_SEQUENCE}\n")

    request = urllib.request.Request(
        ENDPOINT,
        data=BACREDAM_SEQUENCE.encode(),
        headers={"Content-Type": "text/plain"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        pdb_text = response.read().decode()

    OUT.write_text(pdb_text)
    n_atoms = sum(1 for line in pdb_text.splitlines() if line.startswith("ATOM"))
    print(f"Wrote {OUT} ({n_atoms} ATOM records, {len(BACREDAM_SEQUENCE)} residues)")


if __name__ == "__main__":
    main()
