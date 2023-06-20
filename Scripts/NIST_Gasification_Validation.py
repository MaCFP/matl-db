# script to plot and compare predictions for NIST Gasification Apparatus

import math
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.ion()

def get_predictions( case ):
  
    # store all predictions in dictionary
    pred_dict = {}

    # wak through results directory 
    for subdir, dir, files in os.walk(results_dir):
        
        for file in files:
           
            # identify files with results for 'case'
            if ( (case in file) and ('csv' in file) and
                 (not ('Kaowool' in file)) and 
                 (not ('Copper' in file)) ):

                # get data from file
                name = file.partition('_Gasification')[0]
                dir_file = subdir + '/' + file
                
                data = pd.read_csv(dir_file, skiprows=range(1,2))
                data = data.dropna(how='all')
           
                # add data to prediction dictionary
                if name in pred_dict.keys():
                    data_old = pred_dict[name]['Data']
                    data_new = pd.merge( data_old, data, on='Time', how='outer' )
                    pred_dict[name]['Data'] = data_new
                else:
                    pred_dict[name] = {'Data': data}
            
    # compute mean and standard deviation of predictions for each name
    for name in pred_dict.keys():
       
        pred_data = pred_dict[name]['Data']
        
        # extract times and corresponding predicted values
        t       = pred_data['Time'].values
        y_pred  = pred_data.loc[:, pred_data.columns != 'Time'].values
   
        # temporary exception for BUW-FZJ-C
        if (name == 'BUW-FZJ-C') and ('MLR' in case):
            y_pred = pred_data.loc[:, pred_data.columns.str.contains('Combined')].values

        # compute mean and standard deviation
        y_mean  = np.nanmean(y_pred, axis=1)
        y_std   = np.nanstd(y_pred, axis=1)

        # store mean and standar deviation arrays to prediction dictionary
        pred_dict[name]['Time'] = t
        pred_dict[name]['Mean'] = y_mean
        pred_dict[name]['StD'] = y_std

    return pred_dict 
 

# constants
results_dir = '../PMMA/Validation_Results/'
cases = [ "q25_Temp", "q50_Mass", "q50_MLR", "q50_Temp" ]


# plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

plt_dict = {
     "Aalto-I": ['b','-'],
     "Aalto-II": ['b','--'],
     "BUW-FZJ-A": ['lawngreen','-'],
     "BUW-FZJ-B": ['lawngreen','--'],
     "BUW-FZJ-C": ['lawngreen','-.'],
     "DBI-1": ['g','-'],
     "DBI-cal": ['g','--'],
     "NIST-StMU-FSRI": ['r','-'],
     "NIST-FSRI": ['c','-'],
     "EDF": ['m','-'],
     "UMD-FSRI": ['y','-'],
     "UMET": ['orange','-']
}

plt_marker_dict = {
     "Aalto-I": ['b','o'],
     "Aalto-II": ['b','s'],
     "BUW-FZJ-A": ['lawngreen','o'],
     "BUW-FZJ-B": ['lawngreen','s'],
     "BUW-FZJ-C": ['lawngreen','^'],
     "DBI-1": ['g','o'],
     "DBI-cal": ['g','s'],
     "NIST-StMU-FSRI": ['r','o'],
     "NIST-FSRI": ['c','o'],
     "EDF": ['m','o'],
     "UMD-FSRI": ['y','o'],
     "UMET": ['orange','o']
}

# get experimental data

# dictionary to organize all experimental data
expt_dict = {}

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

        for case in cases:

            if case in file:

                if case in expt_dict.keys():
                    data_old = expt_dict[case]
                    data_new = pd.merge( data_old, data, on='Time', how='outer' )
                    expt_dict[case] = data_new
                else:
                    expt_dict[case] = data

# create empty error dictionary
nrms_dict = {}
       
