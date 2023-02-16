import os
import os.path as op
import pandas as pd

# ++++++++++++++++++++++++++++++++++++++
# by grp:
# grp = "retro_fulldsi_btwn_rel"
# filename_pertrack_csv = "all_subjects.csv"

# grp = "retro_wthn_acc"
# filename_pertrack_csv = "all_sessions.csv"

# grp = "retro_btwn_acc"
# acq = "RAND57"
# filename_pertrack_csv = "all_subjects_" + acq + ".csv"

# grp = "retro_btwn_rel"
# acq = "RAND57"
# filename_pertrack_csv =  "all_subjects_" + acq + ".csv"

grp = "prosp_wthn_acc"
filename_pertrack_csv = "ses-1_ind.csv"

# for trk:
trk = "Corpus_Callosum_Body"
# ++++++++++++++++++++++++++++++++++++++

filename_tidy_pertrack_csv = "data_violin-friendly.csv"
filename_concattrack_csv = "data_violin-friendly.csv"

folder_main_output = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores"

fn_pertrack_csv = op.join(folder_main_output, grp, trk, filename_pertrack_csv)
t_pertrack = pd.read_csv(fn_pertrack_csv)

fn_tidy_pertrack_csv = op.join(folder_main_output, grp, trk, filename_tidy_pertrack_csv)
t_tidy_pertrack = pd.read_csv(fn_tidy_pertrack_csv)

fn_concattrack_csv = op.join(folder_main_output, grp, "all_tracks", filename_concattrack_csv)
t_concattrack = pd.read_csv(fn_concattrack_csv)

# assert: the expected "look": symmetric? only half?
t_pertrack.head(10)

# assert: number of rows:
t_pertrack.shape[0]

# assert: input of step 2 (i.e., output of step 1) should match with output of step 2:
t_tidy_pertrack.tail(10)   # output of step 2
t_pertrack.tail(10)     # input of step 2ste



print("")