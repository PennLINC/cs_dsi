# cs_dsi
Project folder for validating CS-DSI bundle segmentations and scalar maps. 

Pipeline matched with paper sections

## Methods

### 2.3 Preprocessing
Preprocessing was performed using [QSIPrep](https://qsiprep.readthedocs.io/en/latest/) 0.4.0:
```bash
qsiprep $bids_folder $der_folder participant \
  --stop_on_first_crash -v -v \
  --b0-motion-corr-to iterative --b0_threshold 100 --b0_to_t1w_transform Rigid \
  --dwi-denoise-window 5 \
  --hmc-model 3dSHORE --hmc-transform Affine \
  --output-resolution 1.7 --output-space T1w \
  --template MNI152NLin2009cAsym \
  --n_cpus 7 \
  --denoise-before-combining --force-spatial-normalization \
  --intramodal-template-transform BSplineSyN \
  --skull_strip_template OASIS \
  --unringing-method mrdegibbs 
```

### 2.4 CS Reconstruction
Full DSI images were extrapolated from CS_DSI schemes using the 3DSHORE basis function, with a radial order of 8 and L2 regularization.
Script in `extrapolate_full_dsi.py`

#### **GQI Reconstruction**
GQI reconstruction was performed with DSIStudio:
```bash
dsi_studio --action=src --source=${extrapolated_dsi}.nii.gz --output=${src_name}.src.gz #create src file for processing with DSI studio
dsi_studio --action=rec --source=${src_name}.src.gz --method=4 --param0=1.25 \
  --record_odf=0 --align_acpc=0 --check_btable=1 --output ${fib_name}.fib.gz #GQI reconstruction
```

### 2.5 Bundle segmentation
DSIStudio was used for automated fiber tracking (atk), and making a binary of the track file generated:
```bash
for trk in $track_list; do
dsi_studio --action=atk --source=${fib_name}.fib.gz --track_id=$trk --check_ending=0 --thread_count=1 #single thread count because parallelization fails in this version of DSIstudio
#trk_file=.trk file generated from previous step
dsi_studio --action=ana --source=${fib_name}.fib.gz --tract=${trk_file}.tt.gz --output=${trk_file}_mask.nii.gz --thread_count=1 #make binary mask of bundle
```

### 2.6 Making whole-brain scalar maps
DSIStudio was used to generate whole-brain voxel-wise maps of NQA, GFA and ISO from the fib files:
```bash
dsi_studio --action=exp --source=${fib_name}.fib.gz --export=nqa,gfa,iso
```

### 2.7 Statistical Testing
**See `code/streamlines_main.md` for analysis steps specific to streamlines generated.**

**See `code/scalars_main.md` for analysis steps specific to scalar maps generated.**

