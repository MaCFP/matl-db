# script to analyze and plot gasification simulations

import math
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

plt.ion()

# constants
A_s = 0.10**2       # surface area of gasification samples (m^2)
N   = 100           # number of data points for common comparisons

# plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

results = []

# list of cases
cases = [ "q10_6mm", "q10_18mm",
          "q30_6mm", "q30_18mm",
          "q60_6mm", "q60_18mm" ]

# list of prediction set names
names = [ "CORIA",
          "UMD_FSRI_DM",
          "UMD_FSRI_OPT",
          "UCB-CONST-PARALLEL-1",
          "UCB-CONST-PARALLEL-2",
          "UCB-CONST-PARALLEL-3",
          "UCB-TDEP-PARALLEL-1",
          "UCB-TDEP-PARALLEL-2",
          "UCB-TDEP-PARALLEL-3",
          "UCB-CONST-PERPENDICULAR-1",
          "UCB-CONST-PERPENDICULAR-2",
          "UCB-CONST-PERPENDICULAR-3", 
          "UCB-TDEP-PERPENDICULAR-1",
          "UCB-TDEP-PERPENDICULAR-2",
          "UCB-TDEP-PERPENDICULAR-3" ]

N_names = len(names) 

name_plt_lines = {
    "CORIA": ['b','-', 'o'],
    "UMD_FSRI_DM": ['lawngreen','-', 'o'],
    "UMD_FSRI_OPT": ['lawngreen','--','o'],

    # PARALLEL → red
    # CONST → line
    # TDEP → dashed line
    # kinetic schemes 1/2/3 → o, s, ^

    "UCB-CONST-PARALLEL-1": ['r','-','o'],
    "UCB-CONST-PARALLEL-2": ['r','-','s'],
    "UCB-CONST-PARALLEL-3": ['r','-','^'],

    "UCB-TDEP-PARALLEL-1": ['r','--','o'],
    "UCB-TDEP-PARALLEL-2": ['r','--','s'],
    "UCB-TDEP-PARALLEL-3": ['r','--','^'],

    # PERPENDICULAR → clear blue
    "UCB-CONST-PERPENDICULAR-1": ['c','-','o'],
    "UCB-CONST-PERPENDICULAR-2": ['c','-','s'],
    "UCB-CONST-PERPENDICULAR-3": ['c','-','^'],

    "UCB-TDEP-PERPENDICULAR-1": ['c','--','o'],
    "UCB-TDEP-PERPENDICULAR-2": ['c','--','s'],
    "UCB-TDEP-PERPENDICULAR-3": ['c','--','^'],
}

name_labels = [
    "CORIA",
    "UMD FSRI (DM)",
    "UMD FSRI (OPT)",

    "UCB PL-CONST-1",
    "UCB PL-CONST-2",
    "UCB PL-CONST-3",

    "UCB PL-TDEP-1",
    "UCB PL-TDEP-2",
    "UCB PL-TDEP-3",

    "UCB PD-CONST-1",
    "UCB PD-CONST-2",
    "UCB PD-CONST-3",

    "UCB PD-TDEP-1",
    "UCB PD-TDEP-2",
    "UCB PD-TDEP-3"
]




# loop through cases
i_case  = 0                     # case counter index
SSE     = np.zeros( N_names )   # initialize sum of squares error for each name

