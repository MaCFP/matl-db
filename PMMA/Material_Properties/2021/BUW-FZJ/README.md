# University of Wuppertal and Forschungszentrum Jülich (BUW-FZJ)
This work is a collaboration of members the University of Wuppertal and the Forschungszentrum Jülich, both in Germany.
Full data sets and scripts are hosted on Zenodo: http://doi.org/10.5281/zenodo.4565475



### Description of the Parameter Estimation Process
All simulations have been conducted with FDS (FDS6.7.5-797-gbcd82f862-master).
The pyrolysis reaction kinetics and thermo-physical parameters were estimated using inverse modelling. The inverse modelling itself was managed with the optimisation framework PROPTI: https://github.com/FireDynamics/propti
It is important to note that the goal of the inverse modelling was to match the data series directly. This means, for the TGA the residual mass over sample temperature and for the simplified cone calorimeter the mass loss rate were used. The experiment data series were used as provided.



### Parameter Set Approach A
Parameter estimation of the reaction kinetics was performed in a simplified TGA simulation setup, see below. These parameters were then used in a second parameter estimation step where the thermo-physical parameters were determined. In this second step a simplified cone calorimeter simulation setup was used, see below.

| Name | Value | Unit |
|:--------:|:--------:|:--------:|
| Activation energy, material 1 | 64117.2 | J/mol |
| Pre-exponential factor, material 1 | 99996.5 | 1/s |
| Reaction order, material 1 | 1 | - |
| Stoichiometric coefficient, material 1 | 0.025 | - |
| Activation energy, material 2 | 162715 | J/mol |
| Pre-exponential factor, material 2 | 1.67093e+11 | 1/s |
| Reaction order, material 2 | 1 | - |
| Stoichiometric coefficient, material 2 | 0.975 | - |
| Density, PMMA | 1168.49 | kg/m3 |
| Emissivity, PMMA | 0.768990 | - |
| Heat of reaction, PMMA | 403.302 | kJ/kg |
| Thermal conductivity, PMMA | 0.116978 | m/K |
| Specific heat capacity, PMMA | 1.95652 | kJ/(kg·K) |
| Density, residue | 1085.97 | kg/m3 |
| Emissivity, residue | 0.407040 | - |
| Thermal conductivity, residue | 0.2629418 | m/K |
| Specific heat capacity, residue | 1.2149 | kJ/(kg·K) |



### Parameter Set Approach B
Parameter estimation of the reaction kinetics and the thermo-physical parameters was performed in a combined process. a simplified TGA simulation setup (see below) and a simplified cone calorimeter simulation setup (see below) were used in parallel to determine the full parameter set in on go.

| Name | Value | Unit |
|:--------:|:--------:|:--------:|
| Activation energy, material 1 | 610756.0 | J/mol |
| Pre-exponential factor, material 1 | 56864.9 | 1/s |
| Reaction order, material 1 | 1 | - |
| Stoichiometric coefficient, material 1 | 0.025 | - |
| Activation energy, material 2 | 180974.37 | J/mol |
| Pre-exponential Factor, material 2 | 6.71256e+12 | 1/s |
| Reaction order, material 2 | 1 | - |
| Stoichiometric coefficient, material 2 | 0.975 | - |
| Density, PMMA | 1207.84 | kg/m3 |
| Emissivity, PMMA | 0.989735 | - |
| Heat of reaction, PMMA | 787.891 | kJ/kg |
| Thermal conductivity, PMMA | 0.166161 | m/K |
| Specific heat capacity, PMMA | 2.20118 | kJ/(kg·K) |
| Density, residue | 842.116 | kg/m3 |
| Emissivity, residue | 0.988559 | - |
| Thermal conductivity, residue | 0.369026 | m/K |
| Specific heat capacity, residue | 1.29517 | kJ/(kg·K) |


### Simulation Conditions: TGA
TGA simulations were conducted in FDS (FDS6.7.5-797-gbcd82f862-master) and the build-in functionality 'TGA_ANALYSIS=.TRUE.' was used. The result of the normalised residual mass was multiplied by the requested sample mass of 5 mg.



###### Test Condition Summary

| Test Label | Heating Rate (K/min) | Initial Sample Mass (mg) | Description |
|:--------:|:--------:|:--------:|:--------:|
| BoWFZJ_TGA_10Kmin_1 | 10 | 5 | Approach A |
| BoWFZJ_TGA_100Kmin_1 | 100 | 5 | Approach A |
| BoWFZJ_TGA_10Kmin_2 | 10 | 5 | Approach B |
| BoWFZJ_TGA_100Kmin_2 | 100 | 5 | Approach B |



### Simulation Conditions: Gasification
Simplified Cone Calorimeter simulation setup in FDS. Domain is divided in cube-shaped cells with an edge length of 5 cm. The simulation was conducted without a gas phase, i.e. 'SOLID_PHASE_ONLY=.TRUE.'. Radiative heat flux was simulated with the 'EXTERNAL_FLUX' parameter. Front face temperature was averaged across a 1 mm thick layer, as requested. For the averaging three devices were utilised. Two devices with quantity 'INSIDE WALL TEMPERATURE' at depths of 0.5 mm and 1.0 mm, and the surface temperature ('WALL TEMPERATURE').


###### Test Condition Summary

| Test Label | Initial Sample Mass (g) | Residual Mass (g) | Sample Thickness (m) | Heat Flux (kW/m²) | Description |
|:------:|:------:|:------:|:------:|:------:|:------:|
| BoWFZJ_Gasification_10kW_6mm_1 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 10 | Approach A |
| BoWFZJ_Gasification_10kW_12mm_1 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 10 | Approach A |
| BoWFZJ_Gasification_25kW_6mm_1 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 25 | Approach A |
| BoWFZJ_Gasification_25kW_12mm_1 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 25 | Approach A |
| BoWFZJ_Gasification_65kW_6mm_1 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 65 | Approach A |
| BoWFZJ_Gasification_65kW_12mm_1 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 65 | Approach A |
| BoWFZJ_Gasification_10kW_6mm_2 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 10 | Approach B |
| BoWFZJ_Gasification_10kW_12mm_2 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 10 | Approach B |
| BoWFZJ_Gasification_25kW_6mm_2 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 25 | Approach B |
| BoWFZJ_Gasification_25kW_12mm_2 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 25 | Approach B |
| BoWFZJ_Gasification_65kW_6mm_2 | 70.99859900000003 | 0.07099860000000027 | 0.006 | 65 | Approach B |
| BoWFZJ_Gasification_65kW_12mm_2 | 141.99720000000005 | 0.14227930000000047 | 0.012 | 65 | Approach B |
