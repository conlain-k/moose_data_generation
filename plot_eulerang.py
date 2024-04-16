from orix import io, plot
from orix.vector import Vector3d
import numpy as np

import matplotlib.pyplot as plt

from orix.quaternion.symmetry import get_point_group

ipfkey = plot.IPFColorKeyTSL(get_point_group(225), direction=Vector3d.zvector())

ipfkey.plot()

ori = np.genfromtxt(
    "outputs/poly_euler_ang_0001.csv",
    names=True,
    delimiter=",",
)

# print(ori)

euler_ang = np.stack(
    [ori["Euler_angles_x"], ori["Euler_angles_y"], ori["Euler_angles_z"]], axis=-1
)

print(euler_ang.shape)

rgb_z = ipfkey.orientation2color(euler_ang)[..., -1]  # NumPy array

print(rgb_z.shape)
rgb_z = rgb_z.reshape(21, 21, 21, 3)
print(rgb_z.shape)


from helpers.plot_cube import plot_cube

plot_cube(rgb_z[..., 0])
plt.show()

# ori.scatter(projection="ipf", c=rgb_z, direction=ipfkey.direction)
# xmap.plot(rgb_z, overlay="RefinedDotProducts")
