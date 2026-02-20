"""

Common functions for MaCFP-4 thermal analysis data processing.

This module provides utilities for:
- Loading and filtering experimental data from multiple institutions
- Mapping institution codes to anonymized labels and colors
- Creating data availability summary tables
- Interpolating temperature-dependent measurements

"""

import re
import pandas as pd
import numpy as np

from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import List, Tuple


#region get input path 
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "Wood" / "Calibration_Data"


# region define labs, corresponding labels and colors
labs = sorted(d.name for d in DATA_DIR.iterdir() if d.is_dir() and d.name != "TEMPLATE-INSTITUTE-X")

CODES = ["Pekin", "Tufted", "Aylesbury", "Orpington","Rouen", 
         "Saxony", "Ruddy", "Cayuga","Redhead", "Buff",  
         "Bali", "Magpie", "Ancona", "Crested", "Call",  
         "Muscovy", "Pomeranian",  "Shetland", "Alabio", "Mallard", "Hardhead"]


colors = ["#1f77b4", "#98df8a", "#17becf", "#ff7f0e", "#aec7e8", 
          "#ff9896", "#c5b0d5", "#2ca02c",  "#c49c94", "#d62728",
          "#dbdb8d", "#c7c7c7",  "#ffbb78", "#bcbd22", "#8c564b", 
          "#f7b6d2","#e377c2", "#9edae5", "#7f7f7f","#9467bd" , "#DAA520"
]


assert len(CODES) >= len(labs), "Not enough codes for all institutions"
assert len(colors) >= len(labs), "Not enough colors for all institutions"

#region functions
def label_def(lab:str) -> Tuple[str,str]:
    """returns label and color for every lab"""
    IDX = labs.index(lab)
    label = CODES[IDX]
    color = colors[IDX]
    return label, color



def device_data(directory:Path, device:str)->List[Path]:
    """creates list of all CSV files for a specific measurement device."""
    paths = [
        p
        for p in DATA_DIR.rglob("*.csv")
        if p.is_file()
        if device in p.name.upper()
        if not any(parent.name.startswith("TEMPLATE-INSTITUTE-X") for parent in p.parents)
    ]
    return paths



def device_subset(serieslist:List, heatingrate:str, atmosphere:str)->List[Path]:
    """creates subset of device data for the specified heating rate and atmosphere"""
    sub_list = [
        p
        for p in serieslist
        if heatingrate in p
        if atmosphere in p
        if 'iso' not in p
    ]
    return sub_list


def get_series_names(data_list:List[Path])->List[str]:
    """Get unique series names from CSV files in the data list"""
    series_set = set()

    # Find all CSV files recursively
    for csv_file in data_list:
        stem = csv_file.stem
        match = re.match(r"^(.*)_[Rr]\d+$", stem)
        series_name = match.group(1) if match else stem
        series_set.add(series_name)

    return sorted(list(series_set))  # Return sorted list for consistent ordering




# tables
def make_institution_table(
    paths: List[Path], materials:List[str],
    atmospheres:List[str],
    heating_rates:List[str],
) -> pd.DataFrame:
    """
    Build a count table of data availability by institution.

    Parameters
    ----------
    paths : list[Path]
        List of CSV file paths
    atmospheres : list[str]
        Atmospheres to include (e.g. ['N2', 'O2-21'])
    heating_rates : list[str]
        Heating rates to include (e.g. ['10K'])

    Returns
    -------
    pandas.DataFrame
    """

    # counts[(inst_code, atmosphere, heating_rate)] = count
    counts = defaultdict(int)

    for p in paths:
        name = p.stem
        parts = name.split("_")
        if len(parts) < 5:
            continue

        inst, mat, _, atm, hr = parts[:5]
        if mat not in materials:
            continue
        if atm not in atmospheres:
            continue
        if hr not in heating_rates:
            continue

        counts[(label_def(inst)[0], mat, atm, hr)] += 1
        
    # ---------- Table construction logic ----------
    inst_codes = [code for code in CODES if any(counts.get((code, mat,atm, hr), 0) > 0 for mat in materials for atm in atmospheres for hr in heating_rates)]
    # Case 1: single atmosphere → columns = heating rates
    if len(atmospheres) == 1 and len(heating_rates) > 1:
        atm = atmospheres[0]
        data = {
            hr: [sum(counts.get((inst,m, atm, hr), 0) for m in materials) for inst in inst_codes]
            for hr in heating_rates
        }
        df = pd.DataFrame(data, index=inst_codes)

    # Case 2: single heating rate → columns = atmospheres
    elif len(heating_rates) == 1 and len(atmospheres) > 1:
        hr = heating_rates[0]
        data = {
            atm: [sum(counts.get((inst,m, atm, hr), 0) for m in materials) for inst in inst_codes]
            for atm in atmospheres
        }
        df = pd.DataFrame(data, index=inst_codes)

    # Case 3: multiple atmospheres AND heating rates
    else:
        columns = pd.MultiIndex.from_product(
            [atmospheres, heating_rates],
            names=["Atmosphere", "Heating Rate"]
        )

        data = []
        for inst in inst_codes:
            row = [
                sum(counts.get((inst,m, atm, hr), 0) for m in materials)
                for atm, hr in columns
            ]
            data.append(row)

        df = pd.DataFrame(data, index=inst_codes, columns=columns)

    return df




