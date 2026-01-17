# Forschungszentrum Jülich (FZJ)

The data has been recorded in collaboration between the FZJ and the
Chair of Computational Civil Engineering (CCE) at the Bergische
Universität Wuppertal (BUW).

## Experimental Conditions: Microscale Combustion Calorimetry (MCC)

Mass down-scaling runs have been performed at 60 K/min, to ensure that the experiments
were conducted under the appropriate conditions. From these runs it could
be determined that a sample mass between 2 mg to 4 mg is appropriate
for the setup (sample preparation, crucible, device, purge gas, ...).
It was observed that sample masses above 4 mg would start to compress in the
crucible under their own weight, while below 2 mg the measured signal started
to weaken. To enable a strong signal for the lower heating rates,
a sample mass of 4 mg was chosen for the main measurements.
For transparency, the mass down-scaling runs are provided with the submitted data.
**They are explicitly marked in the experiment summary table in the 'Purpose' column.
Be mindful which data sets you use for your assessment!**

The baseline of the HRR data was adjusted employing a linear fit. Data points
at the beginning and the end of each experiment were selected manually, for
intervals where the HRR vs. time is nearly constant. A linear fit was
performed through points in these intervals in the temperature vs. HRR space
and subtracted from the HRR.

The data was interpolated to match a 0.5 K spacing, as requested by MaCFP.
Note that this can lead to minor inconsistencies for a few initial data points
where the temperature is not yet monotonically increasing, due to noise.

### Experiment Overview
- Sample
    - Preparation: Powdered, as provided by MaCFP
    - Initial mass: 4.01 mg ± 0.05 mg
    - Final mass: 0.57 mg ± 0.04 mg
    - Notes: None
- Crucible
    - Type: Ceramic
    - Inner diameter: 4.80 mm
    - Inner height: 2.54 mm
    - Outer diameter: 6.30 mm
    - Outer height: 3.22 mm
    - Volume: 45.96 μL
    - Mass: 183.88 mg ± 1.43 mg
- Temperature program (Pyrolyzer)
    - Heating rates, nominal (K/min): 60.0, 45.0, 30.0
    - Initial temperature: 348.13 K ± 0.18 K
    - Initial isotherm: None
    - Final temperature: 911.76 K ± 44.66 K
    - Final isotherm: None
- Pyrolyser carrier gas
    - Type: N2
    - Flow rate: 80.0 cc/min
- Combustor
    - Temperature: 1173.15 K
- Combustor carrier gas
    - Type: O2
    - Flow rate: 20.0 cc/min
- Instrument
    - Type: DEATAK MCC
    - O2 Analyser: Chemical
    - Notes: None
- Calibration
    - Type: At the beginning of each day.

| Run Label | Initial Sample Mass (mg) | Final Sample Mass (mg) | Heating Rate (K/min) | Purpose |
| :---- | :---- | :---- | :---- | :---- |
| FZJ_Wood_MCC_N2_60K_R1 | 0.98 | 0.15 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R2 | 2.0 | 0.28 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R3 | 1.95 | 0.26 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R4 | 1.93 | 0.27 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R5 | 3.97 | 0.63 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R6 | 5.98 | 0.82 | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_60K_R7 | 5.96 | nan | 60 | mass down-scaling |
| FZJ_Wood_MCC_N2_30K_R1 | 4.0 | 0.64 | 30 | main measurement |
| FZJ_Wood_MCC_N2_30K_R2 | 4.01 | 0.54 | 30 | main measurement |
| FZJ_Wood_MCC_N2_45K_R1 | 4.07 | nan | 45 | main measurement |
| FZJ_Wood_MCC_N2_45K_R2 | 3.99 | 0.57 | 45 | main measurement |
| FZJ_Wood_MCC_N2_60K_R8 | 3.91 | nan | 60 | main measurement |
| FZJ_Wood_MCC_N2_60K_R9 | 3.99 | 0.55 | 60 | main measurement |
| FZJ_Wood_MCC_N2_60K_R10 | 4.09 | 0.54 | 60 | main measurement |

