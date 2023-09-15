import subprocess
import argparse
import json
import os

# create the parser
parser = argparse.ArgumentParser()
# add an argument
parser.add_argument('experiment')
parser.add_argument('material')
# parse arguments
args = parser.parse_args()

subprocess.run(["python", args.experiment + ".py", args.material])


# remove results.csv file
#try:
#    os.remove('../results/' + args.material + "_" + "dynamic_TGA_10K" + "_" + "FDS" + "_results.csv")
#except(FileNotFoundError):
#    pass