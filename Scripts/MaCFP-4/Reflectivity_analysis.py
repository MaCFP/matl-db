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

    df_average = pd.DataFrame({"wavenumber (cm-1)": merged_df["wavenumber (cm-1)"]})
    df_average["avg_reflectivity"] = merged_df[reflectivity_cols].mean(axis=1)

    cnt = merged_df[reflectivity_cols].count(axis=1)
    diff_sq = merged_df[reflectivity_cols].sub(df_average["avg_reflectivity"], axis=0) ** 2
    sum_diff_sq = diff_sq.sum(axis=1)
    df_average["stdev_mean_reflectivity(-)"] = np.sqrt(sum_diff_sq / (cnt * (cnt - 1)))
    return df_average


def planck_wavenumber(nu_cm, T):
    h = 6.626e-34
    c = 3.000e8
    kB = 1.381e-23

    nu_m = nu_cm * 100

    return (2*h*c**2*nu_m**3) / (np.exp(h*c*nu_m/(kB*T)) - 1)


def calculate_effective_emissivity(df, T):
    nu = df["wavenumber (cm-1)"]
    rho = df["avg_reflectivity"]

    B = planck_wavenumber(nu, T)

    return 1 - np.sum(rho * B) / np.sum(B)



def plot_average_reflectivity(series_name: str, save: bool = True):
    """
    Plots average reflectivity vs wavenumber for a given series.
    """

    # Get averaged data
    df = average_reflectivity_series(series_name)
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]

    # Create figure
    fig, ax = plt.subplots()

    for path in paths:
        df_ind = pd.read_csv(path)
        df_ind = df_ind.rename(columns={df_ind.columns[0]: "wavenumber (cm-1)", df_ind.columns[1]: "reflectivity"})
        ax.plot(df_ind["wavenumber (cm-1)"], df_ind["reflectivity"], color='black', linewidth=0.3)
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
        save_path = Average_dir / f"{series_name}.{ex}"
        fig.savefig(save_path, bbox_inches='tight')
        df.drop("stdev_mean_reflectivity(-)", axis=1)
        df.to_csv(str(Average_dir) + f'/{series_name}.csv', index=False)
    plt.close(fig)

# Plot all individual reflectivity measurements

for path in Reflectivity_Data:
    fig, ax = plt.subplots(figsize=(6, 4))

    df = pd.read_csv(path)

    df = df.rename(columns={df.columns[0]: "wavenumber (cm-1)", df.columns[1]: "reflectivity"})

    label, color = label_def(path.stem.split('_')[0])

    ax.plot(df["wavenumber (cm-1)"], df["reflectivity"], color=color, label=label)

    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Reflectivity (-)")
    ax.set_ylim(bottom=0)

    ax.legend()

    fig.tight_layout()
    fig.savefig(str(Individual_dir) + f'/{path.stem}.{ex}')
    plt.close(fig)



for series in Reflectivity_sets:
    print(f"Processing series: {series}")
    plot_average_reflectivity(series)


# Plot all averaged reflectivity curves for Wood

fig, ax = plt.subplots(figsize=(6, 4))

wood_sets = [s for s in Reflectivity_sets if 'char' not in s.lower()]

for series in wood_sets:
    df = average_reflectivity_series(series)
    label, color = label_def(series.split('_')[0])

    ax.plot(df["wavenumber (cm-1)"], df["avg_reflectivity"], color=color, label=label)
    ax.fill_between(df["wavenumber (cm-1)"], df["avg_reflectivity"] - 2*df["stdev_mean_reflectivity(-)"], df["avg_reflectivity"] + 2*df["stdev_mean_reflectivity(-)"], color=color, alpha=0.2)

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))

ax.set_xlabel("Wavenumber (cm$^{-1}$)")
ax.set_ylabel("Reflectivity (-)")
ax.set_ylim(bottom=0)
ax.legend(by_label.values(), by_label.keys())

fig.tight_layout()
fig.savefig(str(base_dir / 'Reflectivity') + f'/Wood_Average_reflectivity_all.{ex}')
plt.close(fig)


# Plot all averaged reflectivity curves for Wood-char

fig, ax = plt.subplots(figsize=(6, 4))

char_sets = [s for s in Reflectivity_sets if 'char' in s.lower()]

