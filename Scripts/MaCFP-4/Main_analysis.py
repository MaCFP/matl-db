"""

Main script
This script will run all plotting scripts, needed to generate all images for the MaCFP-4 experimental results summary.

"""
# Main_analysis.py
import subprocess

scripts = [
    'TGA_analysis.py',
    'DSC_analysis.py',
    'MCC_analysis.py',
    'Cone_analysis.py'
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(['python', script], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {script} completed successfully\n")
    else:
        print(f"✗ {script} failed with error:")
        print(result.stderr)
