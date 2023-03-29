import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expi
import csv

# Variables
C = 1.0
A = 10.0
B = 100.0
E = 10000.0
R = 8.314
T0 = 600


alist = []
T = []
tlist = []

#slope of Temperature function
m = 10
#Temperature function
t = 0
while len(T)<100:
    Temp = m*t + T0
    T.append(Temp)
    tlist.append(t)   
    t+=1
print(T)


#Equation
i = 0
while i<100:
    a = 1 - C*np.exp(-(A/B)*T[i]*np.exp((-E)/(R*T[i]))-(A/B)*(E/R)*expi((-E)/(R*T[i])))
    alist.append(a)
    i+=1


# Plot the results
plt.plot(alist, T,)
plt.xlabel('Temperature (K)')
plt.ylabel('a')
plt.title('a vs T')
plt.show()

#Save as CSV
with open('Equation_33_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time', 'a', 'Temperature'])
    writer.writerow(['s', 'a', 'K'])
    for i in range(len(T)):
        writer.writerow([tlist[i], alist[i], T[i]])
