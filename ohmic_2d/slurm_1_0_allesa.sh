#!/bin/sh  
#SBATCH --job-name=heom_2d_L-1_K-0_allesa
#SBATCH --output=heom_2d_L-1_K-0_allesa.log
#SBATCH --error=heom_2d_L-1_K-0_allesa.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --partition=sandyb
#SBATCH --qos=sandyb-long
#SBATCH --time=7-00:00:00

WORKDIR=$SLURM_SUBMIT_DIR
cd $WORKDIR

python -u driver.py 1 0 allesa
