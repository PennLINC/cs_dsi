import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import distributions
import sys
import random

dtype = sys.argv[1] #Streamlines or scalars
trc = sys.argv[2] #Track or metric
cs_acqs = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]
subjects=["0001a", "1041h", "1665h", "2211h", "3058s", "4558a", "4936m", "0097p", "1043f", "1808u", "2453z", "3571z", "4662a", "4961a", "0444g", "1142k", "1853b", "2741x", "3832y", "4680i", "1145h", "2755j", "3992u", "4917f"]

if dtype == "streamlines":
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/"
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/permutation_stats/retro_btwn_rel/"
    der_met = "Dice Score"



if dtype == "scalars":
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/pearson_correlations/"
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/pearson_correlations/permutation_stats/retro_btwn_rel/"
    der_met = "PearsonR"


os.makedirs(odir+trc, exist_ok=True)

def get_median_and_null(trc, sub, acq, nperms=1000):
    # Isolate subject and create dataframes:
    sr_df = pd.read_csv(indir+"retro_fulldsi_btwn_rel/"+trc+"/all_subjects.csv")
    sr_sub = np.array(sr_df[sr_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]
    comb_df = pd.DataFrame(columns=[der_met, "Acquisition"])
    comb_df[der_met] = sr_sub
    comb_df["Acquisition"] = "Full DSI"

    acq_df = pd.read_csv(indir+"retro_btwn_rel/"+trc+"/all_subjects_"+acq+".csv")

    acq_sub = np.array(acq_df[acq_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]
    acq_sub_df = pd.DataFrame(columns=[der_met, "Acquisition"])
    acq_sub_df[der_met] = acq_sub
    acq_sub_df["Acquisition"] = acq
    comb_df = pd.concat([comb_df, acq_sub_df]).reset_index(drop=True)

    # Get true median:
    dev_arr = comb_df[comb_df["Acquisition"]=="Full DSI"][der_met] - comb_df[comb_df["Acquisition"]==acq][der_met].reset_index(drop=True)
    true_median = np.median(dev_arr)

    # Get null distribution:
    shuffled_median_arr = []
    for i in range(nperms):
        shuffled_dev_arr = [x*random.choice([-1,1]) for x in dev_arr]

        shuffled_median = np.median(shuffled_dev_arr)
        shuffled_median_arr.append(shuffled_median)
        # print(shuffled_median_arr)

    # Calculate p-value:
    falsepos_count = np.count_nonzero(shuffled_median_arr>true_median)
    p_value = falsepos_count / nperms
    if p_value > 0.5:
        falsepos_count = np.count_nonzero(shuffled_median_arr<true_median)
        p_value = falsepos_count / nperms
    if p_value == 0:
        p_value = "<"+str(1/nperms)

    return true_median, shuffled_median_arr, p_value

def get_distribution(trc, sub, plot=True, nperms=1000):
    cs_acqs = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]
    stats_df = pd.DataFrame(index=cs_acqs, columns=["Median Difference", "P-Value"])
    null_violin_df = pd.DataFrame(columns=["Median Difference", "Acquisition"])
    for acq in cs_acqs:
        acq_null_violin_df= pd.DataFrame(columns=["Median Difference", "Acquisition"])
        stats_df.loc[acq, "Median Difference"], acq_null_violin_df["Median Difference"], stats_df.loc[acq, "P-Value"] = get_median_and_null(trc, sub, acq, nperms=nperms)
        acq_null_violin_df["Acquisition"] = acq
        null_violin_df = pd.concat([null_violin_df, acq_null_violin_df])

    null_violin_df = null_violin_df.reset_index(drop=True)
    
    return null_violin_df, stats_df

def all_subs_single_trc(trc, nperms=1000):
    null_violin_dict = {}
    stats_dict = {}
    for sub in subjects:
        null_violin_df, stats_df = get_distribution(trc, sub, plot=False, nperms=nperms) 
        null_violin_dict[sub] = null_violin_df
        stats_dict[sub] = stats_df

    all_sub_null_violin_df = pd.DataFrame()
    for sub in subjects:
        all_sub_null_violin_df = pd.concat([all_sub_null_violin_df, null_violin_dict[sub]])

    all_sub_median_df = pd.DataFrame(columns=["Median Difference", "Acquisition"])
    all_sub_p_df = pd.DataFrame(columns=[cs_acqs], index=[subjects])
    all_sub_median_df_untidy = pd.DataFrame(columns=[cs_acqs], index=[subjects])


    for acq in cs_acqs:
        med_arr = []
        cs_median_df = pd.DataFrame(columns=["Median Difference", "Acquisition"])

        for sub in subjects:
            med_arr.append(stats_dict[sub].loc[acq, "Median Difference"])
            all_sub_p_df.loc[sub, acq] = stats_dict[sub].loc[acq, "P-Value"]
            all_sub_median_df_untidy.loc[sub, acq] = stats_dict[sub].loc[acq, "Median Difference"]


        cs_median_df["Median Difference"] = med_arr
        cs_median_df["Acquisition"] = acq
        all_sub_median_df = pd.concat([all_sub_median_df,cs_median_df])

    all_sub_null_violin_df = all_sub_null_violin_df.replace(["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02"], 
                            ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2"])
    cat = pd.Categorical(all_sub_null_violin_df["Acquisition"], categories = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"])
    all_sub_median_df = all_sub_median_df.replace(["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02"], 
                            ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2"])
    cat2 = pd.Categorical(all_sub_median_df["Acquisition"], categories = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"])
    
    return all_sub_null_violin_df, all_sub_median_df, all_sub_median_df_untidy, all_sub_p_df

def main():
    null_df, med_df, med_df_untidy, p_df = all_subs_single_trc(trc)
    null_df.to_csv(odir+trc+"/null_distribution.csv")
    med_df.to_csv(odir+trc+"/median_deviation.csv")
    med_df_untidy.to_csv(odir+trc+"/median_deviation_untidy.csv")
    p_df.to_csv(odir+trc+"/p_values.csv")

if __name__ == "__main__":
    main()