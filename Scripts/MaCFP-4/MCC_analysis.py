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
unique_conditions_material = sorted(set(name.split('_', 1)[1] for name in MCC_sets if '_' in name))

#Print tables with Institute name (Duck version) and amount of repetition experiments
print('Nitrogen table')
print(make_institution_table(MCC_Data,['Wood'],['N2'],['30K','45K','60K']))

print('Oxygen table')
print(make_institution_table(MCC_Data,['Wood'],['O2-20', 'O2-21'],['60K']))

print('Char table')
print(make_institution_table(MCC_Data,['Wood-char'],['O2-20', 'O2-21'],['60K']))

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
def calculate_int_HRR(df:pd.DataFrame):
    total_hrr = np.zeros(len(df))
    for i in range(1, len(df)):
        total_hrr[i] = total_hrr[i-1] + 0.5 * (df['HRR (W/g)'].iloc[i-1] + df['HRR (W/g)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int HRR'] = total_hrr
    return df


def average_MCC_series(series_name: str):
    paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in MCC_Data]

    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data
    for i, path in enumerate(paths):
        df = pd.read_csv(path)
        df = calculate_int_HRR(df)
        #interpolation
        df_interp = interpolation(df)
        #df_interp = df
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
    intHRR_cols = merged_df.filter(regex=r'^Int HRR').columns

    df_average = pd.DataFrame({
        'Temperature (K)': merged_df['Temperature (K)'],
        'HRR (W/g)': merged_df[hrr_cols].mean(axis=1),
        'HRR_std': merged_df[hrr_cols].std(axis=1, skipna=True, ddof=0),
        'dTdt (K/min)': merged_df[dTdt_cols].mean(axis=1),
        'dTdt_std': merged_df[dTdt_cols].std(axis=1, skipna=True, ddof=0),
        'int HRR': merged_df[intHRR_cols].mean(axis=1),
        'int HRR_std': merged_df[intHRR_cols].std(axis=1, skipna=True, ddof=0),
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
for series in unique_conditions_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, atm, hr,  = parts[:4]
    MCC_subset_paths = [p for p in MCC_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]
    for path in MCC_subset_paths:
        df_raw = pd.read_csv(path)
        df_interp = interpolation(df_raw)
        df = calculate_int_HRR(df_interp)
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

    fig1.savefig(str(base_dir) + '/MCC/MCC_{}_{}_{}_HRR.{}'.format(material,atm,hr,ex))
    fig2.savefig(str(base_dir) + '/MCC/MCC_{}_{}_{}_int_HRR.{}'.format(material, atm,hr,ex))
    plt.close(fig1)
    plt.close(fig2)


#check mass scaling FZJ
# HRR and int HRR rate plots for all unique atmospheres and heating rates 
# initial_mass = {
#     'R1': {'mass': 0.98, 'color': 'darkviolet'},
#     'R2': {'mass': 2.0, 'color': 'darkred'},
#     'R3': {'mass': 1.95, 'color': 'red'},
#     'R4': {'mass': 1.93, 'color': 'lightcoral'},
#     'R5': {'mass': 3.97, 'color': 'darkgreen'},
#     'R6': {'mass': 5.98, 'color': 'darkblue'},
#     'R7': {'mass': 5.96, 'color': 'blue'},
#     'R8': {'mass': 6.09, 'color': 'royalblue'},
#     'R9': {'mass': 7.17, 'color': 'darkgoldenrod'},
#     'R10': {'mass': 7.19, 'color': 'goldenrod'},
#     'R11': {'mass': 7.23, 'color': 'gold'},
#     'R12': {'mass': 3.91, 'color': 'lime'},
#     'R13': {'mass': 3.99, 'color': 'limegreen'},
#     'R14': {'mass': 4.09, 'color': 'green'},
#     'R15': {'mass': 7.09, 'color': 'black'}
# }

# fig1, ax1 = plt.subplots(figsize=(6, 4))
# for test in DATA_DIR.rglob("FZJ/FZJ_*60K*.csv"):
#     parts = test.stem.split('_')
#     Repetition = parts[-1]
#     df_raw = pd.read_csv(test)
#     df = calculate_int_HRR(df_raw)
#     ax1.plot(df['Temperature (K)'], df['HRR (W/g)'], label = initial_mass[Repetition]['mass'], color = initial_mass[Repetition]['color'] )
#     #ax1.plot(df['Temperature (K)'], np.gradient(df['Temperature (K)'], df['Time (s)']), label = initial_mass[Repetition]['mass'], color = initial_mass[Repetition]['color'] )

# # Sort legend
# handles, labels = ax1.get_legend_handles_labels()
# labels_float = [float(label) for label in labels]
# sorted_pairs = sorted(zip(labels_float, handles))
# sorted_labels = [label for label, _ in sorted_pairs]
# sorted_handles = [handle for _, handle in sorted_pairs]

# ax1.set_ylim(bottom=0)
# ax1.set_xlabel('Temperature (K)')
# ax1.set_ylabel('HRR [W g$^{-1}$]')
# fig1.tight_layout()
# ax1.legend(sorted_handles, sorted_labels)

# fig1.savefig(str(base_dir) + '/MCC/MCC_FZJ_60K_Mass-Scaling_HRR.{}'.format(ex))
# plt.close(fig1)
 


# plot average per MCC_set (unique institutions, unique material, unique conditions)
# and print a table with values of interest
Average_values = pd.DataFrame({
    'set': MCC_sets,
    'Duck':[label_def(t.split('_')[0])[0] for t in MCC_sets],
    'conditions':[t.split('MCC_')[1] for t in MCC_sets],
    'peak HRR': np.nan,
    'std peak HRR': np.nan,
    'T peak': np.nan,
    'std T peak': np.nan,
    'T onset': np.nan,
    'std T onset': np.nan,
    "HR_total":np.nan,
    "std HR_total":np.nan,
    "HR_capacity":np.nan,
    "std HR_capacity":np.nan,
    "FGC":np.nan,
    "std FGC":np.nan,
})
for idx,set in enumerate(MCC_sets):
    fig, ax_HRR = plt.subplots(figsize=(6, 4))
    ax_intHRR = ax_HRR.twinx()
    df_average = average_MCC_series(set)

    # plot average
    # Plot HRRs (left y-axis)
    ax_HRR.plot(df_average['Temperature (K)'], df_average['HRR (W/g)'],
                        label='HRR', color='limegreen')
    ax_HRR.fill_between(df_average['Temperature (K)'], 
                         df_average['HRR (W/g)']-2*df_average['HRR_std'],
                         df_average['HRR (W/g)']+2*df_average['HRR_std'],
                         color='limegreen', alpha = 0.3)

    # Plot mass loss rate (right y-axis, dashed)
    ax_intHRR.plot(df_average['Temperature (K)'], df_average['int HRR'],
                        label='integral HRR', color='red', alpha=0.9)

    ax_intHRR.fill_between(df_average['Temperature (K)'], 
                        df_average['int HRR']-2*df_average['int HRR_std'],
                        df_average['int HRR']+2*df_average['int HRR_std'],
                        color='red', alpha=0.3)


    #plot individual
    paths_MCC_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    peak_HRR_list = []
    T_peak_list = []
    T_onset_list = []
    FGC_list = []
    HR_total_list = []
    HR_capacity_list = []
    T_0 = 298

    for path in paths_MCC_set:
        df_raw = pd.read_csv(path)
        df = calculate_int_HRR(df_raw)
        peak_HRR = df["HRR (W/g)"].max()
        peak_index = df["HRR (W/g)"].idxmax()
        T_peak = df["Temperature (K)"].iloc[peak_index]
        HR_total = df['Int HRR'].iloc[-1]
        onset_index = df[df['Int HRR'] >= 0.05 * HR_total].index[0]
        T_onset = df["Temperature (K)"].iloc[onset_index]
        endset_index = df[df['Int HRR'] >= 0.95 * HR_total].index[0]
        T_endset = df["Temperature (K)"].iloc[endset_index]
        HR_Capacity = peak_HRR / np.average(np.gradient(df['Temperature (K)'], df['Time (s)']))
        FGC = (HR_total * (T_endset - T_0)) / ((T_endset - T_onset) * (T_onset - T_0)), 1
        

        peak_HRR_list.append(peak_HRR)
        T_peak_list.append(T_peak)
        T_onset_list.append(T_onset)
        FGC_list.append(FGC)
        HR_total_list.append(HR_total)
        HR_capacity_list.append(HR_Capacity)

        ax_HRR.plot(df['Temperature (K)'], df['HRR (W/g)'], '.',color ='black',markersize=0.00000000000002)
        ax_intHRR.plot(df['Temperature (K)'], df['Int HRR'],'.',color='black', markersize=0.5)
    Average_values.at[idx, 'peak HRR'] = np.mean(peak_HRR_list)
    Average_values.at[idx, 'std peak HRR'] = np.std(peak_HRR_list, ddof=1)
    Average_values.at[idx, 'T peak'] = np.mean(T_peak_list)
    Average_values.at[idx, 'std T peak'] = np.std(T_peak_list, ddof=1)
    Average_values.at[idx, 'T onset'] = np.mean(T_onset_list)
    Average_values.at[idx, 'std T onset'] = np.std(T_onset_list, ddof=1)
    Average_values.at[idx, 'HR_total'] = np.mean(HR_total_list)
    Average_values.at[idx, 'std HR_total'] = np.std(HR_total_list, ddof=1)
    Average_values.at[idx, 'HR_capacity'] = np.mean(HR_capacity_list)
    Average_values.at[idx, 'std HR_capacity'] = np.std(HR_capacity_list, ddof=1)
    Average_values.at[idx, 'FGC'] = np.mean(FGC_list)
    Average_values.at[idx, 'std FGC'] = np.std(FGC_list, ddof=1)

    # Set lower limits of both y-axes to 0
    ax_HRR.set_ylim(bottom=0)
    ax_intHRR.set_ylim(bottom=0)

    # Axes labels
    ax_HRR.set_xlabel('Temperature (K)')
    ax_HRR.set_ylabel('HRR [W g$^{-1}$]')
    ax_intHRR.set_ylabel('Integral HRR [J g$^{-1}$]')

    # Figure title
    fig_title = set

    # Legend
    fig.legend()

    fig.tight_layout()
    plt.savefig(str(base_dir) + f'/MCC/Average/{set}.{ex}')
    plt.close(fig)
Average_values.drop('set',axis=1)
print(Average_values)


# Average plot for Mass and mass loss rate per unique condition (averaging over different institutes)
# HR plots for all unique HR
color = {'30K':'blue','45K':'black','60K':'red'}
fig1, ax1 = plt.subplots(figsize=(6, 4))
fig2, ax2 = plt.subplots(figsize=(6, 4))
for series in ['Wood_MCC_N2_30K','Wood_MCC_N2_45K','Wood_MCC_N2_60K']:
    parts = series.split('_')
    atm, hr  = parts[2:]
    df_average = average_MCC_series(series)
    ax1.plot(df_average['Temperature (K)'], df_average['HRR (W/g)'], label = hr, color = color[hr])
    ax1.fill_between(df_average['Temperature (K)'], 
                    df_average['HRR (W/g)']-2*df_average['HRR_std'],
                    df_average['HRR (W/g)']+2*df_average['HRR_std'],
                    color=color[hr], alpha = 0.3)
    ax2.plot(df_average['Temperature (K)'], df_average['int HRR'], label = hr, color = color[hr])
    ax2.fill_between(df_average['Temperature (K)'], 
                    df_average['int HRR']-2*df_average['int HRR_std'],
                    df_average['int HRR']+2*df_average['int HRR_std'],
                    color=color[hr], alpha = 0.3)

ax1.set_ylim(bottom=0)
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('HRR [W/g]')
fig1.tight_layout()
ax1.legend()

ax2.set_ylim(bottom=0)
ax2.set_xlabel('Temperature (K)')
ax2.set_ylabel('Integral HRR [J/g]')
fig2.tight_layout()
ax2.legend()

fig1.savefig(str(base_dir) + '/MCC/MCC_Average_N2_HRR.{}'.format(ex))
fig2.savefig(str(base_dir) + '/MCC/MCC_Average_N2_intHRR.{}'.format(ex))
plt.close(fig1)
plt.close(fig2)