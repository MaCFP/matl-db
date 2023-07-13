"""
Script to generate exact solution for isothermal TGA
"""

import csv
import json
import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd


json_file_path = '../../PMMA/Material_Properties/2021/MaCFP_PMMA_NIST.json'


# ***replace with command line file specification
csv_file_path  = 'iso_tga_data.csv'


# read the json file
with open(json_file_path, 'r') as file:
    kdata            = json.load(file)


# read the CSV file
data                = pd.read_csv(csv_file_path)


# extract imported data from CSV and replace non-number values with NaN values
data['Time']        = pd.to_numeric(data['Time']       , errors = 'coerce')
data['Mass']        = pd.to_numeric(data['Mass']       , errors = 'coerce')
data['Temperature'] = pd.to_numeric(data['Temperature'], errors = 'coerce')

# drop NaN values
data                = data.dropna()


# model predictions
t_m  = data['Time'].values
m_m  = data['Mass'] .values
T_m  = data['Temperature'].values


# kinetic parameters
A    = kdata['Kinetics']['Pre-exponential']   # pre-exponential     , 1/s
E    = kdata['Kinetics']['Activation Energy'] # activation energy   , J/mol

# constants
R    = 8.134                                  # gas constant        , J/mol-K

# scenario parameters
m_0  = 1                                      # initial mass
T    = 700                                    # constant temperature, K
#t_f = 1800                                   # final time          , s

# numerical parameters
N    = len(t_m)

# create solution arrays
m_e  = np.zeros(N)


# calculate the mass at all times
for i in range(0, N):
    m_e[i] = m_0 * np.exp( - A * np.exp( - E / (R * T)) * t_m[i])


# plotting parameters
plt.rc('text' , usetex    = True)
plt.rc('font' , family    = 'serif')
plt.rc('lines', linewidth = 1.5)
plt.rc('xtick', labelsize = 18)
plt.rc('ytick', labelsize = 18)

# Plot the Imported data
plt.plot(t_m, m_m, label  = 'Model Predictions', color = 'red', marker = '.')

# plot the results
plt.plot(t_m, m_e, label  = 'Exact Solution')
plt.xlabel(r'Time (s)', fontsize = 20)
plt.ylabel(r'Mass (-)', fontsize = 20)
plt.legend()
plt.tight_layout()
plt.show()


 # save as CSV
#with open('iso_tga_data.csv', mode = 'w', newline = '') as file:
#    writer = csv.writer(file, delimiter = ', ', quotechar='"', quoting = csv.QUOTE_MINIMAL)
#    writer.writerow(['Time' , 'Mass', 'Temperature'])
#    writer.writerow(['[s]'  , '[-]' , 'K'])
#    for i in range(N):
#        writer.writerow([t_m[i], m_e[i], T])


#calculates root mean square error
rms_err = np.sqrt(np.sum( (m_m - m_e) ** 2) / N)
print('root mean square error:', rms_err)
