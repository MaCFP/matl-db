# Forschungszentrum Jülich (FZJ)

The data has been recorded in collaboration between the FZJ and the
Chair of Computational Civil Engineering (CCE) at the Bergische
Universität Wuppertal (BUW).

## Experimental Conditions: Microscale Combustion Calorimetry (MCC)

The sample powder was provided by MaCFP in a small glass bottle.
Upon arrival, the bottle was opened and placed inside a desiccator for storage.
The samples were kept inside the desiccator for more than four days before
any experiments were conducted. Before an experiment, the bottle was taken out
of the desiccator, on a laboratory scale the desired amount of sample material
was placed inside a crucible and the bottle placed back into the desiccator.
The experiment was conducted shortly after the crucible was filled.
Thus, the sample was subjected to the laboratory environment only for a few minutes.

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



## Experimental Conditions, Cone calorimeter

* Test Standard: ISO 5660
* Extraction flow rate: 24L/s
* Sample Surface Area: 0.01 m2 (nominal) 
* Sample holder dimensions:
    - Square pan: external dimensions: 105mmx105mmx25mm; internal dimensions: 100mmx100mmx 22.5mm 
    - Retainer frame: None
    - Retaining grid: None
* Backing Insulation: Al2O3 ceramic plate
* Sample preparation: Samples were stored at room temperature and humidity, prior to testing
Samples stored in a desiccator prior to testing:
              - FZJ_Wood_Cone_60kW_hor_parallel_R1, 20hrs
              - FZJ_Wood_Cone_60kW_hor_parallel_R2, 22hrs
              - FZJ_Wood_Cone_60kW_hor_parallel_R3, 45hrs
              - FZJ_Wood_Cone_60kW_hor_perpendicular_R1, 333hrs
              - FZJ_Wood_Cone_60kW_hor_perpendicular_R2, 33hrs
* Thermocouple location: None
Experiments with thermocouple type K, d=0.25mm, stapled to the bottom of the sample:
              - FZJ_Wood_Cone_60kW_hor_parallel_R1
              - FZJ_Wood_Cone_60kW_hor_parallel_R2
              - FZJ_Wood_Cone_60kW_hor_parallel_R3 
              - FZJ_Wood_Cone_60kW_hor_perpendicular_R1 
              - FZJ_Wood_Cone_60kW_hor_perpendicular_R2 

* Ignition Source: spark ignitor

###### Test Heating Conditions  
| Run Label | Initial Sample Mass (mg) | Surface area (cm^2) | Thickness (mm) |Time to ignition (s) | 
| :---- | :---- | :---- | :---- | :---- |
| FZJ_Wood_Cone_30kW_hor_parallel_R1 | 93.43 | 99.13 | 25.53 | 19 | 
| FZJ_Wood_Cone_30kW_hor_parallel_R2 | 93.93 | 101.51 | 25.24 | 35 | |
| FZJ_Wood_Cone_30kW_hor_parallel_R3 | 92.64 | 102.03 | 25.42 | 48 | 
| FZJ_Wood_Cone_30kW_hor_perpendicular_R1 | 96.13 | 98.30 | 26.00 | 43 | 
| FZJ_Wood_Cone_30kW_hor_perpendicular_R3 | 117.06 | 99.17 | 26.35 | 56 | 
| FZJ_Wood_Cone_30kW_hor_perpendicular_R4 | 118.47 | 97.74 | 26.11 | 55 | 
| FZJ_Wood_Cone_60kW_hor_parallel_R1 | 83.84 | 98.74 | 25.62 | 8 | 
| FZJ_Wood_Cone_60kW_hor_parallel_R2 | 124.60 | 99.23 | 25.36 | 6 | 
| FZJ_Wood_Cone_60kW_hor_parallel_R3 | 90.308 | 98.46 | 25.49 | 7 | 
| FZJ_Wood_Cone_60kW_hor_parallel_R4 | 88.27 | 102.00 | 25.53 | 10 | 
| FZJ_Wood_Cone_60kW_hor_perpendicular_R1 | 108.12 | 98.59 | 26.07 | 19 | 
| FZJ_Wood_Cone_60kW_hor_perpendicular_R2 | 82.70 | 97.31 | 25.96 | 11 | 
| FZJ_Wood_Cone_60kW_hor_perpendicular_R3 | 85.30 | 97.32 | 25.87 | 13 | 
| FZJ_Wood_Cone_60kW_hor_perpendicular_R4 | 85.19 | 97.24 | 26.05 | 12 | 
| FZJ_Wood_Cone_60kW_hor_perpendicular_R5 | 86.99 | 98.02 | 26.03 | 13 | 
| FZJ_Wood_Cone_75kW_hor_parallel_R1 | 96.43 | 98.17 | 25.44 | 5 | 
| FZJ_Wood_Cone_75kW_hor_parallel_R2 | 96.15 | 102.08 | 25.41 | 5 | 
| FZJ_Wood_Cone_75kW_hor_parallel_R3 | 92.78 | 99.36 | 25.45 | 5 | 
| FZJ_Wood_Cone_75kW_hor_perpendicular_R1 | 94.59 | 98.34 | 26.12 | 11 | 
| FZJ_Wood_Cone_75kW_hor_perpendicular_R2 | 95.22 | 97.65 | 26.10 | 9 | 
| FZJ_Wood_Cone_75kW_hor_perpendicular_R3 | 96.14 | 98.65 | 26.05 | 12 | 
| FZJ_Wood_Cone_75kW_hor_perpendicular_R4 | 94.03 | 98.55 | 26.08 | 9 | 



