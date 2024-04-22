import numpy as np
import json
import os

import argparse
import h5py

from helpers.common import *
from helpers.nphase import *

import re

parser = argparse.ArgumentParser(
    prog="write_nphase_3d",
    description="Writes a 3D n-phase microstructure into a moose input file",
)
parser.add_argument(
    "-m",
    "--micro_file",
    help="HDF5 Microstructure file to use as input (otherwise randomly generated)",
    default=None,
)

parser.add_argument(
    "--isotropic",
    action="store_true",
    default=True,
    help="Whether material is isotropic or cubic (only when randomly generated)",
)

NUM_PHASES = 2
CR = 100

E_VALS = np.array([120, 120 * CR])
NU_VALS = np.array([0.3, 0.3])

C11 = 100
C12 = 0
C44 = 1

N = 20
BASE_NAME = "2phase"

BC_VALS = np.zeros(6)
BC_VALS[0] = 0.001
# BC_VALS[1] = 0.001
# BC_VALS[2] = 0.001

BASE_TEMPLATE = "templates/local3d.i"


def load_micro_file(mf):
    f = h5py.File(mf, "r")

    micro = f["micros"][0]

    # convert 2phase to phase ids
    # 0 if phase zero, 1 if phase 1
    micro = micro[1]

    return micro.astype(int)


def gen_micro(N):
    size = (N, N, N)
    micro = np.random.randint(0, 2, size=size)

    Nx = N
    Ny = N
    Nz = N

    micro = np.zeros((Nx, Ny, Nz), dtype=int)

    x = np.arange(0, Nx)
    y = np.arange(0, Ny)
    z = np.arange(0, Nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    print(X.shape, micro.shape)

    in_box = (X >= 0) & (X <= N - 2) & (Y >= 0) & (Y <= 4) & (Z >= 0) & (Z <= 6)

    print(in_box.shape)
    print(X.shape)
    print(Y.shape)

    # R = X**2 + Y**2 + Z**2

    micro[in_box] = 1

    micro = np.random.randint(0, 2, (N, N, N))

    return micro.astype(int), X


def build_input_nphase(
    micro,
    phase_info,
    bc_vals,
    basename,
    input_dir=INPUT_DIR,
    output_dir=OUTPUT_DIR,
):

    # convert C-to-Fortran ordering
    micro = micro.transpose(-1, -2, -3)

    with open(BASE_TEMPLATE, "r") as f:
        template = "".join(f.readlines())

    template = write_micro_info(micro, template)
    template = write_BCs(bc_vals, template)

    # assumes micro is phase IDs, starting at zero!!
    active_phases = np.unique(micro)

    N_x, N_y, N_z = micro.shape[-3:]
    template = write_mesh_info(N_x, N_y, N_z, template)

    # use same ids as
    template = write_phase_stiffnesses(phase_info, active_phases, template)

    # now write other info
    template = template.replace(r"{{base_name}}", f"{basename}")
    # template = template.replace(r"{{INPUT_DIR}}", f"{INPUT_DIR}")
    template = template.replace(r"{{OUTPUT_DIR}}", f"{output_dir}")

    template = template.replace(r"{{CRYSTAL_MODE}}", f"false")
    template = template.replace(r"{{NPHASE}}", f"true")

    # get rid of any unwritten template entries
    template = remove_unused(template)

    return template


if __name__ == "__main__":

    args = parser.parse_args()
    os.makedirs(INPUT_DIR, exist_ok=True)

    if args.micro_file:
        micro = load_micro_file(args.micro_file)

        print(micro.shape)
    else:
        micro, X = gen_micro(N)

    np.save("structure.npy", micro)

    if args.isotropic:
        # TODO generalize to more than 2 phases ??
        phase_info = np.array([E_VALS, NU_VALS]).T
    else:
        # TODO generalize to more than 2 phases ??
        phase_info = np.array([[C11, C12, C44], [0.1 * C11, 0.1 * C12, 0.1 * C44]])

    template = build_input_nphase(micro, phase_info, BC_VALS, BASE_NAME)

    with open(f"{INPUT_DIR}/{BASE_NAME}.i", "w") as f:
        f.writelines(template)
