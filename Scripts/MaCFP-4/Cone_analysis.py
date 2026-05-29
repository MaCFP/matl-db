"""

Main script for Cone and gasification analysis for MaCFP-4

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import re
from scipy.signal import savgol_filter
from typing import Optional, Union, List, Dict

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, format_latex
from Utils import format_ignition, format_regular, extract_heating_rate, extract_atmosphere, get_condition_key
from Utils import DATA_DIR


#region Save plots as pdf or png
ex = 'pdf' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'


#region create subdirectories to save plots. 
base_dir = Path('../../Documents/SCRIPT_FIGURES')
Average_dir = base_dir / 'Cone' / 'Average'
Average_dir.mkdir(parents=True, exist_ok=True)
Average_dir = base_dir / 'Cone' / 'Individual'
Average_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what cone data is available.
Cone_Data = device_data(DATA_DIR, 'CONE')
Cone_sets = get_series_names(Cone_Data)
Gasification_Data = device_data(DATA_DIR, 'GASIFICATION') + device_data(DATA_DIR, 'CAPA') + device_data(DATA_DIR, 'FPA')
Gas_sets = get_series_names(Gasification_Data)

unique_conditions_cone = { '_'.join(s.split('_')[3:]) for s in Cone_sets}
unique_conditions_cone_material = sorted(set(name.split('_', 1)[1] for name in Cone_sets if '_' in name))
unique_conditions_gas = { '_'.join(s.split('_')[3:]) for s in Gas_sets}
unique_conditions_gas_material = sorted(set(name.split('_', 1)[1] for name in Gas_sets if '_' in name))
kw_values = set()
for item in unique_conditions_gas:
    match = re.search(r'\d+kW', item)
    if match:
        kw_values.add(match.group())
gas_flux = sorted(kw_values)

cone_flux = ['25kW', '30kW', '45kW', '50kW', '60kW', '75kW']
cone_color = {'25kW': 'green', '30kW': 'blue', '45kW': 'cyan', '50kW': 'black', '60kW': 'red', '75kW': 'purple'}


# Print tables
# print('\nAvailable gasification heat fluxes:')
# print(sorted(gas_flux))
#
# print('\nAvailable gasification conditions:')
# for item in sorted(unique_conditions_gas):
#     print(item)

print('Cone table')
table = make_institution_table(Cone_Data,['Wood'],cone_flux,['hor'])
table.loc['Total'] = table.sum(axis=0)
print(table)
latex_str = format_latex(table,'Incident Heat Flux (kW/m$^2$)')
with open(str(base_dir) +'/Cone/Cone_hor.tex', 'w') as f:
    f.write(latex_str)


print('Gasification table')
Capa = make_institution_table(Gasification_Data,['Wood'],['N2'],['30kW','40kW','50kW','60kW','70kW'])
Capa.loc['Total'] = Capa.sum(axis=0)
print(Capa)
latex_str = format_latex(Capa,'Incident Heat Flux (kW/m$^2$)')
with open(str(base_dir) +'/Cone/Capa.tex', 'w') as f:
    f.write(latex_str)

Gasification = make_institution_table(Gasification_Data, ['Wood'], sorted(gas_flux), ['hor'])
Gasification = Gasification.loc[:, Gasification.sum(axis=0) > 0]
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
def get_grain_orientation(path):
    name = path.stem.lower()

    if 'perpendicular' in name:
        return 'Perpendicular'

    return 'Parallel'


def get_cone_grain_series_key(path):
    stem = re.sub(r'_[Rr]\d+$', '', path.stem)

    if 'perpendicular' in stem.lower() or 'parallel' in stem.lower():
        return stem

    return stem + '_Parallel'


def get_cone_grain_paths(series_name):
    return [p for p in Cone_Data if get_cone_grain_series_key(p) == series_name]


def get_grain_linestyle_from_name(name):
    if 'perpendicular' in name.lower():
        return '--'
    return '-'

def average_cone_series(series_name: str, exclude: Optional[Union[str, List[str]]] = None, exclude_individual: Optional[Union[str, List[str]]] = None, include_grain_variants: bool = False) -> pd.DataFrame:
    """Calculate average mass and HRR for a test series.
    Args:
        series_name: Name of the test series to search for
        exclude: String or list of strings to exclude entire groups (partial path matching)
        exclude_individual: String or list of strings to exclude individual experiments (e.g., "R1", "r2")
    """

    if include_grain_variants:
        paths = list(DATA_DIR.glob(f"*/*{series_name}*_[rR]*.csv"))
    else:
        paths = list(DATA_DIR.glob(f"*/*{series_name}_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]

    # Apply institution exclusions
    if exclude is not None:
        if not isinstance(exclude, list):
            exclude = [exclude]  # Convert single string to list
        
        for excl in exclude:
            paths = [p for p in paths if excl not in str(p)]

    # Apply individual experiment exclusions
    if exclude_individual is not None:
        if not isinstance(exclude_individual, list):
            exclude_individual = [exclude_individual]
        
        for excl in exclude_individual:
            # Match full experiment name in the file stem
            paths = [p for p in paths if excl not in p.stem]


    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df_raw = pd.read_csv(path)

        t_floor = df_raw["Time (s)"].iloc[0]
        t_ceil = df_raw["Time (s)"].iloc[-1]
        # Guard against NaN or empty time columns
        if pd.isna(t_floor) or pd.isna(t_ceil) or t_ceil <= t_floor:
            print(f"WARNING: Skipping {path} — invalid time range ({t_floor} to {t_ceil})")
            continue
        t_floor = np.ceil(t_floor) 
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

def average_cone_grain_series(series_name: str, exclude: Optional[Union[str, List[str]]] = None, exclude_individual: Optional[Union[str, List[str]]] = None) -> pd.DataFrame:
    paths = get_cone_grain_paths(series_name)
    paths = [p for p in paths if "TEMPLATE" not in str(p)]

    # Apply institution exclusions
    if exclude is not None:
        if not isinstance(exclude, list):
            exclude = [exclude]

        for excl in exclude:
            paths = [p for p in paths if excl not in str(p)]

    # Apply individual experiment exclusions
    if exclude_individual is not None:
        if not isinstance(exclude_individual, list):
            exclude_individual = [exclude_individual]

        for excl in exclude_individual:
            paths = [p for p in paths if excl not in p.stem]

    Dataframes = []
    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    for path in paths:
        df_raw = pd.read_csv(path)

        t_floor = df_raw["Time (s)"].iloc[0]
        t_ceil = df_raw["Time (s)"].iloc[-1]

        if pd.isna(t_floor) or pd.isna(t_ceil) or t_ceil <= t_floor:
            print(f"WARNING: Skipping {path} — invalid time range ({t_floor} to {t_ceil})")
            continue

        t_floor = np.ceil(t_floor)
        t_ceil = np.floor(t_ceil)

        InterpT = np.arange(t_floor, t_ceil + 1, 1)
        df_interp = pd.DataFrame(index=range(len(InterpT)))

        for column in df_raw.columns:
            df_interp[column] = np.interp(InterpT, df_raw["Time (s)"], df_raw[column])

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

    HRR_cols = merged_df.filter(regex=r'^HRR \(kW/m2\)').columns

    df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})

    n = 2
    sum_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)
    cnt_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).count().sum(axis=1)

    df_average['HRR (kW/m2)'] = sum_hrr / cnt_hrr

    diff = merged_df[HRR_cols].sub(df_average['HRR (kW/m2)'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)

    df_average['unc HRR (kW/m2)'] = np.sqrt(sum_diff/(cnt_hrr*(cnt_hrr-1)))

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

def average_gasification_paths(paths):

    Dataframes = []

    for path in paths:
        df_raw = pd.read_csv(path)

        t_floor = np.ceil(df_raw["Time (s)"].iloc[0])
        t_ceil = np.floor(df_raw["Time (s)"].iloc[-1])

        if pd.isna(t_floor) or pd.isna(t_ceil) or t_ceil <= t_floor:
            continue

        InterpT = np.arange(t_floor, t_ceil + 1, 1)
        df_interp = pd.DataFrame(index=range(len(InterpT)))

        for column in df_raw.columns:
            df_interp[column] = np.interp(InterpT, df_raw["Time (s)"], df_raw[column])

        df_interp = Calculate_dm_dt(df_interp)

        area = get_gas_area(path)
        df_interp['MLR'] = df_interp['dm/dt'] / area

        Dataframes.append(df_interp)

    if len(Dataframes) == 0:
        return None

    merged_df = Dataframes[0]

    for df in Dataframes[1:]:
        merged_df = pd.merge(merged_df, df, on="Time (s)", how="outer", suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"))

    merged_df.rename(columns={'MLR': 'MLR 1'}, inplace=True)

    MLR_cols = merged_df.filter(regex=r'^MLR').columns

    df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})

    n = 2
    sum_mlr = merged_df[MLR_cols].rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)
    cnt_mlr = merged_df[MLR_cols].rolling(2*n+1, min_periods=1, center=True).count().sum(axis=1)

    df_average['MLR'] = sum_mlr / cnt_mlr

    diff = merged_df[MLR_cols].sub(df_average['MLR'], axis=0)**2
    sum_diff = diff.rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)

    df_average['unc MLR'] = np.sqrt(sum_diff / (cnt_mlr * (cnt_mlr - 1)))

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

def get_gas_area(path):
    institute = path.stem.split('_')[0]

    if institute in ['TIFP+UCT', 'Aalto', 'UQ']:
        return 0.01
    elif institute in ['TUBS']:
        return 0.00884
    elif institute in ['UMD', 'FSRI']:
        return 0.00385

    return np.nan

# ------------------------------------
#region Cone plots
# ------------------------------------
# Mass and HRR plots for all unique atmospheres and heating rates
for series in unique_conditions_cone_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))

    parts = series.split('_')
    material, dev, flux, orient = parts[:4]

    Cone_subset_paths = [p for p in Cone_Data
                         if f"{material}_" in p.name and f"_{flux}_{orient}_" in p.name]

    orientation_handles = {
        'Parallel': plt.Line2D([0], [0], color='black', linestyle='-'),
        'Perpendicular': plt.Line2D([0], [0], color='black', linestyle=(0, (1, 2)))
    }

    institution_handles = {}

    for path in Cone_subset_paths:
        df_raw = pd.read_csv(path)
        df = df_raw

        label, color = label_def(path.stem.split('_')[0])

        grain_orientation = get_grain_orientation(path)
        linestyle = '-' if grain_orientation == 'Parallel' else (0, (1, 2))

        institution_handles[label] = plt.Line2D([0], [0],
                                                color=color,
                                                linestyle='-')

        ax1.plot(df['Time (s)'],
                 savgol_filter((-1)*np.gradient(df['Mass (g)'],
                 df['Time (s)']), 53, 3),
                 linestyle=linestyle,
                 color=color)

        if path.stem.split('_')[0] == 'UMET':
            zorder = 1
        else:
            zorder = 5

        ax2.plot(df['Time (s)'],
                 df['HRR (kW/m2)'],
                 linestyle=linestyle,
                 color=color,
                 zorder=zorder)

    ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Mass loss rate [g/s]')
    fig1.tight_layout()

    legend1 = ax1.legend(orientation_handles.values(),
                         orientation_handles.keys(),
                         loc='upper right')

    ax1.add_artist(legend1)

    ax1.legend(institution_handles.values(),
               institution_handles.keys(),
               loc='center right')

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('HRR [kW/m$^2$]')
    fig2.tight_layout()

    legend2 = ax2.legend(orientation_handles.values(),
                         orientation_handles.keys(),
                         loc='upper right')

    ax2.add_artist(legend2)

    ax2.legend(institution_handles.values(),
               institution_handles.keys(),
               loc='center right')

    fig1.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_Mass.{}'.format(material, flux, orient, ex))

    fig2.savefig(str(base_dir) + '/Cone/Cone_{}_{}_{}_HRR.{}'.format(material, flux, orient, ex))

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
        if path.stem.split('_')[0] in ['Aalto', 'FSRI', 'UDRI', 'UQ']:
            A_surf = 0.01
        else: #FPL, IMT, TUBS, UMET
            A_surf = 0.00884
        HOC = A_surf*(df['Int HRR'][index_end]-df['Int HRR'][index_start])/(df['Mass (g)'][index_start]-df['Mass (g)'][index_end])

        ignition_time_list.append(ignition_time)
        HOC_list.append(HOC)

        ax_HRR.plot(df['Time (s)'], df['HRR (kW/m2)'], '-', color='black', linewidth=0.2)

    Average_values.at[idx, 'ignition time'] = np.mean(ignition_time_list)
    Average_values.at[idx, 'std ignition time'] = np.std(ignition_time_list, ddof=1)
    Average_values.at[idx, 'HOC'] = np.mean(HOC_list)
    Average_values.at[idx, 'std HOC'] = np.std(HOC_list, ddof=1)

    # Set lower limits of both y-axes to 0
    ax_HRR.set_ylim(bottom=0)
    

    # Axes labels
    ax_HRR.set_xlabel('Time [s]')
    ax_HRR.set_ylabel('HRR [kW/m2]')

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
color = cone_color
fig1, ax1 = plt.subplots(figsize=(6, 4))
average_data = {}

for series in [f'Cone_{flux}_hor' for flux in cone_flux]:
#for series in ['Cone_30kW_hor','Cone_50kW_hor','Cone_60kW_hor']:
    parts = series.split('_')
    flux, orient  = parts[1:]
    for subset in [item for item in Cone_sets if series in item]:
        paths = list(DATA_DIR.glob(f"*/{subset}_[rR]*.csv"))
        for i, path in enumerate(paths):
            df = pd.read_csv(path)
            df = calculate_int_HRR(df)
            # ax1.plot(df['Time (s)'], df['HRR (kW/m2)'], '-', color = color[flux], alpha=0.2, linewidth = 0.1, zorder=5)
    df_average = average_cone_series(series, ['UMET'], ['IMT_Wood_Cone_25kW_hor_R2', 'IMT_Wood_Cone_25kW_hor_R5'],
                                 include_grain_variants=True)
    average_data[series] = df_average[['Time (s)', 'HRR (kW/m2)']].copy()
    ax1.plot(df_average['Time (s)'], df_average['HRR (kW/m2)'], label = flux + '/m$^2$', color = color[flux], zorder = 2)
    ax1.fill_between(df_average['Time (s)'], 
                    df_average['HRR (kW/m2)']-2*df_average['unc HRR (kW/m2)'],
                    df_average['HRR (kW/m2)']+2*df_average['unc HRR (kW/m2)'],
                    color=color[flux], alpha = 0.3, zorder=3)

ax1.set_ylim(bottom=0,top=250)
ax1.set_xlim(right=2500)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('HRR [kW/m$^2$]')
fig1.tight_layout()
ax1.legend()

fig1.savefig(str(base_dir) + '/Cone/Cone_Average_HRR.{}'.format(ex))


for series, df_data in average_data.items():
    df_data.to_csv(str(base_dir) + '/Cone/Cone_Average_{}.csv'.format(series), index=False)


plt.close(fig1)

# Initial density versus heat of combustion for individual Cone measurements

volume = 10 * 10 * 2.54
marker_map = {'Parallel': 'o', 'Perpendicular': '^'}

for flux in cone_flux:

    fig_hoc, ax_hoc = plt.subplots(figsize=(6, 4))
    institution_handles = {}

    orientation_handles = [
        plt.Line2D([0], [0], color='black', marker='o', linestyle='None', label='Parallel'),
        plt.Line2D([0], [0], color='black', marker='^', linestyle='None', label='Perpendicular')
    ]

    series = f'Cone_{flux}_hor'
    paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]
    paths = [p for p in paths if 'UMET' not in str(p)]
    # paths = [p for p in paths if 'UQ' not in str(p)]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    for path in paths:
        df_raw = pd.read_csv(path)

        if not (df_raw['HRR (kW/m2)'] >= 24).any():
            continue

        df = calculate_int_HRR(df_raw)

        index_start = df[df['HRR (kW/m2)'] >= 24].index[0]
        index_end = df[df['HRR (kW/m2)'] >= 24].index[-1]

        if path.stem.split('_')[0] in ['Aalto', 'FSRI', 'UDRI', 'UQ']:
            A_surf = 0.01
        else:
            A_surf = 0.00884

        HOC = A_surf * (df['Int HRR'][index_end] - df['Int HRR'][index_start]) / (df['Mass (g)'][index_start] - df['Mass (g)'][index_end])

        m0 = np.mean(df["Mass (g)"][1:5])
        density = m0 / volume

        label, color_inst = label_def(path.stem.split('_')[0])
        orientation = get_grain_orientation(path)

        ax_hoc.scatter(density, HOC, color=color_inst, marker=marker_map[orientation], s=45)

        institution_handles[label] = plt.Line2D([0], [0], color=color_inst, marker='o', linestyle='None', label=label)

    ax_hoc.set_xlabel('Initial density [g/cm$^3$]')
    ax_hoc.set_ylabel('Heat of combustion [kJ/g]')
    ax_hoc.set_title(f'{flux}/m$^2$')
    ax_hoc.set_ylim(10, 20)
    if flux != '25kW':
        ax_hoc.set_xlim(0.3, 0.5)
        ax_hoc.set_xticks(np.arange(0.3, 0.51, 0.05))

    legend1 = ax_hoc.legend(institution_handles.values(), institution_handles.keys(), loc='upper right', framealpha=0.25)
    ax_hoc.add_artist(legend1)
    ax_hoc.legend(orientation_handles, ['Parallel', 'Perpendicular'], loc='upper center', framealpha=0.25)

    fig_hoc.tight_layout()
    fig_hoc.savefig(str(base_dir) + f'/Cone/Cone_Density_vs_HOC_{flux}.{ex}')
    plt.close(fig_hoc)



# Average HRR plot separated by grain orientation

color = cone_color
linestyle_map = {'Parallel': '-', 'Perpendicular': (0, (1.5, 2))}

fig_grain, ax_grain = plt.subplots(figsize=(6, 4))

for series in [f'Cone_{flux}_hor' for flux in cone_flux]:
    flux = series.split('_')[1]
    for orientation in ['Parallel', 'Perpendicular']:

        paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
        paths = [p for p in paths if "TEMPLATE" not in str(p)]
        paths = [p for p in paths if p in Cone_Data]

        paths = [p for p in paths if get_grain_orientation(p) == orientation]
        # print(series, orientation, len(paths))

        paths = [p for p in paths if 'UMET' not in str(p)]
        # paths = [p for p in paths if 'UQ' not in str(p)]
        paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
        paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

        if len(paths) == 0:
            continue

        Dataframes = []
        for path in paths:

            df_raw = pd.read_csv(path)
            t_floor = np.ceil(df_raw["Time (s)"].iloc[0])
            t_ceil = np.floor(df_raw["Time (s)"].iloc[-1])

            if pd.isna(t_floor) or pd.isna(t_ceil) or t_ceil <= t_floor:
                continue

            InterpT = np.arange(t_floor, t_ceil + 1, 1)
            df_interp = pd.DataFrame(index=range(len(InterpT)))

            for column in df_raw.columns:
                df_interp[column] = np.interp(InterpT, df_raw["Time (s)"], df_raw[column])

            Dataframes.append(df_interp)

        if len(Dataframes) == 0:
            continue

        merged_df = Dataframes[0]

        for df in Dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on="Time (s)", how="outer", suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"))

        merged_df.rename(columns={'HRR (kW/m2)': "HRR (kW/m2) 1"}, inplace=True)
        HRR_cols = merged_df.filter(regex=r'^HRR \(kW/m2\)').columns
        df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})

        n = 2
        sum_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)
        cnt_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).count().sum(axis=1)
        df_average['HRR (kW/m2)'] = sum_hrr / cnt_hrr

        diff = merged_df[HRR_cols].sub(df_average['HRR (kW/m2)'], axis=0)**2

        sum_diff = diff.rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)

        df_average['unc HRR (kW/m2)'] = np.sqrt(sum_diff / (cnt_hrr * (cnt_hrr - 1)))

        ax_grain.plot(df_average['Time (s)'], df_average['HRR (kW/m2)'], color=color[flux], linestyle=linestyle_map[orientation], label=f'{flux}/m$^2$ {orientation}')

        ax_grain.fill_between(df_average['Time (s)'],
                              df_average['HRR (kW/m2)'] - 2*df_average['unc HRR (kW/m2)'],
                              df_average['HRR (kW/m2)'] + 2*df_average['unc HRR (kW/m2)'],
                              color=color[flux],
                              alpha=0.2)

ax_grain.set_ylim(bottom=0, top=250)
ax_grain.set_xlim(right=2500)

ax_grain.set_xlabel('Time [s]')
ax_grain.set_ylabel('HRR [kW/m$^2$]')

orientation_handles = [
    plt.Line2D([0], [0], color='black', linestyle='-'),
    plt.Line2D([0], [0], color='black', linestyle=(0, (1.5, 2)))
]

orientation_labels = ['Parallel', 'Perpendicular']

flux_handles = [plt.Line2D([0], [0], color=color[flux], lw=2) for flux in cone_flux]

flux_labels = [flux.replace('kW', ' kW/m$^2$') for flux in cone_flux]

legend1 = ax_grain.legend(orientation_handles, orientation_labels, loc='upper center')
ax_grain.add_artist(legend1)
ax_grain.legend(flux_handles, flux_labels, loc='upper right')

fig_grain.tight_layout()

fig_grain.savefig(str(base_dir) + '/Cone/Cone_Average_HRR_grain.{}'.format(ex))

plt.close(fig_grain)


# Average HRR plot separated by grain orientation, only fluxes with both orientations

fig_grain_both, ax_grain_both = plt.subplots(figsize=(6, 4))

cone_flux_both = []

for flux in cone_flux:
    series = f'Cone_{flux}_hor'

    paths_parallel = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths_parallel = [p for p in paths_parallel if "TEMPLATE" not in str(p)]
    paths_parallel = [p for p in paths_parallel if p in Cone_Data]
    paths_parallel = [p for p in paths_parallel if get_grain_orientation(p) == 'Parallel']
    paths_parallel = [p for p in paths_parallel if 'UMET' not in str(p)]
    # paths_parallel = [p for p in paths_parallel if 'UQ' not in str(p)]
    paths_parallel = [p for p in paths_parallel if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths_parallel = [p for p in paths_parallel if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    paths_perpendicular = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths_perpendicular = [p for p in paths_perpendicular if "TEMPLATE" not in str(p)]
    paths_perpendicular = [p for p in paths_perpendicular if p in Cone_Data]
    paths_perpendicular = [p for p in paths_perpendicular if get_grain_orientation(p) == 'Perpendicular']
    paths_perpendicular = [p for p in paths_perpendicular if 'UMET' not in str(p)]
    # paths_perpendicular = [p for p in paths_perpendicular if 'UQ' not in str(p)]
    paths_perpendicular = [p for p in paths_perpendicular if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths_perpendicular = [p for p in paths_perpendicular if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    if len(paths_parallel) > 0 and len(paths_perpendicular) > 0:
        cone_flux_both.append(flux)

for flux in cone_flux_both:
    series = f'Cone_{flux}_hor'

    for orientation in ['Parallel', 'Perpendicular']:

        paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
        paths = [p for p in paths if "TEMPLATE" not in str(p)]
        paths = [p for p in paths if p in Cone_Data]
        paths = [p for p in paths if get_grain_orientation(p) == orientation]
        paths = [p for p in paths if 'UMET' not in str(p)]
        # paths = [p for p in paths if 'UQ' not in str(p)]
        paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
        paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

        if len(paths) == 0:
            continue

        Dataframes = []

        for path in paths:
            df_raw = pd.read_csv(path)
            t_floor = np.ceil(df_raw["Time (s)"].iloc[0])
            t_ceil = np.floor(df_raw["Time (s)"].iloc[-1])

            if pd.isna(t_floor) or pd.isna(t_ceil) or t_ceil <= t_floor:
                continue

            InterpT = np.arange(t_floor, t_ceil + 1, 1)
            df_interp = pd.DataFrame(index=range(len(InterpT)))

            for column in df_raw.columns:
                df_interp[column] = np.interp(InterpT, df_raw["Time (s)"], df_raw[column])

            Dataframes.append(df_interp)

        if len(Dataframes) == 0:
            continue

        merged_df = Dataframes[0]

        for df in Dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on="Time (s)", how="outer", suffixes=("", f" {int(len(merged_df.columns)/2+0.5)}"))

        merged_df.rename(columns={'HRR (kW/m2)': "HRR (kW/m2) 1"}, inplace=True)
        HRR_cols = merged_df.filter(regex=r'^HRR \(kW/m2\)').columns
        df_average = pd.DataFrame({'Time (s)': merged_df['Time (s)']})

        n = 2
        sum_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)
        cnt_hrr = merged_df[HRR_cols].rolling(2*n+1, min_periods=1, center=True).count().sum(axis=1)
        df_average['HRR (kW/m2)'] = sum_hrr / cnt_hrr

        diff = merged_df[HRR_cols].sub(df_average['HRR (kW/m2)'], axis=0)**2
        sum_diff = diff.rolling(2*n+1, min_periods=1, center=True).sum().sum(axis=1)
        df_average['unc HRR (kW/m2)'] = np.sqrt(sum_diff / (cnt_hrr * (cnt_hrr - 1)))

        ax_grain_both.plot(df_average['Time (s)'], df_average['HRR (kW/m2)'], color=cone_color[flux], linestyle=linestyle_map[orientation], label=f'{flux}/m$^2$ {orientation}')

        ax_grain_both.fill_between(df_average['Time (s)'], df_average['HRR (kW/m2)'] - 2*df_average['unc HRR (kW/m2)'], df_average['HRR (kW/m2)'] + 2*df_average['unc HRR (kW/m2)'], color=cone_color[flux], alpha=0.2)

ax_grain_both.set_ylim(bottom=0, top=250)
ax_grain_both.set_xlim(right=2500)
ax_grain_both.set_xlabel('Time [s]')
ax_grain_both.set_ylabel('HRR [kW/m$^2$]')

orientation_handles = [
    plt.Line2D([0], [0], color='black', linestyle='-'),
    plt.Line2D([0], [0], color='black', linestyle=(0, (1.5, 2)))
]

orientation_labels = ['Parallel', 'Perpendicular']

flux_handles = [plt.Line2D([0], [0], color=cone_color[flux], lw=2) for flux in cone_flux_both]
flux_labels = [flux.replace('kW', ' kW/m$^2$') for flux in cone_flux_both]

legend1 = ax_grain_both.legend(orientation_handles, orientation_labels, loc='upper center')
ax_grain_both.add_artist(legend1)
ax_grain_both.legend(flux_handles, flux_labels, loc='upper right')

fig_grain_both.tight_layout()
fig_grain_both.savefig(str(base_dir) + '/Cone/Cone_Average_HRR_grain_both_orientations.{}'.format(ex))
plt.close(fig_grain_both)



# Average gasification MLR plots

color = {'20kW': 'green', '30kW': 'blue', '40kW': 'orange', '45kW': 'cyan', '50kW': 'black', '60kW': 'red', '70kW': 'purple'}

gas_average_sets = {
    'All': None,
    'CAPA': '_CAPA_',
    'Gasification': '_Gasification_'
}

for dataset_name, dataset_filter in gas_average_sets.items():

    fig_gas_avg, ax_gas_avg = plt.subplots(figsize=(6, 4))

    for flux in sorted(gas_flux):

        paths = [p for p in Gasification_Data if f'_{flux}_' in p.name]
        # print(f'\nGasification MLR {flux}')
        #
        # for p in paths:
        #     print(p.stem)
        paths = [p for p in paths if 'Wood' in p.name]
        paths = [p for p in paths if 'TEMPLATE' not in p.name]

        if dataset_filter is not None:
            paths = [p for p in paths if dataset_filter in p.name]

        # print(f'\nAverage gasification MLR {dataset_name} {flux}')
        # for p in paths:
        #     print(p.stem)

        df_average = average_gasification_paths(paths)

        if df_average is None:
            continue

        ax_gas_avg.plot(df_average['Time (s)'], df_average['MLR'], color=color[flux], label=flux)

        ax_gas_avg.fill_between(df_average['Time (s)'], df_average['MLR'] - 2*df_average['unc MLR'], df_average['MLR'] + 2*df_average['unc MLR'], color=color[flux], alpha=0.2)

    ax_gas_avg.set_ylim(bottom=0)
    ax_gas_avg.set_ylim(top=15)
    ax_gas_avg.set_xlabel('Time [s]')
    ax_gas_avg.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')

    ax_gas_avg.legend()

    fig_gas_avg.tight_layout()

    if dataset_name == 'All':
        fig_gas_avg.savefig(str(base_dir) + '/Cone/Gasification_Average_MLR.{}'.format(ex))
    else:
        fig_gas_avg.savefig(str(base_dir) + f'/Cone/Gasification_Average_MLR_{dataset_name}.{ex}')

    plt.close(fig_gas_avg)



# Average gasification MLR plot separated by grain orientation

color = {'20kW': 'green', '30kW': 'blue', '40kW': 'orange', '45kW': 'cyan', '50kW': 'black', '60kW': 'red', '70kW': 'purple'}
linestyle_map = {'Parallel': '-', 'Perpendicular': (0, (1.5, 2))}

fig_gas_grain, ax_gas_grain = plt.subplots(figsize=(6, 4))

for flux in sorted(gas_flux):

    for orientation in ['Parallel', 'Perpendicular']:

        paths = [p for p in Gasification_Data if f'_{flux}_' in p.name]
        paths = [p for p in paths if 'Wood' in p.name]
        paths = [p for p in paths if 'TEMPLATE' not in p.name]
        paths = [p for p in paths if '_Wood_Gasification_' in p.name]
        paths = [p for p in paths if get_grain_orientation(p) == orientation]

        df_average = average_gasification_paths(paths)

        if df_average is None:
            continue

        ax_gas_grain.plot(df_average['Time (s)'], df_average['MLR'], color=color[flux], linestyle=linestyle_map[orientation], label=f'{flux} {orientation}')

        ax_gas_grain.fill_between(df_average['Time (s)'], df_average['MLR'] - 2*df_average['unc MLR'], df_average['MLR'] + 2*df_average['unc MLR'], color=color[flux], alpha=0.2)

ax_gas_grain.set_ylim(bottom=0)
ax_gas_grain.set_ylim(top=15)
ax_gas_grain.set_xlabel('Time [s]')
ax_gas_grain.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')

orientation_handles = [
    plt.Line2D([0], [0], color='black', linestyle='-'),
    plt.Line2D([0], [0], color='black', linestyle=(0, (1.5, 2)))
]

orientation_labels = ['Parallel', 'Perpendicular']

used_fluxes = []
for flux in sorted(gas_flux):

    paths = [p for p in Gasification_Data if f'_{flux}_' in p.name]
    paths = [p for p in paths if '_Wood_Gasification_' in p.name]

    if len(paths) > 0:
        used_fluxes.append(flux)

flux_handles = [plt.Line2D([0], [0], color=color[flux], lw=2) for flux in used_fluxes]
flux_labels = [flux.replace('kW', ' kW/m$^2$') for flux in used_fluxes]

legend1 = ax_gas_grain.legend(orientation_handles, orientation_labels, loc='upper center')
ax_gas_grain.add_artist(legend1)
ax_gas_grain.legend(flux_handles, flux_labels, loc='upper right')

fig_gas_grain.tight_layout()
fig_gas_grain.savefig(str(base_dir) + '/Cone/Gasification_Average_MLR_Gasification_grain.{}'.format(ex))
plt.close(fig_gas_grain)


# Average gasification MLR plots separated by grain orientation for each heat flux

for flux in used_fluxes:

    fig_gas_flux, ax_gas_flux = plt.subplots(figsize=(6, 4))

    ymax = 0

    for orientation in ['Parallel', 'Perpendicular']:

        paths = [p for p in Gasification_Data if f'_{flux}_' in p.name]
        paths = [p for p in paths if '_Wood_Gasification_' in p.name]
        paths = [p for p in paths if 'TEMPLATE' not in p.name]
        paths = [p for p in paths if get_grain_orientation(p) == orientation]

        df_average = average_gasification_paths(paths)

        if df_average is None:
            continue

        upper = df_average['MLR'] + 2*df_average['unc MLR']
        ymax = max(ymax, np.nanmax(upper))

        ax_gas_flux.plot(df_average['Time (s)'], df_average['MLR'], color=color[flux], linestyle=linestyle_map[orientation], linewidth=2, label=orientation)

        ax_gas_flux.fill_between(df_average['Time (s)'], df_average['MLR'] - 2*df_average['unc MLR'], upper, color=color[flux], alpha=0.2)

    ax_gas_flux.set_ylim(bottom=0, top=1.1*ymax)
    ax_gas_flux.set_xlabel('Time [s]')
    ax_gas_flux.set_ylabel('Mass loss rate [g s$^{-1}$ m$^{-2}$]')
    ax_gas_flux.set_title(flux.replace('kW', ' kW/m$^2$'))
    ax_gas_flux.legend(framealpha=0.25)

    fig_gas_flux.tight_layout()
    fig_gas_flux.savefig(str(base_dir) + f'/Cone/Gasification_Average_MLR_Gasification_grain_{flux}.{ex}')
    plt.close(fig_gas_flux)



# Initial density versus ignition time for individual Cone measurements

volume = 10 * 10 * 2.54
marker_map = {'Parallel': 'o', 'Perpendicular': '^'}

for flux in cone_flux:

    fig_density, ax_density = plt.subplots(figsize=(6, 4))
    institution_handles = {}

    orientation_handles = [
        plt.Line2D([0], [0], color='black', marker='o', linestyle='None', label='Parallel'),
        plt.Line2D([0], [0], color='black', marker='^', linestyle='None', label='Perpendicular')
    ]

    series = f'Cone_{flux}_hor'
    paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]
    paths = [p for p in paths if 'UMET' not in str(p)]
    # paths = [p for p in paths if 'UQ' not in str(p)]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    for path in paths:
        df = pd.read_csv(path)

        if not (df['HRR (kW/m2)'] >= 24).any():
            continue

        ignition_index = df[df['HRR (kW/m2)'] >= 24].index[0]
        ignition_time = df["Time (s)"].iloc[ignition_index]

        m0 = np.mean(df["Mass (g)"][1:5])
        density = m0 / volume

        label, color_inst = label_def(path.stem.split('_')[0])
        orientation = get_grain_orientation(path)

        ax_density.scatter(density, ignition_time, color=color_inst, marker=marker_map[orientation], s=45)

        institution_handles[label] = plt.Line2D([0], [0], color=color_inst, marker='o', linestyle='None', label=label)

    ax_density.set_xlabel('Initial density [g/cm$^3$]')
    ax_density.set_ylabel('Time to ignition [s]')
    ax_density.set_title(f'{flux}/m$^2$')
    if flux != '25kW':
        ax_density.set_xlim(0.3, 0.5)
        ax_density.set_xticks(np.arange(0.3, 0.51, 0.05))

    legend1 = ax_density.legend(institution_handles.values(),
                                institution_handles.keys(),
                                loc='upper right',
                                framealpha=0.25)

    ax_density.add_artist(legend1)

    ax_density.legend(orientation_handles,
                      ['Parallel', 'Perpendicular'],
                      loc='upper center',
                      framealpha=0.25)

    fig_density.tight_layout()
    fig_density.savefig(str(base_dir) + f'/Cone/Cone_Density_vs_Ignition_{flux}.{ex}')
    plt.close(fig_density)

# Ignition time versus heat of combustion averaged by institution and grain orientation

marker_map = {'Parallel': 'o', 'Perpendicular': '^'}

for flux in cone_flux:

    fig_ign_hoc, ax_ign_hoc = plt.subplots(figsize=(6, 4))
    results = []

    series = f'Cone_{flux}_hor'
    paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]
    paths = [p for p in paths if 'UMET' not in str(p)]
    # paths = [p for p in paths if 'UQ' not in str(p)]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    for path in paths:
        df_raw = pd.read_csv(path)

        if not (df_raw['HRR (kW/m2)'] >= 24).any():
            continue

        df = calculate_int_HRR(df_raw)

        ignition_index = df[df['HRR (kW/m2)'] >= 24].index[0]
        ignition_time = df["Time (s)"].iloc[ignition_index]

        index_start = df[df['HRR (kW/m2)'] >= 24].index[0]
        index_end = df[df['HRR (kW/m2)'] >= 24].index[-1]

        if path.stem.split('_')[0] in ['Aalto', 'FSRI', 'UDRI', 'UQ']:
            A_surf = 0.01
        else:
            A_surf = 0.00884

        HOC = A_surf * (df['Int HRR'][index_end] - df['Int HRR'][index_start]) / (df['Mass (g)'][index_start] - df['Mass (g)'][index_end])

        institution = path.stem.split('_')[0]
        label, color = label_def(institution)
        orientation = get_grain_orientation(path)

        results.append({'Institution': institution, 'Duck': label, 'color': color, 'orientation': orientation, 'ignition time': ignition_time, 'HOC': HOC})

    results_df = pd.DataFrame(results)

    if len(results_df) == 0:
        plt.close(fig_ign_hoc)
        continue

    grouped = results_df.groupby(['Institution', 'Duck', 'color', 'orientation'])

    for (institution, duck, color, orientation), group in grouped:

        ax_ign_hoc.errorbar(group['ignition time'].mean(), group['HOC'].mean(),
                            xerr=group['ignition time'].std(ddof=1),
                            yerr=group['HOC'].std(ddof=1),
                            fmt=marker_map[orientation],
                            capsize=5, capthick=2, markersize=8,
                            color=color, label=duck)

    ax_ign_hoc.set_xlabel('Ignition time [s]', fontsize=12)
    ax_ign_hoc.set_ylabel('Heat of combustion [kJ/g]', fontsize=12)
    ax_ign_hoc.set_ylim(0, 20)
    ax_ign_hoc.set_title(f'{flux}/m$^2$')

    handles, labels = ax_ign_hoc.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend1 = ax_ign_hoc.legend(by_label.values(), by_label.keys(), loc='best', framealpha=0.25)
    ax_ign_hoc.add_artist(legend1)

    orientation_handles = [
        plt.Line2D([0], [0], color='black', marker='o', linestyle='None', label='Parallel'),
        plt.Line2D([0], [0], color='black', marker='^', linestyle='None', label='Perpendicular')
    ]

    ax_ign_hoc.legend(orientation_handles, ['Parallel', 'Perpendicular'], loc='upper center', framealpha=0.25)

    fig_ign_hoc.tight_layout()
    fig_ign_hoc.savefig(str(base_dir) + f'/Cone/Cone_Ignition_vs_HOC_{flux}.{ex}')
    plt.close(fig_ign_hoc)


# Ignition time and heat of combustion versus heat flux

marker_map = {'Parallel': 'o', 'Perpendicular': '^'}
offset_map = {'Parallel': -0.8, 'Perpendicular': 0.8}

plot_configs = {'ignition time': {'ylabel': 'Ignition time [s]', 'filename': 'Cone_Ignition_time_vs_Flux'},
                'HOC': {'ylabel': 'Heat of combustion [kJ/g]', 'filename': 'Cone_HOC_vs_Flux'},
                'ignition time inv sqrt': {'ylabel': r'Ignition time$^{-1/2}$ [s$^{-1/2}$]',
                                           'filename': 'Cone_Ignition_time_inv_sqrt_vs_Flux'}}

results = []

for flux in cone_flux:
    series = f'Cone_{flux}_hor'
    paths = list(DATA_DIR.glob(f"*/*{series}*_[rR]*.csv"))
    paths = [p for p in paths if "TEMPLATE" not in str(p)]
    paths = [p for p in paths if p in Cone_Data]
    paths = [p for p in paths if 'UMET' not in str(p)]
    # paths = [p for p in paths if 'UQ' not in str(p)]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R2' not in p.stem]
    paths = [p for p in paths if 'IMT_Wood_Cone_25kW_hor_R5' not in p.stem]

    for path in paths:
        df_raw = pd.read_csv(path)

        if not (df_raw['HRR (kW/m2)'] >= 24).any():
            continue

        df = calculate_int_HRR(df_raw)

        ignition_index = df[df['HRR (kW/m2)'] >= 24].index[0]
        ignition_time = df["Time (s)"].iloc[ignition_index]

        index_start = df[df['HRR (kW/m2)'] >= 24].index[0]
        index_end = df[df['HRR (kW/m2)'] >= 24].index[-1]

        if path.stem.split('_')[0] in ['Aalto', 'FSRI', 'UDRI', 'UQ']:
            A_surf = 0.01
        else:
            A_surf = 0.00884

        HOC = A_surf * (df['Int HRR'][index_end] - df['Int HRR'][index_start]) / (df['Mass (g)'][index_start] - df['Mass (g)'][index_end])

        institution = path.stem.split('_')[0]
        label, color = label_def(institution)
        orientation = get_grain_orientation(path)

        results.append({'flux': flux, 'flux_value': int(flux.replace('kW', '')), 'Institution': institution, 'Duck': label, 'color': color, 'orientation': orientation, 'ignition time': ignition_time, 'HOC': HOC})

results_df = pd.DataFrame(results)

if len(results_df) > 0:
    results_df['ignition time inv sqrt'] = results_df['ignition time'] ** (-0.5)
    grouped = results_df.groupby(['flux', 'flux_value', 'Institution', 'Duck', 'color', 'orientation'])

    for quantity, config in plot_configs.items():

        fig_flux, ax_flux = plt.subplots(figsize=(6, 4))

        institution_handles = {}
        orientation_handles = [
            plt.Line2D([0], [0], color='black', marker='o', linestyle='None', label='Parallel'),
            plt.Line2D([0], [0], color='black', marker='^', linestyle='None', label='Perpendicular')
        ]

        for (flux, flux_value, institution, duck, color, orientation), group in grouped:
            x = flux_value + offset_map[orientation]
            y_mean = group[quantity].mean()
            y_min = group[quantity].min()
            y_max = group[quantity].max()

            ax_flux.errorbar(x, y_mean, yerr=[[y_mean - y_min], [y_max - y_mean]], fmt=marker_map[orientation], capsize=5, capthick=2, markersize=8, color=color)

            institution_handles[duck] = plt.Line2D([0], [0], color=color, marker='o', linestyle='None', label=duck)

        ax_flux.set_xlabel('Incident heat flux [kW/m$^2$]')
        ax_flux.set_ylabel(config['ylabel'])
        ax_flux.set_xticks([int(flux.replace('kW', '')) for flux in cone_flux])
        ax_flux.set_xticklabels([flux.replace('kW', '') for flux in cone_flux])

        if quantity == 'HOC':
            ax_flux.set_ylim(0, 20)

        legend1 = ax_flux.legend(institution_handles.values(), institution_handles.keys(), loc='best', framealpha=0.25)
        ax_flux.add_artist(legend1)
        ax_flux.legend(orientation_handles, ['Parallel', 'Perpendicular'], loc='upper center', framealpha=0.25)

        fig_flux.tight_layout()
        fig_flux.savefig(str(base_dir) + f"/Cone/{config['filename']}.{ex}")
        plt.close(fig_flux)


#  Back side temperature plots for all unique atmospheres and heating rates (when available)
linestyle = ['--',':','-']
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
            if 'TC Top (K)' in df.columns:
                ax1.plot(df['Time (s)'], df['TC Top (K)'], label=label, color=color, linestyle = '-')


    ax1.set_ylim(bottom=250)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    fig1.tight_layout()
    
    # Get unique (label, style) combinations
    handles, labels = ax1.get_legend_handles_labels()
    unique = {}
    for handle, label in zip(handles, labels):
        # Create a key based on label and visual properties
        key = (label, handle.get_linestyle(), handle.get_color())
        if key not in unique:
            unique[key] = (handle, label)

    unique_handles = [v[0] for v in unique.values()]
    unique_labels = [v[1] for v in unique.values()]
    ax1.legend(unique_handles, unique_labels)

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
for flux in gas_flux: 
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    Gas_subset_paths = [p for p in Gasification_Data if f"Wood" in p.name and f"_{flux}_" in p.name]
    for path in Gas_subset_paths:
        institute = path.stem.split('_')[0]
        df_raw = pd.read_csv(path)
        df=Calculate_dm_dt(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        if institute in ['TIFP+UCT', 'UQ', 'Aalto']:
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.01,41,3),'-', label = label, color=color)
        elif institute in ['TUBS']:
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.00884,41,3),'-', label = label, color=color)
        elif institute in ['FSRI', 'UMD']:
            ax1.plot(df['Time (s)'],savgol_filter(df['dm/dt']/0.00385,41,3),'-', label = label, color=color)
        ax2.plot(df['Time (s)'], df['Mass (g)'], '-', label = label, color=color)

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

    fig1.savefig(str(base_dir) + '/Cone/Gasification_Wood_{}_MLR.{}'.format(flux,ex))
    fig2.savefig(str(base_dir) + '/Cone/Gasification_Wood_{}_Mass.{}'.format(flux,ex))


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
        ax2.plot(df['Time (s)'], df['Mass (g)'],'-', label = label, color=color[label])

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
        ax1.plot(df['Time (s)'],df['TC Top (K)'],':', label = label + 'Top', color="#bcbd22")


    ax1.set_ylim(bottom=280)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Surface Temperature [K]')
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
    institute = set.split('_')[0]
    # plot average
    # Plot mass (left y-axis)
    if institute in ['TIFP+UCT', 'Aalto', 'UQ']:
        area = 0.01
    elif institute in ['TUBS']:
        area = 0.00884
    elif institute in ['UMD','FSRI']:
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
        ax.plot(df['Time (s)'],savgol_filter(df['dm/dt']/area,41,3), '-',color ='black',linewidth=0.2)

    # Set lower limits of both y-axes to 0
    ax.set_ylim(bottom=0)

    # Axes labels
    ax.set_xlabel('Time [s]')
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
    lambda row: format_ignition(row['ignition time'], row['std ignition time']),
    axis=1
)

# Format HOC total
final_table_sorted['HOC_formatted'] = final_table_sorted.apply(
    lambda row: format_regular(row['HOC'], row['std HOC']),
    axis=1
)


def format_cone_conditions_without_grain(conditions):
    if isinstance(conditions, list):
        parts = conditions.copy()
    else:
        parts = str(conditions).replace('_', ' ').split(', ')

    parts = [p for p in parts if p.lower() not in ['parallel', 'perpendicular']]
    return ', '.join(parts)


def format_cone_grain_orientation(conditions):
    text = ', '.join(conditions) if isinstance(conditions, list) else str(conditions)

    if 'perpendicular' in text.lower():
        return 'Perpendicular'

    if 'parallel' in text.lower():
        return 'Parallel'

    return 'Parallel$^*$'


final_table_sorted['conditions_formatted'] = final_table_sorted['conditions'].apply(format_cone_conditions_without_grain)
final_table_sorted['grain_orientation_formatted'] = final_table_sorted['conditions'].apply(format_cone_grain_orientation)

# Select and rename columns for the table
columns_to_keep = ['Duck', 'conditions_formatted', 'grain_orientation_formatted',
                   'ignitiont_formatted', 'HOC_formatted', 'condition_key']

final_latex_table = final_table_sorted[columns_to_keep].copy()
final_latex_table.columns = ['Institution', 'Conditions', 'Grain orientation',
                             'Ignition time (s)', 'HOC (kJ/g)', 'condition_key']

# Generate LaTeX
latex_string = final_latex_table.to_latex(
    index=False,
    escape=False,
    column_format='llcccccc',
    columns=['Institution', 'Conditions', 'Grain orientation', 'Ignition time (s)', 'HOC (kJ/g)']
)

# Modify the string
latex_string = latex_string.replace('\\toprule', '\\hline')
latex_string = latex_string.replace('\\midrule', '\\hline')
latex_string = latex_string.replace('\\bottomrule', '\\hline')
latex_string = latex_string.replace(
    '\\end{tabular}',
    '\\end{tabular}\n\\\\\n$^*$ Parallel grain orientation assumed when not explicitly specified in the original dataset filenames.'
)

# Make column headers bold
for col in ['Institution', 'Conditions', 'Grain orientation', 'Ignition time (s)', 'HOC (kJ/g)']:
    latex_string = latex_string.replace(col, '\\textbf{'+col+'}')


# Add blank lines between different condition groups
lines = latex_string.split('\n')
new_lines = []
prev_flux = None

# Track condition keys as we iterate through table rows
condition_keys = final_latex_table['condition_key'].tolist()
data_row_index = 0

for i, line in enumerate(lines):

    # Check if this is a data row
    if '&' in line and '\\textbf' not in line and '\\hline' not in line:

        current_condition_key = condition_keys[data_row_index]

        # Extract only heat flux (e.g. 25kW, 50kW)
        if isinstance(current_condition_key, list):
            current_flux = current_condition_key[0]
        else:
            current_flux = current_condition_key.split('_')[0]

        # Add small vertical spacing only when flux changes
        if prev_flux is not None and current_flux != prev_flux:
            new_lines.append('\\noalign{\\vskip 6pt}')

        prev_flux = current_flux
        data_row_index += 1

    new_lines.append(line)

latex_string = '\n'.join(new_lines)

# print('\nInstitution label mapping:')
#
# institutions = sorted([
#     p.name for p in DATA_DIR.iterdir()
#     if p.is_dir() and 'TEMPLATE' not in p.name
# ])
#
# for lab in institutions:
#     label, color = label_def(lab)
#     print(f'{lab} -> {label}')

# Save to file
with open(str(base_dir) + f'/Cone/Cone_Values.tex', 'w') as f:
    f.write(latex_string)

