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
        df.drop("stdev_mean_reflectivity(-)", axis=1)
        df.to_csv(str(Average_dir) +'Reflectivity_average.csv', index=False)
    plt.close(fig)


for series in Reflectivity_sets:
    print(f"Processing series: {series}")
    plot_average_reflectivity(series)

