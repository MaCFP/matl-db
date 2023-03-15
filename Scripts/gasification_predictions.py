# script to analyze and plot gasification simulations

import numpy as np
from matplotlib import pyplot as plt

plt.ion()

# list of cases
cases = [ "10kW_6mm", "10kW_12mm",
          "25kW_6mm", "25kW_12mm",
          "65kW_6mm", "65kW_12mm" ]

# list of parameter sets
preds = [ "Aalto",
          "BUW-FZJ_A",
          "BUW-FZJ_B",
          "DBI",
          "GIDAZE+",
          "NIST",
          "UMD",
          "UMET_GP",
          "UMET_TK" ]

# loop through cases
for case in cases:

    # loop through parameter sets
    for pred in preds:

        # read data from files
        print("Getting gasification predictions from " + pred +
                " for case: " + case)

        dat = np.loadtxt('../PMMA/Computational_Results/Gasification_Predictions/' + 
                            pred + '_Gasification_' + case + '.csv',
                         skiprows=2, delimiter=',')

        # parse data
        t       = dat[:,0]          # times (s)
        m       = dat[:,1]          # mass (g)
        T_back  = dat[:,2]          # bottom surface temperature (K)
        T_top   = dat[:,3]          # top surface temperature (K)
