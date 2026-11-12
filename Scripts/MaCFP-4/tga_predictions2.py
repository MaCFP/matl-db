import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

plt.ion()

# =========================
# PARAMETRES
# =========================
N_interp = 1401

# =========================
# CHEMIN VERS LES DONNEES
# =========================
# Script location: ...\Github\matl-db\Scripts\MaCFP-4\tga_predictions.py
# Data location:   ...\Github\matl-db\Wood\Calibration_Data\InstitutionName\
#
# We build the data path relative to this script's location so it works
# regardless of which machine / working directory it's run from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "Wood", "Calibration_Results")
)
SCRIPT_FIGS = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "Documents", "SCRIPT_FIGURES","MODELING")
)

# =========================
# LISTE DES CAS
# =========================
cases = [ "10K", "100K" ]

# =========================
# LISTE DES MODELES
# =========================
# Note : le nom du dossier institution ne correspond pas toujours
# exactement au nom du modele. Par exemple, "UCB-1", "UCB-2", "UCB-3"
# sont tous des fichiers situes dans le MEME dossier "UCB" (pas un
# dossier par variante). On retire donc le suffixe "-N" pour retrouver
# le nom du dossier correspondant.
names = [ "CORIA",
          "UMD-FSRI",
          "NIST-StMU",
          "UCB-1",
          "UCB-2",
          "UCB-3" ]

def get_institution_folder(name):
    """Deduit le nom du dossier institution a partir du nom de modele.
    Ex: 'UCB-1' -> 'UCB', 'CORIA' -> 'CORIA'
    """
    if 'UCB' in name:
        return 'UCB'
    return name

# =========================
# STYLES
# =========================
name_plt_lines = {
    "CORIA": ['b','-'],
    "UMD-FSRI": ['k','-'],
    "NIST-StMU": ['g','-'],
    "UCB-1": ['firebrick','-'],
    "UCB-2": ['r','--'],
    "UCB-3": ['darkorange','-.'],
}

# =========================
# LABELS PROPRES
# =========================
name_labels = [
    "CORIA",
    "UMD-FSRI",
    "NIST-StMU",

    "UCB-1",
    "UCB-2",
    "UCB-3",
]

# =========================
# STOCKAGE GLOBAL
# =========================
results = []

