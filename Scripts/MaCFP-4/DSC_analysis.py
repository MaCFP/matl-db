import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
from scipy.signal import savgol_filter

from Utils import device_data, get_series_names, make_institution_table, device_subset, label_def, interpolation
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR


#define whether to save files in pdf or png
ex = 'pdf' #options 'pdf' or 'png

#when pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

# check all subdirectories to save plots exist. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Individual_dir = base_dir / 'DSC' / 'Individual'
Average_dir = base_dir / 'DSC' / 'Average'
Individual_dir.mkdir(parents=True, exist_ok=True)
Average_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------
#region data
# ------------------------------------
#This section is used to determine what DSC data is available. 

# All DSC data (including STA)
DSC_Data = device_data(DATA_DIR, 'DSC') + device_data(DATA_DIR, 'STA')
# All unique sets (name without repetition number, e.g.TUT_DSC_N2_10K_40Pa )
DSC_sets = get_series_names(DSC_Data)
# All unique conditions over all institutes
unique_conditions = { '_'.join(s.split('_')[3:]) for s in DSC_sets}
unique_conditions_material = sorted(set(name.split('_', 1)[1] for name in DSC_sets if '_' in name))

#Print tables with Institute name (Duck version) and amount of repetition experiments
print('Nitrogen table')
print(make_institution_table(DSC_Data,['Wood'],['N2'],['5K','10K','20K','30K','40K','50K','60K']))

print('Oxygen table')
print(make_institution_table(DSC_Data,['Wood'],['O2-21'],['5K','10K','20K','30K','40K','50K','60K']))



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

def Integral_DSC(df:pd.DataFrame):
    
    df = interpolation(df)

    int_heatflow = np.zeros(len(df))
    for i in range(1, len(df)):
        int_heatflow[i] = int_heatflow[i-1] + 0.5 * (df['Heat Flow Rate (W/g)'].iloc[i-1] + df['Heat Flow Rate (W/g)'].iloc[i]) * (df['Time (s)'].iloc[i] - df['Time (s)'].iloc[i-1])
    df['Int Heat Flow (J/g)'] = int_heatflow

    return df




#--------------------------------------------------------
#region plots
#--------------------------------------------------------
# Heat flow and integral heat flow plots for all unique atmospheres and heating rates 
for series in unique_conditions_material:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    parts = series.split('_')
    material, dev, atm, hr  = parts[:4]
    DSC_subset_paths = [p for p in DSC_Data if f"{material}_" in p.name and f"_{atm}_{hr}_" in p.name]
    for path in DSC_subset_paths:
        df_raw = pd.read_csv(path)
        df = Integral_DSC(df_raw)
        label, color = label_def(path.stem.split('_')[0])
        ax1.plot(df['Temperature (K)'], df['Heat Flow Rate (W/g)'], label = label, color=color)
        ax2.plot(df['Temperature (K)'], df['Int Heat Flow (J/g)'], label = label, color=color)

    #ax1.set_ylim(bottom=0)
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Heat flow [W g$^{-1}$]')
    fig1.tight_layout()
    ax1.legend()

    #ax2.set_ylim(bottom=0)
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('Integral Heat Flow [J g$^{-1}$]')
    fig2.tight_layout()
    ax2.legend()

    fig1.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_HF.{}'.format(material, atm,hr,ex))
    fig2.savefig(str(base_dir) + '/DSC/DSC_{}_{}_{}_iHF.{}'.format(material, atm,hr,ex))
    plt.close(fig1)
    plt.close(fig2)


