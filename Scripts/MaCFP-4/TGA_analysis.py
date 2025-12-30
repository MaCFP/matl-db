import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from pathlib import Path

from Utils import device_data, get_series_names, make_institution_table
from Utils import SCRIPT_DIR, PROJECT_ROOT, DATA_DIR, FIGURES_DIR
from Secret import Names

TGA_Data = device_data(DATA_DIR, 'TGA')
TGA_sets = get_series_names(TGA_Data)
unique_conditions = { '_'.join(s.split('_')[2:]) for s in TGA_sets}


# Print tables
print(make_institution_table(TGA_Data,['N2'],['10K','60K']))


#region functions
def average_HR_tga_series(series_name: str):
    
    paths = list(DATA_DIR.glob(f"*/{series_name}_[rR]*.csv"))
    Dataframes_HR = []
    rep = []

    # for path in paths:
    #     filename = path.name
    #     match = re.search(r"_[rR](\d+)\.csv$", filename)
    #     if match is None:
    #         raise ValueError(f"Invalid filename format: {filename}")
    #     replicate_number = match.group(1)  # Get the matched number of replicate
    #     rep.append(replicate_number)  # Append to the list

    if len(paths) == 0:
        raise Exception((f"No files found for series {series_name}", "red"))

    # Read data

    for i, path in enumerate(paths):
        df = pd.read_csv(path)
        df = df.drop(columns=["Mass (mg)"])

        # for now do not interpolate. 
        # T_floor = df["Temperature (K)"].iloc[0]
        # T_floor = np.floor(T_floor * 2) / 2
        # T_ceil = df["Temperature (K)"].iloc[-1]
        # T_ceil = np.ceil(T_ceil * 2) / 2

        # InterpT = np.arange(T_floor, T_ceil, 0.5)
        # length = len(InterpT)
        # df_interp = pd.DataFrame(index=range(length))
        # for columns in df_full.columns[1:]:
        #     df_interp[columns] = np.interp(
        #         InterpT, df["Temperature"], df[columns]
        #     )

        Dataframes_HR.append(df)
    print(Dataframes_HR)

        
average_HR_tga_series('UMD_TGA_N2_10K')



for t in TGA_Data:
    data = pd.read_csv(t)
    plt.plot(data['Temperature (K)'], data['Mass (mg)'])
    plt.grid()
    plt.xlabel('Temperature (K)')
    plt.ylabel('Mass (mg)')
plt.show()