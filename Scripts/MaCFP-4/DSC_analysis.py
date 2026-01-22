import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
from scipy.signal import savgol_filter

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR


#define whether to save files in pdf or png
ex = 'pdf' #options 'pdf' or 'png

#when pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

# check all subdirectories to save plots exist. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Individual_dir = base_dir / 'DSC' / 'Individual'
Average_dir = base_dir / 'DSC' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what DSC data is available. 

# All DSC data (including STA)
DSC_Data = device_data(DATA_DIR, 'DSC') + device_data(DATA_DIR, 'STA')
# All unique sets (name without repetition number, e.g.TUT_DSC_N2_10K_40Pa )
DSC_sets = get_series_names(DSC_Data)
# All unique conditions over all institutes
unique_conditions = { '_'.join(s.split('_')[3:]) for s in DSC_sets}
unique_conditions_material = sorted(set(name.split('_', 1)[1] for name in DSC_sets if '_' in name))

#Print tables with Institute name (Duck version) and amount of repetition experiments
print('Nitrogen table')
print(make_institution_table(DSC_Data,['Wood'],['N2'],['3K','5K','10K','20K','30K','40K','50K','60K']))

print('Oxygen table')
print(make_institution_table(DSC_Data,['Wood'],['O2-21'],['3K','5K','10K','20K','30K','40K','50K','60K']))



# ------------------------------------
#region set plot style
# ------------------------------------

def set_plot_style():
    plt.rcParams.update({
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'axes.grid': False,
        'grid.alpha': 0.2,
        'lines.linewidth': 1.5,
        'axes.labelsize': 12,
        'axes.titlesize': 12,
        'legend.fontsize': 10,
    })

set_plot_style()

def Integral_DSC(df:pd.DataFrame):
    
    df = interpolation(df)

    int_heatflow = np.zeros(len(df))
    for i in range(1, len(df)):
        int_heatflow[i] = int_heatflow[i-1] + 0.5 * (df['Heat Flow Rate (W/g)'].iloc[i-1] + df['Heat Flow Rate (W/g)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int Heat Flow (J/g)'] = int_heatflow

    return df




def average_dsc_series(series_name: str):
    
    paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in DSC_Data]

    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df_raw = pd.read_csv(path)
        # calculate derivatives
        df=Integral_DSC(df_raw)
        Dataframes.append(df)

    merged_df = Dataframes[0]
    for df in Dataframes[1:]:
        merged_df = pd.merge(
            merged_df,
            df,
            on="Temperature (K)",
            how="outer",
            suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"),
        )
  
    merged_df.rename(columns={"Time (s)": "Time (s) 1"}, inplace=True)
    merged_df.rename(columns={'Heat Flow Rate (W/g)': "Heat Flow Rate (W/g) 1"}, inplace=True)
    merged_df.rename(columns={'Int Heat Flow (J/g)': "Int Heat Flow (J/g) 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    HF_cols = merged_df.filter(regex=r'^Heat Flow Rate').columns
    iHF_cols = merged_df.filter(regex=r'^Int Heat Flow').columns

    df_average = pd.DataFrame({'Temperature (K)': merged_df['Temperature (K)']})
    n=2
    sum = merged_df[HF_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[HF_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['Heat Flow Rate (W/g)'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[HF_cols].sub(df_average['Heat Flow Rate (W/g)'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc Heat Flow Rate (W/g)'] = np.sqrt(sum_diff/(cnt*(cnt-1)))

    sum = merged_df[iHF_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[iHF_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['Int Heat Flow (J/g)'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[iHF_cols].sub(df_average['Int Heat Flow (J/g)'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc Int Heat Flow (J/g)'] = np.sqrt(sum_diff/(cnt*(cnt-1)))
    return df_average



#--------------------------------------------------------
#region plots
#--------------------------------------------------------
# Heat flow and integral heat flow plots for all unique atmospheres and heating rates 
for series in unique_conditions_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, atm, hr  = parts[:4]
    DSC_subset_paths = [p for p in DSC_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]
    for path in DSC_subset_paths:
        print(path)
        df_raw = pd.read_csv(path)
        df = Integral_DSC(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Temperature (K)'], df['Heat Flow Rate (W/g)'], label = label, color=color)
        ax2.plot(df['Temperature (K)'], df['Int Heat Flow (J/g)'], label = label, color=color)

    #ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Heat flow [W g$^{-1}$]')
    fig1.tight_layout()
    ax1.legend()

    #ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('Integral Heat Flow [J g$^{-1}$]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_HF.{}'.format(material, atm,hr,ex))
    fig2.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_iHF.{}'.format(material, atm,hr,ex))
    plt.close(fig1)
    plt.close(fig2)


# plot average per DSC_set (unique institutions, unique material, unique conditions)
for idx,set in enumerate(DSC_sets):
    fig1, ax_HF = plt.subplots(figsize=(6, 4))
    fig2, ax_iHF = plt.subplots(figsize=(6, 4))
    df_average = average_dsc_series(set)
    
    Duck, color = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])

    # plot average
    # Plot mass (left y-axis)
    ax_HF.plot(df_average['Temperature (K)'], df_average['Heat Flow Rate (W/g)'],
                        label='m/m$_0$', color='limegreen')
    ax_HF.fill_between(df_average['Temperature (K)'], 
                         df_average['Heat Flow Rate (W/g)']-2*df_average['unc Heat Flow Rate (W/g)'],
                         df_average['Heat Flow Rate (W/g)']+2*df_average['unc Heat Flow Rate (W/g)'],
                         color='limegreen', alpha = 0.3)

    # Plot mass loss rate (right y-axis, dashed)
    ax_iHF.plot(df_average['Temperature (K)'], df_average['Int Heat Flow (J/g)'],
                        label='d(m/m$_0$)/dt', color='red', alpha=0.9)

    ax_iHF.fill_between(df_average['Temperature (K)'], 
                        df_average['Int Heat Flow (J/g)']-2*df_average['unc Int Heat Flow (J/g)'],
                        df_average['Int Heat Flow (J/g)']+2*df_average['unc Int Heat Flow (J/g)'],
                        color='red', alpha=0.3)


    #plot individual
    paths_TGA_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    for path in paths_TGA_set:
        df_raw = pd.read_csv(path)
        df = Integral_DSC(df_raw)
        ax_HF.plot(df['Temperature (K)'], df['Heat Flow Rate (W/g)'], '.',color ='black',markersize=0.00000000002)
        ax_iHF.plot(df['Temperature (K)'], df['Int Heat Flow (J/g)'],'.',color='black', markersize=0.0005)

    # Set lower limits of both y-axes to 0
   #ax_mass.set_ylim(bottom=0)
   # ax_rate.set_ylim(bottom=0)

    # Axes labels
    ax_HF.set_xlabel('Temperature (K)')
    ax_HF.set_ylabel('Heat Flow [W/g]')
    ax_iHF.set_xlabel('Temperature (K)')
    ax_iHF.set_ylabel('Integral Heat Flow [J/g]')


    # Figure title
    fig1.suptitle(Duck+"\n"+Conditions)
    fig2.suptitle(Duck+"\n"+Conditions)

    # Legend
    fig1.legend()
    fig2.legend()

    fig1.tight_layout()
    fig1.savefig(str(base_dir) + f'/DSC/Average/HF_{set}.{ex}')
    plt.close(fig1)

    fig2.tight_layout()
    fig2.savefig(str(base_dir) + f'/DSC/Average/iHF_{set}.{ex}')
    plt.close(fig2)