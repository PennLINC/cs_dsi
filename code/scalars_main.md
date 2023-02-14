# Main analysis for scalars:
Documentation for all the analysis steps *after* getting voxel-wise scalars in subject-space. All datafiles created here will be within `/cbica/csdsi/cleaned_paper_analysis/data`

Start with setting up our terminal:
```bash
cd /cbica/projects/csdsi/cleaned_paper_analysis/code/bug_fix
conda activate flywheel
metrics=( nqa gfa iso )
```

All analysis follows the same design as in `streamlines_main.md`. Bug fixes follow the exact same logic as well. 

**BUG FIX: On lines 73 and 144: Deleted lower triangle of matrix for reliability cases so that pair-wise values are not repeated.**


**EDIT: Lines 120-121: Wasn't a bug, but asserting that same-scan accuracy values were not in between-scan accuracy table**
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
grps=( retro_fulldsi_btwn_rel retro_wthn_acc retro_btwn_acc retro_btwn_rel prosp_wthn_acc )
for grp in "${grps[@]}"; do
for met in "${metrics[@]}"; do
python get_pearson_correlations.py $grp $met
done; done
```

### 2. Make violin plots 
*figures 8 and 10*.

#### Making tidy data first, same logic as before.
Look at `"/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_scalars.csv"` to check results. Difference should be 0 for all instances. 
```bash
grps=( retro_wthn_acc retro_btwn_acc retro_btwn_rel prosp_wthn_acc )
for grp in "${grps[@]}"; do
python make_tidydata_scalars.py $grp #first tidy up
done
```

Make violin plot. 
```bash
for grp in "${grps[@]}"; do
for met in "${metrics[@]}"; do
python make_violins_scalars.py $grp $met
done; done
```

### 3. Permutation Testing:
**BUG FIX: Line 36 on inter-scan accuracy, to include all pairs. 8P2 instead of 8C2.**
```bash
for met in nqa gfa iso; do
python stats_permute_retro_wthn_acc.py scalars ${met}_mask
python stats_permute_retro_btwn_acc.py scalars ${met}_mask
python stats_permute_retro_btwn_rel.py scalars ${met}_mask
done

grps=( retro_wthn_acc retro_btwn_acc_unpaired retro_btwn_rel )
for grp in "${grps[@]}"; do
for met in nqa gfa iso; do
python scalars_permutation_stats.py $grp ${met}_mask
done; done
```
#### Supplementary tables are made in [Supplementary Tables.ipynb](https://github.com/PennLINC/cs_dsi/blob/bug_fix/code/Supplementary%20Tables.ipynb)
