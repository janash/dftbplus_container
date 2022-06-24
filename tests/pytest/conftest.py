"""
MDI Driver Fixture
"""

import pytest

@pytest.fixture(scope="session")
def comm():
    import mdi
    from mdi import MDI_NAME_LENGTH, MDI_COMMAND_LENGTH
    import subprocess

    cmd = [ 'python', 
            'driver.py', '-mdi' ,
            "-role DRIVER -name driver -method TCP -port 8021"
        ]

    subprocess.run(cmd)

    mdi_index = cmd.index("-mdi")

    try:
        mdi_call = cmd[mdi_index + 1]
    except IndexError:
        raise Exception("Argument to -mdi option not found")

    mdi.MDI_Init(mdi_call)

    communicator = mdi.MDI_Accept_Communicator()

    yield communicator

    mdi.MDI_Send_Command("EXIT", communicator)