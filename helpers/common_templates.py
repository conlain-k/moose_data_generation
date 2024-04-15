# common template info used for both nphase and crystal

import shutil
import os
import json

INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"

PHASE_STIFF_ISO_TEMPLATE = "templates/phase_stiffness_iso.i"
PHASE_STIFF_CUBIC_TEMPLATE = "templates/phase_stiffness_cubic.i"

EULER_ANG_TEMPLATE = "templates/euler_ang_file.i"
CUBIC_CRYSTAL_TEMPLATE = "templates/crystal_cubic.i"


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


def write_crystal_info(N, C11, C12, C44, euler_ang_file, template):

    # first write mesh info
    # TODO take in D3D file and compute these directly
    template = template.replace(r"{{N_x}}", f"{N}")
    template = template.replace(r"{{N_y}}", f"{N}")
    template = template.replace(r"{{N_z}}", f"{N}")

    with open(EULER_ANG_TEMPLATE, "r") as f:
        euler_template = "".join(f.readlines())

    # get relative path to file and make sure it's in right place
    ang_file = os.path.basename(euler_ang_file)
    shutil.copy2(euler_ang_file, f"{INPUT_DIR}/{ang_file}")

    # write that relative path into template
    euler_template = euler_template.replace(r"{{EULER_ANG_FILE}}", f"{ang_file}")

    with open(CUBIC_CRYSTAL_TEMPLATE, "r") as f:
        cubic_template = "".join(f.readlines())

    cubic_template = cubic_template.replace(r"{{C11}}", f"{C11}")
    cubic_template = cubic_template.replace(r"{{C12}}", f"{C12}")
    cubic_template = cubic_template.replace(r"{{C44}}", f"{C44}")

    # now write elastic tensor and euler ang info to main file
    template = template.replace(r"{{ELAST_TENSORS}}", f"{cubic_template}")
    template = template.replace(r"{{CRYSTAL_FILE_INFO}}", f"{euler_template}")

    # now we know we won't need nphase info, so overwrite that as well
    template = template.replace(r"{{subdomain_info}}", "")

    return template


def write_phase_stiffnesses(phase_info, active_ids, template):

    if len(phase_info[0]) == 2:
        fname = PHASE_STIFF_ISO_TEMPLATE
    else:
        fname = PHASE_STIFF_CUBIC_TEMPLATE

    with open(fname, "r") as f:
        p_temp_base = "".join(f.readlines())

    phase_sections = []

    for id in active_ids:
        phase_val = phase_info[id]

        # make a copy
        p_t = p_temp_base

        # isotropic
        if len(phase_val) == 2:
            E, nu = phase_val
            # replace relevant phases
            p_t = p_t.replace(r"{{E}}", f"{E}")
            p_t = p_t.replace(r"{{nu}}", f"{nu}")
        else:
            c11, c12, c44 = phase_val
            p_t = p_t.replace(r"{{C11}}", f"{c11}")
            p_t = p_t.replace(r"{{C12}}", f"{c12}")
            p_t = p_t.replace(r"{{C44}}", f"{c44}")

        # now write phase id
        p_t = p_t.replace(r"{{id}}", f"{id}")
        phase_sections.append(p_t)

    phases_sec_full = "\n".join(phase_sections)
    template = template.replace(r"{{ELAST_TENSORS}}", f"{phases_sec_full}")

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

    template = template.replace(
        r"{{subdomain_info}}", f"subdomain_ids = {subdomain_ids}"
    )

    # empty out crystal-specific info
    template = template.replace(r"{{CRYSTAL_FILE_INFO}}", "")

    return template
