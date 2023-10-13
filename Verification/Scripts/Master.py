"""

Master script to run verification cases

"""

import subprocess
import argparse

# create the parser
parser = argparse.ArgumentParser()

# add an argument
parser.add_argument('scenario')     # scenario to be considered
parser.add_argument('matl_set')     # material property set to be validated

# parse arguments
args = parser.parse_args()

# running exact solution of scenario
subprocess.run(["python", args.scenario + ".py", args.matl_set])

           