linestyle_map = {
    'CAPA20': '-',
    'CAPA40': '--',
    'CAPA60': ':',
    'CONE50': '-.'
}

for series in char_sets:
    df = average_reflectivity_series(series)
    label, color = label_def(series.split('_')[0])

    linestyle = '-'
    char_type = 'char'

    for key in linestyle_map:
        if key.lower() in series.lower():
            linestyle = linestyle_map[key]
            char_type = key

    ax.plot(df["wavenumber (cm-1)"], df["avg_reflectivity"], color=color, linestyle=linestyle, label=f'{label} {char_type}')
    ax.fill_between(df["wavenumber (cm-1)"], df["avg_reflectivity"] - 2*df["stdev_mean_reflectivity(-)"], df["avg_reflectivity"] + 2*df["stdev_mean_reflectivity(-)"], color=color, alpha=0.2)

institution_handles, institution_labels = ax.get_legend_handles_labels()
by_label = dict(zip(institution_labels, institution_handles))

linestyle_handles = [plt.Line2D([0], [0], color='black', linestyle=linestyle_map[key]) for key in linestyle_map]
linestyle_labels = list(linestyle_map.keys())

legend1 = ax.legend(by_label.values(), by_label.keys(), loc='upper right')
ax.add_artist(legend1)
# ax.legend(linestyle_handles, linestyle_labels, loc='lower right')

ax.set_xlabel("Wavenumber (cm$^{-1}$)")
ax.set_ylabel("Reflectivity (-)")
ax.set_ylim(bottom=0)

fig.tight_layout()
fig.savefig(str(base_dir / 'Reflectivity') + f'/Wood-char_Average_reflectivity_all.{ex}')
plt.close(fig)



# Effective emissivity table

temperatures = [293, 313, 333, 353, 373, 393, 413, 433, 453]

rows = []

for series in sorted(Reflectivity_sets):

    df = average_reflectivity_series(series)

    institution, _ = label_def(series.split('_')[0])

    if 'char' in series.lower():
        sample = 'Wood-char'

        source = ''

        for key in ['CAPA20', 'CAPA40', 'CAPA60', 'CONE50']:
            if key.lower() in series.lower():
                if 'CAPA' in key:
                    flux = key.replace('CAPA', '')
                    source = f'CAPA {flux} kW/m$^2$'

                elif 'CONE' in key:
                    flux = key.replace('CONE', '')
                    source = f'Cone {flux} kW/m$^2$'
    else:
        sample = 'Wood'
        source = ''

    emissivities = []

    for T in temperatures:
        eps = calculate_effective_emissivity(df, T)
        emissivities.append(f'{eps:.3f}')

    rows.append([institution, sample, source] + emissivities)

columns = ['Institution', 'Sample', 'Source'] + [str(T) for T in temperatures]

df_emissivity = pd.DataFrame(rows, columns=columns)

wood_df = df_emissivity[df_emissivity['Sample'] == 'Wood']
char_df = df_emissivity[df_emissivity['Sample'] == 'Wood-char']

latex_str = '\\begin{tabular}{lll' + 'c'*len(temperatures) + '}\n'
latex_str += '\\hline\n'

latex_str += 'Institution & Sample & Source'

for T in temperatures:
    latex_str += f' & {T}'

latex_str += ' \\\\\n'
latex_str += '\\hline\n'

for _, row in wood_df.iterrows():

    latex_str += f"{row['Institution']} & {row['Sample']} & "

    latex_str += f"{row['Source']}"

    for T in temperatures:
        latex_str += f" & {row[str(T)]}"

    latex_str += ' \\\\\n'

latex_str += '\\noalign{\\vskip 4pt}\n'
latex_str += '\\hline\n'
latex_str += '\\noalign{\\vskip 4pt}\n'

for _, row in char_df.iterrows():

    latex_str += f"{row['Institution']} & {row['Sample']} & "

    latex_str += f"{row['Source']}"

    for T in temperatures:
        latex_str += f" & {row[str(T)]}"

    latex_str += ' \\\\\n'

latex_str += '\\hline\n'
latex_str += '\\end{tabular}\n'

with open(str(base_dir) + '/Reflectivity/Reflectivity_Emissivity.tex', 'w') as f:
    f.write(latex_str)

print(df_emissivity)