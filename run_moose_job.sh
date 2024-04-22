# Given a moose .i script, run it and postprocess results

MOOSE_INP=$1

HEADER="\n-------------------------------------------------\n"

POSTPROC_SCRIPT=$(realpath postprocess.py)

# get the job directory and name from the .i file
jobdir=$(dirname $MOOSE_INP)
jobname=$(basename $MOOSE_INP .i)

echo $jobdir $jobname

# what name is this batch of files?
batchname=$(basename $jobdir)

# assume the output dir is in this directory, make sure it exists
output_dir="outputs/${batchname}"
mkdir -p $output_dir

# now that we know it exists, get an absolute path
output_dir=$(realpath $output_dir)

# if our results file already exists, then don't re-run generation 
if [[ -f "${output_dir}/${jobname}.h5" ]]; then
  echo Results file already exists, skipping this file!
  exit 
fi

echo Output dir is: $output_dir


# make sure we have access to moose
MOOSE_EXE="$CONDA_PREFIX/moose/bin/moose";

if ! command -v $MOOSE_EXE &> /dev/null; then
	echo Error! Moose exe "(currently trying $MOOSE_EXE)" not found! Remember to load the moose environment firt
	exit;
fi

# check if we have MPI
if command -v mpiexec &> /dev/null; then
	MPI_CMD="mpiexec";
fi

# now run the moose script 
cmd="$MPI_CMD $MOOSE_EXE -i $MOOSE_INP"
echo Running command $cmd
eval $cmd

# results will be next to the input file
cmd="python $POSTPROC_SCRIPT ${output_dir}/${jobname}.e"
echo Running command $cmd
eval $cmd




