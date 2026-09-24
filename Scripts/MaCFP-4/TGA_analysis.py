"""

Main script for TGA analysis for MaCFP-4

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import re
from collections import defaultdict
from pathlib import Path
from scipy.signal import savgol_filter
from fnmatch import fnmatch
from typing import Optional, Union, List, Dict
from matplotlib.patches import Ellipse

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation, format_latex
from Utils import format_with_uncertainty, format_temperature, format_regular, extract_heating_rate, extract_atmosphere, get_condition_key
from Utils import DATA_DIR


#region Save plots as pdf or png
ex = 'pdf' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

#region create subdirectories to save plots. 
base_dir = Path('../../Documents/SCRIPT_FIGURES')
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
def bold_total_row(latex_str):
    lines = latex_str.splitlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('Total'):
            cells = line.rstrip().removesuffix(r'\\').split('&')
            cells = [f'\\textbf{{{cell.strip()}}}' for cell in cells]
            lines[i] = ' & '.join(cells) + r' \\'

    return '\n'.join(lines)

print('Nitrogen table')
table_N2 = make_institution_table(TGA_Data,['Wood'],['N2'],['2K','3K','5K','10K','20K','30K','40K','50K'])
table_N2.loc['Total'] = table_N2.sum(axis=0)
print(table_N2)

latex_str = bold_total_row(format_latex(table_N2))
with open(str(base_dir) +'/TGA/TGA_Nitrogen.tex', 'w') as f:
    f.write(latex_str)


print('Oxygen table')
oxygen_atmospheres = sorted({s.split('_')[3] for s in TGA_sets if s.split('_')[3].startswith('O2-')}, key=lambda x: float(x.split('-')[1]))
oxygen_heating_rates = sorted({s.split('_')[4] for s in TGA_sets if s.split('_')[3].startswith('O2-')}, key=lambda x: float(x[:-1]))

table = make_institution_table(TGA_Data, ['Wood'], oxygen_atmospheres, oxygen_heating_rates)

# Remove condition columns without any measurements
table = table.loc[:, table.sum(axis=0) > 0]

# Rename atmosphere headers for the LaTeX table
table = table.rename(columns={atm: f'{atm.split("-")[1]}\\% O$_2$' for atm in oxygen_atmospheres}, level=0)

table.loc['Total'] = table.sum(axis=0)
print(table)

latex_str = bold_total_row(format_latex(table))
with open(str(base_dir) + '/TGA/TGA_Oxygen.tex', 'w') as f:
    f.write(latex_str)

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
    df['dm/dt unfiltered'] = df['dm/dt unfiltered'].interpolate(method='linear', limit_direction='both') #avoid nan_values
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

    diff = merged_df[mass_cols].sub(df_average['Normalized Mass'], axis=0) ** 2
    sum_diff = diff.rolling(2 * n + 1, min_periods=1, center=True).sum().sum(axis=1)
    variance = (sum_diff / (cnt * (cnt - 1))).where(cnt > 1)
    variance = variance.mask((variance < 0) & (variance > -1e-15), 0)
    df_average['unc Normalized Mass'] = np.sqrt(variance)

    sum = merged_df[dmdt_cols].rolling(2 * n + 1, min_periods=1, center=True).sum().sum(axis=1)
    cnt = merged_df[dmdt_cols].rolling(2 * n + 1, min_periods=1, center=True).count().sum(axis=1)

    df_average['MLR (1/s)'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns
    diff = merged_df[dmdt_cols].sub(df_average['MLR (1/s)'], axis=0) ** 2
    sum_diff = diff.rolling(2 * n + 1, min_periods=1, center=True).sum().sum(axis=1)

    variance = (sum_diff / (cnt * (cnt - 1))).where(cnt > 1)
    variance = variance.mask((variance < 0) & (variance > -1e-15), 0)
    df_average['unc MLR (1/s)'] = np.sqrt(variance)

    return df_average


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
        condition_data = condition_data[~condition_data['conditions'].apply(lambda x: '40Pa' in x)]
        
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
            
        
        ax1.set_xlabel('Peak Temperature [K]', fontsize=12)
        ax1.set_ylabel('Peak MLR [1/s]', fontsize=12)
        #ax1.set_ylim(bottom=0)
        fig1.tight_layout()
        # Remove duplicate legend entries
        handles, labels = ax1.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys())
        
        ax2.set_xlabel('Peak Temperature [K]', fontsize=12)
        ax2.set_ylabel('Onset Temperature [K]', fontsize=12)
        
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


#--------------------------------------------------------
#region plots
#--------------------------------------------------------
# HR plots for all unique HR
unique_HR = {s.split('_')[4] for s in TGA_sets}

# print('All TGA sets:')
# for s in sorted(TGA_sets):
#     print(s)

for HR in unique_HR:
    if 'iso' in HR:
        continue

    fig, ax = plt.subplots(figsize=(6, 4))
    fig_ranges, ax_ranges = plt.subplots(figsize=(6, 4))
    TGA_sub_set = [s for s in TGA_sets if s.split('_')[4] == HR]

    for set in TGA_sub_set:
        average = average_HR_tga_series(set)
        label, color = label_def(set.split('_')[0])

        ax.plot(average['Temperature (K)'], average['dTdt (K/min)'], '-', label=label, color=color)
        ax_ranges.plot(average['Temperature (K)'], average['dTdt (K/min)'], '-', label=label, color=color)

    for current_ax in [ax, ax_ranges]:
        current_ax.set_xlabel('Temperature [K]')
        current_ax.set_ylabel('Heating Rate dT/dt [K min$^{-1}$]')
        current_ax.set_xlim(right=1100)
        handles, labels = current_ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        current_ax.legend(by_label.values(), by_label.keys(), ncol=math.ceil(len(by_label)/6))

    ax.text(0.97, 0.05, f'{HR[:-1]} K/min', transform=ax.transAxes, ha='right', va='bottom', fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))

    ax_ranges.axvspan(348, 398, color='deepskyblue', alpha=0.20, zorder=0)
    ax_ranges.axvspan(500, 800, color='orange', alpha=0.15, zorder=0)
    ax_ranges.text(0.97, 0.05, f'{HR[:-1]} K/min', transform=ax_ranges.transAxes, ha='right', va='bottom', fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))

    fig.tight_layout()
    fig_ranges.tight_layout()

    fig.savefig(str(base_dir) + '/TGA/dTdt_TGA_{}Kmin.{}'.format(HR[:-1], ex))
    fig_ranges.savefig(str(base_dir) + '/TGA/dTdt_TGA_{}Kmin_ranges.{}'.format(HR[:-1], ex))

    plt.close(fig)
    plt.close(fig_ranges)
#--------------------------------------------------------


# =============================================================================
# Generate LaTeX appendix: heating-rate profiles
# =============================================================================

heating_rate_pdfs = sorted(
    (base_dir / 'TGA').glob('dTdt_TGA_*Kmin.pdf'),
    key=lambda p: float(p.stem.split('_')[-1].replace('Kmin', ''))
)

latex_lines = []

for pdf_path in heating_rate_pdfs:
    hr_value = pdf_path.stem.split('_')[-1].replace('Kmin', '')

    latex_lines.append(rf'\noindent\textbf{{$\beta$ = {hr_value}~K/min}}\par\vspace{{0.3em}}')
    latex_lines.append('')
    latex_lines.append(r'\begin{figure}[H]')
    latex_lines.append(r'    \centering')
    latex_lines.append(rf'    \includegraphics[width=0.75\linewidth]{{../SCRIPT_FIGURES/TGA/{pdf_path.name}}}')
    latex_lines.append(rf'    \caption{{Measured heating-rate profiles for TGA tests conducted at a nominal heating rate of $\beta={hr_value}$~K/min.}}')
    latex_lines.append(r'\end{figure}')
    latex_lines.append('')

latex_heating_rates = '\n'.join(latex_lines)

with open(str(base_dir) + '/TGA/TGA_Appendix_Heating_Rates.tex', 'w') as f:
    f.write(latex_heating_rates)


# =============================================================================
# Generate LaTeX appendix: mass and MLR curves in nitrogen
# =============================================================================

mass_files = sorted(
    [
        p for p in (base_dir / 'TGA').glob('TGA_Wood_N2_*_Mass.pdf')
        if '_zoom' not in p.stem
        and 'iso' not in p.stem
    ],
    key=lambda p: float(p.stem.split('_')[3].replace('K', ''))
)

latex_lines = []

for mass_path in mass_files:
    stem = mass_path.stem[:-5]  # remove "_Mass"

    dmdt_path = mass_path.with_name(stem + '_dmdt.pdf')
    mass_400_path = mass_path.with_name(stem + '_Mass_400Knorm.pdf')
    dmdt_400_path = mass_path.with_name(stem + '_dmdt_400Knorm.pdf')

    if not dmdt_path.exists() or not mass_400_path.exists() or not dmdt_400_path.exists():
        continue

    parts = stem.split('_')
    hr = parts[3]

    if hr.endswith('Kiso'):
        continue

    hr_value = hr.replace('K', '')

    latex_lines.append(rf'\noindent\textbf{{$\beta$ = {hr_value}~K/min}}\par\vspace{{0.3em}}')
    latex_lines.append('')

    # Original normalization
    latex_lines.append(r'\begin{figure}[H]')
    latex_lines.append(r'    \centering')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{mass_path.name}}}')
    latex_lines.append(r'    \hfill')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{dmdt_path.name}}}')
    latex_lines.append(rf'    \caption{{Normalized mass (left) and normalized mass loss rate (right) for TGA tests conducted in pure nitrogen at a nominal heating rate of $\beta={hr_value}$~K/min.}}')
    latex_lines.append(r'\end{figure}')
    latex_lines.append('')

    # Normalization by mass at 400 K
    latex_lines.append(r'\begin{figure}[H]')
    latex_lines.append(r'    \centering')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{mass_400_path.name}}}')
    latex_lines.append(r'    \hfill')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{dmdt_400_path.name}}}')
    latex_lines.append(rf'    \caption{{Mass normalized by the mass at 400~K (left) and corresponding normalized mass loss rate (right) for TGA tests conducted in pure nitrogen at a nominal heating rate of $\beta={hr_value}$~K/min.}}')
    latex_lines.append(r'\end{figure}')
    latex_lines.append('')

latex_mass_mlr = '\n'.join(latex_lines)

with open(str(base_dir) + '/TGA/TGA_Appendix_Mass_MLR_N2.tex', 'w') as f:
    f.write(latex_mass_mlr)



# =============================================================================
# Generate LaTeX appendix: mass and MLR curves in oxidative atmospheres
# =============================================================================

mass_files = sorted(
    [
        p for p in (base_dir / 'TGA').glob('TGA_Wood_O2-*_Mass.pdf')
        if '_zoom' not in p.stem
        and 'iso' not in p.stem
    ],
    key=lambda p: (
        float(p.stem.split('_')[2].split('-')[1]),
        float(p.stem.split('_')[3].replace('K', ''))
    )
)

latex_lines = []

for mass_path in mass_files:
    stem = mass_path.stem[:-5]

    dmdt_path = mass_path.with_name(stem + '_dmdt.pdf')
    mass_400_path = mass_path.with_name(stem + '_Mass_400Knorm.pdf')
    dmdt_400_path = mass_path.with_name(stem + '_dmdt_400Knorm.pdf')

    if not dmdt_path.exists() or not mass_400_path.exists() or not dmdt_400_path.exists():
        continue

    parts = stem.split('_')
    atm = parts[2]
    hr = parts[3]

    oxygen = atm.split('-')[1]
    hr_value = hr.replace('K', '')
    oxygen_fraction = float(oxygen) / 100

    latex_lines.append(rf'\noindent\textbf{{$X_{{\rm O_2}}={oxygen_fraction:.2f}$, $\beta$ = {hr_value}~K/min}}\par\vspace{{0.3em}}')
    latex_lines.append('')

    latex_lines.append(r'\begin{figure}[H]')
    latex_lines.append(r'    \centering')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{mass_path.name}}}')
    latex_lines.append(r'    \hfill')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{dmdt_path.name}}}')
    latex_lines.append(rf'    \caption{{Normalized mass (left) and normalized mass loss rate (right) for TGA tests conducted in an atmosphere containing {oxygen}~\% oxygen at a nominal heating rate of $\beta={hr_value}$~K/min.}}')
    latex_lines.append(r'\end{figure}')
    latex_lines.append('')

    latex_lines.append(r'\begin{figure}[H]')
    latex_lines.append(r'    \centering')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{mass_400_path.name}}}')
    latex_lines.append(r'    \hfill')
    latex_lines.append(rf'    \includegraphics[width=0.48\linewidth]{{../SCRIPT_FIGURES/TGA/{dmdt_400_path.name}}}')
    latex_lines.append(rf'    \caption{{Mass normalized by the mass at 400~K (left) and corresponding normalized mass loss rate (right) for TGA tests conducted in an atmosphere containing {oxygen}~\% oxygen at a nominal heating rate of $\beta={hr_value}$~K/min.}}')
    latex_lines.append(r'\end{figure}')
    latex_lines.append('')

latex_mass_mlr_o2 = '\n'.join(latex_lines)

with open(str(base_dir) + '/TGA/TGA_Appendix_Mass_MLR_O2.tex', 'w') as f:
    f.write(latex_mass_mlr_o2)


# Mass and mass loss rate plots for all unique atmospheres and heating rates 
plot_configs = [
    {'suffix': '', 'xlim': (None, 1100), 'ylim1': (0, None),'ylim2': (0, None)},  # Original
    {'suffix': '_zoom1', 'xlim': (None,600), 'ylim1': (0.85, 1.1),'ylim2': (0, None)},  # Zoomed version
    {'suffix': '_zoom2', 'xlim': (650, 1100), 'ylim1': (-0.09, 0.5),'ylim2': (0, None)},  # Full range
]

for series in unique_conditions_material:
    parts = series.split('_')
    material, dev, atm, hr = parts[:4]

    if atm == 'N2':
        atmosphere_label = 'N$_2$'
    elif atm == 'O2-21':
        atmosphere_label = '20–21% O$_2$'
    elif atm.startswith('O2-'):
        oxygen_concentration = atm.split('-', 1)[1]
        atmosphere_label = f'{oxygen_concentration}% O$_2$'
    else:
        atmosphere_label = atm

    if hr.endswith('Kiso'):
        condition_label = f'{hr[:-4]} K, isothermal'
    else:
        condition_label = f'{hr[:-1]} K/min'

    TGA_subset_paths = [p for p in TGA_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]

    if atm == 'O2-21':
        TGA_subset_paths += [p for p in TGA_Data if f"{material}_" in p.name and f"_O2-20_{hr}_" in p.name]

    for config in plot_configs:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        for path in TGA_subset_paths:
            df_raw = pd.read_csv(path)
            if 'FPL' in path.stem:
                df_raw = df_raw[df_raw['Temperature (K)'] > 400]
            df = Calculate_dm_dt(df_raw)
            label, color = label_def(path.stem.split('_')[0])
            T400_index = df[df['Temperature (K)'] >= 400].index[0]
            mass400 = df['Normalized mass'].iloc[T400_index]
            df['Normalized mass 400K'] = df['Normalized mass'] / mass400
            df['dm/dt 400Knorm'] = df['dm/dt'] / mass400
            if '40Pa' in path.stem:
                ax1.plot(df['Temperature (K)'], df['Normalized mass'], label=label, color=color, linestyle=':')
                ax2.plot(df['Temperature (K)'], df['dm/dt'], label=label, color=color, linestyle=':')
                ax3.plot(df['Temperature (K)'], df['Normalized mass 400K'], label=label, color=color, linestyle=':')
                ax4.plot(df['Temperature (K)'], df['dm/dt 400Knorm'], label=label, color=color, linestyle=':')
            else:
                ax1.plot(df['Temperature (K)'], df['Normalized mass'], label=label, color=color)
                ax2.plot(df['Temperature (K)'], df['dm/dt'], label=label, color=color)
                ax3.plot(df['Temperature (K)'], df['Normalized mass 400K'], label=label, color=color)
                ax4.plot(df['Temperature (K)'], df['dm/dt 400Knorm'], label=label, color=color)
        # Apply configuration
        ax1.set_ylim(bottom=config['ylim1'][0], top=config['ylim1'][1])
        ax1.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax1.set_xlabel('Temperature [K]')
        ax1.set_ylabel('m/m$_0$ [g/g]')
        fig1.tight_layout()
        handles1, labels1 = ax1.get_legend_handles_labels()
        by_label1 = dict(zip(labels1, handles1))

        if config['suffix'] == '_zoom2':
            if hr == '10K':
                ax1.legend(by_label1.values(), by_label1.keys(), fontsize=8, loc='upper left', ncol=3, columnspacing=0.9)
            else:
                ax1.legend(by_label1.values(), by_label1.keys(), loc='upper left', ncol=3, columnspacing=0.9)
        elif config['suffix'] == '_zoom1' and hr == '10K':
            ax1.legend(by_label1.values(), by_label1.keys(), fontsize=8, loc='upper left', ncol=3, columnspacing=0.9)
        elif config['suffix'] == '_zoom1':
            ax1.legend(by_label1.values(), by_label1.keys(), loc='lower left', ncol=2)
        else:
            if hr == '10K':
                ax1.legend(by_label1.values(), by_label1.keys(), fontsize=8, loc='lower left')
            else:
                ax1.legend(by_label1.values(), by_label1.keys(), loc='lower left')

        ax1.text(0.97, 0.95, f'{atmosphere_label}, {condition_label}', transform=ax1.transAxes, ha='right', va='top',
                 fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))
        ax2.set_ylim(bottom=config['ylim2'][0], top=config['ylim2'][1])
        ax2.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax2.set_xlabel('Temperature [K]')
        ax2.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]')
        fig2.tight_layout()
        handles2, labels2 = ax2.get_legend_handles_labels()
        by_label2 = dict(zip(labels2, handles2))

        if hr == '10K':
            ax2.legend(by_label2.values(), by_label2.keys(), fontsize=8, loc='upper right')
        else:
            ax2.legend(by_label2.values(), by_label2.keys(), loc='upper right')

        ax2.text(0.03, 0.95, f'{atmosphere_label}, {condition_label}', transform=ax2.transAxes, ha='left', va='top',
                 fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))

        ax3.set_ylim(bottom=config['ylim1'][0], top=config['ylim1'][1])
        ax3.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax3.set_xlabel('Temperature [K]')
        ax3.set_ylabel('m/m$_{400K}$ [g/g]')
        fig3.tight_layout()

        handles3, labels3 = ax3.get_legend_handles_labels()
        by_label3 = dict(zip(labels3, handles3))

        if config['suffix'] == '_zoom2':
            if hr == '10K':
                ax3.legend(by_label3.values(), by_label3.keys(), fontsize=8, loc='upper left', ncol=3, columnspacing=0.9)
            else:
                ax3.legend(by_label3.values(), by_label3.keys(), loc='upper left', ncol=3, columnspacing=0.9)
        elif config['suffix'] == '_zoom1':
            if hr == '10K':
                ax3.legend(by_label3.values(), by_label3.keys(), fontsize=8, loc='lower left', ncol=2)
            else:
                ax3.legend(by_label3.values(), by_label3.keys(), loc='lower left', ncol=2)
        else:
            if hr == '10K':
                ax3.legend(by_label3.values(), by_label3.keys(), fontsize=8, loc='lower left')
            else:
                ax3.legend(by_label3.values(), by_label3.keys(), loc='lower left')

        ax3.text(0.97, 0.95, f'{atmosphere_label}, {condition_label}', transform=ax3.transAxes, ha='right', va='top',
                 fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))

        ax4.set_ylim(bottom=config['ylim2'][0], top=config['ylim2'][1])
        ax4.set_xlim(left=config['xlim'][0], right=config['xlim'][1])
        ax4.set_xlabel('Temperature [K]')
        ax4.set_ylabel('d(m/m$_{400K}$)/dt [s$^{-1}$]')
        fig4.tight_layout()

        handles4, labels4 = ax4.get_legend_handles_labels()
        by_label4 = dict(zip(labels4, handles4))

        if hr == '10K':
            ax4.legend(by_label4.values(), by_label4.keys(), fontsize=8, loc='upper right')
        else:
            ax4.legend(by_label4.values(), by_label4.keys(), loc='upper right')

        ax4.text(0.03, 0.95, f'{atmosphere_label}, {condition_label}', transform=ax4.transAxes, ha='left', va='top',
                 fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.35))

        fig1.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass{config["suffix"]}.{ex}')

        if material == 'Wood' and atm == 'N2' and hr == '10K' and config['suffix'] == '':

            # BEFORE
            before_ellipse = Ellipse((410, 0.97), width=250, height=0.14, fill=False, edgecolor='black', linewidth=2.0,
                                     zorder=10)
            ax1.add_patch(before_ellipse)
            before_text = ax1.text(0.55, 0.95, 'before', transform=ax1.transAxes, ha='right', va='top', fontsize=14)

            fig1.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass_before.{ex}')

            before_ellipse.remove()
            before_text.remove()

            # MARKED REGIONS
            black_ellipse = Ellipse((340, 0.97), width=160, height=0.14, fill=False, edgecolor='black', linewidth=2.0,
                                    zorder=10)
            blue_ellipse = Ellipse((660, 0.26), width=65, height=0.32, fill=False, edgecolor='dodgerblue',
                                   linewidth=2.0, zorder=10)
            red_ellipse = Ellipse((950, 0.13), width=65, height=0.26, fill=False, edgecolor='red', linewidth=2.0,
                                  zorder=10)

            ax1.add_patch(black_ellipse)
            ax1.add_patch(blue_ellipse)
            ax1.add_patch(red_ellipse)

            fig1.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass_marked_regions.{ex}')

            # AFTER
            after_ellipse = Ellipse((410, 1.02), width=250, height=0.17, fill=False, edgecolor='black', linewidth=2.0,
                                    zorder=10)
            ax3.add_patch(after_ellipse)

            after_text = ax3.text(0.55, 0.95, 'after', transform=ax3.transAxes, ha='right', va='top', fontsize=14)

            fig3.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass_400Knorm_after.{ex}')

            after_ellipse.remove()
            after_text.remove()

        elif material == 'Wood' and atm == 'N2' and hr == '10K' and config['suffix'] == '_zoom1':
            ax1.axvline(400, color='black', linestyle=':', linewidth=2, zorder=10)

            fig1.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass_zoom1_marked.{ex}')

        fig2.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_dmdt{config["suffix"]}.{ex}')
        fig3.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_Mass_400Knorm{config["suffix"]}.{ex}')
        fig4.savefig(f'{base_dir}/TGA/TGA_{material}_{atm}_{hr}_dmdt_400Knorm{config["suffix"]}.{ex}')

        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)
        plt.close(fig4)
#--------------------------------------------------------



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
    ax_rate.plot(df['Temperature (K)'], df['dm/dt unfiltered'],'-',
                    label='d(m/m$_0$)/dt', color='red', alpha=0.9)
    ax_rate.plot(df['Temperature (K)'], df['dm/dt'],
                    label='d(m/m$_0$)/dt, filtered', color='black', linestyle='--', alpha=0.9)

     # Set lower limits of both y-axes to 0
    ax_mass.set_ylim(bottom=0)
    ax_mass.set_xlim(right=1100)
    ax_rate.set_ylim(bottom=0)
    ax_rate.set_xlim(right=1100)

    # Axes labels
    ax_mass.set_xlabel('Temperature [K]')
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
#--------------------------------------------------------



# Average plot for Mass and mass loss rate per unique condition (averaging over different institutes)
'''
Data excluded from average
(1) All data from a certain institution is excluded
- UAI: custom thermogravimetric set-up, data submitted at 20 K/min, but during test actual heating rate curve is not 20 K/min 
- IMT: peak temperature consistently higher than all other submission, considered as an outlier, therefore not included in average. 
(2) Data from a certain institution is excluded before a certain temperature:
- FPL (400K): Exclude sharp decrease in mass at beginning of test due to isotherm. 
- Ucantabria (380K): Avoid sudden drop in mass loss at the beginning of the test (causes very high dm/dt in first seconds of test), especially for the 5K/min tests.
'''

color = {'2K':'green','5K':'blue','10K':'black','20K':'red'}
fig1, ax1 = plt.subplots(figsize=(6, 4))
fig2, ax2 = plt.subplots(figsize=(6, 4))
average_data = {}

for series in ['Wood_*_N2_2K','Wood_*_N2_5K','Wood_*_N2_10K','Wood_*_N2_20K']:
    parts = series.split('_')
    atm, hr  = parts[2:]
    for subset in [item for item in TGA_sets if fnmatch(item, f'*{series}')]:
        paths = list(DATA_DIR.glob(f"*/*{subset}_*[rR]*.csv"))
        for i, path in enumerate(paths):
            df = pd.read_csv(path)
            df = Calculate_dm_dt(df)
            ax1.plot(df['Temperature (K)'], df['Normalized mass'], '-', color = color[hr], alpha=0.1, linewidth = 0.1, zorder=4)
            ax2.plot(df['Temperature (K)'], df['dm/dt'], '-', color = color[hr], alpha=0.15, linewidth = 0.1, zorder=4)
    if hr == '2K':
        df_average = average_tga_series(series, ['UAI'], temp_filter={'FPL': 400, 'UCantabria': 380})
    else:
        df_average = average_tga_series(series, ['UAI', 'IMT'], temp_filter={'FPL': 400, 'UCantabria': 380})
    average_data['Wood_'+ atm +'_' + hr] = df_average[['Temperature (K)', 'MLR (1/s)']].copy()
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
ax1.set_xlabel('Temperature [K]')
ax1.set_ylabel('m/m$_0$ [g/g]')
fig1.tight_layout()
ax1.legend()

ax2.set_ylim(0,0.0035)
ax2.set_xlim(right=1100)
ax2.set_xlabel('Temperature [K]')
ax2.set_ylabel('d(m/m$_0$)/dt [s$^{-1}$]')
fig2.tight_layout()
ax2.legend()

fig1.savefig(str(base_dir) + '/TGA/TGA_Average_N2_Mass.{}'.format(ex))
fig2.savefig(str(base_dir) + '/TGA/TGA_Average_N2_dmdt.{}'.format(ex))

for series, df_data in average_data.items():
    df_data.to_csv(str(base_dir) + '/TGA/TGA_Average_{}.csv'.format(series), index=False)

plt.close(fig1)
plt.close(fig2)




# plot average per TGA_set (unique institutions, unique material, unique conditions)
# and print a table with values of interest
Average_values = pd.DataFrame({
    'set': TGA_sets,
    'Institution':[label_def(t.split('_')[0])[0] for t in TGA_sets],
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
    m_700_400_list = []
    m_950_400_list = []

    for path in paths_TGA_set:
        df_raw = pd.read_csv(path)
        df = Calculate_dm_dt(df_raw)

        peak_index = df[(df['Temperature (K)'] > 400) & (df["dm/dt"].notna())]["dm/dt"].idxmax()
        peak_mlr = df.loc[peak_index, "dm/dt"]
        T_peak = df["Temperature (K)"].iloc[peak_index]
        onset_index = df[(df['dm/dt'] >= 0.1 * peak_mlr) & (df['Temperature (K)'] > 400)].index[0]
        T_onset = df["Temperature (K)"].iloc[onset_index]
        T400_index = df[(df['Temperature (K)'] >=400)].index[0]
        MC400 = 1-df["Normalized mass"].iloc[T400_index] # moisture content
        m400 = df["Normalized mass"].iloc[T400_index]
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

        try:
            m700_400 = m700 / m400
        except:
            m700_400 = np.nan

        try:
            m950_400 = m950 / m400
        except:
            m950_400 = np.nan

        peak_mlr_list.append(peak_mlr)
        T_peak_list.append(T_peak)
        T_onset_list.append(T_onset)
        m_400_list.append(MC400)
        m_700_list.append(m700)
        m_950_list.append(m950)
        m_700_400_list.append(m700_400)
        m_950_400_list.append(m950_400)

        ax_mass.plot(df['Temperature (K)'], df['Normalized mass'], '-', linewidth=0.05, color='black')
        ax_rate.plot(df['Temperature (K)'], df['dm/dt'], '-', linewidth=0.05, color='black', markersize=0.5)

    Average_values.at[idx, 'peak MLR'] = np.mean(peak_mlr_list)
    Average_values.at[idx, 'std peak MLR'] = np.std(peak_mlr_list, ddof=1) if len(peak_mlr_list) > 1 else np.nan
    Average_values.at[idx, 'T peak'] = np.mean(T_peak_list)
    Average_values.at[idx, 'std T peak'] = np.std(T_peak_list, ddof=1) if len(T_peak_list) > 1 else np.nan
    Average_values.at[idx, 'T onset'] = np.mean(T_onset_list)
    Average_values.at[idx, 'std T onset'] = np.std(T_onset_list, ddof=1) if len(T_onset_list) > 1 else np.nan
    Average_values.at[idx, 'm 400'] = np.mean(m_400_list)
    Average_values.at[idx, 'std m 400'] = np.std(m_400_list, ddof=1) if len(m_400_list) > 1 else np.nan
    Average_values.at[idx, 'm 700'] = np.mean(m_700_list)
    Average_values.at[idx, 'std m 700'] = np.std(m_700_list, ddof=1) if len(m_700_list) > 1 else np.nan
    Average_values.at[idx, 'm 950'] = np.mean(m_950_list)
    Average_values.at[idx, 'std m 950'] = np.std(m_950_list, ddof=1) if len(m_950_list) > 1 else np.nan
    Average_values.at[idx, 'm 700 400Knorm'] = np.mean(m_700_400_list)
    Average_values.at[idx, 'std m 700 400Knorm'] = np.std(m_700_400_list, ddof=1) if len(m_700_400_list) > 1 else np.nan
    Average_values.at[idx, 'm 950 400Knorm'] = np.mean(m_950_400_list)
    Average_values.at[idx, 'std m 950 400Knorm'] = np.std(m_950_400_list, ddof=1) if len(m_950_400_list) > 1 else np.nan

    # Set lower limits of both y-axes to 0
    ax_mass.set_ylim(bottom=0)
    ax_mass.set_xlim(right=1100)
    ax_rate.set_ylim(bottom=0)
    ax_rate.set_xlim(right=1100)

    # Axes labels
    ax_mass.set_xlabel('Temperature [K]')
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
plot_average_values(Average_values)
print(Average_values)


# =============================================================================
# Generate LaTeX appendix: individual laboratory results in nitrogen
# =============================================================================

n2_sets = [
    s for s in TGA_sets
    if s.split('_')[1] == 'Wood'
    and s.split('_')[3] == 'N2'
    and s.split('_')[4].endswith('K')
]

# Sort by heating rate, institution, and pressure
def n2_appendix_sort_key(s):
    parts = s.split('_')
    heating_rate = float(parts[4].replace('K', ''))
    institution = parts[0]

    if '40Pa' in parts:
        pressure_order = 0
    elif '100kPa' in parts:
        pressure_order = 1
    else:
        pressure_order = 0

    return heating_rate, institution, pressure_order, s


n2_sets = sorted(n2_sets, key=n2_appendix_sort_key)

heating_rates = sorted(
    {s.split('_')[4] for s in n2_sets},
    key=lambda x: float(x.replace('K', ''))
)

latex_lines = []

for hr in heating_rates:
    hr_value = hr.replace('K', '')

    # Keep the same page breaks as in the original appendix
    if hr in ['10K', '20K']:
        latex_lines.append(r'\newpage')
        latex_lines.append('')

    latex_lines.append(rf'\noindent\textbf{{$\beta$ = {hr_value}~K/min}}\par\vspace{{0.3em}}')
    latex_lines.append('')

    current_sets = [s for s in n2_sets if s.split('_')[4] == hr]

    for i, set_name in enumerate(current_sets):
        # Left figure
        if i % 2 == 0:
            latex_lines.append(r'\begin{minipage}{0.5\textwidth}')
            latex_lines.append(r'    \begin{figure}[H]')
            latex_lines.append(rf'        {{\includegraphics[width=3.25in]{{../SCRIPT_FIGURES/TGA/Average/{set_name}.pdf}}}}\\')
            latex_lines.append(r'    \end{figure}')
            latex_lines.append(r'\end{minipage}')

        # Right figure
        else:
            latex_lines.append(r'\begin{minipage}{0.35\textwidth}')
            latex_lines.append(r'    \begin{figure}[H]')
            latex_lines.append(rf'        {{\includegraphics[width=3.25in]{{../SCRIPT_FIGURES/TGA/Average/{set_name}.pdf}}}}\\')
            latex_lines.append(r'    \end{figure}')
            latex_lines.append(r'\end{minipage}\\')
            latex_lines.append('')
            latex_lines.append(r'\vfill')
            latex_lines.append('')

    # If the number of figures is odd, finish the row
    if len(current_sets) % 2 != 0:
        latex_lines.append('')
        latex_lines.append(r'\vfill')
        latex_lines.append('')

latex_individual_n2 = '\n'.join(latex_lines)

with open(str(base_dir) + '/TGA/TGA_Appendix_Individual_N2.tex', 'w') as f:
    f.write(latex_individual_n2)



# =============================================================================
# Generate LaTeX appendix: individual laboratory results in oxidative atmospheres
# =============================================================================

o2_sets = [
    s for s in TGA_sets
    if s.split('_')[1] == 'Wood'
    and s.split('_')[3].startswith('O2-')
    and s.split('_')[4].endswith('K')
]

def o2_appendix_sort_key(s):
    parts = s.split('_')
    oxygen = float(parts[3].split('-')[1])
    heating_rate = float(parts[4].replace('K', ''))
    institution = parts[0]
    return oxygen, heating_rate, institution, s

o2_sets = sorted(o2_sets, key=o2_appendix_sort_key)

conditions = sorted(
    {(s.split('_')[3], s.split('_')[4]) for s in o2_sets},
    key=lambda x: (float(x[0].split('-')[1]), float(x[1].replace('K', '')))
)

latex_lines = []

for atm, hr in conditions:
    oxygen = atm.split('-')[1]
    hr_value = hr.replace('K', '')

    latex_lines.append(rf'\noindent\textbf{{$X_{{\rm O_2}}={float(oxygen)/100:.2f}$, $\beta$ = {hr_value}~K/min}}\par\vspace{{0.3em}}')
    latex_lines.append('')

    current_sets = [
        s for s in o2_sets
        if s.split('_')[3] == atm
        and s.split('_')[4] == hr
    ]

    for i, set_name in enumerate(current_sets):
        if i % 2 == 0:
            latex_lines.append(r'\begin{minipage}{0.5\textwidth}')
            latex_lines.append(r'    \begin{figure}[H]')
            latex_lines.append(rf'        {{\includegraphics[width=3.25in]{{../SCRIPT_FIGURES/TGA/Average/{set_name}.pdf}}}}\\')
            latex_lines.append(r'    \end{figure}')
            latex_lines.append(r'\end{minipage}')
        else:
            latex_lines.append(r'\begin{minipage}{0.35\textwidth}')
            latex_lines.append(r'    \begin{figure}[H]')
            latex_lines.append(rf'        {{\includegraphics[width=3.25in]{{../SCRIPT_FIGURES/TGA/Average/{set_name}.pdf}}}}\\')
            latex_lines.append(r'    \end{figure}')
            latex_lines.append(r'\end{minipage}\\')
            latex_lines.append('')
            latex_lines.append(r'\vfill')
            latex_lines.append('')

    if len(current_sets) % 2 != 0:
        latex_lines.append('')
        latex_lines.append(r'\vfill')
        latex_lines.append('')

latex_individual_o2 = '\n'.join(latex_lines)

with open(str(base_dir) + '/TGA/TGA_Appendix_Individual_O2.tex', 'w') as f:
    f.write(latex_individual_o2)




# plot 100 kPa versus 40 kPA
fig, ax_mass = plt.subplots(figsize=(6, 4))
color = {'100kPa':'black', '40Pa':'red'}
for series in ['TUT_Wood_TGA_N2_10K_40Pa','TUT_Wood_TGA_N2_10K_100kPa']:
    paths = sorted(list(DATA_DIR.glob(f"*/*{series}_*[rR]*.csv")))

    for i, path in enumerate(paths):
        df_raw = pd.read_csv(path)
        df = Calculate_dm_dt(df_raw)

        if series.endswith('100kPa'):
            if i < 3:
                label = '100 kPa original dataset'
                linestyle = '--'
            else:
                label = '100 kPa additional dataset'
                linestyle = '-'
            plot_color = 'black'
        else:
            label = '40 Pa original dataset'
            linestyle = '--'
            plot_color = 'red'

        ax_mass.plot(df['Temperature (K)'], df['filtered'], label=label, color=plot_color, linestyle=linestyle)

# Set lower limits of both y-axes to 0
ax_mass.set_ylim(bottom=0)
ax_mass.set_xlim(right=1100)
ax_rate.set_ylim(bottom=0)
ax_rate.set_xlim(right=1100)

# Axes labels
ax_mass.set_xlabel('Temperature [K]')
ax_mass.set_ylabel('m/m$_0$ [g/g]')

# Legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), 
        loc='upper right', bbox_to_anchor=(0.85, 0.95), frameon=True)

fig.tight_layout()
fig.savefig(str(base_dir) + f'/TGA/TGA_Pressure.{ex}')
plt.close(fig)


#-----------------------------------------------
# region generate latex table values of interest
#-----------------------------------------------
# Add sorting columns
Average_values['atmosphere'] = Average_values['conditions'].apply(lambda x: x[0])
Average_values['heating_rate'] = Average_values['conditions'].apply(lambda x: x[1])
Average_values['condition_key'] = Average_values['conditions'].apply(get_condition_key)

def atmosphere_group(atm):
    if atm == 'N2':
        return 0
    if atm.startswith('O2-'):
        return 1
    return 2

def oxygen_sort_key(atm):
    if atm == 'N2':
        return 0
    if atm.startswith('O2-'):
        return float(atm.split('-')[1])
    return 999

def heating_rate_sort_key(hr):
    if 'iso' in hr:
        return 999
    return float(hr.replace('K', ''))

Average_values['atmosphere_group'] = Average_values['atmosphere'].apply(atmosphere_group)
Average_values['oxygen_sort'] = Average_values['atmosphere'].apply(oxygen_sort_key)
Average_values['heating_rate_sort'] = Average_values['heating_rate'].apply(heating_rate_sort_key)

Average_values_sorted = Average_values.sort_values(
    ['atmosphere_group', 'oxygen_sort', 'heating_rate_sort', 'Institution']
)

# Add superscript A if std is NaN (single sample)
Average_values_sorted['Institution_formatted'] = Average_values_sorted.apply(
    lambda row: f"{row['Institution']}$^A$" if pd.isna(row['std peak MLR']) else row['Institution'],
    axis=1
)

# Format MLR
Average_values_sorted['MLR_formatted'] = Average_values_sorted.apply(
    lambda row: format_with_uncertainty(row['peak MLR'], row['std peak MLR']),
    axis=1
)

# Format T peak
Average_values_sorted['T_peak_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(row['T peak'], row['std T peak']),
    axis=1
)

# Format T onset
Average_values_sorted['T_onset_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(row['T onset'], row['std T onset']),
    axis=1
)

# Format MC
Average_values_sorted['MC_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(100*row['m 400'], 100*row['std m 400']),
    axis=1
)

# Format char ratio at 700K
Average_values_sorted['c700_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(100*row['m 700'], 100*row['std m 700']),
    axis=1
)

# Format char ratio at 950K
Average_values_sorted['c950_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(100*row['m 950'], 100*row['std m 950']),
    axis=1
)

# Format char ratio at 700K normalized by mass at 400K
Average_values_sorted['c700_400_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(100*row['m 700 400Knorm'], 100*row['std m 700 400Knorm']),
    axis=1
)

# Format char ratio at 950K normalized by mass at 400K
Average_values_sorted['c950_400_formatted'] = Average_values_sorted.apply(
    lambda row: format_temperature(100*row['m 950 400Knorm'], 100*row['std m 950 400Knorm']),
    axis=1
)

# Format conditions (convert list to string)
def format_conditions(x):
    if not isinstance(x, list):
        return x

    conditions = x.copy()

    if conditions[0].startswith('O2-'):
        oxygen = conditions[0].split('-')[1]
        conditions[0] = f'{oxygen}\\% O$_2$'

    return ', '.join(conditions)

Average_values_sorted['conditions_formatted'] = Average_values_sorted['conditions'].apply(format_conditions)

# Select and rename columns for the table
columns_to_keep = ['Institution_formatted', 'conditions_formatted', 'MLR_formatted',
                   'T_peak_formatted', 'T_onset_formatted', 'MC_formatted',
                   'c700_formatted', 'c700_400_formatted',
                   'c950_formatted', 'c950_400_formatted', 'condition_key']

Average_values_table = Average_values_sorted[columns_to_keep].copy()

Average_values_table.columns = [
    'Institution',
    'Conditions',
    'peak MLR',
    'T peak',
    'T onset',
    'MC',
    'c700',
    'c700_400',
    'c950',
    'c950_400',
    'condition_key'
]

# Generate LaTeX
latex_string = Average_values_table.to_latex(
    index=False,
    escape=False,
    column_format='llcccccccc',
    columns=[
        'Institution',
        'Conditions',
        'peak MLR',
        'T peak',
        'T onset',
        'MC',
        'c700',
        'c700_400',
        'c950',
        'c950_400'
    ]
)

# Replace table rules
latex_string = latex_string.replace('\\toprule', '\\hline')
latex_string = latex_string.replace('\\midrule', '\\hline')
latex_string = latex_string.replace('\\bottomrule', '\\hline')

# Replace automatically generated header by two-row header
header_old = (
    'Institution & Conditions & peak MLR & T peak & T onset & MC & '
    'c700 & c700_400 & c950 & c950_400 \\\\'
)

header_new = (
    '\\textbf{Institution} & \\textbf{Conditions} & \\textbf{peak MLR} & '
    '\\textbf{T peak} & \\textbf{T onset} & \\textbf{MC} & '
    '\\multicolumn{2}{c}{\\textbf{700 K}} & '
    '\\multicolumn{2}{c}{\\textbf{950 K}} \\\\\n'
    ' & & \\textbf{(1/s)} & \\textbf{(K)} & \\textbf{(K)} & \\textbf{(\\%)} & '
    '\\textbf{$m/m_0$ (\\%)} & \\textbf{$m/m_{400K}$ (\\%)} & '
    '\\textbf{$m/m_0$ (\\%)} & \\textbf{$m/m_{400K}$ (\\%)} \\\\'
)

latex_string = latex_string.replace(header_old, header_new)

# Add horizontal lines between condition groups
lines = latex_string.split('\n')
new_lines = []
prev_condition_key = None
prev_atmosphere_group = None

condition_keys = Average_values_table['condition_key'].tolist()
atmosphere_groups = Average_values_sorted['atmosphere_group'].tolist()
data_row_index = 0

for line in lines:
    if '&' in line and '\\textbf' not in line and '\\multicolumn' not in line and '\\hline' not in line:
        current_condition_key = condition_keys[data_row_index]
        current_atmosphere_group = atmosphere_groups[data_row_index]

        if prev_condition_key is not None and current_condition_key != prev_condition_key:
            if current_atmosphere_group != prev_atmosphere_group:
                new_lines.append('\\hline\\hline')
            else:
                new_lines.append('\\hline')

        prev_condition_key = current_condition_key
        prev_atmosphere_group = current_atmosphere_group
        data_row_index += 1

    new_lines.append(line)

latex_string = '\n'.join(new_lines)

# Save to file
with open(str(base_dir) + '/TGA/TGA_Values.tex', 'w') as f:
    f.write(latex_string)


# =============================================================================
# Comparison of MaCFP4 and MaCFP2 TGA repeatability and reproducibility
# =============================================================================

tga_comparison_latex = r'''
\begin{tabular}{|c|c|c|}
\hline
 & \textbf{MaCFP-4} & \textbf{MaCFP-2} \\
\hline
\multirow{4}{*}{\shortstack{Intralab\\min--max\\repeatability}}
& \multicolumn{2}{c|}{Peak temperature difference} \\
\cline{2-3}
& $\sim 5$ K & $\sim 5$ K \\
\cline{2-3}
& \multicolumn{2}{c|}{Peak MLR} \\
\cline{2-3}
& $\sim 0.0002$ s$^{-1}$ ($<15\,\%$) & $\sim 0.0002$ s$^{-1}$ ($<10\,\%$) \\
\hline
\multirow{4}{*}{\shortstack{Interlab\\min--max\\reproducibility}}
& \multicolumn{2}{c|}{Peak temperature difference} \\
\cline{2-3}
& $\sim 10$ K (excl.\ outlier) & $\sim 15$ K (excl.\ outlier) \\
\cline{2-3}
& \multicolumn{2}{c|}{Peak MLR} \\
\cline{2-3}
& $\sim 0.0004$ s$^{-1}$ ($30\,\%$) & $\sim 0.0005$ s$^{-1}$ ($20\,\%$) \\
\hline
\end{tabular}
'''

with open(str(base_dir) + '/TGA/TGA_MaCFP2_Comparison.tex', 'w') as f:
    f.write(tga_comparison_latex)