import numpy as np
from scipy.spatial.transform import Rotation
from h5py import File
from einops import rearrange

from plotd3d import plot_cube

import tensor_ops


def mat_to_vec(mat):
    # torch.testing.assert_close(mat[:, 0, 1], mat[:, 1, 0], equal_nan=True)

    # print(mat[:, 0, 1], mat[:, 1, 0])

    new_shape = mat.shape[0:1] + (6,) + mat.shape[-3:]
    vec = mat.new_zeros(new_shape)

    # extract from diagonals
    vec[:, 0] = mat[:, 0, 0]
    vec[:, 1] = mat[:, 1, 1]
    vec[:, 2] = mat[:, 2, 2]

    # off-diag
    vec[:, 3] = mat[:, 0, 1]
    vec[:, 4] = mat[:, 0, 2]
    vec[:, 5] = mat[:, 1, 2]

    # torch.testing.assert_close(mat, vec_to_mat(vec))
    return vec


def delta(i, j):
    # kronecker delta
    return int(i == j)


def vec_to_mat(vec):
    # torch.testing.assert_close(vec, mat_to_vec(vec_to_mat(vec)))

    # assumes vec has size [b, 6, i, j, k]
    # will return mat with size [b, 3, 3, i, j, k]
    # Convert a vector of length 6 to an equivalent symmetric 3 x 3 matrix using abaqus ordering
    new_shape = vec.shape[0:1] + (3, 3) + vec.shape[-3:]
    mat = vec.new_zeros(new_shape)

    # diagonals
    mat[:, 0, 0] = vec[:, 0]
    mat[:, 1, 1] = vec[:, 1]
    mat[:, 2, 2] = vec[:, 2]

    # off-diag
    mat[:, 0, 1] = vec[:, 3]
    mat[:, 1, 0] = vec[:, 3]
    mat[:, 0, 2] = vec[:, 4]
    mat[:, 2, 0] = vec[:, 4]
    mat[:, 1, 2] = vec[:, 5]
    mat[:, 2, 1] = vec[:, 5]

    return mat


def iso_C_matrix(lamb, mu):
    new_mat = np.zeros((6, 6))
    # set up tensor
    for row in range(3):
        # set up off-diag in this row
        new_mat[row, :3] = lamb
        # and diag entry
        new_mat[row, row] = 2 * mu + lamb

    for row in range(3, 6):
        # set up last three diagonals
        new_mat[row, row] = mu

    return new_mat


def compute_local_stiffness(euler_ang, stiff_mat_base):
    # flatten spatial dims
    euler_ang = rearrange(euler_ang, "x y z theta -> (x y z) theta", theta=3)

    # get vector of rotation mats
    R = Rotation.from_euler("ZXZ", euler_ang)

    print(R.as_matrix().shape, stiff_mat_base.shape)

    # do operation over flattened spatial vector and then reshape
    C_field = np.einsum(
        "X i m, X j n, X k o, X l p, mnop -> X i j k l",
        R.as_matrix(),
        R.as_matrix(),
        R.as_matrix(),
        R.as_matrix(),
        stiff_mat_base,
    )

    print(C_field.shape)

    C_field = rearrange(C_field, "(x y z) i j k l -> x y z i j k l", x=62, y=62, z=62)

    print(C_field.shape)

    return C_field


f = File(
    "/home/conlain/programs/d3d/DREAM3D-6.5.171-Linux-x86_64/Data/Output/Synthetic/01_CubicSingleEquiaxedOut.dream3d"
)

euler_ang = f["DataContainers"]["SyntheticVolumeDataContainer"]["CellData"][
    "EulerAngles"
]

print(euler_ang.shape)

# flatten
# euler_ang = euler_ang[:].reshape(-1, 3)


# stiff_mat_base = tensor_ops.isotropic_mandel66(6000, 0.3)
stiff_mat_base = tensor_ops.cubic_mandel66(160, 70, 60)
stiff_mat_base = stiff_mat_base.reshape(1, 6, 6, 1, 1, 1)
stiff_mat_base = tensor_ops.C_mandel_to_mat_3x3x3x3(stiff_mat_base)
stiff_mat_base = stiff_mat_base.squeeze()

C_field = compute_local_stiffness(euler_ang[:], stiff_mat_base)

print(C_field.shape)


plot_cube(C_field[..., 0, 0, 0, 0], "3d_C.png")
