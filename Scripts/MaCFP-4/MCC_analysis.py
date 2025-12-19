import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import re

from Utils import device_data, get_series_names, make_institution_table, device_subset
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR
from Secret import Names

MCC_Data = device_data(DATA_DIR, 'MCC')
MCC_sets = get_series_names(MCC_Data)
unique_conditions = { '_'.join(s.split('_')[2:]) for s in MCC_sets}

# Print tables
print(make_institution_table(MCC_Data,['N2'],['60K']))


#region functions
def average_MCC_series(series_name: str):
    
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    Dataframes = []

    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df = pd.read_csv(path)
        #df = df.drop(columns=["HRR (W/g)"])

        #interpolation
        T_floor = df["Temperature (K)"].iloc[0]
        T_floor = np.floor(T_floor * 2) / 2
        T_ceil = df["Temperature (K)"].iloc[-1]
        T_ceil = np.ceil(T_ceil * 2) / 2

        InterpT = np.arange(T_floor, T_ceil, 0.5)
        length = len(InterpT)
        df_interp = pd.DataFrame(index=range(length))
        for columns in df.columns[:]:
            df_interp[columns] = np.interp(
                InterpT, df["Temperature (K)"], df[columns]
            )
        df_interp['dTdt'] = 60*np.gradient(df_interp['Temperature (K)'], df_interp['Time (s)'])
        Dataframes.append(df_interp)
    
    merged_df = Dataframes[0]
    for df in Dataframes[1:]:
        merged_df = pd.merge(
            merged_df,
            df,
            on="Temperature (K)",
            how="outer",
            suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"),
        )
    merged_df.rename(columns={"HRR (W/g)": "HRR (W/g) 1"}, inplace=True)
    merged_df.rename(columns={"Time (s)": "Time (s) 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    hrr_cols = merged_df.filter(regex=r'^HRR \(W/g\)').columns
    dTdt_cols = merged_df.filter(regex=r'^dTdt').columns

    df_average = pd.DataFrame({
        'Temperature (K)': merged_df['Temperature (K)'],
        'HRR (W/g)': merged_df[hrr_cols].mean(axis=1),
        'HRR_std': merged_df[hrr_cols].std(axis=1, skipna=True, ddof=0),
        'dTdt (K/min)': merged_df[dTdt_cols].mean(axis=1),
        'dTdt_std': merged_df[dTdt_cols].std(axis=1, skipna=True, ddof=0),
    }).dropna(subset=['HRR (W/g)'], how='all')

    return df_average


# HRR plots for all unique HR
# unique heating rates: 
unique_HR = { '_'.join(s.split('_')[3:]) for s in MCC_sets}
for HR in unique_HR:
    fig, ax = plt.subplots(figsize=(4, 3))
    MCC_sub_set = device_subset(MCC_sets, HR, 'N2') + device_subset(MCC_sets, HR, 'O2-20')
    for set in MCC_sub_set:
        average = average_MCC_series(set)
        label = Names[set.split('_')[0]]
        ax.plot(average['Temperature (K)'], average['dTdt (K/min)'], label = label)
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Heating Rate dT/dt [K min$^{-1}$]')
        ax.set_title('dT/dt in MCC tests at {} K/min'.format(HR[:-1]))
        fig.tight_layout()
        ax.legend()


# Data plots for all unique conditions
for conditions in unique_conditions:
    fig, ax = plt.subplots(figsize=(4, 3))
    HR, atm = conditions.split('_')
    MCC_subset = device_subset(MCC_sets, HR, atm)
    for set in MCC_subset:
        average = average_MCC_series(set)
        label = Names[set.split('_')[0]]
        ax.plot(average['Temperature (K)'], average['HRR (W/g)'], label = label)
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('HRR [W g^${-1}$]')
        ax.set_title('HRR in MCC tests at 60 K/min')
        fig.tight_layout()
        ax.legend()
    plt.show()




