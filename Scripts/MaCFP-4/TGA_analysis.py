"""

Main script for TGA analysis for MaCFP-4

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
from scipy.signal import savgol_filter
from fnmatch import fnmatch
from typing import Optional, Union, List, Dict

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation
from Utils import DATA_DIR


#region Save plots as pdf or png
ex = 'png' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

#region create subdirectories to save plots. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Individual_dir = base_dir / 'TGA' / 'Individual'
Average_dir = base_dir / 'TGA' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
# All TGA data (including STA)
TGA_Data = device_data(DATA_DIR, 'TGA') + device_data(DATA_DIR, 'STA')

# All unique sets (name without repetition number, e.g.TUT_TGA_N2_10K_40Pa )
TGA_sets = get_series_names(TGA_Data)

# All unique conditions over all institutes
unique_conditions = { '_'.join(s.split('_')[3:]) for s in TGA_sets}
unique_conditions_material = sorted(set(name.split('_', 1)[1] for name in TGA_sets if '_' in name))

#Print tables with Institute name (Duck version) and amount of repetition experiments
print('Nitrogen table')
print(make_institution_table(TGA_Data,['Wood'],['N2'],['2K','3K','5K','10K','20K','30K','40K','50K','60K']))

print('Oxygen table')
print(make_institution_table(TGA_Data,['Wood'],['O2-20','O2-21'],['2K','5K','10K','20K','30K']))



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
        'xtick.direction': 'in',
        'ytick.direction': 'in',
    })

set_plot_style()


# ------------------------------------
#region functions
# ------------------------------------

def Calculate_dm_dt(df:pd.DataFrame) -> pd.DataFrame:
    """Calculate normalized mass and mass loss rate with smoothing."""
    df = interpolation(df)

    # Normalize mass
    df['Normalized mass'] = df['Mass (mg)'] / np.mean(df['Mass (mg)'].iloc[0:5])

    # Smooth normalized mass
    df['filtered'] = savgol_filter(df['Normalized mass'], 41, 3)

    # Central difference derivative w.r.t. time (NaN at first/last points)
    dt = df['Time (s)'].shift(-1) - df['Time (s)'].shift(1)
    
    df['dm/dt unfiltered'] = (df['Normalized mass'].shift(1) - df['Normalized mass'].shift(-1)) / dt
    
    df['dm/dt'] = savgol_filter(df['dm/dt unfiltered'],41,3)#(df['filtered'].shift(1) - df['filtered'].shift(-1)) / dt
    
    return df



def average_HR_tga_series(series_name: str) -> pd.DataFrame:
    """Averages the actual heating rate (dT/dt) across all repetitions of a test series"""
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in TGA_Data]
    Dataframes_HR = []

    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data
    for i, path in enumerate(paths):
        df = pd.read_csv(path)
        df = df.drop(columns=["Mass (mg)"])
       
        #interpolation
        df_interp = interpolation(df)

        window = 5
        dt = df_interp['Time (s)'].shift(-5) - df_interp['Time (s)'].shift(5)
        df_interp['dTdt'] = -60*(df_interp['Temperature (K)'].shift(5) - df_interp['Temperature (K)'].shift(-5)) / dt
        Dataframes_HR.append(df_interp)

    merged_df = Dataframes_HR[0]
    for df in Dataframes_HR[1:]:
        merged_df = pd.merge(
            merged_df,
            df,
            on="Temperature (K)",
            how="outer",
            suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"),
        )
    merged_df.rename(columns={"Time (s)": "Time (s) 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    dTdt_cols = merged_df.filter(regex=r'^dTdt').columns

    df_average = pd.DataFrame({
        'Temperature (K)': merged_df['Temperature (K)'],
        'dTdt (K/min)': merged_df[dTdt_cols].mean(axis=1),
        'dTdt_std': merged_df[dTdt_cols].std(axis=1, skipna=True, ddof=0),
    })

    return df_average



def average_tga_series(series_name: str, exclude:Optional[Union[str, List[str]]] = None, 
                       temp_filter:Optional[Dict[str, float]] = None) -> pd.DataFrame:
    """Calculate average mass and MLR for a test series with optional filtering."""
    paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in TGA_Data]

    # Apply exclusions
    if exclude is not None:
        if not isinstance(exclude, list):
            exclude = [exclude]  # Convert single string to list
        
        for excl in exclude:
            paths = [p for p in paths if excl not in str(p)]

    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df_raw = pd.read_csv(path)

        # Apply temperature filter for specific institutes
        if temp_filter is not None:
            for institute, min_temp in temp_filter.items():
                if institute in str(path):
                    df_raw = df_raw[df_raw['Temperature (K)'] > min_temp].reset_index(drop=True)

        # calculate derivatives
        df=Calculate_dm_dt(df_raw)
        df = df.drop(columns=['filtered'])
        df = df.drop(columns=['Mass (mg)'])
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
    merged_df.rename(columns={'Normalized mass': "Normalized mass 1"}, inplace=True)
    merged_df.rename(columns={'dm/dt': "dm/dt 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    mass_cols = merged_df.filter(regex=r'^Normalized mass').columns
    dmdt_cols = merged_df.filter(regex=r'^dm/dt').columns

    df_average = pd.DataFrame({'Temperature (K)': merged_df['Temperature (K)']})
    n=2
    sum = merged_df[mass_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[mass_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['Normalized Mass'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[mass_cols].sub(df_average['Normalized Mass'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc Normalized Mass'] = np.sqrt(sum_diff/(cnt*(cnt-1)))

    sum = merged_df[dmdt_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[dmdt_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['MLR (1/s)'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[dmdt_cols].sub(df_average['MLR (1/s)'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc MLR (1/s)'] = np.sqrt(sum_diff/(cnt*(cnt-1)))
    return df_average





#--------------------------------------------------------
#region plots
#--------------------------------------------------------
# HR plots for all unique HR
unique_HR = {s.split('_')[4] for s in TGA_sets}
for HR in unique_HR:
    if 'iso' in HR:
        continue
    else:
        fig, ax = plt.subplots(figsize=(6, 4))
        TGA_sub_set = device_subset(TGA_sets, HR, 'N2') + device_subset(TGA_sets, HR, 'O2-21') + device_subset(TGA_sets, HR, 'O2-20')
        for set in TGA_sub_set:
            average = average_HR_tga_series(set)
            label, color = label_def(set.split('_')[0])
            ax.plot(average['Temperature (K)'], average['dTdt (K/min)'], '.', label = label, color=color, markersize=2)
            ax.set_xlabel('Temperature (K)')
            ax.set_ylabel('Heating Rate dT/dt [K min$^{-1}$]')
            ax.set_title('dT/dt in TGA tests at {} K/min'.format(HR[:-1]))
            fig.tight_layout()
            ax.legend()
            ax.set_xlim(right=1100)
        plt.savefig(str(base_dir) +'/TGA/dTdt_TGA_{}Kmin.{}'.format(HR[:-1], ex))
        plt.close(fig)



# Mass and mass loss rate plots for all unique atmospheres and heating rates 
plot_configs = [
    {'suffix': '', 'xlim': (None, 1100), 'ylim1': (0, None),'ylim2': (0, None)},  # Original
    {'suffix': '_zoom1', 'xlim': (None,600), 'ylim1': (0.85, 1.1),'ylim2': (0, None)},  # Zoomed version
    {'suffix': '_zoom2', 'xlim': (650, 1100), 'ylim1': (-0.09, 0.5),'ylim2': (0, None)},  # Full range
]

for series in unique_conditions_material:
    parts = series.split('_')
    material, dev, atm, hr  = parts[:4]
    TGA_subset_paths = [p for p in TGA_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]
    if atm == 'O2-21':
        TGA_subset_paths += [p for p in TGA_Data if f"{material}_" in p.name and f"_O2-20_{hr}_" in p.name]

    for config in plot_configs:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        for path in TGA_subset_paths:
            df_raw = pd.read_csv(path)
            if 'FPL' in path.stem:
                df_raw = df_raw[df_raw['Temperature (K)'] > 400]
            df = Calculate_dm_dt(df_raw)
            label, color = label_def(path.stem.split('_')[0])
            if '40Pa' in path.stem:
                ax1.plot(df['Temperature (K)'], df['Normalized mass'], label = label, color=color,linestyle =':')
                ax2.plot(df['Temperature (K)'], df['dm/dt'], label = label, color=color,linestyle =':')
            else:
                ax1.plot(df['Temperature (K)'], df['Normalized mass'], label = label, color=color)
                ax2.plot(df['Temperature (K)'], df['dm/dt'], label = label, color=color)
        # Apply configuration
        ax1.set_ylim(bottom=config['ylim1'][0], top=config['ylim1'][1])
        ax1.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax1.set_xlabel('Temperature (K)')
        ax1.set_ylabel('m/m$_0$ [g/g]')
        fig1.tight_layout()
        handles1, labels1 = ax1.get_legend_handles_labels()
        by_label1 = dict(zip(labels1, handles1))
        ax1.legend(by_label1.values(), by_label1.keys())

        ax2.set_ylim(bottom=config['ylim2'][0], top=config['ylim2'][1])
        ax2.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax2.set_xlabel('Temperature (K)')
        ax2.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]')
        fig2.tight_layout()
        handles2, labels2 = ax2.get_legend_handles_labels()
        by_label2 = dict(zip(labels2, handles2))
        ax2.legend(by_label2.values(), by_label2.keys())

        fig1.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass{config["suffix"]}.{ex}')
        fig2.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_dmdt{config["suffix"]}.{ex}')
        plt.close(fig1)
        plt.close(fig2)





# plot all experiments individually to look at filtered data 
for path in TGA_Data:
    fig, ax_mass = plt.subplots(figsize=(6, 4))
    ax_rate = ax_mass.twinx()
    df_raw = pd.read_csv(path)
    df = Calculate_dm_dt(df_raw)

    # Plot mass (left y-axis)
    ax_mass.plot(df['Temperature (K)'], df['Normalized mass'],
                    label='m/m$_0$', color='blue')
    ax_mass.plot(df['Temperature (K)'], df['filtered'],':',
                    label='m/m$_0$, filtered', color='chartreuse')

    # Plot mass loss rate (right y-axis, dashed)
    ax_rate.plot(df['Temperature (K)'], df['dm/dt unfiltered'],'.',
                    label='d(m/m$_0$)/dt', color='red', alpha=0.9)
    ax_rate.plot(df['Temperature (K)'], df['dm/dt'],
                    label='d(m/m$_0$)/dt, filtered', color='black', linestyle='--', alpha=0.9)

     # Set lower limits of both y-axes to 0
    ax_mass.set_ylim(bottom=0)
    ax_mass.set_xlim(right=1100)
    ax_rate.set_ylim(bottom=0)
    ax_rate.set_xlim(right=1100)

    # Axes labels
    ax_mass.set_xlabel('Temperature (K)')
    ax_mass.set_ylabel('m/m$_0$ [g/g]', color = 'blue')
    ax_rate.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]', color ='red')

    # Color the y-axes (spines + ticks) to match
    ax_mass.spines['left'].set_color('blue')
    ax_mass.tick_params(axis='y', colors='blue')
    ax_rate.spines['right'].set_color('red')
    ax_rate.tick_params(axis='y', colors='red')

    # Figure title
    fig_title = path.stem

    # Legend
    fig.legend(loc = 'upper right', bbox_to_anchor=(0.85, 0.95),frameon=True)

    fig.tight_layout()
    fig.savefig(str(base_dir) + f'/TGA/Individual/{path.stem}.{ex}')
    plt.close(fig)









# plot average per TGA_set (unique institutions, unique material, unique conditions)
# and print a table with values of interest
Average_values = pd.DataFrame({
    'set': TGA_sets,
    'Duck':[label_def(t.split('_')[0])[0] for t in TGA_sets],
    'conditions':[t.split('_')[3:] for t in TGA_sets],
    'peak MLR': np.nan,
    'std peak MLR': np.nan,
    'T peak': np.nan,
    'std T peak': np.nan,
    'T onset': np.nan,
    'std T onset': np.nan
})
for idx,set in enumerate(TGA_sets):
    fig, ax_mass = plt.subplots(figsize=(6, 4))
    ax_rate = ax_mass.twinx()
    df_average = average_tga_series(set)
    
    Duck, color = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])

    # plot average
    # Plot mass (left y-axis)
    ax_mass.plot(df_average['Temperature (K)'], df_average['Normalized Mass'],
                        label='m/m$_0$', color='limegreen')
    ax_mass.fill_between(df_average['Temperature (K)'], 
                         df_average['Normalized Mass']-2*df_average['unc Normalized Mass'],
                         df_average['Normalized Mass']+2*df_average['unc Normalized Mass'],
                         color='limegreen', alpha = 0.3)

    # Plot mass loss rate (right y-axis, dashed)
    ax_rate.plot(df_average['Temperature (K)'], df_average['MLR (1/s)'],
                        label='d(m/m$_0$)/dt', color='red', alpha=0.9)

    ax_rate.fill_between(df_average['Temperature (K)'], 
                        df_average['MLR (1/s)']-2*df_average['unc MLR (1/s)'],
                        df_average['MLR (1/s)']+2*df_average['unc MLR (1/s)'],
                        color='red', alpha=0.3)


    #plot individual
    paths_TGA_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    peak_mlr_list = []
    T_peak_list = []
    T_onset_list = []
    m_400_list = []
    m_700_list = []
    m_950_list = []

    for path in paths_TGA_set:
        df_raw = pd.read_csv(path)
        df = Calculate_dm_dt(df_raw)

        peak_index = df[(df['Temperature (K)'] > 400) & (df["dm/dt"].notna())]["dm/dt"].idxmax()
        peak_mlr = df.loc[peak_index, "dm/dt"]
        T_peak = df["Temperature (K)"].iloc[peak_index]
        onset_index = df[(df['dm/dt'] >= 0.1 * peak_mlr) & (df['Temperature (K)'] > 400)].index[0]
        T_onset = df["Temperature (K)"].iloc[onset_index]
        T400_index = df[(df['Temperature (K)'] >=400)].index[0]
        m400 = 1-df["Normalized mass"].iloc[T400_index]
        try:
            T700_index = df[(df['Temperature (K)'] >=700)].index[0]
            m700 = df["Normalized mass"].iloc[T700_index]
        except:
            m700 = np.nan
        try:
            T950_index = df[(df['Temperature (K)'] >=950)].index[0]
            m950 = df["Normalized mass"].iloc[T950_index]
        except:
            m950 = np.nan

        peak_mlr_list.append(peak_mlr)
        T_peak_list.append(T_peak)
        T_onset_list.append(T_onset)
        m_400_list.append(m400)
        m_700_list.append(m700)
        m_950_list.append(m950)

        ax_mass.plot(df['Temperature (K)'], df['Normalized mass'], '.',color ='black',markersize=0.00000000000002)
        ax_rate.plot(df['Temperature (K)'], df['dm/dt'],'.',color='black', markersize=0.5)
    Average_values.at[idx, 'peak MLR'] = np.mean(peak_mlr_list)
    Average_values.at[idx, 'std peak MLR'] = np.std(peak_mlr_list, ddof=1)
    Average_values.at[idx, 'T peak'] = np.mean(T_peak_list)
    Average_values.at[idx, 'std T peak'] = np.std(T_peak_list, ddof=1)
    Average_values.at[idx, 'T onset'] = np.mean(T_onset_list)
    Average_values.at[idx, 'std T onset'] = np.std(T_onset_list, ddof=1)
    Average_values.at[idx, 'm 400'] = np.mean(m_400_list)
    Average_values.at[idx, 'std m 400'] = np.std(m_400_list, ddof=1)
    Average_values.at[idx, 'm 700'] = np.mean(m_700_list)
    Average_values.at[idx, 'std m 700'] = np.std(m_700_list, ddof=1)
    Average_values.at[idx, 'T m 950'] = np.mean(m_950_list)
    Average_values.at[idx, 'std m 950'] = np.std(m_950_list, ddof=1)

    # Set lower limits of both y-axes to 0
    ax_mass.set_ylim(bottom=0)
    ax_mass.set_xlim(right=1100)
    ax_rate.set_ylim(bottom=0)
    ax_rate.set_xlim(right=1100)

    # Axes labels
    ax_mass.set_xlabel('Temperature (K)')
    ax_mass.set_ylabel('m/m$_0$ [g/g]')
    ax_rate.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]')

    # Figure title
    plt.title(Duck+"\n"+Conditions)

    # Legend
    fig.legend()

    fig.tight_layout()
    plt.savefig(str(base_dir) + f'/TGA/Average/{set}.{ex}')
    plt.close(fig)
Average_values.drop('set',axis=1)
print(Average_values)


#plot average values 
def plot_average_values(df):
    """
    Creates 2 plots for each distinct condition:
    1) Peak MLR vs Peak Temperature
    2) Onset T vs Peak Temperature
    """
    for condition in [['N2','5K'],['N2','10K'],['N2','20K']]:
        # Filter data for this condition
        condition_data = df[df['conditions'].apply(lambda x: all(c in x for c in condition))]
        
        fig1, ax1 = plt.subplots(1, 1, figsize=(6, 4))
        fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4))
        
        # Plot 1: Peak HRR vs Peak Temperature
        for idx, row in condition_data.iterrows():
            Duck, color = label_def(row['set'].split('_')[0])
            
            ax1.errorbar(row['T peak'], 
                         row['peak MLR'],
                         xerr=row['std T peak'],
                         yerr=row['std peak MLR'],
                         fmt='o', capsize=5, capthick=2, markersize=8,
                         color=color, label=Duck)
            
            ax2.errorbar(row['T peak'], 
                         row['T onset'],
                         xerr=row['std T peak'],
                         yerr=row['std T onset'],
                         fmt='s', capsize=5, capthick=2, markersize=8,
                         color=color, label=Duck)
            
        
        ax1.set_xlabel('Peak Temperature (K)', fontsize=12)
        ax1.set_ylabel('Peak MLR (1/s)', fontsize=12)
        #ax1.set_ylim(bottom=0)
        fig1.tight_layout()
        # Remove duplicate legend entries
        handles, labels = ax1.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())
        
        ax2.set_xlabel('Peak Temperature (K)', fontsize=12)
        ax2.set_ylabel('Onset Temperature (K)', fontsize=12)
        
        # Remove duplicate legend entries
        handles, labels = ax2.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax2.legend(by_label.values(), by_label.keys())
        
        fig1.tight_layout()
        fig2.tight_layout()
        
        fig1.savefig(str(base_dir) + f'/TGA/Tpeak_Average_{condition[0]}_{condition[1]}_MLR.{ex}')
        fig2.savefig(str(base_dir) + f'/TGA/Tonset_Average_{condition[0]}_{condition[1]}.{ex}')
        
        plt.close(fig1)
        plt.close(fig2)

# Use the function
plot_average_values(Average_values)



# Average plot for Mass and mass loss rate per unique condition (averaging over different institutes)
color = {'5K':'blue','10K':'black','20K':'red'}
fig1, ax1 = plt.subplots(figsize=(6, 4))
fig2, ax2 = plt.subplots(figsize=(6, 4))
for series in ['Wood_*_N2_5K','Wood_*_N2_10K','Wood_*_N2_20K']:
    parts = series.split('_')
    atm, hr  = parts[2:]
    for subset in [item for item in TGA_sets if fnmatch(item, f'*{series}')]:
        paths = list(DATA_DIR.glob(f"*/*{subset}_*[rR]*.csv"))
        for i, path in enumerate(paths):
            df = pd.read_csv(path)
            df = Calculate_dm_dt(df)
            ax1.plot(df['Temperature (K)'], df['Normalized mass'], '.', color = color[hr], alpha=0.05, markersize = 0.01, zorder=4)
            ax2.plot(df['Temperature (K)'], df['dm/dt'], '.', color = color[hr], alpha=0.08, markersize = 0.01, zorder=4)
    df_average = average_tga_series(series,['UAI','IMT'],temp_filter={'FPL': 400})
    ax1.plot(df_average['Temperature (K)'], df_average['Normalized Mass'], label = hr + '/min', color = color[hr], zorder = 3)
    ax1.fill_between(df_average['Temperature (K)'], 
                    df_average['Normalized Mass']-2*df_average['unc Normalized Mass'],
                    df_average['Normalized Mass']+2*df_average['unc Normalized Mass'],
                    color=color[hr], alpha = 0.3, zorder=2)
    ax2.plot(df_average['Temperature (K)'], df_average['MLR (1/s)'], label = hr + '/min', color = color[hr], zorder = 3)
    ax2.fill_between(df_average['Temperature (K)'], 
                    df_average['MLR (1/s)']-2*df_average['unc MLR (1/s)'],
                    df_average['MLR (1/s)']+2*df_average['unc MLR (1/s)'],
                    color=color[hr], alpha = 0.3, zorder=2)

ax1.set_ylim(bottom=0)
ax1.set_xlim(right=1100)
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('m/m$_0$ [g/g]')
fig1.tight_layout()
ax1.legend()

ax2.set_ylim(0,0.0035)
ax2.set_xlim(right=1100)
ax2.set_xlabel('Temperature (K)')
ax2.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]')
fig2.tight_layout()
ax2.legend()

fig1.savefig(str(base_dir) + '/TGA/TGA_Average_N2_Mass.{}'.format(ex))
fig2.savefig(str(base_dir) + '/TGA/TGA_Average_N2_dmdt.{}'.format(ex))
plt.close(fig1)
plt.close(fig2)

