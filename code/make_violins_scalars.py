import pandas as pd
import sys
import os
import plotnine as pn

grp = sys.argv[1] #Analysis group
met = sys.argv[2]
tt = "mask" #tissue type: whole brain (if you want just white matter, change to wm)

odir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/figs/pearson_violins/"+grp+"/"+met+"_"+tt+"/"
os.makedirs(odir, exist_ok=True)

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
    indir = "/cbica/projects/csdsi/cleaned_paper_analysis/bug_fix/data/pearson_correlations/"+grp+"/"+met+"_"+tt+"/"
    comb_df = pd.read_csv(indir+"data_violin-friendly.csv")
    palette_col, palette_fill, cat, comb_df = get_figure_specs(comb_df)
    base = pn.ggplot(comb_df, pn.aes(x=cat, y="PearsonR", fill=cat, color=cat, stroke=2)) \
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
        + pn.labels.ylab("Pearson R") \
        + pn.ylim(0.88,1)
    fig = thme \
        + pn.geom_violin(size = 1.5, data = comb_df, scale = 'width', show_legend = False, trim=True) \
        + pn.geom_boxplot(width=0.2, fill="white", outlier_alpha=0, show_legend = False)

    fig.save(filename = odir+met+"_"+tt+"_notitle_y075-1.svg", dpi=500)
    fig.save(filename = odir+met+"_"+tt+"_notitle_y075-1.png", dpi=500)

if __name__ == "__main__":
    main()