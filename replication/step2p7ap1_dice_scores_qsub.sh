#!/bin/bash

# grp="retro_fulldsi_btwn_rel"
# trk="Corpus_Callosum_Body"

# grp="retro_wthn_acc"
# trk="Corticostriatal_Tract_Anterior_L"

grp="prosp_wthn_acc"
trk="Cingulum_Parahippocampal_R"


folder_logs="/cbica/projects/csdsi/replication/data/logs"

cmd="qsub"
cmd+=" -N step2p7ap1_dice_scores_${grp}_${trk}"    # job name
cmd+=" -e ${folder_logs}"
cmd+=" -o ${folder_logs}"
cmd+=" -pe threaded 1-2"
cmd+=" ../code/run_python_grid_replication.sh"
cmd+=" get_dice_scores_replication.py"
cmd+=" ${grp} ${trk}"

echo $cmd
# $cmd