# =========================
# BOUCLE PRINCIPALE
# =========================
for case in cases:

    mlr_all_t = []
    mlr_all_T = []

    peak_list = []
    tpeak_list = []
    Tonset_list = []

    # =====================
    # FIGURE TEMPS
    # =====================
    fig_t=plt.figure(figsize=(8,6))

    for name in names:

        filename = name + '_Wood_TGA_N2_' + case + '.csv'
        folder = get_institution_folder(name)
        file = os.path.join(DATA_ROOT, folder, filename)
        

        if not os.path.isfile(file):
            filename = name + '_Wood_STA_N2_' + case + '.csv'
            folder = get_institution_folder(name)
            file = os.path.join(DATA_ROOT, folder, filename)
            # continue

        if not os.path.isfile(file):
            print(f"⚠️  fichier absent, on saute : {file}")
            continue

        try:
            # lecture robuste
            data = pd.read_csv(file, sep=None, engine='python')

            data.columns = data.columns.str.strip()  # Safe cleanup for hidden spaces
            print(file)
            # Select, convert to numeric, and drop bad rows all at once
            data = data[['Time (s)', 'Temperature (K)', 'Mass (mg)']].apply(pd.to_numeric, errors='coerce').dropna()
            
            # if len(data) < 5:
            #     continue
                
            # Direct access!
            t = data['Time (s)'].values
            T = data['Temperature (K)'].values
            m = data['Mass (mg)'].values
            print(m)
        except Exception as e:
            print(f"❌ erreur fichier: {file} ({e})")
            continue

        # =====================
        # CALCULATE MLR
        # =====================
        m_smooth = savgol_filter(m, 41, 3)
        dm_dt = np.gradient(m_smooth, t)/ np.mean(m[0:4])
        mlr = -dm_dt
        mlr[mlr < 0] = 0

        # =====================
        # PEAK / ONSET
        # =====================
        idx_peak = np.argmax(mlr)

        peak = mlr[idx_peak]
        t_peak = t[idx_peak]
        T_peak = T[idx_peak]
        # print(filename)
        # print(peak)
        threshold = 0.10 * peak # define onset temperature of ML as 10% of peak MLR (to match exp. report)
        onset_idx = np.where(mlr > threshold)[0]

        if len(onset_idx) > 0:
            t_onset = t[onset_idx[0]]
            T_onset = T[onset_idx[0]]
        else:
            t_onset = np.nan
            T_onset = np.nan

        peak_list.append(peak)
        tpeak_list.append(t_peak)
        Tonset_list.append(t_onset)

        # =====================
        # INTERPOLATION
        # =====================
        t_common = np.linspace(t.min(), t.max(), N_interp)
        T_common = np.linspace(T.min(), T.max(), N_interp)

        mlr_interp_t = np.interp(t_common, t, mlr)
        mlr_interp_T = np.interp(T_common, T, mlr)

        mlr_all_t.append(mlr_interp_t)
        mlr_all_T.append(mlr_interp_T)

        # =====================
        # STYLE
        # =====================
        color, linestyle = name_plt_lines.get(name, ['k','-'])

        plt.plot(t_common, mlr_interp_t,
                 color=color,
                 linestyle=linestyle,
                 linewidth=1.5,
                 label=name)

        # =====================
        # STOCKAGE RESULTATS
        # =====================
        results.append({
            "case": case,
            "model": name,
            "peak_mlr": peak,
            "t_peak": t_peak,
            "T_peak": T_peak,
            "t_onset": t_onset,
            "T_onset": T_onset
        })

    # =====================
    # MOYENNE
    # =====================
    mlr_all_t = np.array(mlr_all_t)

    if len(mlr_all_t) > 0:
        mean = np.mean(mlr_all_t, axis=0)
        std = np.std(mlr_all_t, axis=0)

        plt.plot(t_common, mean, 'k', linewidth=3, label="Mean")

        plt.fill_between(t_common,
                         mean - std,
                         mean + std,
                         color='k', alpha=0.2,
                         label="Std")

    # =====================
    # LEGENDES PROPRES
    # =====================
    handles, labels = plt.gca().get_legend_handles_labels()

    new_labels = []
    for lab in labels:
        if lab in names:
            idx = names.index(lab)
            new_labels.append(name_labels[idx])
        else:
            new_labels.append(lab)

    plt.legend(handles, new_labels, fontsize=8, ncol=2)

    plt.xlabel("Time (s)")
    plt.ylabel("MLR (g/s)")
    plt.title(f"MLR vs Time - {case}")
    plt.grid()
    plt.close(fig_t)


    # =====================
    # FIGURE TEMPERATURE
    # =====================
    fig_T=plt.figure(figsize=(8,6))

    mlr_all_T = np.array(mlr_all_T)

    for i, name in enumerate(names):
        if i >= len(mlr_all_T):
            continue

        color, linestyle = name_plt_lines.get(name, ['k','-'])

        plt.plot(T_common, mlr_all_T[i],
                 color=color,
                 linestyle=linestyle,
                 linewidth=1.5,
                 label=name)

    if len(mlr_all_T) > 0:
        mean_T = np.mean(mlr_all_T, axis=0)
        std_T = np.std(mlr_all_T, axis=0)

        plt.plot(T_common, mean_T, 'k', marker='o', linewidth=3, label="Mean")

        plt.fill_between(T_common,
                         mean_T - std_T,
                         mean_T + std_T,
                         color='k', alpha=0.2,
                         label="Std")

    handles, labels = plt.gca().get_legend_handles_labels()

    new_labels = []
    for lab in labels:
        if lab in names:
            idx = names.index(lab)
            new_labels.append(name_labels[idx])
        else:
            new_labels.append(lab)

    plt.legend(handles, new_labels, fontsize=16, ncol=1)

    plt.xlabel("Temperature (K)", fontsize=16)
    plt.ylabel("MLR (1/s)", fontsize=16)
    plt.title(f"TGA - {case}/min", fontsize=20)
    plt.grid()

    plt.tight_layout()
    os.makedirs(os.path.join(str(SCRIPT_FIGS), 'TGA'), exist_ok=True)
    fig_T.savefig(os.path.join(str(SCRIPT_FIGS), 'TGA',f'TGA_MLR_Predicted_{case}.pdf'))
    plt.close(fig_T)



# =========================
# EXPORT RESULTATS
# =========================
df = pd.DataFrame(results)
df.to_csv(os.path.join(str(SCRIPT_FIGS), 'TGA',f"TGA_Key-Features.csv"), index=False)
df = pd.DataFrame(results)

stats = df.groupby("case").agg({
    "peak_mlr": ["mean", "std"],
    "T_peak": ["mean", "std"],
    "T_onset": ["mean", "std"]
})

stats.columns = [
    "peak_mlr_mean", "peak_mlr_std",
    "T_peak_mean", "T_peak_std",
    "T_onset_mean", "T_onset_std"
]

stats = stats.reset_index()

# export
df.to_csv(os.path.join(str(SCRIPT_FIGS), 'TGA',f"TGA_stats.csv"), index=False)

print("✅ Analyse terminée")

#plt.show()
plt.show(block=True)


