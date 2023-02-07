This is to replicate results reported in the manuscript.
Replicator: Chenying Zhao

# Current problems to fix:
- table 1 - number of dir in cs-dsi scheme 

# Overview
Full list of instances:
* 2 datasets: retrospective and prospective
* a few subjects
* a few sessions (only in retro dataset)
* a few CS-DSI schemes + full DSI
* 56 white matter tracts: listed in [code/streamlines_main.md](code/streamlines_main.md)

* 4 validity metrics - see [code/streamlines_main.md](code/streamlines_main.md) for corresponding flag names
    * same-scan accuracy + retro dataset 
    * inter-scan accuracy + retro dataset 
    * inter-scan reliability + retro dataset 
    * same-scan accuracy + prosp dataset


# Steps
- [step2p4p1_extrapolate.md](step2p4p1_extrapolate.md)
- [step2p4p2_GQI_recon.md](step2p4p2_GQI_recon.md)

# Tricks
## Python on csdsi:
When running in a bash file, cannot use `conda activate <env_name>`, or `source ${CONDA_PREFIX}/bin/activate <env_name>`. Below is a robust way:

```
# in a bash file:

source config.txt
# echo $python_full_path
$python_full_path test.py
```