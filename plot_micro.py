from helpers.plot_cube import plot_cube
import sys
import h5py

fpath = sys.argv[1]
num = int(sys.argv[2])

mfile = h5py.File(fpath, "r")
# get phase indicator
m = mfile["micros"][num, 1]

plot_cube(m, savedir=f"micro_{num}", cmap="viridis")
