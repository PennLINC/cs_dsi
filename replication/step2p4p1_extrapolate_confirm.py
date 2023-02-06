# This is to check number of DWI in the bval files
import os.path as op

folder_main = "/cbica/projects/csdsi/replication/data"
folder = op.join(folder_main, "extrapolated/sub-19708/ses-1")
fn = op.join(folder, "acq-HASC55_run-01_dsi_extrapolated.bval")

with open(fn, 'r') as file:
    bval = file.read().replace("\n", "").strip().split(" ") # strip(): remove trailing space

assert(len(bval), 258) # full DSI should have 258 dirs

# also, check `mrinfo` of the generated dwi, should also have 258 vols