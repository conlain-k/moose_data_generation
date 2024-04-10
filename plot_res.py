import numpy as np
import matplotlib.pyplot as plt


m = np.load("structure.npy")

eps_file = np.genfromtxt(
    "het2d_csv_strain_out_0001.csv",
    names=True,
    delimiter=",",
)

exx = eps_file["strain_xx"][:]
exx = exx.reshape(m.shape)


plt.figure()
plt.imshow(m, origin="lower")
plt.xlabel("x")
plt.ylabel("y")
plt.figure()
plt.imshow(exx, origin="lower")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
