import sys
import xarray as xr
import numpy as np
from h5py import File

from os.path import basename, dirname, splitext


def convert_exo_to_h5(moose_file_base, h5_file):

    print(f"Reading from {moose_file_base} and writing to {h5_file}")

    def load

    strain_data =    np.genfromtxt(
    moose_file,
    names=True,
    delimiter=",",usecols="strain_xx", 
)
    
        #         [
    #             gd(f"{base}_00"),
    #             gd(f"{base}_11"),
    #             gd(f"{base}_22"),
    #             gd(f"{base}_12"),
    #             gd(f"{base}_02"),
    #             gd(f"{base}_12"),

    # ds = xr.open_dataset(moose_file)

    # field_names = list(ds.get("name_elem_var").astype(str))

    # print(field_names)

    # def gd(name):
    #     # 1-based indexing
    #     ind = field_names.index(name) + 1
    #     # get elem var field to read
    #     print(name, ind, f"vals_elem_var{ind}eb1")
    #     data = ds.get(f"vals_elem_var{ind}eb1").astype(np.float32)[:]

    #     # print("datashape", data.shape)
    #     # take data from last timestep
    #     data = data[-1]
    #     # print(data[1])
    #     return data

    # def get_tensor_data(base):
    #     # array of size (6, x, y, z)
    #     return np.stack(
    #         [
    #             gd(f"{base}_00"),
    #             gd(f"{base}_11"),
    #             gd(f"{base}_22"),
    #             gd(f"{base}_12"),
    #             gd(f"{base}_02"),
    #             gd(f"{base}_12"),
    #         ],
    #         axis=0,
    #     )

    strain = get_tensor_data("total_strain")
    stress = get_tensor_data("small_stress")

    # total num voxels
    # TODO just read/write this manually with moose
    VX = round(strain.shape[-1] ** (1 / 3))
    print(VX)
    print(strain.shape, stress.shape)

    # make sure we reshape space in advance
    strain = strain.reshape(6, VX, VX, VX)
    stress = stress.reshape(6, VX, VX, VX)

    print(strain.shape, stress.shape)

    # each channel is one chunk (for all x, y, z)
    chunk_size = (1,) + strain[0].shape
    print("chunk size is", chunk_size)
    print(strain.dtype, strain.shape)
    print(stress.dtype, stress.shape)

    # write to hdf5 file
    output_f = File(h5_file, "w")

    # now make the actual datasets
    output_f.create_dataset(
        "strain",
        data=strain,
        dtype=strain.dtype,
        compression="gzip",
        compression_opts=4,
        shuffle=True,
        chunks=chunk_size,
    )
    output_f.create_dataset(
        "stress",
        data=stress,
        dtype=stress.dtype,
        compression="gzip",
        compression_opts=4,
        shuffle=True,
        chunks=chunk_size,
    )


if __name__ == "__main__":
    input_file = sys.argv[1]
    basedir = dirname(input_file)

    output_file = f"{basedir}/{splitext(basename(input_file))[0]}.h5"
    convert_exo_to_h5(input_file, output_file)
