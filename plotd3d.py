import matplotlib.pyplot as plt
import numpy as np
from h5py import File

ds = 2


def plot_cube(im, savedir, elev=34, azim=-30):
    Ix = im[0, :, :]
    Iy = im[:, 0, :]
    Iz = im[:, :, 0]

    vmin = np.min([Ix, Iy, Iz])
    vmax = np.max([Ix, Iy, Iz])
    norm = plt.Normalize(vmin=vmin, vmax=vmax)

    colors = plt.cm.turbo(norm(im))

    Cx = colors[0, :, :]
    Cy = colors[:, 0, :]
    Cz = colors[:, :, 0]

    # print(Ix, Iy, Iz)

    print(im.shape, Ix.shape)

    xp, yp = Ix.shape

    print(xp, yp)
    x = np.arange(0, xp, 1 - 1e-13)
    y = np.arange(0, yp, 1 - 1e-13)
    Y, X = np.meshgrid(y, x)

    print(x)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.dist = 6.2
    ax.view_init(elev=elev, azim=azim)
    ax.axis("off")

    print(X.shape, Y.shape, np.rot90(Ix, k=1).shape, (X - X + yp).shape)

    # print()

    ax.plot_surface(
        X,
        Y,
        X - X + yp,
        facecolors=np.rot90(Cx, k=1),
        rstride=1,
        cstride=1,
        antialiased=True,
        shade=False,
        vmin=vmin,
        vmax=vmax,
        cmap="turbo",
    )

    ax.plot_surface(
        X,
        X - X,
        Y,
        facecolors=np.rot90(Cy.transpose((1, 0, 2)), k=2),
        rstride=1,
        cstride=1,
        antialiased=True,
        shade=False,
        vmin=vmin,
        vmax=vmax,
        cmap="turbo",
    )

    ax.plot_surface(
        X - X + xp,
        X,
        Y,
        facecolors=np.rot90(Cz, k=-1),
        rstride=1,
        cstride=1,
        antialiased=True,
        shade=False,
        vmin=vmin,
        vmax=vmax,
        cmap="turbo",
    )
    fig.tight_layout()

    # make colorbar directly from normalization code
    m = plt.cm.ScalarMappable(cmap=plt.cm.turbo, norm=norm)
    m.set_array([])
    fig.colorbar(m, ax=ax)
    plt.savefig(savedir, transparent=True, dpi=300)

    plt.show()

    plt.close()


if __name__ == "__main__":
    f = File(
        "/home/conlain/programs/d3d/DREAM3D-6.5.171-Linux-x86_64/Data/Output/Synthetic/01_CubicSingleEquiaxedOut.dream3d"
    )

    euler_ang = f["DataContainers"]["SyntheticVolumeDataContainer"]["CellData"][
        "EulerAngles"
    ]

    print(euler_ang.shape)

    euler_1 = euler_ang[..., 0]
    print(euler_1.shape)

    euler_1 = euler_1[::ds, ::ds, ::ds]

    plot_cube(euler_1, savedir="d3d.png")