for case in cases:
    
    # list of data arrays 
    times           = []
    masses          = []
    temps_back      = []
    temps_top       = []
    mlrates         = []
    mlrates_peak    = []
    times_peak      = []
    times_onset     = []
    times_final     = []

    # loop through predictions for 'case' to get raw data
    for name in names:

        # read data from files
        dat = np.loadtxt(name + '_Wood_Gasification_' + case + '.csv',
                            skiprows=2, delimiter=',')

        # parse data
        t       = dat[:,0]          # times (s)
        m       = dat[:,1]          # mass (g)
        T_back  = dat[:,2]          # bottom surface temperature (K)
        T_top   = dat[:,3]          # top surface temperature (K)

        # compute mass loss rate (g/m^2-s)
        mlr     = -(1/A_s)*np.gradient( m, t )

        # find peak MLR and time to peak MLR
        mlr_p   = mlr.max()         # peak MLR (g/m^2-s)
        t_p     = t[mlr.argmax()]   # time to peak MLR (s)

        # find time to MLR = 1 g/m^2-s
        t_o     = t[np.argwhere( mlr >= 1. ).min()]

        # find maximum time for MLR >= 0.1 g/m^2-s
        t_f     = t[np.argwhere( mlr >= 0.1 ).max()]

        # save data to case lists
        times.append( t )
        masses.append( m )
        temps_back.append( T_back )
        temps_top.append( T_top )
        mlrates.append( mlr )
        mlrates_peak.append( mlr_p )
        times_peak.append( t_p )
        times_onset.append( t_o )
        times_final.append( t_f )

    # compute mean and standard deviations
    t_p_mean    = np.mean( times_peak )
    mlr_p_mean  = np.mean( mlrates_peak )
    t_o_mean    = np.mean( times_onset )
    t_f_mean    = np.mean( times_final )

    t_p_std     = np.std( times_peak )
    mlr_p_std   = np.std( mlrates_peak )
    t_o_std     = np.std( times_onset )
    t_f_std     = np.std( times_final )
    
    # ==========================================================
    # Save results to Excel
    # ==========================================================
    results.append({
        "case": case,
        "t_p_mean": t_p_mean,
        "mlr_p_mean": mlr_p_mean,
        "t_o_mean": t_o_mean,
        "t_f_mean": t_f_mean,
        "t_p_std": t_p_std,
        "mlr_p_std": mlr_p_std,
        "t_o_std": t_o_std,
        "t_f_std": t_f_std,
        "t_p_std_%": t_p_std*100/t_p_mean,
        "mlr_p_std_%": mlr_p_std*100/mlr_p_mean,
        "t_o_std_%": t_o_std*100/t_o_mean,
        "t_f_std_%": t_f_std*100/t_f_mean
    })
    # create array of common times for averaging of predictions
    t_min       = min(times_onset)    # smallest onset time (s)
    t_max       = max(times_final)    # largest final time (s)
    t_c         = np.linspace( t_min, t_max, N )

    # arrays for storing interpolated data to common times 
    T_back_c    = np.zeros( (N, N_names) ) 
    mlr_c       = np.zeros( (N, N_names) ) 

    # loop through predictions to interpolate to common times 
    for i in range(0,N_names):

        # get raw data for prediction i
        t_i         = times[i]
        T_back_i    = temps_back[i]
        mlr_i       = mlrates[i]

        # extend data if necessary
        if t_i.max() < t_max:

            # find times to be added to get up to t_max
            t_add = t_c[np.argwhere( t_c > t_i.max() )]
            
            # append additional times to raw data
            t_i = np.append( t_i, t_add )

            # append MLR = 0 and T_back = T_back_final to raw data
            T_back_i = np.append( T_back_i, T_back_i[-1]*np.ones( len(t_add) ) )
            mlr_i = np.append( mlr_i, np.zeros( len(t_add) ) )

        # interpolate MLR and T_back to common time arrays
        T_back_c[:,i]   = np.interp( t_c, t_i, T_back_i )
        mlr_c[:,i]      = np.interp( t_c, t_i, mlr_i )

    # compute mean and standard deviations at common times
    T_back_c_avg    = np.mean( T_back_c, axis=1 )
    mlr_c_avg       = np.mean( mlr_c, axis=1 )

    T_back_c_std    = np.std( T_back_c, axis=1 )
    mlr_c_std       = np.std( mlr_c, axis=1 )

    # compute total sum of squares errors of predictions from mean MLR and T_back
    dmlr    = mlr_c_avg.max() - mlr_c_avg.min()         # range of MLR values
    dT_back = T_back_c_avg.max() - T_back_c_avg.min()   # range of T_back
    for i in range(0, N_names):

        SSE[i] = SSE[i] + np.sum( (mlr_c_avg - mlr_c[:,i])**2 )/(N*dmlr**2) + \
                          np.sum( (T_back_c_avg - T_back_c[:,i])**2)/(N*dT_back**2)
    
    # back surface temperature versus time
    plt.figure(i_case)
   
    # loop through different predictions
    i_n = 0     # initialize counter for predictions
    for name in names:

        plt.plot( times[i_n]/60, temps_back[i_n],
                  ls=name_plt_lines[name][1],
                  color=name_plt_lines[name][0],
                  label=name_labels[i_n] )
        
        # update prediction counter
        i_n += 1

    # mean and standard deviation
    plt.plot( t_c/60, T_back_c_avg, ls='-', color='gray', lw=2.5,
                label='Mean')
    plt.fill_between(t_c/60, T_back_c_avg - T_back_c_std, T_back_c_avg + T_back_c_std, 
                        color='gray', alpha=0.2)

    plt.xlim(left=0)
    plt.xlim(right=math.ceil( (t_c[-1]/60)/5 )*5 )
    plt.ylim(bottom=200)
    plt.title(case, fontsize=20, fontweight='bold')
    plt.xlabel(r"Time (min)", fontsize=20)
    plt.ylabel(r"Back Surface Temperature (K)", fontsize=20)
    plt.legend(loc=4, numpoints=1, ncol=2, prop={'size':10})
    plt.tight_layout()
    plt.savefig("T_back_vs_t_" +
                case + ".png")
       
    # mass loss rate versus time
    plt.figure(i_case+1)
   
    # loop through different predictions
    i_n = 0     # initialize counter for predictions
    for name in names:

        plt.plot( times[i_n]/60, mlrates[i_n],
                  ls=name_plt_lines[name][1],
                  color=name_plt_lines[name][0],
                  label=name_labels[i_n] )
        
        # update prediction counter
        i_n += 1

    # mean and standard deviation
    plt.plot( t_c/60, mlr_c_avg, ls='-', color='gray', lw=2.5,
                label='Mean')
    plt.fill_between(t_c/60, mlr_c_avg - mlr_c_std, mlr_c_avg + mlr_c_std, 
                        color='gray', alpha=0.2)

    plt.xlim(left=0)
    plt.xlim(right=math.ceil( (t_c[-1]/60)/5 )*5 )
    plt.ylim(bottom=0)
    plt.title(case, fontsize=20, fontweight='bold')
    plt.xlabel(r"Time (min)", fontsize=20)
    plt.ylabel(r"Mass Loss Rate (g m$^{-2}$ s$^{-1}$)", fontsize=20)
    plt.legend(loc=1, numpoints=1, ncol=2, prop={'size':10})
    plt.tight_layout()
    plt.savefig("mlr_vs_t_" +
                case + ".png")

    # update case counter
    i_case += 10

