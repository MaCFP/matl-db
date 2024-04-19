
"""
Script to generate exact solution for constant heating rate TGA at 10 K/min
using the solution from Coheur et al., J Mater Sci, 2021
"""

import json
import csv
import numpy             as     np
import matplotlib.pyplot as     plt
import pandas            as     pd
from   scipy.special     import expi
import argparse
from   mpmath            import mp, findroot

# constants
R       = 8.314     # gas constant, J/mol-K
beta    = 10/60     # heating rate, K/s

# create the parser
parser  = argparse.ArgumentParser()

# add arguments
parser.add_argument('matl_set')
parser.add_argument('matl_set_year')

# ONLY WORKS WITH MASTER.py (maybe clean up...) compare argument must come from Master.py
parser.add_argument('--compare_all', "-co", action = "store_true")

# parse arguments
args          = parser.parse_args()

matl_set      = args.matl_set
matl_set_year = args.matl_set_year

# only for MASTER.py
compare = args.compare_all

def run(matl_set, matl_set_year, compare_all_boolean):
    
    # retrieve kinetic values for given material property set
    json_file_path  = ( '../../PMMA/Material_Properties/' + str(matl_set_year)  
                        + '/' + matl_set + '.json' )
    
    with open(json_file_path, 'r') as file:
        json_data   = json.load(file)
    
    # get kinetic parameters
    # ... check if variables are read as string
    A   = json_data['Kinetics']['Pre-exponential'] 
    E   = json_data['Kinetics']['Activation Energy'] 
    n   = json_data['Kinetics']['Reaction Order'] 
    nu  = json_data['Kinetics']["Solid Yield"] 
    Y_0 = json_data['Kinetics']["Initial Mass Fraction"] 
    
    # store number of reactions
    if type(A) == float:
        N_r = 1
        A   = np.array( [A] )
        E   = np.array( [E] )
        n   = np.array( [n] )
        nu  = np.array( [nu] )
        Y_0 = np.array( [Y_0] )
    else:
        N_r = len(A)
        A   = np.array( A )
        E   = np.array( E )
        n   = np.array( n )
        nu  = np.array( nu )
        Y_0 = np.array( Y_0 )

    # retrieve FDS predictions for given material property set 
    csv_file_path   = ( "../Model_predictions" + '/' + matl_set + "_" 
                        + "dynamic_TGA_10K" + "_" + "FDS" + ".csv" )
    data            = pd.read_csv(csv_file_path)
    
    # extract imported data and replace non-number values with NaN values
    t_m     = pd.to_numeric(data['t'], errors = 'coerce').values[1:]
    T_m     = pd.to_numeric(data['T'], errors = 'coerce').values[1:]
    m_m     = pd.to_numeric(data['m'], errors = 'coerce').values[1:]

    # removes data points one data point before mass = 0
    zero_indices    = np.where(m_m == 0)[0]
    idx_max         = zero_indices[0]
    t_m             = t_m[0:idx_max]        # model times, s
    m_m             = m_m[0:idx_max]        # model masses, [-]
    T_m             = T_m[0:idx_max]        # model temperatures, K
    
    # scenario parameters
    T_0         = T_m[0]        # initial temperature, K
    N           = len(t_m)      # number of points
    m_a         = np.zeros(N)   # array of analytical masses
   
    for i in range(0, N_r):

        # for a reaction order of 1 calculate C
        if n == 1:
           
            # constants
            C     = np.exp( (A[i] / beta) * T_0 * np.exp( - E[i] / (R * T_0) ) + \
                             A[i] * E[i] / (beta * R) * expi( - E[i] / (R * T_0) ) )
      
            # create array of reaction progress values
            alpha = np.zeros(N)
     
            # calculate alpha_i at all temperatures
            for j in range(0, N):
                alpha[j]  = 1 - C*np.exp(-(A[i]/beta)*T_m[j]*np.exp(-E[i]/(R*T_m[j]) ) - \
                                     (A[i]/beta)*(E[i]/R)*expi( -E[i]/(R*T_m[j]) ) )


      #elif n != 1:




    #     for i2 in range(0, N):
    #             # for a reaction order of 1 calculate alpha
    #             if n_i        == 1:
    #                 alpha[i2]  = 1 - C * np.exp(- (A / beta) * T_m[i2] * np.exp(- E / (R * T_m[i2]) ) - \
    #                                     (A / beta) * (E / R) * expi( - E / (R * T_m[i2]) ) )
    #             # for a reaction order that is not 1 solve for alpha
    #             if n_i        != 1:
    #                 # Breaks the Coheurt analytical solution with reaction order into smaller functions 
    #                 g_z        = (1 - n_i) * - (A / beta) * T_m[i2] * np.exp( - E / (R * T_m[i2]) ) - \
    #                              (A / beta) * (E / R) *expi( - E / (R * T_m[i2]) )
    #                 f_z        = (1 - n_i)
    #                 B_z        = (A / beta) * T_0 * np.exp( - E / (R * T_0) ) + expi( - E / (R * T_0)) * \
    #                              (A * E) / (beta * R)
    #                 # set the number of significant figures for the solution to the non-linear equation to 50
    #                 mp.dps = 50
    #                 # solves the non-linear equation for alpha
    #                 def equation(x):
    #                     return 1 - (g_z + ( ( (1 - x * T_0) ** f_z) / f_z + B_z) ) ** (1 / f_z)
    #                     # initial guess for alpha is 0
    #                     if i2             == 0:
    #                         initial_guess  = 0
    #                     # sequential guesses for alpha are the last value of alpha
    #                     if i2             != 0:
    #                         initial_guess  = alpha[i2 - 1]
    #                     # find root of equation as solution for alpha
    #                     root               = findroot(equation, initial_guess)
    #                     alpha[i2]          = root
    #     # convert alpha to masses
    #     v             = NU_MATL
    #     m_i_0         = m_m[0] * Initial_Mass_Fraction_Temporary
    #     m_i_f         = v * m_i_0
    #     m_e           = m_i_0 - (m_i_0 - m_i_f) * alpha
    #     total_mass    = total_mass + m_e
    #     
    # rms_err           = plot_and_rms(total_mass, n_reactions,T_m, m_m, N, compare,A,E)
    rms_err = 1
    plt.plot(T_m, alpha)
    plt.show()

    return rms_err

