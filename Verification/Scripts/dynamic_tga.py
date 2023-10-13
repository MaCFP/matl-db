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


    # ***replace with command line file specification
    csv_file_path  = "../Model_predictions" + '/' + args.material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + ".csv"

    # read the json file
    try:
        with open(json_file_path, 'r') as file:
            year = str(2021)
            kinetic_values           = json.load(file)
        return kinetic_values, csv_file_path
    except:
        year = str(2023)
        with open(json_file_path, 'r') as file:
            kinetic_values           = json.load(file)
        return kinetic_values, csv_file_path



def getvaluesfromjson(kinetic_values):
    n_reactions = kinetic_values['Kinetics']['Number of Reactions']
    A       = kinetic_values['Kinetics']['Pre-exponential']   # pre-exponential    , 1/s
    E       = kinetic_values['Kinetics']['Activation Energy']
    N_S     = kinetic_values['Kinetics']['Reaction Order']
    NU_MATL = kinetic_values['Kinetics']["Solid Yield"]
    fetched_kinetic_values = {"A":A,"E":E,"n_reactions":n_reactions,"N_S":N_S,"NU_MATL":NU_MATL}
    return fetched_kinetic_values



csv_file_path = openjson(args.material)[1]
# read the CSV file
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



 # activation energy  , J/mol


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
#T_0    = T_0  + 273.15;                         # initial temperature, K

# numerical parameters
N       = len(t_m)


                    
def analytical_solution(n_reactions,fetched_kinetic_values,alpha_0,beta,T_0,R,T_m,m_f,m_m,N):
    m_e_dict = {}
    for i in range(0,n_reactions):
        #create solution arrays
        t = np.linspace(0, t_f, N)
        
        try:
            A = (fetched_kinetic_values["A"])[i-1]
            E = int(fetched_kinetic_values["E"][i-1])
        except(TypeError):
            A = (fetched_kinetic_values["A"])
            E = int(fetched_kinetic_values["E"])
            
        C       = (1 - alpha_0) * np.exp( (A / beta) * T_0 * np.exp(-E / (R * T_0) ) + A * E / (beta * R) * expi( - E / (R * T_0) ) )
        alpha = np.zeros(N)
        for i2 in range(0,N):
#            alpha = np.zeros(N)

            alpha[i2] = 1 - C * np.exp(- (A / beta) * T_m[i2] * np.exp(- E / (R * T_m[i2])) - \
                                         (A / beta) * (E / R) * expi( - E / (R * T_m[i2]) ) )
#            print(alpha[i2])
        

        
        # convert alpha to masses
        m_e          = m_m[0] - (m_m[0] - m_f) * alpha
        m_e_dict[i] = m_e
    return m_e_dict
        
 
 
def plot_and_rms(m_e_dict,n_reactions,T_m,m_m):
    
    #plot model
    plt.plot(T_m, m_m, label  = 'Model Predictions', color = 'red', marker = '.')

    for i in range(0,n_reactions):
        m_e = m_e_dict[i]
        # root mean square error is calculated
        rms_err    = np.sqrt(np.sum( (m_m - m_e) ** 2) / N)
        print('root mean square error:', rms_err)
        
    # plot the analytical solution
        plt.plot(T_m, m_e, label  = 'Exact Solution'+ str(i))

        plt.xlabel(r'Temperature (K)', fontsize = 20)
        plt.ylabel(r'Mass (-)'       , fontsize = 20)
        plt.legend()
        plt.tight_layout()
    plt.show()


kinetic_values = openjson(args.material)[0]
csv_file_path = openjson(args.material)[0]

fetched_kinetic_values = getvaluesfromjson(kinetic_values)

n_reactions = int(fetched_kinetic_values["n_reactions"])

m_e_dict = analytical_solution(n_reactions,fetched_kinetic_values,alpha_0,beta,T_0,R,T_m,m_f,m_m,N)

plot_and_rms(m_e_dict,n_reactions,T_m,m_m)


def compare_all():
    material_list = [
        "MaCFP_PMMA_NIST",
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
    print(material_list)
    for material in material_list:
        subprocess.run(["python", dynamic_tga + ".py", args.material])






 # save as CSV
#with open('../results/' + args.material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "_results.csv", mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'alpha', 'Temperature'])
#    writer.writerow([   's',     '-',           'K'])
#    for i in range(len(t_m)):
#        writer.writerow([ t[i], alpha[i], T_m[i] ])
