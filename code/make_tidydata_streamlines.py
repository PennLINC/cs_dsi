import pandas as pd
import sys
import os
import plotnine as pn

grp = sys.argv[1] #Analysis group

def make_violin_friendly_frames(trk):
    """
    Tidies up the dataframe, such that schemes are rows and not columns. Need to do this to make the dataframe plottable with plotnine. Just saves the tidy dataframe.
    """
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/"+grp+"/"+trk+"/"
    fulldsi_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/retro_fulldsi_btwn_rel/"+trk+"/all_subjects.csv")

    comb_df = pd.DataFrame(columns=["Dice", "Acquisition"])
    acq_dict = {"HASC92-55_run-01":"HA-SC92+55-1", "HASC92-55_run-02":"HA-SC92+55-2",  "HASC92":"HA-SC92", "HASC55_run-01":"HA-SC55-1",  "HASC55_run-02":"HA-SC55-2", "RAND57":"RAND57"} #to rename schemes

    if grp == "retro_wthn_acc":
        acq_df = pd.read_csv(indir+"all_sessions.csv")
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Full DSI Reliability"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 8 * 6 + 24 * 28 #CS-DSI same-scan Accuracy (24 subjects, 8 sessions, 6 CS-DSI schemes) + Full DSI reliability (24 subjects, 28 pairs per subject)
        
    if grp == "retro_btwn_acc":
        comb_df = pd.DataFrame(columns=["Dice", "Acquisition"])
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Full DSI Reliability"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            acq_df = pd.read_csv(indir+"all_subjects_"+acq+".csv")
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 56 * 6 + 24 * 28 #CS-DSI inter-scan Accuracy (24 subjects 56 pairs, 6 CS-DSI schemes) + Full DSI reliability (24 subjects, 28 pairs per subject)
       

    if grp == "retro_btwn_rel":
        comb_df = pd.DataFrame(columns=["Dice", "Acquisition"])
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Full DSI"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            acq_df = pd.read_csv(indir+"all_subjects_"+acq+".csv")
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 28 * 7 #CS-DSI inter-scan reliability (24 subjects, 28 pairs, 6 CS-DSI schemes) + Full DSI reliability (24 subjects, 28 pairs per subject)

    if grp == "prosp_wthn_acc":
        acq_df = pd.read_csv(indir+"ses-1_ind.csv")
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Full DSI Reliability"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)    
        comb_df = comb_df.dropna()
        expected_nofail = 20 * 6 + 24 * 28 #CS-DSI same-scan Accuracy (20 subjects, 1 session, 6 CS-DSI schemes) + Full DSI reliability (24 subjects, 28 pairs per subject)

    comb_df.to_csv(indir+"data_violin-friendly.csv")

    # Append this info to sanity_check dataframe:
    os.makedirs("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/", exist_ok=True)
    difference = expected_nofail-comb_df.shape[0]
    sane_df = pd.DataFrame(data=[[trk,expected_nofail,comb_df.shape[0], difference]], columns=["Track", "Expected_NoFail_N", "Observed_N", "Difference"])
    if trk == "Arcuate_Fasciculus_L":
        sane_df.to_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_trackwise.csv", index=False)
    else:
        app_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_trackwise.csv")
        app_df = app_df.append(sane_df)
        app_df.to_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_trackwise.csv", index=False)
        
def main():
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
    for trk in trks:
        print("Tidying up: "+trk)
        make_violin_friendly_frames(trk) 
if __name__ == "__main__":
    main()