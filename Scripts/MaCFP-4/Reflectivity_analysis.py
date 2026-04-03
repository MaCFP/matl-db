"""

Main script for Reflectivity/Emissivity analysis for MaCFP-4

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

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation, format_latex
from Utils import format_with_uncertainty, format_temperature, format_regular, extract_heating_rate, extract_atmosphere, get_condition_key
from Utils import DATA_DIR


#region Save plots as pdf or png
ex = 'pdf' #options 'pdf' or 'png


#region create subdirectories to save plots. 
base_dir = Path('../../Documents/SCRIPT_FIGURES')
Individual_dir = base_dir / 'Reflectivity' / 'Individual'
Average_dir = base_dir / 'Reflectivity' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
# All Reflectivity data
Reflectivity_Data = device_data(DATA_DIR, 'REFLECTIVITY')

# All unique sets (name without repetition number, e.g.TUT_TGA_N2_10K_40Pa )
Reflectivity_sets = get_series_names(Reflectivity_Data)

# All unique conditions over all institutes
# unique_conditions = { '_'.join(s.split('_')[3:]) for s in Reflectivity_sets}
# unique_conditions_material = sorted(set(name.split('_', 1)[1] for name in Reflectivity_sets if '_' in name))


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

def average_reflectivity_series(series_name: str) -> pd.DataFrame:
    """
    For a given series, finds all repeat Reflectivity CSVs (_R#),
    merges them on wavenumber, and computes the average reflectivity.
    """

    # Find files matching series pattern
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]

    if len(paths) == 0:
        raise Exception(f"No files found for series {series_name}")

    merged_df = None

    for i, path in enumerate(sorted(paths)):
        df = pd.read_csv(path)

        # Standardize column names just in case
        df = df.rename(columns={
            df.columns[0]: "wavenumber (cm-1)",
            df.columns[1]: f"reflectivity_R{i+1}"
        })

        if merged_df is None:
            merged_df = df
        else:
            # Merge on wavenumber to ensure alignment
            merged_df = pd.merge(
                merged_df,
                df,
                on="wavenumber (cm-1)",
                how="inner"
            )

    # Compute average reflectivity across all repeat columns
    reflectivity_cols = [col for col in merged_df.columns if "reflectivity_R" in col]
    merged_df["avg_reflectivity"] = merged_df[reflectivity_cols].mean(axis=1)

    cnt = merged_df[reflectivity_cols].count(axis=1)
    diff_sq = merged_df[reflectivity_cols].sub(merged_df["avg_reflectivity"], axis=0) ** 2
    sum_diff_sq = diff_sq.sum(axis=1)
    merged_df["stdev_mean_reflectivity(-)"] = np.sqrt(sum_diff_sq / (cnt * (cnt - 1)))
    return merged_df

print("merged_df")

def plot_average_reflectivity(series_name: str, save: bool = True):
    """
    Plots average reflectivity vs wavenumber for a given series.
    """

    # Get averaged data
    df = average_reflectivity_series(series_name)

    # Create figure
    fig, ax = plt.subplots()

    ax.plot(
        df["wavenumber (cm-1)"],
        df["avg_reflectivity"],
        label=series_name,)
    ax.fill_between(df['wavenumber (cm-1)'], 
            df['avg_reflectivity']-2*df['stdev_mean_reflectivity(-)'],
            df['avg_reflectivity']+2*df['stdev_mean_reflectivity(-)'],
            color='blue', alpha = 0.3, zorder=2)
    

    # Labels and styling
    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Average Reflectivity (-)")
    # ax.set_title(f"{series_name} - Average Reflectivity")

    # ax.legend()
    ax.grid(False)

    # Save figure
    if save:
        # save_path = Average_dir / f"{series_name}_avg_reflectivity.{ex}"
        save_path = Average_dir / f"Avg_reflectivity.{ex}"
        fig.savefig(save_path, bbox_inches='tight')

    plt.close(fig)


for series in Reflectivity_sets:
    print(f"Processing series: {series}")
    plot_average_reflectivity(series)


# #-----------------------------------------------
# # region generate latex table values of interest
# #-----------------------------------------------
# # Add sorting columns
# Average_values['heating_rate'] = Average_values['conditions'].apply(extract_heating_rate)
# Average_values['atmosphere'] = Average_values['conditions'].apply(extract_atmosphere)
# Average_values['condition_key'] = Average_values['conditions'].apply(get_condition_key)

# # Sort by atmosphere, then heating rate, then institution
# Average_values_sorted = Average_values.sort_values(['atmosphere', 'heating_rate', 'Institution'])

# # Add superscript A if std is NaN (single sample)
# Average_values_sorted['Institution_formatted'] = Average_values_sorted.apply(
#     lambda row: f"{row['Institution']}$^A$" if pd.isna(row['std peak MLR']) else row['Institution'],
#     axis=1
# )

# # Format MLR
# Average_values_sorted['MLR_formatted'] = Average_values_sorted.apply(
#     lambda row: format_with_uncertainty(row['peak MLR'], row['std peak MLR']),
#     axis=1
# )

# # Format T peak
# Average_values_sorted['T_peak_formatted'] = Average_values_sorted.apply(
#     lambda row: format_temperature(row['T peak'], row['std T peak']),
#     axis=1
# )

# # Format T onset
# Average_values_sorted['T_onset_formatted'] = Average_values_sorted.apply(
#     lambda row: format_temperature(row['T onset'], row['std T onset']),
#     axis=1
# )

# # Format MC
# Average_values_sorted['MC_formatted'] = Average_values_sorted.apply(
#     lambda row: format_temperature(100*row['m 400'], 100*row['std m 400']),
#     axis=1
# )

# # Format char ratio at 700K
# Average_values_sorted['c700_formatted'] = Average_values_sorted.apply(
#     lambda row: format_temperature(100*row['m 700'], 100*row['std m 700']),
#     axis=1
# )

# # Format char ratio at 950K
# Average_values_sorted['c950_formatted'] = Average_values_sorted.apply(
#     lambda row: format_temperature(100*row['m 950'], 100*row['std m 950']),
#     axis=1
# )


# # Format conditions (convert list to string)
# Average_values_sorted['conditions_formatted'] = Average_values_sorted['conditions'].apply(
#     lambda x: ', '.join(x) if isinstance(x, list) else x
# )

# # Select and rename columns for the table
# columns_to_keep = ['Institution_formatted', 'conditions_formatted', 'MLR_formatted', 
#                 'T_peak_formatted', 'T_onset_formatted','MC_formatted', 'c700_formatted','c950_formatted', 'condition_key']

# Average_values_table = Average_values_sorted[columns_to_keep].copy()
# Average_values_table.columns = ['Institution', 'Conditions', 'peak MLR (1/s)', 
#                                 'T peak (K)', 'T onset (K)', 'MC (\\%)', 'm/m_{0} at 700~K (\\%)','m/m_{0} at 950~K (\\%)' , 'condition_key']

# # Generate LaTeX
# latex_string = Average_values_table.to_latex(
#     index=False,
#     escape=False,
#     column_format='llcccccc',
#     columns=['Institution', 'Conditions', 'peak MLR (1/s)', 'T peak (K)', 'T onset (K)','MC (\\%)', 'm/m_{0} at 700~K (\\%)','m/m_{0} at 950~K (\\%)' ]
# )

# # Modify the string
# latex_string = latex_string.replace('\\toprule', '\\hline')
# latex_string = latex_string.replace('\\midrule', '\\hline')
# latex_string = latex_string.replace('\\bottomrule', '\\hline')

# # Make column headers bold
# latex_string = latex_string.replace('Institution', '\\textbf{Institution}')
# latex_string = latex_string.replace('Conditions', '\\textbf{Conditions}')
# latex_string = latex_string.replace('peak MLR (1/s)', '\\textbf{peak MLR (1/s)}')
# latex_string = latex_string.replace('T peak (K)', '\\textbf{T peak (K)}')
# latex_string = latex_string.replace('T onset (K)', '\\textbf{T onset (K)}')
# latex_string = latex_string.replace('MC (\\%)', '\\textbf{MC (\\%)}')
# latex_string = latex_string.replace('m/m_{0} at 700~K (\\%)', '\\textbf{$m/m_{0}$ at 700~K (\\%)}')
# latex_string = latex_string.replace('m/m_{0} at 950~K (\\%)', '\\textbf{$m/m_{0}$ at 950~K (\\%)}')

# # Add blank lines between different condition groups (first two items)
# lines = latex_string.split('\n')
# new_lines = []
# prev_condition_key = None

# # Track condition keys as we iterate through table rows
# condition_keys = Average_values_table['condition_key'].tolist()
# data_row_index = 0

# for i, line in enumerate(lines):
#     # Check if this is a data row (contains '&' but not '\textbf')
#     if '&' in line and '\\textbf' not in line and '\\hline' not in line:
#         current_condition_key = condition_keys[data_row_index]
        
#         # If condition key changed and this is not the first data row, add blank line
#         if prev_condition_key is not None and current_condition_key != prev_condition_key:
#             new_lines.append('        \\\\')
        
#         prev_condition_key = current_condition_key
#         data_row_index += 1
    
#     new_lines.append(line)

# latex_string = '\n'.join(new_lines)

# # Save to file
# with open(str(base_dir) + f'/TGA/TGA_Values.tex', 'w') as f:
#     f.write(latex_string)