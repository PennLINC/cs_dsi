#!/bin/bash
# Setup qsub options
#$ -S /bin/bash ## shell where it will run this job
#$ -j y ## join error output to normal output
#$ -cwd ## Execute the job from the current working directory
#$ -l h_vmem=64G 
#$ -l h_stack=8m


# Log some useful stuff into that log file 
echo Started at `date` 
echo Running on $HOSTNAME 
echo USER: $USER
echo NSLOTS: $NSLOTS
echo JOB_NAME: $JOB_NAME
echo JOB_ID: $JOB_ID
echo JOB_SCRIPT: $JOB_SCRIPT

grp=$1
sub=$2
ses=$3
acq=$4
orig_fib=/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.src.gz.gqi.1.25.fib.gz

# Copy everything over to the temp directory (.fib file and dsistudio singularity):
echo Temp at: ${CBICA_TMPDIR}
cp /cbica/projects/csdsi/BIDS/singularity/dsistudio_052322.sif ${CBICA_TMPDIR}/dsistudio_052322.sif #need to update with the latest singularity
cp ${orig_fib} ${CBICA_TMPDIR} #just the fib file

sing="singularity exec -B ${CBICA_TMPDIR}:${CBICA_TMPDIR} ${CBICA_TMPDIR}/dsistudio_052322.sif"
fib=${CBICA_TMPDIR}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.src.gz.gqi.1.25.fib.gz

echo Running DSI Studio Bundle making on sub-${sub} ses-${ses} acq-${acq}

# Make tracks, doing each track individually to facilitate rerunning of failed tracks. Could also run things at once outside the for loop, and without the --track_id option:
for trk in Arcuate_Fasciculus_L Arcuate_Fasciculus_R Cingulum_Frontal_Parahippocampal_L Cingulum_Frontal_Parahippocampal_R Cingulum_Frontal_Parietal_L Cingulum_Frontal_Parietal_R Cingulum_Parahippocampal_L Cingulum_Parahippocampal_Parietal_L Cingulum_Parahippocampal_Parietal_R Cingulum_Parahippocampal_R Cingulum_Parolfactory_L Cingulum_Parolfactory_R Corpus_Callosum_Body Corpus_Callosum_Forceps_Major Corpus_Callosum_Forceps_Minor Corpus_Callosum_Tapetum Corticospinal_Tract_L Corticospinal_Tract_R Corticostriatal_Tract_Anterior_L Corticostriatal_Tract_Anterior_R Corticostriatal_Tract_Posterior_L Corticostriatal_Tract_Posterior_R Corticostriatal_Tract_Superior_L Corticostriatal_Tract_Superior_R Fornix_L Fornix_R Frontal_Aslant_Tract_L Frontal_Aslant_Tract_R Inferior_Fronto_Occipital_Fasciculus_L Inferior_Fronto_Occipital_Fasciculus_R Inferior_Longitudinal_Fasciculus_L Inferior_Longitudinal_Fasciculus_R Middle_Longitudinal_Fasciculus_L Middle_Longitudinal_Fasciculus_R Optic_Radiation_L Optic_Radiation_R Parietal_Aslant_Tract_L Parietal_Aslant_Tract_R Reticular_Tract_L Reticular_Tract_R Superior_Longitudinal_Fasciculus1_L Superior_Longitudinal_Fasciculus1_R Superior_Longitudinal_Fasciculus2_L Superior_Longitudinal_Fasciculus2_R Superior_Longitudinal_Fasciculus3_L Superior_Longitudinal_Fasciculus3_R Thalamic_Radiation_Anterior_L Thalamic_Radiation_Anterior_R Thalamic_Radiation_Posterior_L Thalamic_Radiation_Posterior_R Thalamic_Radiation_Superior_L Thalamic_Radiation_Superior_R Uncinate_Fasciculus_L Uncinate_Fasciculus_R Vertical_Occipital_Fasciculus_L Vertical_Occipital_Fasciculus_R; do
if [ ! -e /cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/${trk}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.${trk}.tt.gz ]; then

# Automated fiber tracking:
$sing dsi_studio --action=atk --source=${fib} --check_ending=0 --track_id=$trk --thread_count=1 #single thread count because parallelization fails

# Convert bundle to binary mask:
trk_file=${CBICA_TMPDIR}/${trk}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.${trk}
$sing dsi_studio --action=ana --source=${fib} --tract=${trk_file}.tt.gz --output=${trk_file}_mask.nii.gz --thread_count=1 

# Copy over contents from temp directory:
cp -r ${CBICA_TMPDIR}/${trk}/ /cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/
# rm -r ${CBICA_TMPDIR}/${trk}
fi; done

