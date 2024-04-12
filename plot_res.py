import numpy as np
import matplotlib.pyplot as plt
from helpers.plot_cube import plot_cube

from h5py import File

PLOT_SLICE = 10

E_BAR = 0.001

m = np.load("structure.npy")

eps_file = np.genfromtxt(
    "outputs/2phase_strain_out_0001.csv",
    names=True,
    delimiter=",",
)

sig_file = np.genfromtxt(
    "outputs/2phase_stress_out_0001.csv",
    names=True,
    delimiter=",",
)

sigxx = sig_file["stress_xx"][:]
sigxx = sigxx.reshape(m.shape, order="F")


exx = eps_file["strain_xx"][:] / E_BAR
exx = exx.reshape(m.shape, order="F")

print(sigxx.shape, exx.shape, m.shape)

# exx = exx.transpose(-3, -2, -1)

ab_file = File("00000.h5")

print(ab_file.keys())
exx_ab = ab_file["strain"][0, 0] / E_BAR


def rr(field):
    field = np.roll(field, -25, 0)
    field = np.roll(field, -33, 1)
    field = np.roll(field, -17, 2)

    return field


m = rr(m)
exx = rr(exx)
sigxx = rr(sigxx)
exx_ab = rr(exx_ab)


plot_cube(m, title="m", savedir="m.png", add_cb=False, cmap="viridis")

plot_cube(exx, title="exx", savedir="exx.png")

plot_cube(sigxx, title="sigxx", savedir="sigxx.png")

plot_cube(exx_ab, title="exx_ab", savedir="exx_ab.png")

plot_cube(exx_ab - exx, title="diff", savedir="diff.png")


plt.show()
