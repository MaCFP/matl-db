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
    print(inst_codes)
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

    df.index.name = "Institution"
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