# Record failed runs from tracking:
for trk in Arcuate_Fasciculus_L Arcuate_Fasciculus_R Cingulum_Frontal_Parahippocampal_L Cingulum_Frontal_Parahippocampal_R Cingulum_Frontal_Parietal_L Cingulum_Frontal_Parietal_R Cingulum_Parahippocampal_L Cingulum_Parahippocampal_Parietal_L Cingulum_Parahippocampal_Parietal_R Cingul≈um_Parahippocampal_R Cingulum_Parolfactory_L Cingulum_Parolfactory_R Corpus_Callosum_Body Corpus_Callosum_Forceps_Major Corpus_Callosum_Forceps_Minor Corpus_Callosum_Tapetum Corticospinal_Tract_L Corticospinal_Tract_R Corticostriatal_Tract_Anterior_L Corticostriatal_Tract_Anterior_R Corticostriatal_Tract_Posterior_L Corticostriatal_Tract_Posterior_R Corticostriatal_Tract_Superior_L Corticostriatal_Tract_Superior_R Fornix_L Fornix_R Frontal_Aslant_Tract_L Frontal_Aslant_Tract_R Inferior_Fronto_Occipital_Fasciculus_L Inferior_Fronto_Occipital_Fasciculus_R Inferior_Longitudinal_Fasciculus_L Inferior_Longitudinal_Fasciculus_R Middle_Longitudinal_Fasciculus_L Middle_Longitudinal_Fasciculus_R Optic_Radiation_L Optic_Radiation_R Parietal_Aslant_Tract_L Parietal_Aslant_Tract_R Reticular_Tract_L Reticular_Tract_R Superior_Longitudinal_Fasciculus1_L Superior_Longitudinal_Fasciculus1_R Superior_Longitudinal_Fasciculus2_L Superior_Longitudinal_Fasciculus2_R Superior_Longitudinal_Fasciculus3_L Superior_Longitudinal_Fasciculus3_R Thalamic_Radiation_Anterior_L Thalamic_Radiation_Anterior_R Thalamic_Radiation_Posterior_L Thalamic_Radiation_Posterior_R Thalamic_Radiation_Superior_L Thalamic_Radiation_Superior_R Uncinate_Fasciculus_L Uncinate_Fasciculus_R Vertical_Occipital_Fasciculus_L Vertical_Occipital_Fasciculus_R; do
if [ ! -s /cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/${trk}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.${trk}.tt.gz ]; then
echo ERROR: $trk bundle making failed.
echo $grp $sub $ses $acq $trk >> ${code_path}/cleaned/failed_bundle_tracking.txt
fi; done 

# Record failed runs from masking:
for trk in Arcuate_Fasciculus_L Arcuate_Fasciculus_R Cingulum_Frontal_Parahippocampal_L Cingulum_Frontal_Parahippocampal_R Cingulum_Frontal_Parietal_L Cingulum_Frontal_Parietal_R Cingulum_Parahippocampal_L Cingulum_Parahippocampal_Parietal_L Cingulum_Parahippocampal_Parietal_R Cingulum_Parahippocampal_R Cingulum_Parolfactory_L Cingulum_Parolfactory_R Corpus_Callosum_Body Corpus_Callosum_Forceps_Major Corpus_Callosum_Forceps_Minor Corpus_Callosum_Tapetum Corticospinal_Tract_L Corticospinal_Tract_R Corticostriatal_Tract_Anterior_L Corticostriatal_Tract_Anterior_R Corticostriatal_Tract_Posterior_L Corticostriatal_Tract_Posterior_R Corticostriatal_Tract_Superior_L Corticostriatal_Tract_Superior_R Fornix_L Fornix_R Frontal_Aslant_Tract_L Frontal_Aslant_Tract_R Inferior_Fronto_Occipital_Fasciculus_L Inferior_Fronto_Occipital_Fasciculus_R Inferior_Longitudinal_Fasciculus_L Inferior_Longitudinal_Fasciculus_R Middle_Longitudinal_Fasciculus_L Middle_Longitudinal_Fasciculus_R Optic_Radiation_L Optic_Radiation_R Parietal_Aslant_Tract_L Parietal_Aslant_Tract_R Reticular_Tract_L Reticular_Tract_R Superior_Longitudinal_Fasciculus1_L Superior_Longitudinal_Fasciculus1_R Superior_Longitudinal_Fasciculus2_L Superior_Longitudinal_Fasciculus2_R Superior_Longitudinal_Fasciculus3_L Superior_Longitudinal_Fasciculus3_R Thalamic_Radiation_Anterior_L Thalamic_Radiation_Anterior_R Thalamic_Radiation_Posterior_L Thalamic_Radiation_Posterior_R Thalamic_Radiation_Superior_L Thalamic_Radiation_Superior_R Uncinate_Fasciculus_L Uncinate_Fasciculus_R Vertical_Occipital_Fasciculus_L Vertical_Occipital_Fasciculus_R; do
if [ ! -s /cbica/projects/csdsi/dsistudio_full/dsi_derivatives/${grp}/sub-${sub}/ses-${ses}/acq-${acq}/${trk}/sub-${sub}_ses-${ses}_acq-${acq}_dwi.${trk}_mask.nii.gz ]; then
echo ERROR: $trk bundle masking failed.
echo $grp $sub $ses $acq $trk >> ${code_path}/cleaned/failed_bundle_masking.txt
fi; done 

echo Ended at `date` 

# Cubic call:
# grp=crash_retro
# mkdir -p /cbica/projects/csdsi/dsistudio_full/gridlog/dsistudio_bundles/${grp}
# for sub in 0001a 1041h 1665h 2211h 3058s 4558a 4936m 0097p 1043f 1808u 2453z 3571z 4662a 4961a 0444g 1142k 1853b 2741x 3832y 4680i 1145h 2027j 2755j 3992u 4917f; do
# for ses in 1 2 3 4 5 6 7 8; do
# for acq in HASC92 HASC55_run-01 HASC55_run-02 RAND57 HASC92-55_run-01 HASC92-55_run-02 combined; do
# qsub -o /cbica/projects/csdsi/dsistudio_full/gridlog/dsistudio_bundles/${grp}/sub-${sub}_ses-${ses}_acq-${acq}.txt -N ${acq}${sub}-${ses} -pe threaded 1 /cbica/projects/csdsi/BIDS/code/cleaned/dsistudio_bundles.sh $grp $sub $ses $acq
# done; done; done

