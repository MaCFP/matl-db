"""

Master script to run verification cases

"""

import subprocess
import argparse
import json
import numpy as np
import matplotlib.pyplot as     plt

# create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--compare_all', "-c", action = "store_true")
parser.add_argument('--generate_all_fds', "-g", action = "store_true")
# add an argument
#parser.add_argument('scenario')     # scenario to be considered
#parser.add_argument('matl_set')     # material property set to be validated

# parse arguments
args = parser.parse_args()

matl_set_list = [
        "MaCFP_PMMA_NIST",
        "MaCFP_PMMA_Aalto_I",
        "MaCFP_PMMA_BUW-FZJ_A",
        "MaCFP_PMMA_BUW-FZJ_B",
        "MaCFP_PMMA_DBI_1",
        "MaCFP_PMMA_DBI_2",
        "MaCFP_PMMA_DBI_3",
        "MaCFP_PMMA_DBI_4",
        "MaCFP_PMMA_GIDAZE+",
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

if args.compare_all is True or args.generate_all_fds is True:
    error_list = []
    if args.compare_all is True:
        for matl_set in matl_set_list:
            try:
                subprocess.run(["python", "dynamic_tga" + ".py", str(matl_set), str(2021),"-co"])
            except:
                pass
    if args.generate_all_fds is True:
        for matl_set in matl_set_list:
            try:
                subprocess.run(["python","testing"+".py",str(matl_set)])
            except:
                pass
            
with open('comparison_data.json','r') as file:
            data = json.load(file)
#print(data)
#RMSE = data["A"]
#A = data["A"]
#E = data["E"]

A = np.zeros(len(data))
E = np.zeros(len(data))
RMSE = np.zeros(len(data))

#for i in range(0,len(matl_set_list)):
#    try:
#        matl = matl_set_list[i]
#        A[i] = data[matl]['A']
#        E[i] = data[matl]['E']
#        RMSE[i] = data[matl]['RMSE']
#        print(A[i],RMSE[i])
#    except:
#        pass
#plt.plot(A,E)
#plt.scatter(E,RMSE, label        = 'Model Predictions', color = 'red', marker = '.')
#plt.plot(E, RMSE, label        = 'Model Predictions', color = 'blue', marker = '.')
#plt.show()

