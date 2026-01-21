import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import re

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR
from scipy.signal import savgol_filter

#define whether to save files in pdf or png
ex = 'pdf' #options 'pdf' or 'png

#when pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'


# check all subdirectories to save plots exist. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Individual_dir = base_dir / 'Cone' / 'Individual'
Average_dir = base_dir / 'Cone' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what cone data is available. 
Cone_Data = device_data(DATA_DIR, 'CONE')
Gasification_Data = device_data(DATA_DIR, 'GASIFICATION')
Cone_sets = get_series_names(Cone_Data)
Gas_sets = get_series_names(Gasification_Data)
Gasification_sets = get_series_names(Gasification_Data)
unique_conditions_cone = { '_'.join(s.split('_')[3:]) for s in Cone_sets}
unique_conditions_cone_material = sorted(set(name.split('_', 1)[1] for name in Cone_sets if '_' in name))
unique_conditions_gas = { '_'.join(s.split('_')[3:]) for s in Gas_sets}
unique_conditions_gas_material = sorted(set(name.split('_', 1)[1] for name in Gas_sets if '_' in name))

# Print tables
print('Cone table')
print(make_institution_table(Cone_Data,['Wood'],['30kW','60kW'],['hor']))
print('Gasification table')
print(make_institution_table(Gasification_Data,['Wood'],['30kW','60kW'],['hor']))



