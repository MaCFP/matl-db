# script to plot and compare predictions for NIST Gasification Apparatus

import math
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.ion()

def get_predictions( case ):
   
    # wak through results directory 
    for subdir, dir, files in os.walk(results_dir):
        
        for file in files:
           
            # identify files with results for 'case'
            if ((case and 'csv' in file) and 
                not ('Kaowool' in file) and 
                not ('Copper' in file)):

                print(file)
                
                # get data from file
                name = file.partition('_Gasification')[0]
                print(name)

                #data = pd.read_csv(results_dir + file, skiprows=range(1,2))
                #data = data.dropna(how='all')

                # store times and measured values
                #times = data['Time'].values
                #y_vals = data.loc[:, data.columns != 'Time'].values

    return case 
 

# constants
results_dir = '../PMMA/Validation_Results/'

# plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# list of cases
cases = [ "q25_Temp", "q50_Mass", "q50_MLR", "q50_Temp" ]

# # list of prediction set names
# names = [ "Aalto",
#           "BUW-FZJ_A",
#           "BUW-FZJ_B",
#           "DBI",
#           "GIDAZE+",
#           "NIST",
#           "UMD",
#           "UMET_GP",
#           "UMET_TK" ]
# 
# N_names = len(names) 
# 
# name_plt_lines = {
#     "Aalto": ['b','-'],
#     "BUW-FZJ_A": ['lawngreen','-'],
#     "BUW-FZJ_B": ['lawngreen','--'],
#     "DBI": ['g','-'],
#     "GIDAZE+": ['r','-'],
#     "NIST": ['c','-'],
#     "Sandia": ['m','-'],
#     "UCLAN": ['y','-'],
#     "UMD": ['k','-'],
#     "UMET_GP": ['orange','-'],
#     "UMET_TK": ['orange','--']
# }
# 
# name_labels = [ "Aalto",
#                 "BUW-FZJ (A)",
#                 "BUW-FZJ (B)",
#                 "DBI",
#                 "GIDAZE+",
#                 "NIST",
#                 "UMD",
#                 "UMET (GP)",
#                 "UMET (TK)" ]
# 



# get experimental data

# high level dictionary to organize all experimental data
expt_dict = {}
for case in cases:
    expt_dict[case] = [[],[]] 

# loop through files in NIST Gasification folder
for file in os.listdir("../PMMA/Validation_Data/NIST_Gasification_Apparatus/"):
   
    # check for relevant data file
    if file.startswith("MaCFP-PMMA_Gasification"):
        
        #print("   ",file)

        # store complete path of file
        dir_file = "../PMMA/Validation_Data/NIST_Gasification_Apparatus/" + file

        # get data
        data = pd.read_csv(dir_file, skiprows=range(1,2))
        data = data.dropna(how='all')

        # store times and measured values
        times = data['Time'].values
        y_vals = data.loc[:, data.columns != 'Time'].values

        # average if necessary
        #y_mean = np.nanmean(y_vals, axis=1)
        #y_std = np.nanstd(y_vals, axis=1)
        
        # sort to appropriate group 
        for case in cases:

            if case in file:
               
                expt_dict[case][0].append(times)

                for i in range(0,y_vals.shape[1]):

                    expt_dict[case][1].append(y_vals[:,i])
        
# work with data
idx_case = 1
for case in cases:

    # 1. Get and analyze all experimental data for case

    # extract data to lists 
    t_lst   = expt_dict[case][0]
    y_lst   = expt_dict[case][1]
  
    # make subarrays of equal length
    max_len = max(map(len, t_lst))

    # convert data to numpy array
    t_ar    = np.array([np.hstack((t_s, np.nan*np.ones(max_len-len(t_s)))) for t_s in t_lst])
    y_ar    = np.array([np.hstack((y_s, np.nan*np.ones(max_len-len(y_s)))) for y_s in y_lst])
   
    # compute mean and standard deviation
    # ...this is only works because all our data is at 1 s intervals
    t_mean  = np.nanmean(t_ar, axis=0)
    y_mean  = np.nanmean(y_ar, axis=0)
    y_std   = np.nanstd(y_ar, axis=0)

    # 2. Get and analyze all model predictions for case
    case = get_predictions( case )
  

    # 3. Compute all comparison statistics

    # 4. Plot results

    # plot data versus time
    plt.figure(idx_case)
    for i in range(0,t_ar.shape[0]):
        plt.plot( t_ar[i,:], y_ar[i,:], ls='-', color='black', lw=0.5 )

    plt.plot(t_mean, y_mean, ls='-', color='black', lw=2.0, 
             label='Experimental Mean') 

    plt.fill_between(t_mean, y_mean - 2*y_std, y_mean + 2*y_std, 
                     color='gray', alpha=0.2)

    plt.xlabel(r"Time (s)", fontsize=20)
    if 'Temp' in case:
        plt.ylabel(r"Back Surface Temperature (K)", fontsize=20)
        plt.legend(loc=2, numpoints=1, ncol=2, prop={'size':10})
    if 'Mass' in case:
        plt.ylabel(r"Sample Mass (g)", fontsize=20)
        plt.legend(loc=1, numpoints=1, ncol=2, prop={'size':10})
    if 'MLR' in case:
        plt.ylabel(r"Mass Loss Rate (g/m$^2\ $s)", fontsize=20)
        plt.legend(loc=2, numpoints=1, ncol=2, prop={'size':10})

    plt.tight_layout()
    plt.savefig("../PMMA/Validation_Results/plots/MaCFP-PMMA_Gasification_" +
                case + ".pdf")
    plt.show()
    
    idx_case += 1
    
   



    
