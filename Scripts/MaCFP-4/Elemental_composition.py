import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

#region Save plots as pdf or png
ex = 'pdf' #options 'pdf' or 'png

# TO DO: when prelim document pushed to main repo replace
'../../../matl-db-organizing-committee/' #with
'../../Documents/'

#region create subdirectories to save plots. 
base_dir = Path('../../../matl-db-organizing-committee/SCRIPT_FIGURES')
Composition_dir = base_dir / 'Composition'
Composition_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------
#region data
# ------------------------------------
species = ['C', 'H', 'N', 'S', 'O']
virgin = [48.9, 6.1, 0, 0, 40.7]
char = [91.2, 2.8, 0, 0, 3.7]
pyrolyzate = [22.3, 8.6, 0, 0, 63.9]



# ------------------------------------
#region figure
# ------------------------------------
fig, ax = plt.subplots(figsize=(5, 3))

# Set width of bars and positions
bar_width = 0.25
x = np.arange(len(species))

# Create bars
bars1 = ax.bar(x - bar_width, virgin, bar_width, label='Virgin', color='#FFA500')
bars2 = ax.bar(x, char, bar_width, label='Char', color='#000000')
bars3 = ax.bar(x + bar_width, pyrolyzate, bar_width, label='Pyrolyzate', color='#1E90FF')

# Add value labels on top of bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10)

add_labels(bars1)
add_labels(bars2)
add_labels(bars3)

# Customize the plot
ax.set_ylabel('wt (%)', fontsize=11)
ax.set_xlabel('Species', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(species)
ax.set_ylim(0, 100)
ax.legend(frameon=True)

# Add grid for better readability
ax.yaxis.grid(True, linestyle='-', linewidth=0.5, color='gray', alpha=0.3)
ax.set_axisbelow(True)

# Adjust layout
plt.tight_layout()

# Save as PDF
plt.savefig(str(base_dir) + '/Composition/Elemental_Composition.{}'.format(ex), format='pdf', bbox_inches='tight')
