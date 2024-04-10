import numpy as np
import json
import os

INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"

contrast_ratio = 1000
N = 31
size = (N, N, N)
struct = np.random.randint(0, 2, size=size)

struct = np.zeros(size, dtype=int)

base_name = "2phase"


x = np.arange(0, N)
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")

print(X.shape, struct.shape)

in_box = (X >= 4) & (X <= 6) & (Y >= 0) & (Y <= N)

# print(in_box)
# struct[in_box] = 1


# R = (X - 10) ** 2 + (Y - 20) ** 2

# struct[R < 5**2] = 1

np.save("structure.npy", struct)

E0 = 120
P0 = 0.3

E1 = 120 * contrast_ratio
P1 = 0.3

# Only works in 2d. should be the only line needed to be changed for 3d
subdomain_ids = (
    "'"
    + json.dumps(struct.tolist())
    .replace("[", "")
    .replace("],", "\n")
    .replace("]", "")
    .replace(",", "")
    + "'"
)

constraint_types = "'strain none none none'"
targets = "'strain11 zero zero zero'"


with open("templates/homog3d_nphase.i", "r") as f:
    template = "".join(f.readlines())

template = template.replace(r"{{N_x}}", f"{N}")
template = template.replace(r"{{N_y}}", f"{N}")
template = template.replace(r"{{N_z}}", f"{N}")
template = template.replace(r"{{E0}}", f"{E0}")
# template = template.replace(r"{{P0}}", f"{P0}")
template = template.replace(r"{{E1}}", f"{E1}")
# template = template.replace(r"{{P1}}", f"{P1}")
template = template.replace(r"{{subdomain_ids}}", f"{subdomain_ids}")
template = template.replace(r"{{constraint_types}}", f"{constraint_types}")
template = template.replace(r"{{targets}}", f"{targets}")
template = template.replace(r"{{base_name}}", f"{base_name}")
template = template.replace(r"{{INPUT_DIR}}", f"{INPUT_DIR}")
template = template.replace(r"{{OUTPUT_DIR}}", f"{OUTPUT_DIR}")

os.makedirs(INPUT_DIR, exist_ok=True)

with open(f"{INPUT_DIR}/{base_name}.i", "w") as f:
    f.writelines(template)
