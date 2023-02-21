import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotnine as pn
from scipy.stats import distributions
import sys
indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/permutation_stats/"
cs_acqs = ["HA-SC92+55-1", "HA-SC92+55-2",  "HA-SC92", "HA-SC55-1",  "HA-SC55-2", "RAND57"]
grp = sys.argv[1]
def get_stats_df(grp):
    os.makedirs(indir+grp+"/all_tracks/", exist_ok=True)
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
        
    all_null_df = pd.DataFrame()
    stats_df = pd.DataFrame(columns=["Track", "Acquisition", "Subject Median", "p-value"])
    for trk in trks:
        print(trk)
        null_df = pd.read_csv(indir+grp+"/"+trk+"/null_distribution.csv")

        med_df = pd.read_csv(indir+grp+"/"+trk+"/median_deviation.csv")
        all_null_df = pd.concat([all_null_df, null_df])
        for acq in cs_acqs:
            acq_med = med_df[med_df["Acquisition"]==acq]["Median Difference"].median()
            null_medians = null_df[null_df["Acquisition"]==acq]["Median Difference"]
            print(null_medians.shape)
            # FIX: Get p-value: #https://thomasleeper.com/Rcourse/Tutorials/permutationtests.html
            falsepos_count = np.count_nonzero(np.abs(null_medians)>np.abs(acq_med)) #taking the absolute value instead.
            p_value = falsepos_count / null_medians.shape[0]
            stats_df = pd.concat([stats_df, pd.DataFrame([[trk, acq, acq_med, p_value]], columns=["Track", "Acquisition", "Subject Median", "p-value"])])
    stats_df.to_csv(indir+grp+"/all_tracks/subject_medians_all_stats.csv")
    return stats_df, all_null_df.sample(frac=0.1)

def get_prop_p(grp, stats_df):
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
     
    alltrk_p_df = pd.DataFrame(index=cs_acqs, columns=["Median Median Difference", "p < 0.05", "p < 0.01", "p < 0.001"])
    for acq in cs_acqs:
        acq_med_max = np.max(stats_df[stats_df["Acquisition"]==acq]["Subject Median"])
        alltrk_p_df.loc[acq, "Maximum Median Difference"] = acq_med_max
        acq_med = stats_df[stats_df["Acquisition"]==acq]["Subject Median"].median()
        alltrk_p_df.loc[acq, "Median Median Difference"] = acq_med

        # Get p-value props:
        p_values = stats_df[stats_df["Acquisition"]==acq]["p-value"].astype(float)
        alltrk_p_df.loc[acq, "p < 0.05"] = np.count_nonzero([p_values < 0.05]) / len(trks)
        alltrk_p_df.loc[acq, "p < 0.01"] = np.count_nonzero([p_values < 0.01]) / len(trks)
        alltrk_p_df.loc[acq, "p < 0.001"] = np.count_nonzero([p_values < 0.001]) / len(trks)

    alltrk_p_df.to_csv(indir+grp+"/all_tracks/tracks_summary_proportionandmax.csv")
    return(alltrk_p_df)
 
def main():
    stats_df, all_null_df = get_stats_df(grp)
    get_prop_p(grp, stats_df)

if __name__ == "__main__":
    main()
