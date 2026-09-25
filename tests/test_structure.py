"""Tests for structure parsing and DMS mapping."""

import pytest

from ired_88_research_copilot import structure


@pytest.fixture(scope="module")
def crystal() -> structure.PDBStructure:
    """Load the 7OG3 crystal structure once for this module.

    :returns: The parsed crystal structure.
    """
    return structure.load_crystal_structure()


@pytest.fixture(scope="module")
def predicted() -> structure.PDBStructure:
    """Load the ESMFold prediction once for this module.

    :returns: The parsed predicted structure.
    """
    return structure.load_predicted_structure()


def test_crystal_seqres(crystal: structure.PDBStructure):
    """7OG3 SEQRES is 323 residues including the 21-residue tag.

    :param crystal: The parsed crystal structure.
    """
    assert len(crystal.seqres) == 323
    assert crystal.seqres.startswith("MGSSHHHHHHSSGLVPRGSHTNHA")


def test_crystal_observed_residues(crystal: structure.PDBStructure):
    """Chain A resolves 290 residues with no internal gaps.

    :param crystal: The parsed crystal structure.
    """
    nums = crystal.observed_resnums
    assert len(nums) == 290
    assert nums[0] == 12
    assert nums[-1] == 301
    assert nums == list(range(nums[0], nums[-1] + 1))


def test_crystal_numbering_matches_dms(crystal: structure.PDBStructure):
    """ATOM residue names match WT sequence at the same position (12-301).

    7OG3 numbers ATOM records by wild-type protein position, so each
    observed residue's name must equal the WT residue at that position.

    :param crystal: The parsed crystal structure.
    """
    from ired_88_research_copilot import data

    wt = data.load_wildtype_sequence()
    for resnum in crystal.observed_resnums:
        resname, _, _ = crystal.residues[resnum]
        assert structure.THREE_TO_ONE[resname] == wt[resnum - 1]


def test_ligand_present(crystal: structure.PDBStructure):
    """NADP ligand coordinates were captured (named NDP in this deposit).

    :param crystal: The parsed crystal structure.
    """
    assert crystal.ligand_coords.shape[0] >= 90


def test_position_mapping_is_identity():
    """7OG3 numbering equals DMS numbering; the mapping is explicit."""
    assert structure.dms_position_to_resnum(220) == 220
    assert structure.resnum_to_dms_position(220) == 220
    assert structure.DMS_TO_RESNUM_OFFSET == 0


def test_resolved_dms_positions(crystal: structure.PDBStructure):
    """The crystal resolves positions 12-301 and misses both termini.

    :param crystal: The parsed crystal structure.
    """
    resolved = structure.resolved_dms_positions(crystal)
    assert min(resolved) == 12
    assert max(resolved) == 301
    assert 296 in resolved  # A296I, the top DMS hit, is resolved
    assert 303 not in resolved  # C-terminal tail is not
    assert 5 not in resolved  # N-terminal segment is not


def test_site_classes():
    """Distance classes follow the 6/12 Angstrom thresholds."""
    assert structure.site_class(3.0) == "active_site"
    assert structure.site_class(6.0) == "second_shell"
    assert structure.site_class(11.9) == "second_shell"
    assert structure.site_class(30.0) == "distal"
    assert structure.site_class(None) == "unresolved"


def test_min_ligand_distance(crystal: structure.PDBStructure):
    """Distances compute for resolved residues and None for missing ones.

    :param crystal: The parsed crystal structure.
    """
    d220 = structure.min_ligand_distance(crystal, 220)
    assert d220 is not None
    assert d220 > 12.0  # S220 is distal from the NADP cofactor
    assert structure.min_ligand_distance(crystal, 9999) is None


def test_prediction_covers_tail(predicted: structure.PDBStructure):
    """The ESMFold prediction covers all 304 residues incl. the tail.

    :param predicted: The parsed predicted structure.
    """
    nums = predicted.observed_resnums
    assert len(nums) == 304
    assert max(nums) == 304
    bfactors = structure.per_residue_bfactors(predicted)
    assert set(bfactors) == set(nums)
    assert all(0 <= value <= 100 for value in bfactors.values())


def test_ca_rmsd(crystal: structure.PDBStructure, predicted: structure.PDBStructure):
    """Prediction tracks the crystal (global C-alpha RMSD sanity bound).

    :param crystal: The parsed crystal structure.
    :param predicted: The parsed predicted structure.
    """
    rmsd = structure.ca_rmsd(predicted, crystal)
    assert 0.5 < rmsd < 5.0


def test_kabsch_exact_roundtrip():
    """The Kabsch transform recovers arbitrary proper rotations exactly."""
    import numpy as np

    rng = np.random.default_rng(1)
    for _ in range(20):
        pts = rng.normal(size=(30, 3))
        rot, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        if np.linalg.det(rot) < 0:
            rot = -rot
        moved = pts @ rot + rng.normal(size=3) * 10
        rotation = structure.kabsch_transform(moved - moved.mean(0), pts - pts.mean(0))
        aligned = (moved - moved.mean(0)) @ rotation
        rmsd = float(np.sqrt(((aligned - (pts - pts.mean(0))) ** 2).sum(axis=1).mean()))
        assert rmsd < 1e-8
