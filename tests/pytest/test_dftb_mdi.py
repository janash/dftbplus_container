"""
Tests for MDI-DFTB+
"""

import mdi

def test_name(comm):
    # Get the name of the engine
    mdi.MDI_Send_Command("<NAME", comm)
    name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)

    assert name == "TESTCODE"