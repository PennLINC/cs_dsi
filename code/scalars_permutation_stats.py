import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotnine as pn
from scipy.stats import distributions
import sys

indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/pearson_correlations/permutation_stats/"
cs_acqs = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"]

grp = sys.argv[1]
metric = sys.argv[2]

datagrp = grp.split("_")[0]
if datagrp == "retro":
    subjects = ["0001a", "1041h", "1665h", "2211h", "3058s", "4558a", "4936m", "0097p", "1043f", "1808u", "2453z", "3571z", "4662a", "4961a", "0444g", "1142k", "1853b", "2741x", "3832y", "4680i", "1145h", "2755j", "3992u", "4917f"]
if datagrp == "prosp":
    subjects = ["001", "19779", "20594", "20645", "20698", "20792", "20872", "15852", "19902", "20597", "20676", "20706", "20804", "20909", "19708", "20543", "20642", "20687", "20708", "20840"]
    

def get_stats_df(grp, metric):
    os.makedirs(indir+grp+"/"+metric, exist_ok=True)
           
    all_null_df = pd.DataFrame()
    stats_df = pd.DataFrame(columns=["Acquisition", "Subject Median", "p-value"])
    null_df = pd.read_csv(indir+grp+"/"+metric+"/null_distribution.csv")
    med_df = pd.read_csv(indir+grp+"/"+metric+"/median_deviation.csv")
    all_null_df = pd.concat([all_null_df, null_df])
    for acq in cs_acqs:
        acq_med = med_df[med_df["Acquisition"]==acq]["Median Difference"].median()
        null_medians = null_df[null_df["Acquisition"]==acq]["Median Difference"]
        # FIX: Get p-value: #https://thomasleeper.com/Rcourse/Tutorials/permutationtests.html
        falsepos_count = np.count_nonzero(np.abs(null_medians)>np.abs(acq_med)) #taking the absolute value instead.
        p_value = falsepos_count / null_medians.shape[0]
        stats_df = pd.concat([stats_df, pd.DataFrame([[metric, acq, acq_med, p_value]], columns=["Track", "Acquisition", "Subject Median", "p-value"])])
    stats_df.to_csv(indir+grp+"/"+metric+"/subject_medians_all_stats.csv")
    return stats_df, all_null_df.sample(frac=0.1)

def get_prop_p(grp, metric, stats_df):

    allmetric_p_df = pd.DataFrame(index=cs_acqs, columns=["Median Median Difference", "p < 0.05", "p < 0.01", "p < 0.001"])
    for acq in cs_acqs:
        acq_med_max = np.max(stats_df[stats_df["Acquisition"]==acq]["Subject Median"])
        allmetric_p_df.loc[acq, "Maximum Median Difference"] = acq_med_max
        acq_med = stats_df[stats_df["Acquisition"]==acq]["Subject Median"].median()
        allmetric_p_df.loc[acq, "Median Median Difference"] = acq_med

        # Get p-value props:
        p_values = stats_df[stats_df["Acquisition"]==acq]["p-value"].astype(float)
        allmetric_p_df.loc[acq, "p < 0.05"] = np.count_nonzero([p_values < 0.05]) / len(subjects)
        allmetric_p_df.loc[acq, "p < 0.01"] = np.count_nonzero([p_values < 0.01]) / len(subjects)
        allmetric_p_df.loc[acq, "p < 0.001"] = np.count_nonzero([p_values < 0.001]) / len(subjects)

    allmetric_p_df.to_csv(indir+grp+"/"+metric+"/tracks_summary_proportionandmax.csv")
    return(allmetric_p_df)
    
    
def main():
    stats_df, all_null_df = get_stats_df(grp, metric)
    get_prop_p(grp, metric, stats_df)

if __name__ == "__main__":
    main()
