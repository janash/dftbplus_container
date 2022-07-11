"""
Tests for MDI-DFTB+
"""

import numpy as np

import mdi
import pytest


def test_get_name(comm):
    # Get the name of the engine
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)

    assert name == "TESTCODE"


def test_get_energy(comm):
    # Get the energy of the system

    mdi.MDI_Send_Command("<ENERGY", comm)
    energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)

    assert pytest.approx(energy) == -3.9879153786890273


def test_get_dimensions(comm):
    # Get periodicity information

    periodic = np.zeros(3, dtype=np.int32)
    mdi.MDI_Send_Command("<DIMENSIONS", comm)
    mdi.MDI_Recv(3, mdi.MDI_INT, comm, buf=periodic)

    expected_periodicity = np.array([2, 2, 2], dtype=np.int32)

    assert np.array_equal(periodic, expected_periodicity)


def test_get_cell(comm):

    latvec = np.zeros(9)

    mdi.MDI_Send_Command("<CELL", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=latvec)

    expected = np.array(
        [
            5.1278583974,
            5.1278583974,
            0,
            0,
            5.1278583974,
            5.1278583974,
            5.1278583974,
            0,
            5.1278583974,
        ]
    )

    assert np.allclose(expected, latvec)

def test_get_origin(comm):

    origin = np.empty(3)

    mdi.MDI_Send_Command("<CELL_DISPL", comm)
    mdi.MDI_Recv(3, mdi.MDI_DOUBLE, comm, buf=origin)

    expected_origin = np.zeros(3)

    assert np.allclose(origin, expected_origin)

def test_get_masses(comm):

    mass = np.zeros(3)

    mdi.MDI_Send_Command("<MASSES", comm)
    mdi.MDI_Recv(3, mdi.MDI_DOUBLE, comm, buf=mass)

    # Expected masses in atomic units
    expected_masses = np.array([29184.44464372, 1837.47159281, 1837.47159281])

    conv = mdi.MDI_Conversion_Factor("atomic_unit_of_mass", "atomic_mass_unit")
    #assert False, conv
    # 0.0005485
    assert np.allclose(mass, expected_masses)

def test_get_coords(comm):

    coords = np.empty(9)

    mdi.MDI_Send_Command("<COORDS", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=coords)

    # These are the coordinates from the input file. They are in angstrom
    expected_coords = np.array([0., -1., 0, 0., 0., 0.783064, 0., 0., -0.783064])

    # convert to units of bohr radius
    expected_coords = 1.88973 * expected_coords

    # check that they are equal
    assert np.allclose(coords, expected_coords)

def test_send_coords(comm):
    # Check setting the coordinates

    # Make up some coordinatse
    new_coords = np.linspace(1, 9, 9)

    # Empty array for retrieving set coordinates
    retrieved_coords = np.empty(9)
    retrieved_force1 = np.empty(9)
    retrieved_force2 = np.empty(9)

    # Get starting forces
    mdi.MDI_Send_Command("<FORCES", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=retrieved_force1)

    # Update the coordiantes
    mdi.MDI_Send_Command(">COORDS", comm)
    mdi.MDI_Send(new_coords, 9, mdi.MDI_DOUBLE, comm)

    # Retrieve the coordinates
    mdi.MDI_Send_Command("<COORDS", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=retrieved_coords)

    # Check that coordinates have been set to new values.
    assert np.allclose(new_coords, retrieved_coords)

    # Check that the forces have been updated.
    mdi.MDI_Send_Command("<FORCES", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=retrieved_force2)

    assert not np.allclose(retrieved_force1, retrieved_force2)

