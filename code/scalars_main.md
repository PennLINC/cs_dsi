# Main analysis for scalars:
Documentation for all the analysis steps *after* getting voxel-wise scalars in subject-space. All datafiles created here will be within `/cbica/csdsi/cleaned_paper_analysis/data`

Start with setting up our terminal:
```bash
cd /cbica/projects/csdsi/cleaned_paper_analysis/code
conda activate flywheel
metrics=( nqa gfa iso )
```

All analysis follows the same design as in `streamlines_main.md`

### 1. Calculate pearson correlations.
This first step is to just calculate the pearson correlations for each analysis case and create metric specific CSVs across all participants. 
We do this in `get_pearson_correlations.py`
Just for this section, we add another analysis group: `retro_fulldsi_btwn_rel` to get the full DSI pair-wise reliability CSVs. 
1. `retro_fulldsi_btwn_rel`: Pairwise dice scores between sessions of the full DSI. 
1. `retro_wthn_acc`: Dice score between CS-DSI and full DSI for the **same session**
1. `retro_btwn_acc`: Dice score between CS-DSI and full DSI for the **pairwise sessions**
1. `prosp_wthn_acc`: Dice score between CS-DSI and full DSI for the **same session** (for the prospective data)

```bash
#Bootstrap
python get_pearson_correlations.py $grp $met
```

### 2. Make violin plots 
*figures 8 and 10*.
```bash
python make_violins_scalars.py $grp $met
```

### 3. Permutation Testing:
```bash
for met in nqa gfa iso; do
python stats_permute_retro_wthn_acc.py scalars ${met}_mask
python stats_permute_retro_btwn_acc.py scalars ${met}_mask
python stats_permute_retro_btwn_rel.py scalars ${met}_mask
done
```
