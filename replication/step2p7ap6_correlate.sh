#!/bin/bash

grp="retro_wthn_acc"
# grp="retro_btwn_acc"
# grp="retro_btwn_rel"
# grp="prosp_wthn_acc"

python_path="/cbica/projects/csdsi/miniconda3/envs/replication/bin/python"
cmd="${python_path} ../code/correlate_fullDSI_rel_replication.py ${grp}"

echo $cmd
# $cmd