import numpy as np
import json
import os

import argparse
from h5py import File

from helpers.common import *
from helpers.poly import *

parser = argparse.ArgumentParser(
    prog="write_nphase_3d",
    description="Writes a 3D n-phase microstructure into a moose input file",
)
parser.add_argument(
    "-m",
    "--euler_ang_file",
    help="Dream3D microstructure file (h5py format)",
    required=True,
)

parser.add_argument(
    "-N",
    help="Number of voxels in each direction (assumes square). If different from the given file, will override to a square mesh (USED ONLY FOR TESTING!!)",
    default=None,
)

C11 = 160
C12 = 70
C44 = 60

BASE_NAME = "poly"

RADIAN_TO_DEG = 180 / np.pi


BC_VALS = np.zeros(6)
BC_VALS[0] = 0.001
# BC_VALS[1] = 0.001
# BC_VALS[2] = 0.001

BASE_TEMPLATE = "templates/local3d.i"


def write_euler_to_txt(moose_fname, d3d_fname):
    f = File(d3d_fname, "r")
    # break into 2 lines for legibility
    cell_dat = f["DataContainers"]["SyntheticVolumeDataContainer"]["CellData"]
    euler_ang = cell_dat["EulerAngles"][:]

    print(euler_ang.shape)
    euler_ang = euler_ang.transpose(-1, -2, -3, 0)

    # euler_ang = 0 * euler_ang
    # euler_ang[0, ...] = np.pi / 4
    # euler_ang[2, ...] = np.pi / 4

    # get spatial dims
    N_x, N_y, N_z = euler_ang.shape[-3:]

    print(euler_ang.shape)

    euler_ang *= RADIAN_TO_DEG

    # write in fortran ordering since Moose uses that
    euler_ang = euler_ang.reshape(3, -1, order="C").T

    np.savetxt(moose_fname, euler_ang, fmt="%.14f")

    return N_x, N_y, N_z


def build_input_crystal(
    d3d_fname,
    C11,
    C12,
    C44,
    bc_vals,
    base_name,
    input_dir=INPUT_DIR,
    output_dir=OUTPUT_DIR,
    N_override=None,
):

    with open(BASE_TEMPLATE, "r") as f:
        template = "".join(f.readlines())

    template = write_BCs(bc_vals, template)

    moose_poly_fname = f"{input_dir}/{base_name}_euler_ang.txt"

    N_x, N_y, N_z = write_euler_to_txt(moose_poly_fname, d3d_fname)

    # override size (assumes smaller than given mesh) for testing purposes
    if N_override is not None:
        N_x, N_y, N_z = N_override, N_override, N_override

    template = write_initial_angles(f"{base_name}_euler_ang.txt", template)

    # write mesh size
    template = write_mesh_info(N_x, N_y, N_z, template)
    # crystal coefficients
    template = write_cubic_coeffs(C11, C12, C44, template)

    # now write other info
    template = template.replace(r"{{base_name}}", f"{base_name}")
    template = template.replace(r"{{INPUT_DIR}}", f"{input_dir}")
    template = template.replace(r"{{OUTPUT_DIR}}", f"{output_dir}")

    template = template.replace(r"{{CRYSTAL_MODE}}", f"true")
    template = template.replace(r"{{NPHASE}}", f"false")

    # get rid of elastic filler
    template = remove_unused(template)
    return template


if __name__ == "__main__":

    args = parser.parse_args()

    os.makedirs(INPUT_DIR, exist_ok=True)

    template = build_input_crystal(
        args.euler_ang_file, C11, C12, C44, BC_VALS, BASE_NAME, N_override=args.N
    )

    with open(f"{INPUT_DIR}/{BASE_NAME}.i", "w") as f:
        f.writelines(template)
