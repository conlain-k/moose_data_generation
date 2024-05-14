from pylauncher import pylauncher
import sys
import os
import glob
import re
from natsort import natsorted

from manage_data import concat_files

from pathlib import Path

JOB_ID = os.environ.get("SLURM_JOB_ID", "head")

MOOSE_EXE = "moose"
PP_SCRIPT = "postprocess.py"

# temp directory for pylauncher
TMPDIR = "pyl"
# ensure that temp directory exists before we use it
os.makedirs(TMPDIR, exist_ok=True)

# remember to change this if we don't want to use whole nodes per job
NUM_CORES = 8

# remove trailing slashes
input_dir = sys.argv[1].rstrip("/")
batchname = Path(input_dir).stem
output_dir = f"outputs/{batchname}"


print(input_dir)


# get all inps
globstr = f"{input_dir}/*.i"
# now filter for solely numeric ones
restr = f"{input_dir}/[0-9]*.i"

print(restr, globstr)

# get all numeric inps in directory
all_inputs = glob.glob(globstr)
# check that inps are solely numeric
all_inputs = filter(re.compile(restr).match, all_inputs)
all_inputs = natsorted(all_inputs)

# TODO: filter out inps that were already run!


print(len(all_inputs))
job_lines = []  # = [None] * len(all_inputs)
postproc_lines = []  # = [None] * len(all_inputs)
for ind, input in enumerate(all_inputs):

    # what is output file to watch
    curr_output_csv = f"{output_dir}/{Path(input).stem}_stress_strain.csv"
    curr_output_h5 = f"{output_dir}/{Path(input).stem}.h5"

    # check if results exist, if so skip
    if not os.path.isfile(curr_output_csv):
        # run it through moose
        job_lines.append(f"moose -i {input}")

    # also check h5 file
    if not os.path.isfile(curr_output_h5):
        postproc_lines.append(
            (f"pwd; python {PP_SCRIPT} {curr_output_csv} {curr_output_h5}")
        )


jobfile = f"{TMPDIR}/moose_pylauncher_{JOB_ID}_moose.in"
postproc_file = f"{TMPDIR}/moose_pylauncher_{JOB_ID}_postproc.in"
# now write job lines to a file
with open(jobfile, "w") as f:
    print("\n".join(job_lines), file=f)
with open(postproc_file, "w") as f:
    print("\n".join(postproc_lines), file=f)

workdir = f"{TMPDIR}/pylauncher_moose_{JOB_ID}"
pp_workdir = f"{TMPDIR}/pylauncher_postproc_{JOB_ID}"


# first run all moose jobs
pylauncher.MPILauncher(
    jobfile, cores=NUM_CORES, debug="job+task", workdir=workdir, delay=0.25
)

# then do postprocessing (one core per job since it's easier)
pylauncher.ClassicLauncher(
    postproc_file, cores=1, debug="job+task", workdir=pp_workdir, delay=0.25
)

output_base = f"{Path(input).stem}"
concat_files(basename=f"{output_dir}/{output_base}", output_file=f"output_base.h5")
