Step 2.5 bundle segmentation

- main script: `code/dsistudio_bundles.sh`
    - i deleted the for loop (but add argument of `trk`), and changed the output dir: `code/dsistudio_bundles_replication.sh`
    - ref: DSI studio `--action=atk` and `--action=ana`: https://sites.google.com/a/labsolver.org/dsi-studio/Manual/command-line-for-dsi-studio#TOC-Fiber-tracking
    - ref: DSI studio `--action=atk` 
        - detailed explanation: https://dsi-studio.labsolver.org/doc/cli_atk.html
        - using CLI: https://dsi-studio.labsolver.org/doc/cli_atk.html
    - ref: min and max fiber length: https://dsi-studio.labsolver.org/doc/cli_t3.html -> conventional tracking
- only took several minutes for one track
- expected outputs:
    - *.tt.gz   # track
    - *_mask.nii.gz    # track mask
    - *.stat.txt   # some stats regarding this track