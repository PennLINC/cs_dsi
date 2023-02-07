Step 2.4.2 GQI reconstruction + scalar generation

- main script: code/dsistudio_src_fib_scalars.sh
    - as i need to change the output dir, i saved it as `code/dsistudio_src_fib_scalars_replication.sh`
- very fast!
- Hamsi's output folder: `/cbica/projects/csdsi/replication/data/dsistudio_full/dsi_derivatives/`
- expected output files:
    - `*.src.gz`
    - `*.src.gz.gqi.1.25.fib.gz`  # GQI recon result, can be opened via `[Step T3 Fiber Tracking]`
        - this includes several images (see the script) that can be viewed in DSI studio. Checked the fiber orientations by following [DSI studio manual -> GQI](https://dsi-studio.labsolver.org/doc/gui_t2.html)
    - `*.src.gz.gqi.1.25.fib.gz.<scalar_name>.nii.gz`, where `<scalar_name>` = gfa, iso, nqa, qa, rdi (specified in her code)
        - viewed in itk-snap

- checked 2 subjects, one from retro, one from prosp