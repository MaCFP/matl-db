import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

plt.ion()

# =========================
# PARAMETRES
# =========================
N_interp = 200

# =========================
# LISTE DES CAS
# =========================
cases = [ "10K", "100K" ]

# =========================
# LISTE DES MODELES
# =========================
names = [ "CORIA",
          "UMD_FSRI",
          "NIST_StMU",
          "UCB-1",
          "UCB-2",
          "UCB-3" ]

# =========================
# STYLES
# =========================
name_plt_lines = {
    "CORIA": ['b','-'],
    "UMD_FSRI": ['lawngreen','-'],
    "NIST_StMU": ['purple','-'],
    "UCB-1": ['r','-'],
    "UCB-2": ['k','-'],
    "UCB-3": ['c','-'],
}

# =========================
# LABELS PROPRES
# =========================
name_labels = [
    "CORIA",
    "UMD FSRI",
    "NIST_StMU",

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
    plt.figure(figsize=(8,6))

    for name in names:

        file = name + '_Wood_TGA_N2_' + case + '.csv'

        try:
            # lecture robuste
            data = pd.read_csv(file, sep=None, engine='python')
          

            if name == "UMD_FSRI":
                T = data.iloc[:, 0].copy()
                t = data.iloc[:, 1].copy()
                data.iloc[:, 0] = t
                data.iloc[:, 1] = T


            data = data.iloc[:, :3]
            data = data.apply(pd.to_numeric, errors='coerce').dropna()

            if len(data) < 5:
                continue

            t = data.iloc[:,0].values
            T = data.iloc[:,1].values
            m = data.iloc[:,2].values

        except:
            print(f"❌ erreur fichier: {file}")
            continue

        # =====================
        # CALCUL MLR
        # =====================
        m_smooth = savgol_filter(m, 11, 2)
        dm_dt = np.gradient(m_smooth, t)
        mlr = -dm_dt
        mlr[mlr < 0] = 0

        # =====================
        # PEAK / ONSET
        # =====================
        idx_peak = np.argmax(mlr)

        peak = mlr[idx_peak]
        t_peak = t[idx_peak]
        T_peak = T[idx_peak]

        threshold = 0.05 * peak
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


    # =====================
    # FIGURE TEMPERATURE
    # =====================
    plt.figure(figsize=(8,6))

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
    plt.ylabel("MLR (g/s)", fontsize=16)
    plt.title(f"TGA - {case}/min", fontsize=20)
    plt.grid()

# =========================
# EXPORT RESULTATS
# =========================
df = pd.DataFrame(results)
df.to_excel("results_TGA.xlsx", index=False)

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
stats.to_excel("stats_par_case.xlsx", index=False)


print("✅ Analyse terminée")

plt.show()