import os
import os.path as op
import pandas as pd

# grp="retro_wthn_acc"
# grp = "retro_btwn_acc_unpaired"
grp = "retro_btwn_rel"

trk="Cingulum_Frontal_Parietal_L"

list_filename = ["median_deviation.csv",
                "median_deviation_untidy.csv",
                "p_values.csv",
                "null_distribution.csv"
                ]

folder_main_output_Hamsi = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/permutation_stats/"
folder_main_output_replication = "/cbica/projects/csdsi/replication/data/dice_scores/permutation_stats/"

folder_output_Hamsi = op.join(folder_main_output_Hamsi, grp, trk)
folder_output_replication = op.join(folder_main_output_replication, grp, trk)

for i_fn in range(0, len(list_filename)):
    fn_csv_Hamsi = op.join(folder_output_Hamsi, list_filename[i_fn])
    fn_csv_replication = op.join(folder_output_replication, list_filename[i_fn])

    t_Hamsi = pd.read_csv(fn_csv_Hamsi)
    t_replication = pd.read_csv(fn_csv_replication)

    print(str(i_fn))

    # two tables should be the same:
    assert t_Hamsi.equals(t_replication)

print("")