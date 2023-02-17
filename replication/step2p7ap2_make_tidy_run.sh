#!/bin/bash

# grp="prosp_wthn_acc"
grp="retro_btwn_rel"

python_path="/cbica/projects/csdsi/miniconda3/envs/replication/bin/python"

cmd_python="${python_path}"
cmd_python+=" ../code/make_tidydata_streamlines_replication.py"
cmd_python+=" $grp"

echo $cmd_python
# $cmd_python