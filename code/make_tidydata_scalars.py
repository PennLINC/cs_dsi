import pandas as pd
import sys
import os
import plotnine as pn

grp = sys.argv[1] #Analysis group
tt = "mask" #tissue type: whole brain (if you want just white matter, change to wm)



def make_violin_friendly_frames(met):
    """
    Tidies up the dataframe, such that schemes are rows and not columns. Need to do this to make the dataframe plottable with plotnine. Just saves the tidy dataframe.
    """

    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/pearson_correlations/"+grp+"/"+met+"_"+tt+"/"
    fulldsi_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/pearson_correlations/retro_fulldsi_btwn_rel/"+met+"_"+tt+"/all_subjects.csv")
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/figs/pearson_violins/"+grp+"/"+met+"_"+tt+"/"
    os.makedirs(odir, exist_ok=True)
    comb_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
    acq_dict = {"HASC92-55_run-01":"HA-SC92+55-1", "HASC92-55_run-02":"HA-SC92+55-2",  "HASC92":"HA-SC92", "HASC55_run-01":"HA-SC55-1",  "HASC55_run-02":"HA-SC55-2", "RAND57":"RAND57"} #to rename schemes

    if grp == "retro_wthn_acc":
        acq_df = pd.read_csv(indir+"all_sessions.csv")
        comb_df["PearsonR"] = fulldsi_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI*"
        comb_df = comb_df[comb_df.PearsonR < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
            new_df["PearsonR"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 8 * 6 + 24 * 28 #CS-DSI same-scan Accuracy (24 subjects, 8 sessions, 6 CS-DSI schemes) + Full DSI reliability (24 sessions, 28 pairs)


    if grp == "retro_btwn_acc":
        comb_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
        comb_df["PearsonR"] = fulldsi_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI*"
        comb_df = comb_df[comb_df.PearsonR < 1]
        for acq in acq_dict:
            acq_df = pd.read_csv(indir+"all_subjects_"+acq+".csv")
            new_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
            new_df["PearsonR"] = acq_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 56 * 6 + 24 * 28 #CS-DSI inter-scan Accuracy (24 subjects 56 pairs, 6 CS-DSI schemes) + Full DSI reliability (24 sessions, 28 pairs)
        

    if grp == "retro_btwn_rel":
        comb_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
        comb_df["PearsonR"] = fulldsi_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Full DSI"
        comb_df = comb_df[comb_df.PearsonR < 1]
        for acq in acq_dict:
            acq_df = pd.read_csv(indir+"all_subjects_"+acq+".csv")
            new_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
            new_df["PearsonR"] = acq_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()
        expected_nofail = 24 * 28 * 7 #CS-DSI inter-scan reliability (24 subjects, 28 pairs, 6 CS-DSI schemes) + Full DSI reliability (24 sessions, 28 pairs)
        

    if grp == "prosp_wthn_acc":
        acq_df = pd.read_csv(indir+"ses-1_ind.csv")
        comb_df["PearsonR"] = fulldsi_df.drop(["Subject", "Unnamed: 0"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI**"
        comb_df = comb_df[comb_df.PearsonR < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["PearsonR", "Acquisition"])
            new_df["PearsonR"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)   
        comb_df = comb_df.dropna() 
        expected_nofail = 20 * 6 + 24 * 28 #CS-DSI same-scan Accuracy (20 subjects, 1 session, 6 CS-DSI schemes) + Full DSI reliability (24 sessions, 28 pairs)
    
    comb_df.to_csv(indir+"data_violin-friendly.csv")

    # Append this info to sanity_check dataframe:
    os.makedirs("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/", exist_ok=True)
    difference = expected_nofail-comb_df.shape[0]
    sane_df = pd.DataFrame(data=[[met,expected_nofail,comb_df.shape[0], difference]], columns=["Metric", "Expected_NoFail_N", "Observed_N", "Difference"])
    if met == "nqa":
        sane_df.to_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_scalars.csv", index=False)
    else:
        app_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_scalars.csv")
        app_df = app_df.append(sane_df)
        app_df.to_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_scalars.csv", index=False)


def main():
    mets = ["nqa", "gfa", "iso"]
    for met in mets:
        print("Tidying up: "+met)
        make_violin_friendly_frames(met) 

if __name__ == "__main__":
    main()