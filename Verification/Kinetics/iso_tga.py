"""
Script to generate exact solution for isothermal TGA
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

csv_file_path = 'iso_tga_data.csv'

# constant
R = 8.134  # gas constant, J/mol-K

# Kinetic parameters
A = 4e12  # pre-exponential, 1/s
E = 2e5  # activation energy, J/mol

# scenario parameters
m_0 = 1  # initial mass
T = 700  # constant temperature, K
t_f = 1800  # final time, s

# numerical parameters
N = 500  # number of data points

# create solution arrays
t = np.linspace(0, t_f, N)
m = np.zeros(N)

# Read the CSV file
data = pd.read_csv(csv_file_path)

# Extract Imported data and replace non-number values with NaN values
data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Mass'] = pd.to_numeric(data['Mass'], errors='coerce')
data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce')

# Drop NaN values
data = data.dropna()

# imported values
t_imported = data['Time'].values
m_imported = data['Mass'].values
T_imported = data['Temperature'].values

# calculate the mass at all times
for i in range(0, N):
    m[i] = m_0 * np.exp(-A * np.exp(-E / (R * T)) * t[i])

# plotting parameters
# If receiving tex/latex error try removing plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# Plot the Imported data
plt.plot(t_imported, m_imported, label='Imported data', color='red', marker='.')

# Plot the results
plt.plot(t, m, label='Calculated data')

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

# Checks if number of rows (and therefore data points) are equal
if len(data) == m.shape[0]:

    # Sum of square errors are calculated directly
    sse_mass = np.sum((m_imported - m) ** 2)
    print('Sum of squared errors for mass:', sse_mass)

    sse_Temperature = np.sum((T_imported - T) ** 2)
    print('Sum of squared errors for Temperature:', sse_mass)


else:

    # values are interpolated before calculating sum of square errors
    m_interp = np.interp(t_imported, t, m)
    sse = np.sum((m_imported - m_interp) ** 2)
    print('Sum of square errors for mass:', sse)

    T_interp = np.interp(t_imported, t, T)
    sse = np.sum((T_imported - T_interp) ** 2)
    print('Sum of square errors:', sse)

