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
