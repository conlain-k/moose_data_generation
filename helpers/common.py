# common template info used for both nphase and crystal

import shutil
import os
import json

import re

INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"


def remove_unused(template):
    # overwrite unused entries in the template
    template = re.sub("{{.*?}}", "", template)
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

    # estimate half the BC strains as initial cond (plus some small noise to get GMRES going)
    template = template.replace(r"{{DISP_X_INIT}}", f"{exx }")
    template = template.replace(r"{{DISP_Y_INIT}}", f"{eyy }")
    template = template.replace(r"{{DISP_Z_INIT}}", f"{ezz }")

    # write BC function vals
    return template


def write_mesh_info(N_x, N_y, N_z, template):
    # first write mesh info
    template = template.replace(r"{{N_x}}", f"{N_x}")
    template = template.replace(r"{{N_y}}", f"{N_y}")
    template = template.replace(r"{{N_z}}", f"{N_z}")

    return template
