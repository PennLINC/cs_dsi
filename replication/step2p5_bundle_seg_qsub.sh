#!/bin/bash

# grp="crash_retro"
# sub="4961a"
# ses="2"
# acq="RAND57"
# trk="Arcuate_Fasciculus_L"

grp="crash_retro"
sub="0001a"
ses="1"
acq="HASC92-55_run-01"
trk="Inferior_Fronto_Occipital_Fasciculus_L"


folder_logs="/cbica/projects/csdsi/replication/data/logs"

cmd="qsub -cwd"
cmd+=" -N step2p5_bundle_sub-${sub}_ses-${ses}_${acq}_${trk}"   # job name
cmd+=" -e /cbica/projects/csdsi/replication/data/logs"
cmd+=" -o /cbica/projects/csdsi/replication/data/logs"
cmd+=" ../code/dsistudio_bundles_replication.sh $grp $sub $ses $acq $trk"

echo $cmd
# $cmd

# full list of trk:
# Arcuate_Fasciculus_L Arcuate_Fasciculus_R Cingulum_Frontal_Parahippocampal_L Cingulum_Frontal_Parahippocampal_R Cingulum_Frontal_Parietal_L Cingulum_Frontal_Parietal_R Cingulum_Parahippocampal_L Cingulum_Parahippocampal_Parietal_L Cingulum_Parahippocampal_Parietal_R Cingulum_Parahippocampal_R Cingulum_Parolfactory_L Cingulum_Parolfactory_R Corpus_Callosum_Body Corpus_Callosum_Forceps_Major Corpus_Callosum_Forceps_Minor Corpus_Callosum_Tapetum Corticospinal_Tract_L Corticospinal_Tract_R Corticostriatal_Tract_Anterior_L Corticostriatal_Tract_Anterior_R Corticostriatal_Tract_Posterior_L Corticostriatal_Tract_Posterior_R Corticostriatal_Tract_Superior_L Corticostriatal_Tract_Superior_R Fornix_L Fornix_R Frontal_Aslant_Tract_L Frontal_Aslant_Tract_R Inferior_Fronto_Occipital_Fasciculus_L Inferior_Fronto_Occipital_Fasciculus_R Inferior_Longitudinal_Fasciculus_L Inferior_Longitudinal_Fasciculus_R Middle_Longitudinal_Fasciculus_L Middle_Longitudinal_Fasciculus_R Optic_Radiation_L Optic_Radiation_R Parietal_Aslant_Tract_L Parietal_Aslant_Tract_R Reticular_Tract_L Reticular_Tract_R Superior_Longitudinal_Fasciculus1_L Superior_Longitudinal_Fasciculus1_R Superior_Longitudinal_Fasciculus2_L Superior_Longitudinal_Fasciculus2_R Superior_Longitudinal_Fasciculus3_L Superior_Longitudinal_Fasciculus3_R Thalamic_Radiation_Anterior_L Thalamic_Radiation_Anterior_R Thalamic_Radiation_Posterior_L Thalamic_Radiation_Posterior_R Thalamic_Radiation_Superior_L Thalamic_Radiation_Superior_R Uncinate_Fasciculus_L Uncinate_Fasciculus_R Vertical_Occipital_Fasciculus_L Vertical_Occipital_Fasciculus_R;

# Hamsi's qsub:
# qsub -o /cbica/projects/csdsi/dsistudio_full/gridlog/dsistudio_bundles/${grp}/sub-${sub}_ses-${ses}_acq-${acq}.txt -N ${acq}${sub}-${ses} -pe threaded 1 /cbica/projects/csdsi/BIDS/code/cleaned/dsistudio_bundles.sh $grp $sub $ses $acq

