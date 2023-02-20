import numpy as np
import sys
import pandas as pd
from itertools import combinations, permutations
import os
from dipy.io.image import load_nifti
from scipy.stats import pearsonr
grp = sys.argv[1] #Analysis group
met = sys.argv[2] #metric
tt = "mask" #tissue type: whole brain (if you want just white matter, change to wm)

def pairwise_r(img_path1, img_path2, mask_path):
    """
    Calculates the pearson correlation between two images. 

    Parameters:
    img_path1 (string): Path to first image, the order of images does not matter.
    img_path2 (string): Path to second image, the order of images does not matter.
    mask_path (string): Path to whole brain mask

    Returns:
    rvalue (float): pearson correlation between the two images.
    """
    img1, _ = load_nifti(img_path1) # load images
    img2, _ = load_nifti(img_path2)
    mimg, _ = load_nifti(mask_path)
    rdf = pd.DataFrame() #something weird is happening with the arrays
    rdf["x"] = np.ma.masked_where(mimg <= 0.5, img1).flatten() #to make compatible with the prob masks. This only includes voxels that are 1 in the mask as np.ma.masked_where returns values WHERE THE CONDITION IS NOT TRUE. Just confirmed.
    rdf["y"] = np.ma.masked_where(mimg <= 0.5, img2).flatten() #to make compatible with the prob masks
    rdf = rdf.dropna()
    rvalue, _ = pearsonr(rdf["x"], rdf["y"])
    return rvalue

