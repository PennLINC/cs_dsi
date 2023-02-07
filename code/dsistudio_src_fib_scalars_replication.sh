#!/bin/bash
# Setup qsub options
#$ -V ## pass all environment variables to the job
#$ -S /bin/bash ## shell where it will run this job
#$ -j y ## join error output to normal output
#$ -cwd ## Execute the job from the current working directory
#$ -l h_vmem=32G

# Log some useful stuff into that log file 
echo Started at `date` 
echo Running on $HOSTNAME 
echo USER: $USER
export OMP_NUM_THREADS=$NSLOTS
echo NSLOTS: $NSLOTS
echo JOB_NAME: $JOB_NAME
echo JOB_ID: $JOB_ID
echo JOB_SCRIPT: $JOB_SCRIPT

sing="singularity exec -B /cbica/projects/csdsi:/cbica/projects/csdsi -B /cbica/projects/csdsi/tmp:/tmp /cbica/projects/csdsi/BIDS/singularity/dsistudio_052322.sif" #need to update with the latest singularity, and also change mount directories.

grp=$1
sub=$2
ses=$3
acq=$4
orig_dsi=/cbica/projects/csdsi/dsistudio_full/${grp}/sub-${sub}/ses-${ses}/sub-${sub}_ses-${ses}_acq-${acq}_dwi
# ^^ CZ: this includes both retro and prospective datasets

# out_dir=/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/
# replication out dir:
out_dir="/cbica/projects/csdsi/replication/data/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/"
mkdir -p ${out_dir}

out_src=${out_dir}/sub-${sub}_ses-${ses}_acq-${acq}_dwi

## Generate dsistudio source file:
if [ ! -e ${out_src}.src.gz ]; then
$sing dsi_studio --action=src --source=${orig_dsi}.nii.gz --output=${out_src}.src.gz
fi

## Reconstruct:
if [ ! -e ${out_src}.src.gz.gqi.1.25.fib.gz ]; then
$sing dsi_studio --action=rec --source=${out_src}.src.gz --method=4 --param0=1.25 --record_odf=0 --other_output=qa,nqa,dti_fa,md,ad,rd,gfa,iso,rdi --align_acpc=0 --check_btable=1
fi

## Get scalars from reconstruction:
$sing dsi_studio --action=exp --source=${out_src}.src.gz.gqi.1.25.fib.gz --export=qa,nqa,gfa,iso,rdi