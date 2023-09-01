import subprocess
import argparse
#import csv
import json
import os


# create the parser
parser = argparse.ArgumentParser()
# add an argument
parser.add_argument('experiment')
parser.add_argument('material')

# parse arguments
args = parser.parse_args()

material = 'MaCFP_PMMA_NIST'

year = str(2021)
json_file_path = '../../PMMA/Material_Properties/' + year + '/' + args.material + '.json'


# read the json file
try:
    with open(json_file_path, 'r') as file:
        year = str(2021)
        kdata           = json.load(file)
except:
    year = str(2023)
    with open(json_file_path, 'r') as file:
        kdata           = json.load(file)

A       = kdata['Kinetics']['Pre-exponential']   # pre-exponential    , 1/s
E       = kdata['Kinetics']['Activation Energy'] # activation energy  , J/mol




# Read fds script
with open('properties.txt', 'r') as file:
    file_lines = file.readlines()
# Write fds script
file_lines[6] = "      A(1) = " + str(A) + "\n"
file_lines[7] = "      E(1) = " + str(E) + "\n"

file_lines[20] = "      A(1) = " + str(A) + "\n"
file_lines[21] = "      E(1) = " + str(E) + "\n"
with open('properties.txt', 'w') as file:
    for line in file_lines:
        file.write(line)



os.system('cmd /c "fds_local NIST_TGA_10K.fds"')# NIST_TGA_10K.fds"')#NIST_TGA_10K$$$$




# run experiment
subprocess.run(["py", args.experiment + ".py",args.material])

#remove unnecesary fds files
try:
    os.remove("NIST_TGA_10K_cat_steps.csv")
    os.remove("NIST_TGA_10K_cat.binfo")
    os.remove("NIST_TGA_10K_cat.end")
    os.remove("NIST_TGA_10K_cat.out")
    os.remove("NIST_TGA_10K_cat.sinfo")
    os.remove("NIST_TGA_10K_cat.smv")
    os.remove("NIST_TGA_10K_cat_1_1.s3d")
    os.remove("NIST_TGA_10K_cat_1_2.s3d")
    os.remove("NIST_TGA_10K_cat_1_2.s3d.sz")
    os.remove("NIST_TGA_10K_cat_1_3.s3d")
    os.remove("NIST_TGA_10K_cat_1_3.s3d.sz")
    os.remove("NIST_TGA_10K_cat_git.txt")
    os.remove("NIST_TGA_10K_cat_hrr.csv")
    os.remove("NIST_TGA_10K_cat_cpu.csv")
    os.remove("NIST_TGA_10K_cat_1_1.s3d.sz")

    os.remove("NIST_TGA_10K_cat_devc.csv")

except:
    exc = 1