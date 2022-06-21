import mdi
from mdi import MDI_NAME_LENGTH, MDI_COMMAND_LENGTH
import sys

import numpy as np

iarg = 1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]

    if arg == "-mdi":
        # Initialize MDI
        if len(sys.argv) <= iarg+1:
            raise Exception("Argument to -mdi option not found")
        mdi.MDI_Init(sys.argv[iarg+1])
        iarg += 1
    else:
        raise Exception("Unrecognized argument")

    iarg += 1

# Connect to the engine
comm = mdi.MDI_Accept_Communicator()

# Get the name of the engine
mdi.MDI_Send_Command("<NAME", comm)
name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
mdi.MDI_Send_Command("<ENERGY",comm)

a = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)

latvecs = np.zeros(9)

# Check for periodicity
periodic = np.zeros(3, dtype=np.int32)
mdi.MDI_Send_Command("<DIMENSIONS", comm)
mdi.MDI_Recv(3, mdi.MDI_INT, comm, buf=periodic)

# Lazy check
if periodic[0] == 2:
    mdi.MDI_Send_Command("<CELL", comm)
    mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=latvecs)

    # Retrieve the origin
    origin = np.zeros(3)
    mdi.MDI_Send_Command("<CELL_DISPL", comm)
    mdi.MDI_Recv(3, mdi.MDI_DOUBLE, comm, buf=origin)

    # Print
    print("The simulation is periodic.")

charges = np.zeros(3)
mdi.MDI_Send_Command("<CHARGES", comm)
mdi.MDI_Recv(3, mdi.MDI_DOUBLE, comm, buf=charges)

coords = np.zeros(9)
mdi.MDI_Send_Command("<COORDS", comm)
mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=coords)

elements = np.zeros(3, dtype=np.int32)
mdi.MDI_Send_Command("<ELEMENTS", comm)
mdi.MDI_Recv(3, mdi.MDI_INT, comm, buf=elements)

forces = np.zeros(9)
mdi.MDI_Send_Command("<FORCES", comm)
mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm, buf=forces)


# Print the name of the engine
print("ENGINE NAME: " + str(name))
print(f"ENERGY: {a}")
print(f"CELL: {latvecs}")
print(f"CELL_DISPL: {origin}")
print(f"CHARGES: {charges}")
print(f"COORDS: {coords}")
print(f"ELEMENTS: {elements}")
print(f"FORCES: {forces}")

mdi.MDI_Send_Command("EXIT", comm)
