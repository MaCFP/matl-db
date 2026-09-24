# Aalto – Wood dataset submission (STA: TGA/DSC. Cone Calorimetry / Gasification)

## Overview
At Aalto University, thermogravimetric analysis (TGA) measurements were performed using a simultaneous thermal analyzer (STA). The instrument also provides DSC signals; however, DSC data are not presented here since they are **supplementary only** and were not collected using a separate dedicated DSC instrument. Therefore, DSC signals should **not** be used as primary calibration targets unless explicitly agreed.

In addition, cone calorimeter tests were performed under **air** (flaming combustion) and under **nitrogen** (reported here as **gasification**, i.e., inert atmosphere).

---

## Experimental conditions (TGA/DSC)
### Heating rate(s)
- 5, 10, and 20 K/min

### Temperature program (temperatures in K)
- Initial stabilization about 1200 s (drying stage): 313 K (isothermal hold)
- Heating ramp: from 313 K up to 1073 K
- Final isotherm: 60 s hold at 1073 K
- Note: the stabilization step effectively acted as a drying stage; therefore, the exact initial moisture content is uncertain.

### Sample
- Material / geometry: wood (sawdust chips)
- Initial sample mass: see the **Test list** table below (reported per run).
- Note: lower sample masses were not feasible due to instrument limitations.

### Crucible
- Material: Al₂O₃ (alumina)
- Volume: 85 µL
- Lid: none

### Carrier gas
- Type: Nitrogen (N₂)
- Flow rate: 70 mL/min

## Calibration and instrument setup
A baseline (blank) measurement was performed using an **empty Al₂O₃ (alumina) crucible** under the same gas conditions and for each heating-rate condition used in this dataset (5, 10, and 20 K/min). Temperature/heat-flow calibration was carried out according to the laboratory routine using **metal reference standards** (e.g., In, Bi, Zn, Al, Ag) spanning relevant melting temperatures. Calibration checks are performed **periodically as part of routine instrument maintenance** and were verified prior to the measurement campaign; baseline/blank measurements were repeated as needed when the setup was changed (e.g., crucible handling, gas line configuration, or after extended downtime). The exact calibration sequence and frequency may differ from the template repository example, but the same general approach (blank baseline + periodic temperature/heat-flow calibration with standards) was followed.

## Instrument
- STA: NETZSCH STA 449 F3 Jupiter
- Evolved gas analysis: NETZSCH QMS 403 Aeolos Quadro (coupled)
- Furnace type / material: Steel

## STA test list
| Test name | O2 (vol-%) | Initial sample mass (mg) |
|---|---:|---:|
| Aalto_Wood_STA_N2_5K_R1  | 0 | 8.8730 |
| Aalto_Wood_STA_N2_10K_R1 | 0 | 7.4270 |
| Aalto_Wood_STA_N2_20K_R1 | 0 | 8.3625 |
| Aalto_Wood_STA_N2_5K_R2  | 0 | 8.7090 |
| Aalto_Wood_STA_N2_10K_R2 | 0 | 8.0765 |
| Aalto_Wood_STA_N2_20K_R2 | 0 | 8.2330 |
| Aalto_Wood_STA_N2_5K_R3  | 0 | 8.7710 |
| Aalto_Wood_STA_N2_10K_R3 | 0 | 8.0540 |
| Aalto_Wood_STA_N2_20K_R3 | 0 | 7.9190 |

## Notes (STA)
- Moisture content prior to the ramp is uncertain because the stabilization hold acted as a drying step.

---

## Cone calorimeter conditions (Wood) and gasification datasets

### Naming convention used in this submission
- **Cone tests in air:** filenames use `..._Cone_...` and **do not include "Air"** in the name.
- **Cone tests in nitrogen:** filenames use `..._Gasification_...` (requested naming for inert/gasification conditions).

### Data formatting notes (cone/gasification)
- All cone and gasification time-series data are reported at **1 s intervals**.
- For **gasification datasets** (cone under N₂), the **HRR column is not included**.

### Test program summary
Tests were performed following **ISO 5660-1** (with a minor sample-holder modification noted below). Tests include:
- **Parallel to grain**:
  - Cone in air at **30, 45, 60 kW/m²**, each with **3 repeats**
  - Gasification (N₂) at **30, 45, 60 kW/m²**, each with **3 repeats**