# print final SSEs

print('---------------------------------------------------')
print(' ')
print(' Total Sum of Squares Error for Each Parameter Set ')
print(' ')
print('---------------------------------------------------')
print(' ')

for i in range(0,N_names):

    print( names[i] + ' '*(12-len(names[i])) + ':  ', SSE[i] )
    
    # ==========================================================
# Export vers fichier Excel
# ==========================================================
df = pd.DataFrame(results)
df.to_excel("results_statistics.xlsx", index=False, engine="openpyxl")

print("✅ Result saved to 'results_statistics.xlsx'")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Extraire flux et épaisseur ---
df["flux"] = df["case"].str.extract(r"q(\d+)").astype(int)
df["thickness"] = df["case"].str.extract(r"_(\d+)mm").astype(int)

# --- Trier correctement ---
df = df.sort_values(["flux", "thickness"])

# --- Agrégation ---
df_grouped = df.groupby(["flux", "thickness"]).mean(numeric_only=True).reset_index()

# --- Fonction de tracé ---
def plot_two_series(df, y_mean, y_std, title, ylabel):
    plt.figure(figsize=(8,6))

    for thickness in sorted(df["thickness"].unique()):
        subset = df[df["thickness"] == thickness]

        plt.errorbar(
            subset["flux"],
            subset[y_mean],
            yerr=subset[y_std],
            fmt='o-',
            capsize=5,
            label=f"{thickness} mm"
        )

    plt.xticks([10, 30, 60])
    plt.xlabel("Heat flux (kW/m²)", fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20)
    plt.legend(fontsize=20)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- Tracés ---
plot_two_series(df_grouped, "t_p_mean", "t_p_std", "Mean Time to Peak MLR", "Time to Peak MLR (s)")
plot_two_series(df_grouped, "mlr_p_mean", "mlr_p_std", "Mean Peak MLR", "Mean Peak MLR (kW/m²)")
plot_two_series(df_grouped, "t_o_mean", "t_o_std", "Mean Onset Time", "Onset Time (s)")
plot_two_series(df_grouped, "t_f_mean", "t_f_std", "Mean Final Time", "Final Time (s)")



