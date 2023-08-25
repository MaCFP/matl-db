# script to plot gassification test data

import math
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

plt.ion()

# plotting parameters
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

dat =  np.loadtxt('../PMMA/Validation_Data/NIST_Gasification_Apparatus/Black-Copper_q50_Temp.csv', skiprows=2, delimiter=',')

t = dat[:,0]
T_back = dat[:,1]
Uc_back = dat[:,2]

# mean and standard deviation
plt.plot( t, T_back, ls='-', color='black')
plt.fill_between(t, T_back - Uc_back, T_back + Uc_back,color='black', alpha=0.2)

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"Back Surface Temperature (K)", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_Cu.pdf")

dat =  np.loadtxt('../PMMA/Validation_Data/NIST_Gasification_Apparatus/Black-Insulation_q50_Temp.csv', skiprows=2, delimiter=',')

t = dat[:,0]
T_back_572 = dat[:,1]
T_back_1144 = dat[:,2]
T_back_1716 = dat[:,3]
Uc_back_572 = dat[:,4]
Uc_back_1144 = dat[:,5]
Uc_back_1716 = dat[:,6]

plt.clf()

plt.plot( t, T_back_572, ls='-', color='black', label='5.72 mm')
plt.fill_between(t, T_back_572 - Uc_back_572, T_back_572 + Uc_back_572,color='black', alpha=0.2)

plt.plot( t, T_back_1144, ls='--', color='red', label='11.44 mm')
plt.fill_between(t, T_back_1144 - Uc_back_1144, T_back_1144 + Uc_back_1144,color='red', alpha=0.2)

plt.plot( t, T_back_1716, ls=':', color='blue', label='17.76 mm')
plt.fill_between(t, T_back_1716 - Uc_back_1716, T_back_1716 + Uc_back_1716,color='blue', alpha=0.2)

plt.legend(loc='lower right',title=r'Depth')

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"Temperature (K)", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_Ins.pdf")

dat1 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q25_Temp_R1.csv', skiprows=[1], delimiter=',')
dat2 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q25_Temp_R2.csv', skiprows=[1], delimiter=',')
dat3 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q25_Temp_R3.csv', skiprows=[1], delimiter=',')

plt.clf()
plt.plot(dat1['Time'],dat1['T_back_1'], ls='-', color='black', label='R1')
plt.plot(dat1['Time'],dat1['T_back_2'], ls='-.', color='black')
plt.plot(dat2['Time'],dat2['T_back_1'], ls='-', color='red', label='R2')
plt.plot(dat2['Time'],dat2['T_back_2'], ls='-.', color='red')
plt.plot(dat3['Time'],dat3['T_back_1'], ls='-', color='blue', label='R3')
plt.plot(dat3['Time'],dat3['T_back_2'],ls='-.', color='blue')

plt.legend(loc='lower right')

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"PMMA Backside Temperature (K)", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_25T.pdf")

dat1 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Mass_R3.csv', skiprows=[1], delimiter=',')
dat2 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Mass_R4.csv', skiprows=[1], delimiter=',')
dat3 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Mass_R5.csv', skiprows=[1], delimiter=',')

plt.clf()

plt.plot(dat1['Time'],dat1['Mass'], ls='-', color='black', label='R1')
plt.plot(dat2['Time'],dat2['Mass'], ls='-.', color='red', label='R2')
plt.plot(dat3['Time'],dat3['Mass'], ls=':', color='blue', label='R3')


plt.legend(loc='upper right')

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"Sample Mass (g)", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_50M.pdf")

dat1 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_MLR_R3.csv', skiprows=[1], delimiter=',')
dat2 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_MLR_R4.csv', skiprows=[1], delimiter=',')
dat3 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_MLR_R5.csv', skiprows=[1], delimiter=',')

plt.clf()

plt.plot(dat1['Time'],dat1['MLR'], ls='-', color='black', label='R1')
plt.plot(dat2['Time'],dat2['MLR'], ls='-.', color='red', label='R2')
plt.plot(dat3['Time'],dat3['MLR'], ls=':', color='blue', label='R3')


plt.legend(loc='upper right')

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"Mass Loss Rate (g/(m$^2$~s))", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_50MLR.pdf")

dat1 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Temp_R1.csv', skiprows=[1], delimiter=',')
dat2 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Temp_R2.csv', skiprows=[1], delimiter=',')
dat3 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Temp_R3.csv', skiprows=[1], delimiter=',')
dat4 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Temp_R4.csv', skiprows=[1], delimiter=',')
dat5 = pd.read_csv('../PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_Gasification_q50_Temp_R5.csv', skiprows=[1], delimiter=',')

plt.clf()
plt.plot(dat1['Time'],dat1['T_back_1'], ls='-', color='black', label='R1')
plt.plot(dat1['Time'],dat1['T_back_2'], ls='-.', color='black')
plt.plot(dat1['Time'],dat1['T_back_3'], ls=':', color='black')
plt.plot(dat2['Time'],dat2['T_back_1'], ls='-', color='red', label='R2')
plt.plot(dat2['Time'],dat2['T_back_2'], ls='-.', color='red')
plt.plot(dat2['Time'],dat2['T_back_3'], ls=':', color='red')
plt.plot(dat3['Time'],dat3['T_back_1'], ls='-', color='blue', label='R3')
plt.plot(dat3['Time'],dat3['T_back_2'], ls='-.', color='blue')
plt.plot(dat3['Time'],dat3['T_back_3'], ls=':', color='blue')
plt.plot(dat4['Time'],dat4['T_back_1'], ls='-', color='green', label='R4')
plt.plot(dat4['Time'],dat4['T_back_2'], ls='-.', color='green')
plt.plot(dat5['Time'],dat5['T_back_1'], ls='-', color='purple', label='R5')
plt.plot(dat5['Time'],dat5['T_back_2'], ls='-.', color='purple')

plt.legend(loc='lower right')

plt.xlabel(r"Time (s)", fontsize=20)
plt.ylabel(r"PMMA Backside Temperature (K)", fontsize=20)
plt.tight_layout()
plt.savefig("../PMMA/Validation_Data/NIST_Gasification_Apparatus/NIST_Gasification_Apparatus_50T.pdf")