from helpers.plot_cube import plot_cube
import sys
import h5py
import numpy as np

fpath = sys.argv[1]
if len(sys.argv) > 2:
    num = int(sys.argv[2])
    name = num
else:
    num = np.s_[:]
    name = 0

efile = h5py.File(fpath, "r")
# get phase indicator

strain = efile["strain"][num]
stress = efile["stress"][num]


print(strain.shape)

print(strain.mean(axis=(-3, -2, -1)))
print(stress.mean(axis=(-3, -2, -1)))

plot_cube(strain[0], savedir=f"strain_{name}", cmap="viridis")
