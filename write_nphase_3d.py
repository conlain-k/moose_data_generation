import numpy as np
import json
import os

import argparse
import h5py

parser = argparse.ArgumentParser(
    prog="write_nphase_3d",
    description="Writes a 3D n-phase microstructure into a moose input file",
)
parser.add_argument(
    "-m", "--micro_file", help="HDF5 Microstructure file to use as input", default=None
)

INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"

NUM_PHASES = 2
CR = 1000
E_VALS = np.array([120, 120 * CR])
NU_VALS = np.array([0.3, 0.3])

N = 10
BASE_NAME = "2phase"

BC_VALS = np.zeros(6)
BC_VALS[0] = 0.001

NPHASE_TEMPLATE = "templates/homog3d_nphase.i"
PHASE_STIFF_TEMPLATE = "templates/phase_stiffness.i"


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

    micro = np.zeros(size, dtype=int)

    x = np.arange(0, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")

    print(X.shape, micro.shape)

    in_box = (X >= 0) & (X <= N) & (Y >= 0) & (Y <= 4) & (Z >= 0) & (Z <= 6)

    # R = X**2 + Y**2 + Z**2

    micro[in_box] = 1

    return micro.astype(int), X


def write_phase_stiffnesses(E_vals, nu_vals, ids, template):
    with open(PHASE_STIFF_TEMPLATE, "r") as f:
        p_temp_base = "".join(f.readlines())

    phase_sections = []

    for E, nu, id in zip(E_vals, nu_vals, ids):

        # make a copy
        p_t = p_temp_base

        # replace relevant phases
        p_t = p_t.replace(r"{{E}}", f"{E}")
        p_t = p_t.replace(r"{{nu}}", f"{nu}")
        p_t = p_t.replace(r"{{id}}", f"{id}")
        phase_sections.append(p_t)

    phases_sec_full = "\n".join(phase_sections)
    template = template.replace(r"{{ELAST_TENSORS}}", f"{phases_sec_full}")

    return template


def write_BCs(bc_vals, template):
    # xx xy xz yx yy yz zx zy zz

    # set vals accordingly (assumes bc_vals is voigt order xx yy zz yz xz xy)
    # TODO does moose use mandel or voigt (factor of two on shears)???
    exx, eyy, ezz, eyz, exz, exy = bc_vals

    template = template.replace(r"{{STRAIN_XX}}", f"{exx}")
    template = template.replace(r"{{STRAIN_YY}}", f"{eyy}")
    template = template.replace(r"{{STRAIN_ZZ}}", f"{ezz}")
    template = template.replace(r"{{STRAIN_YZ}}", f"{eyz}")
    template = template.replace(r"{{STRAIN_XZ}}", f"{exz}")
    template = template.replace(r"{{STRAIN_XY}}", f"{exy}")

    # write BC function vals
    return template


def write_micro_info(micro, template):
    # NOTE might need to reorder
    # serialize element phase ids to a string
    subdomain_ids = (
        "'"
        + json.dumps(micro.tolist())
        .replace("[", "")
        .replace("],", "\n")
        .replace("]", "")
        .replace(",", "")
        + "'"
    )
    N_x, N_y, N_z = micro.shape

    # first write mesh info
    template = template.replace(r"{{N_x}}", f"{N_x}")
    template = template.replace(r"{{N_y}}", f"{N_y}")
    template = template.replace(r"{{N_z}}", f"{N_z}")

    template = template.replace(r"{{subdomain_ids}}", f"{subdomain_ids}")

    return template


def build_input_nphase(micro, E_vals, nu_vals, bc_vals, basename):

    # convert C-to-Fortran ordering
    micro = micro.transpose(-1, -2, -3)

    with open(NPHASE_TEMPLATE, "r") as f:
        template = "".join(f.readlines())

    template = write_micro_info(micro, template)
    template = write_BCs(bc_vals, template)

    # assumes micro is phase IDs, starting at zero!!
    active_phases = np.unique(micro)
    print(micro)
    print(active_phases, active_phases.dtype)
    E_active, nu_active = E_vals[active_phases], nu_vals[active_phases]

    # use same ids as
    template = write_phase_stiffnesses(E_active, nu_active, active_phases, template)

    # now write other info
    template = template.replace(r"{{base_name}}", f"{basename}")
    template = template.replace(r"{{INPUT_DIR}}", f"{INPUT_DIR}")
    template = template.replace(r"{{OUTPUT_DIR}}", f"{OUTPUT_DIR}")

    return template


if __name__ == "__main__":

    args = parser.parse_args()

    if args.micro_file:
        micro = load_micro_file(args.micro_file)

        print(micro.shape)
    else:
        micro, X = gen_micro(N)

    np.save("structure.npy", micro)

    template = build_input_nphase(micro, E_VALS, NU_VALS, BC_VALS, BASE_NAME)

    os.makedirs(INPUT_DIR, exist_ok=True)

    with open(f"{INPUT_DIR}/{BASE_NAME}.i", "w") as f:
        f.writelines(template)
