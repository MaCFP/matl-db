"""
Script to generate exact solution for constant heating rate TGA
using the solution from Coheur et al., J Mater Sci, 2021
"""

import json
import csv
import numpy             as     np
import matplotlib.pyplot as     plt
import pandas            as     pd
from   scipy.special     import expi
import argparse


# create the parser
parser             = argparse.ArgumentParser()

# compare_all is false by default unless -C flag is used in command prompt
parser.add_argument("--compare_all", "-c", action = "store_true")

parser.add_argument('matl_set')

parser.add_argument('matl_set_year')

# parse arguments
args               = parser.parse_args()

# function to get kinetic parameters for given material property set
def get_kinetics(matl_set, matl_set_year):
    
    json_file_path = '../../PMMA/Material_Properties/' + str(matl_set_year) + '/' + args.matl_set + '.json'
    
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    n_reactions             = json_data['Kinetics']['Number of Reactions']
    A                       = json_data['Kinetics']['Pre-exponential']
    E                       = json_data['Kinetics']['Activation Energy']
    N_S                     = json_data['Kinetics']['Reaction Order']
    NU_MATL                 = json_data['Kinetics']["Solid Yield"]
    Initial_Mass_Fraction   = json_data['Kinetics']["Initial Mass Fraction"]
    
    fetched_kinetic_values  = {"A" : A, "E" : E, "n_reactions" : n_reactions, "N_S" : N_S, "NU_MATL" : NU_MATL, "Initial_Mass_Fraction" : Initial_Mass_Fraction}

    return fetched_kinetic_values, A, E, Initial_Mass_Fraction

# function to get FDS predictions for given material property set 
def read_csv(matl_set):
    csv_file_path       = "../Model_predictions" + '/' + matl_set + "_" + "dynamic_TGA_10K" + "_" + "FDS" + ".csv"
    data                = pd.read_csv(csv_file_path)

    # extract imported data and replace non-number values with NaN values
    data['Time']        = pd.to_numeric(data['t'], errors = 'coerce')
    data['Temperature'] = pd.to_numeric(data['T'], errors = 'coerce')
    data['Mass']        = pd.to_numeric(data['m'], errors = 'coerce')

    # Drop NaN values
    data                = data.dropna()

    # model predictions 
    t_m     = data['Time'].values
    m_m     = data['Mass'].values
    T_m     = data['Temperature'].values

    # constant
    R       = 8.314                                  # gas constant       , J/mol-K

    # scenario parameters
    T_0     = T_m[0]                                 # initial temperature, C
    beta    = 10 / 60                                # heating rate       , K/min
    alpha_0 = 0                                      # initial progress factor

    # unit conversions
    beta    = 10 / 60    ;                           # heating rate       , K/s

    # numerical parameters
    N       = len(t_m)
    
    return t_m, m_m, T_m, R, T_0, beta, alpha_0, N

def analytical_solution(INITIAL_MASS_FRACTION ,n_reactions,fetched_kinetic_values,alpha_0,beta,T_0,R,T_m,m_m,N):
    total_mass = np.zeros(N)

    for i in range(0, n_reactions):

        #create solution arrays
        t     = []
        t     = np.linspace(0, N)
        
        try:
            A       = int(fetched_kinetic_values["A"][i])
            E       = int((fetched_kinetic_values["E"])[i])
            NU_MATL = (fetched_kinetic_values["NU_MATL"])[i]
            # temporary fix
            INITIAL_MASS_FRACTION_temp = INITIAL_MASS_FRACTION[i]
            
        except(TypeError):
            A = (fetched_kinetic_values["A"])
            E = (fetched_kinetic_values["E"])
            NU_MATL = (fetched_kinetic_values["NU_MATL"])
            # temporary fix
            INITIAL_MASS_FRACTION_temp = INITIAL_MASS_FRACTION
            
        C             = (1 - alpha_0) * np.exp( (A / beta) * T_0 * np.exp( - E / (R * T_0) ) + A * E / (beta * R) * expi( - E / (R * T_0) ) )
        alpha = np.zeros(N)
        for i2 in range(0, N):

            alpha[i2] = 1 - C * np.exp(- (A / beta) * T_m[i2] * np.exp(- E / (R * T_m[i2])) - \
                                         (A / beta) * (E / R) * expi( - E / (R * T_m[i2]) ) )
        
        
        v             = NU_MATL
            
        m_i_0         = m_m[0] * INITIAL_MASS_FRACTION_temp
        
        m_i_f         = v * m_i_0
        
        # convert alpha to masses
        m_e           = m_i_0 - (m_i_0 - m_i_f) * alpha
        
        total_mass    = total_mass + m_e
    
    
    return total_mass
        
 
 
def plot_and_rms(matl_set,matl_set_number, fig, axs, compare_all, total_mass,n_reactions,T_m,m_m,N):
    #rms_err = 0
    #return rms_err,fig,axs
    #fig = fig
    #axs = axs
    
    rms_err                         = np.sqrt(np.sum( (m_m - total_mass) ** 2) / N)
    if compare_all is False:
        print('root mean square error:', rms_err)
        #plot model
        plt.plot(T_m, m_m, label        = 'Model Predictions', color = 'red', marker = '.')

        # root mean square error is calculated
        rms_err                         = np.sqrt(np.sum( (m_m - total_mass) ** 2) / N)
          #  print('root mean square error:', rms_err)
        
        # plot the analytical solution
        plt.plot(T_m, total_mass, label = 'Exact Solution')

        plt.xlabel(r'Temperature (K)', fontsize = 20)
        plt.ylabel(r'Mass (-)'       , fontsize = 20)
        plt.legend()
        plt.tight_layout();
        plt.show()
        

        
    if compare_all is True:
      #  axs = 0
      #  fig = 0
        
        axs[matl_set_number].plot(T_m, m_m)
        axs[matl_set_number].plot(T_m,total_mass)
        axs[matl_set_number].set_title(matl_set)
        
        
    return fig, axs, rms_err

