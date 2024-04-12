import numpy as np
import json
import os

import argparse
import h5py

from helpers.common_templates import *

parser = argparse.ArgumentParser(
    prog="write_nphase_3d",
    description="Writes a 3D n-phase microstructure into a moose input file",
)
parser.add_argument(
    "-m", "--euler_ang_file", help="File containing list of euler angles", required=True
)

parser.add_argument(
    "-N", help="Number of voxels in each direction (assumes square)", required=True
)

C11 = 160
C12 = 70
C44 = 60

BASE_NAME = "poly"


BC_VALS = np.zeros(6)
BC_VALS[0] = 0.001
# BC_VALS[1] = 0.001
# BC_VALS[2] = 0.001

BASE_TEMPLATE = "templates/local3d.i"


def build_input_crystal(N, euler_ang_file, C11, C12, C44, bc_vals, basename):

    with open(BASE_TEMPLATE, "r") as f:
        template = "".join(f.readlines())

    template = write_BCs(bc_vals, template)

    # use same ids as
    template = write_crystal_info(N, C11, C12, C44, euler_ang_file, template)

    # now write other info
    template = template.replace(r"{{base_name}}", f"{basename}")
    template = template.replace(r"{{INPUT_DIR}}", f"{INPUT_DIR}")
    template = template.replace(r"{{OUTPUT_DIR}}", f"{OUTPUT_DIR}")

    return template


if __name__ == "__main__":

    args = parser.parse_args()

    os.makedirs(INPUT_DIR, exist_ok=True)

    template = build_input_crystal(
        args.N, args.euler_ang_file, C11, C12, C44, BC_VALS, BASE_NAME
    )

    with open(f"{INPUT_DIR}/{BASE_NAME}.i", "w") as f:
        f.writelines(template)
