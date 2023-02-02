import pandas as pd
import sys
import os
import plotnine as pn

grp = sys.argv[1] #Analysis group
trk = sys.argv[2] #Track
plot = sys.argv[3] #Whether to plot or not
indir = "/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/"+grp+"/"+trk+"/"
fulldsi_df = pd.read_csv("/cbica/projects/csdsi/cleaned_paper_analysis/data/dice_scores/retro_fulldsi_btwn_rel/"+trk+"/all_subjects.csv")
odir = "/cbica/projects/csdsi/cleaned_paper_analysis/figs/dice_violins/"+grp+"/"+trk+"/"
os.makedirs(odir, exist_ok=True)

def make_violin_friendly_frames():
    """
    Tidies up the dataframe, such that schemes are rows and not columns. Need to do this to make the dataframe plottable with plotnine. Just saves the tidy dataframe.
    """
    comb_df = pd.DataFrame(columns=["Dice", "Acquisition"])
    acq_dict = {"HASC92-55_run-01":"HA-SC92+55-1", "HASC92-55_run-02":"HA-SC92+55-2",  "HASC92":"HA-SC92", "HASC55_run-01":"HA-SC55-1",  "HASC55_run-02":"HA-SC55-2", "RAND57":"RAND57"} #to rename schemes

    if grp == "retro_wthn_acc":
        acq_df = pd.read_csv(indir+"all_sessions.csv")
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI*"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)
        comb_df = comb_df.dropna()

    if grp == "retro_btwn_acc":
        comb_df = pd.DataFrame(columns=["Dice", "Acquisition"])
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI*"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            acq_df = pd.read_csv(indir+"all_subjects_"+acq+".csv")
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)

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

    if grp == "prosp_wthn_acc":
        acq_df = pd.read_csv(indir+"ses-1_ind.csv")
        comb_df["Dice"] = fulldsi_df.drop(["Subject", "Unnamed: 0","Track"],axis=1, errors="ignore").to_numpy().flatten()
        comb_df.loc[:, "Acquisition"] = "Scan-Rescan DSI**"
        comb_df = comb_df[comb_df.Dice < 1]
        for acq in acq_dict:
            new_df = pd.DataFrame(columns=["Dice", "Acquisition"])
            new_df["Dice"] = acq_df[acq]
            new_df.loc[:, "Acquisition"] = acq_dict[acq]
            comb_df = pd.concat([comb_df, new_df], ignore_index=True)    
    
    comb_df = comb_df.dropna()
    comb_df = comb_df[comb_df.Dice < 1] #just double checking
    comb_df.to_csv(indir+"data_violin-friendly.csv")

def get_figure_specs(comb_df):
    """
    Returns image specifics based on analysis group

    Parameters:
    comb_df (DataFrame): The dataframe to be drawing the violins from. Only need this to assign categories.

    Returns:
    palette_col [List]: List of colors in HEX to outline violins
    palette_fill [List]: List of colors in HEX to fill violins
    cat [List]: Categories (x-axis)
    comb_df [DataFrame]: Original dataframe, with categories assigned.


    """
    if grp.split("_")[2] == "acc":
        palette_fill = ["#FFFFFF", "#7781a6", "#477998", "#298e91", "#d24b4e", "#dd6d40", "#ffbf1f"]
        palette_col = ["#767676", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"]
   
    if grp.split("_")[2] == "rel":
        palette_fill = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
        palette_col = ["#767676", "#7781a6", "#477998", "#298e91", "#d24b4e", "#dd6d40", "#ffbf1f"]

    if grp == "retro_wthn_acc":
        cat = pd.Categorical(comb_df["Acquisition"], categories = ["Scan-Rescan DSI*", "HA-SC92+55-1", "HA-SC92+55-2", "HA-SC92", "HA-SC55-1", "HA-SC55-2", "RAND57"])

    if grp == "retro_btwn_acc":
        cat = pd.Categorical(comb_df["Acquisition"], categories = ["Scan-Rescan DSI*", "HA-SC92+55-1", "HA-SC92+55-2", "HA-SC92", "HA-SC55-1", "HA-SC55-2", "RAND57"])

    if grp == "retro_btwn_rel":
        cat = pd.Categorical(comb_df["Acquisition"], categories = ["Full DSI", "HA-SC92+55-1", "HA-SC92+55-2", "HA-SC92", "HA-SC55-1", "HA-SC55-2", "RAND57"])
    
    if grp == "prosp_wthn_acc":
        cat = pd.Categorical(comb_df["Acquisition"], categories = ["Scan-Rescan DSI**", "HA-SC92+55-1", "HA-SC92+55-2", "HA-SC92", "HA-SC55-1", "HA-SC55-2", "RAND57"])

    comb_df = comb_df.assign(cat = cat)
    
    return palette_col, palette_fill, cat, comb_df
        
def main():
    if os.path.exists(indir+"data_violin-friendly.csv") == False:
        make_violin_friendly_frames()
    comb_df = pd.read_csv(indir+"data_violin-friendly.csv")
    if plot == True:
        palette_col, palette_fill, cat, comb_df = get_figure_specs(comb_df)
        base = pn.ggplot(comb_df, pn.aes(x=cat, y="Dice", fill=cat, color=cat, stroke=2)) \
            + pn.scale_fill_manual(values=palette_fill) \
            + pn.scale_color_manual(values=palette_col) 
        thme = base \
            + pn.theme_bw() \
            + pn.theme(plot_title = pn.element_text(face="bold", size=16), 
                    axis_title = pn.element_text(face="bold", size=14), 
                    axis_text_x=pn.element_text(rotation=45, hjust=1, size=12, color="black"), 
                    axis_text_y=pn.element_text(size=12, color="black"), 
                    axis_ticks = pn.element_line(size = 0.2), 
                    panel_border = pn.element_rect(fill = "white", colour="black"), 
                    panel_grid_major = pn.element_blank(), 
                    panel_grid_minor = pn.element_blank()) \
            + pn.labels.xlab("Acquisition Scheme") \
            + pn.labels.ylab("Dice Score") \
            + pn.ylim(0,1)
        fig = thme \
            + pn.geom_violin(size = 1.5, data = comb_df, scale = 'width', show_legend = False, trim=True) \
            + pn.geom_boxplot(width=0.2, fill="white", outlier_alpha=0, show_legend = False)

        fig.save(filename = odir+trk+"_notitle_y0-1.svg", dpi=500)
        fig.save(filename = odir+trk+"_notitle_y0-1.png", dpi=500)

if __name__ == "__main__":
    main()