def main():
    # Initialize and create output path:
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/pearson_correlations/"+grp+"/"+met+"_"+tt+"/"
    os.makedirs(odir, exist_ok=True)

    # Figure dataset to pull from and initialize subjects and sessions:
    datagrp = grp.split("_")[0]
    if datagrp == "retro":
        subjects = ["0001a", "1041h", "1665h", "2211h", "3058s", "4558a", "4936m", "0097p", "1043f", "1808u", "2453z", "3571z", "4662a", "4961a", "0444g", "1142k", "1853b", "2741x", "3832y", "4680i", "1145h", "2755j", "3992u", "4917f"]
        sessions = ["1", "2", "3", "4", "5", "6", "7", "8"]
        pairwise_sessions = list(permutations(sessions, 2)) #get list of pairwise session combinations
        indir = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_retro/"

    if datagrp == "prosp":
        subjects = ["001", "19779", "20594", "20645", "20698", "20792", "20872", "15852", "19902", "20597", "20676", "20706", "20804", "20909", "19708", "20543", "20642", "20687", "20708", "20840"]
        ses = "1"
        indir = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/prospective/"

    acquisitions = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]

    ## Analysis group specific actions:
    if grp == "retro_fulldsi_btwn_rel":
        indir = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_full/" #just a fringe case, so re-initializing
        acq = "full" #just a fringe case, so re-initializing
        df_full = pd.DataFrame()
        for sub in subjects:
            df = pd.DataFrame(columns=sessions, index=sessions)
            for p in pairwise_sessions:
                ses1 = p[0]
                ses2 = p[1]
                img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                img_path2 = indir+"sub-"+sub+"/ses-"+ses2+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses2+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                mask_path = "/cbica/projects/csdsi/dsistudio_full/crash_full/sub-"+sub+"/ses-"+ses1+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_"+tt+".nii.gz"
                if os.path.exists(img_path1) and os.path.exists(img_path2):
                    df.loc[p[0],p[1]] = pairwise_r(img_path1, img_path2, mask_path)
                else:
                    df.loc[p[0],p[1]] = np.nan # if image doesn't exist, unlikely
            df.loc[:,'Subject'] = sub
            df_full = pd.concat([df_full, df])
        df_full.to_csv(odir+"all_subjects.csv")
        print("File saved as: "+odir+"all_subjects.csv")


    if grp == "retro_wthn_acc":
        df_full = pd.DataFrame()
        for ses in sessions:
            df = pd.DataFrame()
            df["Subject"] = subjects
            for acq in acquisitions:
                acqrvalue = []
                for sub in subjects:
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    img_path2 = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_full/"+"sub-"+sub+"/ses-"+ses+"/acq-full/sub-"+sub+"_ses-"+ses+"_acq-full_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    mask_path = "/cbica/projects/csdsi/dsistudio_full/crash_full/sub-"+sub+"/ses-"+ses+"/sub-"+sub+"_ses-"+ses+"_acq-full_"+tt+".nii.gz"
                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        rvalue = pairwise_r(img_path1, img_path2, mask_path)
                    else:
                        rvalue = np.nan # if bundle wasn't detected for this subject/session/acquisition
                    acqrvalue.append(rvalue)
                df[acq] = acqrvalue
            df.loc[:, 'Session'] = ses
            df_full = pd.concat([df_full, df])
        df_full.to_csv(odir+"all_sessions.csv")
        print("File saved as: "+odir+"all_sessions.csv")

    if grp == "retro_btwn_acc":
        for acq in acquisitions:
            df_full = pd.DataFrame()
            for sub in subjects:
                df = pd.DataFrame(columns=sessions, index=sessions)
                for p in pairwise_sessions:
                    ses1 = p[0]
                    ses2 = p[1]
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    img_path2 = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_full/"+"sub-"+sub+"/ses-"+ses2+"/acq-full/sub-"+sub+"_ses-"+ses2+"_acq-full_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    mask_path = "/cbica/projects/csdsi/dsistudio_full/crash_full/sub-"+sub+"/ses-"+ses2+"/sub-"+sub+"_ses-"+ses2+"_acq-full_"+tt+".nii.gz"
                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        df.loc[p[0],p[1]] = pairwise_r(img_path1, img_path2, mask_path)
                    else:
                        df.loc[p[0],p[1]] = np.nan # if bundle wasn't detected for this subject/session/acquisition
                df.loc[:,'Subject'] = sub
                df_full = pd.concat([df_full, df])
            df_full.to_csv(odir+"all_subjects_"+acq+".csv")
            print("File saved as: "+odir+"all_subjects_"+acq+".csv")

    if grp == "retro_btwn_rel":
        for acq in acquisitions:
            df_full = pd.DataFrame()
            for sub in subjects:
                df = pd.DataFrame(columns=sessions, index=sessions)
                for p in pairwise_sessions:
                    ses1 = p[0]
                    ses2 = p[1]
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    img_path2 = indir+"sub-"+sub+"/ses-"+ses2+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses2+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                    mask_path = "/cbica/projects/csdsi/dsistudio_full/crash_full/sub-"+sub+"/ses-"+ses1+"/sub-"+sub+"_ses-"+ses1+"_acq-full_"+tt+".nii.gz"

                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        df.loc[p[0],p[1]] = pairwise_r(img_path1, img_path2, mask_path)
                    else:
                        df.loc[p[0],p[1]] = np.nan # if bundle wasn't detected for this subject/session/acquisition
                df.loc[:,'Subject'] = sub
                df_full = pd.concat([df_full, df])
            df_full.to_csv(odir+"all_subjects_"+acq+".csv")
            print("File saved as: "+odir+"all_subjects_"+acq+".csv")

    if grp == "prosp_wthn_acc":
        df = pd.DataFrame()
        df["Subject"] = subjects
        for acq in acquisitions:
            acqrvalue = []
            for sub in subjects:
                img_path1 = indir+"sub-"+sub+"/ses-"+ses+"/acq-"+acq+"/sub-"+sub+"_ses-"+ses+"_acq-"+acq+"_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                img_path2 = indir+"sub-"+sub+"/ses-"+ses+"/acq-combined/sub-"+sub+"_ses-"+ses+"_acq-combined_dwi.src.gz.gqi.1.25.fib.gz."+met+".nii.gz"
                mask_path = "/cbica/projects/csdsi/dsistudio_full/prospective/sub-"+sub+"/ses-"+ses+"/sub-"+sub+"_ses-"+ses+"_acq-combined_"+tt+".nii.gz"
                if os.path.exists(img_path1) and os.path.exists(img_path2):
                    rvalue = pairwise_r(img_path1, img_path2, mask_path)
                    acqrvalue.append(rvalue)
                else:
                    rvalue = np.nan # if bundle wasn't detected for this subject/session/acquisition
                    acqrvalue.append(rvalue)
            df[acq] = acqrvalue
        df.to_csv(odir+"ses-"+ses+"_ind.csv")
        print("File saved as: "+odir+"ses-"+ses+"_ind.csv")

if __name__ == "__main__":
    main()


