#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Predict the IRED-88 structure with the public ESM Fold API.

Sends the wild-type sequence in ``data/external/ired88_wt.fasta`` to the
ESM Metagenomic Atlas folding endpoint and writes the PDB-format prediction
to ``data/external/ired88_esmfold.pdb``. The B-factor column of the output
carries per-residue pLDDT confidence (0-100).

Run from the repo root (no environment needed; the script is self-contained):

    uv run scripts/predict_structure_esmfold.py
"""

import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FASTA = HERE / "data" / "external" / "ired88_wt.fasta"
OUT = HERE / "data" / "external" / "ired88_esmfold.pdb"
ENDPOINT = "https://api.esmatlas.com/foldSequence/v1/pdb"


def main() -> None:
    """Fold the bundled wild-type sequence and save the predicted PDB."""
    lines = FASTA.read_text().splitlines()
    sequence = "".join(line for line in lines if not line.startswith(">"))

    request = urllib.request.Request(
        ENDPOINT,
        data=sequence.encode(),
        headers={"Content-Type": "text/plain"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        pdb_text = response.read().decode()

    OUT.write_text(pdb_text)
    n_atoms = sum(1 for line in pdb_text.splitlines() if line.startswith("ATOM"))
    print(f"Wrote {OUT} ({n_atoms} ATOM records)")


if __name__ == "__main__":
    main()
