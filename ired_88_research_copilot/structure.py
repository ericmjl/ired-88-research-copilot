"""Structure utilities: PDB parsing and DMS-to-structure position mapping.

The crystal structure is PDB `7OG3 <https://www.rcsb.org/structure/7OG3>`_
(IRED-88, X-ray, 1.90 A, chains A/B, NADP ligands), deposited with the Ma et
al. 2021 ACS Catalysis paper.

Numbering convention
--------------------

7OG3's SEQRES carries a 21-residue N-terminal expression tag
(``MGSSHHHHHHSSGLVPRGSHT``), but the ATOM records are numbered by the
304-residue wild-type protein sequence itself: **ATOM residue number = DMS
position** (validated residue-by-residue, 290/290 match). The crystal
resolves DMS positions 12-301; positions 1-11 (N-terminus) and 302-304
(C-terminal tail) are disordered and absent from the coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from pyprojroot import here

EXTERNAL_DATA_DIR: Path = here() / "data" / "external"

#: Translation table from three-letter to one-letter amino acid codes.
THREE_TO_ONE = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

#: 7OG3 numbers ATOM records by wild-type protein sequence position.
DMS_TO_RESNUM_OFFSET = 0
#: Ligand residue names for NADP in PDB deposits ("NDP" in 7OG3, "NAP" elsewhere).
LIGAND_RESNAMES = ("NAP", "NDP")

#: Maximum distance to the ligand for a residue to count as "active site".
ACTIVE_SITE_MAX_DISTANCE = 6.0
#: Maximum distance to the ligand for a residue to count as "second shell".
SHELL_MAX_DISTANCE = 12.0


@dataclass
class PDBStructure:
    """A minimal parsed representation of a PDB file.

    :param seqres: One-letter SEQRES sequence of chain A.
    :param residues: Mapping of residue number to ``(resname, coords)``
        for chain A ATOM records; ``coords`` is an ``(n_atoms, 4)`` array of
        ``x, y, z, bfactor`` columns.
    :param ligand_coords: ``(n_atoms, 3)`` array of ligand atom coordinates
        (HETATM records whose residue name matches ``LIGAND_RESNAME``).
    """

    seqres: str
    residues: dict[int, tuple[str, np.ndarray, list[str]]] = field(default_factory=dict)
    ligand_coords: np.ndarray = field(default_factory=lambda: np.empty((0, 3)))

    @property
    def observed_resnums(self) -> list[int]:
        """Sorted residue numbers observed in chain A ATOM records.

        :returns: Sorted list of residue numbers with coordinates.
        """
        return sorted(self.residues)


def parse_pdb(path: Path) -> PDBStructure:
    """Parse a PDB file's chain A SEQRES, ATOM and ligand records.

    :param path: Path to a (crystal or predicted) PDB-format file.
    :returns: The parsed :class:`PDBStructure`. B-factors are stored as the
        fourth column of each residue's coordinate array; ESMFold predictions
        encode per-residue pLDDT (0-100) in the B-factor column.
    """
    seqres_codes: list[str] = []
    residues: dict[
        int, tuple[str, list[tuple[float, float, float, float]], list[str]]
    ] = {}
    ligand: list[tuple[float, float, float]] = []

    with open(path) as f:
        for line in f:
            record = line[:6]
            if record == "SEQRES" and line[11] == "A":
                seqres_codes.extend(line[19:70].split())
            elif record.startswith("ATOM") and line[21] == "A":
                resnum = int(line[22:26])
                resname = line[17:20].strip()
                atom_name = line[12:16].strip()
                xyzb = (
                    float(line[30:38]),
                    float(line[38:46]),
                    float(line[46:54]),
                    float(line[60:66]),
                )
                entry = residues.setdefault(resnum, (resname, [], []))
                entry[1].append(xyzb)
                entry[2].append(atom_name)
            elif record == "HETATM" and line[17:20].strip() in LIGAND_RESNAMES:
                ligand.append(
                    (float(line[30:38]), float(line[38:46]), float(line[46:54]))
                )

    residues_parsed = {
        num: (name, np.array(coords), names)
        for num, (name, coords, names) in residues.items()
    }
    return PDBStructure(
        seqres="".join(THREE_TO_ONE.get(code, "X") for code in seqres_codes),
        residues=residues_parsed,
        ligand_coords=np.array(ligand),
    )


def load_crystal_structure() -> PDBStructure:
    """Load the IRED-88 crystal structure (PDB 7OG3) bundled in the repo.

    :returns: Parsed 7OG3 chain A structure with NADP ligand coordinates.
    """
    return parse_pdb(EXTERNAL_DATA_DIR / "7OG3.pdb")


def load_predicted_structure() -> PDBStructure:
    """Load the bundled ESMFold prediction of wild-type IRED-88.

    The prediction covers all 304 residues, including the C-terminal tail
    that the crystal structure does not resolve.

    :returns: Parsed ESMFold-predicted structure.
    """
    return parse_pdb(EXTERNAL_DATA_DIR / "ired88_esmfold.pdb")


def dms_position_to_resnum(position: int) -> int | None:
    """Map a DMS sequence position to its 7OG3 residue number.

    7OG3 numbers ATOM records by wild-type protein position, so this is the
    identity mapping; it exists to keep that convention explicit in one place.

    :param position: DMS position (1-based, in the 304-residue WT numbering).
    :returns: The PDB residue number (equal to the position).
    """
    return position + DMS_TO_RESNUM_OFFSET


def resnum_to_dms_position(resnum: int) -> int | None:
    """Map a 7OG3 residue number back to its DMS sequence position.

    :param resnum: PDB residue number in 7OG3 chain A numbering.
    :returns: The DMS position (equal to the residue number).
    """
    return resnum - DMS_TO_RESNUM_OFFSET


def min_ligand_distance(structure: PDBStructure, resnum: int) -> float | None:
    """Compute the minimum atom distance between a residue and the ligand.

    :param structure: Parsed structure with ligand coordinates.
    :param resnum: Residue number to measure.
    :returns: Minimum distance in Angstrom, or ``None`` if the residue or any
        ligand coordinates are missing.
    """
    if structure.ligand_coords.size == 0 or resnum not in structure.residues:
        return None
    coords = structure.residues[resnum][1][:, :3]  # all atoms of the residue
    deltas = structure.ligand_coords[None, :, :] - coords[:, None, :]
    return float(np.sqrt((deltas**2).sum(axis=-1)).min())


def site_class(distance: float | None) -> str:
    """Classify a residue by its distance to the active-site ligand.

    :param distance: Minimum ligand distance in Angstrom (or ``None``).
    :returns: One of ``"active_site"`` (< 6 A), ``"second_shell"`` (6-12 A),
        ``"distal"`` (> 12 A), or ``"unresolved"`` when the distance is
        unknown.
    """
    if distance is None:
        return "unresolved"
    if distance < ACTIVE_SITE_MAX_DISTANCE:
        return "active_site"
    if distance < SHELL_MAX_DISTANCE:
        return "second_shell"
    return "distal"


def resolved_dms_positions(structure: PDBStructure) -> set[int]:
    """Return the set of DMS positions with coordinates in the structure.

    :param structure: Parsed 7OG3 structure.
    :returns: Set of DMS positions (>= 3) whose residue number is observed.
    """
    return {
        pos
        for resnum in structure.observed_resnums
        if (pos := resnum_to_dms_position(resnum)) is not None
    }


def per_residue_bfactors(structure: PDBStructure) -> dict[int, float]:
    """Compute the mean B-factor per residue.

    For ESMFold-predicted structures the B-factor column carries the
    per-residue pLDDT confidence score (0-100), so this function doubles as
    a confidence extractor for predictions.

    :param structure: Parsed structure.
    :returns: Mapping of residue number to mean B-factor over its atoms.
    """
    return {
        num: float(coords[:, 3].mean())
        for num, (_, coords, _) in structure.residues.items()
    }


def superposed_ca(
    structure_a: PDBStructure,
    structure_b: PDBStructure,
    resnum_offset: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Superpose structure_a onto structure_b and return paired coordinates.

    Pairs residues by number as in :func:`ca_rmsd`.

    :param structure_a: Mobile structure.
    :param structure_b: Target structure.
    :param resnum_offset: Added to structure_a residue numbers to find the
        paired structure_b residue number.
    :returns: ``(ca_a_aligned, ca_b, resnums_a)`` -- the mobile C-alphas in
        the target frame, the target C-alphas, and the mobile residue
        numbers, all ordered consistently.
    :raises ValueError: If the two structures share no residues.
    """
    pairs = [
        (r, r + resnum_offset)
        for r in structure_a.observed_resnums
        if (r + resnum_offset) in set(structure_b.observed_resnums)
    ]
    if not pairs:
        msg = "The two structures share no residues."
        raise ValueError(msg)
    ca_a = np.array([_ca_coord(structure_a, r) for r, _ in pairs])
    ca_b = np.array([_ca_coord(structure_b, t) for _, t in pairs])
    center_a, center_b = ca_a.mean(axis=0), ca_b.mean(axis=0)
    rotation = kabsch_transform(ca_a - center_a, ca_b - center_b)
    return (
        (ca_a - center_a) @ rotation + center_b,
        ca_b,
        np.array([r for r, _ in pairs]),
    )


