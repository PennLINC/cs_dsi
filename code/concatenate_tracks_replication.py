import pandas as pd
import sys
import os

grp = sys.argv[1] #Analysis group

def main():
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/"+grp+"/"
    df_fulltrk = pd.DataFrame()
    # hamsi's:
    # odir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/dice_scores/"+grp+"/all_tracks/"
    # replication:
    odir = "/cbica/projects/csdsi/replication/data/dice_scores/"+grp+"/all_tracks/"
    os.makedirs(odir, exist_ok=True)
    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
    
    for trk in trks:
        ifile = indir+trk+"/data_violin-friendly.csv"
        df = pd.read_csv(ifile)
        df.loc[:,'Track'] = trk
        df_fulltrk = pd.concat([df_fulltrk, df])
    df_fulltrk.to_csv(odir+"data_violin-friendly.csv")

    # More sanity checking:
    sane_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/sanity_check/"+grp+"_tidydata_trackwise.csv")
    expected_total = sane_df["Observed_N"].sum()
    print("*****"+grp+"*****")
    print("Expected rows of Violin Friendly Data Frame (All tracks):"+str(expected_total))
    print("Total rows of Violin Friendly Data Frame (All tracks):"+str(df_fulltrk.dropna().shape[0]))
    difference = expected_total - df_fulltrk.dropna().shape[0]
    print("Difference: "+str(difference))

if __name__ == "__main__":
    main()
