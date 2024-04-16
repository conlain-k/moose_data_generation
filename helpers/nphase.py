# common template info used for both nphase and crystal

import shutil
import os
import json

PHASE_STIFF_ISO_TEMPLATE = "templates/phase_stiffness_iso.i"
PHASE_STIFF_CUBIC_TEMPLATE = "templates/phase_stiffness_cubic.i"


def write_phase_stiffnesses(phase_info, active_ids, template):

    # check whether isotropic or cubic, locally
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

    template = template.replace(
        r"{{subdomain_info}}", f"subdomain_ids = {subdomain_ids}"
    )

    # empty out crystal-specific info
    template = template.replace(r"{{CRYSTAL_FILE_INFO}}", "")

    return template
