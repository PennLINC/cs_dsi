#!/bin/bash
# Run a python code on the grid
# HR February 23, 2022.

#--------------------------------------------------------------------------------------


# Setup qsub options
#$ -V ## pass all environment variables to the job
#$ -S /bin/bash ## shell where it will run this job
#$ -j y ## join error output to normal output
#$ -cwd ## Execute the job from the current working directory
#$ -l h_vmem=64G

# Log some useful stuff into that log file 
echo Started at `date` 
echo Running on $HOSTNAME 
echo USER: $USER
export OMP_NUM_THREADS=$NSLOTS
echo NSLOTS: $NSLOTS
echo JOB_NAME: $JOB_NAME
echo JOB_ID: $JOB_ID
echo JOB_SCRIPT: $JOB_SCRIPT
script=$1
code_path=/cbica/projects/csdsi/cleaned_paper_analysis/code

echo Running Python Script: $script
echo Passed Variables: $2 $3 $4 $5 $6 $7 $8 $9
# top -b -U csdsi > /cbica/projects/csdsi/BIDS/gridlog/get_odf/${2}_${3}_memory.txt
echo "Process Start - `date`"
/cbica/projects/csdsi/miniconda3/envs/flywheel/bin/python ${code_path}/$script $2 $3 $4 $5 $6 $7 $8 $9 
echo "Process Finish - `date`"
