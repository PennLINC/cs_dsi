#!/bin/bash

# grp="retro_wthn_acc"
# grp="retro_btwn_acc"
grp="retro_btwn_rel"

trk="Cingulum_Frontal_Parietal_L"


python_path="/cbica/projects/csdsi/miniconda3/envs/replication/bin/python"

cmd="${python_path}"
cmd+=" ../code/stats_permute_${grp}_replication.py"
cmd+=" streamlines $trk"

echo $cmd
# $cmd
