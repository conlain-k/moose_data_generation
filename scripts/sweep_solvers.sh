# Sweeps over a set of solver settings for a given input file

MOOSE_INP="$1"
# tolerances to sweep
TOLS=(1e-3 1e-4 1e-5 1e-6 1e-7 1e-8 1e-9 1e-10)
# solvers to try
SOLVERS=(gmres bcgs)
jobname=$(basename $MOOSE_INP .i)

# sweep over tolerances
for tol in "${TOLS[@]}"; do
    for solver in "${SOLVERS[@]}"; do
        base_name="sweep_outputs/${solver}_${tol}_${jobname}"
        cmd="./run.sh $MOOSE_INP -ksp_type $solver Executioner/nl_abs_tol=${tol} Outputs/file_base=${base_name}"
        echo $cmd
        eval $cmd
    done
done