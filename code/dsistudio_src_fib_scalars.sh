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

out_dir=/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/
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


# Cubic call:
# grp=crash_retro
# mkdir -p /cbica/projects/csdsi/dsistudio_full/gridlog/dsistudio_src_fib_scalars/${grp}
# for sub in 0001a 1041h 1665h 2211h 3058s 4558a 4936m 0097p 1043f 1808u 2453z 3571z 4662a 4961a 0444g 1142k 1853b 2741x 3832y 4680i 1145h 2027j 2755j 3992u 4917f; do
# for ses in 1 2 3 4 5 6 7 8; do
# for acq in HASC92 HASC55_run-01 HASC55_run-02 RAND57 HASC92-55_run-01 HASC92-55_run-02 combined; do
# qsub -o /cbica/projects/csdsi/dsistudio_full/gridlog/dsistudio_src_fib_scalars/${grp}/sub-${sub}_ses-${ses}_acq-${acq}.txt -N ${acq}${sub}-${ses} -pe threaded 1-2 /cbica/projects/csdsi/BIDS/code/cleaned/dsistudio_src_fib_scalars.sh $grp $sub $ses $acq
# done; done; done
