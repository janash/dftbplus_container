"""
Tests for MDI-DFTB+
"""

import numpy as np

import mdi
import pytest

def test_name(comm):
    # Get the name of the engine
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)

    assert name == "TESTCODE"

def test_energy(comm):

    # Get the energy of the system

    mdi.MDI_Send_Command("<ENERGY", comm)
    energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)

    assert pytest.approx(energy) == -3.9879153786890273

def test_dimensions(comm):

    # Retrieve periodicity information
    periodic = np.zeros(3, dtype=np.int32)
    mdi.MDI_Send_Command("<DIMENSIONS", comm)
    mdi.MDI_Recv(3, mdi.MDI_INT, comm, buf=periodic)

    expected_periodicity = np.array([2, 2, 2], dtype=np.int32)

    assert np.array_equal(periodic, expected_periodicity)