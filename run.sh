MOOSE_EXE="$CONDA_PREFIX/moose/bin/moose"

if command -v mpiexec; then
	MPI_CMD="mpiexec";
fi

if ! command -v $MOOSE_EXE; then
	echo Error! Moose exe "(currently trying $MOOSE_EXE)" not found! Remember to load the moose environment firt
	exit;
fi

# call MPI (if it's around) then pass through args to moose
$MPI_CMD $MOOSE_EXE -i $@
