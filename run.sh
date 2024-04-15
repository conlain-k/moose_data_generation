MOOSE_EXE="$CONDA_PREFIX/moose/bin/moose"

if command -v mpiexec; then
	MPI_CMD="mpiexec";
fi

# call MPI (if it's around) then pass through args to moose
$MPI_CMD $MOOSE_EXE -i $@
