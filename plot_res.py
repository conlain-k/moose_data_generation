import numpy as np
import matplotlib.pyplot as plt
from helpers.plotd3d import plot_cube

from h5py import File

PLOT_SLICE = 10

E_BAR = 0.001

m = np.load("structure.npy")

eps_file = np.genfromtxt(
    "outputs/2phase_strain_out_0001.csv",
    names=True,
    delimiter=",",
)


exx = eps_file["strain_xx"][:] / E_BAR
exx = exx.reshape(m.shape)

# exx = exx.transpose(-3, -2, -1)

ab_file = File("00000.h5")

print(ab_file.keys())
exx_ab = ab_file["strain"][0, 2]


plot_cube(m)

# plt.xlabel("x")
# plt.ylabel("y")
# plt.ylabel("z")
plt.title("micro")
plt.tight_layout()

plot_cube(exx)

# plt.xlabel("x")
# plt.ylabel("y")
# plt.ylabel("z")
plt.title("strain_xx")
plt.tight_layout()


# plt.figure()
# plt.imshow(exx_ab[:, PLOT_SLICE], origin="lower")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("exx abaqus")
# plt.colorbar()
# plt.tight_layout()

plt.show()
