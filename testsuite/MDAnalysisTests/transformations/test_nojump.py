###

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

import MDAnalysis as mda
from MDAnalysis.transformations import NoJump
from MDAnalysisTests import datafiles as data


@pytest.fixture()
def nojump_universes():
    """
    Create the universe objects for the tests.
    """
    u = mda.Universe(data.PSF_TRICLINIC, data.DCD_TRICLINIC)
    transformation = NoJump()
    u.trajectory.add_transformations(transformation)
    return u


@pytest.fixture()
def nojump_universes_nocheck():
    """
    Create the universe objects for the tests.
    Do not check for continunity
    """
    u = mda.Universe(data.PSF_TRICLINIC, data.DCD_TRICLINIC)
    transformation = NoJump(check_continuity=False)
    u.trajectory.add_transformations(transformation)
    return u


def test_nojump_fwd(nojump_universes):
    """
    Test if the nojump transform is returning the correct
    values when iterating forwards over the sample trajectory.
    """
    # These were determined based on determining what the TRICLINIC system
    # would return on a validated version that worked on triclinic and
    # orthogonal systems for a small water trajectory.
    # These are specific to atoms 166 and 362, which moved the most in the
    # trajectory.
    ref_matrix_fwd1 = np.asarray([-3.42261, 11.28495, -1.37211])
    ref_matrix_fwd2 = np.asarray([3.674243, -8.725193, -0.07884017])
    size = (
        nojump_universes.trajectory.ts.positions.shape[0],
        nojump_universes.trajectory.ts.positions.shape[1],
        len(nojump_universes.trajectory),
    )
    parr = np.empty(size)
    for ts in nojump_universes.trajectory:
        parr[..., ts.frame] = ts.positions.copy()
    # Atoms 166 and 362 happen to move alot.
    assert_array_almost_equal(ref_matrix_fwd1, parr[166, :, -1], decimal=5)
    assert_array_almost_equal(ref_matrix_fwd2, parr[362, :, -1], decimal=5)
