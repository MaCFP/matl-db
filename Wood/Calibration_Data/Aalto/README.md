# Aalto – Wood dataset submission (STA: TGA/DSC)

## Overview
At Aalto University, thermogravimetric analysis (TGA) measurements were performed using a simultaneous thermal analyzer (STA). The instrument also provides DSC signals; however, DSC data are not presented here since they are **supplementary only** and were not collected using a separate dedicated DSC instrument. Therefore, DSC signals should **not** be used as primary calibration targets unless explicitly agreed.

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

## Test list
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

## Notes
- Moisture content prior to the ramp is uncertain because the stabilization hold acted as a drying step.
