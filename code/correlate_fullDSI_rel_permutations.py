import pandas as pd
import sys
import os
import plotnine as pn
import numpy as np
from scipy import stats
from sklearn import linear_model
import statsmodels.api as sm

grp = sys.argv[1] #Analysis group
mtrk = sys.argv[2] #Track group
if mtrk == "all_tracks":
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
if mtrk == "no_fail_tracks":
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Fornix_R", "Optic_Radiation_L", "Optic_Radiation_R", "Reticular_Tract_L", "Reticular_Tract_R", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Body", "Corpus_Callosum_Tapetum", "Corpus_Callosum_Forceps_Major"]
# acquisitions = ["Full DSI Reliability", "HASC92-55_run-01", "HASC92-55_run-02", "HASC92", "HASC55_run-01", "HASC55_run-02", "RAND57"]
cs_acquisitions = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]
indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/permutation_stats/"
odir = "/cbica/projects/csdsi/cleaned_paper_analysis/figs/streamlines_corr_fullDSI-rel/permutations/"+grp+"/"
os.makedirs(odir, exist_ok=True)

def get_median_frame():
    median_df = pd.DataFrame(index = trks)
    for trk in trks:
        indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/permutation_stats/"+grp+"/"+trk+"/"
        df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/retro_fulldsi_btwn_rel/"+trk+"/"+"/all_subjects.csv")
        median_sc = df.drop(["Unnamed: 0", "Subject"], axis=1).median().median()
        median_df.loc[trk, "Full DSI Reliability"] = median_sc
        df2 = pd.read_csv(indir+"median_deviation_untidy.csv")
        for acq in cs_acquisitions:
            median = df2[acq].median()
            median_df.loc[trk, acq] = median
    median_df.to_csv("/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/permutation_stats/"+grp+"/"+mtrk+"_medians.csv")

def get_stats_and_linregress(median_df):
    # Get line of best fit:
    fit_df = pd.DataFrame()
    r_df = pd.DataFrame(index = cs_acquisitions, columns = ["Rsq", "Slope", "p-value"]) 
    fit_df["Full DSI Reliability"] = median_df["Full DSI Reliability"]

    for acq in cs_acquisitions:
        s, i, r, p, std = stats.linregress(median_df["Full DSI Reliability"].astype(float), median_df[acq].astype(float))
        fit_df[acq] = median_df["Full DSI Reliability"]*s + i
        fit_df["raw_"+acq] = median_df[acq]
        r_df.loc[acq, "Rsq"] = r**2
        r_df.loc[acq, "Slope"] = s
        r_df.loc[acq, "p-value"] = p
    r_df.to_csv(indir+grp+"/median_tracks_slopes_with_reliability.csv")
    return fit_df

def get_figure_specs():
    if grp == "retro_wthn_acc":
        ylab = "Median Difference \n(Full DSI between scan reliability \n- CS-DSI within scan accuracy)"
    if grp == "retro_btwn_acc":
        ylab = "Median Difference \n(Full DSI between scan reliability \n- CS-DSI between scan accuracy)"
    if grp == "retro_btwn_rel":
        ylab = "Median Difference \n(Full DSI between scan reliability \n- CS-DSI between scan reliability)"
    return ylab


def main():
    if os.path.exists("/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/permutation_stats/"+grp+"/"+mtrk+"_medians.csv") == False:
        get_median_frame()
    median_df= pd.read_csv(indir+grp+"/"+mtrk+"_medians.csv")
    fit_df = get_stats_and_linregress(median_df).astype(float)
    ylab = get_figure_specs()
    fig = (pn.ggplot(data = fit_df) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_HASC92-55_run-01"), color = "#0D0808", fill = "#7781a6", alpha = 0.8, size = 1.5) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_HASC92-55_run-02"), color = "#0D0808", fill = "#477998", alpha = 0.8, size = 1.5) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_HASC92"), color = "#0D0808", fill = "#298e91", alpha = 0.8, size = 1.5) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_HASC55_run-01"), color = "#0D0808", fill = "#d24b4e", alpha = 0.8, size = 1.5) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_HASC55_run-02"), color = "#0D0808", fill = "#dd6d40", alpha = 0.8, size = 1.5) \
       + pn.geom_point(pn.aes(x = "Full DSI Reliability", y = "raw_RAND57"), color = "#0D0808", fill = "#ffbf1f", alpha = 0.8, size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "HASC92-55_run-01"), color = "#7781a6", size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "HASC92-55_run-02"), color = "#477998", size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "HASC92"), color = "#298e91", size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "HASC55_run-01"), color = "#d24b4e", size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "HASC55_run-02"), color = "#dd6d40", size = 1.5) \
       + pn.geom_line(pn.aes(x = "Full DSI Reliability", y = "RAND57"), color = "#ffbf1f", size = 1.5)) \
       + pn.theme_bw() \
       + pn.theme(plot_title = pn.element_text(face="bold", size=16), \
            axis_title = pn.element_text(face="bold", size=12), \
            axis_text_x=pn.element_text(hjust=1, size=12, color="black"), \
            axis_text_y=pn.element_text(size=12, color="black"), \
            axis_ticks = pn.element_line(size = 0.2), \
            panel_border = pn.element_rect(fill = "white", colour="black"), \
            panel_grid_major = pn.element_blank(), \
            panel_grid_minor = pn.element_blank()) \
        + pn.xlab("Full DSI Scan-rescan Reliability") + pn.ylab(ylab) \
        + pn.xlim(0.7, 0.88) + pn.ylim(-0.05, 0.18)  

        
    fig.save(filename = odir+mtrk+"_notitle_x07-88.svg", dpi=500)
    fig.save(filename = odir+mtrk+"_notitle_x07-88.png", dpi=500)

if __name__ == "__main__":
    main()



    
