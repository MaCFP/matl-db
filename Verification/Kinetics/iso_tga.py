"""

Script to generate exact solution for isothermal TGA

"""

import numpy as np
import matplotlib.pyplot as plt
import csv

# constant
R       = 8.134			    # gas constant, J/mol-K

#Kinetic parameters
A       = 4e12				# pre-exponential, 1/s 
E       = 2e5		        # activation energy, J/mol	

#scenario parameters
m_0     = 1					# initial mass
T       = 700				# constant temperature, K
t_f     = 1800				# final time, s

# numerical parameters
N       = 500				# number of data points

# create solution arrays
t       = np.linspace(0, t_f, N)
m       = np.zeros(N)

# calculate the mass at all times
for i in range(0, N):
    
    m[i] = m_0*np.exp( -A*np.exp( -E/(R*T) )*t[i])

# array of temperatures
T       = T*np.ones( N )

# plotting parameters
# If receiving tex/latex error try removing plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# Plot the results
plt.plot(t, m)
plt.xlabel(r'Time (s)', fontsize=20)
plt.ylabel(r'Mass (-)', fontsize=20)
plt.tight_layout()
plt.show()


#Save as CSV
#with open('iso_tga_data.csv', mode='w', newline='') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Time', 'Mass', 'Temperature'])
#    writer.writerow(['[s]', '[-]', 'K'])
#    for i in range(N):
#        writer.writerow([t[i], m[i], T[i]])

 


