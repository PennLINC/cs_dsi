#!/bin/bash
#$ -S /bin/bash
#$ -R y
#$ -l h_vmem=32G

source config.txt
echo $python_full_path

sub=$1
ses=$2
acq=$3

indir="bavasub-${sub}/ses-${ses}/dwi/"
odir="/cbica/projects/csdsi/replication/data/extrapolated/sub-${sub}/ses-${ses}/"
# ^^ seems have to manually add `/` at the end of `indir` and `odir`

$python_full_path ../code/extrapolate_full_dsi.py ${sub} ${acq} ${indir} ${odir}


# actual call Hamsi used:
# qsub -o ${gridlog_path}/extrapolate/sub-${sub}_ses-s${ses}_acq-${acq}.txt -N ex-${acq}_-${sub}_${ses} -pe threaded 1-2 run_python_grid.sh extrapolate_full_dsi.py $sub $ses $acq

# would take <20min
# the log file will be ~100MB!
