#!/bin/bash
#$ -S /bin/bash
#$ -R y


source config.txt
echo $python_full_path

sub=$1
ses=$2
acq=$3

indir="/cbica/projects/csdsi/BIDS/qsiprep_unzipped/sub-${sub}/ses-${ses}/dwi/"
odir="/cbica/projects/csdsi/replication/data/extrapolated/sub-${sub}/ses-${ses}/"
# ^^ seems have to manually add `/` at the end of `indir` and `odir`

$python_full_path ../code/extrapolate_full_dsi.py ${sub} ${acq} ${indir} ${odir}
