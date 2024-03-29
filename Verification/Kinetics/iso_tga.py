"""
Script to generate exact solution for isothermal TGA
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

# ***replace with command line file specification
csv_file_path = 'iso_tga_data.csv'

# constant
R = 8.134  # gas constant, J/mol-K

# Kinetic parameters
A = 4e12    # pre-exponential, 1/s
E = 2e5     # activation energy, J/mol

# scenario parameters
m_0 = 1  # initial mass
T = 700  # constant temperature, K
#t_f = 1800  # final time, s

# Read the CSV file
data = pd.read_csv(csv_file_path)

# Extract Imported data and replace non-number values with NaN values
data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Mass'] = pd.to_numeric(data['Mass'], errors='coerce')
data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce')

# Drop NaN values
data = data.dropna()

# model predictions
t_m = data['Time'].values
m_m = data['Mass'].values
T_m = data['Temperature'].values

# numerical parameters
N = len(t_m)
#N = 500  # number of data points

# create solution arrays
#t = np.linspace(0, t_f, N)
m_e = np.zeros(N)



# calculate the mass at all times
for i in range(0, N):
    m_e[i] = m_0 * np.exp(-A * np.exp(-E / (R * T)) * t_m[i])

# plotting parameters
# If receiving tex/latex error try removing plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# Plot the Imported data
plt.plot(t_m, m_m, label='Model Predictions', color='red', marker='.')

# Plot the results
plt.plot(t_m, m_e, label='Exact Solution')

plt.xlabel(r'Time (s)', fontsize=20)
plt.ylabel(r'Mass (-)', fontsize=20)
plt.legend()
plt.tight_layout()
plt.show()

# Save as CSV
# with open('iso_tga_data.csv', mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'Mass', 'Temperature'])
#    writer.writerow(['[s]', '[-]', 'K'])
#    for i in range(N):
#        writer.writerow([t[i], m[i], T[i]])

# Sum of square errors are calculated directly
#sse_mass = np.sum((m_m - m_e) ** 2)
rms_err = np.sqrt(np.sum((m_m - m_e) ** 2)/N)
#print('Sum of squared errors for mass:', sse_mass)
print('Root Mean Square Error:', rms_err)
