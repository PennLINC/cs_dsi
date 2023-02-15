import os
import os.path as op
import pandas as pd

grp = "retro_fulldsi_btwn_rel"
filename_csv = "all_subjects.csv"

grp = "retro_btwn_acc"
acq = "HASC55_run-01"
filename_csv = "all_subjects_" + acq + ".csv"

trk = "Corpus_Callosum_Body"


folder_main_output = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores"

fn_pertrack_csv = op.join(folder_main_output, grp, trk, filename_csv)
t_pertrack = pd.read_csv(fn_pertrack_csv)

fn_concattrack_csv = op.join(folder_main_output, grp, "all_tracks", filename_csv)
t_concattrack = pd.read_csv(fn_concattrack_csv)

print("")