run(matl_set, matl_set_year, compare)

#      
# def plot_and_rms(total_mass, n_reactions, T_m, m_m, N, compare,A,E):
# 
#     # root mean square error is calculated
#     rms_err                         = np.sqrt(np.sum( (m_m - total_mass) ** 2) / N)
#     
#     # plot model
# #    plt.plot(T_m, m_m, label        = 'Model Predictions', color = 'red', marker = '.')
#     
#     # plot the analytical solution
# 
#     print(len(T_m))
#     print(len(total_mass))
# 
#     plt.plot(T_m, total_mass, label = 'Exact Solution')
# 
#     plt.xlabel(r'Temperature (K)', fontsize = 20)
#     plt.ylabel(r'Mass (-)'       , fontsize = 20)
#     plt.legend()
#     plt.tight_layout();
#     print(f(matl_set,23) + "rms err:" + str(rms_err) )
#     if compare is False:
#         plt.savefig("../Plot Results/" + args.matl_set + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "plot.pdf")
#         plt.show()
# 
# # update comparison_data.json with RMSE and kinetics for creating graph of A vs RMSE
# #    dictionary_1 = {}
# #    results_dictionaries = {matl_set : {"A":A,"E":E, "RMSE":rms_err }}
# #        with open('comparison_data.json','r') as file:
# #            data = json.load(file)
# #            data.update(results_dictionaries)
# #    except:
# #        print("error first try statement")
# #        json.dump(results_dictionaries, file, indent = 4)
# #    with open('comparison_data.json','w') as file:
# #         json.dump(data, file, indent = 4)
#     return rms_err
# 
# #output formatting tool            
# def f(string, length_of_space):
#     string              = str(string)
#     spaces_string       = ""
#     for i in range(0, length_of_space - (len(string))):
#          spaces_string += " "
#     return string + spaces_string
# 
# exceptions = 0
# if compare is False:
#     run(matl_set, matl_set_year, compare)
# if compare is True:
#     try:
#         run(matl_set, matl_set_year,compare)
#     except:
#         if exceptions < 2:    
#             print("error running", matl_set)
#             exceptions = exceptions + 1
#         pass
# 
#  # save as CSV
# #with open('../results/' + args.matl_set + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "_results.csv", mode='w', newline='') as file:
# #    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# #    writer.writerow(['Time', 'alpha', 'Temperature'])
# #    writer.writerow([   's',     '-',           'K'])
# #    for i in range(len(t_m)):
# #        writer.writerow([ t[i], alpha[i], T_m[i] ])
