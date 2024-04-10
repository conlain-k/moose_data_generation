import numpy as np
import itertools

import math

SQRT2 = math.sqrt(2.0)

# where to look in matrix for each vector entry
mandel_ind = np.array([(0, 0), (1, 1), (2, 2), (2, 3), (3, 1), (1, 2)])
# where to look in vector for each matrix entry
mandel_ind_inv = np.array([[0, 5, 4], [5, 1, 3], [4, 3, 2]])


def mat_3x3_to_mandel(mat):
    # print(mat[:, 0, 1], mat[:, 1, 0])

    new_shape = mat.shape[0:1] + (6,) + mat.shape[-3:]
    vec = np.zeros(new_shape)

    # extract from diagonals
    vec[:, 0] = mat[:, 0, 0]
    vec[:, 1] = mat[:, 1, 1]
    vec[:, 2] = mat[:, 2, 2]

    # off-diag
    vec[:, 3] = mat[:, 0, 1] * SQRT2
    vec[:, 4] = mat[:, 0, 2] * SQRT2
    vec[:, 5] = mat[:, 1, 2] * SQRT2

    return vec


def mandel_to_mat_3x3(vec):
    new_shape = vec.shape[0:1] + (3, 3) + vec.shape[-3:]
    mat = np.zeros(new_shape)

    # diagonals
    mat[:, 0, 0] = vec[:, 0]
    mat[:, 1, 1] = vec[:, 1]
    mat[:, 2, 2] = vec[:, 2]

    # off-diag (rescaled)
    mat[:, 0, 1] = vec[:, 3] / SQRT2
    mat[:, 1, 0] = vec[:, 3] / SQRT2
    mat[:, 0, 2] = vec[:, 4] / SQRT2
    mat[:, 2, 0] = vec[:, 4] / SQRT2
    mat[:, 1, 2] = vec[:, 5] / SQRT2
    mat[:, 2, 1] = vec[:, 5] / SQRT2

    return mat


def mandel_C_fac(i, j):
    ret = 1
    if i >= 3:
        ret *= SQRT2
    if j >= 3:
        ret *= SQRT2
    return ret


def C_3x3x3x3_to_mandel(C):
    new_shape = C.shape[0:1] + (6, 6) + C.shape[-3:]
    mat_66 = np.zeros(new_shape)

    # loop over target indices
    for i, j in itertools.product(np.arange(6), repeat=2):
        m, n = mandel_ind[i]
        o, p = mandel_ind[j]

        # now assign value and multiply by mandel scaling
        mat_66[:, i, j] = C[:, m, n, o, p] * mandel_C_fac(i, j)

    return mat_66


def C_mandel_to_mat_3x3x3x3(mat_66):
    new_shape = mat_66.shape[0:1] + (3, 3, 3, 3) + mat_66.shape[-3:]
    C = np.zeros(new_shape)

    # loop over target indices
    for m, n, o, p in itertools.product(np.arange(3), repeat=4):

        i = mandel_ind_inv[m, n]
        j = mandel_ind_inv[o, p]

        # now assign value and divide by mandel scaling
        C[:, m, n, o, p] = mat_66[:, i, j] / mandel_C_fac(i, j)

    return C


def delta(i, j):
    # kronecker delta
    return int(i == j)


def isotropic_mandel66(lamb, mu):
    # extract coefficients and use the fact that isotropic is a subset of cubic
    return cubic_mandel66(2 * mu + lamb, lamb, mu)


def cubic_mandel66(C11, C12, C44):
    # build 6x6 stiffness matrix
    new_mat = np.zeros((6, 6))

    for row in range(3):
        # set up off-diag in this row
        new_mat[row, :3] = C12
        # and diag entry
        new_mat[row, row] = C11

    for row in range(3, 6):
        # set up last three diagonals, scaled by mandel factor
        new_mat[row, row] = C44 * 2

    return new_mat
