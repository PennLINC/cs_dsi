#!/bin/bash

# grp="crash_retro"
# sub="4558a"
# ses="6"
# acq="HASC55_run-02"

grp="prospective"
sub="20909"
ses="1"
acq="HASC92-55_run-01"

folder_logs="/cbica/projects/csdsi/replication/data/logs"

cmd="qsub -cwd"
cmd+=" -N step2p4p2_gqi_sub-${sub}_ses-${ses}_${acq}"   # job name
cmd+=" -e /cbica/projects/csdsi/replication/data/logs"
cmd+=" -o /cbica/projects/csdsi/replication/data/logs"
cmd+=" -pe threaded 1-2"
cmd+=" ../code/dsistudio_src_fib_scalars_replication.sh $grp $sub $ses $acq"

echo $cmd
# $cmd