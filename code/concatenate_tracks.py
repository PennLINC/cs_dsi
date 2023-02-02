import pandas as pd
import sys
import os

grp = sys.argv[1] #Analysis group

def main():
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/"+grp+"/"
    df_fulltrk = pd.DataFrame()
    odir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/"+grp+"/"+mtrk+"/"
    os.makedirs(odir, exist_ok=True)

    acquisitions = ["HASC92-55_run-01", "HASC92-55_run-02",  "HASC92", "HASC55_run-01",  "HASC55_run-02", "RAND57"]


    trks = ["Arcuate_Fasciculus_L", "Arcuate_Fasciculus_R", "Cingulum_Frontal_Parahippocampal_L", "Cingulum_Frontal_Parahippocampal_R", "Cingulum_Frontal_Parietal_L", "Cingulum_Frontal_Parietal_R", "Cingulum_Parahippocampal_L", "Cingulum_Parahippocampal_Parietal_L", "Cingulum_Parahippocampal_Parietal_R", "Cingulum_Parahippocampal_R", "Cingulum_Parolfactory_L", "Cingulum_Parolfactory_R", "Corpus_Callosum_Body", "Corpus_Callosum_Forceps_Major", "Corpus_Callosum_Forceps_Minor", "Corpus_Callosum_Tapetum", "Corticospinal_Tract_L", "Corticospinal_Tract_R", "Corticostriatal_Tract_Anterior_L", "Corticostriatal_Tract_Anterior_R", "Corticostriatal_Tract_Posterior_L", "Corticostriatal_Tract_Posterior_R", "Corticostriatal_Tract_Superior_L", "Corticostriatal_Tract_Superior_R", "Fornix_L", "Fornix_R", "Frontal_Aslant_Tract_L", "Frontal_Aslant_Tract_R", "Inferior_Fronto_Occipital_Fasciculus_L", "Inferior_Fronto_Occipital_Fasciculus_R", "Inferior_Longitudinal_Fasciculus_L", "Inferior_Longitudinal_Fasciculus_R", "Middle_Longitudinal_Fasciculus_L", "Middle_Longitudinal_Fasciculus_R", "Optic_Radiation_L", "Optic_Radiation_R", "Parietal_Aslant_Tract_L", "Parietal_Aslant_Tract_R", "Reticular_Tract_L", "Reticular_Tract_R", "Superior_Longitudinal_Fasciculus1_L", "Superior_Longitudinal_Fasciculus1_R", "Superior_Longitudinal_Fasciculus2_L", "Superior_Longitudinal_Fasciculus2_R", "Superior_Longitudinal_Fasciculus3_L", "Superior_Longitudinal_Fasciculus3_R", "Thalamic_Radiation_Anterior_L", "Thalamic_Radiation_Anterior_R", "Thalamic_Radiation_Posterior_L", "Thalamic_Radiation_Posterior_R", "Thalamic_Radiation_Superior_L", "Thalamic_Radiation_Superior_R", "Uncinate_Fasciculus_L", "Uncinate_Fasciculus_R", "Vertical_Occipital_Fasciculus_L", "Vertical_Occipital_Fasciculus_R"]
    
    if grp == "retro_fulldsi_btwn_rel":
        for trk in trks:
            ifile = indir+trk+"/all_subjects.csv"
            df = pd.read_csv(ifile)
            df.loc[:,'Track'] = trk
            df_fulltrk = pd.concat([df_fulltrk, df])
        df_fulltrk.to_csv(odir+"all_subjects.csv")

    if grp == "retro_wthn_acc":
        for trk in trks:
            ifile = indir+trk+"/all_sessions.csv"
            df = pd.read_csv(ifile)
            df.loc[:,'Track'] = trk
            df_fulltrk = pd.concat([df_fulltrk, df])
        df_fulltrk.to_csv(odir+"all_sessions.csv")

    if grp == "retro_btwn_acc":
        for acq in acquisitions:
            df_fulltrk = pd.DataFrame()
            for trk in trks:
                ifile = indir+trk+"/all_subjects_"+acq+".csv"
                df = pd.read_csv(ifile)
                df.loc[:,'Track'] = trk
                df_fulltrk = pd.concat([df_fulltrk, df])
            df_fulltrk.to_csv(odir+"all_subjects_"+acq+".csv")

    if grp == "retro_btwn_rel":
        for acq in acquisitions:
            df_fulltrk = pd.DataFrame()
            for trk in trks:
                ifile = indir+trk+"/all_subjects_"+acq+".csv"
                df = pd.read_csv(ifile)
                df.loc[:,'Track'] = trk
                df_fulltrk = pd.concat([df_fulltrk, df])
            df_fulltrk.to_csv(odir+"all_subjects_"+acq+".csv")

    if grp == "prosp_wthn_acc":
        for trk in trks:
            ses="1"
            ifile = indir+trk+"/ses-1_ind.csv"
            df = pd.read_csv(ifile)
            df.loc[:,'Track'] = trk
            df_fulltrk = pd.concat([df_fulltrk, df])
        df_fulltrk.to_csv(odir+"ses-"+ses+"_ind.csv")

if __name__ == "__main__":
    main()
