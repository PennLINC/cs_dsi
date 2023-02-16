Step 2.7a permutation tests for streamlines

My sanity checks over step 1-2: `replication/step2p7a_checks.py`

# step 1. Get dice score
- main script: `code/get_dice_scores.py`
    - I copied it as `*_replication.py` where I changed the output dir
- very quick
- checks:
    - csv file should be identical with Hamsi's
    - the structure of csv file table should make sense
        - covering subjects, sessions, acq (for cs-dsi), etc

# step 2. Concat tracks' results
TODO: after having an minor fix of argument by Hamsi in main branch

# step 3. Violin plots
## step 3.1 violin (or csv) per track
- main script: `code/make_violins_streamlines_replication`
    - I copied it as as `*_replication.py`
- quick
- checks: see [step2p7ap3p1_violin_perTrack_compare.py](step2p7ap3p1_violin_perTrack_compare.py)