# work with data
idx_plt = 1
for case in cases:


    # 1. Get and analyze all experimental data for case

    expt    = expt_dict[case]
    t_expt  = expt['Time'].values
    y_expt  = expt.loc[:, expt.columns != 'Time'].values

    # compute mean and standard deviation
    y_mean  = np.nanmean(y_expt, axis=1)
    y_std   = np.nanstd(y_expt, axis=1)

    # 2. Get and analyze all model predictions for case
    pred_dict = get_predictions( case )

    # 3. Compute and print comparison statistics

    nrms_dict[case] = {}
    
    for name in pred_dict.keys():

        # get prediction mean data
        t_pred = pred_dict[name]['Time']
        y_pred = pred_dict[name]['Mean']

        N = len(t_expt)
        y_pred_int = np.interp(t_expt, t_pred, y_pred)

        # compute root mean square error
        RMS = np.sqrt(np.sum( (y_mean-y_pred_int)**2 )/N)
       
        # RMS normalized by range of experimental data
        NRMS = RMS/(max(y_mean)-min(y_mean))

        nrms_dict[case][name] = NRMS

    error_df = pd.DataFrame.from_dict(nrms_dict)
   
    # 4. Plot results for case

    # plot experimental data versus time
    plt.figure(idx_plt)
    for i in range(0,y_expt.shape[1]):
        plt.plot( t_expt, y_expt[:,i], ls='-', color='black', lw=0.5 )

    plt.plot(t_expt, y_mean, ls='-', color='black', lw=2.5, 
             label='Experimental Mean') 

    plt.fill_between(t_expt, y_mean - 2*y_std, y_mean + 2*y_std, 
                     color='gray', alpha=0.2)

    # plot predictions versus time
    for name in pred_dict.keys():

        plt.plot( pred_dict[name]['Time'], pred_dict[name]['Mean'], 
                  ls=plt_dict[name][1],
                  color=plt_dict[name][0],
                  label=name )
    
    plt.xlabel(r"Time (s)", fontsize=20)
    if 'Temp' in case:
        plt.ylabel(r"Back Surface Temperature (K)", fontsize=20)
        plt.xlim([0, np.ceil(t_expt.max()/50)*50])
        plt.ylim([250, np.ceil(np.nanmax(y_expt)/50)*50])
        plt.legend(loc=4, numpoints=1, ncol=2, prop={'size':10})
    if 'Mass' in case:
        plt.ylabel(r"Sample Mass (g)", fontsize=20)
        plt.legend(loc=1, numpoints=1, ncol=2, prop={'size':10})
    if 'MLR' in case:
        plt.ylabel(r"Mass Loss Rate (g/m$^2\ $s)", fontsize=20)
        plt.xlim([0, np.ceil(t_expt.max()/50)*50])
        plt.ylim([0, np.ceil(np.nanmax(y_expt)/20)*20])
        plt.legend(loc=2, numpoints=1, ncol=2, prop={'size':10})

    plt.tight_layout()
    plt.savefig("../PMMA/Validation_Results/plots/MaCFP-PMMA_Gasification_" +
                case + ".pdf")
    
    idx_plt += 1

# print root mean squared errors table
error_df['Total'] = error_df[list(error_df.columns)].sum(axis=1)
error_df = error_df.sort_values(by='Total')

# move any rows with NaNs to end
nan_mask = error_df.isna().any(axis=1)
error_df = pd.concat((error_df[~nan_mask], error_df[nan_mask]), axis=0)


print('-------------------------------------------')
print(' ')
print(' Normalized Root Mean Squared Errors ')
print(' ')
print(error_df.loc[:, error_df.columns != 'Total'])
print(' ')
print('-------------------------------------------')

# plots of normalized RMS errors for q = 50 kW/m^2 data
plt.figure(idx_plt)

q50_Mass_dict = nrms_dict['q50_Mass']
q50_Temp_dict = nrms_dict['q50_Temp']

for name in q50_Mass_dict:

    plt.plot( q50_Mass_dict[name], q50_Temp_dict[name],
                  marker=plt_marker_dict[name][1],
                  mec=plt_marker_dict[name][0], mfc='None',
                  ms=10, mew=2, linestyle='None',
                  label=name )

plt.xlabel(r"NRMS for Sample Mass", fontsize=20)
plt.ylabel(r"NRMS for Back Temperature", fontsize=20)
plt.legend(loc='upper center', numpoints=1, ncol=2, prop={'size':10})
plt.tight_layout()
plt.savefig("../PMMA/Validation_Results/plots/NRMS_q50_T_back_vs_Mass.pdf")
idx_plt += 1


# error plots
plt.rcParams.update(plt.rcParamsDefault)
#plt.rc('font', family='serif')
#plt.rc('xtick', labelsize=12)
#plt.rc('ytick', labelsize=12)

error_df.loc[:, error_df.columns != 'Total'].plot(kind='bar',stacked=True)
plt.ylabel('Normalized RMS Error',fontsize=18)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Results/plots/NRMS_total.pdf")
plt.show()