def run(fig, axs, matl_set_number, matl_set, matl_set_year, compare_all):
    
    t_m, m_m, T_m, R, T_0, beta, alpha_0, N             = read_csv(matl_set)

    fetched_kinetic_values, A, E, INITIAL_MASS_FRACTION = get_kinetics(matl_set, matl_set_year)

    n_reactions                                         = int(fetched_kinetic_values["n_reactions"])

    total_mass                                          = analytical_solution(INITIAL_MASS_FRACTION, n_reactions, fetched_kinetic_values, alpha_0, beta, T_0, R, T_m, m_m, N)
    
    if compare_all is True:
        meaningless = 1
    else:
        fig = False
        axs = False

    fig, axs, rms_err                                             = plot_and_rms(matl_set,matl_set_number,fig, axs, args.compare_all,total_mass,n_reactions,T_m,m_m,N)
    
    #print(fig,axs,rms_err)
    
    return fig, rms_err


# Work in progress to compare all reactions
def compare_all(compare_all):
    matl_set_list = [
        "MaCFP_PMMA_NIST",
        "MaCFP_PMMA_Aalto_I",
        "MaCFP_PMMA_BUW-FZJ_A",
        "MaCFP_PMMA_BUW-FZJ_B",
        "MaCFP_PMMA_DBI_1",
        "MaCFP_PMMA_DBI_2",
        "MaCFP_PMMA_DBI_3",
        "MaCFP_PMMA_DBI_4",
        "MaCFP_PMMA_GIDAZE+",
        "MaCFP_PMMA_Sandia_1",
        "MaCFP_PMMA_Sandia_2",
        "MaCFP_PMMA_Sandia_3",
        "MaCFP_PMMA_Sandia_4",
        "MaCFP_PMMA_Sandia_5",
        "MaCFP_PMMA_Sandia_6",
        "MaCFP_PMMA_UCLAN",
        "MaCFP_PMMA_UMD",
        "MaCFP_PMMA_UMET_GP",
        "MaCFP_PMMA_UMET_TK",
        "MaCFP_PMMA_Aalto_II",
        "MaCFP_PMMA_BUW - FZJ_C",
        "MaCFP_PMMA_DBI_calibrated",
        "MaCFP_PMMA_NIST - StMU",
        "MaCFP_PMMA_UMET",
    ]

    rms_err = {}
    matl_sets_not_run = []
    
    counter = 0
    
    rows = 5
    cols = 5
        #fig = 0
        #axs = 0
    fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize=(20, rows * 4))
    axs = axs.flatten()
    
    for matl_set in matl_set_list:
        try:
            year = 2021
           # fig, axs, rms_err[matl_set] = [run(matl_set, year ,args.compare_all),year]
            #fig,rms_err[matl_set] = [run(counter, matl_set, year ,args.compare_all),year]
            fig,rms_err[matl_set] = run(fig,axs,counter, matl_set, year ,args.compare_all)
            rms_err_list_within_dictionary = [rms_err[matl_set],year ]
            rms_err[matl_set] = rms_err_list_within_dictionary

            
            #rms_err[matl_set[1]] = year
            counter += 1

#            print(fig,axs,rms_err)
        except(FileNotFoundError):
            year = 2023
            try:
                fig,rms_err[matl_set] = run(fig,axs,counter, matl_set, year ,args.compare_all)
                rms_err_list_within_dictionary = [rms_err[matl_set],year ]
                rms_err[matl_set] = rms_err_list_within_dictionary
                counter += 1
            
            except:
                matl_sets_not_run.append(matl_set)
                counter +=1
                continue
   # return fig, axs, rms_err
#print(key, spaces_string, value, "\n")
            
            
    #counter +=1
   # print(rms_err)
    return fig, rms_err, matl_sets_not_run


            
def create_spaces_to_align(string, length_of_space):
    spaces_string = ""
    for i in range(0,length_of_space - (len(string))):
         spaces_string += " "
    return spaces_string
        

        #print(key, spaces_string, value, "\n")
            
            
         #   counter +=1
    #return rms_err, matl_sets_not_run



if args.compare_all is True:
    fig, rms_err, matl_set_not_run = (compare_all(args.compare_all))
   # print(rms_err)
    
    for matl_set in matl_set_not_run:
        print("error - matl set not run:",matl_set,"\n")
        

    #print(rms_err)
    for key,value in rms_err.items():
  #      spaces_string = ""
  #      for i in range(0,20 - (len(key))):
  #          spaces_string += " "
        
#key is matl_set, value[0] is rms_err, value[1] id
        matl_set = key
        rms_err_temp = value[0]
  #      rms_err_temp = value
        year = value[1]
 #       year = 2
        print(year,matl_set,create_spaces_to_align(matl_set,20),"rms_err:" , rms_err_temp ,"\n")
    plt.show()
        
if args.compare_all is False:
    fig = False
    axs = False
    counter = False
    run(fig, axs, counter, args.matl_set, args.matl_set_year, args.compare_all)
    




 # save as CSV
#with open('../results/' + args.matl_set + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "_results.csv", mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'alpha', 'Temperature'])
#    writer.writerow([   's',     '-',           'K'])
#    for i in range(len(t_m)):
#        writer.writerow([ t[i], alpha[i], T_m[i] ])
