"""
Script to generate exact solution for constant heating rate TGA
using the solution from Coheur et al., J Mater Sci, 2021
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expi
import csv

# constant
R       = 8.314             # gas constant, J/mol-K

# kinetic parameters
A       = 10e2              # pre-exponential, 1/s
E       = 50000.0           # activation energy, J/mol
m_f     = 0                 # final mass

# scenario parameters
m_0     = 1                 # initial mass
T_0     = 20                # initial temperature, C
beta    = 10                # heating rate, K/min
t_f     = 1800              # final time, s

# numerical parameters
N       = 500               # number of data points

# unit conversions
beta    = beta/60;          # heating rate, K/s
T_0     = T_0 + 273.15;     # initial temperature, K
alpha_0 = 0                 # initial progress factor

# compute C constant
C = (1 - alpha_0)*np.exp( (A/beta)*T_0*np.exp(-E/(R*T_0)) + \
            A*E/(beta*R)*expi(-E/(R*T_0)))

# create solution arrays
t       = np.linspace(0, t_f, N)
T       = T_0 + beta*t
alpha   = np.zeros( N )

# calculate progress factors at all times
for i in range(0, N):

    alpha[i] = 1 - C*np.exp(-(A/beta)*T[i]*np.exp(-E/(R*T[i])) - \
                (A/beta)*(E/R)*expi(-E/(R*T[i])))

# convert alpha to masses
m       = m_0 - (m_0 - m_f)*alpha

# plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# Plot the results
plt.plot(T, m)
plt.xlabel(r'Temperature (K)', fontsize=20)
plt.ylabel(r'Mass (-)', fontsize=20)
plt.tight_layout()
#plt.title('a vs T')
plt.show()
#
##Save as CSV
#with open('Equation_33_data.csv', mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'a', 'Temperature'])
#    writer.writerow(['s', 'a', 'K'])
#    for i in range(len(T)):
#        writer.writerow([tlist[i], alist[i], T[i]])