- **Perpendicular to grain**:
  - Gasification (N₂) at **30, 45, 60 kW/m²**, each with **3 repeats**
Total cone/gasification tests: **27**

### Key settings
- **Radiant heat flux (incident):** 30, 45, 60 kW/m²
- **Heater temperature (setpoint):**
  - 30 kW/m²: ~565 °C (cone in air, parallel), ~555 °C (gasification, parallel & perpendicular)
  - 45 kW/m²: ~650 °C (cone in air, parallel), ~640 °C (gasification, parallel & perpendicular)
  - 60 kW/m²: ~730 °C (cone in air, parallel), ~715 °C (gasification, parallel & perpendicular)  
  *Note: these temperatures refer to the cone heater setpoint associated with the target heat flux.*
- **Exhaust/extraction flow rate:** 24 L/s
- **Sample orientation:** horizontal
- **Ignition:** spark ignitor
- **Sample holder geometry / characteristics:**
  - Square pan otherwise complying with ISO 5660-1 specifications, **except** for a **1 cm hole drilled in a corner next to the handle** to allow passage of thermocouples below the sample.
  - Retainer frame: **no**
  - Grid: **no**
- **Backing insulation:** two layers of ceramic wool (each ~1 cm thick), density **65 kg/m³** as specified in ISO 5660-1; other thermal properties are unknown.
- **Calibration standard:** ISO 5660-1

### Cone/gasification test matrix and specimen details
All specimen dimensions are reported as measured prior to the test (planform dimensions in mm; thickness in mm). “After burn thickness” is the remaining thickness after the test.

The reported **initial mass** is the mass of the wood specimen measured separately **before the specimen was placed in the sample holder**. It therefore excludes the holder, thermocouples, and backing insulation.

For cone tests in air, **t_ign (s)** is the ignition time and **t_flameout (s)** is the flameout time, both measured from the start of data acquisition. Gasification tests under N₂ do not have ignition or flameout times; their total test duration is reported instead.

