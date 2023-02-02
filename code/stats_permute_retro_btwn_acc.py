import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotnine as pn
from scipy.stats import distributions
import sys
import random

dtype = sys.argv[1] #Streamlines or scalars
trc = sys.argv[2] #Track or metric
if trc == "nqa_mask":
    ylim = [-0.1, 0.15]
if trc == "gfa_mask":
    ylim = [-0.1, 0.3]
if trc == "iso_mask":
    ylim = [-0.05, 0.05]


cs_acqs = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]
subjects=["0001a", "1041h", "1665h", "2211h", "3058s", "4558a", "4936m", "0097p", "1043f", "1808u", "2453z", "3571z", "4662a", "4961a", "0444g", "1142k", "1853b", "2741x", "3832y", "4680i", "1145h", "2755j", "3992u", "4917f"]

if dtype == "streamlines":
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/"
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/permutation_stats/retro_btwn_acc_unpaired/"
    figdir = "/cbica/projects/csdsi/cleaned_paper_analysis/figs/dice_violins/permutation_stats/retro_btwn_acc_unpaired/"
    der_met = "Dice Score"

if dtype == "scalars":
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/pearson_correlations/"
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/pearson_correlations/permutation_stats/retro_btwn_acc_unpaired/"
    figdir = "/cbica/projects/csdsi/cleaned_paper_analysis/figs/pearson_violins/permutation_stats/retro_btwn_acc_unpaired/"
    der_met = "PearsonR"

os.makedirs(odir+trc, exist_ok=True)
os.makedirs(figdir+trc, exist_ok=True)

