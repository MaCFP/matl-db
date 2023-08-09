# University of Wuppertal and Forschungszentrum Jülich (BUW-FZJ)
This work is a collaboration of members the University of Wuppertal and the Forschungszentrum Jülich, both in Germany.
Full data sets and scripts are hosted on Zenodo: http://doi.org/10.5281/zenodo.4565475
The here utilised  parameter estimation strategy is build on a two step inverse modelling process. In the first step the material decomposition (pyrolysis) is determined. The second step uses this information and the thermo-physical parameters are estimated. The general procedure is explained here https://arxiv.org/abs/2303.17446 (preprint).
The presented method here diverges from the one discussed in the article slightly. Here, less decompostion reactions are used. They also release either methane or carbon dioxide. This allows the effective heat of combustion of the released gas mixture to change over the duration of the simulation.



### Description of the Parameter Estimation Process
All simulations have been conducted with FDS (FDS6.7.9-0-gec52dee-HEAD).
The pyrolysis reaction kinetics and thermo-physical parameters were estimated using inverse modelling. The inverse modelling itself was managed with the optimisation framework PROPTI: https://github.com/FireDynamics/propti
It is important to note that the goal of the inverse modelling was to match the data series directly. This means, for the TGA the residual mass over sample temperature, for the DSC the heat flow over sample temperature and for the MCC the HRR over sample temperature were matched. No adjustments to the experiment data series have been conducted other than averaging. All micro-scale data series were used as targets simultaneously during the inverse modelling. The decomposition reactions are constructed from four parallel reactions. One pair covers the low temperature peak and the second pair covers the high temperature peak. For each peak, one reaction releases methane and the other carbon dioxide. This allows for a changing composition of the released gas mixture. It leads to an effective heat of combustion of the gas mixture, that can change during the course of the simulation with respect to  sample temperature. It further enables FDS to use mass loss rates from the solid phase directly, without the usual scaling.

For the thermo-physical parameters, the HRR of cone calorimeter experiments was used as inverse modelling target.

Specifically the following data sets were used as targets:
TGA: LCPP: 2.5 K/min, 5.0 K/min, 15.0 K/min, 20.0 K/min; NIST: 10.0 K/min
MCC: NIST: 60 K/min
DSC: FSRI: 10.0 K/min, 20.0 K/min
Cone: Aalto: 65 kW/m²



### Parameter Set Approach C
(Approaches A and B have been submitted to MaCFP-2 in 2021)
Parameter estimation of the reaction kinetics was performed in a simplified TGA simulation setup, see below. These parameters were then used in a second parameter estimation step where the thermo-physical parameters were determined. In this second step a simplified cone calorimeter simulation setup was used, see below.

| Name | Value | Unit |
|:--------:|:--------:|:--------:|
| Pre-exponential factor, material 1A | 4.89E+08 | 1/s |
| Activation energy, material 1A | 9.32E+04 | J/mol |
| Heat of reaction, material 1A | 6.99E+02 | kJ/kg |
| Reaction order, material 1A | 1 | - |
| Sample mass fraction, material 1A | 0.025 | - |
| Gaseous yield, material 1A | 0.99 | - |
| Released gaseous species, material 1A | Methane | - |
| Residue yield, material 1A | 0.01 | - |

| Pre-exponential factor, material 1B | 3.15E+04 | 1/s |
| Activation energy, material 1B | 5.53E+04 | J/mol |
| Heat of reaction, material 1B | 1.99E+03 | kJ/kg |
| Reaction order, material 1B | 1 | - |
| Sample mass fraction, material 1B | 0.975 | - |
| Gaseous yield, material 1A | 0.99 | - |
| Released gaseous species, material 1B | Carbon Dioxide | - |
| Residue yield, material 1A | 0.01 | - |


| Pre-exponential factor, material 2A | 1.95E+10 | 1/s |
| Activation energy, material 2A | 1.48E+05 | J/mol |
| Heat of reaction, material 2A | 5.29E+02 | kJ/kg |
| Reaction order, material 2A | 1 | - |
| Sample mass fraction, material 1A | 0.025 | - |
| Gaseous yield, material 1A | 0.99 | - |
| Released gaseous species, material 1A | Methane | - |
| Residue yield, material 1A | 0.01 | - |

| Pre-exponential factor, material 2B | 7.80E+13 | 1/s |
| Activation energy, material 2B | 1.97E+05 | J/mol |
| Heat of reaction, material 2B | 1.19E+03 | kJ/kg |
| Reaction order, material 2B | 1 | - |
| Sample mass fraction, material 2B | 0.975 | - |
| Gaseous yield, material 1A | 0.99 | - |
| Released gaseous species, material 2B | Carbon Dioxide | - |
| Residue yield, material 1A | 0.01 | - |


| Density, PMMA | 1201.7 | kg/m3 |
| Emissivity, PMMA | 0.921 | - |
| Thermal conductivity (50.0 deg. C), PMMA | 0.1493661235437337 | W/(m·K) |
| Thermal conductivity (150.0 deg. C), PMMA | 0.0788646039973429 | W/(m·K) |
| Thermal conductivity (300.0 deg. C), PMMA | 0.0478595810772007 | W/(m·K) |
| Thermal conductivity (420.0 deg. C), PMMA | 0.5738201705430981 | W/(m·K) |
| Specific heat capacity (100.0 deg. C), PMMA | 1.092193048203574 | kJ/(kg·K) |
| Specific heat capacity (200.0 deg. C), PMMA | 3.010803502504312 | kJ/(kg·K) |
| Specific heat capacity (300.0 deg. C), PMMA | 2.5064509858647384 | kJ/(kg·K) |
| Specific heat capacity (420.0 deg. C), PMMA | 2.9979447489898297 | kJ/(kg·K) |
| Density, residue | 1155.0 | kg/m3 |
| Emissivity, residue | 0.882 | - |
| Thermal conductivity, residue | 1.02E+00 | W/m/K |
| Specific heat capacity, residue | 3.13E+00 | kJ/(kg·K) |



### Simulation Conditions/Setup
The micro-scale setups (DSC, MCC and TGA) are very simplified simulations, using the TGA_ANALYSIS functionality in FDS.
The simplified cone calorimeter setup incorporates gas phase reactions, using a very coarse fluid grid. The size of the cube-shaped fluid cells is 3.33 cm. The heat flux from the cone heater is imprinted to the sample model directly as a boundary condition (EXTERNAL_FLUX). With the utilised cell size the sample surface can be covered by 3x3 fluid cells. The heat flux from the heater to the sample was determined in a high resolution cone calorimeter simulation that included a heater geometry. The heat flux received by the sample was recorded in the steady-state and mapped to the coarse resolution. Thus, the simplified simulation setup can be used without a heater geometry. Still, the inhomogeneous flux distribution over the sample surface is captured.  The mapping is beneficial, reducing the computational resources necessary during the inverse modelling process.
