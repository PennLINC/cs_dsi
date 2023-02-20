# This is to check number of DWI in the bval files
import os.path as op

sub_id = "sub-19708"
filename = "acq-HASC55_run-01_dsi_extrapolated.bval"
filename_bvec = "acq-HASC55_run-01_dsi_extrapolated.bvec"

folder_main = "/cbica/projects/csdsi/replication/data"
folder = op.join(folder_main, "extrapolated", sub_id, "ses-1")
fn = op.join(folder, filename)
fn_bvec = op.join(folder, filename_bvec)

with open(fn, 'r') as file:
    bval = file.read().replace("\n", "").strip().split(" ") # strip(): remove trailing space
assert len(bval) == 258 # full DSI should have 258 dirs

with open(fn_bvec, 'r') as file:
    bvec = file.read().replace("\n", "").strip().split(" ") # strip(): remove trailing space
assert len(bvec) == 258 *3

# also, check `mrinfo` of the generated dwi, should also have 258 vols

# confirm it's the same as hamsi's:
folder_main_hamsi = "/cbica/projects/csdsi/BIDS/derivatives/extrapolated"
folder_hamsi = op.join(folder_main_hamsi, sub_id)
fn_hamsi = op.join(folder_hamsi, filename)
fn_hamsi_bvec = op.join(folder_hamsi, filename_bvec)

with open(fn_hamsi, 'r') as file:
    bval_hamsi = file.read().replace("\n", "").strip().split(" ") # strip(): remove trailing space
with open(fn_hamsi_bvec, 'r') as file:
    bvec_hamsi = file.read().replace("\n", "").strip().split(" ") # strip(): remove trailing space


# assert identical:
assert bval == bval_hamsi
assert bvec == bvec_hamsi

print("")