def get_median_and_null(trc, sub, acq, nperms=1000):

    # # Isolate subject and create dataframes - original:
    # sr_df = pd.read_csv(indir+"retro_fulldsi_btwn_rel/"+trc+"/all_subjects.csv")
    # sr_sub = np.array(sr_df[sr_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]
    # comb_df = pd.DataFrame(columns=[der_met, "Acquisition"])
    # comb_df[der_met] = sr_sub
    # comb_df["Acquisition"] = "Full DSI"

    # acq_df = pd.read_csv(indir+"retro_btwn_acc/"+trc+"/all_subjects_"+acq+".csv")

    # acq_sub = np.array(acq_df[acq_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]
    # acq_sub_df = pd.DataFrame(columns=[der_met, "Acquisition"])
    # acq_sub_df[der_met] = acq_sub
    # acq_sub_df["Acquisition"] = acq
    # comb_df = pd.concat([comb_df, acq_sub_df]).reset_index(drop=True)

    # # Get true median:
    # dev_arr = comb_df[comb_df["Acquisition"]=="Full DSI"][der_met] - comb_df[comb_df["Acquisition"]==acq][der_met].reset_index(drop=True)
    # true_median = np.median(dev_arr)

    # Get null distribution - original:
    # shuffled_median_arr = []
    # for i in range(nperms):
    #     shuffled_dev_arr = [x*random.choice([-1,1]) for x in dev_arr]
    #     shuffled_median = np.median(shuffled_dev_arr)
    #     shuffled_median_arr.append(shuffled_median)

    #unpaired:
    sr_df = pd.read_csv(indir+"retro_fulldsi_btwn_rel/"+trc+"/all_subjects.csv")
    acq_df = pd.read_csv(indir+"retro_btwn_acc/"+trc+"/all_subjects_"+acq+".csv")
    sr_sub = np.array(sr_df[sr_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]
    acq_sub = np.array(acq_df[acq_df["Subject"]==sub].drop(["Unnamed: 0", "Subject"], axis=1))[np.triu_indices(8, k = 1)]


    # Get null distribution - unpaired:
     # Create tidy data:
    sr_sub_df = pd.DataFrame(columns=["Value", "Label"])
    sr_sub_df["Value"] = sr_sub
    sr_sub_df["Label"] = "Full DSI: Reliability"
    
    acq_sub_df = pd.DataFrame(columns=["Value", "Label"])
    acq_sub_df["Value"] = acq_sub
    acq_sub_df["Label"] = acq+": Accuracy"
    comb_df = pd.concat([sr_sub_df, acq_sub_df]).reset_index(drop=True)
    comb_df = comb_df.dropna()

    # Get true median:
    true_median = np.median(comb_df[comb_df["Label"]=="Full DSI: Reliability"]["Value"]) - np.median(comb_df[comb_df["Label"]==acq+": Accuracy"]["Value"])

    # Get null distribution:
    shuffled_median_arr = []
    for i in range(nperms):
        shuffled_df = pd.DataFrame()
        np.random.seed(i) #for consistency
        shuffled_df["Value"] = np.random.permutation(comb_df["Value"])  #shuffle the values
        shuffled_df["Label"] = comb_df["Label"]
        shuffled_median = np.median(shuffled_df[shuffled_df["Label"]=="Full DSI: Reliability"]["Value"]) - np.median(shuffled_df[shuffled_df["Label"]==acq+": Accuracy"]["Value"])
        shuffled_median_arr.append(shuffled_median)

    # Calculate p-value:
    falsepos_count = np.count_nonzero(shuffled_median_arr>true_median)
    p_value = falsepos_count / nperms
    if p_value > 0.5:
        falsepos_count = np.count_nonzero(shuffled_median_arr<true_median)
        p_value = falsepos_count / nperms
    if p_value == 0:
        p_value = "<"+str(1/nperms)

    return true_median, shuffled_median_arr, p_value

def get_distribution(trc, sub, plot=True, nperms=100):
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

     # Plot:
    all_sub_null_violin_df = all_sub_null_violin_df.replace(["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02"], 
                            ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2"])
    cat = pd.Categorical(all_sub_null_violin_df["Acquisition"], categories = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"])
    all_sub_median_df = all_sub_median_df.replace(["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02"], 
                            ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2"])
    cat2 = pd.Categorical(all_sub_median_df["Acquisition"], categories = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"])


    palette = ["#7781a6", "#477998", "#298e91", "#d24b4e", "#dd6d40", "#ffbf1f"]
    all_sub_null_violin_df = all_sub_null_violin_df.assign(cat = cat)
    hm = pn.ggplot(all_sub_null_violin_df, pn.aes(x=cat, y="Median Difference")) \
        + pn.geom_violin(data = all_sub_null_violin_df, size = 1.0, scale = 'width', show_legend = False, trim=True, alpha=0.5, color = "black", fill = "gray", style = "left") \
        + pn.theme_bw() \
        + pn.theme(plot_title = pn.element_text(face="bold", size=16),
                axis_title = pn.element_text(face="bold", size=14),
                axis_text_x=pn.element_text(rotation=45, hjust=1, size=12, color="black"),
                axis_text_y=pn.element_text(size=12, color="black"),
                axis_ticks = pn.element_line(size = 0.2),
                panel_border = pn.element_rect(fill = "white", colour="black"), \
                panel_grid_major = pn.element_blank(),
                panel_grid_minor = pn.element_blank()) \
        + pn.ylab("Median Difference") \
        + pn.labels.ggtitle(trc.replace("_", " ")) \
        + pn.ylim(ylim[0], ylim[1])

    # Annotate actual median diff:
    am = hm \
        + pn.geom_violin(data = all_sub_median_df, mapping = pn.aes(x=cat2, y="Median Difference", fill=cat2), color="black", size = 1.0, scale = 'width', show_legend = False, trim=True, alpha=1.0, style = "right") \
        + pn.geom_jitter(data = all_sub_median_df, mapping = pn.aes(x=cat2, y="Median Difference", fill=cat2), size=1.3, stroke=0.5, position=pn.position_jitter(0.1), show_legend=False) \
        + pn.scale_fill_manual(values=palette)


    print(am)   
    am.save(filename=figdir+trc+"/all_subs.svg", dpi=300)
    am.save(filename=figdir+trc+"/all_subs.png", dpi=300)
    
    
    return all_sub_null_violin_df, all_sub_median_df, all_sub_median_df_untidy, all_sub_p_df

def main():
    null_df, med_df, med_df_untidy, p_df = all_subs_single_trc(trc)
    null_df.to_csv(odir+trc+"/null_distribution.csv")
    med_df.to_csv(odir+trc+"/median_deviation.csv")
    med_df_untidy.to_csv(odir+trc+"/median_deviation_untidy.csv")
    p_df.to_csv(odir+trc+"/p_values.csv")

if __name__ == "__main__":
    main()