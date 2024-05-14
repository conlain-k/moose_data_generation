import numpy as np
import matplotlib.pyplot as plt
import glob
from natsort import natsorted
import pandas as pd

timing = np.genfromtxt(
    "timing_res.txt.txt",
    names=True,
    delimiter=",",
)

C_TRUE = 242.672224

bases = [f"{i:05}" for i in range(9)]


def load_solver_files(dir, solver):
    dfs = []
    for b in bases:
        # get base filename
        f_base = f"{dir}/{solver}_*_{b}.csv"
        all_files = glob.glob(f_base)
        all_files = natsorted(all_files)
        # read all csv files into one super dataframe
        # source https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
        df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        # use highest tol for "true" value
        # print(df["avg_stiff_xx"].max())
        # print(df["avg_stiff_xx"] == df["avg_stiff_xx"].max())
        C_true = (
            df[df["final_residual"] == df["final_residual"].min()][
                "avg_stiff_xx"
            ].values[0]
            + 1e-12
        )
        print("Ctrue", C_true)
        df["C_err"] = abs(df["avg_stiff_xx"] - C_true) / C_true

        # build up list of dfs
        dfs.append(df)

    # load all of them into one super-df
    df = pd.concat(dfs, ignore_index=True)

    return df


df_gmres = load_solver_files("sweep_outputs", "gmres")
df_bcgs = load_solver_files("sweep_outputs", "bcgs")

print(df_bcgs)
print(df_gmres)


def plot_two(k1, k2, df, df_name=None, fig=None):
    if fig is None:
        fig = plt.figure()
    # sort by x-axis
    df = df.sort_values(k1)
    plt.scatter(df[k1], df[k2], label=df_name)
    plt.xlabel(k1)
    plt.ylabel(k2)
    plt.yscale("log")
    plt.xscale("log")
    plt.title(f"{k1} vs {k2}")

    if df_name is not None:
        plt.legend()

    plt.tight_layout()

    return fig


fig = plot_two("C_err", "solve_time", df_gmres, "GMRES")
plot_two("C_err", "solve_time", df_bcgs, "BCGS", fig)

plt.scatter(1e-3, 0.03, label="NN")
plt.legend()

plt.tight_layout()


plt.savefig("timing_new.png", dpi=300)

fig = plot_two("final_residual", "C_err", df_gmres, "GMRES")
plot_two("final_residual", "C_err", df_bcgs, "BCGS", fig)

plt.savefig("tol_err.png", dpi=300)
