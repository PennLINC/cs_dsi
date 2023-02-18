#!/bin/bash

grp="retro_btwn_rel"

python_path="/cbica/projects/csdsi/miniconda3/envs/replication/bin/python"
${python_path} ../code/concatenate_tracks_replication.py ${grp}
