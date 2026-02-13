"""

Main script for DSC analysis for MaCFP-4

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
from scipy.signal import savgol_filter
from typing import Optional, Union, List, Dict

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation
from Utils import DATA_DIR


#define whether to save files in pdf or png
ex = 'pdf' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

#region create subdirectories to save plots. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Average_dir = base_dir / 'DSC' / 'Average'
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
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


# ------------------------------------
#region functions
# ------------------------------------
def Integral_DSC(df:pd.DataFrame)-> pd.DataFrame:
    """Calculate integral heat flow."""
    df = interpolation(df)

    int_heatflow = np.zeros(len(df))
    for i in range(1, len(df)):
        int_heatflow[i] = int_heatflow[i-1] + 0.5 * (df['Heat Flow Rate (W/g)'].iloc[i-1] + df['Heat Flow Rate (W/g)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int Heat Flow (J/g)'] = int_heatflow

    return df




def average_dsc_series(series_name: str) -> pd.DataFrame:
    
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
        df_raw = pd.read_csv(path)
        df = Integral_DSC(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Temperature (K)'], df['Heat Flow Rate (W/g)'], label = label, color=color)
        ax2.plot(df['Temperature (K)'], df['Int Heat Flow (J/g)'], label = label, color=color)

    #ax1.set_xlim(400,800)
    ax1.set_ylim(bottom=-0.5)
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Heat flow [W g$^{-1}$]')
    fig1.tight_layout()
    handles1, labels1 = ax1.get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    ax1.legend(by_label1.values(), by_label1.keys())

    ax2.set_ylim(bottom=-500)
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('Integral Heat Flow [J g$^{-1}$]')
    fig2.tight_layout()
    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))
    ax2.legend(by_label2.values(), by_label2.keys())

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
                        label='average', color='limegreen')
    ax_HF.fill_between(df_average['Temperature (K)'], 
                         df_average['Heat Flow Rate (W/g)']-2*df_average['unc Heat Flow Rate (W/g)'],
                         df_average['Heat Flow Rate (W/g)']+2*df_average['unc Heat Flow Rate (W/g)'],
                         color='limegreen', alpha = 0.3)

    # Plot mass loss rate (right y-axis, dashed)
    ax_iHF.plot(df_average['Temperature (K)'], df_average['Int Heat Flow (J/g)'],
                        label='average', color='red', alpha=0.9)

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
    ax_iHF.set_ylabel('Integral Heat Flow [J$^{-1}$]')


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



# Average Heat flow and integral heat flow plots per institution for all unique atmospheres and heating rates 
for series in unique_conditions_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, atm, hr  = parts[:4]
    DSC_subset_paths = [p for p in DSC_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]
    for path in DSC_subset_paths:
        df_raw = pd.read_csv(path)
        df = Integral_DSC(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Temperature (K)'], df['Heat Flow Rate (W/g)'],'.', color=color, alpha=0.3, markersize =0.1, zorder=4)
        ax2.plot(df['Temperature (K)'], df['Int Heat Flow (J/g)'],'.', color=color, alpha=0.3, markersize =0.1,zorder=4)
    
    Institute_list = [name for name in DSC_sets if series in name]
    for Institute in Institute_list:
        df_average = average_dsc_series(Institute)
    
        Duck, color = label_def(Institute.split('_')[0])
        Conditions = '_'.join(Institute.split('_')[2:])

        # plot average
        # Plot mass (left y-axis)
        ax1.plot(df_average['Temperature (K)'], df_average['Heat Flow Rate (W/g)'],
                            label=Duck, color=color,zorder=2)
        ax1.fill_between(df_average['Temperature (K)'], 
                            df_average['Heat Flow Rate (W/g)']-2*df_average['unc Heat Flow Rate (W/g)'],
                            df_average['Heat Flow Rate (W/g)']+2*df_average['unc Heat Flow Rate (W/g)'],
                            color=color,alpha=0.3, zorder=3)
        
        # Plot mass loss rate (right y-axis, dashed)
        ax2.plot(df_average['Temperature (K)'], df_average['Int Heat Flow (J/g)'],
                        label=Duck, color=color, zorder=2)

        ax2.fill_between(df_average['Temperature (K)'], 
                        df_average['Int Heat Flow (J/g)']-2*df_average['unc Int Heat Flow (J/g)'],
                        df_average['Int Heat Flow (J/g)']+2*df_average['unc Int Heat Flow (J/g)'],
                        color=color, alpha=0.3,zorder=3)



    ax1.set_ylim(bottom=-0.5)
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Heat flow [W g$^{-1}$]')
    fig1.tight_layout()
    ax1.legend()

    ax2.set_ylim(bottom=-500)
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('Integral Heat Flow [J g$^{-1}$]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_HF_avg.{}'.format(material, atm,hr,ex))
    fig2.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_iHF_avg.{}'.format(material, atm,hr,ex))
    plt.close(fig1)
    plt.close(fig2)



# region heats of reactions:
# only for STA data
STA_Data = device_data(DATA_DIR, 'STA')

for exp in STA_Data:
    df_raw = pd.read_csv(exp)
    df = Integral_DSC(df_raw)
    
    df['Normalized mass'] = df['Mass (mg)'] / np.mean(df['Mass (mg)'].iloc[0:5])
    dt = df['Time (s)'].shift(-1) - df['Time (s)'].shift(1)
    df['dm/dt unfiltered'] = (df['Normalized mass'].shift(1) - df['Normalized mass'].shift(-1)) / dt
    df['dm/dt unfiltered'] = df['dm/dt unfiltered'].interpolate(method='linear', limit_direction='both') #avoid nan_values
    df['dm/dt'] = savgol_filter(df['dm/dt unfiltered'],41,3)
    
    # Find peak MLR and its index
    peak_MLR = df['dm/dt'].max()
    peak_idx = df['dm/dt'].idxmax()
    
    # Find threshold (10% of peak) and indices
    threshold = 0.1 * peak_MLR
    before_peak = df.loc[:peak_idx]
    idx1 = before_peak[before_peak['dm/dt'] >= threshold].index[0]
    after_peak = df.loc[peak_idx:]
    idx2 = after_peak[after_peak['dm/dt'] <= threshold].index[0]
    
    # Extract data for integration
    T1 = df.loc[idx1, 'Temperature (K)']
    T2 = df.loc[idx2, 'Temperature (K)']
    HF1 = df.loc[idx1, 'Heat Flow Rate (W/g)']
    HF2 = df.loc[idx2, 'Heat Flow Rate (W/g)']
    
    # Subset data between the two indices
    df_subset = df.loc[idx1:idx2].copy()
    
    # Create linear baseline
    df_subset['baseline'] = np.interp(
        df_subset['Temperature (K)'], 
        [T1, T2], 
        [HF1, HF2]
    )
    
    # Subtract baseline from heat flow rate
    df_subset['HF_corrected'] = df_subset['Heat Flow Rate (W/g)'] - df_subset['baseline']
    
    # Integrate corrected heat flow rate with respect to time
    value = np.trapezoid(df_subset['HF_corrected'], df_subset['Time (s)'])/(df['Normalized mass'][idx1]- df['Normalized mass'][idx2])
    
    print(f"Experiment: {exp.stem}")
    print(f"Integration from {T1:.1f} K to {T2:.1f} K")
    print(f"Estimated heat of reaction: {value:.4f} J/g")
    print()
