import numpy as np
import sys
from dipy.io.image import load_nifti
import pandas as pd
from itertools import combinations, permutations
import os
grp = sys.argv[1] #Analysis group
trk = sys.argv[2] #streamline

def pairwise_dice(img_path1, img_path2):
    """
    Calculates the dice score between two images. Uses the formula for dice score described in https://gist.github.com/JDWarner/6730747

    Parameters:
    img_path1 (string): Path to first image, the order of images does not matter.
    img_path2 (string): Path to second image, the order of images does not matter.

    Returns:
    dice (float): dice score between the two images.

    """

    img1, _ = load_nifti(img_path1) # load images
    img2, _ = load_nifti(img_path2)
    img1 = np.asarray(img1).astype(np.bool_) # convert to boolean arrays
    img2 = np.asarray(img2).astype(np.bool_)

    # Make sure the images have the same shape
    if img1.shape != img2.shape:
        raise ValueError("Shape mismatch error: Both images passed to pairwise_dice must have the same shape.")

    # Compute Dice coefficient
    intersection = np.logical_and(img1, img2)
    dice = 2. * intersection.sum() / (img1.sum() + img2.sum()) 

    return dice
    
def main():
    # Initialize and create output path:
    #odir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/"+grp+"/"+trk+"/"
    # for replication:
    odir = "/cbica/projects/csdsi/replication/data/dice_scores/"+grp+"/"+trk+"/"
    os.makedirs(odir, exist_ok=True)

    # Figure dataset to pull from and initialize subjects and sessions:
    datagrp = grp.split("_")[0]
    if datagrp == "retro":
        subjects = ["0001a", "1041h", "1665h", "2211h", "3058s", "4558a", "4936m", "0097p", "1043f", "1808u", "2453z", "3571z", "4662a", "4961a", "0444g", "1142k", "1853b", "2741x", "3832y", "4680i", "1145h", "2755j", "3992u", "4917f"]
        sessions = ["1", "2", "3", "4", "5", "6", "7", "8"]
        pairwise_sessions = list(permutations(sessions, 2)) #get list of pairwise session combinations
        # ^^ CZ: this is ordered, i.e., including both ('1', '2'), and ('2', '1'), total 2P8 = 8x7=56
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
                img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                img_path2 = indir+"sub-"+sub+"/ses-"+ses2+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses2+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                if os.path.exists(img_path1) and os.path.exists(img_path2):
                    df.loc[p[0],p[1]] = pairwise_dice(img_path1, img_path2)
                else:
                    df.loc[p[0],p[1]] = np.nan # if bundle wasn't detected for this subject/session/acquisition
                
                # BUG FIX: Delete lower triangle to remove redundant pairs
                df[:] = np.where(np.arange(8)[:,None] >= np.arange(8),np.nan,df)
                
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
                acqdice = []
                for sub in subjects:
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                    img_path2 = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_full/sub-"+sub+"/ses-"+ses+"/acq-full/"+trk+"/sub-"+sub+"_ses-"+ses+"_acq-full_dwi."+trk+"_mask.nii.gz" #Notice comparison with original full scan instead of combined.
                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        dice = pairwise_dice(img_path1, img_path2)
                    else:
                        dice = np.nan # if bundle wasn't detected for this subject/session/acquisition
                    acqdice.append(dice)
                df[acq] = acqdice
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
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                    img_path2 = "/cbica/projects/csdsi/dsistudio_full/dsi_derivatives/crash_full/sub-"+sub+"/ses-"+ses2+"/acq-full/"+trk+"/sub-"+sub+"_ses-"+ses2+"_acq-full_dwi."+trk+"_mask.nii.gz"
                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        df.loc[p[0],p[1]] = pairwise_dice(img_path1, img_path2)
                    else:
                        df.loc[p[0],p[1]] = np.nan # if bundle wasn't detected for this subject/session/acquisition
                    
                    # FIX: Wasn't a bug, but asserting that within-accuracy values aren't here:
                    if p[0] == p[1]:
                        df.loc[p[0],p[1]] = np.nan # removing same session accuracy
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
                    img_path1 = indir+"sub-"+sub+"/ses-"+ses1+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses1+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                    img_path2 = indir+"sub-"+sub+"/ses-"+ses2+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses2+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                    if os.path.exists(img_path1) and os.path.exists(img_path2):
                        df.loc[p[0],p[1]] = pairwise_dice(img_path1, img_path2)
                    else:
                        df.loc[p[0],p[1]] = np.nan # if bundle wasn't detected for this subject/session/acquisition
                
                # BUG FIX: Delete lower triangle to remove redundant pairs
                df[:] = np.where(np.arange(8)[:,None] >= np.arange(8),np.nan,df)
                df.loc[:,'Subject'] = sub
                df_full = pd.concat([df_full, df])
            df_full.to_csv(odir+"all_subjects_"+acq+".csv")
            print("File saved as: "+odir+"all_subjects_"+acq+".csv")

    if grp == "prosp_wthn_acc":
        df = pd.DataFrame()
        df["Subject"] = subjects
        for acq in acquisitions:
            acqdice = []
            for sub in subjects:
                img_path1 = indir+"sub-"+sub+"/ses-"+ses+"/acq-"+acq+"/"+trk+"/sub-"+sub+"_ses-"+ses+"_acq-"+acq+"_dwi."+trk+"_mask.nii.gz"
                img_path2 = indir+"sub-"+sub+"/ses-"+ses+"/acq-combined/"+trk+"/sub-"+sub+"_ses-"+ses+"_acq-combined_dwi."+trk+"_mask.nii.gz"
                if os.path.exists(img_path1) and os.path.exists(img_path2):
                    dice = pairwise_dice(img_path1, img_path2)
                    acqdice.append(dice)
                else:
                    dice = np.nan # if bundle wasn't detected for this subject/session/acquisition
                    acqdice.append(dice)
            df[acq] = acqdice
        df.to_csv(odir+"ses-"+ses+"_ind.csv")
        print("File saved as: "+odir+"ses-"+ses+"_ind.csv")

if __name__ == "__main__":
    main()