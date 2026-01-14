import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import re

from Utils import device_data, get_series_names, make_institution_table, \
                  device_subset, label_def, interpolation
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR
from Secret import Names

#define whether to save files in pdf or png
ex = 'pdf' #options 'pdf' or 'png

#when pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

# check all subdirectories to save plots exist. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Individual_dir = base_dir / 'MCC' / 'Individual'
Average_dir = base_dir / 'MCC' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what MCC data is available. 

# All MCC Data
MCC_Data = device_data(DATA_DIR, 'MCC')
# All unique sets (name without repetition number)
MCC_sets = get_series_names(MCC_Data)
# All unique conditions over all institutes
unique_conditions = { '_'.join(s.split('_')[2:]) for s in MCC_sets}

#Print tables with Institute name (Duck version) and amount of repetition experiments
print('Nitrogen table')
print(make_institution_table(MCC_Data,['N2'],['30K','45K','60K']))

print('Oxygen table')
print(make_institution_table(MCC_Data,['O2-20', 'O2-21'],['60K']))

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
#region set plot style
# ------------------------------------
def average_MCC_series(series_name: str):
    
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    Dataframes = []

    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data
    for i, path in enumerate(paths):
        df = pd.read_csv(path)

        #interpolation
       # df_interp = interpolation(df)
        df_interp = df
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


def calculate_int_HRR(df:pd.DataFrame):
    total_hrr = np.zeros(len(df))
    for i in range(1, len(df)):
        total_hrr[i] = total_hrr[i-1] + 0.5 * (df['HRR (W/g)'].iloc[i-1] + df['HRR (W/g)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int HRR'] = total_hrr
    return df




# HRR plots for all unique HR
# unique heating rates: 
unique_HR = { '_'.join(s.split('_')[3:]) for s in MCC_sets}
for HR in unique_HR:
    fig, ax = plt.subplots(figsize=(4, 3))
    MCC_sub_set = device_subset(MCC_sets, HR, 'N2') + device_subset(MCC_sets, HR, 'O2-20')
    for set in MCC_sub_set:
        average = average_MCC_series(set)
        label, color = label_def(set.split('_')[0])
        ax.plot(average['Temperature (K)'], average['dTdt (K/min)'],'.', markersize=0.8, label = label, color = color)
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Heating Rate dT/dt [K min$^{-1}$]')
        ax.set_title('dT/dt in MCC tests at {} K/min'.format(HR[:-1]))
        fig.tight_layout()
        ax.legend()
    plt.savefig(str(base_dir) + '/MCC/HR_MCC_{}Kmin.pdf'.format(HR[:-1]))
    plt.close(fig)






# HRR and int HRR rate plots for all unique atmospheres and heating rates 
for series in unique_conditions:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    atm, hr,  = parts[:2]
    MCC_subset_paths = [p for p in MCC_Data if f"_{atm}_{hr}_" in p.name]
    for path in MCC_subset_paths:
        df_raw = pd.read_csv(path)
        df = calculate_int_HRR(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Temperature (K)'], df['HRR (W/g)'], label = label, color=color)
        ax2.plot(df['Temperature (K)'], df['Int HRR'], label = label, color=color)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('HRR [W g$^{-1}$]')
    fig1.tight_layout()
    ax1.legend()

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('Integral HRR [J g$^{-1}$]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/MCC/MCC_{}_{}_HRR.{}'.format(atm,hr,ex))
    fig2.savefig(str(base_dir) + '/MCC/MCC_{}_{}_int_HRR.{}'.format(atm,hr,ex))
    plt.close(fig1)
    plt.close(fig2)


#check mass scaling FZJ
# HRR and int HRR rate plots for all unique atmospheres and heating rates 
initial_mass = {
    'R1': {'mass': 0.98, 'color': 'darkviolet'},
    'R2': {'mass': 2.0, 'color': 'darkred'},
    'R3': {'mass': 1.95, 'color': 'red'},
    'R4': {'mass': 1.93, 'color': 'lightcoral'},
    'R5': {'mass': 3.97, 'color': 'darkgreen'},
    'R6': {'mass': 5.98, 'color': 'darkblue'},
    'R7': {'mass': 5.96, 'color': 'blue'},
    'R8': {'mass': 6.09, 'color': 'royalblue'},
    'R9': {'mass': 7.17, 'color': 'darkgoldenrod'},
    'R10': {'mass': 7.19, 'color': 'goldenrod'},
    'R11': {'mass': 7.23, 'color': 'gold'},
    'R12': {'mass': 3.91, 'color': 'lime'},
    'R13': {'mass': 3.99, 'color': 'limegreen'},
    'R14': {'mass': 4.09, 'color': 'green'},
    'R15': {'mass': 7.09, 'color': 'black'}
}

fig1, ax1 = plt.subplots(figsize=(6, 4))
for test in DATA_DIR.rglob("FZJ/FZJ_*60K*.csv"):
    parts = test.stem.split('_')
    Repetition = parts[-1]
    df_raw = pd.read_csv(test)
    df = calculate_int_HRR(df_raw)
    #ax1.plot(df['Temperature (K)'], df['HRR (W/g)'], label = initial_mass[Repetition]['mass'], color = initial_mass[Repetition]['color'] )
    ax1.plot(df['Temperature (K)'], np.gradient(df['Temperature (K)'], df['Time (s)']), label = initial_mass[Repetition]['mass'], color = initial_mass[Repetition]['color'] )

# Sort legend
handles, labels = ax1.get_legend_handles_labels()
labels_float = [float(label) for label in labels]
sorted_pairs = sorted(zip(labels_float, handles))
sorted_labels = [label for label, _ in sorted_pairs]
sorted_handles = [handle for _, handle in sorted_pairs]

ax1.set_ylim(bottom=0)
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('HRR [W g$^{-1}$]')
fig1.tight_layout()
ax1.legend(sorted_handles, sorted_labels)

fig1.savefig(str(base_dir) + '/MCC/MCC_FZJ_60K_HR_Mass-Scaling_HRR.{}'.format(ex))
plt.close(fig1)
 