"""
Script to generate exact solution for constant heating rate TGA
using the solution from Coheur et al., J Mater Sci, 2021
"""

import json
import csv
import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd
from   scipy.special import expi
import argparse




# create the parser
parser = argparse.ArgumentParser()
# add an argument
parser.add_argument('material')
# parse arguments
args = parser.parse_args()


def openjson(material):
    year = str(2021)
    json_file_path = '../../PMMA/Material_Properties/' + year + '/' + args.material + '.json'
    

 

    # read the json file
    
    try:
        with open(json_file_path, 'r') as file:
            year = str(2021)
            kinetic_values           = json.load(file)
        return kinetic_values
    except:
        year = str(2023)
        with open(json_file_path, 'r') as file:
            kinetic_values           = json.load(file)
        return kinetic_values



def getvaluesfromjson(kinetic_values):
    try:
        n_reactions = kinetic_values['Kinetics']['Number of Reactions']
    except(KeyError):
        n_reactions = kinetic_values['Kinetics']['Number of Reactions']
    A       = kinetic_values['Kinetics']['Pre-exponential']   # pre-exponential    , 1/s
    E       = kinetic_values['Kinetics']['Activation Energy']
    N_S     = kinetic_values['Kinetics']['Reaction Order']
    NU_MATL = kinetic_values['Kinetics']["Solid Yield"]
    Initial_Mass_Fraction = kinetic_values['Kinetics']["Initial Mass Fraction"]
    fetched_kinetic_values = {"A":A,"E":E,"n_reactions":n_reactions,"N_S":N_S,"NU_MATL":NU_MATL, "Initial_Mass_Fraction" :Initial_Mass_Fraction}
    return fetched_kinetic_values, A, E, Initial_Mass_Fraction

        


# read the CSV file
def read_csv(material):
    csv_file_path  = "../Model_predictions" + '/' + material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + ".csv"
#    csv_file_path  = "../New folder" + '/' + material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + ".csv"
    data                = pd.read_csv(csv_file_path)



    # extract imported data and replace non-number values with NaN values
    data['Time']        = pd.to_numeric(data['t']    , errors = 'coerce')
    data['Temperature'] = pd.to_numeric(data['T']  , errors = 'coerce')
    data['Mass']        = pd.to_numeric(data['m'] , errors = 'coerce')

    # Drop NaN values
    data    = data.dropna()


    # model predictions 
    t_m     = data['Time'].values
    m_m     = data['Mass'].values
    T_m     = data['Temperature'].values



    # constant
    R       = 8.314                                  # gas constant       , J/mol-K

    # kinetic parameter
    m_f     = m_m[-1]                                # final mass

    # scenario parameters
    T_0     = T_m[0]                                 # initial temperature, C
    beta    = 10 / 60                                # heating rate       , K/min
    t_f     = t_m[-1]                                # final time         , s
    alpha_0 = 0                                      # initial progress factor

    # unit conversions
    beta    = 10 / 60    ;                           # heating rate       , K/s


    # numerical parameters
    N       = len(t_m)
    return t_m, m_m, T_m, R, m_f, t_f, T_0, beta, t_f,alpha_0, N


                    
def analytical_solution(INITIAL_MASS_FRACTION ,n_reactions,fetched_kinetic_values,alpha_0,beta,T_0,R,T_m,m_f,t_f,m_m,N):
    m_e_dict = {}
    total_mass = np.zeros(N)

    for i in range(0,n_reactions):

        #create solution arrays
        t = []
        t = np.linspace(0, t_f, N)
        
        
    
        try:
            A = int(fetched_kinetic_values["A"][i])
            E = int((fetched_kinetic_values["E"])[i])
            NU_MATL = (fetched_kinetic_values["NU_MATL"])[i]
            INITIAL_MASS_FRACTION_temp = INITIAL_MASS_FRACTION[i]
            
            #temporary fix
            
        except(TypeError):
            A = (fetched_kinetic_values["A"])
            E = (fetched_kinetic_values["E"])
            NU_MATL = (fetched_kinetic_values["NU_MATL"])
            #temporary fix
            INITIAL_MASS_FRACTION_temp = INITIAL_MASS_FRACTION
            
        
        
        
        C       = (1 - alpha_0) * np.exp( (A / beta) * T_0 * np.exp(-E / (R * T_0) ) + A * E / (beta * R) * expi( - E / (R * T_0) ) )
        alpha = np.zeros(N)
        for i2 in range(0,N):

            alpha[i2] = 1 - C * np.exp(- (A / beta) * T_m[i2] * np.exp(- E / (R * T_m[i2])) - \
                                         (A / beta) * (E / R) * expi( - E / (R * T_m[i2]) ) )
        
        
        v = NU_MATL
            
        m_i_0 = m_m[0]*INITIAL_MASS_FRACTION_temp
        
        m_i_f = v * m_i_0
        
        # convert alpha to masses
        m_e          = m_i_0 - (m_i_0 - m_i_f) * alpha
        
        total_mass = total_mass + m_e
    
    #total_mass = m_m[0total_mass
    
    return total_mass
        
 
 
def plot_and_rms(total_mass,n_reactions,T_m,m_m,N):
    
    #plot model
    plt.plot(T_m, m_m, label  = 'Model Predictions', color = 'red', marker = '.')

    # root mean square error is calculated
    rms_err    = np.sqrt(np.sum( (m_m - total_mass) ** 2) / N)
    print('root mean square error:', rms_err)
        
    # plot the analytical solution
    plt.plot(T_m, total_mass, label  = 'Exact Solution')

    plt.xlabel(r'Temperature (K)', fontsize = 20)
    plt.ylabel(r'Mass (-)'       , fontsize = 20)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return(rms_err)

def run(material):
    
    kinetic_values = openjson(material)

    t_m, m_m, T_m, R, m_f, t_f, T_0, beta, t_f,alpha_0, N = read_csv(material)
 
    fetched_kinetic_values, A, E, INITIAL_MASS_FRACTION = getvaluesfromjson(kinetic_values)

    n_reactions = int(fetched_kinetic_values["n_reactions"])

    total_mass = analytical_solution(INITIAL_MASS_FRACTION,n_reactions,fetched_kinetic_values,alpha_0,beta,T_0,R,T_m,m_f,t_f,m_m,N)

    rms_err = plot_and_rms(total_mass,n_reactions,T_m,m_m,N)
    
    return rms_err


# Work in progress to compare all reactions
def compare_all():
    material_list = [
       # "MaCFP_PMMA_NIST",
        "MaCFP_PMMA_Aalto_I",
        "MaCFP_PMMA_BUW-FZJ_A",
        "MaCFP_PMMA_BUW-FZJ_B",
        "MaCFP_PMMA_DBI_1",
        "MaCFP_PMMA_DBI_2",
        "MaCFP_PMMA_DBI_3",
        "MaCFP_PMMA_DBI_4",
        "MaCFP_PMMA_GIDAZE+",
        "MaCFP_PMMA_NIST",
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

    A_list = {}
    E_list = {}
    rms_err = {}
    counter = 0
    for material in material_list:
        try:
            rms_err[counter] = run(material)
            counter += 1
            print(material)
        except(FileNotFoundError):
            counter +=1
    return rms_err


#print(compare_all())
        

run(args.material)
#rms_err = compare_all()
#print(rms_err)




 # save as CSV
#with open('../results/' + args.material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "_results.csv", mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'alpha', 'Temperature'])
#    writer.writerow([   's',     '-',           'K'])
#    for i in range(len(t_m)):
#        writer.writerow([ t[i], alpha[i], T_m[i] ])