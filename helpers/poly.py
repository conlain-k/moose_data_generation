# common template info used for polycrystal microstructures

import shutil
import os
import json

EULER_ANG_TEMPLATE = "templates/crystal/euler_ang_file.i"
CUBIC_CRYSTAL_TEMPLATE = "templates/crystal/crystal_cubic.i"
POSTPROC_CRYSTAL_PATH = "templates/crystal/postproc_euler.i"


def write_cubic_coeffs(C11, C12, C44, template):
    # write cubic coefficients for a polycrystal microstructure
    with open(CUBIC_CRYSTAL_TEMPLATE, "r") as f:
        cubic_template = "".join(f.readlines())

    cubic_template = cubic_template.replace(r"{{C11}}", f"{C11}")
    cubic_template = cubic_template.replace(r"{{C12}}", f"{C12}")
    cubic_template = cubic_template.replace(r"{{C44}}", f"{C44}")

    # now write elastic tensor and euler ang info to main file
    template = template.replace(r"{{ELAST_TENSORS}}", f"{cubic_template}")
    return template


def write_initial_angles(euler_ang_txt, template):
    # write initial euler angles part of the .i file
    with open(EULER_ANG_TEMPLATE, "r") as f:
        euler_template = "".join(f.readlines())

    # get relative path to file and make sure it's in right place
    # ang_file = os.path.basename(euler_ang_txt)
    # shutil.copy2(euler_ang_txt, f"{INPUT_DIR}/{ang_file}")

    # write that relative path into template
    euler_template = euler_template.replace(r"{{EULER_ANG_FILE}}", f"{euler_ang_txt}")

    template = template.replace(r"{{CRYSTAL_FILE_INFO}}", f"{euler_template}")

    extra_pp = f"!include {POSTPROC_CRYSTAL_PATH}"

    template = template.replace(r"{{EXTRA_POST}}", f"{extra_pp}")

    return template