| File / test name | Heat flux (kW/m²) | Condition | Grain orientation | Heater temp (°C) | Initial mass (g) | Initial thickness (mm) | Planform (mm × mm) | t_ign (s) | t_flameout (s) | Test duration (min) | Final thickness (mm) | Notes |
|---|---:|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| Aalto_Wood_Cone_30kW_hor_parallel_R1.csv | 30 | cone (air) | parallel | 565 | 119.30 | 26.40 | 99.70 × 99.60 | 38 | 1854 |  | 21.27 |  |
| Aalto_Wood_Cone_30kW_hor_parallel_R2.csv | 30 | cone (air) | parallel | 565 | 87.28 | 26.12 | 100.14 × 99.17 | 54 | 1326 |  | 22.50 |  |
| Aalto_Wood_Cone_30kW_hor_parallel_R3.csv | 30 | cone (air) | parallel | 565 | 114.12 | 25.51 | 101.66 × 101.50 | 43 | 2156 |  | 19.69 |  |
| Aalto_Wood_Cone_45kW_hor_parallel_R1.csv | 45 | cone (air) | parallel | 650 | 112.80 | 26.23 | 99.44 × 99.82 | 13 | 1500 |  | 19.91 |  |
| Aalto_Wood_Cone_45kW_hor_parallel_R2.csv | 45 | cone (air) | parallel | 650 | 103.92 | 25.96 | 100.31 × 100.45 | 34 | 1320 |  | 21.09 |  |
| Aalto_Wood_Cone_45kW_hor_parallel_R3.csv | 45 | cone (air) | parallel | 650 | 116.38 | 25.92 | 101.64 × 101.32 | 18 | 1809 |  | 19.88 |  |
| Aalto_Wood_Cone_60kW_hor_parallel_R1.csv | 60 | cone (air) | parallel | 730 | 99.93 | 25.62 | 101.72 × 101.53 | 12 | 1492 |  | 18.40 |  |
| Aalto_Wood_Cone_60kW_hor_parallel_R2.csv | 60 | cone (air) | parallel | 730 | 103.23 | 26.01 | 100.15 × 100.21 | 16 | 1090 |  | 19.43 |  |
| Aalto_Wood_Cone_60kW_hor_parallel_R3.csv | 60 | cone (air) | parallel | 730 | 106.09 | 26.11 | 99.80 × 99.66 | 11 | 1231 |  | 18.54 |  |
| Aalto_Wood_Gasification_30kW_hor_parallel_R1.csv | 30 | gasification (N₂) | parallel | 565 | 123.80 | 25.52 | 101.42 × 101.98 |  |  | 50 | 16.19 |  |
| Aalto_Wood_Gasification_30kW_hor_parallel_R2.csv | 30 | gasification (N₂) | parallel | 555 | 107.23 | 25.62 | 101.90 × 101.55 |  |  | 45 | 18.10 |  |
| Aalto_Wood_Gasification_30kW_hor_parallel_R3.csv | 30 | gasification (N₂) | parallel | 555 | 125.32 | 26.68 | 99.36 × 99.60 |  |  | 50 | 18.26 |  |
| Aalto_Wood_Gasification_45kW_hor_parallel_R1.csv | 45 | gasification (N₂) | parallel | 640 | 96.04 | 26.19 | 99.34 × 99.36 |  |  | 30 | 19.20 |  |
| Aalto_Wood_Gasification_45kW_hor_parallel_R2.csv | 45 | gasification (N₂) | parallel | 640 | 111.65 | 25.52 | 101.38 × 101.99 |  |  | 31 | 19.59 |  |
| Aalto_Wood_Gasification_45kW_hor_parallel_R3.csv | 45 | gasification (N₂) | parallel | 640 | 86.34 | 26.24 | 100.69 × 98.11 |  |  | 25 | 17.96 |  |
| Aalto_Wood_Gasification_60kW_hor_parallel_R1.csv | 60 | gasification (N₂) | parallel | 715 | 106.24 | 25.39 | 102.13 × 101.66 |  |  | 27 | 18.85 |  |
| Aalto_Wood_Gasification_60kW_hor_parallel_R2.csv | 60 | gasification (N₂) | parallel | 715 | 109.49 | 25.61 | 101.26 × 101.96 |  |  | 27 | 17.94 |  |
| Aalto_Wood_Gasification_60kW_hor_parallel_R3.csv | 60 | gasification (N₂) | parallel | 715 | 108.98 | 25.59 | 101.57 × 101.68 |  |  | 27 | 18.32 |  |
| Aalto_Wood_Gasification_30kW_hor_perpendicular_R1.csv | 30 | gasification (N₂) | perpendicular | 555 | 106.86 | 25.59 | 102.13 × 101.35 |  |  | 46 | 17.80 |  |
| Aalto_Wood_Gasification_30kW_hor_perpendicular_R2.csv | 30 | gasification (N₂) | perpendicular | 555 | 91.64 | 25.56 | 101.58 × 101.82 |  |  | 40 | 17.71 |  |
| Aalto_Wood_Gasification_30kW_hor_perpendicular_R3.csv | 30 | gasification (N₂) | perpendicular | 555 | 127.45 | 25.56 | 101.30 × 101.85 |  |  | 47 | 17.70 |  |
| Aalto_Wood_Gasification_45kW_hor_perpendicular_R1.csv | 45 | gasification (N₂) | perpendicular | 640 | 142.32 | 25.73 | 101.56 × 101.99 |  |  | 35 | 17.09 | specimen split into two pieces |
| Aalto_Wood_Gasification_45kW_hor_perpendicular_R2.csv | 45 | gasification (N₂) | perpendicular | 640 | 93.35 | 25.66 | 101.56 × 101.42 |  |  | 35 | 18.40 |  |
| Aalto_Wood_Gasification_45kW_hor_perpendicular_R3.csv | 45 | gasification (N₂) | perpendicular | 640 | 131.75 | 25.45 | 101.09 × 102.54 |  |  | 36 | 18.36 |  |
| Aalto_Wood_Gasification_60kW_hor_perpendicular_R1.csv | 60 | gasification (N₂) | perpendicular | 715 | 130.04 | 25.54 | 101.72 × 101.66 |  |  | 27 | 17.89 |  |
| Aalto_Wood_Gasification_60kW_hor_perpendicular_R2.csv | 60 | gasification (N₂) | perpendicular | 715 | 111.27 | 25.43 | 101.27 × 101.15 |  |  | 27 | 17.72 |  |
| Aalto_Wood_Gasification_60kW_hor_perpendicular_R3.csv | 60 | gasification (N₂) | perpendicular | 715 | 152.51 | 25.63 | 101.43 × 101.92 |  |  | 30 | 19.54 |  |