def _ca_coord(structure: PDBStructure, resnum: int) -> np.ndarray:
    """Return the C-alpha coordinate of a residue.

    :param structure: Parsed structure.
    :param resnum: Residue number.
    :returns: The ``(x, y, z)`` C-alpha coordinate.
    """
    _, coords, names = structure.residues[resnum]
    return coords[names.index("CA"), :3]


def kabsch_transform(mobile: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Compute the rotation aligning mobile coordinates onto target ones.

    Both arrays must already be centered; use :func:`center` first.

    :param mobile: ``(n, 3)`` centered mobile coordinates.
    :param target: ``(n, 3)`` centered target coordinates.
    :returns: The ``(3, 3)`` rotation matrix ``R`` so that ``mobile @ R``
        best matches ``target`` (row-vector convention).
    """
    u, _, vt = np.linalg.svd(mobile.T @ target)
    d = np.sign(np.linalg.det(u @ vt))
    return u @ np.diag([1.0, 1.0, d]) @ vt


def center(coords: np.ndarray) -> np.ndarray:
    """Return coordinates translated to have zero mean.

    :param coords: ``(n, 3)`` coordinate array.
    :returns: Centered coordinates, plus nothing else (mean is subtracted).
    """
    return coords - coords.mean(axis=0)


def ca_rmsd(
    structure_a: PDBStructure,
    structure_b: PDBStructure,
    resnum_offset: int = 0,
) -> float:
    """Compute the C-alpha RMSD between two structures.

    Residues are paired by number: structure_a residue ``r`` is paired with
    structure_b residue ``r + resnum_offset``. 7OG3 and the ESMFold
    prediction share wild-type numbering, so the default offset (0) pairs
    them directly.

    Coordinates are superimposed with the Kabsch algorithm before computing
    the RMSD, so no prior alignment is needed.

    :param structure_a: Mobile structure.
    :param structure_b: Target structure.
    :param resnum_offset: Added to structure_a residue numbers to find the
        paired structure_b residue number.
    :returns: RMSD in Angstrom over common C-alpha atoms.
    :raises ValueError: If the two structures share no residues.
    """
    pairs = [
        (r, r + resnum_offset)
        for r in structure_a.observed_resnums
        if (r + resnum_offset) in set(structure_b.observed_resnums)
    ]
    if not pairs:
        msg = "The two structures share no residues."
        raise ValueError(msg)
    ca_a = np.array([_ca_coord(structure_a, r) for r, _ in pairs])
    ca_b = np.array([_ca_coord(structure_b, t) for _, t in pairs])

    center_a, center_b = ca_a.mean(axis=0), ca_b.mean(axis=0)
    qa, qb = ca_a - center_a, ca_b - center_b
    rotation = kabsch_transform(qa, qb)
    aligned = qa @ rotation
    return float(np.sqrt(((aligned - qb) ** 2).sum(axis=1).mean()))
