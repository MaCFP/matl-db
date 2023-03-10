import numpy as np
import matplotlib.pyplot as plt
import csv
 
#1.  Stops while condition when mass gets sufficiently close to 0
#2.  Temperature function allows dynamic temperature
#3.  Creates CSV file


# Variables = (1/2/3) refers to different sets of variables
variables = 3
seconds = 60
mtlist = []
tlist = []
 
 
if variables == 1:
    m0 = 1
    A = 1e12
    E = 3e5
    R = 8.314
    T0 = 600
   
if variables == 2:
    m0 = 1e-6
    A = 1e3
    E = 3e4
    R = 8.314
    T0 = 600
 
 
#Double T
if variables == 3:
    m0 = 5
    A = 1e12
    E = 3e5
    R = 8.314
    T0 = 1200
 
int(seconds)
 
 

t = 0
mt = 1
 
def logging(mt,t):
#    while t < seconds:
# while mt >= 1e-8 stops while condition when mt is very close to 0
    while mt >= .01:
        # Input Temperature function here
        T = T0 + (t * 1)
       
        mt = m0 * np.exp(-A * np.exp(-E / (R * T)) * t)
        mtlist.append(mt)
        tlist.append(t)
        #print(mt,t)
        t += 1
 
 
 
 
logging(mt,t)
 
#Graph
plt.plot(tlist, mtlist)
plt.grid()
plt.xlabel('Time (s)')
plt.ylabel('Mass (kg)')
plt.title('Mass vs Time')
plt.show()
 
#Save as CSV
with open('iso_tga.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time', 'Mass'])
    writer.writerow(['[s]','[-]'])
    for i in range(len(mtlist)):
        writer.writerow([tlist[i], mtlist[i]])
