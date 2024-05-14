import numpy as np
import json
import os
from os.path import basename, dirname, splitext

import argparse
import h5py

from helpers.common import *
from helpers.nphase import *

import glob
from natsort import natsorted

from write_nphase_3d import build_input_nphase
from write_poly_3d import build_input_crystal

parser = argparse.ArgumentParser(
    prog="write_micro_batch",
    description="Writes a batch of n-phase or crystalline 3D microstructures into a moose input file",
)

parser.add_argument(
    "-m",
    "--micro_path",
    help="Path to directory of crystalline microstructures or h5 of nphase microstructures",
    required=True,
)

parser.add_argument(
    "-c",
    "--crystal",
    action="store_true",
    default=False,
    help="Whether the structures are crystalline or N-phase.",
)

parser.add_argument(
    "-p",
    "--properties_file",
    type=str,
    default=None,
    help="JSON file for storing material properties.",
)

parser.add_argument(
    "--randomize_props",
    action="store_true",
    default=False,
    help="Randomize material properties (ignoring the provided file)",
)

parser.add_argument(
    "--randomize_bcs",
    action="store_true",
    default=False,
    help="Randomize boundary conditions (ignoring the bc flag)",
)

parser.add_argument(
    "--bc_component",
    default=0,
    type=int,
    choices=[0, 1, 2, 3, 4, 5],
    help="Which direction should we enforce strain for the appplied BCs (in Voigt ordering)? -1 means randomly select a point on the unit ball (in Voigt space)",
)

parser.add_argument(
    "--num_max",
    default=None,
    type=int,
    help="Max number of microstructures to write (defaults to all). If this is bigger than the dataset size, all microstructures will be written exactly once.",
)

parser.add_argument(
    "--applied_strain",
    default=0.001,
    type=float,
    help="Magnitude of the imposed strain",
)

BASE_TEMPLATE = "templates/local3d.i"


def load_nphase_data(prop_file):
    if prop_file is not None:
        f = json.loads(prop_file)
        e_vals = f["e_vals"]
        nu_vals = f["nu_vals"]
    else:
        # if no properties given, take defaults
        e_vals = np.array([120, 120 * 100])
        nu_vals = np.array([0.3, 0.3])

    # load nphase stiffness from json file
    return np.array([e_vals, nu_vals]).T


def load_crystal_data(prop_file):
    # load crystal data from json file
    C11 = 160
    C12 = 70
    C44 = 60

    return C11, C12, C44


def draw_random_bcs():
    bc_vec = np.random.rand(6)
    # return normalized vector (random vector on the unit ball)
    return bc_vec / (bc_vec**2).sum().sqrt()


def draw_random_nphase_prop(num_phases):
    # TODO specialize beyond 2 phases
    assert num_phases == 2

    # first draw a contrast ratio, then use that
    contrast = np.random.choice([2, 10, 50, 100])
    e_vals = np.array([120, 120 * contrast])
    nu_vals = np.array([0.3, 0.3])

    # load nphase stiffness from json file
    return np.array([e_vals, nu_vals]).T


if __name__ == "__main__":

    args = parser.parse_args()
    # get base for output directory
    base_name = splitext(basename(args.micro_path))[0]
    input_dir = f"{INPUT_DIR}/{base_name}"

    print(f"Writing files to {input_dir}")
    os.makedirs(input_dir, exist_ok=True)

    bc_vals = np.zeros(6)
    if args.bc_component == -1:
        bc_vals = np.rand(6)
        # get random point on unit ball
        bc_vals = bc_vals / np.linalg.norm(bc_vals)
    else:
        bc_vals[args.bc_component] = 1

    bc_vals *= args.applied_strain

    if args.crystal:
        C11, C12, C44 = load_crystal_data(args.properties_file)
        micro_dir = args.micro_path
        all_micros = glob.glob(base_name + "/*.dream3d")
        all_micros = natsorted(all_micros)

        num_micros = len(all_micros)

        def make_template(i):
            return build_input_crystal(
                all_micros[i],
                C11,
                C12,
                C44,
                bc_vals,
                f"{i:05}",
                output_dir=f"{OUTPUT_DIR}/{base_name}",
            )

    else:
        phase_info = load_nphase_data(args.properties_file)

        micro_f = h5py.File(args.micro_path)
        # print(micro_f.keys())
        micros = micro_f["micros"]
        print(micros.shape)
        num_micros = micros.shape[0]

        def make_template(i):
            if args.randomize_props:
                # draw random contrast ratio for this instance
                phase_info = draw_random_nphase_prop(micros.shape[1])
            if args.randomize_bcs:
                bc_vals = draw_random_bcs()
            return build_input_nphase(
                micros[i][1],
                phase_info,
                bc_vals,
                f"{i:05}",
                output_dir=f"{OUTPUT_DIR}/{base_name}",
            )

    if args.num_max is not None:
        # take lesser of two
        num_micros = min(args.num_max, num_micros)

    # how often to print?
    pf = max(2, (num_micros // 20))

    # print(f"Writing {num_micros} files in total!")
    for i in range(num_micros):

        if (i + 1) % pf == 1:
            print(f"Writing file {i} of {num_micros}!")
        # Make template file
        template = make_template(i)
        # write template file
        with open(f"{INPUT_DIR}/{base_name}/{i:05}.i", "w") as f:
            f.writelines(template)
