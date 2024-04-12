import numpy as np
import matplotlib.pyplot as plt


def plot_cube(
    im,
    savedir=None,
    elev=30,
    azim=-40,
    ortho=True,
    edges=True,
    coord=True,
    title=None,
    add_cb=True,
    cmap="turbo",
    edges_kw=dict(color="0.3", linewidth=1, linestyle="--", zorder=10),
):

    im = np.flip(np.rot90(np.rot90(im, k=1, axes=(0, 1)), k=-1, axes=(1, 2)), axis=1)

    # im = np.moveaxis(im, 0, -1)

    vmin = im.min()
    vmax = im.max()

    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    colors = plt.get_cmap(cmap)(norm(im))

    Cx = colors[0, :, :]
    Cy = colors[:, 0, :]
    Cz = colors[:, :, 0]

    # back faces
    Cx_b = colors[-1, :, :]
    Cy_b = colors[:, -1, :]
    Cz_b = colors[:, :, -1]

    """
        Cx = .8 * Cx
        Cy = .7 * Cy
        Cz =  1 * Cz
        """

    xp, yp, _ = Cx.shape
    x = np.arange(0, xp, 1 - 1e-13)
    y = np.arange(0, yp, 1 - 1e-13)
    Y, X = np.meshgrid(y, x)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.dist = 6.2
    ax.view_init(elev=elev, azim=azim)
    ax.axis("off")

    print(Cx.shape, X.shape)

    # plot one plane
    def plot_plane(xx, yy, zz, col):
        ax.plot_surface(
            xx,
            yy,
            zz,
            facecolors=col,
            rstride=1,
            cstride=1,
            antialiased=True,
            shade=False,
        )

    # Z=const
    plot_plane(X, Y, 0 * X + yp, np.rot90(Cx, k=1))
    plot_plane(X, Y, 0 * X, np.rot90(Cx_b, k=1))
    # Y=const
    plot_plane(X, 0 * X, Y, np.rot90(Cy.transpose((1, 0, 2)), k=2))
    plot_plane(X, 0 * X + yp, Y, np.rot90(Cy_b.transpose((1, 0, 2)), k=2))
    # X = const
    plot_plane(0 * X + xp, X, Y, np.rot90(Cz, k=-1))
    plot_plane(0 * X, X, Y, np.rot90(Cz_b, k=-1))

    if edges:
        # x+, both z
        ax.plot([xp, xp], [0, xp], xp, **edges_kw)
        ax.plot([xp, xp], [0, xp], 0, **edges_kw)

        # x-, both z
        ax.plot([0, 0], [0, xp], xp, **edges_kw)
        # ax.plot([0, 0], [0, xp], 0, **edges_kw)

        # y+
        # ax.plot([0, xp], [xp, xp], 0, **edges_kw)
        ax.plot([0, xp], [xp, xp], xp, **edges_kw)

        ax.plot([0, xp], [0, 0], 0, **edges_kw)
        ax.plot([0, xp], [0, 0], xp, **edges_kw)

        # z lines
        ax.plot([0, 0], [0, 0], [0, xp], **edges_kw)
        ax.plot([xp, xp], [0, 0], [0, xp], **edges_kw)
        # ax.plot([0, 0], [xp, xp], [0, xp], **edges_kw)
        ax.plot([xp, xp], [xp, xp], [0, xp], **edges_kw)

    if coord:
        coord_kw = dict(linewidth=5, linestyle="-", zorder=1e3)
        coord_scale = 1.1
        gap = 0.05 * xp
        ax.plot([xp + gap, coord_scale * xp], [xp, xp], [0, 0], color="r", **coord_kw)
        ax.text(
            xp * coord_scale + 1.5 * gap,
            xp,
            0,
            "X",
            color="r",
            fontsize=18,
            horizontalalignment="center",
            verticalalignment="center",
        )

        ax.plot([0, 0], [-gap, xp - coord_scale * xp], [0, 0], color="g", **coord_kw)
        ax.text(
            0,
            xp - coord_scale * xp - 1.5 * gap,
            0,
            "Z",
            color="g",
            fontsize=18,
            horizontalalignment="center",
            verticalalignment="center",
        )

        ax.plot([0, 0], [xp, xp], [xp + gap, coord_scale * xp], color="b", **coord_kw)
        ax.text(
            0,
            xp,
            coord_scale * xp + gap,
            "Y",
            color="b",
            fontsize=18,
            horizontalalignment="center",
        )

    if ortho:
        ax.set_proj_type("ortho")

    if title is not None:
        ax.set_title(title)

    # add colorbar if requested
    if add_cb:
        m = plt.cm.ScalarMappable(cmap=plt.cm.turbo, norm=norm)
        m.set_array([])
        fig.colorbar(m, ax=ax)

    # now set title
    fig.tight_layout()

    if savedir is not None:
        plt.savefig(savedir, transparent=True, dpi=300)
        plt.close()

    else:
        return fig, ax
