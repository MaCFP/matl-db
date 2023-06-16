"""
Script to generate exact solution for constant heating rate TGA
using the solution from Coheur et al., J Mater Sci, 2021
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expi
import csv
import pandas as pd
import json


json_file_path = 'MaCFP_PMMA_NIST.json'

# ***replace with command line file specification
csv_file_path = 'NIST_TGA_10K_cat_devc.csv'


with open(json_file_path, 'r') as file:
    data = json.load(file)
    A = data['Kinetics']['Pre-exponential']
    E = data['Kinetics']['Activation Energy']


# Read the CSV file
data = pd.read_csv(csv_file_path)
print(data.columns)
# Extract Imported data and replace non-number values with NaN values
data['Time'] = pd.to_numeric(data['s'], errors='coerce')
data['Mass'] = pd.to_numeric(data['[mg]'], errors='coerce')
data['Temperature'] = pd.to_numeric(data['[K]'], errors='coerce')
data['Heat Flow'] = pd.to_numeric(data['[W/g]'], errors='coerce')

# Drop NaN values
data = data.dropna()

# model predictions 
t_m = data['Time'].values
m_m = data['Mass'].values
T_m = data['Temperature'].values
beta_m = data['Heat Flow'].values


# constant
R       = 8.314             # gas constant, J/mol-K

# kinetic parameters
#A       = 2.85e13              # pre-exponential, 1/s
#E       = 1.91e5           # activation energy, J/mol
m_f     = m_m[-1]                 # final mass

# scenario parameters
#m_0     = 1                 # initial mass
T_0     = T_m[0]                # initial temperature, C
beta    = 10                # heating rate, K/min
t_f     = t_m[-1]              # final time, s



# unit conversions
beta    = beta/60;          # heating rate, K/s
#T_0     = T_0 + 273.15;     # initial temperature, K
alpha_0 = 0                 # initial progress factor







# numerical parameters
N = len(t_m)


# create solution arrays
t       = np.linspace(0, t_f, N)
#T       = T_0 + beta[i]*t
alpha   = np.zeros( N )


# compute C constant
C = (1 - alpha_0)*np.exp( (A/beta)*T_0*np.exp(-E/(R*T_0)) + \
            A*E/(beta*R)*expi(-E/(R*T_0)))


# calculate progress factors at all times
for i in range(0, N):

    alpha[i] = 1 - C*np.exp(-(A/beta)*T_m[i]*np.exp(-E/(R*T_m[i])) - \
                (A/beta)*(E/R)*expi(-E/(R*T_m[i])))

# convert alpha to masses
m_e       = m_m[0] - (m_m[0] - m_f)*alpha

# plotting parameters
#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')
#plt.rc('lines', linewidth=1.5)
#plt.rc('xtick', labelsize=18)
#plt.rc('ytick', labelsize=18)




# Plot the Imported data
plt.plot(T_m, m_m, label='Model Predictions', color='red', marker='.')

# Plot the results
plt.plot(T_m, m_e, label='Exact Solution')

plt.xlabel(r'Temperature (K)', fontsize=20)
plt.ylabel(r'Mass (-)', fontsize=20)
plt.legend()
plt.tight_layout()
plt.show()


##Save as CSV
#with open('Equation_33_data.csv', mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'a', 'Temperature'])
#    writer.writerow(['s', 'a', 'K'])
#    for i in range(len(T)):
#        writer.writerow([tlist[i], alist[i], T[i]])

# Sum of square errors are calculated directly
#sse_mass = np.sum((m_m - m_e) ** 2)
rms_err = np.sqrt(np.sum((m_m - m_e) ** 2)/N)
#print('Sum of squared errors for mass:', sse_mass)
print('Root Mean Square Error:', rms_err)
