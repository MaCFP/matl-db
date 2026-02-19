"""

Main script for Cone and gasification analysis for MaCFP-4

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import re
from scipy.signal import savgol_filter

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, format_latex
from Utils import format_with_uncertainty, format_temperature, format_regular, extract_heating_rate, extract_atmosphere, get_condition_key
from Utils import DATA_DIR


#region Save plots as pdf or png
ex = 'pdf' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'


#region create subdirectories to save plots. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Average_dir = base_dir / 'Cone' / 'Average'
Average_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what cone data is available. 
Cone_Data = device_data(DATA_DIR, 'CONE')
Cone_sets = get_series_names(Cone_Data)
Gasification_Data = device_data(DATA_DIR, 'GASIFICATION') + device_data(DATA_DIR, 'CAPA')
Gas_sets = get_series_names(Gasification_Data)

unique_conditions_cone = { '_'.join(s.split('_')[3:]) for s in Cone_sets}
unique_conditions_cone_material = sorted(set(name.split('_', 1)[1] for name in Cone_sets if '_' in name))
unique_conditions_gas = { '_'.join(s.split('_')[3:]) for s in Gas_sets}
unique_conditions_gas_material = sorted(set(name.split('_', 1)[1] for name in Gas_sets if '_' in name))

# Print tables
print('Cone table')
table = make_institution_table(Cone_Data,['Wood'],['25kW','30kW','50kW','60kW','75kW'],['hor'])
table.loc['Total'] = table.sum(axis=0)
print(table)
latex_str = format_latex(table,'Incident Heat Flux (kW/m$^2$)')
with open(str(base_dir) +'/Cone/Cone_hor.tex', 'w') as f:
    f.write(latex_str)


print('Gasification table')
Capa = make_institution_table(Gasification_Data,['Wood'],['N2'],['30kW','40kW','60kW'])
Capa.loc['Total'] = Capa.sum(axis=0)
print(Capa)
latex_str = format_latex(Capa,'Incident Heat Flux (kW/m$^2$)')
with open(str(base_dir) +'/Cone/Capa.tex', 'w') as f:
    f.write(latex_str)

Gasification = make_institution_table(Gasification_Data,['Wood'],['30kW','40kW','60kW'], ['hor'])
Gasification.loc['Total'] = Gasification.sum(axis=0)
print(Gasification)
latex_str = format_latex(Gasification,'Incident Heat Flux (kW/m$^2$)')
with open(str(base_dir) +'/Cone/Gasification.tex', 'w') as f:
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
def average_cone_series(series_name: str)->pd.DataFrame:
    """Calculate average mass and HRR for a test series."""
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



def average_Gas_series(series_name: str)->pd.DataFrame:
    """Calculate average mass and MLR for a test series."""
    paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Gasification_Data]

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
        df_interp = Calculate_dm_dt(df_interp)
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
  
    merged_df.rename(columns={'Mass (g)': "Mass (g) 1"}, inplace=True)
    merged_df.rename(columns={'dm/dt': "dm/dt 1"}, inplace=True)

    #average
    time_cols = merged_df.filter(regex=r'^Time \(s\)').columns
    mass_cols = merged_df.filter(regex=r'^Mass \(g\)').columns
    dmdt_cols = merged_df.filter(regex=r'^dm/dt').columns

    df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})
    n=2
    sum = merged_df[dmdt_cols].rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    cnt = merged_df[dmdt_cols].rolling(2*n+1, min_periods=1,center=True).count().sum(axis=1)
    df_average['dm/dt'] = sum / cnt  # Series: mean of all non-NaN values in rows i-2..i+2 across all columns

    diff = merged_df[dmdt_cols].sub(df_average['dm/dt'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1,center=True).sum().sum(axis=1)
    df_average['unc dm/dt'] = np.sqrt(sum_diff/(cnt*(cnt-1)))

    return df_average


def calculate_int_HRR(df:pd.DataFrame)->pd.DataFrame:
    """Calculate integral HRR."""
    total_hrr = np.zeros(len(df))
    for i in range(1, len(df)):
        total_hrr[i] = total_hrr[i-1] + 0.5 * (df['HRR (kW/m2)'].iloc[i-1] + df['HRR (kW/m2)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int HRR'] = total_hrr
    return df


def Calculate_dm_dt(df:pd.DataFrame):
    """Calculate mass loss rate ."""
    dt = df['Time (s)'].shift(-2) - df['Time (s)'].shift(2)
    df['dm/dt'] = (df['Mass (g)'].shift(2) - df['Mass (g)'].shift(-2)) / dt
    df['dm/dt'] = df['dm/dt'].interpolate(method='linear', limit_direction='both') #avoid nan_values
    return df


# ------------------------------------
#region Cone plots
# ------------------------------------
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
        if path.stem.split('_')[0] =='UMET':
            zorder =1
        else:
            zorder =5
        ax2.plot(df['Time (s)'], df['HRR (kW/m2)'], '.', label = label, color=color, zorder=zorder)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g/s]')
    fig1.tight_layout()
    handles1, labels1 = ax1.get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    ax1.legend(by_label1.values(), by_label1.keys())

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('HRR [kW/m$^2$]')
    fig2.tight_layout()
    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))
    ax2.legend(by_label2.values(), by_label2.keys())

    fig1.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_Mass.{}'.format(material, flux,orient,ex))
    fig2.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_HRR.{}'.format(material, flux,orient,ex))


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

    Duck, color = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])

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
    paths_CONE_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    ignition_time_list = []
    HOC_list = []

    for path in paths_CONE_set:
        df_raw = pd.read_csv(path)
        df = calculate_int_HRR(df_raw)

        ignition_index = df[df['HRR (kW/m2)'] >= 24].index[0]
        ignition_time = df["Time (s)"].iloc[ignition_index]
        m0 = np.mean(df["Mass (g)"][1:5])
        index_start = df[df['HRR (kW/m2)'] >= 24].index[0]
        index_end = df[df['HRR (kW/m2)'] >= 24].index[-1]
        if path.stem.split('_')[0] == 'UDRI':
            A_surf = 0.01
        else:
            A_surf = 0.00884
        HOC = A_surf*(df['Int HRR'][index_end]-df['Int HRR'][index_start])/(df['Mass (g)'][index_start]-df['Mass (g)'][index_end])

        ignition_time_list.append(ignition_time)
        HOC_list.append(HOC)

        ax_HRR.plot(df['Time (s)'], df['HRR (kW/m2)'], '.',color ='black',markersize=0.0002)

    Average_values.at[idx, 'ignition time'] = np.mean(ignition_time_list)
    Average_values.at[idx, 'std ignition time'] = np.std(ignition_time_list, ddof=1)
    Average_values.at[idx, 'HOC'] = np.mean(HOC_list)
    Average_values.at[idx, 'std HOC'] = np.std(HOC_list, ddof=1)

    # Set lower limits of both y-axes to 0
    ax_HRR.set_ylim(bottom=0)
    

    # Axes labels
    ax_HRR.set_xlabel('Time (s)')
    ax_HRR.set_ylabel('HRR (kW/m2)')

        # Figure title
    plt.title(Duck+"\n"+Conditions)

    # Legend
    fig.legend()

    fig.tight_layout()
    plt.savefig(str(base_dir) + f'/Cone/Average/{set}.{ex}')
    plt.close(fig)
Average_values.drop('set',axis=1)
print(Average_values)






# Average plot for Mass and mass loss rate (averaging over different institutes)
color = {'30kW':'blue','50kW':'black','60kW':'red'}
fig1, ax1 = plt.subplots(figsize=(6, 4))
for series in ['Cone_30kW_hor','Cone_50kW_hor','Cone_60kW_hor']:
    parts = series.split('_')
    flux, orient  = parts[1:]
    for subset in [item for item in Cone_sets if series in item]:
        paths = list(DATA_DIR.glob(f"*/{subset}_[rR]*.csv"))
        for i, path in enumerate(paths):
            df = pd.read_csv(path)
            df = calculate_int_HRR(df)
            ax1.plot(df['Time (s)'], df['HRR (kW/m2)'], '.', color = color[flux], alpha=0.7, markersize = 0.1, zorder=4)
    df_average = average_cone_series(series)
    ax1.plot(df_average['Time (s)'], df_average['HRR (kW/m2)'], label = flux + '/m$^2$', color = color[flux], zorder = 3)
    ax1.fill_between(df_average['Time (s)'], 
                    df_average['HRR (kW/m2)']-2*df_average['unc HRR (kW/m2)'],
                    df_average['HRR (kW/m2)']+2*df_average['unc HRR (kW/m2)'],
                    color=color[flux], alpha = 0.3, zorder=2)

ax1.set_ylim(bottom=0,top=250)
ax1.set_xlim(right=2500)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('HRR [kW/m$^2$]')
fig1.tight_layout()
ax1.legend()

fig1.savefig(str(base_dir) + '/Cone/Cone_Average_HRR.{}'.format(ex))
plt.close(fig1)


#  Back side temperature plots for all unique atmospheres and heating rates (when available)
linestyle = ['-','--',':']
for series in unique_conditions_cone_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, flux, orient  = parts[:4]
    Cone_subset_paths = [p for p in Cone_Data if dev in p.name and f"{material}_" in p.name and f"_{flux}_{orient}_" in p.name]

    for path in Cone_subset_paths:
        label, color = label_def(path.stem.split('_')[0])
        df = pd.read_csv(path)
        for i in range(1, 4):  # Check for Temperature 1, 2, 3
            temp_col = f'TC back {i} (K)'
            if temp_col in df.columns:
                ax1.plot(df['Time (s)'], df[temp_col], label=label, color=color, linestyle = linestyle[i-1])


    ax1.set_ylim(bottom=250)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    fig1.tight_layout()
    ax1.legend()

    fig1.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_BackT.{}'.format(material, flux,orient,ex))
 
    plt.close(fig1)

#  Back side temperature plots for all unique institutions, atmospheres and heating rates (when available)
linestyle = ['-',':','-.']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', "#a686c4", '#8c564b']
for idx,set in enumerate(Cone_sets):
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    paths_CONE_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    color_counter = 0
    Duck,x = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])
    for path in paths_CONE_set:
        label, color = label_def(path.stem.split('_')[0])
        df = pd.read_csv(path)
        for i in range(1, 4):  # Check for Temperature 1, 2, 3
            temp_col = f'TC back {i} (K)'
            if temp_col in df.columns:
                ax1.plot(df['Time (s)'], df[temp_col], label=label, color=colors[color_counter], linestyle = linestyle[i-1])
        if 'TC Top (K)' in df.columns:
            ax1.plot(df['Time (s)'], df['TC Top (K)'], label=label, color=colors[color_counter], dashes=[5, 10])
        color_counter = color_counter+1

    ax1.set_ylim(bottom=250, top=1200)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')

    # Figure title
    ax1.set_title(Duck+"\n"+Conditions)
    fig1.tight_layout()
    fig1.savefig(str(base_dir) + '/Cone/Individual/Cone_{}_BackT.{}'.format(set,ex))
 
    plt.close(fig1)


# ------------------------------------
#region Gasification plots
# ------------------------------------
# Mass and mass loss rate plots for all unique atmospheres and heating rates (gasification)
for series in unique_conditions_gas_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, flux, orient  = parts[:4]
    Gas_subset_paths = [p for p in Gasification_Data if f"{material}" in p.name and f"_{flux}_" in p.name]
    for path in Gas_subset_paths:
        institute = path.stem.split('_')[0]
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        if institute == 'TIFP+UCT':
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.01,41,3),'-', label = label, color=color)
        elif institute == 'FSRI':
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.00385,41,3),'-', label = label, color=color)
        ax2.plot(df['Time (s)'], df['Mass (g)'], '.', label = label, color=color)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')
    fig1.tight_layout()
    handles1, labels1 = ax1.get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    ax1.legend(by_label1.values(), by_label1.keys())

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Mass [g]')
    fig2.tight_layout()
    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))
    ax2.legend(by_label2.values(), by_label2.keys())

    fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_MLR.{}'.format(material, flux,ex))
    fig2.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_Mass.{}'.format(material, flux,ex))


    plt.close(fig1)
    plt.close(fig2)



# Indivdual Mass and mass loss rate plots for all unique institutions atmospheres and heating rates (gasification)
for set in Gas_sets:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    paths_GAS_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    for path in paths_GAS_set:
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        if institute == 'TIFP+UCT':
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.01,41,3),'-', label = label, color=color)
        elif institute == 'FSRI':
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.00385,41,3),'-', label = label, color=color)
        ax2.plot(df['Time (s)'], df['Mass (g)'], '.', label = label, color=color)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')
    fig1.tight_layout()
    handles1, labels1 = ax1.get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    ax1.legend(by_label1.values(), by_label1.keys())

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Mass [g]')
    fig2.tight_layout()
    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))
    ax2.legend(by_label2.values(), by_label2.keys())

    fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_MLR.{}'.format(material, flux,ex))
    fig2.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_Mass.{}'.format(material, flux,ex))


    plt.close(fig1)
    plt.close(fig2)



# Plots comparing parallel verus perpendicular
color = {'perpendicular':'black', 'parallel':'red'}
for flux in [30,60]:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    Cone_subset_paths = [p for p in Gasification_Data if f"TIFP+UCT_Wood_" in p.name and f"_{flux}kW_hor_" in p.name]
    for path in Cone_subset_paths:
        label = path.stem.split('_')[5]
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.01,41,3),'-', label = label, color=color[label])
        ax2.plot(df['Time (s)'], df['Mass (g)'], '.', label = label, color=color[label])

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')
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



#  Back side temperature plots (when available)
color = {'perpendicular':'black', 'parallel':'red'}
for flux in [30,60]:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    Gas_subset_paths = [p for p in Gasification_Data if f"TIFP+UCT_Wood_" in p.name and f"_{flux}kW_hor_" in p.name]
    for path in Gas_subset_paths:
        label = label_def(path.stem.split('_')[0])[0] +' ' + path.stem.split('_')[5]
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        ax1.plot(df['Time (s)'],df['TC back 1 (K)'],'-', label = label, color=color[path.stem.split('_')[5]])
        ax1.plot(df['Time (s)'],df['TC back 2 (K)'],'-',  color=color[path.stem.split('_')[5]])
        ax1.plot(df['Time (s)'],df['TC back 3 (K)'],'-',  color=color[path.stem.split('_')[5]])
    if flux == 30:
        flux = 40
    Capa_subset_paths = [p for p in Gasification_Data if f"FSRI_" in p.name and f"_{flux}kW_" in p.name]
    for path in Capa_subset_paths:
        label = label_def(path.stem.split('_')[0])[0] +' '
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        ax1.plot(df['Time (s)'],df['TC back 1 (K)'],'-', label = label, color='#aec7e8')
        ax1.plot(df['Time (s)'],df['TC Top (K)'],'.', label = label + 'Top', color="#bcbd22")


    ax1.set_ylim(bottom=280)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')
    fig1.tight_layout()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys())
    

    fig1.savefig(str(base_dir) + '/Cone/Gasification_{}_{}_{}_BackT.{}'.format(material, flux,orient,ex))
    
    plt.close(fig1)


#  Back side temperature plots for all unique institutions, atmospheres and heating rates (when available)
linestyle = ['-',':','-.']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', "#a686c4", '#8c564b']
for idx,set in enumerate(Gas_sets):
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    paths_Gas_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    color_counter = 0
    Duck,x = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])
    for path in paths_Gas_set:
        label, color = label_def(path.stem.split('_')[0])
        df = pd.read_csv(path)
        for i in range(1, 4):  # Check for Temperature 1, 2, 3
            temp_col = f'TC back {i} (K)'
            if temp_col in df.columns:
                ax1.plot(df['Time (s)'], df[temp_col], label=label, color=colors[color_counter], linestyle = linestyle[i-1])
        if 'TC Top (K)' in df.columns:
            ax1.plot(df['Time (s)'], df['TC Top (K)'], label=label, color=colors[color_counter], dashes=[1, 1])
        color_counter = color_counter+1

    ax1.set_ylim(bottom=250, top=1200)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    
    # Figure title
    ax1.set_title(Duck+"\n"+Conditions)

    fig1.tight_layout()
    fig1.savefig(str(base_dir) + '/Cone/Individual/Gasification_{}_BackT.{}'.format(set,ex))
 
    plt.close(fig1)


# plot average per Gas_set (unique institutions, unique material, unique conditions)
for idx,set in enumerate(Gas_sets):
    fig, ax = plt.subplots(figsize=(6, 4))
    df_average = average_Gas_series(set)

    Duck, color = label_def(set.split('_')[0])
    Conditions = '_'.join(set.split('_')[2:])

    # plot average
    # Plot mass (left y-axis)
    if institute == 'TIFP+UCT':
        area = 0.01
    elif institute == 'FSRI':
        area = 0.00385
    ax.plot(df_average['Time (s)'], savgol_filter(df_average['dm/dt']/area,41,3),
                        label='average MLR', color='limegreen')
    ax.fill_between(df_average['Time (s)'], 
                         savgol_filter((df_average['dm/dt']-2*df_average['unc dm/dt'])/area,41,3),
                         savgol_filter((df_average['dm/dt']+2*df_average['unc dm/dt'])/area,41,3),
                         color='limegreen', alpha = 0.3)


    #plot individual
    paths_Gas_set = list(DATA_DIR.glob(f"*/{set}_[rR]*.csv"))
    for path in paths_Gas_set:
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        ax.plot(df['Time (s)'],savgol_filter(df['dm/dt']/area,41,3), '.',color ='black',markersize=0.001)

    # Set lower limits of both y-axes to 0
    ax.set_ylim(bottom=0)

    # Axes labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')

    # Figure title
    plt.title(Duck+"\n"+Conditions)

    # Legend
    fig.legend()

    fig.tight_layout()
    plt.savefig(str(base_dir) + f'/Cone/Average/{set}.{ex}')
    plt.close(fig)



#-----------------------------------------------
# region generate latex table values of interest
#-----------------------------------------------

# Add sorting columns
Average_values['heating_rate'] = Average_values['conditions'].apply(extract_heating_rate)
Average_values['atmosphere'] = Average_values['conditions'].apply(extract_atmosphere)
Average_values['condition_key'] = Average_values['conditions']

# Sort by atmosphere, then heating rate, then Duck (institution)
final_table_sorted = Average_values.sort_values(['atmosphere', 'heating_rate', 'Duck'])



# Format ignition time
final_table_sorted['ignitiont_formatted'] = final_table_sorted.apply(
    lambda row: format_regular(row['ignition time'], row['std ignition time']),
    axis=1
)

# Format HOC total
final_table_sorted['HOC_formatted'] = final_table_sorted.apply(
    lambda row: format_regular(row['HOC'], row['std HOC']),
    axis=1
)


# Format conditions (keep as is or clean up)
final_table_sorted['conditions_formatted'] = final_table_sorted['conditions'].apply(
    lambda x: ', '.join(x) if isinstance(x, list) else str(x).replace('_', ' ')
)

# Select and rename columns for the table
columns_to_keep = ['Duck', 'conditions_formatted', 'ignitiont_formatted', 
                    'HOC_formatted', 'condition_key']

final_latex_table = final_table_sorted[columns_to_keep].copy()
final_latex_table.columns = ['Institution', 'Conditions','Ignition time (s)', 'HOC (kJ/g)', 'condition_key']

# Generate LaTeX
latex_string = final_latex_table.to_latex(
    index=False,
    escape=False,
    column_format='llcccccc',
    columns=['Institution', 'Conditions','T onset (K)','Ignition time (s)', 'HOC (kJ/g)']
)

# Modify the string
latex_string = latex_string.replace('\\toprule', '\\hline')
latex_string = latex_string.replace('\\midrule', '\\hline')
latex_string = latex_string.replace('\\bottomrule', '\\hline')

# Make column headers bold
for col in ['Institution', 'Conditions','T onset (K)','Ignition time (s)', 'HOC (kJ/g)']:
    latex_string = latex_string.replace(col, '\\textbf{'+col+'}')


# Add blank lines between different condition groups
lines = latex_string.split('\n')
new_lines = []
prev_condition_key = None

# Track condition keys as we iterate through table rows
condition_keys = final_latex_table['condition_key'].tolist()
data_row_index = 0

for i, line in enumerate(lines):
    # Check if this is a data row (contains '&' but not '\textbf')
    if '&' in line and '\\textbf' not in line and '\\hline' not in line:
        current_condition_key = condition_keys[data_row_index]
        
        # If condition key changed and this is not the first data row, add blank line
        if prev_condition_key is not None and current_condition_key != prev_condition_key:
            new_lines.append('        \\\\')
        
        prev_condition_key = current_condition_key
        data_row_index += 1
    
    new_lines.append(line)

latex_string = '\n'.join(new_lines)

# Save to file
with open(str(base_dir) + f'/Cone/Cone_Values.tex', 'w') as f:
    f.write(latex_string)
