#!/bin/bash

grp="retro_btwn_rel"
trk="Uncinate_Fasciculus_R"   # a specific track

# grp="retro_btwn_acc"
# trk="Thalamic_Radiation_Anterior_L"

folder_logs="/cbica/projects/csdsi/replication/data/logs"

cmd="qsub"
cmd+=" -N step2p7ap3p1_violin_perTrack_${grp}_${trk}"    # job name
cmd+=" -e ${folder_logs}"
cmd+=" -o ${folder_logs}"
cmd+=" -pe threaded 1-2"
cmd+=" ../code/run_python_grid_replication.sh"
cmd+=" make_violins_streamlines_replication.py"
cmd+=" $grp $trk False"

echo $cmd
# $cmd

# Hamsi's qsub call:
# qsub -o /cbica/projects/csdsi/cleaned_paper_analysis/logs/make_violins_streamlines/${grp}/${trk}.txt -N ${grp}_${trk} -pe threaded 1-2 /cbica/projects/csdsi/cleaned_paper_analysis/code/run_python_grid.sh make_violins_streamlines.py $grp $trk False

# way 2: directly call python file:
python_path="/cbica/projects/csdsi/miniconda3/envs/replication/bin/python"

cmd_python="${python_path}"
cmd_python+=" ../code/make_violins_streamlines_replication.py"
cmd_python+=" $grp $trk False"

echo $cmd_python
# $cmd_python