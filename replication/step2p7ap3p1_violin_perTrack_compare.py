import os
import os.path as op
import pandas as pd

grp="retro_btwn_rel"
trk="Uncinate_Fasciculus_R"   # a specific track
filename_csv = "data_violin-friendly.csv"
filename_csv_input = "all_subjects_RAND57.csv"

folder_main_output_Hamsi = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores"
folder_main_output_replication = "/cbica/projects/csdsi/replication/data/dice_scores"

folder_output_Hamsi = op.join(folder_main_output_Hamsi, grp, trk)
folder_output_replication = op.join(folder_main_output_replication, grp, trk)

fn_csv_Hamsi = op.join(folder_output_Hamsi, filename_csv)
fn_csv_replication = op.join(folder_output_replication, filename_csv)
fn_csv_Hamsi_input = op.join(folder_output_Hamsi, filename_csv_input)

t_Hamsi = pd.read_csv(fn_csv_Hamsi)
t_replication = pd.read_csv(fn_csv_replication)
t_Hamsi_input = pd.read_csv(fn_csv_Hamsi_input)

print(t_replication.tail(10)) 
print(t_Hamsi_input.tail(6))
# ^^ another assert: tail of `t_replication` should come from the last line of `t_Hamsi_input`
# and there should not be duplications in `t_replication`

assert t_Hamsi.equals(t_replication)

print("")