#print(len(times_lst),len(y_vals_lst))

## loop through cases
#i_case  = 0                     # case counter index
#SSE     = np.zeros( N_names )   # initialize sum of squares error for each name
#
#for case in cases:
#    
#    # list of data arrays 
#    times           = []
#    masses          = []
#    temps_back      = []
#    temps_top       = []
#    mlrates         = []
#    mlrates_peak    = []
#    times_peak      = []
#    times_onset     = []
#    times_final     = []
#
#    # loop through predictions for 'case' to get raw data
#    for name in names:
#
#        # read data from files
#        dat = np.loadtxt('../PMMA/Computational_Results/Gasification_Predictions/' + 
#                            name + '_Gasification_' + case + '.csv',
#                            skiprows=2, delimiter=',')
#
#        # parse data
#        t       = dat[:,0]          # times (s)
#        m       = dat[:,1]          # mass (g)
#        T_back  = dat[:,2]          # bottom surface temperature (K)
#        T_top   = dat[:,3]          # top surface temperature (K)
#
#        # compute mass loss rate (g/m^2-s)
#        mlr     = -(1/A_s)*np.gradient( m, t )
#
#        # find peak MLR and time to peak MLR
#        mlr_p   = mlr.max()         # peak MLR (g/m^2-s)
#        t_p     = t[mlr.argmax()]   # time to peak MLR (s)
#
#        # find time to MLR = 1 g/m^2-s
#        t_o     = t[np.argwhere( mlr >= 1. ).min()]
#
#        # find maximum time for MLR >= 0.1 g/m^2-s
#        t_f     = t[np.argwhere( mlr >= 0.1 ).max()]
#
#        # save data to case lists
#        times.append( t )
#        masses.append( m )
#        temps_back.append( T_back )
#        temps_top.append( T_top )
#        mlrates.append( mlr )
#        mlrates_peak.append( mlr_p )
#        times_peak.append( t_p )
#        times_onset.append( t_o )
#        times_final.append( t_f )
#
#    # compute mean and standard deviations
#    t_p_mean    = np.mean( times_peak )
#    mlr_p_mean  = np.mean( mlrates_peak )
#    t_o_mean    = np.mean( times_onset )
#    t_f_mean    = np.mean( times_final )
#
#    t_p_std     = np.std( times_peak )
#    mlr_p_std   = np.std( mlrates_peak )
#    t_o_std     = np.std( times_onset )
#    t_f_std     = np.std( times_final )
#    
#    # create array of common times for averaging of predictions
#    t_min       = min(times_onset)    # smallest onset time (s)
#    t_max       = max(times_final)    # largest final time (s)
#    t_c         = np.linspace( t_min, t_max, N )
#
#    # arrays for storing interpolated data to common times 
#    T_back_c    = np.zeros( (N, N_names) ) 
#    mlr_c       = np.zeros( (N, N_names) ) 
#
#    # loop through predictions to interpolate to common times 
#    for i in range(0,N_names):
#
#        # get raw data for prediction i
#        t_i         = times[i]
#        T_back_i    = temps_back[i]
#        mlr_i       = mlrates[i]
#
#        # extend data if necessary
#        if t_i.max() < t_max:
#
#            # find times to be added to get up to t_max
#            t_add = t_c[np.argwhere( t_c > t_i.max() )]
#            
#            # append additional times to raw data
#            t_i = np.append( t_i, t_add )
#
#            # append MLR = 0 and T_back = T_back_final to raw data
#            T_back_i = np.append( T_back_i, T_back_i[-1]*np.ones( len(t_add) ) )
#            mlr_i = np.append( mlr_i, np.zeros( len(t_add) ) )
#
#        # interpolate MLR and T_back to common time arrays
#        T_back_c[:,i]   = np.interp( t_c, t_i, T_back_i )
#        mlr_c[:,i]      = np.interp( t_c, t_i, mlr_i )
#
#    # compute mean and standard deviations at common times
#    T_back_c_avg    = np.mean( T_back_c, axis=1 )
#    mlr_c_avg       = np.mean( mlr_c, axis=1 )
#
#    T_back_c_std    = np.std( T_back_c, axis=1 )
#    mlr_c_std       = np.std( mlr_c, axis=1 )
#
#    # compute total sum of squares errors of predictions from mean MLR and T_back
#    dmlr    = mlr_c_avg.max() - mlr_c_avg.min()         # range of MLR values
#    dT_back = T_back_c_avg.max() - T_back_c_avg.min()   # range of T_back
#    for i in range(0, N_names):
#
#        SSE[i] = SSE[i] + np.sum( (mlr_c_avg - mlr_c[:,i])**2 )/(N*dmlr**2) + \
#                          np.sum( (T_back_c_avg - T_back_c[:,i])**2)/(N*dT_back**2)
#    
#    # back surface temperature versus time
#    plt.figure(i_case)
#   
#    # loop through different predictions
#    i_n = 0     # initialize counter for predictions
#    for name in names:
#
#        plt.plot( times[i_n]/60, temps_back[i_n],
#                  ls=name_plt_lines[name][1],
#                  color=name_plt_lines[name][0],
#                  label=name_labels[i_n] )
#        
#        # update prediction counter
#        i_n += 1
#
#    # mean and standard deviation
#    plt.plot( t_c/60, T_back_c_avg, ls='-', color='gray', lw=2.5,
#                label='Mean')
#    plt.fill_between(t_c/60, T_back_c_avg - T_back_c_std, T_back_c_avg + T_back_c_std, 
#                        color='gray', alpha=0.2)
#
#    plt.xlim(left=0)
#    plt.xlim(right=math.ceil( (t_c[-1]/60)/5 )*5 )
#    plt.ylim(bottom=200)
#    plt.xlabel(r"Time (min)", fontsize=20)
#    plt.ylabel(r"Back Surface Temperature (K)", fontsize=20)
#    plt.legend(loc=4, numpoints=1, ncol=2, prop={'size':10})
#    plt.tight_layout()
#    plt.savefig("../PMMA/Computational_Results/Gasification_Predictions/T_back_vs_t_" +
#                case + ".pdf")
#       
#    # mass loss rate versus time
#    plt.figure(i_case+1)
#   
#    # loop through different predictions
#    i_n = 0     # initialize counter for predictions
#    for name in names:
#
#        plt.plot( times[i_n]/60, mlrates[i_n],
#                  ls=name_plt_lines[name][1],
#                  color=name_plt_lines[name][0],
#                  label=name_labels[i_n] )
#        
#        # update prediction counter
#        i_n += 1
#
#    # mean and standard deviation
#    plt.plot( t_c/60, mlr_c_avg, ls='-', color='gray', lw=2.5,
#                label='Mean')
#    plt.fill_between(t_c/60, mlr_c_avg - mlr_c_std, mlr_c_avg + mlr_c_std, 
#                        color='gray', alpha=0.2)
#
#    plt.xlim(left=0)
#    plt.xlim(right=math.ceil( (t_c[-1]/60)/5 )*5 )
#    plt.ylim(bottom=0)
#    plt.xlabel(r"Time (min)", fontsize=20)
#    plt.ylabel(r"Mass Loss Rate (g m$^{-2}$ s$^{-1}$)", fontsize=20)
#    plt.legend(loc=1, numpoints=1, ncol=2, prop={'size':10})
#    plt.tight_layout()
#    plt.savefig("../PMMA/Computational_Results/Gasification_Predictions/mlr_vs_t_" +
#                case + ".pdf")
#
#    # update case counter
#    i_case += 10
#
## print final SSEs
#
#print('---------------------------------------------------')
#print(' ')
#print(' Total Sum of Squares Error for Each Parameter Set ')
#print(' ')
#print('---------------------------------------------------')
#print(' ')
#
#for i in range(0,N_names):
#
#    print( names[i] + ' '*(12-len(names[i])) + ':  ', SSE[i] )
#
#