def interpolation(df:pd.DataFrame) -> pd.DataFrame:
    """Interpolates dataframe to 0.5 K temperature intervals"""
    T_floor = df["Temperature (K)"].iloc[0]
    T_floor = np.ceil(T_floor) 
    T_ceil = df["Temperature (K)"].iloc[-1]
    T_ceil = np.floor(T_ceil) 
    InterpT = np.arange(T_floor, T_ceil+0.5, 0.5)
    length = len(InterpT)
    df_interp = pd.DataFrame(index=range(length))
    for columns in df.columns[:]:
        df_interp[columns] = np.interp(
            InterpT, df["Temperature (K)"], df[columns]
        )
    return df_interp


def format_latex(table:pd.DataFrame, column_name:str='Heating Rate, $\\beta$ (K/min)'):
    """Given a panda dataframe, formats the latex table""" 
    latex_str = table.to_latex(column_format='l' + 'c'*len(table.columns), escape=False)
    lines = latex_str.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        # Add the header line with multicolumn for "Heating Rate (K/min)"
        if line[0:1] == '\\':
            new_lines.append(line)
        
        # Replace column headers (3K, 5K, etc.) with just numbers
        elif line[0:1] == ' ':
            # Extract and clean the heating rates
            new_line = ' & \\multicolumn{'+ str(len(table.columns)) + '}{c}{' + column_name + '} \\\\' 
            new_lines.append(new_line)
            parts = line.split('&')
            if column_name == 'Heating Rate, $\\beta$ (K/min)':
                rate_parts = [p.split('K')[0] for p in parts[1:]]
                new_line = 'Institution' + ' & ' + ' & '.join(rate_parts) + '\\\\'
                new_lines.append(new_line)
            elif column_name == 'Oxygen concentration (Vol\\%)':
                rate_parts = [p.split('O2-')[1] for p in parts[1:]]
                new_line = 'Institution' + ' & ' + ' & '.join(rate_parts)
                new_lines.append(new_line)
            elif column_name == 'Incident Heat Flux (kW/m$^2$)':
                rate_parts = [p.split('kW')[0] for p in parts[1:]]
                new_line = 'Institution' + ' & ' + ' & '.join(rate_parts) + '\\\\'
                new_lines.append(new_line)


        elif line[0:5] == 'Total':
            new_lines.append('\\hline')
            new_lines.append(line)
        
        else:
            new_lines.append(line)
    
    latex_str = '\n'.join(new_lines)

    latex_str = latex_str.replace('\\toprule', '\\hline')
    latex_str = latex_str.replace('\\midrule', '\\hline \\\\')
    latex_str = latex_str.replace('\\bottomrule', '\\hline \\\\')

    return latex_str


#Formatting functions for latex value tables
# Helper function to format values with uncertainty
def format_with_uncertainty(mean, std):
    """Format value with uncertainty in scientific notation"""
    if pd.isna(std) or std == 0:
        # Single sample: no uncertainty
        exponent = int(np.floor(np.log10(abs(mean))))
        mantissa = mean / (10 ** exponent)
        return f"${mantissa:.2f} \\times 10^{{{exponent}}}$"
    else:
        # Multiple samples: show mean ± std
        exponent = int(np.floor(np.log10(abs(mean))))
        mean_mantissa = mean / (10 ** exponent)
        std_mantissa = std / (10 ** exponent)
        return f"$({mean_mantissa:.2f} \\pm {std_mantissa:.2f}) \\times 10^{{{exponent}}}$"

def format_temperature(mean, std):
    """Format temperature (no scientific notation)"""
    if abs(mean) < 0.005:  # avoid -0.0
        mean = 0.0
    if pd.isna(std) or std == 0:
        return f"${mean:.1f}$"
    else:
        return f"${mean:.1f} \\pm {std:.1f}$"

def format_regular(mean, std):
    """Format regular numbers (no scientific notation)"""
    if pd.isna(std) or std == 0:
        return f"${mean:.2f}$"
    else:
        return f"${mean:.2f} \\pm {std:.2f}$"

# Extract sorting keys from conditions
def extract_heating_rate(conditions):
    """Extract numeric heating rate from conditions string"""
    import re
    match = re.search(r'(\d+)K', str(conditions))
    if match:
        return int(match.group(1))
    return 0

def extract_atmosphere(conditions):
    """Extract atmosphere from conditions string (part before underscore)"""
    return str(conditions).split('_')[0]

def get_condition_key(conditions):
    """Get first two items of conditions for grouping"""
    if isinstance(conditions, list):
        return tuple(conditions[:2]) if len(conditions) >= 2 else tuple(conditions)
    return ()