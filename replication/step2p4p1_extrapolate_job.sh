#!/bin/bash
#$ -S /bin/bash
#$ -R y


# source config.txt
# echo $conda_env_name
# conda activate ${conda_env_name}

# tried way 1:
conda activate replication

# tried way 2:
# source ${CONDA_PREFIX}/bin/activate replication


# echo $CONDA_PREFIX

# sub=$1
# ses=$2
# acq=$3

# indir="/cbica/projects/csdsi/BIDS/qsiprep_unzipped/sub-${sub}/ses-${ses}/dwi/"
# odir="/cbica/projects/csdsi/replication/data/extrapolated/sub-${sub}/ses-${ses}/"
# # ^^ seems have to manually add `/` at the end of `indir` and `odir`

# python ../code/extrapolate_full_dsi.py ${sub} ${acq} ${indir} ${odir}