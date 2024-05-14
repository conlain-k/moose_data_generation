#!/bin/bash
#SBATCH -J sweep_moose                  		
#SBATCH -N 1 -n 24 --mem-per-cpu 20gb
#SBATCH -t 1:00:00
#SBATCH -A gts-skalidindi7
#SBATCH --mail-type NONE                          
#SBATCH -o slurm_outputs/%j.out   


# conda activate moose

# make sure moose conda is loaded before launching the job!!
export PATH=$HOME/ideas_storage/miniforge/bin:$PATH

cd $SLURM_SUBMIT_DIR

echo $SLURM_JOB_ID

pwd

# Add any cli overrides
./scripts/sweep_solvers.sh "$@"