def average_cone_series(series_name: str):
    
    paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]

    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df_raw = pd.read_csv(path)

        t_floor = df_raw["Time (s)"].iloc[0]
        t_floor = np.ceil(t_floor) 
        t_ceil = df_raw["Time (s)"].iloc[-1]
        t_ceil = np.floor(t_ceil) 

        InterpT = np.arange(t_floor, t_ceil+1, 1)
        length = len(InterpT)
        df_interp = pd.DataFrame(index=range(length))
        for columns in df_raw.columns[:]:
            df_interp[columns] = np.interp(
                InterpT, df_raw["Time (s)"], df_raw[columns]
            )
        #interpolation
        Dataframes.append(df_interp)

    merged_df = Dataframes[0]
    for df in Dataframes[1:]:
        merged_df = pd.merge(
            merged_df,
            df,
            on="Time (s)",
            how="outer",
            suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"),
        )
  
    merged_df.rename(columns={'HRR (kW/m2)': "HRR (kW/m2) 1"}, inplace=True)
    merged_df.rename(columns={'Mass (g)': "Mass (g) 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    mass_cols = merged_df.filter(regex=r'^Mass \(g\)').columns
    HRR_cols = merged_df.filter(regex=r'^HRR \(kW/m2\)').columns
    df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})
    n=2
    sum = merged_df[HRR_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[HRR_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['HRR (kW/m2)'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[HRR_cols].sub(df_average['HRR (kW/m2)'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc HRR (kW/m2)'] = np.sqrt(sum_diff/(cnt*(cnt-1)))


    return df_average




# Mass and HRR plots for all unique atmospheres and heating rates
for series in unique_conditions_cone_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, flux, orient  = parts[:4]
    Cone_subset_paths = [p for p in Cone_Data if f"{material}_" in p.name and f"_{flux}_{orient}_" in p.name]
    for path in Cone_subset_paths:
        df_raw = pd.read_csv(path)
        df=df_raw
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Time (s)'],savgol_filter((-1)*np.gradient(df['Mass (g)'],df['Time (s)']),53,3),'-', label = label, color=color)
        ax2.plot(df['Time (s)'], df['HRR (kW/m2)'], '.', label = label, color=color)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g/s]')
    fig1.tight_layout()
    ax1.legend()

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('HRR [kW/m$^2$]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_Mass.{}'.format(material, flux,orient,ex))
    fig2.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_HRR.{}'.format(material, flux,orient,ex))


    plt.close(fig1)
    plt.close(fig2)



# Mass and mass loss rate plots for all unique atmospheres and heating rates
for series in unique_conditions_gas_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, flux, orient  = parts[:4]
    Cone_subset_paths = [p for p in Gasification_Data if f"{material}" in p.name and f"_{flux}_{orient}_" in p.name]
    for path in Cone_subset_paths:
        df_raw = pd.read_csv(path)
        df=df_raw
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Time (s)'],savgol_filter((-1)*np.gradient(df['Mass (g)'],df['Time (s)']),53,3),'-', label = label, color=color)
        ax2.plot(df['Time (s)'], df['Mass (g)'], '.', label = label, color=color)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g/s]')
    fig1.tight_layout()
    ax1.legend()

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Mass [g]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_{}_MLR.{}'.format(material, flux,orient,ex))
    fig2.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_{}_Mass.{}'.format(material, flux,orient,ex))


    plt.close(fig1)
    plt.close(fig2)




# plot average per Cone_set (unique institutions, unique material, unique conditions)
# and print a table with values of interest
Average_values = pd.DataFrame({
    'set': Cone_sets,
    'Duck':[label_def(t.split('_')[0])[0] for t in Cone_sets],
    'conditions':[t.split('_')[3:] for t in Cone_sets],
})
for idx,set in enumerate(Cone_sets):
    fig, ax_HRR = plt.subplots(figsize=(6, 4))
    ax_rate = ax_HRR.twinx()
    df_average = average_cone_series(set)

    # plot average
    # Plot mass (left y-axis)
    ax_HRR.plot(df_average['Time (s)'], df_average['HRR (kW/m2)'],
                        label='HRR', color='limegreen')
    ax_HRR.fill_between(df_average['Time (s)'], 
                         df_average['HRR (kW/m2)']-2*df_average['unc HRR (kW/m2)'],
                         df_average['HRR (kW/m2)']+2*df_average['unc HRR (kW/m2)'],
                         color='limegreen', alpha = 0.3)

    # Plot mass loss rate (right y-axis, dashed)
    # ax_rate.plot(df_average['Temperature (K)'], df_average['MLR (1/s)'],
    #                     label='d(m/m$_0$)/dt', color='red', alpha=0.9)

    # ax_rate.fill_between(df_average['Temperature (K)'], 
    #                     df_average['MLR (1/s)']-2*df_average['unc MLR (1/s)'],
    #                     df_average['MLR (1/s)']+2*df_average['unc MLR (1/s)'],
    #                     color='red', alpha=0.3)


    #plot individual
    paths_TGA_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    # peak_mlr_list = []
    # T_peak_list = []
    # T_onset_list = []

    for path in paths_TGA_set:
        df_raw = pd.read_csv(path)
        df = df_raw

        # peak_mlr = df["dm/dt"].max()
        # peak_index = df["dm/dt"].idxmax()
        # T_peak = df["Temperature (K)"].iloc[peak_index]
        # onset_index = df[df['dm/dt'] >= 0.1 * peak_mlr].index[0]
        # T_onset = df["Temperature (K)"].iloc[onset_index]

        # peak_mlr_list.append(peak_mlr)
        # T_peak_list.append(T_peak)
        # T_onset_list.append(T_onset)

        ax_HRR.plot(df['Time (s)'], df['HRR (kW/m2)'], '.',color ='black',markersize=0.0002)

    # Average_values.at[idx, 'peak MLR'] = np.mean(peak_mlr_list)
    # Average_values.at[idx, 'std peak MLR'] = np.std(peak_mlr_list, ddof=1)
    # Average_values.at[idx, 'T peak'] = np.mean(T_peak_list)
    # Average_values.at[idx, 'std T peak'] = np.std(T_peak_list, ddof=1)
    # Average_values.at[idx, 'T onset'] = np.mean(T_onset_list)
    # Average_values.at[idx, 'std T onset'] = np.std(T_onset_list, ddof=1)

    # Set lower limits of both y-axes to 0
    ax_HRR.set_ylim(bottom=0)
    

    # Axes labels
    ax_HRR.set_xlabel('Time (s)')
    ax_HRR.set_ylabel('HRR (kW/m2)')

    # Figure title
    fig_title = set

    # Legend
    fig.legend()

    fig.tight_layout()
    plt.savefig(str(base_dir) + f'/Cone/Average/{set}.{ex}')
    plt.close(fig)
Average_values.drop('set',axis=1)
print(Average_values)


# parallel versus perpendicular
# Mass and mass loss rate plots for all unique atmospheres and heating rates
color = {'perpendicular':'black', 'parallel':'red'}
for flux in [30,60]:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    Cone_subset_paths = [p for p in Gasification_Data if f"Wood_" in p.name and f"_{flux}kW_hor_" in p.name]
    for path in Cone_subset_paths:
        label = path.stem.split('_')[5]
        df = pd.read_csv(path)
        ax1.plot(df['Time (s)'],savgol_filter((-1)*np.gradient(df['Mass (g)'],df['Time (s)']),53,3),'-', label = label, color=color[label])
        ax2.plot(df['Time (s)'], df['Mass (g)'], '.', label = label, color=color[label])

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g/s]')
    fig1.tight_layout()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys())
    
    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Mass [g]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}kW_{}_MLR_grain.{}'.format(material, flux,orient,ex))
    fig2.savefig(str(base_dir) + '/Cone/Gasification_{}_{}kW_{}_Mass_grain.{}'.format(material, flux,orient,ex))


    plt.close(fig1)
    plt.close(fig2)


#  Back side temperature plots for all unique atmospheres and heating rates (when available)
linestyle = ['-','--',':']
for series in unique_conditions_cone_material+unique_conditions_gas_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, flux, orient  = parts[:4]
    if dev =='Cone':
        Cone_subset_paths = [p for p in Cone_Data if dev in p.name and f"{material}_" in p.name and f"_{flux}_{orient}_" in p.name]
    else:
        Cone_subset_paths = [p for p in Gasification_Data if dev in p.name and f"{material}_" in p.name and f"_{flux}_{orient}_" in p.name]

    for path in Cone_subset_paths:
        label, color = label_def(path.stem.split('_')[0])
        df = pd.read_csv(path)
        for i in range(1, 4):  # Check for Temperature 1, 2, 3
            temp_col = f'TC back {i} (K)'
            if temp_col in df.columns:
                ax1.plot(df['Time (s)'], df[temp_col], label=label, color=color, linestyle = linestyle[i-1])


    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    fig1.tight_layout()
    ax1.legend()
    
    if dev == 'Cone':
        fig1.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_BackT.{}'.format(material, flux,orient,ex))
    elif dev == 'Gasification':
        fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_{}_BackT.{}'.format(material, flux,orient,ex))
    
    plt.close(fig1)
