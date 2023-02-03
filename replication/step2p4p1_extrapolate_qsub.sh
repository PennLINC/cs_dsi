#!/bin/bash


sub="19708"
ses="1"
acq="HASC55_run-01"


cmd="qsub -cwd"
cmd+=" -N step2p4p1_extrap_sub-${sub}_ses-${ses}_${acq}"   # job name
cmd+=" -e /cbica/projects/csdsi/replication/data/logs"
cmd+=" -o /cbica/projects/csdsi/replication/data/logs"
cmd+=" step2p4p1_extrapolate_job.sh"
cmd+=" ${sub} ${ses} ${acq}"

echo $cmd
# $cmd