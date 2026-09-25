"""Tests for data loading utilities."""

import pandas as pd
import pytest

from ired_88_research_copilot import data


@pytest.fixture(scope="module")
def si002() -> pd.DataFrame:
    """Load the activity table once for this module.

    :returns: The SI-002 activities DataFrame.
    """
    return data.load_si002()


def test_si002_shape(si002: pd.DataFrame):
    """SI-002 has the expected columns and single-mutant count.

    :param si002: The SI-002 activities DataFrame.
    """
    assert set(
        ["mutation", "mean", "alpha", "date", "hash", "ratio", "count", "beta"]
    ) <= set(si002.columns)
    singles = data.extract_single_mutants(si002)
    assert len(singles) == 4720
    assert singles["pos"].min() == 2
    assert singles["pos"].max() == 304
    assert singles["pos"].nunique() == 302


def test_si003_experiments():
    """SI-003 carries the expected experiment strategy labels."""
    si003 = data.load_si003()
    expected = {"DMS", "EPPCR1", "EPPCR2", "EPPCR3", "ML", "SGM", "LowN", "FragLib"}
    assert set(si003["experiment"].unique()) == expected


def test_wildtype_sequence():
    """The wild-type sequence is 304 residues with no gaps."""
    wt = data.load_wildtype_sequence()
    assert len(wt) == 304
    assert set(wt) <= set("ACDEFGHIKLMNPQRSTVWY")


def test_summarize_by_position(si002: pd.DataFrame):
    """Per-position summary has one row per measured position.

    :param si002: The SI-002 activities DataFrame.
    """
    singles = data.extract_single_mutants(si002)
    by_position = data.summarize_by_position(singles)
    assert by_position.index.name == "pos"
    assert len(by_position) == singles["pos"].nunique()
    assert (by_position["n_mutants"] > 0).all()
