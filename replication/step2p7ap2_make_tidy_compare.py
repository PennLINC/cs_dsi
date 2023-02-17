import os
import os.path as op
import pandas as pd

# grp="prosp_wthn_acc"
# trk = "Corpus_Callosum_Forceps_Major"

grp="retro_btwn_rel"
trk="Superior_Longitudinal_Fasciculus1_L"

filename_csv = "data_violin-friendly.csv"

folder_main_output_Hamsi = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores"
folder_main_output_replication = "/cbica/projects/csdsi/replication/data/dice_scores"

folder_output_Hamsi = op.join(folder_main_output_Hamsi, grp, trk)
folder_output_replication = op.join(folder_main_output_replication, grp, trk)

fn_csv_Hamsi = op.join(folder_output_Hamsi, filename_csv)
fn_csv_replication = op.join(folder_output_replication, filename_csv)

t_Hamsi = pd.read_csv(fn_csv_Hamsi)
t_replication = pd.read_csv(fn_csv_replication)

print(t_Hamsi.head(10)) 
print(t_replication.head(10)) 
# the diagnol of each subject's matrix is NaN, as no value was assigned to those elements


# two tables should be the same:
assert t_Hamsi.equals(t_replication)

print()