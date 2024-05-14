#!/bin/bash
#SBATCH -J moose_gen                          
#SBATCH --nodes 16 --ntasks-per-node 24
#SBATCH --mem-per-cpu 8gb                         
#SBATCH --time 12:00:00         
#SBATCH -q inferno 
#SBATCH -A gts-skalidindi7
#SBATCH --mail-type NONE                           # please dont email me
#SBATCH -o slurm_outputs/%j.out  

inp_dir=$1
start_ind=$2
stop_ind=$3

module load pylauncher
conda activate moose

cd $SLURM_SUBMIT_DIR

echo $SLURM_JOB_ID
echo $SLURM_JOB_NODELIST


pwd

# first clean the inp directory
# bash clean_dir.sh ${inp_dir}

mpiexec hostname

# run abaqus on the given inputs
cmd="python3 moose_pylauncher.py ${inp_dir}"
echo $cmd; $cmd
