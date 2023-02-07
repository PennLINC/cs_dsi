Step 2.4.1 Run extrapolation

Also see `*_job.sh` and `*_qsub.sh`

* input folder: `/cbica/projects/csdsi/BIDS/qsiprep_unzipped/`
    * this is prosp dataset
* output folder: `/cbica/projects/csdsi/replication/data/`
* log folder: `/cbica/projects/csdsi/replication/data/logs`

How to run:
- in `replication` folder, `bash step2p4p1_extrapolate_qsub.sh`. Copy the command to a terminal.

Run thru:
- sub="19708"
ses="1"
acq="HASC55_run-01"
- Successful job log:
`step2p4p1_extrap_sub-19708_ses-1_HASC55_run-01.o3661526`
- download to local computer to view in MRView, saw valid dwi image
- confirmed that generated DSI images have 258 dirs (in `mrinfo`, also bvals have 258 dirs)

Checks:
- params are the same as those in MS section 2.4
